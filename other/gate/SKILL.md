---
description: Roda o gate de qualidade completo (scripts/quality_gate.py --full) e resume o resultado.
disable-model-invocation: true
---

Rode `python scripts/quality_gate.py --full` (ou `python3`, conforme o SO — ver
`.claude/rules/git.md`/`CLAUDE.md`) a partir da raiz do repositório.

Depois de rodar:

1. Se tudo passar, informe isso em 1-2 linhas — não repita a saída completa do comando.
2. Se algo falhar, resuma **por etapa** o que falhou (ex.: "mypy: 3 erros em
   `app/services/x.py`", "vitest: 2 testes falhando em `checkinsTrend.test.ts`") e pergunte se o
   usuário quer que você corrija antes de seguir — não corrija automaticamente sem perguntar,
   a menos que o usuário já tenha pedido isso na mesma mensagem que invocou `/gate`.
