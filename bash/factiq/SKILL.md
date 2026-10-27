---
name: factiq
description: >
  Answer economic and financial data questions with FactIQ data: US and
  international indicators, trade, markets, earnings calls, executive media,
  central-bank speeches, minutes, and statements (what Fed, ECB, and other
  central-bank officials said), business news, and satellite signals. Satellite coverage includes rainfall,
  fires, air quality, NDVI, heat, soil moisture, nighttime lights, reservoir
  levels, shipping, ports, and chokepoints by country, state, or bounding box.
  Use for unemployment, inflation, GDP, wages, energy, trade flows, stocks,
  commodities, forex, earnings intelligence, drought and monsoon conditions,
  wildfires, economic charts and maps, and research reports.
  Discover series, query read-only SQL, compute, then return a sourced answer or
  local output. Use the bundled SQL generator for national customs trade.
---

# FactIQ Data Tools

You are the analyst. FactIQ provides authenticated MCP tools for discovery and
fetching: catalog, dataset and series search, read-only SQL, series lookup,
market data, transcript and media search, satellite signals, style guides, and
feedback. There is no server-side agent. You decompose the question, fetch the
data, do the math, then answer or build a local output.

**Publishing boundary:** FactIQ cannot host charts or reports publicly or
create public share links. When asked for a FactIQ-hosted link, explain the
limitation and offer a local chart or report file. Do not inspect or
direct the user to FactIQ's legacy authenticated web interface, use browser
automation, or probe HTTP endpoints to work around a missing tool. The legacy
web interface is not a supported product workflow. Normal OAuth connection is
still supported; website, support, privacy, and OAuth URLs do not imply a
publishing capability. If the user rules out other publishers, do not use
ChatGPT Sites or another service. Never call `send_feedback` for this
intentional capability boundary.

Three output modes:

- **Direct answer** — a plain-text sentence with no chart. Use
  when the question asks for a single current value or a simple scalar lookup
  where a chart would add nothing: "what's the US unemployment rate right now?",
  "latest CPI print", "Apple's trailing P/E". Still fetch the value with the MCP
  tools — only the *presentation* is a sentence. State the number with its
  period and source (e.g. "US unemployment was 4.1% in May 2026, per BLS.").
  The moment the question wants a trend, a history, a comparison across
  categories or entities, a breakdown, or explicitly asks for a chart or report,
  switch to one of the modes below.
- **Quick chart** — one focused ChartSpec saved as a local JSON file. Default
  for a single trend or category comparison. See
  `references/output/chart-spec.md`.
- **Detailed report** — a saved report JSON object with summary, sections,
  charts, and methodology. Use for broad analytical
  questions. Covered domains route through `references/report-patterns/README.md`.
  If scope is unclear, use `references/report-patterns/interview-step.md` first.

**Data in, output out:**

- All discovery and fetching go through the FactIQ **MCP tools**. Local scripts
  build and render the final files from the fetched results.
- The local scripts never touch the API:

  ```bash
  python3 "{plugin_root}/scripts/trade_sql.py"  ...   # SQL generator: US/China/India/Korea/Japan/Taiwan customs
  python3 "{plugin_root}/scripts/hs_codes.py"   ...   # HS commodity code <-> name, offline
  python3 "{plugin_root}/scripts/series_math.py" ...  # YoY/YTD/share/index/merge on saved results
  ```

  Resolve `{plugin_root}` once, then reuse it. In Claude Code it is
  `${CLAUDE_PLUGIN_ROOT}`. In Codex, start from the absolute path supplied for
  this `SKILL.md`: the plugin root is two directories above the directory
  containing this file (`skills/factiq/../..`). Never resolve these scripts
  from the shell's current working directory or from a similarly named
  `scripts/` directory in the user's project. Keep the quotes around the
  absolute path so installations under a directory containing spaces still
  work.

  **For a bilateral-trade question on a national customs schema, generate the
  SQL instead of writing it.** `trade_sql.py` encodes each schema's series-ID
  grammar, partner-code system, units, and HS-level rules, so the query is
  correct by construction — run `--help` for the subcommands (total / products
  / trend). For Eurostat Comext (EU) trade, write the SQL with the rules in the
  Comext section of `references/data/sql-guide.md`. Label the HS codes a ranking returns with `hs_codes.py` (zero server
  calls), and use `series_math.py` for growth or shares when you have saved the
  fetched payload locally.

## Setup

One connection covers everything: the FactIQ **MCP server** bundled with this
plugin (`.mcp.json`), authorized over OAuth. On first use the coding agent runs
FactIQ's browser-based **Connect** flow. If the FactIQ tools are missing or
return an auth error, the connection isn't set up yet — tell the user to
authorize the MCP server:

- **Claude Code**: run **`/mcp`**, pick **factiq**, and complete the sign-in.
- **Codex**: run **`codex mcp login factiq`** and complete the sign-in.

The same FactIQ login works everywhere (email, Google, or passkey) and authorizes
the data and feedback tools.

**Local development.** The bundled MCP URL is
`https://api.factiq.com/mcp`. For a local backend, edit `.mcp.json` in your
development checkout or configure a standalone `factiq` MCP server in Codex or
Claude Code that points at the local URL.

## Tools

All FactIQ tools are MCP tools provided by the `factiq` MCP server.

### Data

