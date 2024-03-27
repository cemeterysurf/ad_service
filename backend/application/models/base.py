from pydantic import BaseModel as _BaseModel


class BaseModel(_BaseModel):
    class Config:
        use_enum_values = True
        orm_mode = True


class Pagination(BaseModel):
    page: int = 1
    per_page: int = 100
