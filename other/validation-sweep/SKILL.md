---
name: validation-sweep
description: Project-wide regression sweep run as a follow-up after any issue is identified and corrected, to confirm no sibling issue remains anywhere in the repository. Invoke after fixes that touch multi-surface artefacts, gate inventories, prose claims about repository state, AI-inferred citations, or generated artefacts. Combines the mechanical audit suite with a structured semantic fan-out, and loops until clean.
derives_from: ../../governance/evidence-grounded-completion.md
---

# Validation Sweep

## Project wiring (the parent library's instantiation; adopters substitute their own)

Portable procedure, concrete names. In the parent GRC library this skill runs with:

- Canonical full-audit command: `tools/run_all_audits.sh`; canonical gate inventory: `governance/specification-audit-programme.md` §6.
- Sweep-history register: the sweep-history register in the consuming project's working state (one row per iteration).
- Per-iteration detail directory: the sweep detail directory in the consuming project's working state (filenames `YYYY-MM-DD-sweepN-iterM.md`).
- False-positive memory: the validation-sweep history README in the consuming project's working state, § Accept-list discipline (the human-readable surface), mirrored machine-readably by the scanner exemption file `tools/sweep-preflight-exemptions.json`.
- Deterministic pre-flight scanner: `tools/sweep-preflight-scanner.py`, with shipped pattern ids PF-01 / PF-02 / PF-03 for stale collection counts (skills, governance rules, generic `N <collection>`) and PF-04 for stale version literals; its `CANONICAL_COLLECTIONS` constants and seed patterns target this corpus.
- Document-staleness audit: gate 31 in the canonical inventory.
- Listing-surface coverage gate: gate 47 (the document-index register and the domain READMEs); the candidate-set helper is `tools/suggest-listing-surfaces.py <doc>`.
- Linter-exemption mechanism covering the detail directory: `DEFAULT_EXEMPT_DIRS` in `tools/lint_common.py`.
- Detailed change-log mirror (the surface the chat-surfacing section contrasts with): the detailed change-log mirror in the consuming project's working state.

An adopting project maps each bullet to its own records; the procedure below refers to them generically.

## Overview

After a single defect is found and fixed, a sibling defect may still be lurking elsewhere: same author, same session, same inferred mental model, same blind spot. The mechanical audit gates catch their own classes; this skill is the structured project-wide sweep that catches what the gates do not. It targets cross-file prose drift, mis-attributed citations, multi-surface incompleteness, inferred-as-verified state assertions, and the other failure-mode classes catalogued below.

The sweep is fixed-point: if it finds anything, fix it, then re-run the sweep, until the sweep returns clean. The audit gates are the ground truth for mechanical claims; the parallel subagent fan-out is the ground truth for the semantic claims the gates cannot mechanize.

The skill is project-agnostic in shape but invokes project-specific commands; the consuming project's canonical full-audit command and canonical gate inventory are named in the project wiring above. Slash-command names in this document (`/validate` for this skill, `/validate-pr` and `/retro` for its siblings) are the parent library's paired command names, used as shorthand; an adopting project reads them as its own equivalents.

## When to Use

- Immediately after identifying and correcting any issue in the repository, as a follow-up that confirms no sibling issue remains.
- When taking over from a previous session whose work has not been verified on the current state.
- After landing a PR that touched any "parallel surface" set: the gate inventory, a version-history table, a framework-alignment table, mirror-synced files, generated artefacts.
- Before declaring a multi-PR programme phase complete.
- Periodically, informed by the document-staleness audit (the project wiring names the concrete gate).
- Whenever a user surfaces an AI-introduced error and asks for assurance that no sibling error remains.
- When a scheduled mechanical sweep, where the project runs one (the deterministic half of this discipline, scheduled via CI on a cadence the project sets), reports a failure. A scheduled run catches time-dependent drift (citation freshness, document-date staleness, version-bump recency) when nobody has touched the content; pair the mechanical finding with the semantic triage step 4 fan-out runs.

## Process

