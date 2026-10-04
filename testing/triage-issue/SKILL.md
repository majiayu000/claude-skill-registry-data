---
name: triage-issue
description: "Invoked helper skill for deep bug diagnosis, usually delegated from /qa when a reported issue needs root-cause analysis and a TDD fix plan before implementation. Use when the cause is unclear, the bug is a regression, or the user explicitly wants diagnosis. Not for lightweight QA intake (use /qa) or already-clear implementation tasks (use /execute)."
sources:
  primary:
    - "Thinking in Systems — Donella Meadows"
  secondary:
    - "Why Programs Fail — Andreas Zeller"
    - "Domain-Driven Design — Eric Evans"
---

# Triage Issue

Investigate a reported problem, find its root cause, and create a GitHub issue with a TDD fix plan. This is a mostly hands-off workflow - minimize questions to the user.

## Invocation Position

This is an invoked helper skill, not a normal first stop for bug work. It normally runs from `/qa` when the per-issue depth check decides a specific reported bug needs root-cause analysis before it can be filed as a lightweight issue.

Use `/triage-issue` when the cause is unclear after lightweight exploration, the bug is a regression, reproduction is intermittent, multiple symptoms may share an upstream cause, or the user explicitly asks for diagnosis.

Do not use it directly as the entry point for bug conversations — start with `/qa`, which delegates here per issue when depth is warranted. Do not use it once the fix task is already clear enough for `/execute` either.

> **One question per turn.** When the diagnosis requires user input, ask one question at a time and wait for the answer before asking the next. Triage is mostly hands-off — minimize questions, but the ones you ask are sequential.
>
> **Prefer single-select.** Use single-select multiple choice when the user is choosing one direction, one priority, or one next step.
>
> **Use multi-select rarely.** Reserve it for compatible sets — goals, constraints, non-goals, success criteria — that can all coexist. If prioritization matters, follow up asking which selected item is primary.
>
> **Use the platform's question tool when available.** In Claude Code, use `AskUserQuestion`; in Codex, `request_user_input`; in Gemini, `ask_user`. Otherwise, present numbered options in chat and wait for the user's reply before proceeding.

## Process

### 1. Capture the problem

Get a brief description of the issue from the user. If they haven't provided one, ask ONE question: "What's the problem you're seeing?"

Do NOT ask follow-up questions yet. Start investigating immediately.

**Destination check (carry through from `/qa` or ask now).** If this triage was delegated from `/qa`, the user has already answered the destination question and a `Verification destination:` line is attached to the report — carry it through into the issue (Step 5 template). If the triage was invoked directly without going through `/qa`, ask the destination question now from `references/destination-check.md`:

> How will we know the fix worked end-to-end? Name the specific destination — a file/function, a log query, a dashboard view, a user-observable behavior, an assertion in a test — where the fix's effect must land.

At triage rigor, the answer must be substantive — by the time deep diagnosis is running, the destination should be answerable concretely. A vacuous answer (paraphrases the source-of-change, names "the code change exists", names emission without consumption) is a stronger signal here than at `/qa` intake: it suggests the structural condition `references/destination-check.md` describes (source-level finding without destination-side framing) is in play, and Step 2 should explicitly grep for the consumer/setup code before generating hypotheses. Two-or-more signals firing on the signal table AND a vacuous answer → pause triage and recommend `/research` Phase 0 before continuing.

### 2. Explore and diagnose

**Construct a deterministic feedback loop first.** Before any code analysis or hypothesis work, build a fast, agent-runnable, pass/fail signal that reproduces the failure the user described. This is the highest-leverage activity in this skill — every later step is guessing without it. The loop can be a failing test, a `curl` returning the wrong status, a script that prints a known-wrong value, or whatever the stack supports. It must:

- Run on demand with no manual setup beyond a single command
- Return a clear pass/fail outcome an agent can read
- Reliably reproduce the failure the user described — not a similar-shaped failure

