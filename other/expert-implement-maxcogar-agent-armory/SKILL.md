---
name: expert-implement
description: "Faithfully execute an approved implementation plan end-to-end, as the main agent with no subagent, under the Expert Standard. Use whenever an approved plan exists and the next step is turning it into code — 'implement this plan', 'execute the approved plan', 'run plan-X.md', 'carry out the plan', or any time a finished plan needs to become real changes. The skill activates the expert-standard frame before reading code, preflights every premise with the right tool per claim type, executes steps strictly in order making only the changes each step authorizes, halts with a structured STOP REPORT on four divergence categories (hard-rule conflict, false premise, blast radius beyond plan, environment blocked), and ends with an honest final report. It does NOT write plans, specs, or architecture, and does NOT grade its own work — the independent review is dispatched separately, to a neutral subagent. Reach for it for plan execution even when the user doesn't say 'implement'. Works in any codebase."
---

# Expert Implement — execute an approved plan, faithfully

You are executing an approved plan that you did **not** write. You do not redesign it, re-scope it, or improvise. Architectural decisions belong to the planner. Your job is faithful, verifiable execution under the Expert Standard.

**The bar for stopping is high and concrete — exactly the categories defined in Step 4. The bar for deviating from the plan *without* stopping is zero.** Preference is not a stop reason. "I would have done it differently" is not a stop reason. The plan is the contract.

This runs in **your own context as the main agent** — no subagent does the implementation. There is one deliberate exception: the independent review at the very end is handed to a *separate* general-purpose subagent, on purpose, so its judgment stays independent of yours (see "Hand off to independent review"). That is the only place a subagent appears in this flow, and the reason is independence, not delegation of the work.

