import requests

class CoinAPIAdapter:
    def __init__(self, api_key):
        self.api_key = api_key
        self.base_url = "https://rest.coinapi.io/v1"

    def get_price(self, symbol):
        response = requests.get(f"{self.base_url}/exchangerate/{symbol}/USD", 
                                headers={"X-CoinAPI-Key": self.api_key})
        if response.status_code == 200:
            return response.json().get("rate")
        else:
            response.raise_for_status()
