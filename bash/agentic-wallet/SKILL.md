---
name: agentic-wallet
description: "Crypto wallet operations via the awal CLI — sign in, check balances, send USDC/ETH/POL/SOL, trade tokens, fund the wallet, and use the x402 payment protocol to discover paid services, pay for API calls, monetize an API, or query onchain data. Use whenever the user mentions signing in, login, authentication, wallet status, balance, address, sending money, paying someone, transferring tokens, ENS names, swapping/trading/converting tokens, funding/topping up/onramp, USDC, ETH, POL, SOL, the x402 bazaar, paid APIs, monetizing an endpoint, or querying onchain data on Base."
user-invocable: true
disable-model-invocation: false
allowed-tools: ["Bash(npx awal@2.12.1 *)", "Bash(npm *)", "Bash(node *)", "Bash(curl *)", "Bash(mkdir *)"]
---

# Agentic Wallet

Operate a crypto wallet through the `awal` CLI ([Coinbase agentic-wallet-skills](https://github.com/coinbase/agentic-wallet-skills)). This skill is a router: read the relevant reference file in `references/` for the task at hand.

## Install (Cheshire hub)

```bash
# Official package (agents)
npx skills add coinbase/agentic-wallet-skills

# From this monorepo skills collection
npx skills add ./skills/agentic-wallet
npx skills add ./skills-store/agentic-wallet
npx skills add Solizardking/cheshire-terminal --path skills-store/agentic-wallet
```

## Defining auth / status flow

Complete email OTP sign-in before send/trade/fund (see `references/auth.md`):

```bash
# 1) Check server + auth
npx awal@2.12.1 status
# unpinned alias also works:
npx awal status

# 2) Send OTP to email (flowId printed with --json; also cached locally)
npx awal@2.12.1 auth login you@example.com
npx awal auth login you@example.com

# 3) Complete OTP — primary form (CLI help: <otp>; flowId auto-loaded from login cache)
npx awal@2.12.1 auth verify 123456
npx awal auth verify 123456

# Optional: when you have an explicit flowId from `auth login … --json` or status hints
# (status UX text: verify <flow-id> <6-digit-code>)
npx awal@2.12.1 auth verify <flowId> <otp>

# 4) Confirm authenticated
npx awal@2.12.1 status
npx awal status
```

## Preflight: Confirm wallet state

Before any wallet operation that requires authentication (everything except x402 search/details), check status:

```bash
npx awal@2.12.1 status
```

If the wallet is not authenticated, read `references/auth.md` and complete sign-in first.

## Routing

Pick the reference that matches the task and `Read` it before acting:

| Task | Reference |
| --- | --- |
| Sign in, log in, connect wallet, OTP verification, "not signed in" errors | `references/auth.md` |
| Check balances, "how much USDC/ETH/POL/SOL do I have", balance per chain, JSON balance output | `references/balance.md` |
| Send USDC / ETH / POL / SOL to an address or ENS name (Base, Polygon, Solana) | `references/send-usdc.md` |
| Swap / trade / convert tokens on Base or Polygon | `references/trade.md` |
| Add funds, top up, onramp, buy USDC | `references/fund.md` |
| Find / browse / search paid services on the x402 bazaar | `references/x402-search.md` |
| Call a paid x402 API endpoint with automatic USDC payment | `references/x402-pay.md` |
| Build or deploy a paid API server that other agents can pay to use | `references/x402-monetize.md` |
| Query onchain data on Base (events, transactions, blocks) via the CDP SQL API | `references/query-onchain.md` |

If no clear match and the user wants an external capability, search the x402 bazaar (`references/x402-search.md`) — a paid service may exist.

## Shared rules

- **Input validation**: every reference lists the regexes / allowlists that user-provided values must match before being placed in a shell command. Validate strictly; reject inputs containing spaces, semicolons, pipes, backticks, or other shell metacharacters. Do not pass unvalidated user input into commands.
- **Single-quote `$` amounts**: any amount written as `'$1.00'` must be single-quoted to prevent bash variable expansion.
- **JSON output**: every `awal` command supports `--json` for machine-readable output.
- **Auth errors mean re-auth**: if any command fails with "Not authenticated" or similar, read `references/auth.md` and run the sign-in flow.
- **Insufficient balance**: read `references/fund.md` to top up.

## Quick command index

| Command | Purpose |
| --- | --- |
| `npx awal@2.12.1 status` | Server health + auth status |
| `npx awal@2.12.1 address` | Get wallet address |
| `npx awal@2.12.1 balance` | Get balances across Base, Polygon, Solana (use `--chain` for one chain) |
| `npx awal@2.12.1 show` | Open the wallet companion window (used for funding) |
| `npx awal@2.12.1 auth login <email>` | Send OTP code (flowId via `--json`) |
| `npx awal@2.12.1 auth verify <otp>` | Complete sign-in (cached flowId) |
| `npx awal@2.12.1 auth verify <flowId> <otp>` | Complete sign-in with explicit flowId |
| `npx awal@2.12.1 auth logout` | Sign out and clear the session |
| `npx awal@2.12.1 send <amount> <recipient>` | Send tokens |
| `npx awal@2.12.1 trade <amount> <from> <to>` | Swap tokens |
| `npx awal@2.12.1 x402 bazaar search <query>` | Search paid services |
| `npx awal@2.12.1 x402 bazaar list` | List bazaar resources |
| `npx awal@2.12.1 x402 details <url>` | Inspect payment requirements |
| `npx awal@2.12.1 x402 pay <url>` | Pay and call an x402 endpoint |
