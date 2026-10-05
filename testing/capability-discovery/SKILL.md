---
name: capability-discovery
description: "Discover available agents, skills, quality commands (lint, test, typecheck), tech stack, verification capabilities, and LSP code intelligence features via parallel environment scanning. Use when starting implementation, creating PRs, reviewing PRs, or addressing feedback. This skill MUST be consulted because assuming tools exist causes runtime failures, and assuming they do not causes missing capabilities."
allowed-tools: Bash, Read, Glob, Grep, LSP
agent: Explore
---

# Capability Discovery

## Contract

Iron law: discover before assuming — never hardcode tool availability; scan the environment first. Invoked once per command run, before any quality or verification phase: `/flow:start` Phase 1, `/flow:pr` pre-flight, `/flow:address` before verification, `/flow:resolve` step 1c, `/flow:setup` Phase 1, `/flow:design` and `/flow:brainstorm` EXPLORE, and the `test-runner` agent. Returns the six-section markdown report below (Agents Available, Skills Available, Quality Commands, Tech Stack, Verification Capabilities, LSP Capabilities). The calling command stores the output for later phases and does not re-invoke it within the same run. Permitted skips: the markdown-only early exit (no tech-stack file and no quality commands in CLAUDE.md) and LSP probing when `lsp.enabled` is `false`.

## Detection Order

Steps 1-5 are independent — run them simultaneously with parallel tool calls.

1. **Agents**: `Glob ".claude/agents/*.md"` (project) and `"plugins/*/agents/*.md"` (plugin); parse source, name (filename without `.md`), description (frontmatter).
2. **Skills**: `Glob ".claude/skills/*/SKILL.md"` and `"plugins/*/skills/*/SKILL.md"`; parse source, name (parent directory), description.
3. **Commands**: `Glob ".claude/commands/*.md"` and `"plugins/*/commands/*.md"`; parse source, name, description.
4. **Quality commands from CLAUDE.md** — `.claude/CLAUDE.md` first, then `CLAUDE.md`:

   ```bash
   grep -E "(npm|pnpm|yarn|bun|ruff|pytest|go |cargo |make )" "$CLAUDE_MD"
   ```

5. **Tech stack** by indicator file: `package.json` → node, `tsconfig.json` → typescript, `pyproject.toml` → python, `Gemfile` → ruby, `go.mod` → go, `Cargo.toml` → rust, `Makefile` → makefile.

**Early exit — markdown-only**: no tech-stack file AND no quality commands in CLAUDE.md → report Quality Commands "No code-related quality commands applicable", Tech Stack "Markdown-only project", skip Step 6.

6. **Verification capabilities**: `ls verify.sh scripts/verify* playwright.config.* cypress.config.* 2>/dev/null`.

   Also probe the four dependency-license tools (`license-checker`, `pip-licenses`, `cargo-license`, `go-licenses`) that `agents/security-reviewer.md` Step 4 uses, and `jscpd`, the clone detector `bin/flow-clone-scan.sh` drives. Commands and output lines: `references/runtime-verification-probes.md` § Tool probes.

   An absent tool is reported `not-installed` with its install command, never passed over: a reviewer who never learns a tool was missing reads a thinner judgment as a complete one. `jscpd` has no fallback, so absent it means the verbatim duplication layer reports `STATE=unavailable`. Report it; never install it.

7. **LSP capabilities**: pre-check `lsp.enabled` (default `true`; if `false`, report every feature `Disabled`). Probe `documentSymbol`, `hover`, `goToDefinition`, `findReferences`, `goToImplementation` against one representative source file for the detected stack, each bounded by `lsp.timeout` (default 5000 ms); infer `diagnostics` Available when `documentSymbol` succeeds. Procedure and result rules: `references/lsp-capability-probes.md`.

## Output Format

```markdown
### Agents Available
| Agent | Source | Description |
|-------|--------|-------------|

### Skills Available
| Skill | Source | Description |
|-------|--------|-------------|

### Quality Commands
| Command | Purpose | Source |
|---------|---------|--------|

### Tech Stack
- {language} ({indicator file})

### Verification Capabilities
| Capability | Command | Source |
|-----------|---------|--------|

### LSP Capabilities
| Feature | Status | Use Case |
|---------|--------|----------|
| documentSymbol | {Available/Unavailable} | Symbol navigation in files |
| hover | {Available/Unavailable} | Type info and documentation during CODE phase |
| goToDefinition | {Available/Unavailable} | Trace code paths during EXPLORE phase |
| findReferences | {Available/Unavailable} | Impact analysis during EXPLORE, caller verification during REVIEW |
| goToImplementation | {Available/Unavailable} | Interface resolution |
| diagnostics | {Available/Unavailable} | Quality signal during VERIFY phase (errors→P1, warnings→P2) |
```

## Graceful Degradation

No agents → built-in review checklist. No CLAUDE.md commands → detect from tech stack. No tech stack → ask the user for commands. No LSP server → CLI-only analysis (grep/glob for references, CLI tools for diagnostics); not an error.

## Caching

This skill runs in a forked context. The calling command must store the output for use in later phases — do not re-invoke within the same command execution.
