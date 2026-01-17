from pydantic import BaseModel, Field
from dataclasses import dataclass


class MediaId(BaseModel):
    id: int = Field(ge=1)


class BaseSearchModel(BaseModel):
    keyword: str = Field(min_length=1)
    page: int = Field(ge=1)
