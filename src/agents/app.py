import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

import streamlit as st

from src.agents.orchestrator import run_orchestrator


FIGURES_DIR = (
    PROJECT_ROOT
    / "reports"
    / "figures"
)


# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="Autonomous Data Intelligence Agent",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)


# ============================================================
# HEADER
# ============================================================

st.title(
    "📊 Autonomous Data Intelligence Agent"
)

st.markdown(
    """
Ask a business question about the sales dataset.

The system dynamically selects the required agents,
executes the appropriate analytical tools, and produces
evidence-grounded results.
"""
)


# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:

    st.header("System")

    st.markdown(
        """
**Architecture**

- 🧠 Planner
- 🎯 Orchestrator
- 🔎 Data Agent
- 📈 Analysis Agent
- 📚 Knowledge Agent
- 📊 Visualization Agent
- 💡 Insight Agent
- 📝 Report Agent
"""
    )

    st.divider()

    st.caption(
        "Local LLM powered by Ollama"
    )

    st.caption(
        "Data source: sales_data.csv"
    )


# ============================================================
# QUESTION INPUT
# ============================================================

st.subheader(
    "Ask a Business Question"
)

question = st.text_area(
    "Business question",
    placeholder="Example: Why did sales decline in Q3?",
    height=110,
    label_visibility="collapsed"
)


# ============================================================
# EXAMPLE QUESTIONS
# ============================================================

st.markdown(
    "**Example questions:**"
)

example_columns = st.columns(4)

examples = [
    "What was the total revenue in Q3?",
    "Why did sales decline in Q3?",
    "What should happen if regional revenue falls by more than 15 percent?",
    "Which factors can predict order quantity?"
]

for column, example in zip(
    example_columns,
    examples
):

    with column:

        st.caption(example)


# ============================================================
# RUN ANALYSIS
# ============================================================

run_analysis = st.button(
    "🚀 Run Analysis",
    type="primary",
    use_container_width=True
)


if run_analysis:

    if not question.strip():

        st.warning(
            "Please enter a business question."
        )

        st.stop()

    # --------------------------------------------------------
    # RUN ORCHESTRATOR
    # --------------------------------------------------------

    with st.spinner(
        "Autonomous agent is analyzing your question..."
    ):

        try:

            result = run_orchestrator(
                question.strip()
            )

        except Exception as error:

            st.error(
                "The analysis could not be completed."
            )

            st.exception(
                error
            )

            st.stop()

    st.success(
        "Analysis completed successfully."
    )


    # ========================================================
    # EXECUTION PLAN
    # ========================================================

    st.divider()

    st.subheader(
        "🧠 Execution Plan"
    )

    plan = result.get(
        "plan",
        []
    )

    if plan:

        plan_columns = st.columns(
            len(plan)
        )

        for column, agent in zip(
            plan_columns,
            plan
        ):

            with column:

                st.info(
                    f"✓ {agent}"
                )

    else:

        st.info(
            "No execution plan was returned."
        )


    # ========================================================
    # INSIGHTS
    # ========================================================

    insights = result.get(
        "insights"
    )

    if insights:

        st.divider()

        st.subheader(
            "💡 Insights"
        )

        st.markdown(
            insights
        )


    # ========================================================
    # VISUALIZATIONS
    # ========================================================

    st.divider()

    st.subheader(
        "📊 Visualizations"
    )

    figure_paths = [
        (
            FIGURES_DIR / "monthly_revenue.png",
            "Monthly Revenue"
        ),
        (
            FIGURES_DIR / "quarterly_revenue.png",
            "Quarterly Revenue"
        ),
        (
            FIGURES_DIR / "revenue_by_region.png",
            "Revenue by Region"
        ),
        (
            FIGURES_DIR / "revenue_by_product.png",
            "Revenue by Product"
        )
    ]

    existing_figures = [
        (path, caption)
        for path, caption in figure_paths
        if path.exists()
    ]

    if existing_figures:

        row_columns = st.columns(2)

        for index, (
            figure_path,
            caption
        ) in enumerate(existing_figures):

            with row_columns[index % 2]:

                st.image(
                    str(figure_path),
                    caption=caption,
                    use_container_width=True
                )

    else:

        st.info(
            "No visualization files were generated "
            "for this analysis."
        )


    # ========================================================
    # RESULT / FINAL REPORT
    # ========================================================

    report_result = result.get(
        "report",
        {}
    )

    report_text = None

    if isinstance(report_result, dict):

        report_text = report_result.get(
            "report"
        )

    elif isinstance(report_result, str):

        report_text = report_result


    # --------------------------------------------------------
    # Detect simple questions
    # --------------------------------------------------------

    question_lower = question.lower()

    simple_sql_question = (
        "total revenue" in question_lower
        or "revenue in q3" in question_lower
        or "revenue in q2" in question_lower
    )

    simple_policy_question = (
        "what should happen" in question_lower
        and "15 percent" in question_lower
    )


    # ========================================================
    # SIMPLE ANSWER VIEW
    # ========================================================

    if simple_sql_question:

        st.divider()

        st.subheader(
            "💰 Answer"
        )

        # Try to extract the total revenue from the report.
        import re

        match = re.search(
            r"total revenue.*?\$?([\d,]+(?:\.\d+)?)",
            report_text or "",
            re.IGNORECASE
        )

        if match:

            revenue = match.group(1)

            st.success(
                f"The total revenue for Q3 is "
                f"${revenue}."
            )

        else:

            st.markdown(
                report_text or
                "No answer was generated."
            )


    elif simple_policy_question:

        st.divider()

        st.subheader(
            "📚 Business Policy"
        )

        st.markdown(
            report_text or
            "No policy information was generated."
        )


    # ========================================================
    # DETAILED REPORT VIEW
    # ========================================================

    else:

        st.divider()

        st.subheader(
            "📝 Final Report"
        )

        if report_text:

            st.markdown(
                report_text
            )

        else:

            st.info(
                "No final report was generated."
            )


    # ========================================================
    # REPORT DOWNLOAD
    # ========================================================

    report_path = None

    if isinstance(report_result, dict):

        report_path = report_result.get(
            "report_path"
        )

    if report_path:

        report_file = Path(
            report_path
        )

        if report_file.exists():

            st.divider()

            st.download_button(
                label="⬇️ Download Report",
                data=report_file.read_text(
                    encoding="utf-8"
                ),
                file_name="final_report.txt",
                mime="text/plain"
            )


    # ========================================================
    # RAW AGENT RESULTS
    # ========================================================

    with st.expander(
        "🔧 View Raw Agent Results"
    ):

        st.json(
            result.get(
                "results",
                {}
            )
        )