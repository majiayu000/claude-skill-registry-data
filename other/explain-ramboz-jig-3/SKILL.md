---
name: explain
description: >
  Explain jig vocabulary and artifacts in plain language. Three modes: term
  mode defines one lexicon term; artifact mode walks through a spec or ADR and
  its linked references; passage mode explains pasted jig output. Output is
  ephemeral (chat-only). Auto-triggers when you say explain this term, walk me
  through this spec, explain this ADR, what does this output mean, or explain
  this snippet; invoke explicitly with `/jig:explain`. Defers to any other
  installed skill whose description identifies it as handling plain-language
  explanation, onboarding, or artifact walkthroughs. Does not defer to the
  generic built-in. Do not use for finished-slice compliance (use
  `/jig:independent-review` instead), cross-artifact analysis (use
  `/jig:analyze` instead), or glossary updates (use `/jig:memory-sync`
  instead).
user-invocable: true
---

> Spec 065 introduces this skill as jig's **on-demand explainer** — the third
> consumer of the shipped lexicon (065-01). The barrier jig is lowering is
> vocabulary: the artifacts are dense with opinionated jargon (SPIDR, ADR,
> vertical slice, reconciliation, deviation log, DoR/AC/DoD, frontmatter) and
> almost none of it is explained where the reader meets it. The hook (065-02)
> surfaces one-line defs just-in-time; this skill is the **strong-handholding**
> escalation — define a term in depth, or translate a whole dense spec/ADR into
> plain language for a junior.
>
> Like `/jig:clarify`, `/jig:pr-review`, and `/jig:arch-review`, explain is a
> **judgment skill** — it ships **no `.py` helper**. The only determinism it
> needs (load the merged lexicon, read the named artifact, resolve the refs it
> links) Codex runs inline via Read + the 065-01 loader. The plain-language
> *quality* is judgment exercised by this prompt, not something a unit test can
> assert — the same accepted shape as every judgment-only jig skill.

## What this skill does

Translates jig's vocabulary and artifacts into plain language for a reader who
is **new here** — a junior, or anyone meeting spec-driven work for the first
time. It has three modes, selected by what the argument is:

- **Term mode** — the argument is a word or short phrase (`/jig:explain
  reconciliation`). The skill returns that term's plain-language definition from
  the **merged lexicon** (jig's shipped `lexicon.json` with the project's
  `docs/memory/glossary.md` overlaid on top — 065-01), plus its example and
  see-also when present. If the term is **not** in the lexicon, the skill says
  so plainly rather than inventing a definition.
- **Artifact mode** — the argument is a path to a spec or ADR
  (`/jig:explain docs/specs/062-refactor-workflow/spec.md`). The skill produces
  a fixed-shape, junior-grade **walkthrough** of that artifact, defining every
  jig term it uses inline and **auto-pulling the ADRs/specs it links** so the
  reader doesn't have to chase references.
- **Passage mode** — the argument is a **pasted snippet of jig output** that is
  neither a single term nor a file path: a review `VERDICT:` envelope, a
  status-board row like `IN_PROGRESS (wt-me)`, a hook's *"Unrecognized
  references in prompt…"* message, a `workflow.py` transition refusal, a
  `session-plan` block. The skill scans the snippet for jig terms (defining each
  inline) and explains **what it is** and **what — if anything — the reader
  should do**. When the snippet carries **no jig vocabulary at all**, it gives a
  plain generic read. This is the mode for the most common confusion moment: a
  reader pastes the thing that stumped them.

All three modes are **ephemeral**: the output is chat-only. The skill writes nothing
to disk — no `--save` flag, no appended section, no file mutation. This keeps
the hot path clean (the 055/057 context-cost discipline) and matches the
clarify-Q3 resolution that explain output is always chat-only.

This is a **best-effort comprehension floor**, not a guarantee the reader will
understand everything — the same honest framing as jig's security floor
(ADR-0013) and the soft context mechanisms (055/057). The skill surfaces and
explains; it does not certify understanding.

## When to use vs. when to defer

**Defer to a richer installed skill first.** If another installed skill's
description identifies it as handling plain-language explanation, onboarding, or
artifact/codebase walkthroughs, prefer it — jig's explain is a slim baseline.
This skill does **not** defer to the generic built-in (a bare `explain`/`init`
with no onboarding framing); it only steps aside for a skill whose description
names the explanation/onboarding/walkthrough job.

Three sibling jig skills are easy to confuse with this one:

- **`/jig:independent-review`** — reviews a *finished implementation* against
  its spec's ACs. It evaluates whether the code is correct; this skill explains
  what the spec *says* to a reader who finds it dense. Reach for
  independent-review after a slice is implemented; reach for explain when a
  reader is stuck on the vocabulary or shape of an artifact.
