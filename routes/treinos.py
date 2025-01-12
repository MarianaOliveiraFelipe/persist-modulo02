from fastapi import APIRouter, HTTPException, Depends
from sqlmodel import Session, select
from models.models import Treino, Exercicio
from database import get_session

router = APIRouter(
    prefix="/treinos",
    tags=["Treinos"],
)

@router.post("/", response_model=Treino)
def create_treino(treino: Treino, session: Session = Depends(get_session)):
    session.add(treino)
    session.commit()
    session.refresh(treino)
    return treino

@router.get("/", response_model=list[Treino])
def read_treinos(session: Session = Depends(get_session)):
    treinos = session.exec(select(Treino)).all()
    return treinos

@router.get("/{treino_id}", response_model=Treino)
def read_by_id(treino_id: int, session: Session = Depends(get_session)):
    treino = session.get(Treino, treino_id)
    if not treino:
        raise HTTPException(status_code=404, detail="Treino não encontrado")
    return treino

@router.put("/{treino_id}", response_model=Treino)
def update_treino(treino_id: int, treino: Treino, session: Session = Depends(get_session)):
    db_treino = session.get(Treino, treino_id)
    if not db_treino:
        raise HTTPException(status_code=404, detail="Treino não encontrado")
    for key, value in treino.dict(exclude_unset=True).items():
        setattr(db_treino, key, value)
    session.add(db_treino)
    session.commit()
    session.refresh(db_treino)

    db_treino.exercicios = [exercicio for exercicio in db_treino.exercicios]
    return db_treino

@router.delete("/{treino_id}")
def delete_treino(treino_id: int, session: Session = Depends(get_session)):
    treino = session.get(Treino, treino_id)
    if not treino:
        raise HTTPException(status_code=404, detail="Treino não encontrado")
    session.delete(treino)
    session.commit()
    return {"ok": True}

@router.get("/{treino_id}/exercicios", response_model=list[Exercicio])
def read_exercicios(treino_id: int, session: Session = Depends(get_session)):
    treino = session.get(Treino, treino_id)
    if not treino:
        raise HTTPException(status_code=404, detail="Treino não encontrado")
    return treino.exercicios