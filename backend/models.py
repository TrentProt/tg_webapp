from pydantic import BaseModel

from typing import List


class Container(BaseModel):
    id: int
    name: str
    price: int
    description: str
    image: List[str]
