---
name: writing-article-plans
description: "Produce a detailed .md plan for an academic article that a separate drafter agent then writes section-by-section in LaTeX. This is the academic-writing analog of the superpowers brainstorming → writing-plans workflow: it first interviews the user one question at a time (thesis, contribution, article type, structure, scope), gets approval on a skeleton, then emits a task-decomposed plan that hands off to a fresh section-drafter subagent and downstream to lit-review-orchestrator, cite-placement, and, when it is installed, style-emulation. Use this whenever the user wants to plan, outline, structure, or scaffold a paper before drafting, or asks for 'a plan for a drafter', 'an article plan', 'a paper outline to draft from', 'plan this paper', or 'write up a plan for this article' — even if they don't say the skill name. Also use it in REVISION MODE when the user wants an existing draft restructured or substantively revised (reorganize sections, change or sharpen the argument, conform a manuscript to a genre structure): the draft is treated as the spec and as raw material, with per-section KEEP/REVISE/MERGE/SPLIT/NEW/CUT dispositions. This skill is content- and structure-oriented; style-emulation is voice-oriented. Do NOT use this to restyle prose, fix voice, or purge AI writing patterns (use style-emulation), or to find citations (use lit-review-orchestrator)."
---

# Writing Article Plans

## Overview

Write a comprehensive article plan assuming the drafter has zero context for the
project and will write the manuscript one section at a time. The plan carries the
whole argument down to the level of individual argument moves, so the drafter
produces prose that realizes a decided argument rather than inventing one. This
is the planning half of an academic-writing pipeline that mirrors the superpowers
`writing-plans` → `subagent-driven-development` pattern.

