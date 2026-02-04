---
name: claim-rewards
description: Generate Safe UI compatible multisig batch JSON to claim voting rewards (internal LP fees and external bribes). Use when the user wants to claim bribes, collect voting rewards, or prepare claim transactions for a multisig wallet.
allowed-tools: Bash, Read, Write, Glob, Grep
---

# Claim Voting Rewards Safe Batch Generator

Generate Safe Transaction Builder compatible JSON for claiming all voting rewards (internal LP fees and external bribes) on the Lithos protocol.

## Prerequisites

- The `.env` file must contain `RPC_URL` for Plasma mainnet
- The owner address must be a multisig that owns veNFTs or has claimable rewards

## Contract Addresses (Plasma Mainnet)

- **Voter**: `0x2AF460a511849A7aA37Ac964074475b0E6249c69`
- **VotingEscrow**: `0x2Eff716Caa7F9EB441861340998B0952AF056686`
- **Chain ID**: `9745`

## Key Concepts

### Internal vs External Bribes

- **Internal bribes** (LP fees): Trading fees from liquidity provision, claimed via `claimFees()`
- **External bribes**: Third-party incentives for voting, claimed via `claimBribes()`

### Reward Ownership

Rewards accrue to the **owner address**, not individual veNFT tokenIds. The owner can claim all rewards in a single batch transaction.

## Instructions

### Step 1: Get all pools and gauges

```bash
# Get number of pools
source .env && cast call 0x2AF460a511849A7aA37Ac964074475b0E6249c69 "length()(uint256)" --rpc-url $RPC_URL

# Get pool at index
source .env && cast call 0x2AF460a511849A7aA37Ac964074475b0E6249c69 "pools(uint256)(address)" <INDEX> --rpc-url $RPC_URL

# Get gauge for pool
source .env && cast call 0x2AF460a511849A7aA37Ac964074475b0E6249c69 "gauges(address)(address)" <POOL_ADDRESS> --rpc-url $RPC_URL
```

### Step 2: Get bribe contracts for each gauge

```bash
# Get internal bribe (LP fees)
source .env && cast call 0x2AF460a511849A7aA37Ac964074475b0E6249c69 "internal_bribes(address)(address)" <GAUGE_ADDRESS> --rpc-url $RPC_URL

# Get external bribe
source .env && cast call 0x2AF460a511849A7aA37Ac964074475b0E6249c69 "external_bribes(address)(address)" <GAUGE_ADDRESS> --rpc-url $RPC_URL
```

### Step 3: Get reward tokens for each bribe

```bash
# Get number of reward tokens
source .env && cast call <BRIBE_ADDRESS> "rewardsListLength()(uint256)" --rpc-url $RPC_URL

# Get reward token at index
source .env && cast call <BRIBE_ADDRESS> "rewardTokens(uint256)(address)" <INDEX> --rpc-url $RPC_URL
```

### Step 4: Check claimable amounts

```bash
# Check earned amount for owner
source .env && cast call <BRIBE_ADDRESS> "earned(address,address)(uint256)" <OWNER_ADDRESS> <TOKEN_ADDRESS> --rpc-url $RPC_URL

# IMPORTANT: Check bribe contract has sufficient balance
source .env && cast call <TOKEN_ADDRESS> "balanceOf(address)(uint256)" <BRIBE_ADDRESS> --rpc-url $RPC_URL
```

**CRITICAL**: Only include rewards where `bribe_balance >= earned_amount`. Underfunded bribes will cause the transaction to revert with "ERC20: transfer amount exceeds balance".

### Step 5: Generate claim calldata

For internal bribes (LP fees):

```bash
cast calldata "claimFees(address[],address[][])" "[<BRIBE1>,<BRIBE2>,...]" "[[<TOKEN1A>,<TOKEN1B>],[<TOKEN2A>],...]"
```

For external bribes:

```bash
cast calldata "claimBribes(address[],address[][])" "[<BRIBE1>,<BRIBE2>,...]" "[[<TOKEN1A>,<TOKEN1B>],[<TOKEN2A>],...]"
```

### Step 6: Create Safe batch JSON

Generate a JSON file with this structure:

