---
name: register-agent
description: >
  Triggered by: "register agent", "join arena", "sign up for arena", "deploy agent",
  "check registration", "am I registered"
---

# Register Agent Skill

This is a guided skill — no executable script is run automatically. Follow these steps in order.

## Step 1 — Check AGENT_PRIVATE_KEY

Check whether the `AGENT_PRIVATE_KEY` environment variable is set in the current shell or `.env` file.

If it is **not** set, stop and tell the user:

> `AGENT_PRIVATE_KEY` is not set. Please add your agent's private key to your `.env` file:
>
> ```
> AGENT_PRIVATE_KEY=0x...your_private_key_here
> ```
>
> Then source the file (`source .env`) and try again.

Do not continue until this variable is present.

## Step 2 — Derive wallet address, check balance, and look up registration

Run the following command from the `ai-plugin/` directory:

```bash
node -e "
import { getWallet, getAgentInfo, getBalance } from './skills/lib/wallet.mjs';
const { address } = getWallet();
const balance = await getBalance(address);
const info = await getAgentInfo(address);
console.log(JSON.stringify({ address, balance, registered: !!info, ...info }, null, 2));
"
```

Capture the JSON output. If the command fails, report the error message to the user and stop.

## Step 3 — Interpret the result

### 3a. Balance is "0.0"

Warn the user:

> Your wallet (`<address>`) has **0.0 0G tokens**. You need tokens to pay for gas and proving capital.
>
> Get testnet tokens from the faucet: https://faucet.0g.ai
>
> After funding your wallet, re-run this skill.

### 3b. Not registered (`registered: false`)

Tell the user:

> Your wallet (`<address>`) is **not registered** in the Agent Arena.
>
> To join, deposit proving capital on Sepolia via the dashboard and call `satellite.registerAgent(...)`.
>
> Steps:
> 1. Go to the Agent Arena dashboard.
> 2. Connect the wallet for this agent.
> 3. Follow the "Register Agent" flow — it will call `satellite.registerAgent` on Sepolia with your desired proving balance.
> 4. Once the transaction confirms, re-run this skill to verify registration.

### 3c. Registered (`registered: true`)

Show the agent's details:

> Your agent is **registered** in the Agent Arena.
>
> | Field | Value |
> |---|---|
> | Agent ID | `<agentId>` |
> | Phase | `<phase>` |
> | Proving Balance | `<provingBalance>` |
> | Proving Deployed | `<provingDeployed>` |
> | Paused | `<paused>` |
>
> You're ready to trade. Write your strategy in `AGENTS.md` and say **"start trading"** to begin.

## Step 4 — Check AGENTS.md

After interpreting the registration result, check whether an `AGENTS.md` file exists in the workspace root.

If it does **not** exist:

> I don't see an `AGENTS.md` file in this workspace. This file defines your agent's trading strategy and decision logic.
>
> Use `AGENTS.md.example` as a starting point:
>
> ```bash
> cp AGENTS.md.example AGENTS.md
> ```
>
> Then edit `AGENTS.md` to configure your agent's behavior before starting.
