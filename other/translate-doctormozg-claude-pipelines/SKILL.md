---
name: translate
description: 'Translates docs and i18n resources into another language. Use when the user says "translate X to Y" or "localize", or wants files or docs in another language. Not for one phrase or sentence (answer inline) or same-language rewording (use naturalize).'
argument-hint: <natural language request — e.g. "translate README.md to Russian" or "translate locales/en.json to fr mode:i18n">
allowed-tools: Agent, Bash(git rev-parse *), Bash(git symbolic-ref *), Bash(git merge-base *), Bash(git diff *), Bash(git ls-files *), Bash(mkdir *), Bash(date *), Bash(rg *), Bash(awk *), Read, Write, Edit, Glob, Grep, TaskCreate, TaskUpdate, TaskGet, TaskList, TaskStop, AskUserQuestion, WebFetch
---

# Translate & Localize Pipeline

## Overview

Orchestrates a plan-approve-translate-verify flow for translating documents, READMEs, and i18n resources. Discovery produces a reviewable plan; an approval gate blocks every dispatch until the user confirms; parallel `pipeline-translator` waves produce output with Tier-1 structural checks inside each agent; an LLM-as-Judge sweep runs Tier-2 semantic review across all chunks; uncertainty-driven Tier-3 probes (Wiktionary, MyMemory, back-translation) spend budget only on chunks the earlier tiers flagged. Verification is always on.

## When to Use

Translating or localizing documents, READMEs, docs directories and i18n resource files into another language. Supported formats: `md`, `mdx`, `json`, `yaml`/`yml`, `po`, `properties`, `strings`, `xliff`, `txt`.

### When NOT to use

- A single phrase or sentence — answer inline, do not orchestrate a pipeline.
- Rewording text that stays in its language — use `naturalize`.
- Code comments or string-literal polish — use the `polish` skill.
- Live machine-translation chat — out of scope for a file-oriented pipeline.
- Binary formats (`.docx`, `.pdf`, images) — unsupported; escalate via AskUserQuestion.

## Input

`$ARGUMENTS` is a natural-language request. Accepted forms: `translate <path> to <lang>` and `translate <path> to <lang> mode:<sidecar|inplace|i18n>`. There is no verification opt-in flag in the grammar — tiered verification is always on and its fixed cost is shown to the user at the approval gate. Source language defaults to auto-detect; output mode defaults to `sidecar`. Empty or ambiguous arguments escalate via AskUserQuestion — never guess.

## Scope Parameter

See `<PLUGIN_ROOT>/shared/scope-parameter.md` for the canonical scope modes (`branch`, `global`, `working`) and their git commands. Document any skill-specific overrides or restrictions below this line.

- **Default**: if `$ARGUMENTS` contains path tokens or globs, those paths define the scope; if no path tokens are present, default to `global` (all eligible files in the repo).
- `scope:working` is an explicit opt-in for translating only uncommitted changes — useful for iterating on a draft, but rarely the right default for docs that are usually committed.
- `scope:branch` limits translation to files changed on the current branch vs base.
- `scope:global` translates all eligible project files; discovery excludes vendored, generated, and binary files.
- Scope constrains **which files may be translated**; discovery may read the full project to resolve globs, detect formats, and seed glossary terms.

## Constants

- **PROJECT_ROOT**: resolved once in setup with `echo "${MZ_MEMORY_ROOT:-$(git rev-parse --show-toplevel 2>/dev/null || pwd)}"`; expand `<PROJECT_ROOT>` to it in every command and agent prompt.
- **MAX_PARALLEL_TRANSLATORS**: 6 | **MAX_CHUNK_LINES**: 500 | **MAX_VERIFICATION_ATTEMPTS**: 2 | **MAX_CONTEXT_RETRIES**: 1 | **MAX_APPROVAL_ITERATIONS**: 3
- **MAX_JUDGE_BATCH**: 6 (chunks per parallel judge dispatch)
- **MAX_WIKTIONARY_LOOKUPS**: 10 (per-run cap across all chunks)
- **MAX_MYMEMORY_QUERIES**: 9 (per-run cap, under MyMemory 5K-char/day free tier)
- **TASK_DIR**: `<PROJECT_ROOT>/.mz/task/`
- **SKILL_DIR**: `${CLAUDE_SKILL_DIR}`. Phase files write `<SKILL_DIR>/...` because files opened with Read get no variable substitution; expand it to this absolute path before reading a file, running a command, or passing a path to an agent.
- **PLUGIN_ROOT**: `${CLAUDE_PLUGIN_ROOT}`. Skill and phase files write `<PLUGIN_ROOT>/...` because files opened with Read get no variable substitution; expand it to this absolute path before reading a file, running a command, or passing a path to an agent.

## Core Process

### Phase Overview

