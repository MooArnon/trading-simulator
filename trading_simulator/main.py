##########
# Import #
##############################################################################

import pandas as pd
from logging import Logger

from .port import BasePort

##########
# Flows #
##############################################################################

def simulate_future_trading(
        raw_df: pd.DataFrame,
        port: BasePort,
        logger: Logger,
        price_column: str = 'open',
        stop_loss: int = 0.05,
) -> None:
    logger.debug(f"position:\n{raw_df}")
    
    for idx, value in raw_df.iterrows():
        value = value.to_dict() 
        
        logger.debug(f"port.position: {port.position}")
        
        roi = port.calculate_roi(value[price_column])
        logger.info(f"ROI: {roi}")
        
        # if 

        if value['position'] != port.position:
            port.open_position(position=value['position'], price=value[price_column])
        
        else:
            logger.info(f"Remain position: {port.position}")
        print("="*64)
        
    port.close_position(price=value[price_column])
    logger.info(f"Final port value is {port.current_value}")

#############
# Utilities #
##############################################################################

##############################################################################
