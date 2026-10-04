---
name: skill-diagnostics
description: Perform a static audit of an AL workspace for Business Central against the project's copilot-instructions.md contract. Reports findings by class (Compliance, Code quality, Test coverage, Permissions) and severity (Blocker, Major, Minor, Nit) with file:line citations. Never modifies code. Never invents rules. Use when asked to audit a workspace, run a compliance check, review before PR, or diagnose contract drift.
license: CC-BY-4.0
compatibility: Requires a Business Central AL workspace with .github/copilot-instructions.md at the repository root. Works with any PTE or AppSource app following standard AL-Go layout.
metadata:
  author: Javier Armesto · Workshop V-Valley 2026
  version: "1.0"
  categories: [compliance, code-quality, test-coverage, permissions]
---

# skill-diagnostics

## Purpose

Perform a **static audit** of an AL workspace against the project's
`copilot-instructions.md` contract. Produce a structured report of findings.
**Report only.** Never modify source code. Never invent rules that are not
declared in the contract.

## When to load

Load this skill when the user asks you to:

- Audit the workspace / run a compliance check / scan for issues
- Review the code before a PR / before a release
- Diagnose why a new file does not match project conventions
- List all violations of the `copilot-instructions.md` contract
- Generate a contract-drift report

## Input expectations

- Repository contains `.github/copilot-instructions.md` (required · if missing,
  emit a Blocker finding and continue with a reduced rule set)
- Workspace contains one or more AL projects with `app.json`
- Optional: test folder(s) declared in AL-Go `settings.json` under `testFolders`

## Finding classes

Group every finding into exactly **one** of four classes:

| Class | What it covers |
|---|---|
| **Compliance** | Object prefix, ID range, DataClassification, Caption/ToolTip presence |
| **Code quality** | XML docs, explicit `Access`, prohibited patterns, style ordering |
| **Test coverage** | Missing test codeunits, public procedures without tests |
| **Permissions** | Objects missing from permission sets |

## Severity scale

| Severity | Meaning | Rule of thumb |
|---|---|---|
| **Blocker** | Breaks contract at a fundamental level · must fix before merge | Missing DataClassification, ID out of range, no permission set entry |
| **Major** | Violates a required pattern declared in the contract | Missing Caption/ToolTip, public procedure without XML doc |
| **Minor** | Style deviation or soft convention | Wrong section order, hardcoded numeric ID in code |
| **Nit** | Noise-level observation · safe to ignore | Inconsistent indentation within a file |

**If in doubt between two levels, downgrade.** A noisy Blocker-heavy report
erodes trust. Reserve Blocker for things that would fail review hard.

## Rule catalogue · the ~20 rules this skill checks

Rules map 1:1 to statements in `copilot-instructions.md`. If a rule is not
declared in the contract, **do not check it**.

### Compliance (7 rules)

| # | Rule | Severity | Source in contract |
|---|---|---|---|
| C1 | Every new object name starts with the declared prefix | Major | "Object prefix" |
| C2 | Object IDs fall inside the declared `idRanges` of `app.json` | Blocker | "ID Range" |
| C3 | Every table has `DataClassification` at object level | Blocker | "Required Patterns · Tables" |
| C4 | Every table field has `Caption` | Major | "Required Patterns · Tables" |
| C5 | Every table field has `ToolTip` (except PK of lookup tables) | Major | "Required Patterns · Tables" |
| C6 | Every page has `ApplicationArea` and `UsageCategory` | Major | "Required Patterns · Pages" |
| C7 | Every enum declares `Extensible = true;` unless exception documented | Minor | "Required Patterns · Enums" |

### Code quality (8 rules)

| # | Rule | Severity | Source in contract |
|---|---|---|---|
| Q1 | Public procedures have XML documentation (`///`) | Major | "Required Patterns · Codeunits" |
| Q2 | Every procedure declares `Access` explicitly | Minor | "Required Patterns · Codeunits" |
| Q3 | `Rec.Modify(false)` has inline justification comment | Major | "Prohibited" |
| Q4 | No hardcoded numeric IDs in AL code | Minor | "Prohibited" |
| Q5 | No obsoleted patterns (`LookupFormId`, `RunFormLink`) | Blocker | "Prohibited" |
| Q6 | File naming matches `<ObjectName>.<ObjectType>.al` | Minor | "File naming" |
| Q7 | Indentation is 4 spaces (no tabs) | Nit | "Style" |
| Q8 | Section order inside tables/pages matches contract | Nit | "Style" |

### Test coverage (2 rules)

| # | Rule | Severity | Source in contract |
|---|---|---|---|
| T1 | Every public codeunit has a matching test codeunit | Major | "Test Coverage" |
| T2 | Each public procedure has at least one test method | Minor | "Test Coverage" |

