---
name: init
description: Initialize, verify, or update Bulwark governance in a project. Sets up CLAUDE.md, rules.md, and optional tooling (statusline, LSP, scaffold). --update reviews canonical template changes interactively per-section.
user-invocable: true
argument-hint: "[--scope=project|user] [--verify | --update] [target-dir]"
allowed-tools:
  - AskUserQuestion
  - Bash
  - Read
  - Skill
  - Write
version: 1.2.0
author: "Ashay Kubal @ Qball Inc."
---

# Bulwark Init

Initialize, verify, or update Bulwark governance for a project or user. Installs governance files and optionally configures statusline, LSP, and project scaffolding. The `--update` mode handles propagation of canonical template changes (added rules, new In-Session Protocol sections, etc.) into the user-owned files that init originally wrote — `/plugin` updates skills/agents/hooks but cannot touch user's CLAUDE.md / rules.md.

## Usage

```
/the-bulwark:init                          # Interactive fresh install
/the-bulwark:init --scope=project          # Project scope, skip prompt
/the-bulwark:init --scope=user             # User scope
/the-bulwark:init --verify                 # Verify previous init completed
/the-bulwark:init --update                 # Review canonical template changes interactively
/the-bulwark:init --scope=project /path    # Project scope at specific path
```

---

## Mode Routing

```
IF $ARGUMENTS contains "--verify":
    → Jump to VERIFY MODE (Stage 8)
ELIF $ARGUMENTS contains "--update":
    → Jump to UPDATE MODE (Stage 9)
ELSE:
    → Continue with INIT MODE (Stage 1)
```

The three modes are mutually exclusive. `--verify` and `--update` are different operations: `--verify` asserts the original install completed correctly (read-only health check); `--update` proposes per-section additions from updated canonical templates (mutating, but interactive — no section is written without user approval).

---

## INIT MODE

### Stage 1: Parse Arguments

Extract from `$ARGUMENTS`:
- `--scope=project` or `--scope=user` → SCOPE
- Remaining positional argument → TARGET_DIR (optional, defaults to current directory for project scope)

### Stage 2: Pre-Flight — Cross-Scope Initialization Check

**Check BOTH scopes regardless of which scope the user selected.** This prevents silent conflicts where governance files exist at one scope and the user initializes at another.

Detect existing files at **project scope**:
- `./CLAUDE.md` (or `<target-dir>/CLAUDE.md`)
- `./.claude/rules/rules.md` (or `<target-dir>/.claude/rules/rules.md`)

Detect existing files at **user scope**:
- `~/.claude/CLAUDE.md`
- `~/.claude/rules/rules.md`

**Report findings to the user based on what was detected:**

#### Case A: No files found at either scope
Proceed to Stage 3. No warnings needed.

#### Case B: Files found at the SELECTED scope only
Warn the user:

```
Existing Bulwark files detected at [selected] scope:
  - [list files found]

The init script will create .bak backups of these files before overwriting.
```

Ask: "Proceed with initialization? (existing files will be backed up)"

#### Case C: Files found at the OTHER scope (not the selected one)
Warn the user:

```
Existing Bulwark files detected at [other] scope:
  - [list files found]

You are initializing at [selected] scope. The files at [other] scope will
NOT be modified, but having governance files at both scopes may cause
conflicting instructions that impact accurate functioning.

Options:
  1. Proceed — keep files at both scopes (you manage consistency)
  2. Cancel — remove or descope the [other] scope files first, then re-run
```

Ask the user to choose before proceeding.

#### Case D: Files found at BOTH scopes
Combine warnings from Case B and Case C:

```
Existing Bulwark files detected at BOTH scopes:

  Project scope:
    - [list files found]

  User scope:
    - [list files found]

You are initializing at [selected] scope:
  - Files at [selected] scope will be backed up (.bak) and overwritten.
  - Files at [other] scope will NOT be modified.

Having governance files at both scopes may cause conflicting instructions
that impact accurate functioning.

Options:
  1. Proceed — overwrite [selected] scope (backed up), keep [other] scope as-is
  2. Cancel — clean up the [other] scope files first, then re-run
```

Ask the user to choose before proceeding.

### Stage 3: Run Init Script

Execute the init script using the plugin directory path. First verify the environment variable is set:

