from pydantic import BaseModel, Field
from dataclasses import dataclass


class BaseSearchModel(BaseModel):
    keyword: str
    page: int = Field(ge=1)