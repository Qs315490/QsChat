from typing import Any

from pydantic import BaseModel, Field


class ApiResult(BaseModel):
    message: str
    data: Any
