import openai
import os

from dotenv import load_dotenv
from langchain_openai import OpenAIEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma, FAISS
from langchain.chains import RetrievalQA
from langchain_openai import ChatOpenAI

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

embedding_model = "text-embedding-3-small"
model = "gpt-4o-mini"

book_path = "./data/book.txt"


def extract_book(path: str):
    with open(path, "r") as file:
        return file.read()


# DBの保存先
chroma_persist_dir = "./chroma_db"


def initialize_qa():
    # テキストの読み込み
    book_text = extract_book(book_path)

    # チャンクの設定
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1500, chunk_overlap=200)

    # RAG用のドキュメントを作成
    documents = text_splitter.create_documents([book_text])

    # 埋め込みの作成
    embeddings = OpenAIEmbeddings(model=embedding_model)

    # 永続化されたベクトルストアを使用
    vectorstore = Chroma.from_documents(
        documents, embedding=embeddings, persist_directory=chroma_persist_dir
    )
    vectorstore.persist()

    # 検索の設定
    qa = RetrievalQA.from_chain_type(
        llm=ChatOpenAI(model_name=model, temperature=0),
        chain_type="stuff",
        retriever=vectorstore.as_retriever(search_kwargs={"k": 5}),
        return_source_documents=False,
    )
    return qa


def summarize():
    qa = initialize_qa()

    query = "与えられた本の内容を要約してください。"
    output = qa.invoke(query)

    print("Summary of the Book:")
    print(output["result"])
    return output


# webからのテスト用
def summarize_from_web(book_text):

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

    query = "与えられた本の内容を要約してください。"
    output = qa.invoke(query)

    print("Summary of the Book:")
    print(output["result"])
    return output["result"]


if __name__ == "__main__":
    summarize()
