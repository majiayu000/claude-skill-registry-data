---
description: Roda só o subagent qa-tester sobre as mudanças atuais (gate completo + exploratório) e mostra o relatório.
disable-model-invocation: true
---

Invoque o subagent `qa-tester` sobre as mudanças atuais. Passe no briefing: os critérios de
aceite (inferidos da conversa ou pergunte se não estiver claro), os arquivos alterados, a branch
base, e como subir a aplicação e rodar os testes (`npm run dev` na raiz; ver `CLAUDE.md`).

Depois do relatório, apresente o veredito, os bugs encontrados e as evidências ao usuário — **não
corrija nada automaticamente**; pergunte se quer que você transforme os bugs em teste de
regressão e corrija antes de seguir.
