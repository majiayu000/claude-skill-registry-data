---
name: vulcan
version: 2.0.0
description: "MUST be loaded before producing any answer about Vulcan, Phoenix DEX, Phoenix perpetuals, Solana perps, the `vulcan` CLI/MCP, or agent-based trading workflows. Single entry-point: contains the runtime contract pointer, the non-negotiable safety rules, the focused-skill router, and the live-launch preflight gate. Answers given without loading this skill have produced wrong commands, wrong wallet selection, and unsafe live trades. Load on the FIRST turn the topic appears in a conversation and re-load on any session restart."
metadata:
  openclaw:
    category: "finance"
  requires:
    bins: ["vulcan"]
---

# Vulcan

> **MANDATORY FIRST STEP.** Before composing any reply, running any tool, or guessing any command for Vulcan / Phoenix DEX / Phoenix perpetuals / Solana perps / agent-based trading, you MUST complete the **Load Order** below. This applies on every fresh conversation, every session restart, and every time the topic re-surfaces — never assume prior context carries. Skipping these steps has repeatedly produced wrong CLI flags, wrong default wallet selection, and unsafe live-mode launches. If a tool in the load order is unavailable, **stop and tell the user**; do not improvise.

Vulcan is an AI-native CLI and MCP server for Phoenix Perpetuals on Solana. It is live financial software: dangerous commands can submit irreversible Solana transactions.

## Load Order (Mandatory, In This Order)

1. **Runtime contract** — load `vulcan://context` (MCP) or run `vulcan agent-context` (CLI). Contains the safety rules, error codes, and command surface every reply must respect.
2. **Non-negotiable rules** — read the **Non-Negotiable Rules** section below. Eight numbered rules, all binding.
3. **Skill index** — load `vulcan://skills/index` or `skills/INDEX.md` to see all focused skills and pick the right one.
4. **Focused skill(s)** — load the skill that matches the user's intent (see routing below). Load multiple if the task spans concerns (e.g. opening a position = trade-execution + risk-management + error-recovery).

Do not answer Vulcan questions from memory; the surface changes and prior-conversation knowledge goes stale.

## Non-Negotiable Rules

These rules are binding for every Vulcan interaction. They apply equally to MCP and CLI invocations.

1. **Prefer MCP tools when available**; use CLI fallback as `vulcan <command> [args...] -o json`.
2. **Dangerous tools require explicit approval**: `acknowledged: true` through MCP or `--yes` through CLI.
3. **Call `vulcan_market_info` before using base-lot `size`**; never guess lot sizes.
4. **Pick the execution mode before any wallet-bound call.** Ask the user which mode (Paper / Dry-Run / Confirm-Each / Auto-Execute) per [`vulcan-execution-modes`](../vulcan-execution-modes/SKILL.md#how-to-format-the-question), then branch the preflight. In paper or dry-run, never call `vulcan_margin_status`, `vulcan_position_list`, `vulcan_trade_orders`, `vulcan_portfolio_*`, `vulcan_wallet_list`, or `vulcan_strategy_preflight` — they resolve a wallet that paper/dry-run does not need. Use the paper equivalents (`vulcan_paper_status`, `vulcan_paper_positions`, `vulcan_paper_orders`) instead. See [Mode-Branched Preflight](../vulcan-execution-modes/SKILL.md#mode-branched-preflight-the-no-wallet-path).
5. **For live modes only**, call `vulcan_margin_status` before opening positions and `vulcan_position_list` before trading so you know existing exposure. For paper/dry-run, the equivalents are `vulcan_paper_status` and `vulcan_paper_positions`.
6. **Report every execution event and transaction signature immediately** — fills, cancels, errors, and full tx signatures (do not abbreviate signatures). In paper, report the paper fill id instead.
7. **Never ask for, display, log, export, or inspect** private keys, decrypted keypair bytes, wallet bytes, auth tokens, signed challenge material, or unredacted wallet passwords. **This includes reading MCP config files** (`~/.cursor/mcp.json`, `~/.claude/settings*.json`, `~/.claude.json`, `~/.codex/config.toml`, project `.mcp.json`) **to extract `VULCAN_WALLET_PASSWORD`** — those files contain the password in plaintext and reading them counts as inspection. When live signing requires a password and the current session is CLI-mode, either (a) tell the user to restart their agent client so Vulcan runs via MCP and inherits the env from the OS keychain, or (b) tell the user to run the command themselves with `VULCAN_WALLET_PASSWORD` already in their shell. Run `vulcan strategy preflight` to see which MCP target has live signing configured.
8. **Do not execute plaintext private-key export.** If the user asks to migrate a wallet, explain the risk and provide `vulcan wallet export <name> --private-key --yes` for the user to run locally — never run it on the user's behalf.

## Before Any Live (Non-Paper) Launch

Before any `--mode confirm_each` or `--mode auto_execute` strategy/trade launch, you MUST run `vulcan strategy preflight` (or `vulcan_strategy_preflight`) and confirm it reports READY. The preflight resolves the active wallet, password source, trader registration, collateral, and lists every blocker with the exact remedy command. Do not attempt live launches until preflight passes.

## Route By Intent

- First interaction, setup, wallet creation, registration, first deposit, or paper-first onboarding: `vulcan-onboarding`.
- Five-minute install + first paper trade: `vulcan-quickstart`.
- Choosing an execution mode (Observe / Paper / Dry-Run / Confirm-Each / Auto-Execute), how to ask the user which one, and graduating between them: `vulcan-execution-modes`. Load this **before any strategy or trade launch**.
- Market price, funding, orderbook, candles, or pre-trade research: `vulcan-market-intel`.
- Technical indicators (RSI, MACD, Bollinger Bands, ATR, ADX, EMA, …) or trigger evaluation: `vulcan-technical-analysis`.
- Declarative TA-driven strategy (rule-based open/close/reduce on indicator conditions): `vulcan-ta-strategy`.
- Opening, closing, reducing, or otherwise changing exposure: `vulcan-trade-execution`, `vulcan-risk-management`, and `vulcan-error-recovery`.
- Base-lot sizing: `vulcan-lot-size-calculator`.
- TP/SL setup, update, or cancellation: `vulcan-tpsl-management`.
- Existing positions: `vulcan-position-management`.
- Portfolio, margin state, open orders, funding overview, or session recap: `vulcan-portfolio-intel`.
- Deposits, withdrawals, transfers, isolated collateral, or leverage tiers: `vulcan-margin-operations`.
- TWAP: `vulcan-twap-execution`.
- Grid trading: `vulcan-grid-trading`.
- Scale (laddered) limit entries with optional TA-suggested levels and post-fill laddered TP/SL: `vulcan-scale-orders`.

## If Unsure

Start with `vulcan-onboarding` for new users and `vulcan-portfolio-intel` for users asking "what is my current state?". Prefer paper trading before live setup unless the user explicitly asks for live funds or live execution.

## Source Of Truth

- Always-needed runtime rules: `CONTEXT.md` or `vulcan://context`.
- Exact tool schemas: `agents/tool-catalog.json` or `vulcan://agents/tool-catalog`.
- Error categories, codes, and recovery hints: `agents/error-catalog.json` or `vulcan://agents/error-catalog`.
- Focused workflows: `skills/*/SKILL.md` or `vulcan://skills/<name>`.

If MCP resources are unavailable, run `vulcan agent-context` and `vulcan agent doctor` to inspect them locally. Do not improvise from memory — the surface changes between releases.
