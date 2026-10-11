---
name: pressure-test
description: "Pressure-test an approach or decision against scalability, long-term cost, and efficiency, then recommend one option decisively. Use when the user says \"pressure-test this\", \"stress-test the plan\", or asks whether the current approach is the right one before committing to it."
---

# Pressure Test

Run the decision test on the approach the user named — or, if they named none, on the approach currently on the table in this conversation.

The governing question for the choice: **whatever is scalable, long term, and cannot be done in a more efficient way.**

**Ground it first — don't judge from priors.** A prior isn't only stale training data — it's also a conclusion you minted *this* session from neighboring code. The second kind is more dangerous: it feels freshly earned, so it rides on the credibility of everything else you verified. Verify before ruling.

- For this **infra/tech decision**, research how established services and competitors solved the same problem — engineering blogs, postmortems, talks, and case studies are fair game here. Prior art is signal.
- Verify any **fact** you lean on — an API, a limit, a price, current behavior — against a primary source (official docs, the actual source code), not a remembered version or a random blog. When a docs-retrieval tool is available — Context7, a `find-docs` skill, an MCP docs server — use it to pull the latest docs instead of recalling them.
- **Sweep the whole repo for the symptom before you hypothesise where it lives.** Before deciding *which* subsystem owns the problem, grep/semantic-search the entire codebase for the reported symptom itself — the user's literal words, the error string, the observable behaviour (e.g. every place that can emit "not available / not ready / refused", every `status`/guard early-return on this entity). Enumerate *all* the sites that could produce it across *every* layer, with no assumption about which one is at fault, then rule per site. Anchoring on the subsystem you happen to have been working in is the most common way a careful, well-grounded ruling lands on the wrong code — and the volume of grounding you did there makes the wrong-subsystem conclusion *feel* solid. Narrow to the load-bearing claim only after the sweep.
- Read the actual code and architecture this touches before ruling — locally correct but architecturally wrong is still wrong. That means the exact file the change runs through, not only its neighbors — reading everything *around* the target and inferring the target by analogy is the most seductive way to skip this.
- **Ground per claim, not per session.** Verifying four neighboring things doesn't transfer to the one load-bearing claim. The volume of grounding you've done makes the unverified claim *feel* as solid as the rest — it isn't. Isolate the single claim the ruling rests on and verify *that* one directly: "the thing this touches is built like its neighbors" is not evidence about the thing it touches.
- **Do the cheapest decisive check yourself — don't defer it.** If one file (a `wrangler.jsonc`, an entrypoint, a config) would settle the load-bearing claim, open it. Ending your turn by asking the human to confirm what a file you could have read answers is the same deferral repeating one turn later.
- **Look down the stack, not just sideways.** Before designing any new state — config keys, DB columns, env vars, endpoints, files — search the framework / platform / library you build on (and the rest of this repo) for a native primitive that already models this concern. The leanest correct option is frequently one that already exists one layer down; reinventing what the host exposes is the most common efficiency miss. Verify it against the dependency's actual source, not its docs alone.
- **But don't optimize away the domain object.** "Reuse the primitive one layer down" is a virtue *until it deletes the thing the feature is actually about*. The trap: fusing a **property the feature requires** (email-binding, single-use, consent) with an **implementation that happens to carry it** (a Supabase magic link, an auth token, a signed URL) — once fused, reuse looks automatically correct, and you end up borrowing an *ephemeral auth artifact* to stand in for a *durable domain record*. Separate the two: name the property, then ask whether the primitive models the property or merely coincides with it today. An auth link is not an invitation; a cache key is not a job; a session is not an audit trail. When the feature needs a **lifecycle** — revoke, resend, expire independently, run several concurrently, record who accepted and when, ask consent before acting — that lifecycle *is* the domain object, and a first-class record (a row + a `requested → active / declined` status) is the correct construct, not gold-plating. Reuse that has no place to hang those states pushes the real cost into fragile edges (24h expiry, single-use collisions, "already registered", silent auto-accept). Adding well-chosen, durable state is sometimes the *efficient* move, not the wasteful one.
- **A reused state inherits every behavior already attached to it — enumerate them before you adopt it.** The bullet above warns against reuse that *deletes* the domain object; this is its mirror — reuse that silently *inherits* one. When the approach repurposes an existing status / flag / enum / column to mean something new (`trialing` to mean "currency-migration bridge", `pending` to mean "awaiting review", `archived` to mean "soft-deleted"), it doesn't just carry the one property you wanted — it fires *everything* that already reads that value: webhooks, cron jobs, entitlement gates, billing/credit grants, UI branches, cleanup sweeps. Before committing, **grep every consumer of that value** (`grep -rn 'trialing\|is_trial'` across every layer) and list what each one does with it; a behavior you never intended rides along for free. The tell that you skipped this: you validated the *one* behavior you wanted and discovered the others reactively — one bug (or one "wait, why did all of them get free credits?") at a time. The reused state's full behavior set is part of the decision, not a surprise you pay for after. And when you *do* adopt it, verify by diffing the **whole system's response** (side-effect tables, ledgers, related rows) before/after — not just the fields you predicted would change; the inherited behavior only shows up in the diff you didn't expect.

**Define the three pillars for *this* decision — if they're not already clear.** Before judging, make each concrete for the case at hand:

- what actually grows (what "scalable" means here — the load / data / users / surface that increases),
- the horizon that matters (a throwaway, or the load-bearing path you'll live with for months?),
- what efficiency is measured in (and what it would be traded against).

Pillars you can't name, you can't judge against — so name them first.

Then judge the approach against the **three pillars** — name specifics, not abstractions:

- **Scalable** — does it hold at 100× the load / data / users / surface area? Name the first thing that breaks.
- **Long term** — six months from now, is this a foundation or a wound? What does it cost to live with, or to undo?
- **Efficient** — is this the leanest *correct* way? The leanest option is often **reusing an existing primitive** (host platform, upstream dependency, or elsewhere in this repo) rather than any new construct you write — so confirm none exists before designing one. Then: fewer moving parts, less code, less to maintain. But measure efficiency **over the feature's whole life, not the size of today's diff.** A new column, status, or endpoint is a *cost to price*, not a *cost to avoid* — if it's the object the feature is about, it's the efficient choice, and calling durable domain-appropriate state a "wound" while treating reuse of an ephemeral primitive as free is the tell that you've optimized for implementer convenience instead. The count of migrations you didn't write is not the metric; revoke / resend / audit / consent over months is. "More efficient" never means removing a safety guard — and never means deleting the domain model to save a table.

**Plus any pillars this project adds.** The three above always stand; if the company/codebase has its own vision pillars (e.g. Portability, Privacy, Offline-first), find them in its `AGENTS.md` / `CLAUDE.md` / vision docs and judge against those too — they extend the three, never replace them.

Then:

- **Be decisive.** Recommend ONE option. Don't survey alternatives you won't take.
- **Catch stale time-budget shortcuts.** "No time", "do it later", "quick hack for now" — in an AI session the proper version usually fits *this* session. If you catch yourself reaching for a shortcut, flag it and price the real version.
- **Never trade away** correctness, security, or data-safety for speed.
- If the approach passes all three, say so plainly and proceed — don't manufacture objections.
- If it fails, state the better approach concretely and exactly what changes to get there.
- If the proper version genuinely would take days, say so explicitly and let the user decide — don't silently downgrade to the shortcut.
