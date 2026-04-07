# Metaglass Agent

Plataforma de agentes inteligentes para smart glasses. O sistema recebe inputs multimodais (audio, video, texto) enviados por um middleware e os processa por meio de um orquestrador que roteia as queries para agentes especializados, mantendo contexto de sessao e historico semantico.

## Arquitetura

![Arquitetura](docs/images/arch.png)

O projeto e composto por:

- **Orchestrator** — servico gRPC em Python responsavel por gerenciar sessoes, rotear queries para agentes e manter contexto. Utiliza PostgreSQL para estado relacional e Qdrant para busca semantica.
- **Proto** — definicoes protobuf compartilhadas entre os servicos.

## Dentro do Orquestrador

![Arquitetura interna do Orquestrador](docs/images/into_arch.png)

<details>
<summary><strong>server</strong></summary>

- Recebe as requisicoes via gRPC.
- Valida a estrutura da requisicao.
- Encaminha para o servico correspondente.

</details>

<details>
<summary><strong>service</strong></summary>

- Implementa a logica principal do orquestrador.
- Realiza chamadas personalizadas para agentes locais via LangGraph.
- Usa a camada de DB para buscar/persistir contexto.
- Aplica validacoes adicionais para reduzir bugs.

</details>

<details>
<summary><strong>db</strong></summary>

- Armazena e busca contexto das sessoes de usuario.
- Armazena e busca documentos conforme query e contexto.
- Usa ORM (Object Relational Mapping).

</details>

## Documentacao

- [Como rodar o projeto](docs/GETTING_STARTED.md)
- [Como contribuir](docs/CONTRIBUTING.md)
