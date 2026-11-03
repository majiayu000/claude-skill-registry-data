---
name: Operations Orchestrator (Córtex Central)
description: Skill mestra responsável por gerenciar o fluxo de operações, rotear solicitações e decidir qual skill é a mais apropriada para cada tarefa.
---

# Operations Orchestrator (Córtex Central)

O Córtex Central é o núcleo de tomada de decisão do Agente no Áquila Pro. Ele analisa a intenção do usuário e orquestra o enxame de skills especializadas para entregar o resultado soberano.

## Instruções de Uso
Esta skill deve ser a primeira a ser consultada em qualquer nova solicitação do usuário. Ela define o plano de ação e delega subtarefas.

## Capacidades
- **Intent Mapping**: Classificação de pedidos em categorias (Código, Segurança, UI, Auditoria, Legal).
- **Skill Selection (Routing Matrix)**:
    - *UI/Design* -> `UI Sync`
    - *Segurança/Visão* -> `Vision Worker` + `Experience Intelligence`
    - *Código/Arquitetura* -> `Sovereign Code Governance` + `Performance Audit`
    - *Legal/Dados* -> `LGPD Compliance Guard` + `Document Audit`
    - *Hardware/MCP* -> `MCP Architect` + `NPU Optimizer`
    - *Metabolismo/Evolução* -> `Sovereign Intelligence Evolution (SIE)`
- **Context Awareness**: Leitura do estado atual do "cérebro" (`PROJECT_BRAIN_ORIENTATION.md`) para garantir alinhamento estratégico.
- **Visual Validation**: Uso do `chrome-devtools-mcp` para inspeção dinâmica de resultados.

## Regras Invioláveis (Zero-Bypass)
1. **Consensus Requirement**: Para ações de alto risco (ex: deleção de dados, alteração de firewall), exigir confirmação do usuário ou atingir 60% de consenso no enxame (Nível 22).
2. **Sovereign Alignment**: Nunca rotear tarefas para fluxos que dependam de serviços externos proibidos.
3. **PE-R Cycle**: Todo roteamento deve seguir o ciclo Plan-Execute-Reflect.

## Exemplos
"Antigravity, analise o sistema e decida qual o melhor fluxo para implementar uma nova biometria de voz."
