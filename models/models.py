from sqlmodel import SQLModel, Field, Relationship

class Aluno(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    nome: str
    email: str
    telefone: str
    peso: float
    altura: float
    treinos: list["Treino"] = Relationship(back_populates="aluno")
    

class TreinoExercicioLink(SQLModel, table=True):
    treino_id: int = Field(foreign_key="treino.id", primary_key=True)
    exercicio_id: int = Field(foreign_key="exercicio.id", primary_key=True)
    
class Exercicio(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    nome: str
    series: int
    repeticoes: int
    grupo_muscular: str
    dificuldade: str
    descricao: str
    treinos: list["Treino"] = Relationship(back_populates="exercicios", link_model=TreinoExercicioLink)

class Treino(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    nome: str
    dia_semana: str
    aluno_id: int = Field(foreign_key="aluno.id")
    aluno: Aluno = Relationship(back_populates="treinos")
    exercicios: list[Exercicio] = Relationship(back_populates="treinos", link_model=TreinoExercicioLink)
    
    @property
    def dia_semana_str(self) -> str:
        return self.dia_semana.name.capitalize()