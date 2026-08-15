from src.agents.tool_executor import execute_tool


def run_visualization_agent():
    """
    Generate visualizations for the analysis.
    """

    print("\n===== VISUALIZATION AGENT =====")

    result = execute_tool(
        "visualization"
    )

    return result


if __name__ == "__main__":

    result = run_visualization_agent()

    print("\nVisualization Agent completed.")
    print(result)