---
name: copilot-cli-subsession
description: >-
  Spawn a new isolated Copilot CLI sub-session from a main Copilot CLI or VS Code session.
  Use when you need to programmatically create, resume, or chain Copilot CLI sessions with
  explicit control over session ID, custom agent, model, BYOK provider profile, permissions,
  and working directory. Triggers: "invoke copilot", "spawn copilot", "copilot sub-session",
  "programmatic copilot cli", "programmatic copilot subprocess", "copilot cli session id", "resume copilot session", "chain copilot sessions", "isolated copilot session",
  "subagent copilot cli", "task copilot cli".
argument-hint: "What is the sub-session prompt?"
metadata:
  author: arisng
  version: 0.6.4
  lastVerified: 2026-08-05
  verifiedCliVersion: 1.0.77
---

# Invoke Copilot CLI Sub-Session

Use this skill when a main session (in Copilot CLI or VS Code) needs to spawn a **fresh, isolated Copilot CLI sub-session** with full control over its identity and runtime.

## When to use

- Run a long or risky sub-workflow in a separate process that does not pollute the main session context.
- Pin a specific **custom agent** to the sub-session.
- Pin a specific **BYOK provider / model** for the sub-session (default: `opencode-go-deepseek-v4-flash`, reasoning-effort `high`; per-model levels are grounded in the `copilot-byok` skill's [`references/shared/reasoning-effort-lookup.md`](../copilot-byok/references/shared/reasoning-effort-lookup.md)).
- Self-generate a **session name** (`--name`) and **session UUID** (`--session-id`) so the main session can send follow-up prompts to the same sub-session.
- Capture structured output (text or JSONL) for programmatic parsing.

## What it produces

- A PowerShell script: `scripts/Invoke-CopilotCliSubSession.ps1`.
- This skill guides the agent to call that script with the correct parameters. The agent should proactively assign a descriptive `-Name` in kebab-case.
- By default the sub-session **inherits** the main session's MCP servers and custom instructions (same working directory, same `~/.copilot/`).

## Quick start

```powershell
# Minimal invocation — uses default BYOK profile (opencode-go-deepseek-v4-flash) at reasoning-effort high
.\scripts\Invoke-CopilotCliSubSession.ps1 `
    -Name "analyze-async" `
    -Prompt "Analyze the project structure and list all async methods."

# Specific agent, model override, named session, multi-line prompt
.\scripts\Invoke-CopilotCliSubSession.ps1 `
    -Name "security-audit" `
    -Agent "security-auditor" `
    -Model "claude-opus-4.5" `
    -SessionId "a1b2c3d4-e5f6-7890-abcd-ef1234567890" `
    -Prompt @"
Review the codebase for security vulnerabilities:
1. Check for SQL injection in data access layer
2. Audit authentication middleware
3. Verify CSRF protection is active
4. Report findings with severity levels
"@

# Invoke a built-in command or skill via slash command
.\scripts\Invoke-CopilotCliSubSession.ps1 `
    -SlashCommand "handoff" `
    -Prompt "Describe the current session state" `
    -Name "session-handoff"

# Invoke a skill without extra prompt
.\scripts\Invoke-CopilotCliSubSession.ps1 `
    -SlashCommand "git-atomic-commit" `
    -Name "auto-commit"

# Invoke with a custom agent
.\scripts\Invoke-CopilotCliSubSession.ps1 `
    -Agent "dotnet-diag:optimizing-dotnet-performance" `
    -Name "perf-analysis" `
    -Prompt "Scan for async anti-patterns"

# Context handoff: list relevant file paths; sub-session reads them itself
.\scripts\Invoke-CopilotCliSubSession.ps1 `
    -Name "exec-plan" `
    -Prompt @"
Execute the implementation plan at:
  c:/Workplace/my-repo/openspec/changes/auth-impl/plan.md
  c:/Workplace/my-repo/openspec/changes/auth-impl/tasks.md

Reference specs:
  c:/Workplace/my-repo/openspec/specs/auth/spec.md

Working directory: c:/Workplace/my-repo
Read each file before executing. Report progress after each step.
"@

# Chain two prompts on the same sub-session by reusing SessionId
$uuid = "b2c3d4e5-f6a7-8901-bcde-f12345678901"
$r1 = .\scripts\Invoke-CopilotCliSubSession.ps1 `
    -Name "research-auth" `
    -SessionId $uuid `
    -Prompt "Research this repo's authentication approach." `
    -JsonOutput

$r2 = .\scripts\Invoke-CopilotCliSubSession.ps1 `
    -Name "research-auth" `
    -SessionId $uuid `
    -Prompt "Based on the research, propose three security improvements." `
    -JsonOutput
```

## Required vs optional parameters

| Parameter | Required | Default | Purpose |
|-----------|----------|---------|---------|
| `-SlashCommand` | No | — | Built-in command or skill name to invoke (e.g., `handoff`, `git-atomic-commit`, `plan`, `review`). Script prepends `/`. When given with `-Prompt`, the prompt becomes the command argument. **At least one of `-SlashCommand` or `-Prompt` is required.** |
| `-Prompt` | No* | — | The task prompt, or argument to `-SlashCommand` when both are given. Supports multi-line (here-strings, `` `n ``, literal newlines). \*Required when `-SlashCommand` is not provided. |
| `-Name` | No | — | Human-readable session name (`--name`). Use kebab-case slugs (e.g. `"analyze-async"`). The agent should proactively generate one. |
| `-SessionId` | No | auto-generated UUID | Custom UUID for `--session-id`. Must be valid UUID format. When omitted, a UUID is auto-generated. Reuse the same value across calls to chain messages on the same session. |
| `-Agent` | No | — | Custom agent name. Qualify plugin agents as `plugin:agent-name` (colon, e.g. `dotnet-diag:optimizing-dotnet-performance`). Repo agents use bare name. |
| `-Model` | No | — | Model override. Takes precedence over the BYOK profile's model. |
| `-ByokProfile` | No | `opencode-go-deepseek-v4-flash` | BYOK profile name from `~/.copilot/byok-profiles.json`. |
| `-ByokAccount` | No | — | Account override for account-grouped profiles (e.g., multiple OpenCode Go subscriptions). Takes precedence over the profile's `account` pin and the config-level `activeAccount`. When omitted, the profile pin or `activeAccount` is used. |
| `-CopilotHome` | No | — | **Staging `COPILOT_HOME`** for the sub-process — the explicit opt-in to full config isolation (CLI 1.0.77+: `--config-dir` was removed; `COPILOT_HOME` is the supported override). The **first time** this path is used, the script seeds a minimal staging tree from production `~/.copilot`: `byok-profiles.json` (required) plus `mcp-config.json` when present. Seeding runs **once only** — afterwards production and staging are fully independent; staging is durable and never re-seeded or auto-cleaned (delete the tree manually to reset). Default: production `~/.copilot` (no isolation). Alias: `-ConfigDir` (deprecated). |
| `-ReasoningEffort` | No | `high` | `none`, `minimal`, `low`, `medium`, `high`, `xhigh`, `max` (per-model subset may vary; `minimal` is newer — verified in CLI 1.0.77). The default BYOK profile (`opencode-go-deepseek-v4-flash`) runs at `high` by default. For the grounded per-model lookup — which levels a model supports and whether to omit the flag — see the `copilot-byok` skill's [`references/shared/reasoning-effort-lookup.md`](../copilot-byok/references/shared/reasoning-effort-lookup.md). |
| `-WorkingDir` | No | current location | Working directory for the sub-process. |
| `-JsonOutput` | Switch | off | Emit JSONL instead of plain text. |
| `-NoAllowAll` | Switch | off | Opt out of `--allow-all --no-ask-user`. By default the sub-session runs with full permissions. |
| `-DisableBuiltInMcps` | Switch | off | Isolate from main session's MCP servers. |
| `-NoCustomInstructions` | Switch | off | Skip project custom instructions. |
| `-TimeoutSeconds` | No | `600` | Kill the sub-process after N seconds. |
| `-Passthrough` | No | — | Extra arguments forwarded to `copilot`. |

