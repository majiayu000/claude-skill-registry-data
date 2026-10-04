---
name: setup-lsp
description: Configures Language Server Protocol integration for Claude Code projects. Use when setting up LSP servers, verifying post-restart initialization, or troubleshooting broken LSP configurations.
user-invocable: true
argument-hint: "[--lang <languages>] [--verify | --troubleshoot]"
allowed-tools:
  - AskUserQuestion
  - Bash
  - Edit
  - Read
  - Write
version: 1.0.0
author: "Ashay Kubal @ Qball Inc."
---

# Setup LSP

Configure Language Server Protocol integration for Claude Code projects. LSP replaces text-based grep/glob searches with semantic code intelligence: go-to-definition, find-references, hover type info, call hierarchy, and real-time error detection.

---

## Mandatory Execution Checklist (BINDING)

**Every applicable item below is mandatory. No deviations. No substitutions. No skipping.**

This skill uses a 9-stage pipeline. You are the orchestrator. Follow every item in order. Do NOT return to the user until all applicable items are checked.

- [ ] **Stage 1 — Parse**: Arguments read, MODE determined (`full` | `verify` | `troubleshoot`), `--lang` extracted if present
- [ ] **Stage 2 — Detect**: `references/server-registry.md` loaded, manifest files scanned, DETECTED_LANGUAGES presented to user
- [ ] **Stage 3 — Binaries**: Binary install command run for each confirmed language
- [ ] **Stage 4 — Settings**: `ENABLE_LSP_TOOL=1` set in `~/.claude/settings.json` and shell profile
- [ ] **Stage 5 — Guide Plugin Install**: Present user with exact plugin names and instructions to install via `/plugin` or CLI
- [ ] **Stage 6 — Checkpoint**: Session ID captured via `${CLAUDE_SESSION_ID}`, exact `claude --resume` command presented to user, execution STOPPED
- [ ] **Stage 7 — Verify**: (on `--verify`) Debug log read, `Total LSP servers loaded: N` checked
- [ ] **Stage 8 — Diagnostics**: (if verification failed or `--troubleshoot`) `references/troubleshooting.md` loaded, issues checked in order
- [ ] **Stage 9 — Report**: `templates/diagnostic-output.yaml` loaded, diagnostic YAML written to `logs/diagnostics/`, summary presented to user

**Do NOT declare complete until all applicable checkboxes are marked.**

---

## When to Use This Skill

| Trigger Pattern | Scenario | Mode |
|-----------------|----------|------|
| Starting LSP setup from scratch | Project has no LSP configured | Full setup (no flags) |
| After restarting Claude Code following plugin install | Session resumed, verifying LSP loaded | `--verify` |
| LSP tools not appearing or servers not responding | Debugging a broken LSP configuration | `--troubleshoot` |

**DO NOT use for:**
- Projects where LSP is already confirmed working (check `~/.claude/debug/latest` first)
- Adding new language support to an already-configured LSP environment (run full setup again)

---

## Pre-Flight Gate (BINDING)

**STOP. Before running any installation steps, check the invocation flag.**

```
IF $ARGUMENTS contains "--verify":
    SKIP to Stage 7 (Verify Initialization)
IF $ARGUMENTS contains "--troubleshoot":
    SKIP to Stage 8 (Diagnostics)
IF $ARGUMENTS contains "--lang":
    Extract comma-separated language names → EXPLICIT_LANGUAGES
    Execute ALL stages in order, but Stage 2 uses EXPLICIT_LANGUAGES instead of scanning
OTHERWISE:
    Execute ALL stages in order (Stage 1 through Stage 9)
```

You MUST NOT skip stages or reorder them during full setup.

---

## Dependencies

| File | Requirement | When to Load |
|------|-------------|--------------|
| `references/server-registry.md` | REQUIRED | Stage 2 (detection) and Stage 3 (install) |
| `references/troubleshooting.md` | REQUIRED | Stage 8 (diagnostics) and whenever verification fails |
| `templates/diagnostic-output.yaml` | REQUIRED | Stage 9 (report results) |

Read each file at the stage where it is first needed. Do not defer loading.

