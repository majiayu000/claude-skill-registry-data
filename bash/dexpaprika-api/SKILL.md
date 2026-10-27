---
name: dexpaprika-api
description: Access the DexPaprika API, CLI, and streaming service to query DEX data including networks, pools, tokens, and trading activity. Use this skill when making HTTP requests to api.dexpaprika.com or streaming.dexpaprika.com, or when using dexpaprika-cli for blockchain DEX information.
version: 2.13.1
---

# DexPaprika API Skill

> **Freshness check (run once per session, before relying on this skill):** this file is `version: 2.13.1`, verified against the live API on 2026-10-14. Fetch the latest copy's header:
>
> ```bash
> curl -s -r 0-400 https://raw.githubusercontent.com/coinpaprika/skills/main/dexpaprika-api/SKILL.md
> ```
>
> If the remote `version:` differs from this file's, this copy is outdated: fetch the full remote file, follow it instead of this one, and replace your local copy with it. DexPaprika removes endpoints (they return HTTP 410) and reshapes responses; a stale skill points you at dead endpoints.

DEX data API covering 36 blockchains, 230+ DEXes, 36M+ liquidity pools, and 33M+ tokens, over 96% of on-chain DEX volume. Built by the CoinPaprika team (operating since 2018). No API key and no registration to start: keyless runs at 15 requests/minute per IP on 10,000 credits, and a free key raises that to 30 requests/minute on 100,000 credits. Both allowances are counted over a rolling 30 days, so there is no monthly reset. Register a free key at https://console.dexpaprika.com. Data is delayed up to 60 seconds on both. Paid plans serve real-time data from api-pro.dexpaprika.com with a key: Dev is $30/month for 500,000 credits at 120/minute, Pro is $99/month for 5,000,000 at 500/minute. Docs: https://docs.dexpaprika.com. Rate limits: https://docs.dexpaprika.com/knowledge-base/rate-limits. Plans and checkout: https://dexpaprika.com/api/pricing.

- Documentation: https://docs.dexpaprika.com
- AI Agents showcase: https://agents.dexpaprika.com
- Agent skill files: https://dexpaprika.com/agents/skill.md (REST) and https://dexpaprika.com/agents/streaming/skill.md (SSE)
- GitHub: https://github.com/coinpaprika
- Support: support@coinpaprika.com

> **Field naming note:** URL paths use `network` and `token_address`, but JSON responses return `chain` and `id` for the same values.

---

## Integration options

### Option 1: CLI (recommended for agents)

Install and query in seconds. Best for agents that can run shell commands.

```bash
curl -sSfLO https://raw.githubusercontent.com/coinpaprika/dexpaprika-cli/v0.12.0/install.sh
echo "1cd2759d86d915e3e63087d4199888b44efbe72dbef7b640c2eb89c687503125  install.sh" > install.sh.sha256
{ sha256sum -c install.sh.sha256 || shasum -a 256 -c install.sh.sha256; } && sh install.sh
```

The script comes from a release tag and runs only if its SHA-256 matches. It installs the latest release and checks the binary against that release's `SHA256SUMS`. With Rust installed, `cargo install dexpaprika-cli --locked` works too.

Always use `--output json --raw` for machine-readable output. Run `dexpaprika-cli onboard` for an interactive quick-start guide.

Common commands:

