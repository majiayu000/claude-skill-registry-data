---
name: squad-visualizer
description: Gera e exibe o dashboard visual da squad. Use quando o usuário pedir para "apresentar a squad", "mostrar como vocês funcionam" ou "exibir o dashboard dos agentes".
---

# Skill: Squad Visualizer

**Objetivo:** Esta skill permite que o agente forneça uma apresentação visual ou um painel de controle interativo expondo a governança, a configuração e os papéis dos membros ativos da equipe.

## Gatilhos (Execution Triggers)
Deve ser acionada sempre que o usuário mandar comandos como:
- "Quem são vocês?"
- "Apresente a squad"
- "Dashboard visual"
- "Como a inteligência está organizada?"

## Workflow de Execução

1. **Verificação de Instalação e Leitura de Registry:**
   - ATENÇÃO: Esta skill só deve operar se a Squad já estiver instalada no repositório atual do usuário.
   - Consulta o arquivo principal `.claude/commands/manager.md` e a pasta `.claude/agents/` (incluindo os respectivos arquivos `.md` dos agentes como `product-owner.md`, `techlead.md`, `architect.md`, `developer.md`, `qa-specialist.md`, `security.md`, `ops.md`) para confirmar quais papéis e agentes estão ativos e montar a visão correta do ecossistema.

2. **Reconstrução Dinâmica da Interface (Dashboard Vivo):**
   - O arquivo `dashboard.html` NUNCA deve ser considerado estático. Antes de exibí-lo, o agente atuante DEVE OBRIGATORIAMENTE varrer os arquivos atuais da fundação (`.claude/commands/manager.md`, os manifestos individuais em `.claude/agents/` e a pasta de `.claude/skills/`).
   - Com os dados reais e estruturados em sua memória, o agente vai Reescrever/Atualizar as seções de agentes e fluxos dentro do `.claude/dashboard.html` preservando seu estilo moderno (CSS), transparecendo os Tiers, Ferramentas acopladas e Nomes que acabaram de ser lidos. Assim a tela será um reflexo vivo, idêntico à squad em uso naquele milissegundo.

3. **Hospedagem e Apresentação (SEMPRE via Localhost):**
   - O agente DEVE rodar um servidor na pasta `.claude` usando a tool de comandos do terminal (ex: `python3 -m http.server 8080`).
   - Finaliza fornecendo ao usuário OBRIGATORIAMENTE uma URL localhost para ele clicar (ex: `http://localhost:8080/dashboard.html`). Não retorne chaves ou formatos em `file:///`. A experiência de entrega final do dashboard se dá pela URL web ativa.
