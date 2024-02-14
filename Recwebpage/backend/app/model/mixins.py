from pydantic import BaseModel, Field
from datetime import datetime
from typing import List, Optional
from sqlalchemy import Column, DateTime

class TimeMixin(BaseModel):
    """Mxin to for datatime value of when the entity was created and wehn it was last modified."""

    created_at: datetime = Field(default_factory = datetime.now)
    modified_at:datetime = Field(
        sa_column = Column(DateTime,default=datetime.now,
        onupdate=datetime.now, nullable=False)
    )