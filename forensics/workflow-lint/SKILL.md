---
name: workflow-lint
description: Scan GitHub Actions workflow YAML across one or all local repos for known deprecated-action versions, retired runner images, and PowerShell scripting footguns before they cause a live CI failure. Run before a release wave or when auditing repo governance drift.
disable-model-invocation: true
---

# Workflow Lint

Static scan for GitHub Actions anti-patterns that have caused real, confirmed CI failures in this workspace (see the incidents this skill was built from: `upload-artifact@v3` auto-failing after GitHub's deprecation, `runs-on: ubuntu-20.04` queuing forever after image retirement, a PowerShell script reassigning the reserved `$args` variable and breaking named-parameter splatting).

This is a **static pattern scan**, not a full linter — it catches known-bad patterns, not all possible bugs. Pair with `ci-triage` for triaging failures the scan didn't catch.

## Usage

Scan every local repo under the current directory that has a `.github/workflows/` folder:

```bash
bash .claude/skills/workflow-lint/scripts/scan.sh
```

Scan specific repo roots:

```bash
bash .claude/skills/workflow-lint/scripts/scan.sh /c/dev/rewrite-docs /c/dev/charlie-deep-research
```

## What it checks

| Check | Why it matters |
|---|---|
| `upload-artifact@v[1-3]` / `download-artifact@v[1-3]` | GitHub now auto-fails runs using v3 outright; v1/v2 are further behind |
| `actions/checkout@v[1-3]` | Older majors lose support/Node version compatibility over time |
| `runs-on: ubuntu-16.04\|18.04\|20.04` | Retired hosted images — jobs requesting them queue forever instead of failing fast, which reads as a hang, not an error |
| PowerShell `$args = ...` | `$args` is PowerShell's automatic variable for unbound arguments; reassigning it for use with `@args` splat produces confusing positional-binding bugs (a plain string array like `@("-Flag", $value)` also silently binds positionally instead of by name — the fix is a hashtable splat, not just renaming the variable) |

## After a hit

Don't blanket-fix without confirming the flagged file actually needs it — verify the specific line, then apply the same fix pattern documented in `ci-triage`: reproduce the failure mode locally if possible, fix, re-verify.

## Extending

Add new checks to `scripts/scan.sh` as new anti-pattern classes are confirmed via real CI failures (not speculative ones) — keep this list evidence-based rather than a generic "best practices" lint to avoid false-positive noise across repos with genuinely different requirements.
