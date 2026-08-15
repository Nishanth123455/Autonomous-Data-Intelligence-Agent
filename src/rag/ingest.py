from pathlib import Path

from dotenv import load_dotenv

load_dotenv()

from langchain_chroma import Chroma
from langchain_core.documents import Document
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter


def load_documents(documents_dir):

    documents_dir = Path(documents_dir)

    documents = []

    for file_path in documents_dir.glob("*.txt"):

        text = file_path.read_text(
            encoding="utf-8"
        )

        documents.append(
            Document(
                page_content=text,
                metadata={
                    "source": file_path.name
                }
            )
        )

    return documents


def build_vector_database(
    documents_dir,
    persist_directory
):
    documents = load_documents(
        documents_dir
    )

    if not documents:
        raise ValueError(
            "No documents found."
        )

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=700,
        chunk_overlap=100
    )

    chunks = splitter.split_documents(
        documents
    )

    embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )

    vector_database = Chroma.from_documents(
        documents=chunks,
        embedding=embeddings,
        persist_directory=str(
            persist_directory
        )
    )

    return vector_database, chunks


if __name__ == "__main__":

    project_root = Path(__file__).resolve().parents[2]

    documents_dir = (
        project_root
        / "data"
        / "documents"
    )

    persist_directory = (
        project_root
        / "data"
        / "processed"
        / "chroma_db"
    )

    vector_database, chunks = (
        build_vector_database(
            documents_dir,
            persist_directory
        )
    )

    print("\n===== RAG INGESTION =====")

    print(
        "Documents directory:",
        documents_dir
    )

    print(
        "Number of chunks:",
        len(chunks)
    )

    print(
        "Vector database:",
        persist_directory
    )

    print("\nSample chunk:")

    print(
        chunks[0].page_content[:500]
    )