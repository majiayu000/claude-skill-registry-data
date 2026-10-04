---
name: kelly-invest-stock
description: Build and operate a Busabase-backed mainland China A-share strategy experiment desk with a bundled local Hono App-in-Skill, evidence-backed strategy research, strategy-level L1/L2/L3 manual maturity approvals, one CNY virtual ledger per strategy, and dated strategy backtest reports. Use when the user invokes $kelly-invest-stock or /kelly-invest-stock, wants to define or compare A-share strategies, inspect a strategy and its virtual book, record research evidence, manually approve strategy maturity, or review dated backtests, drawdown, and contribution to the total book. It never connects to a brokerage, places orders, moves money, or presents generated analysis as personalized investment advice.
metadata:
  category: invest
  tags:
    - risk:read-only
    - surface:busabase
    - surface:a-share
  busabase:
    template: true
    folderSlug: kelly-invest-stock
    resources:
      - strategies
      - ledger-accounts
      - ledger-positions
      - strategy-backtests
      - strategy-reviews
    risk: read-only

---

# Kelly Invest Stock

Operate a compact strategy experiment desk. Keep the first screen centered on a
large strategy table: concise thesis, maturity label, account NAV, return,
benchmark, drawdown, cash, and virtual positions. Open a row for the complete
strategy and ledger detail.

## Mandatory Dependencies

Before changing the app:

1. Read and follow `$kelly-app-skill-creator` for product behavior, responsive UI,
   and the canonical local `content/kelly-invest-stock-app/` artifact.
2. Read and follow `$busabase` for connection, target Space, ChangeRequests,
   review, and merge behavior.
3. Read and follow `$busabase-app-creator` for resource modeling, AirApp runtime,
   security, validation, and deployment.
4. Read `references/stock-sdk.md` before changing market-data ingestion.

If a dependency is unavailable, continue safe local artifact work but stop before
the unavailable deployment or Busabase operation. Never create a second
persistent backend.

## Product Boundary

- Limit the product to mainland China A shares. Preserve six-digit stock codes,
  show Chinese security names as the primary identity, and use CNY for every
  virtual account, price, market value, P/L, and portfolio total.
- Keep every account, position, return, stage, and regression result virtual.
  Never connect to Futu or another brokerage, create order UI, or call a trading
  API.
- Give every strategy exactly one virtual account and default every new strategy
  to `L1`.
- Treat `L1`, `L2`, and `L3` as manual labels on the whole strategy, never on an
  individual stock:
  - `L1`: default basic observation;
  - `L2`: manually marked advanced observation;
  - `L3`: manually marked high-confidence observation.
- Do not copy the live-trading meaning of L2/L3 from `invest-ui`. In this skill,
  changing a label never changes execution mode, account type, or capital.
- Keep thesis, evidence, assumptions, confidence, and invalidation separate. A
  label or score is not a recommendation.
- Use exact-pinned `stock-sdk@2.4.0` only in reviewed trusted execution. Browser
  code performs no public market fetch.

## Data And Modes

- Use Busabase as the persistent source by default. A normal invocation or URL
  must never silently switch to Demo.
- Enter Demo only when the user explicitly asks to open or update Demo. Demo data
  is deterministic, clearly labeled, and not persistent.
- Use 10 recognizable investor-style Demo strategies such as Buffett, Munger,
  Duan Yongping, Peter Lynch, Howard Marks, Fisher, Graham, Li Lu, Templeton, or
  Soros style examples. Build every Demo basket from clearly labeled A-share
  examples and use a fixed CNY 1,000,000 nominal account per strategy.
  Label them as style reproductions; never imply actual holdings, endorsement, or
  current advice.
- Read and write persistent state through `busabase-sdk`. Stage changes use a
  `records.changeRequest` update to the strategy record's `status` field and a
  dated approval record containing the human reason and account snapshot. Never
  persist stage changes in browser storage or local files.
- Keep Busabase record page size inside the provider, at no more than the API's
  supported maximum. Follow `nextCursor` until exhaustion and never put transport
  pagination in a Base declaration or treat one page as the complete dataset.
- Offer the deterministic classroom seed only in a completely empty Busabase
  workspace. Submit one reviewable bulk ChangeRequest per Base without automatic
  merge; the user or Space reviewer decides whether to merge it.

## Core Resources

Keep five application-owned Bases under one application Folder:

- `strategies`: name, key, family, `status`, thesis, selection rule,
  invalidation rule, review cadence, next review time, benchmark, and confidence.
- `ledger-accounts`: one virtual account per strategy with nominal capital, NAV,
  cash, benchmark return, maximum drawdown, update time, and return baseline date.
- `ledger-positions`: virtual quantity, entry price, reference price, market
  value, weight, price source/time, strategy key, six-digit A-share code, and
  Chinese security name.
- `strategy-backtests`: dated strategy-level reports with window start/end,
  methodology, coverage, benchmark, total return, CAGR, volatility, Sharpe,
  maximum drawdown, benchmark-relative return, and bias/source notes.
- `strategy-reviews`: dated research sources, source freshness, supporting and
  counter evidence, account snapshots, manual stage decisions, reviewer, reason,
  and the associated ChangeRequest ID.

Provision a new empty workspace lazily through one Busabase structure
ChangeRequest, re-read the Folder, and use only validated materialized IDs. For
an owned older schema, submit only declared suffix fields through reviewable field
ChangeRequests, wait for approval, then update resource metadata. Reject reordered,
changed, or otherwise incompatible fields. Ignore legacy app-owned resources
outside this declaration; never delete or adopt them implicitly.

