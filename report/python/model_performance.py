##########
# Import #
##############################################################################

import matplotlib.pyplot as plt

from space_time_report.__base import BaseReport
from datetime import datetime, timezone, timedelta

##############################################################################

def mtd_accuracy() -> dict:
    current_date = datetime.now(tz=timezone.utc)
    target_date = (current_date - timedelta(days=1)).strftime("%Y-%m") + "-*"

    base_report = BaseReport()

    data = base_report.query_data(
        sql_file="report/sql/mtd_accuracy.sql",
        additional_filter={
            "PREDICTION_TABLE": "historical_prediction",
            "RAW_TABLE": "historical_binance_future",
            "ASSET": "btc",
            "TICKER": "BTCUSDT",
            "PREDICTED_DATE": target_date,
        },
    )

    return data.to_dict(as_series=False)

##############################################################################

def actual_prediction_history() -> dict:
    current_date = datetime.now(tz=timezone.utc)
    target_date = (current_date - timedelta(days=1)).strftime("%Y-%m") + "-*"

    base_report = BaseReport()

    data = base_report.query_data(
        sql_file="report/sql/actual_prediction_history.sql",
        additional_filter={
            "PREDICTION_TABLE": "historical_prediction",
            "RAW_TABLE": "historical_binance_future",
            "ASSET": "btc",
            "TICKER": "BTCUSDT",
            "PREDICTED_DATE": target_date,
        },
    )

    return data.to_pandas()

##############################################################################
