---
name: ai-proxy-discipline
version: "1.5.0"
user-invocable: false
description: "Bounded-authority AI proxy that occupies the human seat at interactive checkpoints of unattended runs: answers intake questions, picks among pre-approved approaches, grants bounded pre-authorization approvals, and adversarially checks completion reports — fresh context, artifact-only inputs, evidence-tagged verdicts, every decision ledger-marked and human-overturnable. Reserved for real humans: irreversible actions, over-budget, protected-branch merges, outcome acceptance, high-impact gates. Referenced by hosts via frontmatter dependencies; activated per-run by Stage-exit policy: ai-proxy. Triggers — 「AI 代理」「模拟人把关」「代理质询」「无人值守交互核对」 / AI proxy, simulated reviewer, bounded proxy. Do NOT use as a substitute for a present human who has not explicitly opted in and completed thin freeze; for auto-mode stage advancement (workflow-mode-lifecycle owns that); or as approval authority for the reserved list."
dependencies:
  - intake-interview-discipline
---

# AI Counterpart Discipline

> Internal shared skill. Single source of truth for **who may occupy the human seat when no human is present, with what authority, and under what anti-sycophancy protocol**. Control flow (when a workflow advances) belongs to `workflow-mode-lifecycle`; interview methodology (what to ask, how to freeze, self-answer ladder, ledger) belongs to `intake-interview-discipline`. This skill composes both: it casts a bounded adversarial agent into the seat their modes leave empty.
>
> **Prerequisite check**: verify `intake-interview-discipline` is available on load; if missing, abort and print `npx skills add FuDesign2008/open-skills -g --skill intake-interview-discipline --yes`. No silent fallback — without it there is no ledger or interview for the proxy to plug into.

## Why bounded authority, not full proxy

The proxy's every decision draws on authority the human already granted at trigger + freeze time; it never creates new authority. That derivation rule is what keeps the proxy from becoming an escape hatch around `design-approval-gate`: that gate governs *new* high-impact scope, and new scope is exactly what the reserved list forbids the proxy from touching.

## Authority charter

**Bounded list** (may exercise, each ledger-marked `proxy-made`):

- Answer intake questions grounded in project context and constraints (never invent facts — investigate or mark `[UNRESOLVED]`)
- Pick an approach among **pre-approved options** presented in the comparison table
- Quality verdicts at enumerated checkpoints — including **rejecting** a report and demanding re-verification
- Card/contract approval as **bounded pre-authorization** within already-delegated scope
- Continue/stop the original frozen scope after re-validating constraints

**Reserved list** (human-only; a hit produces a ticket + park, never self-approval):

- Irreversible actions (deploy, push to protected branches, delete, publish, outbound messages)
- Budget extensions or over-cap dispatch
- Protected-branch merges
- Outcome-type acceptance
- `design-approval-gate` high-impact gates
- Any scope change beyond the frozen contract

Template in [reference.md](reference.md) § Charter.

## Adversarial protocol (anti-sycophancy by construction)

A same-context reviewer tends to anchor on the executor's framing — the failure this protocol exists to prevent. Four structural rules, borrowed from `multi-agent-debate`'s blindness principle:

1. **Fresh context** — instantiate per checkpoint; no session history from the executor.
2. **Artifact-only inputs** — charter + the artifacts under review (card / plan / report / diff) + repository facts it may fetch itself; **never** the executor's reasoning transcript.
3. **Challenge-not-please mandate** — the proxy's job is to find the flaw and ask the question the executor hopes won't be asked; a proxy that only agrees is failing its role.
4. **Evidence-tagged verdicts** — every conclusion carries `[FACT:source] / [INFERENCE] / [UNRESOLVED]`; an untagged verdict is invalid and treated as no verdict (the checkpoint then escalates or parks, it does not pass).

Prompt template in [reference.md](reference.md) § Counterpart Prompt.

## Ledger integration

Every proxy decision enters the host's acceptance ledger per `intake-interview-discipline` §C, marked `proxy-made`, with rationale + evidence tags + impact tier. Acceptance surfaces them like any entry; the human MAY overturn any of them; overturned findings feed the next run's intake.

## Checkpoints

Enumerated in the host contract at opt-in (default set: intake Q&A, approval event, high-impact escalation touchpoint, completion-report check, conflict re-adjudication). Each invocation counts against the run budget. Between checkpoints the `intake-interview-discipline` §B ladder governs — the proxy is not continuously present, and the §B "next human touchpoint" for high-impact items MAY be a proxy checkpoint (reserved items still human-only everywhere).

## Integration guide (for referencing hosts)

1. Declare `ai-proxy-discipline` in frontmatter `dependencies`; prerequisite-check it — abort with install guidance when missing **and the run opted in**; a missing dependency with no opt-in is not a failure.
2. Record `Stage-exit policy: manual | ai-proxy | auto` in the run contract / task card (set by the queue's interaction-budget ticket **or** an independent thin freeze; default absent = host legacy behavior). Any value other than proxy → behavior identical to today.
3. Wire thin pointers at the enumerated checkpoints ("proxy per `ai-proxy-discipline`") — never restate the charter or protocol prose.
4. Pass each checkpoint: fresh agent, charter + artifacts only, require tagged verdicts, ledger the outcome.

### Independent thin freeze

A verbal overlay request (host triggers such as 「ai-proxy 模式」 / "ai-proxy mode" / 「切换 ai-proxy」) is **not** occupancy. Occupancy starts only after this-run contract fields are written and confirmed: destination, constraints (reserved list still human-only), `Stage-exit policy: ai-proxy`. The contract MAY live in conversation output — template in [reference.md](reference.md) § Thin freeze. After confirm, PDCA host-exit rules below apply. A present human who explicitly opted in and completed the freeze MAY have the proxy occupy later checkpoints; freeze Q&A itself stays with that human. Implicit continuation phrases do not start freeze or occupancy.

### PDCA host exits

For stage-gated PDCA hosts (`solve-workflow` / `opsx-solve-workflow` / `jira-fix-workflow` / `opsx-jira-fix-workflow`): when this-run contract or task card records **`Stage-exit policy: ai-proxy`** (auto carrier), each manual stop point (stage exit) becomes a proxy checkpoint under the same charter. Queue-child dispatch is sufficient but **not required**. Hosts starting with a frozen contract (queue child with problem+frozen decisions supplied, **or** independent thin freeze completed) also open with a **stop-point forecast** — every manual exit marked covered-by-frozen-decisions or will-form-a-new-ticket — so the interaction-budget owner knows the interaction count before analysis begins. Mid-run overlay after thin freeze forecasts **remaining** exits and continues the current stage (does not restart analysis). — fresh context, that stage's output as the artifact-only input, evidence-tagged verdict, ledger-marked `proxy-made`. At the pre-execution approval point, the proxy's **bounded pre-authorization replaces the bare auto-mode escape** of `design-approval-gate` — strictly stronger, because the charter bounds, ledger entry, and human overturn replace a 留痕-only pass-through. Merge decisions, irreversible actions, protected-branch operations, and external-tracker writebacks (e.g. Jira status transitions) stay human-only; a hit parks the item with a ticket. Jira / opsx-jira PR-open and archive+PR-open terminals remain bound to an explicit `queue-child` flag. Hosts integrate with one thin pointer section plus the frontmatter dependency — never restating this prose.

## Forbidden

- Restating this charter/protocol in host bodies
- Feeding the proxy the executor's reasoning transcript
- Accepting untagged verdicts; approving into the reserved list; treating proxy approval as human approval
- Continuous presence beyond enumerated checkpoints (cost + authority-surface control)
