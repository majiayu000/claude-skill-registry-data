---
name: audit-interface
description: >-
  Load this skill to audit whether an existing UI, CLI, or API makes sense to a non-expert already
  inside it, or before shipping a screen or public API. Trigger on "this feels confusing", "users
  keep getting stuck", "is this intuitive". Not for the install path or first run.
disable-model-invocation: false
user-invocable: true
effort: high
compatibility: >-
  Probing a live web UI needs the Claude in Chrome browser tools in the main session, and probing a
  CLI needs it installed and runnable. Without them the audit falls back to screenshots, page text
  and static artifacts, and reports those findings as unwalked.
license: Apache-2.0
---

# Audit an interface

`simulate-newcomer-first-run` asks whether a stranger can get _in_. This skill asks whether, once in, they can
tell **where they are, what to do, and what just happened** — on any surface, without being told.

Two failure modes produce nearly every unusable interface, and both are invisible to the person who
built it:

- **The builder's vocabulary leaked into the product.** Words that name the implementation
  (`instance`, `payload`, `sync`, `provision`, `token`) reached the surface, and every one of them
  is a wall for someone who does not already know the system.
- **The next step is obvious only if you know the model.** The affordance exists, the builder can
  see it, and nobody else can — because it is an unlabeled icon, a hover state, or a step that
  assumes a concept the interface never introduced.

Neither is fixed by looking harder. Both are found by constraining who does the looking.

## Procedure

### 1. Pick the surface

"The interface" means different artifacts per surface, and each is probed differently. Take one row.

| Surface                  | The interface is                                                                       | Probe it by                                                                                                                                                 |
| ------------------------ | -------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Web UI**               | Screens, flows, states (empty, loading, error, success)                                | Driving it in the **main session** with the Chrome tools — subagents lose them. One state per screenshot; capture the unhappy paths, not just the happy one |
| **CLI**                  | Flags, `--help`, prompts, stdout/stderr, exit codes                                    | Running it. `--help` is the entire manual — if the answer is not there, it does not exist                                                                   |
| **Library / public API** | Signatures, names, defaults, required arguments, errors, the README's first code block | Writing the smallest real caller **from the docs alone**, without reading the source. Where you have to open the source, that is a finding                  |
| **Desktop / mobile app** | Screens                                                                                | Screenshots the user supplies. Do **not** infer what a screen looks like from its source — you will audit the code's intent, not the product                |

If the target spans several surfaces, audit them separately and keep the findings separate. A
usable web UI in front of a hostile CLI is two verdicts, not an average.

### 2. Ask the five questions

Every surface must answer all five **without the user asking, scrolling, or leaving**. Walk them in
order against each screen, command, or entry point. This is the fastest high-yield pass; run it
before anything else.

| #   | Question                                          | Fails when                                                                                                                                                      |
| --- | ------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| 1   | **Where am I?**                                   | No title, or a title naming the component rather than the task. Nothing distinguishes this screen from three others. `--help` does not say what the tool is for |
| 2   | **What is this for?** — in the user's words       | The purpose is stated in system vocabulary, or only inferable from the field names                                                                              |
| 3   | **What can I do here, and which is _the_ thing?** | Zero or two primary actions. Every button weighted the same. The main action is below the fold, behind a menu, or an unlabeled icon                             |
| 4   | **What just happened?**                           | An action completes with no visible change. A long operation shows no progress. The result appears somewhere the user is not looking                            |
| 5   | **How do I get out or undo?**                     | No back, no cancel, no undo. A modal with no visible dismiss. A destructive action that is final and did not say so                                             |

Question 4 is the one most often failed and least often noticed, because the builder knows the
action worked. **Every action gets visible feedback within about a second**, and anything past ~3
seconds gets progress or an estimate — not a bare spinner.

### 3. Sweep for anti-patterns — reject on sight

Each is one line, each is common, and each has a mechanical fix. Sweep for all of them; a surface
that is clean on all twelve is genuinely rare.

