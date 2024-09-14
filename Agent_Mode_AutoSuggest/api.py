import os
from fastapi import FastAPI
from pydantic import BaseModel
from dotenv import load_dotenv
from chain_auto_suggest import BasicRAG as AutoSuggestRAG
from chain_agent_mode import BasicRAG as AgentRAG
from retriever import get_retriever
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_huggingface import HuggingFaceEmbeddings
from fastapi.middleware.cors import CORSMiddleware  # Thêm thư viện CORSMiddleware

# Load environment variables
load_dotenv()

# Khởi tạo ứng dụng FastAPI
app = FastAPI()

# Thêm middleware CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Cho phép tất cả các nguồn, có thể thay đổi thành danh sách các domain cụ thể
    allow_credentials=True,
    allow_methods=["*"],  # Cho phép tất cả các phương thức HTTP (GET, POST, PUT, DELETE...)
    allow_headers=["*"],  # Cho phép tất cả các headers
)

# Model để nhận input từ người dùng
class QueryRequest(BaseModel):
    question: str

# Khởi tạo các thành phần của hệ thống cho auto-suggest
embedding = HuggingFaceEmbeddings(model_name=os.environ["EMBEDDING_MODEL_NAME"])
retrievers = get_retriever(source="data", embedding=embedding)
gg_llm = ChatGoogleGenerativeAI(model="gemini-1.5-pro", temperature=0)
auto_suggest_rag = AutoSuggestRAG(retrievers, gg_llm)

# Khởi tạo các thành phần của hệ thống cho agent mode
agent_rag = AgentRAG(retrievers, gg_llm)

# Định nghĩa endpoint FastAPI cho auto-suggest
@app.post("/auto/")
async def ask_auto_suggest_question(query: QueryRequest):
    answer = auto_suggest_rag.answer(query.question)
    return {"answer": answer}

# Định nghĩa endpoint FastAPI cho agent mode
@app.post("/agent/")
async def ask_agent_question(query: QueryRequest):
    answer = agent_rag.answer(query.question)
    return {"answer": answer}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("test:app", host="127.0.0.1", port=8000, reload=True)
