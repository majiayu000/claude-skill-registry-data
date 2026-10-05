---
name: aiox-story-cycle
description: >
  Executa o ciclo completo de uma story AIOX: criação (@sm), validação (@po),
  implementação (@dev), QA gate (@qa), correção e fechamento (@po).
  Usar quando o workflow selecionado for story-development-cycle.
---

# AIOX Story Cycle — Ciclo Completo de Story

## Quando esta skill é acionada

Automaticamente quando o workflow determinado for `story-development-cycle` e houver necessidade de criar, validar, implementar ou revisar uma story.

## Sequência de agentes

```
@sm → @po → @dev → @qa → @dev (corrige) → @qa (veredito) → @po (fecha) → @devops (push)
```

## Fase 1: Criação (@sm)

**Task:** `create-next-story.md`
**Agente:** aiox-sm
**Input:** PRD sharded, epic context
**Output:** `docs/stories/story-{epic}.{num}-{slug}.md` com status Draft

Story deve conter: problema, valor, causa raiz, escopo IN/OUT, dependências, riscos, baseline, estado-alvo, AC testáveis (Given/When/Then), testes unitários/integração/regressão, NFR, arquivos afetados, DoD, rollback, restrição de nova dívida.

## Fase 2: Validação (@po)

**Task:** `validate-next-story.md`
**Agente:** aiox-po
**Checklist 10 pontos** (ver `story-lifecycle.md`)
**Veredito:** GO (>=7) → status Ready | NO-GO → retorna ao @sm

## Fase 3: Implementação (@dev)

**Task:** `dev-develop-story.md`
**Agente:** aiox-dev
**Subagent_type:** aiox-dev
**Status:** Ready → InProgress → InReview

Regras do @dev:
- Trabalhar exclusivamente da story validada
- Um incremento por vez, atualizar checkboxes imediatamente
- NÃO: ampliar escopo, duplicar lógica, reduzir cobertura, esconder falhas, alterar contratos públicos sem testes, introduzir TODO sem backlog
- Trabalho fora do escopo → backlog como follow-up/débito/nova story

## Fase 4: QA Gate (@qa)

**Task:** `qa-gate.md`
**Agente:** aiox-qa
**Status:** InReview → Done (ou InProgress se FAIL)

Verificações conforme risco: rastreabilidade, regressão, segurança, integridade, erros, observabilidade, performance, edge cases, concorrência, migrations, compatibilidade, dívida introduzida.

**Veredito:**
- PASS → prossegue para fechamento
- CONCERNS → aprova com itens de backlog (owner, severidade, prazo)
- FAIL → retorna ao @dev
- WAIVED → justificativa documentada

## Fase 5: Correção (@dev)

Se QA FAIL: @dev aplica correções → @qa re-avalia (QA Loop, max 5 iterações).

## Fase 6: Fechamento (@po)

**Task:** `po-close-story.md`
**Agente:** aiox-po

Verifica: veredito QA, checkboxes, status, epic, backlog, débitos, follow-ups, DoD, próxima story.

## Fase 7: Publicação (@devops)

**Agente:** aiox-devops
Pré-condições: story fechada, QA veredito aceitável, lint/typecheck/testes/build passam.

## Condições de interrupção

- Ambiguidade material nos requisitos
- Bloqueio por dependência não resolvida
- QA Loop atinge max iterações (5)
- Violação constitucional detectada
- Operação destrutiva sem autorização

## Artefatos obrigatórios

- Story file em `docs/stories/`
- QA gate result
- Change Log atualizado
- File List atualizada
- PO close confirmation

## Referências

- Story lifecycle: `.claude/rules/story-lifecycle.md`
- Workflow: `.aiox-core/development/workflows/story-development-cycle.yaml`
- Tasks: `.aiox-core/development/tasks/create-next-story.md`, `validate-next-story.md`, `dev-develop-story.md`, `qa-gate.md`, `po-close-story.md`
- QA Loop: `.aiox-core/development/workflows/qa-loop.yaml`
