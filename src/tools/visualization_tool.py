from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt


def create_visualizations(file_path, output_dir):

    file_path = Path(file_path)
    output_dir = Path(output_dir)

    if not file_path.exists():
        raise FileNotFoundError(f"Dataset not found: {file_path}")

    output_dir.mkdir(parents=True, exist_ok=True)

    df = pd.read_csv(file_path)

    df["order_date"] = pd.to_datetime(df["order_date"])
    df["quarter"] = df["order_date"].dt.quarter
    df["month"] = df["order_date"].dt.month

    generated_files = []

    monthly_revenue = (
        df.groupby("month")["revenue"]
        .sum()
    )

    plt.figure(figsize=(10, 5))
    plt.plot(
        monthly_revenue.index,
        monthly_revenue.values,
        marker="o"
    )
    plt.title("Monthly Revenue Trend")
    plt.xlabel("Month")
    plt.ylabel("Revenue")
    plt.grid(True)

    path = output_dir / "monthly_revenue.png"
    plt.savefig(path, bbox_inches="tight")
    plt.close()

    generated_files.append(str(path))

    quarterly_revenue = (
        df.groupby("quarter")["revenue"]
        .sum()
    )

    plt.figure(figsize=(8, 5))
    plt.bar(
        quarterly_revenue.index.astype(str),
        quarterly_revenue.values
    )
    plt.title("Quarterly Revenue")
    plt.xlabel("Quarter")
    plt.ylabel("Revenue")
    plt.grid(axis="y")

    path = output_dir / "quarterly_revenue.png"
    plt.savefig(path, bbox_inches="tight")
    plt.close()

    generated_files.append(str(path))

    region_revenue = (
        df.groupby("region")["revenue"]
        .sum()
        .sort_values(ascending=False)
    )

    plt.figure(figsize=(8, 5))
    plt.bar(
        region_revenue.index,
        region_revenue.values
    )
    plt.title("Revenue by Region")
    plt.xlabel("Region")
    plt.ylabel("Revenue")
    plt.xticks(rotation=20)
    plt.grid(axis="y")

    path = output_dir / "revenue_by_region.png"
    plt.savefig(path, bbox_inches="tight")
    plt.close()

    generated_files.append(str(path))

    product_revenue = (
        df.groupby("product")["revenue"]
        .sum()
        .sort_values(ascending=False)
    )

    plt.figure(figsize=(10, 5))
    plt.bar(
        product_revenue.index,
        product_revenue.values
    )
    plt.title("Revenue by Product")
    plt.xlabel("Product")
    plt.ylabel("Revenue")
    plt.xticks(rotation=30)
    plt.grid(axis="y")

    path = output_dir / "revenue_by_product.png"
    plt.savefig(path, bbox_inches="tight")
    plt.close()

    generated_files.append(str(path))

    return generated_files


if __name__ == "__main__":

    project_root = Path(__file__).resolve().parents[2]

    dataset_path = (
        project_root
        / "data"
        / "processed"
        / "cleaned_sales_data.csv"
    )

    output_dir = (
        project_root
        / "reports"
        / "figures"
    )

    files = create_visualizations(
        dataset_path,
        output_dir
    )

    print("\n===== VISUALIZATION TOOL =====")

    print("Generated visualizations:")

    for file in files:
        print("-", file)