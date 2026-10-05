---
name: aiox-route
description: >
  Classifica solicitações do usuário e seleciona automaticamente o workflow,
  nível de risco e agentes AIOX apropriados. Usar quando o usuário fizer
  qualquer pedido de desenvolvimento sem especificar @agente ou workflow.
---

# AIOX Route — Roteamento Automático

## Quando esta skill é acionada

Automaticamente quando o usuário solicita em linguagem natural qualquer ação de desenvolvimento sem usar `@agente` ou nome de workflow explícito.

**Gatilhos:** "corrija", "implemente", "refatore", "crie", "adicione", "altere", "publique", "faça deploy", "audite", "migre", "otimize", "limpe".

## Classificação

### Nível FAST
- Correção de typo em documentação
- Alteração cosmética isolada
- Mudança trivial comprovadamente sem efeito funcional
- Arquivo de configuração não-crítico

**Fluxo:** Registro leve → diff revisado → sem push automático.

### Nível STANDARD (default)
- Bugs
- Features localizadas
- Refatorações limitadas
- Qualquer coisa não classificada como FAST ou HIGH-RISK

**Fluxo:** @sm → @po → @dev → @qa → @po → @devops

### Nível HIGH-RISK
- Segurança, autenticação, autorização
- Dados, migrations, schema
- Pagamentos, produção
- Arquitetura, infraestrutura
- Refatorações amplas, mudanças sistêmicas

**Fluxo:** @architect (+ @data-engineer se DB) → @sm → @po → @dev → @qa aprofundado → gate sistêmico → @po → @devops

## Mapeamento solicitação → workflow

| Solicitação | Workflow | Nível |
|------------|----------|-------|
| Typo, doc, cosmético | Nenhum | FAST |
| Bug, erro, falha, não funciona | story-development-cycle | STANDARD |
| Feature, funcionalidade, implementar, adicionar | spec-pipeline → story-development-cycle | STANDARD |
| Refatorar, reestruturar, limpar | análise de impacto → story-development-cycle | STANDARD ou HIGH-RISK |
| Migration, schema, banco | data-engineer pipeline → story-development-cycle | HIGH-RISK |
| Segurança, auth, vulnerabilidade | security-review → story-development-cycle | HIGH-RISK |
| Publicar, deploy, push, release | pre-push gates → devops push | STANDARD (gates) |
| Auditoria, discovery, diagnóstico | brownfield-discovery | STANDARD |
| Arquitetura, design sistêmico | architect analysis → spec pipeline | HIGH-RISK |

## Saída

Após classificação, informar ao usuário:
- Nível de risco e justificativa
- Workflow selecionado
- Agentes que serão acionados
- Story necessária (sim/não)
- Próximo passo

## Referências

- Protocolo: `.claude/rules/aiox-project-operating-protocol.md`
- Workflows: `.aiox-core/development/workflows/`
- Agent authority: `.claude/rules/agent-authority.md`
- Constitution: `.aiox-core/constitution.md`
