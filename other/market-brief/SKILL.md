---
name: market-brief
description: >
  Generate a current morning market brief for Mick's indices, commodities,
  currencies, macro, and expanded crypto watchlist. Trigger immediately when the
  user starts with "mb" or asks for a market brief, morning brief, market update,
  pre-market summary, market open summary, or asks what the market is doing.
  Always verify live prices, market session context, and news before answering.
  Never use memory for prices, levels, market status, or headlines.
version: 1.0.0
---

# Market Brief

## Intent

Generate a fast, structured market brief for Mick before or during the trading day. The brief covers index direction, commodities, currencies, expanded crypto, macro context, market-moving headlines, and only the flags that matter.

This is a situational awareness tool. It is not financial advice, trade execution guidance, or a signal service.

## Do Not Use When

- Do not use for buy, sell, hold, price target, or guaranteed performance advice.
- Do not use for a deep single-stock or single-crypto research report when a research skill is a better match.
- Do not include an individual stock quote table unless the user explicitly asks for one outside the normal market brief.
- Do not answer from memory when current prices, market session state, economic events, or headlines are requested.
- Do not invent prices, changes, 52-week ranges, market hours, headlines, or sources.

## Trigger When

Trigger immediately, search first, and do not ask clarifying questions when the user starts with:

```text
mb
```

Also trigger on:

- `market brief`
- `morning brief`
- `market update`
- `pre-market summary`
- `market open summary`
- `what is the market doing`

Instrument modifiers:

- `mb + SOL XRP COPPER` means append those instruments to the relevant non-stock section for this brief only.
- `mb only: BTC ETH DXY GOLD` means use only those instruments for this brief.
- `mb +depth` means add the optional depth sections after Headlines.

## Workflow

1. Parse the request for `+` instruments, `only:` override instruments, and `+depth`.
2. Determine the current market session: pre-market, regular session, after-hours, closed, weekend, or holiday if available.
3. Verify current data before writing. Use reliable finance, exchange, brokerage, or market data pages where available.
4. Gather current index levels and broad risk tone without adding individual stock quotes.
5. Gather commodity prices and explain the inflation, growth, energy, or industrial demand read.
6. Gather currency and rate-sensitive macro data, including DXY and major FX pairs.
7. Gather expanded crypto data, including price, 24-hour change, 7-day change where available, market cap rank or dominance where relevant, and the main catalyst or risk.
8. Gather 3 to 5 market-moving headlines from current sources.
9. Populate only confirmed values. Use `--` for unavailable values.
10. Build the brief in the required markdown format.
11. Add Flags only when something is actually notable.
12. End with the required one-line follow-up.

## Default Instruments

Use these by default unless the user gives `only:`.

### Indices

- SPY
- QQQ
- IWM
- VIX

### Commodities

- WTI crude oil
- Brent crude oil
- Natural gas
- Gold
- Silver
- Copper

### Crypto

- BTC/USD
- ETH/USD
- SOL/USD
- XRP/USD
- BNB/USD
- Total crypto market cap
- BTC dominance

### Currencies And Macro

- TLT
- DXY
- EUR/USD
- USD/JPY
- GBP/USD
- USD/CAD
- USD/CNH

## Source Priority

Prefer sources in this order:

1. Built-in finance or market data tools if available.
2. Exchange, ETF sponsor, brokerage, or official market data pages.
3. Major financial data sites such as Yahoo Finance, Nasdaq, MarketWatch, CNBC, Investing.com, TradingView, CoinMarketCap, or CoinGecko.
4. Major business news sources for headlines.

Use multiple sources when a value looks stale, contradictory, delayed, or out of session.

For economic calendar items, verify against a current economic calendar or official release source where possible.

## Data Requirements

For indices and macro instruments, try to capture:

- current or most recent price
- percent change
- session label if relevant
- short risk-tone note

For commodities, capture:

- current price
- percent change
- contract or spot basis where available
- short analytic read: inflation, energy supply, growth, industrial demand, or safe-haven pressure

For currencies, capture:

- current level
- percent change
- short analytic read: dollar strength, yen risk, risk-on/risk-off pressure, commodity currency pressure, or China sensitivity

For crypto, capture:

- current price
- 24-hour percent change
- 7-day percent change where available
- market cap rank, dominance, ETF flow, funding, liquidation, or volume context where available
- short catalyst or risk note

For headlines, capture:

- source
- headline
- one plain-English sentence explaining why it matters

## Report Format

Use this exact structure. Keep tables compact. Do not add commentary outside these sections except the final follow-up line.

