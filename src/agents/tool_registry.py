from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[2]


TOOLS = {
    "dataset_inspector": {
        "description": (
            "Inspect the uploaded dataset and return "
            "schema, data types, missing values, duplicates, "
            "and basic numerical statistics."
        ),
        "input": "dataset_path",
    },

    "data_cleaning": {
        "description": (
            "Clean the dataset by handling missing values, "
            "duplicates, and date columns."
        ),
        "input": "dataset_path",
    },

    "eda": {
        "description": (
            "Perform exploratory data analysis including "
            "revenue, profit, regional, product, category, "
            "customer-segment and time-based analysis."
        ),
        "input": "dataset_path",
    },

    "diagnostic_analysis": {
        "description": (
            "Compare business performance between periods "
            "and identify major observed changes across "
            "regions, products, categories and customer segments."
        ),
        "input": "dataset_path",
    },

    "visualization": {
        "description": (
            "Generate business visualizations such as "
            "monthly revenue, quarterly revenue, regional "
            "revenue and product revenue charts."
        ),
        "input": "dataset_path",
    },

    "sql": {
        "description": (
            "Execute safe read-only SQL queries against "
            "the structured sales database."
        ),
        "input": "sql_query",
    },

    "ml": {
        "description": (
            "Run the machine-learning analysis tool and "
            "evaluate predictive performance using "
            "MAE, RMSE and R-squared."
        ),
        "input": "dataset_path",
    },

    "rag": {
        "description": (
            "Retrieve relevant information from the "
            "business knowledge base using semantic search."
        ),
        "input": "query",
    },
}


def get_tool_descriptions():

    descriptions = []

    for name, details in TOOLS.items():

        descriptions.append(
            f"- {name}: {details['description']} "
            f"Input: {details['input']}"
        )

    return "\n".join(descriptions)


if __name__ == "__main__":

    print("\n===== AVAILABLE AGENT TOOLS =====\n")

    print(
        get_tool_descriptions()
    )