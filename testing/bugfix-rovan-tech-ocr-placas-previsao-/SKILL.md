---
description: Reproduz um bug com um teste que falha, corrige e segue o fluxo completo (code-reviewer → qa-tester → entrega).
disable-model-invocation: true
argument-hint: "[descrição do bug]"
---

Corrija o bug descrito a seguir seguindo o "Fluxo obrigatório de qualidade" do `CLAUDE.md` raiz:

Bug: $ARGUMENTS

Passos:

1. **Reproduzir primeiro**: escreva um teste (pytest ou Vitest, conforme onde o bug vive) que
   falha *antes* de qualquer correção — esse teste descreve o comportamento esperado. Não avance
   para a correção sem ele falhando de verdade.
2. **Pesquisar**: se o bug envolve uma biblioteca, confirme via **context7** que o uso atual está
   correto/atualizado antes de assumir que é bug de lógica própria.
3. **Corrigir** a causa raiz (não sintoma) seguindo `.claude/rules/`. O teste do passo 1 vira o
   teste de regressão — deve passar a passar.
4. **Gate rápido**: `python scripts/quality_gate.py --fast`.
5. **Revisão**: invoque `code-reviewer` (objetivo = o bug + o teste de regressão, arquivos
   alterados, branch base, como rodar). Reprovado → corrija e invoque de novo (máx. 3 rodadas).
6. **QA**: com a revisão aprovada, invoque `qa-tester`. Reprovado → novo teste por bug encontrado,
   corrija, **volte ao passo 5** (máx. 3 rodadas).
7. Sem convergência em 3 rodadas, pare e explique o impasse com opções.
8. **Entrega**: resuma causa raiz, correção, teste de regressão, vereditos e evidências. **Não
   commite nem dê push** sem autorização explícita.
