from sqlmodel import Session, select
from sqlalchemy.orm import selectinload
from fastapi import HTTPException
from models.aluno import Aluno


def search_alunos_por_nome(nome_parcial: str, session: Session):
    statement = select(Aluno).where(Aluno.nome.ilike(f"%{nome_parcial}%"))
    alunos = session.exec(statement).all()

    if not alunos:
        raise HTTPException(
            status_code=404, detail="Nenhum aluno encontrado com esse nome"
        )

    return alunos


def get_alunos_por_peso(peso_minimo: float, session: Session):
    statement = (
        select(Aluno)
        .where(Aluno.peso > peso_minimo)
        .options(selectinload(Aluno.treinos))
    )
    alunos = session.exec(statement).all()

    if not alunos:
        raise HTTPException(
            status_code=404,
            detail="Nenhum aluno encontrado com peso superior a esse valor.",
        )

    return alunos


def get_alunos_por_altura(altura_minima: float, session: Session):
    statement = (
        select(Aluno)
        .where(Aluno.altura > altura_minima)
        .options(selectinload(Aluno.treinos))
    )
    alunos = session.exec(statement).all()

    if not alunos:
        raise HTTPException(
            status_code=404,
            detail="Nenhum aluno encontrado com altura superior a esse valor.",
        )

    return alunos


def get_treinos_by_aluno_id(aluno_id: int, session: Session):
    statement = (
        select(Aluno).where(Aluno.id == aluno_id).options(selectinload(Aluno.treinos))
    )
    aluno = session.exec(statement).first()

    if not aluno:
        raise HTTPException(status_code=404, detail="Aluno não encontrado.")

    return aluno.treinos
