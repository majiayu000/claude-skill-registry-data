---
name: migrating-persona-to-relayflow
description: "Use when migrating an existing `defineAgent` persona (in AgentWorkforce/agents or AgentWorkforce/internal-agents) to run its LLM-heavy work through a Relayflow v1 workflow via `ctx.workflow.run()`. Covers scope decisions (what to extract, what to leave in the handler), the 4-step durable-workflow shape, materialization through the current 4-file cloud deploy surface, red-first testing with resume proof, `useSubscription: true` semantics for realtime triggers, the `agentworkforce >= 4.1.44` CI-deploy bump requirement, and evidence capture. Applies to schedule-driven, realtime-trigger-driven, and hybrid personas. Reference migration: `hn-monitor` PR #126."
---

# Migrating a persona to Relayflow v1

> **v1 engine.** This skill targets the superseded `@relayflows/core` engine via
> `ctx.workflow.run()`. The current engine is **v2** — `@relayflows/surface` /
> `@relayflows/sdk`, CLI `flows` — documented in
> [`writing-relayflows`](../writing-relayflows/SKILL.md). Use this skill only to move an
> existing persona onto v1's durable execution today.

## When to use this skill

You are working on a persona in `AgentWorkforce/agents` or `AgentWorkforce/internal-agents` that today does its work inline in a `defineAgent({ handler })` — LLM calls via `ctx.llm(...)`, ranking, curation, review — and you want to move the LLM-heavy portion behind a durable Relayflow v1 workflow via `ctx.workflow.run()` so that the work is exactly-once resumable, journaled, and step-level retriable.

