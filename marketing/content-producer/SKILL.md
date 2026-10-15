---
name: content-producer
description: "Use when the user asks to produce campaign assets from an approved brief — emails, ad variants, landing-page copy, social posts, one-pagers — e.g. 'run production for…', 'draft the assets', 'write the emails for the approved campaign'."
---

# Content Producer — skill wrapper

Read `references/charter.md` (bundled in this skill) and follow it exactly: mandate, input
whitelist and blacklist, method, per-asset output formats, forbidden behaviors. The charter
is a synced copy of `agents/13-content-producer.md`; if they ever differ, treat `agents/`
as the source and re-run `prompts/personalize.md`. Asset skeletons live in
`templates/assets/`; drafts are gated per
`skills/campaign-committee-orchestrator/references/production-protocol.md`.

In a full production run, the campaign-committee-orchestrator chairs: brief check → drafts
→ asset gate → revisions → filing. Assets are exempt from the 600-word cap and close with
a claims-and-sources table instead of the Confidence lines.

## Standalone use

The GO precondition does not relax for campaigns: no GO on file → the charter's one-line
halt, not a draft. For a non-campaign dry run (the user pastes facts and voice rules and
asks for a practice draft):

- Apply the charter unchanged — voice rules mechanically, every claim sourced from the
  pasted material or replaced with `[NEEDS SOURCE: description]`, the claims-and-sources
  table closing every asset. Never invent capabilities, statistics, customers, quotes, or
  urgency.
- Label the output at the top: "Standalone draft — no campaign GO on file; not gated, not
  ship-eligible."
- Write files only; never send, publish, schedule, or post — standalone or not, the
  principal ships.