| Anti-pattern              | What it is                                                    | Fix                                                                                                        |
| ------------------------- | ------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------- |
| **Mystery meat**          | Icon-only control with no label or tooltip                    | Add a text label. Icon-only is acceptable only for close, back, and search, the icons everyone has learned |
| **Silent success**        | Action completes, nothing visibly changes                     | Confirm in place, and show the changed thing                                                               |
| **Dead end**              | An error or empty state with no action leading out of it      | Every terminal state carries the next action as a control, not as prose                                    |
| **Jargon leak**           | Implementation vocabulary on the surface                      | Rename to what the user would say. See `write-plain-language`                                              |
| **Blame copy**            | "Invalid input", "You must…"                                  | Name what was expected and give an example. See `audit-error-messages`                                     |
| **Hidden requirement**    | A rule revealed only on failure — password rules after submit | State the rule before and beside the field; validate as they leave it                                      |
| **Ambiguous destructive** | "Remove" / "Delete" / "Archive" with no stated consequence    | Say what disappears, whether it comes back, and how                                                        |
| **Modal trap**            | A dialog with no visible way to dismiss                       | Visible cancel, plus Escape                                                                                |
| **Two primaries**         | Two equally-weighted buttons where one is destructive         | Exactly one primary; the safe one. Everything else is secondary                                            |
| **Infinite prerequisite** | Step 1 needs something only step 4 explains                   | Reorder, or state the prerequisite up front with a link                                                    |
| **Hover-only**            | An affordance that does not exist on touch or keyboard        | Make it a real, focusable control                                                                          |
| **Untimed wait**          | A spinner past ~3s with no progress or estimate               | Show step counts ("3 of 7") or an estimate ("about 2 minutes")                                             |

Then **trace every control** on each screen: every button, link, toggle, and menu item, not a
sample. Use it, name the state it should change, and confirm the change shows where the user is
looking. Flag a control that changes nothing, one that changes only state the user cannot see, and
one that is disabled with no stated reason. Where the surface cannot be driven, follow the code
from handler to state to render instead, and mark those rows unwalked.

### 4. Apply the naming test

A large share of "confusing" is one bad noun. For every label, flag, function name, and menu item:

> Read it aloud inside a sentence describing what the user is doing.

"I'm going to **provision** my **workspace**" fails. "I'm going to **create** my **project**"
passes. If nobody would say the word to a friend describing the task, it is the wrong word — no
matter how correct it is internally.

Two corollaries worth checking explicitly:

- **The same concept has exactly one name** across UI, CLI, API, docs, and errors. Two names for one
  thing is a defect even when both names are good ones.
- **Button labels are verbs naming the outcome** — "Save changes", "Delete 3 files". Never "OK",
  "Submit", "Yes". A user reading only the button must know what will happen.

### 5. Run the persona battery

The three passes above find the failures you can see. The personas find the ones you cannot, because
they constrain what the reader is allowed to know. Dispatch
`ceh-usability-audit:newcomer-simulator` per persona with a concrete in-product goal (not "explore" —
**"change the account email"**), the surface's entry point, an explicit allowlist of what they may
read, and two things without which the battery misreports:

- **An audience baseline** — one line naming what this product's intended audience already knows
  ("a developer who has used a terminal, but has never seen this tool"). Without it, `Blank Slate`
  stalls on "terminal" and "browser tab" and returns a Blocker on every target that has ever
  existed. Everything inside the baseline is free; everything about _this_ product is not.
- **An action budget for the goal** — the number of steps the interface's own affordances imply.
  A walker who reaches the goal in triple that has found a real defect that no stall would catch.

Web UI reminder: **the walkers cannot drive a browser** — subagents lose the Chrome tools. For a
live web UI, either hold each persona yourself in the main session (accepting that you already know
too much) or hand the walker screenshots and page text instead of a URL. Say in the report which you
did.

Read `${CLAUDE_PLUGIN_ROOT}/references/personas-and-severity.md` before dispatching. It holds the
five personas, each a constraint catching a distinct failure class, and the severity scale step 6
ranks with. Run all five unless a surface makes one meaningless (`Small Screen` on a library API),
and record a skipped persona as a skip.

### 6. Rank by observed outcome

