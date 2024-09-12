import os
from operator import itemgetter
from dotenv import load_dotenv
from retriever import get_retriever
from typing import List, Literal
from langchain_core.pydantic_v1 import BaseModel, Field
from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate

from langchain_huggingface.embeddings import HuggingFaceEmbeddings
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from langchain_core.vectorstores import VectorStoreRetriever
from langchain_core.documents import Document
from langchain_core.embeddings import Embeddings
from langchain_core.language_models import LLM
from langchain_community.vectorstores import FAISS

from langchain_google_genai import ChatGoogleGenerativeAI

load_dotenv()

def format_docs(docs: Document):
    def get_content(doc: Document):
        res = doc.page_content
        
        return res
    return "\n\n".join(
        get_content(doc) if isinstance(doc, Document) else get_content(doc[0])
        for doc in docs
    )

class BasicRAG:
    def __init__(self, retriever: VectorStoreRetriever, llm):
        self.retriever = retriever
        self.llm = llm
        template = """Giả sử bạn là một lập trình viên giàu kinh nghiệm, đặc biệt với các câu lệnh command lines dùng trong terminal.
        Đây là tài liệu được cung cấp: {context}
        Đây là những kí tự đầu của 1 lệnh command lines: {question}
        Dựa vào những kí tự đầu {question}, hãy đưa ra đầy đủ câu lệnh command lines đó.

        
        Nếu kí tự đầu vào không thể là bất kì lệnh command lines nào, thì không trả về gì cả. 
        """
        self.prompt = ChatPromptTemplate.from_template(template)
        self.chain = (
            {"context": self.retriever | format_docs, "question": RunnablePassthrough()}
            | self.prompt
            | self.llm
            | StrOutputParser()
        )

    def answer(self, question: str) -> str:
        return self.chain.invoke(question)


class AdvanceMultiQueryRAG:
    """Multi-Query + Semantic Routing"""
    def __init__(self, retrievers: dict[str, VectorStoreRetriever], llm):
        # Load all retrivers
        self.retrievers = retrievers
        self.llm = llm
        # Load route prompt
        template = """Bạn là một trợ lý ngôn ngữ AI. Nhiệm vụ của bạn là tạo ra năm phiên bản khác nhau của câu hỏi người dùng đã đưa ra để truy xuất các tài liệu liên quan từ cơ sở dữ liệu vector. Bằng cách tạo ra nhiều góc nhìn khác nhau về câu hỏi của người dùng, mục tiêu của bạn là giúp người dùng vượt qua một số hạn chế của tìm kiếm tương tự dựa trên khoảng cách. Cung cấp các câu hỏi thay thế này cách nhau bằng dấu xuống dòng. Đây là câu hỏi gốc: {question}"""
        self.multiquery_prompt = ChatPromptTemplate.from_template(template)
        self.chain = (
            self.multiquery_prompt
            | ChatOpenAI(temperature=0)
            | StrOutputParser()
            | (lambda x: x.split("\n"))
        )

    def answer(self, question: str) -> str:
        questions = self.chain.invoke({"question": question})


if __name__ == "__main__":
    pass