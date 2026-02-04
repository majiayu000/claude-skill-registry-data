---
name: vote-set
description: Generate Safe UI compatible multisig batch JSON to set veNFT votes. Use when the user wants to vote on gauges, allocate voting power to pools, or prepare vote transactions for a multisig wallet.
allowed-tools: Bash, Read, Write, Glob, Grep
---

# Vote Set Safe Batch Generator

Generate Safe Transaction Builder compatible JSON for setting veNFT votes on the Lithos protocol.

## Prerequisites

- The `.env` file must contain `RPC_URL` for Plasma mainnet
- The owner address must be a multisig that owns veNFTs
- User must provide target vote amounts for each pool

## Contract Addresses (Plasma Mainnet)

- **Voter**: `0x2AF460a511849A7aA37Ac964074475b0E6249c69`
- **VotingEscrow**: `0x2Eff716Caa7F9EB441861340998B0952AF056686`
- **Chain ID**: `9745`

## Pool Address Reference

| Pool Name | Symbol | Pool Address |
|-----------|--------|--------------|
| XPL/USDT (CL) | aWXPL-USDT | 0x19F4eBc0a1744b93A355C2320899276aE7F79Ee5 |
| USDT/USDe | sAMM-USDe/USDT0 | 0x01b968C1b663C3921Da5BE3C99Ee3c9B89a40B54 |
| WETH/USDT (CL) | aWETH-USDT | 0xca8759814695516C34168BBedd86290964D37adA |
| WETH/WXPL | vAMM-WXPL/WETH | 0x15DF11A0b0917956fEa2b0D6382E5BA100B312df |
| LITH/XPL | vAMM-WXPL/LITH | 0x7dAB98CC51835Beae6dEE43BbdA84cDb96896fb5 |
| MSUSD/USDT0 | sAMM-msUSD/USDT0 | 0xaa1605fbd9c2Cd3854337dB654471a45B2276c12 |
| MSUSD/USDE | sAMM-msUSD/USDe | 0x7257bEC1613d056eD1295721B5f731C05d1302fb |
| XAUT0/USDT0 | vAMM-XAUt0/USDT0 | 0xB1F2724482D8DcCbDCc5480A70622F93d0A66ae8 |
| WXPL/USDT0 (V) | vAMM-WXPL/USDT0 | 0xA0926801A2abC718822a60d8Fa1bc2A51Fa09F1e |
| WETH/weETH (V) | vAMM-WETH/weETH | 0x7483eD877a1423f34Dc5e46CF463ea4A0783d165 |
| WETH/weETH (S) | sAMM-WETH/weETH | 0x82862237F37e8495D88287d72A4C0073250487E0 |
| FBOMB/USDT | vAMM-fBOMB/USDT0 | 0xa82d9DfC3e92907aa4D092f18d89F1C0E129B8AC |
| EBUSD/USDT0 | sAMM-USDT0/ebUSD | 0x4388DcA346165FdC6cbC9e1e388779c66C026d27 |

To get the full list of pools dynamically:

```bash
# Get number of pools
source .env && cast call 0x2AF460a511849A7aA37Ac964074475b0E6249c69 "length()(uint256)" --rpc-url $RPC_URL

# Get pool at index
source .env && cast call 0x2AF460a511849A7aA37Ac964074475b0E6249c69 "pools(uint256)(address)" <INDEX> --rpc-url $RPC_URL

# Get pool symbol
source .env && cast call <POOL_ADDRESS> "symbol()(string)" --rpc-url $RPC_URL
```

## Instructions

### Step 1: Query veNFTs owned by the address

```bash
source .env && cast call 0x2Eff716Caa7F9EB441861340998B0952AF056686 "balanceOf(address)(uint256)" <OWNER_ADDRESS> --rpc-url $RPC_URL
```

### Step 2: Get all token IDs and their voting power

For each index from 0 to (balance - 1):

