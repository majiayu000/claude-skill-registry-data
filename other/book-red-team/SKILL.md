---
name: book-red-team
description: Run a structural and adversarial critique of a drafted chapter of The AI Exoskeleton. Two stages. Stage 2 (default) reviews early/mid drafts and produces review-work/NN-slug/04_red_team.md with weak arguments, unsupported load-bearing claims, structural issues, and counter-positions not yet engaged. Stage 6 reviews post-Stage-5 final-quality drafts as the last rigor gate before export, produces review-work/NN-slug/07_red_team_v2.md, and looks specifically for what slipped through six prior passes. Both stages run inline on main-context Opus.
model: opus
---

# book-red-team

The adversarial critique layer. This skill's job is to make the chapter better by attacking it first. It is modeled on the fourth artifact in the gates-poc review-work pattern (`04_red_team.md`) and the book's own kickoff decision to engage the skeptic case rather than strawman it.

This is not a style edit. `book-fact-check` handles claims. `book-draft-chapter` handles voice. This skill handles argument, structure, and what the chapter is NOT saying that it needs to say.

## Inputs

- **Chapter identifier** — chapter number (1-10), `preface`, or `epilogue`. Slug forms also accepted.
- **Stage** (optional): `2` (default, early/mid-draft red-team, output `04_red_team.md`) or `6` (post-Stage-5 final-quality red-team, output `07_red_team_v2.md`). Stage 6 layers additional procedure on top of Stage 2 (see "Stage 6 mode" section below).
- **Mode** (optional): `audit` (default, produces the critique file without modifying the chapter) or `annotate` (inserts inline `[RED-TEAM: ...]` markers into the chapter draft next to the weakest passages).

## Procedure

### 1. Locate files

Given the chapter identifier, locate:

- The chapter draft: `chapters/NN-<slug>.md`
- The chapter's assertion registry (if any): `review-work/NN-<slug>/01_assertion_registry.md`
- The chapter research: `research/NN-<slug>/findings.md`
- The canon: `canon/thesis.md`, `canon/outline.md`, `canon/audience.md`, `canon/book-voice.md`, `canon/book-craft-notes.md`
- Other drafted chapters: for cross-chapter continuity and contradiction checks

If the draft does not exist, abort and report. Red-team runs on drafts that have cleared at least draft-1 polish.

### 2. Read from four persona positions

The skill does not emulate the personas as characters. It uses them as lenses. Each lens generates a short written critique. Four lenses:

1. **The contrarian** — a thoughtful skeptic of the chapter's thesis. Their job is to identify the strongest version of the counter-position and ask whether the chapter engages it. For Chapter 1, this is the AGI-skeptic who thinks the book sidesteps them unfairly. For Chapter 7, this is the executive who thinks evaluation committees are a feature, not a bug. Etc.

2. **The hostile reviewer** — a book critic writing for a publication whose readers are primed to distrust AI hype. Their job is to read the chapter looking for overclaiming, name-dropping, and the texture of consultant prose. They do not care about charity. They want the chapter's weaknesses in print.

3. **The sympathetic-but-skeptical operator** — a working practitioner who mostly agrees with the book's frame but has done more of the work than the author in some specific respect. Their job is to catch the places the chapter is slightly off from the ground-truth experience they know first-hand. Not about disagreement; about fidelity.

4. **The craft editor** — an editor of long-form executive nonfiction. Their job is structural: does the chapter open well, does the argument earn each move, do the paragraphs flow, does the ending leave the reader with something to do. Different from voice (handled by book-draft-chapter post-draft scan) — this is about shape, pacing, and coherence across the full chapter.

### 3. Generate the critique

For each of the four lenses, produce 4-8 specific findings. A finding must:

- Quote or point at a specific passage (by paragraph and a short verbatim snippet)
- Name the problem in one sentence
- Propose either a concrete fix or an explicit open question

Avoid vague critiques. "The argument is weak here" is not acceptable. "Paragraph 4's move from the distribution gap to the build gap skips the step where the reader would accept that moving from one to the other is a meaningful transition; propose adding a sentence that names what the distribution data does and does not tell us" is acceptable.

### 4. Cross-chapter checks

In addition to the four lenses, run two cross-chapter checks:

- **Contradiction with other drafted chapters** — does this chapter take a position that another chapter undermines? (Not a style issue; an argument issue.)
- **Promise/delivery alignment with canon** — does the chapter do the job it is supposed to do per the outline? If Chapter 7 is supposed to be "weeks 1-2 on-ramp," does it deliver an on-ramp, or does it wander into month-3 territory?

