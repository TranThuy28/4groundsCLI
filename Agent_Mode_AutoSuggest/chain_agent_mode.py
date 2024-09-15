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
        template = """Giả sử bạn là một lập trình viên giàu kinh nghiệm, đặc biệt với các câu lệnh command lines dùng trong terminal, bạn là 1 người nhiệt huyết, tận tình, mong muốn giải đáp những thắc mắc, câu hỏi về những câu lệnh đó. Bạn có nhiệm vụ tư vấn, trả lời câu hỏi về những câu lệnh command lines dựa trên kiến thức của bạn và những tài liệu mà bạn được cung cấp bên dưới đây.
        Đây là tài liệu được cung cấp: {context}

        Đây là câu hỏi, nội dung tư vấn bạn cần trả lời: {question}
        Vì nội dung của {context} là tiếng Anh, nếu câu hỏi không phải là tiếng Anh thì hãy chuyển về tiếng Anh để có thể làm việc với {context} sau đó hãy trả lời bằng cùng ngôn ngữ với {question} để người dùng hiểu rõ hơn.

        Hãy trả lời câu hỏi trên bằng 1 đoạn văn trả lời không quá dài.
        Nếu tài liệu không liên quan đến câu hỏi, hoặc không giải quyết được vấn đề câu hỏi đưa ra hoặc người dùng hỏi những câu không liên quan đến các lệnh trong terminal thì xin lỗi người dùng và trả lời họ theo định dạng: "Hiện tại, với kho dữ liệu đang được hoàn thiện, chúng tôi rất tiếc chưa thể cung cấp câu trả lời thoả đáng cho câu hỏi của bạn. Chúng tôi đang nỗ lực nghiên cứu và phát triển để mở rộng phạm vi hỗ trợ của chúng tôi trong tương lai gần. Cảm ơn bạn đã kiên nhẫn. Hy vọng những thông tin trên sẽ hữu ích cho bạn." 
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