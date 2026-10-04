---
name: tighten
description: >-
  PROACTIVE — tighten one piece of already-written text before it is sent or posted, cutting padding
  without losing a fact. Route on destination: a console turn to the user, a plan's sign-off half, an
  issue body or PR description, a plan's /sy:ship half, a dispatch brief, or one of this plugin's own
  files. Use it on any milestone turn, any drafted plan half, and any brief handed to another agent.
argument-hint: "[the text to tighten, or a path to it] — and its destination"
---

Rewrite one piece of text denser without losing anything its reader acts on. The patterns below were derived by measuring real corpora rather than from style intuition, and the finding that shapes this whole skill is that sentence-level filler was **absent**: the bloat is structural. Cut structures, never adjectives — do not go hunting for weasel words.

## First: which destination?

Ask, or resolve from what you were handed. Several patterns below are destination-specific, and routing on audience alone sends a console caller into plan-half rules.

- **A console turn** to the user → `## Human-facing text` § Everywhere + § A console turn, then `## Mode`.
- **A plan's sign-off half** → `## Human-facing text` § Everywhere + § A plan sign-off half.
- **An issue body, or a PR description** → `## Human-facing text` § Everywhere + § An issue body, or a PR description.
- **A plan's `/sy:ship` half** → `## Agent-facing text` § A plan's machine half.
- **A durable comment's human half** — a retrospective, a seams report, a decision log, a decomposition note, a spike verdict → `## Human-facing text` § Everywhere + § An issue body, or a PR description.
- **A dispatch brief for another agent, or one of this plugin's own files** (a skill, a reference, an agent brief, an MCP tool docstring or `Field(description=...)`) → `## Agent-facing text` § A procedure or a brief.

## Ground rules

Preserve every fact. Cut padding, never substance: the output says everything the input said, in less text — it does not say less. That is absolute for `## Agent-facing text`. For `## Human-facing text` it binds any material whose anchors no companion half carries. An anchor leaves a human half only when a companion half carries it. Handed one half with no companion in sight, this pass is looking at the only copy of everything in it. Match the destination's register; a sign-off half is prose a human reads once, a `/sy:ship` half is instructions a builder executes.

No budget, threshold or target number governs this pass. "Under N lines" is not the goal, a percentage is not a quota, and the cut list is the whole instrument — when nothing on it is present, change nothing.

Do not touch short text, at any destination. Text under 200 chars (`Let me check X.`, `Dispatching BUILD.`) was already correct across the measured console corpus, where all of the removable volume sat in turns of 1,500 chars or more; the same floor at a durable destination is judgment carried across from that measurement rather than a second measurement.

The economy rule this pass enforces lives in one place: `${CLAUDE_PLUGIN_ROOT}/skills/shared/references/context-economy.md`. Read it before rewriting anything; do not copy its tests into your output.

Which half a fact belongs in is a cut of its own, and one tool already makes it: `post-comment` takes `human` and `agent_detail` as separate arguments and writes the boundary itself (`sy_tools/server.py`), so the reader meets the judgment half first and the receipts stay reachable without being in the way — `${CLAUDE_PLUGIN_ROOT}/skills/ship/references/handoff-accounting.md` § 1 is the worked split. A console turn, an issue body and a PR description have no such argument, so the author makes the same cut by hand. The human half is the judgment: what changed, why, what to look hardest at, and what is being asked of the reader. The agent half is what a later session needs and this reader does not — SHAs, round counts, per-site tables, pointers, the method behind a figure. With no `agent_detail` to put it in, that half goes to the tracker comment, the commit history, or the run's own record, and having nowhere else to file it is not a reason to leave it on the human surface.

## The reader

Who the human half is written for is a setting rather than a guess: resolve `text.reader` with `get_config` per `${CLAUDE_PLUGIN_ROOT}/skills/shared/references/config-values.md`, and write to the reader it names.