Findings from cross-chapter checks are separately flagged because their fix is structural across chapters, not within the chapter being reviewed.

### 5. Produce the red-team artifact

Write to `review-work/NN-<slug>/04_red_team.md`. Create the directory if it does not exist.

Format:

```markdown
# Red Team — Chapter NN: <Title>

**Draft reviewed:** `chapters/NN-<slug>.md` (draft-N, word count)
**Run date:** YYYY-MM-DD

## Summary

- Total findings: N
- Blockers (must-fix before ship): N
- Revisions (should-fix): N
- Questions for author (judgment calls, not auto-fixable): N

## The contrarian

Critique from the strongest version of the counter-position to this chapter's thesis. 4-8 findings, each with passage, problem, proposed move.

## The hostile reviewer

Critique from a book critic primed to distrust AI hype. Looks for overclaim, name-drop, consultant-prose texture.

## The sympathetic-but-skeptical operator

Critique from a working practitioner who knows the ground truth better than the author in some specific respect.

## The craft editor

Structural critique. Opening, paragraph flow, transitions, ending, coherence.

## Cross-chapter contradictions

What other drafted chapters does this chapter contradict, and how?

## Promise / delivery alignment

Does the chapter do what the outline promised it would do?

## Recommendations

Ordered list of specific, concrete next actions. Each one references a finding. Blockers first, revisions second, questions last.
```

### 6. Optional: annotate the draft (annotate mode only)

If the user passed `annotate` mode, edit the chapter draft to insert inline `[RED-TEAM: <brief note>]` markers next to the passages flagged. Do not rewrite prose. Only mark. Advance frontmatter status to `draft-N-annotated`.

### 7. Surface for approval

Report to the user:

- Filename written
- Counts: blockers, revisions, questions
- The top 3 blockers (the findings that most threaten ship)
- Any cross-chapter contradictions found
- Any passages where multiple lenses converged on the same complaint (strong signal)

Do not repeat the full critique in chat.

## What this skill does not do

- Does not rewrite the chapter (that is `book-draft-chapter` in `revise` mode)
- Does not check facts against sources (that is `book-fact-check`)
- Does not do multi-persona adversarial READER reviews (that is the future `book-adversarial-reader` skill, which brings in hostile-reader personas for the final draft gate)
- Does not block publication. The skill produces recommendations; the author decides.

## Failure modes to avoid

- **Vague critique.** Every finding must point at a specific passage. If you cannot, cut the finding.
- **Substituting style complaints for argument complaints.** This skill is about what the chapter argues and how it lands. Voice drift and sentence-rhythm are handled elsewhere.
- **Confirming the chapter instead of attacking it.** The default bias is charity; this skill's job is to override that bias. Lenses are adversarial by design.
- **Conflating a red-team finding with a personal preference.** If the finding only surfaces from one lens and has no external grounding, it goes under "Questions for author," not under "Blockers."
- **Forking to a sub-agent.** This skill is judgment-heavy and runs inline on main Opus. **Subagent 8K output cap silently truncates.** All book-* skills run inline.

## Running across multiple chapters

When red-teaming the whole manuscript (11 artifacts):

1. **Sequential, not parallel.** Run one chapter at a time, Write the full `04_red_team.md` to disk, then move to the next. Never dispatch parallel Opus subagents for this work — 8K output cap guarantees truncation, and silent-Write hallucination is a known failure mode.
2. **Read canon once at session start.** `thesis.md`, `outline.md`, `audience.md`, `book-voice.md`, `book-craft-notes.md` stay loaded. Do not re-read per chapter.
3. **Just-in-time chapter reads.** Read each chapter only when red-teaming it; do not pre-load all 11 into context.
4. **Commit before moving on.** Write the file to disk as soon as findings are generated. Terse report to chat (top 3 blockers + convergence signals). Do not recap full critique in chat.
5. **Cross-chapter check caveat.** When red-teaming chapter N, cross-chapter contradictions reference chapters already-drafted and loaded OR a chapter summary held in `ROADMAP.md`. Do not re-read unrelated chapter drafts to check contradictions — use the summary.
6. **One session of work.** 11 chapters × ~1,000-word red-teams = ~11K words of output + extensive reads. Plan for this as a full session, not a warm-up to other tasks.

## Stage 2 summary artifact (full-manuscript red-team)

After per-chapter red-teams land, write `review-work/STAGE_2_SUMMARY.md` covering:

- Blockers-by-artifact table
- Highest-priority structural blockers (cross-chapter, systemic)
- Per-chapter blocker summary (one line each)
- Systemic fixes (apply once across manuscript)
- Convergence signals (multiple lenses agreed)
- ROADMAP accuracy notes (what the roadmap claimed vs what the drafts show)
- Next-step ordering + time estimate

This artifact is where cross-chapter patterns become visible. Per-chapter red-teams are necessary but not sufficient. Systemic issues (meta-voice, cross-reference staleness, productivity overclaims) only appear when you step back from the individual critiques.

## Series reuse

If this project is book 1 of a series, the red-team skill is a candidate for lifting to a template. Canon path assumptions (`canon/*.md`, `chapters/NN-<slug>.md`, `review-work/NN-<slug>/`) are project-local but structurally identical across books. On book 2 init, copy this SKILL.md verbatim; update only the "what this skill does" example chapter references if they become stale.

---

## Stage 6 mode (post-Stage-5 second red team — the rigor gate)

Stage 6 is the last critique pass before `book-export` ship mode. By the time a chapter reaches Stage 6 it has already been through draft-1, draft-2, Stage 2 red-team (Stage 2 of this very skill), Stage 3 fact-check, Stage 4 adversarial reader (and convergence on Ch 1/5/9), the consolidated revise, and Stage 5 voice polish. Six prior passes. Stage 6's job is to catch what slipped through.

That framing changes the procedure in specific ways. This section describes them. Everything in the Stage 2 procedure above still applies unless overridden here.

### When to use Stage 6 vs Stage 2

- **Stage 2** (default): chapter is at draft-1 or draft-2. Has not been through Stage 4 adversarial-reader. Output goes to `04_red_team.md`. The lenses are looking for argument weaknesses, structural issues, and counter-positions not yet engaged.
- **Stage 6** (explicit): chapter has been through Stage 5 voice polish (frontmatter shows a `2026-MM-DD stage-5 voice polish` change_log entry). Output goes to `07_red_team_v2.md`. The lenses are looking for what got missed, NOT what got addressed. Re-flagging issues that prior stages already caught and fixed is failure mode.

### Stage 6 inputs (additive to Stage 2)

In addition to the Stage 2 reads (chapter draft, canon, assertion registry, research findings, other drafted chapters), Stage 6 ALSO reads:

- The chapter's prior `review-work/NN-<slug>/04_red_team.md` (what Stage 2 caught — to avoid re-flagging)
- The chapter's prior `review-work/NN-<slug>/05_adversarial_reader.md` (what Stage 4 caught — to avoid re-flagging)
- The chapter's prior `review-work/NN-<slug>/06_voice_polish.md` (what Stage 5 caught — to avoid re-flagging)
- `review-work/STAGE_2_SUMMARY.md`, `STAGE_4_SUMMARY.md`, `STAGE_5_SUMMARY.md` (cross-chapter systemic patterns already caught)
- `planning/next-session-agenda.md` "Open decisions still on the table" section (Path C fold-in candidates)
- `ROADMAP.md` (deferred-work catalog, locked decisions)

The reads are additive. Do not re-Read the chapter or canon if they are already in context.

### Stage 6 lenses (re-tuned for late-stage critique)

The four Stage 2 lenses still apply — contrarian, hostile reviewer, sympathetic-but-skeptical operator, craft editor — but at this stage each lens is calibrated differently:

1. **Contrarian (Stage 6 calibration):** the chapter has already engaged the most obvious counter-positions. Look for the second-tier counter-positions: ones that are true but quieter, ones that would only bother a careful reader, ones that emerge from the chapter being right rather than from it being wrong. Example: a chapter that successfully argues X may have under-engaged the question "what does X cost the reader who cannot do X?"

2. **Hostile reviewer (Stage 6 calibration):** the prose is now polished. The hostile reviewer reads at a higher bar. Look for residual overclaim that survived voice polish, residual name-drop where the named source is still doing too much load-bearing work, residual citation-asymmetry where one tier of evidence (e.g., X handles + HN) anchors a paragraph that should also have an institutional source. Look for the hostile-reviewer ammunition quotes that the Stage 4 cluster A/B/C neuterings might not have fully closed.

