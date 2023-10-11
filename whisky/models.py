from typing import Optional
from pydantic import BaseModel

class Whisky(BaseModel):
    id: Optional[int] = None
    name: str
    age: int
    type: str