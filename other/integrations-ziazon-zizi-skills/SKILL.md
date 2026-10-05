---
name: integrations
description: >
  Use when connecting to or automating a third-party service/SaaS — its REST API,
  an MCP server, OAuth/token auth, webhooks, or a recurring sync (usage/billing/
  expense trackers, data pushes, scheduled updates). Invoke whenever you: build or
  debug an integration, wire a daily/automated job against an external service,
  choose where automation should run (local hook vs cloud vs in-session MCP), make
  external writes idempotent, or scope/research a vendor API before integrating.
  Carries hard-won gotchas (auth-path reality checks, idempotent upserts, secret
  handling) and accumulates per-service quirks. Do NOT use for internal
  service-to-service calls (IPC, guards, endpoint design) — that's
  service-architecture; do NOT use for CI/deploy/launchd plumbing itself — that's
  infrastructure (this skill owns the external-service side of an automation).
---

# Integrations & Automations

Goal: build integrations with external services that are **correct, idempotent, and
run where they actually can** — and accumulate the per-service quirks so the next one
is faster. External writes are outward-facing and often hard to reverse; treat them
with care.

## Workflow

Follow in order — steps 1, 3, and 4 are hard gates, because each one invalidates all
the work built on top of it when skipped.

1. **Read the per-service quirks first.** Check `LEARNINGS.md` beside this skill, when your
   copy keeps one (an index over per-service reference files), for the target service's
   auth model, gotchas, and idempotency approach — most integration pain here has already
   been paid for once.
   Then read the provider's API/MCP surface and mirror existing patterns.
2. **Nail the spec with worked examples** (section below) — especially anything
   computing money/metrics. Gate: don't write compute code while a formula, period,
   denominator, or rounding question is still open.
3. **Prove the auth path you will SHIP with one real call — before building around it.**
   An interactive MCP session ≠ a usable standalone token (section below). Gate: no
   pipeline design until the headless/PAT/service-token path has succeeded against the
   real service once.
4. **Decide where it runs** (section below): deterministic local hook → in-session
   MCP/slash-command → headless/cloud, constrained by where the data AND the auth
   actually live. Gate: don't build unattended automation on an auth/data source that
   only exists in an interactive session.
5. **Build deterministic compute + idempotent write + state file + once-per-period
   guard** (section below).
6. **Dry-run on real data, show the numbers, then write with explicit user OK** for
   anything billable/outward-facing — an external write may be visible to a client the
   moment it lands.
7. **Verify independently:** read the record back through a second channel (e.g. the
   MCP, a GET) — a 200 on the write proves acceptance, not the state you intended
   (sends can queue-then-suppress; edits can partially apply).
8. **Record what you learned** (protocol at the bottom).

## Nail the spec before you build (esp. anything computing money/metrics)

This is the #1 time-saver. For any calculation-driven integration, pin down the **exact
formula, the period/cadence, the denominator, and the edge cases** *before* writing code.

- Use **worked examples on the user's real data** to confirm the model — show the actual
  numbers, not a description. Surprising results ("this seems too high", "starting later
  bills *more*") surface the right model far better than prose.
- Use **AskUserQuestion for genuine forks** (which denominator, which cost basis, which
  rounding/period, what the markup means when it changes). Don't guess on money.
- Expect to **iterate the model**, not just the code. If you've rewritten the compute
  engine 3+ times, the lesson is "clarify the spec earlier," not "code faster."
- Make every assumption a **single editable config knob** (rate, multiplier, tax, start
  date, period), so re-tuning is a one-line change, not a refactor.

## Reality-check the auth path you will SHIP — early (gate)

An authenticated **MCP session ≠ a usable standalone token.** The MCP may work
interactively while the token-based path you intend to automate fails.

- Test the **actual** auth you'll deploy (PAT / service token / headless) against a real
  write **early**, before building everything around it — discovering the token path is
  blocked after the pipeline is built means rebuilding the pipeline.
- **Interactively-authenticated MCP servers may be absent in headless/cron runs** — don't
  design unattended automation that silently depends on an interactive MCP.
- Watch for **org policy blocks**: SSO-enforced accounts can 401 token API calls with a
  policy message even when the token is valid. Read the error text, don't assume "bad
  token" (a worked case: `LOCAL.md` beside this skill, when your copy keeps one — *SSO
  token-block worked case*).

## Run automation where the data and the auth actually are

- If the source data is **local** (e.g. local files/transcripts/DB), the job must run
  locally — a cloud agent can't see it.
