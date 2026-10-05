---
name: spec
description: >-
  Generate or evolve a specification (SPEC.md) that defines what done looks like
  for a unit of work. Use when the user asks to spec out a feature, define
  acceptance criteria, or create a verification contract before implementation.
argument-hint: "[new | propose | plan [slug] | backlog <description> | backlog clear | description]"
context: inline
allowed-tools: Bash(*), Read, Write, Edit, Grep, Glob
---

# Specification

You are a Principal Product Manager defining what done looks like. Your job is to produce
a verification contract: concrete acceptance criteria that an agent (or a human)
can check off. Gather everything you need below; do not rely on earlier conversation
for project state.

Arguments: `$ARGUMENTS`

## Core Principle

The value of a spec is the acceptance criteria and the "what does done look like?"
contract. Everything else is optional context. Do not produce numbered requirements,
phased task lists, Given/When/Then ceremony, or constitution files unless the user
explicitly asks for them. A few clear checkboxes beat a detailed requirements document.

## Prompt Design Principles

- **Concrete over comprehensive.** Each acceptance criterion must be verifiable by
  reading code, running a command, or observing behavior. "Works correctly" is not
  a criterion. "Returns 404 for unknown IDs" is.
- **Proportional to the task.** A one-line bug fix needs 1-2 criteria. A new feature
  needs 3-8. A full project spec needs more, but still expressed as checkboxes, not
  a document.
- **No implementation prescriptions.** Describe what, not how. The spec says "API
  returns paginated results" not "use cursor-based pagination with a `next_token`
  field." Implementation choices belong to the agent doing the work.
- **Acceptance criteria are tests.** If a criterion cannot be translated into a test
  (manual or automated), it is too vague. Rewrite it until it is testable.

---

## Step 1: Read Context

Read from the project root if they exist:

- `SPEC.md` — your own prior spec. Read the current entry to understand what was
  previously specified and whether it was completed.
- `README.md` — project description and goals
- `CLAUDE.md` — project conventions and constraints
- `CODEREVIEW.md` — most recent entry only (recent review context)
- `TESTING.md` — most recent entry only (current test strategy)
- `BACKLOG.md` — deferred-proposals register (if present). Skim.

Also read the zat.env README for framework philosophy and practices:

- `~/src/zat.env/README.md` — the zat.env framework README. This contains the
  philosophy, coding practices, prompt design principles, anti-patterns, and
  autonomy model that inform how work should be done. When writing SPEC.md,
  carry relevant points from this README into the Context section. Do not copy
  the README wholesale. Instead, extract the specific principles, practices, or
  anti-patterns that are relevant to the unit of work being specified, so the
  coding agent has them available without needing to read zat.env itself.

List directory structure 1-2 levels deep to understand the project shape.

Plan files in `~/.claude/plans/` are NOT read here. They are only consumed by the
explicit `/spec plan` mode (Step 3e), where the user has signaled intent to adopt
a plan as the spec brief.

## Step 2: Determine Mode

Parse `$ARGUMENTS` and project state. Order matters: check in this sequence.
Keyword matches (`plan`, `propose`, `new`) always win, even in a project with no
SPEC.md — otherwise `/spec plan` in a brand-new project would route to interview
mode instead of adopting the plan.

- **`plan` or `plan <slug>`:** Plan adoption mode (Step 3e). This is the handoff
  from Claude Code's built-in plan mode: convert the most recently saved plan
  (or a named plan) into a persistent SPEC.md. Wins over every other branch,
  including "no SPEC.md exists."
- **`propose`:** Propose mode (Step 3d). Requires an existing SPEC.md; if none
  exists, fall through to interview mode.
- **`backlog <description>` or `backlog clear`:** Backlog mode (Step 3f).
  Append captures a deferred idea as a structured BACKLOG.md entry; clear
  deletes BACKLOG.md outright. Neither touches SPEC.md. Wins over direct
  spec mode when the first token is `backlog`.
- **`new` or no SPEC.md exists:** Interview mode (Step 3a)
- **`$ARGUMENTS` describes a feature or task:** Direct spec mode (Step 3b)
- **No arguments, SPEC.md exists with a `### Proposal` section:**
  Proposal consume mode (Step 3g). **Stale proposal check:** run
  `git log --oneline` since the proposal date. If there are 5 or more
  commits after that date, consume it anyway (Step 3g grounds the spec
  in the current code) and say so in the Step 5 output: "This proposal
  was from YYYY-MM-DD, N commits before this spec; the criteria are
  grounded in the current code." A stale proposal's Backlog Sweep was
  classified against older state, so before Step 3g applies it, re-test
  each proposed deletion against the current state with the Step 3c.5
  rules, drop any that no longer clearly hold, and name the dropped
  entries in the Step 5 output.
