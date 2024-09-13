from langchain_core.embeddings import Embeddings
from langchain_community.vectorstores import FAISS
from embedding import get_huggingface_embedding


def get_retriever(source: str, embedding: Embeddings):
    return FAISS.load_local(
        f"./faiss/{source}",
        embedding,
        allow_dangerous_deserialization=True,
    ).as_retriever()

def get_vectorstrore(source: str, embedding: Embeddings):
    return FAISS.load_local(
        f"./faiss/{source}",
        embedding,
        allow_dangerous_deserialization=True,
    )
def normalize_scores(relevant_documents):
    scores = [score for _, score in relevant_documents]
    min_score = min(scores)
    max_score = max(scores)
    
    normalized_documents = []
    for doc, score in relevant_documents:
        # Chuẩn hóa score từ 0 đến 1
        normalized_score = (score - min_score) / (max_score - min_score)
        normalized_documents.append((doc, normalized_score))
    
    return normalized_documents



if __name__ == "__main__":
    embedding = get_huggingface_embedding()
    vectorstore = get_vectorstrore("data", embedding)
    relevant_documents = vectorstore.similarity_search_with_relevance_scores(
        "What is the command to list all files in a directory?",
    )
    normalized_documents = normalize_scores(relevant_documents)
    
    
    for doc, score in normalized_documents:
        print(f"Document: {doc.page_content}, Score: {score}")
        print()