## Session naming (`-Name`)

The agent should always assign a meaningful `-Name` in **kebab-case** that describes the sub-session's purpose:

- `"research-csrf-patterns"` — a research task
- `"implement-oauth-middleware"` — an implementation task
- `"review-pr-142"` — a review task

This name appears in `copilot --resume` listings and session logs. It is distinct from `-SessionId` (the UUID used for programmatic chaining). Pass both: `-Name` for human readability, `-SessionId` for script-level chaining.

## Choosing a session ID

- **Auto-generated**: when `-SessionId` is omitted, a valid UUID is auto-generated using `New-Guid`. Every call gets a fresh session unless you reuse the same UUID.
- **Explicit UUID**: pass a valid UUID (`xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx`). Invalid UUIDs trigger a warning and are replaced with an auto-generated one.
- **Follow-up to the same sub-session**: reuse the exact same `-SessionId` value; the prior session state is reloaded via `--session-id`.
- **Valid UUIDs only**: `--session-id` requires standard format (`xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx`).

## Multi-line prompts

`-Prompt` accepts multi-line strings natively. Use PowerShell here-strings for multi-paragraph task descriptions:

```powershell
.\scripts\Invoke-CopilotCliSubSession.ps1 `
    -Name "code-review" `
    -Prompt @"
Review the following PR checklist:
1. Verify all edge cases are covered
2. Check for proper error handling
3. Ensure tests pass with >80% coverage
4. Validate API contract changes
Report findings in a markdown table.
"@
```