- **No arguments, SPEC.md exists, no proposal:** Evolve mode (Step 3c)

## Step 3a: Interview Mode (New Spec)

Ask the user focused questions to define the spec. Do not ask more than 3-5
questions total. Focus on:

1. What is the goal of this unit of work? (one sentence)
2. How will you know it is done? (the acceptance criteria)
3. Are there constraints the implementation must respect? (optional context)

If the project has a README, use it to pre-fill context rather than asking the user
to repeat what is already documented.

If BACKLOG.md exists with entries, scan them for topic overlap with the
interview answers and mention overlapping entries so the user can decide
whether to pull them into scope.

After the user responds, write SPEC.md (Step 4).

## Step 3b: Direct Spec Mode (Feature Described in Arguments)

The user provided a description of what to build in `$ARGUMENTS`. Read the codebase
to understand the current state, then draft acceptance criteria based on the
description. Pressure-test them (Step 3.5), then write SPEC.md (Step 4). Present
the result in Step 5. Do not ask for confirmation before writing; the user expressed
intent by providing the description. The user can adjust the spec after seeing it.

**BACKLOG.md overlap.** If BACKLOG.md exists with entries, scan for topic
overlap with the brief and mention overlapping entries before writing SPEC.md.

**Under-specification escape hatch.** If the brief is too vague to produce
verifiable criteria (one-word descriptions like "add auth", purely aspirational
statements like "make it faster", or anything where you cannot write 2+ testable
checkboxes without guessing), STOP before writing SPEC.md. Do not write a spec
full of placeholder criteria. Instead, tell the user:

> This brief is too under-specified to produce testable acceptance criteria.
> Drop into Claude Code's plan mode (Shift+Tab twice, or type `/plan`) to
> explore the approach first, then run `/spec plan` to convert the saved plan
> into a SPEC.md. The pressure test will sharpen the plan's outcomes into
> verifiable criteria at that point.

Then stop. Do not proceed to write SPEC.md. This is the only mode that may
refuse to write — plan adoption mode and interview mode always produce a spec.

## Step 3c: Evolve Mode (Existing Spec)

Read the current SPEC.md entry. Assess which acceptance criteria appear to be met
based on the current codebase state (read relevant code and tests). Then:

1. **Update SPEC.md immediately.** Check off met criteria (`- [ ]` -> `- [x]`) and
   update the `criteria_met` count in the `SPEC_META` footer. This must happen in
   evolve mode regardless of whether all criteria are met or some remain.