```bash
# Search for a token
dexpaprika-cli search USDC --output json --raw

# Get token price
dexpaprika-cli token ethereum 0xc02aaa39b223fe8d0a0e5c4f27ead9083c756cc2 --output json --raw

# Top pools on a network
dexpaprika-cli pools ethereum --limit 10 --output json --raw

# Historical OHLCV for a pool: hourly candles over the last 24 hours (CLI 0.7.0+ for a relative --start)
dexpaprika-cli pool-ohlcv ethereum 0x88e6a0c2ddd26feeb64f039a2c41296fcb3f5640 --start -24h --interval 1h --limit 24 --output json --raw

# Historical USD OHLCV for a token across all its pools (Dev or Pro key, CLI 0.9.0+)
DEXPAPRIKA_API_BASE_URL=https://api-pro.dexpaprika.com dexpaprika-cli token-ohlcv ethereum 0xc02aaa39b223fe8d0a0e5c4f27ead9083c756cc2 --start -24h --interval 1h --limit 24 --output json --raw

# Top tokens on a network (ranked, with multi-timeframe metrics)
dexpaprika-cli top-tokens ethereum --limit 20 --output json --raw
dexpaprika-cli top-tokens solana --order-by price_change_percentage_24h --sort asc --output json --raw

# Filter tokens by volume, FDV, liquidity, txns
dexpaprika-cli filter-tokens ethereum --volume-24h-min 100000 --output json --raw
dexpaprika-cli filter-tokens solana --fdv-min 1000000 --liquidity-usd-min 50000 --output json --raw

# Filter pools by volume, liquidity, txns, creation date
dexpaprika-cli pool-filter ethereum --volume-24h-min 500000 --liquidity-usd-min 50000 --output json --raw

# Relative times (CLI 0.8.0+): pools created in the last day
dexpaprika-cli pool-filter solana --created-after -24h --sort-by created_at --output json --raw

# Swaps in the last hour. Dev or Pro key, on the paid host (CLI 0.9.0+)
DEXPAPRIKA_API_BASE_URL=https://api-pro.dexpaprika.com dexpaprika-cli transactions ethereum 0x88e6a0c2ddd26feeb64f039a2c41296fcb3f5640 --from -1h --output json --raw

# Batch token prices
dexpaprika-cli prices ethereum --tokens 0xc02aaa39b223fe8d0a0e5c4f27ead9083c756cc2,0xa0b86991c6218b36c1d19d4a2e9eb0ce3606eb48 --output json --raw

# Stream token prices, pushed when a swap moves the price
dexpaprika-cli stream ethereum 0xc02aaa39b223fe8d0a0e5c4f27ead9083c756cc2

# Stream pool reserve changes, emitted when a swap moves the reserves
dexpaprika-cli stream-reserves ethereum 0x88e6a0c2ddd26feeb64f039a2c41296fcb3f5640 --method pool_reserves

# API health check
dexpaprika-cli status
```

The `pools`, `pool-filter`, `token-pools`, `top-tokens`, and `filter-tokens` commands call the `/search` endpoints under the hood (`token-pools` wraps `/networks/{network}/pools/search?token_address=...`). They accept both the canonical sort-field names (`volume_usd_24h`, `txns_24h`, `price_change_percentage_24h`, `fdv_usd`) and the legacy aliases (`volume_usd`, `volume_24h`, `txns`, `price_change`, `fdv`), which the CLI maps to canonical before sending.

For the full CLI command reference, read `references/cli-reference.md`.

### Option 2: REST API

Base URL: `https://api.dexpaprika.com`

No API key needed to start on the free tier. All responses are JSON.

```bash
curl -s "https://api.dexpaprika.com/networks/ethereum/tokens/0xc02aaa39b223fe8d0a0e5c4f27ead9083c756cc2" | jq
```

**Authentication.** If you have a key, send it as the entire `Authorization` header
value: the key alone, with nothing in front of it. That differs from most other APIs,
so when generating code, emit the bare key.

```bash
curl -s -H "Authorization: api_YOUR_KEY" "https://api.dexpaprika.com/networks"
```

Free keys stay on `api.dexpaprika.com`; Dev, Pro and Enterprise use
`api-pro.dexpaprika.com`, and a free key sent there returns `403`. Read the `x-api-plan`
response header (`keyless`, `free`, `dev`, `pro`) to see which plan a request was billed
to; `GET /usage` reports it too. Check it, because on `api.dexpaprika.com` an unreadable
key is ignored rather than rejected: the call returns `200` with real data while quietly
serving the keyless tier, and only the header says so.

#### Endpoint table