**Do not proceed to hypothesis generation until the loop reproduces the failure.** Hypothesizing without a deterministic loop is guessing; Zeller's TRAFFIC framework names "Reproduce" and "Automate" as separate prerequisite steps for a reason, and they dominate time-to-fix on hard bugs. If you cannot construct a reproducing loop within ~5 minutes, scan Zeller's six dimensions of uncontrolled input — **data** (specific values, sizes, encodings), **user interaction** (sequence and timing of clicks, keystrokes, navigations), **time** (clock state, time-of-day, scheduling), **randomness** (seeds, UUIDs, hash collisions), **OS environment** (locale, filesystem, network, env vars, container vs host), and **thread schedules** (concurrent ordering, race windows) — and stop to ask the user for the one missing input from those dimensions that would unblock reproduction. The taxonomy is a probe, not a recital: name the specific value, flag, environment, or sequence the loop is missing, not the catalog. If reproduction is genuinely impossible (live-only failure, hardware-dependent race), say so explicitly in the issue and flag the diagnosis as best-effort code reading rather than silently proceeding.

**Recognize the Heisenbug pattern.** If the failure disappears under a debugger, vanishes when logging is added, or shifts shape under different observation tools, the bug is almost certainly undefined behavior interacting with environmental differences (memory layout, optimization level, instrumentation overhead). The remedy is to find the undefined behavior in the code — uninitialized memory, a data race, reliance on unspecified ordering — not to switch debuggers or strip the logging. A vanishing bug is evidence about the bug's *shape*, not a reason to abandon the trace; do not silently downgrade Heisenbug-shaped reports to "live-only failure."

**If the bug is a regression and a last-good state is known, bisect before reading code.** A regression is the one bug class where the answer is already recorded: some change turned working code into broken code, and the history knows which one. The loop you just built is exactly the oracle `git bisect run` needs, so hand it over and let history answer instead of reasoning toward it:

```bash
git bisect start <bad-ref> <good-ref>
git bisect run <the-loop-command>
git bisect reset
```

Read `git bisect --help` § "Bisect run" for the exit-status contract your loop has to satisfy — in particular the code reserved for revisions that cannot be built or tested — and confirm the loop meets it before starting, rather than discovering it partway through a run.

Treat the result as **evidence, not a suspect**. The failure-inducing change tells you when the infection entered the code; it does not tell you which line is defective, and the change that introduces a latent defect is often not the change that made it observable. Carry the diff into the trace below as a fact, and keep tracing backward from the failure.

Four conditions bound this:

- **Check the oracle's polarity on both ends before starting.** Run the loop on the known-bad ref and on the known-good ref, and confirm it returns non-zero and zero respectively. This is the cheapest check here and the one most worth doing, because the loop you built in Step 2 is a *reproducing* loop, and "the loop passes" reads two ways — *the bug is gone*, which is what bisect needs, or *the reproduction succeeded*, which is a natural shape for a script written to demonstrate a failure. Hand bisect an inverted or a constant oracle and it still terminates and still names a commit; it just names an innocent one, with exactly the confidence it would report a correct answer. So a completed run is not evidence the polarity was right — only the two-ended check is.
- **Squash-merged history yields a first-bad *PR*, not a first-bad commit.** That is still a narrowed diff and still worth having — but it is not a single line, so do not report it as one.
- **A nondeterministic loop breaks the oracle.** Bisect trusts every verdict it is handed, so a loop that reproduces intermittently will confidently name an innocent change. If the loop is flaky — the Heisenbug case above included — repair it first or skip bisect. Never bisect on a "usually reproduces" signal.
- **No known last-good state means skip it, and say so.** Do not guess a range. A bisect started from an invented `good` ref returns its answer with exactly the confidence of a real one, which is worse than returning nothing.

Use the Agent tool with subagent_type=Explore to deeply investigate the codebase. Your goal is to find:

