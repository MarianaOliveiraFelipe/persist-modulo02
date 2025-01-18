from sqlmodel import SQLModel, Field, Relationship
from .treino_exercicio import TreinoExercicio
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from .aluno import Aluno
    from .exercicio import Exercicio

class TreinoBase(SQLModel):
    id: int | None = Field(default=None, primary_key=True)
    nome: str
    dia_semana: str

class Treino(TreinoBase, table=True):
    aluno_id: int = Field(foreign_key="aluno.id")
    aluno: 'Aluno' = Relationship(back_populates="treinos")
    exercicios: list['Exercicio'] = Relationship(back_populates="treinos", link_model=TreinoExercicio)