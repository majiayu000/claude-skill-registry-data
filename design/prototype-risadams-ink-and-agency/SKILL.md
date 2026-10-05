---
name: prototype
category: meta-orchestration
description: Build a throwaway prototype to answer a design question. Use when the user wants to sanity-check whether a state model or logic feels right, explore what a UI should look like, or resolve a prototype-type decision ticket before committing to a build.
compatibility: claude-code codex opencode
related-skills:
  - work-plan
  - implement
  - plan-to-spec
  - tdd
loop-eligible: false
---

# Prototype

A prototype is **throwaway code that answers a question**. The question decides the shape.

## Pick a branch

Identify which question is being answered — from the user's prompt, the surrounding code, or by asking if the user is around:

- **"Does this logic / state model feel right?"** → [LOGIC.md](LOGIC.md). Build a tiny interactive terminal app that pushes the state machine through cases that are hard to reason about on paper.
- **"What should this look like?"** → [UI.md](UI.md). Generate several radically different UI variations on a single route, switchable via a URL search param and a floating bottom bar.

The two branches produce very different artifacts — getting this wrong wastes the whole prototype. If the question is genuinely ambiguous and the user isn't reachable, default to whichever branch better matches the surrounding code (a backend module → logic; a page or component → UI) and state the assumption at the top of the prototype.

## Frame it before you build

Two lines, written down where the prototype lives, before any code:

1. **The question** — the one thing this prototype exists to settle, phrased so it can come back true or false. "Can a booking hold two overlapping tentative slots?" is a question. "Explore the booking model" is not.
2. **The budget** — how much code you'll spend before reporting back, in files or in a rough time box. A prototype that outgrows its budget has stopped answering and started building; stop and say so rather than pressing on.

If the question can be settled by reading the existing code or running one command, do that instead and say so. The cheapest prototype is the one you didn't write.

Two ways this skill gets reached for wrongly, both worth refusing out loud:

- **The design is already settled.** "Prototype" reads as the obvious next step once tickets exist, but if you know what to build, the next step is `implement`, per ticket. A prototype answers a question that is genuinely open and that talking won't close.
- **"Prototype the whole app."** That's a different artifact wearing this skill's name. A question has a stopping point; a whole application doesn't, so it becomes the production app by momentum — and code written under prototype rules (no tests, no error handling) ends up in front of users. If it's a demo, build it deliberately as a demo and say nothing in it is production. If it's a design question, cut it down to the question.

## Rules that apply to both

1. **Throwaway from day one, and clearly marked as such.** Locate the prototype code close to where it will actually be used (next to the module or page it's prototyping for) so context is obvious — but name it so a casual reader can see it's a prototype, not production. For throwaway UI routes, obey whatever routing convention the project already uses; don't invent a new top-level structure.
2. **One command to run.** Whatever the project's existing task runner supports — `pnpm <name>`, `python <path>`, `bun <path>`, etc. The user must be able to start it without thinking.
3. **No persistence by default.** State lives in memory. Persistence is the thing the prototype is _checking_, not something it should depend on. If the question explicitly involves a database, hit a scratch DB or a local file with a clear "PROTOTYPE — wipe me" name.
4. **Skip the polish.** No tests, no error handling beyond what makes the prototype _runnable_, no abstractions. The point is to learn something fast.
5. **Surface the state.** After every action (logic) or on every variant switch (UI), print or render the full relevant state so the user can see what changed.
6. **Never touch production data or live mutations.** A prototype reads; it does not write to anything real. Point every mutation at a stub or an in-memory store — the question is never "does the backend work".
7. **Capture it when done.** Fold any validated decision into the real code, then capture the prototype itself as a **primary source**: commit it to a throwaway branch, out of main, and leave a context pointer to that branch on the implementation issue. Capture the answer too — the verdict and the question it settled — in the issue or a commit. The main branch keeps only the validated decision.

## When nobody is watching

Both branches are built to be **driven by a human** — that's the point of a prototype. When the run is non-interactive (a background agent, a scheduled run, a sandbox with no browser and no TTY), don't fake an interactive session and don't guess the verdict. Instead:

- Build the artifact anyway, exactly as the branch describes — it's still what the user will drive later.
- Additionally produce a **transcript**: drive the prototype yourself through the specific cases the question hinges on (a scripted sequence of actions for logic; a static render or screenshot of each variant for UI) and save the output next to the prototype.
- Report the question, the transcript, and what you observed — but leave the verdict to the user. "Pushing A then B leaves the machine in `pending` with no exit" is an observation. "The state model is wrong" is a verdict, and it isn't yours to make.

## Quality Loop

Before handing the prototype over, check it against the question it exists to answer:

1. **Answers the question** — driving it exercises exactly the case in doubt, not adjacent ones.
2. **Runnable in one command** — from a clean checkout, no remembered paths or setup steps.
3. **Obviously throwaway** — a reader who stumbles on it in a month can tell it isn't production, and can find the question it was written for.
4. **Nothing real is at risk** — no live data, no real mutations, no persistence the question didn't ask for.
5. **Contained** — it stayed inside its budget, and it didn't grow abstractions for a future it isn't asked about.

If two or more fail, cut back and re-check. Cap at two passes — a prototype that needs a third round of polish has become the thing it was supposed to help you avoid building.

## Delegation Map

| User need | Delegate via | Notes |
| :--- | :--- | :--- |
| A `prototype`-type decision ticket needs resolving | Invoked *by* `work-plan` | `work-plan` charts decision tickets; this skill resolves the prototype-shaped ones |
| The prototype answered its question — now build it properly | Invoke `implement` | Fold the validated decision in; the prototype's constraints (no tests, no error handling) don't survive the promotion |
| The validated logic module needs real tests around it | Invoke `tdd` | Lift the reducer / state machine out first, then build behaviour tests at the agreed seam |
| The decision should become a written spec | Invoke `plan-to-spec` | Inline the decision-rich prototype snippet (state machine, schema, type shape) into the spec |
| The UI branch needs stronger visual direction than "three different layouts" | Give it a design pass directly | Apply design-system, hierarchy, and accessibility judgement to the winning variant |

**Loop eligibility:** false — a prototype answers one question once; there is nothing to re-run on a schedule.

<!-- self-evolve:start -->
## Self-Evolve Loop
Journal `~/.ink-and-agency/learnings/prototype.md` (or workspace-local `.ink-and-agency/` where the sandbox confines writes). Read it first; append what the run taught — [SELF-EVOLVE.md](../SELF-EVOLVE.md).
<!-- self-evolve:end -->
