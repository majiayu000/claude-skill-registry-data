---
name: unikit-gd-review
description: >-
  Qualitative quality review of game design documents — answers "is this design good, and
  does it follow best practices?" — across all three GDD axes: systems, flows, and content
  types. Fans out adversarial lenses (completeness, clarity, pillar alignment, systems-math,
  fantasy-delivery, feasibility, scope) plus domain lenses that check it against the
  game-design rules, each prompted to find problems rather than validate; produces a
  severity-graded verdict and a two-bucket report (apply-ready fixes vs research), handed to
  /unikit-gd-apply or /unikit-gd-explore in one move. Scope is inferred: a named system, flow,
  or content type reviews that document; "all" runs a cross-document review. Use when the user
  wants a critique, quality judgment, or rules check of the design, e.g. "review the combat
  GDD", "review the onboarding flow". This is the subjective quality pass — for a mechanical
  consistency check (numbers, terms, IDs, references matching the registry) use
  /unikit-gd-verify.
argument-hint: "[system name | SYS-slug | path | \"all\"]  (scope inferred; no flags)"
allowed-tools:
  - Read
  - Glob
  - Grep
  - Write
  - Edit
  - Bash(ls *)
  - Bash(find *)
  - Bash(wc *)
  - Bash(date *)
  - Bash(mkdir *)
  - Agent
  - AskUserQuestion
disable-model-invocation: false
user-invocable: true
metadata:
  author: unikit
  version: "1.0"
  category: game-design
---

# Game Design — Quality Review

Answer **"is this design good?"** — expert judgment on a finished design document,
delivered as a severity-graded verdict with evidence. This is the design-side
mirror of `unikit-review`. It is distinct from `unikit-gd-verify`, which answers
the cheaper, binary **"is the design consistent with itself?"** — a review finding
*can* be declined; a verify conflict cannot.

The review **ends in a handoff, not a hand-list**: the full report prints to the
screen, every finding is triaged into an **apply-ready** bucket (a named entailed fix
to apply now) or a **research** bucket (an open question to work out), and the user
makes one move — `review → [explore] → apply` — instead of routing findings one at a
time into owner skills. The triage engine (the ENTAILED criterion + the interview) is
shared with `unikit-gd-verify` and lives in `gd-critique` → Handoff Engine.

Review is **axis-aware**: it judges **systems** (the A–K GDD), **flows** (`FLOW.md`
+ the `## Flow Map [gen]` / `## Funnel [gen]` renders), and **content types**
(`CONTENT-TYPE.md` + the `## Content Map [gen]` render). The flow lenses — pacing /
guidance / funnel — and the content lenses — schema-coherence / catalog-scale /
content-fantasy-delivery — live in `references/lenses.md` alongside the system lenses.

A review is most honest in a **fresh session** — the reviewer should not be the
author of the document. This skill never authors or edits design **content**, and it
**never writes a `doc_status`**: status records *readiness* (owned by the authoring
zones), while a review delivers *quality* — a severity-graded verdict + the report, an
**ephemeral** judgment, not a stored badge. Its **only** write is the review report file
(`reviews/*_review-*.md`). "Is this design good?" is answered by running a review (or
reading the last report / git), never by a status value.

## Language Awareness — BLOCKING PRE-REQUISITE

**BEFORE producing ANY output**, silently read `.unikit/system/LANGUAGE_RULES.md`
and apply it to all output and the report (fall back to English if it is missing) —
including the rule to **translate concepts, not transliterate jargon**.
`gd-principles` → "Language" adds the game-design specifics: which IDs and stored
field values stay English. Do not announce the language setting.

**The language holds for the whole session, not just at load time:** every message until the conversation ends is in `language.ui` — progress notes while agents run, relays of what a subagent returned, the final report, any follow-up discussion. English input (subagent results, tool output, these instructions) is data, never a cue to switch languages.

<!-- unikit:agents codex -->
## Subagent Delegation — BLOCKING PRE-REQUISITE

