---
name: review-to-lint
description: "Move the mechanical items of a reviewer's checklist or past findings into a deterministic script."
disable-model-invocation: true
user-invocable: true
origin: shimo4228
---

# Review → Lint absorption

A reviewer's checklist mixes in items that a script counts more accurately and cheaply than an LLM does.
This skill draws that boundary, moves the mechanical side down into a script, and focuses the reviewer's attention
on semantic checks. Prior examples: `readme_evidence.py` (the author's README skill), `adr_lint.py` and
`adr_review_evidence.py` (adr-writer). The division-of-labor principle is "existence = code, content = LLM":
the script measures, the LLM interprets.

## 0. Entry — checklist-first vs history-first

If the target reviewer is already decided, go straight to §1. If you are deciding "which reviewer / which convention should be linted,"
mine the reviewers' history. A checklist-first inventory surfaces only the items a reviewer **holds in writing**,
so it misses findings that actually recur (measured 2026-08-29: a checklist-first sweep covered only the
document / skill-asset layer and missed 3 recurring classes targeting `hooks/*.sh`).

**Build no mechanism** — create neither an extraction script nor a collection hook; mining is rare enough that a standing
mechanism costs more than it returns. One manual investigation is enough. If a second one is requested, propose a
script then, for the author to approve.

Non-obvious points about the corpus and extraction:

- Reviewer reports are at `~/.claude/projects/<project>/<session-id>/subagents/agent-*.jsonl`.
  **Not next to the parent transcript**
- Identify the reviewer type from the subagent's first user message. There is no `agentType` field, and
  it is not linked to the parent transcript by id (match the final assistant text against the parent's tool_result)
- The built-in `/code-review` signature is `` `medium effort → 3+5 angles × 6 candidates …` ``
- Take the final assistant **message**. `jq | tail -1` takes only the final **line**
  (each file is 100–450KB, so the whole thing cannot be read)
- The structured tool_use of `ReportFindings` is not saved. Extraction becomes natural-language parsing

**Fix the thresholds before mining.** Class granularity is a free variable; cut finely enough and you can always produce a
"class not in the ledger." Defaults: the same class **3 or more times across 2 or more sessions**, **at least 1 adoption**,
and **classes coming only from retired reviewers do not count** (that reviewer no longer runs, so there is no demand).

There are two destinations. **Repeated adoption → lint candidate** (go to §1); **repeated rejection → retirement candidate** (a hollowed-out convention,
or a misaligned reviewer remit. Linting it would make the false positives permanent).

## 1. Inventory and 3-way classification (the core of this skill)

Classify the target reviewer's checklist one item at a time. Criteria:

| Class | Input to the judgment | Destination |
|---|---|---|
| **deterministic** | structure, format, existence, consistency (presence of sections, enums, date format, link resolution, index drift, naming conventions, consistency of cross-references) | script |
| **semantic** | intent, fidelity, two-sidedness, validity (post-hoc justification, straw men, one-sided Consequences, correspondence between claims and evidence) | stays with the reviewer |
| **hybrid** | the script counts, the LLM interprets (the fixed target of a count condition, the denominator of a figure, the distribution of term occurrences) | the script outputs evidence, the reviewer interprets it |

When unsure, lean to semantic — a wrongly mechanized item lets false negatives through wearing the face of "checked."

## 2. search-first cross-check

Before writing, look for external lint tools and existing evidence scripts in the harness (`skills/*/scripts/`).
If an existing one can check the target corpus **without migration**, do not write one. If migration is needed, compare the migration cost with
the cost of building your own, and record the reason for rejection.

## 3. Script design

- Location: under the writer skill for that domain, `skills/<owner>/scripts/` (a single source of truth that works
  cross-repo). A uv sub-project (pyproject + tests, auto-discovered by verify.sh full)
- The default is **evidence mode**: output JSON, make no judgment, exit 0. "evidence, not a verdict" —
  the judgment belongs to a fresh-context judge / reviewer. Add `--gate` only when blocking is needed
- **Measure the exemption boundary first**: run it against every item in the existing corpus and count violations before deciding on prefix checks,
  number/date boundaries, and automatic adaptation to repo-local conventions (reading expected values from the canonical doc).
  A lint that turns the gate red on day one is a design error in the exemption boundary
- Leave the measured grounds for each detection pattern (how many hits in which repo) in a comment

## 4. Thinning the reviewer

- Delete the mechanical items from the checklist and wire in a Step 0 at the top: "run the script → copy the JSON's
  deviations into findings → do not recount by eye → put attention on the semantic checks"
- Keep the instruction to read the target repo's local conventions (the canonical template doc) — write the reviewer on the assumption that
  conventions differ per corpus
- **Examples** of frequent findings go to a catalog in `references/` with dates and commit references (wired into the writer skill's
  prevention at writing time). The reviewer remains the source of truth for the **criteria** — do not duplicate examples and criteria

## 5. Execution coordinates

Decide the location on 2 axes:

- **Tax rate** — the fraction of commits for which the check is meaningful. If low, a step in the writer skill / reviewer;
  if high, the repo's `verify.sh`
- **Off-the-shelf fit** — if a config line for an off-the-shelf tool is enough, `verify.sh`.
  For a self-written script, the skill-step side is the default

The default is the skill-step side — always-on wiring into a commit hook / verify.sh taxes every commit,
including commits that do not touch the target.

**Exception: targets with no canonical writer skill.** Executable assets such as `hooks/*.sh` have no writer skill
equivalent to adr-writer / the author's README skill, so the coordinate "skill step"
does not exist in the first place. In this case `verify.sh` becomes the default.

If hollowing-out is observed, revisit the wiring on the commit surface. Hold no aggregation, viewer, or grader agent
(each one is another asset to keep alive with no demand behind it).

## 6. Recording

Record — in an ADR when it meets adr-writer's filing bar, otherwise in the commit body: the code/LLM boundary (which items go where), overlaps with existing checks and the grounds for why they will not
drift, the measured values of the exemption boundary, and the reasons for rejection in search-first.

## Choosing the next target

Take candidates one at a time in separate sessions. Decide priority by demand — a clear current need on a stable
canonical source — not by room for mechanization; a lint built ahead of demand hollows out.
Skip targets that are already done or need no script: the author's README skill and adr-writer already have evidence scripts;
security-reviewer already delegates to existing gates; `scripts/hooks/harness_lint.py` covers rules-stocktake's mechanical
checks; llm-as-judge and skill-health are the reference designs, not targets; a reviewer whose checks belong to an off-the-shelf
linter (e.g. SwiftLint for swift-reviewer) is thinned by delegating to that tool, not by writing a script.
