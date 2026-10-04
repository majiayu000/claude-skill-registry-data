---
name: qa-plan
description: Generate a QA / acceptance checklist for a just-built change, derived from its intent rather than its diff. Run AFTER implementing, when you'd ask "how do I QA what we built?". Reads the issue / acceptance criteria first — before the code — so the plan probes for gaps instead of rubber-stamping what shipped. Output is a checklist a human or agent can walk; running it is a separate opt-in step. Use for a manual test plan, QA plan, or acceptance walkthrough. NOT verify (drives the app; this writes the plan it drives), NOT tdd (automated, test-first; this is acceptance, test-after), NOT feature-spec / to-issues (define intent before building; this consumes it after).
disable-model-invocation: true
---

# QA Plan

Produce the document a human or an agent walks to confirm a just-built change does what the issue asked. **The plan is the deliverable; running it is a separate, opt-in act.**

> Test the **intent**, against the **build** — never the build against itself.

Owns the _acceptance artifact_. Doesn't run the app (`verify` does) or write automated tests (`tdd` does).

## When this runs

```
intent (issue / feature-spec) → implement [→ tdd] → qa-plan → [optional] execute
```

After implementation, ideally once automated checks are green. TDD is not a prerequisite.

## Two rules

**Intent-first, not diff-first.** Read the acceptance criteria and derive flows _before_ you open the implementation — then read the code only to ground preconditions and selectors. Start from the diff and the plan inherits the code's blind spots.

**Scope to THIS change.** Cover the claimed criteria plus the blast radius they threaten — nothing else. Past ~a dozen steps, or into features this change never touched, you're QA-ing the framework. Cut back.

## Output shape

Fixed sections:

```
## Scope       — what this change put at risk; in / out
## Acceptance  — the criteria, VERBATIM, each linked to its step(s)
## Gaps        — criteria with no code path; risks with no coverage
## Checklist   — steps, grouped by flow
## Execution   — empty by default; filled only on the opt-in run
```

Each step — every `Expected` must be **observable** (a URL, visible text, a value, a state, an error). "Check it works" is not a step.

```
### [n] <flow name>  ·  traces: <criterion / issue line>
- Precondition: <state / data / role needed first>
- Action:       <the concrete thing to do>
- Expected:     <OBSERVABLE result>
- Result:       [ ] pass  [ ] fail
- human-eval:   <yes ONLY for subjective/visual judgement — else omit>
```

**The `human-eval` tag is load-bearing.** A person eyeballs "the modal looks right"; an agent can't, and left untagged it will confidently false-pass. Tag subjective/visual steps so an agent **skips and flags** it rather than faking a verdict. If you can make it observable (screenshot + explicit criteria), do that instead of tagging.

### Worked example

Change: _"Users can reset their password via an emailed link (link expires after 1h)."_

```
## Scope
In:  request-reset form, email dispatch, reset-link landing page, expiry.
Out: login itself, account creation, email deliverability/SMTP config.

## Acceptance
A1. "Submitting a registered email sends a reset link." → [1]
A2. "The link opens a set-new-password page."          → [1]
A3. "Links expire after 1 hour."                       → [2]

## Gaps
- A1 has no code path for UNREGISTERED emails — spec is silent on the
  response. Flagged; see step [3].

## Checklist

### [1] Happy path — reset via link  ·  traces: A1, A2
- Precondition: user alice@x.com exists; inbox reachable.
- Action:       submit alice@x.com on /forgot-password; open the emailed link.
- Expected:     lands on /reset?token=…; heading "Set a new password" visible.
- Result:       [ ] pass  [ ] fail

### [2] Expired link  ·  traces: A3
- Precondition: a reset token issued >1h ago (backdate or wait).
- Action:       open the expired link.
- Expected:     "This link has expired" shown; no password field rendered.
- Result:       [ ] pass  [ ] fail

### [3] Unregistered email (unnamed edge)  ·  traces: A1 (gap)
- Precondition: nobody@x.com is not a registered user.
- Action:       submit nobody@x.com on /forgot-password.
- Expected:     same neutral "check your inbox" message as [1] — no account
                enumeration (no "user not found").
- Result:       [ ] pass  [ ] fail

### [4] Reset form styling  ·  traces: A2
- Precondition: on /reset with a valid token.
- Action:       view the set-new-password form.
- Expected:     matches the design for the auth pages.
- Result:       [ ] pass  [ ] fail
- human-eval:   yes
```

Note step [3]: the spec never named the unregistered-email case, but this change exposes an enumeration risk — that's the value-add over a mechanical criteria→steps transform.

## Process

1. **Anchor on intent.** Pull the criteria **verbatim** — paraphrase is where drift re-enters. No written intent? Reconstruct it in a sentence, but this is the **weak mode** (the misreading that shipped can ship in the plan too) — confirm with the user first.
2. **Ground in the build.** _Now_ read the implementation — just enough for real preconditions, routes, selectors, inputs. Any criterion with no code path → `## Gaps`.
3. **Enumerate flows**: happy path(s) from the criteria → edges the spec **named** → edges the spec **did not name** but this change exposes (empty/invalid input, auth boundaries, error + retry, concurrency, the regression surface).
4. **Write each step in contract format** — observable `Expected` on every one; `human-eval` on the subjective ones.
5. **Present and stop.** Generate-only.
6. **Offer execution separately.** Ask once: walk it yourself, or hand to an executor (`verify` / `run` / `agent-browser`). Only on an explicit yes does anyone run it — and an agent executor must honor `human-eval` tags.

## Boundaries

| Want to…                                | Use                                             | Relationship                                          |
| --------------------------------------- | ----------------------------------------------- | ----------------------------------------------------- |
| Drive the app to observe the change     | `verify` / `run` / `agent-browser`              | They act; this writes the plan they act on.           |
| Write automated unit/integration tests  | `tdd`                                           | Code-contract, test-first; this is intent-acceptance. |
| Define what to build                    | `feature-spec` / `aa-design-spec` / `to-issues` | Produce the intent (before); this consumes it (after).|
| Transcribe reported bugs into a tracker | deprecated `qa`                                 | That's backward (bugs→issues); this is forward.       |

## Before you hand over the plan

- [ ] Flows derived from **intent first**, then grounded in the build?
- [ ] **Every** step has an **observable** `Expected`?
- [ ] Each step **traces** to a criterion; criteria with no code path in `## Gaps`?
- [ ] Happy path, **named** edges, and the **unnamed** edges this change exposes?
- [ ] **Scoped to this change** (~a dozen steps)?
- [ ] Every subjective/visual step tagged **`human-eval`**?
- [ ] **Stopped at the plan** and offered execution separately?
