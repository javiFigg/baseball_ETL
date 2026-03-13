class DataValidator:
    def __init__(self, data):
        self.data = data

    def validate_required_columns(self, required_columns):
        if not required_columns:
            return True
        return all(column in self.data.columns for column in required_columns)

    def validate_not_empty(self):
        return len(self.data) > 0

    def validate_numeric_columns(self, numeric_columns):
        if not numeric_columns:
            return True

        for column in numeric_columns:
            if column not in self.data.columns:
                return False
            dtype_kind = getattr(self.data[column].dtype, "kind", None)
            if dtype_kind not in {"b", "i", "u", "f", "c"}:
                return False
        return True

    def run_all_checks(self, required_columns=None, numeric_columns=None):
        return (
            self.validate_required_columns(required_columns)
            and self.validate_not_empty()
            and self.validate_numeric_columns(numeric_columns)
        )

    def validate(self, required_columns=None, numeric_columns=None):
        return self.run_all_checks(required_columns, numeric_columns)