- **Where** the bug manifests (entry points, UI, API responses)
- **What** code path is involved (trace the flow)
- **Why** it fails — trace backward from the failure point through the dependency chain rather than forward from the entry point. The root cause is often several layers upstream from the visible symptom.
- **What** related code exists (similar patterns, tests, adjacent modules)

Look at:
- Related source files and their dependencies
- Existing tests (what's tested, what's missing)
- Recent changes to affected files (`git log` on relevant files)
- Error handling in the code path
- Similar patterns elsewhere in the codebase that work correctly

**Form falsifiable hypotheses before testing any one.** With the feedback loop in hand and the code path traced, list 3-5 ranked candidate causes. State each in falsifiable form:

> If **X** is the cause, then changing **Y** will make the loop pass, and changing **Z** will make the failure worse or leave it unchanged.

Rank by strength of evidence — recent changes to the suspect path, structural plausibility, prior incident patterns. **"Prior incident patterns" means prior fix commits touching a candidate path**, read from the commit log rather than the issue tracker:

```bash
git log --oneline -i -E --grep='fix|bug|regress|revert' -- <candidate-path>
```

`-E` is passed explicitly rather than relying on the default dialect. `git log --grep` honors the `grep.patternType` config key, so in a repo or user account that sets it to `extended`, `perl`, or `fixed`, an escaped-alternation pattern matches **nothing** — and returns zero quietly, which the "best-effort" bullet below would then read as "no fix-commit convention here." An explicit flag beats config and makes the command mean the same thing in every repo the skill runs in.

Two conditions bind that count, and both are load-bearing:

- **Confirmatory, never generative.** It may only reorder candidates the failure trace already nominated; it must never nominate one. Zeller's rule is to start from the failure rather than from code you suspect, and a file's history is legitimate evidence about a candidate already in hand — it becomes suspicion-led search the moment it puts a file on the list.
- **Best-effort.** The grep presupposes that this repo's authors label fix commits recognizably. Absent such a convention the count is noise, so skip the step and say so rather than ranking on it.

**State the mechanism before reordering anything.** A high fix count is a correlation, and the standard counterexample is that senior developers get assigned the riskiest work, so their files top every defect ranking without those files being defect-prone. Name the mechanism in one line — "three prior fixes here, all null-guards at the same boundary" — or leave the ranking as it stands.

