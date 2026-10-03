---
name: trading-archive
description: Build, run, troubleshoot, or refine Trading Archive, especially the bundled `apps/trading-archive-bar` macOS menu bar app and its feed-ingest helper. Use when Codex needs a dependable trading research archive instead of ad hoc finance tabs and half-lost bookmarks.
---

# Trading Archive

Use this skill when the user wants a reliable archive of trading or macro research articles, a better way to browse market reading later, or help building and refining the matching macOS menu bar app.

Default product shapes:
- a native `MenuBarExtra` app that ingests RSS or Atom feeds, saves a local archive, and lets the user search, favorite, and reopen trading reads
- a deterministic CLI helper that fetches public feeds and emits a reading queue or JSON archive snapshot

## Quick Start

1. Lock the source scope first: RSS or Atom feeds, saved URLs, or a local archive file.
2. Prefer public or user-authorized feeds only. Do not assume access to paywalled content.
3. Run `bash scripts/run_trading_archive.sh doctor`.
4. Run `bash scripts/run_trading_archive.sh inspect` before editing the app.
5. Use `bash scripts/run_trading_archive.sh fetch --feed-url https://example.com/feed.xml --limit 20` for deterministic ingest or a shareable archive snapshot.
6. If the user wants a product surface, open or refine `apps/trading-archive-bar/`.
7. Use `bash scripts/run_trading_archive.sh open` to jump into Xcode when you need the local project open.
8. Use `bash scripts/run_trading_archive.sh generate` after changing `apps/trading-archive-bar/project.yml`.
9. Use `bash scripts/run_trading_archive.sh typecheck` for a fast Swift source sanity pass before a full build.
10. Use `bash scripts/run_trading_archive.sh test` after model, service, or UI changes.
11. Use `bash scripts/run_trading_archive.sh run` when you need the menu bar app relaunched.
12. Return either a `trading-archive-digest`, `reading-queue`, `source-health-report`, or `app-refresh-plan`.

## Accepted Inputs

- one or more RSS or Atom feed URLs
- a time window such as `today`, `7d`, `30d`, or `all`
- a query for symbols, setups, themes, or macro topics
- whether the user wants a concise queue, a richer digest, source diagnostics, or app changes
- a maximum number of surfaced reads
- optional saved article URLs or archive JSON from earlier runs

## Output Artifact

Primary artifacts:
- `trading-archive-digest`
- `reading-queue`
- `source-health-report`
- `app-refresh-plan`

Default `trading-archive-digest` sections:
- Date and archive basis
- Best resurfaced reads
- Why each article matters now
- Source links
- Feed freshness notes

Default `reading-queue` sections:
- Priority reads
- Secondary reads
- Theme tags or symbols
- Source links

Default `source-health-report` sections:
- Configured feeds
- Live or failed status
- Article counts
- Follow-up notes

## Workflow

### Keep Sources Honest

- Use only public feeds or user-provided URLs.
- Do not fabricate article bodies, analyst claims, or paywalled details.
- If a source fails, label it as failed or cached instead of pretending it loaded.

### Build A Dependable Archive

- Prefer feed ingest plus local cache over one-off browsing.
- Merge and deduplicate by canonical link whenever possible.
- Keep titles, timestamps, and source names intact.
- Use the runner or helper script when a deterministic, shareable archive snapshot is better than free-form browsing.

### Shape The Reading Experience

- Favor a queue that helps the user revisit ideas, not just raw chronology.
- Let the user filter by topic, symbol, or favorite status.
- Keep the menu bar experience compact and keyboard-friendly when editing `apps/trading-archive-bar/`.

### Handle Failure Cleanly

- If some feeds succeed, return partial results and call out failures.
- If all feeds fail and no cache exists, say so directly.
- If a feed is valid but empty, make that explicit in the output.

### Mac Product Shape

- Prefer a polished `MenuBarExtra` layout with:
  - a compact top-bar label showing archive activity
  - refresh, copy queue, and settings actions
  - feed-status badges
  - search and time-window filters
  - a scrollable queue of saved articles with favorite toggles
- Keep the popover useful when offline by preserving a local cache.

### Work The Bundled App First

- Read `references/project-map.md` before editing the app.
- If the task changes project settings or app metadata, inspect `apps/trading-archive-bar/project.yml` and `apps/trading-archive-bar/TradingArchiveBarApp/Info.plist` first.
- Prefer the local runner before typing `xcodegen` or `xcodebuild` manually.
- Use `typecheck` when you want the fastest source-level validation before a full build or test run.
- Run `test` after ingest, cache, export, or menu bar UI changes.

### Safety Boundaries

- This skill is for research organization, not trading advice.
- Do not present surfaced articles as recommendations to buy or sell.
- Keep summaries factual and linked back to source URLs.
- Respect robots, auth, and paywall boundaries.

## Example Prompts

- `Use $trading-archive to fetch these RSS feeds, dedupe the latest macro and equities articles, and give me a six-item reading queue.`
- `Use $trading-archive to turn this saved archive JSON into a concise digest of the best trading reads from the last 7 days.`
- `Use $trading-archive to audit these sources, tell me which feeds are stale or broken, and suggest a cleaner archive setup.`
- `Use $trading-archive to build or refine a native macOS menu bar app for browsing archived trading articles with search, favorites, and cached fallback.`

## Resources

- `scripts/run_trading_archive.sh`: local doctor, inspect, fetch, generate, open, typecheck, build, test, and run helper for `apps/trading-archive-bar`
- `scripts/fetch_trading_feeds.py`: deterministic RSS and Atom ingest helper
- `references/project-map.md`: app shape, main files, and validation checkpoints
- `references/product-spec.md`: app shape, fallback behavior, settings UX, and artifact expectations
- `../../apps/trading-archive-bar/`: the matching native menu bar app codebase