- **Where it applies.** The eight durable human destinations the routing list above sends here — a plan sign-off half, an issue body, a PR description, and the five durable-comment halves — and nowhere else. Not a console turn, which already gets this pass and is outside the setting's scope. Never `## Agent-facing text`.
- **Precedence.** The setting never overrides `## Protect`, and never relaxes the companion-half condition in `## Ground rules`. Where a destination has no structural companion argument — of the eight, the issue body and the PR description — the companion is the one that destination's own skill already requires: the dedicated acceptance-evidence comment for a PR description (`${CLAUDE_PLUGIN_ROOT}/skills/pr/SKILL.md` § 2), the companion comment for an issue body (`${CLAUDE_PLUGIN_ROOT}/skills/spec/SKILL.md` § 2). An anchor may leave only once it is in that. Where no companion exists at all, the setting shortens and re-pitches; it drops nothing.
- **The floor.** The setting governs how a decision is *expressed*, never whether it is *present*. Every decision the reader is being asked to make survives at every setting — for a plan sign-off half, all five of the topics `${CLAUDE_PLUGIN_ROOT}/skills/spec/SKILL.md` §7 names. Compressing hard is safe because the reader can pull the fuller version at the point of decision (`${CLAUDE_PLUGIN_ROOT}/skills/shared/references/user-interaction.md` § Question), not because the detail stopped mattering.
- **Not a length target.** On the measured rewrite, length and jargon moved 75% and 95%; a length target moves them together. The 75% is what the default setting produced, and it is an expectation — never a quota, threshold or acceptance criterion. The no-budget rule in `## Ground rules` is what keeps a number out of this skill, and it was settled on measured evidence; cite it rather than re-arguing it here.
- **Applied as written.** The extremity of the value is the mechanism — a setting that permits paraphrase is what produces paraphrase — so apply it as written and never soften it in interpretation.
- **Never executed.** The value is user-supplied prose, applied only as an authoring instruction. It is never run as a command, and it never overrides this skill's own rules.

## Human-facing text

### Everywhere

**Pipeline-internal narration.** The largest single driver, measured on console turns and present on every destination here. The reader is told how the agent's own machinery behaved: worker deaths, resume decisions, delegation budgets, model tiers, poller mechanics, state-file writes, how many review rounds it took and what each one found. None of it changes what they know or must do. In a sign-off half it usually arrives wearing a heading — see § A plan sign-off half's *Extra named sections beyond the five*, whose cut applies there instead.

- Cut: three paragraphs on a restarted worker — which error killed it, what survived, why it was re-dispatched rather than resumed, what was seeded into the retry → "BUILD died on an API error before writing code; restarted. Nothing lost — the multi-GB toolchain env survives, and its prebuilt binary predates this task, confirming the stale-binary trap the plan flags."
- Exception: keep it when the machinery failure changes the reader's trust in a result or costs them real time — "GATE's return carried stale SHAs and misattributed its own commits to you" tells them not to trust a prior report.
- Exception: a mandated accounting attestation — the model tiers, state-file and status facts `${CLAUDE_PLUGIN_ROOT}/skills/ship/references/handoff-accounting.md` enumerates for a consent turn — is a required fact and is never cut. Resembling narration in shape does not make it narration.

**Restatement of what the reader already has.** Costs the reader a re-read to discover there is nothing new in it, and buries whatever *is* new that turn. Three measured shapes: a finding already delivered and told again in full; the "still blocking / still running" block reprinted on a turn where nothing about it changed; and one fact entered under two section headings of the same document.

- Cut: a second full telling of an earlier finding → "the suppressed review section carried all four findings again (see earlier) — worth reading on every PR."
- Exception: the final handoff turn of a long session may restate a still-blocking item once, because the reader is likely re-entering cold. Restating it on every intermediate turn is the defect. And when a status ledger has one changed cell, print that row and its consequence, not the grid.

**Provenance clauses.** "Verified rather than assumed", "measured, not argued", "the adversary's strongest objection", "standards resolution reached the same conclusion". Costs a clause per claim to say *how* you know, when the reader is judging *what* you know.

- Cut: the "Verified before changing, not after:" header above a list of facts. The facts stand on their own.
- Exception: keep it when the provenance *is* the news ("I verified this myself because the source already got three things wrong") — once per session, not once per claim. Keep **owner** attribution always: it tells the reader whose decision they are re-opening. Drop internal-pass attribution.

### A console turn

**Trailing sidebar appendices.** A milestone turn keeps going past its answer with an enumerated block of secondary findings: "Two things worth your attention", "Three things I did not do", "Two things I'm holding myself to". The label forces a second item into existence.

- Cut: the whole block, whenever its items restate the agent's own procedure rather than deliver a finding or a decision.
- Exception: one item the reader would act on differently if they knew it ("anything wrapping that client cannot pickle at all") stays — as a single unlabelled low-key aside, never as a "Two things…" block.

**Delegation-brief pre-announcement.** Before any result exists, the turn describes in detail what each dispatched agent was told to investigate and why.

- Cut: a paragraph per delegate → "Three investigations running: the I/O cost model, the consumer map, and where the seam belongs."
- Exception: a brief encoding a decision the reader could veto before the work is spent ("I've told it explicitly not to assume the old seam was right"). State that clause; drop the rest.

