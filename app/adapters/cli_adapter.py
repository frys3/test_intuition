class CLIAdapter:
    def __init__(self, alert_service):
        self.alert_service = alert_service

    def create_alert(self, symbol, condition, value, email):
        self.alert_service.create_alert(symbol, condition, value, email)

    def list_alerts(self):
        return self.alert_service.list_alerts()

    def delete_alert(self, index):
        self.alert_service.delete_alert(index)

    def modify_alert(self, index, symbol, condition, value, email):
        self.alert_service.modify_alert(index, symbol, condition, value, email)

    def check_alerts(self):
        self.alert_service.check_alerts()
