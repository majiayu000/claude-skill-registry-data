---
name: qa
description: "Side-route skill and single entry point for bug conversations. Use when the user is reporting observed failures and wants durable GitHub issues filed in project language. Delegates per-issue to /triage-issue for bugs that need root-cause diagnosis, then returns to the loop. Not for already-scoped implementation work (use /execute)."
---

# QA Session

Run an interactive QA session. The user describes problems they're encountering. You clarify, explore the codebase for context, and file GitHub issues that are durable, user-focused, and use the project's domain language. For any one bug that needs deeper diagnosis before it can be filed lightweight, you delegate to `/triage-issue` for that issue and then return to the loop for the next observation.

## Invocation Position

This is a side-route skill, not a default shaping or implementation step. It is the **single entry point for bug conversations** — `/triage-issue` is no longer a direct entry point and is instead invoked from here on a per-issue basis when depth is needed.

Use `/qa` when the user is testing behavior, reporting bugs conversationally, or wants help turning observed failures into durable GitHub issues.

Do not use it when the task is already a concrete, well-scoped implementation task ready for `/execute`.

> **One question per turn.** When clarifying a reported bug, ask one question at a time and wait for the answer before asking the next. Do not over-interview — two or three short questions is usually enough, but they are asked *sequentially*, never as a batched list.
>
> **Prefer single-select.** Use single-select multiple choice when the user is choosing one direction, one priority, or one next step.
>
> **Use multi-select rarely.** Reserve it for compatible sets — goals, constraints, non-goals, success criteria — that can all coexist. If prioritization matters, follow up asking which selected item is primary.
>
> **Use the platform's question tool when available.** In Claude Code, use `AskUserQuestion`; in Codex, `request_user_input`; in Gemini, `ask_user`. Otherwise, present numbered options in chat and wait for the user's reply before proceeding.

## For each issue the user raises

### 1. Listen and lightly clarify

Let the user describe the problem in their own words. Ask up to 2–3 short clarifying questions **one at a time**, focused on:

- What they expected vs what actually happened
- Steps to reproduce (if not obvious)
- Whether it's consistent or intermittent

Do NOT over-interview. If the description is clear enough to file, move on.

**Destination check (always ask last).** After symptom / reproducer / expected-vs-actual, ask one more question — the destination check from `references/destination-check.md`:

> How will we know the fix worked end-to-end? Name the specific destination — a file/function, a log query, a dashboard view, a user-observable behavior, an assertion in a test — where the fix's effect must land.

Record the answer as a `Verification destination:` line in the filed issue body (Step 4c template). Then consult `references/destination-check.md`'s signal table against the user's framing of the bug and the proposed fix. Count signals:

- **Zero or one signal firing** → accept any non-empty answer and proceed.
- **Two or more signals firing** AND the destination answer is vacuous (paraphrases the source-of-change, names "the code change exists", names emission without consumption, or is empty) → firmly recommend `/research` Phase 0 before filing. Phase 0 will grep the repo for the corresponding consumer/setup code; if it returns null, reshape the issue from "set the flag" to "wire the missing consumer" before any code is written. The user retains agency to file lightweight anyway, but the nudge surfaces the reachability constraint instead of leaving it in the developer's head.

This catches source-vs-destination mismatch at intake — a fix that flips a producer-side value without verifying that any consumer reads it, a cache invalidation with no subscriber, a permission grant with no enforcer, a telemetry flag with no emission boundary registered in the target runtime. See `references/destination-check.md` for substantive vs vacuous examples and the full signal table.

### 2. Explore the codebase in the background

While talking to the user, kick off an Agent (subagent_type=Explore) in the background to understand the relevant area. The goal is NOT to find a fix — it's to:

- Start with a lightweight hypothesis about what class of failure might explain the behavior so your exploration is guided rather than wandering. Revise the hypothesis as you gather evidence.
- Learn the domain language used in that area (check UBIQUITOUS_LANGUAGE.md)
- Understand what the feature is supposed to do
- Identify the user-facing behavior boundary

This context helps you write a better issue — but the issue itself should NOT reference specific files, line numbers, or internal implementation details.

### 3. Assess scope: single issue or breakdown?

Before filing, decide whether this is a **single issue** or needs to be **broken down** into multiple issues.

Break down when:

- The fix spans multiple independent areas (e.g. "the form validation is wrong AND the success message is missing AND the redirect is broken")
- There are clearly separable concerns that different people could work on in parallel
- The user describes something that has multiple distinct failure modes or symptoms

Keep as a single issue when:

- It's one behavior that's wrong in one place
- The symptoms are all caused by the same root behavior

### 3.5. Decide depth: lightweight file or delegate to /triage-issue