### A plan sign-off half

**Mitigation essay welded to every risk.** The risk is one clause, then two to four times that defending the response: what catches it, why that is enough, what a wider version would break. The reader is deciding whether to approve, not auditing the guard rail.

- Cut: down to the exposure and the guard's real strength → "59 class names are hand-transcribed from another repo and no in-repo test can catch a valid-but-wrong substitution. GATE re-reads the pinned config and a human checks the draft PR; both are eyeball checks, not gates."
- Exception: keep the mitigation when its adequacy *is* the judgment being signed off — one clause.

**Machine-half detail carried in prose.** Paths, build flags, exact values, versions, line anchors, SHAs, job names, and the connective prose hauling them; one file carried 108 backticked spans. None of it changes an approve/reject, and all of it is already in the other half — a premise this pass cannot check when it is handed one half. Apply this entry only with the companion half in hand; without it, the entry does not fire.

- Cut: "a new `<path>` derives a per-service prefix from `<env var>`'s first path segment (three worked examples) and exposes scoped accessors" → "a shared helper derives a per-service storage prefix from the deploy path, and a lint rule bans direct storage access outside it."
- Exception: name the one file or symbol when the decision hinges on it — one anchor per claim, and only where the claim would be unfalsifiable without it.

**Extra named sections beyond the five.** "Deliberate departure from the ticket", "Corrections to this work item", "Why the parent and not START", "Process note", a version preamble. Each re-narrates from a second angle what Approach already said.

- Cut: fold into Approach as two sentences — what was asked, what is shipping, why.
- Exception: a genuine departure from an explicit owner steer is exactly what sign-off is for. Keep it, but inside Approach, not as its own section.

**Runner-up rejected alternatives.** The heading says "Strongest rejected alternative", singular; most files stack a second and a third behind it.

- Cut: delete every alternative after the strongest.
- Exception: an alternative the reader is likely to propose themselves. One sentence, one reason.

**Non-decision risks.** Entries the text itself flags as pre-existing, latent, not-a-regression, or an unchanging property of the environment. The self-flagging phrase is the tell.

- Cut: delete.
- Exception: a pre-existing condition this change makes durable, harder to fix, or load-bearing is a real risk. The test is whether the plan changes the item's status, not whether the plan caused it.

Also delete on sight: the verbatim standing-policy boilerplate about out-of-scope being "a default contract, not a wall". It is standing policy, not this plan's content.

### An issue body, or a PR description

Three shapes, from a single measured body rather than a corpus: one Shipyard PR description of 4,142 words, classified section by section across its ten sections; one of the three was already carried as a clause in the routing list above. One body can place a shape and cannot rank shapes by volume, so only the largest is sized.

**Pipeline-internal narration** (§ Everywhere) reaches its largest form here — 955 of those 4,142 words — because this text is written after the work, so the machinery has a whole run to tell: how many review rounds there were, what each found and how it was fixed, which fix produced which commit. The diff and the commit list carry what changed; the run's retrospective carries how it went.

- Cut: a section per review round → nothing, or one clause where a round changed the shipped answer rather than the route to it.
- Exception: a finding the reader must still weigh — a defect found inside the fix for another defect, a ruling that overturned the author's own judgment. State the finding, not the round.

**Detail the diff or the ticket already carries.** The reader arrives with both open. A file-by-file walk, a table reproducing what the diff shows, or a restatement of the ticket's problem statement is a second copy of what they are already looking at.

- Cut: the walk → the one sentence naming what the reader would otherwise misread the diff as doing.
- Exception: a change whose point is invisible in the diff — a deletion that restores a lost guarantee, an edit that looks cosmetic and carries a semantic fix. The diff shows the edit and never the reason.

**A draft narrating its own revision history.** A figure corrected mid-run is left in beside its replacement and labelled stale; a claim withdrawn is left in and marked withdrawn. The reader is judging the current state and pays twice over to work out which number is live.

- Cut: state the current figure. The superseded one goes wherever the rest of the run's history goes.
- Exception: a figure the reader already acted on — one they were shown at a checkpoint or in a comment — earns one clause saying it is superseded and by how much.

## Agent-facing text

Two document classes bloat differently, and the destination bullet above already split them. Take the one you were routed to.

### A plan's machine half

Seven patterns, in descending measured volume. `Ordered changes` is 32-66% of a plan's ship half and the two largest patterns both live inside it, so a pass aimed only at the trailing fields cannot reach a third.

**1. The same fact in several sections.** The largest. Three axes: `docs requiring updates` re-listing paths an ordered change already names with the same line numbers; `tests and acceptance criteria` restating `verification obligations`; `design invariants` restating ordered changes in other words.