3. **Sympathetic-but-skeptical operator (Stage 6 calibration):** at this stage the chapter's argument is settled. The operator's job is fidelity check at the level of mechanism. Does the chapter still describe a workflow that would actually produce the claimed result if a reader followed it? Does the chapter elide a step that a real practitioner would notice missing? Stage 5 voice polish may have tightened prose at the cost of mechanism specificity — flag any passage where compression bought polish at the cost of operator-fidelity.

4. **Craft editor (Stage 6 calibration):** structural issues at the chapter level were caught at Stage 2 and addressed in revisions. Stage 6 craft editor looks at micro-structure: paragraph-to-paragraph transitions, sentence-to-sentence flow within each paragraph, the rhythm of the closing lines, whether the chapter's final paragraph still earns the handoff to the next chapter after all the upstream changes. Look especially at any paragraph that was substantially rewritten in Stages 4-5 — those are where seam issues hide.

### The fifth Stage 6 lens: "the slipped-through"

Add a fifth lens that does not exist in Stage 2.

5. **The slipped-through reviewer.** Their job is to look for what the prior six passes were not designed to catch. Six categories to scan deliberately:

   a. **Cross-stage contamination:** a Stage 2 fix introduced a new issue that no later stage was tuned to detect. Example: a softened claim from Stage 2 became a vague claim by Stage 5, and the vagueness now reads as hedging.

   b. **Emergent contradictions:** the chapter as it stands now contradicts something a later chapter says — but the later chapter went through its own Stage 5 polish after this chapter's Stage 4 cross-chapter check. The contradiction is new, introduced by the order of revisions.

   c. **Citation freshness:** sources that were ship-ready at Stage 3 fact-check may have moved or been updated by ship date. Spot-check any citation whose URL was load-bearing and where the source is the kind that updates frequently (vendor blogs, job postings, X handles).

   d. **Frontmatter / change_log drift:** the change_log accumulates entries through six stages and tends to accrete more than it consolidates. Flag any chapter where the change_log is now longer than the chapter benefits from, where the touch_note is stale, or where status doesn't reflect the actual state.

   e. **Late-arriving primary sources:** a primary source might have been published between Stage 3 and Stage 6 that should be cited in this chapter. Especially relevant for any chapter that was drafted earlier — the recency of sources may have shifted.

   f. **Ship-readiness frontmatter:** the chapter's `status` field says `draft-N` or `fact-checked` or `ship-ready`. Stage 6's verdict either advances the status to `ship-ready` (no remaining blockers, only optional revisions and questions) or names what specific remaining work prevents ship-ready status.

### Path C fold-in (manuscript-level open decisions)

Per Justin, the remaining open-decision items (#1, #2, #4, #5, #8 from `planning/next-session-agenda.md` "Open decisions still on the table") fold into Stage 6 rather than running as a standalone sweep. Specifically:

- **Open decision #1** — Director-tier upward-mobility moment in Ch 9 → Stage 6 of Ch 9 must surface it as a Question for Author (not a blocker — it's a judgment call about scope).
- **Open decision #2** — Citation-pool acknowledgment in preface → Stage 6 of Preface must surface it as a Question for Author.
- **Open decision #4** — Ch 6 single-vendor exposure (lines 41 and 99-101 ammunition quotes) → Stage 6 of Ch 6 must surface it as a Blocker if not yet applied, or confirm closure.
- **Open decision #5** — Epilogue Director-tier or Fortune 500 CEO vignette → Stage 6 of Epilogue must surface it as a Question for Author.
- **Open decision #8** — Archetype audit shape (Ch 9 4×4 matrix upgrade) → Stage 6 of Ch 9 must surface it as a Question for Author.

These items are not new findings the skill discovers; they are pre-known open decisions surfaced into the Stage 6 artifact for resolution. Mark them clearly as `[PATH-C: open-decision-N]` at the top of the relevant section so they are visible distinct from new Stage 6 findings.

### Stage 6 findings bar (stricter than Stage 2)

At Stage 2, low-priority "should-fix" revisions are valid output because the chapter is still in active development. At Stage 6, the chapter is supposed to be near-ship. Every Stage 6 finding falls into one of three categories:

- **Blockers** — a real ship-stopping issue. Factual error, logical contradiction, broken cross-reference, ammunition quote that survived Stage 4. Must be fixed before `status: ship-ready`.
- **Revisions** — a meaningful improvement. Worth fixing, but not ship-stopping. Each should justify why it earns a fix at this late stage.
- **Questions for author** — clearly-flagged judgment calls that only Justin can answer. Path C fold-ins go here unless they're already-decided blockers (open decision #4 is the exception — it's a decision that needs to be either applied or closed, not deferred indefinitely).