---

## Usage

```
/setup-lsp                          Full setup: detect → install binaries → guide plugin install → checkpoint → verify
/setup-lsp --lang typescript,python Skip detection, install specified languages directly
/setup-lsp --verify                 Post-restart verification only (skip installation)
/setup-lsp --troubleshoot           Diagnostics only (no installation)
```

---

## Workflow

### Stage 1: Parse Arguments

Read `$ARGUMENTS`. Determine MODE (`full` | `verify` | `troubleshoot`) per Pre-Flight Gate above. If `--lang` is present, extract the comma-separated language names into EXPLICIT_LANGUAGES (e.g., `--lang typescript,python` → `["typescript", "python"]`). Report mode (and explicit languages if any) to user before proceeding.

---

### Stage 2: Detect Tech Stack

Read `references/server-registry.md`.

**If EXPLICIT_LANGUAGES was set in Stage 1** (via `--lang`): Look up each language name in the server registry. Build DETECTED_LANGUAGES from the matching entries (use "user-specified" as manifest path). If any language name doesn't match the registry, report the mismatch and ask user to clarify.

**Otherwise**: Scan project root and up to 2 directory levels deep for manifest files listed in the Official LSP Plugins table. For monorepos, scan each subdirectory independently. See registry for monorepo scanning guidance. Build DETECTED_LANGUAGES list (language, manifest path, plugin name).

**If DETECTED_LANGUAGES is empty** (no manifest files found):

```
No supported languages detected in this project.

You can select languages manually from the server registry:
  1. TypeScript/JavaScript
  2. Python
  3. Go
  4. Rust
  5. Java
  6. C#
  7. PHP
  8. C/C++
  9. Kotlin
  10. Swift
  11. Lua
  (See references/server-registry.md for full list)

Select languages to set up (comma-separated numbers), or 'skip' to abort:
```

Use AskUserQuestion to present the language list. If user selects 'skip', report "No languages selected" and proceed directly to Stage 9 (Report Results).

**If DETECTED_LANGUAGES is non-empty**, present to user:

```
Detected languages:
  - {language} ({manifest path}) → plugin: {plugin-name}

Proceed with installation? (yes / adjust)
```

Wait for user confirmation before continuing to Stage 3.

---

### Stage 3: Install Language Server Binaries

Read `references/server-registry.md`. Use the binary install commands for each confirmed language.

For each language in DETECTED_LANGUAGES:
1. Run the binary install command from the registry
2. Verify the binary is available: `which {binary-name}`
3. Report success or failure per language

If any binary install fails: report the error, note the language as FAILED, continue with remaining languages.

---

### Stage 4: Configure Settings

**Step 4a — Set ENABLE_LSP_TOOL in settings.json:**

Read `~/.claude/settings.json`. Add `"ENABLE_LSP_TOOL": "1"` if not already present. Write back.

**Step 4b — Set ENABLE_LSP_TOOL in shell profile:**

Check which shell profile exists (`~/.bashrc` or `~/.zshrc`). Add `export ENABLE_LSP_TOOL=1` if not already present.

