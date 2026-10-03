---
name: book-voice-polish
description: Run a Stage 5 voice-polish pass on a chapter of The AI Exoskeleton. Mechanical scan (em-dashes, banned words, sentence-length monotony, paragraph-rhythm uniformity, banned constructions, heavy-use content-word frequency) plus Opus judgment to fix violations in place at clause and sentence level. Produces review-work/NN-slug/06_voice_polish.md capturing every fix made and every flagged hit ruled context-justified. Strictly clause-and-sentence-level, never restructures the chapter. Grounded in voice.md and book-voice.md. Use after Stage 4 adversarial-reader convergence and before Stage 6 second red team. Runs inline on main-context Opus.
model: opus
---

# book-voice-polish

The final mechanical-and-judgment voice gate before Stage 6. Where `book-draft-chapter` does a post-draft scan after each new draft, this skill does a thorough, deterministic sweep across all 11 artifacts at the end of the revision arc, with the chapter draft already at consolidated-revise-plus-Stage-4-convergence quality.

This skill is **clause-and-sentence-level only**. Never restructures, never moves paragraphs, never reorders the argument. Stage 5 is voice; structure already shipped at Stage 4.

## Inputs

- **Chapter identifier** — chapter number (1-10), `preface`, `epilogue`, or `all`. Slug forms also accepted. `all` runs every chapter sequentially.
- **Mode** (optional): `audit` (default — scans, writes findings, no chapter edits) or `apply` (scans, writes findings, applies the fixes Opus judges as definite voice violations in place; flags context-justified hits and judgment calls for the user).

## Voice-file basis

This skill is grounded in two files, both required reading before any judgment pass:

- `~/.claude/rules/voice.md` — the canonical Justin voice profile (banned words/phrases, register ladder, structural anti-patterns, authenticity rules). The mechanical scanner's banned-pattern list is lifted directly from this file.
- `canon/book-voice.md` — book-specific extensions to the global voice (tier 4 sustained, exoskeleton ≤3 per chapter, executive-nonfiction patterns, the `harness` rotation whitelist).

The carve-out for `harness` (excluded from banned-word scan) is the only book-specific override at the scanner level. Everything else is enforced as voice.md specifies. If voice.md changes, scan.sh's banned-pattern list needs to be updated to match.

## Procedure

### 1. Load voice canon (once per session)

Read these in order:

- `~/.claude/rules/voice.md` — global voice authority
- `canon/book-voice.md` — book-specific extensions
- `review-work/STAGE_4_SUMMARY.md` — what's already been done; signature beats to protect
- `planning/next-session-agenda.md` — the three out-of-scope findings logged from a prior voice calibration session (must be hit explicitly):
  1. Ch 9 §2 line 45 em-dash
  2. Ch 9 §4 line 73 "The identity is real…" parallel + "The book's mission statement lands here" meta-voice
  3. Ch 5 line 77 em-dash (already fixed; scan-confirm)

Do **not** re-read these per chapter when running across the manuscript.

### 2. Locate the chapter

Given the identifier, locate:

- The chapter draft: `chapters/NN-<slug>.md`
- The chapter's existing review work: `review-work/NN-<slug>/` (all of `01_*` through `05_*` if present — useful for understanding what each line is doing in the argument before deciding whether a hit is context-justified)

If the chapter is at status `draft-1` only, abort and report. Voice polish runs on chapters that have at least cleared Stage 4 convergence.

### 3. Run the mechanical scan

Invoke `scripts/scan.sh <chapter-file>` from the skill directory. The script handles:

1. **Frontmatter strip** — scans body only, so `touch_note` history doesn't generate noise. Line numbers below are body-relative.
2. **Em-dashes** — zero tolerance. Both `—` (Unicode) and `--` (ASCII pair) flagged.
3. **Banned words and phrases** — full list lifted from `~/.claude/rules/voice.md`. NOTE: `harness` is intentionally NOT in the banned list because `book-voice.md` whitelists it as a rotation word for "exoskeleton." The verb forms (`harnesses/harnessed/harnessing`) remain technically banned per voice.md but cannot be regex-separated from the noun; Opus judges per hit.
4. **Exoskeleton frequency** — flags any chapter using "exoskeleton" more than three times.
5. **Banned structural constructions** — "not only X but," "it's not just X it's," "so what does this mean," "in this chapter we," "in this book we."
6. **Sentence-length monotony** — runs of 3+ consecutive sentences in the 12-18 word band (the LLM-default rhythm).
7. **Paragraph-rhythm uniformity** — runs of 3+ consecutive paragraphs of 3-4 sentences (uniform-block tell).
8. **Heavy-use content words** — top content words by frequency (stop-word filtered, threshold ≥8 occurrences or ≥0.5% of content). NOT a violation list. A signal for Opus to judge per word: load-bearing concept that earns its repetition (e.g. "rig" 28x in Ch 6 as the operator-tier object), intentional rotation for a metaphor (e.g. "harness" 11x as a synonym for exoskeleton), or unconscious crutch (e.g. "thing" / "feel" / "stuff" leaning hard when a more specific noun was available).

