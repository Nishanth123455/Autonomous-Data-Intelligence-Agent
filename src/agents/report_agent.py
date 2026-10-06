from pathlib import Path


def _unwrap_analysis(analysis_results):


    data = analysis_results

    for _ in range(5):
        if not isinstance(data, dict):
            break

        if "tool" in data and "result" in data:
            return (
                data.get("tool"),
                data.get("result")
            )

        if "analysis" in data:
            data = data["analysis"]
            continue

        if "result" in data:
            data = data["result"]
            continue

        break

    return None, data


def _format_percent(value):
    return f"{float(value):.2f}%"


def _build_diagnostic_report(data):

    overall = data.get("overall", {})

    regional = data.get("regional")
    product = data.get("product")
    category = data.get("category")
    segment = data.get("segment")

    q3_revenue = overall.get("revenue_target")
    q2_revenue = overall.get("revenue_comparison")
    revenue_change = overall.get("revenue_change_percent")

    q3_profit = overall.get("profit_target")
    q2_profit = overall.get("profit_comparison")
    profit_change = overall.get("profit_change_percent")

    quantity_change = overall.get("quantity_change_percent")
    price_change = overall.get("average_price_change_percent")
    discount_change = overall.get("average_discount_change_percent")

    report = f"""
EXECUTIVE SUMMARY

Q3 revenue was {q3_revenue:,.2f}, compared with Q2 revenue
of {q2_revenue:,.2f}, representing a revenue decline of
{abs(float(revenue_change)):.2f}%. Profit changed by
{_format_percent(profit_change)}.


KEY FINDINGS

- Q3 revenue: {q3_revenue:,.2f}
- Q2 revenue: {q2_revenue:,.2f}
- Revenue change: {_format_percent(revenue_change)}
- Q3 profit: {q3_profit:,.2f}
- Q2 profit: {q2_profit:,.2f}
- Profit change: {_format_percent(profit_change)}
- Quantity change: {_format_percent(quantity_change)}
- Average price change: {_format_percent(price_change)}
- Average discount change: {_format_percent(discount_change)}


SUPPORTING EVIDENCE

Regional revenue changes:
"""

    if regional is not None:

        for name, row in regional.iterrows():

            report += (
                f"- {name}: "
                f"{_format_percent(row['change_percent'])}\n"
            )

    report += "\nProduct revenue changes:\n"

    if product is not None:

        for name, row in product.iterrows():

            report += (
                f"- {name}: "
                f"{_format_percent(row['change_percent'])}\n"
            )

    report += "\nCategory revenue changes:\n"

    if category is not None:

        for name, row in category.iterrows():

            report += (
                f"- {name}: "
                f"{_format_percent(row['change_percent'])}\n"
            )

    if segment is not None:

        report += "\nCustomer segment changes:\n"

        for name, row in segment.iterrows():

            report += (
                f"- {name}: "
                f"{_format_percent(row['change_percent'])}\n"
            )

    report += """

POSSIBLE EXPLANATIONS

The available evidence does not establish causation.
The observed changes identify areas that require further
investigation.


BUSINESS RECOMMENDATIONS

1. Investigate the regional revenue changes, particularly
   the regions with the largest declines.

2. Investigate product-level revenue changes to identify
   high-impact products.

3. Review changes in order volume, pricing, discounts,
   customer segments, and operational issues.


LIMITATIONS

The analysis identifies observed changes and associations,
but the available evidence does not establish causation.

Further investigation is required before making a specific
causal conclusion.
"""

    return report.strip()


def _build_ml_report(data):

    features = data.get("features", [])

    mae = data.get("mae")
    rmse = data.get("rmse")
    r2 = data.get("r2")

    feature_text = ", ".join(features)

    report = f"""
EXECUTIVE SUMMARY

A Random Forest regression model was evaluated for predicting
order quantity using the available dataset features.


KEY FINDINGS

- Target variable: order quantity
- Model: Random Forest Regressor
- MAE: {float(mae):.4f}
- RMSE: {float(rmse):.4f}
- R²: {float(r2):.4f}


SUPPORTING EVIDENCE

The model used the following features:

- {feature_text}


POSSIBLE EXPLANATIONS

The model shows very weak predictive performance, with an
R² of approximately {float(r2):.4f}. The available evidence
does not establish that any individual feature causes changes
in order quantity.


BUSINESS RECOMMENDATIONS

1. Use the identified features as inputs for further
   predictive experiments.

2. Investigate additional features or improved feature
   engineering to determine whether predictive performance
   can be improved.

3. Treat the current model as a baseline because its
   predictive performance is weak.


LIMITATIONS

The current model has very weak predictive performance.
An R² close to zero indicates that the model explains very
little of the variation in order quantity.

The model's predictive relationships should not be interpreted
as causal relationships.
"""

    return report.strip()


def _correlation_strength(value):
    """Describe correlation without exaggerating weak values."""

    value = float(value)
    magnitude = abs(value)

    if magnitude < 0.10:
        strength = "very weak"
    elif magnitude < 0.30:
        strength = "weak"
    elif magnitude < 0.50:
        strength = "moderate"
    elif magnitude < 0.70:
        strength = "strong"
    else:
        strength = "very strong"

    if value > 0:
        direction = "positive"
    elif value < 0:
        direction = "negative"
    else:
        direction = "zero"

    return f"{strength} {direction}"


