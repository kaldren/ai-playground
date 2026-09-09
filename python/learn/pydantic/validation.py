"""Pydantic field-validation example."""

from pydantic import BaseModel, field_validator


class User(BaseModel):
    name: str
    age: int

    @field_validator("age")
    @classmethod
    def age_must_be_non_negative(cls, value: int) -> int:
        if value < 0:
            raise ValueError("age must be non-negative")
        return value
