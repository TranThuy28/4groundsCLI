import os
from dotenv import load_dotenv
from pydantic import BaseModel
from chain_auto_suggest import BasicRAG, AdvanceMultiQueryRAG
from retriever import get_retriever
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_huggingface import HuggingFaceEmbeddings

embedding = HuggingFaceEmbeddings(model_name=os.environ["EMBEDDING_MODEL_NAME"])
retrievers = get_retriever(source="data", embedding=embedding)
gg_llm = ChatGoogleGenerativeAI(model="gemini-1.5-pro", temperature=0)
basicrag = BasicRAG(retrievers, gg_llm)
print(basicrag.answer(question="git comm"))