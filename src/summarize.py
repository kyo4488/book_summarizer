import openai
import os

from dotenv import load_dotenv
from langchain_openai import OpenAIEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain.chains import RetrievalQA
from langchain_openai import ChatOpenAI

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

embedding_model = "text-embedding-3-large"
model = "gpt-4o"

book_path = "./data/book.txt"

def extract_book(path: str):
    with open(path, "r") as file:
        return file.read()

def summarize(push_count=5):
    # テキストの読み込み
    book_text = extract_book(book_path)
    # チャンクの設定
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1500,
        chunk_overlap=200
    )

    # RAG用のドキュメントを作成
    documents = text_splitter.create_documents([book_text])

    # 埋め込みの作成
    embeddings = OpenAIEmbeddings(model=embedding_model)
    vectorstore = Chroma.from_documents(documents, embedding=embeddings)

    # 検索の設定
    qa = RetrievalQA.from_chain_type(
        llm=ChatOpenAI(model_name=model, temperature=0),
        chain_type="stuff",
        retriever=vectorstore.as_retriever(search_kwargs={"k": 5}),
        return_source_documents=False
    )

    if push_count <= 2:
        query = "与えられた本の内容を短めに要約してください。"
    elif push_count<= 4:
        query = "与えられた本の内容を要約してください。"
    else:
        query = "与えられた本の内容を長めに要約してください。"
        
    print(query)
    output = qa.invoke(query)

    print("Summary of the Book:")
    print(output["result"])

if __name__ == "__main__":
    summarize(6)