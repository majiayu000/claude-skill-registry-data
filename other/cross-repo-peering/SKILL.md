---
name: cross-repo-peering
description: How agents pick the right cross-repo interaction mode (advisory call / spec-out call / async handoff / convention import) and compose well-shaped peer-call prompts. Load when a session touches a sibling Hero workspace's surface.
compatibility: opencode
metadata:
  audience: agents
  purpose: cross-repo-coordination
---

## What I do

Teach agents how to use Hero's cross-repo peering protocol — the three-tier ladder (advisory peer call, spec-out peer call, async handoff) plus the convention-import fallback — so work that crosses a sibling workspace's surface gets the protocol's provenance for free.

The full protocol convention lives at `.hero/knowledge/conventions/peering-protocol.md`. Read it once for depth. This skill is the agent-facing operational distillation.

## When to use me

Load me when any of these are true:

- The user names a sibling repo by alias ("ask hero-code", "hand off to hero-cloud").
- The user describes a question whose answer lives in a sibling's surface ("what's their error envelope?", "does this break X?").
- The active spec touches files whose contract is owned by a sibling (see `hero context` for contract-import surfacing).
- The work being asked for is genuinely a sibling's responsibility and the user hasn't called it out yet.

Don't load me for purely local work, even if a sibling repo exists in the workspace's `repos` config.

## The three-tier ladder

Pick the **least invasive mode that resolves the work**. Don't escalate when an advisory call would suffice; don't drop to convention import when a handoff would close the loop.

| Mode | Writes? | Pick when |
|---|---|---|
| **Sync peer call: advisory** | Nothing | You need a fact — "what's X's shape?", "is there already an endpoint for this?", "does this break you?". Peer investigates, returns findings text, writes nothing on its side. |
| **Sync peer call: spec-out** | Spec on peer | You realized the work is genuinely the peer's — its conventions should kick in. Peer's Hero designs the spec natively on its side and returns the slug; your local spec moves to `awaiting_peer`. |
| **Async handoff** | Spec on peer (scaffolded) | You already did the investigation; the fix clearly belongs to the peer and you want it on their queue. Your local spec moves to `handed_off`; theirs lands as `planning` with `received_from:` provenance. |
| **Convention import (fallback)** | Nothing | Work legitimately stays in your workspace but must respect the peer's surface (e.g. a serializer producing a payload they parse). Pull the peer's peer-surface conventions into context. |

Full-delivery peer call (peer designs AND delivers) is v2. Not available.

## Decision tree

```
Does the user already know the answer is on the peer's side?
├─ Yes, and they did the investigation → ASYNC HANDOFF
├─ Yes, but they want peer's conventions to shape the design → SPEC-OUT
└─ No, they need to learn something first → ADVISORY

Then ask: does the work itself stay on our side once we know the answer?
├─ Yes, but it crosses peer's surface → CONVENTION IMPORT (after advisory)
└─ No, it should move → ESCALATE to spec-out or handoff
```

When the user's intent is genuinely ambiguous between two modes, **ask one focused clarifying question** rather than guessing. Example: "Want hero-cloud to design the migration, or just a quick read on whether this breaks their schema?"

## Composing a good peer-call prompt

A peer call spawns a subagent in the peer's workspace with its full Hero context loaded. Treat it like sending a colleague a focused brief — not paraphrasing the user verbatim.

### Required elements

- **The specific question or task** — name the artifact, the field, the constraint. Bad: "what about the error format?" Good: "What's the current shape of the `errors` array in the `/v1/order` POST response? Any deprecations in flight?"
- **The reason** (`--reason "..."`) — what's happening on your side that prompted the call. Helps the peer subagent triage urgency and rank against in-flight work.
- **The related spec** (`--related-spec <slug>`) — when there's an active spec driving the call, attach it. The peer's trail and your local handoff record link to it; cross-repo `hero why` can walk the chain later.

### Mode flags

- `--mode=advisory` — read-only investigation. Default budget: 20 turns / 50,000 tokens. Use `--budget-turns` / `--budget-tokens` to override.
- `--mode=spec-out` — peer designs a spec. Default budget: 50 turns / 150,000 tokens.

### Prompt shape — advisory mode

