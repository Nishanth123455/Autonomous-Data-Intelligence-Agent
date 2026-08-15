from pathlib import Path
import pandas as pd


def run_eda(file_path):

    file_path = Path(file_path)

    if not file_path.exists():
        raise FileNotFoundError(f"Dataset not found: {file_path}")

    df = pd.read_csv(file_path)

    df["order_date"] = pd.to_datetime(df["order_date"])

    df["month"] = df["order_date"].dt.month
    df["quarter"] = df["order_date"].dt.quarter

    total_revenue = df["revenue"].sum()
    total_profit = df["profit"].sum()
    average_order_value = df["revenue"].mean()
    total_orders = df["order_id"].nunique()

    revenue_by_region = (
        df.groupby("region")["revenue"]
        .sum()
        .sort_values(ascending=False)
    )

    revenue_by_product = (
        df.groupby("product")["revenue"]
        .sum()
        .sort_values(ascending=False)
    )

    revenue_by_category = (
        df.groupby("category")["revenue"]
        .sum()
        .sort_values(ascending=False)
    )

    revenue_by_segment = (
        df.groupby("customer_segment")["revenue"]
        .sum()
        .sort_values(ascending=False)
    )

    monthly_revenue = (
        df.groupby("month")["revenue"]
        .sum()
        .sort_index()
    )

    quarterly_revenue = (
        df.groupby("quarter")["revenue"]
        .sum()
        .sort_index()
    )

    quarterly_profit = (
        df.groupby("quarter")["profit"]
        .sum()
        .sort_index()
    )

    profit_margin = (
        total_profit / total_revenue
        if total_revenue != 0
        else 0
    )

    numerical_columns = [
        "quantity",
        "unit_price",
        "discount",
        "revenue",
        "cost",
        "profit"
    ]

    correlation_matrix = df[numerical_columns].corr()

    return {
        "total_revenue": total_revenue,
        "total_profit": total_profit,
        "average_order_value": average_order_value,
        "total_orders": total_orders,
        "profit_margin": profit_margin,
        "revenue_by_region": revenue_by_region,
        "revenue_by_product": revenue_by_product,
        "revenue_by_category": revenue_by_category,
        "revenue_by_segment": revenue_by_segment,
        "monthly_revenue": monthly_revenue,
        "quarterly_revenue": quarterly_revenue,
        "quarterly_profit": quarterly_profit,
        "correlation_matrix": correlation_matrix
    }


if __name__ == "__main__":

    project_root = Path(__file__).resolve().parents[2]

    dataset_path = (
        project_root
        / "data"
        / "processed"
        / "cleaned_sales_data.csv"
    )

    results = run_eda(dataset_path)

    print("\n===== EDA RESULTS =====")

    print(
        f"\nTotal Revenue: "
        f"{results['total_revenue']:,.2f}"
    )

    print(
        f"Total Profit: "
        f"{results['total_profit']:,.2f}"
    )

    print(
        f"Average Order Value: "
        f"{results['average_order_value']:,.2f}"
    )

    print(
        f"Total Orders: "
        f"{results['total_orders']}"
    )

    print(
        f"Profit Margin: "
        f"{results['profit_margin']:.2%}"
    )

    print("\nRevenue by Region:")
    print(results["revenue_by_region"])

    print("\nRevenue by Product:")
    print(results["revenue_by_product"])

    print("\nRevenue by Category:")
    print(results["revenue_by_category"])

    print("\nRevenue by Customer Segment:")
    print(results["revenue_by_segment"])

    print("\nMonthly Revenue:")
    print(results["monthly_revenue"])

    print("\nQuarterly Revenue:")
    print(results["quarterly_revenue"])

    print("\nQuarterly Profit:")
    print(results["quarterly_profit"])

    print("\nCorrelation Matrix:")
    print(results["correlation_matrix"].round(3))