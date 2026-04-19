import pandas as pd
from src.config import MASTER_DIR, TRANSACTION_DIR, OPERATIONAL_DIR, ANALYTICAL_DIR

def load_all_data():
    data = {
        # master
        "products": pd.read_csv(
            MASTER_DIR / "products.csv",
            low_memory=False
        ),
        "customers": pd.read_csv(
            MASTER_DIR / "customers.csv",
            parse_dates=["signup_date"],
            low_memory=False
        ),
        "promotions": pd.read_csv(
            MASTER_DIR / "promotions.csv",
            parse_dates=["start_date", "end_date"],
            low_memory=False
        ),
        "geography": pd.read_csv(
            MASTER_DIR / "geography.csv",
            low_memory=False
        ),

        # transaction
        "orders": pd.read_csv(
            TRANSACTION_DIR / "orders.csv",
            parse_dates=["order_date"],
            low_memory=False
        ),
        "order_items": pd.read_csv(
            TRANSACTION_DIR / "order_items.csv",
            low_memory=False
        ),
        "payments": pd.read_csv(
            TRANSACTION_DIR / "payments.csv",
            low_memory=False
        ),
        "shipments": pd.read_csv(
            TRANSACTION_DIR / "shipments.csv",
            parse_dates=["ship_date", "delivery_date"],
            low_memory=False
        ),
        "returns": pd.read_csv(
            TRANSACTION_DIR / "returns.csv",
            parse_dates=["return_date"],
            low_memory=False
        ),
        "reviews": pd.read_csv(
            TRANSACTION_DIR / "reviews.csv",
            parse_dates=["review_date"],
            low_memory=False
        ),

        # operational
        "inventory": pd.read_csv(
            OPERATIONAL_DIR / "inventory.csv",
            parse_dates=["snapshot_date"],
            low_memory=False
        ),
        "web_traffic": pd.read_csv(
            OPERATIONAL_DIR / "web_traffic.csv",
            parse_dates=["date"],
            low_memory=False
        ),

        # analytical
        "sales": pd.read_csv(
            ANALYTICAL_DIR / "sales.csv",
            parse_dates=["Date"],
            low_memory=False
        ),
        "sample_submission": pd.read_csv(
            ANALYTICAL_DIR / "sample_submission.csv",
            parse_dates=["Date"],
            low_memory=False
        ),
    }
    return data