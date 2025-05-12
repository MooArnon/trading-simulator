##########
# Import #
##############################################################################

from .__base import BasePort

#########
# Class #
##############################################################################

class BinancePort(BasePort):
    """Port class for Binance

    Parameters
    ----------
    BasePort : BasePort
        Base port
    
    Attributes
    ----------
    initial_value : int, optional
        Initial value with unit USDT, by default 100
    taker_fee : float, optional
        Fee ratio for taker, by default 0.0005
    maker_fee : float, optional
        Fee ratio for maker, by default 0.0002
    leverage : int, optional
        Leverage when open position, by default None
    """
    def __init__(
            self, 
            logger,
            initial_value = 100, 
            taker_fee = 0.0005, 
            maker_fee = 0.0002, 
            leverage = None,
    ) -> None:
        super().__init__(
            initial_value=initial_value, 
            taker_fee=taker_fee, 
            maker_fee=maker_fee, 
            leverage=leverage,
            logger=logger
        )
    
    ##########################################################################

##############################################################################
