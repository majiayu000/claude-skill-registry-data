---
name: submit-intent
description: >
  Submit a trading intent to the AgentManager contract on 0G Chain.
  Trigger phrases: "submit intent", "open position", "close position",
  "deploy capital", "rebalance".
---

# submit-intent

Submit an on-chain intent that tells the AgentManager what LP action the agent wants to take. The intent is recorded on-chain and evaluated by the arena at the next settlement window.

## Prerequisites

- `AGENT_PRIVATE_KEY` is set in your environment
- The wallet has been registered as an agent (run `register-agent.mjs` first)
- The wallet holds enough 0G native token for gas ([faucet](https://faucet.0g.ai))

## Action types

| Value | Name   | Meaning                              |
|-------|--------|--------------------------------------|
| `0`   | OPEN   | Open a new concentrated LP position  |
| `1`   | CLOSE  | Close (remove) the current position  |
| `2`   | MODIFY | Rebalance to new tick boundaries     |

## Command format

```bash
node skills/submit-intent/submit-intent.mjs <actionType> [paramsJson]
```

`paramsJson` is required for OPEN and MODIFY; omit or pass `{}` for CLOSE.

## Usage examples

| User phrase | Command |
|---|---|
| "Open position at ticks -887272 to 887272 with 100 USDC" | `node skills/submit-intent/submit-intent.mjs 0 '{"amountUSDC":"100","tickLower":-887272,"tickUpper":887272}'` |
| "Close my position" | `node skills/submit-intent/submit-intent.mjs 1` |
| "Rebalance to ticks -100000 to 100000 with 50 USDC" | `node skills/submit-intent/submit-intent.mjs 2 '{"amountUSDC":"50","tickLower":-100000,"tickUpper":100000}'` |
| "Deploy 200 USDC of capital between ticks -60000 and 60000" | `node skills/submit-intent/submit-intent.mjs 0 '{"amountUSDC":"200","tickLower":-60000,"tickUpper":60000}'` |

## paramsJson fields (OPEN / MODIFY only)

| Field | Type | Description |
|-------|------|-------------|
| `amountUSDC` | string | Amount of USDC to deploy (e.g. `"100"`) |
| `tickLower` | number | Lower tick boundary of the LP range |
| `tickUpper` | number | Upper tick boundary of the LP range |

## What it does

1. Reads `AGENT_PRIVATE_KEY` from env and derives the wallet address.
2. Looks up the `agentId` via `AgentManager.addressToAgentId(address)`.
3. ABI-encodes the intent:
   - **CLOSE**: empty bytes (`0x`)
   - **OPEN / MODIFY**: `abi.encode(uint8 actionType, uint256 amountUSDC6, int24 tickLower, int24 tickUpper)`
4. Calls `AgentManager.submitIntent(agentId, intentData)` and waits for confirmation.
5. Prints the transaction hash and block number.

## Environment variables

| Variable | Required | Description |
|----------|----------|-------------|
| `AGENT_PRIVATE_KEY` | Yes | Private key for the agent wallet |
