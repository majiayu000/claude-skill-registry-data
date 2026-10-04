---
name: which-workflow
description: Pick the right RepoPrompt workflow for a task — or none. Use when the user asks which workflow to run, when dispatching a RepoPrompt workflow (Build It, Deep Plan, Orchestrate, Ship Spec, Pro Edit) and the choice isn't already named, or when deciding whether a change warrants Pro Edit's enforced pipeline versus a direct edit.
---

# Which Workflow?

Decision guide for picking a RepoPrompt workflow (or none). Read top to bottom; take the first row that fits.

## Quick table

| The task is… | Use | Why |
|---|---|---|
| A question, orientation, "how does X work?" | No workflow — chat, or built-in **Investigate** | Workflows add overhead; reading is enough |
| A trivial edit you could describe as one diff hunk | No workflow — direct edit + `commit-me` | Plan/review stages cost more than the change |
| One clear, coherent change (single seam, low fan-out) | **Build It** | Orientation → plan → implement → review → commit in one session |
| A clear multi-file change with regression risk | **Pro Edit** (built-in) — see rule below | Enforced plan → delegate → independent review; direct edit tools are disabled |
| A fuzzy request where the real work is deciding *what* to build | **Deep Plan (TDD)** | Deliverable is a plan doc, not code; implement later via Build It / Orchestrate |
| A large task that decomposes into independent pieces | **Orchestrate (TDD)** | Plan, decompose, delegate to sub-agents, verify each |
| Tickets published, slicing unvalidated | `/slice-check` (skill, user-invoked) | Cold-read probes grade each ticket against the smart zone before any dispatch |
| A spec / ticket graph to land as one PR | **Ship Spec** | Walks the frontier, dispatches Build It children, cold-reviews, opens the PR |
| "What happened while I was away?" | **catch-up** | |
| Docs drifted from code | **doc-sync** | |
| New repo, no map | **onboarding** | |

## The Pro Edit rule

Pro Edit is Build It with the seatbelt bolted on: the outer agent **cannot** touch files directly (`apply_edits`/`file_actions` disabled), must delegate through a validated XML payload, and must review the actual changed tree with an independent critique. That enforcement is its only advantage over Build It — and its whole cost.

Take Pro Edit when **all** of these hold:

1. **The desired behaviour is already clear.** You can state acceptance criteria without research. (If not → Deep Plan first.)
2. **One cohesive change, several related files.** Refactor of a shared flow, API-shape change, bug spanning consistent code paths. (One file → Build It or direct edit. Independent pieces → Orchestrate.)
3. **Regression risk makes "verify, don't trust" worth paying for.** Public types, serialization, auth, money, anything with existing callers you might break.
4. **You'd be tempted to skip a step.** Honest tell: if running Build It you'd plausibly shortcut the review or edit opportunistically mid-plan, the enforced pipeline earns its overhead.

Skip Pro Edit when **any** of these hold:

- The change is small enough that plan + delegate + review triples the cost of just doing it.
- The task needs discovery or design judgment mid-implementation — the rigid delegate payload can't adapt; Build It can.
- The RepoPrompt delegation bridge is acting up (see `misc/repoprompt-agent-run-*` skills). Pro Edit sits on that bridge and is told to halt-and-report on failure, not fall back — a flaky bridge means a stalled run.

### Prompting Pro Edit

Give behaviour and boundaries, not files: desired outcome, invariants ("public types unchanged", "no unrelated refactoring"), test expectations, and a verification command. The Architect finds the files; your acceptance criteria are what the Reviewer checks against.

### Failure handling

`partial_failure` still reaches review — read the report for which files failed. `failed` / `no_changes` / `timed_out` / preflight rejection stop the run: fix the prompt or fall back to Build It manually. Never let it (or yourself) silently hand-edit around a bridge failure.

## Rules of thumb

- **Enforcement is the product.** Pick Pro Edit for the seatbelt, Build It for the speed, Orchestrate for the fan-out, Deep Plan when the deliverable is a decision.
- **Chain, don't cram.** Fuzzy + risky = Deep Plan → Pro Edit, not one workflow stretched over both jobs.
- **Escalate lazily.** Start with the cheapest row that fits; a Build It run that turns out to need decomposition can be aborted and re-dispatched, which is cheaper than defaulting to heavy pipelines.
