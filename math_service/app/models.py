from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime

class OperationRequest(BaseModel):
    op_type: str = Field(..., description="pow, fibonacci, factorial")
    operands: List[int]

class OperationResponse(BaseModel):
    result: Optional[int]
    op_type: str
    operands: List[int]
    timestamp: datetime = Field(default_factory=datetime.utcnow)

class JobStatusResponse(BaseModel):
    job_id: str
    status: str  # PENDING, DONE, ERROR
    result: Optional[int] = None
    error: Optional[str] = None
