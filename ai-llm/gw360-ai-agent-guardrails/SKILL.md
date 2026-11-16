---
name: ai-agent-guardrails
description: Apply safety controls when an LLM agent has authority to act on real systems. Covers blast-radius classification, dry-run-first patterns, out-of-band approval gates, scope locking, idempotency, kill switches, and rollback strategies. Invoke when designing an autonomous agent, when granting an LLM write access to production, or after an agent makes an unexpected change.
---

# AI Agent Guardrails

LLMs make confident wrong decisions at scale. The cost of one wrong decision used to be one wrong commit; the cost of one wrong decision by an agent loop can be 30 wrong commits, 100 deleted DB rows, or a whole production site refactored into nonsense in 90 seconds.

This skill is a design checklist — not a runtime tool. It tells you **what to put in place before** giving an agent write access to anything that matters.

## When to invoke

- Designing a new agent, scheduled job, or autonomous workflow
- Granting an existing LLM access to a higher-tier credential or new tool
- After an agent did something unintended (start here; do not just tighten one prompt)
- Reviewing a third-party agent (e.g. an MCP that takes broad actions) before connecting it

## The core idea — blast radius

Classify every action an agent can take by what happens if it fires when it should not have.

| Tier | Example | Reversible? | Required guard |
|---|---|---|---|
| 1 | Read a local file, run a query | Trivially | None |
| 2 | Modify a single local file, write to a sandbox | Yes, with backup | Backup before action |
| 3 | Mutate a staging service or shared dev resource | Recoverable in minutes | Dry-run mode + explicit confirm |
| 4 | Production-data write, customer-visible change | Recoverable in hours, with effort | Approval gate + audit log + rollback plan |
| 5 | Send mail, spend money, modify DNS, deploy, push to main | Sometimes irreversible, externally visible | Out-of-band approval + rate limit + kill switch |

Every tool an agent can call belongs to exactly one tier. If you cannot say which, classify up.

## Pattern: dry-run-first

For tier ≥ 3, every write tool should support an explicit dry-run that produces the *exact* diff/plan that would be applied. The agent runs dry-run first by default; only after the operator approves the plan does it run the real action.

Implementation sketch:

```ts
type WriteToolResult =
  | { mode: "dryrun"; plan: ChangeSet; estimate: ImpactEstimate }
  | { mode: "apply"; applied: ChangeSet; receipt: string };

async function update_widget(args: Args, opts: { dryrun: boolean }) {
  const plan = computePlan(args);
  if (opts.dryrun) return { mode: "dryrun", plan, estimate: estimateImpact(plan) };
  const receipt = await applyPlan(plan);
  return { mode: "apply", applied: plan, receipt };
}
```

The orchestration prompt makes dry-run the default; switching to apply requires a literal token (e.g. user clicks "Approve plan #abc123" out-of-band).

## Pattern: approval gates (out-of-band)

For tier ≥ 4, approval must happen on a channel the agent does not control. The most common right-sized patterns:

- **Telegram / Slack / Discord bot button** — agent posts a one-line summary + plan diff, waits for human button click before executing. Tokens for approval are single-use and short-lived (≤ 15 min).
- **Email click-link** — for slower-tempo actions. Click-link must be HMAC-signed and single-use.
- **Manual ticket assignment** — agent files a ticket and stops; human moves it to "approved" and a separate worker picks it up.

Anti-pattern: asking the LLM "are you sure?" in the same conversation. The LLM will say yes.

## Pattern: scope locking

Forbid wildcards and cross-resource actions at the *tool* layer, not the prompt layer.

- ❌ `delete_posts(filter)` → agent might pass `filter={}`
- ✅ `delete_post(id)` — one id per call, plus a per-conversation cap (e.g. ≤ 5 deletions before forcing a checkpoint)

Other variants:
- **Path allowlists** — file-system tools accept only paths under a configured root
- **Domain allowlists** — outbound HTTP tools allow only known hosts
- **Time-bounded sessions** — credentials valid only during the active session, refreshed externally

## Pattern: idempotency

Every state-changing tool should accept (or compute) an idempotency key, and the backend should de-duplicate on it. This survives:
- Agent retries after a tool-result parsing failure
- Network blips that re-run the same call
- Double-clicks on the approval button

Without idempotency, a retry storm can multiply the blast radius without any of the guards firing.

## Pattern: separate read and write agents

Run analysis in a read-only agent with read-only credentials. When an action is decided, hand off to a second, narrowly-scoped write agent with a fresh credential and a single, well-defined task. This:
- Prevents the analyzing agent from acting on injected content it read
- Makes the audit trail clean (decision → action is a hand-off, not a single opaque step)
- Lets you use a cheaper model for read and a stricter one for write

## Pattern: kill switch and rate limit

Every agent must have:
- A **kill switch** the operator can hit without logging into the agent's environment (a feature flag, a DNS record the agent checks, a config file the agent reads on every tool call). It must default to *off* when unreachable.
- A **per-minute and per-hour cap** on write tool calls. The agent is paused — not failed — when the cap is hit, so a human can resume after inspection.
- A **cost cap** for paid-API or money-moving tools. The agent halts when reached. Always.

## Pattern: rollback before forward

For every write tool, before adding it to an agent's toolset, write down: **"to undo this, do X"**. If you cannot, the tool is not safe to expose. Examples:

- File edit → keep a timestamped backup of the original
- DB row update → snapshot row prior in an `audit_undo` table
- DNS change → record the prior record set in a journal
- Deploy → previous artifact is retained for at least 24h and a one-command rollback is documented

## Anti-patterns observed in the wild

These are common failure modes — recognize them before they bite you.

- **"Read this whole site and fix everything"** — too broad; LLM picks confident wrong fixes. Bound the scope per call.
- **Single agent with admin credentials** — gives the LLM more power than any human contractor would normally hold
- **Approval message contains the entire plan** — operator skims, clicks approve. Surface only the diff and the *blast estimate* ("This will modify 47 pages"); make the full plan accessible but secondary.
- **Confirmation in the LLM context** — the LLM cannot meaningfully confirm itself
- **Bulk operations without per-item rate limit** — one bad decision multiplies to N items
- **Logging the agent's reasoning but not its tool calls** — at incident-response time you need the tool calls (with arguments, results, timestamps), not the prose
- **No replay protection on approval tokens** — token leaks into the LLM context → LLM uses it → bypass

## When you cannot add a guardrail

Sometimes a tool genuinely cannot be made safe (irreversible external API, no dry-run, no idempotency). In that case:

- Do not expose it to a general-purpose agent
- Use a narrow CLI script that a human runs intentionally
- If it must be agentic, require an interactive confirmation per call with the *human* — not the LLM — typing the destination identifier as proof

## Quick design checklist

Before shipping an agent that can write anywhere, you should be able to answer yes to all of these:

- [ ] Every write tool is classified by blast radius
- [ ] Every tier ≥ 3 tool has a dry-run mode
- [ ] Every tier ≥ 4 tool has out-of-band approval
- [ ] Every state-changing tool is idempotent
- [ ] There is a kill switch the agent itself cannot disable
- [ ] There is a per-period rate limit on writes
- [ ] There is a cost cap for paid-API tools
- [ ] Tool calls (not just chat) are logged with arguments, results, timestamps
- [ ] Every write has a documented undo procedure
- [ ] Read and write run in separate processes with separate credentials

If any answer is "no", document it and the compensating control. Do not skip the question.

## What this skill will not do

- Recommend disabling guardrails for convenience
- Help build agents that act on systems you do not own
- Endorse a single-agent design that holds high-blast-radius credentials full-time