Structure is first order here: the plan inherits its architecture — section
skeleton, proportions, intro moves, footnote policy — from a per-genre
structural profile extracted from a candidate manuscript (see "Genre Structural
Profiles"). Prose style is entirely downstream: the drafter writes plain,
correct prose and `style-emulation` restyles it later. A structural mistake,
unlike a stylistic one, cannot be fixed downstream. In standalone mode there is
no later restyle, so the drafter's plain, correct prose is the final prose: it
still avoids authorial-voice mimicry, but its clarity and polish must reach
delivery quality rather than a draft awaiting a restyle.

Position in the pipeline:

```
spec ──▶ [writing-article-plans]  ──▶ plan.md
                                        │
                                        ▼
                          section-drafter subagents ──▶ draft .tex (with % CITE slots)
                                        │
                                        ▼
                          lit-review-orchestrator   (find the literature; keyed pipeline, defaults)
                                        │
                                        ▼
                          cite-placement               (fill every % CITE slot; mode per the profile's citation architecture)
                                        │
                                        ▼
                          style-emulation           (restyle to author voice — the refinement)
```

The plan is always Markdown. The manuscript the drafter writes is LaTeX
(`main.tex` + `\input{sections/<name>.tex}`), so it drops straight into the
existing estout / latex-results pipeline.

**The deliverable is a written `.md` plan file on disk — not an outline pasted
into the chat.** The interview and the skeleton happen in conversation, but the
skill is not done until the full, expanded, task-decomposed plan has been written
to a `.md` file with the Write tool and its path reported to the user. Producing
the plan only in the chat, or stopping at the skeleton, is a failure to complete
the skill. Drafting the manuscript is a separate, later step that the user opts
into after the plan file exists.

**Announce at start:** "I'm using the writing-article-plans skill to build the
article plan."

## Standalone Mode (style-emulation optional)

`style-emulation` is an optional downstream companion, not a required
dependency. Before the interview, check once whether it is available: the folder
`~/.claude/skills/style-emulation/` exists, or `style-emulation` appears in the
session's available-skills list. If it is absent, **standalone mode** is in
effect for the whole run; every other mention of `style-emulation` in this
document is written for the installed case and is read through this switch.
Standalone mode changes three things:

- The interview does not pin a restyle style, and the plan header records
  `Restyle style: n/a (standalone — style-emulation not installed)` (with the
  `Restyle genre` line likewise for the `review` type).
- The downstream pipeline ends after `cite-placement`: the drafters' prose is
  the final prose, with no restyle stage after it.
- The section-drafters are told their prose is final, so its clarity and polish
  must be delivery-quality rather than a plain draft awaiting a restyle.

When `style-emulation` is installed the skill behaves exactly as documented, and
the restyle is the pipeline's final refinement step.

## Two Modes: New Article and Revision

The skill has two entry points that share the same pipeline.

**`new`** — no manuscript exists; the plan is built from a spec and drafted
from scratch. Everything below applies as written.

**`revision`** — a draft already exists and the user wants it restructured or
substantively revised: sections reorganized, the argument changed or sharpened,
the manuscript conformed to a genre structure. The draft plays two roles: it is
the spec (evidence of the argument already committed) and it is raw material
(prose, citations, and numbers to preserve). Mode detection: an explicit
"revise / restructure this draft" is revision mode; a draft supplied merely as
background for a new paper is `new`; when ambiguous, ask.

**Boundary with style-emulation.** This skill owns changes to *what is said and
where* — structure, argument, sections, footnote architecture. `style-emulation`
owns changes to *how it is said* — authorial voice and purging AI writing
patterns. A request that is purely "make this read better" routes there, even
though this skill can touch existing drafts. This boundary applies when
`style-emulation` is installed; in standalone mode the same division holds —
this skill still owns only structure and argument — but there is no downstream
restyle stage, so authorial-voice work is simply out of scope.

**Draft inventory + gap analysis (revision mode's first step).** Before the
interview, run the same structural extraction used for profile ingestion on the
user's draft: section inventory with word shares, the argument moves each
section actually makes, evidence anchors and citations present, the footnote
layer. Diff it against the selected structure profile. The gaps — an oversized
intro, a missing counterarguments Part, results ahead of methodology, inline
proofs the profile sends to an appendix — are what the interview and skeleton
are built on. Show the inventory-vs-profile diff alongside the skeleton at
approval.

**Dispositions.** In revision mode every existing section gets exactly one
disposition, and every planned section names its source material:

- `KEEP` — carried over verbatim; the drafter copies, never rewrites.
- `REVISE` — the moves state what changes and what is retained ("keep ¶2–4's
  argument on X; replace the opening; add a move on Y").
- `MERGE` / `SPLIT` — with the target sections named on both sides.
- `NEW` — drafted from scratch, exactly as in `new` mode.
- `CUT` — with a note on where any salvageable content goes (a footnote, an
  appendix, another section, or explicitly nowhere).

**Preservation discipline** (the revision analog of No Placeholders):

- Existing real citations are carried through verbatim, never converted to
  `% CITE:` slots. Slots appear only for claims new to this revision.
- Existing numbers stay; the source draft anchors them.
- `KEEP` text is copied byte-for-byte. A drafter who believes a kept passage
  conflicts with a move flags it in a `%` comment instead of rewriting it.
- The original manuscript is never modified. The revision is drafted into a
  fresh `main.tex` + `sections/` tree beside it; a monolithic source draft gets
  a mechanical split step in the plan's file layout so the per-section drafter
  contract is unchanged.

## Workflow

1. **Interview** the user to lock intent (below). This is a gate — do not write
   the plan until the thesis and article type are settled. In revision mode,
   run the draft inventory (see Two Modes) before the interview so the
   questions address the actual gaps.
2. **Show the skeleton in chat** — thesis, contribution, argumentative spine, and
   a one-line-per-section outline — and get the user's approval. This is the only
   part shown inline.
3. **Write the full plan to a `.md` file.** Expand the approved skeleton into the
   complete task-decomposed plan (per-section move blocks below) and write it to
   disk with the Write tool. This file is the skill's deliverable; do not paste the
   expanded plan into the chat instead of writing it.
4. **Write the prompt-and-choices companion `.md`** (below) beside the plan,
   recording the initial spec and every interview question with the option chosen.
5. **Self-review, then run the plan red-team gate** (see Self-Review below):
   dispatch `codex-plan-redteam.md` and fix any BLOCKING findings in the plan, one
   round. Then **report the path** to the user for approval and offer the drafter
   handoff. Only draft the manuscript if the user then opts in.

## Interview First (do not skip)

Like the superpowers brainstorming → writing-plans flow, the plan is only as good
as the intent behind it. Before writing anything, interview the user to settle the
decisions that most change the plan. A plan built on an unexamined thesis wastes
the drafter's entire pass.

**Gate:** Do not write the plan skeleton until the thesis and the article type are
settled with the user. This holds even when the spec looks complete — a short
confirmation is cheap; a plan on the wrong thesis is not.

**How to ask:**
- One question at a time, in priority order. Do not dump a long questionnaire.
- Prefer multiple choice (use the AskUserQuestion tool in Claude Code) when the
  options are enumerable; open-ended is right for the thesis and contribution.
- Read the spec and the project first (existing `.tex`, `.bib`, computed tables),
  and ask only what is genuinely open — never re-ask what the spec already answers.
- Stop once you can state the thesis, type, structure, and evidence back to the
  user without guessing.

**What to settle (rough priority):**
1. **Thesis** — the single central claim. Never invent this; if the user has not
   committed to one, that is the first question. Everything else hangs on it.
2. **Contribution / gap** — what is new, and which alternative explanations the
   paper must rule out.
3. **Article type** — empirical / theory / law_review / review. Default to
   `empirical` unless the spec or the user says otherwise. The type selects the
   structural profile and the downstream style-emulation genre; when the genre
   folder holds several profiles and the choice is live, ask which structure to
   follow. Also pin the restyle style (installed mode only — in standalone mode
   skip this step and record `Restyle style: n/a (standalone — style-emulation
   not installed)` in the header): run style-emulation's
   `pipeline.py --styles --json` (a pure read, no model calls) and apply its
   asking rule — a sole style or a `marked default` resolution is recorded
   without asking; several styles with no marked default → ask which to use
   (AskUserQuestion, options carrying each style's `author` / `source_corpus`
   provenance). Record the result in the plan header's Restyle style line;
   an empty extraction tree records `unpinned`.
4. **Evidence in hand** — tables/figures computed, data available, or theory only.
   This decides what is an anchor versus a `% RESULT` slot.
5. **Target venue and length** — sets section proportions and depth. Length is
   always a soft guideline. When the user names no target: `empirical`
   defaults ex ante to the median *Journal of Law & Economics* article absent
   all appendixes (~14,000 words of main text); `theory` to the median
   *Journal of Law, Economics, and Organization* article absent all appendixes
   (~13,000 words of main text); `law_review` has no silent default — ask the
   user to choose between two scales (AskUserQuestion):
   (a) **OJLS scale** — the median *Oxford Journal of Legal Studies* article,
   ~13,000 words including footnotes (OJLS caps submissions at 15,000);
   (b) **US law review scale** — the median US law review article, ~27,000
   words including footnotes (top journals state a ≤25,000 preference but
   publish 30,000+). These are approximate medians, not journal rules — record
   whichever default or choice was used in the plan header. The content sets the
   length, never the reverse: when the settled argument cannot fill the
   default, plan the shorter article. Do not stretch moves, add filler
   sections, or restate claims to approach a target — padding costs more to
   remove downstream than it saves, since every repeated claim must later be
   found and deflated.
6. **Framing / positioning** — the literature to engage and the causal-language
   ceiling the design earns, so the plan never over-claims.
7. **Constraints** — coauthor directives, required structure, word limits.
8. **Revision scope** (revision mode) — what must change and what is
   sacrosanct; whether the thesis itself moves; which structure profile to
   restructure toward. Anchor these questions in the draft-inventory diff, not
   in abstractions.

Then propose two or three structural approaches — for example, separating
institutional background from the identification section versus folding them
together, or a combined results-and-discussion versus a split — with a
recommendation and reasoning, and let the user choose.

## Inputs

The typical spec is a research proposal or an existing manuscript (the latter
usually triggers revision mode — see Two Modes). Anything else that pins down
intent also works: a one-line topic, a research question, an abstract, rough
notes, or a results summary (tables/figures already computed). Read whatever
the user gives; the interview fills the rest.

Accepted formats: Markdown (`.md`), LaTeX (`.tex`), and Word (`.docx`). Read
`.md` and `.tex` directly. For `.docx`, invoke the `word-docx` skill to parse
the document (body, footnotes, and any comments or tracked changes) before
planning; do not hand-roll the extraction. Save the parsed output as a stable
text artifact beside the plan (`docs/plans/YYYY-MM-DD-<slug>-source-parsed.md`)
— in revision mode this artifact, never the `.docx` itself, is what every
anchor uses: the plan header's Source draft records the original `.docx` as
provenance plus the parsed artifact as the working source, and all Source
material / disposition-map / drafter anchors point at the artifact's
section/paragraph positions, so KEEP text can be located and copied
deterministically.

Citations are handled as **slots only**. This skill never runs a web search. A
claim that needs a source is marked with a typed slot (`% CITE: <kind of source
needed>`), and any keys the user already provided are used as-is. Finding and
verifying references is left to the user or a later `lit-review-orchestrator`
pass.

## Article-Type Detection

Pick the type from the spec; it selects the structural profile (next section)
and the downstream style-emulation genre. **Default to `empirical` unless the
spec or the user states otherwise** — an ambiguous spec is an empirical
article, and the user corrects if that read is wrong.

| Type | Fallback sections (used only when no structural profile exists) |
|------|------------------|
| `empirical` | introduction, literature, data, methodology/identification, results, discussion, conclusion |
| `theory` | introduction, related literature, model, analysis, extensions, implications, conclusion |
| `law_review` | introduction, background, problem, analysis, proposal, counterarguments, implications, conclusion |
| `review` | introduction, scope/method, thematic sections (one per theme), synthesis, agenda, conclusion |

The type names match the `style-emulation` genres (`empirical`, `theory`,
`law_review`) so the downstream restyle uses the right voice spec; record the
type in the plan header. `review` has no style-emulation genre and no
structural profile; it uses the fallback row, and the plan header notes which
genre the eventual restyle should borrow. In standalone mode this
type-to-genre mapping is informational only — no restyle consumes it — but the
structural profile the type selects still applies in full.

## Genre Structural Profiles (structure is first order)

Structure is the first-order concern of this skill. The downstream
style-emulation pass can fix prose but cannot restructure a draft, so the plan
must get the architecture right at planning time. Each genre's architecture
comes from a **structural profile** extracted from a candidate manuscript,
stored at `references/genre-structures/<genre>/<name>.md`. A profile records
the exemplar's section inventory with word-share proportions, heading and
numbering conventions, introduction architecture (an ordered move template),
per-section internal organization, footnote architecture, formal-object
conventions (theory), and signposting.

Selection rules:

- A genre folder may hold **several profiles** (law_review especially —
  different journals favor different architectures). One carries
  `default: true` in its frontmatter.
- Sole profile, or several with a default → use the default and name it in the
  plan header. Several profiles and the choice is live (the user hints at a
  different venue or structure) → ask in the interview.
- No profile for the type (`review`, or a genre not yet ingested) → fall back
  to the type table above and say so in the plan header.

The profile drives the plan: the section skeleton and order, the introduction's
move scaffold, each section block's Structure notes for the drafter, and the
footnote policy. The profile's word shares are descriptive of the exemplar and
a soft guide to relative section weight; every word count in the plan is a soft
target, set by the planner for the article's own target length during the
interview and skeleton. Depart from the profile when the argument demands it —
profiles are exemplars, not straitjackets — but name each structural deviation
in the skeleton shown for approval.

**Ingesting a new candidate manuscript.** When the user supplies an exemplar
(`.tex`) for a genre, extract a new profile: strip comments, compute
per-section word shares with a small script, map the introduction as ordered
moves, record each section's recurring internal pattern, and (law_review)
count footnotes per 1,000 body words with a citation-only vs substantive
split. Write the result to a new `references/genre-structures/<genre>/<slug>.md`
following the schema of the existing profiles. Multiple profiles per genre
coexist; ask the user which one should carry `default: true`.

## The Argumentative Spine Comes First

Before decomposing sections, lock the spine — the through-line every section
serves. Writing sections before the spine produces prose that wanders. The spine
is an ordered list of the paper's load-bearing claims (C1…Cn), each tagged with
the kind of evidence that carries it (a specific table/figure anchor, a citation
slot, or a logical argument). Every later section block references the claims it
realizes, which is how you later check that the argument is covered end to end.

## Article Structure (File Layout)

Map the `.tex` files before writing tasks — this locks the decomposition.

- `main.tex` at the project root (the user's convention), with preamble and an
  ordered list of `\input{sections/<name>.tex}`.
- One file per section under `sections/`, named for its role
  (`sections/intro.tex`, `sections/results.tex`).
- Tables and figures are **anchors** the drafter references, never redraws:
  cite them by their existing path or label (`Tables/table_h1.tex`,
  `\ref{fig:event}`). If a table does not exist yet, mark it as a slot, do not
  invent its numbers.

Each section file is a self-contained drafting task that reads well on its own.

## Confirm the Skeleton Before Expanding

After the interview, write the skeleton only — the header (thesis, contribution),
the argumentative spine (C1…Cn with evidence types), and a one-line-per-section
outline — and show it to the user. Name the structure profile in use and flag
every structural deviation from it (a merged section, a reordered Part) so the
user approves the structure explicitly; word-share differences are not
deviations. Ask whether the
thesis, the spine order, and the section breakdown are right before expanding
any section into moves. This is
the cheap place to fix a wrong through-line, and it mirrors the design-approval
gate in superpowers brainstorming. Only once the user approves the skeleton do you
write the full per-section move blocks below.

The skeleton is the only thing shown inline. The expanded plan that follows is
written to a `.md` file (next section), never pasted into the chat as a
substitute for the file.

## Plan Document Structure

Full annotated template and a worked micro-example: `references/plan-template.md`.
Read it before writing your first plan. The plan's skeleton:

```markdown
# [Working Title] — Article Plan

> **For the drafter:** REQUIRED SUB-SKILL — dispatch a fresh section-drafter
> subagent per section (see "Drafter Handoff" in writing-article-plans), or draft
> inline section-by-section. Write LaTeX. Realize the argument moves below; do not
> invent evidence, numbers, or citations beyond the typed slots. Checkboxes track
> progress.

**Mode:** new | revision
**Article type:** empirical | theory | law_review | review
**Restyle genre:** [review type only: which style-emulation genre the restyle borrows | n/a (standalone)]
**Restyle style:** [style-emulation `--spec` name | unpinned | n/a (standalone — style-emulation not installed)]
**Structure profile:** references/genre-structures/<genre>/<name>.md | fallback table
**Source draft:** [absolute path, revision mode only]
**Target venue / length:** [field + approx. word count]
**Draft format:** LaTeX — main.tex with \input{sections/<name>.tex}

## Thesis
[One or two sentences: the central claim.]

## Contribution
[What is new and what gap it fills — a few bullets.]

## Argumentative spine
C1: [claim] — evidence: [Table 2 anchor | CITE slot | logical]
C2: …

## Claims register
| ID | Claim | Supported by | Appears in |

## Hypotheses            (empirical / theory)
H1: … → tested by … → result: [from spec, or slot to fill from analysis]

## Terminology
[Key term → the exact definition to use consistently.]

## Evidence inventory
- Tables / figures available (by anchor): …
- Citation slots (typed, no keys yet): …

## Source draft disposition map        (revision mode only)
| Source section | Disposition | Target section(s) / destination | Source anchor |

---

## File layout
- Create: main.tex   (preamble; \input order)
- Create: sections/intro.tex
- …

---

### Section N: [Name]  `sections/<name>.tex`   (~N words, soft)

**Role:** [what this section accomplishes in the spine]
**Realizes claims:** C1, C3
**Structure notes:** [from the profile: internal organization to follow,
footnote policy, formal environments required — what the drafter must
structurally honor]
**Disposition:** KEEP | REVISE | MERGE | SPLIT | NEW   (revision mode; CUT
appears only in the Source draft disposition map — it has no target block)
**Source material:** [old draft section / ¶ range, or "none — NEW"]
**Opens from:** [prior section]   **Hands to:** [next section]

- [ ] **Move 1 — [label].** [the actual content of the move: the specific
      puzzle, claim, or result — stated, not described]
- [ ] **Move 2 — [label].** [… `% CITE: study establishing X`]
- [ ] **Draft** sections/<name>.tex realizing the moves above in LaTeX.
- [ ] **Verify:** every move present; named claims stated; citation slots
      marked; no invented numbers.
```

## Argument-Move Granularity

Each move is one paragraph-sized argumentative step the drafter can execute
without further decisions — the analog of a bite-sized task. A move states its
actual content, not a topic label. "Move: motivate the problem" is a planning
failure; "Move: open on the 2019 buyback surge that standard agency theory does
not predict, to set up the puzzle" is a move. The drafter should be able to write
the paragraph from the move alone.

## No Placeholders

Every move must carry the content the drafter needs. These are plan failures —
never write them:

- "TBD", "discuss the literature here", "add motivation", "expand on this".
- A results claim with an invented number. Results come from the spec or an
  anchor; if neither exists, mark a slot (`% RESULT: coefficient on X, fill from
  Table 3`) rather than fabricating.
- An untyped citation slot. Say what kind of source is needed
  (`% CITE: meta-analysis on Y`), not a bare `[cite]`.
- A claim in a later section that no earlier section or anchor establishes.
- A move that names a table, figure, or term defined nowhere in the plan.

## Self-Review

After writing the full plan, reread it against the spec with fresh eyes. This is
a checklist you run yourself, not a subagent dispatch.

1. **Spine coverage.** Every claim C1…Cn is realized by at least one section
   move. List any orphan claims and add moves for them.
2. **Thesis coverage.** Skim the spec's intent; each part maps to a section.
3. **Placeholder scan.** Search for the red flags above and fix them inline.
4. **Consistency.** A term defined in the terminology block is used the same way
   everywhere; a table referenced in Section 5 exists in the evidence inventory;
   a claim asserted late is set up early.
5. **Claim–evidence match.** No move asserts more than its evidence type
   supports (an association claim on observational data, a causal claim only
   where the design earns it).
6. **Structural conformance.** Section order follows the named structure
   profile or the deviation is declared (word counts are soft targets, not a
   conformance criterion); the introduction's moves realize the profile's intro
   architecture; every section block carries the Structure notes the drafter
   needs (internal organization, footnote policy, formal environments).
7. **Disposition coverage** (revision mode). The Source draft disposition map
   has exactly one row per source section — this is where CUT rows and the
   source side of MERGE/SPLIT live, since those have no target block of their
   own; nothing is silently dropped (a CUT names where salvage goes, or
   explicitly nowhere); kept citations and numbers survive into the plan's
   section blocks; every Source material reference resolves.

Fix issues inline; no need to re-review. For a rigorous pass, optionally dispatch
the plan reviewer in `prompts/plan-reviewer.md` before handoff.

**Plan red-team gate.** After self-review, run one substantive red-team pass on a
different model family before showing the plan to the user for approval. Where
`plan-reviewer.md` asks whether a drafter can build from the plan, this asks
whether the argument is worth building — thesis contestability, spine logic, and
the objections a hostile referee would raise. Fill the slots in
`prompts/codex-plan-redteam.md` (plan path, spec), pipe it on stdin to `codex
exec` with the session's standard Codex flags (per the global CLAUDE.md defaults)
and `-o <scratch>/plan_redteam.txt` — where `<scratch>` is any fresh temp dir for
this run, reused by the conformance check below — then read the artifact back. Fix any BLOCKING findings in the plan — one round only, no
convergence loop — and proceed to user approval. The prompt file's dispatch header
carries the rubric, severity rules, and the optional Firecrawl grant.

## Write the Plan to Disk (the Deliverable)

Write the full expanded plan to a `.md` file with the Write tool — this file is
what the skill produces. Save to
`docs/plans/YYYY-MM-DD-<slug>-article-plan.md` under the user's project (user
preferences for location override this). If there is no obvious project directory,
pick a sensible path, create it, and tell the user where the file is, offering to
move it. Reporting the plan only in the chat, or ending at the skeleton, means the
skill did not finish. After writing, report the absolute path.

## Write the Prompt & Choices Companion (also a deliverable)

Beside the plan, write a second `.md` recording *how the plan was decided*: the
initial spec verbatim and every interview question with the option chosen. Save to
`docs/plans/YYYY-MM-DD-<slug>-prompt-and-choices.md` (same directory as the plan).
This makes each plan reproducible — a reader sees the thesis, jurisdiction, venue,
and citation-style decisions that shaped it, not just the result.

Include:

- **Initial prompt** — the user's spec verbatim (fenced), whatever they gave: an
  outline, abstract, or one-liner.
- **Interview choices** — one block per interview round. Show the question, list the
  enumerated options with their `A/B/C/D` letters and one-line descriptions, and mark
  the selected one with `✅`. When the user typed a custom answer instead of picking an
  option, record it under **Answer (custom):** with a one-line note on which option it
  is closest to and how it differs.
- **How the choices shaped the plan** — a short table mapping each decision to its
  effect on the plan (section merged, appendix added, jurisdiction lead, etc.).
- **Revision provenance** (revision mode) — the source draft path, the selected
  structure profile, a one-paragraph summary of the draft inventory, and the
  inventory-vs-profile gaps that drove the interview.

Worked example: `references/prompt-and-choices-example.md`. Report this file's path
alongside the plan's.

## Drafter Handoff

After saving, offer execution.

**This skill's section-drafter subagent.** A fresh
subagent per section that drafts the `.tex` from each section's move block. It
preserves the plan's per-section Verify gates and its typed `% CITE:` / `% RESULT:`
slots (no `.bib` of real keys required yet), and it is the faithful clone of
superpowers `subagent-driven-development`. Prefer it for a slots-only,
footnote-cited plan — which most `law_review` work is.

**How to run it.** Dispatch one section-drafter subagent per section (Opus
4.8), each given `prompts/section-drafter.md`, the plan path, its section block
(including its Structure notes), and any anchor paths. Because every subagent reads the full plan header plus its
own self-contained block, sections can be drafted in parallel for a first pass
(seams are mended downstream by style-emulation's per-section seam pass and its
orchestrator diff read; in standalone mode there is no such downstream pass, so
chain dependent sections or do a manual seam read after drafting); chain them
only if a section's prose genuinely depends on another's. Review each returned `.tex` against its Verify step.
That inline check — the "Reviewing a returned section" step in `section-drafter.md`
— may instead be delegated per section to `prompts/codex-section-conformance.md`,
run as parallel background `codex exec` jobs (one `-o <scratch>/conformance_<section>.txt`
artifact each) since sections are independent; a REDISPATCH verdict feeds the existing redispatch loop, re-sending
that section to a fresh drafter with the named gaps. Both this conformance pass and
the plan red-team above are single-shot by design — do not add convergence loops or
trackers. An **inline** variant (draft the sections yourself, section by section) is
fine when subagents are unavailable.

The output is a set of per-section `.tex` files whose citations
are still `% CITE:` slots.

**Assemble them into one self-contained manuscript before any downstream tool:**

```
python scripts/assemble_manuscript.py --main main.tex --out combined.tex
```

This inlines every `\input{sections/…}` and rewrites one-line
`\footnote{% CITE: …}` slots into the brace-safe two-line form. Skipping it risks
two failures: an unresolved `\input` path, and — because a `%` on the same line as
a footnote's closing `}` deletes that brace when a parser strips comments — a
brace-matching runaway that silently swallows whole sections (lit-review-orchestrator
read only 2 of 8 sections from an unassembled draft). The script reports the section
count and the comment-stripped brace balance; require `balanced — parser-safe` and
0 unresolved before proceeding.

Then take `combined.tex` downstream in this order:

1. **`lit-review-orchestrator`** — find the literature for the article. Feed it the
   draft (or the plan/abstract). Use its **keyed pipeline with defaults**.
2. **`cite-placement`** — fill every `% CITE:` slot in the mode the structure
   profile's citation architecture implies: inline mode where the exemplar cites
   author-date in the body (the empirical profile — its footnotes are
   substantive, never bare citations), footnote mode where citations live in
   footnotes, in the plan's citation style (e.g. OSCOLA for a Bluebook/OSCOLA
   `law_review`; note the current law_review exemplar cites author-date in
   footnotes, not full Bluebook).
3. **`style-emulation`** *(installed mode only — in standalone mode the chain
   ends after step 2 and the drafters' prose is final)* — restyle the
   fully-cited draft into the author's voice, using the genre matching the
   plan's article type (for `review`, which has no style-emulation genre, use
   the genre the plan header says to borrow). Pass the plan header's Restyle
   style as `--spec`; when it is `unpinned`, let style-emulation's own
   resolution (or its wizard's SELECT stage) pick. This is the refinement step
   in this pipeline.

State this pipeline in the handoff so the user knows the plan is step one of five
(four in standalone mode), not the whole job.

Revision-mode notes: run steps 1–2 only if the revision introduced new
`% CITE:` slots — existing citations were carried through and need no
lit-review pass. A manuscript previously checkpointed by style-emulation's
incremental restyle will read as heavily changed after restructuring; once the
revision settles, record a fresh checkpoint (`--checkpoint`) before the next
restyle.

## Bundled Files

- `references/plan-template.md` — full annotated plan template + worked example.
  Read before writing your first plan.
- `references/genre-structures/<genre>/<name>.md` — structural profiles
  extracted from candidate manuscripts (one or more per genre; `default: true`
  marks the genre's presumption). The source of section skeletons, proportions,
  intro architecture, and footnote policy. Read the selected profile before
  writing the skeleton.
- `references/prompt-and-choices-example.md` — worked example of the prompt &
  choices companion `.md` (initial spec + interview options chosen).
- `prompts/section-drafter.md` — subagent prompt for drafting one section into
  `.tex` from its plan block.
- `prompts/plan-reviewer.md` — optional plan-completeness reviewer prompt.
- `prompts/codex-plan-redteam.md` — cross-model substantive red-team of the plan
  (thesis/spine/objections), run before user approval; one round, fix BLOCKING.
- `prompts/codex-section-conformance.md` — optional per-section cross-model check
  that delegates the inline "Reviewing a returned section" step; REDISPATCH feeds
  the drafter redispatch loop.
- `scripts/assemble_manuscript.py` — flatten per-section `.tex` files into one
  self-contained, parser-safe `combined.tex` (run after drafting, before handoff).
