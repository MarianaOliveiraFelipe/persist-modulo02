from sqlmodel import SQLModel, Field, Relationship
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .treino import Treino


class AlunoBase(SQLModel):
    id: int | None = Field(default=None, primary_key=True)
    nome: str
    email: str
    telefone: str
    peso: float
    altura: float


class Aluno(AlunoBase, table=True):
    treinos: list["Treino"] = Relationship(back_populates="aluno")
