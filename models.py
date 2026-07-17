from pydantic import BaseModel


class Generators(BaseModel):
    names: list[str]


class Relations(BaseModel):
    expressions: list[str]


class CheckAbelianThingies(BaseModel):
    generators: Generators
    relations: Relations


class CheckAbelianResponse(BaseModel):
    order: str
    abelian: str
