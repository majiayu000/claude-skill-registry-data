---
name: dep-inheritance
description: "Dependency inheritance audit: for every direct dependency answers the questions nobody asks - why is it here (from actual usage sites), how deep is the coupling, how replaceable is it, and what is the concrete exit plan. Parses manifests/lockfiles, scans usage, optionally enriches with registry metadata (offline-safe). Read-only. Trigger: /deps-audit"
trigger: /deps-audit
---
# /deps-audit

For each direct dependency answers the inheritance questions nobody asks:
What is it REALLY used for, how deep is the coupling, how replaceable is
it, and what is the concrete exit plan.

## What this is for

- Dependency decisions ("can we remove/replace X?") otherwise take days of
  research. This skill delivers a living inheritance register.
- **Read-only skill.** No CVE scan (use `npm audit` & co - not duplicated).
  No transitive dependencies in deep analysis, only counted.


## PROTECTION RULE - never ~/.claude/

Read-only skill. Guard required if write mode added later.

## What You Must Do When Invoked
During analysis, assign a confidence level to each finding: proven (confirmed by evidence), likely (strong signal, needs review), or suspected (weak signal).

If `/deps-audit -help` or `/deps-audit -h` (without further arguments)
is invoked: output the `## Usage` section unchanged and stop.

Otherwise follow these steps in order, skipping none.

### Step 1 - Help check
If invoked with `-help` or `-h`, output the `## Usage` section unchanged and stop.

### Step 2 - Clarify target

Clarify `-ProjectDir` and optionally a focus on individual dependency names.
Get confirmation.

### Step 3 - Inventory

```powershell
& "<SKILL_DIR>/scripts/deps-inventory.ps1" -ProjectDir "<path>" [-Only <names>]
```

No manifest found: cleanly report, stop.

### Step 4 - Registry metadata (optional)

Network available and user not opposed:

```powershell
& "<SKILL_DIR>/scripts/registry-meta.ps1" -Names <dependency-names> -Ecosystem npm
```

`metaError` for individual packages: continue without maintenance signal for the
affected dependency, note in report - no abort. Note: the
field `lastRelease` comes from the `time.modified` field of the registry, which
does not necessarily mean exact "last publish date" (registry metadata can be
updated without a new release) - label as approximation in the report.

### Step 5 - Analysis

Per direct dependency:

1. **Purpose** (from usage sites): what is it REALLY used for - the
   honest answer is often "for a single function". State confidence.
2. **Coupling depth**: `shallow` (few locations, simple calls) /
   `medium` / `deep` (API types in own signatures, inheritance, config magic).
   Evidence: `usageCount` + characteristic locations.
3. **Risk**: combination of coupling depth, maintenance signal (if
   registry metadata available), license anomaly (only hint, no
   legal advice), `unusedDeclared`.
4. Before confirming any `unusedDeclared`: check config files (json/yaml/rc) -
   e.g. eslint plugins are often referenced only there, not in code. Only then
   classify as "truly unused".
5. **Replaceability + exit plan**: name concrete alternative(s)
   (check stdlib replacement first), effort estimate (hours/days/weeks),
   the first 3 concrete steps of the exit.
6. If > 50 dependencies: register table for all, detail analysis only top 15 by
   risk, rest on request.
7. Evidence requirement: purpose/coupling always with locations; maintenance
   statements only with registry data (otherwise "no metadata available" - never guess).

### Step 6 - Write report

File `deps-inheritance-report.md` in the current working directory:

1. **Summary** - inventory, top 3 risks, quick wins (`unusedDeclared`).
2. **Register table** - name, purpose, coupling, risk, replaceability.
3. **Detail sections** per notable dependency.
4. **Open questions**.

### Step 7 - Summarize

State the report path, quick wins first.

## Usage

```
/deps-audit                    # interactive, all direct dependencies
/deps-audit <dir>              # analyze project
/deps-audit <dir> <dep> [...]  # only specified dependencies
/deps-audit -help
```