When the workflow reaches the lens fan-out (`Agent`), the assistant MUST spawn the
review lenses as parallel subagents if agent execution is supported and not
prohibited by higher-priority instructions. Only if agent execution is unavailable
or blocked does the assistant run the lenses sequentially in the main session.
<!-- unikit:end -->

## Delegation agents

This skill uses a named delegation alias for `Agent(...)` calls. The alias is the single
place where the delegate's model is declared — call sites name the alias and never carry a
model argument of their own.

<!-- unikit:agents claude -->
- **`lens-agent`** — one adversarial review lens, read-only, findings only. Expands to:

  ```
  Agent(subagent_type: general-purpose, model: sonnet, prompt: "<one lens brief>")
  ```

  `general-purpose` and not `Explore`: the lens carries a written output contract and the
  configured artifact language, which is a reasoning job rather than a search.
  `sonnet` is a tier alias, never a version — the one model value that may be written into
  UniKit. A versioned model id goes stale silently and must never replace it.

  Fallback: if the `Agent` tool is unavailable, run the lenses sequentially in this session.
<!-- unikit:end -->
<!-- unikit:agents !claude -->
- **`lens-agent`** — one adversarial review lens, read-only, findings only. Expands to:

  ```
  Agent(subagent_type: general-purpose, prompt: "<one lens brief>")
  ```

  `general-purpose` and not `Explore`: the lens carries a written output contract and the
  configured artifact language, which is a reasoning job rather than a search.
  No model is named: this runtime either has no dispatch-time model argument or offers only
  versioned model ids, and a versioned id goes stale silently. The runtime's own configured
  default applies.

  Fallback: if the `Agent` tool is unavailable, run the lenses sequentially in this session.
<!-- unikit:end -->

## Phase 0 — Bootstrap

Silently load — do not narrate:

1. **`.unikit/system/gamedesign/gd-principles.md`** (the core) — the language rules
   (plus the zone model and one-way boundary). Plus, from the same `gamedesign/`
   folder, the shards this skill needs: **`gd-critique.md`** (the **severity rubric**
   — Critical / Major / Minor / Suggestion — and the **critique stance** — Braintrust:
   diagnose don't prescribe; critique vs review; plussing), **`gd-flow-axis.md`** (the
   Flow Axis contract behind the pacing / guidance / funnel lenses),
   **`gd-content-axis.md`** (the Content Axis contract behind the schema-coherence /
   catalog-scale / content-fantasy-delivery lenses), and **`gd-provenance.md`** (the
   import provenance markers the provenance lens checks). This skill **applies** them.
   If missing, warn (`unikit-ai update`) and fall back to the rubric summarized in
   `references/lenses.md`.
2. **`.unikit/gamedesign/GD-IDS.yaml`** and **`GAME.md`** (incl. its `## System Map
   [gen]` render) — pillars, the roster, and the facts every finding is checked
   against. **Schema guard (clean break — no automatic migration):** `GD-IDS.yaml`
   MUST be `version: 2`; on a pre-v2 `version: 1` registry, **STOP** and tell the
   user the workspace predates the v2 clean break (the standalone markdown
   system-index was dropped; the roster renders into `GAME.md` now) — upgrade via
   `/unikit-gd-spec` before reviewing.
3. **`{{skills_dir}}/{{self_name}}/references/lenses.md`** — the lens catalog and
   the adversarial prompts (absorbed from the former `review-lenses` rule).
4. **`.unikit/memory/gamedesign/RULES_INDEX.md`** — load the **core** domain rules
   for the target's behaviour/domain (by `Load When`) so each domain lens has its theory:
   `economy`, `balance`, `progression`, `ux-onboarding`, `accessibility`,
   `monetization-ethics`, `liveops`, `frameworks`. Obey the index's
   **Rule-Loading Discipline**: load by `Load When`, load a reference only from its
   parent rule's `> **References**:`, and **never glob the memory tree**
   (`.unikit/memory/gamedesign/**`) to discover rules.
5. **`.unikit/RULES.md`** (if present) — project overrides, highest priority. **Rule topics:** load the topic files listed under its `## Topics` whose `Load when` matches the design work at hand — the concept, system, flow or content type; when unsure, load.