| Tool | Purpose |
|---|---|
| `get_data_catalog` (`schemas?`, `full?`) | Per-schema index + the shared table DDL. **Call once per session before anything else.** `full=true` returns the heavy per-dataset dump (rarely needed — use `describe_dataset`). Schemas listed under `schemas_without_data` have no rows — skip them. |
| `search_datasets` (`query`, `schemas?`, `limit?`) | Keyword (not semantic) ranking of datasets across all schemas. **The first discovery step** — find the right `schema` + `dataset_code`. |
| `describe_dataset` (`schema`, `dataset_code`) | Full metadata for one dataset: topic, methodology, base-change notice, dimensions, example series. Call after `search_datasets`. |
| `search_series` (`schema`, `terms`, `limit?`, `include_compound?`) | Series-level title-substring search within one schema (`terms` is a list — prefer short stems). Includes `COMPOUND::` series. |
| `run_sql` (`schema`, `sql`, `question?`, `explore?`, `auto_retry?`, `page?`) | Read-only SELECT against one schema. The power tool for joins, pivots, aggregation. `page` works on the `nasa_fires` schema only, where individual rows are the answer; everywhere else, aggregate. |
| `get_series` (`schema`, `series_id`, `from_year?`, `to_year?`, `transform?`) | Fetch one series — timeseries, tabular, or `COMPOUND::` ids all work. `transform="yoy_pct"` (percent change) or `"yoy_diff"` (difference, for rates) adds a column with the change versus the same period one year earlier, matched by calendar date; the cell is null where that period is absent. A `coverage_note` with `missing_periods` means the series skips a period — disclose it. SEC-backed results include `row_sources` keyed by `result_index`, with the supporting filing, accession/form/date, reported-vs-derived status, and a standardized `source_link`. For those series `schema="filings"` and `schema="sec"` return the same result. |
| `get_market_data` (`asset`, `data_type?`, `frequency?`, `limit?`) | Provider-neutral quotes, daily/weekly/monthly price history, company and ETF profiles, symbol search, FX, and commodities. `data_type` is `price_history`, `quote`, `company_profile`, `etf_profile`, or `symbol_search`; `limit` is 1–5,000. |
| `get_geo_data` (`dataset`, `region`, `start_date`, `end_date`, `aggregation?`, `resolution?`, `include_flares?`) | Satellite-derived signals: `fires_viirs` (crop burning/wildfires; every detection since 2012 is held in FactIQ's own database, so calls answer in under a second — `aggregation="seasons"` compares the same calendar window in every year since 2012 in one call, `"grid"` maps the footprint at a cell size you pick with `resolution`, `"points"` returns exact detection coordinates), `no2_tropomi` / `so2_tropomi` / `co_tropomi` (industrial, coal/smelting, and combustion activity), `aerosol_index_tropomi` (smoke/dust/haze), `ndvi_s2` (crop condition) — these five also accept `aggregation="grid"` for a cell-by-cell spatial snapshot — `precip_chirps` (0.05° gauge-calibrated rainfall within 50S-50N), `precip_imerg` (0.1° global rainfall), `temperature_power`, `soil_moisture_power`, `wind_power` (wind speed and the direction it blows from), `humidity_power` — aggregated over a country, state (`"India/Punjab"`), or bbox. `resolution` and `include_flares` apply to `fires_viirs` only; gas flares and other permanent industrial heat are excluded unless you ask for them. **Read `references/data/satellite.md` before first use** — it covers windows (50 intervals, 200 for fires; grid/points 92 days, 366 for fires), the `valid_obs_share` rule, and attribution. For fire questions this tool does not cover, query the `nasa_fires` SQL schema (`references/data/schemas.md`). |
| `search_company_filings` (`company`, `query?`, `concept?`, `search_target?`, `report_type?`, `fiscal_year?`, `fiscal_period?`, `metric_class?`, `segment?`, `date_from?`, `date_to?`, `active_only?`, `format?`, `limit?`) | The central tool for company filings. Deterministic (no model) search over the structured facts and report metadata in one company's filed reports, for every company FactIQ covers: US SEC filers (10-K, 10-Q, 8-K, plus 20-F/40-F/6-K for foreign filers, and for companies that went public recently the S-1/F-1 registration statement and the 424B4 or 424B1 final prospectus) and companies listed in Germany (annual, half-year, Q1, and Q3 reports, values in EUR — e.g. `company="BAS"` for BASF SE), the UK (`ULVR` for Unilever plc), France (`MC.PA` for LVMH), Switzerland (`NESN` for Nestlé), and India (the Nifty 50 companies, from their NSE quarterly results and annual reports — `RELIANCE` for Reliance Industries; an Indian company's Q4 results hold its audited full year). Use an exact ticker; a share-class sibling (GOOGL for GOOG) resolves to the same filer; a German, UK, French, or Swiss company resolves by its local ticker, full name, or LEI, and carries its exchange suffix (MC.PA, BA.L, ROP.SW) when the bare symbol also belongs to a US filer; an Indian company resolves by its NSE symbol (RELIANCE, M&M), the same symbol with `.NS`, its BSE scrip code, or its full name; an ambiguous name comes back with `possible_matches`. Start with `search_target="coverage"` to see which report types, periods, and metric classes exist. Then set `concept` to one metric name (`"revenue"`, `"net income"`) to get that concept's values across periods, or use `search_target="metrics"` to list stored concepts and `"facts"` for reported values. `query` is a lexical text search across concept names, source labels, aliases, and segment names; narrow with `metric_class` (`financial`, `ifrs`, `segment`, `geography`, `product`, `kpi`, `apm`, `guidance`, `offering_terms` for the IPO price, shares offered and proceeds), `segment`, `report_type` (`annual`, `quarterly`, `half_year`, `10-K`, `10-Q`; `424B4` with `search_target="commentary"` reads only a final IPO prospectus), `fiscal_year` + `fiscal_period` (`2025`, `Q3`), or `date_from`/`date_to`. Every result is a tree: company → metric class → concept → series → period. With `format="json"`, filing/fact nodes retain the report URL and add a standardized `source_link`; exact-ticker metrics/facts misses may fall back to standardized statements with no filing evidence. `format="pretty"` returns a rendered text tree instead of JSON. When a company reports the same concept twice in one filing, the second copy is labeled "Reported line 2" — never add it to the first. Results stop at `limit` (max 50) with `truncated: true`; narrow the filters rather than paging. For joins or aggregations across companies over the same archive, use `run_sql` on the `filings` schema (open to every account; tables in `references/data/schemas.md`). |
| `search_earnings_transcripts` (`query`, `search_target?`, `ticker?`, `company_name?`, `quarter_filter?`, `claim_family?`, `section?`, `detail?`, `limit?`) | Lexical (not semantic) retrieval over atomic, quote-anchored earnings-call rows — never a raw transcript dump. Tickers go in `ticker` and company names in `company_name`; pass one of the two, never both (both ignore case; a name in `ticker` is still read as a name, and the response says so). `company_filter` is the old name of `ticker` and still works. Companies listed in India carry the NSE suffix (`RELIANCE.NS`, `TCS.NS`); a plain NSE symbol is also accepted and reported in `read_as_exchange_symbol`, but a symbol that is also a US ticker (`INFY`) selects the US listing, so pass `INFY.NS` for the NSE one. Companies listed in Switzerland carry `.SW` (`NESN.SW`, `ROP.SW`) and follow the same rules (`ROP` is Roper Technologies; Roche is `ROP.SW`); their half-year calls are Q2 and full-year calls Q4. For a non-empty `query`, strict websearch matches rank above an automatically broadened loose partial-match OR-of-tokens tier, so lower-ranked rows may match only some terms; trigram fallback runs only when full-text search returns no rows. Inspect every row for support and retry concise company-native vocabulary (`"capital expenditure"`, `"capex"`, segment names) before concluding lexical silence. For one-call notes, first use `search_target="coverage"`, choose its exact returned `latest_period`, then browse `claims` with `query=""`, that ticker + `quarter_filter`, `detail=true`, and a deliberate limit; fetch `pressure_points` with the same ticker and quarter. The browse is capped, not a promise of a complete call. Claim and pressure rows include `transcript_id`, `source_block_index`, `qa_turn_id`, and `source_link`; `source_link.source_label` names the company or ticker, fiscal period, and earnings call transcript, never the ingestion vendor. Quote only `verbatim_quote`, preserving any `[…]` omission marker exactly; `canonical_statement` is normalized, and neither `analyst_hypothesized` nor `mgmt_declined_to_confirm` is a management assertion. For filed actuals use `search_company_filings`; for formal targets use `sec_guidance`. Full target/filter reference and workflows: `references/report-patterns/earnings-intelligence.md`. |
| `search_media_appearances` (`query`, `search_target?`, `company?`, `person?`, `sort?`, `appearance_type?`, `claim_family?`, `date_from?`, `date_to?`, `detail?`, `limit?`, `offset?`, `institution?`, `country?`, `show?`, `channel?`, `company_filter?`) | Two kinds of source: (1) what company executives, investors, fund managers, analysts, economists, journalists, and other guests said on podcasts, TV interviews, and at conferences outside earnings calls; (2) documents that central banks and monetary authorities published from late 2025 onward: speeches, testimony before legislatures, policy statements, meeting minutes, press-conference transcripts, press releases, blog posts, interviews, and reports from the Federal Reserve Board and the regional Reserve Banks, the European Central Bank, the Bank of England, the Bank of Japan, the Reserve Bank of India, the People's Bank of China, the Bank of Korea, the Hong Kong Monetary Authority, Taiwan's central bank, and the national central banks of the euro area and other EU members (a document in another language yields English paraphrases; its title may stay in the source language). Use it for what Fed, ECB, or other central-bank officials said, not only for what executives said. **Search with one to three key words** in `query` (`"inflation outlook"`, `"export controls"`) and put the speaker in `person`, the publisher in `institution`, and the kind of document in `appearance_type`. A returned row must contain most of the query words, so a long question returns few or no rows; retry with the speaker's own vocabulary or a synonym before concluding there is no coverage. Retrieval is deterministic and lexical over precomputed public-safe paraphrases; **no serving-time model** interprets or expands the query. Strict full-text matching (all query words) runs first, loose full-text matching (most of the query words) only when strict finds no candidates, and trigram matching only when both are empty. Claims cover listed and unlisted companies (OpenAI, DeepSeek, MiniMax), institutions (central banks, regulators), and whole markets and industries, not only the speaker's own employer. Targets are `search` (default claims + passages blend), `claims`, `passages`, `pressure_points`, `appearances`, and `coverage`. `sort="relevance"` ranks lexical score before publication date; `sort="newest"` ranks publication date before lexical score. `company` takes comma-separated tickers and company names together (`"NVDA,OpenAI,Federal Reserve"`): a stored ticker matches by ticker, and any other value matches the name of the company, institution, or organisation a section is about, ignoring punctuation, a leading "The", and corporate suffixes (`"NVIDIA Corp."` finds NVIDIA; `"Alphabet"` also reaches GOOGL rows). Each result records `company_tickers`, `company_names`, `company_matched`, and `company_unmatched`; a name that matches nothing returns no rows plus up to five possible matches under `company_unmatched`, so retry with one of them. For `appearances` and `coverage`, each value is also matched exactly, upper-cased, against the entity references of claims (products, rivals, partners such as `"CUDA"`) and listed under `company_references` when found only there, so alternate spellings can return different rows. `company_filter` is the old name of `company` and still works, but do not pass both. `company` matches what a claim is about, not who published it (`company="European Central Bank"` also returns a Bank of England speech about the ECB). To select a publisher, use `institution`, a case-insensitive substring of the publishing institution (`"Bank of Japan"`, `"Bundesbank"`), or `country`, the ISO code of its jurisdiction (`"US"`, `"IN"`, `"EU"` for the European Central Bank); either one restricts every target to official documents, and `coverage` then returns one `UNATTRIBUTED` row with the document count, date span, and claim count. `person` is a case-insensitive speaker-name substring; `show` is a case-insensitive podcast show-name substring (`"Odd Lots"`, podcast episodes only) and `channel` a case-insensitive YouTube channel-name substring (`"Bloomberg Television"`, YouTube videos only); when more than one of `show`, `channel`, and `institution` is given, rows that match any of them are returned; `coverage` lists the stored show and channel names for each company. `appearance_type` values are `podcast`, `tv_interview`, `conference`, and `other` for interviews, and for official documents `speech` (also blog posts and opening remarks), `tv_interview` (published interviews), `statement` (also implementation notes), `minutes` (also summaries of opinions), `press_conference`, `testimony`, `hearing`, and `other` (press releases, reports, projections). `claim_family`, inclusive `date_from`/`date_to`, and `detail` narrow further. `limit` is one page of 1-50 rows and `offset` skips that many ranked rows; every result carries `has_more`, and `next_offset` when more rows follow. Dates are the publication/upload date, not necessarily the event date; an official document also carries `event_date`, the date of the meeting, speech, or hearing (FOMC minutes are published about three weeks after the meeting). `claim_family` makes blended search claims-only, is invalid with `passages`, and requires matching claims for catalog targets. Finding rows expose `result_kind`, `canonical_paraphrase`, speaker/topic/video metadata, relevance, and `source_url`: a timestamped YouTube URL for a video, the episode page for a podcast, or the document page for an official document (a PDF transcript links to the page, `...pdf#page=4`); for an official document, `channel` is the institution name. `appearances` returns video-level metadata, attribution, matching-claim count, URL, relevance, and `institution`, `document_kind`, and `event_date` (null on interview rows); `coverage` returns company-level structured corpus counts and date/channel inventory. `detail=true` adds normalized claim/attribution fields plus `institution`, `document_kind`, and `event_date` to finding rows, but never raw transcript text or evidence spans; claim-only fields remain null on passages and detail does not change catalog rows. Never put `canonical_paraphrase` in quotation marks or claim it is verbatim; follow the timestamped or document source when exact wording or tone matters. In a press-conference transcript, a row whose speaker is `Questioner` is a journalist's question, not the institution's position. Empty-query behavior and the complete workflow are in `references/report-patterns/media-intelligence.md`. |
| `search_news` (`query?`, `tickers?`, `topic?`, `sources?`, `start_date?`, `end_date?`, `sort?`, `limit?`) | Search FactIQ's curated business-news feed — public RSS headlines and summaries from Bloomberg, the Financial Times, and the Wall Street Journal, plus India-macro (Zerodha Daily Brief, ET HealthWorld) and global-health sources (WHO, ECDC, CDC, STAT News, KFF), aggregated and processed by FactIQ so each article carries the listed companies it names (`{symbol, exchange, country}`) and an `analysis` block: searchable keywords, a geography, and an `angle` — one sentence on why the story matters to an investor. Company stories get analysis too, not just macro ones; only content with no business read at all (sports, lifestyle, celebrity) comes back with `analysis: null`. Results are headline + short publisher summary + link out, never full articles. `query` is lexical full-text over the headline, the publisher summary and the article's `analysis` fields (keywords, geography, angle), so a subject that an article covers without naming it in the headline still matches — start with short concrete stems (`"obesity drug"`, `"rate cut"`, `"ai governance"`); if a multi-word query matches nothing in full, the tool automatically retries matching ANY of the words with rare words ranked first, flagged as `meta.query_mode: "any_term"`, so one query attempt is usually enough. `tickers` matches share classes and cross-listings automatically (GOOG also finds GOOGL-tagged articles, TSM its Taiwan listing) — pass whichever symbol you know; most macro stories name no listed company, so zero ticker matches is a normal answer. `topic` is one of markets / economics / companies / technology / politics / world / energy / health / india / opinion — combined with a `query` it is a ranking preference (matching sections rank first, but strong matches from other sections still return, since stories often run outside their obvious feed); without a query it filters to the topic's feeds. `sort` is `"latest"` (default) or `"relevance"` (needs a query); `limit` 1–50 (default 20). Coverage is recent news (most feeds start late 2025) — treat it as a current-events lens, not an archive. |
| `get_style_guides` (`guides`) | FactIQ house-style guides (`"chart"`, `"report"`, `"sql"`, `"earnings"`, or `"all"`). Use these for current style and sourcing rules. Fetch `"earnings"` before writing from `search_earnings_transcripts`. |

