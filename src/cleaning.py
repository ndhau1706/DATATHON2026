from __future__ import annotations

from pathlib import Path
from typing import Any

import pandas as pd

from src.config import CLEANED_DATA_DIR, REPORTS_DIR


DATE_COLUMNS: dict[str, list[str]] = {
    "customers": ["signup_date"],
    "promotions": ["start_date", "end_date"],
    "orders": ["order_date"],
    "shipments": ["ship_date", "delivery_date"],
    "returns": ["return_date"],
    "reviews": ["review_date"],
    "inventory": ["snapshot_date"],
    "web_traffic": ["date"],
    "sales": ["Date"],
    "sample_submission": ["Date"],
}

DROP_COLUMNS: dict[str, list[str]] = {
    "order_items": ["promo_id_2"],
}

FILL_VALUES: dict[str, dict[str, Any]] = {
    "order_items": {"promo_id": "None"},
    "promotions": {"applicable_category": "None"},
}


def coerce_datetime_columns(df: pd.DataFrame, columns: list[str]) -> tuple[pd.DataFrame, dict[str, int]]:
    result = df.copy()
    parse_failures: dict[str, int] = {}

    for col in columns:
        if col not in result.columns:
            continue
        raw = result[col]
        parsed = pd.to_datetime(raw, errors="coerce")
        parse_failures[col] = int(parsed.isna().sum() - raw.isna().sum())
        result[col] = parsed

    return result, parse_failures


def clean_table(table_name: str, df: pd.DataFrame) -> tuple[pd.DataFrame, list[dict[str, Any]]]:
    cleaned = df.copy()
    actions: list[dict[str, Any]] = []

    date_cols = DATE_COLUMNS.get(table_name, [])
    if date_cols:
        cleaned, parse_failures = coerce_datetime_columns(cleaned, date_cols)
        for col in date_cols:
            if col in cleaned.columns:
                actions.append(
                    {
                        "table": table_name,
                        "column": col,
                        "action": "convert_to_datetime",
                        "affected_count": len(cleaned),
                        "details": f"parse_failures={parse_failures.get(col, 0)}",
                    }
                )

    fill_map = FILL_VALUES.get(table_name, {})
    for col, fill_value in fill_map.items():
        if col in cleaned.columns:
            missing_before = int(cleaned[col].isna().sum())
            cleaned[col] = cleaned[col].fillna(fill_value)
            actions.append(
                {
                    "table": table_name,
                    "column": col,
                    "action": "fill_missing",
                    "affected_count": missing_before,
                    "details": f"fill_value={fill_value}",
                }
            )

    for col in DROP_COLUMNS.get(table_name, []):
        if col in cleaned.columns:
            cleaned = cleaned.drop(columns=[col])
            actions.append(
                {
                    "table": table_name,
                    "column": col,
                    "action": "drop_column",
                    "affected_count": len(df),
                    "details": "dropped as requested",
                }
            )

    return cleaned, actions


def clean_dataframes(data: dict[str, pd.DataFrame]) -> tuple[dict[str, pd.DataFrame], pd.DataFrame]:
    cleaned_data: dict[str, pd.DataFrame] = {}
    action_rows: list[dict[str, Any]] = []

    for table_name, df in data.items():
        cleaned_df, actions = clean_table(table_name, df)
        cleaned_data[table_name] = cleaned_df
        action_rows.extend(actions)

    action_summary = pd.DataFrame(action_rows)
    if not action_summary.empty:
        action_summary = action_summary[
            ["table", "column", "action", "affected_count", "details"]
        ].sort_values(["table", "action", "column"]).reset_index(drop=True)

    return cleaned_data, action_summary


def save_clean_data(cleaned_data: dict[str, pd.DataFrame], output_dir: Path | None = None) -> Path:
    output_dir = CLEANED_DATA_DIR if output_dir is None else Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    for table_name, df in cleaned_data.items():
        df.to_csv(output_dir / f"{table_name}.csv", index=False)

    return output_dir


def build_cleaning_overview(
    raw_data: dict[str, pd.DataFrame],
    cleaned_data: dict[str, pd.DataFrame],
) -> pd.DataFrame:
    rows: list[dict[str, Any]] = []

    for table_name in raw_data:
        raw_df = raw_data[table_name]
        clean_df = cleaned_data[table_name]

        rows.append(
            {
                "table": table_name,
                "raw_rows": int(raw_df.shape[0]),
                "raw_cols": int(raw_df.shape[1]),
                "clean_rows": int(clean_df.shape[0]),
                "clean_cols": int(clean_df.shape[1]),
                "raw_missing_cells": int(raw_df.isna().sum().sum()),
                "clean_missing_cells": int(clean_df.isna().sum().sum()),
            }
        )

    return pd.DataFrame(rows).sort_values("table").reset_index(drop=True)


def export_clean_data() -> dict[str, Path]:
    from src.data_loader import load_all_data

    raw_data = load_all_data(clean=False)
    cleaned_data, action_summary = clean_dataframes(raw_data)

    cleaned_dir = save_clean_data(cleaned_data)

    report_dir = REPORTS_DIR / "data_audit"
    report_dir.mkdir(parents=True, exist_ok=True)

    overview = build_cleaning_overview(raw_data, cleaned_data)
    overview_path = report_dir / "cleaning_overview.csv"
    actions_path = report_dir / "cleaning_actions.csv"

    overview.to_csv(overview_path, index=False)
    action_summary.to_csv(actions_path, index=False)

    return {
        "cleaned_dir": cleaned_dir,
        "overview_path": overview_path,
        "actions_path": actions_path,
    }


if __name__ == "__main__":
    outputs = export_clean_data()
    for name, path in outputs.items():
        print(f"{name}: {path}")
