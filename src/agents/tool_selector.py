import json

from src.llm.llm_client import generate_response
from src.agents.tool_registry import get_tool_descriptions


VALID_TOOLS = {
    "dataset_inspector",
    "data_cleaning",
    "eda",
    "diagnostic_analysis",
    "visualization",
    "sql",
    "ml",
    "rag"
}


def deterministic_route(question):
    """
    Route high-confidence questions using explicit rules.
    Return None when the question is ambiguous.
    """

    text = question.lower().strip()

    # --------------------------------------------------------
    # Policy / Knowledge Base
    # --------------------------------------------------------

    policy_terms = [
        "policy",
        "policies",
        "guideline",
        "guidelines",
        "business rule",
        "rules",
        "according to the document",
        "according to policy",
        "what should happen"
    ]

    if any(term in text for term in policy_terms):

        return {
            "tool": "rag",
            "reason": (
                "Question requires information "
                "from the knowledge base."
            )
        }

    # --------------------------------------------------------
    # Machine Learning
    # --------------------------------------------------------

    ml_terms = [
        "predict",
        "prediction",
        "machine learning",
        "train a model",
        "model performance",
        "mae",
        "rmse",
        "r-squared",
        "r2"
    ]

    if any(term in text for term in ml_terms):

        return {
            "tool": "ml",
            "reason": (
                "Question explicitly requires "
                "predictive or ML analysis."
            )
        }


    # --------------------------------------------------------
    # Business Insight / Diagnostic Questions
    # --------------------------------------------------------

    diagnostic_terms = [
        "business insights",
        "main business insights",
        "key business insights",
        "why did sales decline",
        "why did revenue decline",
        "why did profit decline",
        "sales decline",
        "revenue decline",
        "profit decline",
        "diagnose",
        "diagnostic analysis"
    ]

    if any(term in text for term in diagnostic_terms):

        return {
            "tool": "diagnostic_analysis",
            "reason": (
                "Question requires diagnostic analysis "
                "of business performance."
            )
        }

    # --------------------------------------------------------
    # SQL / Numerical Questions
    # --------------------------------------------------------

    sql_terms = [
        "total revenue",
        "total profit",
        "sum",
        "average revenue",
        "average profit",
        "count",
        "how many",
        "revenue by",
        "profit by"
    ]

    if any(term in text for term in sql_terms):

        return {
            "tool": "sql",
            "reason": (
                "Question requires structured "
                "numerical aggregation."
            )
        }

    return None


def llm_route(question):
    """
    Use the LLM only for ambiguous questions.
    """

    tools = get_tool_descriptions()

    prompt = f"""
You are a tool router for a data intelligence system.

Available tools:

{tools}

User question:
{question}

Choose exactly ONE tool.

Return ONLY valid JSON.

Example:

{{
    "tool": "eda",
    "reason": "Question asks for general patterns in the dataset."
}}

Valid tool names are:

dataset_inspector
data_cleaning
eda
diagnostic_analysis
visualization
sql
ml
rag

Do not invent tool names.
Do not add extra text.
"""

    response = generate_response(
        prompt
    ).strip()

    # --------------------------------------------------------
    # Remove markdown code fences if the LLM adds them
    # --------------------------------------------------------

    if response.startswith("```"):

        response = response.replace(
            "```json",
            ""
        )

        response = response.replace(
            "```",
            ""
        )

        response = response.strip()

    # --------------------------------------------------------
    # Parse JSON
    # --------------------------------------------------------

    try:

        decision = json.loads(
            response
        )

    except json.JSONDecodeError as error:

        raise ValueError(
            "Tool router returned invalid JSON: "
            f"{response}"
        ) from error

    # --------------------------------------------------------
    # Validate structure
    # --------------------------------------------------------

    if not isinstance(
        decision,
        dict
    ):

        raise ValueError(
            "Tool router response must be a JSON object."
        )

    selected_tool = decision.get(
        "tool"
    )

    # --------------------------------------------------------
    # Normalize LLM output
    # --------------------------------------------------------

    if selected_tool is not None:

        selected_tool = str(
            selected_tool
        ).strip().lower()

    # --------------------------------------------------------
    # Validate tool
    # --------------------------------------------------------

    if selected_tool not in VALID_TOOLS:

        raise ValueError(
            "Invalid tool selected by LLM: "
            f"{selected_tool}"
        )

    # Store normalized value
    decision["tool"] = selected_tool

    # Make sure reason exists
    if not decision.get("reason"):

        decision["reason"] = (
            "Selected based on the user's question."
        )

    return decision


def select_tool(question):
    """
    Select a tool using deterministic routing first,
    then the LLM for ambiguous questions.
    """

    deterministic_decision = deterministic_route(
        question
    )

    if deterministic_decision is not None:

        return deterministic_decision

    return llm_route(
        question
    )


if __name__ == "__main__":

    questions = [
        "What was the total revenue in Q3?",
        "What should happen if regional revenue falls by more than 15 percent?",
        "Which factors can predict order quantity?",
        "Show me the general patterns in the dataset.",
        "What are the main business insights?"
    ]

    print(
        "\n===== HYBRID TOOL ROUTER TEST ====="
    )

    for question in questions:

        try:

            decision = select_tool(
                question
            )

            print(
                "\nQuestion:"
            )

            print(
                question
            )

            print(
                "Selected tool:"
            )

            print(
                decision["tool"]
            )

            print(
                "Reason:"
            )

            print(
                decision["reason"]
            )

        except Exception as error:

            print(
                "\nQuestion:"
            )

            print(
                question
            )

            print(
                "ERROR:"
            )

            print(
                error
            )