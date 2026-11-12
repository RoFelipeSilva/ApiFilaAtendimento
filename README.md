# API de Fila de Atendimento

**Autor:** Rodrigo Felipe da Silva

**Curso:** Análise e Desenvolvimento de Sistemas

**Tecnologia:** Python e FastAPI

## Descrição do Projeto

API REST desenvolvida para gerenciar uma fila de atendimento presencial, permitindo integração com sistemas de totens de atendimento.

O sistema permite cadastrar clientes, consultar a fila, avançar o atendimento e remover clientes, respeitando a prioridade de atendimento.

## Tecnologias Utilizadas

- Python
- FastAPI
- Uvicorn
- Swagger UI
- GitHub
- Render

## Endpoints da API

| Método | Endpoint | Descrição |
|---|---|---|
| GET | /fila | Consulta os clientes aguardando |
| GET | /fila/{id} | Consulta o cliente pela posição |
| POST | /fila | Adiciona um cliente à fila |
| PUT | /fila | Avança o atendimento |
| DELETE | /fila/{id} | Remove um cliente pela posição |

## Regras de Negócio

1. Clientes são cadastrados com nome e tipo de atendimento.
2. O tipo P representa atendimento prioritário.
3. O tipo N representa atendimento normal.
4. Clientes prioritários têm preferência na fila.
5. Ao avançar a fila, o próximo cliente é atendido e os demais são reorganizados.
6. Uma fila vazia retorna uma lista JSON vazia.

## Exemplo de Cadastro

Método: POST /fila

```json
{
  "nome": "Maria",
  "tipo": "P"
}
```

## Testes Realizados

Os cinco endpoints foram testados na documentação Swagger da API publicada no Render.

Foram verificados cadastro, consulta, exclusão, avanço da fila e prioridade de atendimento.

## Links do Projeto

**Documentação Swagger:**
https://apifilaatendimento.onrender.com/docs

**Repositório GitHub:**
https://github.com/RoFelipeSilva/ApiFilaAtendimento

## Finalidade Acadêmica

Projeto desenvolvido como avaliação final da disciplina de Desenvolvimento de APIs, do curso de Análise e Desenvolvimento de Sistemas.

**Desenvolvido por Rodrigo Felipe da Silva — 2026.**
