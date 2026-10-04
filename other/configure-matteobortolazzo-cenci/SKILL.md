---
name: configure
description: "Configure cenci's neutral project core and generate Claude/Codex adapters."
compatibility: Requires Claude Code settings, plugin environment variables, and AskUserQuestion.
argument-hint: [additional context]
user-invocable: true
disable-model-invocation: true
allowed-tools: Read, Write, Edit, Glob, Grep, AskUserQuestion, Bash(bash "${CLAUDE_PLUGIN_ROOT}/skills/configure/scripts/detect-project.sh"), Bash(bash "${CLAUDE_PLUGIN_ROOT}/skills/configure/scripts/merge-sandbox-config.sh":*), Bash(bash "${CLAUDE_PLUGIN_ROOT}/scripts/migrate-project-core.sh":*), Bash(pen interactive --help:*), Bash(test:*), Bash(which:*), Bash(jq:*), Bash(mv ~/.claude/settings.json.tmp ~/.claude/settings.json), Bash(mkdir -p:*), Bash(rm -f .claude/hooks/check-pending-plans.sh), Bash(rmdir .claude/hooks:*), Bash(gh auth status:*), Bash(gh label list:*), Bash(gh label create:*), Bash(gh pr create:*), Bash(gh pr view:*), Bash(git rev-parse:*), Bash(git add:*), Bash(git commit:*), Bash(git worktree add:*), Bash(git -C:*), Bash(git diff --no-index:*), Bash(rm -f ${TMPDIR:-/tmp}/cenci/cenci-configure-:*), Bash(cenci dispatch status:*), Bash(cenci dispatch enroll:*)
---

> **Client dispatch**: In Codex, read `codex-runtime` and `configure/codex.md`, execute that native procedure, and do not continue into the Claude procedure below.

> **Interaction rule**: Every question, confirmation, or approval directed at the user — anywhere in this skill, including error recovery — MUST be asked with the `AskUserQuestion` tool. Never ask in plain text. If an instruction says "ask the user" or "confirm", that means `AskUserQuestion`.

## Task

Help the user set up this project for the cenci plugin.

### Parse `$ARGUMENTS`

All of `$ARGUMENTS` is optional **user context** (additional instructions or focus areas).
If empty, proceed normally with defaults.

### Existing Config Detection

Resolve project configuration in this order:

1. `.cenci/config.json` is canonical. If present, read it as `existingConfig`.
2. Otherwise read `.claude/config.json` as `legacyConfig`. Treat this as a migration run.
3. If neither exists, set `existingConfig` to null.

On migration, preserve every unknown key from `legacyConfig`; new writes go only to
`.cenci/config.json`. If both files exist, recursively merge them into one
`migrationBase` with canonical values winning, then overlay managed answers. Use
`"${CLAUDE_PLUGIN_ROOT}/scripts/migrate-project-core.sh" <root>` to preview the exact
config/guidance diff:
```bash
bash "${CLAUDE_PLUGIN_ROOT}/scripts/migrate-project-core.sh" <root> [--apply]
```
Rerun it with `--apply` only after approval, with `<root>` set to `<worktree-path>` (see
Create Worktree below — the worktree exists by the time any `--apply` can run). Never
rewrite or delete `.claude/config.json`; it is a read-only compatibility artifact.

When `existingConfig` is present, tell the user before starting questions:
"Found existing configuration. Each question will show your current setting as the default — select it to keep it unchanged."

Reconfiguration runs are how a project picks up configure features added since its config was written. The plugin's SessionStart hook (`hooks/scripts/check-config-staleness.sh`) compares `existingConfig.configVersion` against the installed flow plugin version and nudges the user to re-run this skill when the config is stale or unstamped; completing this run refreshes the stamp (step 6) and clears the nudge.

### Create Worktree

`/cenci:configure` writes files into the repo (`.cenci/config.json`, `AGENTS.md`/`CLAUDE.md`, `.mcp.json`, `.lsp.json`, `.gitignore`, `.claudeignore`, `.github/workflows/ci.yml`, `.cenci/Dockerfile`, `.lazyboards.yml`, `.codex/agents/`) and updates `.claude/settings.json`. Like every other change in this repo, these ship as a PR — configure never writes directly to the main worktree (see `cenci:worktrees` and `docs/git-workflow.md`).

Create the worktree now, before any file is written (including a migration `--apply` above) and before the detection/question steps below, since none of them depend on it existing yet:

1. Verify at least one commit exists: `git rev-parse HEAD 2>/dev/null`. If the repository has no commits, create an initial commit as two standalone Bash calls (never compound `&&` — shell-rules: every segment of a compound is evaluated independently by the approval system): `git add -A`, then `git commit -m "chore: initial commit" --allow-empty`.
2. Derive a slug: `init` when `existingConfig` is null (first-ever configure run), `update` for a plain reconfiguration, or a short kebab-case description of the user's focus when `$ARGUMENTS` names one (e.g. "refresh MCP servers" → `mcp-refresh`).
3. Create the worktree: `git worktree add .worktrees/configure-<slug> -b chore/configure-<slug> main`. If that branch/directory name is already taken by an unrelated prior run, append `-2`, `-3`, etc. until it's free.

From this point on, `<worktree-path>` is `.worktrees/configure-<slug>`. Every file this skill reads or writes below — `.cenci/config.json`, `AGENTS.md`, `CLAUDE.md`, `.mcp.json`, `.lsp.json`, `.gitignore`, `.claudeignore`, `.claude/settings.json`, `.github/workflows/`, `.cenci/Dockerfile`, `.lazyboards.yml`, `.codex/` — and every "the repo root" / "the project root" reference in the steps below resolves against `<worktree-path>`, never the main checkout. Use absolute paths rooted at `<worktree-path>` for every Write/Edit; verify the CWD before Bash commands rather than relying on a single `cd` persisting across calls. `gh label create` / `gh issue` calls (step 3c) are GitHub API calls, not file writes, and run the same regardless of worktree.

### Scripted Detection

The deterministic detections this skill needs (platform, container, package manager, MCP/LSP/dind/Playwright catalog triggers, plugin version) are scripted, not re-derived ad hoc. Run the bundled detector once, as its **own** Bash call (per `cenci:shell-rules`), from the repository root of the main checkout — it only reads, nothing is written:

```bash
bash "${CLAUDE_PLUGIN_ROOT}/skills/configure/scripts/detect-project.sh"
```

(the detector is `scripts/detect-project.sh` inside this skill; its tests live next to it). Parse its stdout as a JSON object and keep it as `detection` for the rest of this run:

- `detection.pluginVersion` — installed flow plugin version; stamped into config as `configVersion` (step 6)
- `detection.platform` — `{name, owner, repo}` parsed from the git remote, or `null`
- `detection.inContainer` — cenci-sandbox container detection result
- `detection.packageManager` — `pnpm` / `yarn` / `npm` from lockfiles, or `null`
- `detection.mcpServers` — MCP catalog triggers found in the dependency scan (e.g. `angular`, `primeng`)
- `detection.lspServers` — LSP catalog triggers found (e.g. `typescript`, `gopls`)
- `detection.dindDetected` — Testcontainers/Docker-SDK trigger found (question 9b default)
- `detection.playwrightTest` — `@playwright/test` in root `devDependencies`
- `detection.warnings` — non-fatal detection notes; relay them to the user as informational messages

If the script exits non-zero or its output is not valid JSON, fall back to the **manual fallback** procedure kept in each consuming section below — a detection either comes from `detection` or from its manual fallback, never silently skipped. The script only detects: every question, catalog decision, and user choice stays in this skill.

### Platform Detection

Use `detection.platform`: when non-null it carries the platform name plus extracted owner/repo; when `null`, fall back to manual questions.

**Manual fallback** (only if Scripted Detection failed): run `git remote get-url origin 2>/dev/null` and parse the result:

| Remote URL pattern | Platform | Extracted values |
|---|---|---|
| `git@github.com:OWNER/REPO.git` | github | owner, repo |
| `https://github.com/OWNER/REPO.git` | github | owner, repo |
| Unrecognized / no remote | — | Fall back to manual questions |

Strip trailing `.git` suffix from repo names.

If user context was provided, use it to steer the configuration (e.g., skip certain questions, pre-select options, focus on specific areas).

### Container Detection

cenci runs inside `sandbox`'s cenci-sandbox container with `--dangerously-skip-permissions`. The **container is the security boundary** — there is no host profile. Claude Code's own host sandbox stays disabled, and `permissions.allow`/`deny` are kept only as defense-in-depth for plain `claude` runs inside the container (e.g. `cenci open --shell`).

Use `detection.inContainer` (the detector checks `CENCI_SANDBOX`, then `/.dockerenv`).

**Manual fallback** (only if Scripted Detection failed) — detect the container (stop at the first match; run each check as its **own** Bash call, per `cenci:shell-rules` — never compound them):

1. **`CENCI_SANDBOX` env var** (works for both Docker and Podman): run `test "${CENCI_SANDBOX:-}" = "1"` as its own Bash call. Exit 0 → in container.
2. **Docker fallback**: run `test -f /.dockerenv` as its own Bash call. Exit 0 → in container.

This detection is a **non-blocking advisory** — it never gates configuration and never uses `AskUserQuestion`:

- **In container**: emit an informational message: "Detected the cenci-sandbox container — the container is the security boundary. Claude Code's host sandbox stays disabled." Then continue normally.
- **Not in container**: emit an advisory and continue anyway: "cenci is designed to run inside the cenci-sandbox container (the security boundary). You appear to be running on the host — continuing, but running outside the container is unsupported." Proceed with the same container-shaped output.

**Default values from existing config**: When `existingConfig` is not null, each question below MUST present the existing value as the pre-selected default (list it first, marked "(current)"). The user can accept with one click or change it. New fields not in `existingConfig` (e.g., `lspServers` when upgrading from a pre-LSP config) have no default and are asked normally.

**`AskUserQuestion` cannot pre-check `multiSelect` options** — its options only carry `label`/`description`/`preview`, no "selected by default" field. So for the two multi-select questions (5. MCP Servers, 6. LSP Servers), "pre-select" cannot mean a pre-ticked checkbox — re-asking the full multi-select on every reconfigure would force re-clicking every already-enabled server one at a time. Instead, gate behind a single Keep/Change confirmation first (see *Keep-or-change gate* under each question below): when `existingConfig` already has a value for that field, ask one Yes/No question summarizing the current selections; only "No — let me change them" drops into the full multi-select. This is a single click to keep everything unchanged, instead of one click per server.

| Question | `existingConfig` field | Default when field exists |
|---|---|---|
| 1. Tech stack | `stack` | Pre-fill with formatted stack |
| 2. Project structure | `isMonorepo` | Pre-select based on existing value |
| 3. Branching strategy | `branchPattern` | Pre-fill with existing pattern |
| 5. MCP Servers | `mcpServers` | Keep-or-change gate (see below); only "change" enters the multi-select, pre-sorted with enabled servers first |
| 6. LSP Servers | `lspServers` | Keep-or-change gate (see below); only "change" enters the multi-select, pre-sorted with enabled servers first |
| 7. Auto-compact | `autoCompactDisabled` | Pre-select Yes/No |
| 7b. Pin subagents to 200K | `pinSubagents200K` | Pre-select Yes/No |
| 8. CI/CD pipeline | `cicd` | Pre-select Yes/No based on `cicd.enabled` |
| 9. Sandbox Dockerfile | `sandbox` | Pre-select Yes/No based on `sandbox.enabled` |
| 9b. Nested Docker (dind) | `sandbox` | Pre-select Yes/No based on `existingConfig.sandbox.dind` (else Yes when a Testcontainers/Docker-SDK trigger was detected, No otherwise) |
| 9c. Azure CLI | `sandbox` | Pre-select Yes/No based on `existingConfig.sandbox.azure`; if field absent, ask normally |
| 10. Board config (lazyboards) | `lazyboards` | Only asked when no `.lazyboards.yml` exists; if one exists, suggest missing actions or skip (see *Board Config*) |

Ask these questions one at a time using the `AskUserQuestion` tool:

1. **Tech stack**: "What's your tech stack?" (capture for stack pack selection)
   - Backend framework + version
   - Frontend framework + version
   - Test frameworks
   - Any other key technologies

2. **Project structure**: "Is this a monorepo or single project?"

**If monorepo**, continue with Steps 2a and 2b below. Otherwise skip to question 3.

#### Step 2a — Auto-detect projects

Scan the repo for project directories using these strategies (try all, deduplicate):

1. **Node workspaces**: Read `package.json` `workspaces` field and `pnpm-workspace.yaml` `packages` field
2. **Lerna**: Read `lerna.json` `packages` field
3. **.NET solutions**: Find `*.sln` files and parse `Project(...)` references for `.csproj` paths
4. **Convention directories**: Scan `packages/*/`, `apps/*/`, `projects/*/`, `src/*/` for directories containing `package.json` or `*.csproj`

For each discovered project, detect:
- **Path**: relative directory (e.g., `packages/api`)
- **Stack**: auto-detect from dependencies:
  - `@angular/core` in `package.json` → Angular
  - `react` in `package.json` → React
  - `next` in `package.json` → Next.js
  - `vue` in `package.json` → Vue
  - `.csproj` with `Microsoft.NET.Sdk.Web` → .NET API
  - `.csproj` with `Microsoft.NET.Sdk` → .NET library
  - Fallback: read `package.json` `name` or directory name
- **Build command**: auto-detect (`dotnet build` for .NET, `npm run build` for Node, etc.)
- **Test command**: auto-detect (`dotnet test` for .NET, `npm test` for Node, etc.)
- **Lint command**: derive from the Stack-to-CI mapping table's Lint column (see the table under question 8 below); omit `lintCommand` entirely when the detected stack has no Lint row (e.g. `markdown-shell`, `docker-shell`)

Present discovered projects for confirmation using AskUserQuestion:
"Found these projects in the monorepo:
1. `<path>` — <detected-stack>
2. `<path>` — <detected-stack>
...
Are these correct? (You can add or remove projects)"

#### Step 2b — Per-project details

For each confirmed project, ask for a **one-line description** using AskUserQuestion:
"Provide a short description for each project:"
- `<path>` (<stack>): ___

Generate a slug for each project from its directory name (e.g., `packages/api` → `api`, `apps/web-client` → `web-client`).

3. **Branching strategy**: "What's your branch naming convention?"
   - Default suggestion: `feature/<id>-<description>`