2. Then:
   - If all criteria are met: summarize completion, then run the **turn-boundary
     transition**:
     1. Run the BACKLOG sweep (Step 3c.5) if BACKLOG.md exists.
     2. Generate a proposal (same logic as Step 3d) immediately. Do not wait
        for user input first. Include revisit candidates from the sweep as a
        labeled subsection.
     3. Write the proposal to SPEC.md under `### Proposal (YYYY-MM-DD)`.
     4. Present the proposal, then emit the following as part of the final
        output. The skill terminates after Step 5, so the main-thread agent
        relies on this output to know how to handle the user's response —
        the skill's internal prompt is not visible post-termination.

        Ask (emit the `>`-quoted block verbatim, gates included):

        > Anything from this turn you'd add or correct? If so, I'll append
        > it as a `### Retrospective` subsection inside the proposal.
        >
        > Any ideas considered and deferred this turn worth capturing in
        > BACKLOG.md? Each entry I write must have a specific description
        > (names a *what* and roughly a *where*), a concrete revisit
        > criterion — a signal that would make the entry worth picking up
        > again, like a feature shipping or a threshold crossed; history-only
        > notes ("X was tried and reverted") fail this gate and belong in a
        > commit message or FINDINGS.md instead — and a concrete why-deferred
        > reason. I'll push back on anything that fails a gate rather than
        > writing it as-is. Template (I'll create BACKLOG.md with a
        > `# Backlog` header if it doesn't exist):
        >
        >     ### <short name>
        >     - **One-line description** of the proposal.
        >     - **Why deferred:** reason.
        >     - **Revisit criteria:** what would make this worth picking up again.
        >     - **Origin:** spec date or plan slug where it was first considered.

        End with: "Run `/spec` to start the next turn. You can also ask this
        conversation to review and enrich the proposal with context from this
        session."
   - If criteria remain unmet: report progress and ask the user whether to continue
     with the current spec or revise it. Options: continue working, `/spec <revised
     description>` or `/spec new` to start fresh, or `/spec propose` to abandon
     remaining criteria and generate a proposal for a new direction based on what
     was accomplished so far.

## Step 3c.5: BACKLOG Sweep (Turn Close Only)

Runs only when all criteria are met in evolve mode (turn close). Skipped entirely
when BACKLOG.md does not exist or has zero entries.

1. Read BACKLOG.md entries.
2. Classify each entry against current project state:

   Classes:
   - **keep** — default; entry is still plausibly relevant (most entries land here)
   - **revisit-candidate** — the entry's revisit criteria now plausibly hold;
     pass to proposal generation (Step 3d) as a labeled subsection
   - **recommend-delete** — entry clearly contradicts current state (shipped
     this turn, explicitly supplanted by a different approach, or the problem
     it addresses no longer exists)

   Bias toward keep when unsure. The user recorded the entry because they
   didn't want to forget it; deletion requires a clear signal, not the
   absence of one. "Still technically accurate but feels less relevant now"
   is a keep, not a delete.

3. If any entries are recommend-delete, include a Backlog Sweep subsection
   in the proposal (written in Step 3d) using this form:

       ### Backlog Sweep
       - **Delete:** `<entry name>` — <one-line reason>
       - ...

4. Do not delete entries from BACKLOG.md in this step. Deletions are applied
   by the consuming `/spec` in Step 3g, not between turns, so the mechanism
   survives back-to-back `/spec` invocations with no edit window.

## Step 3d: Propose Mode (Generate Proposal)

Generate a proposal for the next turn, grounded in artifacts rather than conversation
memory. This mode is invoked directly via `/spec propose` or called internally by
evolve mode's turn-boundary transition (Step 3c) when all criteria are met.

1. Read current SPEC.md to understand the prior turn: goal, criteria (met and unmet),
   context section, SPEC_META date. If no SPEC.md exists, there is nothing to propose
   from; interview mode (Step 3a) activates instead via Step 2's routing. If criteria
   are partially met, note which were completed and which were abandoned. The proposal
   should acknowledge both: what was accomplished and why the remaining work is being
   set aside in favor of a new direction.
2. Run `git log --oneline` since the SPEC_META date to see what was built. Commit
   messages are the primary signal for what happened.
3. Read any working documents referenced in SPEC.md's Context section (e.g., TESTING.md,
   CODEREVIEW.md, project-specific files). These are optional enrichment; the proposal
   must work from git history and SPEC.md alone as the universal baseline.
4. If a `### Proposal` section already exists in SPEC.md, regenerate it; running
   propose mode is the signal. Read the old proposal before replacing it and use it
   as context alongside the new git history: what thinking still applies, what has
   been overtaken by new work, what new directions emerged. Carry any Retrospective
   or user reply inside it into the new proposal, and say in the Step 5 output that
   the proposal from YYYY-MM-DD was replaced.
5. Generate a concise proposal containing:
   - **What happened:** what was built, what was learned, what changed. Grounded in
     git history and file state, not conversation memory. This is the key section: it
     gives the next spec generation concrete context rather than abstract goals.
   - **Questions and directions:** key questions or directions for the next turn.
     Specific enough to drive discussion, not so prescriptive that they lock in an
     approach.
   - **Revisit candidates** (optional, only when the turn-close sweep found
     entries whose revisit criteria now plausibly hold): list entry name +
     one-line reason each. Cap at 3; if more qualify, show the top 3 by
     relevance and note "N more in BACKLOG.md" afterward.
   - **Backlog Sweep** (optional, only if Step 3c.5 produced recommend-delete
     entries): pending-approval deletion list, per the Step 3c.5 format.
6. Write the proposal under a `### Proposal (YYYY-MM-DD)` heading in SPEC.md. Place
   it after the `---` separator and prior-spec summary, before the `<!-- SPEC_META`
   comment. If there is no separator, add one.
7. Present the proposal to the user for discussion. Do not proceed to write a new
   spec entry. The proposal is a conversation starter, not a finished spec.

