---
name: mutation-survivor-triage
description: Triage Stryker mutation testing survivors (mutation-report.json) into false negatives (log-only or metadata mutants with no observable behavior) vs real coverage gaps (mutants affecting return values, thrown errors, persisted data, or side-effecting branches). Produces a per-file consolidated table of gaps with concrete test recommendations, and maps false negatives to Stryker's native suppression mechanisms (disable comments, mutate globs). Use when user says "triage mutation survivors", "review Stryker report", "why did these mutants survive", "reduce mutation testing false negatives", or shares a Stryker JSON or HTML report asking what to fix.
metadata:
  author: Ronnasayd Machado - github.com/Ronnasayd
  version: 1.1.0
---

# Mutation Survivor Triage

Classify Stryker survivors into false negatives (no test should reasonably kill them) vs real gaps (untested behavior). Core question per cluster: **is the mutated value's output ever asserted on, directly or indirectly?** Deliverable is a table (file, line, gap, test), not narrative.

## Workflow

| Step             | Action                                                                                                                                                                                                    | Output/Gate                                    |
| ---------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ---------------------------------------------- |
| 1. Locate        | Find `reports/mutation/mutation.json` (check `stryker.config.mjs` `jsonReporter`/`htmlReporter` path if not default). Check if config already uses `mutate` globs for exclusion — reuse that idiom later. | report path + existing exclusion idiom         |
| 2. Rank          | `jq -r '.files \| to_entries[] \| {file: .key, survived: [.value.mutants[] \| select(.status=="Survived")] \| length} \| select(.survived>0) \| "\(.survived)\t\(.file)"' mutation.json \| sort -rn`      | files ranked by survivor count, worst first    |
| 3. Group         | Per file: `jq -r --arg f "<file>" '.files[$f].mutants[] \| select(.status=="Survived") \| "\(.mutatorName)\t\(.location.start.line)"' mutation.json \| sort \| uniq -c \| sort -rn`                       | clusters by mutator+line                       |
| 4. Read context  | Read ~5-10 lines around each cluster location                                                                                                                                                             | know what's mutated + where output flows       |
| 5. Classify      | See classification table below                                                                                                                                                                            | each cluster tagged false-negative or real-gap |
| 6. Flag security | Redaction lists, env branching (prod/dev), auth-state flags → always real gap even if "just config"                                                                                                       | security-flagged gaps called out               |
| 7. Note repeats  | Same guard-clause/state-check shape across methods → one gap _class_, not N incidents                                                                                                                     | repeated-pattern note                          |
| 8. Summarize     | One row per real gap: file, line, gap, concrete test (e.g. "call with valid redirectUri to cover refine's success branch")                                                                                | consolidated table                             |
| 9. Suppress      | See suppression table below                                                                                                                                                                               | suppression recs per false-negative cluster    |
| 10. Repeat       | Next file by rank until list exhausted                                                                                                                                                                    | full checklist                                 |

Work top-down by rank (step 2) — a large count in one file is usually one repeated pattern, not N bugs; confirm before assuming otherwise.

## Classification

| Signal                                                                                                                                                | Verdict                                                                                                         |
| ----------------------------------------------------------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------- |
| Only feeds logging/telemetry (`logger.info(msg, {field})`, a `duration` only used in a log line, a ternary picking a log message)                     | False negative — unless log content itself is a requirement (audit/security logging)                            |
| Doc/metadata annotation, no runtime effect (e.g. `.openapi("Name")` on a schema)                                                                      | False negative — verify it's truly metadata-only first                                                          |
| Affects return value, thrown error, persisted data, or a branch gating a side-effecting call (`next(err)`, business guard, default on created entity) | Real gap — name one test that kills it                                                                          |
| File under test _is_ the logging implementation itself (e.g. `LoggerAdapter`)                                                                         | Inversion — call-signature conditionals, redaction config etc. are real gaps here, "just logging" doesn't apply |

## Suppression (for false negatives)

| Situation                                                   | Mechanism                                                                                                   |
| ----------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------- |
| Single mutant/block                                         | `// Stryker disable next-line all` or `// Stryker disable all` … `// Stryker restore all`                   |
| Pattern copy-pasted across many call sites                  | Extract shared helper first, then disable-comment once at the helper (dedup is a side effect, not the goal) |
| Config already uses `mutate` globs for file-level exclusion | Reuse that same idiom for consistency, don't introduce a second mechanism                                   |

## Reference files

- `references/example-and-troubleshooting.md` — worked example triage run + jq/report-path error fixes
