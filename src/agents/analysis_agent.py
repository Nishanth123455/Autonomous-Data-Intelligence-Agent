from src.agents.tool_selector import select_tool
from src.agents.tool_executor import execute_tool


def run_analysis_agent(user_question):
    """
    Select and execute the appropriate analytical tool.
    """

    print("\n===== ANALYSIS AGENT =====")

    # ---------------------------------------------------------
    # 1. Select the analytical tool
    # ---------------------------------------------------------

    decision = select_tool(
        user_question
    )

    tool_name = decision["tool"]
    reason = decision["reason"]

    print("\nSelected tool:")
    print(tool_name)

    print("\nReason:")
    print(reason)

    # ---------------------------------------------------------
    # 2. Prepare tool input
    # ---------------------------------------------------------

    if tool_name == "sql":

        tool_input = """
        SELECT
            SUM(revenue) AS total_revenue
        FROM sales
        WHERE CAST(
            strftime('%m', order_date)
            AS INTEGER
        ) BETWEEN 7 AND 9
        """

    elif tool_name == "rag":

        tool_input = user_question

    else:

        tool_input = None

    # ---------------------------------------------------------
    # 3. Execute tool
    # ---------------------------------------------------------

    result = execute_tool(
        tool_name,
        tool_input
    )

    return {
        "tool": tool_name,
        "reason": reason,
        "result": result
    }


if __name__ == "__main__":

    questions = [
        "What was the total revenue in Q3?",
        "Why did sales decline in Q3?",
        "Which factors can predict order quantity?"
    ]

    for question in questions:

        print("\n" + "=" * 50)

        print(
            "Question:",
            question
        )

        result = run_analysis_agent(
            question
        )

        print("\nResult:")
        print(result)