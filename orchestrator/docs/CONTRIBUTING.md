# Contribuindo para o Metaglass Agent

## Pull Requests

Todo codigo que entra na branch `main` deve passar por uma Pull Request. Commits diretos na `main` nao sao permitidos.

### Requisitos para merge

1. **Aprovacao obrigatoria** — a PR precisa de pelo menos **uma aprovacao** de outro membro do time antes do merge.

2. **Limite de 500-530 linhas** — PRs nao devem ultrapassar 500 linhas alteradas (somando adicoes e remocoes). PRs menores facilitam a revisao e reduzem o risco de bugs. Se a mudanca for maior que isso, quebre em PRs menores e independentes.

3. **Sem erros de lint e formatacao** — o codigo deve passar pelo linter e pela verificacao de formatacao sem erros. Rode `make lint` localmente antes de abrir a PR. Para corrigir problemas automaticamente, rode `make fmt`.

4. **CI verde** — todos os workflows do GitHub Actions devem estar passando. A pipeline roda lint, typecheck e testes automaticamente em cada PR. Nenhuma PR sera aceita com checks falhando.

5. **Testes para funcionalidades novas** — toda PR que implementa uma nova funcionalidade deve incluir testes correspondentes. PRs de features sem testes nao serao aceitas.

## Verificando localmente antes de abrir a PR

A partir do diretorio `orchestrator/`, rode:

```bash
make check
```

Isso executa lint, typecheck e testes de uma vez. Garanta que tudo esta passando antes de abrir a PR.

Para corrigir problemas de formatacao automaticamente:

```bash
make fmt
```
