from fastapi import APIRouter, HTTPException, Depends
from sqlmodel import Session, select
from models.models import Exercicio, Treino, TreinoExercicioLink
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

@router.post("/{treino_id}/exercicios/{exercicio_id}")
def add_exercicio_to_treino(treino_id: int, exercicio_id: int, session: Session = Depends(get_session)):
    treino = session.get(Treino, treino_id)
    if not treino:
        raise HTTPException(status_code=404, detail="Treino não encontrado")
    
    exercicio = session.get(Exercicio, exercicio_id)
    if not exercicio:
        raise HTTPException(status_code=404, detail="Exercício não encontrado")
    
    link_existente = session.query(TreinoExercicioLink).filter_by(treino_id=treino_id, exercicio_id=exercicio_id).first()
    if link_existente:
        raise HTTPException(status_code=400, detail="Exercício já associado a este treino")
    
    link = TreinoExercicioLink(treino_id=treino_id, exercicio_id=exercicio_id)
    session.add(link)
    session.commit()
    return {"ok": True, "message": "Exercício adicionado ao treino com sucesso"}

@router.get("/", response_model=list[Exercicio])
def read_exercicios(session: Session = Depends(get_session)):
    return session.exec(select(Exercicio)).all()

@router.get("/{exercicio_id}", response_model=Exercicio)
def read_exercicio(exercicio_id: int, session: Session = Depends(get_session)):
    exercicio = session.get(Exercicio, exercicio_id)
    if not exercicio:
        raise HTTPException(status_code=404, detail="Exercício não encontrado")
    return exercicio

@router.put("/{exercicio_id}", response_model=Exercicio)
def update_exercicio(exercicio_id: int, exercicio: Exercicio, session: Session = Depends(get_session)):
    db_exercicio = session.get(Exercicio, exercicio_id)
    if not db_exercicio:
        raise HTTPException(status_code=404, detail="Exercício não encontrado")
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
        raise HTTPException(status_code=404, detail="Exercício não encontrado")
    session.delete(exercicio)
    session.commit()
    return {"ok": True}