(There is no question 4 — sandboxing is not asked. The cenci-sandbox container is the security boundary and Claude Code's host sandbox is always disabled; numbering of the remaining questions is kept for stability.)

### Dependency Detection

The dependency scan is scripted: `detection.mcpServers` carries the MCP catalog triggers found, and `detection.dindDetected` is the `dindDetected` value question 9b uses below.

**Manual fallback** (only if Scripted Detection failed) — scan the project for framework dependencies:

1. If `package.json` exists in the repo root, read `dependencies` and `devDependencies`
2. If `.csproj` files exist, read `PackageReference` entries
3. Store the detected package names for matching against the MCP catalog below
4. **Testcontainers/Docker-SDK detection** (for question 9b below — nested Docker/dind): scan for these triggers and store the result as `dindDetected` (`true` if any match, `false` otherwise):
   - npm: `testcontainers`, `@testcontainers/*`, or `dockerode` in `dependencies`/`devDependencies`
   - NuGet: `Testcontainers*` or `Docker.DotNet` in `.csproj` `PackageReference` entries
   - Python: `testcontainers` in the dependency list (`requirements.txt`, `pyproject.toml`) — dep list only, no source scan
   - Go: `github.com/testcontainers/testcontainers-go` in `go.mod`

### MCP Server Catalog

| Trigger Package | Server Name | Command | Args | Env Vars | Scope |
|---|---|---|---|---|---|
| *(always available)* | context7 | `npx` | `["-y", "@upstash/context7-mcp@3.2.5"]` | `CONTEXT7_API_KEY` | project |
| `@angular/core` | angular | `npx` | `["-y", "@angular/cli", "mcp"]` | — | project |
| `primeng` | primeng | `npx` | `["-y", "@primeng/mcp"]` | — | project |

**Scope:**
- **project**: Add to the project's root `.mcp.json`.

### LSP Server Catalog

| Trigger | Server Name | Command | Args | Extension Map | Install Command |
|---|---|---|---|---|---|
| `typescript` or `@angular/core` or `react` or `next` or `vue` in package.json | typescript | `typescript-language-server` | `["--stdio"]` | `{".ts": "typescript", ".tsx": "typescriptreact", ".js": "javascript", ".jsx": "javascriptreact"}` | `npm install -g typescript-language-server typescript` |
| `*.py` files or `pyproject.toml` or `requirements.txt` | pyright | `pyright-langserver` | `["--stdio"]` | `{".py": "python"}` | `pip install pyright` or `npm install -g pyright` |
| `Cargo.toml` present | rust-analyzer | `rust-analyzer` | `[]` | `{".rs": "rust"}` | See rust-analyzer docs |
| `*.csproj` present | csharp-ls | `csharp-ls` | `[]` | `{".cs": "csharp"}` | `dotnet tool install --global csharp-ls` |
| `go.mod` present | gopls | `gopls` | `["serve"]` | `{".go": "go"}` | `go install golang.org/x/tools/gopls@latest` |

5. **MCP Servers**: Match detected dependencies against the MCP catalog above. Build a suggestion list:
   - Always include **Context7** (general-purpose docs lookup)
   - Add each MCP whose trigger package was found in the dependency scan

   **Keep-or-change gate**: if `existingConfig.mcpServers` is present, do not jump straight into the multi-select — `AskUserQuestion` can't pre-check boxes, so re-asking it fresh would force re-clicking every already-enabled server. Instead present the current state and ask a plain Yes/No:

   "Current MCP servers: `<name>` ✓ enabled, `<name>` ✗ disabled, … . Keep these settings?"
   Options: "Yes — keep current settings (Recommended)", "No — let me change them"

   - **Yes**: carry `existingConfig.mcpServers` forward unchanged, skip the multi-select below entirely.
   - **No**: continue to the multi-select below.

   If `existingConfig.mcpServers` is absent (first-ever configure run, or a newly-detected MCP not previously offered), skip the gate and ask the multi-select directly.

   Present using AskUserQuestion with multiSelect=true (sort currently-enabled servers first when `existingConfig.mcpServers` exists, so they're easiest to re-tick):

   "Based on your project dependencies, these MCP servers can enhance AI assistance.
    Which would you like to enable?"

   Options (only show those whose trigger was detected, plus Context7 always):
   - "Context7 — Live documentation lookup for any library (requires free API key from context7.com/dashboard)"
   - "Angular — Official Angular AI tutor, best practices, and documentation search"
   - "PrimeNG — Component documentation, props, events, theming, and examples"

   If only Context7 is available (no framework-specific MCPs detected), still present it:
   "Do you want to enable Context7 for live documentation lookup?
    (Requires a free API key from context7.com/dashboard)"

### UI Conventions

**Condition**: Only ask question 5c when a frontend framework is detected in the stack from
question 1. Frontend frameworks include: Angular, React, Next.js, Vue, Svelte, or any UI
framework.

If no frontend framework is detected, skip this section entirely.

5c. **UI conventions**: The answers here become guidance prose in the generated `AGENTS.md`
   `## UI Conventions` section — they are **not** written to `.cenci/config.json`. There is no
   config key for this.

   Ask using AskUserQuestion:

   "Your project includes `<detected-frontend-framework>`. Where does its shared component
    library live? (Path relative to the repo root — leave blank if there isn't one yet.)"

   Options: offer any directory the repository scan suggests — for example a `components/`,
   `ui/`, or `design-system/` directory, or a workspace library under `libs/` or `packages/` —
   plus "None yet".

   Then ask:

   "Is there a component catalog app — Storybook, an Angular component workshop, or a similar
    browsable gallery — and how is it run?"

   Options: offer the detected candidates — a `storybook` or `ng serve <app>` script in
   `package.json`, an `.storybook/` directory, or a dedicated showcase project in the
   `projects` array — plus "None".

   **Writing the answers**: fill the `## UI Conventions` block in the generated `AGENTS.md`
   (from `templates/agents-md-project.md` for a monorepo project, or
   `templates/agents-md-root.md` / `templates/agents-md-root-monorepo.md` for the root):
   - `<path-to-component-library>` becomes the library path; drop the bullet when "None yet".
   - `<storybook-like-app-path>` and `<catalog-command>` become the catalog's path and its run
     command; drop the bullet when "None".
   - `<project-specific UI rules populated during configure>` stays as a placeholder for the
     user to fill in later, or is removed when no conventions are known yet.

   Keep the reuse-before-authoring bullet verbatim in every case — it is the rule the planner
   and implementer look for, and it holds whether or not a library exists yet.

   In a monorepo, ask per frontend project when the projects have different libraries; ask
   once and write the shared answer into the root `AGENTS.md` when they share one.

### Playwright CLI Setup

**Condition**: Only ask this when a frontend framework is detected in the stack from question 1 AND `detection.playwrightTest` is `true` (manual fallback: `@playwright/test` found in root `devDependencies`).

If both conditions are met, present using AskUserQuestion:

   "Your project uses Playwright Test. Do you want to set up Playwright CLI (`@playwright/cli`) for interactive browser automation during development?
    (Screenshots, snapshots, form filling, network inspection — more token-efficient than Chrome MCP for agents.)"

   Options: "Yes — install and configure Playwright CLI", "No — skip"

   **If Yes**:
   1. Check if `playwright-cli` is already installed: `which playwright-cli 2>/dev/null`
      - **Found** → "✓ `playwright-cli` found at `<path>`"
      - **Not found** → "Run `npm i -g @playwright/cli` to install, then `playwright-cli install --skills` to set up agent skills."
   2. Set `playwrightCli: true` in `.cenci/config.json`

   **If No**: Set `playwrightCli: false` in `.cenci/config.json` (or omit the field)

If the conditions are not met, skip this section entirely (do not set `playwrightCli` in config).

### LSP Detection

`detection.lspServers` carries the detected LSP catalog triggers directly.

**Manual fallback** (only if Scripted Detection failed) — reuse the dependency detection results from earlier and add file-type detection to match against the LSP Server Catalog:

- `typescript`, `@angular/core`, `react`, `next`, or `vue` in `package.json` dependencies → **typescript**
- `*.py` files present, or `pyproject.toml`, or `requirements.txt` → **pyright**
- `Cargo.toml` present → **rust-analyzer**
- `*.csproj` present → **csharp-ls**
- `go.mod` present → **gopls**

If no LSP servers are detected, skip question 6 entirely.

6. **LSP Servers**: If **two or more** LSP servers were detected above:

   **Keep-or-change gate**: if `existingConfig.lspServers` is present, do not jump straight into the multi-select — `AskUserQuestion` can't pre-check boxes, so re-asking it fresh would force re-clicking every already-enabled server. Instead present the current state and ask a plain Yes/No:

   "Current LSP servers: `<name>` ✓ enabled, `<name>` ✗ disabled, … . Keep these settings?"
   Options: "Yes — keep current settings (Recommended)", "No — let me change them"

   - **Yes**: carry `existingConfig.lspServers` forward unchanged, skip the multi-select below entirely.
   - **No**: continue to the multi-select below.

   If `existingConfig.lspServers` is absent (first-ever configure run, or a newly-detected LSP server not previously offered), skip the gate and ask the multi-select directly.

   Present using AskUserQuestion with multiSelect=true (sort currently-enabled servers first when `existingConfig.lspServers` exists, so they're easiest to re-tick):

   "LSP servers provide real-time diagnostics (type errors, unused variables, dead code) during implementation. Based on your project, which would you like to enable?"

   Options (only show those whose trigger was detected):
   - "typescript — TypeScript/JavaScript type checking and diagnostics"
   - "pyright — Python type checking and diagnostics"
   - "rust-analyzer — Rust type checking and diagnostics"
   - "csharp-ls — C# type checking and diagnostics"
   - "gopls — Go type checking and diagnostics"

   If exactly **one** LSP server was detected, ask a plain Yes/No instead — a multi-select checkbox with a single option has no sensible "none" choice:

   "Your project uses `<detected-language>`. Do you want to enable `<server-name>` for real-time diagnostics (type errors, unused variables, dead code) during implementation?"

   Options: "Yes — enable `<server-name>`", "No — skip"

#### Binary Verification

For each LSP server the user selected, verify the binary is installed:

```bash
which <command>
```

- **Found**: Confirm with a checkmark: "✓ `<command>` found at `<path>`"
- **Not found**: Warn with install command: "⚠ `<command>` not found. Install with: `<install-command>`. Server will activate once installed."

Include the server in `.lsp.json` regardless — it activates once the binary is installed.

7. **Disable auto-compact**: "Do you want to disable Claude Code's auto-compact feature?
    Auto-compact compresses conversation history as the context window fills,
    which can lose important context during long sessions. (Recommended: Yes — disable it)"
   - Default: Yes
   - If Yes: set `"autoCompactEnabled": false` in `~/.claude/settings.json` using jq (see step 5c for the exact jq/mv sequence, and its Write-then-mv variant when the file doesn't exist yet)
   - If No: remove the `autoCompactEnabled` key from `~/.claude/settings.json` (if present)
   - Either way, also remove any `CLAUDE_AUTOCOMPACT_PCT_OVERRIDE` key from the `env` object in `~/.claude/settings.json`. Earlier versions of this skill set it to `"1"` believing that meant manual-only compaction; Claude Code interprets it as "compact once 1% of the context window is used", so any leftover value causes constant compaction and must be purged.

7b. **Pin subagents to 200K context**: "Do you want to pin cenci's subagents to a 200K-context
    model? cenci delegates reviews to subagents, and on 1M-context sessions that delegation can be
    gated — every subagent inherits the session's 1M flag but not its extra-usage entitlement, so
    reviews fail with 'Usage credits required for 1M context' (Claude Code bug #51060). Pinning
    subagents to Sonnet 200K keeps reviews working while your main session keeps its 1M context.
    (Recommended: Yes if you run a 1M-context session; No otherwise — see the tiering caveat below)"
   - Default: Yes when the session plausibly runs a 1M model; No otherwise
   - If Yes: merge `{"env": {"CLAUDE_CODE_SUBAGENT_MODEL": "claude-sonnet-5"}}` into `~/.claude/settings.json` using jq (see step 5c-bis for the exact jq/mv sequence, and its Write-then-mv variant when the file doesn't exist yet). This runs all `Task` subagents on Sonnet 200K regardless of the main session model. (Pin Sonnet, not Opus — Opus is auto-upgraded to 1M on Max/Team/Enterprise plans and would re-trigger the gate.)
   - If No: remove the `CLAUDE_CODE_SUBAGENT_MODEL` key from the `env` object in `~/.claude/settings.json` (if present)
   - **Tiering caveat (state regardless of answer)**: the pin overrides every agent's `model:` frontmatter — cenci's model tiering (opus refiner/planner/security-reviewer, haiku context-gatherer/structure-analyzer/lessons-collector) is flattened onto the pinned model while it is set. On a standard 200K session the 1M gate never fires, so answer No there to keep the tiering active.
   - **Caveat (state regardless of answer)**: this only affects **new** sessions — restart after configuring. If subagent reviews still fail with the 1M gate even after pinning (the pin didn't strip `[1m]`), run `/model sonnet` for the current session, which always yields 200K.

8. **CI/CD pipeline**: "Do you want to generate a CI/CD pipeline?"
   - Options: "Yes — generate a CI workflow", "No — skip"
   - Default: No
   - Platform: GitHub Actions

   **Conflict check**: If the user selects Yes, scan for existing CI configuration:
   - Use the `Glob` tool with patterns `.github/workflows/*.yml` and `.github/workflows/*.yaml`

   If any files are found, present them and ask:
   - **Single file**: "Found existing CI configuration at `<path>`. What would you like to do?"
   - **Multiple files**: "Found existing CI workflows:\n  - `<path1>`\n  - `<path2>`\n  ...\nWhat would you like to do?"

   Options: "Overwrite — generate `ci.yml` (existing files are not deleted)", "Skip — keep existing files", "Show existing — display the current file contents"
   - If Skip: still record `cicd` in config.json, don't write the file
   - If Show existing: read and display each file, then re-ask Overwrite/Skip

   **Stack-to-CI mapping**: Use the detected stack from question 1 to select the appropriate lint, build, and test commands:

   | Stack | Lint | Build | Test |
   |---|---|---|---|
   | `dotnet*` | `dotnet format --verify-no-changes` | `dotnet build --no-restore` | `dotnet test --no-build --collect:"XPlat Code Coverage"` |
   | `go` | `golangci-lint run ./...` | `go build ./...` | `go test ./... -coverprofile=coverage.out` |
   | `python` | `ruff check .` | *(none)* | `pytest --cov=. --cov-report=xml` |
   | `rust` | `cargo clippy -- -D warnings` | `cargo build` | `cargo test` |
   | `angular*` | `ng lint` | `ng build --configuration production` | `ng test --watch=false --code-coverage` |
   | `react` / `next` | `npx eslint .` | `npm run build` | `npm test -- --coverage --watchAll=false` |
   | `vue` | `npx eslint .` | `npm run build` | `npm run test:unit -- --coverage` |

   **Package manager detection** (for Node-based stacks): use `detection.packageManager`. Manual fallback:
   - `pnpm-lock.yaml` → pnpm
   - `yarn.lock` → yarn
   - `package-lock.json` → npm
   - .NET → NuGet cache on `**/*.csproj`
   - Go → built-in cache in `actions/setup-go@v5`

   **Version pinning**:
   - Node: `engines.node` from `package.json`, fallback `"20"`
   - .NET: extract from stack token (`dotnet10` → `"10.x"`)
   - Go: first line of `go.mod`
   - Python: `python-requires` from `pyproject.toml`, fallback `"3.12"`
   - Rust: `rust-toolchain.toml` or `"stable"`

9. **Sandbox Dockerfile**: "Generate a sandbox Dockerfile for this repo? (Tailors the sandbox image to your stack; committed so your team shares it.)"
   - Options: "Yes — generate `.cenci/Dockerfile`", "No — skip"
   - Default: Yes

   **Mandatory agent runtime**: Always include `node.dockerfile`, regardless of the detected project stack. Claude Code and Codex are npm-distributed launchers installed by the isolated shared-volume updater, so generated images need Node.js but must not bake either agent CLI.

   **Stack-to-fragment mapping**: In addition to the mandatory Node runtime fragment, use the detected stack from question 1 (or, for monorepos, the union of every `projects[].stack.framework` value) to select which `sandbox/fragments/*.dockerfile` blocks to include:

   | Detected stack | Fragment |
   |---|---|
   | `dotnet*` | .NET SDK block (version from the token) |
   | `angular*` / `react` / `next` / `vue` / `node` | Node block |
   | `angular*` / `react` / `next` / `vue` | Playwright block (Chromium, for `verify-ui` screenshot capture) |
   | `go` | Go block |
   | `python` | Python + uv block |
   | `rust` | Rust block |
   | *(none — config-selected)* | Docker block, when `sandbox.dind: true` (question 9b) |
   | *(none — config-selected)* | Azure block, when `sandbox.azure: true` (question 9c) |

   Playwright is scoped to the frontend-framework tokens, not plain `node` — a Node-based
   backend/API project gets the Node block without paying Chromium's image-size cost for a
   visual-verification step it will never run.

   **Docker fragment** (config-selected, not stack-token-selected): when the config being
   written enables nested Docker (`sandbox.dind: true`, question 9b), additionally include
   `sandbox/fragments/docker.dockerfile` — it installs the Docker CLI, the `docker-ce`
   engine and `containerd.io` so `entrypoint.sh` can start an inner daemon under
   `sysbox-runc`. This block used to live in `Dockerfile.base` and so shipped in every
   image; since #831 it is selected only for repos that actually run nested Docker.
   **A `dind: true` repo whose `.cenci/Dockerfile` omits this fragment builds an image
   with no `dockerd`** — the sandbox still boots and stays usable, but nested Docker is
   unavailable and `~/.cenci-dockerd-startup-error` explains why. So when Q9 is answered
   No (no `.cenci/Dockerfile` generated) and Q9b is answered Yes, tell the user their repo
   will use the shared `cenci-sandbox:latest` monolith, which carries the Docker block
   already — no action needed.

   **Azure fragment** (config-selected, not stack-token-selected): when the config being
   written enables the Azure CLI (`sandbox.azure: true`, question 9c), additionally
   include `sandbox/fragments/azure.dockerfile` — it installs `az` from Microsoft's apt
   repo so an agent can check real command syntax with `az <group> <cmd> --help` instead
   of guessing it. There is no stack token for this: an Azure repo can be written in any
   language, so the opt-in is the only signal. Unlike the Docker fragment there is **no**
   monolith fallback — `cenci-sandbox:latest` carries no `az` either — so a repo that
   answers Yes to Q9c but No to Q9 gets no Azure CLI at all; tell the user Q9 must also be
   Yes for the CLI to reach their sandbox.

   **Monorepo**: take the union of all `projects[].stack.framework` values, deduplicated — e.g. a repo with a Go API project and a React web client project selects both the Go and Node fragments. Node is still emitted only once because the mandatory runtime set and stack-selected set are deduplicated.

   A stack token that matches no row above (e.g. `markdown-shell`, `docker-shell`) contributes no additional project fragment. This is not an error — the generated Dockerfile still contains the mandatory Node runtime fragment.

   **.NET version substitution** (the only row with a version-from-token adjustment): `sandbox/fragments/dotnet.dockerfile` ships with `ARG DOTNET_SDK_VERSION=10.0.100` as its own default. When including this fragment, replace that default's version with `<major>.0.100`, where `<major>` is extracted from the stack token using the same extraction as the CI mapping's version-pinning table above (`dotnet10` → `10`) — e.g. a `dotnet8` stack writes `ARG DOTNET_SDK_VERSION=8.0.100`. **Monorepo tie-break**: when multiple projects map to the dotnet fragment with different major versions (e.g. one project on `dotnet8`, another on `dotnet10`), use the **highest** major version found across all matching projects. If no major version can be extracted from the token, leave the fragment's own default (`10.0.100`) unmodified — and add an inline comment immediately after the `ARG DOTNET_SDK_VERSION` line noting the version could not be auto-detected from the stack token and the fragment's default was used instead, e.g. `# .NET version could not be auto-detected from the stack token — using fragment default. See sandbox/README.md to pin manually.` The other fragments (node, playwright, go, python, rust, docker, azure) are included verbatim with their own `ARG` defaults unmodified — every fragment `ARG` (including `DOTNET_SDK_VERSION` and `BASE_VERSION`) remains overridable at build time via `--build-arg`, so an unmodified default is never a hard lock-in.

   > **Sync obligation**: `sandbox/fragments/*.dockerfile` is the source of truth for these blocks; the mapping table above mirrors their content and existence, not their byte contents (generation reads the fragment files directly — see step 5e). If a fragment is added, removed, or renamed, this table needs a matching manual update. Low risk in practice — both live in the same monorepo and are maintained together — but currently unenforced by tooling.

   > **Trust / security note**: `.cenci/Dockerfile` is committed to the repo, so it is reviewed like any other file in the PR that adds or changes it. It only runs `docker build` steps assembled from `sandbox/fragments/*.dockerfile` — no arbitrary runtime hooks execute during configure or during the build it produces.

9b. **Nested Docker (dind)**: "Does this repo need Docker inside the sandbox — Testcontainers, `docker build`/`docker run` in tests, or a Docker SDK client?"
   - Options: "Yes — enable nested Docker (`sandbox.dind`)", "No — skip"
   - Default: Yes when `dindDetected` is `true` (a Testcontainers/Docker-SDK trigger was found above), otherwise No
   - This question is independent of question 9 (Sandbox Dockerfile) — ask it regardless of how Q9 was answered, and record its answer separately (see the `sandbox.dind` schema note below).
   - If Yes: inform the user that nested Docker requires the host to have Docker (not Podman) with the `sysbox-runc` container runtime registered — `cenci doctor` reports this — and point at `sandbox/README.md#nested-docker-sysbox` for host install instructions per distro.
   - If Yes **and** question 9 generated a `.cenci/Dockerfile`: that Dockerfile must include `sandbox/fragments/docker.dockerfile` (see the mapping table's Docker rule under question 9). Because Q9b is asked after Q9, generate the Dockerfile only once this answer is known — or regenerate it here — so a `dind: true` repo never ends up with an image that has no `dockerd`. Tell the user to re-run `/cenci:configure` and then `cenci sandbox build` to pick the fragment up.

9c. **Azure CLI**: "Does this repo need the Azure CLI (`az`) inside the sandbox — Azure resources, Bicep/ARM templates, or Azure DevOps?"
   - Options: "Yes — install the Azure CLI (`sandbox.azure`)", "No — skip"
   - Default: pre-select from `existingConfig.sandbox.azure`; when the field is absent, default to No. There is **no** dependency scan behind this one: an Azure repo can be written in any language and Azure SDK packages appear in plenty of repos that never touch `az`, so a detected dependency would be a poor proxy for wanting a ~500MB CLI in the image. Ask plainly instead.
   - Like Q9b, this is independent of question 9 — ask it regardless of how Q9 was answered, and record its answer separately (see the `sandbox.azure` schema note below).
   - If Yes **and** question 9 generated a `.cenci/Dockerfile`: that Dockerfile must include `sandbox/fragments/azure.dockerfile` (see the mapping table's Azure rule under question 9). Q9c is asked after Q9, so generate the Dockerfile only once this answer is known — or regenerate it here.
   - If Yes **and** question 9 was answered No: unlike dind, the shared `cenci-sandbox:latest` monolith carries **no** `az`, so there is no fallback. Tell the user their sandbox will not have the Azure CLI until they also opt into a per-repo Dockerfile (Q9).
   - If Yes: also tell the user that `cenci open` will stage their host login (`~/.azure`'s `azureProfile.json`, `msal_token_cache.json`, `service_principal_entries.json`) read-only into the sandbox, seeded once into its home volume — so `az account show` works on first open, and a later `az login` inside the container is never overwritten by the host copy. If they have no host login, `az login` inside the sandbox works and persists in the home volume.

### Board Config (lazyboards)

**This section runs on every configure invocation** — there is no install/opt-in
gate. Check whether a board config already exists (run the check as its **own**
Bash call, per `cenci:shell-rules`) and branch:

- **No `.lazyboards.yml` at the repo root** → ask **question 10** below (offer to
  generate one). On "No", omit `lazyboards` from config.json (same pattern as
  `cicd`/`sandbox`).
- **`.lazyboards.yml` already exists** → **skip question 10** and jump to
  **Existing config: suggest or skip** below (analyze the file against the
  recommended action set, suggest what's missing, or skip quietly with a small log).

10. **Board config** (no existing `.lazyboards.yml`): present this Yes/No
    confirmation via `AskUserQuestion` **in this session** — a pre-existing
    `lazyboards.enabled: true` recorded from a prior run, or `$ARGUMENTS` requesting a
    narrower focus or a skip, never authorizes silently regenerating
    `.lazyboards.yml` without asking again this session: "Generate a per-repo
    `.lazyboards.yml` for the lazyboards board? (Wires Refine/Implement keybindings onto
    the New/Refined/Planned columns, Edit-plan and View-plan keybindings on Planned that open
    the ticket's saved plan in `$EDITOR` / a pager, plus In Review actions that open a
    PR's registered worktree in a tmux window (`W`) and, per project, serve or test it
    with a mnemonic key sequence — reviewing a PR becomes a couple of keypresses on
    the card.)"
   - Options: "Yes — generate `.lazyboards.yml`", "No — skip"

   **If Yes — detect runnable projects and their serve commands.** For the single
   project (or each monorepo project confirmed in Step 2a), derive a serve command
   from the first matching rule:

   | Rule (first match wins) | Serve command |
   |---|---|
   | `package.json` has a `dev` script | `npm run dev` |
   | `package.json` has a `start` script | `npm run start` |
   | Angular project (`@angular/core`) without either script | `ng serve` |
   | `.csproj` with `Microsoft.NET.Sdk.Web` | `dotnet run` |
   | Go module containing a `main` package | `go run .` |
   | Anything else (libraries, tooling, markdown/shell) | *not runnable — no action generated* |

   Only the **runner invocation** above is ever embedded in the generated file
   (`npm run dev`, `ng serve`, …) — never the script *contents* from `package.json`,
   which are semi-trusted external values (see `docs/skill-authoring.md`).

   **Also derive a test command** for each project (first match wins), so the In
   Review column can offer a one-keypress "run the PR's tests in its worktree"
   action alongside serve. Reuse the project's stored `testCommand` from
   `existingConfig.projects[]` when present before falling back to this table:

   | Rule (first match wins) | Test command |
   |---|---|
   | `package.json` has a `test` script | `npm test` |
   | Angular project (`@angular/core`) | `ng test --watch=false` |
   | `.csproj` or `.sln` present | `dotnet test` |
   | Go module | `go test ./...` |
   | Anything else (no detectable tests) | *not testable — no test action generated* |

   As with serve, only the **runner invocation** is embedded — never the raw `test`
   script *contents* from `package.json`.

   **Key assignment**: any key, of any case, can carry a binding — there is no
   reserved namespace — and lazyboards supports multi-key sequences, not just
   single keys, so per-project serve/test actions never have to compete for a
   scarce pool. A sequence is written in
   **canonical space-separated form and quoted** — `"S b"`, not `Sb`, which would
   parse as a single two-character key rather than a two-key sequence.

   **`W` is reserved board-wide for Open worktree** — a single action, always emitted
   on `In Review`, that opens the PR's registered worktree in a tmux window with a
   plain shell and runs no command (see the generated example below). `W` is never
   assigned to serve, test, or any other action.

   **Keys lazyboards claims by default.** A user binding wins over a built-in
   default, so binding one of these silently replaces the built-in command rather
   than erroring. Never assign any of them:
   `?` `q` `n` `e` `c` `o` `r` `p` `x` `d` `P` `m` `A` `G` `D` `s` `f` `a` `/`
   `j` `k` `l` `h` `tab` `shift+tab` `1`–`9` `ctrl+c`, plus the `g` prefix (`g a`,
   `g r`). Of the keys cenci generates, none collides with lazyboards' own bindings —
   `R I E V W C X S T` are all free.

   **Never bind or unbind `ctrl+c`.** It always force-quits, ahead of any table
   lookup; a `ctrl+c` token anywhere in any key or sequence — even as an explicit
   `~` unbind — is a load-time config error that stops the whole config from
   loading.

   **Prefix constraint**: a bound key that is a strict, whitespace-boundary prefix
   of another bound key in the same effective table is a **load-time config error**
   — lazyboards refuses to load the file at all, rather than the shorter key merely
   losing at dispatch time. The effective table is the fully resolved namespace:
   built-in defaults **plus** the user's `keymaps.<mode>` table **plus** that
   column's `keymaps.columns.<name>` overlay. So the built-in defaults are a prefix
   source too — a `d`-prefixed sequence (`"d x"`) is invalid because the default
   `d` (`card.delete`) is already bound, and the `g` prefix is unavailable in the
   other direction because `g a`/`g r` already exist. Before assigning the `S`/`T`
   mnemonic prefixes below, check the whole resolved namespace — the default keys
   above, `keymaps.normal`/`keymaps.detail`, and the target column's own overlay,
   including any user-added binding such as a manually bound `S: Sync` — for a
   standalone key sharing the leading letter. If one is claimed, pick a different
   leading letter for that project's serve/test group instead (e.g. `R` for "Run")
   and call out the substitution explicitly in the AskUserQuestion mapping prompt
   below so the user can approve or rename it.

   Assign **serve** keys as `S` followed by a project-specific mnemonic letter:
   pick whichever second letter best identifies the project for its type — e.g.
   `"S b"` for a backend/API project, `"S f"` for a frontend project, or the first
   letter of the project slug when neither fits (e.g. `"S w"` for `web-client`,
   `"S a"` for `admin`). For a single-project repo, plain `S` is enough — there's
   nothing to disambiguate. On a mnemonic collision between two projects, fall back
   to the next letter of that project's slug.

   Assign **test** keys the same way: plain `T` for a single testable project, or
   `T` + mnemonic (`"T b"`, `"T f"`, …) for multiple, following the same mnemonic
   rule as serve.

   Never use `C` or `X` (the generated file's own `keymaps.normal`/`keymaps.detail`
   tables claim them for the Claude/Codex board-level launch actions), never use `E`
   or `V` (the Planned column's Edit-plan and View-plan actions claim them), never
   reuse a key or key sequence already assigned
   to a serve action, never repurpose `W` for anything but Open worktree, and never
   assign a leading letter already bound as a standalone key anywhere in the
   resolved namespace per the prefix constraint above.

   Present the proposed mapping with AskUserQuestion before generating, e.g.:
   "Proposed In Review actions: `W` → open PR worktree, `S b` → api serve
   (`dotnet run`), `S f` → web-client serve (`ng serve`), `T f` → web-client tests
   (`ng test --watch=false`). Generate these?" Options: "Yes — use this mapping
   (Recommended)", "Change keys or drop projects" (then re-ask with the user's
   adjustments; enforce the reserved-key exclusions above).

### Fleet Dispatch Enrollment

**This section runs on every configure invocation** — there is no install/opt-in
gate, matching Board Config (lazyboards) above. Its side effect fires immediately at
question time; nothing here is deferred to the generation step below.

**Container guard (runs first).** Use `detection.inContainer` (already resolved above).
When it is `true`, this section asks nothing, runs no `cenci dispatch` command, and writes nothing anywhere
— the sandbox mounts `/home/dev` as a per-repo named volume, so
the container's `~/.config/cenci/config.json` is not the host file the dispatch daemon
reads, and an in-container enroll would be a silently dead fleet config. Emit an
informational message naming that reason and the host-side fix: "Fleet dispatch
enrollment can't run inside the sandbox — its `~/.config/cenci/config.json` lives in
the container's `/home/dev` volume, not the file the host dispatch daemon reads. To
enroll, run `cenci dispatch enroll --session <name>` from the repo root on the host."
Never claim the repo was enrolled, and never fabricate a host path for `--dir` — the
workspace is bind-mounted at a container-local path that has no reliable host
equivalent, so the advisory omits `--dir` entirely and lets the host-side command
resolve its own working directory. Skip the remainder of this section
(main-checkout resolution, status probe, questions 11/12) and continue directly to
the next section (`### Autonomy Settings`).

**Main-checkout resolution (host runs only).** Run
`git rev-parse --path-format=absolute --git-common-dir` as its own Bash call (already
covered by the existing `Bash(git rev-parse:*)` grant) and strip the trailing `/.git` from its output to get
`<main-checkout>`. If that call fails, log one informational line noting the
fallback, then use the repository root the Scripted Detection step ran from.
`<main-checkout>` must always be used below — never
`<worktree-path>` (see Create Worktree above) and never a bare default: `cenci dispatch
enroll` defaults its directory to the current directory, which inside a configure run is
the transient `.worktrees/configure-<slug>` checkout, not the repo.

**Main-checkout path validation (shell safety only).** If the resolved
`<main-checkout>` value contains a single quote or a newline, log one informational
line and skip the rest of this section — same skip-to-`### Autonomy Settings`
behavior as the container guard above — rather than emit a broken command. This
mirrors the session-name rule in question 12 below; it is shell-safety only, not
semantic path validation.

**Status probe.** Run `cenci dispatch status --json --dir '<main-checkout>'` as its own
Bash call (per `cenci:shell-rules`, never compounded with the resolution call above) and
parse its stdout as JSON.

- If the command exits non-zero, or its stdout is not parseable JSON, log one
  informational line and fall through — this never blocks or aborts the configure run.
- If the parsed object has no `session` key, the installed `cenci` binary predates
  #933's `status --json` support. Ask nothing, run no `enroll`, and
  advise the user to update cenci before enrolling (flow and watch version independently — see root
  `AGENTS.md`).

**Three-way branch** on the parsed object's `enrolled`/`session` fields:

- `enrolled: false` → ask question 11 below.
- `enrolled: true, session: ""` → the repo is already enrolled but has no session yet —
  the state lazyboards' board-driven enrollment leaves behind (see the "Fleet dispatch
  from the board" section of `docs/orchestration.md`), so this is the common repair
  path, not an edge case. Skip question 11 and ask only question 12.
- `enrolled: true, session: "<set>"` → skip both questions, log the resolved session
  quietly, and fall through.

Re-running `/cenci:configure` on an already-configured repo never re-prompts and never
rewrites the config. If the enrolled `dir` reported by `status --json` differs from the
resolved `<main-checkout>`, log the mismatch as an informational line only — never
re-enroll to correct it; the no-rewrite rule wins.

11. **Enroll in fleet dispatch**: ask via `AskUserQuestion`: "Enroll this repo in fleet
    dispatch? This lets `cenci dispatch` and the fleet dispatch loop pick up approved
    plans for this repo automatically. `dispatch.*` is a user-level, fleet-wide setting
    stored in `~/.config/cenci/config.json` — distinct from this repo's
    `.cenci/config.json` — and the effect is immediate, not part of this PR."
    - Options: "Yes — enroll this repo", "No — skip"
    - On "No", write nothing to `~/.config/cenci/config.json` and leave any existing
      block untouched. A decline is not recorded anywhere — this section re-asks on the
      next invocation, mirroring the Board Config (lazyboards) precedent. There is no
      unenroll offer here.

12. **Fleet dispatch session name** (asked via `AskUserQuestion` when question 11 was
    answered "Yes", or directly when the branch above found `enrolled: true, session:
    ""`): "What tmux session should fleet dispatch use for this repo? Without one, this
    repo is skipped on every dispatch pass and the daemon reports
    `dispatch_session_unconfigured` (#927) — this is not optional." Collect the answer
    in a single `AskUserQuestion` free-text field only: no pre-filled value and no picker
    of running sessions. This section never guesses the session name from `$TMUX_PANE`,
    an attached client, the current pane, running tmux sessions, or the repo/directory
    name — guessing ambient state is the bug #927 exists to close. Reject the answer and
    re-ask when it is empty, whitespace-only, or contains a single quote or a newline
    (shell safety only; semantic validation of the name stays in `cenci dispatch
    enroll`).

    Once a valid session name is collected, issue a single combined write — both
    enrollment and session in one call, never two separate writes — as its own Bash
    call: `cenci dispatch enroll --dir '<main-checkout>' --session '<name>'`, with both
    `<main-checkout>` and `<name>` single-quoted.

**Scope.** `dispatch.*` lives in `~/.config/cenci/config.json` (or
`$XDG_CONFIG_HOME/cenci/config.json`) — user-level and fleet-wide, the same file
`automerge.enabled` above reads from — but `repos[].session` and each repo's enrollment
are nonetheless per-repo entries inside that fleet-wide file. This section
never reads, modifies, or writes ~/.config/cenci/config.json itself: every mutation goes through
`cenci dispatch enroll`, which already owns the atomic, key-preserving write path
(`EnrollRepo`, `watch/internal/dispatch/enroll.go`), including creating the file and its
parent directory. The effect is immediate and user-level, so nothing lands in
`<worktree-path>` and no key is added to this repo's `.cenci/config.json` — this
section contributes nothing to the configure PR diff.

**Next step.** After a successful enroll, point the user at `cenci dispatch loop on` as
the explicit next step to start the recurring dispatch loop — that command already
defaults its interval to `5m` when the user doesn't set one, so this section never asks
about the dispatch loop's enable flag or interval setting itself.

### Autonomy Settings

**This section runs on every configure invocation** — there is no container guard: unlike
Fleet Dispatch Enrollment above, `planning` and `automerge` are repo-committed keys that
land inside this run's PR, so an in-container run is fine. Both questions below only
collect an answer; neither writes anything itself — step 6 below performs the actual
write, overlaying whatever was collected here onto the merged config.

**Absent-only rule.** When `planning` or `automerge` is already present, report the
existing value verbatim, never re-prompt, never narrow, and never remove it.

**Presence detection**, read from `existingConfig` (already in hand from Existing Config
Detection above):
- `planning` is present iff `existingConfig.planning` exists.
- `automerge` is present iff a top-level `automerge` key exists or any `projects[]` entry
  carries its own `automerge` key — monorepo automerge can be per-project only, so a
  top-level-only check would wrongly re-offer the question on a repo whose policy lives
  entirely in `projects[]`.

13. **Plan approval autonomy** (asked via `AskUserQuestion` only when `planning` is
    absent): "Should plan approval stay interactive, or switch to lean self-approval?
    `interactive` keeps today's behavior — the planner asks up to 6 clarifying questions
    and never self-answers. `lean` lets a plan with no escalations continue straight into
    implementation in the same session, and also authorizes `cenci dispatch`'s unattended
    planning pickup and autonomous re-plan once pushed to `main` (see
    `docs/autonomous-loop.md`'s \"Let plans approve themselves\")."
    - Options: "Keep `interactive` (Recommended)", "Switch to `lean`"
    - Declining omits the `planning` key entirely — no `planning` key is written.

14. **Automerge policy block** (asked via `AskUserQuestion` only when `automerge` is
    absent): "Scaffold a starter `automerge` policy block for this repo? This does not
    enable automerge by itself — it only seeds a deny-by-default policy that a human must
    still review, and the fleet-wide `automerge.enabled` switch (see
    `docs/autonomous-loop.md`) stays off until you flip it separately. This section never
    invents a risk policy field-by-field — it's a binary choice between no block and a
    conservative starter block."
    - Options: "Skip — no block (deny-by-default) (Recommended)", "Scaffold a starter
      block for hand review"
    - Declining omits the `automerge` key entirely — no `automerge` key is written.
    - On "Scaffold a starter block for hand review", seed `protectedPaths` from the union
      of three sources, deduplicated, additive only, never narrowing any of them: (a) the
      **full** mandatory baseline of category globs — the complete implement Sensitive-path
      backstop default pattern list (`flow/skills/implement/SKILL.md`'s built-in defaults,
      all 36 patterns, verbatim), plus the release/CI path; (b) any confirmed repo-shape
      paths (e.g. `.cenci/`); and (c) `existingConfig.security.sensitivePaths` when that key
      is present — the repo owner's own hand-declared sensitive-path patterns (see
      `security.sensitivePaths` elsewhere in this file), the one signal the built-in
      defaults can't cover by design. Set tight caps. The template below is the value
      written to the top-level `automerge` key, verbatim (with `protectedPaths` extended
      per repo shape and `existingConfig.security.sensitivePaths` when applicable):

<!-- cenci:automerge-scaffold:begin -->
```json
{
  "protectedPaths": [
    "*auth*",
    "*login*",
    "*logout*",
    "*session*",
    "*password*",
    "*passwd*",
    "*credential*",
    "*secret*",
    "*secrets*",
    "*token*",
    "*jwt*",
    "*apikey*",
    "*api_key*",
    "*.pem",
    "*.key",
    "*.env*",
    "*oauth*",
    "*sso*",
    "*saml*",
    "*openid*",
    "*permission*",
    "*acl*",
    "*rbac*",
    "*role*",
    "*crypto*",
    "*encrypt*",
    "*decrypt*",
    "*sign*",
    "*hash*",
    "*payment*",
    "*billing*",
    "*invoice*",
    "*checkout*",
    "*stripe*",
    "*migrat*",
    "*schema*",
    ".github/",
    ".cenci/"
  ],
  "maxChangedFiles": 10,
  "maxDiffLines": 400,
  "mergeMethod": "squash"
}
```
<!-- cenci:automerge-scaffold:end -->

      In a monorepo, this scaffold is always written as a single top-level block (never
      per-`projects[]` blocks) — a complete, valid, most-restrictive policy on its own
      that needs no per-project path derivation; the PR-body review flag (below) tells the
      human to consider splitting it into per-project blocks if that fits the repo better.

**Next step.** Point the user at the fleet-side verbs from #964/#968 as the explicit next
steps — neither is flipped by this skill:
- `cenci dispatch plan-refined on|off|status` to let dispatch pick up unattended planning
  once `planning.autonomy` is `lean` on `origin/main`.
- `cenci automerge on|off|status` to arm the fleet-wide automerge kill switch once a
  policy block exists.
- See `docs/autonomous-loop.md` for the full walkthrough of all four switches.

### Auth Verification

Before generating config, verify CLI authentication:

Run `gh auth status` and check it returns authenticated. If not, instruct the user to run `gh auth login` first.

After gathering answers:

0. **Generate Codex agent adapters**: copy the reviewed TOML role templates from
   `templates/codex/agent-roles/` into `.codex/agents/`. Preserve unknown user-authored agent
   files. Planning, implementation, and critical review use GPT-5.6/high; gathering and
   read-heavy analysis use GPT-5.6-terra/medium. Native procedures must fall back to built-in
   workers with the same role prompt when an adapter is unavailable.

1. **Generate canonical guidance and client adapters**:
   - `AGENTS.md` at the repository root is canonical shared guidance. Use
     `templates/agents-md-root.md` or `templates/agents-md-root-monorepo.md`.
   - For each monorepo project, generate `<project>/AGENTS.md` from
     `templates/agents-md-project.md`.
   - Generate root `CLAUDE.md` as `@AGENTS.md`, followed only by an optional block
     delimited with `<!-- cenci:claude-only:start -->` and
     `<!-- cenci:claude-only:end -->`.
   - Generate each `<project>/CLAUDE.md` as `@AGENTS.md` with the same optional block.

   Discover root `AGENTS.md`, root `CLAUDE.md`, legacy `.claude/CLAUDE.md`, and every
   configured project's AGENTS/CLAUDE pair. A retained `.claude/CLAUDE.md` adapter imports
   `@../AGENTS.md`. Before replacing any substantive existing guidance, render and show
   the complete proposed diff with `git diff --no-index`, then require approval through
   `AskUserQuestion`. Preserve existing material by merging it into the shared AGENTS
   content or the explicitly Claude-only block. Never silently delete guidance. Stable
   markers make reruns idempotent. Never delete a second substantive guidance file unless
   the user explicitly approves its content having been merged into AGENTS.md.

1b. **Generate `.lsp.json`** (if any LSP servers were selected in question 6):

   Write `.lsp.json` **in the project root** (not `${CLAUDE_PLUGIN_ROOT}`) with entries for selected servers only, using the command, args, and extension map from the LSP Server Catalog. Claude Code only reads `.lsp.json` from the project root — plugin-scoped LSP config is not supported. If `.lsp.json` already exists in the project root, merge new entries into it (preserve existing entries). Example:

   ```json
   {
     "typescript": {
       "command": "typescript-language-server",
       "args": ["--stdio"],
       "extensionToLanguage": {
         ".ts": "typescript",
         ".tsx": "typescriptreact",
         ".js": "javascript",
         ".jsx": "javascriptreact"
       }
     },
     "csharp-ls": {
       "command": "csharp-ls",
       "extensionToLanguage": { ".cs": "csharp" }
     }
   }
   ```

   Omit the `args` field if the catalog entry has an empty array `[]`.

2. Create the `docs/` directory at the repo root (if it doesn't exist) and deploy on-demand reference docs from `${CLAUDE_PLUGIN_ROOT}/templates/docs/`:
   - `docs/git-workflow.md` — branching, commit format, PR workflow

   `.claude/rules/` is reserved for files explicitly imported by the generated Claude adapter. Do NOT deploy shared reference docs there.

   **Backward compatibility**: Do NOT delete or migrate any existing `.claude/rules/lessons-learned.md`, `.claude/rules/lessons-learned-<slug>.md`, or `.claude/rules/git-workflow.md` files. Skills and agents continue to read them as legacy fallback if present.

   Do NOT deploy `testing.md` or `security.md` — testing rules load on-demand via the `testing` skill, and security rules are distributed across root/project AGENTS.md and stack skills.

**Monorepo-only additional files:**

3a. For each project, create `<project-path>/AGENTS.md` using `templates/agents-md-project.md`, then create its `CLAUDE.md` import adapter — customize with:
   - `<project-name>`: the project name (from slug or user input)
   - `<stack>`: detected stack
   - `<repo-name>`: the repository name
   - `<framework + version>`: detected framework
   - `<test-framework>`: detected test framework
   - `<build-command>`: detected or user-provided build command
   - `<test-command>`: detected or user-provided test command
   - `<project-specific rules populated during configure>`: leave as a placeholder for the user to fill in later, or remove the bullet if no conventions are known yet

3c. **Ensure board lifecycle labels exist**: `gh issue edit --add-label` fails when the label is missing from the repository, so create the lifecycle set now. Run `gh label list --repo <owner>/<repo> --limit 100 --json name` once, then for each **missing** label run its own `gh label create` call (never modify or recolor a label that already exists):

   ```bash
   gh label create "<name>" --repo <owner>/<repo> --color "<color>" --description "<description>"
   ```

   | Label | Color | Description |
   |---|---|---|
   | `Working` | `FBCA04` | Actively being refined or implemented |
   | `Refined` | `0E8A16` | Ready for implementation |
   | `Planned` | `1D76DB` | Plan on disk, ready to pick up |
   | `In Review` | `A2EEEF` | PR open, under review / CI running |
   | `Implemented` | `6F42C1` | PR merged — done |
   | `Input Needed` | `D4C5F9` | Planner escalated a question — answer on the ticket to auto-resume |
   | `Followup` | `C5DEF5` | Deferred/out-of-scope item captured from a session — triage before working |
   | `Browser` | `BFD4F2` | Implementation needs interactive browser access (Playwright CLI) |
   | `ui:visual-check` | `FEF2C0` | Visual/layout change — verify in a browser before merge |
   | `automerge:ok` | `006B75` | Human granted hands-off merge at refinement — babysit may merge this PR without review |
   | `dispatch-failed` | `b60205` | cenci: dispatched work failed after exhausting its retry budget |
   | `plan-invalid` | `d93f0b` | cenci: ticket is Planned but has no parseable plan file |
   | `reconcile-stuck` | `5319e7` | cenci: reconciliation itself is stuck (apply-retry budget exhausted) |

   This is the canonical color/description table. The lifecycle rows above are self-healed by the skills' own `gh label create … || true` fallbacks; the reconciler-owned `dispatch-failed` / `plan-invalid` / `reconcile-stuck` rows are self-healed instead by cenci's Go `GHMutator.EnsureLabels` (not a skill-level fallback) — see "Reconciler-managed labels" under Board lifecycle labels below.

   `Followup` is a capture-queue marker, never release-blocking (there is no release gate that reads labels). Captured items are triaged out of the queue by grouping/consolidation via `/cenci:maintain backlog` — which merges duplicates and batches small items, supersede-closing the sources — or promoted individually via `/cenci:refine`. See `docs/followup-triage.md`.

4. **Create or update `.claude/settings.json`**:

   Write the minimal shape below — Claude Code's host sandbox is disabled because the container is the boundary. Under `--dangerously-skip-permissions` Claude Code ignores `permissions.allow/deny`, but keep the base allow list + deny rules as defense-in-depth for the case where a user runs plain `claude` (no skip-permissions) inside the container, e.g. via `cenci open --shell`.

   ```json
   {
     "sandbox": { "enabled": false },
     "permissions": { "allow": [ … ], "deny": [ … ] }
   }
   ```

   - **Fresh** (no existing settings.json): copy `${CLAUDE_PLUGIN_ROOT}/templates/settings.json` as the base.
   - **Existing** settings.json: read it first, then **replace the entire `sandbox` block** with `{ "enabled": false }` (drop `network`, `excludedCommands`, `autoAllowBashIfSandboxed`, and any other sandbox sub-keys an older config may carry). **Preserve** every existing `permissions.allow` and `permissions.deny` entry, including user-added ones — never remove one, with the single legacy-supersession exception called out in the base deny list clause below.
   - Omit `sandbox.network`, `sandbox.excludedCommands`, and `sandbox.autoAllowBashIfSandboxed` entirely — they are meaningless when the sandbox is disabled. Never write `sandbox.network.allowedDomains`.

   Then **append** to it:

   > **IMPORTANT**: All base permissions from the template (`Write`, `Edit`, `Read(~/.claude/plugins/**)`, `Read(//tmp/claude*/**)`, `Edit(//tmp/claude*/**)`, `Read(//tmp/cenci*/**)`, `Edit(//tmp/cenci*/**)`, `Bash(cd:*)`, `Bash(git:*)`, `Bash(gh:*)`, `Bash(wc:*)`, etc.) **MUST** remain in `permissions.allow`. Only **append** new entries — never remove or replace existing ones. When updating an **existing** `settings.json`, also ensure these base entries are present — add any that are missing (older configs predate them — e.g. the `//tmp/cenci*/**` pair for the `${TMPDIR:-/tmp}/cenci/` temp-root migration). The `Read(~/.claude/plugins/**)` rule lets the pipeline read its own plugin files (phase docs resolve to `~/.claude/plugins/cache/<marketplace>/<plugin>/<version>/skills/…`) without prompting — it is deliberately scoped to `plugins/` so subagents cannot read session transcripts or global config under `~/.claude/`. The two `//tmp/*` rule pairs cover two temp roots side by side: `//tmp/claude*/**` still covers the `shell-rules` heredoc temp-file pattern's legacy paths and the Claude Code session scratchpad; `//tmp/cenci*/**` covers the canonical `${TMPDIR:-/tmp}/cenci/` root skills now write under — but only under the default `TMPDIR`, since a custom `TMPDIR` cannot be expressed as a static permission rule, so those writes may still prompt.

   > **IMPORTANT**: All base deny rules from the template **MUST** be present in `permissions.deny`. Only **append** new entries — never remove or replace existing ones, including user-added entries. When updating an **existing** `settings.json`, also ensure these base entries are present — add any that are missing (older configs predate them: they shipped only `Bash(git push --force:*)` and `Bash(git reset --hard:*)`). Two healing specifics: (a) **remove** the legacy `Bash(git push --force:*)` and `Bash(git reset --hard:*)` entries when adding the base list — the boundary-safe forms below supersede them, and the legacy `--force` form also blocks `git push --force-with-lease`, which implement's PR phase requires; (b) deduplicate — never add a base entry the list already contains. **Verify** after healing that every base deny entry is present and neither legacy entry remains.

   The deny list is written with explicit word boundaries rather than the `:*` shorthand wherever the boundary is load-bearing: `Bash(git push --force *)` blocks a bare force-push while leaving `git push --force-with-lease` usable, which implement's PR phase depends on. Deny always overrides allow, so a permitted form must never be caught by a deny rule. `git -C <path>` (used by every phase), `git rebase`, `git branch -D`, `git worktree remove`, and unscoped `git config --get`/`--list` are deliberately **not** denied. Two limits are inherent to prefix rules and are not covered: env-var-prefixed invocations (`GIT_CONFIG_GLOBAL=… git …`) never match a `git …` rule, and implicit-local `git config <key> <value>` writes are caught only for the enumerated code-execution keys.
   `-C <path>` prefix coverage is now added for the highest-value groups (force-push — scoped to the `--force`/`-f` forms only, since `push --mirror`, `push --delete`, `push --no-verify`, and the refspec-force form `push * +*` have no `-C`-prefixed mirror and remain a residual gap — reset --hard, filter-branch/filter-repo, and the `-c` exec-key rules) but not for the `git config` scope-selector write forms (`--global`, `--system`, `--local`, `--unset`, `--add`, `--replace-all`, `--edit`), and `--git-dir=`/`--work-tree=` global-flag prefixes remain entirely uncovered by any rule, old or new — both are residual, documented gaps pending empirical Claude Code Bash-matcher verification (blocked in this environment — no `claude` CLI installed).
   The config-key case-insensitivity fix covers only the four keys with non-lowercase spellings already in the rule set (`core.hooksPath`, `core.sshCommand`, `core.gitProxy`, `core.askPass`); full section-name case variants (e.g. `CORE.hooksPath`, `Alias.foo`) are not exhaustively covered.
   Beyond `-C`, other bypasses are known but not exhaustively covered: (a) arbitrary global-flag prefixes before the subcommand (e.g. `git --no-pager -c core.hooksPath=… status`) can still defeat even the mid-position `-c` forms, since only `-C` is specifically mirrored; (b) quoted or embedded arguments (e.g. `git -c 'core.pager=less -R' log`) break the literal-prefix match entirely — this is not an exhaustive bypass list, only the known ones.

   `gh api` destructive-method coverage denies `DELETE`/`PUT` (method-first and path-first, `-X`/`-XM`/`-X=`/`--method`/`--method=` forms — ten syntactic forms in total — plus lowercase mirrors) so the path-only `Bash(gh api repos/:*)` grant cannot be used to issue `DELETE`/`PUT` requests; like the `-C`/`--git-dir=` residual gaps above, this coverage is unverified pending empirical Claude Code Bash-matcher verification (blocked in this environment — no `claude` CLI installed). The mixed-case form (e.g. `-X Delete`) is an accepted residual under literal prefix matching and remains undenied, alongside `gh api graphql` mutations, `gh` aliases, env-prefixed invocations (e.g. `GH_TOKEN=… gh api …`), quoted method values (e.g. `-X "DELETE"`), and combined shorthand (e.g. `-iXDELETE`) — this residual list is illustrative of known gaps under literal prefix matching, not exhaustive. Two broader gaps remain entirely out of scope for this rule set: `Bash(gh:*)` (the pre-existing blanket allow grant) still permits native destructive `gh` subcommands that never go through `gh api` at all — e.g. `gh repo delete`, `gh release delete`, `gh secret set`, and `gh auth token` (credential exfiltration) — and the still-allowed `-X PATCH` form can itself overwrite or mutate resources (e.g. `gh api repos/o/r -X PATCH -f private=false`).

<!-- cenci:settings-deny:start -->
```json
[
  "Bash(git push --force)",
  "Bash(git -C * push --force)",
  "Bash(git push --force *)",
  "Bash(git -C * push --force *)",
  "Bash(git push * --force)",
  "Bash(git -C * push * --force)",
  "Bash(git push * --force *)",
  "Bash(git -C * push * --force *)",
  "Bash(git push -f)",
  "Bash(git -C * push -f)",
  "Bash(git push -f *)",
  "Bash(git -C * push -f *)",
  "Bash(git push * -f)",
  "Bash(git -C * push * -f)",
  "Bash(git push * -f *)",
  "Bash(git -C * push * -f *)",
  "Bash(git push * +*)",
  "Bash(git push --mirror*)",
  "Bash(git push * --mirror*)",
  "Bash(git push --delete *)",
  "Bash(git push * --delete *)",
  "Bash(git push --no-verify*)",
  "Bash(git push * --no-verify*)",
  "Bash(git commit --no-verify*)",
  "Bash(git commit * --no-verify*)",
  "Bash(git reset --hard*)",
  "Bash(git -C * reset --hard*)",
  "Bash(git reset * --hard*)",
  "Bash(git -C * reset * --hard*)",
  "Bash(git clean:*)",
  "Bash(git checkout -- *)",
  "Bash(git checkout * -- *)",
  "Bash(git restore:*)",
  "Bash(git filter-branch:*)",
  "Bash(git -C * filter-branch)",
  "Bash(git -C * filter-branch *)",
  "Bash(git filter-repo:*)",
  "Bash(git -C * filter-repo)",
  "Bash(git -C * filter-repo *)",
  "Bash(git reflog expire*)",
  "Bash(git reflog delete*)",
  "Bash(git gc --prune*)",
  "Bash(git gc * --prune*)",
  "Bash(git update-ref:*)",
  "Bash(git replace:*)",
  "Bash(git branch -f *)",
  "Bash(git branch --force *)",
  "Bash(git -c core.hooksPath*)",
  "Bash(git -c core.hookspath*)",
  "Bash(git -c * core.hooksPath*)",
  "Bash(git -c * core.hookspath*)",
  "Bash(git -C * -c core.hooksPath*)",
  "Bash(git -C * -c core.hookspath*)",
  "Bash(git -c core.sshCommand*)",
  "Bash(git -c core.sshcommand*)",
  "Bash(git -c * core.sshCommand*)",
  "Bash(git -c * core.sshcommand*)",
  "Bash(git -C * -c core.sshCommand*)",
  "Bash(git -C * -c core.sshcommand*)",
  "Bash(git -c core.pager*)",
  "Bash(git -c * core.pager*)",
  "Bash(git -C * -c core.pager*)",
  "Bash(git -c core.editor*)",
  "Bash(git -c * core.editor*)",
  "Bash(git -C * -c core.editor*)",
  "Bash(git -c core.fsmonitor*)",
  "Bash(git -c * core.fsmonitor*)",
  "Bash(git -C * -c core.fsmonitor*)",
  "Bash(git -c alias.*)",
  "Bash(git -c * alias.*)",
  "Bash(git -C * -c alias.*)",
  "Bash(git -c credential.helper*)",
  "Bash(git -c * credential.helper*)",
  "Bash(git -C * -c credential.helper*)",
  "Bash(git -c core.gitProxy*)",
  "Bash(git -c core.gitproxy*)",
  "Bash(git -c * core.gitProxy*)",
  "Bash(git -c * core.gitproxy*)",
  "Bash(git -C * -c core.gitProxy*)",
  "Bash(git -C * -c core.gitproxy*)",
  "Bash(git -c core.askPass*)",
  "Bash(git -c core.askpass*)",
  "Bash(git -c * core.askPass*)",
  "Bash(git -c * core.askpass*)",
  "Bash(git -C * -c core.askPass*)",
  "Bash(git -C * -c core.askpass*)",
  "Bash(git -c sequence.editor*)",
  "Bash(git -c * sequence.editor*)",
  "Bash(git -C * -c sequence.editor*)",
  "Bash(git -c gpg.program*)",
  "Bash(git -c * gpg.program*)",
  "Bash(git -C * -c gpg.program*)",
  "Bash(git -c diff.external*)",
  "Bash(git -c * diff.external*)",
  "Bash(git -C * -c diff.external*)",
  "Bash(git --config-env*)",
  "Bash(git --exec-path*)",
  "Bash(git config --global*)",
  "Bash(git config --system*)",
  "Bash(git config --local*)",
  "Bash(git config --file*)",
  "Bash(git config -f *)",
  "Bash(git config --unset*)",
  "Bash(git config * --unset*)",
  "Bash(git config --add *)",
  "Bash(git config * --add *)",
  "Bash(git config --replace-all*)",
  "Bash(git config * --replace-all*)",
  "Bash(git config --edit*)",
  "Bash(git config -e*)",
  "Bash(git config set *)",
  "Bash(git config unset *)",
  "Bash(git config core.hooksPath*)",
  "Bash(git config core.hookspath*)",
  "Bash(git config * core.hooksPath*)",
  "Bash(git config * core.hookspath*)",
  "Bash(git config core.sshCommand*)",
  "Bash(git config core.sshcommand*)",
  "Bash(git config * core.sshCommand*)",
  "Bash(git config * core.sshcommand*)",
  "Bash(git config core.pager*)",
  "Bash(git config * core.pager*)",
  "Bash(git config core.editor*)",
  "Bash(git config * core.editor*)",
  "Bash(git config core.fsmonitor*)",
  "Bash(git config * core.fsmonitor*)",
  "Bash(git config alias.*)",
  "Bash(git config * alias.*)",
  "Bash(git config credential.helper*)",
  "Bash(git config * credential.helper*)",
  "Bash(git config core.gitProxy*)",
  "Bash(git config core.gitproxy*)",
  "Bash(git config * core.gitProxy*)",
  "Bash(git config * core.gitproxy*)",
  "Bash(git config core.askPass*)",
  "Bash(git config core.askpass*)",
  "Bash(git config * core.askPass*)",
  "Bash(git config * core.askpass*)",
  "Bash(git config sequence.editor*)",
  "Bash(git config * sequence.editor*)",
  "Bash(git config gpg.program*)",
  "Bash(git config * gpg.program*)",
  "Bash(git config diff.external*)",
  "Bash(git config * diff.external*)",
  "Bash(git remote set-url*)",
  "Bash(git config remote.*)",
  "Bash(gh api -X DELETE*)",
  "Bash(gh api -X delete*)",
  "Bash(gh api -XDELETE*)",
  "Bash(gh api -Xdelete*)",
  "Bash(gh api --method DELETE*)",
  "Bash(gh api --method delete*)",
  "Bash(gh api --method=DELETE*)",
  "Bash(gh api --method=delete*)",
  "Bash(gh api * -X DELETE*)",
  "Bash(gh api * -X delete*)",
  "Bash(gh api * -XDELETE*)",
  "Bash(gh api * -Xdelete*)",
  "Bash(gh api * --method DELETE*)",
  "Bash(gh api * --method delete*)",
  "Bash(gh api * --method=DELETE*)",
  "Bash(gh api * --method=delete*)",
  "Bash(gh api -X PUT*)",
  "Bash(gh api -X put*)",
  "Bash(gh api -XPUT*)",
  "Bash(gh api -Xput*)",
  "Bash(gh api --method PUT*)",
  "Bash(gh api --method put*)",
  "Bash(gh api --method=PUT*)",
  "Bash(gh api --method=put*)",
  "Bash(gh api * -X PUT*)",
  "Bash(gh api * -X put*)",
  "Bash(gh api * -XPUT*)",
  "Bash(gh api * -Xput*)",
  "Bash(gh api * --method PUT*)",
  "Bash(gh api * --method put*)",
  "Bash(gh api * --method=PUT*)",
  "Bash(gh api * --method=put*)",
  "Bash(gh api -X=DELETE*)",
  "Bash(gh api -X=delete*)",
  "Bash(gh api -X=PUT*)",
  "Bash(gh api -X=put*)",
  "Bash(gh api * -X=DELETE*)",
  "Bash(gh api * -X=delete*)",
  "Bash(gh api * -X=PUT*)",
  "Bash(gh api * -X=put*)",
  "Read(~/.ssh/**)",
  "Edit(~/.ssh/**)",
  "Read(~/.aws/**)",
  "Edit(~/.aws/**)",
  "Read(.env)",
  "Edit(.env)",
  "Read(.env.*)",
  "Edit(.env.*)"
]
```
<!-- cenci:settings-deny:end -->

   **Append to `permissions.allow`:**
   - Stack-specific rules (e.g., `Bash(dotnet:*)` for .NET, `Bash(ng:*)` for Angular, `Bash(go:*)` for Go)
   - For each enabled MCP, add its tool permissions. Look up the server's available tools
     and add entries in the format `mcp__<server-name>__<tool-name>` (for project-scoped).
     Known tools:
     - **Context7**: `mcp__context7__resolve-library-id`, `mcp__context7__query-docs`
     - **Angular**: `mcp__angular__:*` (auto-allow all Angular CLI MCP tools)
     - **PrimeNG**: `mcp__primeng__:*` (auto-allow all PrimeNG MCP tools)

   **Pending-plans detection** — no per-project setup required. The pending-plans
   SessionStart hook is shipped plugin-side (`${CLAUDE_PLUGIN_ROOT}/hooks/scripts/check-pending-plans.sh`,
   registered in `flow/hooks/hooks.json`) and runs automatically wherever cenci is
   enabled. Do **not** add a SessionStart entry to `.claude/settings.json` or copy any
   script into `.claude/hooks/`.

   **Legacy cleanup (hook path)** — heal projects configured by an older cenci that installed the
   hook per-project (a fragile cwd-relative path that errored in worktrees and
   subdirectories):
   1. If `.claude/settings.json` has a `hooks.SessionStart` hook whose `command` is
      `.claude/hooks/check-pending-plans.sh`, remove that hook entry. If its enclosing
      block's `hooks` array becomes empty, remove the block too; if `SessionStart`
      becomes empty, remove it. Preserve every other SessionStart entry untouched.
   2. Delete the orphaned script if present: `rm -f .claude/hooks/check-pending-plans.sh`.
      Then remove the directory only if it is now empty: `rmdir .claude/hooks 2>/dev/null || true`
      (the `|| true` keeps it non-fatal when the dir is absent or still holds other hooks;
      run as its own Bash call, never compounded with a `cd` — see `cenci:shell-rules`).

   **Legacy cleanup (permissions)** — heal projects configured by an older cenci that shipped
   scoped-path `Write(<path>)` entries in `permissions.allow` and/or
   `permissions.deny` (Claude Code's file permission checker never matches
   scoped-path `Write(<path>)` rules — only scoped-path `Edit(<path>)` rules,
   which also cover Write — so a scoped `Write(<path>)` entry is dead weight
   that produces a startup warning per entry, in both lists):
   1. For **every** scoped-path `Write(<path>)` entry found in
      `permissions.allow` **or** `permissions.deny` (not just the known
      template rules like `Write(//tmp/claude*/**)` or `Write(~/.ssh/**)`),
      **replace** it in place with the corrected `Edit(<path>)` form rather
      than appending the missing entry alongside it. Deduplicate as you go:
      if that same list already contains an `Edit(<path>)` entry with that
      same `<path>` (the template's deny list always did), drop the redundant
      `Write(<path>)` entry instead of creating a duplicate `Edit(<path>)`.
   2. If `permissions.allow` contains a blanket `Write(*)` entry, normalize
      it to bare `Write`. (This normalization applies to `allow` only — a
      bare `Write` in `deny` would block all file writes and was never
      shipped by any template.)
   3. **Verify**: after healing, confirm neither `permissions.allow` nor
      `permissions.deny` contains a remaining scoped-path `Write(<path>)`
      entry (a blanket bare `Write` or `Write(*)`→`Write` normalization
      result in `allow` is fine — only scoped-path `Write(<path>)` forms are
      the problem). If any remain, the heal step above was incomplete — fix
      before continuing.

   **Legacy cleanup (Context7 scope migration)** — heal projects configured by an older
   cenci that granted the plugin-scoped Context7 permission pair before Context7 moved
   to project scope:
   1. Remove every `permissions.allow` entry matching the `mcp__plugin_cenci_context7__*`
      prefix. Leave every other `permissions.allow` entry untouched, including other
      `mcp__*` grants — this cleanup is scoped to the Context7 prefix only, never a
      broader `mcp__plugin_*` or `mcp__*` match.
   2. If Context7 is enabled this run, ensure the project-scoped
      `mcp__context7__resolve-library-id` and `mcp__context7__query-docs` pair is present
      in `permissions.allow` — add whichever is missing, and deduplicate rather than
      appending a duplicate entry.
   3. If Context7 is declined this run, remove the pair without adding a replacement.
   4. **Verify**: after healing, confirm `permissions.allow` contains no remaining entry
      with the `mcp__plugin_cenci_context7__*` prefix, and that every non-Context7 entry
      present before this step is still present unchanged. If either check fails, the
      heal step above was incomplete or over-broad — fix before continuing.

### MCP Server Configuration

For each MCP selected in question 5:

**Project-scoped (Context7, Angular, PrimeNG):**
- Only create or modify the project's root `.mcp.json` if at least one project-scoped MCP server was selected. Never *create* an empty `.mcp.json`.
- Create or update the project's root `.mcp.json`
- Add entries from the catalog, e.g.:
  ```json
  {
    "mcpServers": {
      "context7": {
        "command": "npx",
        "args": ["-y", "@upstash/context7-mcp@3.2.5"],
        "env": { "CONTEXT7_API_KEY": "${CONTEXT7_API_KEY}" }
      },
      "angular": {
        "command": "npx",
        "args": ["-y", "@angular/cli", "mcp"]
      },
      "primeng": {
        "command": "npx",
        "args": ["-y", "@primeng/mcp"]
      }
    }
  }
  ```
- If Context7 was selected: note to user: "Set CONTEXT7_API_KEY in your shell environment (free key from context7.com/dashboard)"
- If the file already exists, merge into the existing `mcpServers` object — never overwrite existing entries, with two field-scoped exceptions:
  - **Version-pin refresh**: for a catalog server whose catalog `Args` are version-pinned (e.g. Context7), if an existing entry's `args` differ from the catalog value, overwrite **`args` only** — every other key (including `env` and any user-added keys) is preserved. This is the single explicit, documented exception to "never overwrite existing entries."
  - **Declined servers**: for each catalog server recorded `false` in `mcpServers` (question 5's answer), delete that entry from an existing `.mcp.json` if present. If `mcpServers` becomes empty as a result, leave the file in place with an empty `mcpServers` object — never delete the file. (The "never create an empty `.mcp.json`" rule above applies to *creating* a new file only, not to editing an existing one down to empty.)

5. Update `.gitignore`:
   - Add `.worktrees/` if not present
   - Add `.plans/` if not present (plan files are ephemeral, session-specific)
   - Add `.cenci/pipeline/` if not present (transient per-run `cenci pipeline` state, anchored to the main-checkout root — see `phase-2-worktree.md`'s Gate Check)
   - Add `**/.cenci/maintain-report.json` if not present (`/cenci:maintain`'s generated report; matched at any depth since it can land in any project subdir, e.g. `watch/.cenci/`)
   - Check each entry individually before adding — skip any that are already in `.gitignore`. (If a prior cenci version appended a `# Claude Code sandbox artifacts` block, leave it in place — the entries are harmless and removing them would violate the append-only rule.)
5b. **Generate `.claudeignore`**: Create or update `.claudeignore` in the project root. This file tells Claude Code to ignore files that are tracked by git but not useful as context (binary assets, lock files, generated bundles). Claude already respects `.gitignore`, so `.claudeignore` is only for tracked files.

   - If `.claudeignore` already exists, merge new entries into it — preserve user-added entries, skip duplicates.
   - If it does not exist, create it from `${CLAUDE_PLUGIN_ROOT}/templates/claudeignore` as the base.
   - Then **append** stack-specific patterns based on the tech stack from question 1:

   #### Stack-specific `.claudeignore` patterns

   | Stack trigger | Patterns to add |
   |---|---|
   | Node / npm | `package-lock.json` |
   | Yarn | `yarn.lock` |
   | pnpm | `pnpm-lock.yaml` |
   | .NET | `*.Designer.cs`, `*.g.cs`, `**/wwwroot/lib/` |
   | Python | `poetry.lock`, `Pipfile.lock` |
   | Go | `go.sum` |
   | Rust | `Cargo.lock` |
   | Angular | `.angular/` |
   | Next.js | `.next/` |

   Add patterns under a `# <stack> files` comment section. Only add sections for stacks detected in the project. Example output for an Angular + .NET project:

   ```
   # .claudeignore — Files tracked by git but not useful for Claude's context.
   # Claude already respects .gitignore, so only list tracked files here.

   # ── Binary & media assets ──
   *.png
   *.jpg
   ...

   # ── .NET generated files ──
   *.Designer.cs
   *.g.cs
   **/wwwroot/lib/

   # ── Node / Angular files ──
   package-lock.json
   .angular/
   ```

5c. **Configure auto-compact** (from question 7):
   - If disabled: set the setting in `~/.claude/settings.json`. Ensure the directory
     exists, as its own Bash call:
     ```bash
     mkdir -p ~/.claude
     ```
     If `~/.claude/settings.json` exists, update it in place with two standalone Bash
     calls (never compound with `&&` — shell-rules):
     ```bash
     jq '.autoCompactEnabled = false | del(.env.CLAUDE_AUTOCOMPACT_PCT_OVERRIDE) | if .env == {} then del(.env) else . end' ~/.claude/settings.json > ~/.claude/settings.json.tmp
     ```
     The `jq` call and the `mv` call are separate Bash calls (no pipe, no `&&`) — this
     is a single non-compound command whose result the agent inspects before proceeding.
     `>` creates `~/.claude/settings.json.tmp` even when `jq` fails, so before running
     `mv`, verify the `jq` call exited 0 and that `~/.claude/settings.json.tmp` is
     valid non-empty JSON. Only run `mv` if that check passes; otherwise stop and
     report the failure instead of proceeding — an unconditional `mv` would silently
     clobber the user's real settings file with a broken/empty one.
     ```bash
     mv ~/.claude/settings.json.tmp ~/.claude/settings.json
     ```
     If `~/.claude/settings.json` does not exist, use the `Write` tool to create
     `~/.claude/settings.json.tmp` (the same `.tmp` intermediate as the existing-file
     path above, not the final file) with `{"autoCompactEnabled": false}` as its
     content, then run the same `mv ~/.claude/settings.json.tmp ~/.claude/settings.json`
     Bash call shown above (already allowlisted in this skill's frontmatter
     `allowed-tools`, so no permission change needed) to move it into place. This
     mirrors the jq+mv two-step pattern used for the existing-file case just above —
     Write-then-mv instead of jq-then-mv, since there's no existing file for jq to
     transform — and avoids a direct Write to the live `~/.claude/settings.json`
     path, which the flow plugin's own `guard-main-worktree.sh` hook now blocks as a
     self-protection measure for hook-config paths outside the repo (#1072).
   - If enabled (re-enable): remove the setting with two standalone Bash calls (the
     file necessarily already exists on this path — it was written by the "If disabled"
     branch above on an earlier run):
     ```bash
     jq 'del(.autoCompactEnabled) | del(.env.CLAUDE_AUTOCOMPACT_PCT_OVERRIDE) | if .env == {} then del(.env) else . end' ~/.claude/settings.json > ~/.claude/settings.json.tmp
     ```
     The `jq` call and the `mv` call are separate Bash calls (no pipe, no `&&`) — this
     is a single non-compound command whose result the agent inspects before proceeding.
     `>` creates `~/.claude/settings.json.tmp` even when `jq` fails, so before running
     `mv`, verify the `jq` call exited 0 and that `~/.claude/settings.json.tmp` is
     valid non-empty JSON. Only run `mv` if that check passes; otherwise stop and
     report the failure instead of proceeding — an unconditional `mv` would silently
     clobber the user's real settings file with a broken/empty one.
     ```bash
     mv ~/.claude/settings.json.tmp ~/.claude/settings.json
     ```
   Both paths also delete any `CLAUDE_AUTOCOMPACT_PCT_OVERRIDE` env key left behind by earlier versions of this skill — that override makes compaction trigger at 1% of context *used*, i.e. constantly (#725).
   This writes to `~/.claude/settings.json` (user-level Claude Code settings).

5c-bis. **Pin subagents to 200K context** (from question 7b):
   - If enabled (pin subagents): merge the env var into `~/.claude/settings.json`.
     Ensure the directory exists, as its own Bash call:
     ```bash
     mkdir -p ~/.claude
     ```
     If `~/.claude/settings.json` exists, update it in place with two standalone Bash
     calls:
     ```bash
     jq '. * {"env": {"CLAUDE_CODE_SUBAGENT_MODEL": "claude-sonnet-5"}}' ~/.claude/settings.json > ~/.claude/settings.json.tmp
     ```
     The `jq` call and the `mv` call are separate Bash calls (no pipe, no `&&`) — this
     is a single non-compound command whose result the agent inspects before proceeding.
     `>` creates `~/.claude/settings.json.tmp` even when `jq` fails, so before running
     `mv`, verify the `jq` call exited 0 and that `~/.claude/settings.json.tmp` is
     valid non-empty JSON. Only run `mv` if that check passes; otherwise stop and
     report the failure instead of proceeding — an unconditional `mv` would silently
     clobber the user's real settings file with a broken/empty one.
     ```bash
     mv ~/.claude/settings.json.tmp ~/.claude/settings.json
     ```
     If `~/.claude/settings.json` does not exist, use the `Write` tool to create
     `~/.claude/settings.json.tmp` (the same `.tmp` intermediate as the existing-file
     path above, not the final file) with
     `{"env": {"CLAUDE_CODE_SUBAGENT_MODEL": "claude-sonnet-5"}}` as its content, then
     run the same `mv ~/.claude/settings.json.tmp ~/.claude/settings.json` Bash call
     shown above (already allowlisted in this skill's frontmatter `allowed-tools`, so
     no permission change needed) to move it into place. This mirrors the jq+mv
     two-step pattern used for the existing-file case just above — Write-then-mv
     instead of jq-then-mv, since there's no existing file for jq to transform — and
     avoids a direct Write to the live `~/.claude/settings.json` path, which the flow
     plugin's own `guard-main-worktree.sh` hook now blocks as a self-protection
     measure for hook-config paths outside the repo (#1072).
   - If disabled (unpin): remove the env var key with two standalone Bash calls:
     ```bash
     jq 'del(.env.CLAUDE_CODE_SUBAGENT_MODEL) | if .env == {} then del(.env) else . end' ~/.claude/settings.json > ~/.claude/settings.json.tmp
     ```
     The `jq` call and the `mv` call are separate Bash calls (no pipe, no `&&`) — this
     is a single non-compound command whose result the agent inspects before proceeding.
     `>` creates `~/.claude/settings.json.tmp` even when `jq` fails, so before running
     `mv`, verify the `jq` call exited 0 and that `~/.claude/settings.json.tmp` is
     valid non-empty JSON. Only run `mv` if that check passes; otherwise stop and
     report the failure instead of proceeding — an unconditional `mv` would silently
     clobber the user's real settings file with a broken/empty one.
     ```bash
     mv ~/.claude/settings.json.tmp ~/.claude/settings.json
     ```
   This writes to `~/.claude/settings.json` (user-level Claude Code settings). Takes effect on **new** sessions only — remind the user to restart if the current session is on a `[1m]` model.

5d. **Generate CI/CD pipeline** (from question 8, only if user selected Yes):

   **GitHub Actions** — write `.github/workflows/ci.yml`:

   ```yaml
   name: CI
   on:
     push:
       branches: [main]
     pull_request:
       branches: [main]
   jobs:
     ci:
       runs-on: ubuntu-latest
       steps:
         - uses: actions/checkout@v4
         # Setup + cache for detected stack
         # Install deps → Lint → Build → Test
         # Upload coverage artifact
   ```

   Compose the `steps` array based on the detected stack from question 1:

   **Node-based stacks** (Angular, React, Next.js, Vue):
   - `actions/setup-node@v4` with `node-version` from `engines.node` or `"20"`, and `cache` set to the detected package manager (npm/yarn/pnpm)
   - Install: `npm ci` (or `yarn install --frozen-lockfile` / `pnpm install --frozen-lockfile`)
   - Lint step, Build step, Test step from the stack-to-CI mapping table
   - `actions/upload-artifact@v4` for coverage output

   **.NET stacks**:
   - `actions/setup-dotnet@v4` with `dotnet-version` extracted from stack token
   - `dotnet restore`
   - Lint, Build, Test from the mapping table
   - `actions/upload-artifact@v4` for coverage output

   **Go**:
   - `actions/setup-go@v5` with `go-version-file: 'go.mod'` (enables built-in caching)
   - Lint: `golangci/golangci-lint-action@v6`
   - Build, Test from the mapping table
   - `actions/upload-artifact@v4` for coverage output

   **Python**:
   - `actions/setup-python@v5` with `python-version` from `pyproject.toml` or `"3.12"`
   - `pip install -e ".[dev]"` (or `pip install -r requirements.txt`)
   - Lint, Test from the mapping table (no build step)
   - `actions/upload-artifact@v4` for coverage output

   **Rust**:
   - `dtolnay/rust-toolchain@stable` (or version from `rust-toolchain.toml`)
   - `Swatinem/rust-cache@v2`
   - Lint, Build, Test from the mapping table
   - `actions/upload-artifact@v4` for coverage output

   **Monorepo strategies**:
   - **Same stack family** (all projects share same stack type): Use a matrix job with `working-directory` per project
   - **Mixed stacks** (projects have different stack types): Generate separate named jobs per project (e.g., `ci-api`, `ci-web-client`)
   - **Path-based trigger filters**: Add `paths` filters under `push`/`pull_request` scoped to each project's directory, so CI only runs for changed projects

   After writing the file, create the parent directory if needed (`mkdir -p .github/workflows` for GitHub Actions).

5e. **Generate `.cenci/Dockerfile`** (from question 9, only if user selected Yes):

   **`BASE_VERSION` is always `latest`** — there is no resolution step. `buildBase` (`watch/internal/sandbox/launcher/engine.go:337-349`) only ever tags the base image `cenci-sandbox-base:<12-hex content hash>` and `cenci-sandbox-base:latest`; no semver tag exists in any environment, so the ARG default can only ever be the `latest` alias. `cenci sandbox build` always overrides it at build time via `--build-arg BASE_VERSION=...` (`engine.go:372,392`), so the default is never load-bearing for that path — it only matters for a bare manual `docker build`, where `latest` is exactly the recipe `sandbox/README.md` documents. An empty default must never be written instead: Docker's `InvalidDefaultArgInFrom` lint check flags any `ARG` used in a `FROM` whose default resolves to an empty or invalid image reference, and it evaluates the file statically regardless of a build-time override — so the literal `latest` (never empty, never unresolved) is what step 5e always writes.

   **Generated file format** — always emit the ARG/FROM pair below, **never** a literal `FROM cenci-sandbox-base:<version>`. `cenci sandbox build` always passes `--build-arg BASE_VERSION=...` at build time; a literal `FROM` would silently drift from what's actually built:

   ```dockerfile
   # cenci:managed-begin
   ARG BASE_VERSION=latest
   FROM cenci-sandbox-base:${BASE_VERSION}

   SHELL ["/bin/bash", "-o", "pipefail", "-c"]

   # cenci:fragment-begin <fragment 1 name>
   <selected fragment 1 content, from sandbox/fragments/*.dockerfile>
   # cenci:fragment-end <fragment 1 name>

   # cenci:fragment-begin <fragment 2 name>
   <selected fragment 2 content>
   # cenci:fragment-end <fragment 2 name>
   ...
   # cenci:managed-end
   ```

   **Per-fragment markers**: wrap each fragment's content in a `# cenci:fragment-begin <name>` / `# cenci:fragment-end <name>` marker pair, placed immediately before and after that fragment's own content within the managed block (see the example above). `<name>` is the fragment file's basename without `.dockerfile` (e.g. `sandbox/fragments/docker.dockerfile` → `docker`). This lets `watch/internal/sandbox/launcher`'s fragment-drift detector (#1048) identify exactly which installed fragment a block of content came from; an already-generated block with no per-fragment markers still gets detected, via that detector's legacy banner-line fallback.

   **Fragment concatenation order** (when multiple fragments apply, e.g. a monorepo union): **dotnet → node → playwright → go → python → rust → docker → azure**, regardless of the order projects were discovered in. Node is mandatory; the remaining fragments are stack-selected (docker and azure are config-selected — see the mapping table's Docker and Azure rules). Concatenate the selected `sandbox/fragments/*.dockerfile` file contents in that fixed order, each wrapped in its own per-fragment marker pair, applying the **.NET version substitution** from the mapping table above to the dotnet fragment only — every other fragment is included verbatim. Deduplicate — each fragment appears at most once even when multiple monorepo projects map to the same fragment.

   **Merge-safe regeneration**: the whole block above (from `# cenci:managed-begin` through `# cenci:managed-end` inclusive) is the managed block.
   - **File doesn't exist**: create `.cenci/` (`mkdir -p .cenci`) and write the managed block as the full file content.
   - **File exists with both markers present**: replace only the text from `# cenci:managed-begin` through `# cenci:managed-end` (inclusive) with the freshly generated block. Preserve everything before the begin marker and everything after the end marker exactly as-is — this is where a team can hand-append their own `RUN` steps across re-runs.
   - **File exists with no markers** (e.g. a hand-authored legacy `.cenci/Dockerfile`): do not silently overwrite it. Reuse the exact Overwrite/Skip/Show conflict-check UX already used for CI/CD generation (question 8 / step 5d) — same three options, same behavior:
     "Found existing `.cenci/Dockerfile` without cenci's managed markers. What would you like to do?"
     Options: "Overwrite — wrap it in managed markers and replace with the generated block", "Skip — keep the existing file, still record `sandbox` in config.json", "Show existing — display the current file contents"
     - If Skip: still record `sandbox` in config.json, don't write the file.
     - If Show existing: read and display the file, then re-ask Overwrite/Skip.
   - **File exists with malformed markers** (exactly one of `# cenci:managed-begin` / `# cenci:managed-end` present, markers out of order, or duplicate marker pairs): do **not** attempt a partial text replace — a malformed marker pair cannot be trusted to safely bound the managed block. Route this through the exact same Overwrite/Skip/Show conflict-check UX as the "no markers" case above — same prompt text, same three options, same behavior.

   **Monorepo**: fragments are the mandatory Node runtime fragment plus the deduplicated union described in the Stack-to-fragment mapping table under question 9, concatenated in the dotnet → node → playwright → go → python → rust → docker → azure order above — one `.cenci/Dockerfile` for the whole repo, not one per project.

   **Committed, not ignored**: `.cenci/Dockerfile` is committed to the repo. Do **not** add `.cenci/` or `.cenci/Dockerfile` to `.gitignore` — the whole point is a team-shared, reviewed Dockerfile that the launcher's per-repo image selection (see `sandbox/README.md`) builds identically for every teammate.

5f. **Generate `.lazyboards.yml`** (when question 10 was asked and answered Yes
   in this session — the no-existing-file path). When a file already existed, the *Board
   Config* branch instead runs the **Existing config: suggest or skip** sub-step at
   the end of this section; the generation format below is what both paths write:

   Write `.lazyboards.yml` at the repo root with the confirmed key mapping. Two
   lazyboards behaviors to honor:

   - A local `columns:` list **replaces** the global column list entirely — it
     **never merges**. Because the generated file must stand alone, it never relies
     on inheritance from a global config cenci no longer creates: every column the
     board should show is declared here. `Implemented` is dropped from the generated
     file entirely — it is a label in the ticket lifecycle, not a board column.
   - **Every key binding goes in the `keymaps:` namespace.** Per-column bindings
     live under `keymaps.columns.<name>` (matched case-insensitively); board-level
     bindings go in **both** `keymaps.normal` and `keymaps.detail`, since
     `keymaps.normal` alone would silently kill them while the detail panel is
     focused. `columns:` itself is the board layout — a bare name list.

   ```yaml
   # Generated by /cenci:configure — per-repo lazyboards board config. This file
   # is self-contained and needs no other config: a local `columns:` list REPLACES
   # the global column list entirely — it never merges — and every key binding
   # below lives in the `keymaps:` namespace.
   columns:
     - name: New
     - name: Refined
     - name: Planned
     - name: In Review

   keymaps:
     # Board-level agent launchers. Emitted in BOTH tables so they fire whether the
     # card list or the detail panel is focused. `window:` opens a tmux window and
     # `focus: true` switches to it; lazyboards builds and escapes the tmux call.
     normal:
       C: { name: Claude, type: shell, window: "claude", focus: true, command: "cenci open --agent claude" }
       X: { name: Codex, type: shell, window: "codex", focus: true, command: "cenci open --agent codex" }
     detail:
       C: { name: Claude, type: shell, window: "claude", focus: true, command: "cenci open --agent claude" }
       X: { name: Codex, type: shell, window: "codex", focus: true, command: "cenci open --agent codex" }

     # Per-column overlays — these apply to normal + detail only, matched
     # case-insensitively against the column names declared above.
     columns:
       New:
         R:
           name: Refine
           type: shell
           command: "cenci run refine {number}"

       Refined:
         I:
           name: Implement
           type: shell
           command: "cenci run implement {number}"

       Planned:
         I:
           name: Implement
           type: shell
           command: "cenci run implement {number}"
         E:
           name: Edit plan
           type: shell
           terminal: true
           command: 'f=$(ls .plans/{number}-*.md 2>/dev/null | head -1); [ -n "$f" ] && ${EDITOR:-vi} "$f"'
         V:
           name: View plan
           type: shell
           terminal: true
           command: 'f=$(ls .plans/{number}-*.md 2>/dev/null | head -1); [ -n "$f" ] && ${PAGER:-less} "$f"'

       "In Review":
         W:
           name: Open worktree
           type: shell
           scope: pr
           window: "pr-{pr_number}"
           cwd: "{pr_worktree}"
         "S w":
           name: Serve web-client worktree
           type: shell
           scope: pr
           window: "pr-{pr_number}"
           cwd: "{pr_worktree}/apps/web-client"
           command: "ng serve"
         "T w":
           name: Test web-client worktree
           type: shell
           scope: pr
           terminal: true
           cwd: "{pr_worktree}/apps/web-client"
           command: "ng test --watch=false"

   # Auto-close a card's agent window when its ticket closes. `cleanup` stays a
   # top-level scalar — it is not a key binding and has no place in `keymaps:`.
   cleanup: "cenci close {number}"
   ```

   - **`W` (Open worktree) is always emitted on `In Review`, for every repo, whether
     or not any project is runnable or testable.** It opens the PR's registered
     worktree in a tmux window with a plain shell and runs no command — it never
     carries a project path or a serve/test command, even in a monorepo. `W` is
     never reused for serve, test, or any other action. `command:` is omitted
     deliberately: on an action that sets `window:`, lazyboards treats "open a
     window on this directory" as complete and runs the default shell there.
   - `Planned` gets a local `I` (Implement) action too, so a ticket that already
     passed planning can still be manually re-dispatched straight from the board, plus
     local `E` (Edit plan, opens in `${EDITOR:-vi}`) and `V` (View plan, opens in
     `${PAGER:-less}`) actions on the ticket's persisted plan file. Both carry
     `terminal: true`, so the editor/pager gets lazyboards' own terminal and the
     board returns when it exits — the same shape lazyboards' built-in `e` (edit
     card) uses, and one that needs no multiplexer. Plan files are
     `.plans/<number>-<slug>.md`; the slug isn't derivable from the number, so both
     actions glob `.plans/{number}-*.md` (the same resolution the implement skill
     uses) and no-op when no plan file is present (e.g. already consumed in Phase 9).
     `{number}` is a validated integer, safe to interpolate.
   - `Implemented` is **never** re-emitted as a generated column in
     `.lazyboards.yml` — only `New`, `Refined`, `Planned`, and `In Review` appear.
   - `C` and `X` are board-level Claude/Codex launch actions, emitted under
     **`keymaps.normal` and `keymaps.detail`** — never under
     `keymaps.columns.<name>` (they are board-level, not per-column). lazyboards
     merges `keymaps:` tables and scalar fields across a global and a local config
     file, with **local keys winning** (and the merged user config always winning
     over the built-in defaults), so the generated file is self-contained and a
     stray `~/.config/lazyboards/config.yml` cannot conflict with it. `cleanup` is
     a top-level scalar for the same reason: it is always emitted here, outside
     `keymaps:`; delete the line to opt out.
   - One `In Review` **serve** action per runnable project, using the confirmed key
     (`S` alone for a single runnable project, or the `S` + mnemonic sequence —
     `"S b"`, `"S f"`, … — for multiple, per the Key assignment rules above) and
     serve command; action name `Serve <slug> worktree`. One `In Review` **test**
     action per testable project, using the confirmed test key (`T` alone, or the
     `T` + mnemonic sequence for multiple) and test command; action name
     `Test <slug> worktree`. Sequence keys are written in canonical
     **space-separated** form and quoted (`"S w"`), never concatenated (`Sw`).
   - **Never hand-write a `tmux new-window` invocation.** lazyboards assembles it
     from four `type: shell` fields and escapes the window name, the working
     directory, and the command as single shell tokens, so a worktree path or
     project subpath containing a space, a quote, `;`, or `$(…)` cannot break out
     of the command line:

     | Field | Meaning |
     |-------|---------|
     | `window:` | Window name. Its presence is what makes the action open a window. Template-expanded. |
     | `cwd:` | Working directory. Template-expanded. Applies to **every** shell action — windowed, `terminal: true`, and plain buffered alike. |
     | `focus:` | `true` switches to the new window; omitted leaves it detached (what the old `-d` flag did). |
     | `terminal: true` | Hands the command lazyboards' own terminal: full output and input, board restored on exit. |

     All four are modifiers on `type: shell` and are a **load-time config error**
     on a `type: url` action, as are the two contradictory combinations:
     `window:` together with `terminal:`, and `focus:` without a `window:`.
   - **Pick the run mode by what the command is**, never by how fast it is:
     a **serve** action keeps running alongside the board, so it takes
     `window: "pr-{pr_number}"` (detached, no `focus:`); a **test** action is
     watched to completion and then hands the board back, so it takes
     `terminal: true`. `W` takes `window:` with no `command:`. All three set
     `cwd:` — only the key, the run mode, and the command differ.
   - **The project path is a plain `cwd:` segment, in a monorepo too.**
     **Single project**: `cwd: "{pr_worktree}"`. **Monorepo**: append the project
     path directly — `cwd: "{pr_worktree}/apps/web-client"`. No nested POSIX
     quoting, no `'\''` escaping, and never a `cd <path> && ` prefix in the
     command: `cwd:` is expanded and then escaped as one token, so quoting it by
     hand would double-escape it.
   - `{pr_worktree}` resolves the PR branch's registered Git worktree at action
     time, so the file stays machine-independent — never embed absolute paths.
     `{number}` (used in `command: "cenci run refine {number}"` /
     `implement {number}`) is a validated GitHub issue/PR
     integer, not free text, so it is safe to interpolate without additional
     escaping. `window:` and `cwd:` are template-expanded like `url:`/`command:`,
     so they count for scope inference and the scope variable restrictions too — a
     `{pr_*}` placeholder in either one requires `scope: pr` on that action, and a
     board-scope action may not reference one at all.
   - A `window:` action needs a tmux session: outside tmux lazyboards reports
     `Not inside tmux` in the status bar instead of running anything. A
     `terminal: true` action has no such dependency and works over a plain SSH
     session — which is why the `E`/`V` plan actions above use it.
   - **Zero runnable projects**: `W` (Open worktree) is emitted regardless — it
     doesn't depend on any project being runnable or testable. If no project in the
     repo has a detected serve or test command, `In Review` still carries just `W`:
     ```yaml
     keymaps:
       columns:
         "In Review":
           W:
             name: Open worktree
             type: shell
             scope: pr
             window: "pr-{pr_number}"
             cwd: "{pr_worktree}"
     ```
   - **Trust (run after writing the file).** A repo-local `.lazyboards.yml` is
     attacker-controlled, so lazyboards silently strips every `type: shell` binding
     **and** the `cleanup:` line until the file's exact content is trusted — and the
     generated file is entirely shell actions plus `cleanup`, so it is completely
     inert until then. After the write, ask via `AskUserQuestion`: "Run `lazyboards
     trust` now so the generated shell actions are honored?" Options: "Yes — run
     `lazyboards trust` (Recommended)", "No — I'll run it myself". On Yes, run it as
     its **own** Bash call from the repo root:
     ```bash
     lazyboards trust
     ```
     **Either way, always print the caveat**: trust is keyed to the file's exact
     content, not its path, so it must be re-granted after the configure PR merges
     if review changed a single byte, and again after any later regeneration of the
     file. A teammate cloning the repo has to run `lazyboards trust` once themselves.
     (Running `lazyboards trust` inside the worktree trusts the worktree copy's
     content; the same content at the repo root is trusted too, since the trust store
     is keyed by content hash, not path.)
   - **Existing config: suggest or skip** (the branch taken from *Board Config*
     above when `.lazyboards.yml` already exists — question 10 is **not** asked and
     the file is **not** blindly overwritten). This file-exists conflict check fires
     **unconditionally** whenever `.lazyboards.yml` already exists at the repo root,
     regardless of any prior `lazyboards.enabled` state recorded in
     `.cenci/config.json` — a stale or missing flag never causes this branch to be
     skipped, since the check is driven by the file's presence on disk, not the
     recorded flag:
     1. Read the existing file and derive the **recommended action set** this repo
        would generate above: Refine/Implement on `New`/`Refined`/`Planned`,
        Edit-plan (`E`) and View-plan (`V`) actions on `Planned`, an unconditional `W` (Open worktree) on `In Review`, and
        per runnable/testable project a serve (`S`/`"S b"`/`"S f"`/…) and test
        (`T`/`"T b"`/`"T f"`/…) In Review action. Outside the per-column tables it also includes the board-level `C`/`X` launch actions and `cleanup: "cenci close {number}"`.
     2. Compute the **delta** = recommended actions absent from the existing file,
        read from its `keymaps.normal`/`keymaps.detail`/`keymaps.columns.<name>`
        tables. A concatenated sequence key (`Sw`) and its canonical form (`"S w"`)
        are the same key, not two.
        Match by column + action intent (name/command) — or, for the column-less
        board-level `C`/`X`/`cleanup` actions, by intent alone — **not** by raw key,
        so a user's custom key binding is respected rather than flagged as
        "missing". Before assigning a key to any delta action, apply the
        prefix constraint from the key-assignment step above: if the resolved
        namespace already binds a standalone key (built-in default, or user-added
        such as a custom `S: Sync` board-level action) that would prefix-collide
        with the proposed `S`/`T` key, pick a different leading letter for that
        action instead.
        - **Hand-written tmux (any action, add or carry-over)**: an existing
          action whose `command:` starts with `tmux new-window` matches by intent
          — it is not "missing" — but counts toward the delta as an **update** to
          the `window:`/`cwd:`/`focus:` form, since the hand-written invocation
          puts the escaping of the worktree path and window name on the config
          file. Translate it: `-n <name>` → `window:`, `-c <dir>` → `cwd:`
          (dropping any nested `'…'` quoting and any `cd <dir> && ` prefix in the
          command), absence of `-d` → `focus: true`, and the remaining shell
          command → `command:`. Anything the four fields cannot express (a split,
          an existing window, `send-keys`, shell logic wrapped around the command)
          stays a plain `command:` and is **not** flagged. These two bullets are
          the only command-content comparisons in the delta; every other action is
          matched by intent alone, never diff-compared.
     3. **Delta non-empty** → present the concrete additions via `AskUserQuestion`,
        e.g. "`.lazyboards.yml` is missing a PR-worktree test action: `T` → run tests
        (`dotnet test`) in the PR worktree. Add it?" — or, when a leading letter had
        to be substituted for the reason above, surface it explicitly, e.g.
        "`.lazyboards.yml`'s custom `S` (Sync) action would block `"S w"` (serve
        watch) — proposing `"R w"` instead. Add it?" Options: "Apply suggested
        additions (Recommended)", "Overwrite fully — regenerate from scratch", "Keep
        as-is — no changes", "Show existing — display the current file". **Apply** and
        **Overwrite** both rewrite the whole file — a local `columns:` list *replaces*
        the global list (it never merges, so a partial in-place patch is impossible):
        merge the user's existing custom actions with the missing recommended ones,
        including the board-level `C`/`X` bindings and the `cleanup:` scalar, and
        carry the existing top-level `provider:`, `repo:`, and `project:` identity
        lines (if present) through unchanged — they are project-identity keys
        lazyboards only reads from the local file. **Keep as-is** leaves the file
        untouched. **Both rewrite paths always emit `keymaps:` form** — including
        for the user's own custom actions carried over, whose concatenated sequence
        keys (`Rw`) are rewritten space-separated (`"R w"`) and whose translatable
        hand-written `tmux new-window` commands are rewritten into
        `window:`/`cwd:`/`focus:` per the delta rule above.
     4. **Delta empty** → do **not** prompt. Emit a small log line
        (`.lazyboards.yml already covers all recommended actions — no changes.`) and
        move on.

     In every case above, record `lazyboards.enabled: true` in config.json, since a
     working board config exists. Whenever this branch **rewrote** the file (case 3),
     run the trust sub-step above as well — a rewrite changes the file's bytes, so
     any trust previously granted for it is void.
   - **Committed, not ignored**: `.lazyboards.yml` is committed (same reasoning as
     `.cenci/Dockerfile` — team-shared and reviewed; `{pr_worktree}` keeps it
     portable). Do **not** add it to `.gitignore`.

6. **Write `.cenci/config.json`** with their choices using **merge semantics**:

   - If `existingConfig` is not null: start from the existing object, overwrite each field with the user's answers. This preserves fields the skill doesn't manage.
   - If `existingConfig` is null: create the file fresh.

   **Autonomy Settings wiring.** `planningAnswer`/`automergeAnswer` are overlaid onto
   `merge-sandbox-config.sh`'s stdout before the write: `planningAnswer` contributes a
   `planning: { "autonomy": "lean" }` key only when question 13 above was asked and
   answered `lean`, and `automergeAnswer` contributes the scaffolded `automerge` key only
   when question 14 above was asked and answered "Scaffold a starter block for hand
   review" — a declined answer contributes no key. When either question was skipped
   because its key was already present in `existingConfig`, there is no collected answer
   to overlay — the existing value simply survives the merge semantics above untouched.
   After overlaying `planningAnswer`/`automergeAnswer` onto the merge script's stdout,
   validate the resulting JSON is well-formed (`jq empty`) before writing it — the same
   fail-closed discipline as the adjacent `sandbox` merge above: if the overlaid result
   is not valid JSON, do not write it, report the failure, and fall back to the
   pre-overlay config content (the merge script's stdout as-is).

   **Always stamp `configVersion`** on every write (fresh or re-config): set it to `detection.pluginVersion`. If Scripted Detection was unavailable, read `.version` from `${CLAUDE_PLUGIN_ROOT}/.claude-plugin/plugin.json` with jq, verifying the command succeeded before using its output. If neither resolves, preserve any existing `configVersion` unchanged and tell the user the stamp could not be refreshed — never invent a version.

```json
{
  "configVersion": "0.22.0",
  "branchPattern": "feature/<id>-<description>",
  "stack": {
    "backend": "dotnet10",
    "frontend": "angular21",
    "testing": ["xunit", "jasmine"]
  },
  "guidanceLocation": "AGENTS.md",
  "mcpServers": {
    "context7": true,
    "angular": false,
    "primeng": false
  },
  "lspServers": {
    "typescript": true,
    "csharp-ls": true
  },
  "autoCompactDisabled": true,
  "pinSubagents200K": true,
  "cenci": {
    "compactImplementation": false,
    "reviewConcurrency": "parallel",
    "implementerConcurrency": "parallel",
    "diffContextMode": "inline",
    "liteReviewEnabled": true,
    "planComment": false,
    "gateOutputLines": 120
  },
  "planning": { "autonomy": "interactive" },
  "cicd": {
    "enabled": true,
    "platform": "github-actions"
  },
  "sandbox": {
    "enabled": true,
    "dind": true,
    "azure": true
  },
  "lazyboards": {
    "enabled": true,
    "serveCommand": "ng serve",
    "boardKey": "S"
  }
}
```

(The `planning` value shown above is illustrative of the schema, not something this skill
writes by default: question 13 (`### Autonomy Settings`) writes the `planning` key only when
you explicitly choose `lean`, or when it was already present in `existingConfig`; declining —
keeping `interactive` — writes nothing, since a missing key already resolves to `interactive`.)

`configVersion` records the flow plugin version that last wrote this config (managed by this skill — always overwritten with the current plugin version in step 6, never a question). Consumers:
- the plugin's SessionStart hook (`hooks/scripts/check-config-staleness.sh`) — nudges the user at session start when the stamp's major.minor is behind the installed plugin (or missing entirely), so they learn a `/cenci:configure` re-run would pick up new configure features without watching the changelog;
- maintain's `config-version` check (`/cenci:maintain`, via the same staleness resolver) — reports the same staleness as an advisory `warn`.

Patch-only drift is deliberately silent: configure features that warrant a re-run land in minor (`feat`) or major bumps per the plugin-version-bump workflow. Do **not** add `configVersion` to the migration-removal list below — it is a managed field, not a legacy one.

The `cenci` field is optional. If present, preserve existing user values during reconfiguration. Schema:
- `compactImplementation` — `true` allows small, low-risk tickets to combine red/green/refactor into one implementer subagent turn while preserving all TDD/reporting gates. Default: `false`.
- `reviewConcurrency` — `"parallel"` runs security, code, and silent-failure reviews together; `"sequential"` runs the same reviews one after another to smooth usage limits. Default: `"parallel"`.
- `implementerConcurrency` — `"parallel"` (default) runs planner-declared `### Parallel Lanes` implementers concurrently during implement Phase 3; `"sequential"` runs the same lanes one after another to smooth usage limits. Quality gates identical either way; the setting never creates lanes on its own — plans without a lanes section always run the standard sequential flow.
- `diffContextMode` — `"inline"` passes small diffs directly to reviewers; `"file"` writes the diff to this implement run's artifact directory (`$RUN_DIR/diff.patch` — see implement Phase 6 + 7) and passes paths so reviewers read targeted hunks. Default: `"inline"`.
- `liteReviewEnabled` — `true` (default) lets Phase 6 + 7 classify each diff into `full` (all three reviewers), `lite-docs` (no reviewers, docs-only), or `lite-small` (`code-reviewer` only, small config/data-only diffs); `false` forces the full trio on every run regardless of diff size or content. See Phase 6 + 7 for the precedence-ordered classification rules.
- `planComment` — `true` makes implement Phase 1 also post the saved plan as a ticket comment (ticket mode only) right before marking the ticket `Planned` (the label call stays the last ticket edit — it records the plan-freshness baseline), for audit / off-host visibility; `.plans/` stays the executable source of truth. Default: `false` (no comment).
- `gateOutputLines` — the number of trailing lines of a gate command's combined stdout+stderr that `hooks/scripts/run-gate.sh` prints (see `docs/health-gates.md`); the full untruncated output stays retrievable at `GATE_LOG` on a red gate. Default: `120`.

Configure always writes `sandbox: { "enabled": false }` in `.claude/settings.json` (no `network`/`excludedCommands`/`autoAllowBashIfSandboxed`) — the cenci-sandbox container is the security boundary. The config no longer carries `profile` or `sandboxEnabled` fields; re-config strips them from older configs (see the migration-removal list below).

Optional external usage reducer: RTK (`https://github.com/rtk-ai/rtk`) can compress shell command output before it reaches Claude Code. It is not required for cenci and should not be installed automatically, but it is worth recommending when users are hitting usage limits from command-heavy sessions. After separate installation, `rtk init -g` enables Claude Code Bash command rewriting where supported. Built-in tools like `Read`, `Grep`, and `Glob` do not pass through RTK hooks.

The `cicd` field is only present when the user selected Yes in question 8. Schema:
- `cicd.enabled` — `true` if user opted in, omit `cicd` entirely if declined
- `cicd.platform` — `"github-actions"`

Omit `cicd` entirely when the user says No.

The `sandbox` field carries three **independently toggled** sub-answers — question 9 (Sandbox Dockerfile), question 9b (Nested Docker/dind) and question 9c (Azure CLI) — that do not gate each other. Its merge into `existingConfig` (or a fresh config) is delegated to a shared, deterministic script rather than hand-merged, so Claude Code and Codex configure runs produce byte-equivalent `sandbox` JSON for equivalent answers — "prose presence alone is not evidence that generated JSON is correct" (#632):

```bash
bash "${CLAUDE_PLUGIN_ROOT}/skills/configure/scripts/merge-sandbox-config.sh" <path to existingConfig, or "-" for stdin> \
  --dockerfile <true|false, from question 9> \
  --dind <true|false, from question 9b> \
  --azure <true|false, from question 9c>
```

Run it as its own Bash call (per `cenci:shell-rules`). If `existingConfig` is null (first-ever configure run), pass `-` as the config argument and pipe `{}` in as stdin. The script prints the **full merged config** (not just the `sandbox` object) to stdout — treat that stdout as the new full config content going into step 6's write (after also stamping `configVersion` per above).

`scripts/merge-sandbox-config.sh` (tested by its own `scripts/merge-sandbox-config.test.sh`) is the source of truth for the merge; the schema and outcomes below document its contract, not a procedure to hand-execute. On any non-zero exit from the script, do not use its (possibly empty) stdout as the new config content — read stderr for the cause. The script fails closed (exit 2) for several distinct reasons: `jq` missing, an unreadable existing config, invalid existing JSON, a missing/invalid `--dockerfile`/`--dind`/`--azure` value, or an unknown argument. Every boolean flag is **required** — an omitted one would default to false and silently delete an existing opt-in, so the script refuses instead. If `jq` is genuinely unavailable, fall back to this manual procedure; for any other validation failure, fix the inputs (e.g. re-check the existing config's readability/JSON validity, the resolved flag values) and retry the script rather than falling back:
- `sandbox.enabled` — `true` if the user opted in to question 9; omit the key entirely if declined (same pattern as `cicd` — never write `enabled: false`). The script also deletes a legacy `sandbox.baseVersion` it finds on the existing config — that key is retired (see step 5e above).
- `sandbox.dind` — `true` if the user opted in to question 9b; omit the key entirely if declined (never write `dind: false`)
- `sandbox.azure` — `true` if the user opted in to question 9c; omit the key entirely if declined (never write `azure: false`). Read by `/cenci:configure` (to select `sandbox/fragments/azure.dockerfile`) **and** at launch by `cenci open`/`cenci audit` (`RepoAzureConfig` in `watch/internal/sandbox/launcher/azure.go`), which stage the host's `~/.azure` auth files read-only only for repos that set it

Because the answers are independent, `sandbox` is written whenever **any** of them is Yes:
- Q9=Yes, 9b=No, 9c=No → `"sandbox": { "enabled": true }` (no `dind`/`azure` keys)
- Q9=No, 9b=Yes, 9c=No → `"sandbox": { "dind": true }` (no `enabled`/`azure` keys)
- Q9=No, 9b=No, 9c=Yes → `"sandbox": { "azure": true }` (no `enabled`/`dind` keys)
- Q9=Yes, 9b=Yes, 9c=Yes → `"sandbox": { "enabled": true, "dind": true, "azure": true }`
- All No → omit `sandbox` entirely (same pattern as `cicd`)

On re-configuration, merge into any existing `sandbox` object rather than replacing it wholesale — this preserves the sibling keys when only one answer changes (e.g. a dind-only re-config that answers 9b=No must drop only `dind` and retain an already-enabled `sandbox.enabled`/`azure`, and so on for each sibling).

> **Not the same as `.claude/settings.json`'s `sandbox.enabled`.** Step 4 above always writes `"sandbox": { "enabled": false }` into `.claude/settings.json` — that key disables **Claude Code's own host sandbox**, because the cenci-sandbox container is the security boundary instead. This `.cenci/config.json` `sandbox` field is unrelated: it's this ticket's per-repo `.cenci/Dockerfile` toggle, consumed by cenci's configure skill and by `cenci sandbox build`'s per-repo image build — not by Claude Code itself. Same field name (`sandbox.enabled`), two different files, two different consumers, two unrelated meanings. Do not conflate them when reading or writing either file.

The `lazyboards` field is present when question 10 was answered Yes **or** a
`.lazyboards.yml` already existed (the suggest-or-skip branch also records
`enabled: true`). Schema:
- `lazyboards.enabled` — `true` if a board config exists (generated or pre-existing); omit `lazyboards` entirely when the user declines question 10 and no file exists (same pattern as `cicd`/`sandbox`)
- **Single project**: `lazyboards.serveCommand` + `lazyboards.boardKey` record the generated serve action, and `lazyboards.testCommand` + `lazyboards.testKey` record the generated test action (command and its key — a single letter, or a multi-key mnemonic sequence like `"S b"`/`"T f"` in a monorepo). Omit the test pair when the project is not testable. `W` (Open worktree) is never recorded here — it carries no command and isn't project-specific.
- `boardKey`/`testKey` are written in lazyboards' **canonical space-separated** sequence form (`"S b"`, `"T f"`) — the same spelling the generated `.lazyboards.yml` uses. A concatenated value read from `existingConfig` (`"Sb"`, `"Tf"`) is the **same key**, not a different one: normalize it to the space-separated form on write rather than treating it as a distinct binding or as a key collision. A single-letter key (`"S"`, `"T"`) is already canonical and is written unchanged.
- **Monorepo**: `serveCommand`/`boardKey` and `testCommand`/`testKey` live on each project entry in the `projects` array instead (a project gets the serve pair only when runnable and the test pair only when testable), and the top-level `lazyboards` field carries only `enabled`
- These recorded values are advisory: the suggest-or-skip analyzer re-derives serve/test commands from the derivation tables above, so a config missing them still works.

Omit `lazyboards` entirely when the user says No (same pattern as `cicd`/`sandbox`).

The `security` field is optional and is **never written by a configure prompt** — there is
no question for it. It is a manually-editable escape hatch that lets a project extend
implement's Trivial-Ticket Triage sensitive-path backstop (see `skills/implement/SKILL.md`,
"Sensitive-path backstop"). Schema:
- `security.sensitivePaths` — an array of glob-pattern strings. Each pattern is matched
  whole-path / substring-style (`*` matches any characters including `/`, case-insensitive)
  against the file path(s) a trivial-candidate ticket names; a match disqualifies the ticket
  from the trivial fast path and forces full planning.

These entries are **additive to** implement's built-in default pattern list (`*auth*`,
`*payment*`, `*billing*`, `*migrat*`, `*secret*`, `*credential*`, `*oauth*`, `*token*`, and
more) — they extend it and never replace it, so the defaults apply even when `security` is
absent. Add patterns here only to cover project-specific sensitive areas the defaults miss
(e.g. a domain-specific module name).

Because the config write below uses merge semantics (step 6 — start from `existingConfig` and
overwrite only the fields the skill manages), a hand-added `security` block is **preserved
untouched** across re-configuration. Do **not** add `security` to the migration-removal list
below — it is a supported optional field, not a legacy one.

The `planning` field is optional. `### Autonomy Settings` question 13 above asks for it only
when absent, defaulting to `interactive`; when the key is already present, this skill reports
it verbatim and never re-prompts, narrows, or removes it — merge semantics (step 6) preserve a
hand-added or previously-written value untouched across reconfiguration either way. It is a
safety/checkpoint toggle read by the implement skill's Phase 1 (see `skills/implement/SKILL.md`
and `skills/implement/phases/phase-1-plan.md`'s `## Lean Approval Path`). Schema:
- `planning.autonomy` — `"lean"` or `"interactive"`, default `"interactive"`. Only the exact
  string `"lean"` changes behavior — a missing `planning` block, a missing `autonomy` key, or
  any other value all resolve to `"interactive"` (today's behavior: the planner asks up to 6
  clarifying questions via `AskUserQuestion` and never self-answers). `"lean"` activates
  `agents/planner.md`'s `## Self-Answer Policy`: the planner self-resolves everything except
  its five named escalation classes, and a plan persisted with no escalations is implicitly
  approved and continues straight into Phase 2 in the same session.

  `planning.autonomy` has a second consumer besides `skills/implement/phases/phase-1-plan.md`:
  `cenci dispatch`'s pickup gate (`watch/internal/dispatch/autonomy.go`) reads this same
  `.cenci/config.json` field to authorize an unattended planning pickup or autonomous
  re-plan (`dispatch.planRefined: true`) — only the exact string `"lean"` authorizes
  either consumer; both default-deny identically on a missing block, missing key, or any
  other value. Unlike the implement-side consumer above (which reads the local working
  tree), the dispatch-side consumer reads this field from the remote-confirmed
  `refs/remotes/origin/main` object, never local `HEAD` or the working tree, and only
  when that pass's `git fetch origin` actually succeeded (#877) — a committed-but-unpushed
  `planning` block on local `main` can never authorize unattended planning, and a fetch
  failure holds the gate with a distinct retryable reason rather than falling back to
  stale local state. See [`watch/README.md`'s Planning pickup and autonomous
  re-plan](../../../watch/README.md#planning-pickup-and-autonomous-re-plan) for the
  dispatch-side gate.

Because the config write below uses merge semantics, a hand-added `planning` block is
**preserved untouched** across re-configuration, exactly like `security`. Do **not** add
`planning` to the migration-removal list below — it is a supported optional field, not a
legacy one.

**Monorepo config** — when `isMonorepo` is true, add `isMonorepo` and `projects` fields:

```json
{
  "configVersion": "0.22.0",
  "isMonorepo": true,
  "projects": [
    {
      "slug": "api",
      "path": "packages/api",
      "name": "API",
      "description": "REST API backend",
      "stack": { "framework": "dotnet10", "testing": "xunit" },
      "buildCommand": "dotnet build",
      "testCommand": "dotnet test",
      "lintCommand": "dotnet format --verify-no-changes",
      "gateCommand": "dotnet build && dotnet test",
      "serveCommand": "dotnet run",
      "boardKey": "S b",
      "testKey": "T b"
    },
    {
      "slug": "web-client",
      "path": "apps/web-client",
      "name": "Web Client",
      "description": "Angular frontend",
      "stack": { "framework": "angular21", "testing": "jasmine" },
      "buildCommand": "npm run build",
      "testCommand": "npm test",
      "lintCommand": "ng lint",
      "gateCommand": "npm run build && npm test -- --watch=false",
      "serveCommand": "ng serve",
      "boardKey": "S f",
      "testKey": "T f"
    }
  ],
  "lazyboards": {
    "enabled": true
  },
  "autoCompactDisabled": true,
  "pinSubagents200K": true,
  "cicd": {
    "enabled": true,
    "platform": "github-actions"
  },
  "sandbox": {
    "enabled": true
  }
}
```

Each project entry's `lintCommand` is optional — it is omitted for stacks with no Lint row in the Stack-to-CI mapping table (e.g. `markdown-shell`, `docker-shell`), the same way `buildCommand`/`testCommand` are already handled for stacks without one.

Each project entry's `gateCommand` is optional — unlike `lintCommand`, its presence isn't tied to the Stack-to-CI mapping table; it may simply be omitted for any project. Like the other `<verb>Command` fields, its value is executed as a shell command, so it must come only from trusted project configuration, never from untrusted input.

`babysitInterval` is an optional field — there is **no configure question for it**; it is a manually-editable escape hatch, like `security` above, and merge semantics (step 6) preserve a hand-added value untouched across reconfiguration. It sets the polling cadence for the `cenci babysit` supervisor that implement Phase 9 auto-launches (and that the standalone `babysit` skill uses), resolved the same way as `gateCommand` — a top-level `babysitInterval` for a single-project repo, or a per-`projects[]` `babysitInterval` in a monorepo. Its value is a Go duration string (e.g. `"15m"`, `"30m"`, `"1h"`); when unset (or when no config file exists) `cenci babysit` falls back to its built-in `15m` default. Both forms are valid:

```json
{ "babysitInterval": "20m" }
```

```json
{ "isMonorepo": true, "projects": [ { "slug": "api", "path": "packages/api", "babysitInterval": "5m" } ] }
```

Existing single-project configs (no `isMonorepo` field) work unchanged.

The `automerge` field is optional. `### Autonomy Settings` question 14 above offers to
scaffold a conservative starter block only when absent (top-level or per-`projects[]`);
when a block is already present, this skill reports it verbatim and never re-prompts,
narrows, or removes it — merge semantics (step 6) preserve a hand-added or
previously-scaffolded value untouched across reconfiguration either way. Do **not** add
`automerge` to the migration-removal list below — it is a supported optional field, not a
legacy one.

`automerge` is split across two config locations, each with a distinct scope and default:

- `automerge.enabled` — the fleet-wide kill switch, read from `~/.config/cenci/config.json`
  (or `$XDG_CONFIG_HOME/cenci/config.json`), **not** `.cenci/config.json`. Default `false`;
  the `cenci babysit` supervisor never evaluates automerge for any repo until this is
  explicitly set `true`.
- A per-repo `automerge` block in this repo's `.cenci/config.json` — top-level for a
  single-project repo, or per-`projects[]` entry in a monorepo (falling back to the
  top-level block when a project sets none). Schema:
  - `automerge.protectedPaths` — an array of glob-pattern strings (`*` matches any
    characters including `/`, case-insensitive, same as `security.sensitivePaths`).
    Unlike `security.sensitivePaths`, each pattern here is anchored against the
    **whole repo-relative path from the root** (not substring-matched), and a pattern
    ending in `/` with no trailing `*` matches that directory and everything under it
    — see `docs/autonomous-loop.md`. A changed file matching any pattern denies
    automerge for that PR. Absent means an empty denylist — a genuine "nothing is
    protected" statement, not a malformed block.
  - `automerge.maxChangedFiles` — required whenever an `automerge` block is present; a
    missing or non-positive value makes the whole block malformed (denied), it does **not**
    fall back to a built-in default.
  - `automerge.maxDiffLines` — required on the same terms as `maxChangedFiles` (additions +
    deletions combined).
  - `automerge.mergeMethod` — one of `"squash"`, `"merge"`, `"rebase"`; defaults to
    `"squash"` when omitted. The field stays readable for configuration compatibility, but
    only `"squash"` is ever executed at merge time: a `"merge"` or `"rebase"` value produces
    its own logged policy hold instead of being validated against the repo's allowed merge
    methods or executed, and is never a retry loop.

In a monorepo, a changed file is resolved to the `projects[]` entry with the longest
matching `path` prefix; that project's own `automerge` block applies, falling back to the
top-level block when the project sets none, and to the top-level block directly for files
owned by no project. When a PR's changed files span more than one applicable block, the
effective policy is the **most restrictive** merge: the minimum of each numeric cap and the
union of `protectedPaths` across every block actually touched. **Any required block
missing is a deny** — an `.cenci/config.json` that is unreadable, not valid JSON, or simply
has no applicable `automerge` key (top-level or per-project) denies automerge for that PR;
there is no fallback to built-in thresholds. This means enabling `automerge.enabled`
fleet-wide with only one `projects[]` entry's `automerge` block defined immediately denies
every PR touching files outside that project — expected, not a bug, until a top-level
block (or per-project blocks for the other projects) is added.

The per-repo block is always read from the **PR's base branch**, never the PR's own head
branch or worktree — this is deliberate: reading policy from the head ref would let a PR
widen its own `protectedPaths`/caps and self-approve, exactly the fail-open hole this
feature exists to close.

See the `automerge:ok` label (label table above) for the complementary per-ticket grant —
`.cenci/config.json`'s `automerge` block is the repo-wide risk *policy* (paths, size caps,
merge method); `automerge:ok` is the per-ticket *grant* a human adds at refinement, with no
repo-level default (there is no `automerge.defaultRisk` setting) — see the "no repo-level
default" note further below. Both must hold, alongside green CI and a mergeable PR, before
`cenci babysit` will merge.

The `maintenance` field is optional and is **never written by a configure prompt** —
there is no question for it. It is a manually-editable escape hatch, like `security`
above, and merge semantics (step 6) preserve a hand-added value untouched across
reconfiguration. Do **not** add `maintenance` to the migration-removal list below — it
is a supported optional field, not a legacy one.

Maintenance is a core cenci workflow feature and is independent of
[lazyboards](https://github.com/matteobortolazzo/lazyboards): automatic changed-file
maintenance checks run during normal `/cenci:implement` runs, with no `.lazyboards.yml`
or `lazyboards` config required. A full, on-demand audit is always available via
`/cenci:maintain`.

Schema — every field below defaults as shown, so omitting `maintenance` entirely is
equivalent to writing all four defaults explicitly:
- `maintenance.enabled` — gates optional scheduled-maintenance and reminder UX only
  (default `true`); it never disables core correctness checks
- `maintenance.checkDuringImplement` — whether Phase 8 may repair findings
  automatically (default `true`); when `false`, Phase 8 still runs its changed-file
  correctness check but carries every non-pass result forward as report-only
- `maintenance.remindAfterDays` — days between reminders to run a full
  `/cenci:maintain` audit (default `30`)
- `maintenance.generatedDocs` — whether marker-bounded generated documentation sections are checked and regenerated
  (default `true`); when `false`, generated-section maintenance is skipped without
  suppressing other checks

```json
{
  "maintenance": {
    "enabled": true,
    "checkDuringImplement": true,
    "remindAfterDays": 30,
    "generatedDocs": true
  }
}
```

Core correctness checks always run when the maintenance checker is applicable, regardless
of whether this block is present or `maintenance.enabled` is false. The block controls
optional scheduled/reminder UX, whether Phase 8 may repair versus report findings, and
whether generated documentation sections participate. Omitting it keeps all optional UX
and repair/generated-section behavior enabled by default.

Only include servers in `mcpServers` that were presented as options (i.e., detected or always-available). Value is `true` if enabled, `false` if declined.

Only include servers in `lspServers` that were detected and presented in question 6. Value is `true` if enabled, `false` if declined. Omit `lspServers` entirely if no LSP servers were detected.

When migrating from an older config that has `ticketSystem`, `prSystem`, `ticketPrefix`, `adoOrg`, `adoProject`, `adoRepo`, `profile`, or `sandboxEnabled` fields, remove them during the merge.

7. **Commit, Push, and Open PR**: configure's changes live in `<worktree-path>` — ship them the same way every other change in this repo ships.

   Read `<worktree-path>/docs/git-workflow.md` for the commit/branch/PR conventions used below. Target the worktree explicitly with `git -C <worktree-path>` on every command below so they resolve against the worktree and stay auto-approved (see `cenci:shell-rules` — never compound `cd` with the git command itself).

   **Commit**:
   ```bash
   git -C <worktree-path> add -A
   git -C <worktree-path> commit -m "chore(configure): <one-line summary of what changed>

   <bullet list of generated/updated files>"
   ```
   If nothing is staged (a re-run that changed nothing), skip Commit/Push/PR entirely and report "No configuration changes — nothing to commit" instead of opening an empty PR.

   **Push**:
   ```bash
   git -C <worktree-path> push -u origin chore/configure-<slug>
   ```
   If push fails due to sandbox/network/auth, show the exact command and use `AskUserQuestion` ("Pushed, continue" / "Abort") to wait for the user to push manually before continuing.

   **PR**: write the body to `${TMPDIR:-/tmp}/cenci/cenci-configure-<slug>-pr-body.md` first (never a heredoc or large inline string), then:
   ```bash
   gh pr create --title "chore(configure): <one-line summary>" --body-file ${TMPDIR:-/tmp}/cenci/cenci-configure-<slug>-pr-body.md
   ```
   Body:
   ```markdown
   ## Summary
   Project configuration generated/updated by `/cenci:configure`.

   ## Changes
   - <one bullet per file/section actually written this run>

   ## Testing
   N/A — configuration/tooling only, no application code changed.
   ```
   Append a `## Review required — automerge policy` section — emitted only when question
   14 scaffolded a block this run (`### Autonomy Settings`), never on a re-config that
   reported an existing block verbatim:
   ```markdown
   ## Review required — automerge policy
   This PR scaffolds a starter `automerge` policy block (`protectedPaths`, size caps,
   `mergeMethod`). Review it before enabling automerge fleet-wide — see
   `docs/autonomous-loop.md#3-declare-what-a-merge-is-allowed-to-touch`.
   ```
   If `gh pr create` fails because a PR for this branch already exists (re-entry after a prior turn already created it), recover the URL with `gh pr view chore/configure-<slug> --json url -q .url` and continue. For any other failure (auth, network, validation), show the exact error and use `AskUserQuestion` ("Created, continue" / "Abort") to let the user resolve it before continuing.

   Delete the PR-body temp file after a successful `gh pr create` (or a successful recovery via `gh pr view`):
   ```bash
   rm -f ${TMPDIR:-/tmp}/cenci/cenci-configure-<slug>-pr-body.md
   ```

Report what was created and suggest next steps (e.g., "Try `/cenci:refine <ticket-id>` on a ticket"), including the PR URL from step 7. If question 14 (`### Autonomy Settings`) scaffolded an `automerge` block this run, say so explicitly and flag it for review, then point at the fleet-side next steps: `cenci dispatch plan-refined on` (once `planning.autonomy` is `lean` on `origin/main`) and `cenci automerge on` (once the scaffolded block has been reviewed) — the same verbs named in `### Autonomy Settings`'s own "Next step" block. If `sandbox.enabled` is `true`, mention the generated `.cenci/Dockerfile` and that `cenci sandbox build` (run from inside the repo, after the PR merges) builds the repo's own tailored image on top of the shared base. If `lazyboards.enabled` is `true`, list the generated `.lazyboards.yml` In Review actions with their keys, serve, and test commands (e.g., "`W` opens web-client's PR worktree, `S w` serves it with `ng serve`, `T w` runs its tests with `ng test --watch=false`") and point at `docs/orchestration.md` for the board recipe. Repeat the trust caveat here too, since this run's file ships as a PR: the generated shell actions and `cleanup` stay inert until `lazyboards trust` is run against the file's exact content, so trust must be re-granted after the PR merges if review changed a byte — and every teammate runs it once on their own clone. When the suggest-or-skip branch ran instead, report what happened (added actions, migrated to `keymaps:`, or "already complete — no changes").

### Board lifecycle labels

configure creates any missing lifecycle labels during project setup (step 3c) — `gh issue edit
--add-label` fails when a label is missing from the repository, which used to silently drop
labels (e.g. `Planned`) on projects configured before a label was introduced. The skills apply
the labels via `gh issue edit` as a ticket moves through the workflow, and self-heal with a
`gh label create … || true` before adding a label that may be missing. Document the label set
in the completion summary so the user can mirror it as columns on their board:

| Label | Applied by | Meaning |
|---|---|---|
| `Working` | refine (after the confirmation gate) / implement (at start) | Actively being refined or implemented |
| `Refined` | refine | Ready for implementation |
| `Planned` | implement Phase 1 (plan persisted) | Plan on disk, ready to pick up |
| `In Review` | implement Phase 9 (at PR-open) | PR is open, under review / CI running |
| `Implemented` | babysit (on PR merge) | PR merged — done |
| `Followup` | implement Phase 9 / address-review | Deferred/out-of-scope item captured from a session — triage before working; enters backlog unrefined |

`Followup` is orthogonal to the linear lifecycle above — it is never part of the `New → … → Implemented` chain and applies to a separate followup ticket (not the original). It is a capture-queue marker, never release-blocking; it is removed when the item is triaged out of the queue — promoted to real work via `/cenci:refine`, or grouped/superseded via `/cenci:maintain backlog` (see `docs/followup-triage.md`).

`Browser`, `ui:visual-check`, and `automerge:ok` are likewise refine-applied orthogonal markers, not columns in the `New → … → Implemented` chain — like `Followup`, they are not rows in the "Applied by / Meaning" table above, which enumerates board columns only; `automerge:ok` in particular is a per-ticket grant made by `/cenci:refine` at refinement time, with no repo-level default (there is no `automerge.defaultRisk` setting) — granted per ticket at refine's confirmation gate; never inherited by split children or followups.

A ticket judged trivial by implement's Trivial-Ticket Triage still transits through `Planned` — same labels, same board columns as any other ticket — just collapsed into one session instead of a stop-and-relaunch between `Planned` and `Working`. No new label state is introduced by the trivial-ticket fast path.

**Reconciler-managed labels**: `dispatch-failed`, `plan-invalid`, and `reconcile-stuck` are not applied by refine or implement — cenci's dispatch reconciler applies them automatically when it detects a stuck or failed automation state (dispatched work exhausted its retry budget, a `Planned` ticket has no parseable plan file, or reconciliation itself is stuck with its apply-retry budget exhausted). Like `Followup`, they are orthogonal to the `New → … → Implemented` lifecycle above and are not columns in that chain.

`Input Needed` is likewise orthogonal — like `Followup`, it is never part of the `New → … → Implemented` chain and is not a column in it. Unlike the skill-applied lifecycle labels above (which self-heal via each skill's own `gh label create … || true` fallback), `Input Needed` is applied by implement's unattended lean-mode escalation path via the `cenci pipeline label --transition input-needed` CLI call, which self-heals the label's existence through cenci's Go `ghLabelCreate` — the same mechanism `dispatch-failed`/`plan-invalid`/`reconcile-stuck` use, not a skill-level fallback. It is removed (swapping back to `Working`) when the ticket resumes.

Lifecycle: `New → Refined → Planned → Working → In Review → Implemented`.

UI conventions — the component library, its browsable catalog, and the reuse-before-authoring rule — live in each project's `AGENTS.md` `## UI Conventions` section (question 5c), which the planner and implementer read via the plan's `## Project Context`. There is no separate design stage or design ticket.

**Migration note for existing boards** (state this when re-configuring a project that predates
`In Review`): add an **`In Review`** column/label. Previously, tickets dropped straight into
`Implemented` the moment the PR was opened; now PR-open lands them in `In Review`, and
`/cenci:babysit` promotes them to `Implemented` when the PR actually merges. Existing tickets
that carry `Implemented` from before this change but whose PRs are still open can be relabeled to
`In Review` by hand; new work follows the split automatically.

**Migration note for existing boards** (state this when re-configuring a project that predates
`Planned`): add a **`Planned`** column/label between `Refined` and `Working`. Previously, a
planning session applied `Working` at pipeline start and then stopped once the plan was saved —
so the board showed `Working` on a ticket nobody was actively working. Now a planning session
lands the ticket on `Planned` ("a plan exists on disk, ready to pick up"); the swap to
`Working` happens when the plan-file implementation run begins. New work follows this
automatically.

**Migration note for existing boards** (state this when re-configuring a project that predates
the reconciler-managed labels): re-running `/cenci:configure` on an existing project creates
the `dispatch-failed`, `plan-invalid`, and `reconcile-stuck` labels retroactively via step 3c's
missing-only `gh label create` loop. No other action is needed — the reconciler already
self-heals these labels itself via `EnsureLabels`, so a board that skips this step is not
blocked; re-running configure just creates them proactively instead of waiting for the
reconciler to hit the corresponding error state first.
