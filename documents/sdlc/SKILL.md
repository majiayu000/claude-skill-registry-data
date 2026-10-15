---
name: sdlc
description: >
  The single entry point for turning an idea into shipped, verified code. Triggers on:
  "/sdlc", "let's build", "new feature idea", "start a new project", "add this idea",
  "/sdlc list". Runs a right-sized process — a small ask stays one conversational pass; a
  substantial ask walks intent -> spec/plan -> build -> ship, with a git commit as the
  approval gate at each transition. Delegates all build-phase dispatch and verification to
  the separately-installed `unlazy` skill rather than reimplementing it.
---

# SDLC Orchestrator

This is the only skill you need to invoke by name. It runs the whole idea-to-shipped-code
process itself, tiered to how big the ask actually is.

## Step 0: Classify the ask

Before anything else, decide:

- **Small** — a one-file fix, a fleet-site article idea, a config tweak, anything that fits in
  one sitting with no real design decision. Skip straight to a plain conversational
  implementation. Write `docs/sdlc/<slug>/intent.md` only if it's worth remembering later —
  often a couple of sentences is enough and no `spec.md`/`PLAN.md` is needed at all.
- **Substantial** — a new project, a new subsystem, a multi-file feature, anything with a real
  design decision or where "what does success look like" isn't obvious. Run the full sequence
  below.

When in doubt, say which way you're leaning and why, in one sentence, before proceeding — the
user can override either direction. Nothing about this skill requires spawning agents or
writing three files for a small ask; that would be exactly the over-engineering this design
exists to avoid.

## Invocation forms

- `/sdlc "describe an idea"` — start a new slug (`docs/sdlc/<slug>/`, slug = short kebab-case
  name derived from the idea).
- `/sdlc <slug> "add or change this"` — amend an in-flight slug. See "Amendments" below.
- `/sdlc` or `/sdlc list` — show the status board (see "Status board" below).

## Step 1: Intent interview

Ask one question at a time, conversationally — never dump a numbered list in one message. Skip
any question the user's opening description already answered. Fields to cover, in whatever
order fits the conversation:

1. What's the problem, in the user's own words?
2. Who's affected / who is this for?
3. What does success look like — specific and measurable if possible?
4. What are you explicitly *not* building (non-goals)?
5. Any known constraints (time, tech, budget)?
6. What does the smallest useful version look like?
7. Priority: speed, quality, or cost, if that's ever in tension here?
8. Any existing systems/data this touches?

**Always end with:** "Anything else you'd like to add before I write this up?"

Then write `docs/sdlc/<slug>/intent.md`:

```markdown
---
slug: <slug>
created: <ISO date>
---

# Intent: <short title>

## Problem
[1-3 sentences, user's own words]

## Who's affected
[...]

## Definition of success
[Specific, measurable where possible — this is what later gates get checked against]

## Non-goals
- [...]

## Constraints
- [...]

## Smallest useful version
[...]

## Priority
[speed | quality | cost, if stated]

## Integration points
[existing systems/data touched, or "none"]

## Amendments
[empty until amended — see "Amendments" below]
```

Show it to the user before committing. Commit only after they confirm it's right:

```bash
git add docs/sdlc/<slug>/intent.md && git commit -m "intent: <slug>"
```

## Step 2: Define (spec + plan, one pass)

Do the requirements judgment, the design judgment, and the task breakdown back to back, in one
sitting — this used to be four separate skills/personas; it's one pass now.

1. **Requirements & design → `spec.md`.** Read `intent.md`. Decide: what are the concrete
   acceptance criteria (testable statements, not vague goals)? What's the technical approach
   and why — note real alternatives you rejected and why, only where a decision was genuinely
   non-obvious. Write `docs/sdlc/<slug>/spec.md`:

   ```markdown
   ---
   slug: <slug>
   built_from: intent.md@<git-hash-of-intent.md-at-this-commit>
   ---

   # Spec: <title>

   ## Acceptance criteria
   - [ ] [testable statement]
   - [ ] [testable statement]

   ## Approach
   [what you're building and why, in plain terms]

   ## Rejected alternatives
   [only where a real decision was made — omit if there wasn't one]

   ## Open questions
   [anything still unresolved, or "none"]
   ```

