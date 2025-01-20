from fastapi import APIRouter, HTTPException, Depends, Query
from sqlmodel import Session, select
from sqlalchemy.orm import selectinload
from models.treino import Treino
from database import get_session
from services import treinos_service


router = APIRouter(
    prefix="/treinos",
    tags=["Treinos"],
)


@router.post("/", response_model=Treino)
def create_treino(treino: Treino, session: Session = Depends(get_session)):
    """
    Cria um novo treino.
    """
    session.add(treino)
    session.commit()
    session.refresh(treino)
    return treino


@router.get("/", response_model=list[Treino])
def read_treinos(
    offset: int = 0,
    limit: int = Query(default=10, le=100),
    session: Session = Depends(get_session),
):
    """
    Retorna uma lista de treinos com paginação.
    """
    statement = (
        select(Treino)
        .offset(offset)
        .limit(limit)
        .options(selectinload(Treino.aluno), selectinload(Treino.exercicios))
    )
    treinos = session.exec(statement).all()
    return treinos


@router.get("/{treino_id}", response_model=Treino)
def read_treino(treino_id: int, session: Session = Depends(get_session)):
    """
    Retorna um treino específico pelo ID.
    """
    statement = (
        select(Treino)
        .where(Treino.id == treino_id)
        .options(selectinload(Treino.aluno), selectinload(Treino.exercicios))
    )
    treino = session.exec(statement).first()
    if not treino:
        raise HTTPException(status_code=404, detail="Treino not found")
    return treino


@router.get("/dia/{dia_semana}")
def read_treinos_por_dia(dia_semana: str, session: Session = Depends(get_session)):
    """
    Retorna treinos de um dia específico da semana.
    """
    return treinos_service.get_treinos_por_dia(session, dia_semana)


@router.get("/alunos/treinos-count")
def count_treinos_por_aluno(session: Session = Depends(get_session)):
    """
    Retorna a contagem de treinos por aluno.
    """
    return treinos_service.count_treinos_por_aluno(session)


@router.get("/contagem/dia", response_model=list[dict])
def count_treinos_por_dia(session: Session = Depends(get_session)):
    """
    Retorna a contagem de treinos por dia da semana.
    """
    return [
        {"dia_semana": dia, "quantidade": quantidade}
        for dia, quantidade in treinos_service.count_treinos_por_dia(session)
    ]


@router.put("/{treino_id}", response_model=Treino)
def update_treino(
    treino_id: int, treino: Treino, session: Session = Depends(get_session)
):
    """
    Atualiza os dados de um treino pelo ID.
    """
    db_treino = session.get(Treino, treino_id)
    if not db_treino:
        raise HTTPException(status_code=404, detail="Treino not found")
    for key, value in treino.dict(exclude_unset=True).items():
        setattr(db_treino, key, value)
    session.add(db_treino)
    session.commit()
    session.refresh(db_treino)
    return db_treino


@router.delete("/{treino_id}")
def delete_treino(treino_id: int, session: Session = Depends(get_session)):
    """
    Deleta um treino pelo ID.
    """
    treino = session.get(Treino, treino_id)
    if not treino:
        raise HTTPException(status_code=404, detail="Treino not found")
    session.delete(treino)
    session.commit()
    return {"ok": True}