When an answer uses a quote or filing-backed figure, place that row's provided
`source_link.source_url` immediately beside the claim as a Markdown link whose
text is `source_link.source_label`. Do not replace that evidence label with an
ingestion vendor, make a second tool call solely to find a citation, reconstruct
a URL, or substitute a related press release. `source_precision="document"` is
not exact context. If `source_url` is null, state that the direct link is
unavailable and use the returned locator/document ID only as provenance
metadata.

Every row-returning tool (`run_sql`, `get_series`, `search_company_filings`,
`search_earnings_transcripts`, `search_media_appearances`) returns **at most 50
rows**, but the remedy is tool-specific:

- For `run_sql`, aggregate to the needed grain; for a long `get_series`
  result, use `from_year` / `to_year`. See **Context budget** below.
- For earnings, narrow by ticker, exact fiscal quarter, target, family, and
  (for claims) section. Synthesize multiple bounded calls and disclose when a
  50-row result may be incomplete. Never query the gated `transcripts` schema
  with `run_sql`, request a raw transcript, or assume pagination exists.
- For media, narrow by ticker, person, show, channel, institution, dates,
  target, appearance type, and claim family, or read the next page with
  `offset=next_offset` while the result says `has_more`. Synthesize multiple
  bounded searches; never use SQL or assume a full-transcript path.

