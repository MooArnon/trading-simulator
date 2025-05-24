import logging

class BasePort:
    """
    Base portfolio class for simulating leveraged trading with maker and taker fees.
    """
    def __init__(
        self,
        initial_value: float,
        taker_fee: float,
        maker_fee: float,
        logger: logging.Logger,
        leverage: int = 1,
        buy_ratio: float = 0.8,
    ) -> None:
        self.initial_value = initial_value
        self.current_value = initial_value
        self.leverage = leverage
        self.taker_fee = taker_fee
        self.maker_fee = maker_fee
        self.buy_ratio = buy_ratio
        self.logger = logger

        self.__position = "HODL"
        self.__entry_price = None
        self.__position_size = 0
        self.__capital_used = 0

    @property
    def position(self) -> str:
        return self.__position

    @property
    def entry_price(self) -> float:
        return self.__entry_price

    @property
    def position_size(self) -> float:
        return self.__position_size

    @property
    def capital_used(self) -> float:
        return self.__capital_used

    def set_position(self, position: str) -> None:
        self.__position = position

    def set_entry_price(self, price: float) -> None:
        self.__entry_price = price

    def set_position_size(self, size: float) -> None:
        self.__position_size = size

    def set_capital_used(self, capital: float) -> None:
        self.__capital_used = capital

    ##########################################################################
    
    def open_position(self, position: str, price: float) -> None:
        self.logger.info(f"Position changes from {self.position} to {position}")
        if self.position != "HODL":
            self.close_position(price)

        self.set_entry_price(price)
        self.set_position(position)

        buy_power = self.buy_ratio * self.current_value
        self.set_capital_used(buy_power)

        notional_value = buy_power * self.leverage
        fee = notional_value * self.maker_fee
        self.current_value -= fee

        self.set_position_size(notional_value / price)

        self.logger.info(f"Entered price: {self.entry_price}")
        self.logger.debug(f"Buy power: {buy_power}")
        self.logger.debug(f"Notional value: {notional_value}")
        self.logger.debug(f"Maker fee: {fee}")
        self.logger.debug(f"Current value after fee: {self.current_value}")

    ##########################################################################
    
    def close_position(self, price: float) -> None:
        if self.position == "HODL":
            raise Exception("No open position to close.")

        pnl = self.calculate_pnl(price)
        self.current_value += pnl

        fee = abs(self.position_size) * price * self.taker_fee
        self.current_value -= fee

        self.set_position("HODL")
        self.set_entry_price(None)
        self.set_position_size(0)
        self.set_capital_used(0)

        self.logger.debug(f"PnL: {pnl}")
        self.logger.debug(f"Taker fee: {fee}")
        self.logger.debug(f"Current value after closing: {self.current_value}")

    ##########################################################################
    
    def calculate_pnl(self, price: float) -> float:
        if self.position == "LONG":
            return (price - self.entry_price) * self.position_size
        elif self.position == "SHORT":
            return (self.entry_price - price) * self.position_size
        else:
            return 0

    def calculate_roi(self, price: float) -> float:
        if self.position == "HODL" or self.capital_used == 0:
            return 0

        pnl = self.calculate_pnl(price)
        return (pnl / self.capital_used) * 100

    def get_port_value(self) -> float:
        return self.current_value

    def reset(self) -> None:
        self.__position = "HODL"
        self.__entry_price = None
        self.__position_size = 0
        self.__capital_used = 0
        self.current_value = self.initial_value