| Need | Endpoint |
|------|----------|
| List all networks | `GET /networks` (returns volume_usd_24h, txns_24h, pools_count per network) |
| DEXes on a network | `GET /networks/{network}/dexes` (returns volume_usd_24h, txns_24h, pools_count per DEX) |
| Top pools on network | `GET /networks/{network}/pools/search` (order_by=volume_usd_24h; rows under `results`, cursor pagination) |
| Filter pools | `GET /networks/{network}/pools/search` (volume_usd_24h/7d/30d, liquidity_usd, txns_24h, price_usd, price_change_percentage_24h/6h/1h/5m, creation date filters) |
| Biggest movers on network | `GET /networks/{network}/pools/search?order_by=price_change_percentage_1h&sort=desc` (also 5m, 6h, 24h) |
| Pool details | `GET /networks/{network}/pools/{pool_address}` |
| Pool OHLCV (charts) | `GET /networks/{network}/pools/{pool_address}/ohlcv` |
| Token OHLCV (USD, across every pool; Dev or Pro) | `GET /networks/{network}/tokens/{token_address}/ohlcv` on `api-pro.dexpaprika.com` |
| Pool RSI, EMA, MACD, Bollinger Bands, VWAP | `GET /networks/{network}/pools/{pool_address}/indicators?indicator=rsi` (computed by the API, same plan limits as pool OHLCV) |
| Token indicators (USD, across every pool; Dev or Pro) | `GET /networks/{network}/tokens/{token_address}/indicators?indicator=rsi` on `api-pro.dexpaprika.com` |
| Pool transactions (Dev or Pro) | `GET /networks/{network}/pools/{pool_address}/transactions` on `api-pro.dexpaprika.com`; free tier: transaction counts from pool details |
| Token price + data | `GET /networks/{network}/tokens/{token_address}` |
| Pools containing token | `GET /networks/{network}/pools/search?token_address={token_address}` |
| Filter tokens | `GET /networks/{network}/tokens/search` (volume_usd_24h, liquidity_usd, fdv_usd, txns_24h, creation date filters) |
| Top tokens on network | `GET /networks/{network}/tokens/search` (order_by=volume_usd_24h/liquidity_usd/txns_24h/fdv_usd/price_change_percentage_24h; rows under `results`, cursor pagination) |
| Filter pools across all networks | `GET /pools/search` (same filters and order_by as the per-network variant) |
| Filter tokens across all networks | `GET /tokens/search` (same filters and order_by as the per-network variant) |
| Batch token prices | `GET /networks/{network}/multi/prices?tokens={addr1},{addr2}` |
| Pools for a DEX | `GET /networks/{network}/pools/search?dex_name={dex_id}` (rows under `results`, cursor pagination) |
| Search tokens/pools/DEXes | `GET /search?query={term}` |
| Platform statistics | `GET /stats` |

**Removed endpoints (HTTP 410):** `/networks/{network}/pools`, `/pools`, `/networks/{network}/pools/filter`, `/networks/{network}/tokens/filter`, `/networks/{network}/tokens/top`, `/networks/{network}/tokens/{token_address}/pools`, and `/networks/{network}/dexes/{dex}/pools` are gone. They return HTTP 410 with a pointer to the `/search` replacement. Do not call them.

**`dex_name` replaces the DEX path segment:** the removed `/networks/{network}/dexes/{dex}/pools` becomes `GET /networks/{network}/pools/search?dex_name={dex_id}`. The DEX moves out of the path and into a query parameter. `dex_name` takes the dex id (`uniswap_v3`), matched case-insensitively, not the human display name. Get valid values from `GET /networks/{network}/dexes` and pass the `dex_id` field. Passing that object's `dex_name` field instead, a display name like `Uniswap V3`, returns HTTP 200 with an empty `results` array rather than an error, so the mistake reads as a DEX with no pools. The response shape changes with the endpoint: rows arrive under `results` instead of `pools`, pagination is `cursor` plus `has_next_page`/`next_cursor` instead of `page`/`page_info`, and the 24h volume field is `volume_usd_24h`, not `volume_usd`.

**`token_address` is network-scoped only:** the cross-network `GET /pools/search` accepts `token_address` but silently ignores it (results are unfiltered); to find pools containing a token, use the per-network `GET /networks/{network}/pools/search`. An unknown address returns HTTP 200 with empty `results`. Repeating `token_address` does not act as a pair filter; the API uses only one of the values (not guaranteed by order).

