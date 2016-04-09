import jsonschema


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


def validate_subscription(subscription_schema, subscription):
    raise NotImplementedError()  # TODO implement


def validate_event(subscription_schema, event):
    raise NotImplementedError()  # TODO implement


def schema_digests(subscription_schema):
    raise NotImplementedError()  # TODO implement


def subscription_digests(subscription_schema, subscription):
    raise NotImplementedError()  # TODO implement


def event_digests(subscription_schema, event):
    raise NotImplementedError()  # TODO implement


if __name__ == "__main__":
    validate_subscription_schema(EXAMPLE_SUBSCRIPTION_SCHEMA)
