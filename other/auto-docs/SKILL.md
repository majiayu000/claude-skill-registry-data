---
name: auto-docs
description: "Write session documentation into _intelligence/documentation/sessions and re-route LLM comment slop."
invocation: on-demand
operad_source_colours: ["State", "Code"]
operad_target_colour: "Receipt"
operad_arity: 2
operad_residual: "unknown"
families: [meta, documentation]
---

# Auto Docs

`AuthorityEffect: None.`

## Overview

The `auto-docs` skill coordinates session-level documentation synthesis and code hygiene. It inspects touched files and session activity, compiles timestamped markdown documentation into `_intelligence/documentation/sessions/`, and triggers `techne-comment-slop-hunter-killer` to purge and re-route low-signal LLM comment slop into structured documentation.

By pairing documentation capture with comment purging, architectural insights remain permanently recorded in documentation custody while source files stay lean and uncluttered. To prevent polluting other IDEs' context, session documentation is consolidated exclusively under `_intelligence/documentation/` and is deliberately not mirrored across host seats (`.claude`, `.codex`, `.grok`).

Session records are digest inputs, not shelf laws. A record with no defect is `touch_provenance` and keeps its touched-file list. A substantive record fills `source_path`, `source_revision`, `failed_claim`, `counterexample`, `cause`, `correction`, `verification`, `applicability`, and `exceptions`. `oewas digest-governance` classifies a complete record as `lesson_candidate` and does not promote it.

For complete protocol details, see [Session Documentation Protocol](references/session_documentation_protocol.md).

---

## Sequential Execution Protocol

When invoked, `auto-docs` executes a 4-step pipeline:

```text
[Step 1] Session Activity Audit
         │ Inspects git status for modified/uncommitted code and tests
         │ Discovers touched paths and filters out frozen surfaces (.lake, target, venv)
         │ Excludes prior session logs and documentation trees (_intelligence, _ic, sessions)
         ▼
[Step 2] Session Documentation Synthesis
         │ Synthesizes structured markdown log to _intelligence/documentation/sessions/
         │ Bounds displayed touched files to max 100 entries to prevent log bloat (HP_MD_055)
         │ Records clickable file links, timestamps, and actual scan activity (HP_MD_054)
         ▼

[Step 3] LLM Comment Slop Hunter-Killer Execution
         │ Runs comment_slop_router across session-modified code files
         │ Re-routes extracted comments to _intelligence/documentation/<module_path>.md
         │ Purges low-signal comments while protecting docstrings and safety pragmas
         ▼
[Step 4] Host Isolation Hygiene
         │ Ensures mirror hosts (.claude, .codex, .grok) remain free of documentation slop
         │ Enforces zero-pollution discipline for third-party IDE environments
```

---

## Quick Commands & Scripts

### 1. Document Current Session and Re-route Slop

```bash
# Execute auto-docs for current session changes
python -m operations.use_cases.packaging.auto_docs_service

# Run via skill entrypoint with a custom topic label
python operads/skills/auto-docs/scripts/run.py --topic "feature_refactor"
```

### 2. Inspection / Scan-Only Mode

Scan the session-touched files for comment slop without modifying code:

```bash
python -m operations.use_cases.packaging.auto_docs_service --scan-only
```

### 3. Targeted Path Execution

Document and clean specific files or directories:

```bash
python -m operations.use_cases.packaging.auto_docs_service operations/use_cases/packaging
```

---

## Integration with `auto-oe-autop`

`auto-docs` is integrated into the autonomous `auto-oe-autop` meta-pipeline as **Stage 7**. Following the evaluation and proposal phases, Stage 7 automatically runs `auto-docs` to ensure all session artifacts are documented and comment hygiene is enforced before turn completion.

---

## Mandatory Defect Investigation Logging (`RULE_DEFECT_INVESTIGATION_LOGGING_001`)

Whenever `auto-docs` encounters any write refusal, git parsing error, or comment extraction failure:

1. Create a formal investigation report under:
   `_intelligence/blackrod/investigations/investigation_{YYYYMMDD}_auto_docs_{defect_id}.md`
2. Include full trace, target source code snippet, affected paths, and recommended remediation.