**Short price-change windows are pool-only, the 24h window is not:** the two pool searches order by and filter on all four windows, `price_change_percentage_24h`, `_6h`, `_1h` and `_5m`. Filter names are `price_change_percentage_{24h,6h,1h,5m}_{min,max}` and the values are signed, so `price_change_percentage_1h_max=-20` selects pools down 20 percent or more. The token searches take the 24h window for both sorting and filtering, and reject the three short ones: `order_by=price_change_percentage_1h` returns HTTP 400 on `/tokens/search`, and `price_change_percentage_1h_min` and friends are accepted there and silently ignored. Token rows carry `price_change_percentage_24h` and no `price_change_percentage_6h`, `_1h` or `_5m`; `detailed=true` adds `6h`, `1h` and `5m` objects to each row, but those hold volume and trade counts, so there is no short-window token figure to sort or filter on. A misspelled filter name is ignored rather than rejected, so a typo looks exactly like a 200 with a full result set. Compare against an unfiltered baseline when you need to be sure a filter landed:

```bash
# Baseline: 1h changes on the busiest ethereum pools sit near zero
curl -s "https://api.dexpaprika.com/networks/ethereum/pools/search?limit=5" | jq '[.results[].price_change_percentage_1h]'

# Filtered: only pools up 50 percent or more over the last hour
curl -s "https://api.dexpaprika.com/networks/ethereum/pools/search?price_change_percentage_1h_min=50&limit=5" | jq '[.results[].price_change_percentage_1h]'

# The 24h window filters on the token side too: every row comes back at 20 percent or better
curl -s "https://api.dexpaprika.com/networks/ethereum/tokens/search?price_change_percentage_24h_min=20&limit=5" | jq '[.results[].price_change_percentage_24h]'
```

For the full OpenAPI 3.1 specification with all schemas, parameters, and response types, read `references/openapi.yml`.

### Option 3: MCP Server (for AI IDEs)

Hosted MCP server for Claude Desktop, Cursor, Windsurf, and any MCP client.

Add to `claude_desktop_config.json` or equivalent:

```json
{
  "mcpServers": {
    "dexpaprika": {
      "url": "https://mcp.dexpaprika.com/sse"
    }
  }
}
```

No API key needed to start. Provides 20 tools for querying networks, pools, tokens, OHLCV, technical indicators, transactions, and search. Verify the count with a live `tools/list`.

Tools that need a paid plan run on the user's own Dev, Pro or Enterprise key: add `"headers": { "Authorization": "YOUR_API_KEY" }` next to `url`, the key on its own, and reconnect. That is `getTokenOHLCV`, `getTokenIndicator` and `getPoolTransactions`. Without a key such a tool returns `DP401_API_KEY_REQUIRED` and calls nothing. Fall back to `getPoolOHLCV` or `getPoolIndicator` on the token's most liquid pool for candles or indicators, and to `getPoolDetails` for a pool's transaction counts. Every other hosted tool runs on the server's shared capacity, not on the user's plan, so a key does not raise its limits; on `DP429_RATE_LIMITED` wait `retry_after_seconds` and retry.

Documentation: https://docs.dexpaprika.com/ai-integration/hosted-mcp-server

### Option 4: Streaming API (prices, reserves, swaps, OHLCV candles)

Base URL: `https://streaming.dexpaprika.com`

Four SSE feeds share one transport, and access differs per feed:
- `/sse/prices`: token price updates, pushed when a swap moves the price. Updates are swap-driven, not clock-driven or per block: a quiet chain can go minutes without emitting anything. Keyless on the showcase tokens, a free key for any token.
- `/sse/reserves`: pool reserve updates with USD-denominated deltas, emitted when a swap changes the pool's reserves, not on every block. Any key, a free one included.
- `/sse/transactions`: individual swaps, for one pool (`method=pool`) or every pool a token trades in (`method=token`). **Dev, Pro or Enterprise**, on `https://streaming-pro.dexpaprika.com`.
- `/sse/ohlcv`: sealed token candles at `1s`, `5s` or `60s`. Dev, Pro or Enterprise, on `https://streaming-pro.dexpaprika.com`.

