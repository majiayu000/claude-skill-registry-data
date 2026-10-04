---
name: antigravity-guide
description: "Guia Completo e Referência Canônica para Google Antigravity (AGY), cobrindo Antigravity CLI (agy), Antigravity 2.0 Desktop, IDE, Python SDK, slash commands, keybindings e o Sistema de Customizações (Skills, Rules, Plugins, Hooks, Sidecars e MCP Servers). Use esta skill quando for requisitado a explicar, configurar ou customizar o ecossistema Antigravity."
---

# Google Antigravity (AGY) Guide, Architecture & Customizations

O **Google Antigravity** é uma plataforma de desenvolvimento assistido por inteligência artificial em pares (*AI-first pair programming*). Esta skill unifica o guia operacional das superfícies do Antigravity com o **Sistema Completo de Customizações** (Skills, Rules, Plugins, Hooks e MCP Servers).

---

## 🖥️ 1. Superfícies do Ecossistema (Documentação Local)

- **Antigravity CLI (`agy`)**: [`references/cli.md`](references/cli.md) — Comandos de barra (*slash commands*), flags de linha de comando, configuração de terminals e boas práticas.
- **Antigravity IDE**: [`references/ide.md`](references/ide.md) — IDE standalone, painéis laterais de chat, lentes de código embutidas e atalhos de teclado.
- **Antigravity 2.0**: [`references/app.md`](references/app.md) — Aplicação desktop paralela, Chat Canvas, Painel Auxiliar HTML (Subagentes, Tarefas em Segundo Plano, Artefatos, Arquivos Alterados e Terminais Persistentes).
- **Antigravity Python SDK**: [`references/sdk.md`](references/sdk.md) — SDK oficial para locação de agentes, orquestração e exposição de ferramentas customizadas.

---

## ⚙️ 2. Sistema de Customizações (Extensibilidade)

O sistema de customizações permite adaptar o comportamento do agente, ensinar procedimentos, aplicar regras de codificação e integrar serviços externos:

| Tipo | Configuração / Diretório | Escopo | Aplicação Primária | Referência Local |
| :--- | :--- | :--- | :--- | :--- |
| **Rules** | `GEMINI.md`, `AGENTS.md` | Contextual / Hierárquico | Padrões de código, restrições de arquitetura e diretrizes locais | [`references/customizations/rules.md`](references/customizations/rules.md) |
| **Skills** | `skills/<nome>/SKILL.md` | Sob Demanda (*Progressive*) | Procedimentos em múltiplos passos, runbooks, orquestração de ferramentas | [`references/customizations/skills.md`](references/customizations/skills.md) |
| **Plugins** | `plugins/<nome>/plugin.json`| Pacote Integrado | Empacotamento unificado de skills, rules e servidores MCP | [`references/customizations/plugins.md`](references/customizations/plugins.md) |
| **Hooks** | `hooks.json` | Eventos de Ciclo de Vida | Execução de scripts pré/pós execução de ferramentas | [`references/customizations/hooks.md`](references/customizations/hooks.md) |
| **MCP Servers** | `mcp_config.json` | Integração de Ferramentas | Conexão com serviços externos via Model Context Protocol | [`references/customizations/mcp_servers.md`](references/customizations/mcp_servers.md) |

---

## 📍 3. Locais de Descoberta e Precedência de Carregamento

1. **Customizações da Workspace (Projeto)**:
   - Pastas `.agents/` ou `.agent/` na raiz do projeto (versionadas no Git).
2. **Regras Hierárquicas de Diretório**:
   - `GEMINI.md`, `AGENTS.md`, `.agents/rules/*.md`. O agente sobe recursivamente até a raiz do repositório agregando as regras.
3. **Configuração Global (Máquina Local)**:
   - `~/.gemini/config/` para regras e MCPs compartilhados entre todos os projetos da máquina.

---

## 🌐 4. Documentação Online Atualizada

Para novidades e integrações com a Vertex AI:
- Documentação Principal: `https://antigravity.google/docs`
- Customizações (Skills/Rules/MCP): `https://antigravity.google/docs/skills`
- Changelog: `https://antigravity.google/changelog`
