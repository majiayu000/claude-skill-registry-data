---
name: auto-update
description: Check and update Claude Code to latest version, update plugins, and show changelog.
disable-model-invocation: true
allowed-tools: Bash Read WebFetch
argument-hint: [--check | --full]
---

# Auto-Update Claude Code + Plugins

## Passo 1 — Checar versão atual

```!
claude --version 2>/dev/null || echo "unknown"
```

## Passo 2 — Verificar se há update disponível

```bash
npm show @anthropic-ai/claude-code version 2>/dev/null
```

## Passo 3 — Se houver update

1. Mostrar versão atual vs disponível
2. Buscar changelog em https://github.com/anthropics/claude-code/releases
3. Listar mudanças relevantes para o workflow DME
4. Perguntar se quer atualizar

## Passo 4 — Atualizar (se autorizado)

```bash
npm update -g @anthropic-ai/claude-code
```

## Passo 5 — Atualizar plugins

```bash
claude /reload-plugins
```

## Passo 6 — Verificar integridade

1. Confirmar que agents em `~/.claude/agents/` estão intactos
2. Confirmar que skills em `~/.claude/skills/` estão intactas
3. Confirmar que `settings.json` não foi sobrescrito
4. Reportar status final