If a finding is purely a "nice-to-have" that doesn't meaningfully change the chapter's quality, cut it. Stage 6 is a last-chance gate, not a wishlist.

### Stage 6 output format

Write to `review-work/NN-<slug>/07_red_team_v2.md`. The structure mirrors Stage 2's `04_red_team.md` but with the Stage 6-specific sections added.

```markdown
# Red Team v2 (Stage 6) — Chapter NN: <Title>

**Draft reviewed:** `chapters/NN-<slug>.md` (draft-N, word count)
**Run date:** YYYY-MM-DD
**Prior stages reviewed:** Stage 2 (`04_red_team.md`), Stage 4 (`05_adversarial_reader.md`), Stage 5 (`06_voice_polish.md`)

## Summary

- Total findings: N
- Blockers (must-fix before ship-ready status): N
- Revisions (should-fix, justify each): N
- Questions for author (judgment calls + Path C fold-ins): N
- Ship-readiness verdict: <ship-ready / blockers-only / blockers-and-revisions>

## The contrarian (Stage 6 calibration)

Second-tier counter-positions and quieter weaknesses. 0-4 findings — empty section is acceptable if Stage 2 + Stage 4 already covered the territory.

## The hostile reviewer (Stage 6 calibration)

Residual overclaim, name-drop, citation-asymmetry, ammunition quotes. 0-4 findings.

## The sympathetic-but-skeptical operator (Stage 6 calibration)

Mechanism fidelity. Did Stage 5 polish cost specificity? 0-4 findings.

## The craft editor (Stage 6 calibration)

Micro-structure: paragraph transitions, sentence flow within paragraphs, rhythm of closing lines. Special attention to passages substantially rewritten in Stages 4-5. 0-4 findings.

## The slipped-through

Six categories: cross-stage contamination, emergent contradictions, citation freshness, change_log drift, late-arriving primary sources, ship-readiness frontmatter. 0-4 findings.

## Path C fold-ins (if applicable to this chapter)

Pre-known open decisions surfaced for resolution. Each marked `[PATH-C: open-decision-N]`.

## Cross-chapter contradictions (Stage 6)

Only NEW contradictions introduced by post-Stage-2 revisions. Skip if none.

## Recommendations

Ordered list. Blockers first, revisions second, questions + Path C last. Each recommendation references a finding by section + number.

## Ship-readiness verdict

One paragraph. Either: "Ship-ready pending Justin's resolution of N questions" OR "Blockers-only fixes required: <list>" OR "Blockers and revisions both required, with revision count justified by <reason>."
```

### Stage 6 sequential run across manuscript

Same rules as Stage 2 sequential run with the following adjustments:

1. **Read STAGE_2_SUMMARY.md, STAGE_4_SUMMARY.md, STAGE_5_SUMMARY.md once at session start** in addition to canon. These are the systemic-patterns map; without them, Stage 6 will re-flag issues already caught.
2. **Path C items live in `planning/next-session-agenda.md`** — read once at session start so the right chapter's Stage 6 artifact surfaces the right item.
3. **Per chapter, read the prior `04_red_team.md` and `05_adversarial_reader.md` and `06_voice_polish.md` BEFORE writing the Stage 6 artifact.** Re-flagging is failure mode.
4. **Empty lens sections are valid output.** A chapter where Stage 2 + Stage 4 already covered everything in a given lens just gets "No new findings at this stage." The integrity check is whether Stage 6 has anything to ADD, not whether it can fill all five lenses.
5. **Ship-readiness verdict is mandatory.** Every Stage 6 artifact must end with one of three explicit verdicts. This drives the per-chapter status-field update and the manuscript-level go/no-go for `book-export` ship mode.
6. **Write `STAGE_6_SUMMARY.md` after all 11 per-chapter Stage 6 artifacts land.** Same structure as STAGE_2_SUMMARY but with ship-readiness verdicts table front-and-center.

### Stage 6 success condition

Stage 6 is successful when:

- All 11 per-chapter Stage 6 artifacts written
- All Path C fold-ins surfaced in the right artifacts
- All Stage 6 blockers either fixed or explicitly carried as known-deferred
- All chapters' status fields reflect the ship-readiness verdict from their Stage 6 artifact
- `STAGE_6_SUMMARY.md` written with manuscript-level go/no-go

After Stage 6 closes, `book-export` can run in ship mode. If any chapter has remaining blockers, ship mode refuses (per `book-export` SKILL.md).
