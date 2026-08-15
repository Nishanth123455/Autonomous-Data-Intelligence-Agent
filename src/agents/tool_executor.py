from pathlib import Path

from src.tools.sql_tool import run_sql_query
from src.tools.dataset_tool import inspect_dataset
from src.tools.cleaning_tool import clean_dataset
from src.tools.eda_tool import run_eda
from src.tools.analysis_tool import compare_quarters
from src.tools.visualization_tool import create_visualizations
from src.tools.ml_tool import run_ml_analysis

from src.rag.retrieve import retrieve_documents


PROJECT_ROOT = Path(__file__).resolve().parents[2]

DATASET_PATH = (
    PROJECT_ROOT
    / "data"
    / "raw"
    / "sales_data.csv"
)

DATABASE_PATH = (
    PROJECT_ROOT
    / "data"
    / "processed"
    / "sales.db"
)

CHROMA_PATH = (
    PROJECT_ROOT
    / "data"
    / "processed"
    / "chroma_db"
)


def execute_tool(tool_name, tool_input=None):
    """
    Execute an approved tool.
    """

    # 1. Dataset Inspector
    if tool_name == "dataset_inspector":

        return inspect_dataset(
            DATASET_PATH
        )

    # 2. Data Cleaning
    if tool_name == "data_cleaning":

        processed_path = (
            PROJECT_ROOT
            / "data"
            / "processed"
            / "cleaned_sales_data.csv"
        )

        return clean_dataset(
            DATASET_PATH,
            processed_path
        )

    # 3. EDA
    if tool_name == "eda":

        return run_eda(
            DATASET_PATH
        )

    # 4. Diagnostic Analysis
    if tool_name == "diagnostic_analysis":

        return compare_quarters(
            DATASET_PATH,
            target_quarter=3,
            comparison_quarter=2
        )

    # 5. Visualization
    if tool_name == "visualization":

        output_dir = (
            PROJECT_ROOT
            / "reports"
            / "figures"
        )

        return create_visualizations(
            DATASET_PATH,
            output_dir
        )

    # 6. Machine Learning
    if tool_name == "ml":

        return run_ml_analysis(
            DATASET_PATH
        )

    # 7. SQL
    if tool_name == "sql":

        if not isinstance(tool_input, str):
            raise ValueError(
                "SQL tool requires a SQL query string."
            )

        result = run_sql_query(
            DATABASE_PATH,
            tool_input
        )

        return result.to_dict(
            orient="records"
        )

    # 8. RAG
    if tool_name == "rag":

        if not isinstance(tool_input, str):
            raise ValueError(
                "RAG tool requires a query string."
            )

        documents = retrieve_documents(
            CHROMA_PATH,
            tool_input,
            k=3
        )

        return [
            {
                "source": document.metadata.get(
                    "source"
                ),
                "content": document.page_content
            }
            for document in documents
        ]

    # Unknown tool
    raise ValueError(
        f"Unknown or unapproved tool: {tool_name}"
    )


if __name__ == "__main__":

    print("\n===== TOOL EXECUTOR TEST =====")

    # Test Dataset Inspector
    print("\n1. Dataset Inspector")

    result = execute_tool(
        "dataset_inspector"
    )

    print(result)

    # Test EDA
    print("\n2. EDA")

    result = execute_tool(
        "eda"
    )

    print(result)

    # Test ML
    print("\n3. ML")

    result = execute_tool(
        "ml"
    )

    print(result)