**One-way boundary:** never read `.unikit/code/`, project source, or build
artifacts. **Single sanctioned exception:** the **feasibility lens** may read
**only** `.unikit/DESCRIPTION.md` and `.unikit/ARCHITECTURE.md` (two files, exact
paths) to flag implementability risks. It must NOT read `.unikit/code/`, `Assets/`,
or any source/build artifact — doing so violates the one-way boundary. A
feasibility finding cites the line it relied on in DESCRIPTION/ARCHITECTURE as its
evidence.

## Phase 1 — Resolve Scope & Mode (no flags)

**Scope** is a function of the prompt:

1. The argument names a system or a path → **single** review of that document.
2. The prompt says "all" / "all systems" / "все" → **cross** review of every
   `detailed` system.
3. Empty argument and several systems are detailed → **ask**:

   ```
   AskUserQuestion: What should I review?
   Options: <each detailed system> · All systems (cross-review) · None
   ```

**Mode** is the user's call — **critique** (iterate on a draft) or **review**
(verdict on a finished document). Default to review on a `detailed` document; offer
critique if the user is mid-authoring. Announce scope + mode in one line, then proceed.

## Phase 2 — Run the Lenses (adversarial fan-out)

Select the lenses from `references/lenses.md`: the **core** lenses always
(including **fantasy-delivery** — does section B's promised feeling actually arise
from C/D/E, and is an SDT need served?), plus the **domain** lenses matching the
system's behaviour/domain. When the system was built by import (its sections carry
provenance markers — see `gd-provenance` → Provenance), also run the **provenance**
lens over each `<!-- provenance: generated -->` section: inferred content is held to
a stricter bar (≥ Major against source/registry) than author-sourced text.

When the review **target is a `FLOW.md`** (or the scope is "all"), select the **flow
lenses** (pacing / guidance / funnel) from `references/lenses.md` alongside the system
lenses — a flow finding cites the `FLOW-<slug>` / `GOAL-<flow>-<n>` and the system
`AC` / pillar it serves, on the same `RF-<date>-n` rubric.

When the review **target is a `CONTENT-TYPE.md`** (or the scope is "all"), select the
**content lenses** (schema-coherence / catalog-scale / content-fantasy-delivery) from
`references/lenses.md` alongside the system lenses — a content finding cites the
`CT-<slug>` / `CU-<ct>-<n>` and the `belongs_to` system / pillar it serves, on the same
`RF-<date>-n` rubric.

Run them as **2–4 parallel inline `lens-agent`** dispatches, each given one lens, the
configured **artifact language**, and the adversarial framing *"find what is wrong —
do NOT validate"*. Each agent is **read-only** and returns findings only; it never
writes. Fall back to running the lenses sequentially in this session if the Agent
tool is unavailable.

```
lens-agent(prompt:
  "Review <doc path> through the <lens> lens. Your job is to FIND PROBLEMS, not
   validate. For each: severity (Critical/Major/Minor/Suggestion per the rubric),
   the document section, and the contradicted fact/pillar/rule as evidence.
   Diagnose — do not prescribe a fix. Return a findings list; write nothing.
   Write every finding in <artifact language> — this prompt is your only language
   source (you do not read Bootstrap or LANGUAGE_RULES), so translate domain concepts
   to their meaning (pacing→темп, exploit→лазейка, beacon→маяк); never transliterate
   jargon or code-switch mid-sentence. Keep only the id-tokens
   (RF-/SYS-/AC-/GOAL-/FORM-/CT-) and the lifecycle enum verbatim in English.")
```

Collect and de-duplicate the findings. Drop any finding with no section+evidence
citation to **Suggestion** (`gd-critique`).

**Flow lenses (active).** When the target is a `FLOW.md`, run the flow review lenses
(pacing, guidance, funnel — does the wiring-mode deliver its intended arc, is each
`GOAL` step guided, does the `## Funnel [gen]` measure the moments that matter?) from
`references/lenses.md`, with the same adversarial framing. A `FLOW.md` **is** a review
target; the lenses run over systems, flows, and `GAME.md`.