Keyless requests to a feed or token that needs a key get `403` with `"error":"preview_only"`. A paid-only feed refuses keyless and free keys with `403` and `"error":"plan_required"`, plus `tier`, `message`, `required_tier` (`dev`) and `links`. Match on `error`, not the message text.

**Limits:** 25 subscriptions per POST connection. Concurrent SSE streams: 10 keyless (counted per IP), 10 on a free key, 30 on Dev, 100 on Pro (counted per account); the next one gets `429` with `"error":"rate_limited"` and `Concurrent stream limit reached`. A `ping` event lands every 15 s. Keyless streaming covers 35 showcase tokens, a flagship asset on most chains; a free API key opens prices and reserves for any token.

Single token price (GET):
```bash
curl --http1.1 -N "https://streaming.dexpaprika.com/sse/prices?method=token_price&chain=ethereum&address=0xc02aaa39b223fe8d0a0e5c4f27ead9083c756cc2"
```

Multiple token prices (POST, up to 25):
```bash
curl --http1.1 -N -X POST "https://streaming.dexpaprika.com/sse/prices" \
  -H "Accept: text/event-stream" -H "Content-Type: application/json" \
  -d '[{"chain":"ethereum","address":"0xc02aaa39b223fe8d0a0e5c4f27ead9083c756cc2","method":"token_price"}]'
```

Pool reserves (GET, free key):
```bash
curl --http1.1 -N -H "Authorization: $DEXPAPRIKA_API_KEY" "https://streaming.dexpaprika.com/sse/reserves?method=pool_reserves&chain=ethereum&address=0x88e6a0c2ddd26feeb64f039a2c41296fcb3f5640"
```

`token_price` event fields: `address`, `chain`, `price` (USD as string), `timestamp`, `timestamp_price` (both unix seconds). The legacy `t_p` method still answers on `/sse/prices` with a compact `{a, c, p, t, t_p}` shape; it is not in the spec, so do not use it in new code. `/stream` itself is gone (`410`).

The reserves feed now emits **method-named events**: the old single `reserve_update` event is gone. Match on the two event names instead:

- `pool_reserves` event (one pool, nested tokens): `chain`, `pool_id`, `block`/`previous_block` (strings; `previous_block` can be omitted), `tokens[]` (each `token_id`, `reserve`/`delta` as strings, `price_usd`/`reserve_usd`/`delta_usd` as numbers), `total_reserve_usd`, `total_delta_usd`, `timestamp`, `block_timestamp` (both unix seconds).
- `token_reserves` event (one token across all its pools, flat): `chain`, `token_id`, `reserve`/`delta` (strings), `block` (string), `price_usd`, `reserve_usd`, `delta_usd`, `updated_at`, `timestamp` (both unix seconds).

Raw integer fields (`reserve`, `delta`, `block`, `previous_block`) exceed `Number.MAX_SAFE_INTEGER`, parse with `BigInt`. A consumer tailing reserves must stop matching `reserve_update` and handle these two event names plus their new timestamp fields.