- **`/jig:analyze`** — cross-artifact consistency analysis: does spec A
  contradict ADR B? It hunts for *drift between* artifacts. This skill explains
  *one* artifact (and the refs it pulls in) to a human. Reach for analyze to
  audit alignment; reach for explain to understand.
- **`/jig:memory-sync`** — *persists* a new term to the project glossary or
  hot cache. It writes vocabulary. This skill *reads* the existing lexicon to
  explain a term; it never authors one. Reach for memory-sync to record a term;
  reach for explain to look one up. (If explain flags a term as absent and the
  user wants it captured, route them to `/jig:memory-sync`.)

Rule of thumb: **understand an artifact or term → this skill. Persist a term →
`/jig:memory-sync`. Check the implementation → `/jig:independent-review`. Audit
across artifacts → `/jig:analyze`.**

## Inputs — mode precedence

The argument selects the mode by a fixed resolution order:

> **path → artifact mode · exact / normalized lexicon key → term mode ·
> otherwise → passage mode.**

1. **A resolvable path to a spec or ADR** → artifact mode. Examples:
   `/jig:explain docs/specs/062-refactor-workflow/spec.md`,
   `/jig:explain docs/decisions/adr-0021-lexicon-home-and-overlay.md`. A spec
   *directory* (`docs/specs/065-lower-vocabulary-barrier/`) resolves to its
   `spec.md`.