def _build_eda_report(data):

    total_revenue = data.get("total_revenue")
    total_profit = data.get("total_profit")
    average_order_value = data.get("average_order_value")
    total_orders = data.get("total_orders")
    profit_margin = data.get("profit_margin")

    revenue_by_region = data.get("revenue_by_region")
    revenue_by_product = data.get("revenue_by_product")
    correlation_matrix = data.get("correlation_matrix")

    report = f"""
EXECUTIVE SUMMARY

The exploratory analysis summarizes the major revenue, profit,
order, regional, product, and correlation patterns in the
dataset.


KEY FINDINGS

- Total revenue: ${float(total_revenue):,.2f}
- Total profit: ${float(total_profit):,.2f}
- Average order value: ${float(average_order_value):,.2f}
- Total orders: {int(total_orders):,}
- Profit margin: {float(profit_margin):.4f}


SUPPORTING EVIDENCE

Revenue by region:
"""

    if revenue_by_region is not None:

        for name, value in revenue_by_region.items():

            report += (
                f"- {name}: ${float(value):,.2f}\n"
            )

    report += "\nRevenue by product:\n"

    if revenue_by_product is not None:

        for name, value in revenue_by_product.items():

            report += (
                f"- {name}: ${float(value):,.2f}\n"
            )

    report += "\nCorrelation observations:\n"

    if correlation_matrix is not None:

        correlations = []

        columns = list(
            correlation_matrix.columns
        )

        for i in range(len(columns)):

            for j in range(i + 1, len(columns)):

                first = columns[i]
                second = columns[j]

                value = correlation_matrix.loc[
                    first,
                    second
                ]

                correlations.append(
                    (
                        abs(float(value)),
                        first,
                        second,
                        float(value)
                    )
                )

        correlations.sort(
            reverse=True
        )

        for _, first, second, value in correlations[:5]:

            description = _correlation_strength(
                value
            )

            report += (
                f"- {first} and {second}: "
                f"{value:.4f} "
                f"({description} correlation)\n"
            )

    report += """

POSSIBLE EXPLANATIONS

The exploratory analysis identifies patterns and associations,
but these observations do not establish causation.


BUSINESS RECOMMENDATIONS

1. Use the identified regional and product patterns to guide
   further business investigation.

2. Investigate the strongest observed relationships using
   additional analysis before making causal conclusions.


LIMITATIONS

EDA identifies distributions, relationships, and associations.
Correlation does not establish causation.
"""

    return report.strip()


def _build_sql_report(data):

    return f"""
EXECUTIVE SUMMARY

The SQL analysis returned the requested structured-data result.


KEY FINDINGS

{data}


SUPPORTING EVIDENCE

The result was obtained through a SQL query over the dataset.


POSSIBLE EXPLANATIONS

No causal explanation is required for this numerical query.


BUSINESS RECOMMENDATIONS

No business recommendation is required for this query.


LIMITATIONS

The result is limited to the information returned by the SQL query.
""".strip()


def _build_rag_report(data):

    return f"""
EXECUTIVE SUMMARY

The requested business-policy information was retrieved from
the available knowledge base.


KEY FINDINGS

{data}


SUPPORTING EVIDENCE

The answer is based on the retrieved business-policy information.


POSSIBLE EXPLANATIONS

The policy describes the required business response but does
not establish a causal explanation.


BUSINESS RECOMMENDATIONS

Follow the relevant business policy and perform the required
review and investigation.


LIMITATIONS

The answer is limited to the policies available in the
knowledge base.
""".strip()


def _build_generic_report(
    user_question,
    insights
):

    return f"""
EXECUTIVE SUMMARY

{user_question}


KEY FINDINGS

{insights}


SUPPORTING EVIDENCE

The findings are based on the available analytical evidence.


POSSIBLE EXPLANATIONS

The available evidence does not establish causation.


BUSINESS RECOMMENDATIONS

Further investigation is required before making a specific
business recommendation.


LIMITATIONS

The report is limited to the evidence available from the
executed analytical tools.
""".strip()


def run_report_agent(
    user_question,
    insights,
    analysis_results=None
):

    tool_name, data = _unwrap_analysis(
        analysis_results
    )

    if tool_name == "diagnostic_analysis":

        report = _build_diagnostic_report(
            data
        )

    elif tool_name == "ml":

        report = _build_ml_report(
            data
        )

    elif tool_name == "eda":

        report = _build_eda_report(
            data
        )

    elif tool_name == "sql":

        report = _build_sql_report(
            data
        )

    elif tool_name == "rag":

        report = _build_rag_report(
            data
        )

    else:

        report = _build_generic_report(
            user_question,
            insights
        )

    project_root = (
        Path(__file__)
        .resolve()
        .parents[2]
    )

    report_path = (
        project_root
        / "reports"
        / "final_report.txt"
    )

    report_path.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    report_path.write_text(
        report,
        encoding="utf-8"
    )

    print("\nReport saved to:")
    print(report_path)

    return {
        "report": report,
        "report_path": str(report_path)
    }