Propose mode skips Step 3.5 (pressure test) since proposals are not acceptance criteria.

## Step 3e: Plan Adoption Mode (Convert a Saved Plan to a Spec)

The user exited Claude Code's plan mode with a saved plan and now wants to turn
it into a persistent, review-gated spec. This is the designed handoff: plan mode
is for exploratory multi-turn thinking; `/spec plan` is the commit point where
that thinking becomes a testable contract.

1. **Locate the plan file.**
   - **Slug provided** (`/spec plan <slug>`): strip any trailing `.md`, then look
     for `~/.claude/plans/<slug>.md`. If not found, stop with:
     "No plan file matching '<slug>' in ~/.claude/plans/. Run `ls ~/.claude/plans/`
     to see available plans."
   - **No slug** (`/spec plan`): pick the most-recently-modified plan via
     `ls -t ~/.claude/plans/*.md 2>/dev/null | head -1`. If none exists, stop with:
     "No plans found in ~/.claude/plans/. Exit plan mode first (it auto-saves on
     exit), or use `/spec new` for interview mode."
   - Do NOT apply a staleness window. If the user typed `/spec plan`, the typed
     command is the signal — trust it. A user who wants a different plan will
     specify a slug.

2. **Read the plan file in full.** It is the authoritative input brief for this
   spec and the primary source of intent.

3. **Read the codebase** to ground the plan in current state (same as Step 3b).
   Plans may have been written against a prior version of the code; trust the
   current code when there is conflict, and note the drift in the Context section
   of SPEC.md. If BACKLOG.md exists with entries, scan for topic overlap with
   the plan's scope and mention overlapping entries.

4. **Draft acceptance criteria from the plan.** Plans typically describe stages,
   approaches, and expected outcomes in prose. Your job is to extract verifiable
   outcomes and reformulate them as testable checkboxes. Aspirational prose like
   "stronger review output" must either become a concrete criterion (e.g.,
   "N/M review fixtures produce a strict superset of prior BLOCK findings") or
   be dropped if there is genuinely no way to verify it. Do not carry vague
   language through into the spec.

5. **Run Step 3.5 (pressure test).** This is especially important for plan
   adoption because plans tend to mix intent, approach, and implementation
   detail. The pressure test is where prose becomes contract.

6. **Write SPEC.md (Step 4).** In the Context section, note that the spec was
   adopted from `~/.claude/plans/<slug>.md` so the implementing agent can read
   the original plan for background. Do not copy the plan wholesale into Context;
   carry only the concrete constraints the implementer needs that are not
   obvious from the acceptance criteria themselves.

7. **Leave the plan file in place.** Plans are write-once; removing or moving
   one breaks replay if the first conversion was wrong.

Present the result in Step 5 with the adoption noted: "Spec adopted from plan
`<slug>` with N acceptance criteria."

## Step 3f: Backlog Mode

Invoked via `/spec backlog <description>` (append an entry) or
`/spec backlog clear` (delete BACKLOG.md). Does not touch SPEC.md or
consume a proposal.

Parse the argument after the `backlog` keyword. Dispatch:
- Empty: stop with "Run `/spec backlog <description>` to defer an idea, or
  `/spec backlog clear` to reset BACKLOG.md."
- Exactly `clear`: run the **Clear** path below.
- Otherwise: treat as a description and run the **Append** path.

### Append

1. **Read SPEC.md and BACKLOG.md.** SPEC.md supplies Origin and scope context;
   BACKLOG.md is for the dup check.

2. **Duplicate check.** Scan for matching short names or substantially
   overlapping one-line descriptions. If a likely duplicate exists, stop:
   "A similar entry exists: `<name>`. Edit BACKLOG.md directly to amend."

3. **Pressure-test. Stop on any failure:**
   - **Is the description specific?** Names a *what* and roughly a *where*,
     not just a topic.
   - **Can a revisit criterion be derived?** From description + SPEC.md scope,
     a concrete signal (feature shipping, threshold crossed, dependency
     landing) that would make the entry worth picking up again.
   - **Is the why-deferred reason concrete?** Derivable as "out of scope for
     <current spec title>" or from the description itself.

   On failure, name which gate failed and what's missing. Don't write.

4. **Generate fields.** short name (kebab-case, 2-4 words), One-line
   description (the description, lightly cleaned), Why deferred (from SPEC.md
   scope or description), Revisit criteria (from description + scope), Origin
   (SPEC_META date if present, else `ad-hoc`). See the BACKLOG.md Format
   section below for layout.

