# from dotenv import load_dotenv
# import os
# from langchain_pinecone import PineconeVectorStore
# from langchain_groq import ChatGroq
# from langchain.chains import create_retrieval_chain
# from langchain.chains.combine_documents import create_stuff_documents_chain
# from langchain_core.prompts import ChatPromptTemplate
# from flask import Flask, render_template, jsonify, request
# from src.helper import download_embeddings
# from src.prompt import *

# app = Flask(__name__)

# load_dotenv()

# PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")
# OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# os.environ["PINECONE_API_KEY"] = PINECONE_API_KEY
# os.environ["OPENAI_API_KEY"] = OPENAI_API_KEY

# embedding = download_embeddings()

# index_name = "medical-chatbot"

# docsearch = PineconeVectorStore.from_existing_index(
#     index_name="medical-chatbot",
#     embedding=embedding
# )

# retriever = docsearch.as_retriever(search_type="similarity", search_kwargs={"k": 3})
# chatModel = ChatGroq(
#     model="llama-3.3-70b-versatile",
#     api_key=OPENAI_API_KEY,
#     temperature=0.2
# )
# prompt = ChatPromptTemplate.from_messages(
#     [
#         ("system", system_prompt),
#         ("human", "{input}")
#     ]
# )
# question_answer_chain = create_stuff_documents_chain(chatModel, prompt)
# rag_chain = create_retrieval_chain(retriever, question_answer_chain)

from dotenv import load_dotenv
import os

print("STEP 1: Imports starting")

from langchain_pinecone import PineconeVectorStore
print("STEP 2: Pinecone imported")

from langchain_groq import ChatGroq
print("STEP 3: Groq imported")

from langchain.chains import create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_core.prompts import ChatPromptTemplate
from flask import Flask, render_template, jsonify, request

print("STEP 4: Flask and LangChain imported")

from src.helper import download_embeddings
from src.prompt import *

print("STEP 5: Helper imported")

app = Flask(__name__)

load_dotenv()

print("STEP 6: Environment loaded")

PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

print("STEP 7: Keys loaded")

os.environ["PINECONE_API_KEY"] = PINECONE_API_KEY
os.environ["OPENAI_API_KEY"] = OPENAI_API_KEY

# print("STEP 8: Creating embeddings")

# embedding = download_embeddings()

# print("STEP 9: Embeddings created")

# docsearch = PineconeVectorStore.from_existing_index(
#     index_name="medical-chatbot",
#     embedding=embedding
# )

# print("STEP 10: Pinecone connected")

# retriever = docsearch.as_retriever(
#     search_type="similarity",
#     search_kwargs={"k": 3}
# )

# print("STEP 11: Retriever created")

# chatModel = ChatGroq(
#     model="llama-3.3-70b-versatile",
#     api_key=OPENAI_API_KEY,
#     temperature=0.2
# )

# print("STEP 12: Groq model created")

# prompt = ChatPromptTemplate.from_messages(
#     [
#         ("system", system_prompt),
#         ("human", "{input}")
#     ]
# )

# print("STEP 13: Prompt created")

# question_answer_chain = create_stuff_documents_chain(
#     chatModel,
#     prompt
# )

# print("STEP 14: QA chain created")

# rag_chain = create_retrieval_chain(
#     retriever,
#     question_answer_chain
# )

# print("STEP 15: RAG chain created")

rag_chain = None

def get_rag_chain():
    global rag_chain

    if rag_chain is None:

        print("Creating embeddings...")
        embedding = download_embeddings()

        print("Connecting Pinecone...")
        docsearch = PineconeVectorStore.from_existing_index(
            index_name="medical-chatbot",
            embedding=embedding
        )

        retriever = docsearch.as_retriever(
            search_type="similarity",
            search_kwargs={"k": 3}
        )

        chatModel = ChatGroq(
            model="llama-3.3-70b-versatile",
            api_key=GROQ_API_KEY,
            temperature=0.2
        )

        prompt = ChatPromptTemplate.from_messages(
            [
                ("system", system_prompt),
                ("human", "{input}")
            ]
        )

        question_answer_chain = create_stuff_documents_chain(
            chatModel,
            prompt
        )

        rag_chain = create_retrieval_chain(
            retriever,
            question_answer_chain
        )

        print("RAG chain ready")

    return rag_chain

@app.route("/")
def index():
    return render_template("chat.html")

# @app.route("/get",methods=["GET", "POST"])
# def chat():
#     msg = request.form["msg"]
#     input = msg
#     print(input)
#     response = rag_chain.invoke({"input": msg})
#     print("Response: ", response["answer"])
#     return str(response["answer"])

@app.route("/get", methods=["GET", "POST"])
def chat():
    msg = request.form["msg"]

    chain = get_rag_chain()

    response = chain.invoke({"input": msg})

    return str(response["answer"])



if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)


# from flask import Flask

# app = Flask(__name__)

# @app.route("/")
# def home():
#     return "Medi-Bot is running!"

# if __name__ == "__main__":
#     app.run(host="0.0.0.0", port=8080)