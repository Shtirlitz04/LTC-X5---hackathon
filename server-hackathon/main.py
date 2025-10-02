from fastapi import FastAPI
from lifespan import lifespan
from api.routes import router
import uvicorn

app = FastAPI(
    title="Мой API-бэкенд",
    description="FastAPI с батчингом BERT и статикой",
    version="1.0.0",
    lifespan=lifespan
)

app.include_router(router)

if __name__ == "__main__":

    print("Start programm!")
    
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)