Note: `ENABLE_LSP_TOOL` is an undocumented flag required for LSP tool activation (community report #15619).

---

### Stage 5: Guide User Through Plugin Installation (BLOCKING — User Action Required)

**IMPORTANT: Claude CANNOT run `claude plugin install` or `claude plugin enable` commands from within a session.** These must be performed by the user.

**Step 5a — Ask about installation scope:**

Use AskUserQuestion to ask the user which scope to install plugins in:

```
Which scope should the LSP plugins be installed in?

1. User scope (default) — available across all your projects (~/.claude/settings.json)
2. Project scope — shared with team via version control (.claude/settings.json)
3. Local scope — project-specific, gitignored (.claude/settings.local.json)
```

Record the chosen scope. For Option B CLI instructions, map to: `--scope user`, `--scope project`, or `--scope local`.

**Step 5b — Present plugin installation instructions and ask for status:**

First, present the installation instructions as plain text output (NOT inside AskUserQuestion):

```
PLUGIN INSTALLATION — USER ACTION REQUIRED

The language server binaries are installed. Now you need to install the
Claude Code LSP plugins for each language.

Scope: {chosen scope} ({scope description})

Option A — Using /plugin (within this session):
  1. Type /plugin
  2. Go to the "Discover" tab
  3. Search for and install each plugin:
{for each language in DETECTED_LANGUAGES}
     - {plugin-name}
{end}
  4. When prompted for scope, select "{scope label}" to match your
     earlier choice. The options shown will be:
       - "Install for you (user scope)"
       - "Install for all collaborators on this repository (project scope)"
       - "Install for you, in this repo only (local scope)"
     Select the one matching: {chosen scope}.

Option B — Using CLI (from a separate terminal):
  claude plugin marketplace update claude-plugins-official
{for each language in DETECTED_LANGUAGES}
  claude plugin install {plugin-name} --scope {chosen-scope}
{end}
```

Then use AskUserQuestion with two options:

```
1. "I've installed them" — plugins are already installed, proceed to next step
2. "I'll install them in this session" — dismiss this prompt so I can use /plugin
```

**If user selects option 1**: Proceed to Stage 6 (Checkpoint).

**If user selects option 2**: Dismiss the question and present this note as plain text:

```
No problem. Install the plugins using /plugin or from a separate terminal.

Once installation is complete, confirm here and I'll continue with the
remaining setup (exit+resume for LSP initialization).
```

Then WAIT for the user's natural text confirmation before proceeding to Stage 6. Do NOT present another AskUserQuestion — let the user type freely so they can use `/plugin` and other commands.

---

### Stage 6: Exit and Resume Checkpoint (BLOCKING)

**LSP servers only initialize at startup. This stage is mandatory and non-skippable.**

The current session ID is available as `${CLAUDE_SESSION_ID}`. Present to user and STOP:

```
LSP SETUP REQUIRES EXIT AND RESUME

Exit Claude Code now, then resume this session:

    claude --resume ${CLAUDE_SESSION_ID}

After resuming, run /setup-lsp --verify to confirm servers loaded.
```

**Do NOT continue past this stage.** Execution resumes only when user invokes `--verify` in the resumed session.

---

### Stage 7: Verify Initialization

This stage runs on `--verify` invocation after session resume.

Read `~/.claude/debug/latest` (internal debug log, path may change in future versions). Search for `Total LSP servers loaded: N`.

- N > 0 → PASSED. Note which servers appear.
- N = 0 → FAILED. Proceed to Stage 8.
- Line absent → Log not yet updated. Ask user to wait 10 seconds and retry.

Also check the `/plugin` Errors tab output if available — `Executable not found in $PATH` indicates a binary installation issue (see troubleshooting issue #5).

---

### Stage 8: Diagnostics

Read `references/troubleshooting.md`. Work through the 5 common issues in order: run each detection method, apply fix if detected, report result. After applying fixes, re-run verification (Stage 7) and report outcome.

---

### Stage 9: Report Results

Read `templates/diagnostic-output.yaml`. Fill all fields. Write completed diagnostic to `logs/diagnostics/lsp-setup-{YYYYMMDD-HHMMSS}.yaml`.

Present summary:

```
LSP Setup Complete

Detected languages:   {list}
Installed binaries:   {list with status: ok | failed}
Plugins installed:    {list — user-confirmed}
Verification status:  PASSED | FAILED | PENDING (awaiting resume)
Issues found:         {count} ({list if any})
Session ID:           {SESSION_ID}
Diagnostic log:       ./logs/diagnostics/lsp-setup-{timestamp}.yaml
```

If any server failed or verification failed, include next steps from `references/troubleshooting.md`.

**If plugins were installed for languages without matching source files in the project** (e.g., rust-analyzer-lsp installed but no `.rs` files or `Cargo.toml` present), append this note:

```
Note: Some LSP servers may show startup errors if there are no matching
source files in this project yet. This is expected — the server starts
but cannot find a workspace to index. Once you add source files for that
language (e.g., create a Cargo.toml for Rust), the server will activate
automatically on next session start.
```
