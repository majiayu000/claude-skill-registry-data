---
description: "Launch and trade tokens on Pump.fun bonding curves. Create memecoins, buy/sell tokens, check prices, and collect creator fees on Solana."
---
# Pump.fun Skill

Launch and trade tokens on Pump.fun's bonding curve protocol on Solana.

## Token Launch

Create a new token on pump.fun with metadata:
```bash
# Launch a new token
pumpfun launch --name "My Token" --symbol "MTK" --description "A cool memecoin" --image "./logo.png"

# Launch with initial buy
pumpfun launch --name "My Token" --symbol "MTK" --description "A cool memecoin" --initial-buy 0.5
```

## Trading

Buy tokens from a bonding curve:
```bash
# Buy tokens with 0.1 SOL
pumpfun buy <mint_address> --sol 0.1 --slippage 5

# Get a buy quote first
pumpfun quote buy <mint_address> --sol 0.1
```

Sell tokens to a bonding curve:
```bash
# Sell tokens
pumpfun sell <mint_address> --amount 1000000 --slippage 5

# Get a sell quote first
pumpfun quote sell <mint_address> --amount 1000000
```

## Token Info

Check token price and bonding curve state:
```bash
# Get current price
pumpfun price <mint_address>

# Get bonding curve progress (% to graduation)
pumpfun progress <mint_address>

# Get full bonding curve state
pumpfun info <mint_address>
```

## Creator Fees

Collect accumulated creator fees:
```bash
# Check claimable fees
pumpfun fees check <creator_address>

# Collect fees
pumpfun fees collect
```

## Key Concepts

- **Bonding Curve**: Automated market maker that provides liquidity for new tokens
- **Graduation**: When a token reaches ~85 SOL in the bonding curve, it migrates to PumpSwap AMM
- **Mayhem Mode**: New token creation mode using Token2022 program
- **Slippage**: Percentage tolerance for price changes during trade execution

## Program IDs

- Pump Program: `6EF8rrecthR5Dkzon8Nwu78hRvfCKubJ14M5uBEwF6P`
- PumpSwap: `pAMMBay6oceH9fJKBRHGP5D4bD4sWpmSwMn52FMfXEA`
- Mayhem: `MAyhSmzXzV1pTf7LsNkrNwkWKTo4ougAJ1PPg47MD4e`