2. **A word or short phrase that is an exact / normalized lexicon key** → term
   mode. Examples: `/jig:explain SPIDR`, `/jig:explain "vertical slice"`,
   `/jig:explain deviation log`. Matching is case-insensitive and
   whitespace-collapsed (the lexicon's key convention).
3. **Anything else** → passage mode (a pasted snippet of jig output, or any
   text that is neither a resolvable path nor a lexicon key).

Two carve-outs sit on top of that order:

- **Term-mode honesty (do not let passage mode swallow the absent-term
  signal).** An unknown **short query phrase** — a brief, single-line argument
  that *looks* like it wants a definition but isn't a lexicon key — still routes
  to **term mode** and gets its honest *"that term isn't in the lexicon"* flag
  (see Term mode step 4). It is **not** silently absorbed into a passage-mode
  guess. Distinguish by **shape, not word count**: a short single-line phrase is
  a term query (some lexicon keys are themselves 3+ words, e.g. `closed-spec
  drift policy`); a multi-line block or output-shaped paste is a passage. Passage
  mode is for pasted output, not a greedy catch-all that erodes the absent-term
  signal.
- **Path-shaped-but-unresolvable input — ask, don't guess (clarify Q1).** When
  the argument **looks like a repo file path** — it sits under `docs/` (e.g.
  `docs/specs/…`, `docs/decisions/…`) or ends in a doc/code extension like `.md`
  — but **no file exists there**, the most likely cause is a typo, a stale path,
  or a path from another repo. **Ask the user whether they meant a file path (and
  offer to retry with a corrected one) or a snippet to explain** — don't silently
  fall through to passage mode and answer the path string as if it were prose. (A
  bare `/` alone — as in a pasted command line or URL — does **not** count as
  path-shaped; that's a passage.)

## Term mode

1. **Load the merged lexicon.** Resolve the project root, then load jig's
   shipped lexicon with the project's glossary overlaid on top, using the
   065-01 loader. Run it inline via Bash — the loader is stdlib-only:

   ```bash
   python3 -c "
   import sys, os, json
   # Auto-resolve the loader across both layouts (copy-paste-safe):
   #   jig repo -> skills/_common; scaffolded project -> .codex/skills/_common.
   for d in ('skills/_common', '.codex/skills/_common'):
       if os.path.isfile(os.path.join(d, 'lexicon.py')):
           sys.path.insert(0, d); break
   import lexicon
   merged = lexicon.load('.')             # project root; reads docs/memory/glossary.md overlay
   print(json.dumps(merged, indent=2))
   "
   ```

   (The loader lives at `.codex/skills/_common/lexicon.py` in a scaffolded
   project and `skills/_common/lexicon.py` in the jig repo itself — the snippet
   above probes both. The project glossary overlay **wins** on a collision — a
   project that redefines a term gets its own definition, per ADR-0021.)

2. **Look up the term.** Normalize the argument (lowercase, collapse internal
   whitespace) and find its key in the merged lexicon.

3. **Present the definition.** When the term is found, render:
   - the **plain-language** definition (the `plain` field — a junior-readable
     paragraph, not just the one-line `short`);
   - the **example**, if the entry has one;
   - the **see-also** terms, if present, so the reader can follow related
     vocabulary.

4. **Flag an absent term — never invent.** If the term is **not** in the merged
   lexicon, say so explicitly: *"`<term>` isn't in jig's lexicon or this
   project's glossary."* Offer the nearest matches if any look close, and
   suggest `/jig:memory-sync` if the user wants to capture it. **Do not
   fabricate a definition** for a term the lexicon doesn't carry — a confident
   wrong answer is worse than an honest gap (the clarify/AC-honesty boundary).

## Artifact mode — strong handholding

The argument is a path to a spec or ADR. Read it, resolve the artifacts it
links, and produce a **junior-grade walkthrough** with this **fixed shape**:

1. **In one sentence.** What this artifact is and what it decides/delivers, in a
   single plain sentence a newcomer can hold onto.
2. **Why it exists.** The problem or pressure that made someone write this — the
   motivation, not the mechanism.
3. **Words you'll need first.** The jig terms **a newcomer won't know**, defined
   inline from the merged lexicon (the `plain` field) — the ones load-bearing for
   this artifact, not a glossary dump of every term it uses. This is the
   vocabulary-barrier fix: the reader gets the words *before* the prose that
   uses them. If a term the artifact uses is **not** in the lexicon, flag the
   gap (don't invent) and define it from the artifact's own context if you can,
   marking it as not-from-the-lexicon.
4. **Walkthrough.** Section by section, in plain language. Translate the dense
   prose: spell out acronyms, unpack jargon, and say what each section is
   actually doing. Keep the artifact's own order.
5. **The decisions & why** *(ADRs especially)*. For an ADR, lay out the
   **alternatives considered** and the **trade-off** that settled it — the
   reasoning, so the reader understands *why* this and not the others. For a
   spec, summarize the load-bearing choices (the Clarifications / Design notes).
6. **If you had to work on this.** A short, concrete orientation: where the real
   work lives, what the reader would touch first, and the one or two things that
   would trip them up.

**Auto-pull linked refs.** While reading the artifact, follow the ADRs and specs
it links (e.g. `[ADR-0021](...)`, `[spec 055](...)`, sibling slice files) and
**read them too**, so you can resolve those references *for* the reader inside
the walkthrough instead of leaving a trail of links to chase. Pull what the
artifact directly depends on; don't recurse the entire graph — one hop of the
links that carry the artifact's meaning is the target. If a linked artifact is
missing or unreadable, note it briefly and keep going (fail-soft).

## Passage mode — explain a pasted snippet

The argument is a chunk of text the reader copy-pasted because it confused
them — typically jig output. Reuse the term-scan primitive from artifact mode,
then explain the snippet:

1. **Load the merged lexicon** (the same inline loader recipe shown under Term
   mode) and **scan the passage for jig terms** — the "Words you'll need first"
   primitive, applied to the pasted text instead of a file. Define each jig term
   present, inline, from the `plain` field. Not capped at the 065-02 hook's
   per-prompt N (clarify Q4): this is an explicit, on-demand request, so define
   as many as the passage genuinely needs — but scope to the terms that are
   **load-bearing for understanding it**, not every term present.
2. **Say what the passage is and what to do.** In plain language: what this
   snippet is telling the reader, and what — if anything — they should do next
   (e.g. *"this is a review verdict saying the slice passed; nothing to do"* or
   *"this transition was refused because another branch holds the claim — release
   it with `… --release` or pick a different slice"*).
3. **Identify the source — best-effort, never fabricated (clarify Q3 / AC3).**
   When the snippet is recognizably from a known jig surface, name it and explain
   accordingly:
   - a `VERDICT: …` block → a review verdict (compliance / craft / arch /
     reconciliation pass);
   - a `| … | … | DONE | … |` row → a `docs/specs/README.md` status-board row;
   - *"Jig terms in this prompt…"* / *"Unrecognized references in prompt…"* → the
     `jig-memory-scan` hook's `additionalContext`;
   - *"refuses a foreign still-IN_PROGRESS claim"* / *"transitioned … →"* → a
     `workflow.py` transition / claim message;
   - a numbered `implement → compliance → …` block → a `session-plan` dispatch
     plan.

   When the source is **not** recognizable, say so plainly (*"I don't recognize
   which jig surface produced this"*) and still explain the content — **do not
   invent a source.**
4. **No jig vocabulary at all → explain generically (clarify Q2).** If the
   passage contains no recognizable jig terms (generic prose, or output from a
   non-jig tool), give a plain-language read of what it appears to be, with **no
   jig framing** — explain it the way a general assistant would. (This doesn't
   conflict with the deferral clause: that only steps aside for a *richer
   installed* explanation skill, not for the absence of jig content.)
5. **Hold the honesty line (never invent).** Any jig-shaped token in the passage
   (an `ADR-####`, a `NNN-NN` slice id, a `/jig:*` skill, a `STATUS` word) that
   is **not** in the merged lexicon is flagged as unrecognized rather than given
   a fabricated meaning — the same never-invent rule as term mode.
6. **Large, artifact-like pastes → nudge toward artifact mode (clarify Q3).**
   Passage mode still processes a big block, but if the paste looks like a whole
   spec or ADR (it has the section shape, or names its own path), **suggest
   `/jig:explain <path>`** for the richer six-block walkthrough with auto-pulled
   linked refs — passage mode reads only the pasted text, artifact mode resolves
   the references too.

Passage mode is **ephemeral** like the others — it explains in chat and writes
nothing.

## Ephemeral output (writes nothing)

The skill's output is **always chat-only**. It does **not**:

- write or append to the explained artifact (no `## Explanation` section);
- create any new file;
- offer a `--save` flag or any disk-writing option.

This was resolved at clarify (Q3): explain is always ephemeral, for zero
context-cost risk and a clean hot path (055/057). If a reader wants the
explanation preserved, that's a deliberate, separate act they take (copy it into
a doc, or run `/jig:memory-sync` to capture a term) — explain itself never
writes.

## No `.py` helper

Like `/jig:clarify`, this skill ships **no helper script**. The only determinism
it needs runs inline:

- **lexicon lookup** via the 065-01 loader (`skills/_common/lexicon.py` — a
  one-line `python3 -c` invocation, shown above);
- **artifact + linked-ref reading** via the Read tool.

There is no `explain.py`; section surgery and lookups happen inline. The
trade-off, accepted for a judgment skill: the walkthrough is generated prose, so
its quality is judgment exercised by this prompt, not asserted by a unit test
(the AC-testability gap flagged at clarify, accepted — the structural surface
*is* tested: registration, ephemeral contract, no-helper, deferral language).

## Gotchas

- **Never invent a definition.** A term absent from the merged lexicon is
  flagged as absent, not fabricated. Honesty over a confident-sounding guess.
- **Project glossary wins.** The merged lexicon overlays the project's
  `docs/memory/glossary.md` on jig's shipped `lexicon.json`; a project that
  redefines a term gets its own definition (ADR-0021). Always load via the
  loader, never read `lexicon.json` alone — that would miss the overlay.
- **Ephemeral, always.** No file writes, ever. If you catch yourself about to
  Edit/Write the artifact, stop — that's not this skill.
- **One hop of links, not the whole graph.** Auto-pull the refs the artifact
  directly links; don't recurse indefinitely or you'll blow the reader's (and
  the orchestrator's) context budget.
- **Fail-soft on a degraded lexicon.** The loader returns shipped-only (or
  empty) on a missing/malformed glossary and never raises; if the lexicon is
  empty, term mode still works for whatever is shipped, and artifact mode just
  defines fewer terms in "Words you'll need first."
- **Mode is chosen by the argument, not a flag.** Resolution order: resolvable
  path → artifact mode; exact/normalized lexicon key → term mode; otherwise →
  passage mode. An unknown *single term* still goes to term mode (honest
  "absent" flag), and a path-shaped-but-missing argument is **asked about**, not
  routed to passage (see Inputs — mode precedence). There is no silent
  "ambiguous → give up" dead-end any more: a snippet that is neither a path nor
  a key is explained in passage mode.
- **Passage provenance is best-effort, never fabricated.** Name the producing
  jig surface only when you actually recognize the shape; otherwise say you
  don't recognize it and explain the content anyway. Don't invent a source.

## Relationship to other skills

- **`/jig:memory-sync`** — complementary. memory-sync *persists* a term to the
  glossary/hot cache; explain *reads* the merged lexicon to define one. When
  explain flags an absent term the user wants kept, route them to memory-sync.
- **`/jig:independent-review`** — downstream and different. independent-review
  checks a finished slice against its spec; explain helps a reader *understand*
  the spec (or ADR) in the first place.
- **`/jig:analyze`** — sibling, different scope. analyze surfaces drift
  *between* artifacts; explain illuminates *one* artifact (plus the refs it
  pulls in) for a human.
- **`/jig:clarify`** — sibling judgment skill, opposite direction. clarify asks
  the author questions to *remove* ambiguity from a DRAFT spec; explain helps a
  *reader* get through an already-written dense artifact. Both are no-helper
  judgment skills.
- **The 065-02 hook (`jig-memory-scan`)** — the just-in-time sibling. The hook
  surfaces a one-line `short` def of any lexicon term that appears in a prompt,
  automatically; this skill is the on-demand, strong-handholding escalation
  (full `plain` def, or a whole-artifact walkthrough).