Show the ranked list to the user in one short message before testing the top hypothesis. The user checkpoint is cheap and catches insights you cannot infer from code reading alone ("we just deployed a change to candidate #3" is a common save). Drive the loop against the top hypothesis, revise the ranking when evidence contradicts it, and avoid anchoring on the first plausible idea — Zeller's scientific-method recipe.

 ### 2.5. Structural Diagnosis
 
 If the bug is straightforwardly isolated (off-by-one, missing null check, typo), skip this section. Not every bug is systemic — structural diagnosis is for bugs where the root cause suggests a recurring condition.
 
 After gathering evidence, step back from the code and diagnose the structural condition that allowed this bug to exist. This is the difference between "what broke" and "why the system is prone to this type of breakage."

 Start by reading the failure at three levels: **event** (what just happened), **pattern** (what keeps happening), and **structure** (what conditions, incentives, delays, or missing feedback loops make the pattern likely). If you only explain the event, you have not finished diagnosing the issue.
 
 Apply the diagnostic playbook:
 
 1. **Observe** — Describe the failure as a causal chain, not a single point. Include timing, sequence, and what triggered the chain.
 2. **Map** — Identify the stocks (accumulated state), flows (rates of change), feedback loops, and delays in the failing code path. Where does state build up? What governs the rate? Is there a balancing loop that should have prevented this? Is a delayed consequence hiding the connection between cause and effect?
 3. **Diagnose** — Match the failure pattern to a system archetype. See [systems-reference.md](systems-reference.md) for the archetype catalog and diagnostic questions. Common matches for bugs:
   - **Shifting the burden** — A workaround suppressed the symptom, weakening the fundamental fix. The symptom returned in a different form.
   - **Drift to low performance** — A standard eroded gradually. What was once a hard constraint became a soft preference, until it broke.
   - **Fixes that fail** — A previous fix introduced a delayed side effect that caused this bug.
 4. **Intervene** — Choose a fix at the right leverage level. See [systems-reference.md](systems-reference.md) for the leverage point ranking. Avoid parameter-level fixes (#12) when a structural fix (#5–#3) is available. Ask: "Does this fix address the condition, or just the symptom?" and "What feedback loop would keep this from quietly reappearing?"
 5. **Check for similar conditions** — Search the codebase for the same structural pattern elsewhere. If the archetype matches, the same bug is latent in those locations.

If the structural diagnosis reveals a deeper architectural problem, note it in the issue for follow-up via `/improve-codebase-architecture`.

**Feedback-loop diagram (optional).** If a system archetype applies (shifting the burden, drift to low performance, fixes that fail, or any other named archetype from the catalog), consider invoking `/mermaid` to render the causal-loop diagram and embed it in the issue. Meadows' archetypes are canonically drawn in the source material; rendering them as prose loses part of what makes the archetype transferable to a reader pattern-matching their own failure. Skip when the archetype is named but its loop is one short causal step that prose already captures cleanly.

### 3. Identify the fix approach

Run the proposed fix against the Step 2 feedback loop and confirm the loop now passes. If the loop still fails, your root cause identification is wrong — return to Step 2 and revise the hypothesis ranking. Only in the explicit "reproduction was genuinely impossible" branch from Step 2 may you skip this verification; in that case, restate that the root cause is a best-effort analysis based on code reading.

 Based on your investigation, determine:
 
 - The minimal change needed to fix the root cause
 - Which modules/interfaces are affected
 - What behaviors need to be verified via tests
 - Whether this is a regression, missing feature, or design flaw
 - If the structural diagnosis identified a leverage level, prefer fixes at that level or higher. A parameter fix (changing a constant, adding a null check) is appropriate for isolated bugs. A feedback-loop fix (circuit breaker, invariant assertion, monitoring check) is appropriate for bugs matching a system archetype.
 - If you choose a symptomatic fix for pragmatic reasons, say so explicitly and note what fundamental fix would remove the condition instead of merely managing it.

### 4. Design TDD fix plan

**Seam check first.** Before drafting cycles, confirm a regression test can be written at the *right* call site — a seam that exercises the real bug pattern, not a shallower stand-in. If the only available seam is too shallow (the bug lives in an inline closure inside a private method, only manifests through a global side effect with no public observer, or requires dependencies the production caller never injects), the regression test will encode false confidence.

**Stop and treat that as the diagnosis output.** A regression test at the wrong seam is worse than no regression test — it locks in a false-positive guard. Note in the issue that the bug exposes a missing test seam, recommend `/improve-codebase-architecture` with the specific call-site pattern, and either:

- Block this fix on the architectural work (preferred when the bug is structural in origin), or
- Proceed with a clearly labeled workaround-class fix and a follow-up seam-creation issue (when operational pressure justifies it).

This is Ousterhout's `rules-of-thumb` red-flag posture: when the right test is "too hard to write," the structure itself is the finding.

Create a concrete, ordered list of RED-GREEN cycles. Each cycle is one vertical slice:

- **RED**: Describe a specific test that captures the broken/missing behavior
- **GREEN**: Describe the minimal code change to make that test pass

Rules:
- Tests verify behavior through public interfaces, not implementation details
- One test at a time, vertical slices (NOT all tests first, then all code)
- Each test should survive internal refactors
- Include a final refactor step if needed
- **Durability**: Only suggest fixes that would survive radical codebase changes. Describe behaviors and contracts, not internal structure. Tests assert on observable outcomes (API responses, UI state, user-visible effects), not internal state. A good suggestion reads like a spec; a bad one reads like a diff.

### 5. Create the GitHub issue

Create a GitHub issue using `gh issue create` with the template below. Do NOT ask the user to review before creating - just create it and share the URL.

**Match the repo's label convention first.** When invoked from `/qa`, this issue *replaces* the lightweight one `/qa` Step 4 would have filed — including that step's labeling, which is skipped along with the rest of Step 4. A QA session that mixes lightweight and deep issues would otherwise emit some labeled and some not, and inconsistency reads as intentional. Apply the same rule as `/qa`'s "Match the repo's label convention" step: read `gh label list` and the labels on recent issues, apply what matches, and ask before creating a new label. Do not impose a taxonomy — this skill runs in repos it does not own.

<issue-template>

## Problem

Open with a short plain-language walkthrough (usually a single paragraph) that frames the bug for a reader who doesn't have the codebase in their head: what part of the system this touches in domain terms, what the user or system was trying to do, and why the failure matters. Then the concrete details:

- What happens (actual behavior)
- What should happen (expected behavior)
- How to reproduce (if applicable)

Skip the walkthrough only for narrow, self-evident failures whose domain meaning is obvious from the stack trace. See `references/writing-for-humans.md` for the shape and revision bar.

## Verification destination

[The destination the fix's effect must reach, named in domain terms — a user-observable behavior, a log/trace observation, a dashboard view, an assertion in a test. Distinct from the source-of-change. See `references/destination-check.md` for substantive vs vacuous examples. The TDD Fix Plan below should land its final passing assertion at this destination, not at a paraphrase of the source.]

## Root Cause Analysis

Describe what you found during investigation:
- The code path involved
- Why the current code fails
- Any contributing factors

**Fix type:** Correction (addresses root cause) / Workaround (suppresses symptom — note what the real fix would require)

Do NOT include specific file paths, line numbers, or implementation details that couple to current code layout. Describe modules, behaviors, and contracts instead. The issue should remain useful even after major refactors.

## Structural Diagnosis

- **Pattern:** [Archetype name if one matches, e.g., "Shifting the burden" — or "Isolated incident"]
- **Structural condition:** [Why the system is prone to this class of failure]
- **Similar conditions:** [Other code paths with the same structural pattern, if found]
- **Leverage level:** [Parameter fix / Feedback loop fix / Structural fix]
- **Delayed effects to watch:** [What consequence might show up later if this fix is incomplete or creates a new side effect]
 
 [Omit entirely for straightforward isolated bugs.]

## TDD Fix Plan

A numbered list of RED-GREEN cycles:

1. **RED**: Write a test that [describes expected behavior]
   **GREEN**: [Minimal change to make it pass]

2. **RED**: Write a test that [describes next behavior]
   **GREEN**: [Minimal change to make it pass]

...

**REFACTOR**: [Any cleanup needed after all tests pass]

## Acceptance Criteria

- [ ] Criterion 1
- [ ] Criterion 2
- [ ] All new tests pass
- [ ] Existing tests still pass

</issue-template>

After creating the issue, print the issue URL and a one-line summary of the root cause.

## Handoff

- **Expected input:** a single reported bug, usually delegated from `/qa`'s per-issue depth check, that needs diagnosis before implementation
- **Produces:** a GitHub issue with root-cause analysis, structural diagnosis when relevant, and a TDD fix plan — replaces the lightweight issue `/qa` would otherwise have filed for this bug
- **May recommend:** `/improve-codebase-architecture` when the bug reveals a deeper structural pattern, or when the Step 4 seam check finds no correct call site for a regression test
- **Usually invoked by:** `/qa`
- **Returns control to:** the calling `/qa` loop for the next observation, or `/execute` (often via `/tdd`) when the bug is ready to implement
