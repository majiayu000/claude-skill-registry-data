---
name: ens
description: Resolve ENS names (.eth) to Ethereum addresses and vice versa. Use when a user provides an .eth name (e.g. "send to vitalik.eth"), when displaying addresses (show ENS names), looking up ENS profiles, or helping users register, renew, or manage .eth names.
homepage: https://docs.ens.domains/
metadata:
  openclaw:
    emoji: "🏷️"
    requires: { env: [] }
---

# ENS (Ethereum Name Service) — Skill

## What this skill does

Enables Gundwane to:
1. **Resolve ENS names** to Ethereum addresses (forward resolution)
2. **Resolve addresses** to ENS names (reverse resolution)
3. **Look up ENS profiles** (avatar, social records, text records)
4. **Help users register, renew, and manage** .eth names on Ethereum mainnet

## When to use

- User mentions any `.eth` name: "send to vitalik.eth", "look up nick.eth", "who is luc.eth"
- Displaying wallet addresses to the user — show the ENS primary name alongside the address
- User asks "what's my ENS?", "do I have an ENS name?", "set my ENS"
- User asks to register a new .eth name, renew an existing one, or update records
- User sends to or receives from an `.eth` address

## ENS Name Detection

Any token matching `*.eth` in user input is likely an ENS name. Examples:
- "send 0.1 ETH to vitalik.eth" → resolve `vitalik.eth`
- "what's the address for nick.eth?" → resolve `nick.eth`
- "register myname.eth" → check availability for `myname`

**Always resolve before using.** Never pass a `.eth` name directly to LI.FI or transaction tools — resolve to a `0x` address first.

## Resolution

### Forward Resolution (Name → Address)

Use `curl` to resolve an ENS name to its Ethereum address. Try in priority order.

#### Approach 1: ENS Subgraph (The Graph)

Best for detailed data (expiry, registrant, resolver). Requires `GRAPH_API_KEY` env var.

```bash
curl -s -X POST \
  --url "https://gateway.thegraph.com/api/$GRAPH_API_KEY/subgraphs/id/5XqPmWe6gjyrJtFn9cLy237i4cWw2j9HcUJEXsP5qGtH" \
  --header 'Content-Type: application/json' \
  --data '{"query":"{ domains(where: { name: \"vitalik.eth\" }) { name resolvedAddress { id } expiryDate registration { registrant { id } expiryDate } } }"}'
```

Response: `data.domains[0].resolvedAddress.id` = the `0x` address.

#### Approach 2: web3.bio API (free, no key needed)

Good for quick resolution + profile data in one call.

```bash
curl -s "https://api.web3.bio/profile/vitalik.eth"
```

Returns JSON with `address`, `identity`, `displayName`, `avatar`, `description`, and linked social profiles. Use the `address` field for the resolved `0x` address.

#### Approach 3: Node.js with viem (fallback)

If APIs are down and `node` is available (viem is in the project deps):

```bash
node --input-type=module -e "
import { createPublicClient, http } from 'viem';
import { mainnet } from 'viem/chains';
import { normalize } from 'viem/ens';
const c = createPublicClient({ chain: mainnet, transport: http('https://eth.llamarpc.com') });
const addr = await c.getEnsAddress({ name: normalize('REPLACE_NAME') });
console.log(JSON.stringify({ address: addr }));
"
```

Replace `REPLACE_NAME` with the actual ENS name.

**Priority:** Approach 1 → 2 → 3. Use whichever is available and fastest.

### Reverse Resolution (Address → Name)

Given a `0x` address, find the primary ENS name.

#### Via ENS Subgraph

```bash
curl -s -X POST \
  --url "https://gateway.thegraph.com/api/$GRAPH_API_KEY/subgraphs/id/5XqPmWe6gjyrJtFn9cLy237i4cWw2j9HcUJEXsP5qGtH" \
  --header 'Content-Type: application/json' \
  --data '{"query":"{ domains(where: { resolvedAddress: \"0xd8da6bf26964af9d7eed9e03e53415d37aa96045\" }) { name } }"}'
```

Note: address must be **lowercase** in the query.

#### Via web3.bio

```bash
curl -s "https://api.web3.bio/profile/0xd8da6bf26964af9d7eed9e03e53415d37aa96045"
```

Returns ENS name and profile if a primary name is set.

#### Via viem (fallback)

