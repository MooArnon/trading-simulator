##########
# Import #
##############################################################################

import logging

#########
# Class #
##############################################################################

class BasePort:
    """
    Base portfolio class for simulating leveraged trading with maker and taker fees.

    Parameters
    ----------
    initial_value : float
        The initial capital of the portfolio.
    taker_fee : float
        Transaction fee rate when closing a position.
    maker_fee : float
        Transaction fee rate when opening a position.
    leverage : int, optional
        The leverage factor to apply when opening positions. Defaults to 1 (no leverage).

    Attributes
    ----------
    initial_value : float
        The initial portfolio value.
    current_value : float
        The current portfolio value after trades and fees.
    leverage : int
        Leverage factor used for trading.
    taker_fee : float
        Fee rate applied when closing a position.
    maker_fee : float
        Fee rate applied when opening a position.
    position : str or None
        Current open position ('LONG', 'SHORT', or None).
    entry_price : float or None
        The entry price at which the current position was opened.
    position_size : float
        Dollar size of the current open position (can be larger than current value due to leverage).
    """
    def __init__(
            self, 
            initial_value: float,
            taker_fee: float,
            maker_fee: float,
            logger: logging.Logger,
            leverage: int = None,
            buy_ratio: float = 0.8,
    ) -> None:
        self.current_value = initial_value
        self.leverage = leverage if leverage is not None else 1
        self.taker_fee = taker_fee
        self.maker_fee = maker_fee
        
        self.buy_ratio = buy_ratio
        
        self.logger = logger
        
        # dollar value of position
        self.set_position("HODL")
        self.set_position_size(0)
    
    ##############
    # Properties #
    ##########################################################################
    
    @property
    def position(self) -> str:
        return self.__position

    ##########################################################################
    
    def set_position(self, position: str) -> None:
        self.__position = position
        
    ##########################################################################
    
    @property
    def entry_price(self) -> float:
        return self.__entry_price
    
    ##########################################################################
    
    def set_entry_price(self, entry_price: str) -> None:
        self.__entry_price = entry_price
        
    ##########################################################################
    
    @property
    def position_size(self) -> str:
        return self.__position_size
    
    ##########################################################################

    def set_position_size(self, position_size: str) -> None:
        self.__position_size = position_size

    ##########################################################################
    
    def open_position(self, position: str, price: float) -> None:
        """
        Open a new trading position.

        Parameters
        ----------
        direction : str
            Direction of the position, either 'LONG' or 'SHORT'.
        price : float
            The price at which the position is opened.

        Raises
        ------
        Exception
            If there is already an open position.
        """
        if self.position != 'HODL':
            self.close_position(price)
        
        self.set_entry_price(price)
        self.set_position(position)
        
        buy_power = self.buy_ratio * self.current_value
        
        # Choose the worse fee as a safety factor
        notional_value = buy_power * self.leverage 
        fee = notional_value * self.taker_fee
        
        self.current_value -= fee
        
        # Buying power / price
        # position_size is how many asset unit (one asset) you get
        self.set_position_size(notional_value/price)
        
        self.logger.info(f"position changes from {self.position} to {position}")
        self.logger.info(f"Entered price: {self.entry_price}")
        self.logger.debug(f"Buy power: {buy_power}")
        self.logger.debug(f"notional_value: {notional_value}")
        self.logger.debug(f"fee: {fee}")
        self.logger.debug(f"current_value: {self.current_value}")
        
    ##########################################################################
    
    def close_position(self, price: float) -> None:
        """
        Close the current open trading position.

        Parameters
        ----------
        price : float
            The price at which the position is closed.

        Raises
        ------
        Exception
            If there is no open position to close.
        """
        if self.position is None:
            raise Exception("No open position to close.")
        
        if self.position == 'LONG':
            pnl = (price - self.entry_price) * self.position_size
        elif self.position == 'SHORT':
            pnl = (self.entry_price - price) * self.position_size
        elif self.position == 'HODL':
            return
        else:
            raise Exception("Invalid position type.")
        
        self.current_value += pnl
        
        fee = abs(self.position_size) * self.taker_fee * price
        self.current_value -= fee
        
        self.set_position(None)
        self.set_entry_price(None)
        self.set_position_size(0)
        
    ##########################################################################
    
    def get_port_value(self) -> float:
        """
        Get the current portfolio value.

        Returns
        -------
        float
            The current portfolio value after trades and fees.
        """
        return self.current_value

    ##########################################################################
    
    def reset(self) -> None:
        """
        Reset the portfolio to its initial state.

        Resets the current value to the initial value and clears any open position.
        """
        self.position = None
        self.entry_price = None
        self.position_size = 0
    
    ##########################################################################

##############################################################################
