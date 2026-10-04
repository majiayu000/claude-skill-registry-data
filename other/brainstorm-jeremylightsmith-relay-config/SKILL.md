---
name: brainstorm
description: Use BEFORE any feature, component, UI, or behavior work, and before entering plan mode — for every project however small, when no approved design exists yet. Also invocable as /brainstorm.
---

# Brainstorm

Turn an idea into a fully-formed design through collaborative dialogue.

This skill takes an **optional card ref** as its first argument (`$ARGUMENTS`), e.g.
`/brainstorm RLY-42`. The **card is the home for this unit of work** — its `spec` field, read
and written with `./bin/relay`, is where the approved design lives, never a shared repo file.

<HARD-GATE>
Do NOT write code, scaffold, run a plan, or take any implementation action until a design is
presented AND the user approves it. This applies to EVERY project regardless of perceived
simplicity.
</HARD-GATE>

**"Too simple to need a design"?** No. Every project goes through this — a one-function
helper, a config tweak, a copy change. "Simple" work is exactly where unexamined assumptions
cause the most wasted effort. The design can be a few sentences, but you MUST present it and
get approval before moving on.

## Which card?
- **Ref given** (`/brainstorm RLY-42`) → read that card first (`./bin/relay card <ref>`) for
  context and brainstorm against it. If `./bin/relay card <ref>` shows a **CHANGES REQUESTED**
  block, treat resolving that feedback as this pass's primary goal. On approval, write the
  spec back to that card.
- **No ref given** → first confirm with the user that the goal is to **create a new card**. On
  confirmation, create it in **Backlog** and capture its ref:

      ./bin/relay create "<title>" --stage Backlog --json

  New cards are **intake**: they land in Backlog for a human to triage and prioritize later —
  never drop a fresh card straight into a planning column (Spec/Plan/Code). Brainstorm as
  usual, then write the approved spec to the new card and report its ref.

## Process
1. Explore current project context (files, docs, recent commits). If a card ref was given,
   read the card first (above) for context.
