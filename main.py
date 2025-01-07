# Importando as bibliotecas necessárias
from fastapi import FastAPI

# Criando a instância da aplicação FastAPI
app = FastAPI()

# Definindo uma rota simples
@app.get("/")
def read_root():
    return {"message": "Hello, World!"}

# Para rodar a aplicação:
# No terminal, execute: uvicorn nome_do_arquivo:app --reload