Capture stdout. The script's report becomes the input for Opus judgment.

### 4. Opus judgment pass

For each flagged hit, decide:

- **VIOLATION (fix)** — clear voice violation with no context that justifies it. Examples: an em-dash in body prose; "is real" used as hollow-emphasis ("the data behind this argument is real and current"); "transformative" describing AI; "ultimately" as a transition.
- **CONTEXT-JUSTIFIED (keep)** — the flagged token is doing real work that no rewrite would preserve. Examples: "leverage" as a noun ("more leverage than before, not less"); "optimize" inside a technical reference to Peter Senge's "sub-optimization"; "robust" inside a quoted source; a sentence-length-monotony run that is rhythmically intentional (e.g. parallel structure that the chapter is using deliberately).
- **JUDGMENT CALL (flag for user)** — Opus is uncertain and the call belongs to Justin. Examples: a paragraph-rhythm run that might be intentional pacing; an "is real" usage that arguably reports on a fact rather than performing emphasis; a banned structural construction that is doing rhetorical work.

For sentence-length runs and paragraph-rhythm runs, the judgment is rarely "fix one sentence." It's "rewrite this run for variation." The fix may add a fragment, split a sentence, or merge two short ones, clause-and-sentence-level only, never argument-level.

For the heavy-use frequency table, judgment is per top word:

- **Load-bearing concept** (KEEP, no action) — the word is the chapter's central object and earning every repetition. Examples: "rig" 28x in Ch 6 where the on-ramp is built around a tangible operator setup; "harness" recurring in component chapters; "operator" recurring in identity chapters. These are the chapter's vocabulary, not a crutch.
- **Intentional rotation** (KEEP, optionally check distribution) — the word is one of several synonyms doing rotation work for "exoskeleton" or another core concept. Confirm it's not stacked next to its synonyms in the same paragraph (which would defeat the rotation).
- **Vague-content crutch** (FIX) — generic nouns like "thing," "stuff," "feel," "way," "place" appearing 8+ times where a more specific noun was available each time. Substitute per usage.
- **Spillover from earlier draft** (FIX selectively) — words that show up heavily because of revision residue rather than authorial intent. Trim the redundant uses, keep the load-bearing ones.

Do not auto-fix heavy-use words. Surface them in the findings file as "frequency observations" with Opus's per-word verdict, and let Justin call the judgment on whether anything needs to change. Most heavy-use is the chapter doing its job.

### 5. Apply fixes (apply mode only)

In `apply` mode, edit `chapters/NN-<slug>.md` in place using the `Edit` tool. Constraints:

- **No structural changes.** Do not move paragraphs, do not reorder sections, do not delete a paragraph wholesale. If a paragraph is fundamentally broken at the argument level, that's a Stage 6 finding, not a Stage 5 fix.
- **Preserve all factual content.** Numbers, dates, named people, citations stay exactly as they are.
- **Preserve all signature beats.** Refer to the universal-landings list in `STAGE_4_SUMMARY.md` (preface line 25; Ch 1 lines 15-19; Ch 2 lines 15-21; etc.). Touch only what voice requires.
- **Apply only definite VIOLATIONS.** Context-justified hits and judgment calls go in the findings file, not into the chapter edits.

After applying:

