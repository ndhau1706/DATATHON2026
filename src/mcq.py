from pathlib import Path

import pandas as pd

from src.config import FINAL_REPORT_DIR
from src.data_loader import load_all_data
from src.data_prep import build_sales_fact


TEXT_OPTIONS = {
    "Q2": {
        "A": "Premium",
        "B": "Performance",
        "C": "Activewear",
        "D": "Standard",
    },
    "Q3": {
        "A": "defective",
        "B": "wrong_size",
        "C": "changed_mind",
        "D": "not_as_described",
    },
    "Q4": {
        "A": "organic_search",
        "B": "paid_search",
        "C": "email_campaign",
        "D": "social_media",
    },
    "Q6": {
        "A": "55+",
        "B": "25–34",
        "C": "35–44",
        "D": "45–54",
    },
    "Q7": {
        "A": "West",
        "B": "Central",
        "C": "East",
        "D": "Cả ba vùng có doanh thu xấp xỉ bằng nhau",
    },
    "Q8": {
        "A": "credit_card",
        "B": "cod",
        "C": "paypal",
        "D": "bank_transfer",
    },
    "Q9": {
        "A": "S",
        "B": "M",
        "C": "L",
        "D": "XL",
    },
    "Q10": {
        "A": "1 kỳ (trả một lần)",
        "B": "3 kỳ",
        "C": "6 kỳ",
        "D": "12 kỳ",
    },
}

NUMERIC_OPTIONS = {
    "Q1": {
        "A": 30,
        "B": 90,
        "C": 180,
        "D": 365,
    },
    "Q5": {
        "A": 0.12,
        "B": 0.25,
        "C": 0.39,
        "D": 0.54,
    },
}


def _pick_exact_option(question: str, value: str) -> tuple[str, str]:
    options = TEXT_OPTIONS[question]
    for opt, text in options.items():
        if text == value:
            return opt, text
    raise ValueError(f"Khong map duoc {question} voi value={value}")


def _pick_closest_numeric_option(question: str, value: float) -> tuple[str, str]:
    options = NUMERIC_OPTIONS[question]
    best_opt = min(options, key=lambda k: abs(options[k] - value))
    return best_opt, str(options[best_opt])


def _pick_q7_option(region_revenue: pd.Series, equal_tol: float = 0.03) -> tuple[str, str]:
    # Neu doanh thu 3 vung gan nhu bang nhau thi chon D
    spread_ratio = (region_revenue.max() - region_revenue.min()) / region_revenue.mean()
    if spread_ratio <= equal_tol:
        return "D", TEXT_OPTIONS["Q7"]["D"]

    top_region = region_revenue.idxmax()
    return _pick_exact_option("Q7", top_region)


