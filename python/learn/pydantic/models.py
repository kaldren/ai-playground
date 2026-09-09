"""Basic Pydantic model examples."""

from pydantic import BaseModel


class User(BaseModel):
    name: str
    age: int
