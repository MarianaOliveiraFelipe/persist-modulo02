from sqlmodel import Session, select, func
from sqlalchemy.orm import joinedload
from models.aluno import Aluno
from models.treino import Treino
from fastapi import HTTPException


# Função para contagem de treinos por aluno
def count_treinos_por_aluno(session: Session):
    try:
        statement = (
            select(Aluno.nome, func.count(Treino.id).label("treino_count"))
            .join(Treino, Treino.aluno_id == Aluno.id)
            .group_by(Aluno.nome)
        )
        result = session.exec(statement).all()

        if not result:
            raise ValueError("Nenhum treino encontrado para os alunos.")

        return [{"aluno": row[0], "treinos": row[1]} for row in result]

    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Erro ao carregar os treinos por aluno: {str(e)}"
        )


# Função para obter treinos por dia da semana
def get_treinos_por_dia(session: Session, dia_semana: str):
    try:
        statement = (
            select(Treino)
            .options(joinedload(Treino.aluno))
            .where(Treino.dia_semana == dia_semana)
            .order_by(Treino.nome)
        )
        treinos = session.exec(statement).all()

        if not treinos:
            raise ValueError(f"Nenhum treino encontrado para o dia {dia_semana}.")

        return treinos

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Erro ao carregar os treinos para o dia {dia_semana}: {str(e)}",
        )


# Função para contagem de treinos por dia da semana
def count_treinos_por_dia(session: Session) -> list[tuple]:
    try:
        statement = select(
            Treino.dia_semana, func.count(Treino.id).label("quantidade")
        ).group_by(Treino.dia_semana)
        result = session.exec(statement).all()

        if not result:
            raise ValueError("Nenhuma contagem de treinos encontrada.")
        return result

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Erro ao carregar a contagem de treinos por dia: {str(e)}",
        )
