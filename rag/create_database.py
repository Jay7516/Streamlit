from langchain_community.document_loaders import DirectoryLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter

from langchain.schema import Document
from langchain.document_loaders.pdf import PyPDFDirectoryLoader
from langchain_chroma import Chroma
from rag.get_embedding_function import get_embedding_function
from dotenv import load_dotenv
import os
import shutil
import argparse
CHROMA_PATH = "chroma"
PATHS = ["books","board_games"]
DATA_PATH = f"data/{PATHS[1]}"
load_dotenv()


def main():
    # Check if the database should be cleared (using the --clear flag).
    parser = argparse.ArgumentParser()
    parser.add_argument("--reset", action="store_true", help="Reset the database.")
    args = parser.parse_args()
    if args.reset:
        print("✨ Clearing Database")
        clear_database()
    generate_data_store()

def generate_data_store() -> None:
    documents = load_documents()
    chunks = split_text(documents)
    save_to_chroma(chunks)
def load_documents() -> list[Document]:
    #document_loader = DirectoryLoader(DATA_PATH,glob="*.md")
    document_loader = PyPDFDirectoryLoader(DATA_PATH)
    return document_loader.load()

def split_text(documents: list[Document]):
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=800,
        chunk_overlap=80,
        length_function=len,
        #add_start_index=True,
        is_separator_regex=False
    )
    # 300 100 800 80 1000 500
    chunks = text_splitter.split_documents(documents)
    print(f"Split {len(documents)} documents into {len(chunks)} chunks.")
    return chunks
    # document = chunks[10]
    # document1 = chunks[11]
    # print(document.page_content)
    # print("BLANK")
    # print(document1.page_content)
    # print(document.metadata)



# def save_to_chroma(chunks: list[Document]):
#     # Clear out the database first.
#     clear_database()

#     #embedding_function = SentenceTransformerEmbeddings(model_name="all-MiniLM-L6-v2")
#     # Create a new DB from the documents.
#     db = Chroma.from_documents(
#         chunks, get_embedding_function, persist_directory=CHROMA_PATH
#     )
#     db.persist()
#     print(f"Saved {len(chunks)} chunks to {CHROMA_PATH}.")
def save_to_chroma(chunks: list[Document]):
    # Load the existing database.
    db = Chroma(
        persist_directory=CHROMA_PATH, embedding_function=get_embedding_function()
    )

    # Calculate Page IDs.
    chunks_with_ids = calculate_chunk_ids(chunks)

    # Add or Update the documents.
    existing_items = db.get(include=[])  # IDs are always included by default
    existing_ids = set(existing_items["ids"])
    print(f"Number of existing documents in DB: {len(existing_ids)}")

    # Only add documents that don't exist in the DB.
    new_chunks = []
    for chunk in chunks_with_ids:
        if chunk.metadata["id"] not in existing_ids:
            new_chunks.append(chunk)

    if len(new_chunks):
        print(f"👉 Adding new documents: {len(new_chunks)}")
        new_chunk_ids = [chunk.metadata["id"] for chunk in new_chunks]
        db.add_documents(new_chunks, ids=new_chunk_ids)
        #db.persist()
    else:
        print("✅ No new documents to add")


def calculate_chunk_ids(chunks):

    # This will create IDs like "data/monopoly.pdf:6:2"
    # Page Source : Page Number : Chunk Index

    last_page_id = None
    current_chunk_index = 0

    for chunk in chunks:
        source = chunk.metadata.get("source")
        page = chunk.metadata.get("page")
        current_page_id = f"{source}:{page}"

        # If the page ID is the same as the last one, increment the index.
        if current_page_id == last_page_id:
            current_chunk_index += 1
        else:
            current_chunk_index = 0

        # Calculate the chunk ID.
        chunk_id = f"{current_page_id}:{current_chunk_index}"
        last_page_id = current_page_id

        # Add it to the page meta-data.
        chunk.metadata["id"] = chunk_id

    return chunks

def clear_database():
    if os.path.exists(CHROMA_PATH):
        shutil.rmtree(CHROMA_PATH)
if __name__ == "__main__":
    main()