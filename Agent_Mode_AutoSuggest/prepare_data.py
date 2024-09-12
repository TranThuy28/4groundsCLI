from langchain_community.document_loaders import Docx2txtLoader
from langchain_core.documents import Document
import pickle
from typing import List


def load_docx(file_path) -> List[Document]:
    """Load documents from file .docx"""
    loader = Docx2txtLoader(file_path)
    documents = loader.load()
    return documents


def split_text_by_line(text: str) -> List[Document]:
    """Chia văn bản thành từng dòng, mỗi Document chứa 1 dòng"""
    lines = text.split("\n")
    result = []
    for line in lines:
        line = line.strip()
        if line:  
            result.append(Document(page_content=line))
    return result


def save_2_pickle(documents: List[Document], file_path: str):
    """Lưu danh sách Document vào file pickle"""
    with open(file_path, "wb") as file:
        pickle.dump(documents, file)

def load_data(file_path: str) -> List[Document]:
    with open(file_path, "rb") as file:
        documents = pickle.load(file)
    return documents

def prepare(file_path: str, file_destination_path: str):
    """Chuẩn bị và lưu dữ liệu từ file .docx vào pickle"""
    document = load_docx(file_path)
    print(f"Loaded data from {file_path}")
    documents = split_text_by_line(document[0].page_content)
    print(f"Split into {len(documents)} chunks")
    save_2_pickle(documents, file_destination_path)
    print(f"Saved to {file_destination_path}")


if __name__ == "__main__":
    prepare(
        "./git_commands.docx",
        "./datapickle/git_commands.pkl",
    )