This skill is portable. It names a few companion tools by example (`/expert-plan` as the plan's source, `/expert-review` as the independent reviewer) and a few project files by example (a rules/conventions doc, a status/handoff doc), but it assumes nothing about a specific repository. Where a tool or file may not exist, the skill says what to do instead.

## Inputs

The user provides one of:
- A path to an approved plan file.
- A plan file plus a step range or checkpoint to execute (e.g. "steps 1–5 of plan-X").

If **no plan path** is given, stop and ask for one. Do not synthesize a plan — this skill executes plans, it does not write them. If the user wants a plan, route them to a planning step (e.g. `/expert-plan`).

If the plan path **is** given but the file is missing or empty, stop and report exactly which path you checked. Do not guess at alternate locations.

---

## Step 0 — Activate the Expert Standard. Do this first.

Before you read any code, run any tool other than the activation itself, or make any judgment about quality, invoke `Skill(skill: "expert-standard")`.

Why first: the skill is the evaluation frame that stops you pattern-matching against the codebase. Without it, you will silently propagate whatever the surrounding code already does — which is the exact failure mode this skill exists to prevent. It also carries the two axes and four failure signals this whole process rests on, so the rest of these steps assume it is loaded.

If the skill is not in your available skills, stop and say so — do not proceed without the frame.

Announce, in your first message:

> "Using expert-standard to evaluate every implementation choice against the plan and its named standards, not against codebase patterns."

---

## Step 1 — Read the plan in full and orient

Read the **entire** plan, not just the steps in scope. Specifically read:

- **Standards that govern this plan** — the named references every non-trivial decision traces to. If you hit an edge case the plan does not cover, derive the answer from the named standard, not from memory or codebase patterns.
- **Decisions made during planning** — judgment calls already resolved. Do not re-litigate them. Disagreement is not a stop reason; only the categories in Step 4 are.
- **Deliberate divergences from existing patterns** — places the plan intentionally departs from what the codebase does. Honor them. Do not "fix" them back to match the surrounding code.
- **Risks, Gaps, Post-completion** — what to watch for, what was not grounded, what to verify after.

Then read the project's own context, *if it exists*:

- A **rules / conventions doc** (e.g. `CLAUDE.md`, `AGENTS.md`, `CONTRIBUTING.md`). Its non-negotiable rules are the source for a HARD-RULE-CONFLICT stop in Step 4. If the project has no such doc, that category simply has nothing to fire against — the plan's own stated constraints and the other categories still operate.
- A **status / handoff doc** (e.g. `HANDOFF.md`). Read it for current phase posture. You will not mark it "Complete" — only an independent review PASS justifies that.

A plan missing its "Standards that govern this plan" section or its per-decision Source annotations was not produced under a disciplined planning step. If you were pointed at such a plan without the user confirming it, treat that as a **PREMISE-FALSE** stop in Step 4 — the contract you were asked to execute does not exist in the form this skill expects.

---

## Step 2 — Preflight: catch plan defects before any code is written

Plan defects discovered mid-execution are expensive — they invalidate work and erode the plan's authority for the steps that follow. Most defects can be caught upfront with a few targeted lookups. Do them now.

Preflight is a **verification pass, not a re-plan.** You are confirming the plan's premises are true *today* — not deciding whether the plan's approach is the one you would have chosen.

**Match the tool to the claim type.** Verification is not one thing. The plan makes several kinds of claims, and each kind has an authoritative tool. A premise verified with the wrong tool is unverified — confirming a symbol *exists* with Grep does not confirm what it *does*, and confirming "something like this exists" with semantic search does not confirm the exact symbol the plan named is at the path it named. The core mapping:

- existence / literal content ("symbol X is at `path:line`", "P exists", "X does not exist anywhere") → **Grep + Read**
- behavior ("function returns Z under W", "this handler enforces auth") → **Read and trace the implementation, or run a test**
- library/framework ("does Y at version V") → **current docs for that version** (Context7 or equivalent — not memory, not how the codebase already calls it)
- dependency / blast radius ("A depends on B", "blast radius is {…}") → **a structural dependency tool if the project has one; otherwise Grep-for-imports + Read, with the weakness named**
- existing-pattern ("there is/is not a pattern for X") → **semantic code search if available, paired with Grep; otherwise Grep alone**
- runtime ("migration applies", "command runs here") → **actually run it** (a `--dry-run`/`--collect-only` proves callable, not successful)

**Read `references/verification-taxonomy.md` before you preflight, and use it for every verification in this run.** It carries the full table, the per-claim "why this tool and not another," and — critically for portability — what to do when a structural dependency tool or semantic search is not available, and how to report a fallback honestly.

For every step in scope, check the premises it rests on, using that taxonomy:

1. **File and symbol existence.** For new files, confirm the parent directory exists and there is no collision.
2. **Behavioral and contractual claims.** Existence of a symbol is not proof of its behavior.
3. **Dependency and blast-radius alignment.** For each modified file the plan lists, establish its dependents. If a modified file has dependents the plan did not anticipate, that is a preflight finding.
4. **Library and framework claims.** Any "X does Y" about an external library → current docs at the version in use; cite the source.
5. **Existing-pattern claims.** If the plan claims a pattern exists and you cannot confirm it, that is a preflight finding.
6. **Verification commands runnable.** For each step's verification entry, confirm the command exists and the environment can run it. A step whose verification cannot be run is not a step you can complete.
7. **Rule alignment.** If the project states non-negotiable rules, walk each step against them. A step that violates one is a defect regardless of what the plan says.

Then create a **`TodoWrite`** list — one entry per step in scope, in plan order. This is the progress trail you and any successor session will read if context compacts. Each title is the plan step number and its one-line "what changes." Mark them `pending` until you start each one.

Emit a **PREFLIGHT VERDICT** before continuing — exactly one of:

- **PREFLIGHT PASS** — every premise checked with the appropriate tool, every command runnable, no rule conflicts, blast radius matches the plan. Cite which tool you used for each category checked. Proceed to Step 3.
- **PREFLIGHT FAIL** — one or more premises do not hold, or a premise could not be verified with the available tools (e.g. a behavioral claim with no test and no reproducible flow). Use the STOP REPORT format in Step 4 and halt. Do not begin execution.

---

## Step 3 — Execute the steps in order

Once preflight passes, the plan is authoritative until you finish or hit one of the stop categories in Step 4. There is no third option. You do not silently adjust a step. You do not skip a step. You do not insert a step the plan did not authorize.

For each step in scope:

1. Mark its `TodoWrite` entry `in_progress`. In one short sentence, state the step number, what it changes, and the Source/standard the plan cites for it.
2. Make the changes the step specifies — **only those changes.** No cleanup, refactors, comments, renames, or "while I'm here" improvements the plan did not authorize. Adjacent code that looks wrong is not your concern unless the plan names it as a foundation correction.
3. **Verify the step using the right tool for each claim it makes**, per the taxonomy. The plan's "Verification" line for a step usually names a runtime command, but confirming the step is *done correctly* often needs more than that:
   - **Runtime claim** (a test passes, a build succeeds, a migration applies) → run the command and **show the actual command and the actual output.** "Tests pass" with no output is assertion, not verification.
   - **Behavioral claim** (the new function returns X under Y, the new endpoint enforces auth, the new handler emits the right error) → cite the test that exercises the path, or Read the specific lines that establish the behavior, or reproduce the condition and report what you observed.
   - **Structural claim** (no new dependents outside the plan's "Files affected", the change does not cross an architectural boundary) → re-establish dependents on the *actually-modified* files and compare against the plan.
   - **Library claim** (the new code calls the library correctly per its current API) → cite the docs lookup that confirmed the API shape, including the version.
   - **Standard-compliance claim** (matches OWASP X, RFC Y, framework convention Z) → cite the standard's text and the specific property in the new code that satisfies it.

   Each verification entry in your report names the **claim type, the tool, and the evidence** — not just the command. A verification that does not name what kind of claim it is verifying is the same failure as an unnamed approval that the Expert Standard rejects.
4. If verification fails: diagnose the root cause and fix it **within the step's authorized scope**, then re-verify. If the failure reveals one of the stop categories, halt per Step 4. If it is just a bug in your own implementation of the step, fix and re-verify.
5. Mark the entry `completed` only after every claim type the step makes has been verified with the appropriate tool and the evidence is recorded.

---

## Step 4 — When (and only when) to stop mid-execution

Stopping is reserved for cases where continuing would either violate a non-negotiable rule or build work on a false premise. Only the categories below qualify, and no others:

- **HARD-RULE-CONFLICT** — A step would violate a non-negotiable rule the project has stated (in its rules/conventions doc). Cite the specific rule. If the project has no such doc, this category has no source and does not fire.
- **PREMISE-FALSE** — A factual claim the step depends on is provably wrong against current source. ("Plan says `update_status()` is at `services/status.py:42`; a Read of that file shows the function is named `apply_status_change` at line 87.") Memory or intuition is not evidence — show the grep / Read / docs output.
- **BLAST-RADIUS-EXCEEDS-PLAN** — Implementing the step as written cascades into files outside the plan's "Files affected." Cite the dependents the plan did not list.
- **ENVIRONMENT-BLOCKED** — A verification command cannot run for an environmental reason (missing service, broken migration state, missing secret). Cite the command and the exact error.

What does **not** qualify as a stop reason — continue in every one of these:
- "I would have used a different library / pattern / abstraction." Disagreement is not a defect.
- "The codebase has a different convention." Plan divergences from codebase patterns are intentional unless the plan says otherwise.
- "This step seems unnecessary." Scope is the planner's call, not yours.
- "I think there's a more elegant approach." Elegance is not a standard.
- "The next step would be cleaner if I also did X now." Do only the current step. The plan's ordering is part of its contract.

**Before you emit a stop, verify it yourself.** With no subagent, there is no second party to re-run your evidence — so you re-run it. Re-Read the cited line *now*, re-run the grep, re-resolve the library against current docs, re-run the failed command. Memory of what you saw earlier is not evidence; emit the stop only if the evidence reproduces freshly at the moment you stop. This self-check catches stale and sloppy stops. Be honest that it cannot fully replace an independent reviewer — a consistent blind spot will survive your own re-check. The genuinely independent check lives at the review gate (see "Hand off to independent review"), not here.

When one of those categories triggers and your evidence reproduces, **emit a STOP REPORT in this exact format and halt:**

```
STOP REPORT
Category: <HARD-RULE-CONFLICT | PREMISE-FALSE | BLAST-RADIUS-EXCEEDS-PLAN | ENVIRONMENT-BLOCKED>
Step: <plan step number and one-line title>
What the plan asserts: <verbatim quote or paraphrase from the plan, with location>
What is actually true: <evidence — grep output, Read of file:line, docs source + version, command + error>
Why this blocks the step (not just inconveniences it): <one paragraph>
Project rule cited (if applicable): <rule reference and the rule's text>
Options for the user:
  A. Amend plan — what specifically changes (route to the planning step)
  B. Override and continue — what the override means and what risk it accepts
  C. Abort the step / scope — what state the work is left in
Recommendation: <A | B | C> — one sentence why
Working tree state at stop: <committed / uncommitted / partial>
Steps completed before stop: <list with verification evidence>
```

Do not implement the fix yourself. Do not pick the option for the user. Halt and return the report.

---

## Step 5 — Apply the Expert Standard to your own work

Before marking any step `completed`:

- Did the verification command actually run? Cite the command and its output, not your impression of it.
- For any "looks good"-type judgment, did you name the property that makes it good and how you confirmed it? The standard requires this for every approval.
- For any claim about what code does, did you verify it against current source — not memory, not the plan's assertion?
- Did you avoid silently propagating a codebase pattern the plan explicitly diverged from?

If any answer is no, fix the gap before marking the todo complete.

---

## Step 6 — Final report

Whether you finish all steps in scope or halt with a STOP REPORT, your final message contains, in this order:

1. **Preflight verdict** — `PREFLIGHT PASS` (one line per category checked) or `PREFLIGHT FAIL` with the report.
2. **`TodoWrite` final state** — every entry with its terminal status (`completed`, `in_progress`, `pending`, `cancelled`).
3. **Steps completed** — plan step numbers, each with the verification command and a one-line summary of its observed output. When you are dispatched by the expert-lifecycle orchestrator, this list is reconciled mechanically against the plan's declared step IDs: a `completed` status with any plan step missing from the list, or without evidence referencing each step, is refused as a premature completion claim. Only a `halted` return may be partial.
4. **Files changed** — every file created, modified, or deleted, mapped to the plan's "Files affected." Any file you touched that the plan did not list is called out explicitly with reasoning (and likely should have been a BLAST-RADIUS-EXCEEDS-PLAN stop).
5. **Stop report (if any)** — the structured block from Step 4, verbatim. Empty if execution completed.
6. **State of the working tree** — what is committed, what is uncommitted, what tests pass, what is red, and the exact commands to reproduce the state.
7. **Review-gate readiness** — exactly one of: `READY FOR INDEPENDENT REVIEW` (all in-scope steps completed, no stop report, verifications green), or `NOT READY — <one-line reason citing the stop report or remaining failed verification>`.

Do not summarize away problems. Do not soften severity. The full record is the deliverable. You do not grade your own work — this flag only tells whether the review gate should run next.

---

## Hand off to independent review

You never grade your own work — ever. The review that decides whether the work is done is performed by a **separate general-purpose subagent**, given **only mechanical facts**, so its judgment is independent of yours. This is the one place this skill uses a subagent, and contaminating it with your own assessment defeats the entire point of having it.

When the final report reads `READY FOR INDEPENDENT REVIEW`, obtain the review this way:

- **Subagent:** general-purpose.
- **Inputs — mechanical only:** the diff (or the list of files changed) and the plan path. Nothing else.
- **Instruction:** run the independent review (e.g. `/expert-review`, or this project's independent review tool) against the plan. Nothing more.

The dispatch must be **neutral** — no "check my fixes," no "I think this is solid," no pointing the reviewer at specific areas, no opinionated or suggestive language of any kind. Every review is dispatched the same neutral way, so no review is softened or steered.

**Use `references/review-handoff.md` for every review.** It carries the exact mechanical-only dispatch template, the neutral-language rules, a good-vs-bad example, and what to do after the review returns (PASS → you may record the work complete in the project's status doc, honestly; findings → route them to a planning step for a remediation plan, then re-run this skill against that plan — fixes go through a plan, never informally).

---

## Resuming after a stop

When the user resolves a STOP REPORT — A (amend plan), B (override), or C (abort) — and execution continues, you continue **in this same session.** There is no re-dispatch.

- Skip steps already verified-complete (mark them `completed` in `TodoWrite` up front, carrying their verification evidence).
- Re-run preflight on the remaining in-scope steps before resuming execution.
- An override is scoped to **that one resume only.** It does not generalize. If the same condition recurs in a later step, STOP REPORT again — the slippery slope to prevent is "an exception made once becomes assumed everywhere."

---

## Boundaries — what this skill does NOT do

- It does not write or revise plans. That is a planning step (e.g. `/expert-plan`).
- It does not write specs. That is a spec step (e.g. `/expert-spec`).
- It does not produce architecture documents. That is an architecture step (e.g. `/architecture`).
- It does not grade its own output. The independent review is dispatched to a neutral subagent, per "Hand off to independent review."
- It does not mark the project's status doc "Complete" on its own say-so. Only an independent review PASS justifies that; until then the honest state is "code-complete, pending independent review."

## Inbound owner messages: questions are not work orders

Before acting on any owner message, classify it: **INTERROGATIVE** (asks why/what/how/whether,
explores an option, requests status or explanation) or **DIRECTIVE** (explicitly instructs a
change). An interrogative is answered with evidence only — candidate fixes may be described as
candidates, but NO artifact, code, ledger, or plan edit is made in response to it. Only an
explicit directive authorizes changes, and only the changes it names. If classification is
ambiguous, ask the owner one clarifying question before touching anything.

In this skill specifically: an owner question mid-execution never expands the current
step's authorized scope — the Step-3 scope rule binds until an explicit directive changes it.
