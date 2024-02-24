import requests
import json
from config import allow_values, token

class APIException(Exception):
    pass
class ConvertValue:
    @staticmethod
    def get_price(base, quote, amount):
        res = requests.get(f"https://api.freecurrencyapi.com/v1/latest/?apikey=fca_live_oDovnNMclkxFCHC4hjfuVo8EplV9Sk217tgXRqyN&base_currency={allow_values[base]}&currencies={allow_values[quote]}")
        data_json = json.loads(res.content)["data"][allow_values[quote]]
        return data_json * amount