Inline newlines via `` `n `` also work: `-Prompt "Line 1`nLine 2`nLine 3"`.

## Slash command invocation (`-SlashCommand`)

`-SlashCommand` wraps Copilot CLI's interactive slash commands for non-interactive use. Pass just the command name (no leading `/`) — the script prepends `/` automatically.

**Supported commands**: Any built-in CLI command (`help`, `init`, `diff`, `pr`, `review`, `plan`, `research`, `delegate`, `rewind`, `compact`, `share`, `allow-all`, `add-dir`, `skills`) and any installed skill (`git-atomic-commit`, `handoff`, `mermaid-creator`, etc.).

> ⚠️ **`model` is excluded from reliable non-interactive use** (verified CLI 1.0.77, 2026-08-03, **BYOK/custom-provider routing**). `-p "/model X"` forwards the text to the *current* model as a prompt — it roleplays the switch and the backend never changes (`model.call_start` stays the same in JSONL).
> ⚠️ **Scope of this finding**: the roleplay behavior was verified with **BYOK** (custom provider, e.g. OpenCode Go). For **GitHub Copilot Subscription** models it is **unverified** — do not assume `-p "/model X"` is roleplay there, since model selection routes through the GitHub platform rather than a custom endpoint. The only verified in-session switch is the interactive TUI `/model` picker (emits `session.model_change`); the only verified programmatic switch is `-Model` / `--model` at process start (e.g. `-Model kimi-k2.7-code`), which switches the real backend.

```powershell
# Slash command only
.\scripts\Invoke-CopilotCliSubSession.ps1 -SlashCommand "plan" -Name "planning-pass"

# Slash command with arguments (Prompt becomes the argument)
.\scripts\Invoke-CopilotCliSubSession.ps1 -SlashCommand "handoff" -Prompt "Describe session results" -Name "handoff-pass"

# Equivalent freeform prompt (also valid)
.\scripts\Invoke-CopilotCliSubSession.ps1 -Prompt "/handoff Describe session results" -Name "handoff-pass"
```

**Multi-step orchestration pattern**:

```powershell
# Plan → Execute → Review with slash commands
.\scripts\Invoke-CopilotCliSubSession.ps1 -SlashCommand "plan" -Prompt "Implement user auth" -Name "plan-auth" -SessionId $uuid
.\scripts\Invoke-CopilotCliSubSession.ps1 -Prompt "Execute the plan above" -Name "exec-auth" -SessionId $uuid
.\scripts\Invoke-CopilotCliSubSession.ps1 -SlashCommand "review" -Name "review-auth" -SessionId $uuid
```
## Custom agent invocation (`-Agent`)

Pin a specific agent to the sub-session. Plugin agents use **colon**: `plugin:agent-name`. Repo agents use bare name.

```powershell
# Plugin agent
.\scripts\Invoke-CopilotCliSubSession.ps1 `
    -Agent "dotnet-diag:optimizing-dotnet-performance" `
    -Prompt "Analyze this project's performance" `
    -Name "perf-analysis"

# Repo agent (discovered from .github/agents/)
.\scripts\Invoke-CopilotCliSubSession.ps1 `
    -Agent "my-custom-agent" `
    -Prompt "Execute the workflow" `
    -Name "custom-workflow"
