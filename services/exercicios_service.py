from fastapi import HTTPException
from sqlmodel import Session, select
from sqlalchemy.orm import selectinload
from models.exercicio import Exercicio


def get_exercicios_por_dificuldade(session: Session, dificuldade: str):
    statement = (
        select(Exercicio)
        .where(Exercicio.dificuldade == dificuldade)
        .options(selectinload(Exercicio.treinos))
    )
    exercicios = session.exec(statement).all()
    if not exercicios:
        raise HTTPException(
            status_code=404, detail="Nenhum exercício encontrado para essa dificuldade"
        )
    return exercicios


def get_exercicios_por_grupo(session: Session, grupo_muscular: str):
    statement = (
        select(Exercicio)
        .where(Exercicio.grupo_muscular == grupo_muscular)
        .options(selectinload(Exercicio.treinos))
    )
    exercicios = session.exec(statement).all()
    if not exercicios:
        raise HTTPException(
            status_code=404,
            detail="Nenhum exercício encontrado para esse grupo muscular",
        )
    return exercicios


def get_exercicios_por_descricao(session: Session, palavra_chave: str):
    statement = select(Exercicio).where(Exercicio.descricao.ilike(f"%{palavra_chave}%"))
    exercicios = session.exec(statement).all()
    if not exercicios:
        raise HTTPException(
            status_code=404,
            detail="Nenhum exercício encontrado com essa palavra-chave na descrição",
        )
    return exercicios