2. Ask clarifying questions ONE at a time (prefer multiple-choice). Understand purpose,
   constraints, success criteria. If the request is really several subsystems, decompose
   first and brainstorm the first piece.
   - **Re-interview when the request contradicts a shipped decision.** If it conflicts with
     how an already-merged feature works, stop and interview the user about the intended
     behavior — don't silently re-litigate a shipped decision from a one-line request (this
     caught the workspace-cascade direction).
   - **Group MMFs that touch the same files onto one branch / one plan.** When two roadmap
     MMFs edit the same modules (e.g. M06 + M07 both touched `profile.ex`, `index.ex`, and the
     client card), brainstorm and plan them together to avoid merge conflicts and contradictory
     edits, and note the shared files in the spec header.
   - **UI features — settle artboard fidelity explicitly, and record the decision in the
     spec.** Hi-fi mockups live in `docs/designs/*.dc.html`, but they **drift from the shipped
     app over time**, so matching one is a deliberate per-feature choice, never a default. If
     the work has a UI, ask the user whether it should match an artboard. If **yes**: open the
     named artboard, confirm you understand exactly what's required — which screen/component,
     which elements and states — and write that into the spec explicitly: **name the artboard
     file and list the specific elements/states that must match it** (this is the signal
     `/write-plan` keys off; without it the planner won't chase a mockup). If **no** (it
     shouldn't track a mockup, the mockup is known-stale, or none fits): say so in the spec so
     nothing downstream tries to match one. Non-UI work skips this.
3. Propose 2–3 approaches with trade-offs and a recommendation.
4. Present the design in sections scaled to complexity (architecture, components, data
   flow, error handling, testing); get approval section by section. YAGNI ruthlessly.

## Design principles
- **Design for isolation.** Break the system into units that each have one clear purpose,
  communicate through well-defined interfaces, and can be understood and tested
  independently. For each unit you should be able to say what it does, how it's used, and
  what it depends on. If you can't understand a unit without reading its internals, or can't
  change its internals without breaking consumers, the boundaries need work. (A file growing
  large is usually a signal it does too much — and focused units are easier to implement and
  review, which your per-task gates reward.)
- **Work with the existing codebase.** Explore the current structure first and follow
  established patterns (Phoenix/LiveView/Ecto idioms per `AGENTS.md`). Where existing code
  genuinely blocks the work — a tangled module, unclear boundaries — fold a *targeted*
  improvement into the design, the way a good developer improves code they're touching. Do
  NOT propose unrelated refactoring; stay focused on the current goal.

## After approval
- Write the approved spec to the **card**, not a shared repo file. Save it to a temp file and:

      ./bin/relay spec <ref> @<tmpfile>

  Do **NOT** write or commit a spec file under a shared `docs/…` specs directory — that home is
  retired; work travels with the card.
- Write the card's **acceptance criteria** in this same step — they are a required output of
  the Spec stage, not an optional extra. Save them to a temp file and:

      ./bin/relay criteria <ref> @<tmpfile>

  They are the human's Approve checklist first and the robot's script second: at the Code
  stage the `acceptance-tester` reads this field off the card and actually runs them.

  **Required format** — a numbered criterion, each with numbered steps, each ending in one
  observable expectation:

  ```markdown
  ### 1. <Short criterion title>
  1. <action step>
  2. <action step>
  3. Expect: <one observable outcome>

  ### 2. <Short criterion title>
  1. …
  ```

  Rules:
  - Every criterion ends in **one observable expectation** — something a tester can see, not a
    feeling. "The page loads" is not a criterion; "the drawer shows Acceptance Criteria above
    Spec" is.
  - Steps are concrete and executable from a cold start: name the URL, the button, the command.
  - Criteria describe **user-observable behavior**, not implementation.
  - Aim for the handful that would actually change an Approve decision. YAGNI — this is not a
    test plan, and it does not restate the unit tests.
  - **Always author them**, including for a card with **no runtime surface** (META work on
    skills, docs, workflow files). For those, the criteria are static-verifiable assertions
    ("file X contains Y", "`mix test <path>` passes") — which is what makes them checkable at all.
  - A criterion the robot cannot possibly check (needs a real device, a subjective aesthetic
    call) is still authored: the tester returns `human-verify` for it, which does not block.
- Self-review: placeholder scan, internal consistency, scope, ambiguity — fix inline. **For any
  UI feature, confirm the spec records an explicit artboard decision** — either "match
  `docs/designs/<file>.dc.html`" naming the elements/states, or a deliberate "no mockup"
  (with why: none fits / known-stale / not visual enough). A UI spec with *no* artboard
  decision is a gap: resolve it (ask the user if it's still open) before writing the spec.
  **Confirm the spec has acceptance criteria** in the required format: a spec written without
  them is a gap, not a style choice. Resolve it before writing.
- Point the user to `/write-plan <ref>`. Do NOT start implementation or launch execution.

## Headless / runner use (no human to dialogue with)
**The work is pre-authorized.** A flow node invokes this skill on the board's behalf — proceed
without asking for confirmation to begin. Your blast radius is this one card: **do not touch git,
branches, or any other card.** And it is **terminal** — stop after writing the spec back to the
card. Do not start implementation, do not run `/write-plan`, do not move the card. The board's
`Spec:Review` lane is the approval gate; landing there is the whole job.

When the board runner invokes this skill there is no human to dialogue with in real time, but
that does **not** mean skip the questions. Do the **same** clarifying-question discovery you'd
do interactively (Process step 2) — surface every question you'd ask a human. Headless mode
changes only *how* you deliver them, not *whether* you ask.

- **If you have questions, ask them.** Collect *all* of them into a **single**
  `needs-input` call carrying a **structured** question array, then STOP. Do not
  guess-and-write a spec when real questions remain. Write the array to a scratch JSON file
  under `$RELAY_NODE_SCRATCH`'s directory (never an invented `/tmp` path — see
  [`relay.md`](../../../relay.md#the-relay_node_scratch-contract))
  and pass it with `--questions`:

      questions_file="$(dirname "$RELAY_NODE_SCRATCH")/questions.json"
      cat > "$questions_file" <<'JSON'
      [
        {
          "prompt": "**<Subject of the decision>.** <The question, stated plainly.>",
          "options": [
            "<A full, self-contained choice.> — RECOMMENDED",
            "<Another full, self-contained choice.>"
          ],
          "allow_text": true
        },
        {
          "prompt": "**<Subject>.** <A genuinely open-ended ask.>",
          "options": [],
          "allow_text": true
        }
      ]
      JSON
      ./bin/relay needs-input <ref> --questions @"$questions_file"

  The array **is** the batch — the drawer paginates it into a one-question-at-a-time
  stepper, so **never** hand-number questions into one big string. Prose gives the human
  a wall of text where they should get clickable options.

  - **One decision per array item.** `prompt` is markdown (the drawer renders it) — bold
    the decision's subject, then state the question plainly.
  - **`options` are the concrete choices**, each a full self-contained sentence. The
    human sees one option per button with **no surrounding prose**, so an option must
    make sense alone. Mark the one you'd pick with a trailing `— RECOMMENDED`.
  - **`allow_text` defaults to `true`** — leave it true unless the options are genuinely
    exhaustive. Use `"options": []` for a genuinely open-ended ask; the stepper then
    renders just its multi-line answer box.

  Calling `needs-input` blocks the card on a human and posts your questions to its
  timeline; the runner stops working it until the human answers.

- **On re-entry** (the card comes back after the human answers): the answers are in the card
  timeline — `./bin/relay card <ref>` shows your question comment and the human's answer
  comment (also honor any CHANGES REQUESTED block). Read them, incorporate, then write **both**
  the spec and the acceptance criteria to the card (`./bin/relay spec <ref> @<tmpfile>` and
  `./bin/relay criteria <ref> @<tmpfile>`, exactly as **After approval** describes) and stop —
  or send one more batched `needs-input` only if something is genuinely still ambiguous.
  Writing only the spec fails the node: the Spec flow declares
  `"writes": ["spec", "acceptance_criteria"]`, and a declared field left blank rewrites this
  node's `succeeded` to `failed`.

- **Only write the spec directly, without asking, when there are genuinely no meaningful
  questions.** The board's `Spec:Review` lane is the approval gate for the spec itself.
