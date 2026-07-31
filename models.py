from pydantic import BaseModel

# [("a", 2), ("b", -1)] is the relation a^2*b^-1
word = list[tuple[str, int]]
words = list[word]


class Generators(BaseModel):
    names: list[str]


class Relations(BaseModel):
    words: words


class CheckAbelianThingies(BaseModel):
    generators: Generators
    relations: Relations


class CheckAbelianResponse(BaseModel):
    order: int | None = None
    abelian: bool | None = None


class GroupResult(BaseModel):
    index: int
    generators: Generators
    relations: Relations
    order: int | None = None
    abelian: bool | None = None
    status: str  # "ok", "skipped", "timeout", or "error"
    lean_code: str | None
