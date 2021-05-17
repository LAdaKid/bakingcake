"""
    Store general crypto api interations in this module.
"""
from pycoingecko import CoinGeckoAPI

# Initialize
CG_API = CoinGeckoAPI()
# Get the coin list
COIN_LIST = CG_API.get_coins_list()

def get_token_info(ticker):
    """
        Get the information provided a token's ticker.

        Args:
            ticker (str): ticker symbol as a string

        Return:
            ticker information
    """
    success = False
    token_info = {}
    token_list = [i for i in COIN_LIST if ticker.lower() == i["symbol"]]
    if token_list:
        success = True
        if len(token_list) == 1:
            token_info = token_list[0]
        else:
            i = 0
            while True:
                token_info = token_list[i]
                if (
                    "governance" not in token_info["id"] and
                    "-" in token_info["id"]
                ):
                    i += 1
                else:
                    break

    return token_info, success
