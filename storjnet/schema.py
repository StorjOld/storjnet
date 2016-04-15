import json
import hashlib
import jsonschema
from decimal import Decimal, InvalidOperation


SUBSCRIPTION_SCHEMA_FORMAT = {
    "$schema": "http://json-schema.org/schema#",

    "definitions": {

        "boolean": {
            "type": "object",
            "properties": {
                "type": {"enum": ["boolean"]},
            },
            "required": ["type"],
            "additionalProperties": False,
        },

        "number": {
            "type": "object",
            "properties": {
                "type": {"enum": ["number"]},
                "minimum": {"type": "number"},
                "maximum": {"type": "number"},
                "resolution": {"type": "integer", "minimum": 1},
            },
            "required": ["type", "minimum", "maximum", "resolution"],
            "additionalProperties": False,
        },

        "object": {
            "type": "object",
            "properties": {
                "type": {"enum": ["object"]},
            },
            "required": ["type"],
            "additionalProperties": False,
        },

        "enum": {
            "type": "object",
            "properties": {
                "type": {"enum": ["enum"]},
                "choices": {
                    "type": "array",
                    "minItems": 1,
                    "items": {
                        "oneOf": [
                            {"type": "boolean"},
                            {"type": "string"},
                            {"type": "number"},
                            {"type": "null"},
                        ]
                    }
                }
            },
            "required": ["type", "choices"],
            "additionalProperties": False,
        },
    },

    "type": "object",
    "properties": {

        "application": {"type": "string"},
        "title": {"type": "string"},
        "uuid": {"type": "string"},

        "indexes": {
            "type": "array",
            "minItems": 1,
            "items": {
                "type": "array",
                "minItems": 1,
                "items": {"type": "string"}
            }
        },

        "fields": {
            "type": "object",
            "minProperties": 1,
            "patternProperties": {
                ".*": {
                    "oneOf": [
                        {"$ref": "#/definitions/boolean"},
                        {"$ref": "#/definitions/number"},
                        {"$ref": "#/definitions/object"},
                        {"$ref": "#/definitions/enum"},
                    ]
                }
            }
        }

    },
    "required": ["application", "title", "uuid", "fields", "indexes"],
    "additionalProperties": False
}


def _num_denormalize(normal, minimum, maximum, resolution):
    frame_size = (maximum - minimum) / resolution
    return normal * frame_size + minimum


def _num_normalize(number, minimum, maximum, resolution):
    frame_size = (maximum - minimum) / resolution
    return int((number - minimum) / frame_size)


def validate_schema(schema):
    """ Validate schema

    Args:
        schema: The schema to validate.

    Raises:
        jsonschema.exceptions.ValidationError: If input is not valid.
    """
    jsonschema.validate(schema, SUBSCRIPTION_SCHEMA_FORMAT)
    for index in schema["indexes"]:
        for index_field in index:
            if index_field not in schema["fields"]:
                raise jsonschema.exceptions.ValidationError(
                    "Index field '{0}' not in fields!".format(index_field)
                )
    # FIXME check number min <= max


def _validate_subscription_boolean(key, value, description):
    if not isinstance(value, list):
        raise jsonschema.exceptions.ValidationError(
            "{0} value not a list.".format(key)
        )
    for choice in value:
        if not isinstance(choice, bool):
            raise jsonschema.exceptions.ValidationError(
                "{0} value {1} not a boolean.".format(key, value)
            )


def _validate_subscription_number(key, value, description):
    if not isinstance(value, list):
        raise jsonschema.exceptions.ValidationError(
            "{0} value not a list.".format(key)
        )
    if len(value) != 2:
        raise jsonschema.exceptions.ValidationError(
            "{0} value {1} does not have two entries.".format(key, value)
        )
    try:
        lower = Decimal(value[0])
        upper = Decimal(value[1])
    except InvalidOperation:
        raise jsonschema.exceptions.ValidationError(
            "{0} values {1} not numbers.".format(key, value)
        )
    minimum = Decimal(description["minimum"])
    maximum = Decimal(description["maximum"])
    if not (minimum <= lower <= upper < maximum):  # maximum is exclusive
        raise jsonschema.exceptions.ValidationError(
            "{0} values {1} not in limits: {2} <= {4} <= {5} < {3}.".format(
                key, value, minimum, maximum, lower, upper
            )
        )


def _validate_subscription_object(key, value, description):
    try:
        json.dumps(value)
    except TypeError:
        raise jsonschema.exceptions.ValidationError(
            "{0} value {1} not an object.".format(key, value)
        )


def _validate_subscription_enum(key, value, description):
    if not isinstance(value, list):
        raise jsonschema.exceptions.ValidationError(
            "{0} value not a list.".format(key)
        )
    choices = description["choices"]
    for choice in value:
        if choice not in choices:
            raise jsonschema.exceptions.ValidationError(
                "{0} value {1} not in valid choices {2}.".format(
                    key, value, choices
                )
            )


