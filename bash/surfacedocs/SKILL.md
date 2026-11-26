---
name: surfaceDocs
description: Keep the command reference (docs/reference.md) and the Mermaid diagrams (docs/diagrams/*.mmd) generated from the code (rules 55, 103). Use when adding or changing a command, a flag, an MCP tool, a hook or a page state, or when `bun run check:docs` refuses a commit.
---

# surfaceDocs

The command reference, `docs/reference.md`, and `docs/diagrams/*.mmd` are
generated, never edited by hand (the README is only for setting up, rule 103).
What is generated and checked is in the spec, [Command shape](../../docs/specs/commandShape.md).
Everything comes from the code:

| What | From |
|---|---|
| Each command, what it does, its flags | `COMMANDS` (`src/cli/runner/index.ts`), each command's `usage` |
| Its MCP tool, or why it is terminal-only | `toolsFromCommands`, `TERMINAL_ONLY` |
| The hooks that fire on it (shell, MCP) | `AGENT_HOOKS` (`src/agentHooks/registry`) |
| Live log, rules | `LONG_RUNNING`, `COMMAND_RULES` |
| Saved flows | `src/browser/flow/definitions/*.json` |
| Page states | `PAGE_STATES` (`src/browser/flow/helpers/pageState.ts`) |
| Which browser each command runs on | `commandBrowser`, `OPENER_ACTIONS`, `IN_OPEN_BROWSER`, `CAMOUFOX_ONLY` (`src/browser/run`) |
| The browsers | `BROWSER_DRIVERS` (`src/browser/driver`) |

`src/surface/catalog` gathers it, `src/surface/diagrams` draws the diagrams
(browsers, platforms, surface, commands, hooks, pageStates), and
`src/surface/readme` writes the section of `docs/reference.md` between
`<!-- surface:start` and `<!-- surface:end -->`.

log-cli is browser-agnostic: no command summary or page heading
presents one browser as log-cli's. A command moved onto the driver goes from `CAMOUFOX_ONLY` to
`OPENER_ACTIONS`, and the Browsers section and its diagram follow. The check
parses every diagram with Mermaid (as GitHub does): text in a label, note or
message goes through `label()`, which escapes quotes, angle brackets and `;`.

## After a change

```bash
bun run docs:build     # rewrites docs/reference.md's section and docs/diagrams/*.mmd
bun run check:docs     # what lefthook runs: refuses any drift
```

## A new command or flag

- Give the command a `usage` (its `*_USAGE` constant): every subcommand and flag.
  The typecheck refuses a command without one.
- A flag the command parses (`parseArgs`, `takePairs`, `token === "--x"`) must be
  in its usage, and every flag in its usage must be parsed: `check:docs` names
  the folder and the flag either way.
- The MCP tool's description carries the same usage, so agents over MCP see the
  same flags as the terminal.
