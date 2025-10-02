from contextlib import asynccontextmanager
from fastapi import FastAPI
from model import load_model
from batcher import DynamicBatcher

_model_predict = None
_batcher = None

@asynccontextmanager
async def lifespan(app: FastAPI):

    global _model_predict, _batcher

    # --- Startup ---
    _model_predict = load_model()

    _batcher = DynamicBatcher(
        predict_fn=_model_predict,
        batch_size=8,
        max_wait=0.05
    )
    await _batcher.start()

    app.state.batcher = _batcher

    yield  # ← приложение работает

    # --- Shutdown ---
    await _batcher.stop()
    print("🛑 Batcher остановлен")