```bash
if [ -z "${CLAUDE_PLUGIN_ROOT}" ]; then
  echo "ERROR: CLAUDE_PLUGIN_ROOT is not set. This skill must be run as a plugin."
  exit 1
fi
"${CLAUDE_PLUGIN_ROOT}/scripts/init.sh" [arguments]
```

`${CLAUDE_PLUGIN_ROOT}` is the Claude Code plugin runtime variable that resolves to the installed plugin root (substituted in skill content and exported as env var to subprocesses). If unset, the skill is not running in a plugin context.

Where `[arguments]` is the original `$ARGUMENTS` string (excluding `--verify`) passed through verbatim. This preserves `--scope=` and any target directory the user provided.

If `--scope` was not provided, init.sh will present its own interactive scope selection prompt.

### Stage 4: Report Results and Restart Warning

After init.sh completes successfully, present to the user as visible text (NOT hidden in bash output):

```
Bulwark governance initialized!

Files created:
  - [CLAUDE.md path]
  - [rules.md path]

IMPORTANT: Hooks do not activate until you restart your Claude Code session.
This is a known Claude Code limitation (#10997). After restarting, Bulwark's
quality gates (typecheck, lint, build) will enforce automatically on every
code change.
```

If init.sh exits with a non-zero status, report the error output to the user and stop.

### Stage 5: Post-Init Setup Selection

Use AskUserQuestion to present optional setup choices:

**Question:** "Which additional setup would you like to configure?"
**multiSelect:** true
**Options:**
1. **Status line** — Configure the Bulwark status line display (quick, no dependencies)
2. **LSP integration** — Set up Language Server Protocol for code intelligence (requires language servers)
3. **Project scaffold** — Generate Justfile with build/test/lint recipes (requires project manifest)

If the user selects nothing (skips), proceed to Stage 7 (write state and finish).

### Stage 6: Execute Selected Setup

Follow this order strictly:

#### 6a: Statusline (if selected)

Invoke the statusline skill immediately — it has no language dependencies:

```
/the-bulwark:bulwark-statusline
```

Follow the bulwark-statusline skill instructions completely. Once done, continue.

#### 6b: Language Selection (if LSP or scaffold selected)

If the user selected LSP, scaffold, or both, use AskUserQuestion to determine the tech stack:

**Question:** "What languages/frameworks does this project use?"
**multiSelect:** true
**Options:**
1. **Node/TypeScript** — JavaScript, TypeScript, React, Vue, etc.
2. **Python** — Python with pip, poetry, or uv
3. **Rust** — Rust with Cargo
4. **Other** — User specifies manually

Based on the selection, ensure the language toolchain is installed:
- **Node/TypeScript**: Check for `node`, `npm`. If missing, guide installation.
- **Python**: Check for `python3`, `pip`/`poetry`/`uv`. If missing, guide installation.
- **Rust**: Check for `rustc`, `cargo`. If missing, guide installation.
- **Other**: Ask the user what package manager and build tools they use.

**bun runtime (required for Bulwark eval framework + generated TS scripts)**:

The `create-skill` skill emits TypeScript-via-`bun` for eval-loop runs and generated archetype scripts. Verify and install via the bundled platform-aware installer:

1. Locate the installer:
   - Plugin install: `${CLAUDE_PLUGIN_ROOT}/scripts/install-bun.sh`
   - Local dev: `${CLAUDE_PROJECT_DIR}/scripts/install-bun.sh`

2. Verify-only check (does not install):
   ```bash
   bash <installer-path> --verify
   ```
   Exit 0 → bun ≥ 1.0 present, skip install.
   Exit 1 → bun missing or version below required.

3. Active install (idempotent — no-ops if already installed):
   ```bash
   bash <installer-path>
   ```
   Or via the scaffolded Justfile: `just install-bun`.

Platform support: Linux + macOS + WSL via `curl|bash` from `bun.sh/install`; Windows-native prints PowerShell instructions (`powershell -c "irm bun.sh/install.ps1 | iex"`). PATH integration writes to bun's default location (`$HOME/.bun/bin`) — installer prints rc-line guidance for bash/zsh/fish if the new shell does not pick it up automatically.

Also check for project manifest files (`package.json`, `pyproject.toml`, `Cargo.toml`). If none exist, ask the user if they want to initialize one (e.g., `npm init`, `cargo init`).

Once the language toolchain is confirmed present, proceed with the selected skills.

#### 6c: Scaffold (if selected)

Map the language selection to the scaffold `--lang` argument:
- Node/TypeScript → `--lang=node`
- Python → `--lang=python`
- Rust → `--lang=rust`
- Other/generic → `--lang=generic`

