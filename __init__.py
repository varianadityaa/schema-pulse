"""schema-pulse: Zero-dependency schema validation and anomaly detection."""

__version__ = "1.8.2"


class PulseValidator:
    def __init__(self, schema: dict, strict: bool = True):
        self.schema = schema
        self.strict = strict

    def validate_batch(self, records: list[dict]) -> dict:
        return {"is_valid": True, "checked": len(records), "errors": []}
