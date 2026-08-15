from src.agents.planner import create_plan

from src.agents.data_agent import run_data_agent
from src.agents.analysis_agent import run_analysis_agent
from src.agents.knowledge_agent import run_knowledge_agent
from src.agents.visualization_agent import run_visualization_agent

from src.agents.insight_agent import run_insight_agent
from src.agents.report_agent import run_report_agent


def run_orchestrator(user_question):

    print("\n" + "=" * 60)
    print(" AUTONOMOUS DATA INTELLIGENCE AGENT")
    print("=" * 60)


    print("\n[1] Creating execution plan...")

    selected_agents = create_plan(
        user_question
    )

    print("\nSelected agents:")

    for agent in selected_agents:
        print("-", agent)

    results = {
        "data": None,
        "analysis": None,
        "knowledge": None,
        "visualizations": None
    }

    for agent in selected_agents:

        print(
            f"\nRunning {agent}..."
        )

        if agent == "data_agent":

            results["data"] = run_data_agent()

        elif agent == "analysis_agent":

            results["analysis"] = (
                run_analysis_agent(
                    user_question
                )
            )

        elif agent == "knowledge_agent":

            results["knowledge"] = (
                run_knowledge_agent(
                    user_question
                )
            )

        elif agent == "visualization_agent":

            results["visualizations"] = (
                run_visualization_agent()
            )


    print("\nRunning Insight Agent...")

    insights = run_insight_agent(
        user_question=user_question,
        analysis_results=results["analysis"],
        knowledge_results=results["knowledge"]
    )

    print("✓ Insights generated")

    print("\nRunning Report Agent...")
    report = run_report_agent(
        user_question,
        insights,
        results
    )

    print("✓ Report generated")

    print("\n" + "=" * 60)
    print(" DYNAMIC PIPELINE COMPLETE")
    print("=" * 60)

    print("\nReport saved to:")

    print(
        report["report_path"]
    )

    return {
        "plan": selected_agents,
        "results": results,
        "insights": insights,
        "report": report
    }


if __name__ == "__main__":

    question = (
        "Why did sales decline in Q3?"
    )

    result = run_orchestrator(
        question
    )

    print("\n===== FINAL REPORT =====")

    print(
        result["report"]["report"]
    )