- Beware **self-referential cost**: an LLM-driven job that measures usage *consumes* the
  thing it measures. Prefer a **deterministic script** for the compute and reserve the
  LLM/MCP for the one step that needs it.
- Decision order for "run it daily": **deterministic local hook** (zero-token, best) →
  **in-session MCP / slash-command** (when only the MCP auth works) → **headless/cloud**
  (only if data + auth are both reachable there).

## Make external writes idempotent (gate)

Recurring jobs must not create duplicates — a re-run that re-creates is a bug the user
discovers on their invoice/board/inbox, not in your tests.

- Track a **stable target id** in a small local **state file**; re-runs **update** that
  id, they don't re-create.
- Prefer **recompute-from-source each run** (re-derive the whole current value) over
  incremental deltas — it's self-healing and drift-free.
- Add a **once-per-period guard** (e.g. `last_run_date == today → no-op`) so multiple
  triggers in a day don't double-write.
- If the provider offers an idempotency/external key, use it; if not, the state-file id
  is the fallback. Know the provider's **lock semantics** (e.g. records freeze once
  invoiced/finalized) and branch on them — a PATCH against a locked record fails or,
  worse, silently no-ops.
- Append-only surfaces (comments, sends) can't be updated — gate them behind a flag and
  a stated intent, since idempotency-by-update is unavailable.

## Secrets & confidential economics

- Keep tokens **out of the repo** (e.g. a secrets manager or a tool-specific private
  configuration directory); support an **env-var override**. **Never echo secret
  values**; redact them in any `--status`/debug output.
- Pasting a secret into chat persists it in the transcript — prefer the user enters it
  into the config themselves, and recommend a **least-scoped, revocable** token.
- **Any field written to an outward-facing record is client-visible** (a billable
  expense's "notes" can land on the invoice). Keep **internal economics out of it** —
  markup/margin, cost basis, your own rates. Put the full breakdown in a **local log**,
  send a minimal client-safe value (e.g. just a label + date).
- **Beware derivable secrets:** showing the cost basis *and* the share/quantity alongside
  the billed total lets a client back out the markup by division (worse when the
  underlying price is public). Omit the inputs, not just the markup factor.

## Don't let an automation break the host

- A hook/automation must **never** crash the thing that runs it: catch everything,
  **exit 0**, run **detached/async**, log to a file. A failed external call should be a
  logged no-op — the session/host matters more than the sync.

## Close the loop upstream

When the provider's API/MCP forced a workaround (missing field, no idempotency key,
confusing error), **submit feedback** to that provider (most MCPs expose a feedback tool)
framed as a concrete feature request. Future integrations get easier.

## Common failure modes

- **Building the whole pipeline on interactive-MCP auth**, then discovering the headless
  path 401s — step 3 exists to catch this on day one.
- **Blind re-create on every run** (no state file / no period guard) → duplicate
  expenses, double comments, repeated sends.
- **Trusting the write's 200:** a queued send can still be suppressed/undeliverable;
  always read state back (step 7).
- **Leaking economics or secrets into outward-facing fields or logs** — notes, debug
  output, error messages that interpolate a token.
- **Guessing a money formula** instead of confirming with worked examples on real data.
- **An automation that can crash its host** — un-caught errors in a hook, foreground
  blocking, unlogged failures.
- **Assuming the identifier scheme** (email-as-id, key-independent tokens) — verify the
  provider's actual keying before lookups; error text like "invalid key" can point at
  the wrong credential.

## Before you call this done

- [ ] Read the service's LEARNINGS/reference entries before building.
- [ ] Spec confirmed with worked examples; every assumption is a config knob.
- [ ] The SHIPPED auth path proven with a real call (not just the MCP session).
- [ ] Writes are idempotent: state file + once-per-period guard + lock-semantics handling.
- [ ] No secret or internal economics in any outward-facing field, log, or transcript.
- [ ] Dry-run shown; outward/billable writes made only with explicit user OK.
- [ ] Result verified through a second channel (read-back), not just the write's response.
- [ ] New quirks recorded per the protocol below.

## Related skills

- [security-and-hardening](../security-and-hardening/SKILL.md): a new integration or inbound webhook is a security trigger path; secrets handling follows that skill.

## Capturing learnings (session-handoff protocol)

Accumulate per-service quirks, auth notes, and reusable patterns in `LEARNINGS.md` beside
this skill, when your copy keeps one (an index over per-service/theme reference files). On
handoff / "update skills" / after integration work: record the service, its auth model, gotchas,
idempotency approach, and any feedback submitted — append under a new `##` section in the
most relevant reference file (not the index). Dedupe/merge, tag by service. **Read it
before starting work on that service.**