For each issue identified in Step 3, decide whether it can be filed lightweight or needs deeper diagnosis. Apply this decision **per issue**, not per session — most QA sessions mix both kinds.

**Delegate to `/triage-issue` when at least one of these holds:**

- The user explicitly asks for diagnosis, root cause, or "why" this is happening
- The bug is a regression — it worked before and broke recently
- Your lightweight Step 2 exploration could not form a confident hypothesis about the cause
- Reproduction is intermittent or unreliable
- Multiple symptoms might share an upstream cause and the user wants that confirmed

**Stay lightweight (continue to Step 4) when:**

- Reproduction steps are clear and the cause is obvious in class (missing validation, cosmetic issue, clear null case)
- The user just wants the bug on the backlog, not debugged
- The behavior is wrong in one place and the fix is uncontroversial

**When delegating to `/triage-issue`:**

`/triage-issue` will require building a deterministic, agent-runnable feedback loop that reproduces the failure before any hypothesis work, then ranking 3-5 falsifiable hypotheses against that loop. Expect a longer cycle than a lightweight file — the discipline pays off on hard bugs by replacing guesswork with a measurable signal.

1. State the decision and the reason to the user in one sentence — e.g. "This one looks like a regression and I can't form a hypothesis without reproducing it, so I'll switch to deep diagnosis for this issue."
2. Run `/triage-issue` Steps 2–5 (reproduce, explore + diagnose, optional structural diagnosis, fix approach, TDD fix plan, issue creation) on this single bug.
3. The issue created by `/triage-issue` **replaces** the lightweight issue Step 4 would otherwise have filed for this bug — do not file both.
4. Once the triage issue is created, return to the `/qa` loop and continue with the next observation in Step 5.

If Step 3 produced a breakdown, apply this depth decision to each sub-issue independently. A single QA report can produce a mix of lightweight `/qa` issues and deep `/triage-issue` issues.

### 4. File the GitHub issue(s)

This step runs only for issues that stayed lightweight in Step 3.5. Issues that delegated to `/triage-issue` are already filed by that skill and skip this step.

#### 4a. Closed-wontfix lookback (before filing)

Before creating each issue, search closed `wontfix` issues for the same idea. Already-rejected enhancements resurfacing as fresh issues consume triage cycles every time:

```bash
gh issue list --state closed --label wontfix --search "<keywords from this report>"
```

Pick keywords from the user's own description and the domain language you learned in Step 2 — not internal module names. Run the search before each issue, not once per session.

If a prior rejection surfaces:

