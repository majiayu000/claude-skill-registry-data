---
name: pp-xray
description: "Parallel Process X-Ray - line-by-line reading of an external module/repo with evidence, risks and calls for the next investigation"
type: skill
---

> **Auto-Trigger:** When the user asks for a technical x-ray, a line-by-line audit, a deep read of an external module or an explanation backed by file evidence.
> **Keywords:** "pp-xray", "x-ray", "line by line", "deep audit", "external repo", "read everything", "end-to-end map"
> **Priority:** HIGH
> **Tools:** Bash, Read, Grep, Glob

# pp-xray - x-ray with evidence

## Goal

Produce a traceable technical reading of a delimited target. Unlike `pp-discovery`, this skill goes into the content of the selected files and records findings with path, line and impact.

Use it after a discovery, or when the user has already provided a scope small enough for a deep read.

## When NOT to Activate

- The target is still too broad for a complete read; use `pp-discovery`.
- The job is to merge reports/agents that have already run; use `pp-consolidate`.
- The question requires current external research; use a research flow with sources.
- The user asked for an immediate implementation/fix; use the appropriate feature/dev skill.

## Committed repository evidence (HPP 2.13+)

For a Git target, begin with `python -m hpp inventory --target .` and retain
its commit, universe, exclusions and dirty tracked count in your report. Do not
execute runner hints or CI command candidates. Inventory counts do not prove test
outcomes or document freshness. Read only the selected paths for deeper analysis;
use `python -m hpp codegraph build --target .` for static relationship evidence,
and keep coverage and unresolved references visible. No cache write is needed.
If the core or a committed HEAD is absent, report this and use the manual process
below; never convert an inspection failure into an empty-project finding.

## Process

1. Fix the scope and the completeness criterion.
2. Capture the state:
   - `git status --short --branch`
   - the exact list of files in the target.
3. Read the files in dependency order: manifests/configs, entrypoints, core libs, tests/docs.
4. For each finding, record:
   - file and line;
   - observed fact;
   - impact;
   - uncertainty or pending check.
5. Separate fact from recommendation.

## Expected Output

```md
# PP X-Ray - <target>

## Scope
- included:
- excluded:

## Files Read
| file | lines | role |

## Findings
| severity | file:line | fact | impact |

## Flows
1. input -> processing -> output

## Gaps
| gap | why it blocks certainty | how to verify |

## Recommendations
| priority | action | reason |
```

## Guardrails

- Do not claim "the whole repo" if the scope read was partial.
- Do not edit files during the x-ray, unless explicitly requested.
- Do not replace a live audit with old docs.
- If the target is too large, go back to `pp-discovery` and propose waves.

## Contract

**INPUT:** a delimited target and a completeness criterion.

**OUTPUT:** findings with severity, file:line, fact, impact and gaps.

**EXIT CODES:**

| Exit | Meaning |
|---|---|
| 0 | reading complete within the declared scope |
| 1 | warning: gap declared without invalidating the findings |
| 2 | block: scope too broad or evidence missing |
| 3 | error reading the target |

**STATE IT TOUCHES:**

| Path | Action |
|---|---|
| delimited target | read |
| destination chosen by the operator | write the report |

## Executed examples

```console
$ python -c "print('files_read=4')"
files_read=4
```
<!-- executed: 2026-09-22 · exit=0 -->

```console
$ python -c "print('findings=2 gaps=1')"
findings=2 gaps=1
```
<!-- executed: 2026-09-22 · exit=0 -->

```console
$ python -c "import sys; print('block: missing evidence'); sys.exit(2)"
block: missing evidence
```
<!-- executed: 2026-09-22 · exit=2 -->

## Proof

```bash
python -c "print('files_read=4')"
```