```markdown
# Market Brief - [Day, Month DD YYYY] [Time and timezone]

## Indices

| Instrument | Level | % Change | Read |
| --- | ---: | ---: | --- |
| SPY | $XXX.XX | +X.XX% | [Pre-market / Open / After-hours / Closed] |
| QQQ | $XXX.XX | +X.XX% | [Tech risk tone] |
| IWM | $XXX.XX | +X.XX% | [Small-cap risk tone] |
| VIX | XX.XX | +X.XX% | [Low <15 / Elevated 20-30 / High >30] |

## Commodities

| Instrument | Level | % Change | Read |
| --- | ---: | ---: | --- |
| WTI crude | $XX.XX | +X.XX% | [Energy inflation / supply / demand read] |
| Brent crude | $XX.XX | +X.XX% | [Global oil read] |
| Natural gas | $X.XX | +X.XX% | [Weather / storage / demand read] |
| Gold | $X,XXX.XX | +X.XX% | [Rates / dollar / safe-haven read] |
| Copper | $X.XX | +X.XX% | [Growth / China / industrial demand read] |

## Currencies

| Instrument | Level | % Change | Read |
| --- | ---: | ---: | --- |
| DXY | XXX.XX | +X.XX% | [Dollar strength read] |
| EUR/USD | X.XXXX | +X.XX% | [Euro / dollar read] |
| USD/JPY | XXX.XX | +X.XX% | [Yen / rates / intervention read] |
| GBP/USD | X.XXXX | +X.XX% | [Sterling / dollar read] |
| USD/CAD | X.XXXX | +X.XX% | [Oil / dollar / Canada read] |

## Crypto

| Asset | Price | 24H | 7D | Context |
| --- | ---: | ---: | ---: | --- |
| BTC | $XX,XXX | +X.XX% | +X.XX% | [Dominance / ETF flows / risk tone] |
| ETH | $X,XXX | +X.XX% | +X.XX% | [ETH/BTC / ETF / network read] |
| SOL | $XXX.XX | +X.XX% | +X.XX% | [Layer 1 risk appetite / ecosystem note] |
| XRP | $X.XX | +X.XX% | +X.XX% | [Legal / payments / listing catalyst] |
| BNB | $XXX.XX | +X.XX% | +X.XX% | [Exchange-token / ecosystem read] |
| Total crypto market cap | $X.XXT | +X.XX% | +X.XX% | [Broad crypto risk tone] |
| BTC dominance | XX.X% | +X.X pts | -- | [Rotation read] |

## Macro Rates

| Instrument | Level | % Change | Read |
| --- | ---: | ---: | --- |
| TLT | $XXX.XX | +X.XX% | [Long-duration Treasury read] |
| 10Y Treasury yield | X.XX% | +X bps | [Rates pressure read] |

## Headlines

1. **[Source]** - [Headline]. [One sentence plain-English summary.]
2. **[Source]** - [Headline]. [One sentence plain-English summary.]
3. **[Source]** - [Headline]. [One sentence plain-English summary.]

## Flags

- [Only include this section when something is notable.]

## Sources

- [Source name] - [What it supplied]

*Data pulled [HH:MM timezone]. Verify before trading.*

Add instruments or pull a specific chart level?
```

## Optional Depth Sections

If the user includes `+depth`, add these sections after Headlines and before Flags.

### Sector Performance

Use a compact table for the 11 S&P 500 sector ETFs:

- XLK
- XLV
- XLE
- XLF
- XLI
- XLC
- XLRE
- XLU
- XLB
- XLP
- XLY

Columns: Sector ETF, Price, % Change, Note.

### Equity Catalysts

Show notable earnings or mega-cap headlines only when they could move the broader market. Do not add a stock quote table.

Columns: Company, Ticker, Event, Date, Why It Matters.

### Economic Calendar

Show Fed events, CPI, PPI, jobs data, PMI, Treasury auctions, or other major macro events due today or this week.

Columns: Date, Event, Prior, Estimate.

## Constraints

- Always verify current data before answering.
- Use `--` for any value that cannot be confirmed.
- State the session context clearly when markets are not in regular trading.
- Keep the brief factual and compact.
- Do not use green or red formatting.
- Do not include an individual stock quote table in the default brief.
- Do not include placeholder text in Flags.
- Do not output a buy, sell, hold, entry, stop, target, or position sizing recommendation.
- Do not describe a headline as market-moving unless it plausibly affects indices, rates, mega-cap tech, energy, crypto, the Fed, inflation, jobs, or broad risk appetite.
- Keep headlines to 3 to 5 items.
- Include a Sources section with the data source names or links used.
- End with exactly: `Add instruments or pull a specific chart level?`

## Flag Rules

Include Flags only for meaningful conditions such as:

- VIX above 25.
- SPY, QQQ, IWM, TLT, or DXY move above roughly 1% intraday.
- WTI, Brent, gold, copper, or a major FX pair moves enough to affect inflation, rates, or risk appetite.
- BTC moves more than 3% in 24 hours.
- ETH, SOL, XRP, or BNB moves more than 5% in 24 hours.
- BTC dominance shifts enough to show rotation between BTC and altcoins.
- A major Fed, CPI, PPI, jobs, or earnings event is due today or this week.
- Data conflict or stale quote risk could materially affect the brief.

## Validation Checklist

- [ ] Current prices were verified during this run.
- [ ] Market session context is labeled.
- [ ] Default, appended, or override instruments were parsed correctly.
- [ ] Missing values are marked `--` instead of guessed.
- [ ] No default individual stock quote table is included.
- [ ] Commodities, currencies, and expanded crypto context are included.
- [ ] Headlines are current and limited to 3 to 5.
- [ ] Flags are omitted when nothing notable is found.
- [ ] Sources are listed.
- [ ] Output avoids financial advice and trade instructions.

## Help And Examples

If the user asks how to use the skill, give short examples and ask for the fastest next prompt.

Minimum useful input:

- `mb`

Example prompts:

- `mb`
- `mb + PLTR SOFI`
- `mb only: NVDA TSLA BTC`
- `mb +depth`
- `market brief before open`