- Cut: the *invariant*, and only it. State the fact once, in the ordered change; the obligation shrinks to `lens: …; claim: …; evidence: <that change>`.
- Never cut: an entry in `docs requiring updates` or `tests and acceptance criteria`, however exactly an ordered change already names the same path. They are discharge-tracking fields — BUILD keys "updated or inspected" off the doc list (`${CLAUDE_PLUGIN_ROOT}/skills/ship/references/implementation.md`) and GATE composes its acceptance criteria from the tests field (`${CLAUDE_PLUGIN_ROOT}/skills/ship/references/immutable-gate.md`) — and this pass runs after sign-off review, so a deleted entry removes an obligation with nothing downstream to notice. Dedupe the *wording* instead: keep the path and its own check, drop the rationale the ordered change already carries.
- Exception: **an invariant earns its line when it states a property the ordered change does not state as a property** — that is what the gate reviewer checks against, and it is not always recoverable from imperative prose.

**2. Rationale a builder cannot act on.** Absorbs "narration of how the plan reached its own conclusions", which is never a shape of its own.

- Cut: "Snake-case, not kebab: kebab is exactly `CANONICAL_VERBS` (`scripts/validate.py:27`), and this adds no adapter method, so the adapter contract still holds and the exact-set check is untouched — `SHIP_WORKER_TRACKER_VERBS` needs no edit." → "Snake-case, not kebab (kebab = `CANONICAL_VERBS`, `scripts/validate.py:27`). No adapter method, no verb: `SHIP_WORKER_TRACKER_VERBS` unedited."
- Exception: rationale that **selects between two implementations the builder would otherwise pick wrong** — "Do **not** read `os.environ`: that is a false green, because a value set from Python arrives after libc init" chooses the predicate. The test is whether deleting the clause changes what gets typed. "Why we chose X" after an imperative fails it; "X not Y because Y silently passes" survives it.

**3. An obligation restating its own ordered change.**

- Cut: an obligation whose `evidence` respecifies a test the plan already ordered → "evidence: step 13's narrow->wide->narrow case", with the non-vacuity requirement moved into step 13, where the test is written.
- Rule, not an exception: **if the evidence is a test or step the plan already ordered, cite it by number.** Spell out only evidence the ordered changes do not create.

**4. The traced counterfactual.** After stating a rule, the plan walks the failure state by state instead of naming the consequence. Not the same as pattern 2: this is a simulation of the bad path, not a justification of the good one. The compressed form is a gotcha and is kept; the traced form costs 3-5x the assertion it protects.

- Cut: a five-clause walk of how a miscounted fake voids a retry case → "the fakes at `:71-77` and `:88-94` increment on every invocation — if the head read consumes a state, the retry case at `:96` passes without exercising `failed_once` (`:48-52`)."
- Exception: when the failure is **invisible** — a test that still passes, a green that is false — the trace is the only thing stopping the builder simplifying it away. Cap it at one clause, not one paragraph.

**5. Negatives argued at length.** Two shapes: a `none` field carrying 150-450 chars justifying the word "none", and an audit trail of paths checked and found clean.

- Cut: "`docs requiring updates`: **none**. Checked: [three doc paths, each with a sentence on why it does not apply]. Nothing existing becomes stale." → "`docs requiring updates`: **none**."
- Exception: a negative the builder is actively tempted to violate is an instruction, not an audit — "Leave `REQUIRED_TOOLS` and its length assertion **unchanged**" stays, as does a negative ending in a live disposition ("**accept it and do not regenerate in this PR**").

**6. Workflow choreography the downstream phase already owns.** The machine half instructing a later phase on process: who attests, what goes in the PR body, how to frame a checkpoint, halting protocol. The workflow already encodes all of it, and one plan told its flip window four times.

- Cut: "a 'compared, matches' claim does not discharge this obligation — the read-out is the evidence, because BUILD writes the PR body and cannot be the party that attests to its own transcription. BUILD's own step-1 cross-check is a first pass, not this." → "GATE reproduces the six lists in its verdict; a 'matches' claim does not discharge it."
- Exception: choreography that changes what the builder does — a halt condition genuinely belongs. Keep one telling of about 250 chars.

**7. Restating the standard instead of citing it.** `Standards authority` sections that name the authority and then reproduce its content: "Docstrings on public functions", "Tests mirror from `sy_tools/tests/`", "Ruff line length 120". All standing policy the run resolves anyway.

