# Metaglass Agent

Plataforma de agentes inteligentes para smart glasses. O sistema recebe inputs multimodais (audio, video, texto) enviados por um middleware e os processa por meio de um orquestrador que roteia as queries para agentes especializados, mantendo contexto de sessao e historico semantico.

## Arquitetura

![Arquitetura](docs/images/arch.png)

O projeto e composto por:

- **Orchestrator** — servico gRPC em Python responsavel por gerenciar sessoes, rotear queries para agentes e manter contexto. Utiliza PostgreSQL para estado relacional e Qdrant para busca semantica.
- **Proto** — definicoes protobuf compartilhadas entre os servicos.

## Documentacao

- [Como rodar o projeto](docs/GETTING_STARTED.md)
- [Como contribuir](docs/CONTRIBUTING.md)
