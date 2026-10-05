---
name: codexqa-rootcause-analyzer
description: >
  Diagnoses exception root causes from stack traces, logs, call-chain dumps,
  and debug output using the CodexQA CLI for structured repo analysis. Use when
  the user mentions codexqa-rootcause-analyzer, exception RCA, crash analysis, AI code
  diagnosis, stack diagnosis, 异常根因, 堆栈诊断, 崩溃分析, 异常诊断, or asks to
  turn an exception into a root-cause report. Not structure/impact analysis
  (that is codexqa-code-analyzer), not SAST + Agent LLM Detection code-risk scan reports (that is
  codexqa-defect-analyzer), and not CodexQA evidence-pack HTML review (that is codexqa-code-reviewer).
  Former skill name: root-cause-diagnosis.
license: Apache-2.0
compatibility: >
  Requires Node.js 22+ and git on PATH when cloning remotes. Talks to the
  `@openqa-cn/codexqa` CLI via npm (`codexqa` binary only); do not copy engine
  or skill source. Task data lives under this skill's `data/` directory.
metadata:
  author: open-source
  version: "0.0.1"
  open-standard: agentskills
---

# Root Cause Diagnosis

Turns exception evidence into an **English** root-cause report. Structured understanding of the business codebase comes from the CodexQA CLI; this skill diagnoses **on top of** that analysis.

CLI: `node {baseDir}/scripts/diagnose.ts` (`$SKILL_SCRIPT`). Task data: `{baseDir}/data/{taskId}/`.

`README.md` / `README.zh-CN.md` / `HOW_IT_WORKS.md` / `KNOWN_LIMITATIONS.md` (and their `.zh-CN` twins) are human-facing. Do not load them at runtime.

## Boundaries

| Need | Skill |
|---|---|
| Symbol-graph change impact, callers, test gaps, entry risk | `codexqa-code-analyzer` |
| Exception RCA from stacks/logs on top of CLI analysis | **this skill** |
| SAST + Agent LLM Detection → `report_scan.*` | `codexqa-defect-analyzer` |
| CodexQA evidence-pack + Agent LLM judgment → bilingual `REVIEW-REPORT.html` | `codexqa-code-reviewer` |

## Split of work

| Layer | Owns |
|---|---|
| TypeScript (`draft-report`) | First-level English headings, extracted facts (`facts.json`), mechanical `storyGaps` |
| Model | Report narrative inside those headings, using only cited facts |
| TypeScript (`write-report`) | Reject missing headings and story gaps. Do **not** reject on section length |

Do **not** put exception-class fix wording in `scripts/draft_report.ts`. Mechanical defects stay in TypeScript; causal truth in this business domain stays with the model.

## Happy path

`run` is seconds. Wall-clock is LLM round-trips. Do **not** load `references/`, other skills, `--help`, or `scripts/*.ts` before `run`. Do not invent `Class#search:1` for `→ Class` tails. Do not count 字 or trim to a hint.

1. Collect exception evidence and the code location. Write an exception file if needed.
2. One process: `run` (or `submit --with-analyze`) with `--exception`/`--exception-file` plus `--git`/`--branch`, `--file`, or `--dir`. Bare flags without `run` still run. Uploaded files and non-git folders are copied into `data/<taskId>/repo` and git-inited **there only**. Do not invent a git remote. Do not `git init` in the user's original path.
3. `run` writes `brief.json`, `facts.json`, and a heading-only `report.draft.md`. It does **not** author or persist `report.md`. `parse-exception` is already done; skip unless `parsed.json` is missing.
4. If stdout has `facts` / `factsPath`, fill `report.draft.md` from `facts.json` in one pass (Report rules below). If `codexqa.ready=true` and `brief` exists but facts are missing, `draft-report --task-id` then fill. Do **not** read `analysis.json` when `brief`/`facts` exist. Do **not** open `~/.codexqa/`.
5. `write-report --from-draft`. If stdout has `storyGaps`, edit the draft **once** from that output and retry. Do not retry to shrink length.
6. Show **one English paragraph** from stdout `chat.en` (the first line of Executive summary) plus paths to `report.md` / `report.en.md` / `report.html`. If `chat.en` is empty, use that summary line. Do not paste the full document.
7. Observe stdout/meta `timings` after every CLI step. If a step is abnormally slow, diagnose that delay and fix it before continuing RCA.
8. Skill defects (mandatory): if a step is wrong, truncates, skips a rule, or is flaky, **first encode the rule in TypeScript** (`scripts/*.ts` + `tests/*.test.ts`) so later `run`s cannot regress. Keep an Agent-only note in this file only when the check cannot be decided without an LLM (for example: whether a causal sentence is *true* in this business domain). After the TS fix, re-`run` or `draft-report` before filling the report.

Abbreviated class-only `→ Foo` frames expand to hinted types ending with `Foo` before staying weak.

## Report rules (mandatory)

English Markdown only. Same eight `##` headings as [references/report-template.md](references/report-template.md). No extra top-level headings. Do not write a Chinese report.

The **Target** column is a prompt hint for the model, not a `write-report` reject. Keep the report complete even if a section exceeds the hint.

