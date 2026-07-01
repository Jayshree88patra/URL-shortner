from pydantic import BaseModel, HttpUrl, Field
import datetime

class CreateRequest(BaseModel):
    url: HttpUrl
    custom_code: str | None = None

class UpdateRequest(BaseModel):
    url: HttpUrl

class URLResponse(BaseModel):
    id: int
    url: HttpUrl
    shortCode: str = Field(..., alias="shortCode")
    createdAt: datetime.datetime
    updatedAt: datetime.datetime
    class Config:
        orm_mode = True
        allow_population_by_field_name = True

class StatsResponse(BaseModel):
    id: int
    url: HttpUrl
    shortCode: str = Field(..., alias="shortCode")
    createdAt: datetime.datetime
    updatedAt: datetime.datetime
    accessCount: int
    class Config:
        orm_mode = True
        allow_population_by_field_name = True
