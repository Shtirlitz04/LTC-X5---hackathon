from fastapi import APIRouter, Request
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from schemas import PredictRequest, EntityResponse, HealthResponse

router = APIRouter()

router.mount("/static", StaticFiles(directory="static"), name="static")

@router.get("/")
async def read_index():
    return FileResponse("static/index.html")

@router.get("/about")
async def read_about():
    return FileResponse("static/about.html")

@router.get("/health", response_model=HealthResponse)
async def health():
    return {"status": "ok"}

@router.get("/api/data")
async def get_data():
    return {
        "message": "Привет из FastAPI!",
        "items": ["яблоко", "банан", "апельсин"],
        "status": "success"
    }

@router.post("/api/predict", response_model=list[EntityResponse])
async def predict(request: PredictRequest, req: Request):
    batcher = req.app.state.batcher
    result = await batcher.submit(request.input)
    return result