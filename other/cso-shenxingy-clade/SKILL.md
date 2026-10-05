---
name: cso
description: "Security audit skill — systematic OWASP + STRIDE review of a project. Covers attack surface, secrets archaeology, dependency supply chain, OWASP Top 10, threat modeling, and false-positive filtering. Outputs a prioritized findings report."
---

# Clade for Codex

This workflow runs **directly in Codex**. Do not launch the `claude` CLI or
delegate the workflow to Clade's MCP bridge.

Codex compatibility rules:

- Plugin skills are namespaced. Invoke this workflow explicitly as
  `$clade:cso`; a bare `$name` does not select the installed Clade plugin.
- Read the nearest `AGENTS.md` files for repository instructions. If a project
  has only `CLAUDE.md`, treat it as legacy project guidance and read it too.
- Store new Clade working state under `.clade/` (or `~/.clade/` for personal
  state). Existing legacy Claude state may be read for migration, but do not
  create new vendor-specific state.
- A `/skill-name` reference means the corresponding Codex
  `$clade:skill-name` plugin skill, or the same workflow invoked naturally when
  explicit skill invocation is not available.
- Use Codex web, file, shell, image, and subagent capabilities when the source
  workflow names a vendor-specific tool. If a capability is unavailable, use
  the documented fallback instead of spawning another agent CLI.
- Paths such as `<plugin-root>/...` are relative to the installed Clade plugin
  containing this `SKILL.md`; resolve that root before invoking a helper.

## Canonical Clade workflow

You are the CSO (Chief Security Officer) skill. You perform a systematic security audit of the project.

## Mode

- **Daily mode** (default) — flag findings with confidence ≥ 8/10. Fast, high-signal only.
- **Comprehensive mode** (`/cso --full`) — flag findings with confidence ≥ 2/10. Exhaustive, for pre-launch audits.

---

## Weigh findings by whether the layer runs

Before ranking anything, read `docs/layers.json`. It declares which surfaces of
this repository are actually run and how much a finding in each one is worth:

- **load-bearing** — a defect here is a defect. Rank normally.
- **dormant** — builds and passes CI but is not run. Report findings, and rank
  them *below* any load-bearing finding. Do not propose deleting the layer and
  do not present its gaps as debt; new work there is opt-in.
- **generated** — never edit directly. The finding belongs in the source surface
  plus its regen script, not in the copy.

This exists because an audit of this repository spent most of its effort on the
orchestrator, a layer the owner had switched off months earlier. Nothing in the
tree said so, so the effort looked well spent right up until it was reported.

---

## Phase 0: Context Gathering

```bash
git branch --show-current
ls -la                    # project structure
cat AGENTS.md 2>/dev/null | head -30   # tech stack
```

Identify:
- Language(s) and framework(s)
- Entry points (HTTP routes, CLI, cron jobs, webhooks)
- External integrations (DBs, 3rd party APIs, auth providers)
- Data sensitivity (PII? financial? health?)

---

## Phase 1: Attack Surface Census

Map all entry points where attacker-controlled data enters the system:

**Code surface:**
- HTTP routes / API endpoints — enumerate all
- Form inputs and query parameters
- File uploads
- Webhook receivers (does the code verify signatures?)
- CLI arguments

**Infrastructure surface:**
- Env vars — which ones hold secrets?
- Exposed ports (check docker-compose, configs)
- Public S3 buckets / storage
- CORS configuration

---

## Phase 2: Secrets Archaeology

Search for hardcoded secrets and credential exposure:

```bash
# Hardcoded secrets patterns
grep -rn "sk-\|api_key\s*=\|password\s*=\|secret\s*=\|token\s*=" \
     --include="*.py" --include="*.ts" --include="*.js" --include="*.env*" \
     . | grep -v ".git" | grep -v "__pycache__" | grep -v "node_modules"

# Check for .env files committed to git
git log --all --full-history -- "**/.env" "*.env"

# Check git history for removed secrets (they're still there)
git log --all -S "password" --oneline | head -10
git log --all -S "sk-" --oneline | head -10
```

Check CI/CD configs for exposed secrets:
```bash
find .github -name "*.yml" -o -name "*.yaml" 2>/dev/null | xargs grep -l "secret\|password\|key" 2>/dev/null
```

---

## Phase 3: Dependency Supply Chain

