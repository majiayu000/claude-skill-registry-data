---
name: alpaca-trading
description: Work safely in the Trading repository for Alpaca helpers, backtesting, journaling, scheduling, and related PowerShell modules. Prefer additive changes, preserve existing trading logic unless the user asks otherwise, and default to paper-trading-safe guidance.
version: 1.1.0
---

# Alpaca Trading

## Intent

Support safe paper trading, Alpaca automation, broker workflow analysis, and Trading repo changes without increasing live trading risk.

## Do Not Use When

- Do not use for financial advice, guaranteed performance claims, live order execution without explicit user instruction, or unrelated trading platforms.
- Required context is missing and cannot be reasonably inferred.
- A more specific skill in this repo is a better match.

Use this skill when the user is working in the `Trading` repository on Alpaca-connected scripts, backtesting workflows, journaling, scheduling, or reusable PowerShell Alpaca modules.

## Trigger When

- The user mentions the `Trading` repo, Alpaca scripts, paper trading, backtesting, journaling, scheduler jobs, or Alpaca PowerShell modules.
- The task touches `Alpaca/`, `Backtesting/`, `Journal/`, `Scheduler/`, `src/`, `Tests/`, `rsi_macd_bot/`, or `btc-signal-executor/`.
- The user wants to build, extend, debug, document, test, or review repo workflows around Alpaca trading.

## Repo Shape

The current repository is a mixed Python and PowerShell project with these main areas:

```text
Trading/
|-- Alpaca/
|-- Backtesting/
|-- Journal/
|-- Scheduler/
|-- src/
|-- Tests/
|-- rsi_macd_bot/
`-- btc-signal-executor/
```

Use the existing structure instead of inventing a new module layout.

## Default Behavior

- Preserve what already exists unless the user asks for a larger redesign.
- Prefer additive scaffolding over speculative rewrites of trading logic.
- Default to paper-trading-safe patterns and make live-trading risk explicit.
- Keep API secrets in environment variables or existing repo config flows, never hardcoded.
- Align with the repo's existing GitHub Spec workflow for non-trivial changes.

## Workflow

1. Identify which existing repo area the change belongs to.
2. Read the nearby README, script, or module before proposing changes.
3. Reuse current patterns for Python, PowerShell, logging, and tests.
4. For non-trivial work, follow the repo workflow: requirements, spec, plan, tasks, implementation, audit, regression test.
5. Prefer paper-trading examples unless the user explicitly asks for live-trading support.
6. If live-trading code is requested, require explicit confirmation patterns and keep the safety guard intact.
7. Update docs and tests alongside behavior changes.

## Safety Rules

- Default to the Alpaca paper endpoint unless the user explicitly requests live trading.
- Never remove a live-trading confirmation guard from real-money scripts.
- Treat AI analysis as advisory only. Do not let model output directly trigger order placement without deterministic code checks.
- Log trade actions and failures using the repo's existing logging and journal patterns.
- Call out when a request would move from paper trading into live execution risk.

## Implementation Notes

### Python And PowerShell

- The repo is mixed-stack. Do not force everything into one language.
- `Alpaca/` contains existing paper-trading helpers.
- `src/` contains reusable PowerShell Alpaca modules such as auth, config, market data, risk, orders, positions, and account helpers.
- `Tests/` contains Python and PowerShell verification coverage.

### Live Trading Guard

If a script can send live orders, include an explicit confirmation gate and make the live path opt-in.

```powershell
param(
    [switch]$LiveTrading
)

