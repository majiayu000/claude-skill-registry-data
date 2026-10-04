---
name: solar-security
description: >
  Solar umbrella skill for security-sensitive workflows. Use when preparing
  markdown or plain text that will be sent to an AI provider: strip or replace
  GDPR-relevant and other sensitive patterns (emails, international phones,
  international IBANs, URLs) with stable placeholders so context stays usable without
  leaking identifiers. V1 is deterministic regex-based; extend via planet-local
  rules or future modules under this skill.
---

# Solar Security

## Purpose

Reduce accidental exposure of personal and sensitive identifiers when Solar
context (markdown, notes, exports) is used with LLMs. This skill defines a
**small, auditable first step**: pattern-based sanitization with consistent
placeholders inside a single run.

It does **not** claim legal anonymization or zero false negatives. Names,
free-form addresses, and novel identifier formats may still require human review
or planet-specific rules.

## When to Use

Use this skill when:

- You are about to paste or route **planet markdown** (or similar text) into
  Claude, Codex, Gemini, or other providers.
- You need a **repeatable** way to replace obvious international PII patterns
  before sharing context.
- You want a **single core skill** name (`solar-security`) for future security
  tooling (e.g. secret scanning) without scattering ad-hoc scripts.

Do not use as the only control for regulated data flows. Pair with governance
(no raw logs to providers, planet `AGENTS.md` rules, and explicit approvals where
Solar policy requires them).

## Required MCP

None

## Workflow

1. **Identify** the text to sanitize (single file path, directory for recursive in-place, or stdin).
2. **Run** `scripts/sanitize_context.py` (see below). Prefer writing output to a
   new file (e.g. `*.sanitized.md`) when not using directory in-place mode.
3. **Review** the optional JSON report for counts and placeholder mapping (do not
   commit reports that contain reversible mappings if your policy forbids it).
4. **Use** the sanitized text as the only input passed to the model for that task.

Planet-specific dictionaries (e.g. extra regex or literal replacements) can
live under `planets/<planet>/` and be merged manually or via a future flag; core
V1 ships with built-in patterns only.

For repository path consistency (rename files with placeholder tokens and
rewrite markdown links), use `scripts/sanitize_paths.py`.

For stable placeholders across runs, use the global Solar runtime mapping file:
`<runtime root>/security-map.json`.

## Script usage (`scripts/`)

Run from the active workspace (`SOLAR_WORKSPACE`; framework under `SOLAR_ROOT/core`).
Examples below use `planets/<planet>/...` as a generic Solar pattern, the scripts
also accept any valid file or directory path.

```bash
# Show options
python3 core/skills/solar-security/scripts/sanitize_context.py --help

# File in → file out (`target` + optional output path)
python3 core/skills/solar-security/scripts/sanitize_context.py \
  planets/<planet>/operations/example.md \
  /tmp/example.sanitized.md

# In-place: overwrite the single file
python3 core/skills/solar-security/scripts/sanitize_context.py \
  planets/<planet>/operations/example.md

# Directory: recursive in-place only (same idea as sanitize_paths target)
python3 core/skills/solar-security/scripts/sanitize_context.py \
  planets/<planet>/operations/meetings

# Directory: default is *.md only; add other suffixes explicitly when needed
python3 core/skills/solar-security/scripts/sanitize_context.py \
  planets/<planet>/workspace \
  --extensions md,txt,html,json

# Stdin → stdout (shell pipe)
cat some-context.md | python3 core/skills/solar-security/scripts/sanitize_context.py

# Optional: force backticks around `[PLACEHOLDER]` tokens in markdown
python3 core/skills/solar-security/scripts/sanitize_context.py \
  planets/<planet>/operations/example.md \
  /tmp/example.sanitized.md \
  --md on

# Emit a JSON sidecar report (counts + mapping of original→placeholder)
python3 core/skills/solar-security/scripts/sanitize_context.py \
  some-context.md \
  /tmp/sanitized.md \
  --report /tmp/sanitize-report.json
```

**Mapping file (automatic):** every run also reads and then **rewrites** `<runtime root>/security-map.json`
(paths are relative to the shell’s current working directory; from repo root that is `<runtime root>/security-map.json`).
That file stores stable placeholder assignments (for example `[EMAIL_001]`) across runs and for directory mode
is updated **once after processing all files**. It is separate from the sanitized document path (for example `/tmp/example.sanitized.md` above).

**Dependencies:** Python 3.9+ from the host. No third-party packages.

### Path sanitizer (`sanitize_paths.py`)

Requires replacement rules: either `--use-mapping` (reads `<runtime root>/security-map.json` by default when run from repo root) and/or `--old` / `--new`. Paths are relative to the shell’s current working directory, same as `sanitize_context.py`.

```bash
# Preview: rules from default <runtime root>/security-map.json (no --mapping needed)
python3 core/skills/solar-security/scripts/sanitize_paths.py \
  planets/<planet>/workspace \
  --use-mapping \
  --dry-run

# Apply rename + markdown reference updates (same default mapping file)
python3 core/skills/solar-security/scripts/sanitize_paths.py \
  planets/<planet>/workspace \
  --use-mapping

# Explicit one-off rule (no mapping file)
python3 core/skills/solar-security/scripts/sanitize_paths.py \
  planets/<planet>/workspace \
  --old TOKEN_SOURCE \
  --new TOKEN_TARGET

# Optional: non-default mapping path
python3 core/skills/solar-security/scripts/sanitize_paths.py \
  planets/<planet>/workspace \
  --use-mapping \
  --mapping /path/to/other-security-map.json

# Single-file mode
python3 core/skills/solar-security/scripts/sanitize_paths.py \
  planets/<planet>/workspace/pipeline.md \
  --use-mapping \
  --dry-run
```

## Examples

### Example 1

**User input:** “Sanitize this meeting note before sending it to the model.”

**Expected behavior:** Run `sanitize_context.py` on the note; hand the model
only the `.sanitized` output; discard or restrict the report per policy.

### Example 2

**User input:** “We need a security skill umbrella for Solar.”

**Expected behavior:** Load `solar-security`; use sanitize script for context
prep today; reserve this skill name for additional security scripts later.

## Failure protocol

- If the script errors, **do not** fall back to sending raw text to a provider
  without explicit human approval.
- If output still looks sensitive, treat it as a **false negative** gap: add a
  planet-local rule or extend patterns in a controlled change to this skill.

## References

- `references/pattern-notes.md` — scope and limits of built-in detectors.

## Provenance

Authored for Solar `core/skills/` under `solar-skill-creator` conventions.
