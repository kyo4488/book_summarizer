import openai
import os
import requests
import json

from dotenv import load_dotenv
from langchain_openai import OpenAIEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma, FAISS
from langchain.chains import RetrievalQA
from langchain_openai import ChatOpenAI

from scraper import scrape_book_content

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

embedding_model = "text-embedding-3-large"
model = "gpt-4o"

book_path = "./data/book.txt"

def extract_book(path: str):
    with open(path, "r") as file:
        return file.read()
    
def get_push_count():
    try:
        with open("push_count.json", "r") as f:
            data = json.load(f)
            return data["push_count"]
    except (FileNotFoundError, json.JSONDecodeError):
        return 0


def summarize(book_text):
    # チャンクの設定
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1500, chunk_overlap=200)

    # RAG用のドキュメントを作成
    documents = text_splitter.create_documents([book_text])

    # 埋め込みの作成
    embeddings = OpenAIEmbeddings(model=embedding_model)

    # 永続化されたベクトルストアを使用
    vectorstore = FAISS.from_documents(
        documents,
        embedding=embeddings,
    )

    # 検索の設定
    qa = RetrievalQA.from_chain_type(
        llm=ChatOpenAI(model_name=model, temperature=0),
        chain_type="stuff",
        retriever=vectorstore.as_retriever(search_kwargs={"k": 5}),
        return_source_documents=False,
    )
    push_count = get_push_count()
    print("push_count:", push_count)

    if push_count <= 2:
        query = "与えられた本の内容を非常に短めに要約してください"
    elif push_count <= 5:
        query = "与えられた本の内容を短めに要約してください。"
    elif push_count<= 10:
        query = "与えられた本の内容を要約してください。"
    elif push_count <= 15:
        query = "与えられた本の内容を長めに要約してください。"
    else:
        query = "与えられた本の内容を非常に長めに要約してください。"
        
    print(query)
    output = qa.invoke(query)

    print("Summary of the Book:")
    print(output["result"])
    return output["result"]


if __name__ == "__main__":
    summarize(6)