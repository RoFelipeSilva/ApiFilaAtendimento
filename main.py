
from datetime import datetime
from typing import Literal

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field, field_validator

app = FastAPI(
    title="API de Fila de Atendimento",
    description="API para gerenciamento de filas presenciais.",
    version="1.0.0",
)


class NovoCliente(BaseModel):
    nome: str = Field(..., min_length=1, max_length=20)
    tipo: Literal["N", "P"]

    @field_validator("nome")
    @classmethod
    def validar_nome(cls, valor: str) -> str:
        valor = valor.strip()
        if not valor:
            raise ValueError("O nome é obrigatório.")
        return valor

    @field_validator("tipo", mode="before")
    @classmethod
    def normalizar_tipo(cls, valor):
        if isinstance(valor, str):
            return valor.strip().upper()
        return valor


fila = []
proximo_id = 1


def clientes_aguardando():
    return sorted(
        [cliente for cliente in fila if not cliente["atendido"]],
        key=lambda cliente: (
            0 if cliente["tipo"] == "P" else 1,
            cliente["id"],
        ),
    )


def atualizar_posicoes():
    aguardando = clientes_aguardando()

    for posicao, cliente in enumerate(aguardando, start=1):
        cliente["posicao"] = posicao


@app.get("/fila")
def consultar_fila():
    atualizar_posicoes()

    return [
        {
            "posicao": cliente["posicao"],
            "nome": cliente["nome"],
            "data_chegada": cliente["data_chegada"],
        }
        for cliente in clientes_aguardando()
    ]


@app.get("/fila/{id}")
def consultar_cliente(id: int):
    atualizar_posicoes()

    for cliente in clientes_aguardando():
        if cliente["posicao"] == id:
            return {
                "posicao": cliente["posicao"],
                "nome": cliente["nome"],
                "data_chegada": cliente["data_chegada"],
            }

    raise HTTPException(
        status_code=404,
        detail="Não existe cliente aguardando nessa posição da fila.",
    )


@app.post("/fila", status_code=201)
def adicionar_cliente(novo: NovoCliente):
    global proximo_id

    cliente = {
        "id": proximo_id,
        "posicao": 0,
        "nome": novo.nome,
        "tipo": novo.tipo,
        "data_chegada": datetime.now().isoformat(timespec="seconds"),
        "atendido": False,
    }

    fila.append(cliente)
    proximo_id += 1

    atualizar_posicoes()

    return {
        "mensagem": "Cliente adicionado à fila com sucesso.",
        "cliente": cliente,
    }


@app.put("/fila")
def avancar_fila():
    atualizar_posicoes()
    aguardando = clientes_aguardando()

    if aguardando:
        primeiro = aguardando[0]
        primeiro["posicao"] = 0
        primeiro["atendido"] = True

    atualizar_posicoes()

    return {
        "mensagem": "Fila atualizada com sucesso.",
        "fila": consultar_fila(),
    }


@app.delete("/fila/{id}")
def remover_cliente(id: int):
    atualizar_posicoes()

    cliente_removido = next(
        (
            cliente
            for cliente in clientes_aguardando()
            if cliente["posicao"] == id
        ),
        None,
    )

    if cliente_removido is None:
        raise HTTPException(
            status_code=404,
            detail="Não existe cliente aguardando nessa posição da fila.",
        )

    fila.remove(cliente_removido)
    atualizar_posicoes()

    return {
        "mensagem": "Cliente removido da fila com sucesso."
    }
