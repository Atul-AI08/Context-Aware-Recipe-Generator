import os
import chromadb
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import PyPDFLoader
from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings


def load_chunk_persist_pdf():
    pdf_folder_path = "docs/"
    documents = []
    for file in os.listdir(pdf_folder_path):
        if file.endswith(".pdf"):
            pdf_path = os.path.join(pdf_folder_path, file)
            loader = PyPDFLoader(pdf_path)
            documents.extend(loader.load())
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=20)
    chunked_documents = text_splitter.split_documents(documents)
    client = chromadb.Client()
    if client.list_collections():
        consent_collection = client.create_collection("test")
    else:
        print("Collection already exists")

    embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
    vectordb = Chroma.from_documents(
        documents=chunked_documents,
        embedding=embeddings,
        persist_directory="chroma_store",
        collection_name="test",
    )
    return vectordb


if __name__ == "__main__":
    vectorstore = load_chunk_persist_pdf()
    matching_docs = vectorstore.similarity_search(
        "What are some milk alternatives?", k=2
    )
    for doc in matching_docs:
        print(doc.page_content)
        print("--------------------------------------------------------")
