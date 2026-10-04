---
name: harness
description: >
  Inspeciona, diagnostica e melhora o harness de desenvolvimento do projeto
  para Claude Code e OpenAI Codex e o harness de runtime em Google ADK. Use
  para auditar o que realmente está ativo, investigar regras ignoradas, portar
  configuração entre os hosts ou adicionar guias, skills, hooks, testes e
  sensores de CI.
allowed-tools: Read, Grep, Glob, Bash(ruff:*), Bash(mypy:*), Bash(pytest:*)
license: MIT
metadata:
  version: "3.0"
---

# Harness do Projeto (Claude Code + Codex + GitHub Copilot + ADK)

Trate o projeto como dois contextos de execução:

1. O **harness de desenvolvimento** governa Claude Code, Codex ou GitHub Copilot (VS Code) enquanto alteram o repositório.
2. O **harness de runtime** governa agentes que a aplicação executa com Google ADK.

Identifique primeiro qual contexto e qual host a solicitação afeta. Não pressuponha que um artefato documentado exista ou esteja ativo.

## Inventariar antes de diagnosticar

Execute um inventário mínimo:

```bash
git status --short
rg --files -uu \
  -g 'AGENTS.md' -g 'AGENTS.override.md' -g 'CLAUDE.md' \
  -g '.agents/**' -g '.claude/**' -g '.codex/**' \
  -g '.github/copilot-instructions.md' -g '.github/instructions/**' \
  -g '.github/prompts/**' -g '.github/agents/**' -g '.github/hooks/**' \
  -g '.github/skills/**' -g '.mcp.json' -g '.pre-commit-config.yaml' \
  -g '.github/workflows/**' -g 'tests/**' -g 'harness/**'
```

Classifique cada item citado na documentação como:

- **ativo**: existe e o host o descobre;
- **presente, mas não conectado**: existe sem mecanismo de carregamento;
- **planejado**: aparece apenas em documentos;
- **ausente**: não existe e não está declarado como plano.

Relate essa classificação. Nunca descreva um sensor planejado ou ausente como proteção ativa.

## Harness de desenvolvimento

### Camada compartilhada

| Artefato | Papel |
|---|---|
| `CLAUDE.md` | contexto de arquitetura, convenções e fluxo de trabalho compartilhado neste repositório |
| `AGENTS.md` | entrada do Codex e do GitHub Copilot (lido diretamente pelo VS Code) e ponte explícita para o contexto compartilhado |
| `.agents/skills/*/SKILL.md` | skills descobertos tanto pelo Codex quanto pelo GitHub Copilot, sem duplicação |
| `pyproject.toml` | dependências, configuração de testes e limites do pacote Python |
| testes em `tests/` | sensores determinísticos compartilhados pelos hosts |
| pre-commit e CI, quando existirem | sensores fora do loop do modelo |

Mantenha regras compartilhadas em um ponto canônico sempre que possível. Se uma regra continuar em `CLAUDE.md`, preserve em `AGENTS.md` a instrução explícita para o Codex e o Copilot lerem esse arquivo. Nunca crie `.github/copilot-instructions.md` junto de `AGENTS.md` — o VS Code trata os dois como alternativos e recomenda usar apenas um.

### Claude Code

| Artefato | Papel |
|---|---|
| `CLAUDE.md` | instrução persistente carregada pelo Claude Code |
| `.claude/rules/*.md` | regras condicionais por caminho |
| `.claude/skills/*/SKILL.md` | skills do projeto |
| `.claude/commands/**/*.md` | comandos personalizados |
| `.claude/agents/*.md` | subagentes especializados |
| `.claude/settings.json` | permissões e hooks versionados |
| `.claude/settings.local.json` | preferências locais não versionadas |

Use `/doctor` para conferir instruções e skills e `/hooks` para inspecionar hooks carregados.

### OpenAI Codex

| Artefato | Papel |
|---|---|
| `AGENTS.md` e `AGENTS.override.md` | instruções descobertas da raiz até o diretório atual |
| `.agents/skills/*/SKILL.md` | skills de repositório, invocáveis com `$nome` |
| `.agents/skills/*/agents/openai.yaml` | metadados opcionais de interface e política do skill |
| `.codex/config.toml` | configuração de projeto, carregada apenas em projeto confiável |
| `.codex/hooks.json` | hooks de ciclo de vida, também sujeitos à confiança do projeto |

