from sqlmodel import Session, select, func
from sqlalchemy.orm import joinedload
from models.aluno import Aluno
from models.treino import Treino
from fastapi import HTTPException


def count_treinos_por_aluno(session: Session):
    """
    Conta o número de treinos associados a cada aluno.

    Args:
        session (Session): Sessão do banco de dados.

    Returns:
        list[dict]: Lista de dicionários com o nome do aluno e a quantidade de treinos.
    """
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


def get_treinos_por_dia(session: Session, dia_semana: str):
    """
    Obtém a lista de treinos para um dia específico da semana.

    Args:
        session (Session): Sessão do banco de dados.
        dia_semana (str): Dia da semana para o filtro (ex.: 'Segunda', 'Terça').

    Returns:
        list[Treino]: Lista de treinos correspondentes ao dia da semana especificado.
    """
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


def count_treinos_por_dia(session: Session) -> list[tuple]:
    """
    Conta o número de treinos para cada dia da semana.

    Args:
        session (Session): Sessão do banco de dados.

    Returns:
        list[tuple]: Lista de tuplas contendo o dia da semana e a quantidade de treinos.
    """
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