```bash
# Python
pip-audit 2>/dev/null || safety check 2>/dev/null || \
  pip list --format=json | python3 -c "import sys,json; pkgs=json.load(sys.stdin); print(f'{len(pkgs)} packages — run pip-audit for vuln scan')"

# Node.js
npm audit --json 2>/dev/null | python3 -c "
import sys, json
try:
    d = json.load(sys.stdin)
    vulns = d.get('metadata', {}).get('vulnerabilities', {})
    print(f'Vulnerabilities: critical={vulns.get(\"critical\",0)}, high={vulns.get(\"high\",0)}, moderate={vulns.get(\"moderate\",0)}')
except: pass
" 2>/dev/null || true
```

Flag: unpinned major dependencies (e.g., `requests>=2.0.0` instead of `requests==2.31.0`).

---

## Phase 4: OWASP Top 10 Analysis

Load `references/owasp-top10.md` now — it contains the full checklist, high-signal grep patterns, and confidence guidance for each category.

Check each of the 10 categories using that reference. For each finding, confirm it's exploitable before flagging (skip if false positive — see Phase 6).

---

## Phase 5: STRIDE Threat Model

Load `references/stride.md` now — it contains the full STRIDE analysis table, component template, and priority matrix.

For each major component (web server, database, auth service, background workers), work through S-T-R-I-D-E using that reference. Only flag items with a plausible attack path for this project's threat model.

---

## Phase 6: False Positive Filter

Load `references/false-positive-filter.md` now — it contains 12 auto-discard rules, a self-check protocol, and confidence level definitions.

Apply all 12 rules to every finding. For each surviving finding, confirm there's a concrete attack path and real impact specific to this codebase. Assign a confidence level (HIGH/MEDIUM/LOW) per the reference.

---

## Phase 7: Findings Report

Output a prioritized report:

```
SECURITY AUDIT REPORT
════════════════════════════════════════
Project: [name]   Branch: [branch]   Date: [date]
Mode: daily | comprehensive
Threat model: [brief description of attacker profile]

CRITICAL (must fix before ship)
  [C1] [A03-Injection] SQL injection at routes/users.py:87
       Attack: GET /users?id=1 OR 1=1--
       Impact: Full DB read access
       Fix: Use parameterized query — `cursor.execute("SELECT ... WHERE id = %s", (id,))`

HIGH (fix in this sprint)
  [H1] ...

MEDIUM (fix in next sprint)
  [M1] ...

LOW / Informational
  [L1] ...

DISCARDED (false positives filtered)
  - [DoS exclusion] Rate limiting on /api/generate — LLM cost risk is LOW (auth required)
  - [Test-only exclusion] Hardcoded credentials in tests/fixtures/

Summary: N critical, M high, P medium, Q low
════════════════════════════════════════
```

Save report to `.clade/security-reports/YYYY-MM-DD.md`.

---

## Completion Status

- ✅ **DONE** — audit complete, report saved
- ⚠ **DONE_WITH_CONCERNS** — audit complete but some phases were skipped (e.g., no package manager detected)
- ❌ **BLOCKED** — cannot read key files or missing context
- ❓ **NEEDS_CONTEXT** — need to know threat model or data sensitivity before starting

**Scope note:** This is an AI-assisted audit, not a penetration test. Flag findings confidently but caveat that manual verification is needed before treating any finding as confirmed exploitable.

---

## Deep-Dive Mode (optional)

For HIGH-confidence findings in critical files, spawn the `security-auditor` subagent for line-by-line analysis:

```
Use a Codex subagent when available with subagent_type="security-auditor":
  "Audit [file path] for [specific vulnerability category]. Context: [what you already know about this component]"
```

Merge the subagent's findings into the main report. The subagent has no Write access — it only reads and reports.

---

## Error Handling

| Scenario | Action |
|----------|--------|
| Cannot read key source files (permission denied) | Note in report as "Partial audit — [file] unreadable". Continue with what's accessible. |
| No package manager detected (no requirements.txt, package.json, etc.) | Skip Phase 3, note "Dependency audit skipped — no package manifest found" |
| Git history unavailable | Skip git-based secret archaeology, note it |
| Project is non-code (docs-only, config-only) | Output "No attack surface found — this directory contains no executable code" |
| Ambiguous tech stack | List what was detected, ask user to confirm before proceeding with OWASP analysis |

## Delivery completion

If this workflow changes files or external state:

- Inspect the real final state before responding, including `git status` for a
  repository task.
- Never report `DONE` while task-owned changes are uncommitted. Use or continue
  `$clade:delivery` and create a repository-compliant checkpoint or preserve
  the work when committing is unavailable.
- When the user request or trusted repository policy makes publication,
  deployment, or live verification part of the task, do not silently downgrade
  the result to local-only work.
- If a required delivery transition lacks authority, credentials, a destination,
  or reachable external state, report `BLOCKED` or `NEEDS_CONTEXT` rather than
  appending a "not committed/pushed/deployed" caveat after `DONE`.
