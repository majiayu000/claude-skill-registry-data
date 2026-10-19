---
name: seo-utils-mcp-guide
description: Use whenever the user asks about their SEO data or asks to run an SEO task through the SEO Utils MCP server (tools such as query_database, query_gsc, search_actions, read_action, lookup_action, write_action). Covers rank trackers ("my rankings", "my keywords"), Google Search Console, Google Business / GMB grids and reviews, LLM rank tracking, AI Visibility (brand share of voice in AI answers against competitors), keyword research and metrics, backlinks, competitors, SERP clustering, content briefs, log analysis and AI bots, indexing, automations and email. Tells you which tool to use (local SQL vs paid lookup vs write), which tables to query, and which action to run with which run tool.
---

# SEO Utils MCP Tool Selection Guide

When the user asks about SEO data, use this guide to pick the correct tool.

## How the SEO Utils tools work

**Data tools** are listed as tools: `list_tables`, `describe_table`, `query_database` (read-only SQL on the user's local database), `query_gsc` (Search Console tables), `list_workspaces` and `set_workspace`. SQL sees every workspace: filter tables that have a `workspace_id` column by the workspace the user means — the active one, which `list_workspaces` shows, unless they name another. Actions run in the active workspace, so if a report the user names is missing, check `list_workspaces`. When the user names a workspace for an action ("in the Client A workspace"), pass its ID as `workspace_id` on the run tool, beside `action` (not inside `arguments`): it applies to that call only and is not lost on a reconnect, unlike a `set_workspace` switch. SEO Utils 2.7.0 and older refuse `workspace_id`; use `set_workspace` there.

**Everything else is an action**, and actions are NOT tools. You can't call `get_organic_keywords` directly. Run an action with the run tool of its class, passing `{"action": "<name>", "arguments": {...}}`:

| Run tool | Actions that… |
|---|---|
| `read_action` | read local data only. Free |
| `lookup_action` | call an external service (DataForSEO, Google, …). May spend the user's provider credits |
| `write_action` | create, change, delete or run reports and settings, or send something (email, indexing submissions) |

- In this guide each action is followed by its class: `get_organic_keywords` (lookup) means `lookup_action` with `"action": "get_organic_keywords"`. Every action in the **External data** list below is a lookup.
- Call `describe_action` (1–10 names) before the first use of an action, to get its parameters. Arguments it doesn't declare, or the wrong run tool, are refused and nothing runs.
- Not sure which action fits? `search_actions` with a few words ("backlink summary", "create rank tracker").
- Pass each argument in the type `describe_action` shows; a value of the wrong type can be ignored without an error. Most lists (keywords, domains, competitors, email recipients) are JSON arrays, but `send_email`'s `attachment_path` is one comma-separated string and `create_automation`'s `actions` is a JSON array encoded as a string.
- When a tool result says "call run_rank_tracker" or names another action, run it the same way, through its run tool.
- SEO Utils 2.5.0 and older list every action as its own tool and have no run tools. If `read_action` isn't available, call the action by name with the same arguments.

## Rule 1: Local Data vs External Data

The user has TWO types of SEO data:

**Local database** (synced/tracked over time) — use `query_database` or `query_gsc`:
- Organic Rank Tracker reports → `organic_rank_tracker_*` tables. Ranked-page capture metadata is in `organic_rank_tracker_page_html_captures`, but the HTML body is stored on disk; discover two completed capture IDs with `query_database`, then use `compare_ranked_page_html` (read) to read and diff them
- Google Business Rank Tracker → `google_business_rank_tracker_*` tables
- Review Fetcher (Google Business reviews) → `google_business_review_fetches`, `google_business_review_snapshots`, and the GLOBAL deduplicated `google_business_reviews` table — review rows are SHARED across businesses, so NEVER filter it alone; always JOIN through `google_business_review_snapshot_reviews` against the business's latest completed snapshot and exclude `visibility_status = 'missing'`
- Google Search Console data → `search_console_*` tables (use `query_gsc`)
- LLM Rank Tracker → `llm_rank_tracker_*` tables
- AI Visibility explorations → `ai_visibility_explorations` (one row per exploration). Its numbers are app-internal JSON parts: read them with `get_ai_visibility_overview`, `get_ai_visibility_gaps`, `search_ai_mentions` and `get_ai_visibility_citations` (all read; free, from the cache), never with SQL. A different tool from the LLM Rank Tracker: it reads DataForSEO's database of collected AI answers instead of running the user's own prompts
- Content Struct outlines → `content_struct*` tables
- SERP Clustering → `serp_clustering_reports` + `serp_clustering_keywords` (parent_id = own id AND intersection_count NOT NULL → cluster parent; parent_id = 0 → unclustered orphan; else child of parent_id) + `serp_items` for the SERP URLs behind each keyword (filter to MAX(updated_at) per unique_id). WORD-ORDER TWIN FORK: a row with `serp_source_keyword_id` NOT NULL reused its twin's SERP (run with `reuse_word_order_twins=true`) — no SERP was bought for it, its own `serp_item_unique_id` rows in `serp_items` are NOT its results (never read its ranks/URLs through them), and its stored `intersection_count` describes the twin. Read clusters with the SQL the clustering tools print (it NULLs that count and names the twin in `serp_reused_from`); join `serp_items` only for rows where `serp_source_keyword_id IS NULL`
- NLP Analysis → `nlp_analysis_*` tables
- NAP Finder → `nap_finder_*` tables
- Saved Keywords → `saved_keywords_*` tables
- Automations → `automations`, `automation_*` tables
- Indexing status → `site_urls`, `index_now_urls` tables
- Log Analysis → `log_analysis_reports`, `log_file_analysis_*` tables, per-report `log_sources` (auto-import config), per-hit `log_file_analysis_ai_requests` (AI answer/assistant bots, 90d retention), and the GLOBAL `bot_categories` lookup (bot → bucket: ai_answer / ai_assistant / ai_training / search / social / seo_tool / monitoring / other). For upgraded reports (`log_analysis_reports.bucket_schema_version >= 1`), `log_file_analysis_page_activities` has denormalized `ai_answer_hits` / `ai_assistant_hits` / `ai_training_hits` / `search_hits` / `other_bot_hits` columns; for pre-upgrade reports those are 0 and you must parse `bot_hits` JSON + JOIN `bot_categories`.
- SEO Tests → `tests`, `test_*` tables

Column names vary by table: run `describe_table` before writing SQL against a table you haven't used in this conversation.

**External data** (on-demand, third-party estimates) — lookup actions, run with `lookup_action`:
- `get_keyword_suggestions` / `get_bing_related_keywords` — keyword research. `get_keyword_suggestions` takes an optional `source`: `labs` (database, cheapest) or `google_ads` (live Google Ads). Omitted = the installation default when it is one of those two, else `labs`; the other metric sources are refused because they cannot discover keywords
- `get_organic_keywords` — what keywords a domain ranks for (estimated)
- `get_traffic_summary` / `get_historical_rank` — traffic estimates
- `get_traffic_competitors` / `get_top_pages` / `get_content_gap` — competitor/page analysis
- `fetch_backlinks` / `get_backlink_summary` / `get_referring_domains` / `get_anchor_texts` / `get_backlink_history` / `get_backlink_competitors` / `get_backlink_gap` — backlink data
- `bulk_traffic_analysis` / `bulk_backlink_analysis` — multi-domain comparison
- `check_keyword_metrics` — search volume, KD, CPC. Optional `source` picks the data source (empty = the default set in SEO Utils); results land in `keyword_metrics`, tagged in its `source` column
- `fetch_serp_data` — live SERP results
- `get_robots_compliance` — whether bots in a log analysis report obeyed robots.txt

## Rule 2: Common Mistakes to Avoid

| User says | WRONG tool | CORRECT approach |
|-----------|-----------|-----------------|
| "rank tracker report" or "my rankings" | `get_organic_keywords` (lookup) | `query_database` on `organic_rank_tracker_*` tables |
| "what changed on this ranked page?", "why did this page become lost/new?", or "compare the captured HTML" | `query_database` alone (it can only see capture metadata/file paths, not the HTML body) or `fetch_serp_data` (lookup; SERP HTML is not ranked-page HTML) | Use `query_database` to select two completed `organic_rank_tracker_page_html_captures`, then `compare_ranked_page_html` (read). Start with `content_mode=main_content`; use `full_html` for title/canonical/robots/structured-data/template checks. Prefer equal `page_key` for before/after; different page keys are only an explicit lost-page vs replacement-page comparison. Treat changes as correlated evidence, not proof of ranking causation |
| "add keywords to my rank tracker" or "start tracking X for example.com" | `add_keywords_to_list` (write; saved keyword lists, a separate feature) or `query_database` (SQL is read-only, can't INSERT) | `add_organic_rank_tracker_keywords` (write) — then ASK the user whether to run `run_rank_tracker` (write) as a follow-up (don't auto-rerun). Saved keyword lists are a separate feature |
| "remove keywords from my rank tracker" or "delete X from my rank tracker" or "clean up keywords in <report>" | `remove_keywords_from_list` (write; saved keyword lists, wrong feature) or `query_database` (SQL is read-only, can't DELETE) | `remove_organic_rank_tracker_keywords` (write) — match is by keyword text. DESTRUCTIVE: also deletes historical positions, PAA appearances, and insights for those keywords. Confirm with the user before running on a large set |
| "delete my GMB report(s)", "remove these local rank trackers / grids", or "clean up my GMB test reports" | `delete_gmb_report_group` (write; deletes only the GROUP — its reports stay) or `query_database` (SQL is read-only, can't DELETE) | `delete_gmb_rank_tracker_reports` (write) with `report_ids` (whole-number IDs from `google_business_rank_tracker_reports`, max 100 per call; one report = one-item list). DESTRUCTIVE and permanent: also deletes the reports' keywords, grid markers, snapshots and ranking history — confirm the report names and IDs with the user first. Deleting reports does not delete a group that contained them |
| "search volume is 0 / missing but Keyword Planner shows numbers" or "get Google Ads volume for these keywords" | `check_keyword_metrics` (lookup) with no `source` (repeats the default, usually `labs`, whose database omits many keywords) | `check_keyword_metrics` (lookup) with `source='google_ads'` (or `dfs_search_volume`) — both need the user's own DataForSEO credentials and cost more, so confirm first. A re-check replaces the keyword's figures AND monthly history with the new source's. When reading `keyword_metrics`: `search_volume IS NULL` = checked but the source had no figure ("no data"); `0` = the source reported zero searches — never report NULL as 0 |
| "keyword ideas / suggestions from Google Ads", "Keyword Planner ideas for X", or "suggestions are empty / the database has no data for this niche keyword" | `get_keyword_suggestions` (lookup) with no `source` (usually `labs`, which misses many niche keywords) followed by `check_keyword_metrics` (lookup) on the whole list (a second paid call per keyword batch) | `get_keyword_suggestions` (lookup) with `source='google_ads'` — one search returns live Google Ads volume/CPC/competition for the seed AND every idea (~$0.10 per search vs ~$0.012 for `labs`; billed to the user's own DataForSEO credentials, so confirm first). The ideas carry NO keyword difficulty, search intent, backlink or SERP-results figures: `kd_from`/`kd_to`/`search_intents` filters are refused in this mode, and sorting by difficulty falls back to volume. The figures are also saved to `keyword_metrics` with `source = 'google_ads'` |
| "keyword cannibalization" | `get_organic_keywords` (lookup) | `query_database` on `search_console_query_pages` |
| "trending queries" or "GSC data" | `get_organic_keywords` (lookup) | `query_gsc` on `search_console_queries` |
| "my backlink history" | `fetch_backlinks` (lookup) | Could be either — ask if they mean tracked data or fresh API data |
| "optimization opportunities" | `get_organic_keywords` (lookup) | `query_database` on `search_console_query_pages` + `search_console_query_page_mentions` |
| "weak pages" or "low CTR pages" | `get_organic_keywords` (lookup) | `query_gsc` on `search_console_pages` or `search_console_queries` |
| "my automations" | N/A | `query_database` on `automations` table |
| "show me the content brief/outline" (existing report) | N/A | `query_database` on `content_struct_layout_headings` + `content_struct_layout_metadata` |
| "analyze competitors for keyword X" or "create/generate a content brief or outline" | `query_database` (SQL can only read outlines, not produce them) | `create_content_struct` (write; scrapes top SERP + competitor headings, async), then `generate_content_outline` (write; AI outline; needs provider + model — ask the user which) |
| "cluster these keywords" or "group my keywords by topic/SERP similarity" | `query_database` (read-only), saved-keywords actions (wrong feature), or `fetch_serp_data` (lookup; buys SERPs without clustering them) | `create_serp_clustering_report` (write; async — poll `serp_clustering_reports.clustering_status`). To add keywords to an EXISTING report there is no add-keywords action: `run_serp_clustering` (write) with `keywords` + `distribute_keywords=true` (keeps existing clusters). To cut SERP cost on lists with word-order variants ("laravel horizon" / "horizon laravel"), pass `reuse_word_order_twins=true` on either action (opt-in, default false; typically saves 6-16% of SERP cost) — tell the user the trade-off first: some keywords can land in a slightly different cluster, and word order occasionally changes intent. A twin that already has fresh SERP data keeps its own |
| "which pages are AI bots fetching?" | `get_organic_keywords` (lookup) | Check `log_analysis_reports.bucket_schema_version` first. If ≥1, `query_database` on `log_file_analysis_page_activities WHERE ai_answer_hits + ai_assistant_hits > 0`. If =0, parse `bot_hits` JSON + JOIN `bot_categories` |
| "what questions are AI engines asking about my site?" | N/A | `query_database` on `log_file_analysis_ai_requests` grouping by `extracted_query`. Low counts are NORMAL if traffic is mostly ChatGPT-User / Claude-User — those bots strip prompt data |
| "is GPTBot / ClaudeBot / Google-Extended violating my robots.txt?" | `query_database` | `get_robots_compliance` (lookup) — SQL cannot evaluate robots.txt rules, the matcher is Go-side |
| "my share of voice in AI answers", "where do competitors beat us in ChatGPT / AI Overviews?", "which prompts name my competitors and not me?" | `query_database` on `ai_visibility_explorations` (the parts are app-internal JSON) or on `llm_rank_tracker_*` (the user's own tracked prompts, another tool) | `list_ai_visibility_explorations` (read), then `get_ai_visibility_overview`, `get_ai_visibility_gaps` or `search_ai_mentions` (read). What is not loaded comes back with `needsSpend` and the paid call (`run_ai_visibility_load` (write), `load_ai_visibility_list` (lookup)): tell the user the price and send it unchanged only after they agree |
| "how is AI traffic trending?" | N/A | `query_database` on `log_file_analysis_page_activities` summing `ai_answer_hits + ai_assistant_hits` by date (upgraded reports only) |

## Rule 3: When to Use Lookup Actions

Use the research lookups (keyword, traffic, backlink, SERP and competitor data; they spend the user's DataForSEO credits) ONLY when:
- User asks about a **domain they don't track** (competitor research)
- User explicitly asks for **fresh/live data** from DataForSEO
- User wants **keyword suggestions** or **keyword metrics** for new keywords
- User wants **backlink data** for any domain
- User wants to **compare multiple domains** (bulk analysis)

Task lookups are fine whenever the task needs them: `find_google_business` / `find_google_business_from_maps_url` (the place ID a GMB report or review fetch needs), `get_robots_compliance`, `check_google_indexing_status` / `check_index_now_status`, `get_demographics` and `fetch_autocomplete_keywords`.

Never use a lookup action as a substitute for data the local database already has.

## Rule 4: Export and Send

- `send_email` (write) — send any email with SMTP. Check `smtp_credentials` table first
- Automations — use `create_automation` (write) for recurring workflows (triggered by events)
- For one-time exports, generate the content and use `send_email` to deliver it

## Rule 5: Visualizing GMB Rank Tracker Grids

When the user asks to "draw", "render", "show on a map", or "visualize" GMB rank tracker grids or rankings, produce an HTML artifact using **Leaflet 1.9.4 from cdnjs** (artifacts block most other script hosts) that matches the in-app heatmap style. Do NOT use Google Maps (needs an API key, won't render in artifacts) or default Leaflet pins (wrong style — the app uses small colored circles).

**Data query** — use `query_database` to fetch grid points:
- Grid layout only (no rankings): `SELECT lat, lng FROM google_business_rank_tracker_markers WHERE google_business_rank_tracker_report_id = ? AND enabled = 1`
- Grid with rankings: join `google_business_rank_tracker_markers` with `google_business_rank_tracker_snapshot_items` on `(lat, lng)`, filtered by `place_id = report.place_id` and the chosen `google_business_rank_tracker_snapshot_id`. For "best rank across all keywords" per grid point use `MIN(rank)` grouped by `(lat, lng)`. See the `google_business_rank_tracker_snapshot_items` schema annotation for the canonical avg_rank / SoLV math — do not invent your own.

**Pick the right marker size — this is the most common mistake:**

| Context | Marker style | Mirrors |
|---|---|---|
| **Full-page / standalone artifact** (default when the user asks "draw a map", "show me the grid", "visualize my rankings") | 32 px circle with the **rank number inside** + 2 px white border | Google Maps view in `GoogleBusinessRankTrackerMap.vue` (`createMarkerContentWithRank`, `frontend/src/helpers/googleMaps.js:81-250`) |
| **Compact / dashboard thumbnail** (only when the user says "thumbnail", "card", "widget", "compact preview", or marker count is ≥225 and labels would overlap) | 10 px solid colored dot, no text | Heatmap card in `GoogleBusinessRankTrackerReportHeatmap.vue` |

**Rendering recipe — full-page (default):**

1. Load Leaflet from CDN: `https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.9.4/leaflet.css` + `https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.9.4/leaflet.js`.
2. Init the map **interactive** with an OpenStreetMap tile layer so the user can see streets/neighborhoods:
   ```js
   const map = L.map(el)
   L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
     attribution: '&copy; OpenStreetMap contributors', maxZoom: 19
   }).addTo(map)
   ```
3. One marker per grid point with a labeled `L.divIcon` (text = rank, or `21+` when no rank):
   ```js
   L.marker([lat, lng], {
     icon: L.divIcon({
       className: 'gmb-rank-marker',
       html: `<div style="display:flex;align-items:center;justify-content:center;
                          width:32px;height:32px;border-radius:9999px;
                          background:${color};color:#fff;font-weight:600;font-size:13px;
                          border:2px solid #fff;box-shadow:0 1px 3px rgba(0,0,0,0.35);">
                ${rank ?? '21+'}
              </div>`,
       iconSize: [32, 32],
       iconAnchor: [16, 16],
     }),
   }).addTo(map).bindTooltip(`Rank: ${rank ?? '21+'}`, {direction:'top'})
   ```
4. Auto-fit bounds: `map.fitBounds(bounds, {padding:[24,24], maxZoom:18})`.

**Rendering recipe — compact thumbnail (only when explicitly asked):**

- Same CDN load, but init map read-only and **omit the tile layer** for a transparent dot-only heatmap:
  ```js
  L.map(el, {dragging:false, zoomControl:false, scrollWheelZoom:false, doubleClickZoom:false,
             touchZoom:false, boxZoom:false, keyboard:false, attributionControl:false})
  ```
- Markers: `width:10px;height:10px;border-radius:9999px;border:1px solid rgba(0,0,0,0.15);` no text, `interactive:false`.
- Fit bounds with `padding:[12,12]` (use `[6,6]` when ≥121 markers).

**Color by rank — exact thresholds, do not improvise (both modes):**
- rank ≤ 3 → `#22c55e` (green)
- rank 4–10 → `#eab308` (yellow)
- rank > 10 (i.e. 11–20) OR no rank → `#ef4444` (red)

If the user wants extras (hover popups with rank/keyword/title, side-by-side per-keyword maps, dark mode), build on top of these recipes — but keep the marker dimensions, color thresholds, and Leaflet 1.9.4 CDN URL unchanged so the artifact stays visually consistent with the desktop app.