```bash
# Get token ID
source .env && cast call 0x2Eff716Caa7F9EB441861340998B0952AF056686 "tokenOfOwnerByIndex(address,uint256)(uint256)" <OWNER_ADDRESS> <INDEX> --rpc-url $RPC_URL

# Get voting power for token
source .env && cast call 0x2Eff716Caa7F9EB441861340998B0952AF056686 "balanceOfNFT(uint256)(uint256)" <TOKEN_ID> --rpc-url $RPC_URL
```

### Step 3: Select the best veNFT and strategy

**Key insight**: When voting with a veNFT, its **entire voting power** is distributed proportionally across the pools based on weight ratios. You cannot partially vote - all power gets used.

Compare each veNFT's voting power against the total target votes:
- **Overshoot** (veNFT power > target): Actual votes will be higher than targets, but ratios preserved
- **Undershoot** (veNFT power < target): Actual votes will be lower than targets, but ratios preserved

**Recommended strategy**: Prefer overshooting over undershooting. Select the veNFT whose voting power is closest to (but ideally above) the target total.

Calculate the scale factor and show the user the projected actual votes:

```
scale_factor = veNFT_voting_power / total_target_votes
actual_votes_per_pool = target_weight * scale_factor
```

**Multi-veNFT handling**: If the multisig owns multiple veNFTs:
1. Ask the user whether to vote with ONE veNFT or ALL veNFTs
2. If voting with ONE veNFT, the others should be RESET to clear their votes
3. Include reset transactions in the same batch BEFORE the vote transaction
4. Present the comparison table showing each veNFT's % of target to help user decide

### Step 4: Check if veNFTs have already voted

```bash
source .env && cast call 0x2Eff716Caa7F9EB441861340998B0952AF056686 "voted(uint256)(bool)" <TOKEN_ID> --rpc-url $RPC_URL
```

Check ALL veNFTs, not just the one you plan to vote with. If any veNFT has `voted=true`, include a reset transaction for it in the batch.

### Step 5: Generate reset calldata (if needed)

For any veNFT that needs to be reset (either already voted, or not being used for voting):

```bash
cast calldata "reset(uint256)" <TOKEN_ID>
```

The function selector for `reset(uint256)` is `0x310bd74b`.

### Step 6: Generate vote calldata

**IMPORTANT**: The `vote()` function takes **POOL addresses**, not gauge addresses!

```bash
cast calldata "vote(uint256,address[],uint256[])" <TOKEN_ID> "[<POOL1>,<POOL2>,...]" "[<WEIGHT1>,<WEIGHT2>,...]"
```

The function selector for `vote(uint256,address[],uint256[])` is `0x7ac09bf7`.

### Step 7: Create Safe batch JSON

Generate a JSON file with this structure. **Include reset transactions BEFORE the vote transaction** in the transactions array:

```json
{
  "version": "1.0",
  "chainId": "9745",
  "createdAt": <UNIX_TIMESTAMP>,
  "meta": {
    "name": "Reset #<IDs> & Vote with #<TOKEN_ID>",
    "description": "Reset votes for veNFT #<RESET_IDs>, then cast votes with veNFT #<TOKEN_ID> (<VOTING_POWER> voting power) across <NUM_POOLS> pools.\n\nVote Distribution:\n<POOL_BREAKDOWN_WITH_ACTUAL_VOTES>",
    "txBuilderVersion": "1.16.5"
  },
  "transactions": [
    {
      "to": "0x2AF460a511849A7aA37Ac964074475b0E6249c69",
      "value": "0",
      "data": "<RESET_CALLDATA>",
      "contractMethod": {
        "inputs": [
          {
            "internalType": "uint256",
            "name": "_tokenId",
            "type": "uint256"
          }
        ],
        "name": "reset",
        "payable": false
      },
      "contractInputsValues": {
        "_tokenId": "<RESET_TOKEN_ID>"
      }
    },
    {
      "to": "0x2AF460a511849A7aA37Ac964074475b0E6249c69",
      "value": "0",
      "data": "<VOTE_CALLDATA>",
      "contractMethod": {
        "inputs": [
          {
            "internalType": "uint256",
            "name": "_tokenId",
            "type": "uint256"
          },
          {
            "internalType": "address[]",
            "name": "_poolVote",
            "type": "address[]"
          },
          {
            "internalType": "uint256[]",
            "name": "_weights",
            "type": "uint256[]"
          }
        ],
        "name": "vote",
        "payable": false
      },
      "contractInputsValues": {
        "_tokenId": "<TOKEN_ID>",
        "_poolVote": "[<POOL_ADDRESSES>]",
        "_weights": "[<WEIGHTS>]"
      }
    }
  ]
}
```

