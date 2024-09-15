from dotenv import load_dotenv
import os
from typing import List
from prepare_data import load_data
from langchain_core.documents import Document
from langchain_core.embeddings import Embeddings
from langchain_community.vectorstores import FAISS
from langchain.text_splitter import RecursiveCharacterTextSplitter
import numpy as np
import faiss
from embedding import get_huggingface_embedding

def save_vector_db(
    documents: List[Document],
    embedding: Embeddings,
    path=os.environ["VECTOR_DATABASE_PATH"],
) -> FAISS:
    vector_store = FAISS.from_documents(
        documents=documents, 
        embedding=embedding
    )
    vector_store.save_local(path)
    return vector_store

if __name__ == "__main__":
    embedding = get_huggingface_embedding()
    documents = load_data("./datapickle/all_commands.pkl")
    print(documents[0])
    save_vector_db(documents, embedding, path="./faiss/data")
   
