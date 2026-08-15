from src.llm.llm_client import generate_response


AVAILABLE_AGENTS = [
    "data_agent",
    "analysis_agent",
    "knowledge_agent",
    "visualization_agent"
]


def create_plan(user_question):

    question = user_question.lower().strip()

    # ---------------------------------------------------------
    # 1. POLICY / KNOWLEDGE QUESTIONS
    # ---------------------------------------------------------

    policy_keywords = [
        "policy",
        "policies",
        "rule",
        "rules",
        "should happen",
        "threshold",
        "procedure",
        "business document",
        "what should",
        "according to"
    ]

    if any(
        keyword in question
        for keyword in policy_keywords
    ):

        return ["knowledge_agent"]


    # ---------------------------------------------------------
    # 2. DATA QUALITY QUESTIONS
    # ---------------------------------------------------------

    data_keywords = [
        "missing values",
        "duplicates",
        "data types",
        "schema",
        "data quality",
        "clean the data",
        "clean dataset",
        "inspect dataset"
    ]

    if any(
        keyword in question
        for keyword in data_keywords
    ):

        return ["data_agent"]


    # ---------------------------------------------------------
    # 3. VISUALIZATION QUESTIONS
    # ---------------------------------------------------------

    visualization_keywords = [
        "show charts",
        "show visualizations",
        "visualize",
        "visualization",
        "plot",
        "plots",
        "chart",
        "charts",
        "graph",
        "graphs"
    ]

    if any(
        keyword in question
        for keyword in visualization_keywords
    ):

        return [
            "analysis_agent",
            "visualization_agent"
        ]


    # ---------------------------------------------------------
    # 4. ML / PREDICTION QUESTIONS
    # ---------------------------------------------------------

    ml_keywords = [
        "predict",
        "prediction",
        "predictive",
        "machine learning",
        "ml",
        "factors can predict",
        "which factors"
    ]

    if any(
        keyword in question
        for keyword in ml_keywords
    ):

        return ["analysis_agent"]


    # ---------------------------------------------------------
    # 5. BUSINESS DIAGNOSTIC QUESTIONS
    # ---------------------------------------------------------

    diagnostic_keywords = [
        "why did",
        "why has",
        "why have",
        "decline",
        "decreased",
        "decrease",
        "dropped",
        "drop",
        "changed",
        "change",
        "performance",
        "drivers",
        "main business insights"
    ]

    if any(
        keyword in question
        for keyword in diagnostic_keywords
    ):

        return ["analysis_agent"]


    # ---------------------------------------------------------
    # 6. GENERAL DATA ANALYSIS
    # ---------------------------------------------------------

    analysis_keywords = [
        "patterns",
        "trends",
        "eda",
        "exploratory",
        "analyze",
        "analysis",
        "dataset",
        "revenue",
        "profit",
        "sales",
        "quantity"
    ]

    if any(
        keyword in question
        for keyword in analysis_keywords
    ):

        return ["analysis_agent"]


    # ---------------------------------------------------------
    # 7. LLM FALLBACK FOR AMBIGUOUS QUESTIONS
    # ---------------------------------------------------------

    prompt = f"""
Classify this business question into the minimum
required agent.

Question:
{user_question}

Available agents:

data_agent:
Dataset inspection and cleaning.

analysis_agent:
EDA, diagnostic analysis and machine learning.

knowledge_agent:
Business policies, rules and documents.

visualization_agent:
Charts and visualizations.

Return ONLY:

AGENTS: agent_name

Do not select more than two agents.
Do not invent agent names.
"""

    response = generate_response(
        prompt
    ).strip()

    print("\nPlanner fallback response:")
    print(response)

    if "AGENTS:" not in response:

        return ["analysis_agent"]

    agents_text = response.split(
        "AGENTS:",
        1
    )[1].strip()

    agents = [
        agent.strip()
        for agent in agents_text.split(",")
        if agent.strip()
        and agent.strip() in AVAILABLE_AGENTS
    ]

    if not agents:

        return ["analysis_agent"]

    return agents


if __name__ == "__main__":

    questions = [

        "What was the total revenue in Q3?",

        "What should happen if regional revenue "
        "falls by more than 15 percent?",

        "Which factors can predict order quantity?",

        "Show me the general patterns in the dataset."
    ]

    print("\n===== PLANNER TEST =====")

    for question in questions:

        print("\nQuestion:")
        print(question)

        agents = create_plan(
            question
        )

        print(
            "Selected agents:",
            agents
        )