### Permissions (3 rules)

| # | Rule | Severity | Source in contract |
|---|---|---|---|
| P1 | Every object declared in the app appears in ≥1 permission set | Blocker | "Permissions" |
| P2 | Permission sets follow naming `CEB <Feature> Basic/Full` | Minor | "Permissions" |
| P3 | At least one `Basic` and one `Full` permission set per feature area | Minor | "Permissions" |

## Workflow

Follow these steps in order.

### Step 1 · Verify contract presence

- Check that `.github/copilot-instructions.md` exists
- If missing: emit finding `[Blocker · Compliance] No copilot-instructions.md
  found — running with reduced rule set`
- Parse the contract and extract which rules are declared. **Only check rules
  that are declared.**

### Step 2 · Enumerate AL objects

- Read every `*.al` file in the declared `appFolders` from `.AL-Go/settings.json`
  (or `app/` by default)
- For each file, extract object type, ID, name, declared properties, fields,
  procedures

### Step 3 · Apply the rule catalogue

- For every object, run the rules in the catalogue above
- Record each violation as a **finding** with these fields:
  - `id` (e.g. `C3`, `Q1`)
  - `severity` (Blocker, Major, Minor, Nit)
  - `class` (Compliance, Code quality, Test coverage, Permissions)
  - `message` (short human-readable description)
  - `file` (relative path)
  - `line` (starting line number)
  - `remediation` (one-sentence suggestion · never code)
  - `contract_source` (which section of the contract backs this rule)

### Step 4 · Aggregate and prioritize

- Group findings by class
- Within each class, sort by severity (Blocker → Major → Minor → Nit)
- Within severity, sort by file path then line number

### Step 5 · Emit the report

Use the output format below. Stick to it exactly.

## Output format

```markdown
# skill-diagnostics · audit report

**Scanned:** <N> files · <M> objects
**Contract:** `.github/copilot-instructions.md` (<rules_declared>/<rules_catalogue> rules active)

## Summary

- **Blocker:** <n1>
- **Major:**   <n2>
- **Minor:**   <n3>
- **Nit:**     <n4>

## Findings

### Compliance (<count>)

- **[C3 · Blocker]** Table `CEB Sample Table` missing `DataClassification`
  at object level
  - `app/src/Tables/CEBSampleTable.Table.al:7`
  - *Remediation*: add `DataClassification = CustomerContent;` at object level
  - *Rule source*: `copilot-instructions.md` → "Required Patterns · Tables"

### Code quality (<count>)

- ...

### Test coverage (<count>)

- ...

### Permissions (<count>)

- ...

## Skills Applied

| Rule IDs checked | Count | Source |
|---|---|---|
| C1, C2, C3, C4, C5, C6, C7 | 7 | copilot-instructions.md → "Required Patterns · Tables / Pages / Enums" |
| Q1, Q2, Q3, Q4, Q5, Q6, Q7, Q8 | 8 | copilot-instructions.md → "Required Patterns · Codeunits" + "Prohibited" + "Style" |
| T1, T2 | 2 | copilot-instructions.md → "Test Coverage" |
| P1, P2, P3 | 3 | copilot-instructions.md → "Permissions" |

Rules skipped because not declared in contract: <list or "none">
```

## Constraints

- **NEVER modifies code.** This skill only reports. If the user asks for
  automatic fixes, politely decline and point them to `skill-fix` (if
  available) or manual remediation.
- **NEVER invents rules.** If a rule sounds reasonable but is not declared
  in the contract, do not apply it. Instead, list it in a separate section
  called "Suggested contract additions" at the end of the report.
- **NEVER aggregates severities into a single "score".** Findings are
  qualitative · a single Blocker matters more than ten Nits.
- **Report is idempotent.** Running the skill twice on the same workspace
  produces the same output.
- **Findings cite file:line.** Every finding must be traceable to a specific
  location in the source.

## References

- Agent Skills specification: https://agentskills.io/specification
- Workshop Bloque 02 material: https://javiarmesto.github.io/workshop-v-valley-aldc-2026-04/bloques/02-aldc/
- Project contract: `.github/copilot-instructions.md` (sibling file)

## Example invocations

Any of these trigger this skill via Copilot's auto-match on the description:

- "Audit my workspace for compliance issues"
- "Run a diagnostics scan before I open the PR"
- "Check which objects violate the project contract"
- "Give me a list of Blocker findings in this repo"
- "Scan for missing tooltips in the tables"

Explicit invocation also works:

```
Load skill-diagnostics and scan the workspace. Use the output format strictly
and include the Skills Applied block at the end.
```
