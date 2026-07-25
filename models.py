from pydantic import BaseModel


class Generators(BaseModel):
    names: list[str]


class Relations(BaseModel):
    words: list[str]


class CheckAbelianThingies(BaseModel):
    generators: Generators
    relations: Relations


class CheckAbelianResponse(BaseModel):
    order: str
    abelian: str


class GroupResult(BaseModel):
    index: int
    generators: Generators
    relations: Relations
    order: str | None
    abelian: str | None
    status: str  # "ok", "skipped", "timeout", or "error"
    lean_code: str | None
