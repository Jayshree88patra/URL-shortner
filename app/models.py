from sqlmodel import SQLModel, Field
import datetime

class URLMap(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    code: str = Field(index=True, nullable=False)
    url: str
    access_count: int = 0
    created_at: datetime.datetime = Field(default_factory=datetime.datetime.utcnow)
    updated_at: datetime.datetime = Field(default_factory=datetime.datetime.utcnow)
    custom: bool = False
