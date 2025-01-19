from sqlmodel import SQLModel, Field


class TreinoExercicio(SQLModel, table=True):
    treino_id: int = Field(default=None, foreign_key="treino.id", primary_key=True)
    exercicio_id: int = Field(
        default=None, foreign_key="exercicio.id", primary_key=True
    )