The sweep runs in nine steps. Steps 1-3 establish the baseline and scope; steps 4-5 are the semantic sweep; step 6 triages; step 7 is the fixed-point loop that runs until clean; step 8 appends a row to the sweep history on every iteration; step 9 writes a per-iteration detail file only when the iteration produced findings.

### 1. Establish mechanical baseline

Run the canonical full-audit command standalone (named in the project wiring). Capture exit code and any failure output. The expected state is exit 0 on the current working tree.

If the audit reports failures, the sweep cannot proceed semantically until the mechanical baseline is clean. Address the gate failures first, then return to this step.

### 2. Enumerate recent changes

Identify the scope of recently-touched files. The focus window is a bound the project sets; the default is **the past two calendar days**: wide enough to span overnight handoffs, weekend work, and post-meeting reviews; narrow enough that the in-window set stays reviewable. A project on a different rhythm substitutes its own window and its own contextual history depth, and states the bounds it used when it reports the sweep.

- `git log --since="2 days ago" --name-only --pretty=format:""` : files touched in the focus window (substitute the project's window).
- `git status --short` : files in the current working tree.
- `git log --name-only -10` : files touched in the last ten commits, as additional context (substitute the project's depth).

These files are the highest-priority targets for the semantic sweep. Findings on files outside the focus window (i.e. on pre-existing issues the sweep surfaces incidentally) are still reportable and ARE handled by step 6, not silently discarded.

### 3. Identify failure-mode classes in scope

The sweep targets failure modes the mechanical gates do not cover. Each class has a known shape; new classes may surface as the project and its audit programme evolve.

| Class | Shape |
| --- | --- |
| Stale prose references | "N gates" or "gates 1-N" or "the N-gate programme" prose where N is no longer the canonical count; library, spec, or pack version mentioned in prose that has since bumped. |
| Mis-attributed citations | A citation of "step X" or "section Y" of another file where the cited content does not match the source; phrase-level quotes attributed to one rule but actually living in another. |
| Multi-surface incompleteness | A change that should update N surfaces but updated N-1: CHANGELOG entry coverage of files touched, README claims, governance registers, doctype-doctype cross-references. |
| Inferred-as-verified state assertions | A claim about a file's contents written without re-reading the file. |
| Per-document version-bump omission | A non-exempt document substantively changed but its `Version:` field not bumped. |
| Generated-artefact lag | A source file edited but its generator not re-run, or vice versa; the gates catch the drift but the underlying lag is the failure. |
| Stale docstrings | A linter or script docstring describing behaviour that no longer matches the code. |
| Cross-document term drift | Different files use different terms for the same concept, with no canonical glossary entry to anchor the choice. |

### 3a. Run the deterministic pre-flight scanner (optional but recommended)

Before subagent fan-out, run the project's deterministic pre-flight scanner (named in the project wiring). This is a deterministic regex-based pass that surfaces candidate findings for shapes the high-precision mechanical gates do not catch (stale skill counts, stale governance-rule counts, prose-form number drift). The scanner exits 0 always; its output is a list of candidates, not verified findings.

Pass the scanner's output to each subagent as a "known suspect locations to verify or dismiss" list. This lowers each subagent's discovery burden and guarantees candidate shapes the gates miss get semantic triage. Many candidates will be false positives (legitimate historical references, comparative prose, references to other projects' counts); that is expected: the scanner is high-recall, the subagent triage is the precision layer.

The scanner is project-specific (its canonical-collection constants and seed patterns target the consuming project's artefacts); a project adopting the validation-sweep pattern swaps in its own scanner with project-specific patterns.

The scanner's pattern set is extensible. The shipped patterns cover stale collection counts (a stale skill count, a stale governance-rule count, a generic `N <collection>` count) and stale version literals (a prose phrase asserting a current version that no longer matches any canonical version surface); the parent library's concrete pattern ids are listed in the project wiring. The stale-version-literal pattern was added after a sweep finding of exactly that shape, so future sweeps catch it mechanically.

The scanner applies two layers of noise reduction so the same false positives do not re-surface on every sweep. **Layer 1, in-scanner heuristics**: skip matches preceded by section-like words (`Section N`, `Article N`, `Phase N`, `Chapter N`, `Step N`), hyphenated compounds (`under-14 rules`), legal bill prefixes (`AB 1394`, `SB 234`, `Bill 1394`), year-with-title-cased-legal-noun (`The 2025 Rules`), markdown version-history table rows (rows containing both a version-shape and a date-shape), lines containing historical-narrative keywords (`completed at`, `now ships`, `previously`, `past`, `originally`, `historically`, `earlier`, `before gate`, `false positive`, `in-window`, `out-of-window`), and lines matching sweep-history narrative regex patterns (`Sweep N`, `Subagent A/B/C`, `recurring-class`). **Layer 2, exemption file** (the scanner exemption file named in the project wiring): per-entry `(path, pattern_id, line_hash)` records that suppress unique edge cases the heuristics miss. The `line_hash` is the 16-char prefix of SHA-256 of the stripped line content, so the exemption is stable under line-number drift but invalidates automatically if the line text changes (which forces a re-triage). The register's false-positive memory section is the human-readable source of truth; the exemption file is its machine-readable mirror.

### 4. Fan out parallel subagent reviews

**All three subagents must be dispatched on every full sweep.** This is unconditional. The pre-tool verification preamble's "skip corroboration-seeking calls" discipline (Rule 4 preamble) applies to individual tool calls a subagent makes during its work, not to whether to dispatch the subagent in the first place. Skipping a subagent because "the prior sweep covered this scope" is an inference-cascade failure mode: the orchestrator decides without evidence that the subagent's coverage is unnecessary, and the corpus quietly drifts in the unscanned surface.

**No abbreviation discretion either.** The orchestrator does NOT have discretion to substitute an abbreviated check, a spot-check, a memory-only review, an orchestrator-self-check, a "quick scan", or any other informal substitute for the formal three-subagent fan-out the skill encodes. "Abbreviated /validate" is not a sanctioned shape; the only sanctioned shapes are the full formal run and a maintainer-authorized explicit scope-reduction recorded in the history register's entry with rationale (see paragraph below). Throughput pressure (a long batch of PRs about to land, a tight session window, an apparent need to make progress) does NOT authorize abbreviation; the corpus-wide sweep IS the cadence, and "the next sweep will catch it" is the failure mode this rule prevents.

The only sanctioned exception is **maintainer-authorized scope reduction**: the operator explicitly authorizes a thin sweep (e.g., "only Subagent A this time; B and C scope-skipped") in advance, and the sweep history register's entry for the sweep records the authorization in writing. An unauthorized skip is a discipline failure and must surface in the register entry for the next sweep as a corrective action.

Launch subagents in parallel for the semantic sweep. Each receives a self-contained brief, reads target files in full (not excerpts), and reports findings by severity. The three baseline briefs:

- **Subagent A : recent-PR deep review**. Read every file touched by the recent PRs in full; verify every CHANGELOG entry, commit message, and docstring claim against the actual diff; specifically flag mis-attributed citations and claims that contradict the file's actual contents.
- **Subagent B : corpus-wide stale-reference sweep**. Grep the repository for stale gate counts, project and pack versions, and dates; cross-check against the canonical sources (the README, the canonical gate inventory). Also check listing-surface coverage drift on the SEMANTIC surfaces that no gate enforces: the project's own judgment-call listing surfaces (in the parent library: the framework matrices and crosswalks, the glossary and key-terms registers, and per-document `Related Documents` fields). (The MECHANICAL listing surfaces are enforced by the project's listing-surface coverage gate, so a recently-added document missing from those is a gate failure, not a sweep finding; the sweep's value is the relevance-based surfaces where a new document plausibly belongs but inclusion is a judgment call. The project wiring names the gate and the candidate-set helper that produces the candidate set.)
- **Subagent C : audit-programme integrity check**. Independently re-verify that all of the project's parity surfaces agree (in the parent GRC library: workflow, runner, pre-commit, and specification inventory); verify mirror-sync between each mirrored source and its copies (in the parent GRC library, the pack sources and their local copies); verify any new linter's docstring matches its code; spot-check generated-artefact regeneration.

Each subagent reports under 600 words, grouped by severity:
- **High**: factual error, stale reference in a normative document, mis-attribution.
- **Medium**: style inconsistency, minor wording drift, off-by-one in a count.
- **Low / FYI**: cosmetic, historical context, worth noting but not actionable.

**Required for every finding**: a `path:line` evidence quote. A finding without an explicit file path and line number (or line range) is not a finding, it is a hypothesis. Reject any subagent report whose findings lack quoted evidence and re-dispatch the subagent with a re-emphasized brief. This guards against the failure mode where a subagent returns an inferred or confused report instead of read-verified findings; without enforcement of the evidence requirement, the sweep degrades into inference cascade.

**SARIF-lite output format.** Each subagent emits findings as a fenced markdown block per finding so the parent's dedupe (Rule 5.1) and synthesis are mechanical rather than narrative. Each block carries six labelled lines plus an evidence paragraph, in this order:

```
### Finding: <one-line title>
- tool: <subagent-name>           # e.g. A, B, C
- ruleId: <short-stable-id>       # e.g. stale-version-literal, mis-attributed-citation
- level: error|warning|note       # SARIF v2.1.0 result.level enum
- location: <path>:<line>         # uri + region.startLine collapsed
- fingerprint: <ruleId>:<path>:<line>   # deterministic dedupe key
- rubric: 5.1 | 5.2 | 5.3 | 5.4 | 5.5   # synthesis-rubric tag

<evidence quote or 1-2 sentence rationale>
```

Three rules:

1. **One finding equals one block.** Each opens with `### Finding:` and contains exactly the six labelled lines followed by an evidence paragraph. No prose findings outside blocks; no blocks missing fields.
2. **Fingerprint is deterministic.** `<ruleId>:<path>:<line>`, lowercase, no spaces. Parent-side dedupe is then string-match, not semantic comparison. Mirrors Semgrep's `primaryLocationLineHash` shape minus the hash.
3. **Severity enum is closed.** Only `error` / `warning` / `note` (SARIF v2.1.0 spec values). The parent maps to the synthesis rubric's three-level scale (`must-fix-before-merge` / `should-fix-this-PR` / `track-as-follow-up`) at Rule 5.3.

Anti-rubric: do not emit JSON inside prose (parse-anxiety, partial-block failures); do not require the SARIF `$schema` / `version` / `runs[]` envelope (those are wire-format compliance for tools, not field needs for the rubric); do not multiply fingerprint algorithms (one deterministic string suffices when three subagents share one scheme).

**Pre-tool verification discipline**. Every subagent brief carries the following rule (Popper-style falsification preamble, composed with AnyTool's redundancy gate and AgentDiet's dedup check). Before each tool call, the subagent states in one line: (a) the hypothesis this call tests, (b) the observation that would falsify it, and (c) one prior tool result that does not already answer the question. If the falsifying observation is undefined, the call is corroboration-seeking; skip it or reframe. If a prior result already answers the question, do not re-call; cite the prior result in the finding. This produces an auditable trace (every tool call carries its own justification) and filters corroboration-only calls at the source rather than at the report-writing stage, where they have already consumed budget.

If the working tree shows no recent activity (a "cold" sweep), subagent A becomes a narrower spot-check of the most recently-merged PRs (`git log -5 --merges`).

### 5. Synthesize findings

Apply the synthesis rubric: deterministic structure that makes the parent's triage reproducible across sweeps. Six rules, no ceremony.

**Rule 5.1, dedupe by claim, not by line.** The dedupe key for two findings is the tuple `(file_path, normalised_section_or_artefact, claim_type)`, not `(file_path, line_number)`. Two subagents pointing at the same logical defect with different phrasings or slightly different line ranges collapse to a single synthesized row. Line numbers drift under edits and produce false uniques; the file plus the section plus the kind-of-claim is the stable identifier.

**Rule 5.2, tag every synthesized finding with an evidence letter.** `R` = read-verified, accompanied by a quoted line from the file in question (the form the subagent reports already require). `I` = inferred, no read in this sweep. `K` = already-known from the trigger that motivated the sweep, surfaced again as confirmation. Only `R` findings enter the actionable queue. `I` findings go to a "promote to R by reading" sub-list (one extra read closes the gap); `K` findings are dropped after acknowledgement. This makes the evidence-grounded-completion discipline mechanical at the synthesis step rather than relying on parent recall.

**Rule 5.3, severity is adjudicated, not averaged.** Use a fixed three-level scale on the synthesized row: `must-fix-before-merge | should-fix-this-PR | track-as-follow-up`. When two subagents disagree on severity for the same dedupe-key, the parent picks the higher and records both raw subagent severities in a `raw:` field on the synthesized entry. Averaging across subagents is forbidden: it hides disagreement under a number. The two-raters-plus-adjudicator pattern (Cochrane / GRADE systematic-review methodology) is the right shape; the parent is the adjudicator.

**Rule 5.4, record subagent provenance.** Each synthesized row carries the set of subagents that surfaced it (e.g. `source: [A, B]`). A re-run can attribute coverage gaps to a specific subagent's brief; without this, the maintainer cannot tell which fan-out brief to tune.

**Rule 5.5, debate when divergence is large, not when adjacent.** Rule 5.3's "pick higher, record raw" handles the routine case of adjacent severity disagreement (e.g. one subagent says `should-fix-this-PR`, another says `track-as-follow-up`). When divergence is larger, route the finding to a single-round debate before the parent adjudicates. Trigger conditions: (a) two subagents report the same dedupe-key with severities more than one level apart (`must-fix-before-merge` vs `track-as-follow-up`); or (b) one subagent reports the finding as real (`R` evidence) and another flags the same dedupe-key as a false positive. Debate protocol: re-prompt each disagreeing subagent with the other's claim plus reasoning attached; ask each to either update its position with new justification or hold with a concrete rebuttal. One round only. The parent synthesizes the second-round positions; no third "judge" subagent. If both subagents hold after the round, persist disagreement: record both raw severities, the parent still picks the higher, and the synthesized row is flagged `debated: divergence-persisted` so reviewers see the finding was contested rather than silently adjudicated. Single round is empirically where most of the accuracy lift sits; round 3+ can degrade accuracy.

**Rule 5.6, subagent dispatch must be declared in the history row.** Every iteration row in the project's validation-sweep history register (named in the project wiring) names which subagents were dispatched in the `Subagents` column (e.g. `A, B, C` for a full sweep; `A only` for a thin sweep, with the maintainer authorization reason in the Summary cell). If a subagent was skipped without explicit maintainer authorization in the same sweep cycle, the next iteration's row records the discipline failure in its Summary. The mechanism is the auditable trail: a subagent's silent absence in the history table cannot be reconstructed later, so the dispatch declaration is the only point at which the discipline can be enforced.

Cross-reference each synthesized finding against the **false-positive memory** entries listed in the validation-sweep history README (named in the project wiring). Findings the maintainer has previously triaged as not-a-real-finding are suppressed; they should not be re-surfaced.

**Anti-rubric (what NOT to do).** Do not compute inter-rater kappa (N=3 subagents with no pre-shared codebook makes the statistic uninterpretable). Do not average severities. Do not require mandatory consensus across all three subagents: the subagents have non-overlapping specializations (recent-PR deep review vs corpus-wide stale-reference sweep vs audit-programme integrity), and a defect only one subagent could plausibly find must not be down-weighted by the others' silence.

### 6. Triage

Triage depends on whether the finding is **in the configured focus window** (per step 2) or **outside the focus window** (a pre-existing issue surfaced incidentally).

**For findings IN the focus window:**

For each High and Medium finding, propose a concrete fix. For Low / FYI findings, document but do not act unless requested. Surface the proposed fix scope to the operator if any of the following is true: the fix touches a public API or branch-protected artefact; the fix involves an authorial judgement (which option, which scope); the fix spans more than five files. Otherwise, if the operator has pre-authorized the fix scope, proceed.

**For findings OUTSIDE the focus window:**

Surface each finding to the operator with named action options (action now, defer to a tracked follow-up, dismiss as not-a-real-finding). Do not auto-defer an out-of-window finding to "Low / FYI" status; the operator's per-finding decision is the point. The default action is "ask, then do what the operator says"; the failure mode this guards against is silent triage of pre-existing issues that the sweep is well-placed to surface but no longer-running ticket exists to track. The cost of asking is small; the cost of the operator not knowing the sweep saw the finding is larger.

**Ratcheting-baseline discipline for dismissed findings.** Findings the operator dismisses as not-a-real-finding accumulate in the register's false-positive memory section. The accept-list discipline keeps this from drifting into permanent debt:

- **Rule 6.1, fingerprint not count.** Each dismissed finding gets a stable ID: `(file_path, normalised_section_or_artefact, claim_type)` plus the SARIF-lite `ruleId` if one was assigned. The accept-list is keyed on the fingerprint, not on a count or a file-level total. Counts oscillate with subagent noise; fingerprints do not. (Pattern: ESLint per-location suppressions, not per-file counts; relates to the synthesis-rubric dedupe key at Rule 5.1.)
- **Rule 6.2, expiry plus rationale.** Each accept-list entry carries a one-line rationale and an `expires: YYYY-MM-DD` date (default `accepted_on + 90 days`). On expiry, the entry is re-triaged, not auto-renewed. Mirrors ESLint's `--prune-suppressions` discipline and the basedmypy "untyped surface can only shrink" ratchet; without expiry the list normalizes borderline findings into permanent debt.
- **Rule 6.3, net-negative invariant on close.** A sweep cannot close green if `|accept-list|` grew net of fixes. Adding two new acceptances while fixing one is a regression; the sweep must add to the accept-list OR fix, not both freely. This is the "hold-the-line" core; without it, Rules 6.1 and 6.2 still drift upward by accident.

The pre-flight scanner's exemption file and the register's `false-positive memory` section together form the accept-list. The exemption file is the machine-readable surface for the scanner's known false-positive shapes; the register's section is the human-readable surface for subagent-surfaced findings the operator has dismissed. Both are subject to Rules 6.1-6.3; future entries in either should carry the fingerprint, expiry, and rationale fields.

### 7. Apply fixes, re-baseline, repeat

Apply the fixes. **Re-run step 1 (the full audit standalone) AFTER committing each fix, not on the working tree**. Per the canonical rule's "Relying on prior runs" anti-pattern, the audit must see the final state; per the git-history-aware-gates discipline, the audit's view of "final state" is the committed git history, not the uncommitted working tree. Running the audit on uncommitted changes misses what git-history-aware gates, such as a project version-bump-recency check, would flag once those changes are committed. If new findings surface, repeat from step 4. The sweep is complete when one full cycle returns no High or Medium findings.

**Termination conditions** (replacing the older "stop after three iterations" cap; first matching condition fires):

1. **Empty-delta (primary, principled stop).** An iteration produces zero new High or Medium findings AND the synthesized finding-set is identical (by dedupe-key per the synthesis rubric) to the previous iteration's set. The sweep has reached a fixed point. This is the desired exit.
2. **Patience-plateau (secondary, structural-stall stop).** Two consecutive iterations produce no strict shrinkage of the finding-set (no new High or Medium resolved, no new High or Medium discovered). The remaining findings are structurally unresolvable by this sweep alone; surface the residual to the operator with a named decision (defer, escalate, descope). Default patience is 2 iterations, mirroring early-stopping conventions in iterative-solver and ML-training literature.
3. **Hard ceiling (runaway guard, defect signal).** Six iterations regardless of state. Hitting this is signal that something is wrong, not signal of completion: the typical cause is a fix-cycle (fix A re-introduces fix B's finding, ESLint/RuboCop pattern) or scope creep (each iteration uncovers a new class). When hit, do not declare the sweep complete; report whether the cause is a cycle or scope expansion.

The empty-delta is the principled stop; the hard ceiling is the sanity guard. Dual-criterion termination follows the standard iterative-solver pattern (residual-tolerance OR max-iterations, whichever first); the patience-plateau in the middle is the ML-training early-stopping adaptation that handles "the finding-set is not shrinking but is not oscillating" cases that neither extreme catches.

### 8. Append a row to the sweep history (every iteration)

After the cycle terminates, append a row to the project's validation-sweep history register (named in the project wiring). The history file is a reverse-chronological table with one row per iteration:

| Date | Sweep | Subagents | Findings | Resulting PR | Detail | Summary |
|---|---|---|---|---|---|---|

- **Date** is `YYYY-MM-DD`.
- **Sweep** is `N` (sweep ordinal) or `N iter M` (iteration within a multi-iteration sweep).
- **Subagents** declares which subagents were dispatched (e.g. `A, B, C` for a full sweep; `A only` for a thin sweep, with the authorization reason in the Summary cell). Per Rule 5.6, every iteration declares this, including zero-finding ones; a subagent's silent absence cannot be reconstructed later.
- **Findings** is a brief count (e.g. `0`, `3 (1H, 1M, 1L)`, or class-coded `4 (C3, C1)`).
- **Resulting PR** is the GitHub PR link or `none` for zero-finding iterations.
- **Detail** is a link to the per-iteration file (see step 9), or the marker `none` for zero-finding iterations.
- **Summary** is a one-line description of what the iteration found (or what the sweep verified, for zero-finding iterations).

New rows on top. Zero-finding iterations still get a row: the history is the audit trail of every invocation, not just the ones that found something. The trend signal (which classes recur, how iteration counts shrink to convergence) lives in the table itself.

**Same-PR recording (recursion-avoidance retired).** Every sweep invocation gets a history row. The old model deferred a zero-finding row into a next PR to avoid a row-addition-triggers-a-sibling-sweep loop. The synchronous model records the row in the PR that carries the sweep's close-out instead: a sweep run as a PR's finalizing step writes its row in that PR; a standalone or resume-time sweep whose findings warrant a dedicated close-out PR writes its row in that close-out PR. A findings-producing `/validate` may still warrant its own close-out PR when findings are numerous or coherent enough (the project-wide sweep's distinguishing case from the PR-scoped sibling, whose fixes land in-PR by default). The audit trail is preserved: the row records the sweep's ordinal and date, so a reader traces from the row's PR back to the sweep.

### 9. Write the per-iteration detail file (only when findings exist)

When the iteration produced findings, write a per-iteration detail file to the project's per-iteration detail directory, using the naming scheme recorded in the project wiring; the parent GRC library's is `YYYY-MM-DD-sweepN-iterM.md`, where `N` and `M` match the **Sweep** column that step 8 defines for the history row. The file captures detail the history table summary intentionally omits, so a maintainer reading the file weeks later can reconstruct the iteration without the chat transcript. Before committing either surface (the step-8 history row or this detail file), verify each fixed-in-window claim against the actual diff (grep for the claim's target text); a claim whose edit is absent is downgraded to routed, never recorded as fixed (the record-asserts-unapplied-fix guard, shared with the guardrail-review and PR-scoped-sweep record steps).

Six top-level H2 sections in this order:

1. `## Trigger & state snapshot`, what triggered this iteration; the project's canonical version(s) and machinery counts (for example gate/skill/rule counts) at HEAD; iteration ordinal within the sweep.
2. `## Subagent A, Recent-PR deep review`, verbatim return from subagent A (full SARIF-lite findings + summary).
3. `## Subagent B, Corpus-wide stale-reference sweep`, verbatim return from subagent B.
4. `## Subagent C, Audit-programme integrity reviewer`, verbatim return from subagent C.
5. `## Orchestrator synthesis`, in-window classification, severity adjudication, dedupe choices, debate outcomes if any, actions decided for each finding.
6. `## Resulting PR`, link to the close-out PR.

**Zero-finding iterations leave no detail file.** The history row alone is the persistent trace. This keeps the subdirectory's file list aligned with the iterations that actually produced substantive content: a maintainer scanning the subdirectory sees only iterations they might want to read.

The per-iteration record's directory should be covered by the project's linter-exemption mechanism (the parent library's concrete mechanism is named in the project wiring). Files there are frozen-state archives; the `path:line` references in subagent reports are kept verbatim even if the lines later shift.

**Iterations with findings write both a per-iteration detail record and the register-row summary; zero-finding iterations write only the register row** (per the rule above).

## Surfacing findings in chat

**When findings exist, surface them prominently in the chat reply, not only in the per-iteration detail file.** The chat surface is for maintainer awareness and triage; the per-iteration record is the authoritative archive. A maintainer should not need to open the per-iteration detail file or scroll through the detailed change-log mirror to see what the sweep found.

Chat-surface shape: a per-finding line (or short block) carrying the ruleId, the severity / level, the `path:line` location, a one-line evidence quote, a one-line impact, a one-line recommendation, and the in-window / out-of-window classification. Group by severity tier if multiple findings landed. Zero-finding iterations still need a one-line chat acknowledgement.

The chat surface is non-negotiable when the sweep produces findings: a finding that lives only in working-state files is not surfaced to the maintainer's attention.

## Red Flags

- Running the audit suite once and declaring the sweep complete without the post-fix re-run.
- Skipping the semantic subagent fan-out because the mechanical gates passed.
- Treating Low findings as automatically actionable (they document; they do not require action).
- Looping past the termination conditions (an empty-delta close, the patience window, the hard iteration ceiling) without surfacing the recurring pattern.
- Accepting a subagent report that infers rather than quotes (insist on quoted evidence).
- Treating "no findings" from a subagent as proof when the subagent reports no commands run or no files read.

## Verification

The sweep is complete when:
- The full audit programme passes standalone on the final state (exit 0 from the canonical full-audit command).
- All planned subagent reports have been received and synthesized.
- All High and Medium findings have been addressed in scope, or surfaced to the operator and pre-authorized to defer.
- The cycle has terminated cleanly (one full re-baseline after the last fix with no new High or Medium findings).

If any of these is missing, the sweep is incomplete and a clean-bill report is not yet permitted.

## Common Rationalizations

| Rationalization | Reality |
|---|---|
| "The audit gates pass; that's enough." | Gates prove what they check. The semantic sweep targets what they do not. |
| "I just fixed the one issue; nothing else can be wrong." | Same author, same session, same blind spot. Sibling defects are the typical pattern. |
| "Subagents are expensive; I'll just grep myself." | Grep finds what you search for. The subagents catch what you would not have thought to search for. |
| "The sweep returned clean last time; skip it this time." | The project changes between sweeps. Last time's clean does not authorize this time's skip. |
| "The fix was small; the sweep is overkill." | The sweep's cost is bounded. The cost of a sibling defect that lands compounds. |

## See Also

- Canonical rule [`governance/evidence-grounded-completion.md`](../../governance/evidence-grounded-completion.md), specifically the `## Worked example: the multi-surface gate-name parity case` section that motivates this sweep.
- Related skill [`evidence-grounded-completion`](../evidence-grounded-completion/SKILL.md): the per-claim verification protocol this sweep applies at corpus scope.
- Related skill [`gate-discipline-diagnose`](../gate-discipline-diagnose/SKILL.md): when a mechanical gate fails, that skill diagnoses; this sweep then verifies the fix is complete.
- Related skill [`clarify-before-acting`](../clarify-before-acting/SKILL.md): when the sweep surfaces a fix that requires authorial choice (which option, which scope), invoke clarify-before-acting before applying.
- Related skill [`citation-quote-verification`](../citation-quote-verification/SKILL.md): when the sweep flags a finding on citation-bearing content, this skill is the targeted follow-up that verifies quote-to-source correspondence.
- Related skill [`fresh-reader-validation`](../fresh-reader-validation/SKILL.md): when the sweep flags a substantively-revised governance document, this skill is the per-document follow-up that surfaces tacit-context gaps via a fresh-context subagent.
- Related skill [`validate-inference`](../validate-inference/SKILL.md): the per-premise form of Rule 5.6's dispatch-declaration discipline, for a single inferred premise outside a sweep context.
