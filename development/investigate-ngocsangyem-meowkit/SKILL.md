---
name: mk:investigate
preamble-tier: 2
version: 1.0.0
description: |
  Systematic debugging with root cause investigation. Produces a diagnostic report;
  mk:fix owns remediation and mk:build-fix owns compile/build failures.
  Use when asked to "debug this", "fix this bug", "why is this broken",
  "investigate this error", or "root cause analysis".
  Proactively suggest when the user reports errors, unexpected behavior, or
  is troubleshooting why something stopped working.
  NOT for applying fixes without investigation (see mk:fix); NOT for
  step-by-step evidence-based reasoning (see mk:sequential-thinking).
allowed-tools:
  - Bash
  - Read
  - Write
  - Grep
  - Glob
  - AskUserQuestion
  - WebSearch
hooks:
  PreToolUse:
    - matcher: Write
      hooks:
        - type: command
          command: bash ${CLAUDE_SKILL_DIR}/bin/check-report-path.sh
          statusMessage: Checking diagnostic report path...
source: gstack
keywords:
  - investigate
  - root-cause
  - debug
  - four-phase
  - iron-law
  - systematic-debugging
when_to_use: Use when debugging with systematic root-cause investigation (four phases). NOT for applying fixes without investigation (see mk:fix).
user-invocable: true
owner: research
criticality: medium
status: active
runtime: claude-code
---

<!-- Split for progressive disclosure (checklist #11, #14): 497 → ~65 lines -->
<!-- References loaded just-in-time, not all upfront -->

# Systematic Investigation

> **Path convention:** Commands below assume cwd is `$CLAUDE_PROJECT_DIR` (project root). Prefix paths with `"$CLAUDE_PROJECT_DIR/"` when invoking from subdirectories.

**Iron Law: NO FIXES WITHOUT ROOT CAUSE INVESTIGATION FIRST.**

## Skill wiring

- **Reads memory:** canonical `.meowkit/memory/fixes.json` and `architecture-decisions.json`; fall back to matching generated Markdown views only when JSON is absent. See `.claude/rules/memory-read-rules.md`.
- **Writes:** a diagnostic report only, under `tasks/reports/**`; the hook enforces this path. `mk:fix` owns remediation and any memory capture after a fix.

## Plan-First Gate

Investigation precedes planning for bug fixes:

1. Confirm root cause FIRST (Iron Law)
2. After root cause confirmed, hand off to `mk:fix`. If the remedy affects more than two files, `mk:fix` requests an approved bug-fix plan using supported plan-creator syntax.

Skip: Investigation itself doesn't need a plan — it produces the input for planning.

## When to Use

- User reports errors, bugs, unexpected behavior
- "debug this", "fix this bug", "why is this broken"
- "investigate this error", "root cause analysis"
- Troubleshooting why something stopped working

## Process

1. **Run preamble** — load `references/preamble.md` and execute the startup bash block
2. **Collect symptoms** — read error messages, stack traces, reproduction steps
3. **Investigate root cause** — load `references/debugging-methodology.md` and follow Phase 1-3. For recurring patterns or complex failures, load `references/rca-method-selection.md` for methodology selection. Load `references/rca-anti-patterns.md` to avoid common RCA mistakes.
4. **Check alternatives** — test the strongest competing explanation before declaring a root cause.
5. **Write diagnostic report** — save only to `tasks/reports/{timestamp}-investigation-{slug}.md`; include the required output contract below.
6. **Hand off** — route confirmed defects to `mk:fix`, compile/build failures to `mk:build-fix`, and unresolved causes back to the user with explicit uncertainty.
7. **Run shared protocols** — load `references/shared-protocols.md` for completion status + telemetry

## References

Load **only when executing** the corresponding step — not upfront.

| Reference                                                             | When to load                    | Content                                                                     |
| --------------------------------------------------------------------- | ------------------------------- | --------------------------------------------------------------------------- |
| **[preamble.md](./references/preamble.md)**                           | Step 1 — skill startup          | Session init, env detection, upgrade check                                  |
| **[debugging-methodology.md](./references/debugging-methodology.md)** | Steps 2-4 — investigation | Evidence collection and hypothesis testing |
| **[shared-protocols.md](./references/shared-protocols.md)**           | Step 7 — completion             | AskUserQuestion format, completion status, telemetry, contributor mode      |

### Specialized Techniques (load based on bug type)

| Bug type | Load reference | What it adds |
|----------|---------------|-------------|
| Deep stack trace errors | `references/root-cause-tracing.md` | Backward trace: symptom → cause → ROOT CAUSE |
| Server/CI/DB incidents | `references/system-investigation.md` | 5-step system investigation methodology |
| CI/CD failures, log correlation | `references/log-analysis.md` | Filter → timeline → pattern → cross-source |
| Performance issues | `references/performance-diagnostics.md` | Quantify → layer isolation → bottleneck |
| Post-fix validation | `references/reporting-standards.md` | Enhanced DEBUG REPORT with timeline + recommendations |
| Test pollution | Run `scripts/find-polluter.sh <file> <test-pattern>` | Bisection to find which test creates unwanted state |
| Defense-in-depth | See `mk:fix/references/prevention-gate.md` | 4-layer validation (DRY — shared with mk:fix) |

## Constraints

- **Diagnostic only** — never edit source, tests, configuration, plans, or memory stores
- **Report-only writes** — `Write` is allowed solely for `tasks/reports/**` and is hook-enforced
- **3-strike rule** — if 3 hypotheses fail, STOP and escalate
- **Evidence boundary** — label each claimed cause as confirmed or uncertain; do not imply remediation completed

## Diagnostic Output Contract

Every report includes: symptom, reproduction status, expected versus actual behavior, ranked causes,
confirmed root cause or explicit uncertainty, evidence, and blast radius. Recommendations may name a
next owner but must not implement a fix.

## Hooks

- **Iron Law enforcement**: No fixes without confirmed root cause; `mk:fix` is the only remediation owner.
- **Report-path hook**: the `PreToolUse:Write` hook fails closed unless the destination is under `tasks/reports/**`.
- If root cause cannot be confirmed after 3 hypotheses, escalate to human
- **Interaction with mk:careful**: If mk:careful is active, debugging commands that touch state will still prompt for confirmation. This is expected — do not bypass.

## Gotchas

- **Confirming hypothesis without disproving alternatives**: Finding evidence FOR a theory doesn't mean it's correct → Actively test at least one alternative hypothesis before concluding
- **Log timestamps in wrong timezone**: Server logs in UTC, local comparison in local time → Normalize all timestamps to UTC before correlation

## Delegation: `mk:web-to-markdown`

When investigation requires fetching an arbitrary external URL (e.g. a vendor error page,
a remote log endpoint, a referenced issue URL), this skill delegates to
`mk:web-to-markdown` via the `--wtm-accept-risk` flag.

- **Without `--wtm-accept-risk`:** `mk:web-to-markdown` refuses cross-skill delegation.
  External URL resolution falls back to Context7 / chub / WebSearch only.
- **With `--wtm-accept-risk`:** delegation proceeds through all security layers
  (SSRF guard, injection scanner, DATA boundary, secret scrub). The flag is a conscious
  trust-boundary crossing — the caller acknowledges the target URL may contain prompt
  injection and that the skill's defenses are best-effort.
- Delegation example: `.claude/skills/.venv/bin/python3 .claude/skills/web-to-markdown/scripts/fetch_as_markdown.py "<url>" --wtm-accept-risk --caller mk:investigate`
