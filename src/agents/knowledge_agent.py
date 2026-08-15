from src.agents.tool_executor import execute_tool


def run_knowledge_agent(question):
    """
    Retrieve relevant business knowledge
    for the user's question.
    """

    print("\n===== KNOWLEDGE AGENT =====")

    result = execute_tool(
        "rag",
        question
    )

    return result


if __name__ == "__main__":

    question = (
        "What should happen if regional revenue "
        "falls by more than 15 percent?"
    )

    result = run_knowledge_agent(
        question
    )

    print("\nKnowledge Agent completed.")
    print(result)