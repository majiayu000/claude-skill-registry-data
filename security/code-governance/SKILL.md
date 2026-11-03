---
name: Sovereign Code Governance
description: Rege a criação, refatoração e auditoria de código no ecossistema Áquila Pro sob o paradigma Agent-First.
---

# Sovereign Code Governance

Este documento define os padrões de excelência para o desenvolvimento do Áquila Pro.

## Instruções de Uso
Ativar em toda tarefa de desenvolvimento, refatoração ou auditoria de código.

## Capacidades
- **Protocolo de Subagente**: Spawn de subagentes para exploração arquitetural e review de commits.
- **Commit Audit**: Validação contra o `CLAUDE.md`.
- **NPU Awareness**: Estratégias para delegação de processamento pesado.

## Regras Invioláveis (Zero-Bypass)
1. **Cloud Isolation**: O código deve ser resiliente a falhas de rede e priorizar processamento local.
2. **LGPD First**: Todo dado de aluno deve ser acessado via `SecurityService`.
3. **Architecture Sync**: Seguir rigorosamente o `PROJECT_BRAIN_ORIENTATION.md`.

## Exemplos
"Refatore o serviço de biometria seguindo a governança de código soberano."