**Content lenses (active).** When the target is a `CONTENT-TYPE.md`, run the content
review lenses (schema-coherence, catalog-scale, content-fantasy-delivery — does
`CT.fields` cover what the consuming system needs and are its types / `ref<>` right, is
`bulk` vs `curated` the right call, does the catalog deliver the feeling section B
promises?) from `references/lenses.md`, with the same adversarial framing. A
`CONTENT-TYPE.md` **is** a review target; the lenses run over systems, flows, content
types, and `GAME.md`.

**Genre lens (active, declinable).** When `GAME.md` carries a `genre_profile:` id, run
the genre **profile-completeness** lens (`references/lenses.md`): read that installed
profile's `critical_sections` (`.unikit/system/gamedesign/genres/<id>.json`) and ask
whether each is present and filled across the docs under review — a missing genre-critical
section is a **Major** (declinable / advisory — never a blocker). The profile's
`review_emphasis` is an advisory **re-weight** of the lens priorities, not a new rubric.
This is the **only** profile read on the design side — `unikit-gd-verify` stays
genre-blind (it never reads `critical_sections`). No `genre_profile:` (universal
baseline) → skip the lens.

## Phase 3 — Cross-Scope Checks (cross review only)

When the scope is "all", add the cross-system lenses from `references/lenses.md`:
formula compatibility, cross-AC consistency, pillar drift, total scope vs tiers,
and **3–5 end-to-end "one moment through N systems"** scenarios. These are the
checks no single-document review can make. **Depends symmetry is not a review
lens** — `unikit-gd-verify` owns the Depends 3-way check (section F ↔ GD-IDS
`depends_on` ↔ the `## System Map` Depends cell).

## Phase 4 — Verdict, Full Report (to screen) & Triage

**Verdict.** Compute it from the findings:

- **Single:** `APPROVED` (no Critical/Major) · `NEEDS REVISION` (Major, no
  Critical) · `MAJOR REVISION` (≥1 Critical).
- **Cross:** `PASS` · `CONCERNS` · `FAIL` (≥1 Critical anywhere).

**Ids.** Give each finding a **stable id** `RF-<YYYY-MM-DD>-<n>` (numbered in
severity order, Critical first). The id is what a later `unikit-gd-apply` /
`unikit-gd-system` edit cites in its changelog — it must survive the handoff.

**Print the full report to the screen.** Render the *whole* findings table, the
verdict line, and the "I like" calibration to the screen — not a one-line summary.
(Printing only a summary and burying the report in a file was the complaint this
fixes.) The file below is the *durable* copy of the same content; the screen is the
*primary* surface.

**Triage into two buckets** — the handoff engine (`gd-critique` → Handoff Engine),
shared with `unikit-gd-verify`. Sort every finding by the silent **ENTAILED**
criterion:

- **Entailed** (all five points hold) → **apply-ready** automatically; record the
  one named fix.
- **Not entailed** → the **interview pool**.

Then run the **interview** (Braintrust — the user decides). Offer one **per-run**
choice up front — **[Run the interview]** or **[Send everything to research]** —
then, when interviewing, batch the pool through `AskUserQuestion` (**≤ 4 findings
per call**). Print the findings in this batch to the screen as plain markdown first —
the question mechanism carries the options and nothing else. Per finding: **[I decide: <fix>]** → apply-ready · **[To research]** →
research · **[Decline]** → dropped. The interview **only classifies** and records
the decision text; it **writes nothing** to the GDD (review stays non-authoring). A
finding whose fix the user already holds in their head lands in apply-ready directly
— no detour through `unikit-gd-explore`.

**Write `.unikit/gamedesign/reviews/<date>_review-<scope>.md`** (`mkdir -p` the
`reviews/` dir; `<scope>` is the SYS-slug or `all`) with the **two explicit
buckets** — this is the durable handoff interface (`unikit-gd-apply` reads
apply-ready, `unikit-gd-explore` reads research):

