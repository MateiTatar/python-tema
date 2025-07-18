import threading
import uuid
import queue
from typing import Dict, Any, Tuple, List, Optional
from app.math_ops import MathOps

class JobQueue:
    def __init__(self, cache, db):
        self.queue = queue.Queue()
        self.results: Dict[str, Dict[str, Any]] = {}  # job_id -> status/result
        self.cache = cache
        self.db = db
        self.thread = threading.Thread(target=self._worker, daemon=True)
        self.thread.start()

    def submit(self, op_type: str, operands: List[int]) -> str:
        job_id = str(uuid.uuid4())
        self.results[job_id] = {"status": "PENDING", "result": None, "error": None, "op_type": op_type, "operands": operands}
        self.queue.put((job_id, op_type, operands))
        return job_id

    def get_status(self, job_id: str) -> Dict[str, Any]:
        return self.results.get(job_id, {"status": "NOT_FOUND"})

    def _worker(self):
        while True:
            job_id, op_type, operands = self.queue.get()
            try:
                # Try cache first
                operands_tuple = tuple(operands)
                cached = self.cache.get(op_type, operands_tuple)
                if cached is not None:
                    result = cached
                else:
                    if op_type == "pow":
                        result = MathOps.pow(operands[0], operands[1])
                    elif op_type == "fibonacci":
                        result = MathOps.fibonacci(operands[0])
                    elif op_type == "factorial":
                        result = MathOps.factorial(operands[0])
                    else:
                        raise ValueError("Invalid operation")
                    self.cache.set(op_type, operands_tuple, result)
                self.results[job_id] = {
                    "status": "DONE", "result": result, "error": None, "op_type": op_type, "operands": operands
                }
                self.db.save_request(op_type, operands, result)
            except Exception as ex:
                self.results[job_id] = {
                    "status": "ERROR", "result": None, "error": str(ex), "op_type": op_type, "operands": operands
                }