| Section | Target (hint) | Must contain |
|---|---|---|
| Executive summary | 100 | what failed, in-repo root, literal `Confidence: high\|medium\|low` |
| Symptom and exception facts | 100 | type, message gist, primary `Class#method:line` |
| Mapped call path | **300** | entry → each hop → extracted branch then-call → throw; mark weak frames |
| Root cause | **300** | earliest wrong contract in *this* repo, why that path ran; cite `Class#method`. Include race/contend **only** when `facts.raceEvidence` is true |
| Trigger | 100 | throw site; not the root cause |
| Contributing factors | 100 | factors grounded in `facts` (`swallowKey`, `evidenceGaps`); do **not** invent swallow / race / weak-frame claims |
| Suggested fix and verification | 100 | one fix + one verify; do not apply code |
| Confidence and gaps | 100 | use `facts.confidence` (`high`/`medium`); never write `Confidence: high` when facts say `medium`; one gap |

Mapped call path and Root cause must tell the story: entry, hops, branch, and throw. Mention race/contend **only** when `facts.raceEvidence` is true. Cite catch-all swallow **only** when `facts.swallowKey` is set. Mark `hypothesis` when `facts.lineDrift` is non-empty; do not invent line-drift or weak-frame claims without facts. A slogan or a bare `A→B→C` is invalid. Do not paste `facts.json` as the report.

When `facts.lineDrift` is non-empty, Root cause must mark hypothesis. Trigger must cite the throw class and say it is not the root. Root must cite the throw class and (if extracted) the branch else-call.

`write-report` `storyGaps` (edit the draft once if rejected):

| Gap | Section | Required text |
|---|---|---|
| `missing-confidence` | Executive summary | `Confidence:` |
| `confidence-overstated` | Executive summary | do not write `Confidence: high` when `facts.confidence` is `medium` |
| `mapped-missing-branch-then` | Mapped call path | `facts.branch.thenCall` |
| `mapped-missing-throw` | Mapped call path | throw class from `facts.throwKey` |
| `mapped-invented-weak` | Mapped call path | drop "weak frame" wording when `facts.weakCount` is 0 |
| `root-missing-branch-else` | Root cause | `facts.branch.elseCall` |
| `root-missing-throw` | Root cause | throw class |
| `root-missing-race` | Root cause | `raced`/`race`/`contend` — **only when** `facts.raceEvidence=true` |
| `root-invented-race` | Root cause | remove race/contend when `facts.raceEvidence` is false |
| `root-missing-hypothesis-on-drift` | Root cause | `hypothesis` when `facts.lineDrift` is non-empty |
| `root-invented-line-drift` | Root cause | drop line-drift claims when `facts.lineDrift` is empty |
| `contributing-missing-swallow` | Contributing / Root | cite `facts.swallowKey` (or swallow wording) when set |
| `contributing-invented-swallow` | Contributing / Root | drop swallow/catch-all claims when `facts.swallowKey` is null |
| `trigger-missing-throw` | Trigger | throw class |
| `trigger-missing-not-root` | Trigger | `not the root` (or `not root`) |

Citations: one `Class#method` (or file:line) per causal claim. No SQL dumps, no numbered evidence lists, no whole-class pastes.

Chat: one English paragraph + paths to `report.md` / `report.en.md`. Do not paste the full document.

## Entry

```bash
node "$SKILL_SCRIPT" run --exception-file "$PATH" --dir "$LOCAL_DIR"
# uploaded business file (non-git OK; stack sibling sources in the same folder are bundled):
#   node "$SKILL_SCRIPT" run --exception-file "$PATH" --file /abs/path/OrderService.java
# remote:
#   node "$SKILL_SCRIPT" run --exception "$TEXT" --git "$GIT_URL" --branch "$BRANCH"
# already-open IDE / cwd:
#   node "$SKILL_SCRIPT" run --exception "$TEXT"
# stepwise (debug only):
node "$SKILL_SCRIPT" submit --exception-file "$PATH" --dir "$LOCAL_DIR"
node "$SKILL_SCRIPT" ensure-codexqa --task-id $TASK_ID --with-analyze
# fill data/<id>/report.draft.md from facts.json, then:
node "$SKILL_SCRIPT" write-report --task-id $TASK_ID --from-draft
```

## Load order

Load each reference **at most once**, and **never before `run`**. Links from this file are one level deep.

| File | When to load |
|---|---|
| [references/workflow.md](references/workflow.md) | Stepwise debug, or `facts` missing after `run` |
| [references/codexqa.md](references/codexqa.md) | Before `ensure-codexqa` / `analyze-frames` when `run` did not index |
| [references/exception-parse.md](references/exception-parse.md) | Before interpreting `parsed.json` when `facts`/`brief` are missing |
| [references/report-template.md](references/report-template.md) | Before filling `report.draft.md`, only if Report rules above are not already in context |

## RCA rules

- Distinguish **trigger** (the throw), **root cause** (earliest incorrect state/contract in *this* repo), and **contributors**.
- Do not treat the last stack frame as the root cause.
- Every causal claim cites `Class#method` or file:line. Do not add extra evidence lists.
- Missing graph → hypothesis + how to verify. Never invent call edges.
- After a real `ensure-codexqa` attempt with `ready=false`, grep is allowed and evidence is **weak**.

## CodexQA (CLI only)

Install if missing: `npm install -g @openqa-cn/codexqa --registry https://registry.npmjs.org/`. Talk to the `codexqa` binary only (`index` / `query` / `stats` / `repos`). Do **not** copy engine or skill source into this skill. Details: [references/codexqa.md](references/codexqa.md).
