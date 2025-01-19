from sqlmodel import SQLModel, Field, Relationship
from .treino_exercicio import TreinoExercicio
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .treino import Treino


class ExercicioBase(SQLModel):
    id: int | None = Field(default=None, primary_key=True)
    nome: str
    grupo_muscular: str
    dificuldade: str
    series: int
    repeticoes: int
    descricao: str


class Exercicio(ExercicioBase, table=True):
    treinos: list["Treino"] = Relationship(
        back_populates="exercicios", link_model=TreinoExercicio
    )