```markdown
# Review: <scope> — <YYYY-MM-DD>
> Verdict: <APPROVED|NEEDS REVISION|MAJOR REVISION | PASS|CONCERNS|FAIL>
> Scope signal: <single SYS-slug | cross: N systems>  ·  Mode: <review|critique>

## Findings
| RF | Severity | Document / Section | Lens | Diagnosis (problem + evidence) |
|----|----------|--------------------|------|--------------------------------|
| RF-<date>-1 | Critical | SYS-combat / D | systems-math | FORM-damage output contradicts PIL-2's design test |

## Apply-ready  ← hand to /unikit-gd-apply
<entailed + user-decided findings; one line each:
 `RF-<date>-n · <target doc/section> · Fix (entailed): <the single named edit>`.
 Empty bucket is valid — write "(none)".>

## Research  ← hand to /unikit-gd-explore
<the diagnoses that still need a decision; one line each:
 `RF-<date>-n · <the open question to work out>`.
 Empty bucket is valid — write "(none)".>

## I like
<what genuinely works — honest calibration, not flattery>
```

The two buckets **replace** the old `Required before implementation` / `Suggestions`
split and are **orthogonal to severity**: severity stays a column in the Findings
table (the blocking-vs-non-blocking discipline still holds there); the buckets sort
by *who acts* — the rule applies an entailed fix, the user decides the rest. A
**clean** review (zero findings) still writes the report (the audit trail) with both
buckets `(none)`, and **skips the handoff** (Phase 6) entirely — verdict only.

## Phase 5 — No status write (the verdict is ephemeral)

`unikit-gd-review` **writes no `doc_status`** — it is **not** a status writer (it was the
former writer of the dropped `reviewed` status; that status no longer exists). The verdict
is a **quality** judgment, ephemeral by design: it lives in the printed report + the
durable report file + git, **never** in a stored badge. A `detailed` document stays
`detailed` through a review — quality is re-checked by **re-running** the review, not read
off a status. Status records *readiness* and is owned by the authoring zones
(`unikit-gd-system` / `unikit-gd-flow` / `unikit-gd-content`).

A review never auto-applies fixes — the handoff (Phase 6) hands the apply-ready bucket to
`unikit-gd-apply` and the research bucket to `unikit-gd-explore`, in one move, instead of
routing revisions one finding at a time into the owning zones.

## Phase 6 — Handoff (only when there are findings)

The review's job ends at the **diagnosis**; this phase hands the two buckets to the
skills that act on them so the user makes **one** move — `review → [explore] →
apply` — instead of routing findings one at a time into owner skills.

**Safeguard — never decide alone.** When the **apply-ready** bucket is non-empty,
first **show the apply-ready edits** on screen and let the user confirm or adjust
them (the entailed fixes were sorted by the rule, but the user owns the call). Then:

```
AskUserQuestion: <K> apply-ready fix(es) are ready. Apply them now?
Options:
1. Apply now — runs /unikit-gd-apply on the apply-ready bucket, then verify
2. Not now — I'll read the file first
```

**Hand off — recommend-only (never a `Skill` call).** Neither `unikit-gd-review` nor
`unikit-gd-verify` carries `Skill` in `allowed-tools`; each **prints** the
`/unikit-gd-apply` recommendation for the user to run, and on Codex the auto-invoke
nudge runs it — the two handoff tails are identical by contract.

<!-- unikit:agents codex -->
### Auto-invoke the handoff — BLOCKING PRE-REQUISITE

When this phase prints the `/unikit-gd-apply` recommendation, automatically invoke it
(`$unikit-gd-apply <review-file>`) rather than asking the user to run it by hand — the
printed command is the recommend-only fallback for agents without auto-invocation.
This is a single handoff, not a per-finding dispatch: invoke `unikit-gd-apply` once
with the review file and let it route the apply-ready bucket to the owners.
<!-- unikit:end -->

- **Apply now → yes:** print the apply command for the review file —
  ```
  /unikit-gd-apply .unikit/gamedesign/reviews/<date>_review-<scope>.md
  ```
  `unikit-gd-apply` reads the **apply-ready** bucket as its deltas, dispatches them to
  the owning zones, and closes with one verify pass. Then **recommend**
  `/unikit-gd-explore <same file>` for the **research** bucket.