## Operating Loop

### Research

Define a strategy's thesis, selection rule, invalidation rule, benchmark, review
cadence, next review time, and virtual account before evaluating it. Preserve
research source, source date, supporting evidence, counter evidence, and data
freshness in a dated review record.

### Plan

State the evidence needed for the next review. New strategies remain L1. Treat an
L2/L3 change as a human maturity judgment, not an automated promotion or trading
authorization.

### Action

Allow reviewed research updates, virtual-ledger records, and mouse-driven manual
stage marking. Before promotion, require complete strategy rules, one account with
a baseline date, dated research evidence, quote provenance, and reconciled NAV.
Require a human reason and confirmation for every stage change. Send persistent
stage changes through Busabase ChangeRequest, write the approval timeline record,
and reload canonical records after materialization.

### Retrospective

Compare virtual return, benchmark, maximum drawdown, and contribution to the
whole book. Record whether thesis or process failed before changing a strategy's
rules.

## UI Contract

- Use a fixed desktop sidebar with Strategy, L1, L2, L3, Regression, and Help &
  Settings. Do not add a separate Virtual Ledger tab.
- Make the Strategy route a large full-width table that combines strategy summary
  and ledger reality. Clicking the entire row opens Strategy Detail.
- Put the manual L1/L2/L3 segmented control and compact performance summary at
  the top of Strategy Detail. Below it, use shareable hash-routed tabs in this
  order: `组合持仓`, `研究与审批`, `策略逻辑`, `回测表现`.
- Open `组合持仓` by default. Make it the dominant detail surface with account
  NAV/capital/cash/P&L, invested-versus-cash allocation, and a full-width table
  showing Chinese security name, six-digit code, quantity, virtual entry price,
  reference price, virtual market value, portfolio weight, and virtual P/L. Keep
  cash visible as part of the portfolio rather than hiding it in a summary.
- Make L1/L2/L3 routes filter strategies, not stocks.
- Sort the default strategy table by next review time with missing or overdue
  review dates first. Do not rank the default workflow by return or confidence.
- In `研究与审批`, show dated positive and counter evidence, source provenance,
  freshness, stage decisions, human reasons, reviewer, snapshot metrics, and
  ChangeRequest IDs. Clearly state that Demo approvals reset on full refresh.
- Treat Strategy/L1/L2/L3 navigation as an in-memory strategy filter after the
  desk has loaded. Preserve the sidebar and workspace header DOM, update only
  the main strategy content, and do not refetch Busabase or show a full-page
  loading state for these route changes.
- Make Regression a dated strategy backtest table aligned with `invest-ui`:
  report date, start/end dates, window label, methodology, coverage, total
  return, CAGR, volatility, Sharpe, maximum drawdown, and benchmark-relative
  return. Keep hindsight warnings visible. Show current virtual-book contribution
  (`strategy P/L / total nominal capital`) and the removal case in a clearly
  separate secondary section. Do not invent a backtest or any historical metric
  without a stored dated report backed by historical observations.
- Do not show a rerun action unless a trusted historical-market-data workflow is
  actually available. A stored report is inspectable data, not an executable
  backtest engine.
- On mobile, use the shared off-canvas sidebar, a separate detail route, sticky
  back action, and no horizontal page overflow at 390px or 360px.
- Keep the virtual-only boundary visible. Do not describe L2 as Futu paper trading
  or L3 as real trading anywhere in this app.

## Metric Rules

- Calculate position P/L as `quantity * (latest reference price - virtual entry
  price)` and account return as `NAV / nominal capital - 1`.
- Treat the account's baseline date as the start of nominal-capital performance.
  Do not compare, rank, or aggregate returns as comparable when baseline dates or
  quote provenance are missing. Display missing metrics as unavailable, never as
  zero.
- Reconcile each account NAV against cash plus position market values. Flag a
  mismatch before allowing promotion.
- Calculate total-book return from summed account NAV and summed nominal capital.
- Calculate regression snapshot contribution as `strategy account P/L / total
  nominal capital`; calculate the removal case from the remaining accounts.
- Sort and compare dated backtest reports only after checking that report date,
  window start/end, method, coverage, and benchmark are present.
- Compare strategies on the same window and benchmark before ranking them.
- Keep Demo observations fixed and dated. Never present them as live data.
- Format account and position money in CNY. Show the Chinese security name first
  and retain the six-digit code as secondary identity.

## Completion Criteria

Finish only when:

- `pnpm --dir content/kelly-invest-stock-app dev` remains supported and deterministic checks pass;
- Strategy overview/detail, L1/L2/L3 strategy filters, manual stage marking, and
  Regression work on desktop and mobile;
- every strategy has one virtual account plus explicit selection and invalidation
  rules;
- the five-resource declaration, additive schema migration, and lazy provisioning
  pass fixture tests;
- research evidence and manual approvals persist in Busabase, with reason and
  account snapshot visible in the strategy timeline;
- normal mode uses Busabase, while Demo is explicit, deterministic, and labeled;
- no brokerage path, real-money stage, trading action, or personalized investment
  claim exists; and
- available dependency-skill deployment and real-data checks pass.

## Stop Conditions

Stop before consequential Busabase mutation when the target Space is ambiguous,
the viewer lacks permission, ownership cannot be proven, a stale record would be
overwritten, or the request crosses into brokerage execution or money movement.