- If the new report adds genuinely new evidence (a stronger user case, a regression that wasn't there at rejection time, a constraint that has changed), reopen the prior issue and add the new evidence as a comment — do not file a duplicate.
- If the new report is the same idea with no new evidence, link the prior closed issue back to the user with a one-sentence summary of why it was rejected, and ask whether they want to reopen with new evidence or accept the prior decision. Do not silently file a duplicate.
- If unsure, link the prior issue in the new issue's body so the rejection rationale is one click away for the next reviewer.

This is a process check, not an enforcement gate — closed-wontfix history is treated as durable state that lives in GitHub. Skill Kit deliberately does not maintain a parallel filesystem archive of rejected enhancements (per `SYSTEM-OVERVIEW.md` "State lives in GitHub, not the filesystem").

#### 4b. Match the repo's label convention (before filing)

Read the labels the repo already uses, then apply the ones that fit:

```bash
gh label list
gh issue list --state all --limit 20 --json number,labels \
  --jq '.[] | select(.labels | length > 0) | {number, labels: [.labels[].name]}'
```

Apply the matching labels with `--label` on `gh issue create`. Match what is there — do not impose a taxonomy. Skill Kit runs in repos it does not own, and a convention you invent is one the maintainers have to live with. If nothing fits and a new label would genuinely help, **ask the user before creating one**.

If the repo has no labels at all, file without them and say so once; do not manufacture a scheme.

This step is load-bearing rather than cosmetic. GitHub's `parent-issue:` search qualifier does not work — the sub-issue progress badge links to a query the search backend rejects, and `has:parent-issue` silently matches every issue in the repo. A shared label is currently the only mechanism that makes a batch of related issues retrievable by someone who was not in the session that filed them.

#### 4c. Create the issue

Create issues with `gh issue create`. Do NOT ask the user to review first — just file and share URLs.

Issues must be **durable** — they should still make sense after major refactors. Write from the user's perspective.

#### For a single issue

Use this template:

```
## What happened

[Describe the actual behavior the user experienced, in plain language]

## What I expected

[Describe the expected behavior]

## Steps to reproduce

1. [Concrete, numbered steps a developer can follow]
2. [Use domain terms from the codebase, not internal module names]
3. [Include relevant inputs, flags, or configuration]

## Verification destination

[The destination the fix's effect must reach, named in domain terms — a user-observable behavior, a log/trace observation, a dashboard view, an assertion in a test. Must be distinct from the proposed source-of-change. See `references/destination-check.md` for the substantive vs vacuous bar.]

## Additional context

[A short plain-language walkthrough that frames the bug for a reader unfamiliar with the codebase: one paragraph of domain setup (what part of the system this touches, in the user's own words), the bug stated in plain English, and why it matters to a user or future maintainer. Skip the walkthrough for trivially-reproducible bugs with no domain nuance — a single line is fine there. Use domain language but don't cite files or line numbers. See `references/writing-for-humans.md` for the shape and revision bar.]
```

#### For a breakdown (multiple issues)

Create issues in dependency order (blockers first) so you can reference real issue numbers.

Use this template for each sub-issue:

```
## Parent issue

#<parent-issue-number> (if you created a tracking issue) or "Reported during QA session"

## What's wrong

[Describe this specific behavior problem — just this slice, not the whole report]

## What I expected

[Expected behavior for this specific slice]

## Steps to reproduce

1. [Steps specific to THIS issue]

## Verification destination

[The destination this slice's fix must reach — domain-language, distinct from the source-of-change. See `references/destination-check.md`.]

## Blocked by

- #<issue-number> (if this issue can't be fixed until another is resolved)

Or "None — can start immediately" if no blockers.

## Additional context

[Any extra observations relevant to this slice]
```

When creating a breakdown:

- **Prefer many thin issues over few thick ones** — each should be independently fixable and verifiable
- **Mark blocking relationships honestly** — if issue B genuinely can't be tested until issue A is fixed, say so. If they're independent, mark both as "None — can start immediately"
- **Create issues in dependency order** so you can reference real issue numbers in "Blocked by"
- **Maximize parallelism** — the goal is that multiple people (or agents) can grab different issues simultaneously

**Then wire each blocking relationship as a native GitHub dependency.** The prose `## Blocked by` section records *why* a bug is gated and survives a tracker migration, but no tool reads it. The native edge is what automated selection queries — including `/execute`'s Blocked-slice gate, which stops before implementing a slice with an open blocker. A `/qa` bug filed with prose only returns no edges from that gate, so a genuinely blocked bug reads as takeable.

Once the issues exist and you have real numbers, wire one edge per `Blocked by` entry:

```bash
gh issue edit <blocked-number> --add-blocked-by <blocker-number>,<blocker-number>
```

⚠️ **Do not pass `--blocked-by` to `gh issue create`.** `create` applies relationships as a deferred second mutation; if it fails, `gh` reports an error, **suppresses the issue URL**, and offers a `--recover` prompt — but the issue was already created, so following the prompt files a **duplicate**. Create bare, capture the URL, then wire. (Verified in `gh` 2.97.0; [cli/cli#13899](https://github.com/cli/cli/pull/13899) is open and unmerged.)

Then confirm the prose and the edges agree — they encode the same fact, so a divergence check belongs at the one moment both are being written:

```bash
gh issue view <blocked-number> --json blockedBy \
  --jq '[.blockedBy.nodes[] | .number]'
```

A prose entry with no edge is a gate nothing enforces; an edge with no prose entry is a gate nobody can explain. Fix whichever is wrong.

**Graceful degradation.** Issue dependencies require `gh` ≥ 2.94.0 and are unavailable on GitHub Enterprise Server below 3.19. If the `edit` fails for that reason, keep the prose, tell the user the edges could not be wired, and carry on — the issues themselves are the deliverable. Do not fail a bug report over a relationship.

#### Rules for all issue bodies

- **No file paths or line numbers** — these go stale
- **Use the project's domain language** (check UBIQUITOUS_LANGUAGE.md if it exists)
- **Describe behaviors, not code** — "the sync service fails to apply the patch" not "applyPatch() throws on line 42"
- **Reproduction steps are mandatory** — if you can't determine them, ask the user
- **Keep it concise** — a developer should be able to read the issue in 30 seconds

After filing, print all issue URLs (with blocking relationships summarized) and ask: "Next issue, or are we done?"

### 5. Continue the session

Keep going until the user says they're done. Each issue is independent — don't batch them.

## Handoff

- **Expected input:** observed user-facing failures, regressions, or QA findings — `/qa` is the single entry point for bug conversations
- **Produces:** durable GitHub issues written in domain language, carrying the repo's existing label convention and native dependency edges alongside the prose `## Blocked by` section, plus per-issue triage issues from `/triage-issue` when depth was needed
- **Delegates per-issue to:** `/triage-issue` for bugs that fail the Step 3.5 depth check; control returns to the `/qa` loop after each delegation
- **Feeds back into:** `/execute` once the filed bug work is ready to implement
