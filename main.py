import warnings
from contextlib import asynccontextmanager

from fastapi import FastAPI
from pydantic import BaseModel

from ai_service import AIServices
from database import VectorStore
from settings import configs

warnings.filterwarnings("ignore", category=UserWarning, module="pydantic")


class QueryRequest(BaseModel):
    query: str


class ResponseModel(BaseModel):
    articals: list
    summary: str


app = FastAPI()


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Initialize connections when the service starts and clean up on shutdown"""
    try:
        persist_dir = configs.get("CHROMA_PERSIST_DIR", "./chroma_db")
        vector_store = VectorStore(persist_directory=persist_dir)

        if vector_store.health_check():
            print("Vector store connection established successfully")
        else:
            print("Vector store health check failed")
            raise RuntimeError("Failed to establish vector store connection")
        yield
    except Exception as e:
        print(f"Failed to initialize services: {e}")
        raise


app.router.lifespan_context = lifespan


def summa_reponse_generator():
    articals = [
        "Article 1: Sky News launches new AI-driven news platform.",
        "Article 2: Advances in AI technology reshape media landscape.",
        "Article 3: Ethical considerations in AI-generated content.",
    ]
    summary = "Sky News is leveraging AI to enhance news delivery, raising important ethical questions."
    return ResponseModel(articals=articals, summary=summary)


@app.get("/")
async def root():
    return {"message": "WELCOME TO SKY NEWS RAG SYSTEM"}


@app.get("/api/v1/health")
async def health_check():
    return {"status": "ok"}


@app.post("/api/v1/query")
async def handle_query(request: QueryRequest):
    query = request.query
    sky_ai = AIServices()
    response = sky_ai.generate_summary(query)
    return response