Use `/skills` para confirmar a descoberta do skill e `/hooks` para revisar, confiar e depurar hooks. Reinicie a sessão se instruções antigas continuarem em contexto.

Não trate `.claude/commands/`, `.claude/agents/` ou `.claude/settings.json` como configuração automática do Codex. Porte o comportamento necessário para os equivalentes do Codex.

### GitHub Copilot (VS Code)

| Artefato | Papel |
|---|---|
| `AGENTS.md` | instrução persistente lida diretamente pelo VS Code (alternativa a `.github/copilot-instructions.md`, use só uma) |
| `.agents/skills/*/SKILL.md` ou `.github/skills/*/SKILL.md` | skills do projeto; o Copilot já descobre `.agents/skills/`, não é necessário duplicar em `.github/skills/` |
| `.github/instructions/*.instructions.md` | regras condicionais por `applyTo` |
| `.github/prompts/*.prompt.md` | comandos parametrizados de tarefa única |
| `.github/agents/*.agent.md` | subagentes com restrição de ferramentas por papel |
| `.github/hooks/*.json` | hooks de ciclo de vida versionados (workspace) |

Skills e a leitura de `AGENTS.md` já funcionam sem trabalho extra, pois o Copilot os descobre nos mesmos caminhos usados pelo Codex. Hooks e subagentes especializados (`.claude/agents/`, `.claude/settings.json`) não são portados automaticamente — recrie-os em `.github/hooks/` e `.github/agents/` quando o comportamento precisar ser garantido também no Copilot.

## Harness de runtime (Google ADK)

Descubra a implementação real antes de listar componentes. Procure agentes, ferramentas, callbacks, políticas e avaliações:

```bash
rg -n -uu 'google\.adk|Agent\(|BaseAgent|tool|callback|guard|eval' \
  --glob '*.py' --glob '!**/.venv/**'
```

Considere como sensores de runtime somente os componentes efetivamente importados ou executados pela aplicação. `AGENTS.md` configura o Codex; ele não configura agentes Google ADK automaticamente. Só o classifique como prompt de runtime se o código da aplicação o carregar de modo explícito.

## Diagnosticar uma regra ignorada

### 1. Localizar a regra

```bash
rg -n -uu '<palavra-chave>' \
  AGENTS.md CLAUDE.md .agents .claude .codex tests pyproject.toml
```

Se a regra não estiver documentada, adicione um guia inferencial no host correto.

### 2. Localizar o mecanismo de aplicação

Verifique hooks, testes, pre-commit e CI existentes. Separe uma recomendação ao modelo de um bloqueio determinístico.

### 3. Confirmar descoberta e execução

- No Claude Code, inspecione `/doctor` e `/hooks`.
- No Codex, inspecione `/skills` e `/hooks`; confirme que o projeto está confiável para carregar `.codex/`.
- No GitHub Copilot, confirme que o skill aparece no seletor de barra (`/`) e que `.github/hooks/*.json` está versionado; skills em `.agents/skills/` não exigem passo extra.
- Para sensores compartilhados, execute diretamente o comando configurado e observe o código de saída.
- Para runtime ADK, rastreie o ponto de importação/registro e execute o teste ou avaliação correspondente.

### 4. Fortalecer a camada certa

Converta falhas repetidas de instrução em sensores determinísticos quando houver uma condição objetivamente verificável. Prefira testes, análise estática, pre-commit ou CI para invariantes de código; use hooks para feedback rápido dentro do host.

## Adicionar guias

### Regra compartilhada

Atualize o contexto canônico do projeto e confirme que ambos os entrypoints de desenvolvimento chegam até ele. Evite copiar parágrafos longos entre `CLAUDE.md` e `AGENTS.md`.

### Regra apenas do Claude Code

Use `CLAUDE.md` para regra global, `.claude/rules/` para escopo por caminho e `.claude/skills/` para fluxos reutilizáveis.

### Regra apenas do Codex