| #   | Phase                                                                    | Reference                                | Loop?                           |
| --- | ------------------------------------------------------------------------ | ---------------------------------------- | ------------------------------- |
| 0   | Setup                                                                    | inline below                             | —                               |
| 1   | Discovery + planning                                                     | `phases/discovery_and_planning.md`       | —                               |
| 1.5 | User approval gate                                                       | inline below                             | re-plan on feedback             |
| 2   | Parallel translation + Tier-1 structural verification (inside agent)     | `phases/translation_and_verification.md` | wave loop                       |
| 3   | Cross-file consistency scan + glossary delta merge                       | `phases/translation_and_verification.md` | —                               |
| 4   | Tier-2 semantic verification (LLM-as-Judge, all chunks, wave-split)      | `phases/translation_and_verification.md` | bounded                         |
| 5   | Tier-3 uncertainty-driven verification (Wiktionary / MyMemory / back-tr) | `phases/translation_and_verification.md` | bounded                         |
| 6   | Bounded re-translation loop on chunks with `Critical:` findings          | `phases/translation_and_verification.md` | max `MAX_VERIFICATION_ATTEMPTS` |
| 7   | Finalization + summary                                                   | inline below                             | —                               |

### Phase 0: Setup

- Resolve `PROJECT_ROOT` with the command in Constants, before any `cd` or worktree switch, and use it for every `.mz/` path below.
- Derive task name `<YYYY_MM_DD>_translate_<slug>` where `<YYYY_MM_DD>` is today's date (underscores) and `<slug>` is a snake_case summary of the raw argument (max 20 chars); on same-day collision append `_v2`, `_v3`.
- Create `TASK_DIR/<task_name>/` on disk.
- Write initial `state.md` with, in order: `schema_version: 2` (first line), `Status: running`, `Phase: setup`, `Started: <ISO 8601>`, `phase_complete: false`, `what_remains: []`, `approval_iterations: 0`.
- TaskCreate a top-level task for the run so progress is visible to the user.

### Phase 1: Discovery + Planning

Read `phases/discovery_and_planning.md` at phase entry and run steps 1.1 through 1.8 in order. Output: `<task_dir>/translation_plan.md`, `<task_dir>/discovery.md`, `<task_dir>/glossary.json`. State → `discovery_complete`.

### Phase 1.5: User Approval Gate

**This orchestrator** (not a subagent) presents this gate. This step is interactive and must not be delegated. Full detail in `phases/discovery_and_planning.md` under `Phase 1.5`; the load-bearing elements are:

- **Pre-read**: Read `<task_dir>/translation_plan.md` with the Read tool. Capture the full contents (files, languages, output mode, seeded glossary summary, verification cost block, wave plan, and any `INPLACE_DESTRUCTIVE` flags) into context.

- **State**: write `state.md` with the artifact path and `what_remains: [awaiting approval: plan gate]`; `Status` stays `running`.

- **Surface 1 — emit the plan message.** Output the artifact verbatim as a normal markdown chat message. Emit the full verbatim contents of `<task_dir>/translation_plan.md` — do not substitute a path, summary, or placeholder:

  ```
  ## Translation plan ready for review — translate

  <verbatim contents of <task_dir>/translation_plan.md>

  ---
  **Approve** → proceed to Phase 2 (parallel translation and Tier-1 verification)  ·  **Reject** → task marked aborted, no files written  ·  reply with feedback to revise
  ```

- **Surface 2 — call AskUserQuestion.** A short selector — do not re-embed the plan in the question body:

  - question: `The translation plan above is ready for review.`
  - header: `Plan`
  - options: **Approve** — proceed to Phase 2 (parallel translation and Tier-1 verification) · **Reject** — task marked aborted, no files written

- **Approve** → add `- plan approved: .mz/task/<task_name>/translation_plan.md` under `## Decisions` in `state.md`, remove the `awaiting approval` entry from `what_remains`, set `Phase: plan_approved`, and proceed to Phase 2.

- **Reject** → state `aborted_by_user`, stop. Do not proceed.

- **Any other reply (feedback)** → re-run affected Phase 1 sub-steps, overwrite the plan, return to this gate, re-read `<task_dir>/translation_plan.md`, re-emit the entire plan message from scratch with the full new contents, re-present the selector. Increment `approval_iterations`; bounded by `MAX_APPROVAL_ITERATIONS`. This is a loop — repeat until the user explicitly approves. Never proceed to Phase 2 without explicit approval.

- **No answer** → set `Status: blocked`, keep `awaiting approval: plan gate`, stop. A missing answer is never approval.

- **Cap reached** → when `approval_iterations` reaches `MAX_APPROVAL_ITERATIONS`, follow the escalation branch in `phases/discovery_and_planning.md` Phase 1.5 "Iteration accounting" — it is the single source of truth for the three-choice escalation (abort / approve as-is / one final narrow revision with counter reset). Do not re-state the logic here; the phase file owns it.

### Phases 2–6

Read `phases/translation_and_verification.md` on entry to Phase 2 and keep it loaded through Phase 6. Each phase ends with a state transition:

- **Phase 2** — parallel `pipeline-translator` waves, each running Tier-1 structural verification before returning. State → `translation_complete`.
- **Phase 3** — merge every `glossary_delta_<chunk_id>.json`, sweep for cross-file term drift, re-dispatch drifted chunks. State → `consistency_complete`.
- **Phase 4** — LLM-as-Judge on every chunk via `ceil(total_chunks / MAX_JUDGE_BATCH)` parallel `pipeline-code-reviewer` dispatches. State → `judge_complete`.
- **Phase 5** — Tier-3 only on chunks flagged uncertain or carrying a Tier-2 `Critical:`. Wiktionary and MyMemory bounded by their constants; back-translation only on chunks with a Tier-2 `Critical:`. State → `deep_verify_complete`.
- **Phase 6** — bounded re-translation on chunks with an unresolved `Critical:` finding, capped per chunk by `MAX_VERIFICATION_ATTEMPTS` shared with Phase 3.3 consistency re-dispatches. Phase 2.2 `NEEDS_CONTEXT` re-dispatches use a separate per-chunk `MAX_CONTEXT_RETRIES` counter. State → `retranslation_complete`.

### Phase 7: Finalization

- Write `<task_dir>/summary.md` per the Phase 7.1 shape in `phases/translation_and_verification.md`.
- Set `Status: complete`, `Phase: complete`, `phase_complete: true` and `what_remains: []` in `state.md`, and record `ended_at`, `final_outputs`, `escalations`, `phase_history`, `tier3_ledger_path`.
- Print the summary block to the user as the terminal orchestrator message.

## Common Rationalizations

| Rationalization                               | Rebuttal                                                                                                                                    |
| --------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------- |
| "skip the plan gate, it's just a translation" | "sidecar vs inplace is the difference between a review diff and a destroyed original; the gate costs seconds and prevents days of cleanup." |
| "LLM translation is good enough, skip Tier-1" | "an LLM will silently drop `{{user.name}}` and your app will crash in production; `grep -c` costs nothing."                                 |
| "only judge the headings; skip full Tier-2"   | "the prioritized rubric already front-loads headings — the rest of the chunk is judged in the same pass; the savings are illusory."         |

## Red Flags

- You dispatched translators without user approval.
- You used `mode:inplace` without showing the destructive warning.
- You marked a chunk `DONE` without running Tier-1 verification.
- You skipped Tier-2 on any chunk (judge must run on every chunk).
- You ran Tier-3 on every chunk instead of only those flagged uncertain.

## Verification

On completion, print the summary block from `<task_dir>/summary.md` covering files translated, Tier-1 pass/fail, Tier-2 verdicts and finding counts, Tier-3 lookup counts (`<used> / MAX_*`), glossary seeded/added/conflict counts, Phase 6 re-translation count, and every `DONE_WITH_CONCERNS` chunk surfaced for human review.

## References

- `${CLAUDE_SKILL_DIR}/references/language-codes.md`: ISO 639-1 normalization table, regional-variant collapse, script-based language detection and the anti-injection allow-list. Grep it in Phase 1 for the row or section a target or source token needs.
- `${CLAUDE_SKILL_DIR}/references/markdown-preservation-rules.md`: what a translator may and may not rewrite in Markdown (never and always translate tables, frontmatter, code fences) and the Tier-1 structural parity checks. Grep it for the element type a chunk contains.
- `${CLAUDE_SKILL_DIR}/references/placeholder-patterns.md`: regexes for i18n and format-string placeholders by framework, plus the combined ripgrep recipe and substitution strategy. Grep it for the framework section a chunk uses; translators do this in Phase 2.

## State Management

State persists to `.mz/task/<task_name>/state.md` under the project root, `${MZ_MEMORY_ROOT:-$(git rev-parse --show-toplevel 2>/dev/null || pwd)}`, resolved once at the start of the run. Schema is **v2**: line 1 is `schema_version: 2`; line 2 is `Status:` with one of `pending`, `running`, `blocked`, `complete`, `aborted_by_user` or `failed`, lowercase and unquoted; then `Phase`, `Started`, `phase_complete` (boolean) and `what_remains` (YAML list of strings), with skill-specific keys below them. Milestones go in `Phase`; the reason for `blocked` or `failed` goes in `what_remains`. Set `phase_complete: false` on phase entry and `true` once the phase's artifacts are written and its gates pass. Refresh `what_remains` on every phase transition; it is `[]` when `Status` is `complete`. Write the file after every phase and before every gate, and re-read it after compaction. Record decisions worth recalling under a heading that reads exactly `## Decisions`, placed before `## Notes`; mz-memory harvests them only once `Status` is `complete`. Under a heading that reads exactly `## Lessons`, add one line whenever a review finding is accepted and fixed, a step fails, gate feedback corrects a mistake, or an approved approach is reversed, in the form `- (review|failure|correction|change) WHEN <situation> → <what to do> — WHY <cause>`, concrete and under about 40 words; mz-memory harvests lessons whatever the `Status`. Treat a legacy `completed` as `complete`. On reading a `schema_version: 1` or unversioned file, put `schema_version: 2` on line 1 and `Status` on line 2, add the missing keys, and log the upgrade. Leave a file with a higher `schema_version` untouched: ask whether to Restart (archive it), start New (`_v2`) or Abort, and stop if nobody can answer.
