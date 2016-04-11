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
            "items": {
                "type": "array",
                "minItems": 1,
                "items": {
                    "type": "string"
                }
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


EXAMPLE_SCHEMA = {
    "application": "Test Application",
    "title": "Test Schema",
    "uuid": "test",
    "fields": {
        "foo": {"type": "boolean"},
        "bar": {
            "type": "number",
            "minimum": -1.0,
            "maximum": 3.0,
            "resolution": 4
        },
        "baz": {"type": "object"},
        "bam": {
            "type": "enum",
            "choices": [None, 1, 3.14, "example"]
        },
    },
    "indexes": [
        ["foo", "bar", "bam"],
        ["foo", "bar"]
    ]
}


EXAMPLE_EVENT = {
    "foo": True,
    "bar": 2.99,
    "baz": {"some": "object"},
    "bam": None
}


def _number_to_resolution_index(number, minimum, maximum, resolution):
    frame_size = (maximum - minimum) / resolution
    return int((number - minimum) / frame_size)


def validate_schema(schema):
    """ Validate subscription schema.

    Raises: jsonschema.exceptions.ValidationError: If schema is not valid.
    """
    jsonschema.validate(schema, SUBSCRIPTION_SCHEMA_FORMAT)
    for index in schema["indexes"]:
        for index_field in index:
            if index_field not in schema["fields"]:
                raise jsonschema.exceptions.ValidationError(
                    "Index field '{0}' not in fields!".format(index_field)
                )
    # TODO check number min <= max


def validate_subscription(schema, subscription):
    raise NotImplementedError()  # TODO implement


def _validate_required_fields(required_fields, event):
    if set(event.keys()) != required_fields:
        raise jsonschema.exceptions.ValidationError(
            "Event fields {0} != {1}".format(
                set(event.keys()), required_fields
            )
        )


def _validate_boolean(key, value, description):
    if not isinstance(value, bool):
        raise jsonschema.exceptions.ValidationError(
            "{0} value {1} not a boolean.".format(key, value)
        )


def _validate_object(key, value, description):
    try:
        json.dumps(value)
    except TypeError:
        raise jsonschema.exceptions.ValidationError(
            "{0} value {1} not an object.".format(key, value)
        )


def _validate_enum(key, value, description):
    if value not in description["choices"]:
        raise jsonschema.exceptions.ValidationError(
            "{0} value {1} not in allowed choices {2}".format(
                key, value, description["choices"]
            )
        )


def _validate_number(key, value, description):
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
    """Validate event is for a given subscription schema."""
    validate_schema(schema)
    if not isinstance(event, dict):
        raise jsonschema.exceptions.ValidationError("Event must be a dict.")
    required_fields = set(schema["fields"].keys())
    _validate_required_fields(required_fields, event)
    for key in required_fields:
        description = schema["fields"][key]
        if description["type"] == "boolean":
            _validate_boolean(key, event[key], description)
        elif description["type"] == "number":
            _validate_number(key, event[key], description)
        elif description["type"] == "object":
            _validate_object(key, event[key], description)
        elif description["type"] == "enum":
            _validate_enum(key, event[key], description)


def schema_digests(schema):
    raise NotImplementedError()  # TODO implement


def subscription_digests(schema, subscription):
    raise NotImplementedError()  # TODO implement


def event_digests(schema, event):
    """Returns the topic digest for a given event."""
    validate_event(schema, event)
    indexes = schema["indexes"]
    return list(set(map(lambda idx: index_digest(schema, event, idx), indexes)))


def index_digest(schema, event, index):
    data = {"fields": {}}
    for header in ["application", "title", "uuid"]:
        data[header] = schema[header]
    for field in index:
        if schema["fields"][field]["type"] == "number":
            minimum = schema["fields"][field]["minimum"]
            maximum = schema["fields"][field]["maximum"]
            resolution = schema["fields"][field]["resolution"]
            data["fields"][field] = _number_to_resolution_index(
                Decimal(event[field]), Decimal(minimum),
                Decimal(maximum), Decimal(resolution)
            )
        else:
            data["fields"][field] = event[field]
    json_data = json.dumps(data, sort_keys=True)
    h = hashlib.sha256()
    h.update(json_data)
    return h.hexdigest()


if __name__ == "__main__":
    validate_schema(EXAMPLE_SCHEMA)
    print event_digests(EXAMPLE_SCHEMA, EXAMPLE_EVENT)
