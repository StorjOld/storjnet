import six
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

        "string": {
            "type": "object",
            "properties": {
                "type": {"enum": ["string"]},
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
                        {"$ref": "#/definitions/string"},
                        {"$ref": "#/definitions/enum"},
                    ]
                }
            }
        }

    },
    "required": ["application", "title", "uuid", "fields", "indexes"],
    "additionalProperties": False
}


EXAMPLE_SUBSCRIPTION_SCHEMA = {
    "application": "Test Application",
    "title": "Test Schema",
    "uuid": "test",
    "fields": {
        "foo": {"type": "boolean"},
        "bar": {
            "type": "number",
            "minimum": -1.2,
            "maximum": 3.1337,
            "resolution": 128
        },
        "baz": {"type": "string"},
        "bam": {
            "type": "enum",
            "choices": [None, 1, 3.14, "example"]
        },
    },
    "indexes": [
        ["foo", "bar"],
        ["foo"]
    ]
}


EXAMPLE_EVENT = {
    "foo": True,
    "bar": 2.1,
    "baz": "something",
    "bam": None
}


def validate_subscription_schema(subscription_schema):
    """ Validate subscription schema.

    Raises: jsonschema.exceptions.ValidationError: If schema is not valid.
    """
    jsonschema.validate(subscription_schema, SUBSCRIPTION_SCHEMA_FORMAT)
    for index in subscription_schema["indexes"]:
        for index_field in index:
            if index_field not in subscription_schema["fields"]:
                raise jsonschema.exceptions.ValidationError(
                    "Index field '{0}' not in fields!".format(index_field)
                )
    # TODO check number min <= max


def validate_subscription(subscription_schema, subscription):
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


def _validate_string(key, value, description):
    if not isinstance(value, six.string_types):
        raise jsonschema.exceptions.ValidationError(
            "{0} value {1} not a string.".format(key, value)
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
    if not (minimum <= number <= maximum):
        raise jsonschema.exceptions.ValidationError(
            "{0} value {1} not in limits {2} {3}.".format(minimum, maximum)
        )


def validate_event(subscription_schema, event):
    """Validate event is for a given subscription schema."""
    validate_subscription_schema(subscription_schema)
    if not isinstance(event, dict):
        raise jsonschema.exceptions.ValidationError("Event must be a dict.")
    required_fields = set(subscription_schema["fields"].keys())
    _validate_required_fields(required_fields, event)
    for key in required_fields:
        description = subscription_schema["fields"][key]
        if description["type"] == "boolean":
            _validate_boolean(key, event[key], description)
        elif description["type"] == "number":
            _validate_number(key, event[key], description)
        elif description["type"] == "string":
            _validate_string(key, event[key], description)
        elif description["type"] == "enum":
            _validate_enum(key, event[key], description)


def schema_digests(subscription_schema):
    raise NotImplementedError()  # TODO implement


def subscription_digests(subscription_schema, subscription):
    raise NotImplementedError()  # TODO implement


def event_digests(subscription_schema, event):
    """Returns the topic digest for a given event."""
    schema = subscription_schema
    validate_event(schema, event)
    indexes = [schema["fields"].keys()]
    indexes.extend(schema["indexes"])
    return set(map(lambda idx: index_digest(schema, event, idx), indexes))


def index_digest(subscription_schema, event, index):
    data = {"fields": {}}
    for header in ["application", "title", "uuid"]:
        data[header] = subscription_schema[header]
    for field in index:
        data["fields"][field] = event[field]
        # TODO number conversion
    h = hashlib.sha256()
    h.update(json.dumps(data, sort_keys=True))
    return h.hexdigest()


if __name__ == "__main__":
    validate_subscription_schema(EXAMPLE_SUBSCRIPTION_SCHEMA)
    print event_digests(EXAMPLE_SUBSCRIPTION_SCHEMA, EXAMPLE_EVENT)
