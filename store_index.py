# from dotenv import load_dotenv
# import os
# from pinecone import Pinecone
# from pinecone import ServerlessSpec
# from langchain_pinecone import PineconeVectorStore

# from src.helper import load_pdf_files, filter_to_minimal_docs, text_split, download_embeddings

# load_dotenv()


# PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")
# OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# os.environ["PINECONE_API_KEY"] = PINECONE_API_KEY
# os.environ["OPENAI_API_KEY"] = OPENAI_API_KEY

# extracted_data=load_pdf_files(data='data/')
# filter_data = filter_to_minimal_docs(extracted_data)
# text_chunks=text_split(filter_data)

# embedding = download_embeddings()


# pinecone_api_key = PINECONE_API_KEY

# pc = Pinecone(api_key = pinecone_api_key)   

# index_name = "medical-chatbot"


# if index_name not in pc.list_indexes():
#     pc.create_index(name=index_name, dimension=384, metric="cosine", spec=ServerlessSpec(cloud="aws", region="us-east-1"))
# index = pc.Index(index_name)



# docsearch = PineconeVectorStore.from_documents(
#     documents=text_chunks,
#     embedding=embedding,
#     index_name="medical-chatbot"
# )

from dotenv import load_dotenv
import os
from pinecone import Pinecone, ServerlessSpec
from langchain_pinecone import PineconeVectorStore

from src.helper import (
    load_pdf_files,
    filter_to_minimal_docs,
    text_split,
    download_embeddings
)

load_dotenv()

PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")

pc = Pinecone(api_key=PINECONE_API_KEY)

index_name = "medical-chatbot"

if index_name not in pc.list_indexes().names():
    pc.create_index(
        name=index_name,
        dimension=384,
        metric="cosine",
        spec=ServerlessSpec(
            cloud="aws",
            region="us-east-1"
        )
    )

extracted_data = load_pdf_files("data/")
filtered_data = filter_to_minimal_docs(extracted_data)
text_chunks = text_split(filtered_data)

embedding = download_embeddings()

PineconeVectorStore.from_documents(
    documents=text_chunks,
    embedding=embedding,
    index_name=index_name
)

print(f"Successfully uploaded {len(text_chunks)} chunks to Pinecone")