- **Apply now → no:** give **two recommendations** — `/unikit-gd-apply <file>`
  (apply-ready) and `/unikit-gd-explore <file>` (research) — for the user to run when
  ready.
- **apply-ready empty** (the common case for a single subjective review): **skip the
  apply offer** — recommend only `/unikit-gd-explore <file>` (research).
- A **single-zone** apply-ready set still goes through `/unikit-gd-apply`: its own
  GATE 2 bounces a lone zone straight to that owner — this skill never pre-routes.

## Final: Compact Report & Next Steps

Follow the **Handoff Tail contract** (`gd-critique` → Handoff Engine): the runnable
command is the **last block** on screen. Print the report and any note first, then
close with **one** icon-prefixed command on its own line — nothing after it.

Print the compact report:

```
Scope: <SYS-slug | all (N systems)>   Mode: <review|critique>
Verdict: <verdict>
Findings: <C> Critical · <M> Major · <m> Minor · <s> Suggestion
Buckets: <A> apply-ready · <R> research
Report: .unikit/gamedesign/reviews/<date>_review-<scope>.md
```

If the same finding recurs across reviews of different systems, note it **here**
(above the command) as a candidate **studio `library` rule** (`/unikit-memory
--module gamedesign`) so the lesson is captured as durable domain knowledge, not
re-discovered each review. No summary document beyond the report file.

**Then end with the handoff as the LAST block** — one command, following the
pipeline `review → [explore] → apply`. Pick the single tail from the bucket state:

- **research non-empty** → `🔎 /unikit-gd-explore <review-file>`
- **research empty, apply-ready non-empty** → `🛠️ /unikit-gd-apply <review-file>`
- **clean (no findings)** → `✅ /unikit-gd-verify <system>`

Nothing prints after the command line — no verdict recap, no description of what
the called skill does next.

## Ownership Boundaries

- **Owns:** `.unikit/gamedesign/reviews/` report files — including the **triage**
  (every finding sorted into the apply-ready / research bucket). review writes **no**
  `doc_status` and edits **no** GDD content — the report file is its only write. The
  report is a **living pipeline artifact**: `unikit-gd-explore` is sanctioned to mutate it
  **in place** — promoting a developed `## Research` finding into `## Apply-ready`
  (research-bucket mode) — so the pipeline `review → [explore] → apply` runs on the one
  file. That cross-skill write is explore's only write to this folder.
- **Read-only:** every design document (sections A–K, `GAME.md`, all of `GD-IDS.yaml`
  including `doc_status`); plus `DESCRIPTION.md`/`ARCHITECTURE.md` for the feasibility
  lens only. review makes **no** design-surface write — only the report file.
- **Not this skill:** consistency/impact checks → `unikit-gd-verify`; **applying** the
  apply-ready bucket → `unikit-gd-apply`; **developing** the research bucket →
  `unikit-gd-explore`; authoring → `unikit-gd-system` (systems) / `unikit-gd-spec`
  (`GAME.md`). The handoff to apply/explore is **recommend-only** — this skill prints
  the command, it never invokes it.
- **Never:** edit design **content** (any section A–K, `GAME.md`, or a `GD-IDS.yaml`
  fact value); write a `doc_status` (review is not a status writer); prescribe a fix the
  user did not ask for; inflate severity past the evidence; carry `Skill` in
  `allowed-tools` or apply a fix / invoke `unikit-gd-apply` itself (the handoff is a
  printed recommendation); read the code workspace beyond the feasibility exception.

## Quick Reference

```
/unikit-gd-review SYS-combat              → single review → verdict + report (apply-ready + research buckets) → handoff
/unikit-gd-review combat                  → resolve to the SYS-slug; same flow
/unikit-gd-review all systems             → cross-review with end-to-end checks → buckets → handoff
/unikit-gd-review systems/SYS-combat.md   → review a specific document path
# handoff (recommend-only print): /unikit-gd-apply <review-file> (apply-ready) · /unikit-gd-explore <review-file> (research)
```