### Step 8: Write to file

Save the JSON to `safe-txs/safe.vote-<TOKEN_ID>.json`.

## Verification

After the transaction is executed, verify the vote was successful:

```bash
# Check voted status
source .env && cast call 0x2Eff716Caa7F9EB441861340998B0952AF056686 "voted(uint256)(bool)" <TOKEN_ID> --rpc-url $RPC_URL

# Check vote amount on a specific pool
source .env && cast call 0x2AF460a511849A7aA37Ac964074475b0E6249c69 "votes(uint256,address)(uint256)" <TOKEN_ID> <POOL_ADDRESS> --rpc-url $RPC_URL
```

## Example Usage

User: "Set votes for veNFTs owned by 0x495a98fd059551385Fc9bAbBcFD88878Da3A1b78 with these targets:
- XPL/USDT (V): 4,000,000
- USDT/USDe: 125,000
- LITH/XPL: 1,500,000
- MSUSD/USDT0: 2,000,000
- MSUSD/USDE: 200,000
- XAUT0/USDT0: 35,000"

**Workflow:**

1. Query veNFTs: finds 1163 (11.4M), 1447 (6.67M), 1448 (0.22M)
2. Calculate total target: 7,860,000
3. Present options to user:
   - veNFT #1163: 145% of target (overshoot by +3.5M)
   - veNFT #1447: 85% of target (undershoot by -1.2M)
   - veNFT #1448: 3% of target (way under)
4. User chooses: "Use #1163 and reset the others" (prefers overshoot)
5. Check voted status: #1447 is true (already voted), others false
6. Generate reset calldata for #1447 and #1448
7. Generate vote calldata for #1163
8. Create single batch with: reset #1447 → reset #1448 → vote #1163
9. Report actual vote distribution:
   - XPL/USDT (V): 5,803,896 (target was 4M)
   - MSUSD/USDT0: 2,901,948 (target was 2M)
   - etc.

## Common Mistakes to Avoid

1. **Using gauge addresses instead of pool addresses** - The `vote()` function takes pool addresses. Use the Pool Address Reference table above.

2. **Forgetting to check voted status** - If the veNFT has already voted this epoch, the transaction will fail. Reset first.

3. **Including pools with 0 weight** - Only include pools with non-zero weights in the arrays.

4. **Not resetting unused veNFTs** - If the multisig owns multiple veNFTs but only votes with one, the others' votes from previous epochs may still be active. Always reset veNFTs not being used.

5. **Assuming target weights = actual votes** - The veNFT's entire voting power is distributed proportionally. Actual votes = target × (veNFT_power / total_target). Always show the user the projected actual votes.

6. **Voting with all veNFTs when user wants specific totals** - If user provides target vote amounts, they likely want TOTAL votes across all veNFTs to approximate those targets. Ask whether to use one or all veNFTs.

## Notes

- Votes are proportional: weights determine the ratio, not absolute amounts
- The veNFT's total voting power is distributed across pools based on weight ratios
- Voting automatically resets previous votes for that token
- Votes persist until the next epoch or until manually reset
- Only the veNFT owner or approved address can vote
- **This is a weekly process** - votes need to be set each epoch

## Default Multisig Address

The primary multisig that owns veNFTs: `0x495a98fd059551385Fc9bAbBcFD88878Da3A1b78`

Current veNFTs owned (as of last update):
- #1163: ~11.4M voting power
- #1447: ~6.67M voting power
- #1448: ~0.22M voting power