**Severity comes from what happened to a walker, never from how bad something looks to you.** This
is what keeps the report from becoming a list of preferences. Assign each stall one of the four
severities (Blocker, Detour, Friction, Polish) by the conditions in
`${CLAUDE_PLUGIN_ROOT}/references/personas-and-severity.md`.

A walker that ran out of turns produced no result at all — re-dispatch it over a narrower goal, and
never read turn exhaustion as a failure to complete. Overrunning the action budget is a **Detour**
(a **Blocker** past 2×), which keeps "technically possible but absurdly long" from passing as clean.

An anti-pattern you spotted that no walker stalled on is a **Hypothesis**, not a finding. It is
listed separately, unranked, and does not count against the gate. This will feel too strict on a
real violation — keep it anyway; the alternative is a report where the loud items are the ones the
auditor happened to care about.

A control you used in the step 3 trace that visibly changed nothing is observed, not a Hypothesis.
Rank it **Blocker** when a walked goal needs that control, otherwise **Friction**. A traced row you
only read in code stays a Hypothesis.

### 7. Report and loop

Write the report described under Output. Then fix the **top Blocker only** and re-run **only the
personas that stalled on it**. Repeat until the gate reads 5/5: the gate is the done condition. A
user who is present may still stop the loop early or accept a lower score; record that in the
report.

## Rules

### The gate

| #   | Criterion                                                                           |
| --- | ----------------------------------------------------------------------------------- |
| 1   | Every surface audited answers all five questions                                    |
| 2   | Zero open Blockers                                                                  |
| 3   | Zero unfixed anti-patterns that a walker actually stalled on                        |
| 4   | Every concept has exactly one name across UI, CLI, API, docs, and errors            |
| 5   | Every destructive action states its consequence before the action and names an undo |

Mark an unmeasurable criterion **N/A with a reason** and report the gate out of the remainder
(`4/4, 1 N/A`). Never score an unmeasured criterion as passing.

## Output

Write `.agents_workspace/ux-audits/<target>/run-<NNN>/UX_AUDIT.md` (zero-padded sequential run
index, so a re-run never overwrites prior evidence). Keep the walker transcripts and any screenshots
in that folder.

```markdown
# Interface Audit — <target> (<surface>)

**Goal(s) walked:** <the concrete in-product tasks, with the action budget for each>
**Audience baseline:** <verbatim — what the intended audience already knows>
**Allowlist:** <what walkers were permitted to read>
**Walkers:** <personas run> (<skipped, and why>)
**Method:** cold persona-constrained agents — proxy for a user test, not a user test
**Gate:** <N>/5

## Five questions

| Screen / command | Where am I | What for | Primary action | What happened | Way out |

## Findings

### <ID> — <Blocker|Detour|Friction|Polish> — <title>

- **Where:** <screen, command, or file:line>
- **Persona:** <who stalled>
- **Expected / got:** <what they thought would happen / what happened>
- **Fix:** <the concrete change>

## Hypotheses (no walker stalled — unranked)

## Delegated

<what went to make-ui-accessible / design-ui / audit-error-messages>

## Not covered
```

## Stop conditions

- **No concrete goal can be named.** "Audit the UI" with no task to complete produces preferences,
  not findings → ask for one real task per surface.
- **The surface cannot be run** — no screenshots, no running instance, no installable CLI → audit
  the static artifacts, and say plainly which findings are unwalked.
- **A fix requires a product decision** (removing a feature, changing what the thing is for) →
  report it; do not decide it.

## Hands off to

- Can a stranger even get in? `ceh-usability-audit:simulate-newcomer-first-run`.
- The finding is an error string: `ceh-usability-audit:audit-error-messages`.
- The finding is wording: `ceh-usability-audit:write-plain-language`.
- Layout, hierarchy, spacing, theme: `ceh-ui-design:design-ui`.
- Keyboard, contrast, ARIA, focus: `ceh-web-frontend:make-ui-accessible`.
- The fix is a doc, not the product: `ceh-documentation:write-guides-and-runbooks` when the reader
  needed a task or a runbook, `ceh-documentation:write-api-reference` when they needed a lookup.
