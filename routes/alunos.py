from fastapi import APIRouter, HTTPException, Depends, Query
from sqlmodel import Session, select
from sqlalchemy.orm import selectinload
from database import get_session
from models.aluno import Aluno, AlunoBase
from models.treino import Treino
from models.exercicio import Exercicio
from services.aluno_service import search_alunos_por_nome, get_treinos_by_aluno_id 
from services.aluno_service import get_alunos_por_peso, get_alunos_por_altura 


router = APIRouter(
    prefix="/alunos",
    tags=["Alunos"],
)

@router.post("/", response_model=Aluno)
def create_aluno(aluno: Aluno, session: Session = Depends(get_session)):
    session.add(aluno)
    session.commit()
    session.refresh(aluno)
    return aluno

@router.get("/", response_model=list[Aluno])
def read_alunos(
    offset: int = 0,
    limit: int = Query(default=10, le=100),
    session: Session = Depends(get_session),
):
    statement = select(Aluno).offset(offset).limit(limit).options(selectinload(Aluno.treinos))
    alunos = session.exec(statement).all()
    return alunos

@router.get("/{aluno_id}", response_model=Aluno)
def read_aluno(aluno_id: int, session: Session = Depends(get_session)):
    statement = select(Aluno).where(Aluno.id == aluno_id).options(selectinload(Aluno.treinos))
    aluno = session.exec(statement).first()
    if not aluno:
        raise HTTPException(status_code=404, detail="Aluno not found")
    return aluno

#Consultas Extras -----------------------------------------------------------------------------------------
@router.get("/busca/{nome_parcial}", response_model=list[Aluno])
def search_alunos(nome_parcial: str, session: Session = Depends(get_session)):
    return search_alunos_por_nome(nome_parcial, session)


@router.get("/peso/{peso_minimo}", response_model=list[Aluno])
def read_alunos_por_peso(peso_minimo: float, session: Session = Depends(get_session)):
    return get_alunos_por_peso(peso_minimo, session)


@router.get("/altura/{altura_minima}", response_model=list[Aluno])
def read_alunos_por_altura(altura_minima: float, session: Session = Depends(get_session)):
    return get_alunos_por_altura(altura_minima, session)


@router.get("/{aluno_id}/treinos", response_model=list[Treino])
def read_treinos_by_aluno_id(aluno_id: int, session: Session = Depends(get_session)):
    return get_treinos_by_aluno_id(aluno_id, session)
#-----------------------------------------------------------------------------------------------------------

@router.put("/{aluno_id}", response_model=Aluno)
def update_aluno(aluno_id: int, aluno: Aluno, session: Session = Depends(get_session)):
    db_aluno = session.get(Aluno, aluno_id)
    if not db_aluno:
        raise HTTPException(status_code=404, detail="Aluno not found")
    for key, value in aluno.dict(exclude_unset=True).items():
        setattr(db_aluno, key, value)
    session.add(db_aluno)
    session.commit()
    session.refresh(db_aluno)
    return db_aluno

@router.delete("/{aluno_id}")
def delete_aluno(aluno_id: int, session: Session = Depends(get_session)):
    aluno = session.get(Aluno, aluno_id)
    if not aluno:
        raise HTTPException(status_code=404, detail="Aluno not found")
    session.delete(aluno)
    session.commit()
    return {"ok": True}