There is no universal "give me everything" option, by design.

#### Earnings target/filter quick reference

| Target | Use and applicable arguments |
|---|---|
| `claims` | Lexical search or empty browse; company, exact quarter, family (primary or secondary), claims-only section, detail, limit |
| `pressure_points` | Lexical search or empty browse; company, exact quarter, linked family, detail, limit. `section` is ignored because these rows are Q&A |
| `disclosure_profile` | Direct lookup by the first `ticker` value, the first ticker resolved from `company_name`, or `query`; not text or quarter search; other filters, detail, and limit are ignored |
| `coverage` | Company inventory and limit; query, quarter, family, section, and detail do not narrow it |

Canonical call patterns:

- **Latest-call note:** `coverage` for one ticker → read `latest_period` →
  empty-query `claims` with that ticker + exact `quarter_filter`, `detail=true`,
  deliberate limit → `pressure_points` with the same ticker + quarter.
- **Cross-company theme:** check coverage, then run the same concise query and
  synonym sweep separately for each ticker + exact comparable quarter; inspect
  partial-term rows before merging them.
- **Disclosure habits:** call `disclosure_profile` with one ticker; do not add a
  quarter or treat the ticker as a theme query.
- **Latest figure** (a share of sales, mix, guidance or target that
  management restates from call to call): `coverage` for the ticker → read
  `latest_period` and `latest_call_date` → search the topic with that ticker
  and no `quarter_filter`, then check that the newest row comes from
  `latest_period`. If it does not, search the latest call by itself
  (`quarter_filter=<latest_period>`). If the latest call does not mention
  the figure, report the newest call that does, and say that the later
  calls did not repeat it. Give the call date beside the figure.

