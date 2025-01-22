class AlertService:
    def __init__(self, alerts, price_provider, notifier):
        self.alerts = alerts
        self.price_provider = price_provider
        self.notifier = notifier

    def create_alert(self, symbol, condition, value, email):
        self.alerts.append({
            "symbol": symbol,
            "condition": condition,
            "value": value,
            "email": email
        })

    def list_alerts(self):
        return self.alerts

    def delete_alert(self, index):
        if 0 <= index < len(self.alerts):
            self.alerts.pop(index)

    def modify_alert(self, index, symbol, condition, value, email):
        if 0 <= index < len(self.alerts):
            self.alerts[index] = {
                "symbol": symbol,
                "condition": condition,
                "value": value,
                "email": email
            }

    def check_alerts(self):
        for alert in self.alerts:
            price = self.price_provider.get_price(alert["symbol"])
            if (alert["condition"] == "below" and price < alert["value"]) or \
               (alert["condition"] == "above" and price > alert["value"]):
                self.notifier.send_notification(
                    alert["email"],
                    f"Alert triggered for {alert['symbol']}",
                    f"The price of {alert['symbol']} is now {price} USD.")
