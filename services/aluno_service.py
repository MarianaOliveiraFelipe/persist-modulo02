from sqlmodel import Session, select
from sqlalchemy.orm import selectinload
from fastapi import HTTPException
from models.aluno import Aluno


def search_alunos_por_nome(nome_parcial: str, session: Session):
    """
    Busca alunos passando o nome parcialmente.

    Args:
        nome_parcial (str): Parte do nome do aluno para busca.
        session (Session): Sessão do banco de dados.

    Returns:
        list[Aluno]: Lista de alunos encontrados.
    """
    statement = select(Aluno).where(Aluno.nome.ilike(f"%{nome_parcial}%"))
    alunos = session.exec(statement).all()

    if not alunos:
        raise HTTPException(
            status_code=404, detail="Nenhum aluno encontrado com esse nome"
        )

    return alunos


def get_alunos_por_peso(peso_minimo: float, session: Session):
    """
    Retorna alunos com peso superior ao valor mínimo especificado.

    Args:
        peso_minimo (float): Peso mínimo para filtro.
        session (Session): Sessão do banco de dados.

    Returns:
        list[Aluno]: Lista de alunos que atendem ao critério de peso.
    """
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
    """
    Retorna alunos com altura superior ao valor mínimo especificado.

    Args:
        altura_minima (float): Altura mínima para filtro.
        session (Session): Sessão do banco de dados.

    Returns:
        list[Aluno]: Lista de alunos que atendem ao critério de altura.
    """
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
    """
    Retorna os treinos associados a um aluno pelo ID.

    Args:
        aluno_id (int): Identificador único do aluno.
        session (Session): Sessão do banco de dados.

    Returns:
        list[Treino]: Lista de treinos associados ao aluno.
    """
    statement = (
        select(Aluno).where(Aluno.id == aluno_id).options(selectinload(Aluno.treinos))
    )
    aluno = session.exec(statement).first()

    if not aluno:
        raise HTTPException(status_code=404, detail="Aluno não encontrado.")

    return aluno.treinos
