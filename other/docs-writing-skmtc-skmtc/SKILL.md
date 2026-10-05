---
name: docs-writing
version: 0.2.0
description: |
  Write, restructure, or review documentation — tutorials, how-to
  guides, reference pages, concept/explanation docs, API references,
  READMEs, changelogs, release notes, and troubleshooting guides.
  Distills documentation craft from Mintlify's guides (compiled from
  technical writers at Stripe, GitHub, Amplitude, and Anaconda), the
  Diátaxis framework (including the compass and per-type voice), the
  Google and Microsoft style guides, Every Page Is Page One, Write
  the Docs, and Docs for Developers: audience analysis, content-type
  selection, style and word-level rules, procedure writing, structure
  for humans and AI agents, code-example standards, page templates
  (templates.md), mechanical enforcement and llms.txt (mechanics.md),
  maintenance, and success metrics.

  Use this skill when the user asks to "write docs", "document this
  feature", "improve this page", "review these docs", "write a
  tutorial / how-to / reference page", "structure the docs",
  "write API documentation", "write a README / changelog", or when
  authoring any file under a `docs/` tree. For SKMTC docs
  specifically, this skill governs the *craft* (what makes the page
  good); the content split between skills, `llms.md`, and the docs
  tree is governed by `docs/skills/README.md`.

  Distinct from `skmtc-retro` (captures observations about work) and
  the `skmtc-*` operational skills (guide doing the work) — this
  skill guides writing *about* the work for readers.
allowed-tools:
  - Read
  - Write
  - Edit
  - Glob
  - Grep
  - Bash
metadata:
  internal: true
---

# Writing documentation

Documentation craft distilled for the moment of writing. The core stance:
**people don't read docs for fun; they arrive with a goal — and they read at
most ~20–28% of the words on a page** (NN/g). Every rule below serves getting
the reader from arrival to accomplished goal with minimum friction — and the
same properties that serve a skimming human serve an AI agent reading the page.

Companion files, read on demand:

- `templates.md` — page skeletons + quality bars for how-to, tutorial,
  reference, concept, README, changelog, release notes, and troubleshooting
  pages.
- `mechanics.md` — mechanical enforcement (Vale, markdownlint, link checking,
  testing code examples) and the llms.txt format.

## 1. The seven principles that override default writing intuitions

Writing docs is not writing prose. These override what generic "good writing"
instincts would suggest:

1. **Verify before you document.** Never document behavior you haven't executed,
   observed, or read in the source. LLM-written docs fail here in characteristic
   ways: plausible flags that don't exist, documented _intent_ instead of actual
   behavior, invented defaults, hedged claims papering over unchecked ones. If
   you can't run it, read the code that implements it; if you can do neither,
   mark the claim unverified rather than asserting it. This is the docs analogue
   of `skmtc-debug`'s verify-first stance.

2. **One page, one content type, one persona.** Decide _before_ drafting whether
   the page is a tutorial, how-to, reference, or explanation (§3), and who it's
   for (§2). "Writing for multiple audiences leads to compromises that satisfy
   no one." A page that teaches AND exhaustively catalogs AND justifies design
   does none of them well.

3. **Lead with the answer, not the context.** Readers scan in an F-pattern and
   abandon pages whose opening doesn't confirm what the title promised. Put the
   outcome or instruction in the first paragraph; front-load the
   information-carrying words in headings. A reader should be able to leave
   after the first paragraph having gotten what they came for.

4. **The curse of knowledge is the default failure mode.** You know how
   everything works; the reader doesn't. State prerequisites explicitly, define
   acronyms on first use, never assume internal conventions (naming schemes,
   auth flows, team shorthand) are known. Validate against real evidence —
   support tickets, friction logs, user questions — not assumptions. Test: could
   someone who joined yesterday follow this?

