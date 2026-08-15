from pathlib import Path
import pandas as pd


def compare_quarters(file_path, target_quarter, comparison_quarter):

    file_path = Path(file_path)

    if not file_path.exists():
        raise FileNotFoundError(f"Dataset not found: {file_path}")

    df = pd.read_csv(file_path)

    df["order_date"] = pd.to_datetime(df["order_date"])
    df["quarter"] = df["order_date"].dt.quarter

    target = df[df["quarter"] == target_quarter]
    comparison = df[df["quarter"] == comparison_quarter]

    if target.empty:
        raise ValueError(
            f"No data found for quarter {target_quarter}"
        )

    if comparison.empty:
        raise ValueError(
            f"No data found for quarter {comparison_quarter}"
        )

    def percentage_change(target_value, comparison_value):

        if comparison_value == 0:
            return 0

        return (
            (target_value - comparison_value)
            / comparison_value
        ) * 100

    target_revenue = target["revenue"].sum()
    comparison_revenue = comparison["revenue"].sum()

    target_profit = target["profit"].sum()
    comparison_profit = comparison["profit"].sum()

    target_quantity = target["quantity"].sum()
    comparison_quantity = comparison["quantity"].sum()

    target_price = target["unit_price"].mean()
    comparison_price = comparison["unit_price"].mean()

    target_discount = target["discount"].mean()
    comparison_discount = comparison["discount"].mean()

    overall = {
        "revenue_target": target_revenue,
        "revenue_comparison": comparison_revenue,
        "revenue_change_percent": percentage_change(
            target_revenue,
            comparison_revenue
        ),
        "profit_target": target_profit,
        "profit_comparison": comparison_profit,
        "profit_change_percent": percentage_change(
            target_profit,
            comparison_profit
        ),
        "quantity_change_percent": percentage_change(
            target_quantity,
            comparison_quantity
        ),
        "average_price_change_percent": percentage_change(
            target_price,
            comparison_price
        ),
        "average_discount_change_percent": percentage_change(
            target_discount,
            comparison_discount
        )
    }

    target_region = (
        target.groupby("region")["revenue"]
        .sum()
    )

    comparison_region = (
        comparison.groupby("region")["revenue"]
        .sum()
    )

    regional = pd.DataFrame({
        "target_revenue": target_region,
        "comparison_revenue": comparison_region
    }).fillna(0)

    regional["change"] = (
        regional["target_revenue"]
        - regional["comparison_revenue"]
    )

    regional["change_percent"] = (
        (
            regional["target_revenue"]
            - regional["comparison_revenue"]
        )
        / regional["comparison_revenue"].replace(0, pd.NA)
    ) * 100

    regional = regional.sort_values(
        "change"
    )

    target_product = (
        target.groupby("product")["revenue"]
        .sum()
    )

    comparison_product = (
        comparison.groupby("product")["revenue"]
        .sum()
    )

    product = pd.DataFrame({
        "target_revenue": target_product,
        "comparison_revenue": comparison_product
    }).fillna(0)

    product["change"] = (
        product["target_revenue"]
        - product["comparison_revenue"]
    )

    product["change_percent"] = (
        (
            product["target_revenue"]
            - product["comparison_revenue"]
        )
        / product["comparison_revenue"].replace(0, pd.NA)
    ) * 100

    product = product.sort_values("change")

    target_category = (
        target.groupby("category")["revenue"]
        .sum()
    )

    comparison_category = (
        comparison.groupby("category")["revenue"]
        .sum()
    )

    category = pd.DataFrame({
        "target_revenue": target_category,
        "comparison_revenue": comparison_category
    }).fillna(0)

    category["change"] = (
        category["target_revenue"]
        - category["comparison_revenue"]
    )

    category["change_percent"] = (
        (
            category["target_revenue"]
            - category["comparison_revenue"]
        )
        / category["comparison_revenue"].replace(0, pd.NA)
    ) * 100

    category = category.sort_values("change")

    target_segment = (
        target.groupby("customer_segment")["revenue"]
        .sum()
    )

    comparison_segment = (
        comparison.groupby("customer_segment")["revenue"]
        .sum()
    )

    segment = pd.DataFrame({
        "target_revenue": target_segment,
        "comparison_revenue": comparison_segment
    }).fillna(0)

    segment["change"] = (
        segment["target_revenue"]
        - segment["comparison_revenue"]
    )

    segment["change_percent"] = (
        (
            segment["target_revenue"]
            - segment["comparison_revenue"]
        )
        / segment["comparison_revenue"].replace(0, pd.NA)
    ) * 100

    segment = segment.sort_values("change")

    return {
        "target_quarter": target_quarter,
        "comparison_quarter": comparison_quarter,
        "overall": overall,
        "regional": regional,
        "product": product,
        "category": category,
        "segment": segment
    }


if __name__ == "__main__":

    project_root = Path(__file__).resolve().parents[2]

    dataset_path = (
        project_root
        / "data"
        / "processed"
        / "cleaned_sales_data.csv"
    )

    results = compare_quarters(
        dataset_path,
        target_quarter=3,
        comparison_quarter=2
    )

    overall = results["overall"]

    print("\n===== QUARTER COMPARISON =====")

    print(
        f"\nQ{results['target_quarter']} "
        f"vs Q{results['comparison_quarter']}"
    )

    print(
        f"\nRevenue change: "
        f"{overall['revenue_change_percent']:.2f}%"
    )

    print(
        f"Profit change: "
        f"{overall['profit_change_percent']:.2f}%"
    )

    print(
        f"Quantity change: "
        f"{overall['quantity_change_percent']:.2f}%"
    )

    print(
        f"Average price change: "
        f"{overall['average_price_change_percent']:.2f}%"
    )

    print(
        f"Average discount change: "
        f"{overall['average_discount_change_percent']:.2f}%"
    )

    print("\nRegional Changes:")
    print(results["regional"].round(2))

    print("\nProduct Changes:")
    print(results["product"].round(2))

    print("\nCategory Changes:")
    print(results["category"].round(2))

    print("\nCustomer Segment Changes:")
    print(results["segment"].round(2))