---
name: aiox-brownfield
description: >
  Executa o workflow Brownfield Discovery para diagnóstico de sistemas legados
  e planejamento de saneamento por waves. Usar quando o usuário solicitar
  auditoria, diagnóstico ou análise de sistema legado.
---

# AIOX Brownfield — Discovery e Saneamento de Legado

## Quando esta skill é acionada

- "faça a auditoria do sistema"
- "analise o estado do código"
- "diagnostique a dívida técnica"
- "mapeie o sistema legado"
- Qualquer solicitação de avaliação sistêmica de código existente

## Discovery (10 fases)

| Fase | Agente | Output |
|------|--------|--------|
| 1 | @architect | `system-architecture.md` |
| 2 | @data-engineer | `SCHEMA.md` + `DB-AUDIT.md` |
| 3 | @ux-design-expert | `frontend-spec.md` |
| 4 | @architect | `technical-debt-DRAFT.md` |
| 5 | @data-engineer | `db-specialist-review.md` |
| 6 | @ux-design-expert | `ux-specialist-review.md` |
| 7 | @qa | `qa-review.md` (APPROVED | NEEDS WORK) |
| 8 | @architect | `technical-debt-assessment.md` |
| 9 | @analyst | `TECHNICAL-DEBT-REPORT.md` |
| 10 | @pm | Epic + stories |

## Pós-Discovery (obrigatório)

**Discovery Complete ≠ Sistema Saneado.**

1. Revisão de débitos por causa raiz
2. Agrupamento por dependências
3. Organização em waves
4. Refinamento de stories (@sm)
5. Validação (@po)
6. Implementação (@dev)
7. QA local (@qa)
8. Fechamento (@po)
9. Gate sistêmico ao final de cada wave (@architect + @qa)
10. Atualização do baseline

## Waves — ordem preferencial

```
Wave 1: segurança e integridade de dados
Wave 2: build, testes e observabilidade
Wave 3: fronteiras e fundações arquiteturais
Wave 4: redução de acoplamento e duplicação
Wave 5: performance e confiabilidade
Wave 6: UX, acessibilidade e consistência
Wave 7: otimizações não críticas
```

## Agrupamento de débitos

Antes de criar stories, @architect verifica causas raiz comuns. Agrupar por: causa raiz, fronteira arquitetural, dependências, domínio, risco, camada, ordem necessária, potencial de regressão.

Evitar stories de remendo quando mudança estrutural trata a origem comum.

## Ledger de dívida técnica

Manter em `docs/technical-debt/ledger.md`. Cada item: ID, descrição, causa raiz, origem, categoria, severidade, probabilidade, impacto, status, owner, story, wave, data, prazo, evidência, decisão.

Status: Identified → Validated → Planned → In Progress → Partial → Resolved | Accepted | False Positive | Obsolete

## Condições de interrupção

- Discovery QA Gate retorna NEEDS WORK (retorna à fase 4)
- Gate sistêmico de wave falha (próxima wave bloqueada)
- Débito HIGH sem owner e prazo

## Referências

- Workflow: `.aiox-core/development/workflows/brownfield-discovery.yaml`
- Protocolo: `.claude/rules/aiox-project-operating-protocol.md`
- Ledger template: `docs/technical-debt/ledger.md`
