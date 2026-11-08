---
name: mcp-stack
description: Which free MCP server or framework to reach for, and its traps — finance/gov data (SEC EDGAR, Yahoo, SAM.gov, USAspending), web research (Exa, Firecrawl, Crawl4AI, Jina reader), design/art/brand (Canva, Inkscape, Penpot, Figma, Orshot, Hugging Face image gen, vectorizing, charts), data/spatial (DuckDB spatial, live ArcGIS layers, OpenStreetMap/Overpass, Census, MapLibre), and ops (PostHog, iMessage, context7 docs). Use when making a social post, OG card, poster, logo/vector, chart, map, or brand asset; when querying parquet/geojson/duckdb or a city's open-data layer; when an MCP "needs authentication" or fails; or when asked "what tools do we have", "is there an MCP for X", "should we add X".
---

# The MCP stack

A field guide from a bake-off where every server was run on the same real jobs (a
1080x1350 social post in a riso house style; real spatial questions checked by an
independent query). **Free tiers only.**

**Rule: free only.** Never upgrade, start a billing trial or enter a card on any of these
without the owner saying so. A paywall is a finding, not a purchase.

**Rule: nothing publishes.** Orshot has a `publish` param that posts to social; Canva and
Figma can share. Never pass them unasked. Output is a local file a human reviews.

## Design / art / brand — pick by job

| Job | Use | Why / cost |
|---|---|---|
| Finished marketing piece from a brief, best-looking | **canva** `create-design` -> `resize-design` -> `export-design` | Best-looking output of the set. **~6 AI designs/month free** (one design = ~15% of quota; resets monthly). Edit with `edit-design` rather than regenerate. |
| Riso post / card / poster, unlimited, exact numbers | **inkscape** MCP `inkscape_vector construct_svg` (params.header + params.body) -> `inkscape_render export_preview` | Renders real halftone patterns, feTurbulence grain, multiply overprint, misregistration. ~5s, headless, unlimited. **Default for anything repeatable**; keep your SVG body as a template file. |
| Precise vector layout in a design file | **penpot** `execute_code` -> `export_shape` | Free, unlimited. **A Penpot tab with the file must be open** (headless OK) or every call fails. |
| Same, but in Figma for someone to pick up | **figma** `create_new_file` + `use_figma` | Free Starter = **~20 counted calls/month, 3 files**. Budget it. No `createImageAsync`/`setPluginData`. |
| Reusable template with variables (OG card, IG post series) | **orshot** | ~100 renders/month free. Shape colour goes in `style.fill` (`backgroundColor` paints black). Output URLs are public-unguessable. |
| AI illustration draft, free | **huggingface** `dynamic_space` -> `mcp-tools/Qwen-Image`, `aspect_ratio:"3:4"` | Closest to riso of the free models. **~6 images/day** (ZeroGPU quota). 1.6MP; paints fake signature scribbles in corners — crop. Finals go to a paid engine (`make-art`). |
| Transparent PNG cutout | **huggingface** `space_name: Upsampler/birefnet-background-removal`, `{"image":"<public URL>"}` | ~5s. Spaces take **public URLs only**, never local paths. |
| Colour raster -> SVG (logos, marks) | **shapesoda** `vectorize {image_base64, image_type:"artwork", colors:8, format:["svg"]}` | ~10/day free. Download link expires in 24h — fetch immediately. Strip stray `#ff00ff` paths at cutout edges. Render the SVG at 4x = free upscale for flat art. |
| One-ink SVG (stamp, stencil, keyline plate) | **svg-tracer** `trace_bitmap_to_svg` (absolute paths) | Local potrace, unlimited, 0.1s. |
| Chart from real numbers | **antv-chart** | Hand-drawn texture option. **Sends your data to a third-party render service and returns a public URL** — public numbers only. Empty x-axis title prints "category". |
| 3D type / product mockup | Blender MCP (needs the app running) | Launch Blender with the add-on, then add the server ad hoc (`uvx mcp-for-blender@<pinned>`) with `DISABLE_TELEMETRY=true`. Telemetry is ON by default — always disable. |
| Raster finishing (newsprint halftone, photo edit) | GIMP MCP (needs gimp-console running) | For GIMP 3.2 headless: `gimp-console -i --batch-interpreter=python-fu-eval -b "p=Gimp.get_pdb().lookup_procedure('plug-in-mcp-server'); c=p.create_config(); c.set_property('run-mode', Gimp.RunMode.NONINTERACTIVE); p.run(c)" &`. Newsprint defaults to lines — set `circle`. Hex colours only. Kill gimp-console after. |
| HTML -> PNG card, nothing leaves the machine | Satori MCP, patched | The stock version uploads every image to public blob storage; patch it to save locally. Install with a frozen lockfile. |

