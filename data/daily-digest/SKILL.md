---
name: daily-digest
description: Use when authoring or extending the digest set in a relayfile workspace - covers the contract for files under `<mount>/digests/` (`yesterday.md`, `today.md`, `this-week.md`, date-stamped daily files), the per-provider section format, link conventions back into the canonical mount tree, when digests are regenerated, and how adapter authors expose new provider data to the digest pipeline. NOT for agents answering activity questions — those should use the `activity-summary` skill to consume digests, not produce them.
---

# Daily Digest — Authoring Contract

## Overview

`<mount>/digests/` is a relayfile-managed directory containing deterministic, pre-computed Markdown summaries of provider activity over fixed time windows. Digests are the cheap entry point for activity-summary queries (see the `activity-summary` skill). This skill is for **producers** — adapter authors, provider integrators, and anyone extending what shows up in a digest.

## When to use this skill

- You are writing a new relayfile adapter (Notion, Linear, …) and need to wire it into the digest pipeline.
- You want a new digest window (e.g. `last-30-days.md`) and need to know the contract.
- A digest is missing a provider's content and you need to know why.
- You need to debug why `yesterday.md` was empty or stale this morning.

If you're an agent **reading** the digest to answer a user question, switch to the `activity-summary` skill instead.

## Digest file taxonomy

| File | Window | Mutability |
|---|---|---|
| `today.md` | 00:00 local → now | Updated on every change-event for the current day |
| `yesterday.md` | full prior calendar day | Generated at 00:00 local, immutable for the rest of the day |
| `YYYY-MM-DD.md` | that calendar day | Immutable once the day closes |
| `this-week.md` | Mon 00:00 → now (ISO week) | Updated on every change-event |
| `last-week.md` | full prior ISO week | Immutable |

A digest file is **always present** for each window even if the window contains no activity (the body says `_no activity_`). Agents can detect empty windows without retrying.

## File header

Every digest starts with a frontmatter-style header that callers can verify before trusting the body:

```markdown
# Activity for 2026-05-12

> window: 2026-05-12T00:00:00-07:00 → 2026-05-13T00:00:00-07:00
> generated: 2026-05-13T00:01:14Z
> providers: linear, github, notion, slack
> events: 47
```

- `window` is the half-open interval in the workspace's configured timezone.
- `providers` lists every adapter that contributed (or attempted to). A missing provider here means the adapter never ran, not that it had zero activity.
- `events` is the raw change-event count over the window — useful for sanity-checking against the body.

## Per-provider section format

Each provider gets exactly one `## <provider>` section, in alphabetical order. Bullets within a section are sorted by event time, ascending. Each bullet must:

1. Start with the canonical record identifier the provider uses (`AGE-16`, `#412`, page title, etc.).
2. Describe the change in past tense — "moved to Blocked", "merged to main", "edited".
3. End with a Markdown link to the canonical file path in the mount, in square brackets.

```markdown
## linear
- AGE-16 moved to Blocked (waiting on design) — [/linear/issues/AGE-16__87389837-62b1-4e1a-a237-59218bab2974.json]
- AGE-9 closed — [/linear/issues/AGE-9__2bb2c00f-ee93-4c73-a793-df5b725d9a1a.json]
```

The link target is what makes the digest interactive — a follow-up "tell me more about AGE-16" is one `cat` away from the digest line.

## Adapter contract

For an adapter to contribute to digests it must export a `digest()` function in addition to its sync/writeback handlers:

```typescript
import type { DigestContext, DigestSection } from '@relayfile/adapter-sdk';

export async function digest(ctx: DigestContext): Promise<DigestSection | null> {
  const events = await ctx.changeEvents({
    window: ctx.window,        // { from: ISO8601, to: ISO8601 }
    providers: [ctx.provider],
  });

  if (events.length === 0) return null;

  return {
    provider: ctx.provider,
    bullets: events.map((e) => ({
      text: renderBullet(e),
      canonicalPath: e.resource.path,
    })),
  };
}
```

Returning `null` is correct for "ran successfully, no activity"; throwing is reserved for "could not produce a digest" and surfaces as a warning in the digest header.

## Regeneration

- **Rolling windows** (`today.md`, `this-week.md`) are regenerated on every change event for the current window, coalesced to a max of one rebuild per 30 seconds.
- **Closing windows** (`yesterday.md`, `YYYY-MM-DD.md`, `last-week.md`) are produced once at window close (00:00 local for daily, Monday 00:00 for weekly) and never modified afterward. This is what makes them safe to cache and quote verbatim.
- If you need to force a rebuild (e.g. after fixing an adapter bug), `relayfile digest rebuild --window yesterday` re-derives from the change log.

## Common mistakes when adding a new digest

- **Don't inline raw provider payloads.** Bullets are one line. Anything larger belongs in the canonical file the bullet links to.
- **Don't summarize across providers in one section.** Cross-provider correlation is the agent's job; the digest's job is exhaustive per-provider listing.
- **Don't omit the canonical link.** A digest line without a link is dead weight — the agent can't follow up without re-deriving the path.
- **Don't generate non-deterministic content.** Two runs over the same change-event window must produce byte-identical output. LLM-generated prose belongs in the agent, not the digest.