def solve_mcq(data: dict) -> pd.DataFrame:
    products = data["products"].copy()
    customers = data["customers"].copy()
    orders = data["orders"].copy()
    order_items = data["order_items"].copy()
    payments = data["payments"].copy()
    returns = data["returns"].copy()
    web_traffic = data["web_traffic"].copy()

    answers = []

    # Q1
    q1 = orders.sort_values(["customer_id", "order_date", "order_id"]).copy()
    q1["prev_order_date"] = q1.groupby("customer_id")["order_date"].shift()
    q1["inter_order_gap_days"] = (q1["order_date"] - q1["prev_order_date"]).dt.days
    q1_value = float(q1["inter_order_gap_days"].dropna().median())
    q1_opt, q1_text = _pick_closest_numeric_option("Q1", q1_value)
    answers.append(["Q1", q1_value, "days", q1_opt, q1_text])

    # Q2
    q2 = (
        ((products["price"] - products["cogs"]) / products["price"])
        .groupby(products["segment"])
        .mean()
        .sort_values(ascending=False)
    )
    q2_value = float(q2.iloc[0])
    q2_choice = q2.idxmax()
    q2_opt, q2_text = _pick_exact_option("Q2", q2_choice)
    answers.append(["Q2", q2_value, "gross_margin_ratio", q2_opt, q2_text])

    # Q3
    q3 = (
        returns.merge(products[["product_id", "category"]], on="product_id", how="left")
        .query("category == 'Streetwear'")["return_reason"]
        .value_counts()
    )
    q3_value = int(q3.iloc[0])
    q3_choice = q3.idxmax()
    q3_opt, q3_text = _pick_exact_option("Q3", q3_choice)
    answers.append(["Q3", q3_value, "records", q3_opt, q3_text])

    # Q4
    q4 = web_traffic.groupby("traffic_source")["bounce_rate"].mean().sort_values()
    q4_value = float(q4.iloc[0])
    q4_choice = q4.idxmin()
    q4_opt, q4_text = _pick_exact_option("Q4", q4_choice)
    answers.append(["Q4", q4_value, "mean_bounce_rate", q4_opt, q4_text])

    # Q5
    q5_value = float(order_items["promo_id"].notna().mean())
    q5_opt, q5_text = _pick_closest_numeric_option("Q5", q5_value)
    answers.append(["Q5", q5_value, "promo_share", q5_opt, q5_text])

    # Q6
    customer_order_cnt = orders.groupby("customer_id").size().rename("order_cnt")
    q6 = customers[["customer_id", "age_group"]].merge(
        customer_order_cnt, on="customer_id", how="left"
    )
    q6["order_cnt"] = q6["order_cnt"].fillna(0)
    q6 = q6[q6["age_group"].notna()].groupby("age_group").agg(
        total_orders=("order_cnt", "sum"),
        total_customers=("customer_id", "nunique"),
    )
    q6["avg_orders_per_customer"] = q6["total_orders"] / q6["total_customers"]
    q6 = q6.sort_values("avg_orders_per_customer", ascending=False)
    q6_value = float(q6.iloc[0]["avg_orders_per_customer"])
    q6_choice = q6.index[0]
    q6_opt, q6_text = _pick_exact_option("Q6", q6_choice)
    answers.append(["Q6", q6_value, "avg_orders_per_customer", q6_opt, q6_text])

    # Q7
    sales_fact = build_sales_fact(data)
    q7 = sales_fact.groupby("region")["line_revenue"].sum().sort_values(ascending=False)
    q7_value = float(q7.iloc[0])
    q7_opt, q7_text = _pick_q7_option(q7)
    answers.append(["Q7", q7_value, "top_region_revenue", q7_opt, q7_text])

    # Q8
    q8 = orders.loc[orders["order_status"] == "cancelled", "payment_method"].value_counts()
    q8_value = int(q8.iloc[0])
    q8_choice = q8.idxmax()
    q8_opt, q8_text = _pick_exact_option("Q8", q8_choice)
    answers.append(["Q8", q8_value, "orders", q8_opt, q8_text])

    # Q9
    q9_num = (
        returns.merge(products[["product_id", "size"]], on="product_id", how="left")
        .groupby("size")
        .size()
    )
    q9_den = (
        order_items.merge(products[["product_id", "size"]], on="product_id", how="left")
        .groupby("size")
        .size()
    )
    q9 = (q9_num / q9_den).sort_values(ascending=False)
    q9_value = float(q9.iloc[0])
    q9_choice = q9.index[0]
    q9_opt, q9_text = _pick_exact_option("Q9", q9_choice)
    answers.append(["Q9", q9_value, "return_record_rate", q9_opt, q9_text])

    # Q10
    q10 = payments.groupby("installments")["payment_value"].mean().sort_values(ascending=False)
    q10_value = float(q10.iloc[0])
    q10_installments = int(q10.index[0])

    install_map = {
        1: "1 kỳ (trả một lần)",
        3: "3 kỳ",
        6: "6 kỳ",
        12: "12 kỳ",
    }
    q10_choice = install_map[q10_installments]
    q10_opt, q10_text = _pick_exact_option("Q10", q10_choice)
    answers.append(["Q10", q10_value, "avg_payment_value", q10_opt, q10_text])

    result = pd.DataFrame(
        answers,
        columns=[
            "question",
            "metric_value",
            "metric_unit",
            "answer_option",
            "answer_text",
        ],
    )
    return result


def export_mcq_answers(output_path: Path | None = None) -> Path:
    data = load_all_data()
    result = solve_mcq(data)

    output_path = FINAL_REPORT_DIR / "mcq_answers.csv" if output_path is None else Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    result.to_csv(output_path, index=False)
    return output_path


if __name__ == "__main__":
    out = export_mcq_answers()
    print(f"Saved MCQ answers to: {out}")