```bash
hero peer call <alias> --mode=advisory \
  --related-spec <active-slug> \
  --reason "Why this call is happening on our side" \
  "Specific question. Concrete. Mention the file/symbol/field you care about."
```

### Prompt shape — spec-out mode

```bash
hero peer call <alias> --mode=spec-out \
  --related-spec <active-slug> \
  --reason "Why peer should design this rather than us" \
  "Design the [thing]. Constraints: <list>. Out of scope: <list>. Acceptance shape: <list>."
```

The peer's `/design` flow runs on this prompt. Treat it like a `/design` kickoff brief — clearer the better.

## Anti-patterns

Don't:

- **Paraphrase the user's words verbatim** as the peer-call prompt. The peer's subagent needs a structured question, not a chat fragment. Translate intent into a specific brief.
- **Make a peer call when the answer is in your own workspace.** Check `hero search` and `hero relevant` first. Peer calls cost a subagent spawn.
- **Skip `--related-spec` when one exists.** The trail breaks; cross-repo `hero why` can't walk the chain.
- **Use spec-out when advisory would resolve it.** Spec-out writes a spec on the peer's side; advisory writes nothing. Escalate only when the work genuinely belongs to the peer.
- **Use handoff to dump unfinished investigation on the peer.** Handoff is for *completed* investigations where the fix clearly belongs to the peer. If you haven't found the cause yet, do advisory first.
- **Run multiple peer calls when one would do.** Bundle questions in a single advisory call when they're related.
- **Wait synchronously on a handoff** — handoff is async by design. Your local spec moves to `handed_off`; you continue other work. The status auto-flips to `handed_back` when peer completes.

## Async handoff — when and how

Use handoff when:

- You've diagnosed the root cause and it's on the peer's side.
- The peer should own the fix end-to-end (their conventions, their PR, their merge).
- You can scope the handoff well enough to scaffold a useful spec on their side.

```bash
hero handoff <local-slug> <peer-alias> \
  --reason "Symptom in our workspace, root cause in peer's surface" \
  --type bug
```

Your local spec moves through these states:

| Status | Meaning |
|---|---|
| `handed_off` | Just dropped on peer's queue. Receiver scaffold landed; trail entry written. |
| `awaiting_peer` | Peer's spec is `delivering`. |
| `handed_back` | Peer's spec is `completed`. Verify the symptom is gone on your side. |

When the peer completes, status auto-flips on next `hero status` run. To pick up:

```bash
hero handoff accept <slug>
```

Then verify the original symptom resolved before marking your spec done.

## Convention import — the fallback

Use when the work legitimately stays on your side but must respect a peer's surface. Example: a JSON serializer in your workspace producing a payload the peer parses; you can't escape knowing their schema.

```bash
hero relevant --peer <alias> --surface http-response
```

Pulls the peer's peer-surface conventions matching the surface tag into your active context. Less powerful than a peer call (no investigation, no new info), but free.

## Discovery commands

| Need | Command |
|---|---|
| Which peers are configured here? | `hero peer list` |
| What's reachable? Manifests current? | `hero peer list` (output includes status) |
| What does one peer expose? | `hero peer show <alias>` |
| What's in flight across the boundary? | `hero handoff status` |

If `hero peer list` returns empty, peers aren't registered yet. Run `hero admin repos add <alias> <path>` first (see `CROSS-REPO-PEERING.md`).

## Output discipline

After a peer call returns, **summarize the findings for the user before acting on them**. The peer's response is a structured block; the user wants the headline plus the actionable shape, not the raw envelope. Quote relevant excerpts in your reply; don't dump the full peer response unless asked.

After a handoff, **confirm the trail wrote** (`hero handoff status` shows the entry) and tell the user the peer-side slug + which side now owns the next move. Don't pretend the handoff is the work — it's the start of work happening elsewhere.

## Related

- Convention: `.hero/knowledge/conventions/peering-protocol.md` — the full protocol with edge cases and v2 directions.
- Decision: `.hero/knowledge/decisions/cross-repo-peering-local-first.md` — why local-first by default.
- Setup guide: `CROSS-REPO-PEERING.md` (workspace root) — one-time registration and config.
- Slash command: `/peer` — structured front door for peer call / handoff / list / show.
