---
name: Skill Inventory Manager
description: Habilidade para gerenciar, auditar e reportar as capacidades operacionais do Agente.
---

# Skill Inventory Manager

Gestor do catálogo de competências do Áquila Pro.

## Instruções de Uso
Ativar quando o usuário solicitar status do agente, lista de habilidades ou auditoria de capacidades.

## Capacidades
- **Catalog Audit**: Listagem e leitura de metadados em `.agent/skills/`.
- **Health Check**: Verificação de integridade e prontidão operacional de cada skill.
- **Dynamic Reporting**: Geração de dashboards Markdown de prontidão (Ativas/Pendentes).

## Regras Invioláveis (Zero-Bypass)
1. **Governance Link**: Sempre referenciar a [governance_matrix.md](file:///c:/aquila/.agent/governance_matrix.md).
2. **Privacy Audit**: Verificar se as novas skills possuem as travas LGPD necessárias.
3. **No Ghost Skills**: Skills sem `SKILL.md` válido devem ser reportadas como "Críticas/Inoperantes".

## Exemplos
"Gere um relatório completo das habilidades atuais do agente e identifique lacunas na cobertura de segurança."
