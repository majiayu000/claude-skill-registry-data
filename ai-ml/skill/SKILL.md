---
name: api-bill
description: Use when the owner asks what their Claude Code use would cost on the API, wants an API shadow bill or cost card for a time frame, or types /api-bill (with a time frame such as 24h, 7d, 30d, 6m or all). Prices every reply in this PC's session logs at Anthropic's live per-model list prices and shows the result as a card on a private claude.ai link.
---

# API shadow bill

`$BILL` below is `python "$HOME/.claude/skills/api-bill/scripts/apibill.py"`.

1. Take the time frame from the request: `24h`, `7d`, `2w`, `30d`, `6m`, `1y` or
   `all`. Default `30d`.
2. Run `$BILL <timeframe>`. It fetches the live pricing page, reads every Claude
   Code log on this PC (subagents included), prices each reply at the rate of the
   model that wrote it, and writes the card to `~/api-bill/`.
   - Never edit the price list or guess a rate. A model with no list price is left
     out and named as unpriced; say so.
3. Publish the card as a private Artifact, the same link every run:
   - Read `artifact_url` from `~/api-bill/config.json`.
   - If it is set: `Artifact` with `action: "read"` on that url, then publish with
     `url` set to it and `file_path` set to the card path the script printed.
   - If it is not set: publish the card with `icon: "chart"` and no `url`, then
     save the returned link as `artifact_url` in `~/api-bill/config.json`, keeping
     the other keys.
   - Never share it or make it public: it holds project names and usage.
   - If the Artifact tool is not available in this session, give the local card
     path instead and offer to open it (`$BILL <timeframe> --open`).
4. Reply with the script's first line (the API cost), the per-model split, any
   unpriced models, a stale-price warning if the script printed one, the "Includes an
   estimate" or "No estimate" line if there is one, and the link.

Claude Code deletes session logs after its cleanup period (30 days by default), so
for longer time frames the days before the oldest kept log come from the running
totals /stats keeps in `~/.claude/stats-cache.json`. /stats adds up every log line
and each reply is written as several lines, so its token counts run several times
high; the script measures that overcount on the days both exist and divides it out.
That part is an estimate, and its cache writes are priced at the 5-minute rate, so
it is a lower bound. Per-project and per-day breakdowns cover only the logged days.
Without the cache file or a day both cover, there is no estimate and the card says
why.

The card says which prices it used and the date they were fetched. If the live page
could not be fetched it uses the last saved prices and says so on the card.