Invoke:

```
/the-bulwark:bulwark-scaffold --lang=<detected>
```

Follow the bulwark-scaffold skill instructions completely. Once done, continue.

#### 6d: LSP (if selected)

Map the language selection to the LSP `--lang` argument:
- Node/TypeScript → `--lang typescript`
- Python → `--lang python`
- Rust → `--lang rust`
- Other → `--lang <user-specified>`

Invoke:

```
/the-bulwark:setup-lsp --lang <languages>
```

Follow the setup-lsp skill instructions completely. Note: setup-lsp has its own restart checkpoint at Stage 6. That restart is separate from the init restart.

### Stage 7: Write State and Finish

Two separate state artifacts are written at this stage:

**Artifact 1 — Ephemeral verification state** (this skill writes):

```bash
mkdir -p "$CLAUDE_PROJECT_DIR/tmp/init"
```

Write to `$CLAUDE_PROJECT_DIR/tmp/init/init-state.yaml` using the schema from [templates/init-state.yaml](templates/init-state.yaml). Populate all placeholder values with actual data from this session. This file is read once by `--verify` (Stage 8) and deleted on successful verification.

**Artifact 2 — Durable install marker** (`scripts/init.sh` writes automatically):

`scripts/init.sh` writes `.bulwark/init-marker.yaml` to the scope root (project: `$PROJECT_DIR/.bulwark/init-marker.yaml`; user: `$HOME/.bulwark/init-marker.yaml`) at install time. Schema:

```yaml
version: "1.2.0"             # Bulwark version at install (from plugin.json)
init_at: "2026-05-09T22:30:00Z"
scope: project | user
scope_root: "/path/to/scope/root"
artifacts_written:
  - path: "CLAUDE.md"        # relative to scope_root
    canonical: "lib/templates/claude.md"  # relative to plugin root
  - path: ".claude/rules/rules.md"
    canonical: "lib/templates/rules.md"
```

This marker is durable (not deleted by `--verify`). It is consumed by:
- `scripts/hooks/check-template-drift.sh` — SessionStart hook silent-skips when marker absent (no false-positive drift on user-custom Rules.md projects)
- `/the-bulwark:init --update` (UPDATE MODE, Stage 9) — iterates `artifacts_written` to know which user files to diff against canonical templates

The marker is updated (NOT recreated) when UPDATE MODE applies template changes — the `version` field bumps to the current Bulwark version on successful update.

Present final summary to the user:

```
Bulwark initialization complete!

  Governance: CLAUDE.md + rules.md installed
  Statusline: [configured / skipped]
  LSP:        [configured / skipped]
  Scaffold:   [configured / skipped]

Next step: Restart your Claude Code session, then run:

  /the-bulwark:init --verify

This will confirm all components are working correctly.
```

---

## VERIFY MODE

### Stage 8: Verify Previous Init

Triggered by `--verify` flag. Reads the state file from the previous init run and checks each component.

#### 8a: Read State File

Read `$CLAUDE_PROJECT_DIR/tmp/init/init-state.yaml`. If it does not exist:

```
No init state found. Run /the-bulwark:init first to initialize Bulwark governance.
```

Stop.

#### 8b: Verify Governance Files

Check that the governance files exist at the scope recorded in the state file:

- **Project scope**: Check `./CLAUDE.md` and `./.claude/rules/rules.md`
- **User scope**: Check `~/.claude/CLAUDE.md` and `~/.claude/rules/rules.md`

Report: pass or fail for each file.

#### 8c: Verify Hooks Active

Check that hooks are firing. The simplest check: read the session's hook execution by looking for the governance protocol in the current session context. If this skill was invoked and Bulwark governance protocol was displayed at session start, hooks are active.

Report: pass or fail.

#### 8d: Verify Statusline (if selected)

If `statusline: true` in state file, check that `~/.claude/settings.json` contains statusline configuration.

Report: pass or fail.

#### 8e: Verify LSP (if selected)

If `lsp: true` in state file, invoke the LSP verification:

```
/the-bulwark:setup-lsp --verify
```

Follow the setup-lsp verification flow. Report result.

#### 8f: Verify Scaffold (if selected)

