from pathlib import Path
import pandas as pd


def clean_dataset(input_path, output_path):

    input_path = Path(input_path)
    output_path = Path(output_path)

    if not input_path.exists():
        raise FileNotFoundError(f"Dataset not found: {input_path}")

    df = pd.read_csv(input_path)

    original_rows = len(df)
    original_columns = len(df.columns)

    missing_before = int(df.isnull().sum().sum())

    duplicates_before = int(df.duplicated().sum())

    date_columns = []

    for column in df.columns:

        if "date" in column.lower():

            converted = pd.to_datetime(
                df[column],
                errors="coerce"
            )

            valid_ratio = converted.notna().mean()

            if valid_ratio > 0.8:
                df[column] = converted
                date_columns.append(column)

    numerical_columns = df.select_dtypes(
        include="number"
    ).columns

    categorical_columns = df.select_dtypes(
        include="object"
    ).columns

    for column in numerical_columns:

        if df[column].isnull().any():
            df[column] = df[column].fillna(
                df[column].median()
            )

    for column in categorical_columns:

        if df[column].isnull().any():
            df[column] = df[column].fillna(
                "Unknown"
            )

    duplicates_removed = int(df.duplicated().sum())

    if duplicates_removed > 0:
        df = df.drop_duplicates()

    output_path.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    df.to_csv(
        output_path,
        index=False
    )

    missing_after = int(df.isnull().sum().sum())

    final_rows = len(df)

    return {
        "original_rows": original_rows,
        "final_rows": final_rows,
        "original_columns": original_columns,
        "missing_values_before": missing_before,
        "missing_values_after": missing_after,
        "duplicates_before": duplicates_before,
        "duplicates_removed": duplicates_removed,
        "date_columns_converted": date_columns,
        "output_path": str(output_path)
    }


if __name__ == "__main__":

    project_root = Path(__file__).resolve().parents[2]

    input_path = (
        project_root
        / "data"
        / "raw"
        / "sales_data.csv"
    )

    output_path = (
        project_root
        / "data"
        / "processed"
        / "cleaned_sales_data.csv"
    )

    result = clean_dataset(
        input_path,
        output_path
    )

    print("\n===== DATA CLEANING =====")

    print(
        "Original rows:",
        result["original_rows"]
    )

    print(
        "Final rows:",
        result["final_rows"]
    )

    print(
        "Original columns:",
        result["original_columns"]
    )

    print(
        "Missing values before:",
        result["missing_values_before"]
    )

    print(
        "Missing values after:",
        result["missing_values_after"]
    )

    print(
        "Duplicates before:",
        result["duplicates_before"]
    )

    print(
        "Duplicates removed:",
        result["duplicates_removed"]
    )

    print(
        "Date columns converted:",
        result["date_columns_converted"]
    )

    print(
        "Cleaned dataset:",
        result["output_path"]
    )