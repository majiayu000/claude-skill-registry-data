---
name: book-fact-check
description: Fact-check a drafted chapter of The AI Exoskeleton against the chapter's research findings. Extracts every factual claim from the chapter, matches each to a source in research/<chapter-slug>/findings.md or research/source-index.md, and flags any claim that cannot be matched. Produces an assertion registry + an open-claims list per chapter. Use when a chapter draft exists and needs verification before it can be considered ready.
model: opus
---

# book-fact-check

Verify every factual claim in a drafted chapter against the research record. This is the rigor scaffold. It exists so the book cannot ship a claim that does not trace to a source.

The pattern is lifted from the Gates POC `review-work` four-artifact model. This skill produces two of those four artifacts per chapter: the assertion registry (`01_assertion_registry.md`) and the open-claims list. The structural and adversarial artifacts are produced by `book-red-team` and `book-adversarial-reader`, which are separate skills.

## Inputs

- **Chapter identifier** — chapter number (1-10), `preface`, or `epilogue`. Slug forms also accepted.
- **Mode** (optional): `audit` (default, produces the registry without modifying the chapter) or `annotate` (inserts inline `[VERIFY]` / `[SOURCED]` markers into the chapter draft).

## Procedure

### 1. Locate files

Given the chapter identifier, locate:

- The chapter draft: `chapters/NN-<slug>.md`
- The chapter research: `research/NN-<slug>/findings.md`
- The chapter raw research dir: `research/NN-<slug>/_raw/`
- The master source index: `research/source-index.md`
- The running claims queue: `research/claims-to-verify.md`
- The running verified list: `research/verified-claims.md` (create if missing)

If the chapter draft does not exist, abort and report. Fact-check runs on drafts, not plans.

If the chapter research dir does not exist, the chapter is either pre-research or was drafted from reused essay material where the source essays carry the citations. Report this condition and ask the user whether to proceed against `source-index.md` alone or to abort until chapter research exists.

### 2. Extract factual claims

Read the chapter draft. Extract every sentence or clause that makes a checkable factual assertion. A factual claim is any statement that includes one or more of:

- A named person (Karpathy, Mollick, Marcus, etc.) in the context of having said, done, or produced something specific
- A dated event ("on April 9, 2026", "in January", "last quarter")
- A specific number, percentage, metric, or benchmark ("88 percent of organizations", "20,000 likes", "$200/month")
- A named system, product, paper, or artifact ("Claude Code", "nanoGPT", "ARC-AGI-2", "the Karpathy autoresearch repo")
- A named organization's stated position ("Anthropic renamed...", "McKinsey reports...", "Gartner forecasts...")

Skip:

- The author's own opinions and arguments (not factual claims)
- General observations about the AI landscape that are not pinned to a specific source
- Rhetorical constructions ("the reader may be feeling X")
- Subjective characterizations ("the thread landed with relief")

For each extracted claim, record:

- Exact sentence or clause as quoted from the chapter
- Chapter section / paragraph reference
- Claim type (person/date/number/system/org-position)
- The name/date/number/system at the center of the claim

### 3. Match to research

For each claim, look for a matching entry in this order:

1. `research/NN-<slug>/findings.md` under `## Findings`
2. `research/source-index.md` by citation key or by scanning the Source column
3. The raw files in `research/NN-<slug>/_raw/` if the claim is not found in `findings.md` (the raw files are the ground truth; findings.md is the consolidation and can miss things)

A match requires:

- The same named entity (person/system/org)
- Consistent date (within rounding for imprecise references like "early 2026")
- Consistent number (exact match for percentages and counts; ranges allowed for soft estimates)
- A source URL or a research-file reference pointing to the origin

Matches are classified as:

- **SOURCED** — claim matches a research entry with a verifiable source URL and a citation key
- **PARTIAL** — claim matches an entry but the source is weak (secondary reporting, not primary; or older than the 12-month hard floor)
- **UNSOURCED** — no matching entry in any research file
- **DRIFT** — claim matches an entry but the chapter's wording drifts from the source (number rounded, date shifted, attribution changed, or the chapter's paraphrase contradicts the source)

**DRIFT classification is revise-required between fact-check and adversarial-reader (Stage 3 → Stage 4), not voice-polish-deferrable.** Voice polish (Stage 5) is a clause-and-sentence-level pass for banned words and rhythm. It does not check paraphrase fidelity. Any DRIFT finding must be resolved in the chapter draft before the chapter advances out of Stage 3. Marking a DRIFT finding "resolve at voice polish" is a process bug.

### 4. Produce the assertion registry

Write to `review-work/NN-<slug>/01_assertion_registry.md`. Create the directory if it does not exist.

Format:

```markdown
# Assertion Registry — Chapter NN: <Title>

**Draft reviewed:** `chapters/NN-<slug>.md` (draft-N, word count)
**Run date:** YYYY-MM-DD
**Research file:** `research/NN-<slug>/findings.md`

## Summary

- Total claims extracted: N
- SOURCED: N
- PARTIAL: N
- UNSOURCED: N
- DRIFT: N

## Claims (one table)

| # | Claim (verbatim quote) | Section | Type | Status | Citation key / source | Notes |
|---|------------------------|---------|------|--------|----------------------|-------|
| 1 | "On April 9, 2026, Andrej Karpathy posted a thread on X..." | Opening | date+person+system | SOURCED | karpathy-two-groups-2026-04-09 | |
| 2 | "The thread landed with twenty thousand likes..." | Opening | number | SOURCED | karpathy-two-groups-2026-04-09 | Exact at capture; verify at publish time |
| ... | | | | | | |

## Blockers

Claims that must be resolved before the chapter can ship:

- Claim #N: reason
- ...

## Recommendations

- Move claim #X from PARTIAL to SOURCED by: ...
- Cut claim #Y if it cannot be sourced by: ...
```

### 5. Update rolling lists

For each UNSOURCED or PARTIAL claim, add an entry to `research/claims-to-verify.md` under a `## Chapter NN` heading. Include the claim, the chapter reference, and what would source it (a specific search, a specific URL to scrape, a specific person to ask).

For each SOURCED claim, add or update an entry in `research/verified-claims.md` (create the file if it does not exist). This is the cumulative record of everything the book has on solid ground.

Update `research/source-index.md` with any new sources encountered during the match phase that were in `findings.md` or `_raw/` but not yet in the master index.

### 6. Optional: annotate the draft (annotate mode only)

If the user passed `annotate` mode, edit the chapter draft to insert inline markers:

- `[SOURCED: citation-key]` after each sourced claim
- `[VERIFY: what's missing]` after each unsourced or partial claim

Do not modify chapter prose in annotate mode beyond inserting markers. Do not rewrite, reorder, or otherwise edit the text. The chapter frontmatter gets `status: draft-N-annotated` (without advancing the draft number).

### 7. Surface for approval

Report to the user:

- Filename written (`review-work/NN-<slug>/01_assertion_registry.md`)
- Summary counts: total claims, SOURCED, PARTIAL, UNSOURCED, DRIFT
- The top 3 blockers (UNSOURCED claims that are load-bearing for the chapter's argument)
- Any DRIFT claims that suggest the chapter is misrepresenting a source
- Recommendations for resolving blockers (where to search, who to ask, what to cut)

Do not repeat the full registry in chat. The user reads it from the file.

## What this skill does not do

- Does not rewrite the chapter (that is `book-draft-chapter` in `revise` mode)
- Does not do structural critique (that is `book-red-team`)
- Does not do multi-persona adversarial review (that is `book-adversarial-reader`)
- Does not run fresh research to plug gaps — it reports gaps; filling them is a user decision
- Does not auto-cut unsourced claims

## Failure modes to avoid

- **Hallucinating a match.** If a claim does not have a clear entry in the research files, do not invent one. Mark UNSOURCED.
- **Treating the chapter's own argument as a factual claim.** The author's synthesis is not a factual assertion that needs a source. Only pinned facts (named people, dated events, numbers, systems) need sourcing.
- **Letting reply-thread material slide because it was in research.** A claim sourced to "replies on a tweet" without a named, citable individual is a weak source; mark PARTIAL and flag.
- **Skipping DRIFT detection.** A chapter that says "88 percent of organizations" when the source says "78 percent" is worse than one that says "most organizations" without a source. DRIFT is the most dangerous status because it looks SOURCED at a glance.
- **Forking to a sub-agent.** This skill is judgment-heavy and runs inline on main Opus. Subagent 8K output cap silently truncates claim registries.
- **Deferring DRIFT findings to voice polish.** Voice polish is a clause-and-sentence-level rhythm and banned-word pass. It does not check that a paraphrase still represents the source faithfully. A DRIFT finding marked "fix at voice polish" will roll forward through adversarial-reader, voice-polish, and second-red-team without anyone re-checking the source — because none of those stages re-reads source material. Resolve DRIFT in the chapter before Stage 4. Root cause: Ch 7 Stage 6 Blocker 2 — an Anthropic paraphrase-fidelity issue marked DRIFT at Stage 3 was deferred to "voice polish," which never checks paraphrase fidelity, and survived five passes before Stage 6 caught it.

## Running across multiple chapters

When fact-checking the whole manuscript (11 artifacts):

1. **Sequential, not parallel.** One chapter at a time, write `01_assertion_registry.md` to disk, then move to the next.
2. **Read canon + source-index once at session start.** Stay loaded across runs.
3. **Just-in-time chapter + findings reads.** Read chapter draft and `research/NN-<slug>/findings.md` only when fact-checking that chapter.
4. **Maintain running claims-to-verify and verified-claims files as you go.** These are the drain queue and the stone-solid list respectively. Update after every chapter, not at the end.
5. **Cross-chapter stat disambiguation.** Watch for numbers reused across chapters — the 88% stat is used three times with three different sources. Flag any claim that uses a metric already in `verified-claims.md` with a different number or source.
6. **Terse reports.** Top 3 blockers per chapter to chat; full registry to file.

## Series reuse

The fact-check skill is a direct candidate for cross-series lifting. The pattern (extract claims → match to findings → tag SOURCED/PARTIAL/UNSOURCED/DRIFT → maintain drain queue) is structure-invariant across books. Copy verbatim to new book dirs; only update example citations.