If `scaffold: true` in state file, run the checks below in order. Check 8f.1 determines the scaffold pass/fail; checks 8f.2–8f.6 are a non-blocking **toolchain smoke-run** that reports which language tools are installed on this machine. 8f.2 is the entrypoint (delegates to `scripts/toolchain-smoke-run.sh`); 8f.3–8f.6 are the contract the script implements.

##### 8f.1: Scaffold artifacts exist

Check that:
- `Justfile` exists in the project root
- `logs/` directory exists

If either is missing: scaffold status = **FAIL** and skip the remaining checks (toolchain smoke-run requires a valid Justfile).

##### 8f.2: Invoke the toolchain smoke-run script

All of 8f.2–8f.6 are implemented by `scripts/toolchain-smoke-run.sh` to keep the skill-to-script contract single-sourced. Verify the plugin directory variable is set (matching the Stage 3 pattern — bash subshells do not persist Claude Code runtime env vars unless re-resolved), then invoke:

```bash
if [ -z "${CLAUDE_PLUGIN_ROOT}" ]; then
  echo "Toolchain check: CLAUDE_PLUGIN_ROOT is not set — toolchain smoke-run unavailable."
  # Non-blocking: report toolchain: unavailable and continue with Stage 8g.
  TOOLCHAIN_STATUS=unavailable
else
  bash "${CLAUDE_PLUGIN_ROOT}/scripts/toolchain-smoke-run.sh" .
fi
```

The script is **non-blocking** and always exits 0. It prints a per-tool availability report to stdout and a machine-parseable trailer to stderr:

```
TOOLCHAIN_STATUS={ready|partial|unavailable|fail-loudly}
TOOLCHAIN_LANG={node|python|rust|go|kotlin|swift|shell|generic|unknown|none}
TOOLCHAIN_MISSING={comma-separated tool names or empty}
```

Read the trailer to fill in the Stage 8g summary's `Toolchain:` line. The sub-steps below (8f.3–8f.6) describe the contract the script implements; they are the spec, not a re-implementation.

##### 8f.3: Language detected from Justfile header

Read the first line of `./Justfile` and match against the canonical header format:

```
# Bulwark Justfile Template - <Language>
```

Where `<Language>` is one of: `Node/TypeScript | Python | Rust | Go | Kotlin | Swift | Shell | Generic (Fail-Loudly Fallback)`.

Store the detected language. If the header is missing or unrecognized, skip 8f.4–8f.6 and report `toolchain: unavailable (could not detect language from Justfile header)`. Scaffold check still counts as PASS — the toolchain smoke-run is non-blocking.

##### 8f.4: Justfile parses (`just --dry-run lint`)

Run `just --dry-run lint` in the project root. This asks `just` to resolve the `lint` recipe without executing it — confirms the Justfile is structurally sound and the `lint` recipe exists.

- Exit 0: proceed to 8f.5
- Exit non-zero: report `toolchain: unavailable (Justfile failed to parse or lint recipe missing)` with the stderr output. Scaffold check still PASS (the Justfile file exists), but toolchain cannot be verified.

##### 8f.5: Tool-by-tool availability check

For the detected language, run `command -v <tool>` for each tool the recipe invokes. Expected tools per language:

| Language | Tools to check |
|----------|---------------|
| Node/TypeScript | `tsc` or `./node_modules/.bin/tsc`, `eslint` or `./node_modules/.bin/eslint` |
| Python | `mypy`, `ruff`, `pytest` |
| Rust | `cargo` (ships with rustup; `cargo clippy` and `cargo fmt` are cargo subcommands) |
| Go | `go`, `golangci-lint`, `gofmt` (ships with Go) |
| Kotlin | `java` (prerequisite, 11+), `ktlint`, `detekt` |
| Swift | `swiftlint`, `swift-format` |
| Shell | `shellcheck`, `shfmt` |
| Generic | (skip — generic template has no real tools; status = `toolchain: fail-loudly (generic template by design)`) |

For each tool: record `installed` or `missing`.

##### 8f.6: Report toolchain status and install hints

Print a tool-by-tool table to the user:

```
Toolchain check (Go):
  - go             ✓ installed (/usr/local/go/bin/go)
  - golangci-lint  ✗ missing — install: brew install golangci-lint (macOS) | scoop install golangci-lint (Win) | see Justfile header
  - gofmt          ✓ installed (ships with Go)
```