```bash
node --input-type=module -e "
import { createPublicClient, http } from 'viem';
import { mainnet } from 'viem/chains';
const c = createPublicClient({ chain: mainnet, transport: http('https://eth.llamarpc.com') });
const name = await c.getEnsName({ address: '0xd8da6bf26964af9d7eed9e03e53415d37aa96045' });
console.log(JSON.stringify({ name }));
"
```

### Profile Lookup

Get ENS profile details: avatar, description, social links, text records.

```bash
curl -s "https://api.web3.bio/profile/nick.eth"
```

Common text record keys (for reference):
- `com.twitter` — Twitter/X handle
- `com.github` — GitHub username
- `url` — Website
- `email` — Email address
- `avatar` — Avatar URL or NFT reference
- `description` — Bio/description
- `com.discord` — Discord handle

### ENS Avatar URL

Direct avatar image:
```
https://metadata.ens.domains/mainnet/avatar/{name}
```

Example: `https://metadata.ens.domains/mainnet/avatar/nick.eth`

Use this URL when displaying a user's ENS avatar in messages.

## Display Rules

### When showing addresses
- After getting a user's wallet via `defi_get_wallet`, optionally check for a reverse ENS name.
- If user has a primary ENS name, display it: `fabri.eth (0xabc...def)`
- In portfolio views, prefer the ENS name when available.
- Don't resolve on every message — cache the result for the session.

### When resolving for transactions
- **Always confirm the resolved address** before executing:
  ```
  vitalik.eth → 0xd8dA...6045
  Send 0.1 ETH to this address?
  ```
- Never blindly trust resolution — ENS records can change. Always show the `0x` address.

### In transaction summaries
- Use both: `0.1 ETH → vitalik.eth (0xd8d...6045) on Base`

## Registration

### .eth Name Registration

Registration happens on **Ethereum mainnet only**. Requires ETH for the name price + gas. If the user's ETH is on L2, flag that they need to bridge first.

**Pricing:**
- 5+ characters: $5/year in ETH
- 4 characters: $160/year in ETH
- 3 characters: $640/year in ETH

**Contracts (Mainnet):**
| Contract | Address |
|----------|---------|
| ENS Registry | `0x00000000000C2E074eC69A0dFb2997BA6C7d2e1e` |
| ETH Registrar Controller | `0x253553366Da8546fC250F225fe3d25d0C782303b` |
| Public Resolver | `0x231b0Ee14048e9dCcD1d247744d114a4EB5E8E63` |
| Reverse Registrar | `0xa58E81fe9b61B5c3fE2AFD33CF304c454AbFc7Cb` |
| Name Wrapper | `0xD4416b13d2b3a9aBae7AcD5D6C2BbDBE25686401` |
| Universal Resolver | `0xce01f8eee7E479C928F8919abD53E553a36CeF67` |

### Check Availability

Via the ENS subgraph:

```bash
curl -s -X POST \
  --url "https://gateway.thegraph.com/api/$GRAPH_API_KEY/subgraphs/id/5XqPmWe6gjyrJtFn9cLy237i4cWw2j9HcUJEXsP5qGtH" \
  --header 'Content-Type: application/json' \
  --data '{"query":"{ registrations(where: { labelName: \"myname\" }) { labelName expiryDate } }"}'
```

If no result or `expiryDate` is in the past (+ 90 day grace period), the name is available.

Or link the user to check directly: `https://ens.app/myname.eth`

### Registration Flow

Registration uses a 2-step commit/reveal process (prevents front-running):

1. **Check availability** (subgraph query above).
2. **Check price**: ~$5/year for 5+ char names. Current ETH price determines the exact cost.
3. **Present summary**:
   ```
   Register myname.eth:
   • Cost: ~0.002 ETH ($5) for 1 year
   • Chain: Ethereum mainnet
   • 2-step process (~2 min total)

   Register?
   ```
4. **Step 1 — Commit**: Call `commit(bytes32)` on the ETH Registrar Controller via `defi_send_transaction` (chainId: 1). The commitment hash must be computed from the name, owner address, duration, and a random secret.
5. **Wait 60 seconds** (tell the user: "Commitment submitted. Registration completes in ~1 minute.").
6. **Step 2 — Register**: Call `register(name, owner, duration, secret, resolver, data, reverseRecord, fuses)` with the name price as `value`.
7. **Confirm**: `myname.eth registered! Yours for 1 year (expires Feb 2027). [View tx](...)`
8. **Store in strategy** and suggest setting a primary name.