Read the RFC first: [`docs/RFC-0001-everything-is-a-relayflow.md`](https://github.com/AgentWorkforce/flows/blob/main/docs/RFC-0001-everything-is-a-relayflow.md). This skill is the practical recipe; the RFC is why.

**Reference migration to imitate:** `hn-monitor` — [`agents#126`](https://github.com/AgentWorkforce/agents/pull/126), evidence at [`hn-monitor/evidence/2026-09-03-relayflow-v1.md`](https://github.com/AgentWorkforce/agents/blob/main/hn-monitor/evidence/2026-09-03-relayflow-v1.md).

## Do not use this skill for

- **Authoring a v1 workflow from scratch** — use [`writing-agent-relay-workflows`](../writing-agent-relay-workflows/SKILL.md).
- **Authoring for the v2 engine** — v2 (`@relayflows/surface`/`@relayflows/sdk`, CLI `flows`, packages `2.0.x`) is a different product that ships today; see [`writing-relayflows`](../writing-relayflows/SKILL.md). This skill and `writing-agent-relay-workflows` cover the superseded **v1** engine. Personas still migrate to v1 first: v2 becomes an opt-in `relayflowVersion: "v2"` flip on the same `ctx.workflow.run()` call once the persona runtime supports it.
- **Repointing a workflow between packages** (`@agent-relay/sdk/workflows` → `@relayflows/core`) — that is covered in `writing-agent-relay-workflows`.

## The seven-step recipe

### 1. Scope decision — what to extract, what to leave

Do not migrate the whole handler. Migrate only the **LLM-heavy curation** — the part that benefits from durability + resume:

- **Extract to workflow:** scoring / ranking / summarizing / review / repair / validation — anything that consumes tokens and would be expensive to redo on crash.
- **Leave in persona handler:** trigger routing, fetches (HN, RSS, provider reads), dedupe / seen-checks, delivery (Slack/Telegram/DM posts), Q&A on inbound mentions.

The persona surface (schedule, triggers, integrations, exact-state semantics) **does not change**. Only the curation step moves.

**Test:** if you remove the workflow file, the persona should still fetch, dedupe, and refuse to publish. That is the invariant.

### 2. Design the 4 static durable steps

Every migrated workflow uses **four static durable steps with stable identities**. Stability matters because resume keys on step ID.

Canonical HN-shape:

| Step ID | Purpose |
|---|---|
| `prepare-input` | Normalize + validate the batch payload the persona hands in |
| `analyze-*` | The primary LLM pass (analyze stories / classify tickets / summarize threads) |
| `review-*` | A second LLM pass that judges the first (score, catch hallucinations, redact) |
| `validate-*` | Deterministic final gate — asserts exact batch key, output bounds, required fields |

Names can vary by domain (`analyze-batch/review-batch/repair-batch/validate-batch`, `analyze-stories/review-digest/validate-digest`, etc.) but **the four-step shape is fixed** and each step ID must be stable across runs so resume matches.

### 3. Colocate the workflow with its persona

Put the workflow source under the persona's directory, not a top-level `workflows/` sibling:

```
hn-monitor/
  agent.ts              # defineAgent, handler
  persona.ts            # persona spec
  workflows/
    scheduled-digest.ts # the v1 workflow — export a `workflow` builder
```

**Why not top-level `workflows/`:** it separates the workflow from the persona that owns it, adds import indirection, and makes the persona directory an incomplete unit. Colocate. When the cloud deploy surface eventually accepts multi-file workflow bundles, this is the shape it will accept.

**Interim note (as of 2026-09-03):** the current cloud deploy surface still takes 4 files per persona. That means workflows-with-imports need to be materialized as a single self-contained file at runtime via `ctx.files.write(target, source)`. The colocated `workflows/scheduled-digest.ts` becomes the *source-of-truth*; a small shim in `agent.ts` writes it out before `ctx.workflow.run()`. Track [cloud issue](https://github.com/AgentWorkforce/cloud/issues) for the surface fix that lets you drop the shim.

### 4. Persona handler invokes via `ctx.workflow.run()`

The schedule / trigger path in `agent.ts` does its fetch + dedupe + provisional claim, then calls the workflow, then delivers on success:

```ts
export default defineAgent({
  schedules: [{ name: 'scan', cron: '0 9,17 * * *', tz: 'America/New_York' }],
  triggers: { /* unchanged */ },

  handler: async (ctx, event) => {
    if (isCron(event)) {
      const batch = await fetchAndClaim(ctx);
      if (!batch.stories.length) return;

      const workflowInput = deriveStableInput(batch);          // sorted, unique IDs
      const runId = deriveStableRunId(SCHEDULED_DIGEST_VERSION, workflowInput);

      const result = await ctx.workflow.run({
        name: SCHEDULED_DIGEST_WORKFLOW_NAME,
        runId,                                                  // idempotent
        input: workflowInput,
        relayflowVersion: 'v1',                                 // explicit — see step 7
      });

      if (!result.ok) {
        await releaseClaim(ctx, batch);
        return;
      }

      await deliverToProviders(ctx, result.output);             // Slack, Telegram, etc.
      return;
    }
    // Q&A path: unchanged — mentions, DMs, thread replies
  },
});
```

Rules:

- **Derive `runId` from the input**, not the wall clock. Two ticks that see the same stories must produce the same `runId` so the second is a memoized no-op.
- **Release the provisional claim on failed completion** *before* any provider post. Otherwise a partial failure re-runs and posts the same digest twice.
- **Pin one retry with fail exhaustion.** Do not retry forever inside the persona; let the durable workflow's step-level retries handle it.

### 5. Red-first tests

Before you write the fix, write the failing assertion that the scheduled path enters the workflow:

```ts
test('defineAgent scan schedule invokes the durable Relayflow v1 digest before publishing', async () => {
  const workflow = mockWorkflow();
  const provider = mockProvider();
  await runScheduledScan({ ctx, workflow, provider });
  expect(workflow.run).toHaveBeenCalledWith({
    name: SCHEDULED_DIGEST_WORKFLOW_NAME,
    input: expect.any(Object),
    relayflowVersion: 'v1',
  });
  expect(provider.post).not.toHaveBeenCalledBefore(workflow.run);
});
```

Run it. Confirm it fails. Then implement the migration. Rerun. Confirm it passes.

**Also add a resume test:**

```ts
test('pinned Relayflow v1 resumes a failed run without replaying completed HN step identities', async () => {
  const fixture = pinnedFixture({ failAt: 'analyze-stories' });
  const first = await runWorkflow(fixture);
  expect(first.status).toBe('failed');
  const resumed = await runWorkflow({ ...fixture, resumeRunId: first.runId, failAt: null });
  expect(resumed.status).toBe('completed');
  expect(resumed.replayedSteps).toEqual([]);                    // prepare-input was memoized
  expect(resumed.executedSteps).toEqual(['analyze-stories', 'review-digest', 'validate-digest']);
});
```

The resume test is what proves you have durability, not just orchestration.

### 6. Keep `useSubscription: true` if the persona has realtime triggers

Do **not** drop `useSubscription: true` as part of the migration. It is standing consent for realtime triggers (`message.created`, `reaction.added`, `app_mention`); without it, mention Q&A never fires. Runtime 4.x only registers a realtime-trigger subscription when the persona declares it. See internal-agents commit [`9144c8ee00`](https://github.com/AgentWorkforce/internal-agents/commit/9144c8ee00).

**Only remove it if:**

- The persona has no realtime triggers (schedule-only), *and*
- You are chasing the "anthropic credentials are not connected" error on CI deploy.

If you are chasing that CI error, **the real fix is not removing `useSubscription`.** Read step 7.

### 7. Bump `agentworkforce` to ≥ 4.1.44 before CI-deploying

The `agentworkforce` 4.1.43 (and earlier) CLI has a credential-probe bug: it probes for harness credentials by calling `GET /api/v1/cloud-agents` using the user's stored CLI login on disk (`~/.agentworkforce/relay/workspaces.json`). Headless CI has no such login — it authenticates with `WORKFORCE_WORKSPACE_TOKEN`. Without the local login, the probe returns "could not check," which the old CLI reports as **"credentials not connected"** — misleading, because the creds are connected in the workspace.

**Fix:** bump `agentworkforce` (and every `@agentworkforce/*` peer package) to `4.1.44` or later. `4.1.44` makes the probe tri-state and lets cloud be the authority. Reference: internal-agents commit [`d606bc4f65`](https://github.com/AgentWorkforce/internal-agents/commit/d606bc4f65).

```json
// package.json
{
  "dependencies": {
    "@agentworkforce/compose": "4.1.52",
    "@agentworkforce/delivery": "4.1.52",
    "@agentworkforce/persona-kit": "4.1.52",
    "@agentworkforce/runtime": "4.1.52",
    "agentworkforce": "4.1.52"
  }
}
```

Regenerate `package-lock.json` (`npm install --package-lock-only`) — the deploy uses `npm ci` and rejects mismatches.

**If you can't wait for a lockfile regen**, deploy locally: `agentworkforce deploy ./<persona>/persona.ts --on-exists update --input KEY=VALUE`. Your local CLI login handles the probe without hitting the bug.

## Evidence you must capture

Per [`AGENTS.md`](https://github.com/AgentWorkforce/flows/blob/main/AGENTS.md) — "evidence is captured, not narrated." In the PR body, paste literal command output for each of:

1. **Red test failure** — the assertion above, failing with the pre-migration handler.
2. **All tests green** — post-migration count matches expectation; no regressions in unrelated tests.
3. **Mutation verification** — pick a key assertion (e.g. `model: 'claude-haiku-4-5-20251001'` in the workflow); revert the source line, rerun, confirm the assertion fails; restore byte-for-byte, rerun, confirm it passes. Paste both.
4. **Resume test green** — the durability assertion above.
5. **Cloud deploy dry-run** — `agentworkforce deploy ./<persona>/persona.ts --dry-run` exits 0.
6. **Live deploy or invoke** — either a successful CI deploy run, or a local `agentworkforce deploy` followed by a manual trigger of the deployed persona and confirmation the digest posted to its target channel.

## Common pitfalls

- **Dropping `useSubscription: true` to escape the CI credential error** — fixes the wrong problem; breaks all mention Q&A. See step 7.
- **Top-level `workflows/` directory** — separates the workflow from its persona; use `<persona>/workflows/` instead.
- **Deriving `runId` from `Date.now()`** — makes memoization useless; every tick becomes a fresh run.
- **Delivering before workflow success** — the whole point of migration is that a failed workflow releases its slot; if you deliver on partial completion, dedupe fails on retry.
- **`--no-verify` on the deploy commit** — the hooks catch real issues; investigate rather than bypass.
- **Skipping the resume test** — orchestration passes without it; durability doesn't.

## Post-migration checklist

- [ ] Persona surface (schedules, triggers, integrations, `useSubscription`) unchanged
- [ ] Workflow file colocated under `<persona>/workflows/`
- [ ] Persona handler calls `ctx.workflow.run({ relayflowVersion: 'v1', runId, input })`
- [ ] `runId` derived from input, not clock
- [ ] Provisional claim released on failed workflow completion before any provider post
- [ ] Red-first test present and green post-migration
- [ ] Resume test present and green
- [ ] Mutation-verified evidence in PR body
- [ ] `agentworkforce` bumped to ≥ 4.1.44 (only if CI-deploying)
- [ ] Live deploy or invoke evidence captured
- [ ] `SCHEDULED_<PERSONA>_VERSION` constant declared as the future v2 migration seam