Extract the install hint per tool from the Justfile template's header comment (the `Install:` block). If a tool has no hint in the header, fall back to the generic message: `install: see <tool's> upstream documentation`.

Set `toolchain` status:
- **`ready`** — all tools installed
- **`partial`** — Justfile parses, at least one tool missing (list them with install hints)
- **`unavailable`** — Justfile did not parse OR language could not be detected (pre-condition failure)
- **`fail-loudly`** — language is `Generic` (by design — no tools expected)

**Scope boundary (critical — non-negotiable):**
- This toolchain smoke-run **does not** install any tools.
- This toolchain smoke-run **does not** modify the Justfile.
- This toolchain smoke-run **does not** exit non-zero on any tool being missing.

A missing tool is informational. The user picks when to install based on their workflow.

#### 8g: Verification Summary

Present results:

```
Bulwark Init Verification
=========================

  Governance files:  [PASS / FAIL]
  Hooks active:      [PASS / FAIL]
  Statusline:        [PASS / FAIL / SKIPPED]
  LSP:               [PASS / FAIL / SKIPPED]
  Scaffold:          [PASS / FAIL / SKIPPED]
  Toolchain:         [READY / PARTIAL / UNAVAILABLE / FAIL-LOUDLY / SKIPPED]

  Overall: [ALL PASS / X failures]
```

**Notes on Overall status:**
- `Toolchain: PARTIAL` and `Toolchain: FAIL-LOUDLY` are informational and do NOT count as failures.
- Only `PASS/FAIL` checks count toward the overall verdict.
- If `Toolchain: PARTIAL`, list missing tools and install hints under the summary block.

If any failures, provide specific remediation steps for each.

Clean up the state file after successful verification:

```bash
rm $CLAUDE_PROJECT_DIR/tmp/init/init-state.yaml
```

---

## UPDATE MODE

### Stage 9: Review Canonical Template Changes

Triggered by `--update` flag. Detects sections present in canonical templates (`${CLAUDE_PLUGIN_ROOT}/lib/templates/`) that are missing from the user's installed copies, and offers batched per-section interactive review (Accept / Skip), with full-content inspection available upfront at Stage 9c pre-flight.

**Detail reference (BINDING)**: [references/update-mode.md](references/update-mode.md). Load before executing UPDATE MODE — covers full step-by-step procedure (marker read + backward-compat, drift detection, pre-flight summary, per-section interactive loop, marker version bump + audit log, final summary, full error matrix).

**Sub-references** (load on-demand):
- [references/update-section-anchor-diff.md](references/update-section-anchor-diff.md) — diff algorithm spec; section-anchor extraction; per-artifact-type recipes
- [references/update-askuser-prompts.md](references/update-askuser-prompts.md) — canonical AskUserQuestion templates per artifact type

**Helper scripts** (in `${CLAUDE_PLUGIN_ROOT}/scripts/`):
- `update.sh` — marker parsing, section-anchor diff, drift report writer
- `apply-section.sh` — position-aware section insertion (with append-at-end fallback)

**Stage 9 high-level flow** (each step expanded in references/update-mode.md):
1. **9a — Read marker**: `${SCOPE_ROOT}/.bulwark/init-marker.yaml`. If absent, fire backward-compat AskUserQuestion (offers to write marker for the current install state).
2. **9b — Compute drift**: invoke `update.sh --check --marker="$MARKER"` → drift report at `${SCOPE_ROOT}/.bulwark/drift-report-{timestamp}.yaml`. Zero drift → present "up to date" and exit.
3. **9c — Pre-flight confirm**: single AskUserQuestion summarizing drift count + offering full-content inspection ("Show full content for all sections first") + abort option before the batched loop.
4. **9d — Batched review loop**: drift items grouped into batches of ≤4 (AskUserQuestion's max questions-per-call); each batch fires ONE AskUserQuestion with tabbed questions, each tab Accept/Skip only. After batch submitted, Accepted items are applied SEQUENTIALLY via `apply-section.sh` (any failure aborts the entire run). Continues until all drift items processed.
5. **9e — Marker bump + audit log**: bump `version` field to current plugin version, update `init_at`, write `update-log-{timestamp}.yaml` recording per-section decisions.
6. **9f — Final summary**: present applied/skipped counts + audit log path + reassurance that next-session drift hook will silent-skip (or re-fire if user skipped sections they later want).

**Critical contract (read references/update-mode.md before executing)**: helper-script failures abort the loop — partial-state writes to user files are NOT acceptable. Marker absence is a backward-compat case, NOT an error. User-driven Skip is a valid outcome (write audit log normally).
