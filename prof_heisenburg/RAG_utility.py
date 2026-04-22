from dotenv import load_dotenv
from langchain_text_splitters import RecursiveCharacterTextSplitter
import os 
from langchain_community.document_loaders import DirectoryLoader, PyPDFLoader
from langchain_ollama import OllamaEmbeddings
from langchain_chroma import Chroma
from langchain_classic.chains import RetrievalQA
#loading embedding model
embedding_model = OllamaEmbeddings(
        model = "mxbai-embed-large:335m",

    )
#loading the paths for pdfs and vectordb
load_dotenv()
pdfs_path = os.getenv("path_of_pdf")
vector_db_path = os.getenv("path_of_vector_db")

def document_ingestion():
    #--------------first step is to load ncert pdfs and convert them into text-------------
    #initialize loader
    loader = DirectoryLoader(
        path = pdfs_path,
        glob ="**/*.pdf",
        loader_cls=PyPDFLoader

    )
    #extracted data
    extracted_data = loader.load()

    #---------------second step si to convert this data into chunks------------------
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size = 500,#max number of chars in one cunk
        chunk_overlap = 150 #chars overlapping in [revious and next chunk]
        )

    text_chunks = text_splitter.split_documents(extracted_data)

    #--------------third step is to store this text in vector db-------------------------
    
    #loading vector_db
    vector_db = Chroma.from_documents(
        collection_name="ncert_book_collection",
        persist_directory=vector_db_path,
        documents=text_chunks,
        embedding=embedding_model 
    )

    return vector_db

#-------------------next step is retrieval -----------------------------
def retrieval_process(vector_db,user_prompt,llm):
    # calling reteriver
    retriever = vector_db.as_retriever(
        search_type = "similarity"
    )

    qa_chain = RetrievalQA.from_chain_type(
    llm = llm,
    retriever = retriever,
    return_source_documents = True
    )
    response = qa_chain.invoke({"query":user_prompt})

    return response

#-------------------function to load vector_db once created-----------------
def load_vector_db():

    vector_db = Chroma(
    collection_name="ncert_book_collection",
    embedding_function=embedding_model,
    persist_directory=vector_db_path
)
    return vector_db





