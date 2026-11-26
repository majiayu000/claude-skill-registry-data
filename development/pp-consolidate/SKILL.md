---
name: pp-consolidate
description: "Parallel Process Consolidate - consolidates the outputs of parallel sessions/agents into a single, deduplicated, verifiable verdict"
type: skill
---

> **Auto-Trigger:** When there are multiple outputs from agents, sessions, audits or waves and the user asks for a synthesis, a verdict, a consolidation or the top findings.
> **Keywords:** "pp-consolidate", "consolidate", "agent synthesis", "parallel outputs", "verdict", "dedup", "merge audits"
> **Priority:** HIGH
> **Tools:** Bash, Read, Grep, Glob

# pp-consolidate - consolidation of parallel waves

## Goal

Turn several parallel answers or artifacts into a single traceable decision. The focus is removing duplicates, resolving conflicts and stating what is proven, what is hypothesis and what still needs live verification.

## When NOT to Activate

- There are not yet multiple outputs or artifacts to consolidate.
- The request is to inventory a repo/folder before the analysis; use `pp-discovery`.
- The request is a deep read of a single target; use `pp-xray`.
- The consolidation would require running operational actions; produce the verdict and route it to your operational executor.

## Process

1. Inventory the inputs: files, messages, task ids, commits or reports.
2. For each input, extract atomic findings with their source, and tag each one with `[ID:<input id>]` (the `id` column of the Inputs table).
3. Deduplicate by entity + root cause + evidence, not by similar wording.
4. Classify conflicts:
   - confirmed by two sources;
   - contradictory;
   - stale or without evidence.
5. Produce a TOP-N with severity, impact and next step.
6. Check the citations (requires the HPP core, `python -m hpp`): export the Inputs table as `inputs.json` (`[{"id": "<input id>", "text": "<source> · <date>"}]`) and run the check below over the written verdict. Its exit 0/1/2 is this skill's exit 0/1/2; a refused input (a message on stderr and no report, e.g. invalid JSON) is this skill's exit 3. It proves every marker resolves to an input, not that the input supports the finding.

```bash
python -m hpp cite check --text CONSOLIDATED.md --context inputs.json
```

## Expected Output

```md
# PP Consolidate - <topic>

## Inputs
| id | source | date | confidence |
| [ID:<input id>] | <source> | <date> | <confidence> |

## Verdict
- status:
- decision:
- blockers:

## Deduplicated Findings
| rank | state | finding | sources | evidence | action |
| <rank> | <state> | <finding> | [ID:<input id>] | <evidence> | <action> |

## Conflicts
| topic | source A | source B | resolution |

## Gaps
| gap | owner | evidence needed |

## TOP-10
1. ...
```

## Guardrails

- Do not promote consensus without evidence.
- Do not erase divergences; resolve them or mark them as a conflict.
- Do not treat an agent's output as a live fact without verifying, when the information may have changed.
- Do not run operational tasks; this skill consolidates knowledge for a decision.
- Every row or sentence with a number (a date, a rank, a count) carries a marker; `hpp cite check` warns (exit 1) on an uncited number, which is why the Inputs rows cite themselves.

## Contract

**INPUT:** two or more outputs identified by source.

**OUTPUT:** one deduplicated verdict with conflicts and gaps preserved.

**EXIT CODES:**

| Exit | Meaning |
|---|---|
| 0 | consolidation complete and traceable |
| 1 | warning: partial input declared, or `hpp cite check` warned (an uncited number, too many markers in a sentence) |
| 2 | block: missing source or hidden conflict (`hpp cite check`: a marker that does not resolve to an input) |
| 3 | error reading the inputs |

**STATE IT TOUCHES:**

| Path | Action |
|---|---|
| the given outputs | read |
| destination chosen by the operator | write the verdict |
| `inputs.json` next to the verdict | write (the Inputs table as the citation context) |

## Executed examples

```console
$ python -c "print('inputs=3 findings=2')"
inputs=3 findings=2
```
<!-- executed: 2026-09-22 · exit=0 -->

```console
$ python -c "print('conflicts=1 preserved=1')"
conflicts=1 preserved=1
```
<!-- executed: 2026-09-22 · exit=0 -->

A finding cites `[ID:C]`, and there is no input `C`:

```console
$ cat inputs.json
[{"id": "A", "text": "audit-api.md"}, {"id": "B", "text": "audit-db.md"}]
$ cat CONSOLIDATED.md
| rank | state | finding | sources |
|---|---|---|---|
| 1 | confirmed | retry loop has no upper bound | [ID:A] |
| 2 | conflict | index missing on orders.created_at | [ID:B] [ID:C] |
$ python -m hpp cite check --text CONSOLIDATED.md --context inputs.json
{
  "context_sha256": "64026fae29ba8cf577a140176e6ec451654eb177f350f38aa8307d9b34f192c0",
  "counts": {
    "cited_ids": 2,
    "context_ids": 2,
    "markers": 3,
    "quantitative_sentences": 2,
    "sentences": 3,
    "unique_cited_ids": 2,
    "unused_context_ids": 0
  },
  "exit_code": 2,
  "findings": [
    {
      "code": "UNKNOWN_ID",
      "excerpt": "| 2 | conflict | index missing on orders.created_at | [ID:B] [ID:C] |",
      "line": 4,
      "marker": "[ID:C]",
      "message": "marker cites 'C', which is not in the context",
      "sentence": 3,
      "severity": "block"
    }
  ],
  "marker_pattern": "\\[ID:([^\\]\\n]*)\\]",
  "max_per_sentence": 4,
  "schema": "hpp.citation-check/v1",
  "text_sha256": "1ebabd9eaf9e946bb73af58d9f6c7f5d5a7a6a4a2d0bd29435948c1cb8fe2f88",
  "verdict": "block"
}
```
<!-- executed: 2026-09-24 · exit=2 -->

## Proof

```bash
python -c "print('inputs=3 findings=2')"
```
