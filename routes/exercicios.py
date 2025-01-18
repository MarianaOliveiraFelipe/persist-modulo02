from fastapi import APIRouter, HTTPException, Depends, Query
from sqlmodel import Session, select
from sqlalchemy.orm import selectinload
from models.exercicio import Exercicio
from database import get_session

router = APIRouter(
    prefix="/exercicios",
    tags=["Exercícios"],
)

@router.post("/", response_model=Exercicio)
def create_exercicio(exercicio: Exercicio, session: Session = Depends(get_session)):
    session.add(exercicio)
    session.commit()
    session.refresh(exercicio)
    return exercicio

@router.get("/", response_model=list[Exercicio])
def read_exercicios(
    offset: int = 0,
    limit: int = Query(default=10, le=100),
    session: Session = Depends(get_session),
):
    statement = select(Exercicio).offset(offset).limit(limit).options(selectinload(Exercicio.treinos))
    exercicios = session.exec(statement).all()
    return exercicios

@router.get("/{exercicio_id}", response_model=Exercicio)
def read_exercicio(exercicio_id: int, session: Session = Depends(get_session)):
    statement = select(Exercicio).where(Exercicio.id == exercicio_id).options(selectinload(Exercicio.treinos))
    exercicio = session.exec(statement).first()
    if not exercicio:
        raise HTTPException(status_code=404, detail="Exercício not found")
    return exercicio

@router.put("/{exercicio_id}", response_model=Exercicio)
def update_exercicio(exercicio_id: int, exercicio: Exercicio, session: Session = Depends(get_session)):
    db_exercicio = session.get(Exercicio, exercicio_id)
    if not db_exercicio:
        raise HTTPException(status_code=404, detail="Exercício not found")
    for key, value in exercicio.dict(exclude_unset=True).items():
        setattr(db_exercicio, key, value)
    session.add(db_exercicio)
    session.commit()
    session.refresh(db_exercicio)
    return db_exercicio

@router.delete("/{exercicio_id}")
def delete_exercicio(exercicio_id: int, session: Session = Depends(get_session)):
    exercicio = session.get(Exercicio, exercicio_id)
    if not exercicio:
        raise HTTPException(status_code=404, detail="Exercício not found")
    session.delete(exercicio)
    session.commit()
    return {"ok": True}
