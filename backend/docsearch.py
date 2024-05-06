from fastapi import FastAPI, HTTPException
from langchain_community.document_loaders import TextLoader, DirectoryLoader
from langchain_community.vectorstores import FAISS
from langchain_text_splitters import CharacterTextSplitter
from langchain_community.embeddings import HuggingFaceEmbeddings
from fastapi.middleware.cors import CORSMiddleware
import time

embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
app = FastAPI()
origins = [
    "https://chat.openai.com",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["*"],
)

@app.get("/create-vector-db/")
def create_vector_db():
    
    loader = DirectoryLoader("./data")
    print(2)
    documents = loader.load()
    text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
    docs = text_splitter.split_documents(documents)
    embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
    db = FAISS.from_documents(docs, embeddings)
    print(db)
    db.save_local("faiss_index")
    return {"message": "Vector database created successfully."}
    
@app.get("/inference/")
async def inference(query: str):

    new_db = FAISS.load_local("faiss_index", embeddings, allow_dangerous_deserialization=True)
    docs_and_scores = new_db.similarity_search_with_score(query)
    if docs_and_scores[0][1] < 1:
        return {"response": True, "score": str(docs_and_scores[0][1])}
    return {"response": False, "score": str(docs_and_scores[0][1])}
    
if __name__ == "__main__":
    create_vector_db()
