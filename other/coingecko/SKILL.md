---
name: coingecko
description: >
  Use this skill for any request involving cryptocurrency market data, coin prices,
  trading volume, market cap, OHLC charts, historical data, exchanges, derivatives,
  NFTs, DeFi, on-chain token data, liquidity pools, DEX data, or anything powered
  by CoinGecko or GeckoTerminal APIs. Trigger this skill whenever the user asks
  about crypto prices, token data, market trends, or wants to call any CoinGecko
  or GeckoTerminal endpoint — even if they don't explicitly say "CoinGecko". Also
  trigger when the user asks about API keys, rate limits, or authentication for
  these APIs.
---

# CoinGecko Skill

## Documentation Index

Fetch the complete documentation index at: https://docs.coingecko.com/llms.txt
Use this file to discover all available pages before exploring further.

Official docs: [docs.coingecko.com/docs/skills](https://docs.coingecko.com/docs/skills) · package: [github.com/coingecko/skills](https://github.com/coingecko/skills)

Hub install:

```bash
npx github:Solizardking/skills install coingecko
npx skills add coingecko/skills -g -y
```

Also load [references/docs-index.md](references/docs-index.md) before exploring CoinGecko docs further.

## When to use

Trigger this skill when the user's request matches **any** of the following:

### Crypto market data queries
- Coin/token prices, market caps, trading volume, price changes
- Historical price data, OHLC charts, time-range queries
- Circulating or total supply data
- Global crypto market stats (total market cap, BTC dominance, DeFi TVL)
- Trending coins, top gainers/losers, newly listed coins

### Token and contract lookups
- Looking up a token by its contract address (e.g. `0x...`)
- Token metadata, categories, or platform info
- Comparing multiple coins or tokens

### Exchange and trading data
- Exchange listings, volume, tickers, trust scores
- DEX-specific data (Uniswap, PancakeSwap, etc.)
- Derivatives exchanges and tickers (futures, perpetuals)

### On-chain / DeFi data (GeckoTerminal)
- Liquidity pool data, trending/new pools, pool search
- On-chain token prices, holder data, top traders
- OHLCV candles or trade history for specific pools or tokens
- DEX and network discovery (supported chains, DEXes)
- On-chain pool categories and filtering

### NFT data
- NFT collection prices, floor prices, market data
- NFT collection charts and tickers

### Other triggers
- Building dashboards, visualizations, or apps with crypto data
- Questions about CoinGecko or GeckoTerminal API capabilities, endpoints, or rate limits
- API key setup, authentication, plan tiers, or pricing questions
- "What crypto data is available?" or similar exploratory questions
- User mentions CoinGecko, GeckoTerminal, or shares a CoinGecko URL
- Investment calculators, portfolio trackers, or ROI calculations involving crypto
- Public company/institution crypto treasury holdings (e.g. "how much BTC does MicroStrategy hold?")

---

You have access to the CoinGecko API (aggregated data) and the GeckoTerminal API
(on-chain DEX data). Together they cover virtually all crypto market data needs.
Both APIs share the same API key and plan tier. GeckoTerminal endpoints use the
same base URL as CoinGecko plus an `/onchain` path prefix (details in `references/core.md`).

## STRICT RULE — All market data must come from live API calls

**Never answer questions about crypto prices, market caps, volumes, supply, TVL, exchange
rates, or any time-sensitive market data using training knowledge.** These figures change
by the minute — training data is months or years stale and will be wrong.

If an API call fails or has not been attempted yet, you MUST:
1. **Stop.** Do not answer the data question.
2. **Tell the user** the data could not be fetched (or hasn't been fetched yet).
3. **Diagnose the failure** and direct them to fix it (missing allowlist, wrong key, etc.).

Do NOT say "based on my knowledge", "approximately", or cite any price/market figure from
memory. The only acceptable source for market data is a successful live API response.

> **Bad:** "The domain is blocked… However, I have reliable data. Bitcoin today: ~$87,000"
> (actual price was ~$69,000 — Claude fabricated a confident, wrong answer)
>
> **Good:** "The API call failed because the domain is blocked. Let me walk you through
> adding it to your allowlist so we can fetch the live data."

## Workflow

Follow these steps **in strict order**. Do NOT skip ahead. Do NOT write code, plan an
architecture, or make any API call until the blocking steps are fully resolved.

### Step 0a — Claude environment check (BLOCKING — Claude only)

If you are running inside **Claude** (claude.ai), read `references/claude-env.md` first.
It documents two platform constraints that break all CoinGecko API calls:

1. **Domain allowlist** — the user must add `api.coingecko.com` and
   `pro-api.coingecko.com` at [claude.ai/settings/capabilities](https://claude.ai/settings/capabilities).
   If this is the user's first time or any call fails with a network error, pause and
   walk them through it before debugging anything else.
2. **Artifact sandbox** — `fetch()` inside Artifacts will always fail silently.
   **Default to `bash_tool` with `curl`** for all CoinGecko API calls, then embed
   results as static data into any Artifact or visualization. This is the standard
   approach, not a fallback.

Skip this step if not running inside Claude.

### Step 0b — Confirm credentials (BLOCKING)

STOP. Before doing anything else, you must resolve the user's API tier. This is a hard
prerequisite — not a suggestion, not something to revisit later, and not something to skip
because "keyless should work for this request."

**Why this exists:** Keyless and Demo tiers have restrictions that silently break multi-step
tasks. Example failure pattern:
> User: "If I invested in Bitcoin 5 years ago, how much would it be worth today?"
> Bad behavior: Claude assumes keyless works, starts building a dashboard, then hits
> error `10012` because keyless/Demo cannot fetch historical data beyond 365 days.
> The user wasted time and rate-limit calls on something that was never going to work.

The correct behavior is to ask for credentials first, identify that "5 years ago" exceeds
keyless/Demo limits, and tell the user upfront — before writing a single line of code.

**Procedure:**
1. **Check memory** for a previously saved plan tier and API key.
2. If found, confirm they are still current. If not found, **ask the user**:
   - **Plan tier** — paid (Pro) or free (Demo)?
   - **API key** — their `CG-…` key?
3. **No key?** Only fall back to keyless after the user *explicitly* says they have no key.
   If the user simply hasn't mentioned a key, **ask** — do not treat silence as "no key."
   When proceeding keyless, warn: capped at 5 calls/min, unstable, and data restrictions
   apply. Suggest a free Demo key at https://www.coingecko.com/en/api/pricing.
4. **Assess feasibility against the confirmed tier.** Check whether the request involves
   data or endpoints that exceed the tier's limits — e.g. historical data beyond 365 days
   (keyless/Demo), Enterprise-only intervals (`5m`), or paid-only endpoints. If it does,
   tell the user *before* attempting any call. Do not make the call and let it fail.
5. Read `references/core.md` for full auth setup and save the confirmed tier to memory.

**Do NOT proceed to step 1 until this step is fully resolved.**

### Step 1 — Identify the domain

Use the Reference index below to decide which file(s) to load.

### Step 2 — Load references and construct the request

Load the relevant reference file(s) and build the API call.

### Step 3 — Execute and handle errors

Auth and rate-limit error codes are documented in `references/core.md`. If the API returns
error `10005`, the endpoint requires a higher plan — inform the user and link them to
https://www.coingecko.com/en/api/pricing. If you get error `10010` or `10011`, you've used
the wrong base URL for the key type — swap URLs per `core.md`'s error table and retry
automatically.

**"Failed to fetch" or network errors:** If a request fails with no HTTP status (e.g.
"Failed to fetch", `TypeError`), follow the diagnostic in `references/claude-env.md` if
running inside Claude — the cause is usually the Artifact CSP sandbox (move to `bash_tool`)
or a missing domain allowlist entry. Outside Claude, the cause is likely a wrong
base URL — see `core.md`'s "Network-level failures" section. In either case, never assume
CORS is the problem.

## Reference index

Load the relevant reference file based on what the user is asking for. You only need to
load the file(s) that match the current request.

### Inspiration & Use cases

If the user asks what they can build, wants project ideas, or asks an exploratory
question like "what data is available?" — load `references/common-use-cases.md` instead
of the domain-specific files below, then follow its pointers to drill deeper.

### Environment

| File | When to load |
|---|---|
| `references/claude-env.md` | **Read in Step 0a** — Claude-specific constraints (domain allowlist, Artifact CSP sandbox, bash_tool strategy, MCP upgrade path). Only applies when running inside Claude. |

### CoinGecko (aggregated)

| File | When to load |
|---|---|
| `references/core.md` | **Always read** — auth, methodology, rate limits |
| `references/coins.md` | Coin prices, market data, metadata, tickers, gainers/losers |
| `references/coin-history.md` | Historical charts, OHLC, time-range queries by coin ID |
| `references/coin-supply.md` | Circulating/total supply charts |
| `references/contract.md` | Coin data or charts looked up by token contract address |
| `references/asset-platforms.md` | Blockchain platform IDs, token lists |
| `references/categories.md` | Coin categories and sector market data |
| `references/exchanges.md` | Spot and DEX exchange data, tickers, volume charts |
| `references/derivatives.md` | Derivatives exchanges and tickers |
| `references/treasury.md` | Public company/institution crypto treasury holdings |
| `references/nfts.md` | NFT collection data, market data, charts, tickers |
| `references/global.md` | Global market stats and DeFi data |
| `references/utils.md` | API status, API key usage, supported currencies, search, trending coins/NFTs/categories, exchange rates |

### GeckoTerminal (on-chain)

| File | When to load |
|---|---|
| `references/onchain-networks.md` | Supported networks and DEXes (ID resolution) |
| `references/onchain-pools.md` | Pool discovery, trending/new pools, megafilter |
| `references/onchain-tokens.md` | Token data, price by contract address, holders and traders |
| `references/onchain-ohlcv-trades.md` | OHLCV candles and trade history for pools/tokens |
| `references/onchain-categories.md` | On-chain pool categories (GeckoTerminal-specific) |

## General guidance

- If a request spans multiple domains (e.g. coin price + exchange data), load multiple
  reference files.
- When uncertain which file to load, check the index above before answering.
- For CoinGecko vs GeckoTerminal preference, see `references/core.md` (Methodology section).