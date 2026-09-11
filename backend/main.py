from fastapi import FastAPI, BackgroundTasks, HTTPException
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
from models import ResearchRequest, ResearchJob, ProductOpportunity
from database import SessionLocal
from services import run_research
import uuid
from product_generator import generate_product
from pdf_generator import create_pdf

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def home():
    return {"message": "Niched backend is running"}


@app.get("/health")
def health_check():
    return {"status": "healthy", "service": "niched-backend"}


@app.post("/research")
async def research(request: ResearchRequest, background_tasks: BackgroundTasks):
    job_id = str(uuid.uuid4())
    job = ResearchJob(id=job_id, seed=request.seed, status="running")
    db = SessionLocal()

    db.add(job)
    db.commit()
    db.close()
    background_tasks.add_task(run_research, job_id, request.seed)

    return {"job_id": job_id, "status": "running"}


@app.get("/research/{job_id}")
def get_research(job_id: str):
    db = SessionLocal()

    job = db.query(ResearchJob).filter(ResearchJob.id == job_id).first()

    if not job:
        db.close()
        raise HTTPException(status_code=404, detail="Research job not found")

    result = {
        "job_id": job.id,
        "seed": job.seed,
        "status": job.status,
        "result": job.result,
        "error": job.error,
    }

    db.close()

    return result


@app.post("/products")
def create_product(opportunity: ProductOpportunity):
    product = generate_product(opportunity)

    filename = f"{product.title.replace(' ', '_')}.pdf"

    create_pdf(product, filename)

    return {
        "title": product.title,
        "filename": filename,
        "product": product.model_dump(),
    }

@app.get("/products/download/{filename}")
def download_product(filename: str):
    file_path = f"./{filename}"

    return FileResponse(
        path=file_path,
        media_type="application/pdf",
        filename=filename
    )