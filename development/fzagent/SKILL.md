---
name: fzagent
description: Operador do cerebro secundario do workspace fzagent. Use quando o usuario digitar `/fzagent`, pedir para `ingerir uma fonte no wiki`, `consultar a base de conhecimento`, `gerar artefatos a partir do wiki` (Marp slides, comparacoes, graficos) ou `lintar paginas orfas`. A skill assume que o workspace tem `wiki/`, `db/`, `raw/` e o binario `fzagent` instalado.
license: MIT
compatibility: Claude Code, Codex, Cursor, Gemini CLI.
metadata:
  author: fzagent-team
  version: '1.0.0'
  framework: fzagent
  role: secondary-brain-operator
---

Voce e o operador do **cerebro secundario fzagent**. Use as 4 capacidades
abaixo conforme o pedido do usuario.

## Capacidades

### 1. Ingest

Quando o usuario disser "ingere", "indexa", "adiciona ao wiki", "le essa
fonte":

```bash
fzagent wiki ingest <caminho-da-fonte> [--summarize]
```

Use `--summarize` se o usuario quiser resumo automatico via LLM.

### 2. Query

Quando o usuario perguntar algo que parece estar no wiki ("o que diz o
dossie sobre X", "qual a decisao tomada sobre Y", "encontre referencia a Z"):

```bash
fzagent wiki query "<pergunta>" [--top 5] [--synthesize]
```

Use `--synthesize` para resposta sintetica com citacoes `[[slug]]`.

### 3. Lint

Quando o usuario pedir auditoria do wiki ("verifique paginas orfas",
"checa links quebrados", "audita o cerebro secundario"):

```bash
fzagent wiki lint
```

Reporta orfas, links quebrados, fontes nao-anexadas. Apresente os primeiros
10 de cada categoria; ofereca a lista completa se mais.

### 4. Geracao de artefatos

Quando o usuario quiser:

- **Marp slides** a partir de uma analise: leia `wiki/analyses/<slug>.md`,
  converta em formato Marp e salve em `_fzagent_artifacts/slides/`.
- **Comparacao** entre dois conceitos: query no wiki por cada, sintetize
  diferencas em tabela markdown.
- **Grafico** (mermaid): gere diagrama mermaid a partir de relacoes em
  `pages` e `links` do indexer; salve em `_fzagent_artifacts/diagrams/`.

## When to use

- `/fzagent`, `fzagent`, `cerebro secundario`, `wiki ingest/query/lint`.
- Pedidos claros de RAG sobre o conteudo de `wiki/`.
- Geracao de derivados a partir do wiki existente.

## When NOT to use

- Tarefas que nao envolvem o wiki — use as outras tools do agente.
- Operacoes destrutivas no banco SQLite ou Qdrant — exigem confirmacao
  explicita.
- Modificacoes de arquivos do projeto fora de `wiki/` e `_fzagent_artifacts/`.

## Pre-requisitos

- `npm install` rodado no workspace.
- `npm run build` para gerar `dist/`.
- `.env` com pelo menos `ANTHROPIC_API_KEY` ou `CLAUDE_CODE_OAUTH_TOKEN`
  para sintese LLM (opcional para query simples).
- Qdrant rodando em `QDRANT_URL` (default `http://localhost:6333`).

## Confidence scale

🟢 CONFIRMADO (do wiki indexer) / 🟡 INFERIDO (do RAG semantico) / 🔴 LACUNA.

## Regra absoluta

Escreve apenas em `wiki/`, `db/` e `_fzagent_artifacts/`. Nunca toca
arquivos de codigo do projeto.
