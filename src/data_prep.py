import pandas as pd


def add_line_metrics(order_items: pd.DataFrame, products: pd.DataFrame) -> pd.DataFrame:
    """Them cac metric doanh thu, discount, COGS o muc line item."""
    enriched = order_items.merge(
        products[
            [
                "product_id",
                "product_name",
                "category",
                "segment",
                "size",
                "color",
                "price",
                "cogs",
            ]
        ],
        on="product_id",
        how="left",
    )

    enriched["discount_amount"] = enriched["discount_amount"].fillna(0)
    enriched["gross_revenue"] = enriched["quantity"] * enriched["unit_price"]
    enriched["line_revenue"] = enriched["gross_revenue"]
    enriched["net_revenue_after_discount"] = (
        enriched["gross_revenue"] - enriched["discount_amount"]
    )
    enriched["line_cogs"] = enriched["quantity"] * enriched["cogs"]
    enriched["gross_margin_sales_target"] = (
        enriched["gross_revenue"] - enriched["line_cogs"]
    )
    enriched["gross_profit_after_discount"] = (
        enriched["net_revenue_after_discount"] - enriched["line_cogs"]
    )
    enriched["gross_margin"] = enriched["gross_margin_sales_target"]

    return enriched


def build_sales_fact(data: dict) -> pd.DataFrame:
    """View line-level cho doanh thu va EDA tong quan."""
    line_items = add_line_metrics(data["order_items"], data["products"])

    sales_fact = (
        line_items
        .merge(
            data["orders"][[
                "order_id", "order_date", "customer_id", "zip", "order_status",
                "payment_method", "device_type", "order_source"
            ]],
            on="order_id",
            how="left",
        )
        .merge(
            data["customers"][[
                "customer_id", "city", "signup_date", "gender", "age_group", "acquisition_channel"
            ]],
            on="customer_id",
            how="left",
            suffixes=("", "_customer"),
        )
        .merge(
            data["geography"][["zip", "region", "district"]],
            on="zip",
            how="left",
        )
        .merge(
            data["payments"][["order_id", "payment_value", "installments"]],
            on="order_id",
            how="left",
        )
    )
    return sales_fact


def build_daily_target_from_transactions(data: dict) -> pd.DataFrame:
    """Tai tao sales.csv tu transaction. Khong loc theo order_status."""
    sales_fact = build_sales_fact(data)
    daily = (
        sales_fact.groupby("order_date", as_index=False)
        .agg(Revenue=("line_revenue", "sum"), COGS=("line_cogs", "sum"))
        .rename(columns={"order_date": "Date"})
        .sort_values("Date")
        .reset_index(drop=True)
    )
    return daily


def validate_daily_target(data: dict) -> pd.DataFrame:
    """So sanh daily target tai tao voi sales.csv."""
    reconstructed = build_daily_target_from_transactions(data)
    compare = data["sales"].merge(reconstructed, on="Date", suffixes=("_sales", "_reconstructed"), how="left")
    compare["Revenue_abs_diff"] = (compare["Revenue_sales"] - compare["Revenue_reconstructed"]).abs()
    compare["COGS_abs_diff"] = (compare["COGS_sales"] - compare["COGS_reconstructed"]).abs()
    return compare


def aggregate_returns(data: dict) -> pd.DataFrame:
    """Gom returns ve muc order-product de de merge phan tich."""
    return (
        data["returns"]
        .groupby(["order_id", "product_id"], as_index=False)
        .agg(
            return_record_count=("return_id", "count"),
            return_quantity=("return_quantity", "sum"),
            refund_amount=("refund_amount", "sum"),
            last_return_date=("return_date", "max"),
        )
    )


def aggregate_reviews(data: dict) -> pd.DataFrame:
    """Gom reviews ve muc order-product."""
    return (
        data["reviews"]
        .groupby(["order_id", "product_id"], as_index=False)
        .agg(
            review_count=("review_id", "count"),
            avg_rating=("rating", "mean"),
            last_review_date=("review_date", "max"),
        )
    )


def build_post_purchase_fact(data: dict) -> pd.DataFrame:
    """View phuc vu shipment / return / review. Loai cancelled."""
    sales_fact = build_sales_fact(data)
    returns_agg = aggregate_returns(data)
    reviews_agg = aggregate_reviews(data)

    post_purchase = (
        sales_fact[sales_fact["order_status"] != "cancelled"]
        .merge(data["shipments"], on="order_id", how="left")
        .merge(returns_agg, on=["order_id", "product_id"], how="left")
        .merge(reviews_agg, on=["order_id", "product_id"], how="left")
    )
    return post_purchase


def build_order_status_revenue_summary(data: dict) -> pd.DataFrame:
    """Tom tat revenue va cogs theo order_status."""
    sales_fact = build_sales_fact(data)
    summary = (
        sales_fact.groupby("order_status", as_index=False)
        .agg(
            order_count=("order_id", pd.Series.nunique),
            item_lines=("order_id", "size"),
            revenue=("line_revenue", "sum"),
            cogs=("line_cogs", "sum"),
        )
        .sort_values("revenue", ascending=False)
        .reset_index(drop=True)
    )
    summary["revenue_pct"] = summary["revenue"] / summary["revenue"].sum()
    summary["cogs_pct"] = summary["cogs"] / summary["cogs"].sum()
    return summary
