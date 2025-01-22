class Alert:
    def __init__(self, symbol, condition, value, email):
        self.symbol = symbol
        self.condition = condition
        self.value = value
        self.email = email

    def to_dict(self):
        return {
            "symbol": self.symbol,
            "condition": self.condition,
            "value": self.value,
            "email": self.email
        }