Use `AGENTS.md` para regra global, um `AGENTS.md` aninhado para escopo de diretório e `.agents/skills/` para fluxos reutilizáveis. Inclua apenas `name` e `description` no frontmatter de `SKILL.md`; mantenha metadados de interface em `agents/openai.yaml`.

### Regra apenas do GitHub Copilot

Use `.github/instructions/*.instructions.md` com `applyTo` para escopo por caminho, `.github/prompts/` para tarefas parametrizadas e `.github/agents/*.agent.md` para subagentes com ferramentas restritas. Skills reutilizáveis não precisam de cópia própria: reaproveite `.agents/skills/`.

### Regra de runtime ADK

Coloque a instrução no prompt, spec ou configuração realmente consumida pelo agente. Adicione um teste ou eval que prove o comportamento.

## Adicionar sensores

Priorize sensores compartilhados quando a regra independer do host:

1. teste unitário ou estrutural;
2. lint ou typecheck;
3. pre-commit;
4. CI.

Use hooks específicos para antecipar o feedback:

- Claude Code: `.claude/settings.json`;
- Codex: `.codex/hooks.json`, com scripts em `.codex/hooks/`;
- GitHub Copilot: `.github/hooks/*.json`, um arquivo por hook, sem `matcher` — o script recebido decide com base em `tool_name`.

Ao portar hooks, adapte o formato de entrada. Em hooks do Codex, `apply_patch` aparece como `tool_name: "apply_patch"` e o patch fica em `tool_input.command`; não conte com `tool_input.file_path`. Em hooks do Copilot, ferramentas de edição (`create_file`, `replace_string_in_file`) expõem `tool_input.filePath` diretamente, mais próximo do formato do Claude Code do que do Codex.

Teste cada script de hook diretamente com JSON representativo em `stdin`. Para bloqueio em `PreToolUse`, emita uma decisão suportada ou encerre com código `2` e uma mensagem em `stderr`.

## Medir a saúde

| Sinal | Diagnóstico provável |
|---|---|
| Skill não aparece | diretório errado, descrição inválida ou sessão antiga |
| Skill nunca é acionado implicitamente | descrição pouco específica ou política de invocação desativada |
| Regra funciona no Claude, mas não no Codex | artefato existe apenas em `.claude/` |
| Regra funciona no Claude ou Codex, mas não no Copilot | hook ou subagente existe apenas em `.claude/` ou `.codex/`; falta o equivalente em `.github/` |
| Hook do Codex não executa | projeto não confiável, hook ainda não aprovado ou matcher incorreto |
| Hook do Copilot não executa | arquivo fora de `.github/hooks/`, JSON inválido ou script sem permissão de execução |
| Guia é ignorado repetidamente | regra ambígua ou ausência de sensor determinístico |
| Documento cita proteção inexistente | inventário desatualizado; marque como planejada ou implemente-a |
| Sensor fica lento | mova validação pesada para pre-commit ou CI |

## Concluir a alteração

1. Valide o frontmatter do skill.
2. Valide JSON/TOML e execute scripts adicionados.
3. Execute os testes relevantes do repositório.
4. Revise `git diff --check` e `git diff`.
5. Informe separadamente o que ficou ativo, o que depende de confiança/reinício e o que continua apenas planejado.

## Referências

- `AGENTS.md`
- `CLAUDE.md`
- `.claude/settings.json`
- `.codex/hooks.json`
- [AGENTS.md no Codex](https://developers.openai.com/codex/guides/agents-md/)
- [Skills no Codex](https://developers.openai.com/codex/skills/)
- [Hooks no Codex](https://developers.openai.com/codex/hooks/)
- [Custom instructions no VS Code](https://code.visualstudio.com/docs/copilot/customization/custom-instructions)
- [Agent Skills no VS Code](https://code.visualstudio.com/docs/copilot/customization/agent-skills)
- [Custom Agents no VS Code](https://code.visualstudio.com/docs/copilot/customization/custom-agents)
- [Hooks no VS Code](https://code.visualstudio.com/docs/copilot/customization/hooks)
- [Harness Engineering for Coding Agent Users](https://martinfowler.com/articles/harness-engineering.html)