def _validate_subscription_field(schema, key, value):
    description = schema["fields"][key]
    if description["type"] == "boolean":
        _validate_subscription_boolean(key, value, description)
    elif description["type"] == "number":
        _validate_subscription_number(key, value, description)
    elif description["type"] == "object":
        _validate_subscription_object(key, value, description)
    elif description["type"] == "enum":
        _validate_subscription_enum(key, value, description)


def validate_subscription(schema, subscription, indexes=None):
    """ Validate subscription for given schema.

    Args:
        schema: Schema to which the subscription belongs.
        subscription: The subscription to validate.
        indexes: Limit to given list of indexes, otherwise all indexes.

    Raises:
        jsonschema.exceptions.ValidationError: If input is not valid.
    """
    validate_schema(schema)
    indexes = range(len(schema["indexes"])) if indexes is None else indexes
    _validate_indexes(schema, indexes)
    for index in indexes:
        for key in schema["indexes"][index]:
            try:
                value = subscription[key]
                _validate_subscription_field(schema, key, value)
            except KeyError:
                raise jsonschema.exceptions.ValidationError(
                    "Subscription missing required field {0}!".format(key)
                )


def _validate_required_fields(required_fields, event):
    if set(event.keys()) != required_fields:
        raise jsonschema.exceptions.ValidationError(
            "Event fields {0} != {1}".format(
                set(event.keys()), required_fields
            )
        )


def _validate_event_boolean(key, value, description):
    if not isinstance(value, bool):
        raise jsonschema.exceptions.ValidationError(
            "{0} value {1} not a boolean.".format(key, value)
        )


def _validate_event_object(key, value, description):
    try:
        json.dumps(value)
    except TypeError:
        raise jsonschema.exceptions.ValidationError(
            "{0} value {1} not an object.".format(key, value)
        )


def _validate_event_enum(key, value, description):
    if value not in description["choices"]:
        raise jsonschema.exceptions.ValidationError(
            "{0} value {1} not in allowed choices {2}".format(
                key, value, description["choices"]
            )
        )


def _validate_event_number(key, value, description):
    try:
        number = Decimal(value)
    except InvalidOperation:
        raise jsonschema.exceptions.ValidationError(
            "{0} value {1} not a number.".format(key, value)
        )
    minimum = Decimal(description["minimum"])
    maximum = Decimal(description["maximum"])
    if not (minimum <= number < maximum):  # maximum is exclusive
        raise jsonschema.exceptions.ValidationError(
            "{0} value {1} not in limits: {2} <= {1} < {3}.".format(
                key, value, minimum, maximum
            )
        )


def validate_event(schema, event):
    """ Validate event for given schema.

    Args:
        schema: Schema to which the event belongs.
        event: The event to validate.

    Raises:
        jsonschema.exceptions.ValidationError: If input is not valid.
    """
    validate_schema(schema)
    if not isinstance(event, dict):
        raise jsonschema.exceptions.ValidationError("Event must be a dict.")
    required_fields = set(schema["fields"].keys())
    _validate_required_fields(required_fields, event)
    for key in required_fields:
        description = schema["fields"][key]
        if description["type"] == "boolean":
            _validate_event_boolean(key, event[key], description)
        elif description["type"] == "number":
            _validate_event_number(key, event[key], description)
        elif description["type"] == "object":
            _validate_event_object(key, event[key], description)
        elif description["type"] == "enum":
            _validate_event_enum(key, event[key], description)


def schema_digests(schema, indexes=None):
    """Get all possible topic digests for given content schema.

    Args:
        schema: Content schema to get topic digests for.
        indexes: Limit to given list of indexes, otherwise all indexes.

    Returns:
        List of all possible topic digests.

    Raises:
        TypeError if index on object field (possible values cannot be deduced).
    """
    validate_schema(schema)
    indexes = range(len(schema["indexes"])) if indexes is None else indexes
    _validate_indexes(schema, indexes)
    raise NotImplementedError()  # TODO implement


def _validate_indexes(schema, indexes):
    if not isinstance(indexes, list):
        raise jsonschema.exceptions.ValidationError("Indexes must be a list.")
    maximum = len(schema["indexes"])
    for index in indexes:
        try:
            number = Decimal(index)
        except InvalidOperation:
            raise jsonschema.exceptions.ValidationError(
                "Index value {0} not a number.".format(index)
            )
        if not (0 <= number < maximum):
            raise jsonschema.exceptions.ValidationError(
                "Index value {0} not in limits: {1} <= {0} < {2}.".format(
                    number, 0, maximum
                )
            )


