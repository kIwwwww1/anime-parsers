from pydantic import BaseModel, Field
from dataclasses import dataclass
from typing import Literal, Optional

OrderModel = Literal['RATING', 'NUM_VOTE', 'YEAR']
TypeModel = Literal['FILM', 'TV_SHOW', 'TV_SERIAL', 'MINI_SERIAL', 'ALL']

class MediaId(BaseModel):
    id: int = Field(ge=1)


class BaseSearchModel(BaseModel):
    keyword: str = Field(min_length=1)
    page: int = Field(ge=1, default=1)


class SearchModel(BaseModel):
    countries: int | None
    genres: int | None
    order: OrderModel | None
    type: TypeModel | None
    ratingFrom: int | float | None
    ratingTo: int | float | None
    yearFrom: int | None
    yearTo: int | None
    imdbId: int | None
    keyword: str | None = Field(min_length=1)
    page: int = Field(ge=1, default=1)
