---
name: clean-code
description: Remove comentários e docstrings do código alterado (backend Python e frontend TS/TSX), mantendo só diretivas funcionais que ferramentas exigem (# noqa, # nosec, # type:, eslint-disable, /// <reference). Roda testes depois para confirmar que nada quebrou. Use sempre que terminar de desenvolver algo (antes de considerar a tarefa pronta, e como parte do /prepare-pr) ou quando pedirem "limpa o código", "remove os comentários", "deixa profissional".
---

# clean-code

Este projeto adota código autoexplicativo: nomes de variável/função claros em vez de comentário
explicando o óbvio. **Comentário e docstring não fazem parte do estilo do projeto** — nem em
português explicando "o quê", nem docstring de função. Regra de negócio e decisão não-óbvia vão
para o `CLAUDE.md` do módulo (ou a mensagem do commit), não para dentro do código.

## Quando rodar

- Ao terminar qualquer tarefa de desenvolvimento (feature, fix, refactor), antes de considerar o
  trabalho pronto.
- Como parte do `/prepare-pr`, antes de abrir o PR — o código muda de mãos ali.
- Sob pedido explícito ("limpa o código", "remove os comentários").

## O que remove

- Python: comentários `#` e docstrings (`"""..."""`/`'''...'''`), incluindo docstrings de
  módulo, classe e função.
- TypeScript/TSX: comentários `//`, blocos `/* ... */` e `/** JSDoc */`, incluindo comentário
  JSX `{/* ... */}`.

## O que **não** remove (diretivas funcionais, não documentação)

Essas linhas mudam o comportamento de uma ferramenta — removê-las reintroduz avisos que o
projeto já silenciou de propósito (ver `CLAUDE.md` da raiz, seção de segurança/testes):

- Python: `# noqa`, `# noqa: <código>`, `# nosec`, `# nosec <código>`, `# type: ignore`,
  `# pragma: no cover`, shebang (`#!/usr/bin/env python`).
- TypeScript: `// eslint-disable`, `// eslint-disable-next-line`, `// @ts-expect-error`,
  `// @ts-ignore`, `/// <reference types="..." />`.
- Qualquer outra diretiva de linter/formatter/type-checker que, sem o comentário, muda o
  resultado do `bandit`, `pip-audit`, `oxlint`, `tsc` ou `npm audit`.

Na dúvida se uma linha é diretiva funcional ou documentação: comente o trecho e rode o lint
correspondente (`bandit -r app -q` ou `npm run lint`) — se o aviso reaparecer, é diretiva.

## Passo a passo

1. **Escopo**: normalmente só os arquivos alterados nesta tarefa (`git diff --name-only`, ou
   `git diff origin/main...HEAD --name-only` se já commitado). Se o pedido for "limpa o código"
   de forma geral, o escopo é o repositório inteiro (`backend/**/*.py`,
   `frontend/src/**/*.{ts,tsx}`, `frontend/tests/**/*.{ts,tsx}`) — exceto `.venv/`,
   `node_modules/` e `dist/`, que não são código deste projeto.

2. **Python**: para cada arquivo, remova comentários `#` linha a linha e docstrings (primeira
   `Expr` de string de um módulo/classe/função). Se a docstring era o único conteúdo do corpo de
   uma função/classe, deixe um `pass` no lugar — nunca um corpo vazio (`SyntaxError`). Depois de
   editar, confirme que o arquivo ainda faz `ast.parse` sem erro antes de seguir para o próximo.

3. **TypeScript/TSX**: edite manualmente (não regex-substituir o arquivo inteiro de uma vez) —
   comentário dentro de JSX, union type ou string literal tem sintaxe própria e um regex ingênuo
   corrompe o arquivo. Preste atenção em comentário de fechamento de `catch {}` vazio: remover o
   comentário e deixar o bloco vazio é válido em JS/TS, não precisa de substituto.

4. **Verificar que nada quebrou**:

   ```bash
   cd backend && source .venv/bin/activate && pytest -q
   cd frontend && npm run test -- --run && npm run test:e2e && npm run lint && npm run build
   ```

   Rode só a parte (backend/frontend) que de fato foi alterada, mas sempre rode antes de reportar
   pronto — remoção de comentário não deveria quebrar nada, mas confirmar é mais barato que um
   CI vermelho.

5. **Reportar**: quantos arquivos mudaram e confirmar que os testes/lint/build continuam verdes.
   Não abrir PR sozinho — isso segue a regra normal do projeto (`CLAUDE.md` da raiz: só com
   pedido explícito).

## O que não fazer

- Não remover diretivas funcionais (ver lista acima) — isso quebra `bandit`/`pip-audit`/lint.
- Não reescrever/reformatar código além de remover comentários (não é hora de refatorar).
- Não remover a string de `description=` do FastAPI (`app/main.py`) nem título/descrição
  equivalentes no frontend — são conteúdo exibido (Swagger UI, etc.), não comentário de código.
- Não tocar em `CHANGELOG`, `README.md` ou `CLAUDE.md` — são documentação de propósito, não
  comentário dentro de código.
