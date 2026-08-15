from src.agents.planner import create_plan
from src.agents.tool_selector import select_tool


TEST_CASES = [
    {
        "question": "What was the total revenue in Q3?",
        "expected_agent": "analysis_agent",
        "expected_tool": "sql"
    },
    {
        "question": (
            "What should happen if regional revenue "
            "falls by more than 15 percent?"
        ),
        "expected_agent": "knowledge_agent",
        "expected_tool": "rag"
    },
    {
        "question": "Why did sales decline in Q3?",
        "expected_agent": "analysis_agent",
        "expected_tool": "diagnostic_analysis"
    },
    {
        "question": "Which factors can predict order quantity?",
        "expected_agent": "analysis_agent",
        "expected_tool": "ml"
    }
]


def evaluate_planner():

    print("\n===== PLANNER EVALUATION =====")

    passed = 0

    for index, test in enumerate(
        TEST_CASES,
        start=1
    ):

        question = test["question"]

        agents = create_plan(
            question
        )

        success = (
            test["expected_agent"]
            in agents
        )

        if success:
            passed += 1
            status = "PASS"
        else:
            status = "FAIL"

        print(
            f"\nTest {index}: {status}"
        )

        print(
            "Question:",
            question
        )

        print(
            "Selected agents:",
            agents
        )

        print(
            "Expected agent:",
            test["expected_agent"]
        )

    accuracy = (
        passed / len(TEST_CASES)
    ) * 100

    print("\n===== SUMMARY =====")

    print(
        f"Passed: {passed}/{len(TEST_CASES)}"
    )

    print(
        f"Planner success rate: {accuracy:.2f}%"
    )


def evaluate_tool_router():

    print("\n===== TOOL ROUTER EVALUATION =====")

    passed = 0

    for index, test in enumerate(
        TEST_CASES,
        start=1
    ):

        question = test["question"]

        decision = select_tool(
            question
        )

        selected_tool = decision["tool"]

        success = (
            selected_tool
            == test["expected_tool"]
        )

        if success:
            passed += 1
            status = "PASS"
        else:
            status = "FAIL"

        print(
            f"\nTest {index}: {status}"
        )

        print(
            "Question:",
            question
        )

        print(
            "Selected tool:",
            selected_tool
        )

        print(
            "Expected tool:",
            test["expected_tool"]
        )

    accuracy = (
        passed / len(TEST_CASES)
    ) * 100

    print("\n===== SUMMARY =====")

    print(
        f"Passed: {passed}/{len(TEST_CASES)}"
    )

    print(
        f"Tool routing success rate: {accuracy:.2f}%"
    )


if __name__ == "__main__":

    evaluate_planner()

    evaluate_tool_router()