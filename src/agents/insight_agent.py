import json

from src.llm.llm_client import generate_response


def run_insight_agent(
    user_question,
    analysis_results,
    knowledge_results=None
):
    """
    Generate evidence-grounded business insights.
    """

    prompt = f"""
You are the Insight Agent in an Autonomous Data
Intelligence system.

User question:
{user_question}

ANALYSIS EVIDENCE:
{json.dumps(analysis_results, indent=2, default=str)}

BUSINESS KNOWLEDGE:
{json.dumps(knowledge_results, indent=2, default=str)}

Your task is to produce evidence-grounded insights.

STRICT EVIDENCE RULES:

1. Every numerical claim must come directly from
   the provided evidence.

2. Never invent a number.

3. Never change the meaning of a number.

4. Distinguish clearly between:
   OBSERVED FACT
   ASSOCIATION
   POSSIBLE EXPLANATION
   RECOMMENDATION

5. An observed decline does NOT prove its cause.

6. Never use causal language such as:
   "caused by"
   "driven by"
   "resulted from"
   "because of"
   unless the provided evidence explicitly establishes
   causation.

7. Correlation does not establish causation.

8. If the evidence is insufficient to identify a cause,
   explicitly say:
   "The available evidence does not establish causation."

9. Do not invent external factors such as:
   market trends, seasonality, competition, customer
   behavior, economic conditions, or operational issues
   unless they appear in the provided evidence.

10. Do not say that a region caused a company-wide decline
    merely because that region experienced the largest decline.

11. If an ML model has weak predictive performance,
    explicitly report the limitation.

12. Recommendations must follow from observed evidence
    or stated business policy.

Return exactly these sections:

EXECUTIVE SUMMARY

OBSERVED FACTS

ASSOCIATIONS

POSSIBLE EXPLANATIONS

RECOMMENDATIONS

LIMITATIONS
"""

    response = generate_response(
        prompt
    )

    return response


if __name__ == "__main__":

    sample_analysis = {
        "quarterly_revenue_change": -27.55,
        "quarterly_profit_change": -27.73,
        "quantity_change": -19.43,
        "west_revenue_change": -60.56,
        "east_revenue_change": -19.60,
        "south_revenue_change": -17.75,
        "north_revenue_change": -7.37,
        "laptop_revenue_change": -44.80,
        "ml_r2": 0.0027
    }

    result = run_insight_agent(
        "Why did sales decline in Q3?",
        sample_analysis
    )

    print("\n===== INSIGHT AGENT =====")
    print(result)