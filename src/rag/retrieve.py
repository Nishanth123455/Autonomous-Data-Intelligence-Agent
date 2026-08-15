from pathlib import Path

from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings


def create_retriever(persist_directory):

    embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )

    vector_database = Chroma(
        persist_directory=str(persist_directory),
        embedding_function=embeddings
    )

    return vector_database


def retrieve_documents(
    persist_directory,
    query,
    k=3
):

    vector_database = create_retriever(
        persist_directory
    )

    results = vector_database.similarity_search(
        query,
        k=k
    )

    return results


if __name__ == "__main__":

    project_root = Path(__file__).resolve().parents[2]

    persist_directory = (
        project_root
        / "data"
        / "processed"
        / "chroma_db"
    )

    query = (
        "What should happen when regional "
        "revenue declines significantly?"
    )

    results = retrieve_documents(
        persist_directory,
        query,
        k=3
    )

    print("\n===== RAG RETRIEVAL =====")

    print("\nQuery:")
    print(query)

    print("\nRetrieved Documents:")

    for index, document in enumerate(
        results,
        start=1
    ):

        print(
            f"\n--- Result {index} ---"
        )

        print(
            "Source:",
            document.metadata.get("source")
        )

        print(
            document.page_content
        )