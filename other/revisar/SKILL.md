---
description: Roda só o subagent code-reviewer sobre o diff atual (contra a branch base) e mostra o relatório.
disable-model-invocation: true
---

Invoque o subagent `code-reviewer` sobre as mudanças atuais (diff da working tree contra a
branch base, mais arquivos novos não rastreados). Passe no briefing: objetivo (inferido da
conversa ou pergunte se não estiver claro), a lista de arquivos alterados (`git status`/`git
diff --name-only`), a branch base, e como subir a aplicação/rodar os testes (ver `CLAUDE.md`).

Depois do relatório, apresente o veredito e a lista de problemas ao usuário — **não corrija nada
automaticamente**; pergunte se quer que você corrija os itens bloqueantes antes de seguir.