if ($LiveTrading) {
    $Confirm = Read-Host "Type CONFIRM to proceed with live trading"
    if ($Confirm -ne "CONFIRM") {
        exit 0
    }
}
```

### AI Coaching Pattern

If AI analysis is added, keep it advisory:

- AI returns a labeled assessment such as `BULLISH`, `BEARISH`, or `NEUTRAL`
- deterministic code applies risk checks and order rules
- model output alone must not place an order

### Alpaca Capability Profile

Tailor repo advice to how Alpaca actually behaves rather than generic broker assumptions:

- Paper and live use the same API shape but different endpoints; paper fills are simulated and optimistic, so backtest and paper results overstate live fill quality, especially for market orders in thin symbols.
- Fractional shares trade market-only and have order type restrictions; do not propose fractional limit logic.
- Bracket and OCO orders are supported but legs cannot be amended freely; cancel and replace is the realistic pattern.
- Crypto trading has different fee, precision, and minimum rules than equities; do not reuse equity assumptions in `btc-signal-executor/`.
- Equity market data on the free tier is IEX-only and delayed for some uses; flag when a strategy assumes SIP-quality data the account may not have.
- PDT rules apply to margin equity accounts under $25k; day trading logic should check account status instead of assuming.

When a proposal depends on an Alpaca behavior not listed here, verify it against current Alpaca docs instead of assuming.

### Order Lifecycle Checklist

Before proposing or reviewing a change that touches order placement, walk the full lifecycle:

- **Entry**: validated symbol, side, quantity, and order type; idempotency or duplicate-submit protection; behavior when the market is closed
- **Open order**: what happens to unfilled limit orders at end of day; time-in-force is explicit, not defaulted silently
- **Partial fills**: position sizing, journaling, and exit logic handle a partially filled entry without double-ordering
- **Exits**: stop and target exist before or at entry (bracket or managed); exit logic survives a restart with positions already open
- **Cancel/replace**: replaces are atomic from the strategy's view; stale order IDs are not reused
- **Failure paths**: rejected orders, API errors, and timeouts are logged to the journal and do not leave untracked positions

A change is incomplete if it improves one lifecycle stage and silently breaks another.

## Regression Test Matrix

Map the kind of change to the test passes that must run before it ships:

| Change touches | Run |
| --- | --- |
| `src/` PowerShell modules | Pester tests in `Tests/`, plus a paper-endpoint smoke call for the touched module |
| `Alpaca/` helpers | Python tests in `Tests/`, paper-endpoint smoke test |
| Order or risk logic anywhere | Full `Tests/` suite plus a paper trade round trip: place, verify, cancel |
| `Backtesting/` | Backtest determinism check: same data in, same results out, before and after |
| `Scheduler/` | Dry-run the scheduled job manually and verify journal output |
| `rsi_macd_bot/` or `btc-signal-executor/` | That bot's own tests plus a paper session observed end to end |

If a needed test does not exist, write it as part of the change rather than noting it as a gap.

## Constraints

- Do not invent folders like `PaperTrading`, `LiveTrading`, `TradeJournal`, or `AICoaching` if the work belongs in the current repo structure.
- Do not hardcode credentials.
- Do not rewrite business logic just to modernize style.
- Do not describe the repo as a Claude-only system; it is a general trading repo with Claude-relevant integrations.

## References

- Root repo guide: `Trading/README.md`
- GitHub Spec baseline: `Trading/specs/001-core-trading-foundation/`
- Copilot instructions already present in the repo: `Trading/.github/copilot-instructions.md`

## Validation Checklist

- [ ] Repo area matches the real Trading repository layout
- [ ] Paper trading is the default path in examples and guidance
- [ ] Live trading remains explicit and guarded
- [ ] Secrets are sourced from environment variables or existing config flows
- [ ] Changes preserve existing trading logic unless requested otherwise
- [ ] Docs and tests are updated when behavior changes

## Help And Examples

If the user is not sure how to use this skill, asks what it needs, or asks for examples:

- Explain in plain language what this skill can do.
- Tell the user the minimum input needed for a useful first pass.
- Show the example prompts below.
- Offer the fastest next prompt the user can send.

Minimum useful input:

- A trading goal, repo context, or strategy question plus any symbols, timeframes, or risk rules that matter.

Example prompts:

- `Use alpaca-trading to review my Trading repo and tell me the safest way to add bracket orders.`
- `Help me build an Alpaca paper trading workflow for SPY with clear entry, exit, and risk rules.`
- `Show me how to use this skill for a repo level trading automation plan.`