- Cut: keep only the **delta** — where the standard is unenforced, where two authorities conflict, and which wins: "Ruff's `ANN` rules are unselected in the root config, so this is hand-checked, not linter-caught"; "where the user's global 'always add docstrings' conflicts, `CONTRIBUTING:18-25` wins".
- Exception: an unusual constraint the authority does not carry — a seam scan, a set of string invariants a validator enforces — keeps its full statement.

### A procedure or a brief

**Rationale a builder cannot act on** and **The traced counterfactual** apply unchanged. **Workflow choreography the downstream phase already owns** applies with "a delegate or a tool the reader merely invokes" in place of "a later phase" — a poller's sleep/exit behaviour, a renderer's truncation rules, how soon a review bot comments. **The same fact in several sections** applies on this class's own axes: a reference restating a field or rule that another file's named section owns, and sibling paragraphs of one family each repeating the family's shared rationale. Patterns 3, 5 and 7 are keyed to plan fields and match nothing here — do not go looking for them. A docstring or a `Field(description=...)` is this class at smaller scale, and its keep test is the one `${CLAUDE_PLUGIN_ROOT}/skills/ship/references/immutable-gate.md` § Net-new agent-facing text states.

Four more, in descending measured volume, derived by classifying every changed prose unit of two full passes over Shipyard's own eleven always-resident `/sy:ship` files (`skills/**`, `agents/*.md`) — 56 units.

**A brief restating the procedure it is told to follow.** Most of the cut volume in both `agents/*.md` briefs, and absent everywhere else, because only an agent brief opens by naming a reference it must follow exactly and then re-states that reference's own routing, triggers and mechanism.

- Cut: "a fact found false returns `needs-decision` (or `bail-to-spec` when it invalidates the contract), never gets followed" → "a fact found false is never followed".
- Exception: what the delegate acts on **before** it ever opens the reference — a tool it must never call, a model override it must pass, its own return contract. That is the brief's content, not the reference's.

**The pointer that also summarises what it points at.** The citation earns its place; the table of contents welded to it does not, and that is the half that goes stale when the target moves.

- Cut: "The full dispatch rule, including requested-vs-observed reconciliation and why effort is not symmetrical with model, is `<path>`" → "The full dispatch rule is `<path>`".
- Exception: name the one thing in the target the reader must act on *here* rather than on arrival — a precondition to resolve before dispatch.

**The unit's own topic sentence, said twice.** The most frequent of the four, in three positions: a section opening with a summary of a section further down, a paragraph closing by re-asserting the sentence it opened with, and a set named and then referred back to in the same breath.

- Cut: the opener or the closer, never the body — "Not every fix round needs a fresh automated-reviewer request." above the paragraph stating exactly when one is needed.
- Exception: an opener stating the section's **scope** — who it binds, when it applies — is content.

**The rule stated in both directions.** A rule, then its own contrapositive: "X, not Y" where Y is a reading nobody would reach for, or a condition given positively and then again as its negative.

- Cut: whichever direction the reader meets second → "a field name drifting from the list below is a failed write", dropping the "not a comment nobody notices is wrong" foil.
- Exception: a wrong reading a reader genuinely does reach for, where the negative is the only thing blocking it. That is the invisible-failure case — one clause, not a sentence each way.

## Mode

A correctness check, not a cut. A turn is exactly one of Status, Question or Action needed, and never a blend; the two violations this pass catches are a question folded into status prose — if a turn's prose asks anything, it is not a Status turn — and an Action-needed block that is not the last thing in the turn. The three modes are defined once, in `${CLAUDE_PLUGIN_ROOT}/skills/shared/references/user-interaction.md`; read them there.

## Protect

Nothing mechanical stands between this rewrite and a lost anchor, so this is a hard rule rather than a caution: **no file path, symbol, config key, flag, SHA, job name, obligation, invariant or acceptance criterion leaves the text unless the entry being applied names it as removable.** An obligation loses a sentence, never its lens, its claim or its named evidence.

In `## Agent-facing text` that is absolute. In `## Human-facing text` an entry that names an anchor as removable fires only under the condition `## Ground rules` states. An anchor leaves a human half only when a companion half carries it. No `text.reader` setting relaxes either rule.

Two things a naive densifier takes that are not padding:

- **The vacuity defence** — "the size assertions are what keep the test from passing vacuously", "an always-empty fake exits 0 either way and would assert nothing", "else it passes against the base unchanged". These stop a builder writing a test that already passes on the base.
- **Current source quoted at an anchor.** A plan whose line numbers must be re-located by content uses the quoted line as the re-location key. It is not duplication.

## Report

Name the patterns cut, and nothing else. When the text was already tight, say so and change nothing.