```

Agent discovery paths (in precedence order):
1. `~/.copilot/agents/` (user-level)
2. `.github/agents/` (repo-level)
3. `plugin:agent-name` (qualified, from installed plugins)

The agent is invoked via the Copilot CLI `--agent` flag and inherits the sub-session's model, BYOK config, and all other parameters.

## Context handoff convention

When delegating to a sub-session, **always prioritize listing the full absolute paths of relevant files** in `-Prompt`. The sub-session can read those files itself using its own tools (`cat`, `grep`, `read`). Only embed content inline when the context is short and simple enough to fit in a single message.

### Why

- The sub-session starts with a blank context — it does not know what files the main session worked with, what decisions were made, or what artifacts exist.
- MCP and custom instructions inheritance provides *environment* (tools, config), not *session memory*.
- Listing file paths is cheaper, avoids duplication, and lets the sub-session choose what to read in depth.

### Do this

```powershell
# PREFERRED — list full paths; sub-session reads files itself
.\scripts\Invoke-CopilotCliSubSession.ps1 `
    -Name "exec" `
    -Prompt @"
Execute the implementation plan at:
  c:/Workplace/my-repo/openspec/changes/auth-impl/plan.md
  c:/Workplace/my-repo/openspec/changes/auth-impl/tasks.md

Reference specs:
  c:/Workplace/my-repo/openspec/specs/auth/spec.md

Start from working directory: c:/Workplace/my-repo
After each step, report progress.
"@

# EXCEPTION — directly embed only when context is short and simple
.\scripts\Invoke-CopilotCliSubSession.ps1 `
    -Name "quick-fix" `
    -Prompt "Fix the typo in src/utils/helpers.ts line 42: change 'teh' to 'the'."
