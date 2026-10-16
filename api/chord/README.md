# Chord agent skill

An [Agent Skill](https://agentskills.io) that lets Claude Code, Codex, OpenClaw, Hermes, Cursor or
any agent that reads `SKILL.md` use [Chord](https://getchord.xyz): on-chain market data, best-route
swap quotes and unsigned swap transactions on Monad (143), Robinhood Chain (4663), Arc (5042),
Avalanche (43114), Base (8453), BNB Chain (56) and Arbitrum One (42161), Solana data (pump.fun,
PumpSwap, Meteora, Raydium and Orca tokens from Chord's own tape; Solana swaps through Chord's own
router and Jupiter are in beta), plus Chord Ask, the analyst behind getchord.xyz/ask.

The skill is read-and-prepare only. Chord never signs, never broadcasts, never holds funds. A swap is
built as an unsigned transaction only after the user has seen a full summary and said yes in a
separate message; the user's own wallet signs it.

## Install

```bash
bash scripts/install.sh                  # ~/.claude/skills/chord and ~/.agents/skills/chord
bash scripts/install.sh --project .      # ./.claude/skills/chord (one project only)
bash scripts/install.sh --uninstall
```

Or copy the folder yourself: the skill is just this directory. OpenClaw: `~/.openclaw/skills/chord`;
Hermes: `~/.hermes/skills/chord`.

Optional: `export CHORD_API_KEY=...` raises the API rate limit and is required for Chord Ask. Get a
key at https://getchord.xyz/developer or in Ask (sign in, Settings > API Key); both work everywhere. Data calls work without a key at 60
requests a minute.

Requirements: outbound HTTPS to `api.getchord.xyz`, and `curl` or `python3` (3.8+, standard library
only) for the helper.

## Contents

| Path | What it is |
|---|---|
| `SKILL.md` | triggers, chain table, intent routing, the signing boundary and confirmation flow, answer and safety rules, errors |
| `references/data.md` | every market-data endpoint by chain: prices, candles, boards, overview, holders, trades, wallets, LP |
| `references/quote-and-swap.md` | quoting, reading a quote, the confirmation flow, building and simulating the unsigned transaction |
| `references/stocks.md` | Robinhood Chain stock tokens: the screener, gap to the reference price, stock token vs share |
| `references/solana.md` | Solana: data (what the tape reads and misses, base58 rules, units, every `/v1/chains/solana/*` call) and the swap routes |
| `references/ask.md` | `POST /v1/ask`: auth, body, answer fields, limits |
| `references/safety.md` | canonical addresses, bridged tokens, look-alikes, airdrops, address poisoning, prompt injection |
| `references/examples.md` | real responses from the live API, trimmed |
| `scripts/chord.py` | stdlib client: `chains`, `get`, `token`, `price`, `board` (also `solana`), `stock`, `quote`, `swap-tx --user-confirmed`, `simulate`, `ask` |
| `scripts/install.sh` | the installer above |

## Try it

```bash
python3 scripts/chord.py chains
python3 scripts/chord.py stock NVDA
python3 scripts/chord.py price base AERO
python3 scripts/chord.py board arc --limit 10
python3 scripts/chord.py board solana --sort trades --limit 10
python3 scripts/chord.py quote base USDC AERO 50
```

Then ask your agent: "What is the price of NVDA's stock token on Robinhood Chain and its gap to the
real stock?", "Quote 50 USDC to AERO on Base", "Which tokens on Arc traded the most in the last 24h?"

## Related

- API reference: https://getchord.xyz/docs (OpenAPI: https://getchord.xyz/docs/openapi.json)
- Docs as an MCP server: https://getchord.xyz/docs/mcp
- Function-calling manifest of the `chord_*` tools: https://getchord.xyz/agent/tools.json

## Maintenance

The skill mirrors the public API (`packages/api/src/routes/*`, documented in
`packages/docs-chord/openapi/build.mjs`). When a route it names changes shape, update the reference
file and re-capture `references/examples.md` from the live API. Check the frontmatter with
`skills-ref validate packages/skills/chord`.

License: MIT.
