---
name: sci-select
description: "Use when a user needs SCI/SCIE/ESCI/SSCI journal-submission help: evidence-backed candidate-journal discovery from a title, abstract, keywords, or manuscript text; public-metric and risk lookup for a known journal; or a pre-submission compliance check of a draft against a chosen journal's Author Guidelines and same-journal conventions. Also for Chinese requests such as 选刊、投稿期刊推荐、期刊查询、中科院分区、投稿前检查、期刊要求核对. This skill produces candidates, evidence, checks, and uncertainty; it does not judge research quality, predict acceptance, choose a uniquely best journal, draft prose, or simulate peer review."
---

# sci-select

Use sci-select to reduce journal-search and submission-checking uncertainty. The researcher remains responsible for research design, manuscript quality, target choice, and the final submission decision. Provide candidates, source-backed observations, reproducible checks, and explicit uncertainty—never substitute them for scholarly or editorial judgment.

## Mode routing

- **Candidate discovery** — The user provides a title, abstract, keywords, or excerpt and wants journals to investigate. Use the workflow below.
- **Known-journal lookup** — The user names one or more journals and wants public metrics, coverage, or risk flags. Query those journals directly; do not force a recommendation.
- **Pre-submission review** — The user provides a chosen target journal and a draft and asks about requirements, readiness, or same-journal conventions. Read `references/presubmission-review.md`; default to Quick Check.
- **Both** — Discover first. Start the pre-submission review only after the user chooses a target journal.

Do not automatically broaden the research question, add adjacent disciplines, choose a new target, or turn a request into a manuscript review. Ask before a meaningful scope expansion. Treat stated filters as hard filters only when the user explicitly asks to exclude; otherwise report them as preferences and expose missing data.

## Non-negotiable academic boundary

- Do not judge novelty, methods, data, figures, writing quality, peer-review readiness, or acceptance probability from an abstract or a full draft.
- Do not label venues `冲刺`, `主投`, `稳妥`, `保底`, guaranteed, or uniquely best. Journal level is objective venue metadata, never a claim that the manuscript is suitable or safe to accept.
- Do not use IF, JCR, CAS, XinRui, a journal name, or broad category as a proxy for scope fit. Never let metrics outrank publication precedents or verified scope.
- Do not invent requirements from publisher-wide defaults, bypass logins, CAPTCHAs, paywalls, or access controls, or present a third-party summary as an official rule.
- When evidence is absent, say `待核验` / `Unable to assess`, explain why, and state the smallest useful human verification step.

## Candidate discovery workflow

1. **Build a manuscript fingerprint.** When text beyond a title is available, create a profile grounded only in supplied content: field, specialty, object, question, contribution, audience, method role, exclusions, and two or three discriminative queries. Read `references/paper-profile.schema.json`. Keep Chinese output natural, but make matching terms English or bilingual. Do not promote a method to the field unless the contribution is methodological. Use `infer_paper_profile(text)` only as a documented fallback.
2. **Retrieve independently.** Use recent OpenAlex similar works and the local specialist-title channel as separate recall paths. Normalize similar-paper evidence by the journal's recent output, favor repeated topical precedents, and never claim that a failed lookup means no similar work exists. Use LetPub category recall only when recall is thin or the user supplies categories.
3. **Aggregate metrics without filling gaps.** Use the bundled or user override index for stable title-keyed fields, and live sources only for their stated fields. Read `references/data-sources.md` for source authority, current-year labels, and conflict handling. Do not infer a missing IF, coverage type, partition, OA/APC, or warning status.
4. **Verify leading scopes.** For the final three to five, compare the fingerprint with official aims-and-scope text and accepted article types when legally available. An official URL must belong to the journal or publisher. Aggregators, search snippets, Finder suggestions, and memory are not official scope evidence. If exact-script comparison is impossible, leave the result unresolved.
5. **Rank evidence before metrics.** Use this order: (a) recent same-topic publication precedents, (b) official scope and article type, (c) fine-grained topic/audience match, (d) broad category, (e) metrics. A venue supported only by name, category, or metrics is provisional at most.
6. **Report, do not decide.** Preserve multiple scope-supported levels and make weak recall, profile disagreement, source gaps, and unverified scope visible. If two independent profiles are available, compare them without sharing outputs; retain alternative queries on disagreement rather than forcing consensus.

Use official publisher Journal Finders only when the user requests a manual cross-check or recall remains weak. Provide links and copy-ready text; do not automate login or make Finder results part of default scoring.

## Evidence and source-status contract

For every material source used or considered, expose a compact `source_status` entry with `status` and `reason`:

| Status | Meaning |
|---|---|
| `succeeded` | The check completed; `reason` states usable evidence or `no matching record`. |
| `partial` | Some usable evidence was returned, but named fields, pages, or sample depth are incomplete. |
| `attempted` | A check was made but failed or produced unusable evidence; give the failure reason. |
| `skipped` | The source was intentionally not queried; state why (for example, Quick scope, no key, or higher-priority evidence already available). |

Never collapse “not found” into “not checked”: a completed no-match is `succeeded` with that reason; a failed request is `attempted`; an intentional non-query is `skipped`. Existing API fields such as `_sources`, `_source_errors`, and `_skipped_sources` remain compatible; the machine-readable map is `_source_status`.

Report only statuses material to the conclusion. A source status records retrieval state, not a quality score or a substitute for reading the evidence. If a source returned a record missing a requested field, say `partial` and name the field; do not list the source as fully checked.

## Known-journal lookup handling

1. Resolve the journal identity with title and ISSN when supplied; do not merge an incompatible ISSN/title record.
2. Return the available IF, `2025中科院`, `2026新锐`, coverage, OA/APC, h-index, review-speed text, warning/status notes, and `_source_status` reasons.
3. Label unconfirmed current coverage `收录需复核`. Distinguish a missing metric from a failed source request.
4. Compare named journals only on disclosed evidence and stated preferences. Do not turn a metric comparison into a recommendation, ranking, or acceptance forecast.
5. Read official scope only when the user asks about fit or comparison; report it separately from metric data.

## Minimum output contract

For each candidate, provide:

- status: `优先核验`, `可选`, `谨慎`, or `排除`; keep legacy internal tiers only for API compatibility;
- fit confidence (`强`/`中`/`弱`) and a concrete fit reason;
- up to three recent same-topic precedents, or the reason they are unavailable;
- official-scope status (`已核验`, `已读取待判断`, or `待核验`) and official URL when read;
- journal level (`高位`, `中位`, `常规`, or `待定`) based on current partition/JCR evidence, separately from fit;
- available metrics: IF, `2025中科院`, `2026新锐`, coverage, review-speed text, h-index/OA/APC;
- risks, conflicts, missing fields, and source-status notes.

Begin with the supplied constraints. If none were supplied, proceed under the default evidence-first workflow and end with one short refinement hint (for example IF/JCR range, `2025中科院`, `2026新锐`, coverage, OA/APC, warning exclusion, review speed, or count). Do not block on a long intake form.

Keep machine-readable fields and human-facing labels separate. API compatibility fields may retain legacy values; user-facing language must preserve the boundaries above.

For a known journal, report only available metrics, current-coverage caveats, risk flags, and source status. For “is my paper good enough?”, state the boundary and offer only scope/metric fit plus the separate review dimensions a researcher must assess.

## Pre-submission review

Read `references/presubmission-review.md` whenever the target and draft are known. Quick Check verifies only official-or-pasted requirements, essential counts/items, obvious missing statements, and clear format risks; it does not benchmark style, rewrite text, or predict acceptance. Escalate to Full or same-journal analysis only on request or after naming the specific uncovered need.

When guideline retrieval fails, read `references/guidelines-fallback-matrix.md` for the fallback sequence and evidence acceptance rules. When a result could be misleading, sparse, or improperly inferred, read `references/pitfalls-and-solutions.md` before reporting. Treat third-party guidelines and search snippets as tentative only; they cannot support a confirmed P0.

## Direct resource routing

- `references/paper-profile.schema.json` — profile fields and validation before candidate discovery.
- `references/data-sources.md` — runtime source authority, current-status rules, and conflict/missing-data behavior.
- `references/presubmission-review.md` — Quick/Full review scopes, diagnostics, and output format.
- `references/guidelines-fallback-matrix.md` — only when official guideline retrieval is blocked, thin, or a hub page.
- `references/pitfalls-and-solutions.md` — only for pre-submission failure cases, sparse exemplars, or QA of a tentative finding.
- `references/index-maintenance.md` — only when building, refreshing, auditing, or packaging a local journal index.
- `references/common-mistakes.md` — only for a deeper candidate-report QA pass.
- `references/benchmarking.md` — only when running or publishing a benchmark; never claim accuracy before complete independent expert labels.

Load only the resource needed for the active mode or failure. Do not follow a reference citation recursively unless that file is directly listed above or the task cannot proceed without it.

Prefer a short evidence summary over copying source text. Preserve URLs, source type, status, and reason so a researcher can reproduce or challenge the conclusion.

Keep API details, index construction, development tests, and benchmark operations out of normal task context. Preserve their existing scripts and compatibility; load the relevant reference or inspect the script only when that operation is requested.
