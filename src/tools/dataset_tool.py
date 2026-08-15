from pathlib import Path
import pandas as pd

def inspect_dataset(file_path):

    file_path = Path(file_path)

    if not file_path.exists():
        raise FileNotFoundError(f"Dataset not found: {file_path}")

    df = pd.read_csv(file_path)

    rows, columns = df.shape

    column_names = df.columns.tolist()

    data_types = {
        column: str(dtype)
        for column, dtype in df.dtypes.items()
    }

    missing_values = {
        column: int(value)
        for column, value in df.isnull().sum().items()
    }

    duplicate_rows = int(df.duplicated().sum())

    numerical_columns = df.select_dtypes(
        include="number"
    ).columns.tolist()

    categorical_columns = df.select_dtypes(
        include="object"
    ).columns.tolist()

    date_columns = []

    for column in df.columns:

        if column in categorical_columns:

            converted = pd.to_datetime(
                df[column],
                errors="coerce",
                format="mixed"
            )
            if converted.notna().mean() > 0.8:
                date_columns.append(column)

    numerical_summary = {}

    if numerical_columns:

        summary = df[numerical_columns].describe()

        numerical_summary = summary.to_dict()

    return {
        "rows": rows,
        "columns": columns,
        "column_names": column_names,
        "data_types": data_types,
        "missing_values": missing_values,
        "duplicate_rows": duplicate_rows,
        "numerical_columns": numerical_columns,
        "categorical_columns": categorical_columns,
        "date_columns": date_columns,
        "numerical_summary": numerical_summary
    }


if __name__ == "__main__":

    dataset_path = (
        Path(__file__).resolve().parents[2]
        / "data"
        / "raw"
        / "sales_data.csv"
    )

    result = inspect_dataset(dataset_path)

    print("\n===== DATASET INSPECTION =====")

    print("\nRows:", result["rows"])
    print("Columns:", result["columns"])

    print("\nColumn Names:")
    for column in result["column_names"]:
        print("-", column)

    print("\nData Types:")
    for column, dtype in result["data_types"].items():
        print(f"{column}: {dtype}")

    print("\nMissing Values:")
    for column, value in result["missing_values"].items():
        print(f"{column}: {value}")

    print("\nDuplicate Rows:")
    print(result["duplicate_rows"])

    print("\nNumerical Columns:")
    print(result["numerical_columns"])

    print("\nCategorical Columns:")
    print(result["categorical_columns"])

    print("\nDate Columns:")
    print(result["date_columns"])

    print("\nNumerical Summary:")
    print(pd.DataFrame(result["numerical_summary"]))