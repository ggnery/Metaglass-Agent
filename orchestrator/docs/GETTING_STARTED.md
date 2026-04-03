# Como rodar o projeto

## Requisitos

### Com Docker

- [Docker](https://docs.docker.com/get-docker/) e [Docker Compose](https://docs.docker.com/compose/install/)

### Sem Docker

- [Python 3.13+](https://www.python.org/downloads/)
- [uv](https://docs.astral.sh/uv/getting-started/installation/)
- [PostgreSQL 14+](https://www.postgresql.org/download/)
- [Qdrant](https://qdrant.tech/documentation/quick-start/)

---

## Rodando com Docker

Todos os comandos abaixo devem ser executados a partir do diretório `orchestrator/`.

### 1. Subir todos os servicos

```bash
make up
```

Isso inicia em background: PostgreSQL, Qdrant, migrations e o orchestrator.

### 2. Ver logs do orchestrator

```bash
make logs
```

### 3. Parar tudo

```bash
make down
```

### 4. Parar tudo e remover volumes (reset completo)

```bash
make clean
```

Isso apaga os dados persistidos do PostgreSQL e do Qdrant.

### 5. Rebuild das imagens

```bash
make build
```

Use apos alterar o `Dockerfile` ou o `pyproject.toml`.

### 6. Reiniciar apenas o orchestrator

```bash
make restart
```

### 7. Rodar apenas o banco de dados

```bash
make db
```

### 8. Rodar migrations manualmente

```bash
make migrate
```

### 9. Formatar e corrigir codigo automaticamente

```bash
make fmt
```

Aplica formatacao e corrige problemas de lint no codigo em `src/`.

### 10. Gerar codigo a partir dos arquivos .proto

```bash
make proto
```

Os arquivos gerados ficam em `generated/`.

---

## Rodando sem Docker

### 1. Instalar dependencias

```bash
uv sync
```

Isso cria o virtualenv em `.venv/` e instala todas as dependencias (incluindo as de desenvolvimento).

### 2. Subir PostgreSQL e Qdrant localmente

Voce precisa ter PostgreSQL e Qdrant rodando na sua maquina. As variaveis de ambiente esperadas sao:

| Variavel            | Valor padrao   |
|---------------------|----------------|
| `POSTGRES_USER`     | `postgres`     |
| `POSTGRES_PASSWORD` | `postgres`     |
| `POSTGRES_DB`       | `orchestrator` |
| `POSTGRES_HOST`     | `db`           |
| `POSTGRES_PORT`     | `5432`         |
| `QDRANT_HOST`       | `qdrant`       |
| `QDRANT_PORT`       | `6333`         |
| `QDRANT_GRPC_PORT`  | `6334`         |
| `GRPC_PORT`         | `50051`        |

Ao rodar localmente (sem Docker), ajuste `POSTGRES_HOST` e `QDRANT_HOST` para `localhost`:

```bash
export POSTGRES_HOST=localhost
export QDRANT_HOST=localhost
```

> **Dica:** voce pode subir apenas as dependencias via Docker e rodar o orchestrator localmente:
>
> ```bash
> make db
> make qdrant
> make migrate
> ```

### 3. Rodar migrations

```bash
uv run alembic upgrade head
```

### 4. Iniciar o orchestrator

```bash
uv run python src/main.py
```

---

## Testando a API com grpcurl

Com o orchestrator rodando, voce pode testar a API usando [grpcurl](https://github.com/fullstorydev/grpcurl).

### Listar servicos disponiveis

```bash
grpcurl -plaintext localhost:50051 list
```

### Criar uma sessao

```bash
grpcurl -plaintext -d '{
  "user_id": "user-123",
  "device_id": "device-456",
  "initial_metadata": {"language": "pt-BR", "timezone": "America/Sao_Paulo"}
}' localhost:50051 metaglass.SessionService/CreateSession
```

---

## Testes e qualidade de codigo

Todos os comandos abaixo usam `uv run` e nao precisam de Docker.

### Rodar testes

```bash
make test
```

Executa o `pytest` com os testes em `tests/`.

### Linter (ruff)

```bash
make lint
```

Verifica erros de lint e formatacao sem alterar nenhum arquivo.

### Formatar e corrigir automaticamente

```bash
make fmt
```

Corrige problemas de lint e aplica formatacao automatica no codigo em `src/`.

### Type checking (pyright)

```bash
make typecheck
```

Roda o pyright para verificar tipos no codigo.

### Rodar todas as verificacoes de uma vez

```bash
make check
```

Equivale a rodar `lint` + `typecheck` + `test` em sequencia.

---

## Referencia rapida de comandos

| Comando          | Descricao                                    |
|------------------|----------------------------------------------|
| `make up`        | Sobe todos os servicos via Docker             |
| `make down`      | Para todos os servicos                        |
| `make restart`   | Reinicia o orchestrator                       |
| `make logs`      | Mostra logs do orchestrator                   |
| `make db`        | Sobe apenas o PostgreSQL                      |
| `make qdrant`    | Sobe apenas o Qdrant                          |
| `make migrate`   | Roda migrations do banco                      |
| `make build`     | Rebuild das imagens Docker                    |
| `make clean`     | Para tudo e remove volumes                    |
| `make proto`     | Gera codigo Python a partir dos .proto        |
| `make fmt`       | Formata e corrige o codigo automaticamente    |
| `make lint`      | Verifica lint e formatacao                    |
| `make typecheck` | Verifica tipos com pyright                    |
| `make test`      | Roda os testes                                |
| `make check`     | Roda lint + typecheck + test                  |
| `make help`      | Lista todos os comandos disponiveis           |
