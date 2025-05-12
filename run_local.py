##########
# Import #
##############################################################################

from datetime import datetime, timezone
import os
import logging

import pandas as pd

from trading_simulator.port import BinancePort
from trading_simulator.main import simulate_future_trading
from utilities.logger import get_logger

###########
# Statics #
##############################################################################

now = datetime.now(tz=timezone.utc)

logger = get_logger(logger_name=os.path.basename(__file__), level=logging.DEBUG)

raw_data = {
    "open": [100, 110, 105, 95, 99, 100, 101, 105, 100],
    "position": ["LONG", "SHORT", "SHORT", "SHORT", "LONG", "LONG", "SHORT", "LONG", "LONG"],
    "open_time": [
        now.replace(hour=0, minute=0, second=0),
        now.replace(hour=0, minute=15, second=0),
        now.replace(hour=0, minute=30, second=0),
        now.replace(hour=0, minute=45, second=0),
        now.replace(hour=1, minute=0, second=0),
        now.replace(hour=1, minute=15, second=0),
        now.replace(hour=1, minute=30, second=0),
        now.replace(hour=1, minute=45, second=0),
        now.replace(hour=2, minute=0, second=0),
    ]
}


#############
# Functions #
##############################################################################

def main() -> None:
    raw = pd.DataFrame(raw_data)
    port = BinancePort(logger=logger, leverage=10)
    simulate_future_trading(
        raw_df=raw, 
        port=port,
        logger=logger,
    )

#######
# Run #
##############################################################################

if __name__ == "__main__":
    main()