def _possible_number_values(minimum, maximum, resolution, lower, upper):
    lower_conversion = _num_normalize(lower, minimum, maximum, resolution)
    upper_conversion = _num_normalize(upper, minimum, maximum, resolution)
    normal_values = [lower_conversion, upper_conversion]
    normal_values.extend(range(lower_conversion + 1, upper_conversion))
    values = []
    for normal in sorted(normal_values):
        values.append(_num_denormalize(normal, minimum, maximum, resolution))
    return list(set(values))


def _possible_subscription_values(schema, subscription, index):
    possible_values = {}
    for key in schema["indexes"][index]:
        description = schema["fields"][key]
        if description["type"] == "boolean":
            possible_values[key] = subscription[key]
        if description["type"] == "enum":
            possible_values[key] = subscription[key]
        elif description["type"] == "object":
            possible_values[key] = [subscription[key]]
        elif description["type"] == "number":
            possible_values[key] = _possible_number_values(
                Decimal(description["minimum"]),
                Decimal(description["maximum"]),
                Decimal(description["resolution"]),
                Decimal(subscription[key][0]),
                Decimal(subscription[key][1])
            )
    return possible_values


def _subscription_index_digests(schema, subscription, index):
    possible_values = _possible_subscription_values(schema, subscription,
                                                    index)
    print possible_values
    digests = []
    # TODO get digests
    return digests


def subscription_digests(schema, subscription, indexes=None):
    """Get topic digests for a given schema subscription.

    Args:
        schema: Schema the given subscription belongs to.
        subscription: Subscription to get digests of.
        indexes: Limit to given list of indexes, otherwise all indexes.

    Returns:
        List of the topic digests.
    """
    validate_subscription(schema, subscription, indexes=indexes)
    indexes = range(len(schema["indexes"])) if indexes is None else indexes
    digests = []
    for index in indexes:
        digests.extend(_subscription_index_digests(schema, subscription,
                                                   index))
    return list(set(digests))


def event_digests(schema, event, indexes=None):
    """Get topic digests for a given schema event.

    Args:
        schema: Schema the given event belongs to.
        event: Event to get digests of.
        indexes: Limit to given list of indexes, otherwise all indexes.

    Returns:
        List of the topic digests.
    """
    validate_event(schema, event)
    indexes = range(len(schema["indexes"])) if indexes is None else indexes
    _validate_indexes(schema, indexes)
    return list(set(map(lambda i: _index_digest(schema, event, i), indexes)))


def _index_digest(schema, event, index):
    data = {"fields": {}}
    for header in ["application", "title", "uuid"]:
        data[header] = schema[header]
    for key in schema["indexes"][index]:
        if schema["fields"][key]["type"] == "number":
            minimum = Decimal(schema["fields"][key]["minimum"])
            maximum = Decimal(schema["fields"][key]["maximum"])
            resolution = Decimal(schema["fields"][key]["resolution"])
            number = Decimal(event[key])
            data["fields"][key] = _num_normalize(number, minimum,
                                                 maximum, resolution)
        else:
            data["fields"][key] = event[key]
    json_data = json.dumps(data, sort_keys=True)
    h = hashlib.sha256()
    h.update(json_data)
    return h.hexdigest()


EXAMPLE_SCHEMA = {
    "application": "Test Application",
    "title": "Test Schema",
    "uuid": "test",  # FIXME make more strict
    "fields": {
        "sell": {"type": "boolean"},
        "price": {
            "type": "number",
            "minimum": 0.0,
            "maximum": 100.0,
            "resolution": 8
        },
        "amount": {
            "type": "number",
            "minimum": 1.0,
            "maximum": 100.0,
            "resolution": 4
        },
        "metadata": {"type": "object"},
        "category": {
            "type": "enum",
            "choices": [None, 1, 3.14, "example"]
        },
    },
    "indexes": [
        ["sell", "price"],
        ["sell", "price", "amount", "category"],
    ]
}


EXAMPLE_SUBSCRIPTION_NARROW = {
    "sell": [True],  # list of choices
    "price": [0.0, 10.0],  # range subscription
}


EXAMPLE_SUBSCRIPTION_BROAD = {
    "sell": [True, False],  # list of choices
    "price": [1.0, 99.0],  # range subscription
    "amount": [1.0, 99.0],  # range subscription
    "category": [None, "example"],  # list of choies
}


EXAMPLE_EVENT = {
    "sell": True,
    "price": 2.99,
    "amount": 5,
    "metadata": {"some": "object"},
    "category": None
}


if __name__ == "__main__":
    validate_schema(EXAMPLE_SCHEMA)
    print event_digests(EXAMPLE_SCHEMA, EXAMPLE_EVENT)
    print subscription_digests(EXAMPLE_SCHEMA, EXAMPLE_SUBSCRIPTION_BROAD)
    print subscription_digests(
        EXAMPLE_SCHEMA, EXAMPLE_SUBSCRIPTION_NARROW, indexes=[0]
    )
