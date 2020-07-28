import requests


def get_current_BTC_to_USD_price():
    response = requests.get("https://api.coindesk.com/v1/bpi/currentprice.json")
    return response.json()["bpi"]["USD"]["rate_float"]
