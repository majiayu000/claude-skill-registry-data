---
name: book-adversarial-reader
description: Run a multi-persona reader simulation on a drafted chapter of The AI Exoskeleton. Produces review-work/NN-slug/05_adversarial_reader.md capturing what each of five real audience personas thinks while reading — what convinces them, what loses them, what they would do on Monday morning. Different from book-red-team (which critiques argument and structure from editorial lenses); this skill simulates the actual readers the book is written for, including the hostile augmented-leadership reviewer the book argues against. Use after Stage 3 fact-check and before Stage 5 voice polish. Runs inline on main-context Opus.
model: opus
---

# book-adversarial-reader

The reader-simulation layer. Where `book-red-team` attacks the chapter from editorial lenses (contrarian critic, hostile reviewer, sympathetic operator, craft editor), this skill reads the chapter from the seats of the actual humans the book is written for — plus one hostile reader who represents the position the book argues against. The output is what each of those readers takes away, not what an editor would change.

This is the final gate before voice polish. By the time this skill runs, claims are verified (Stage 3) and arguments have been adversarially edited (Stage 2). The remaining question is: does the chapter actually land for the people it is for, and does the hostile reader put it down or push back?

## Inputs

- **Chapter identifier** — chapter number (1-9), `preface`, or `epilogue`. Slug forms also accepted.
- **Mode** (optional): `audit` (default, produces the artifact without modifying the chapter) or `annotate` (inserts inline `[READER: <persona>: <brief reaction>]` markers next to the passages a persona reacted strongly to).

## Procedure

### 1. Locate files

Given the chapter identifier, locate:

- The chapter draft: `chapters/NN-<slug>.md`
- Prior review artifacts (must exist for this skill to run): `review-work/NN-<slug>/04_red_team.md` and `review-work/NN-<slug>/01_assertion_registry.md`
- The canon: `canon/thesis.md`, `canon/outline.md`, `canon/audience.md`, `canon/book-voice.md`, `canon/book-craft-notes.md`
- Other drafted chapters: only when a persona's reaction depends on cross-chapter coherence (sparingly; do not pre-load all 11)

If `04_red_team.md` does not exist, abort and report. This skill is the next layer on top of red-team, not a substitute for it.

### 2. Read from five persona positions

The personas are real audience segments named in `canon/audience.md` plus one hostile-reader segment representing the position the book engages and routes past. Do not invent personas. Do not split or merge them. The five are fixed:

#### Persona 1 — VP-in-position (core reader)

Senior VP or VP at a Fortune 500 / large enterprise. Sits in the core of the audience definition — wide surface area, high daily-decision density. Has read a stack of AI think pieces, sat through vendor demos, sponsored an AI center of excellence. Knows AI matters, doesn't know what to personally do about it on Monday morning. Smart, time-constrained, skeptical of hype. They are the protagonist of the book.

**Their reading job:** Does the chapter give them something they can act on? Do they recognize themselves in the diagnosis? Does the prescription feel like it could work for someone in their seat, or does it feel like advice for engineers wearing executive titles?

#### Persona 2 — Aspiring Director (aspiring reader)

Director or Senior Director at a Fortune 500 / large enterprise growing into ED-and-above roles. The book gives them the ladder and the vocabulary to argue for the identity before they inherit the title. They read for ambition: what does the next role look like, and how do they pre-equip for it?

**Their reading job:** Does the chapter give them language they can use in their own organization to argue for the role they want? Does it set a ladder they can start climbing this week without permission from their boss?

#### Persona 3 — Fortune 500 CEO (critical secondary)

The rare technically-fluent Fortune 500 CEO who runs at high daily-decision density. Jensen Huang is the canonical archetype. Portfolio is too wide to personally build every artifact for the business, but technically fluent enough to read builder-leader output directly and shape strategy from it. Distinct from the augmented-leadership CEO cohort (Nadella, Pichai, Jassy) whom this book leaves out of scope. Needs builder-leaders on the team. Reads for recognition (how to spot a real builder-leader in a candidate pool) and promotion cover (how to defend the hire and the promotion in rooms that would otherwise block it). Some Fortune 500 CEO readers also operate the harness for their own leadership work: synthesizing board briefings, stress-testing strategy docs, running multi-agent research on a market question.

