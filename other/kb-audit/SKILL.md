---
name: kb-audit
description: "Audit / curate KB-vault hygiene — surfaces mechanical drift (broken [[wikilinks]], dangling §-pointers, status-enum violations, status-drift, index-row bloat) the librarian's KB-curator role consumes. REPORTS only; never auto-edits the vault. Use to check KB drift, audit the KB, or do KB hygiene."
argument-hint: "[--project <name>]"
---

# /kb-audit — KB-vault drift report

Explicit, opt-in surface over the offline KB-drift scanner
(`tests/kb_drift_scan.py`, checks C1–C7). Runs Phase-0 KB discovery, invokes the
scanner in `--summary` mode against the resolved vault + project, and presents
the grouped digest. **REPORTS only — never edits the KB.**

C7 (`C7_backlog_done_bloat`) fires when a project `BACKLOG.md` carries too many
completed items inline; the C7 detail recommends running
`python3 tests/backlog_archive.py <kb_root> --project <p> --dry-run` to review
and archive them.

### Caveman activation in this flow

Caveman compression is mandatory in this flow. The wire prefix
`[COMPRESSION:terse]` MUST be prepended to every subagent Task description and to
every Codex MCP `developer-instructions:` field within this flow. Machine-output
payloads (the scanner's `--summary` / `--json` text) are exempt per
`skills/caveman/SKILL.md` §7.

## When to use

- "audit the KB", "check KB drift", "kb hygiene", "проверь КБ на дрейф".
- After a spec ships or a session wraps — to catch broken links, dangling
  §-pointers, status-enum violations, or status-drift before they pile up.
- Periodically — the scanner is offline (no git, no network), cheap to re-run.

## Argument parsing

`$ARGUMENTS` is optional. The only supported flag:

- `--project <name>` — override the Phase-0-discovered project. The scan is
  restricted to `<kb_path>/repos/<name>/`. Without it, the discovered project is
  used.

## Phase 0: KB discovery

Resolve `kb_path` and `project` via the shared algorithm in
`docs/kb-discovery.md` (single source of truth:
`.ai-dev-team.local.yml → .ai-dev-team.yml → memory → sibling → ask`). No
skill-specific config extensions. If `--project <name>` was passed, it overrides
the discovered `project`.

## Run the scanner

Invoke the scanner in `--summary` mode (the human digest — stable headline line
plus per-class grouped detail):

```bash
python3 "${CLAUDE_PLUGIN_ROOT}/tests/kb_drift_scan.py" "<kb_path>" --project <project> --summary
```

`${CLAUDE_PLUGIN_ROOT}` is the plugin install dir exposed at runtime; the scanner
lives at `${CLAUDE_PLUGIN_ROOT}/tests/kb_drift_scan.py`.

## Present the report

Present the scanner's `--summary` output verbatim, then one line of
interpretation: `auto_safe:false` findings (every C2/C3/C4, plus any flagged C1)
are **human-decision items** — this skill REPORTS them, it never auto-edits the
KB (the scanner's autonomy boundary). The reader decides each flip/fix.

## Exit-code branch table

The scanner's exit code drives what `/kb-audit` does. **Exit `1` is the primary
SUCCESS path — findings present is the skill's whole reason to exist, NOT an
error.**

| Scanner exit | Meaning | `/kb-audit` action |
|---|---|---|
| `0` | clean, 0 findings | present the clean `--summary` headline (one line) |
| `1` | findings present | present the FULL grouped `--summary` (headline + detail) — **the main success path; never treat exit 1 as a failure** |
| `2` / `python3` absent / `kb_path` or `project` unresolved | scanner unavailable | one-line diagnostic, then stop — never crash, never fabricate a clean result |

Silent-degrade applies **ONLY** to the exit-`2`/unavailable row: emit a single
diagnostic line (e.g. "KB-drift scanner unavailable: <reason>") and stop. Do NOT
treat exit `1` (findings) as a degrade — render the findings; that is the skill's
job.
