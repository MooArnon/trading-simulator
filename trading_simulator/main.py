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
) -> None:
    logger.debug(f"position:\n{raw_df}")
    
    for idx, value in raw_df.iterrows():
        value = value.to_dict() 
        
        logger.debug(f"port.position: {port.position}")

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

def __get_position(
        df: pd.DataFrame,
        price_column: str = 'open',
        time_column: str = 'open_time'
) -> pd.DataFrame:
    
    df = df.sort_values(time_column)
    
    # Compute price difference from previous row
    df['price_diff'] = df[price_column].diff().shift(-1)

    # Generate position based on price_diff
    df['position'] = df['price_diff'].apply(
        lambda x: 'LONG' if x > 0 else ('SHORT' if x < 0 else 'HODL')
    )

    return df[[price_column, time_column, 'price_diff', 'position']]

##############################################################################
