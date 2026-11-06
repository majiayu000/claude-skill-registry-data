---
name: dep-audit
description: Dependency audit for Aegis SWR. Invoke on changes to pyproject.toml / uv.lock / requirements.txt, or on a weekly cadence, or manually as /dep-audit. Runs a CVE scan and a licence-compatibility check and delegates the deep write-up to the background-reviewer agent.
allowed-tools: Read, Grep, Glob, Bash, Agent
invocation: /dep-audit
# Ported from Claude (.claude/skills/dep-audit/SKILL.md) on 2026-07-03
# Note: In Copilot a lightweight dep_audit.py native PostToolUse hook now runs on
#       manifest edits, while /dep-audit remains the deeper on-demand review.
---

# Dependency Audit

Audit Python dependencies for known CVEs and licence conflicts.

> **Copilot note**: In Claude Code this ran automatically when `pyproject.toml` /
> `uv.lock` / `requirements*.txt` was edited (via `dep_audit.py` PostToolUse hook).
> Copilot CLI now also runs a lightweight native PostToolUse audit after manifest
> edits. Invoke `/dep-audit` when you need the full CVE + licence review report, or
> on a weekly cadence.

## Steps

1. **Vulnerabilities**:
   - `uv run pip-audit --progress-spinner off` (or `pip-audit` directly).
   - For each finding, note package, installed version, CVE/GHSA id, fixed
     version, and severity.
2. **Outdated pins**: `uv tree --outdated` - flag majors behind that carry
   security relevance.
3. **Licences**: enumerate direct deps from `pyproject.toml`; identify each
   licence (use `pip-licenses` if available, else WebSearch). Classify each into
   Allow / Flag / Block using
   **`.github/copilot/skills/dep-audit/references/licence-policy.md`** — GPL/AGPL/SSPL
   and unknown licences are blocking for this proprietary product; LGPL/MPL are
   flags needing sign-off.
4. **Delegate the report**: spawn the `background-reviewer` agent to compile the
   findings into `docs/reviews/YYYY-MM-DD-dep-audit.md` with severities and
   recommended bumps.

## Output

```
## Dependency Audit - <date>
### Vulnerabilities
| Package | Version | CVE/GHSA | Severity | Fixed in |
### Licence risks
| Package | Licence | Risk |
### Recommended actions (for coder)
- bump <pkg> <old> → <new>
```

If any CRITICAL/HIGH CVE is found, recommend an immediate `python-expert` bump + `testing-expert`
regression run before the next release.

## Completion checklist

- [ ] `pip-audit` run; every finding has package, version, CVE/GHSA id, severity, and fixed-in version
- [ ] `uv tree --outdated` reviewed; security-relevant majors-behind flagged
- [ ] Every direct dep licence classified Allow / Flag / Block per licence policy
- [ ] Any GPL/AGPL/SSPL/unknown licence reported as a **blocking** risk
- [ ] `UNKNOWN`/unclassified licences reported explicitly
- [ ] `background-reviewer` spawned to compile `docs/reviews/YYYY-MM-DD-dep-audit.md`
- [ ] Any CRITICAL/HIGH CVE → immediate `python-expert` bump + `testing-expert` regression recommended
