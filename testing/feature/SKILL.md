---
description: Executa o fluxo completo de implementação de uma feature (entender → pesquisar → implementar com testes → gate rápido → code-reviewer → qa-tester → entrega).
disable-model-invocation: true
argument-hint: "[descrição da feature]"
---

Implemente a feature descrita a seguir seguindo **à risca** o "Fluxo obrigatório de qualidade" do
`CLAUDE.md` raiz e as regras em `.claude/rules/`:

Feature: $ARGUMENTS

Passos:

1. **Entender**: escreva os critérios de aceite. Se a tarefa for grande ou ambígua, apresente um
   plano curto e espere aprovação antes de codificar.
2. **Pesquisar**: para cada biblioteca envolvida, consulte o **context7**
   (`resolve-library-id` → `query-docs`) antes de usar uma API — não confie só na memória.
3. **Implementar com teste** (TDD quando der: teste falhando → código → refatoração), seguindo
   `.claude/rules/python.md`/`typescript.md`/`architecture.md`/`testing.md`/`security.md`
   conforme os arquivos tocados.
4. **Gate rápido**: `python scripts/quality_gate.py --fast` — corrija tudo antes do passo 5.
5. **Revisão**: invoque o subagent `code-reviewer` com o objetivo, os critérios de aceite, os
   arquivos alterados, a branch base e como rodar os testes. Reprovado → corrija todo
   `[BLOQUEANTE]`/`[IMPORTANTE]` e invoque de novo (máx. 3 rodadas).
6. **QA**: com a revisão aprovada, invoque `qa-tester` com o mesmo briefing. Reprovado → cada bug
   vira um teste que falha, corrija, **volte ao passo 5** (qualquer mudança de código invalida a
   aprovação anterior; máx. 3 rodadas).
7. Sem convergência em 3 rodadas numa etapa, pare e explique o impasse com opções — não insista.
8. **Entrega**: resuma o que mudou e por quê, os vereditos finais, evidências do `qa-tester`,
   sugestões não bloqueantes e pendências. **Não commite nem dê push** sem autorização explícita.
