---
name: vendor-insights
description: Generate a Claude-/insights-style faceted usage report for any OTHER agent estate on the host — codex, copilot, opencode, antigravity/agy, gemini (and claude itself for parity). Use when asked for "/insights on codex", "insights for copilot/opencode/agy/gemini", a cross-vendor usage report, or "what has <lane> been doing". The mechanical half (session index, bounded transcript reads, HTML render) is scripts/vendor-insights.py; this skill is its model-in-the-loop faceting + narrative complement, the sibling of experience-judge and decorum-voice-judge.
---

# vendor-insights

Claude Code's built-in `/insights` covers only Claude sessions. This skill produces the same
class of report — per-session facets → aggregate narrative → shareable HTML — for every other
agent lane on the host. `scripts/vendor-insights.py` owns everything deterministic; this skill
owns only judgment (reading transcripts, writing facets, composing narrative).

Vendors: `codex` · `copilot` · `opencode` · `antigravity` (alias `agy`) · `gemini` · `claude`.
Store paths live in `scripts/insight-cross-vendor-ingest.py` `VENDOR_REGISTRY` — never
hand-resolve a store path; if a store moved, fix the registry (fix bases, not outputs).

## Steps

1. **Index.** `python3 scripts/vendor-insights.py index --vendor <v> [--window-days N] [--max-sessions M]`
   → `logs/vendor-insights/<v>/index.json`. Pick the window from the ask (default 14d; a lane
   that has been quiet needs a wider window — check `list` first if unsure). Codex note: the
   index groups resumed rollout files by parent session_id — one entry = one logical session.
   **Read `meta` before anything else**: `meta.total_in_window` is the true in-window population;
   if `meta.capped` is true, either widen `--max-sessions` or carry the cap into
   `coverage_notes` — the shown sample is the newest N by `meta.order_key`, and the narrative
   must never speak as if the sample were the corpus. `meta.notes` carries store-level caveats
   (pruned blobs, responses-not-captured) that belong in `coverage_notes` verbatim.
2. **Facet.** For each session worth reading (order by activity; state the sampling cap
   honestly), run `python3 scripts/vendor-insights.py cat-session --vendor <v> --session <id>`
   (bounded; raise `--max-chars` only when needed) and write
   `logs/vendor-insights/<v>/facets/<id>.json` with the Claude-facet shape:
   `session_id, vendor, underlying_goal, goal_categories{}, outcome
   (fully|mostly|partially_achieved | not_achieved | unclear), user_satisfaction_counts{},
   agent_helpfulness, session_type, friction_counts{}, friction_detail, primary_success,
   brief_summary`. Facets must be PII-clean: no verbatim personal content, no secrets, no
   third-party names — summaries and counts only. Dispatch-lane sessions: the first "user"
   turn is usually an injected AGENTS.md/plan, not a human — read past it before judging goals.
3. **Narrate.** Write `logs/vendor-insights/<v>/narrative.json`:
   `tldr, at_a_glance{whats_working, whats_hindering, quick_wins, ambitious_workflows},
   areas[{name, session_count, description}], interaction_style, friction[{category,
   description, examples[]}], suggestions[{title, detail}], coverage_notes[]`.
   Ground every claim in the index numbers or a read transcript — the Data Grounding rules in
   `CLAUDE.md` apply in full (state denominators: "N of M sessions read"; a window is not the
   corpus; speech acts are not events). **The denominator is `meta.total_in_window`, not
   `len(sessions)`** — a capped index shows a sample, and every aggregate you quote must say
   which of the two it counts. Put every scope limit in `coverage_notes` — the renderer prints
   them and adds the unfaceted count, the index cap, and store notes itself.
4. **Render.** `python3 scripts/vendor-insights.py render --vendor <v>` → prints the
   `report-<ts>.html` path. Send that file to the requester (render display). Exit 2 means
   facets/narrative are missing — that is sequencing feedback, not an error to suppress.

## Boundaries

- Everything under `logs/vendor-insights/` is gitignored personal data — never commit it,
  never paste raw transcript excerpts into chat or durable files.
- All store access is read-only and goes through the script — no hand-crafted sqlite or
  file spelunking against vendor stores.
- "all" = run the loop per vendor; each vendor gets its own report. Cross-vendor synthesis
  goes in the message, not into a merged file.
