from langchain_huggingface.embeddings import HuggingFaceEmbeddings
import os
from dotenv import load_dotenv

load_dotenv()

def get_huggingface_embedding(model_name=os.environ["EMBEDDING_MODEL_NAME"]):
    print(f"Loading model embedding {model_name}")
    return HuggingFaceEmbeddings(model_name=model_name)
if __name__ == "__main__":
    model = get_huggingface_embedding()
    print(model)