2. **Task breakdown & gates → `unlazy`'s own format.** Read the local `unlazy` skill's
   `references/method.md`, `references/orchestration.md`, and — if the work has independent
   parallel pieces — `references/parallel.md` before writing anything. Produce `unlazy`'s
   `PLAN.md` (Depth Tree / dispatch table) plus one gate file per leaf under
   `.unlazy/<slug>/gates/`, using `unlazy`'s own templates (`templates/PLAN.md`,
   `templates/gates-leaf.md`, `templates/gates-node.md`) verbatim — do not invent a different
   plan format. **One gate per acceptance criterion** from `spec.md`. For each, decide whether
   a `CHECK:`/`EXPECT:` can be made runnable — a script, a CLI, a Playwright/claude-in-chrome
   driven check — or whether no tool can decide the outcome, in which case it's an explicit
   manual gate (never silently skipped). Lint before proceeding:

   ```bash
   node ~/.claude/skills/unlazy/scripts/gate-lint.mjs .unlazy/<slug>/gates/<leaf>.md
   ```

Show both files to the user, then commit:

```bash
git add docs/sdlc/<slug>/spec.md && git commit -m "define: <slug>"
```

## Step 3: Build & verify — hand off to `unlazy`

Do not reimplement dispatch or verification here. Follow the local `unlazy` skill's own
instructions exactly:

1. Approve each `CHECK:` after reading it (`gate-check.mjs --approve`) — never run unreviewed
   commands.
2. For independent leaves, dispatch per `unlazy`'s Claude Code adapter
   (`references/dispatch.md`): native background `Agent` tasks for normal fan-out, the
   Workflow tool's `pipeline()` only for a large fan-out.
3. Before reporting anything done, run `gate-check.mjs --reverify` — re-execution, not just
   `--status`.
4. If a gate proves impossible, use `unlazy`'s `ABANDON:` mechanism and surface it — never
   silently drop it or claim completion anyway.

If a long multi-leaf build is starting, ask once whether to install `unlazy`'s optional Stop
hook for this session (`node ~/.claude/skills/unlazy/scripts/install-hooks.mjs`) — **never
install it without that explicit yes.**

## Step 4: Simplify & review

Once gates are green, invoke the already-installed global `simplify` skill on the diff, then
the already-installed global `code-review` skill. Neither is reimplemented here — this step is
just "call them, in this order, before asking for human review."

## Step 5: Human review

Present the diff/PR to the user. This is an existing hard gate — code merges only after
explicit human approval, same as before this redesign. Do not merge or push on your own
judgment.

## Step 6: Ship

Once merged: bump the version if the project uses one, write a one-paragraph changelog/release
note, commit. That's the whole step for the overwhelming majority of projects. Only run this
step when the user explicitly asks to ship — never automatically off a green build. If the
project has real deployment infrastructure (rare — e.g. a project with its own production
server), reference that project's own runbook if one exists; none is maintained inside this
skill.

## Amendments — changing an in-flight slug

`/sdlc <slug> "add or change this"`:

1. Append a timestamped entry under `intent.md`'s `## Amendments` section. Don't rewrite prior
   sections — append-only, so history stays visible.
2. Check drift: does `spec.md` exist? Its frontmatter `built_from:` names the `intent.md` git
   hash it was built against. Compare that to `intent.md`'s current hash
   (`git log -1 --format=%H -- docs/sdlc/<slug>/intent.md`).
3. If they differ, tell the user: is this amendment small enough to patch `spec.md`/the gates
   in place, or does it change acceptance criteria enough to warrant re-running Step 2? State
   your read and let them decide — never silently patch over a scope change, and never force a
   full redo for a trivial addition.
4. Commit whichever files changed.

## Status board — `/sdlc` or `/sdlc list`

List every directory under `docs/sdlc/`. For each slug, report:
- Stage: intent-only / spec'd / gates written / building / shipped (derived from which files
  exist and, for "shipped", whether `Step 6` ran — check git log for a ship commit on that
  slug).
- Drift: compare `built_from:` hashes as in "Amendments" step 2; flag any mismatch.

No separate tracking file — this is entirely derived from `docs/sdlc/*` and git history, so it
can't go stale relative to the actual files.

## Reference: human gates (never automated or skipped)

Ported from the project's prior methodology doc — still true:
- Architecture/design decisions — human approves the `spec.md`, not just Claude.
- Production deploys — human sign-off (Step 6 only runs when explicitly requested).
- Code review approval — human approves before merge (Step 5).
- Deleting data, dropping tables, changing auth/security config — human must review, always,
  regardless of what phase this skill thinks it's in.
