---
name: tradingview-indicator
description: Build, modify, document, compile, install, visually verify, and publish TradingView indicators or strategies in the latest stable Pine Script. Use when the user invokes $tradingview-indicator or asks Codex to create, repair, migrate, test, backtest, add alerts to, install, or publish a Pine Script or TradingView indicator/strategy.
---

# TradingView Indicator Builder

Create production-quality Pine artifacts with a local canonical copy and evidence from the TradingView bridge. Keep the workflow practical for a trader who wants to describe the idea, not restate Pine or tool instructions.

Match the language of the user's request for conversation and generated user-facing artifacts. If the request mixes languages, use the dominant language. Use another language only when the user explicitly requests it.

## Resolve the task

1. Read `references/local-workspace.md` if it exists. Treat it as private machine configuration.
2. Locate the canonical local source before editing an existing script. Do not fork silent duplicates.
3. Ask only about ambiguity that materially changes the indicator. Otherwise default to:
   - `indicator()`, not `strategy()`,
   - the chart timeframe unless another timeframe is specified,
   - confirmed-bar logic for signals,
   - input labels, concise tooltips, documentation, comments, and alert field names in the user's language,
   - no order placement or exchange integration.
4. Translate screenshots and informal descriptions into explicit rules: setup, invalidation, confirmation, lifetime of drawings, timeframe, alerts, and visible output.

## Use current Pine standards

- For a new script or migration, verify the newest stable Pine version in official TradingView documentation. Use `//@version=6` while v6 remains current.
- Read `references/pine-standards.md` when implementing higher-timeframe data, alerts, strategies, publication, or non-repainting signals.
- Follow the official Pine style guide. Prefer small named functions and typed variables over duplicated blocks.
- Group inputs by feature. Expose only settings that help the user; hide implementation noise behind sensible defaults.
- Manage `line`, `label`, `box`, array, request, plot, execution, and memory limits deliberately. Delete or recycle obsolete drawings.
- Do not present a level, zone, indicator, or projection as a guaranteed entry.

## Prevent misleading behavior

- Use closed-bar confirmation when the rule depends on candle closure.
- For confirmed higher-timeframe values, use a non-repainting request pattern. Never use future-looking `barmerge.lookahead_on` without a one-bar historical offset.
- If the user explicitly wants intrabar/early signals, label that mode as repainting or provisional in both settings and documentation.
- Keep historical and realtime behavior consistent. Do not hide unfavorable signals or tune retrospectively to a screenshot.
- Build a separate `strategy()` companion when genuine backtesting is requested. Do not call visual inspection a backtest.
- In strategies include commission, slippage, position sizing, date range, and unambiguous entry/exit rules. Report sample size and limitations alongside results.

## Work locally first

Create or update one project folder under the configured indicator root. If no private local configuration exists, use `./tradingview-indicators` in the current workspace. For a new indicator use:

```text
indicator-slug/
├── indicator-slug.pine
├── README.md
└── CHANGELOG.md        # only when version history is useful
```

Use stable ASCII identifiers in Pine code. Match comments and working documentation to the user's language. The `.pine` file is the canonical source. Keep `README.md` synchronized with:

- what the script detects and what it does not,
- installation steps,
- visible elements and settings,
- alert creation and message format,
- repainting/confirmation behavior,
- current limitations and version.

Use `apply_patch` for file edits. Preserve unrelated user files and changes.

## Prefer the TradingView bridge

Use the dedicated TradingView MCP before any generic UI control:

1. Run `tv_health_check`; use `tv_discover` or `tv_launch` only if needed.
2. Call `chart_get_state` once and reuse the returned state and study IDs.
3. Use `capture_screenshot` for visual context.
4. Inject the complete canonical source with `pine_set_source`.
5. Compile with `pine_smart_compile`; inspect `pine_get_errors` and console output when needed.
6. Save through `pine_save` only after successful compilation.
7. Verify visible lines, labels, boxes, and tables with the targeted `data_get_pine_*` tools and `study_filter`.
8. Close the Pine Editor after completion when it obstructs the chart.

Avoid `pine_get_source` for large scripts when a canonical local copy exists. Do not use `verbose=true`; request summarized OHLCV data. Use Computer Use only as a last resort when the bridge cannot perform the required action and the user explicitly allows it. If live access is unavailable, finish and validate the local artifact as far as possible and state exactly what remains unverified.

## Design alerts economically

- Default to one dynamic `alert()` router when several event types should fit under one TradingView alert slot.
- Include symbol, timeframe, event, direction, level, price, and bar time in machine-readable messages when appropriate.
- Use distinct `alertcondition()` entries only when separate items in the Condition menu are genuinely useful.
- Explain that code only exposes alert events; the user must create the running alert in TradingView.
- After script or input changes, remind the user that existing alerts retain a snapshot and must be recreated.

## Validate before handoff

Require proportionate evidence:

1. local source and documentation are synchronized,
2. Pine compilation has zero errors,
3. no runtime error is visible,
4. drawings align with the intended candles and prices,
5. confirmed signals do not disappear unexpectedly after reload,
6. object counts remain bounded,
7. settings and alert text are understandable,
8. changes are checked on the requested symbol/timeframe and, for reusable scripts, at least one additional representative context.

Do not claim installation, saving, compilation, backtest quality, or TradingView verification without direct evidence.

## Publish safely

Publish to GitHub or TradingView only when explicitly requested.

- Scan the exact public files for secrets, webhook URLs, credentials, account identifiers, and private system details.
- Default public repository metadata, public README files, release notes, and the published skill documentation to English. This does not override the user's language for indicator settings, tooltips, alerts, or working documentation.
- Publish only Pine source, user documentation, license, and safe examples.
- Keep local configuration and private research out of Git.
- Use an honest description, screenshots with clean charts, known limitations, and a not-financial-advice statement.
- Follow TradingView publication rules when publishing in its Community Scripts catalog.

End with the canonical file paths, Pine version, compile/runtime results, live-install status, tests performed, limitations, and any alert or publication steps still required.