- Increment frontmatter `status` (e.g. `draft-3.1` → `draft-3.2` for surgical Stage 5 pass; `draft-3` → `draft-3-stage5` if it's a clean unified pass).
- Append a one-line entry to a `change_log` array in frontmatter: `<date> stage-5 voice polish: <N> violations fixed (em-dashes: X, banned words: Y, monotony runs: Z)`.

### 6. Write findings to disk

Write `review-work/NN-<slug>/06_voice_polish.md` (create directory if needed). Format:

```markdown
# Voice Polish — Chapter NN: <Title>

**Draft scanned:** `chapters/NN-<slug>.md` (status, word count)
**Scanned date:** YYYY-MM-DD
**Mode:** audit | apply

## Summary

- Mechanical hits total: N
- Violations fixed (apply mode) or recommended (audit mode): N
- Context-justified hits (kept): N
- Judgment calls (for user): N

## Violations

For each VIOLATION:

### NN. <one-line description>
- **Line:** body-relative line number
- **Quote:** verbatim flagged passage (clause or sentence)
- **Class:** em-dash | banned-word | banned-construction | sentence-monotony | paragraph-rhythm | exoskeleton-overuse
- **Fix:** the rewrite (if apply mode, exactly what was written; if audit mode, the proposed rewrite)

## Context-justified hits (kept as-is)

For each CONTEXT-JUSTIFIED:

### <pattern>
- **Line / quote**
- **Why kept:** one-sentence rationale

## Judgment calls (for user)

For each JUDGMENT-CALL:

### <pattern>
- **Line / quote**
- **The question:** what Opus is uncertain about
- **Two paths:** the two viable rewrites with one-line tradeoff each

## Heavy-use frequency observations

Top 10 content words from scan.sh Section 7. For each, Opus's verdict:

### <word> (count, % of content)
- **Verdict:** load-bearing | rotation | crutch | residue
- **Why:** one-sentence rationale
- **Action:** none / substitute X usages / trim N redundant uses

## Three out-of-scope findings from voice calibration (Ch 5 + Ch 9 only)

If running on Ch 5 or Ch 9, explicitly confirm or close the three findings logged in `planning/next-session-agenda.md`:

- Ch 9 §2 line 45 em-dash: status (closed if fixed, open with proposed fix if not)
- Ch 9 §4 line 73 "The identity is real…" parallel + "The book's mission statement lands here" meta-voice: status
- Ch 5 line 77 em-dash: status (scan-confirm clean)
```

### 7. Surface for approval

Report to the user (terse):

- Filename written
- Counts: violations fixed/recommended, context-justified, judgment calls
- The chapter's voice posture in one sentence
- Any judgment calls that need Justin's input before Stage 6

Do not repeat the full findings file in chat.

## Running across all 11 artifacts

When running with identifier `all`:

1. **Sequential, not parallel.** One chapter at a time. Subagent 8K output cap silently truncates; never dispatch parallel Opus subagents for this work.
2. **Read voice canon once at session start.** Stays loaded across all 11 chapters.
3. **Just-in-time chapter reads.** Read each chapter only when polishing it.
4. **Commit findings before moving to the next chapter.** Write `06_voice_polish.md` to disk as soon as the per-chapter pass finishes. Terse chat summary; no recap of full findings.
5. **One session of work.** 11 chapters × ~30-50 fixes each = ~500 surgical edits + 11 findings files. Plan as a full session.
6. **After all 11 are done, write `review-work/STAGE_5_SUMMARY.md`** capturing:
   - Total violations fixed across manuscript (by class)
   - Context-justified hit patterns that recurred (often a sign that the global ban list needs a book-specific carve-out)
   - All judgment calls collected, indexed by chapter, for one batch user decision
   - Voice-posture observations across the manuscript (which chapters drifted further from voice; which held it best)

## What this skill does not do

- Does not restructure chapters (Stage 6 second red team handles structural concerns)
- Does not check facts (`book-fact-check` already ran; assertion registries live)
- Does not re-engage personas (`book-adversarial-reader` already converged on Ch 1, Ch 5, Ch 9)
- Does not commit to git (the user does that explicitly)
- Does not edit chapter titles or H1 headings — those were already converted to period style in an earlier holistic sweep

## Failure modes to avoid

- **Restructuring under the banner of voice.** If the fix requires moving a sentence between paragraphs or rewriting a paragraph from scratch, it's not a Stage 5 fix. Flag it as a judgment call or a Stage 6 finding.
- **Auto-fixing context-justified hits.** "Leverage" as a noun is fine. "Robust" inside a quoted source is fine. The mechanical scan can't distinguish; Opus must.
- **Touching signature beats.** The universal-landings list in `STAGE_4_SUMMARY.md` enumerates the lines that converted readers across personas. Do not touch them unless they contain an unambiguous voice violation (em-dash, banned-word verb).
- **Bulk-applying paragraph-rhythm fixes.** A run of 3-4 sentence paragraphs is sometimes the chapter's intentional rhythm. Read the run; decide per case.
- **Forking to a sub-agent.** This skill is judgment-heavy and runs inline on main Opus. Subagent 8K output cap silently truncates.
- **Skipping the findings file in apply mode.** Even when fixes are applied, the findings file is the audit trail. Write it.
- **Trusting voice polish to catch leaks from same-day holistic sweeps.** If the chapter went through a holistic naming, structural, or thematic sweep on the same day as voice polish, prose introduced by that sweep enters Stage 5 looking like canon. The mechanical scanner only sees patterns; it does not flag a meta-voice sentence ("the book's mission statement lands here") as new just because the sweep wrote it. Always run a manual voice scan on any prose changed by a same-day holistic sweep before declaring Stage 5 done. Root cause: Ch 2 Stage 6 Blocker 1 — a meta-voice leak from an earlier holistic sweep slipped through voice polish on the same day and rolled forward to Stage 6, where it was finally caught.

## Why this exists separately from `book-draft-chapter`'s post-draft scan

`book-draft-chapter` runs the scan against a fresh draft, where most violations are first-pass LLM patterns. After Stage 2 (red team), Stage 3 (fact-check), Stage 4 (adversarial reader + convergence + persona rename + holistic naming sweep), the chapters have been edited many times. New violations get introduced during revisions. Old ones get re-introduced when paragraphs are reworked. The Stage 5 sweep is the one that catches what accumulated through revision.

This is also the first pass that runs the mechanical scanner script. The post-draft scan in `book-draft-chapter` is judgment-only; this skill grounds the judgment in deterministic findings so no banned-word slip can hide.
