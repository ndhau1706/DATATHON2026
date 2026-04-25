from pathlib import Path

import pandas as pd

from src.config import ANALYTICAL_DIR, CLEANED_DATA_DIR, MASTER_DIR, OPERATIONAL_DIR, TRANSACTION_DIR
from src.cleaning import DATE_COLUMNS


CSV_PATHS = {
    "products": MASTER_DIR / "products.csv",
    "customers": MASTER_DIR / "customers.csv",
    "promotions": MASTER_DIR / "promotions.csv",
    "geography": MASTER_DIR / "geography.csv",
    "orders": TRANSACTION_DIR / "orders.csv",
    "order_items": TRANSACTION_DIR / "order_items.csv",
    "payments": TRANSACTION_DIR / "payments.csv",
    "shipments": TRANSACTION_DIR / "shipments.csv",
    "returns": TRANSACTION_DIR / "returns.csv",
    "reviews": TRANSACTION_DIR / "reviews.csv",
    "inventory": OPERATIONAL_DIR / "inventory.csv",
    "web_traffic": OPERATIONAL_DIR / "web_traffic.csv",
    "sales": ANALYTICAL_DIR / "sales.csv",
    "sample_submission": ANALYTICAL_DIR / "sample_submission.csv",
}


def _read_csv_map(csv_paths: dict[str, Path], keep_default_na: bool = True) -> dict[str, pd.DataFrame]:
    return {
        table_name: pd.read_csv(
            path,
            parse_dates=DATE_COLUMNS.get(table_name, []),
            low_memory=False,
            keep_default_na=keep_default_na,
        )
        for table_name, path in csv_paths.items()
    }


def load_all_data(clean: bool = False) -> dict[str, pd.DataFrame]:
    data = _read_csv_map(CSV_PATHS)
    if clean:
        from src.cleaning import clean_dataframes

        data, _ = clean_dataframes(data)
    return data


def load_clean_data() -> dict[str, pd.DataFrame]:
    csv_paths = {table_name: CLEANED_DATA_DIR / f"{table_name}.csv" for table_name in CSV_PATHS}

    missing_files = [str(path) for path in csv_paths.values() if not path.exists()]
    if missing_files:
        raise FileNotFoundError(
            "Chua tim thay cleaned data. Hay chay `python -m src.cleaning` truoc. "
            f"Missing: {missing_files[:3]}"
        )

    return _read_csv_map(csv_paths, keep_default_na=False)
