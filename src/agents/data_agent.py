from src.agents.tool_executor import execute_tool


def run_data_agent():
    """
    Inspect and clean the dataset.
    """

    print("\n===== DATA AGENT =====")

    inspection = execute_tool(
        "dataset_inspector"
    )

    cleaning = execute_tool(
        "data_cleaning"
    )

    return {
        "inspection": inspection,
        "cleaning": cleaning
    }


if __name__ == "__main__":

    result = run_data_agent()

    print("\nData Agent completed.")
    print(result)