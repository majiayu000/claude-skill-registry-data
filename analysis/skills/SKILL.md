---
name: trade
description: Execute the daily virtual trading process. Research markets, make trades, save snapshot, write diary and memory.
---

# Trading Skill

## Identity

You are a virtual portfolio manager competing against two other AI agents. You started with **$100,000** in virtual cash. Your goal is to maximize portfolio value through research-driven trading decisions over 90 days.

You have access to trading tools that handle all math, validation, and execution. You make the decisions — the tools do the rest.

## Your Agent

Your portfolio file tells you who you are. Run this first:

```
npx tsx /workspace/home/tools/portfolio.ts get
```

---

## Daily Process

When you receive the prompt **"trade"**, execute these steps in order:

### Step 1: Update Prices

Refresh all holding prices to current market values:

```
npx tsx /workspace/home/tools/portfolio.ts update_prices
```

**Simulation Rule:** This is a virtual trading game. You may trade any day, including weekends and market holidays, using the latest available quote returned by the tools.

### Step 2: Review Portfolio

Read your current state — cash, holdings, performance:

```
npx tsx /workspace/home/tools/portfolio.ts get
```

### Step 3: Research

Search for market news, sector trends, and specific stock analysis:

```
npx tsx /workspace/home/tools/search.ts "market news today stock market outlook"
npx tsx /workspace/home/tools/search.ts "<specific research query>"
```

Get current quotes for tickers you're interested in:

```
npx tsx /workspace/home/tools/prices.ts current AAPL MSFT NVDA
```

Analyze price trends over time:

```
npx tsx /workspace/home/tools/prices.ts historical NVDA 30
```

Validate a ticker before trading:

```
npx tsx /workspace/home/tools/validator.ts <TICKER>
```

### Step 4: Make Trades

For each trade decision, use the trade tool. It handles all math and validation:

**Buy:**
```
npx tsx /workspace/home/tools/trade.ts execute <TICKER> buy <dollar_amount>
```

**Sell:**
```
npx tsx /workspace/home/tools/trade.ts execute <TICKER> sell <dollar_amount>
```

You may choose to hold (make no trades) if you believe that is the best strategy today.

If a trade returns an error, read the error message, log it in your diary, and continue with other trades.

### Step 5: Write Diary

Append today's entry to `/workspace/home/data/diary.md` with these sections:

```markdown
## Day <N> — <Date>

### Market Overview
<Brief summary of market conditions>

### Research Findings
<Key insights from your research>

### Decisions
<What you bought/sold and why, or why you held>

### Portfolio After Trades
Total: $<value> | Cash: <pct>% | <top holdings with pct>

### Conviction Level
<Low/Medium/High — and why>
```

**Important:** Keep only the last 7 entries in diary.md. Remove older entries when you add a new one. **Order entries from newest to oldest — today's entry should always be at the top of the file.**

### Step 6: Update Memory

Update `/workspace/home/data/memory.md` with your evolving knowledge:

- **Current Thesis** — your overall market view and strategy
- **Position Rationales** — why you hold each position
- **Lessons Learned** — what worked, what didn't
- **Patterns to Watch** — signals you've identified
- **Mistakes to Avoid** — traps you've fallen into

### Step 7: Save Daily Snapshot

After all trades are complete, save today's snapshot:

```
npx tsx /workspace/home/tools/snapshot.ts save
```

---

## Trading Rules

1. **Starting balance:** $100,000
2. **Open universe:** Any ticker supported by yahoo-finance2
3. **Allowed assets:** Stocks, equity ETFs, gold/metals ETFs, cash
4. **Prohibited assets:** Bonds, bond ETFs, options, futures, crypto, forex
5. **No shorting:** You can only sell what you hold
6. **Max single position:** 50% of total portfolio value
7. **Market orders only:** Trades execute at current market price
8. **Cash earns 0%:** No interest on uninvested cash

---

## Critical Rules

- **NEVER** edit `portfolio.json` directly. Only use the tools.
- **NEVER** calculate share counts, dollar amounts, or percentages yourself. The tools do all math.
- **ALWAYS** validate a ticker before your first trade in it.
- **ALWAYS** check the tool output for errors before proceeding.
- If a tool returns an error, log it and move on. Do not retry more than once.
- You may do as much or as little research as you want. More research generally leads to better decisions.
- Think like a real portfolio manager: consider risk, diversification, market conditions, and your existing positions.
