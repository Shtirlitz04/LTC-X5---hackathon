import asyncio
import time
from typing import List, Dict, Any, Callable

class DynamicBatcher:
    def __init__(
        self,
        predict_fn: Callable[[List[str]], List[List[Dict[str, Any]]]],
        batch_size: int = 8,
        max_wait: float = 0.5
    ):
        self.predict_fn = predict_fn
        self.batch_size = batch_size
        self.max_wait = max_wait
        self.queue = asyncio.Queue()
        self._task = None

    async def start(self):
        self._task = asyncio.create_task(self._run())

    async def stop(self):
        if self._task:
            self._task.cancel()
            try:
                await self._task
            except asyncio.CancelledError:
                pass

    async def submit(self, text: str):
        future = asyncio.Future()
        await self.queue.put((text, future))
        return await future

    async def _run(self):
        while True:
            batch, futures = [], []
            text, future = await self.queue.get()
            batch.append(text)
            futures.append(future)

            deadline = time.time() + self.max_wait
            while len(batch) < self.batch_size and time.time() < deadline:
                try:
                    text, future = await asyncio.wait_for(
                        self.queue.get(),
                        timeout=deadline - time.time()
                    )
                    batch.append(text)
                    futures.append(future)
                except asyncio.TimeoutError:
                    break

            loop = asyncio.get_running_loop()
            try:
                predictions = await loop.run_in_executor(None, self.predict_fn, batch)
                for fut, pred in zip(futures, predictions):
                    if not fut.done():
                        fut.set_result(pred)
            except Exception as e:
                for fut in futures:
                    if not fut.done():
                        fut.set_exception(e)
                        