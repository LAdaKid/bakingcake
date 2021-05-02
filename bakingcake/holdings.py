from marshmallow import Schema, fields, post_load, validates, ValidationError
from . import utils, crypto


class HoldingSchema(Schema):
    """
        Schema for specifying the holding characteristics.
    """
    name = fields.String(required=True)
    ticker = fields.String(required=True)
    quantity = fields.Float(required=True)
    apr = fields.Float()
    apy = fields.Float()

    @post_load
    def create_holding(self, input_data, **kwargs):
        return Holding(**input_data)


class Holding(object):
    """
        This class will function as the base object class for a portfolio.
    """

    def __init__(self, name, ticker, quantity, apr=None, apy=None):
        """
            Holding constructor.
        """
        # Setup required args
        self.name = name
        self.ticker = ticker
        self.quantity = quantity
        # Setup annual percentage rate and yield
        if apr and not apy:
            apy = utils.calculate_apy(apr)
        elif apy and not apr:
            apr = utils.calculate_apr(apy)
        else:
            apr = 0.0
            apy = 0.0
        self.apr = apr
        self.apy = apy
        # TODO: Add list of different base currencies
        self.base_currency = "usd"
        # Ger holding info
        token_info, success = crypto.get_token_info(ticker)
        self.id = token_info["id"]
        # Calculate price
        self.price = crypto.CG_API.get_price(
            ids=self.id, vs_currencies=self.base_currency
        )[self.id][self.base_currency]
        # Calculate the holding total
        self.total = self.price * self.quantity
        # Calculate the annual yield
        self.annual_yield_usd = self.total * self.apy
        self.annual_yield_token = self.quantity * self.apy

        return
