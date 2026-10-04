---
name: refactor
description: Skill para reestruturação estrutural de código sem alterar o comportamento externo, melhorando manutenibilidade.
---

# Skill: Safe Code Refactoring (Lean)

Esta skill é focada em aplicar técnicas de refatoração seguras para diminuir dívida técnica, geralmente acionada pelo `architect` ou `techlead`.

## Pré-requisitos
- O código atual DEVE ter cobertura de testes ou se comportar de maneira validável antes da refatoração.
- As diretrizes base devem ser lidas em `memorys/guidelines.md`.

## Passos de Execução
1. **Entendimento da Base**: Avalie o arquivo ou componente alvo, listando as responsabilidades (Single Responsibility Principle) que ele fere atualmente.
2. **Plano de Corte**: Crie um `docs/todo/[NOME_REFACTOR].md` definindo os micro-passos (extrair função, mover componente, unificar interfaces).
3. **Delegação**: O `techlead` delega a task criada no passo 2 para o `developer` executar, informando que o comportamento (features) deve permanecer intacto.
4. **Verificação (QA)**: O `.claude/agents/qa-specialist.md` revisa se os testes continuam passando.