Quote only `verbatim_quote`; use `canonical_statement` unquoted. A `[…]`
inside `verbatim_quote` marks omitted transcript sentences between
non-adjacent evidence spans — preserve it exactly when quoting, and never
present the text on either side of it as one continuous statement. Treat
`analyst_hypothesized` as the analyst’s framing and
`mgmt_declined_to_confirm` as a refusal. Keep spoken call claims, formal
`sec_guidance` targets, and filed actuals as separate source classes. Put
the row's provided source URL beside every quote you use, with the provided
source label as link text; if it is null, say the link is unavailable instead
of searching for or inventing one.

#### Media target/filter quick reference

| Target | Use and empty-query behavior |
|---|---|
| `search` | Default blend of high-signal claims and broad passage cards. Empty query browses recent high-signal claims only, without generic passages |
| `claims` | Structured, decision-relevant claims by executives, investors, analysts, central-bank officials, and other guests. Empty query browses recent claims |
| `passages` | Broader substantive topics not promoted to claims. Empty query browses recent passage cards |
| `pressure_points` | Stored refusal / declined-to-confirm rows, not a complete interviewer-Q&A map. Empty query browses recent refusals |
| `appearances` | Video-level title, channel, publication date, type, attribution, claim-count, URL, and relevance rows. Empty query browses the catalog |
| `coverage` | Company-level structured corpus inventory: appearance/claim counts, date span, covered channels, and attribution status. Empty query returns the inventory |

All targets accept `company`, `person`, `show` (podcast show name; returns
only podcast episodes), `channel` (YouTube channel name; returns only YouTube
videos), `appearance_type`, `claim_family` where compatible, publication-date `date_from`/`date_to`, `limit`, and
`offset`; finding targets also support `detail`.
`institution` (publisher-name substring) and `country` (ISO code, `EU` for
the European Central Bank) restrict any target to official documents;
when more than one of `show`, `channel`, and `institution` is given, rows
that match any of them are returned;
`company` matches the subject of a claim, not its publisher.
`claim_family` suppresses passage cards in `search` and cannot be combined
with `passages`. Catalog rows are not expanded by `detail=true`.

Start with `coverage` before absence claims. Use `search` plus
`sort="relevance"` for a theme sweep, then drill into `claims` and
`passages`. Use explicit `sort="newest"` plus date filters for a timeline.
If a result reaches 50 rows or says `has_more`, read the next page with
`offset=next_offset`, or narrow by ticker, person, show, channel, target,
appearance type, institution or country, claim family, or date window.
Never query the gated `transcripts` schema or ask for a full transcript.

Media findings are sourced paraphrases. Attribute person, company/ticker when
available, publication date, title/channel, and the timestamped link. For an
official document, attribute the institution, the document title, the
publication date, the `event_date` when it differs, and the document link.
`canonical_paraphrase` must stay outside quotation marks. Verify the linked
source independently when exact wording or tone is material. For coverage,
theme sweeps, timelines, cross-company work, and media-vs-earnings comparison,
read `references/report-patterns/media-intelligence.md` before searching.


### Feedback

| Tool | Purpose |
|---|---|
| `send_feedback` (`message`, `category?`) | Report a problem to the FactIQ team: `category` is `"data_issue"` (a value that contradicts the official source, wrong units/scale, duplicated or missing periods), `"tool_error"` (a tool that errors or returns malformed results), `"missing_data"` (advertised but empty, or coverage ends too early), or `"other"`. Returns an acknowledgment. |

