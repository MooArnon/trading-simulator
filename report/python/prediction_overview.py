##########
# Import #
##############################################################################

import matplotlib.pyplot as plt

from space_time_report.__base import BaseReport
from datetime import datetime, timezone, timedelta

##############################################################################

def monthly_balanced_prediction() -> None:
    current_date = datetime.now(tz=timezone.utc)
    target_date = (current_date - timedelta(days=1)).strftime("%Y-%m") + "-*"

    base_report = BaseReport()

    data = base_report.query_data(
        sql_file="report/sql/balanced_prediction.sql",
        additional_filter={
            "PREDICTION_TABLE": "historical_prediction",
            "ASSET": "btc",
            "PREDICTED_DATE": target_date,
        },
    )

    # Convert to dictionary if needed
    data_dict = {row["position"]: row["count"] for row in data.to_dicts()}
    long_count = data_dict.get("LONG", 0)
    short_count = data_dict.get("SHORT", 0)
    total = long_count + short_count if (long_count + short_count) > 0 else 1  # avoid division by zero

    # Plot
    plt.figure(figsize=(6, 4))
    plt.bar(["Position"], [long_count], label="LONG", color="green")
    plt.bar(["Position"], [short_count], bottom=[long_count], label="SHORT", color="red")
    plt.text(0, long_count / 2, f"{(long_count/total)*100:.1f}% LONG", ha='center', va='center', color='white', fontweight='bold')
    plt.text(0, long_count + short_count / 2, f"{(short_count/total)*100:.1f}% SHORT", ha='center', va='center', color='white', fontweight='bold')
    plt.title("Market Share by Position")
    plt.ylabel("Count")
    plt.legend()
    plt.tight_layout()

    # Save the figure
    output_path = "monthly_balanced_prediction.png"
    plt.savefig(output_path)
    plt.close()

##############################################################################