**Their reading job:** Does the chapter give them the language to defend builder-leaders in institutional rooms? Does it tell them how to recognize the real thing? Does it make them feel respected as a senior who is not the protagonist but is critical to the protagonist's success?

#### Persona 4 — Aspiring senior practitioner (secondary)

Data science lead, AI engineering manager, or principal engineer who already operates an exoskeleton but lacks the vocabulary to explain it to leadership. Reads to hand a copy to their boss and to sharpen their own articulation.

**Their reading job:** Does the chapter give them prose they can quote in a Monday meeting to convince a non-builder leader? Does it accurately describe what they actually do, or does it idealize / misrepresent the practitioner experience?

#### Persona 5 — Hostile augmented-leadership reviewer

The school the book argues against. A consultant, executive coach, or B-school professor who teaches augmented leadership — that the senior role is orchestration, ethical framing, and human judgment, not personal building. Cites Esade, McKinsey, Duke, TalentSprint, AILeadership.com, Mollick's "Management as AI Superpower." Reviews the book for a publication whose readers are primed to find AI-builder hype overblown. Their job is to put the book down, not to be persuaded.

**Their reading job:** Where does the chapter overclaim? Where does it strawman the augmented-leadership position? Where does it fail to engage the strongest version of the counter-argument? Where does the prose reveal the author's identity politics rather than an argument? Does the chapter give them ammunition for a published rebuttal?

### 3. Generate the persona reactions

For each of the five personas, produce a structured reaction with five fields:

1. **Where they nodded** — passages where the chapter clearly landed for this persona. Quote the passage (paragraph + short verbatim snippet).
2. **Where they paused** — passages where this persona slowed down, re-read, or felt friction. Specify whether the friction is productive (made them think) or destructive (made them lose faith).
3. **Where they would push back** — the strongest objection this persona would raise after reading. Not a generic objection — the specific objection that comes from sitting in this persona's seat.
4. **What they would do Monday morning** — the concrete next action this persona would take after reading the chapter, if any. "Nothing" is a valid answer and signals the chapter failed to convert.
5. **Verdict** — one of `converted`, `engaged-but-skeptical`, `tolerated`, `lost`, or `weaponized` (only the hostile reviewer earns `weaponized` — meaning they now have a quote they will use against the book in print).

A reaction is not a critique. The reader is not a copy editor. They cannot tell you "tighten paragraph 4." They can tell you "I lost the thread here" or "this is the part I would forward to my boss."

### 4. Cross-persona convergence pass

After all five personas have reacted, run a convergence analysis. Three buckets:

- **Universal landings** — passages where four or five personas all nodded. These are the chapter's strongest beats; protect them in any later edit.
- **Universal losses** — passages where four or five personas all paused destructively or pushed back. These are the chapter's worst moments; flag for revision.
- **Asymmetric reactions** — passages where personas split sharply (e.g., VP nodded, Fortune 500 CEO pushed back, hostile reviewer weaponized). These are the most informative. They reveal where the chapter is doing the right job for one audience at the cost of another, and force a deliberate decision about whose reaction to weight.

### 5. Hostile-reviewer specific check

The hostile reviewer is unique among the five personas because the book's argument explicitly engages their position (Ch 5 §1b, Ch 9 §1b). After their reaction, run an additional check:

- **Did the chapter engage their strongest position?** If the chapter strawmans the augmented-leadership case, mark this as a blocker. The book's credibility depends on engaging the steelman, not the strawman.
- **Did the chapter give them a clean quote to weaponize?** Specifically, are there sentences in the chapter that, lifted out of context, would land in their published rebuttal as evidence the book is engineer-supremacist or anti-leadership? Quote those sentences and propose neutering rewrites.

