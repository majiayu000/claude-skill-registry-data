---
name: mcp-usage
description: Descreve como usar MCPs relevantes (filesystem, git, runtime) para trabalhar com o projeto Daylyou.
---

# Skill: MCP Usage para o Daylyou

## Filesystem MCP
- Usa o filesystem MCP para:
  - ler ficheiros longos,
  - escrever alterações usando patches,
  - criar novos ficheiros ou pastas.
- Nunca alteres ficheiros fora da pasta do projeto Daylyou.

## Git MCP
- Antes de um conjunto de alterações:
  - verifica o estado (`git status`);
  - cria uma branch nova (ex: `feature/habits-layout`).
- Depois de completar uma micro-tarefa:
  - faz commit com mensagem clara (ex: `feat(habits): add basic habits page layout`).
- Evita commits gigantes com mudanças misturadas.

## Runtime MCP
- Usa o runtime MCP para:
  - correr `npm run dev` ou `npm run lint`;
  - executar scripts específicos (ex: seed de dados, testes).
- Se um comando falhar, lê o erro com atenção e devolve-me um resumo claro + sugestão.

## Ordem recomendada numa tarefa grande
1. Task Breakdown → plano de passos.
2. Git → nova branch.
3. Filesystem → editar ficheiros (safe-editing).
4. Runtime → correr testes/dev server.
5. Git → commit.