```json
{
  "version": "1.0",
  "chainId": "9745",
  "createdAt": <UNIX_TIMESTAMP>,
  "meta": {
    "name": "Claim All Voting Rewards for <SHORT_ADDRESS>...",
    "description": "Claim all internal (LP fees) and external bribes across <NUM_BRIBES> bribe contracts for address <FULL_ADDRESS>",
    "txBuilderVersion": "1.16.5"
  },
  "transactions": [
    {
      "to": "0x2AF460a511849A7aA37Ac964074475b0E6249c69",
      "value": "0",
      "data": "<CLAIM_FEES_CALLDATA>",
      "contractMethod": {
        "inputs": [
          { "internalType": "address[]", "name": "_fees", "type": "address[]" },
          { "internalType": "address[][]", "name": "_tokens", "type": "address[][]" }
        ],
        "name": "claimFees",
        "payable": false
      },
      "contractInputsValues": {
        "_fees": "[<BRIBE_ADDRESSES>]",
        "_tokens": "[[<TOKEN_ARRAYS>]]"
      }
    },
    {
      "to": "0x2AF460a511849A7aA37Ac964074475b0E6249c69",
      "value": "0",
      "data": "<CLAIM_BRIBES_CALLDATA>",
      "contractMethod": {
        "inputs": [
          { "internalType": "address[]", "name": "_bribes", "type": "address[]" },
          { "internalType": "address[][]", "name": "_tokens", "type": "address[][]" }
        ],
        "name": "claimBribes",
        "payable": false
      },
      "contractInputsValues": {
        "_bribes": "[<BRIBE_ADDRESSES>]",
        "_tokens": "[[<TOKEN_ARRAYS>]]"
      }
    }
  ]
}
```

### Step 7: Write to file

Save the JSON to `safe-txs/safe.claim-bribes-<OWNER_SHORT>.json`.

## Using the Script

There is an existing script that automates this process:

```bash
npx tsx scripts/claimAllBribesForAddress.ts <OWNER_ADDRESS>
```

This script:
1. Enumerates all 25+ gauges
2. Gets internal and external bribes for each
3. Checks all reward tokens and claimable amounts
4. Verifies bribe contracts have sufficient balance (skips underfunded)
5. Generates Safe batch JSON with `claimFees` and `claimBribes` transactions
6. Outputs a summary of claimable and skipped rewards

## Verification

Simulate the transactions before executing:

```bash
# Simulate claimFees
source .env && cast call 0x2AF460a511849A7aA37Ac964074475b0E6249c69 "<CLAIM_FEES_CALLDATA>" --from <OWNER_ADDRESS> --rpc-url $RPC_URL

# Simulate claimBribes
source .env && cast call 0x2AF460a511849A7aA37Ac964074475b0E6249c69 "<CLAIM_BRIBES_CALLDATA>" --from <OWNER_ADDRESS> --rpc-url $RPC_URL
```

## Example Usage

User: "Claim all voting rewards for 0x495a98fd059551385Fc9bAbBcFD88878Da3A1b78"

1. Run the script or manually enumerate all gauges
2. Find claimable rewards:
   - vAMM-WXPL/USDT0 (internal): 15,625 WXPL, 3,196 USDT0
   - sAMM-msUSD/USDT0 (external): 3,330 USDT0
   - vAMM-WXPL/LITH (internal): 91 WXPL, 3,719 LITH
   - etc.
3. Skip underfunded bribes (e.g., ELITE bribe with insufficient balance)
4. Generate `safe-txs/safe.claim-bribes-0x495a98.json`
5. Simulate both transactions
6. Report success with rewards breakdown

## Common Token Addresses

| Token | Address | Decimals |
|-------|---------|----------|
| WXPL | 0x6100E367285b01F48D07953803A2d8dCA5D19873 | 18 |
| USDT0 | 0xB8CE59FC3717ada4C02eaDF9682A9e934F625ebb | 6 |
| LITH | 0xAbB48792A3161E81B47cA084c0b7A22a50324A44 | 18 |
| USDe | 0x5d3a1Ff2b6BAb83b63cd9AD0787074081a52ef34 | 18 |
| msUSD | 0x29AD7fE4516909b9e498B5a65339e54791293234 | 18 |
| WETH | 0x9895D81bB462A195b4922ED7De0e3ACD007c32CB | 18 |
| ebUSD | 0xEf7B1A03E0897C33b63159e38d779e3970C0E2fc | 18 |
| ELITE | 0x30C8Cf6B46AA4DF3F9fbC2857aca92F10a6cAd7f | 18 |

## Common Mistakes to Avoid

1. **Including underfunded bribes** - Always check `balanceOf(bribe)` >= `earned(owner, token)`. Underfunded bribes will revert the entire batch.

2. **Including tokens with 0 claimable** - Only include tokens where `earned() > 0`.

3. **Using wrong address** - Verify the owner address actually owns veNFTs or has earned rewards.

4. **Missing reward tokens** - Check ALL reward tokens in each bribe contract, not just the first one.

## Notes

- Rewards accrue to the owner address, not individual tokenIds
- Internal bribes are LP trading fees (claimFees)
- External bribes are third-party incentives (claimBribes)
- Both can be batched into a single Safe transaction
- Always simulate before executing to catch revert conditions
- Underfunded bribes are a known issue - skip them and report to protocol team
