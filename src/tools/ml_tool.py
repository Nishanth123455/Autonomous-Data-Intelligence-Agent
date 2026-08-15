from pathlib import Path

import pandas as pd

from sklearn.compose import ColumnTransformer
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder


def run_ml_analysis(file_path):
    """
    Train a Random Forest model to predict order quantity.
    """

    file_path = Path(file_path)

    if not file_path.exists():
        raise FileNotFoundError(
            f"Dataset not found: {file_path}"
        )

    df = pd.read_csv(file_path)

    df["order_date"] = pd.to_datetime(
        df["order_date"]
    )

    # Create time features
    df["month"] = df["order_date"].dt.month
    df["quarter"] = df["order_date"].dt.quarter

    # Features and target
    features = [
        "unit_price",
        "discount",
        "region",
        "product",
        "category",
        "customer_segment",
        "month",
        "quarter"
    ]

    target = "quantity"

    X = df[features]
    y = df[target]

    # Identify feature types
    categorical_features = [
        "region",
        "product",
        "category",
        "customer_segment"
    ]

    numerical_features = [
        "unit_price",
        "discount",
        "month",
        "quarter"
    ]

    # Preprocessing
    preprocessor = ColumnTransformer(
        transformers=[
            (
                "categorical",
                OneHotEncoder(
                    handle_unknown="ignore"
                ),
                categorical_features
            )
        ],
        remainder="passthrough"
    )

    # Model
    model = RandomForestRegressor(
        n_estimators=200,
        random_state=42,
        n_jobs=-1
    )

    pipeline = Pipeline(
        steps=[
            ("preprocessor", preprocessor),
            ("model", model)
        ]
    )

    # Train/test split
    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=0.2,
        random_state=42
    )

    # Train
    pipeline.fit(
        X_train,
        y_train
    )

    # Predict
    predictions = pipeline.predict(X_test)

    # Metrics
    # Baseline prediction
    baseline_prediction = y_train.mean()

    baseline_predictions = [
                               baseline_prediction
                           ] * len(y_test)

    # Model metrics
    mae = mean_absolute_error(
        y_test,
        predictions
    )

    rmse = mean_squared_error(
        y_test,
        predictions
    ) ** 0.5

    r2 = r2_score(
        y_test,
        predictions
    )

    # Baseline metrics
    baseline_mae = mean_absolute_error(
        y_test,
        baseline_predictions
    )

    baseline_rmse = mean_squared_error(
        y_test,
        baseline_predictions
    ) ** 0.5

    baseline_r2 = r2_score(
        y_test,
        baseline_predictions
    )

    return {
        "model": pipeline,
        "mae": mae,
        "rmse": rmse,
        "r2": r2,
        "baseline_mae": baseline_mae,
        "baseline_rmse": baseline_rmse,
        "baseline_r2": baseline_r2,
        "features": features,
        "target": target
    }


if __name__ == "__main__":

    project_root = Path(__file__).resolve().parents[2]

    dataset_path = (
        project_root
        / "data"
        / "processed"
        / "cleaned_sales_data.csv"
    )

    results = run_ml_analysis(
        dataset_path
    )

    print("\n===== ML ANALYSIS =====")

    print(
        "\nTarget:",
        results["target"]
    )

    print(
        "Features:",
        results["features"]
    )

    print(
        f"\nMAE: "
        f"{results['mae']:.4f}"
    )

    print(
        f"RMSE: "
        f"{results['rmse']:.4f}"
    )

    print(
        f"R²: "
        f"{results['r2']:.4f}"
    )

    print("\n===== BASELINE =====")

    print(
        f"Baseline MAE: "
        f"{results['baseline_mae']:.4f}"
    )

    print(
        f"Baseline RMSE: "
        f"{results['baseline_rmse']:.4f}"
    )

    print(
        f"Baseline R²: "
        f"{results['baseline_r2']:.4f}"
    )