```

### Practical workflow

1. Identify the relevant files from the main session (plan, research, spec, ADR, design doc, task list).
2. List their **full absolute paths** in the `-Prompt` argument, grouped by role.
3. Include the **working directory** and the **final instruction** — what the sub-session should produce.
4. Only embed content inline (via here-string) when the context is trivially short (a few lines).
5. Use the returned `SessionId` to chain follow-up messages if the task requires multiple turns.

### What to reference

| Context type | Files to reference by path |
|--------------|----------------------------|
| Implementation plan | `openspec/changes/*/plan.md`, `openspec/changes/*/tasks.md` |
| Research findings | `openspec/research/*.md`, `docs/design-docs/*.md` |
| Specifications | `openspec/specs/**/spec.md`, `requirements/*.md` |
| Active task checklist | Current todo list, task breakdown |
| Configuration / conventions | `.github/git-scope-constitution.md`, relevant `*.agent.md` |
| **Copilot CLI session state** | `~/.copilot/session-state/<session-uuid>/` (see below) |

### Copilot CLI session-state handoff

When the main session is itself a **Copilot CLI session**, its session state is persisted under `~/.copilot/session-state/<session-uuid>/`. These files capture what the main session already worked on — plans, research, file changes, and checkpoints. Forward them to the sub-session so it does not start from scratch.

| File / Dir | Description |
|------------|-------------|
| `plan.md` | The implementation plan generated by `/plan`. The sub-session should read this to understand what to build and in what order. |
| `research/` | Output from `/research`. Contains search results, analyzed code snippets, and external references the main session already gathered. |
| `files/` | File snapshots or diffs touched during the session. Lets the sub-session see what was changed without re-reading the whole repo. |
| `checkpoints/` | Session checkpoints. Useful for resuming work from a specific point if the sub-session needs to continue where the main session left off. |

**How to discover the session UUID:**

```powershell
# List all session IDs
Get-ChildItem "$HOME\.copilot\session-state" -Directory | Select-Object Name

# Or get the latest session
Get-ChildItem "$HOME\.copilot\session-state" -Directory |
    Sort-Object LastWriteTime -Descending |
    Select-Object -First 1 -ExpandProperty Name
```

**How to reference in `-Prompt`:**

```powershell
# PREFERRED — pass knowledge from previous session
.\scripts\Invoke-CopilotCliSubSession.ps1 `
    -Name "continue-from-session" `
    -Prompt @"
Continue the work from the previous Copilot CLI session.

Session state is at:
  ~/.copilot/session-state/a1b2c3d4-e5f6-7890-abcd-ef1234567890/

Review these files before executing:
  ~/.copilot/session-state/a1b2c3d4-e5f6-7890-abcd-ef1234567890/plan.md
  ~/.copilot/session-state/a1b2c3d4-e5f6-7890-abcd-ef1234567890/research/
  ~/.copilot/session-state/a1b2c3d4-e5f6-7890-abcd-ef1234567890/files/

Working directory: c:/Workplace/my-repo
Continue from where the plan left off.
"@
```

**Note**: The session-state directory is tied to the **main** session's UUID. The sub-session gets its own separate session-state (under its own `--session-id`). Forwarding the main session's state paths is what bridges the gap.

### Path formatting

- Use **absolute paths** (`c:/Workplace/my-repo/...`) so the sub-session can read them regardless of its working directory.
- If the sub-session's `-WorkingDir` matches the repo root, relative paths rooted there also work.
- Group paths by purpose with a short header line before each group.

## MCP and custom instructions inheritance

By default the sub-session **inherits** the main session's MCP servers and custom instructions because:

- It runs in the same working directory (project-level `.mcp.json`, `.github/mcp.json`, `copilot-instructions.md` are picked up).
- It uses the same `~/.copilot/` directory (user-level `mcp-config.json`, agents, skills).

To isolate the sub-session, pass `-DisableBuiltInMcps` and/or `-NoCustomInstructions`. To fully isolate, set `-CopilotHome` (mapped to `$env:COPILOT_HOME` for the sub-process) to a separate config tree.

### Staging `COPILOT_HOME` — the skill's testing sandbox (dojo)

`-CopilotHome <path>` is the explicit opt-in to a **staging `COPILOT_HOME`** — a durable, separate config tree that keeps test sub-sessions from polluting the production `~/.copilot/`. The recommended convention is a sibling directory, e.g. `Join-Path $HOME '.copilot-dojo'` (derived from `$HOME`, so it works on any machine — never hardcode a user path).

**Why a staging env (dojo vision)**: staging is the designated testing environment for this skill and its ecosystem. Any sub-session spawned with `-CopilotHome` runs fully inside staging — session state, checkpoints, logs, BYOK profile, and MCP config all land there — so you can exercise every supported feature of this skill (custom agents, slash commands, model pinning/switching, session chaining, BYOK profiles, MCP/custom-instructions isolation, reasoning-effort handling) without touching production. Because env vars are process-scoped, the main (root) session keeps running in production `~/.copilot/` while the child works in staging (verified: parent env is never modified).

**Tight feedback loop** (develop the skill safely):

1. **Edit** the artifact under test — e.g. `scripts/Invoke-CopilotCliSubSession.ps1`, this `SKILL.md`, or a referenced skill/agent.
2. **Stage it** — repo-level skills/agents/hooks are picked up from the working directory (`.github/skills/`, `.github/agents/`, `.github/hooks/`) with **no extra step** (discovery is workspace-relative, independent of `COPILOT_HOME`). Personal-level artifacts can be staged with the publish scripts' `-CopilotHome` override:
   ```powershell
   # Agents → <CopilotHome>/agents (skips WSL mirroring)
   pwsh -NoProfile -File scripts/publish/publish-agents.ps1 -CopilotHome "$HOME\.copilot-dojo" -Force

   # Instructions → <CopilotHome>\Code\{Stable|Insiders}\User\prompts (skips WSL)
   pwsh -NoProfile -File scripts/publish/publish-instructions.ps1 -CopilotHome "$HOME\.copilot-dojo" -Force

   # User-level hooks → <CopilotHome>/hooks (skips WSL + VS Code settings mutation)
   pwsh -NoProfile -File scripts/publish/publish-hooks.ps1 -Scope user-level -CopilotHome "$HOME\.copilot-dojo" -Force

   # Or direct copy for anything else
   Copy-Item -Recurse "$PWD\skills\copilot-cli-subsession" "$HOME\.copilot-dojo\skills\"
   ```
3. **Spawn** a sub-session in staging:
   ```powershell
   .\scripts\Invoke-CopilotCliSubSession.ps1 -CopilotHome "$HOME\.copilot-dojo" -Prompt "test the change"
   ```
4. **Observe** — the returned object's `CopilotHome` confirms the child used staging; session artifacts live under `$HOME\.copilot-dojo\session-state\<session-uuid>\`.
5. **Iterate** — repeat 1–4. Staging is never re-seeded and never auto-cleaned, so state persists across iterations; delete the tree to reset.

**Seeding & independence**:

- **One-time seeding**: the first time the staging path is used (its `byok-profiles.json` is missing), the script seeds a minimal functional tree from production — `byok-profiles.json` (required) plus `mcp-config.json` when present. This makes an empty staging dir immediately usable.
- **Independent envs**: after seeding, production and staging are fully independent. The staging tree is **never re-seeded** (existing files are never overwritten) and **never auto-cleaned** — the user owns its lifecycle. Delete the tree to reset.
- **What's available in staging**: always the seeded `byok-profiles.json` + `mcp-config.json`, plus repo-level agents/skills/hooks from the working directory; personal-level agents/skills/hooks and `moonshot-proxy` only if staged in (publish scripts accept `-CopilotHome`, or copy manually).
- **Profile resolution**: with `-CopilotHome`, the BYOK profile is resolved from the staging tree (seeded copy). Production's `byok-profiles.json` is the seed source, not a live fallback — the staged copy is authoritative.
- **Chaining in staging**: to resume a staging sub-session, pass the **same** `-CopilotHome` plus the same `-SessionId` — session state lives under staging, not production.

## BYOK profile handling

The script looks up the profile in `~/.copilot/byok-profiles.json` (production) or, when `-CopilotHome` is given, the seeded staging tree (`$env:COPILOT_HOME/byok-profiles.json`). The **default profile** is `opencode-go-deepseek-v4-flash`.

It maps profile fields to environment variables:

```text
COPILOT_PROVIDER_BASE_URL
COPILOT_PROVIDER_TYPE
COPILOT_MODEL
COPILOT_PROVIDER_API_KEY
COPILOT_PROVIDER_WIRE_API
COPILOT_PROVIDER_MAX_PROMPT_TOKENS
COPILOT_PROVIDER_MAX_OUTPUT_TOKENS
COPILOT_OFFLINE
```

If the profile contains `proxyPort`, the script routes the request through the local Moonshot proxy (`https://moonshot.local/v1`) used by `copilot-byok`.

A `-Model` parameter, when provided, takes precedence over the profile's model.

### Switching models within a sub-session

Verified CLI 1.0.77 (2026-08-03): `-p "/model X"` does **not** switch the backend model (the current model roleplays the switch) — **verified under BYOK/custom-provider routing only**. ⚠️ Do not generalize to **GitHub Copilot Subscription** models: there the CLI selects models via the GitHub platform (not a custom endpoint), and `-p "/model X"` behavior is **unverified** — treat it as unreliable and prefer the interactive TUI `/model` picker, which is the verified in-session switch (it emits `session.model_change` and subsequent calls route to the new model). The verified programmatic switch is `-Model` / `--model` at process start. For OpenCode Go, all models (DeepSeek, GLM, Kimi, MiMo, Qwen3.x, MiniMax, GPT-5.6 Luna) are served through the single OpenAI `chat/completions` endpoint — the `anthropic` type and Responses-only constraints documented earlier were falsified by probe (see `copilot-byok` `references/provider/opencode-go/cli.md` and `references/shared/environment-variables.md`).

### Reasoning effort per model

The script forwards `--reasoning-effort` (default `high`) only when the resolved profile supports it. If the profile carries `"reasoningEffortSupported": false` (models whose API exposes no controllable levels — e.g., Kimi K2.x, GLM, MiMo, Qwen3.x, MiniMax), the argument is stripped with a warning, mirroring `byok-profile.ps1 run`. The authoritative per-model lookup — which levels a model supports and the recommended default — is the `copilot-byok` skill's `references/shared/reasoning-effort-lookup.md`. For the default profile (`deepseek-v4-flash`), `high` is within the supported `low`/`medium`/`high` range.

## Copilot SDK parity & keeping up

The CLI flag surface, `COPILOT_*` env vars, the .NET SDK (`copilot-sdk-dotnet`), and VS Code `chatLanguageModels.json` are four façades over the same Copilot CLI engine. The single source of truth for how they map is the [capability parity matrix](references/copilot-sdk-parity-matrix.md) — update it whenever a new capability appears in any surface, and link it from new reference material instead of re-documenting equivalence.

To detect drift between this skill's documented surface and the installed CLI, run the parity gate before publishing:

```powershell
.\scripts\Test-CopilotCliParity.ps1
```

The gate compares documented flags, env vars, and reasoning-effort levels against `copilot --help` / `copilot help environment`, exits non-zero on drift, and lists new capabilities the CLI gained that the skill does not document yet. After re-verifying, bump `lastVerified` / `verifiedCliVersion` in this skill's frontmatter and the `Verified` column of the matrix.

Historical (v1.0.77, resolved 2026-08-03): `--config-dir` is no longer listed in CLI help; `-CopilotHome` maps to `COPILOT_HOME` for the sub-process (the supported config-override mechanism). The parameter was originally named `-ConfigDir` (deprecated alias retained).

## Output

By default the script returns a plain-text block. With `-JsonOutput` it returns JSONL; the final `result` line contains `exitCode` and `usage`.

The script prints a structured result object (metadata only — StdOut is written to the console directly):

```powershell
[PSCustomObject]@{
    ExitCode      = $proc.ExitCode
    SlashCommand  = $SlashCommand
    Name          = $Name
    SessionId     = $SessionId
    Agent         = $Agent
    Model         = $env:COPILOT_MODEL
    ByokProfile   = $ByokProfile
}
```

## Safety rules

- Always assign a descriptive `-Name` in kebab-case.
- `-NoAllowAll` lets you opt out of the default `--allow-all --no-ask-user` for read-only or untrusted contexts.
- The sub-session inherits MCP and custom instructions by default; use `-DisableBuiltInMcps` or `-NoCustomInstructions` only when isolation is intended.
- The sub-process inherits the main session's environment except where the script overrides it.

## Tests (empirical argument audit)

Terminology used here (shim, live mode, KNOWN-GAP, polarity-agnostic, case-ID buckets, dojo, COST
GUARDRAIL) is defined in the [harness vocabulary glossary](references/glossary.md) — self-contained
within this skill, so it travels with the skill when published.

`tests/Invoke-CopilotCliSubSession-args-audit.ps1` is an empirical audit harness that executes the real
script against the seeded staging home (`~/.copilot-dojo`, the "dojo") and asserts, for every supported
argument: the exact CLI argv forwarded to the copilot child (via a shim), the `COPILOT_*` env emitted, the
9-field return object, and seeding/validation/precedence behaviors. It includes an opt-in live pass
(`-Live`, cheap models only, COST GUARDRAIL enforced) that probes real sub-sessions: session-state
`events.jsonl`, `model.call_start`, slash command, custom agent, SessionId chaining, and same/different-family
model hot-switching and cold-switch resume (`l8`: luna→flash across an exit+resume).

```powershell
# Shim matrix (zero cost, deterministic)
pwsh -NoProfile -File skills/copilot-cli-subsession/tests/Invoke-CopilotCliSubSession-args-audit.ps1
# Shim matrix + live probes (real keys; needs OPENCODE_API_KEY_WORK in this process)
pwsh -NoProfile -File skills/copilot-cli-subsession/tests/Invoke-CopilotCliSubSession-args-audit.ps1 -Live
# Dispatcher equivalents
pwsh -NoProfile -File scripts/workspace/run-command.ps1 -Command tests:subsession-audit
pwsh -NoProfile -File scripts/workspace/run-command.ps1 -Command tests:subsession-audit-live
```

Exit codes: `0` all passed, `1` any failed, `2` harness/preflight error. Known-gap locks (s4-3, s5-4, s9-4,
s11-2, l2, ...) report as PASS with a gap label so the harness stays green while documenting behavior.
Reports land in `scripts/test/.artifacts/copilot-cli-subsession-args-audit/run-<ts>-<pid>/report.md`.
Evolve cases in `tests/` and re-run on demand; the fixture (`tests/fixtures/byok-profiles.fixture.json`)
drives throwaway-home cases so production and the dojo are never mutated (verified by isolation gates).

## References

- [Programmatic Copilot CLI cheatsheet](./references/copilot-cli-programmatic-cheatsheet.md)
- [BYOK configuration](../copilot-byok/SKILL.md)