5. **Every page is page one.** Readers arrive from search engines, deep links,
   and AI retrieval — never at your table of contents. Each page must establish
   its own context (what it covers, who it's for, what it assumes) in its
   opening. Reading-order dependencies ("as mentioned above", "in the previous
   section") are forbidden; link to supporting material instead.

6. **Code examples are load-bearing, not decorative.** Many readers only read
   the code blocks. Every example must be complete and runnable as-copied —
   imports, setup, the call, response handling. "A code example is worth a
   thousand words."

7. **Wrong docs are worse than no docs.** "Consider incorrect documentation to
   be worse than missing documentation" (Write the Docs). Outdated or misleading
   content wastes users' time and erodes trust in the whole product. When you
   can't maintain a page, delete it — removal often serves users better than
   retention.

## 2. Know your audience

Center the reader's goal, not the product's feature list.

### The four personas

| Persona                  | Needs                              | Serve with                                                                          |
| ------------------------ | ---------------------------------- | ----------------------------------------------------------------------------------- |
| Technical decision maker | Evaluate fit and architecture      | Overviews, concept docs, comparison-friendly framing                                |
| New end user             | Get to first success fast          | Getting-started tutorial, quickstart                                                |
| Integrating developer    | Implement correctly                | How-tos, reference, complete examples                                               |
| AI agent / LLM           | Retrieve and act without inference | Structure, explicit prerequisites, self-contained sections, unambiguous terminology |

Pick **one** primary persona per page. The AI-agent persona is served by the
same properties that serve skimming humans — clear headings, semantic markup,
defined terms, runnable examples — so it rarely needs separate pages, but it
does raise the bar on explicitness (§6).

### Defeating the curse of knowledge

- Talk to users (or their proxies: support, UX research, product). Harvest the
  _terminology they actually use_ — it often differs from internal naming, and
  it's what they'll search for.
- **Keep a friction log**: use the product as a new user would and record every
  step — expected vs. actual, every confusion, workaround, and surprise. Each
  entry is either a docs fix or a product bug; file it as one or the other.
  (This ecosystem already runs one at `docs/friction-log/`.)
- Use the five W's to define a page's scope before writing: who is this for,
  what will they accomplish, why would they need it, where/when does it apply —
  then how.
- Embed with support: recurring tickets are a ranked list of doc gaps.
- Test docs by asking an AI assistant product questions and seeing whether the
  docs let it answer correctly — a cheap proxy for "does the page carry its own
  context".
- **Assume the reader is qualified** for the page's task; don't explain basics
  inline. Give unqualified readers enough context to _recognize_ they're on the
  wrong page, plus a link to where they can qualify themselves — a page "can't
  bring every possible reader up to speed without becoming a textbook."
- Don't over-document niche edge cases in guides; route those to community
  channels and keep guides focused on majority paths. (Reference is different —
  see §3: exhaustive within its scope.)

## 3. Content types (Diátaxis)

Four types, distinguished by what the reader is trying to do. Assign each page
exactly one type before drafting.

| Type             | Reader's goal               | Reader's mode | Structure                            | Voice                              |
| ---------------- | --------------------------- | ------------- | ------------------------------------ | ---------------------------------- |
| **Tutorial**     | "Teach me by doing"         | Study         | Linear steps, guaranteed outcome     | Guiding: "we", first person plural |
| **How-to guide** | "Solve my specific problem" | Work          | Problem → solution steps, may branch | Direct, conditional imperatives    |
| **Reference**    | "Give me the precise fact"  | Work          | Scannable catalog, consistent format | Neutral, terse, austere            |
| **Explanation**  | "Help me understand why"    | Study         | Discursive, conceptual               | Reflective, comparative            |

### The compass — when the type is unclear

Ask two questions about the content (works at page, section, or sentence level):

1. Does it inform **action** (doing) or **cognition** (thinking)?
2. Does it serve **acquisition** of skill (study) or **application** of skill
   (work)?

action + acquisition → tutorial · action + application → how-to · cognition +
application → reference · cognition + acquisition → explanation.

**Type is function, not difficulty.** An advanced course is still a tutorial (a
lesson, safely in the instructor's hands); a trivial one-step procedure is still
a how-to (a worker's task). "Beginner content = tutorial, advanced content =
how-to" is Diátaxis's most common and most harmful misreading — classify by
study-vs-work, never by difficulty.

Navigation should mirror the split: Getting Started → Guides → Reference →
Concepts. The SKMTC docs tree instantiates this as `using/tutorials/` +
`using/how-to/` + `using/recipes/`, `authoring/` (same trio), `reference/`, and
`concepts/` + `explanation/`. **Recipes are how-to guides in recipe form** — the
recipe is Diátaxis's own model for the type (assumes competence, answers one
specific question, no teaching). The four types classify _needs_, not directory
names; a section may be named anything so long as each page serves one need
well.

### Writing rules per type

**Tutorials** — learning-oriented:

- Open by stating exactly what the reader will have built/achieved at the end.
- First person plural, teacher's voice: "In this tutorial, we will…";
  unambiguous imperatives: "First, do x. Now, do y."
- Every step delivers a **visible result**, and the text names it: "The output
  should look something like…" — checkpoints let readers self-verify they're on
  track.
- Small incremental steps; a tutorial "doesn't offer choices or alternatives" —
  one carefully-managed path.
- Teach through experience, not explanation — link to explanation docs rather
  than digressing: "We must do x before y because… (see [explanation] for
  details)."
- Must work every time: "so well constructed that things can't go wrong" — a
  tutorial that fails at step 4 loses the user, possibly permanently. Expect
  high maintenance cost as the product evolves.

**How-to guides** — task-oriented:

- Title is the task in the user's words ("Skip operations for one generator"),
  not the feature's name.
- **Conditional imperatives** carry the branching: "If you want x, do y. To
  achieve w, do z." (Tutorials never branch; how-tos usually do.)
- About goals, not machinery: address the real-world task, not a walkthrough of
  the tool's controls.
- Assume foundational knowledge; state the specific prerequisites, then skip the
  obvious steps.
- "Practical usability is more helpful than completeness" — only the context
  necessary for _this_ task; offload option inventories to reference: "Refer to
  the x reference for a full list."

**Reference** — information-oriented:

- "Austere and uncompromising": describe, and _only_ describe. Neutral statement
  of fact; no instruction, no rationale.
- Structure mirrors the product's structure, and entry order mirrors the source
  of truth, so drift is visible.
- Maximize scannability: tables, identical per-entry format, parallel phrasing,
  one naming convention across every entry.
- Copy-paste-ready examples per entry (examples illustrate without explaining —
  they're welcome); required vs. optional marked explicitly; constraints and
  defaults stated, not just the name restated.
- Exhaustive within its declared scope — a reference that omits entries is
  broken in a way a how-to never is.

**Explanations** — understanding-oriented:

- The "About" test: an explanation title should tolerate an implicit "About …"
  prefix ("About user authentication"). If it can't, the page probably isn't
  explanation.
- Cover design decisions, constraints, and the alternatives that were rejected
  (and why).
- Opinion is allowed and required here: explanation "can and must consider
  alternatives, counter-examples or multiple different approaches."
- Explanation "tends to absorb other things" — expel instruction and technical
  description to their proper homes.

### Type-mixing smells

- A tutorial that pauses for three paragraphs of rationale → move the rationale
  to an explanation doc, link it.
- A tutorial offering choices ("you could also use…") → cut; one path.
- A reference entry with step-by-step setup → extract a how-to.
- A how-to that exhaustively lists every option → extract reference material,
  keep only the options the task needs.
- A how-to that keeps stopping to teach → trust the reader's competence; link
  the tutorial instead.
- Time-sensitive content (release notes, announcements) in evergreen docs →
  belongs in a changelog or blog (see `templates.md`).

**Scoped exception — API reference surfaces.** Reference pages for an HTTP API
may deliberately blend the catalog with per-language samples, request/response
pairs, and short usage notes (the Stripe pattern, §8). That blend is confined to
the API reference surface; docs-tree pages keep one type each.

### Applying Diátaxis incrementally

Don't restructure top-down into four empty boxes and shovel content in —
"Diátaxis changes the structure of your documentation from the inside." The
loop: choose something small; assess what user need it serves and how well;
decide on a single next action; do it and publish immediately. Documentation is
_never finished_ — but at every moment it can be _complete_: useful, correct,
and coherent at its current scope. Never hold back an improvement waiting for
"done".

## 4. Style and tone

- **Cut ruthlessly — within a section.** Every unnecessary word taxes a reader
  who is there to get something done. But brevity governs sentences and
  paragraphs; **explicitness governs boundaries**: restating context at a page
  or section opening is not filler — it's the entry point for a reader (or
  retrieval chunk) landing there (§1.5). Cut words, not context.
- **Active voice, imperative mood.** "Create a file", not "a file should be
  created".
- **Second person.** "You" — the doc serves the reader's task. (Exception:
  tutorials use "we" — §3.)
- **Short paragraphs** (2–4 sentences), meaningful headings, lists for
  enumerable things, tables for structured facts.
- **One term per concept, everywhere.** "API key" and "API token" used
  interchangeably reads as two different things. Pick one; grep for the other
  (enforceable with a Vale `consistency` rule — `mechanics.md`).
- **Don't narrate the obvious.** "Click Save to save" is negative value.
  Document what isn't intuitive.
- **Spelling and grammar are trust signals.** Errors in the docs read as errors
  in the product.

### Word-level rules (bad → good)

The high-leverage subset of the Google and Microsoft style guides — rules a
fluent writer (or LLM) gets wrong by default:

- **Delete "simply", "easily", "just", "obviously", "of course".** What's easy
  for the writer isn't for the reader; the sentence survives without them.
  "Simply run the installer" → "Run the installer."
- **No "please" in instructions.** "Please click Save" → "Click Save."
- **Present tense for product behavior; never "will" or "would".** "The server
  will send an acknowledgment" → "The server sends an acknowledgment."
- **Timeless docs: ban "currently", "new", "now", "soon", "as of this writing",
  "latest", "old", "eventually".** "The emulator now supports filters" → "The
  emulator supports filters." If "new" is unavoidable, anchor it to a date.
  Exception: changelogs and release notes.
- **No anthropomorphism.** Software doesn't want, think, see, know, or care.
  "The PC sees a new device" → "The PC detects a new device."
- **"may" = permission only; "might" = possibility; "can" = ability.** "The call
  may fail" → "The call might fail."
- **"should" is ambiguous** — use "must" for requirements; rewrite
  recommendations as "we recommend" or a direct imperative.
- **Spell out Latin abbreviations**: "e.g." → "for example", "i.e." → "that is";
  avoid "etc." (finish the list or use "such as").
- **"allows you to" / "enables you to" → "lets you"** — or make the reader the
  subject: "The API allows you to filter results" → "Filter results with…".
- **"in order to" → "to"; "utilize"/"leverage" → "use".**
- **Start instructions with the verb** — kill "You can…" and "There is/are…"
  openers. "You can access the settings from…" → "Open the settings from…".
- **Sentence-style capitalization for all headings.** Never Title Case. Oxford
  comma always. Contractions are fine.
- **"select"** for UI interaction (not "click"/"tap" — accurate for keyboard,
  touch, and assistive tech); **select/clear** checkboxes (never
  "check"/"uncheck").
- **Never inflect code identifiers** — attach a noun and inflect that: "`Node`s"
  → "`Node` objects"; "`ADDRESS`'s value" → "the `ADDRESS` constant's value".
- **Inclusive defaults**: allowlist/blocklist, primary/replica, placeholder (not
  dummy), "stops responding" (not hangs), singular "they" (never "he/she").

### Writing for a global audience

Docs are read by non-native speakers and machine translation:

- Short sentences, one idea each; no more than two clauses chained with
  and/or/but.
- Keep optional function words — "Verify all tables migrated" → "Verify **that**
  all tables **were** migrated."
- Avoid ambiguous connectives: "once" → "after"/"when"; "while" →
  "although"/"during"; "since"/"as" → "because" (unless temporal).
- Place "only" immediately before the word it modifies: "Only request one token"
  → "Request only one token."
- No noun stacks (max two nouns as modifiers), no phrasal verbs where a single
  verb exists, no idioms, colloquialisms, humor, or culture-bound references.
- Dates: spell out the month ("January 19, 2026") or ISO 8601 (2026-01-19);
  never 04/15/17; never seasons.

Lean on the Google or Microsoft style guide for the long tail; automate
enforcement with Vale in CI (`mechanics.md`) rather than relitigating style in
review.

## 5. Writing procedures

Step sequences have their own mechanics (Google/Microsoft procedure rules):

- **Numbered list; one action per step.** Combine actions only when they're
  trivial and happen in the same place.
- **Location and purpose before action**: "In Google Docs, select **File >
  New**" — not "Select **File > New** in Google Docs". "To start a new run,
  click…" — the goal first, so the reader can skip steps they don't need.
- **State a step's result in the same paragraph as the action**, after it — not
  as its own numbered step: "Drag the tiles to an open space. When a gray bar
  appears, release them."
- **A single-step procedure is one bullet**, not "1.".
- **Optional steps start with "Optional:"**.
- **End with the completing action** — the **Save**/**Apply** step; don't leave
  the procedure hanging. If the end state isn't obvious, say what success looks
  like.
- **Menu paths**: bold items separated by ">" (**File > New > Document**); use
  one convention throughout, and only when every hop uses the same interaction.
- **One method per procedure.** Alternatives and keyboard shortcuts belong in a
  reference table, not woven into the steps.
- **Task-phrased, parallel headings** ("Create a profile", "Add an account");
  don't follow the heading with a sentence that repeats it.

## 6. Structure for humans AND AI agents

The same page properties serve skimming humans, search engines, and LLM
retrieval. Optimize once:

- **Establish context in the opening**: what the page is about, who it's for,
  where it fits — position in the nav tree doesn't travel with the page into a
  search result or a retrieval chunk.
- **Descriptive headings with honest information scent.** Readers choose links
  and sections by an estimate of what's behind them — from the label alone.
  "Rate limiting" beats "Keeping things under control"; phrase task headings the
  way a user would ask ("Rotate an API key"). A heading should answer "is my
  answer in this section?" without reading the section. Over-promising titles
  get the page abandoned and burn trust.
- **Semantic markup**: proper heading hierarchy (H2 → H3 → H4, no skipped
  levels), lists for enumerations, tables for structured data (headers in the
  first row only, no merged cells), fenced code blocks with language tags.
- **Explicit prerequisites** at the top of task pages — humans skip them at
  their own risk; AI agents cannot infer unstated context.
- **Definitions before edge cases; common cases before advanced.**
- **Stay on one level.** Don't oscillate between high-level principle and
  low-level detail on one page; link _up_ to concepts and _down_ to reference
  and let the reader change levels when they choose.
- **Link richly, along subject affinity** — every page is a hub. Descriptive
  anchors ("see the enrichments reference"), never "click here"; no positional
  language ("above"/"below" → name the section or link it).
- **Self-contained sections**: a section pulled out of the page by a retrieval
  system should still make sense. Restate the subject noun (not "it"); restate
  (briefly) rather than relying on "as mentioned above".
- **Conform to type**: pages with the same purpose share the same sections in
  the same order (`templates.md`) — predictability serves scanners, and a
  defined shape makes gaps visible.
- **Document error scenarios and deprecations explicitly** — error strings are
  among the highest-value search and retrieval targets, and the least often
  documented.
- Delete or clearly mark outdated content: AI retrieval surfaces deprecated
  pages with no sense of staleness.
- **Ship the machine surface**: an `/llms.txt` index (and `llms-full.txt` if the
  corpus fits a context window) — format and rules in `mechanics.md`.

### Validating the structure

- Analytics: where do readers enter, what do they search for ( especially
  searches with zero results), where do they exit.
- Session paths: do readers follow the navigation you designed, or fight it?
- Direct tests: watch a user (or a new hire — an excellent proxy) try to answer
  a specific question using only the docs.
- Common pitfalls: overloaded top-level categories (seven items is a comfortable
  limit for an unordered list), essential pages buried three levels deep,
  section labels only insiders understand.

## 7. Code examples

The most-read part of any developer doc. Standards:

- **Runnable as-copied.** Full workflow: imports, setup, authentication
  placeholder, the call, response handling. A fragment that needs unstated
  scaffolding is a support ticket.
- **Realistic data** — not `foo`/`bar`; use values shaped like real usage so
  readers can map the example onto their case.
- **Placeholders in `UPPER_SNAKE_CASE`**, followed by "Replace the following:"
  with one line per placeholder in order of appearance.
- **Show the expected output/response** alongside the request, so readers can
  verify success without guessing.
- **Include error handling** in longer examples — it's where real integrations
  spend their time.
- **Multiple languages via tabs** where the audience spans ecosystems; every
  tab's example kept equivalent.
- **Test examples in CI.** A fenced code block is a claim; untested claims rot,
  and an example that rots is worse than none (§1.7). Extraction and doc-testing
  patterns per ecosystem are in `mechanics.md`; mark deliberately non-runnable
  fragments so the untagged default stays "this must run".

## 8. API documentation

The specialized high-stakes case. Structure around the developer's journey, and
measure it by **time-to-first-successful-call**.

### Required components

| Component       | Bar to clear                                                                                                    |
| --------------- | --------------------------------------------------------------------------------------------------------------- |
| Getting started | Working integration inside ~15 minutes; never buried                                                            |
| Authentication  | Step-by-step credential setup, token placement, expiry and rate limits, per-method examples (curl + SDKs)       |
| API reference   | Complete request/response cycles — paths, methods, parameters, schemas, status codes — not a bare endpoint list |
| Guides          | Organized by real tasks ("Send a message", "Accept a payment"), not by endpoint inventory                       |
| Error catalog   | Every error code with context and the _remediation_, including near-miss distinctions (400 vs 422)              |
| Changelog       | Timestamped, discoverable, flags breaking changes and deprecations loudly (`templates.md` for the format)       |

### Practices that separate the best API docs

- **Pair generated reference with authored guides.** Auto-generation from an
  OpenAPI spec is a starting point only — it has no editorial judgment, no
  use-case coverage, no workflow ordering. Layer opinionated guides on top;
  never ship the generated reference alone.
- **Workflow-first organization** (the Stripe pattern): each reference page
  carries descriptive titles, per-language samples, realistic request/response
  pairs, and usage notes. This is the sanctioned type-blend — scoped to the API
  reference surface (§3).
- **Copy-paste-ready everywhere**, ideally with the reader's own test
  credentials injected when docs are behind a logged-in state — but never
  _require_ login to read the docs; gated docs kill self-service evaluation.
- **Skimmable and searchable**: developers arrive with a task, not to read
  linearly.
- **Interactive playgrounds** on reference pages turn specs into executable
  experiences.
- **Design for LLM consumption**: consistent formatting and rich examples let AI
  assistants generate correct integration code from your docs — an adoption
  channel in its own right.

## 9. Page templates

`templates.md` holds compressed skeletons — ordered sections, a one-line note
per section, and the 2–3 quality criteria separating a good instance from a
mediocre one — for:

how-to guide · tutorial · reference entry · concept/explanation · README ·
changelog (Keep a Changelog format) · release notes · troubleshooting guide

Use them as the "conform to type" baseline (§6): start from the skeleton, delete
sections that genuinely don't apply, and keep the order. Two worth
internalizing:

- **README = cognitive funnel, not manual.** Broadest first — what it is (< 120
  chars), who it's for, a runnable usage example — so the reader can bail out at
  any depth having lost minimal time. Depth belongs in the docs tree; the README
  links there. License last.
- **Changelogs are for humans, not machines.** Never paste `git
  log`. Group by
  Added/Changed/Deprecated/Removed/Fixed/Security, newest first, ISO dates, an
  `[Unreleased]` section at the top, and _always_ announce deprecations one
  version before removal — selective entries "can be as dangerous as not having
  a changelog".

## 10. Media

Media is supplementary. **If the workflow is clear in text alone, don't add
visuals** — every asset is a maintenance liability that silently rots when the
UI changes. Screenshots for UI elements that are hard to describe; diagrams as
code (Mermaid — text-diffable) over image exports; video only for long
procedures, and only with captions. Non-negotiable: alt text on images
(descriptive and specific — "OAuth 2.0 flow", not "diagram"), and never present
information _only_ in an image — it's invisible to screen readers, search, and
AI retrieval alike.

## 11. Discoverability (SEO and AEO)

Most readers arrive from a search engine or an AI assistant, not your nav.
**Answer Engine Optimization is §6 done well** — there is no separate trick:
literal headings, self-contained sections, defined terms, stated prerequisites,
complete examples, documented errors and deprecations, loud deprecation markers.
The classic mechanical layer still applies: titles ~50–60 characters and meta
descriptions ~150–160 frontloading the terms users actually search (harvested
from user language, §2); descriptive link anchors; compressed images; a current
sitemap. Skip structured-data gymnastics unless you have evidence your audience
arrives through them.

## 12. Maintenance

Docs rot by default; only a system prevents it.

- **Docs-as-code**: docs live in git, change via PRs, deploy automatically,
  version alongside the code they describe. Review catches errors before
  publication and lets engineers contribute through tools they already use.
- **ARID, not DRY** — "Accept (some) Repetition In Documentation." Docs are read
  in fragments, so they can't be as DRY as code: single-source what you can,
  duplicate deliberately where the reader needs it in place — and give every
  duplicated fact one designated canonical home so drift is detectable (this
  ecosystem's selective-duplication policy in `docs/skills/README.md` is this
  principle applied).
- **Couple docs to shipping**: a user-facing change isn't done until its docs
  are updated — enforce in the definition of done or PR template, and automate
  detection of drift (e.g. flag when the OpenAPI spec changes but the guide
  didn't).
- **Automate the boring checks**: broken links, heading hierarchy, missing alt
  text, filler words, terminology consistency, example compilation — the full
  toolbox with configs is in `mechanics.md`.
- **Edit in sequenced passes, one concern each** — drafting and editing are
  different acts; never do both at once. The order: (1) technical accuracy — do
  the instructions produce the promised result; (2) completeness — can the
  reader succeed with what's here; (3) structure — do headings and prerequisites
  guide the reader; (4) clarity and brevity — cut. Self-review with the §13
  checklist first, then peer review with a _specific ask_, then expert technical
  review for complex topics.
- **Prioritize by impact, not schedule**: the 10 most-viewed pages get
  disproportionate attention. Use the traffic × rating grid:
  high-traffic/low-rating pages are the urgent queue; low-traffic/ high-rating
  pages hold patterns worth replicating.
- **Assign ownership.** Documentation without a named owner diffuses into no
  one's job and quietly dies.
- **Deprecate before deleting**: mark the content deprecated in place, point to
  the replacement, give notice — then delete what no longer serves users (§1.7).

## 13. Measuring success

Numbers require interpretation — "don't fall into the trap that a bigger number
means better performance."

| Signal                                     | Reading it honestly                                             |
| ------------------------------------------ | --------------------------------------------------------------- |
| Page views                                 | Interest — or bots, or a product bug driving people to the docs |
| Time on page                               | Engagement — or frustration hunting for an answer               |
| Zero-result searches                       | Direct gap list; the highest-signal analytic                    |
| Thumbs-up ratio                            | Target ~75%+; below that, the page misleads or misses           |
| Support ticket volume on documented topics | The docs' business case: each deflected ticket is the win       |
| AI-assistant query logs                    | What users actually ask, in their words — feeds §2              |

Compare against your own baseline over time, not absolute thresholds. Tie the
program to business outcomes: onboarding speed, support deflection, retention.

## 14. Pre-publish checklist

Before a page ships:

- [ ] Every behavioral claim verified — executed, observed, or read in source;
      anything unverifiable is marked, not asserted (§1.1)
- [ ] One content type, chosen via the compass if unclear; no type-mixing smells
      (§3)
- [ ] One primary persona; prerequisites stated at the top
- [ ] The answer/outcome appears in the first paragraph; the opening establishes
      context for a reader arriving from search
- [ ] Headings are descriptive, front-load key terms, and don't skip levels
- [ ] Every code example runs as-copied and shows expected output; non-runnable
      fragments are marked
- [ ] Terminology consistent — grep for known synonyms of key terms
- [ ] No filler (`simply|easily|just|obviously`), no time-bound words
      (`currently|new|soon`) outside release notes, present tense for product
      behavior (§4)
- [ ] Procedures follow §5: one action per step, location before action, results
      stated, completing action present
- [ ] Page conforms to its type's skeleton (`templates.md`)
- [ ] Errors and edge cases the reader will hit are documented
- [ ] Links have descriptive anchors and resolve; no positional language
- [ ] Images have alt text; media passes the "necessary?" test (§10)
- [ ] Title/description frontload searchable terms
- [ ] The page has an owner and a reason to exist that analytics could later
      confirm

## 15. Task cards

### Card: Documenting a new feature

1. Identify the persona and their goal (§2). Write the five W's.
2. **Verify the behavior first** (§1.1): run the feature, note the actual
   commands, flags, outputs, and failure modes — this raw material is the
   draft's skeleton and its fact-check.
3. Split the material by type (§3): quickstart steps → tutorial or how-to;
   option/flag inventory → reference; design rationale → explanation. Resist the
   single mega-page.
4. Outline first — every step the reader needs, then reorder to the reader's
   flow. Draft the how-to first (it forces the user-goal framing) from its
   `templates.md` skeleton, then extract reference entries, then backfill
   explanation.
5. Write and _run_ every code example.
6. Edit in passes — accuracy, completeness, structure, brevity (§12) — then run
   the §14 checklist; place pages in the tree by type.

### Card: Reviewing/auditing an existing page

1. Determine its intended type (use the compass, §3) and persona. If
   undeclarable, that's finding #1.
2. Check the opening: does it establish context and state what the page
   delivers?
3. Run examples. Diff terminology against the rest of the docs.
4. Check staleness against the product's current behavior — wrong content is the
   highest-severity finding (§1.7).
5. Grep for the mechanical smells: filler words, time-bound words, "click here",
   skipped heading levels (§14).
6. Verdict per finding: fix, split (type-mixing), or delete.

### Card: Standing up docs for a new project

1. Skeleton by type: Getting Started → How-to Guides → Reference → Concepts
   (§3), pages from `templates.md`.
2. Write the getting-started path first and make it bulletproof — working result
   in ≤15 minutes.
3. Reference next (breadth), explanations last (depth).
4. Wire the maintenance system before content grows: docs-as-code, link
   checking, prose lint, docs-updated-with-change policy, and the machine
   surface (llms.txt) — configs in `mechanics.md`.
5. Thereafter improve incrementally (§3): one small published step at a time;
   never a big-bang restructure.

## 16. Sources

Distilled July 2026 from:

- Mintlify Guides — https://mintlify.com/guides/introduction
  (`know-your-audience`, `content-types`, `writing-style-tips`, `navigation`,
  `media`, `seo`, `maintenance`, `success`), itself compiled from interviews
  with technical writers at Stripe, Amplitude, Anaconda, and GitHub; plus
  Mintlify's API-documentation recommendations and developer-docs blog posts
- Diátaxis framework — https://diataxis.fr (the four types, the compass,
  tutorials-vs-how-to, complex hierarchies, per-type language guidance, quality;
  Daniele Procida)
- Google developer documentation style guide —
  https://developers.google.com/style (word list, tense, anthropomorphism,
  timeless documentation, procedures, link text, accessibility, translation)
- Microsoft Writing Style Guide — https://learn.microsoft.com/en-us/style-guide/
  (top 10 tips, bias-free communication, global communications, step-by-step
  instructions)
- Every Page Is Page One — Mark Baker (the seven characteristics of EPPO topics;
  information foraging) — https://everypageispageone.com
- Write the Docs — https://www.writethedocs.org/guide/ (docs principles incl.
  ARID, docs-as-code, style guides)
- Docs for Developers (Bhatti, Corleissen, Lambourne, Nunez, Waterhouse) —
  https://docsfordevelopers.com (friction log, drafting process, editing passes,
  content taxonomy)
- Nielsen Norman Group — how little users read, the F-shaped pattern,
  information scent — https://www.nngroup.com/articles/
- The Good Docs Project templates — https://thegooddocsproject.dev (via
  `templates.md`)
- Keep a Changelog 1.1.0 — https://keepachangelog.com (via `templates.md`)
- Art of README + standard-readme (via `templates.md`)
- llms.txt spec — https://llmstxt.org; Vale — https://vale.sh; markdownlint;
  lychee (via `mechanics.md`)
