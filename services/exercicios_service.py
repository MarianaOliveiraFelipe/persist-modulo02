from fastapi import HTTPException
from sqlmodel import Session, select
from sqlalchemy.orm import selectinload
from models.exercicio import Exercicio


def get_exercicios_por_dificuldade(session: Session, dificuldade: str):
    """
    Retorna exercícios filtrados pela dificuldade.

    Args:
        session (Session): Sessão do banco de dados.
        dificuldade (str): Nível de dificuldade para o filtro.

    Returns:
        list[Exercicio]: Lista de exercícios que correspondem à dificuldade especificada.
    """
    statement = (
        select(Exercicio)
        .where(Exercicio.dificuldade == dificuldade)
    )
    exercicios = session.exec(statement).all()
    if not exercicios:
        raise HTTPException(
            status_code=404, detail="Nenhum exercício encontrado para essa dificuldade"
        )
    return exercicios

def get_exercicios_por_grupo(session: Session, grupo_muscular: str):
    """
    Retorna exercícios filtrados pelo grupo muscular.

    Args:
        session (Session): Sessão do banco de dados.
        grupo_muscular (str): Grupo muscular para o filtro.

    Returns:
        list[Exercicio]: Lista de exercícios que correspondem ao grupo muscular especificado.
    """
    statement = (
        select(Exercicio)
        .where(Exercicio.grupo_muscular == grupo_muscular)
    )
    exercicios = session.exec(statement).all()
    if not exercicios:
        raise HTTPException(
            status_code=404,
            detail="Nenhum exercício encontrado para esse grupo muscular",
        )
    return exercicios


def get_exercicios_por_descricao(session: Session, palavra_chave: str):
    """
    Retorna exercícios filtrados por palavra-chave na descrição.

    Args:
        session (Session): Sessão do banco de dados.
        palavra_chave (str): Palavra-chave para buscar na descrição.

    Returns:
        list[Exercicio]: Lista de exercícios que contêm a palavra-chave na descrição.
    """
    statement = select(Exercicio).where(Exercicio.descricao.ilike(f"%{palavra_chave}%"))
    exercicios = session.exec(statement).all()
    if not exercicios:
        raise HTTPException(
            status_code=404,
            detail="Nenhum exercício encontrado com essa palavra-chave na descrição",
        )
    return exercicios