**Simpler alternative:** Direct the user to the ENS Manager App for registration: `https://ens.app/myname.eth` — this handles the full flow with a nice UI. Recommend this for first-time registrations.

## Renewal

Simpler than registration — single transaction, no commit step.

When user says "renew myname.eth":

1. Look up current expiry via subgraph or strategy.
2. Get renewal price (same as registration pricing).
3. Present summary:
   ```
   Renew myname.eth:
   • Current expiry: Feb 8, 2027
   • Cost: ~0.002 ETH ($5) for 1 year
   • New expiry: Feb 8, 2028
   ```
4. On approval: Call `renew(string name, uint256 duration)` on the ETH Registrar Controller via `defi_send_transaction` (chainId: 1) with the renewal price as `value`. Duration in seconds (1 year = 31536000).
5. Update expiry in strategy.

**Grace period:** Names have a 90-day grace period after expiry. Only the original owner can renew during this window. After grace period, name goes to public auction with a temporary premium that decreases over 21 days.

## Setting Records

### Set Primary Name (Reverse Record)

When user says "set my ENS primary name" or "make myname.eth my primary":
- Call `setName(string name)` on the Reverse Registrar (`0xa58E81fe9b61B5c3fE2AFD33CF304c454AbFc7Cb`) via `defi_send_transaction` on mainnet (chainId: 1).
- This makes the user's address resolve to `myname.eth` in reverse lookups.
- The user must own the name and it must point to their address.

### Set Text Records

Update social/text records via the Public Resolver (`0x231b0Ee14048e9dCcD1d247744d114a4EB5E8E63`):
- Function: `setText(bytes32 node, string key, string value)`
- The `node` is the namehash of the full name.
- Common keys: `com.twitter`, `com.github`, `url`, `email`, `avatar`, `description`

For complex record updates, recommend the ENS Manager App: `https://ens.app/myname.eth`

## Expiry Monitoring

Store registered ENS names in the user's strategy for heartbeat monitoring:

```json
{
  "ensNames": [
    {
      "name": "fabri.eth",
      "expiry": "2027-02-08T00:00:00Z",
      "isPrimary": true
    }
  ]
}
```

During heartbeats, check `ensNames` from each user's strategy:
- **30 days before expiry**: "Your name fabri.eth expires in 30 days. Want to renew?"
- **7 days before expiry**: "fabri.eth expires in 7 days. Renew now to keep it."
- **Expired (in grace period)**: "fabri.eth expired! You have 90 days to renew before it's released."

## Data Storage — Strategy JSON

ENS data is stored per-user in strategy JSON (via `defi_set_strategy`):

```json
{
  "ensNames": [
    {
      "name": "fabri.eth",
      "expiry": "2027-02-08T00:00:00Z",
      "isPrimary": true
    }
  ],
  "ensPreferences": {
    "showEnsInPortfolio": true,
    "expiryAlertDays": 30
  }
}
```

Read via `defi_get_strategy`, write via `defi_set_strategy`. Automatically per-user.

Narrative data (e.g., "resolved vitalik.eth for a 0.1 ETH transfer") goes to per-user daily memory.

## Rules

1. **Always resolve before transacting.** Never pass `.eth` names to LI.FI or transaction tools. Resolve to a `0x` address first.
2. **Confirm resolved address.** Always show the user the resolved `0x` address before sending funds. ENS records can change.
3. **Mainnet only for registration/renewal.** .eth names live on Ethereum mainnet. Flag if user needs to bridge ETH for gas + fees.
4. **No permission for lookups.** ENS resolution and profile lookups are read operations — do them silently.
5. **Cache within session.** If you resolve a name in a conversation, reuse the result. Don't re-resolve every message.
6. **Handle failures gracefully.** If resolution fails (name doesn't exist, API down), tell the user clearly. Never guess an address.
7. **Monitor expiry during heartbeats.** Check `ensNames` in user strategies. Alert before names expire.
8. **Per-user isolation.** ENS data lives in the user's strategy JSON. Never cross-read.
9. **Suggest ENS once.** If user doesn't have an ENS name and frequently uses their raw address, mention ENS once. Don't push it.
10. **ENSv2 awareness.** ENS is migrating to a new L2-based system (ENSv2). Current mainnet registration still works. Be aware this may change.
