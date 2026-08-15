from pathlib import Path

from retrieve import retrieve_documents


def evaluate_retrieval():

    project_root = Path(__file__).resolve().parents[2]

    persist_directory = (
        project_root
        / "data"
        / "processed"
        / "chroma_db"
    )

    test_queries = [
        {
            "query": "What happens if regional revenue falls by more than 15 percent?",
            "expected": "management review"
        },
        {
            "query": "What should be reviewed when a product revenue declines?",
            "expected": "sales team"
        },
        {
            "query": "How should discounts be analyzed?",
            "expected": "discounts"
        },
        {
            "query": "Should analysts assume correlation means causation?",
            "expected": "causal"
        },
        {
            "query": "What should management recommendations be based on?",
            "expected": "measurable evidence"
        }
    ]

    print("\n===== RAG RETRIEVAL EVALUATION =====")

    passed = 0

    for index, test in enumerate(
        test_queries,
        start=1
    ):

        results = retrieve_documents(
            persist_directory,
            test["query"],
            k=3
        )

        combined_text = " ".join(
            document.page_content.lower()
            for document in results
        )

        expected = test["expected"].lower()

        found = expected in combined_text

        status = "PASS" if found else "FAIL"

        if found:
            passed += 1

        print(
            f"\nTest {index}: {status}"
        )

        print(
            "Query:",
            test["query"]
        )

        print(
            "Expected concept:",
            test["expected"]
        )

    print("\n===== SUMMARY =====")

    print(
        f"Passed: {passed}/{len(test_queries)}"
    )

    print(
        f"Retrieval success rate: "
        f"{passed / len(test_queries):.2%}"
    )


if __name__ == "__main__":
    evaluate_retrieval()