Every number on a piece comes from the live source (curl it), never typed. Contrast-check
accent colours on light grounds (a mid red on cream can be ~3.8:1, which fails small text;
darken it under ~24px).

Dropped (don't re-test): Pollinations (watermark, low res), Stability (one-time trial),
fal/Replicate/Together (no card-free tier), Krita MCP (no text), tldraw and Excalidraw MCP
apps (draw only inside a chat UI), Bannerbear/Placid (trials), Postiz (no free cloud, needs
Docker), Remotion MCP (docs only), Buffer (signup CAPTCHA).

## Data / spatial

| Job | Use | Traps |
|---|---|---|
| SQL + spatial over parquet/csv/geojson/.duckdb | **duckdb** MCP (in-memory, spatial loaded) | `ST_Transform(ST_Point(lon,lat),'EPSG:4326','EPSG:26915')` returns `POINT(inf inf)` silently, so distance filters count 0. Pass `always_xy := true`. Assessor columns are often VARCHAR (max sorts as text); sale prices can carry a 999,999,999 placeholder. If the server runs read-write it can `COPY TO` anywhere: attach your real files `READ_ONLY`. |
| Live ArcGIS FeatureServer layer | **duckdb** `ST_Read('<FeatureServer>/0/query?where=...&outFields=...&orderByFields=OBJECTID&f=geojson&resultOffset=N')` | **Silently truncates at the server's maxRecordCount (often 2,000)** with no warning. Check `returnCountOnly=true` first, page with `resultOffset` + `orderByFields`, and name columns in the `UNION ALL` (an empty last page has none). |
| OSM / Overpass (restaurants in a neighbourhood...) | **osm** `openstreetmap_search_places` -> relation id -> `openstreetmap_query_bbox{within:"R..."}` | Area-by-name leaks: a neighbourhood name can pull rows from a same-named place in another state. Always search **inside the relation id**. Overpass mirrors 500 often; retry. |
| Census ACS by address/tract | **census** `census_resolve_geography{name:"<address>"}` -> `census_query_data{dataset:"acs/acs5", ...}` | Returns MOE (`...M` vars) — report it. Needs a free CENSUS_API_KEY. |
| Render a map PNG to see what you built | **maplibre** `render_style` | Headless Chrome, OpenFreeMap basemap, no key. |

Dropped: gis-mcp (88 tools, DuckDB covers it), the official Census MCP (needs
Docker+Postgres), crawler-style ArcGIS MCPs with no paging, PostGIS (DuckDB covers it).

## Web research / extraction

| Job | Use | Traps |
|---|---|---|
| "Who runs ops at X", people/company research | **exa** `web_search_exa` | Keyless. Often finds a company's own team page where generic web search finds nothing. |
| Fast read of a known page | **exa** `web_fetch_exa {urls:[...]}` | Sub-second from its index — **cached and no JS**; stale is possible. |
| Exact-phrase search, rendered scrape | **firecrawl** | ~1,000 credits/mo free (scrape 1, search 2, JSON 5). **JSON extraction invents fields** — trust only what appears in the returned `markdown`. |
| Rendered crawl, unlimited, Cloudflare-hidden emails | Crawl4AI CLI `crwl <url> -o markdown` | Decodes `data-cfemail` that curl misses. Batch: `AsyncWebCrawler(...).arun_many`. |
| JS page with nothing installed | `curl https://r.jina.ai/<url>` | ~20 req/min keyless, 2-18s. |

- Some city portals sit behind Cloudflare that nothing gets through headless; their
  ArcGIS REST layer usually has the same data.
- Email: use the address the business publishes on its own site, then check MX for that
  exact domain. Directories mangle domains (a dropped or added letter is common).
  Mailbox-level verification usually isn't possible from a home connection; port 25 is
  blocked.
- Dropped: Reddit MCP (403 anonymous — use `reddit-mining`), browser-use (needs a paid
  LLM key), Browserbase (phone verify). Tavily/Apify/Hunter/Brave all stop at a CAPTCHA
  on signup — one human click each if wanted.

## Finance / government data

| Job | Use | Traps |
|---|---|---|
| Reported financials, latest quarter | **sec-edgar** `get_xbrl_concepts` (per-filing) | EDGAR **companyfacts** (what many tools' `get_key_metrics` read) can be a quarter behind — it silently stops at the prior quarter. Per-filing XBRL gets the latest right. See `sec-financials`. |
| Prices, analyst up/downgrades, estimates | **yfinance** | Treat as flaky; verify a close against the exchange's own page before using a number. |
| SAM.gov opportunities, grants.gov, data.gov | a keyless **gov** data MCP | The free SAM route (SAM's own API needs login.gov MFA). Search results omit NAICS/set-aside — fetch each notice. |
| USAspending awards | **usaspending** | Filters by **place of performance**, not recipient location — for "recipients in state X" call `spending_by_award` with `recipient_locations`. "Award Amount" is lifetime, not fiscal year. |
| 10-yr Treasury etc. | keyless `curl "https://fred.stlouisfed.org/graph/fredgraph.csv?id=DGS10&cosd=<YYYY-MM-DD>"` | FRED lags Treasury's own curve by ~1 day. |

## Frameworks

- **Claude Agent SDK** for scheduled headless agents (e.g. a uv script that calls the
  sec-edgar MCP and writes JSON). Under macOS launchd it can't read `~/Desktop` or
  `~/Documents` — stage files elsewhere.
- **promptfoo** evals for a chat product: run the real system prompt through `claude -p`
  with deterministic asserts (banned words, word caps). Set
  `PROMPTFOO_DISABLE_TELEMETRY=1`. Pass the prompt on stdin (`--tools ""` swallows a
  positional prompt).
- **Observable Framework** for data -> static site (Python loaders via `uv run`). A literal
  analytics `<script>` tag breaks the build; inject it at runtime.
- **uv scripts** (PEP 723 inline deps) for every small pipeline.
- Dropped: Evidence.dev (now a login-gated studio), Pydantic AI/DSPy for small jobs (the
  SDK covers it), heavy vendor plugins that cost thousands of context tokens per session.

## Ops

| Need | Use | Note |
|---|---|---|
| One-off product-analytics questions ("what events exist", funnels) | **posthog** (single `exec` tool) | Same numbers as HogQL. A personal API key can write flags/cohorts — keep it read only. |
| Read texts on a Mac | **imessage** MCP | Beats raw `chat.db` SQL: decodes `attributedBody`, drops tapbacks, resolves contacts. **No send tool.** Pin it — single maintainer. |
| Current library docs | **context7** | Name the vendor in the query or it resolves the wrong library. |

**Keep a skill, not the MCP**, where the MCP is slower and heavier for the same answer:
Vercel (its MCP is ~240 tools incl. `buy_domain`; see `vercel-api`), Stripe (its MCP
redacts customer names; see `stripe-dashboard`), GitHub (`gh`), Notion (curl; the hosted
MCP rejects integration tokens), Apple Notes (`apple-notes`; MCPs ship delete tools).
**Never add an email provider's MCP that carries a send tool** if your rule is that a
human presses send.

## Auth state

- OAuth servers (canva, figma, orshot): if `claude mcp list` says "Needs authentication",
  run `/mcp` once in an interactive session. Keep passwords and tokens in the Keychain,
  never in a repo.
- Revoke any OAuth grant in that site's settings -> Connected apps.

## Adding a new MCP

Test before registering: `npx -y @modelcontextprotocol/inspector --cli <cmd> --method
tools/list` (wrap the server in a shell script — the inspector swallows `-e` and server
flags). Then: pin the version (`pkg@x.y.z`; reference servers do renumber), read the tool
list for send/delete/publish tools, check telemetry defaults, and add one row above with
its trap. Drop it when it stops earning its place.