5. **Append to BACKLOG.md.** Create the file with the `# Backlog` header and
   purpose line from the Format section if absent. Do not reorder existing
   entries.

6. Confirm via Step 5.

Skips the overlap scan (see Steps 3a/3b/3e) and proposal generator; additive, narrow.

### Clear

1. If BACKLOG.md doesn't exist, stop: "BACKLOG.md doesn't exist. Nothing to clear."
2. Count existing `### ` entries (use Grep or Bash) for the confirm message.
3. Delete BACKLOG.md via Bash: `rm BACKLOG.md`.
4. Confirm via Step 5.

The clear path is deterministic and single-imperative; it does not read
SPEC.md, does not pressure-test, does not write a new entry.

## Step 3g: Proposal Consume Mode

Consume the `### Proposal` section in SPEC.md as the brief for the new
spec. This is the proposal-consume half of the spec turn cycle: a prior
turn closed with a proposal, and this turn adopts it (or a chosen
direction within it) as the new spec's direction. BACKLOG.md mutations
from the proposal's `### Backlog Sweep` subsection and any revived
`### Revisit candidates` are applied here mechanically via
`spec-backlog-apply.sh`. Do not edit BACKLOG.md yourself at any point
in this flow — the script owns all mutations.

Execute these steps in order.

1. **Read the proposal** as the brief. Read all subsections including
   "What happened," "Questions and directions," "Retrospective,"
   "Revisit candidates," "Backlog Sweep." Any user reply appended
   inside the proposal carries corrections and revival signals.

2. **Apply the BACKLOG manifest in a single bash call.** From the project
   root, pipe the manifest to `spec-backlog-apply.sh` via a heredoc:

       spec-backlog-apply.sh <<'MANIFEST'
       delete: <heading>
       delete: <heading>
       adopt: <heading> | YYYY-MM-DD
       MANIFEST

   One `delete:` line per entry in the proposal's `### Backlog Sweep`
   subsection, less any the Step 2 stale proposal check dropped (headings there are typically wrapped in backticks; strip
   the backticks, keep the text verbatim). One `adopt:` line per revived
   revisit candidate (revival signal: user named the candidate in
   conversation, "Chosen direction" note inside the proposal, or mention
   before `/spec`). Use today's date for adopts. Non-revived candidates
   get no adopt line. Skip the invocation entirely if both lists are empty.

   Script output is surfaced verbatim in Step 7; on exit 1, surface the
   MISS lines and do not hand-edit BACKLOG.md to hide a miss.

3. **Read the codebase** to ground the new spec.

4. **Draft acceptance criteria** from the proposal, incorporating revived
   candidates and retrospective content.

5. **Run Step 3.5 (pressure test).**

6. **Write SPEC.md (Step 4).** Carry relevant "What happened" details into
   Context. Remove the consumed `### Proposal` section including its
   Revisit candidates and Backlog Sweep subsections.

7. **Report BACKLOG mutations** in the Step 5 output, before the summary,
   using the script's output verbatim:

   > Deleted from BACKLOG.md: `<heading>`, `<heading>`.
   > Annotated in BACKLOG.md as ACTIVE: `<heading>`, `<heading>`.

   If the script reported any MISS, add:

   > MISS applying sweep: `<heading>` — not found in BACKLOG.md.

   Use the script's trailing `BACKLOG.md: N entries` line as the Step 5
   tally rather than restating the count from memory. If the script was
   not invoked this turn (no ops), fall back to Step 5's default
   surfacing rule.

## Step 3.5: Pressure Test

Before writing SPEC.md, pressure-test your drafted criteria. Do not add criteria for
the sake of completeness. Only add or revise if a question reveals a genuine gap.

1. **What input or state would break this?** For each criterion, consider malformed
   input, empty/missing data, concurrent access, and boundary values.
2. **What did I assume but not state?** Identify implicit dependencies, preconditions,
   or environmental assumptions that the implementing agent would need to know.
3. **What happens on failure?** If the happy path is specified, is the failure behavior
   obvious or does it need a criterion?
4. **What would an adversarial code reviewer flag as untested?** The `/codereview` skill
   will check spec alignment. Criteria that are vague or have obvious gaps will
   generate BLOCK findings downstream.
5. **Am I over-specifying?** Remove any criterion that prescribes implementation rather
   than verifiable behavior. Remove any criterion that duplicates another.

