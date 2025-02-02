# :weight_lifting: FitGoal

Trabalho final da disciplina de Desenvolvimento de Software para Persistência (2024.2). A proposta da aplicação é a de ser uma plataforma para gerenciamento de treinos personalizados para alunos de uma academia ou de personal trainers, usando um banco de dados relacional para a persistência de dados. A aplicação permite o cadastro de alunos, criação de treinos, associação de exercícios aos treinos, e oferece consultas personalizadas sobre cada entidade. 



## :wrench: Tecnologias Utilizadas:
- Linguagem de programação: Python 3.12

- Framework: FastAPI

- ORM: SQLModel

- Banco de Dados: Suporta SQLite e PostgreSQL

- Gerenciamento de dependências: python-dotenv

- Ferramenta de linting: ruff

## :page_facing_up: Diagrama de Classes UML:

```mermaid
classDiagram
    direction LR
    class Aluno {
        id: int
        nome: str
        email: str
        telefone: str
        peso: float
        altura: float
    }
    class Treino {
        id: int
        nome: str
        dia_semana: str
        aluno_id: int
    }
    class Exercicio {
        id: int
        nome: str
        grupo_muscular: str
        dificuldade: str
        series: int
        repeticoes: int
        descricao: str
    }

    Aluno "1" -- "*" Treino
    Treino "*" -- "*" Exercicio
```