The goal is not to make the hostile reviewer agree. The goal is to leave them with no easy ammunition.

### 6. Produce the adversarial-reader artifact

Write to `review-work/NN-<slug>/05_adversarial_reader.md`. Create the directory if it does not exist (it should already exist from Stage 2).

Format:

```markdown
# Adversarial Reader — Chapter NN: <Title>

**Draft reviewed:** `chapters/NN-<slug>.md` (draft-N, word count)
**Run date:** YYYY-MM-DD
**Prior review:** `review-work/NN-<slug>/04_red_team.md`

## Summary

- Personas converted: N of 5 (excluding hostile reviewer where `tolerated` is the win condition)
- Universal landings: N
- Universal losses: N
- Asymmetric reactions requiring decision: N
- Hostile-reviewer ammunition flagged: N quotes

## Persona 1 — VP-in-position

**Where they nodded:** ...
**Where they paused:** ...
**Where they would push back:** ...
**What they would do Monday morning:** ...
**Verdict:** converted | engaged-but-skeptical | tolerated | lost

## Persona 2 — Aspiring Director

(same five fields)

## Persona 3 — Fortune 500 CEO

(same five fields)

## Persona 4 — Aspiring senior practitioner

(same five fields)

## Persona 5 — Hostile augmented-leadership reviewer

(same five fields, with `weaponized` available as a verdict)

### Hostile-reviewer specific check

- **Engaged their strongest position?** yes | partial | strawman
- **Ammunition quotes** (verbatim, with proposed neutering rewrites): ...

## Convergence

### Universal landings (protect in later edits)

- Paragraph N: "<short snippet>" — landed for personas A, B, C, D
- ...

### Universal losses (revise)

- Paragraph N: "<short snippet>" — failed for personas A, B, C, D — pattern: <one sentence>
- ...

### Asymmetric reactions (require deliberate decision)

- Paragraph N: VP nodded; Fortune 500 CEO pushed back. Decision: which reader does this paragraph serve, and is that the right call?
- ...

## Recommendations

Ordered list of specific, concrete next actions. Each one references a finding. Blockers first (anything that loses the core reader OR weaponizes the hostile reviewer), revisions second, persona-asymmetry decisions last.
```

### 7. Optional: annotate the draft (annotate mode only)

If the user passed `annotate` mode, edit the chapter draft to insert inline `[READER: <persona>: <brief reaction>]` markers next to the passages each persona reacted to most strongly (limit to top 2-3 reactions per persona to avoid clutter). Do not rewrite prose. Only mark. Advance frontmatter status to `draft-N-reader-annotated`.

### 8. Surface for approval

Report to the user:

- Filename written
- Persona verdicts: one line per persona (e.g., `VP: converted | Aspiring Director: engaged-but-skeptical | Fortune 500 CEO: converted | Practitioner: converted | Hostile: tolerated`)
- Counts: universal landings, universal losses, asymmetric reactions, hostile ammunition flagged
- The single most important finding from this run — the one that, if left unfixed, would most damage the chapter's job

Do not repeat the full reactions in chat.

## What this skill does not do

- Does not rewrite the chapter (that is `book-draft-chapter` in `revise` mode)
- Does not check facts (that is `book-fact-check`, run earlier in Stage 3)
- Does not critique argument and structure from an editorial seat (that is `book-red-team`, Stage 2)
- Does not do voice polish or banned-phrase scan (that is the future `book-voice-polish` skill, Stage 5)
- Does not invent new personas. The five are fixed and tied to `canon/audience.md`. If `audience.md` materially changes, update this skill in lockstep.

## Failure modes to avoid

