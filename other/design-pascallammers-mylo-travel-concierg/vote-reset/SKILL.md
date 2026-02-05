---
name: vote-reset
description: Generate Safe UI compatible multisig batch JSON to reset veNFT votes. Use when the user wants to reset votes, clear voted status, or prepare vote reset transactions for a multisig wallet.
allowed-tools: Bash, Read, Write, Glob, Grep
---

# Vote Reset Safe Batch Generator

Generate Safe Transaction Builder compatible JSON for resetting veNFT votes on the Lithos protocol.

## Prerequisites

- The `.env` file must contain `RPC_URL` for Plasma mainnet
- The owner address must be a multisig that owns veNFTs

## Contract Addresses (Plasma Mainnet)

- **Voter**: `0x2AF460a511849A7aA37Ac964074475b0E6249c69`
- **VotingEscrow**: `0x2Eff716Caa7F9EB441861340998B0952AF056686`
- **Chain ID**: `9745`

## Instructions

### Step 1: Query veNFTs owned by the address

```bash
source .env && cast call 0x2Eff716Caa7F9EB441861340998B0952AF056686 "balanceOf(address)(uint256)" <OWNER_ADDRESS> --rpc-url $RPC_URL
```

### Step 2: Get all token IDs

For each index from 0 to (balance - 1):

```bash
source .env && cast call 0x2Eff716Caa7F9EB441861340998B0952AF056686 "tokenOfOwnerByIndex(address,uint256)(uint256)" <OWNER_ADDRESS> <INDEX> --rpc-url $RPC_URL
```

### Step 3: Generate reset calldata for each token

```bash
cast calldata "reset(uint256)" <TOKEN_ID>
```

The function selector for `reset(uint256)` is `0x310bd74b`.

### Step 4: Create Safe batch JSON

Generate a JSON file with this structure:

```json
{
  "version": "1.0",
  "chainId": "9745",
  "createdAt": <UNIX_TIMESTAMP>,
  "meta": {
    "name": "Reset votes for <SHORT_ADDRESS> (veNFTs <TOKEN_IDS>)",
    "description": "Resets all active votes for veNFTs owned by <FULL_ADDRESS>. This clears the voted flag on each token, allowing new vote allocations or withdrawals if locks have expired.",
    "txBuilderVersion": "1.16.4"
  },
  "transactions": [
    {
      "to": "0x2AF460a511849A7aA37Ac964074475b0E6249c69",
      "value": "0",
      "data": "<RESET_CALLDATA>",
      "contractMethod": {
        "name": "reset",
        "payable": false,
        "inputs": [
          { "name": "_tokenId", "type": "uint256" }
        ]
      },
      "contractInputsValues": {
        "_tokenId": "<TOKEN_ID>"
      }
    }
  ]
}
```

### Step 5: Write to file

Save the JSON to `safe.vote-reset.json` in the project root.

## Verification

After the transaction is executed, verify the reset was successful:

```bash
source .env && cast call 0x2Eff716Caa7F9EB441861340998B0952AF056686 "voted(uint256)(bool)" <TOKEN_ID> --rpc-url $RPC_URL
```

All tokens should return `false` for their voted status.

## Example Usage

User: "Generate vote reset data for 0x495a98fd059551385Fc9bAbBcFD88878Da3A1b78"

1. Query balance: returns 3
2. Get token IDs: 1163, 1447, 1448
3. Generate calldata for each
4. Create `safe.vote-reset.json` with 3 transactions
5. Report success and file location

## Notes

- The `reset()` function clears all vote allocations for a veNFT
- Resetting is required before withdrawing LITH if the lock has expired
- Resetting allows re-voting with different allocations
- Safe to call even if the token has no active votes (no-op)
