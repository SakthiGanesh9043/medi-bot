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

# @app.route("/")
# def index():
#     return render_template("chat.html")

# @app.route("/get",methods=["GET", "POST"])
# def chat():
#     msg = request.form["msg"]
#     input = msg
#     print(input)
#     response = rag_chain.invoke({"input": msg})
#     print("Response: ", response["answer"])
#     return str(response["answer"])




# if __name__ == "__main__":
#     port = int(os.environ.get("PORT", 8080))
#     app.run(host="0.0.0.0", port=port)


from flask import Flask

app = Flask(__name__)

@app.route("/")
def home():
    return "Medi-Bot is running!"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)