Call this when a tool result looks broken. Write one short, specific message with the concrete
identifiers (schema, `dataset_code` / `series_id`, the SQL you ran, expected
vs. observed, the official source's value or URL if you have one). Don't
include the user's personal details or your conversation. It's one-way — the
team reviews every report, but nothing comes back — so file it and continue
with the task; never block on it.

## Orchestration workflow

0. **Interview before major forks.** If the request is broad, vague, or about
   to become a high-commitment workflow — especially a detailed report or one
   that could follow multiple scopes — interview the user before fetching data
   or spawning research subagents. Read
   `references/report-patterns/interview-step.md` and ask only the few choices
   that would materially change the work: detail level, audience, user context
   or hypothesis, priority lens, required/excluded entities, and time window.
   Pass the answers into all downstream research and assembler prompts as hard
   context. Skip the interview for direct answers, narrow quick charts, or when
   the user already gave clear scope, audience, and detail level. If the user
   does not answer, proceed with the defaults in the interview guide.
1. **Catalog first.** Call `get_data_catalog` once to get the compact
   per-schema index and the table DDL. It tells you what each schema covers,
   not every dataset. Skip schemas under `schemas_without_data`. (You rarely
   need `full=true`; use `describe_dataset` for detail on one dataset.)
2. **Find datasets, then drill in.** Call `search_datasets` to rank datasets
   across all schemas by keyword — the primary discovery step. Survey every
   schema that could be relevant before committing: for India check both
   `mospi` and `rbi`; for the US check `bls`, `bea`, `census`; energy means
   `eia`. Once a dataset looks right, `describe_dataset` for its dimensions and
   example series, then find the exact series with `search_series` (substring —
   prefer short stems like `rare`, not `rare earth`) or exploration SQL
   (`run_sql` with `explore=true`) on the `series` and `dimensions` tables.
   For multi-source stories, actually fetch data from 2+ schemas.
   Satellite-derived series live in two schemas: `portwatch` (daily shipping —
   chokepoints, ports, country trade estimates) and `satellite` (nighttime
   lights by state, lake/reservoir water levels) — see
   `references/data/schemas.md` for routing and
   `references/data/satellite.md` for the on-demand geo tool. Fire detections
   live in a third schema, `nasa_fires`, which holds raw detections rather than
   series and is shaped unlike the others — read its section in
   `references/data/schemas.md` before writing SQL against it.
   To find companies that match conditions (sector, market value,
   price-to-sales, margins, growth), run one `run_sql` query on the view
   `screener.companies` — read **Company screener** in
   `references/data/sql-guide.md` first, and state `price_as_of` in the answer.

   Eurostat Comext is the exception: country schemas contain millions of
   series, so do not explore their `series` or `dimensions` tables by text or
   dimension value. Read the **Eurostat Comext country schemas** section in
   `references/data/sql-guide.md`; it uses the small product lookup table and
   exact indexed series IDs.

   The IMF replaces each forecast in place, but the `imf` schema also keeps the
   recent earlier releases of the World Economic Outlook, the Fiscal Monitor,
   the Regional Economic Outlooks and COFER. Use them for any question about how
   a forecast has been revised. The plain series id is always the newest
   release; an earlier one is the same id with the year and month appended
   (`WEO_IND.NGDPD.A_2025OCT`), lives in a dataset whose code ends in
   `_vintages`, and carries a `release` dimension. See **IMF past releases** in
   `references/data/schemas.md`.

   **Domain report patterns.** If the question is broad and analytical —
   policy, trade, revenue, investment analysis, "what's driving X" — read
   `references/report-patterns/README.md` **before fetching**. It teaches the
   dialectical method every report follows (thesis: the headline reading;
   antithesis: the strongest contradiction, fetched, not footnoted;
   synthesis: one claim that explains both) and routes covered domains
   (bilateral trade, bilateral economic policy, monetary policy,
   fiscal-policy revenue, business formation) to a playbook of that domain's
   canonical antitheses with ready SQL. For domains without a playbook, apply
   the method directly. Either way it changes what you fetch, not just how
   you write it up. The interview step does not replace this method: it sets
   the user's preferred scope and audience first, then the report-pattern
   method determines the thesis, antithesis, synthesis, and data work inside
   that scope.

   For report-mode questions covering multiple topics, companies, or data
   sources, consider decomposing the research into parallel subagents — see
   **Subagent orchestration** below.

3. **Fetch in batches.** Once you know which series you need, issue the fetch
   calls together (multiple tool calls in one turn). Use `get_series` for 1–2
   known ids; `run_sql` with a CASE-WHEN pivot for 3+ series or joins. Keep
   results inside the 50-row cap — aggregate in SQL to the granularity a chart
   actually needs. For report tables, pick row granularity to fit the window
   (see the granularity note in `references/output/report-spec.md`).
4. **Compute deterministically.** For YoY/YTD growth, shares, rebasing, or
   merging compatible results, save the fetched `columns` and `results` as a
   local FactIQ payload and use `series_math.py`. Never inspect Claude/Codex
   transcripts or session directories to recover tool results. For other
   metrics such as per-capita values or custom ratios, write a small local
   Python calculation on the fetched values. There is no server-side code
   interpreter in this loop.
   Year-over-year is the same period one year earlier, **matched by date**,
   never by row position: for one series use `get_series` with
   `transform="yoy_pct"` (or `"yoy_diff"` for a rate); for several series or a
   merged table use `series_math.py yoy`; in SQL join on the calendar month
   (`date_trunc('month', prior.time) = date_trunc('month', cur.time) - interval '1 year'`
   — the stored day of the month varies by source, so never compare exact
   dates), never `LAG(value, 12)` (see the trap in
   `references/data/sql-guide.md`). When a tool result carries a
   `coverage_note`, the rows skip the periods in `missing_periods`: name them
   in the answer, do not interpolate, and label any aggregate that spans them
   as partial ("Q4 2025 average of two months").
5. **Recent market data.** The DB lags for very recent market/price data — use
   `get_market_data` for current quotes, commodities, and FX. For what the
   news is saying about a company, sector, or economy right now, use
   `search_news` — each business article carries keywords, a geography, and a
   one-sentence investor angle, plus the tickers it names; chase a company
   story with `get_market_data` or `search_earnings_transcripts`, and a macro
   story with `search_series`/`run_sql`.

   Three kinds of fact go out of date quickly, or are often reported wrongly
   in other sources. Take each one from the source named here:

   - **Price moves.** For any move in a share price, an index, a commodity
     or a currency, take the number from `get_market_data` price history.
     Give the two closing prices and their dates, and compute the change
     from them ("closed at $50.00 on 3 Mar and $46.00 on 4 Mar, −8.0%").
     A news article can say why the price moved. It is not the source of the
     size of the move: an article written before the market closed cannot
     know the closing price. If a news figure and the price history
     disagree, use the price history.
   - **Figures that management updates from call to call** (a business's
     share of sales, product or channel mix, guidance, targets). Before you
     call such a figure the latest one, read `coverage` for the company and
     search its most recent call for the same topic. If the most recent call
     does not repeat the figure, use the newest call that does, and say that
     later calls did not update it. Give the call date beside the figure.
     The steps are under **Latest figure** in the earnings quick reference
     below.
   - **Policy that changes often** (tariff rates, sanctions, export
     controls, subsidy rules, a central bank's policy rate). Before you state
     the rule that applies now, look for the latest change. For a policy
     rate, fetch the latest value from the warehouse (`bis`, `frb` and the
     country schemas). For other policy, use `search_news` with
     `sort="latest"`: search the name of the legal instrument as well as the
     topic (a trade-law section number, the name of a sanctions list),
     because an article about a new rule often does not name every country
     it covers. When `search_news` has no recent article on the topic, use
     the host's web search if it has one. Give the date from which the
     stated rule applies and the instrument that set it. If you cannot
     confirm that the rule is still in force, say so and give the date of
     your newest source.
6. **Satellite signals.** For crop burning, wildfires, air-quality-based
   activity (NO2/SO2/CO), smoke and dust plumes, crop condition (NDVI),
   monsoon rainfall, heatwaves, or agricultural drought — where satellite
   observation runs ahead of official statistics — use `get_geo_data`. Read
   `references/data/satellite.md` first: it covers the ten datasets, region
   syntax, the window budget (50 intervals, 200 for fires), the `grid` mode for
   mapping where a signal sits (fires, NDVI, air quality), the fires-only
   `points`, `seasons`, `resolution`, and `include_flares` controls, cloud-cover
   caveats, and required attribution. Fires are the one dataset FactIQ stores
   itself — every detection since 2012 — so a fourteen-year seasonal comparison
   is one call. Satellite data complements warehouse series; prefer curated
   series where both exist.
7. **Answer or render.** Direct-answer mode: reply with one sentence
   that states the number, period, and source. Quick-chart mode: build a
   ChartSpec from wide-format data (see `references/output/chart-spec.md`;
   required keys are `title`, `type`, `xField`, `series`, `data`, and a y-axis
   label goes in `yAxisLabel`), save it to JSON, and return the JSON path with
   a short statement of what the chart shows. Report mode: build and save a
   report object (see `references/output/report-spec.md`) and return the
   findings and the local JSON path.

   When an answer reports a company's debt, give the part due within twelve
   months and the rest as two figures, with the date of the next large
   maturity. In US filings the concept "Long term debt" includes the part
   due within a year. Look in `search_company_filings` for the current
   portion and for the repayments due in the next twelve months (for
   example `query="debt"`) before you describe debt as long term.

## Subagent orchestration

For report-mode questions that span multiple distinct topics, companies, or data
sources, decompose the work into parallel subagents. This does two things:
each research thread gets a full, focused context instead of competing for
attention in one serial pass, and the report-assembly step gets the spec
loaded directly in its prompt so it never guesses at field names.

Before spawning subagents for a broad or underspecified request, run the
interview described in
`references/report-patterns/interview-step.md` unless the user already gave
clear scope, detail level, audience, and priority lens. Include the interview
answers in every research-agent prompt and in the report-assembler prompt so
the final artifact reflects the user's context instead of only the generic
version of the question.

### The interview runs in the main context

Run the interview yourself, in the main conversation — a background subagent
cannot put questions to the user. Its job is to clarify the decision,
audience, scope, output shape, and success criteria and produce a compact
brief before any data is fetched or chart schemas are chosen. Research
subagents run only after the brief and the relevant report pattern are known.

**Do NOT use subagents** for quick-chart mode or single-topic questions — the
overhead is not worth it. The decision point is right after step 2 of the
orchestration workflow: once you have done the catalog lookup and initial
dataset discovery, you know whether the question decomposes into 2+ independent
research threads. If it does, fan out.

### Research subagents

Spawn one Agent call per research thread. Each agent inherits the skill's
FactIQ MCP tools, so it can discover, fetch, and compute on its own. Give each
agent a tightly scoped prompt and tell it to return structured findings — not
prose and not a final artifact.

Agent prompt template (adapt the specifics per thread):

```
You are a FactIQ research agent. Answer one sub-question and return structured
findings only. Do not assemble the final chart or report.

Sub-question: {sub_question}

Relevant schemas/datasets (from the parent's catalog step): {hints}

Constraints: every tool result is capped at 50 rows, so aggregate in SQL to
the grain the finding needs; compute derived metrics (YoY, ratios, indices)
yourself from the fetched values. Year-over-year is the same period one year
earlier matched by date (get_series with transform="yoy_pct", series_math.py
yoy, or a SQL join on date_trunc('month', time)), never a 12-row offset or an
exact-date comparison. Report any
coverage_note / missing_periods from the tool results in your findings.

Return your findings as a structured block:

FINDINGS:
- sub_question: (echo it back)
- series_used: [{schema, series_id, title}, ...]
- sql_queries: [the exact SQL you ran, formatted multi-line]
- data: [{columns: [...], rows: [...]}, ...] — the actual fetched/computed values
- key_insights: [1-3 sentences stating what the data shows, with numbers]
- chart_suggestion: {chart_type, title, x_column, y_columns, units}
```

Launch the agents in parallel — multiple subagent calls in one turn, each
with its own research prompt and a short name such as
`research-supply-chain`, `research-pricing`, `research-demand`.

Each agent runs independently and returns its findings block. Wait for all of
them before proceeding to assembly.

### Report assembler subagent

After all research is complete, spawn a single report-assembler agent. Its
prompt must contain two things: (1) the full content of `references/output/report-spec.md`,
so the assembler has the spec without needing the plugin path, and
(2) all the research findings from the previous step.

Before spawning the assembler, read `references/output/report-spec.md` yourself with
the Read tool. Then embed its entire content in the assembler's prompt.

Agent prompt template:

```
You are a FactIQ report assembler. Build a complete report object and save it.
Do not do data discovery or fetching; all data is provided below.

USER QUESTION: {original_question}

=== REPORT SPEC (from references/output/report-spec.md) ===
{paste the full content of references/output/report-spec.md here}
=== END REPORT SPEC ===

=== RESEARCH FINDINGS ===
{paste all findings blocks from the research agents, labeled by thread}
=== END RESEARCH FINDINGS ===

Instructions:
1. Design 2-5 sections. Each section makes one claim its chart(s) prove.
2. Chart titles state the finding with numbers, not the topic.
3. Narratives are plain text — no markdown formatting.
4. Every chart must have columns, data (from the findings above), x_column,
   y_columns (for line/bar), sources, and lineage.
5. Lineage code must be formatted multi-line SQL/Python with real newlines.
   series_refs must list every series the step used.
6. Save the full report object to JSON.
7. Return the JSON path and the key findings.
```

Launch the assembler as one subagent (name it `report-assembler`) with the
spec-plus-findings prompt.

The assembler has the full spec in context, so it builds the report object,
saves the JSON, and returns the local path plus the key findings.

### Example decomposition

Question: "How is the US EV market evolving — supply chain, pricing, and demand?"

After step 2 (catalog + discovery), you identify three independent threads:

| Thread | Sub-question | Schemas |
|---|---|---|
| Supply chain | What does US EV battery/component production look like? | `census`, `bea` |
| Pricing | How have EV prices and average selling prices changed? | `bls` (CPI), market data |
| Consumer demand | What are EV sales and registration trends? | `bts`, `bea`, market data |

Spawn three research agents in parallel. When all return, spawn one assembler
agent with the spec and all three findings blocks. The assembler builds a
3-section report, saves it, and returns the path and findings.

### When NOT to use subagents

- Quick-chart mode (single metric, single chart).
- Single-topic questions even in report mode ("How has US unemployment evolved
  since 2020?" — one thread, no decomposition needed).

For these cases, do the research and build the output in the main context.

## Detailed reports

A report is a structured local research output: a bulleted summary, sections
that pair narrative with charts, and methodology notes. Author every chart row
and narrative claim from data fetched in this session. The JSON format and a
worked example are in `references/output/report-spec.md`. For reliable assembly,
load that full file into a dedicated report-assembler subagent.

Ground rules:

- **2–5 sections, 1–2 charts each** is the normal size. The format allows up to 12
  sections, 16 charts). Each section should make one claim its charts prove.
- **Chart titles state the finding** ("Health care added 652k jobs in 2024 —
  triple tech's losses"), not the topic ("Jobs by sector").
- **Narratives are plain text.** Keep them short and direct.
- **Cite sources and lineage.** Every chart must identify the datasets and the
  exact SQL or computation used. Format SQL and Python with real newlines. List
  every series used in `series_refs`.
- **Do not pad.** If the data only supports one chart, build a quick chart
  instead of inflating a report.
- **Broad analytical questions get the dialectic.** Follow the
  thesis → antithesis → synthesis method in
  `references/report-patterns/README.md`: sections that only restate the
  headline reading are an unfinished report. Covered domains (bilateral
  trade, bilateral economic policy, monetary policy, fiscal-policy revenue,
  business formation) must additionally meet the required coverage in the
  playbook the README routes to — do not reduce them to the easiest single
  chart.

Check the report object against `references/output/report-spec.md`, save it to
JSON. Return the report findings and the local JSON path.

## Context budget — the 50-row cap

Every row-returning MCP tool (`run_sql`, `get_series`) returns **at most 50
rows**, and there is no "give me everything" option — by design. The cap keeps
results context-sized, so you do **not** stage data to disk to protect your
context; you take the tool result directly.

There is one exception. In the `nasa_fires` schema a row is a single satellite
fire detection, which belongs to no series and carries no value to average, so
the rows themselves can be the answer. There `run_sql` accepts `page` and walks
the result 50 rows at a time. Give the query an `ORDER BY`, or the pages will
not line up. No other schema accepts `page`.

When a result comes back `"truncated": true`, there is more data and your move
is to **aggregate or compute it in SQL**, not to try to fetch the raw rows:

- Roll a long daily/monthly series up with `GROUP BY date_trunc('month', time)`
  (or quarter/year) — a chart wants a few hundred points at most, and 50
  aggregated points usually says everything.
- Return a SUM / AVG / rank / ratio instead of the underlying rows.
- For one series, window it with `get_series(..., from_year=, to_year=)`, or
  make a few windowed calls and stitch them.

Whatever you chart or report has to be the aggregated result you bring back —
which is also all it needs.

## Errors and limits

- **MCP tool unavailable / auth error** — the FactIQ MCP is not connected. Tell
  the user to authorize it (Claude Code: `/mcp` → factiq; Codex:
  `codex mcp login factiq`).
- **429** — either the 1 request/second rate limit or the monthly tool-call
  quota. The error states when it resets. Do not re-fetch data you already have.
- **403** — that schema is admin-restricted for this account; drop it.
- **SQL errors** come back in the tool result as an `error` (syntax errors,
  timeouts, bad column names). Revise the query and rerun.
- **Zero rows** — your filter was too narrow. Broaden it yourself (see
  `references/data/sql-guide.md`). `auto_retry=true` opts into a server-side LLM
  reviser, but you can usually revise better and cheaper yourself.
- **`coverage_note` on a result** — not an error: the rows skip the periods in
  `missing_periods` (a month the source never published, or one the query
  window cut off). Any period-over-period figure built with a fixed row
  offset (`LAG(value, 12)`, `shift(12)`, "the row 12 back") over those rows
  is wrong for the 12 rows after each gap (a forward offset: the 12 rows
  before it). Recompute by matching dates, name the missing periods in the
  answer, and label partial aggregates as partial.
- **SQL timeout** — statements are capped at 30s. Filter on indexed columns
  (`series_id`, `dataset_code`) instead of scanning titles, and never
  pattern-match `series_id` on `data_points` — resolve ids from `series` first
  (see the pitfall in `references/data/sql-guide.md`). For `eu_comext_*`, do
  not retry a dimension scan; use `eu_comext_lookup.product_codes` and exact
  IDs as described in the Comext section of that guide.
- **Anything that looks broken on FactIQ's side** — a value that contradicts
  the official source, wrong units, missing periods, an advertised dataset
  that returns nothing, a tool that keeps erroring — report it with
  `send_feedback` (see **Feedback** above), then work around it and continue.
  The FactIQ team reviews every report and fixes what it can.

## References

**`references/data/`** — the data layer:

- `schemas.md` — what lives in each schema. The `get_data_catalog` tool is the
  live, authoritative version; `search_datasets` / `describe_dataset` drill
  into individual datasets on demand.
- `sql-guide.md` — table structure, query idioms, pitfalls (frequency
  literals, national vs sub-national, pivots, tabular data).
- `satellite.md` — the `get_geo_data` satellite tool: datasets and their
  economic reading, region syntax and coverage, window budgeting, the
  spatial `grid` mode, the fires-only `points` and `seasons` modes and the
  `resolution` / `include_flares` controls, cloud/quality caveats,
  attribution requirements.

**`references/output/`** — local output formats:

- `chart-spec.md` — ChartSpec format, chart-type selection, and a worked example.
- `report-spec.md` — report JSON format: sections, per-chart fields,
  sources, lineage, limits, and a worked example.

**`references/report-patterns/`** — how to think about broad analytical
questions. Start at `report-patterns/interview-step.md` when the request is
vague or high-commitment; it defines the interview that clarifies scope and
audience before data work. Then read
`report-patterns/README.md`: it teaches the dialectical method (thesis →
antithesis → synthesis) that every report follows and routes covered domains
(bilateral trade, bilateral economic policy, monetary policy, fiscal-policy
revenue, business formation, and any added later) to a playbook of that
domain's canonical antitheses with ready SQL. For uncovered domains —
investment analysis, general macro — the README shows how to apply the method
directly.
