---
name: bdd
description: Behavior-first feature development — use when building new
  capabilities, continuing feature work, or when work introduces new state
  or multiple user flows. Discovers desired behavior through examples and
  scenarios before implementation. Do NOT use for bug fixes, typos, or small
  isolated changes.
allowed-tools: "*"
---

# BDD Orchestrator

Behavior-first development for features. Discovery → Scenarios → Implementation.

**Iron Law:** DEFINE BEHAVIOR BEFORE IMPLEMENTATION

## Phase Tracking

Features progress through phases. Track in ticket frontmatter:

```yaml
---
type: feature
phase: implement # intake | define-behavior | scenario-gate | implement | verify | done
---
```

**Phase meanings:**

| Phase             | What happens                    | Details      |
| ----------------- | ------------------------------- | ------------ |
| `intake`          | Context check, discovery        | DISCOVERY.md |
| `define-behavior` | Writing Given/When/Then         | SCENARIOS.md |
| `scenario-gate`   | Validating scenarios            | SCENARIOS.md |
| `implement`       | Outside-in TDD                  | TDD.md       |
| `verify`          | Evidence gate: /verify + /audit | VERIFY.md    |
| `done`            | Close ticket                    | DONE.md      |

**Update phase when:**

- Completing a BDD phase → set next phase
- Scenario-gate complete → set `implement` (test-layer + sequencing happens at the scenario-gate exit)
- Handing off to TDD → set `implement`
- All scenarios pass → set `verify`
- /verify + /audit complete (verify.md exists) → set `done`

### Phase-exit review (Tier 2)

Leaving a phase is gated on an **independent** review of that phase's work — not
your own pass. (Your own inline pass is Tier 1: `/self-review`, per asset, as you
author.) The phase exit is reviewed by a _fresh reviewer with no conversation
history_ so the author can't grade their own work: run it in a forked subagent —
a skill with `context: fork`, or an explicit subagent — hand it only the phase's
artifacts and the ticket's scope, and let **its** verdict decide. On a pass,
record the stamp that unblocks the advance:

```bash
bun .safeword/hooks/write-review-stamp.ts --phase <phase you are leaving>
```

If the reviewer finds blocking issues, fix them and re-review — don't stamp. To
skip a trivial or docs-only phase, append a reason
(`… --phase <phase> "<why no independent review is needed>"`). The phase-advance
gate enforces this when the review gate is enabled, and is inert otherwise.

---

## Resume Logic

When user references a ticket, resume work:

1. **Read ticket** → get current `phase:`
2. **Find progress** → first unchecked `[ ]` in test-definitions
3. **Check context** → read last work log entry
4. **Announce resume** → "Resuming at [phase]. Last: [log entry]."

**Resume by phase:**

| Phase             | Resume action                              |
| ----------------- | ------------------------------------------ |
| `intake`          | Start understanding (propose-and-converge) |
| `define-behavior` | Continue drafting scenarios                |
| `scenario-gate`   | Continue validating scenarios              |
| `implement`       | Find first unchecked scenario, run TDD     |
| `verify`          | Run /verify and /audit, write verify.md    |
| `done`            | Close ticket (verify.md must exist)        |

---

## Current Behavior

1. Understand first (see SAFEWORD.md "Understanding") — propose-and-converge until user accepts proposal with structured scope
2. Size internally (see SAFEWORD.md "Sizing") — state scope assessment in proposal, not as a separate announcement
3. **If user references iteration/story/phase from a spec:**
   - Check if child ticket exists for that iteration
   - If not → create ticket, run full BDD
   - If yes → resume at current phase
4. **If ticket exists:** Read phase, resume at appropriate point
5. **Artifact-first rule:** Before doing work, create/verify the phase artifact:
   - intake → ticket at `.safeword-project/tickets/{id}-{slug}/ticket.md`
   - define-behavior → test-definitions at `.safeword-project/tickets/{id}-{slug}/test-definitions.md`
6. **Execute phase** using the appropriate phase file
7. **Update phase** in ticket when transitioning

---

## Phase Files

Load the appropriate file based on current phase:

| Phase             | File         |
| ----------------- | ------------ |
| `intake`          | DISCOVERY.md |
| `define-behavior` | SCENARIOS.md |
| `scenario-gate`   | SCENARIOS.md |
| `implement`       | TDD.md       |
| `verify`          | VERIFY.md    |
| `done`            | DONE.md      |

For splitting large features, see SPLITTING.md.

---

## Key Takeaways

- **patch/task** → TDD directly (RED → GREEN → REFACTOR)
- **feature** → full BDD flow, track in ticket `phase:` field
- **Resume** → read ticket, find first unchecked scenario, continue
- **Split** → check thresholds at Entry, define-behavior, scenario-gate; user decides (see SPLITTING.md)
- **Verify gate** → run /verify + /audit, writes verify.md. Stop hook blocks done without it.
- **Done** → close ticket (trivial — verify.md must already exist)
- When unsure → default to task, user can `/bdd` to override