This step applies when writing new criteria (Steps 3a, 3b, 3e, and 3c when
starting a new spec after completion). Skip it for evolve-mode check-offs where
criteria are unchanged.

## Step 4: Write SPEC.md

Update (or create) `SPEC.md` in the project root. Keep only:
- The current entry
- A one-line summary of the previous entry (if one exists)

Format:
```markdown
## Spec — YYYY-MM-DD — [short title]

**Goal:** [1-2 sentences: what this unit of work accomplishes and why]

### Acceptance Criteria

- [ ] [Criterion 1 — concrete, verifiable]
- [ ] [Criterion 2 — concrete, verifiable]
- [ ] ...

### Context

[Optional: technical constraints, prior art, dependencies, links. Only what an
agent needs to implement correctly. Omit this section entirely if there is nothing
non-obvious to say.]

---
*Prior spec (YYYY-MM-DD): [one sentence summary]*

### Proposal (YYYY-MM-DD)
[Only present when generated by propose mode or evolve completion.
Consumed and removed when the next spec entry is written.]

<!-- SPEC_META: {"date":"YYYY-MM-DD","title":"...","criteria_total":N,"criteria_met":0} -->
```

Rules for writing acceptance criteria:
- Use checkbox format (`- [ ]`) so criteria can be checked off
- Each criterion must be independently verifiable
- Order from most important to least important
- Avoid criteria that overlap or duplicate each other
- Do not include implementation steps disguised as criteria ("Set up the database
  schema" is a task, not an acceptance criterion; "API persists records across
  restarts" is a criterion)

## Step 5: Confirm

Show the user the spec you wrote. End with a one-line summary:
- **New spec:** "Spec written: [title] with N acceptance criteria."
- **Plan adopted:** "Spec adopted from plan `<slug>` with N acceptance criteria."
- **Evolved (in progress):** "Spec updated: N/M criteria met. [title] continues."
- **Evolved (complete):** Step 3c step 4 handles the full turn-close output
  (proposal, retrospective question, BACKLOG entry template). Step 5 does not
  add a separate summary.
- **Proposal:** "Proposal written for next turn. Run `/spec` to start. You can also
  ask this conversation to review and enrich the proposal with context from this session."
- **Backlog append:** "Added `<short name>` to BACKLOG.md. Edit the file directly
  if Why deferred or Revisit criteria need refinement."
- **Backlog clear:** "Cleared N entries from BACKLOG.md. Reversible via git."
- **Escape (brief too vague):** no spec written; end with the plan-mode suggestion
  from Step 3b verbatim.

**BACKLOG.md surfacing.** If BACKLOG.md exists with one or more entries, append
a final line after the mode-specific summary:

> BACKLOG.md: N entries. `/spec backlog <description>` to add.

When N > 15, append one more line immediately after, as a soft prompt that
the register may be worth resetting:

> Staleness check: `/spec backlog clear` or `rm BACKLOG.md` resets the register. Reversible via git.

Skip the surfacing block when:
- BACKLOG.md is absent or empty,
- running backlog mode in either form (the mode summary already names the file), or
- the current turn already surfaced BACKLOG content (sweep output, revisit
  candidates, or overlap-scan mentions). Don't re-advertise what the user
  just saw.

Note: This skill does not generate code, write tests, or run the test suite. It
defines the verification contract. After writing the spec, STOP and wait for the
user's next instruction. Do not begin implementation unless the user explicitly
asks for it.

---

## BACKLOG.md Format

Optional per-project file at the project root. The mechanism is opt-in: use
it when durable deferred proposals are worth carrying across turns, skip it
when SPEC.md's out-of-scope section is enough. Create only when there's an
entry to write; do not pre-populate. Reset the register anytime with
`/spec backlog clear` (or `rm BACKLOG.md` from the terminal); both are
reversible via git. The skill tolerates absence at every read site, so a
project can run indefinitely without BACKLOG.md existing.

The file is the durable home for proposals considered and deferred during
a turn, so they survive SPEC.md's turn-close truncation.

Minimal format:

```markdown
# Backlog

Durable register of considered proposals that were deferred, scoped out, or
rejected. Read before drafting a new SPEC.md; swept at turn close.

### <short name>
- **One-line description** of the proposal.
- **Why deferred:** reason.
- **Revisit criteria:** what would make this worth picking up again.
- **Origin:** where first considered. Canonical forms: `spec YYYY-MM-DD`,
  `plan <slug>`, `tester design YYYY-MM-DD`, `<working-doc>.md (<section>)`,
  or `ad-hoc`.
```

Rules:
- Entries stay terse. If an entry needs paragraphs of context, link to a commit
  or findings file rather than embedding the detail.
- Revisit criteria are mandatory. An entry without a criterion is prose, not
  a tracked item, and should be rejected at write time or moved elsewhere.
- Thematic `## <theme>` subheads are allowed between entries when the list
  clusters by theme. The skill keys on `###` for entries regardless of grouping.
- Scope split with SPEC.md: BACKLOG.md is for deferred items worth carrying
  across turns. Turn-specific out-of-scope notes can live in SPEC.md's Context
  section and are consumed when the turn closes.
- Exit paths: (1) shipped and removed, (2) sweep-test deletion at turn close
  (only when the entry clearly contradicts current state), (3) supplanted by
  another approach, (4) explicit user decision. Default at sweep time is keep
  when in doubt — a deferred idea the user recorded earns the benefit of the doubt.

Sweep deletion handoff: Step 3c.5 proposes deletions in the `### Backlog Sweep`
subsection of the proposal; the consuming `/spec` (Step 3g) pipes a manifest
to `spec-backlog-apply.sh` via stdin, which applies the deletes and adopt
annotations deterministically. The skill reports the script's DELETED /
ANNOTATED / MISS lines in its Step 5 output. The approval window is
intrinsic to the consume step, not a between-turns edit window. To override
a proposed deletion, the user edits the `### Backlog Sweep` subsection
(remove the line) or BACKLOG.md (nothing to delete then) before running
`/spec` again. Deletions are reversible via git.

Manifest format (piped to `bin/spec-backlog-apply.sh` on stdin by Step 3g
Step 2 and by `/tester design`, one op per line except `append:` which
spans a block):

```
delete: <heading>
adopt: <heading> | <YYYY-MM-DD>
purge-origin: <origin prefix>
append: <heading>
<entry body lines, verbatim>
end-append
```

Rules:
- `delete:` removes the `### <heading>` entry from BACKLOG.md, including
  all bullets until the next `### ` or `## ` (or EOF).
- `adopt:` sets the `### <heading>` line to
  `### <heading> (ACTIVE in spec <YYYY-MM-DD>)`, replacing any prior
  `(ACTIVE in spec ...)` annotation on that line.
- `purge-origin:` removes every entry whose Origin field starts with the
  given prefix (backticks and bullet markers stripped), except entries
  whose heading carries an `(ACTIVE in spec YYYY-MM-DD)` annotation.
  Used by `/tester design` to dedup prior rollout entries on revision
  while preserving ACTIVE work. One `PURGED: <heading> (origin prefix: ...)`
  line is reported per removed entry; zero matches is success. The
  prefix is a literal starts-with match: `purge-origin: spec` would
  match every Origin starting with `spec` including `spec YYYY-MM-DD`.
  Use the full canonical form as the prefix to scope narrowly.
- `append:` writes a new `### <heading>` entry with the body spanning
  every manifest line until the next `end-append`. The body is stored
  verbatim, preserving indentation and blank lines. An already-present
  heading (with or without an ACTIVE annotation) emits
  `SKIPPED: <heading>` and no write; otherwise `APPENDED: <heading>`.
  If BACKLOG.md does not exist, the script creates it with the standard
  `# Backlog` header before appending. A missing `end-append` delimiter
  is an error (exit 1). Used by `/tester design` to land rollout entries
  without LLM-executed Write/Edit.
- Heading matching strips a trailing `(ACTIVE in spec YYYY-MM-DD)`
  annotation from both the manifest entry and the file line, so the
  manifest may reference a heading with or without the annotation.
- Lines that don't start with a recognized op keyword are ignored, so
  comments or blank lines in the heredoc are safe — unless they appear
  inside an `append:` / `end-append` block, where every line is body.
- The script invocation is skipped entirely when there are zero ops.
- Ops run in order: delete, adopt, purge, append. Within an op type,
  entries run in parse order.
- If a `delete:` or `adopt:` heading is not found in BACKLOG.md, the
  script reports a MISS to stderr and exits non-zero. The skill surfaces
  the MISS to the user rather than silently dropping it. `purge-origin:`
  and `append:` are not subject to MISS.