- **Persona drift into editor.** A reader is not a copy editor. If a finding reads like "tighten the prose," it belongs in voice polish, not here. Reader findings must be in the form of "I felt X reading this," not "you should fix X."
- **Hollow personas.** Each persona must have something specific to say that the others don't. If the VP-in-position and Fortune 500 CEO both nod at the same paragraph for the same reason, you have not actually read from two different seats.
- **Reflexive hostile-reviewer steelmanning.** The hostile reviewer is a real position with real arguments. Engage the steelman. But the skill's job is also to flag where the chapter overclaims; do not soft-pedal the hostile review to keep peace with the book's thesis.
- **Treating "weaponized" as a normal verdict.** It is the worst possible outcome. If the hostile reviewer weaponizes a passage, that passage is a blocker, no matter how strong the rest of the chapter is.
- **Forking to a sub-agent.** Same as `book-red-team`: this skill is judgment-heavy and runs inline on main Opus. Subagent 8K output cap silently truncates. All book-* skills run inline.
- **Skipping the convergence pass.** Per-persona reactions are necessary but not sufficient. The signal is in where personas converge or diverge. Without convergence analysis, you have five disconnected critiques and no decision support.

## Running across multiple chapters (Stage 4 full-manuscript pass)

When running adversarial reader on the whole manuscript (11 artifacts):

1. **Sequential, not parallel.** One chapter at a time. Write the full `05_adversarial_reader.md` to disk, then move to the next. Never dispatch parallel Opus subagents.
2. **Read canon once at session start.** `audience.md` especially — the personas come from there and must stay in working memory across all chapters.
3. **Just-in-time chapter reads.** Read each chapter only when reviewing it. Hold a one-line summary of prior chapters from `ROADMAP.md` for cross-chapter coherence checks.
4. **Commit before moving on.** Write the file as soon as the convergence pass is done. Terse report to chat.
5. **Track persona verdicts across chapters.** Keep a running ledger: for each chapter, which personas converted, which lost. Patterns show up across the manuscript that single-chapter reviews miss (e.g., Fortune 500 CEO loses interest from Ch 6 onward because the on-ramp chapters are not for them — that is a feature, not a bug, but it must be a deliberate decision).
6. **One session of work.** 11 chapters × ~1,200-word reader-reactions = ~13K words of output plus extensive reads. Plan as a full session, not a warm-up.

## Stage 4 summary artifact (full-manuscript adversarial reader)

After per-chapter reader reviews land, write `review-work/STAGE_4_SUMMARY.md` covering:

- Per-chapter persona verdict matrix (5 personas × 11 artifacts)
- Conversion arc per persona across the manuscript (does the VP convert by Ch 3 or Ch 9? does the hostile reviewer get angrier or calmer over the read?)
- Universal landings across chapters (signature beats to protect)
- Universal losses across chapters (signature failures to fix)
- Hostile-reviewer ammunition inventory (every quote flagged across all 11 chapters; cluster by pattern)
- Persona-arc decisions surfaced (e.g., is it acceptable that Fortune 500 CEO tunes out for the on-ramp chapters? confirm or revise)
- Next-step ordering into Stage 5 voice polish

This artifact is where the manuscript's reader-experience patterns become legible. Per-chapter reader reviews are necessary but not sufficient. Reading-arc problems (a persona who converts in Ch 1 and is lost by Ch 7) only appear at the manuscript level.

## Loop until convergence

The agenda specifies "loop until critiques converge." A reading is converged when, on a re-run after revision:

- No persona moved from `converted` to a worse verdict
- No new universal losses appeared
- No new hostile-reviewer ammunition was flagged
- At least one previously-flagged ammunition quote was successfully neutered

If a re-run surfaces a new universal loss (a passage that was fine before is now flagged), the revision introduced a regression and must be reconsidered. If two consecutive runs produce identical findings, convergence is reached for that chapter and the chapter advances to Stage 5.

## Series reuse

If this project is book 1 of a series, this skill is a candidate for lifting to a template, but with caveats. The persona definitions are tightly bound to `canon/audience.md` for *this* book. On book 2 init, the audience canon will differ; the persona list must be re-derived from book 2's `audience.md`, not copied from book 1. Copy this SKILL.md as scaffolding and rewrite Section 2 (the persona definitions) before first use.
