from pydantic import BaseModel
from typing import Optional

class RequestModel(BaseModel):
    message: str
    level: Optional[str] = None
    service: str