`request_id` correlation (optional): pass `request_id` as a `uint32` (0..4294967295) on GET via the query string, or per-asset in the POST body (it defaults to the asset's array index). The server echoes it back as a `request_id:` SSE line on data events only. `ping`, `warning`, and `error` events carry no `request_id`.

```bash
# GET with request_id; the value comes back on each pool_reserves event
curl --http1.1 -N -H "Authorization: $DEXPAPRIKA_API_KEY" "https://streaming.dexpaprika.com/sse/reserves?method=pool_reserves&chain=ethereum&address=0x88e6a0c2ddd26feeb64f039a2c41296fcb3f5640&request_id=12345"
```

**Important:** Streaming requires HTTP/1.1. Add `--http1.1` with curl. One invalid asset cancels the entire stream with HTTP 400. SSE parsers must buffer one message between blank-line boundaries before dispatching: both `event:`/`data:` orderings are valid and the server uses either, and a `request_id:` line can appear alongside `event:`/`data:`.

For the full streaming reference (all four feeds, events, errors, parser patterns), read `references/streaming-api.md`.

### Option 5: SDKs

| Language | Repository |
|----------|------------|
| Go | https://github.com/coinpaprika/dexpaprika-sdk-go |
| Python | https://github.com/coinpaprika/dexpaprika-sdk-python |
| TypeScript | https://github.com/coinpaprika/dexpaprika-sdk-ts |
| PHP | https://github.com/coinpaprika/dexpaprika-sdk-php |

---

## Common workflows

### Get a token price

CLI:
```bash
dexpaprika-cli token ethereum 0xc02aaa39b223fe8d0a0e5c4f27ead9083c756cc2 --output json --raw
```

curl:
```bash
curl -s "https://api.dexpaprika.com/networks/ethereum/tokens/0xc02aaa39b223fe8d0a0e5c4f27ead9083c756cc2" | jq '.summary.price_usd'
```

Python:
```python
import requests
r = requests.get("https://api.dexpaprika.com/networks/ethereum/tokens/0xc02aaa39b223fe8d0a0e5c4f27ead9083c756cc2")
token = r.json()
print(f"{token['symbol']}: ${token['summary']['price_usd']}")
```

### Search for a token

```bash
curl -s "https://api.dexpaprika.com/search?query=PEPE" | jq '.tokens[:5]'
```

Note: Search uses fuzzy name+symbol matching. "UNI" returns "Uniswap", "United Stables", etc. Filter by exact `symbol` match client-side.

### Get historical OHLCV for a pool

```bash
curl -s "https://api.dexpaprika.com/networks/ethereum/pools/0x88e6a0c2ddd26feeb64f039a2c41296fcb3f5640/ohlcv?start=-24h&interval=1h&limit=24" | jq
```

OHLCV params: `start` (required; a relative offset such as `-24h` or `-7d`, Unix seconds, RFC3339 or `yyyy-mm-dd`), `end` (same formats), `interval` (`1m`|`5m`|`10m`|`15m`|`30m`|`1h`|`6h`|`12h`|`24h`), `limit` (default 10, max 1000), `inversed` (boolean, inverts price ratio for USD-denominated prices from stablecoin-paired pools).

### Get historical OHLCV for a token (Dev or Pro)

USD candles for a token, from a volume-weighted price across every pool it trades in on the network; `volume` is the USD traded across all of them. No pool to pick and no pair price to convert.

```bash
curl -s -H "Authorization: $DEXPAPRIKA_API_KEY" "https://api-pro.dexpaprika.com/networks/ethereum/tokens/0xc02aaa39b223fe8d0a0e5c4f27ead9083c756cc2/ohlcv?start=-24h&interval=1h&limit=24" | jq
```

- Needs a Dev, Pro or Enterprise key, called on `https://api-pro.dexpaprika.com`. Keyless and free keys get `403` with `"error":"plan_required"`: fall back to pool OHLCV on the token's busiest pool.
- Same `start`, `end`, `interval` and `limit` as pool OHLCV, and no `inversed`. `interval` defaults to `24h` and `limit` to 10, so set both.
- A candle exists only for an interval in which the token traded, so short intervals on quiet tokens have gaps. The latest candle can still be open.
- Reference: https://docs.dexpaprika.com/api-reference/tokens/get-ohlcv-data-for-a-token

### Get a technical indicator for a pool

RSI, EMA, MACD, Bollinger Bands or VWAP, computed by the API from the pool's completed candles, so there is no need to fetch OHLCV and compute them yourself.

```bash
curl -s "https://api.dexpaprika.com/networks/ethereum/pools/0x88e6a0c2ddd26feeb64f039a2c41296fcb3f5640/indicators?indicator=rsi&interval=1h&start=-24h" | jq
```

- `indicator` (required): `rsi`, `ema`, `macd`, `bbands` or `vwap`. Also `interval` (`1m` to `24h`, or `1d`), `start`, `end`, `limit` (default 100, max 1000) and `cursor`.
- Send only the parameters of the chosen indicator: `period` for rsi (14), ema (20), bbands (20) and vwap (14); `fast_period` (12), `slow_period` (26) and `signal_period` (9) for macd; `std_dev` (2) for bbands. Any other parameter answers `400` `invalid_param`.
- Response: `parameters` (what was used) and `data`, oldest first, one point per completed candle. rsi, ema and vwap give `value`; macd gives `macd`, `signal` and `histogram`; bbands gives `upper`, `middle` and `lower`.
- Same plan limits as pool OHLCV (below). Always pass `interval`; without a key it defaults to `1h`, otherwise to `24h`.
- RSI, EMA and MACD are smoothed: start ten or more periods before the first value you rely on. Without a key the 24-hour window is too short for RSI(14) to settle; a free key opens 7 days.
- Token indicators: the same on `/networks/{network}/tokens/{token_address}/indicators`, from the token's USD candles across every pool. Dev, Pro or Enterprise on `api-pro.dexpaprika.com`; keyless and free keys get `403` `plan_required`, so use the pool endpoint on the token's busiest pool instead.
- Guide: https://docs.dexpaprika.com/tutorials/technical-indicators. Reference: https://docs.dexpaprika.com/api-reference/pools/get-a-technical-indicator-for-a-pool

### Batch prices for multiple tokens

```bash
curl -s "https://api.dexpaprika.com/networks/ethereum/multi/prices?tokens=0xc02aaa39b223fe8d0a0e5c4f27ead9083c756cc2,0xa0b86991c6218b36c1d19d4a2e9eb0ce3606eb48" | jq
```

Returns an **ARRAY** (not a keyed object). Max 10 tokens per request.

### Stream real-time prices (Python)

```python
import requests, json

assets = [
    {"chain": "ethereum", "address": "0xc02aaa39b223fe8d0a0e5c4f27ead9083c756cc2", "method": "token_price"},
    {"chain": "solana",   "address": "So11111111111111111111111111111111111111112",  "method": "token_price"}
]

r = requests.post("https://streaming.dexpaprika.com/sse/prices",
    headers={"Accept": "text/event-stream", "Content-Type": "application/json"},
    json=assets, stream=True)

# Buffer one SSE message at a time, then dispatch. Both `event:`/`data:`
# line orderings are valid SSE and the server has emitted either, so a
# line-by-line parser that assumes one order will silently mis-dispatch.
msg_lines = []
for line in r.iter_lines(decode_unicode=True):
    if line:
        msg_lines.append(line); continue
    event_type, data_str = "message", None
    for ml in msg_lines:
        if ml.startswith("event:"):
            event_type = ml.split(":", 1)[1].strip()
        elif ml.startswith("data:"):
            data_str = ml[5:].lstrip()
    msg_lines = []
    if event_type == "token_price" and data_str:
        d = json.loads(data_str)
        print(f"{d['chain']} {d['address']}: ${d['price']}")
```

---

## Common token addresses

Do not guess addresses. Use `search` to find tokens, or use these known addresses:

| Token | Chain | Address |
|-------|-------|---------|
| WETH | ethereum | `0xc02aaa39b223fe8d0a0e5c4f27ead9083c756cc2` |
| USDC | ethereum | `0xa0b86991c6218b36c1d19d4a2e9eb0ce3606eb48` |
| USDC | polygon | `0x2791bca1f2de4661ed88a30c99a7a9449aa84174` |
| USDC | solana | `EPjFWdd5AufqSSqeM2qN1xzybapC8G4wEGGkZwyTDt1v` |
| SOL | solana | `So11111111111111111111111111111111111111112` |

## Common network IDs

Always lowercase: `ethereum`, `solana`, `bsc`, `polygon`, `arbitrum`, `base`, `avalanche`, `optimism`, `sui`, `ton`, `tron`.

Full list: `GET /networks` or `dexpaprika-cli networks`.

## Pagination

Two pagination models coexist:

- **Page-based** (`/networks/{network}/dexes`): `?page=1&limit=10&order_by=volume_usd&sort=desc`. Pages are 1-indexed (first page is `page=1`). Max 1000 pages. `order_by` values on this endpoint: `volume_usd`, `price_usd`, `transactions`, `last_price_change_usd_24h`, `created_at`.
- **Cursor-based** (the four `/search` endpoints): pass `limit` plus the `cursor` value from the previous response. Rows arrive under `results`, alongside `has_next_page` and `next_cursor`. `limit` defaults to 50, maximum 100. **Paging needs an API key:** without one you get the first page, and a keyless request that sends `cursor` gets `403` with `"error": "plan_required"`, `"required_tier": "free"`, `"param": "cursor"` (during the warning period it still answers `200` with an `x-api-warning` header). Any key, a free one from https://console.dexpaprika.com included, pages without limit. Treat that `403` as a missing key, never retry it. `order_by` values are canonical: `volume_usd_24h`, `volume_usd_7d`, `volume_usd_30d`, `liquidity_usd`, `txns_24h`, `created_at`, `price_change_percentage_24h`, plus `price_usd`, `price_change_percentage_6h`, `price_change_percentage_1h` and `price_change_percentage_5m` (pools only) and `fdv_usd` (tokens only). The legacy names (`volume_usd`, `transactions`, `last_price_change_usd_24h`) return HTTP 400 on `/search` endpoints.

## Timestamps

All timestamps support Unix, RFC3339, or `yyyy-mm-dd` format, and an offset back from now (`-24h`, `-7d`, `-90m`; units s, m, h, d). That covers OHLCV `start` and `end`, pool transactions `from` and `to`, and `created_after` and `created_before` on the four `/search` endpoints, so `from=-1h` is the last hour of swaps and `created_after=-24h` what was created in the last day. Transactions `from` is inclusive and `to` exclusive, and nothing older than 7 days comes back; the search bounds include both ends and the response echoes the resolved unix value in `query`. OHLCV returns up to 1000 candles per request.

**OHLCV depends on the plan.** No key: `1h` and longer over the last 24 hours. Free key: `10m` and longer over 7 days. Dev: every interval over 30 days. Pro and Enterprise: no plan limit on history. Pool indicators follow the same limits. Token OHLCV and token indicators need Dev or above and follow the same Dev and Pro rules. Outside those limits the API answers `403` with a message naming the plan that allows it. `start=-24h` works on every plan. Current limits: https://docs.dexpaprika.com/knowledge-base/rate-limits#ohlcv-limits-by-plan

## Rate limits and errors

- Rate limits and quotas: 15 requests/minute keyless per IP on 10,000 credits, 30/minute with a free key (register at https://console.dexpaprika.com) on 100,000. Both allowances roll over the last 30 days rather than resetting on the 1st, so a burst today constrains the next 30 days, and a 402 on a free tier carries no `resets_at`. Data is delayed up to 60 seconds on both. Paid plans are real-time, on api-pro.dexpaprika.com with a key: Dev $30/month for 500,000 credits at 120/minute, Pro $99/month for 5,000,000 at 500/minute, each per Stripe billing period with $20 per additional 1M. One request = one credit; a batch endpoint costs one credit per item, and each delivered streaming update costs one credit. Current numbers: https://docs.dexpaprika.com/knowledge-base/rate-limits. Plans and checkout: https://dexpaprika.com/api/pricing
- HTTP errors: `200` OK | `400` bad params | `401` key present and rejected | `402` credit allowance spent (retrying does not help) | `403` wrong host for the key, (`"error":"wrong_host"`), or a paid-only endpoint (token OHLCV, token indicators, pool transactions) called keyless or with a free key (`"error":"plan_required"`, `required_tier` names the plan) | `404` not found | `410` endpoint removed, body names the `replacement` | `429` rate limited | `500` server error
- On `api-pro` a request the edge does not recognise, one with no `Authorization` header for example, gets a `403` HTML page instead of JSON. Fix the header; the next request recovers.
- **On 429 rate limit:** wait the `Retry-After` seconds, then retry. Blocks are temporary. If persistent, contact support@coinpaprika.com.
- Check API health: `dexpaprika-cli status` or `GET https://api.dexpaprika.com/stats`
- Full docs: https://docs.dexpaprika.com
