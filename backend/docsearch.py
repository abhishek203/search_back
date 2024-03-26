from fastapi import FastAPI, HTTPException
import os
import dotenv
from langchain_community.document_loaders import TextLoader, DirectoryLoader
from langchain_community.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings
from langchain_text_splitters import CharacterTextSplitter

dotenv.load_dotenv()
os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")

app = FastAPI()

@app.post("/create-vector-db/")
async def create_vector_db():
    try:
        loader = DirectoryLoader("./data")
        documents = loader.load()
        text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
        docs = text_splitter.split_documents(documents)
        embeddings = OpenAIEmbeddings()
        db = FAISS.from_documents(docs, embeddings)
        db.save_local("faiss_index")
        return {"message": "Vector database created successfully."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/inference/")
async def inference(query: str):
    try:
        embeddings = OpenAIEmbeddings()
        new_db = FAISS.load_local("faiss_index", embeddings, allow_dangerous_deserialization=True)
        docs_and_scores = new_db.similarity_search_with_score(query)
        if docs_and_scores[0][1] < 0.5:
            return {"match": True, "score": str(docs_and_scores[0][1])}
        return {"match": False, "score": str(docs_and_scores[0][1])}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
