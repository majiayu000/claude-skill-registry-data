---
name: morpho-solana-frontend
description: Build production-ready frontend for Morpho Blue lending protocol on Solana. Covers all 26 program instructions across supply/borrow, flash loans, liquidations, authorization, and admin features. Uses Next.js 14, Anchor client, Jupiter wallet adapter, and Kamino-style UI/UX. Integrates with morpho-solana-builder skill for contract understanding.
---

# Morpho Solana Frontend Builder

Build a complete, production-ready frontend for the Morpho Blue lending protocol on Solana with all 26 instructions implemented.

## Overview

This skill guides you through building a DeFi lending interface that covers:
- **Core Lending**: Supply, withdraw, borrow, repay, collateral management
- **Flash Loans**: All 3 flash loan modes (single-instruction, two-step start/end)
- **Liquidations**: Unhealthy position scanner and liquidation interface
- **Authorization**: Time-based delegation system with revocation
- **Admin Panel**: Protocol management, whitelisting, fee controls
- **Position Management**: Auto-create positions, close empty positions

## Tech Stack

```typescript
Core Framework:
├── Next.js 14 (App Router)
├── TypeScript
├── TailwindCSS + shadcn/ui
└── Framer Motion

Solana Integration:
├── @solana/web3.js
├── @solana/wallet-adapter-react (Jupiter)
├── @coral-xyz/anchor
└── @solana/spl-token

State Management:
├── Zustand (global state)
├── TanStack Query (async state)
└── WebSocket subscriptions

UI Components:
├── Recharts (analytics)
├── Radix UI (primitives)
└── shadcn/ui (pre-built components)
```

## Project Structure

```
app/
├── (user)/                             # User routes (no auth required)
│   ├── markets/
│   │   ├── page.tsx                    # Markets explorer
│   │   └── [marketId]/
│   │       └── page.tsx                # Market detail
│   ├── dashboard/page.tsx              # User positions
│   ├── liquidations/page.tsx           # Liquidation opportunities
│   ├── flash-loans/page.tsx            # Flash loan interface
│   ├── settings/page.tsx               # User settings
│   └── page.tsx                        # Landing page
├── (admin)/                            # Admin routes (owner only)
│   └── admin/
│       ├── layout.tsx                  # Admin auth wrapper
│       ├── page.tsx                    # Admin dashboard
│       ├── protocol/page.tsx           # Protocol settings
│       ├── markets/page.tsx            # Market management
│       └── whitelist/page.tsx          # LLTV/IRM whitelist
└── layout.tsx                          # Root layout

components/
├── wallet/
│   ├── WalletProvider.tsx              # Jupiter wallet setup
│   ├── WalletButton.tsx                # Connect button
│   └── WalletDropdown.tsx              # Balance, disconnect
├── market/
│   ├── MarketCard.tsx                  # Market list item
│   ├── MarketStats.tsx                 # TVL, APY display
│   └── tabs/
│       ├── SupplyTab.tsx               # supply()
│       ├── WithdrawTab.tsx             # withdraw()
│       ├── CollateralTab.tsx           # supply_collateral() + withdraw_collateral()
│       ├── BorrowTab.tsx               # borrow()
│       ├── RepayTab.tsx                # repay()
│       ├── LiquidateTab.tsx            # liquidate()
│       ├── FlashLoanTab.tsx            # flash_loan() variants
│       └── AuthorizationTab.tsx        # set_authorization()
├── position/
│   ├── PositionCard.tsx                # Position display
│   ├── HealthFactor.tsx                # Health visualization
│   └── PositionManager.tsx             # create_position(), close_position()
├── admin/
│   ├── ProtocolControls.tsx            # Pause, ownership
│   ├── WhitelistManager.tsx            # enable_lltv(), enable_irm()
│   ├── MarketControls.tsx              # set_fee(), set_market_paused()
│   └── FeeClaimButton.tsx              # claim_fees()
├── shared/
│   ├── TokenSelector.tsx               # Token dropdown
│   ├── TransactionModal.tsx            # TX signing flow
│   ├── HealthFactorBar.tsx             # Visual health
│   └── APYBadge.tsx                    # Supply/borrow APY
└── layout/
    ├── Header.tsx                      # Nav + wallet
    ├── Sidebar.tsx                     # Navigation
    └── Footer.tsx

lib/
├── anchor/
│   ├── idl.ts                          # Morpho program IDL
│   ├── client.ts                       # Anchor Program instance
│   └── instructions/
│       ├── supply.ts                   # Supply instruction builders
│       ├── borrow.ts                   # Borrow instruction builders
│       ├── liquidate.ts                # Liquidation instruction
│       ├── flashLoan.ts                # Flash loan instructions
│       ├── admin.ts                    # Admin instructions
│       └── utils.ts                    # Utility instructions
├── hooks/
│   ├── useMarkets.ts                   # Fetch all markets
│   ├── useMarket.ts                    # Fetch single market
│   ├── usePosition.ts                  # User position data
│   ├── usePositions.ts                 # All user positions
│   ├── useLiquidations.ts              # Liquidation opportunities
│   ├── useFlashLoan.ts                 # Flash loan helpers
│   └── useAuthorizations.ts            # User's delegations
├── math/
│   ├── shares.ts                       # Share calculations (ERC-4626)
│   ├── interest.ts                     # APY calculations
│   ├── liquidation.ts                  # LIF, seized collateral
│   └── health.ts                       # Health factor logic
├── constants/
│   ├── addresses.ts                    # Program IDs
│   ├── markets.ts                      # Known markets
│   └── tokens.ts                       # Token metadata
└── utils/
    ├── format.ts                       # Number formatting
    ├── transaction.ts                  # TX builders
    └── websocket.ts                    # Account subscriptions

stores/
├── walletStore.ts                      # Wallet state
├── marketStore.ts                      # Market data cache
└── uiStore.ts                          # UI preferences
```

## Complete Instruction Reference

### Admin Instructions (9 total)

| Instruction | Accounts | Parameters | UI Location |
|------------|----------|------------|-------------|
| `initialize` | payer, protocol_state, system_program | owner, fee_recipient | One-time setup |
| `transfer_ownership` | owner, protocol_state | new_owner | Admin → Protocol |
| `accept_ownership` | pending_owner, protocol_state | - | Admin → Protocol |
| `set_fee_recipient` | owner, protocol_state | new_recipient | Admin → Protocol |
| `set_protocol_paused` | owner, protocol_state | paused | Admin → Protocol |
| `set_market_paused` | owner, protocol_state, market | market_id, paused | Admin → Markets |
| `enable_lltv` | owner, protocol_state | lltv | Admin → Whitelist |
| `enable_irm` | owner, protocol_state | irm | Admin → Whitelist |
| `set_fee` | owner, protocol_state, market | market_id, fee | Admin → Markets |

### Market Instructions (1 total)

| Instruction | Accounts | Parameters | UI Location |
|------------|----------|------------|-------------|
| `create_market` | creator, protocol_state, market, collateral_mint, loan_mint, collateral_vault, loan_vault, oracle, irm, token_program, system_program | collateral_mint, loan_mint, oracle, irm, lltv | Markets → Create |

### Position Instructions (2 total)

| Instruction | Accounts | Parameters | UI Location |
|------------|----------|------------|-------------|
| `create_position` | payer, owner, market, position, system_program | market_id | Auto-prepend |
| `close_position` | owner, rent_receiver, position | market_id | Dashboard |

### Supply Instructions (2 total)

| Instruction | Accounts | Parameters | UI Location |
|------------|----------|------------|-------------|
| `supply` | supplier, protocol_state, market, position, on_behalf_of, supplier_token_account, loan_vault, loan_mint, token_program | market_id, assets, min_shares | Market → Supply |
| `withdraw` | caller, protocol_state, market, position, authorization (optional), receiver_token_account, loan_vault, loan_mint, token_program | market_id, assets, shares | Market → Withdraw |

### Borrow Instructions (4 total)

| Instruction | Accounts | Parameters | UI Location |
|------------|----------|------------|-------------|
| `supply_collateral` | depositor, protocol_state, market, position, on_behalf_of, depositor_token_account, collateral_vault, collateral_mint, token_program | market_id, amount | Market → Collateral |
| `withdraw_collateral` | caller, protocol_state, market, position, authorization (optional), oracle, receiver_token_account, collateral_vault, collateral_mint, token_program | market_id, amount | Market → Collateral |
| `borrow` | caller, protocol_state, market, position, authorization (optional), oracle, receiver_token_account, loan_vault, loan_mint, token_program | market_id, assets, max_shares | Market → Borrow |
| `repay` | repayer, market, position, on_behalf_of, repayer_token_account, loan_vault, loan_mint, token_program | market_id, assets, shares | Market → Repay |

### Liquidation Instructions (1 total)

| Instruction | Accounts | Parameters | UI Location |
|------------|----------|------------|-------------|
| `liquidate` | liquidator, market, borrower_position, borrower, oracle, liquidator_loan_account, liquidator_collateral_account, loan_vault, collateral_vault, loan_mint, collateral_mint, token_program | market_id, seized_assets | Market → Liquidate |

### Flash Loan Instructions (3 total)

| Instruction | Accounts | Parameters | UI Location |
|------------|----------|------------|-------------|
| `flash_loan_start` | borrower, protocol_state, market, borrower_token_account, loan_vault, loan_mint, token_program | market_id, amount | Flash Loans |
| `flash_loan_end` | borrower, market, borrower_token_account, loan_vault, loan_mint, token_program | market_id, borrowed_amount | Flash Loans |
| `flash_loan` | borrower, protocol_state, market, borrower_token_account, loan_vault, loan_mint, token_program | market_id, amount | Flash Loans |

### Utility Instructions (4 total)

| Instruction | Accounts | Parameters | UI Location |
|------------|----------|------------|-------------|
| `accrue_interest_ix` | market | market_id | Auto-called |
| `set_authorization` | authorizer, authorized, authorization, system_program | is_authorized, expires_at | Settings → Auth |
| `revoke_authorization` | authorizer, authorization | - | Settings → Auth |
| `claim_fees` | protocol_state, market, fee_position | market_id | Admin → Markets |

## Implementation Guide

### Step 1: Setup Anchor Client

```typescript
// lib/anchor/client.ts
import { Program, AnchorProvider, Idl } from '@coral-xyz/anchor';
import { Connection, PublicKey } from '@solana/web3.js';
import { AnchorWallet } from '@solana/wallet-adapter-react';
import IDL from './idl.json';

export const MORPHO_PROGRAM_ID = new PublicKey('YOUR_PROGRAM_ID');

export function getMorphoProgram(
  connection: Connection,
  wallet: AnchorWallet
) {
  const provider = new AnchorProvider(connection, wallet, {
    commitment: 'confirmed',
  });
  
  return new Program(IDL as Idl, MORPHO_PROGRAM_ID, provider);
}

// Derive PDAs
export const PROGRAM_SEED = Buffer.from('morpho');

export function getProtocolStatePDA() {
  return PublicKey.findProgramAddressSync(
    [PROGRAM_SEED, Buffer.from('protocol_state')],
    MORPHO_PROGRAM_ID
  );
}

export function getMarketPDA(
  collateralMint: PublicKey,
  loanMint: PublicKey,
  oracle: PublicKey,
  irm: PublicKey,
  lltv: number
) {
  const marketId = calculateMarketId(collateralMint, loanMint, oracle, irm, lltv);
  return PublicKey.findProgramAddressSync(
    [PROGRAM_SEED, Buffer.from('market'), marketId],
    MORPHO_PROGRAM_ID
  );
}

export function getPositionPDA(
  marketId: Buffer,
  owner: PublicKey
) {
  return PublicKey.findProgramAddressSync(
    [PROGRAM_SEED, Buffer.from('position'), marketId, owner.toBuffer()],
    MORPHO_PROGRAM_ID
  );
}

export function getAuthorizationPDA(
  authorizer: PublicKey,
  authorized: PublicKey
) {
  return PublicKey.findProgramAddressSync(
    [
      PROGRAM_SEED,
      Buffer.from('authorization'),
      authorizer.toBuffer(),
      authorized.toBuffer()
    ],
    MORPHO_PROGRAM_ID
  );
}

// Market ID calculation (keccak256)
import { keccak256 } from 'js-sha3';

export function calculateMarketId(
  collateralMint: PublicKey,
  loanMint: PublicKey,
  oracle: PublicKey,
  irm: PublicKey,
  lltv: number
): Buffer {
  const data = Buffer.concat([
    collateralMint.toBuffer(),
    loanMint.toBuffer(),
    oracle.toBuffer(),
    irm.toBuffer(),
    Buffer.from(new BN(lltv).toArray('le', 8))
  ]);
  
  return Buffer.from(keccak256(data), 'hex');
}
```

### Step 2: Core Instruction Builders

```typescript
// lib/anchor/instructions/supply.ts
import { BN } from '@coral-xyz/anchor';
import { PublicKey, TransactionInstruction } from '@solana/web3.js';
import { getAssociatedTokenAddress } from '@solana/spl-token';

export async function buildSupplyInstruction(
  program: Program,
  marketId: Buffer,
  supplier: PublicKey,
  onBehalfOf: PublicKey,
  assets: BN,
  minShares: BN
): Promise<TransactionInstruction> {
  const [protocolState] = getProtocolStatePDA();
  const [market] = getMarketPDA(/* derive from marketId */);
  const [position] = getPositionPDA(marketId, onBehalfOf);
  
  const marketAccount = await program.account.market.fetch(market);
  
  const supplierTokenAccount = await getAssociatedTokenAddress(
    marketAccount.loanMint,
    supplier
  );
  
  const [loanVault] = PublicKey.findProgramAddressSync(
    [PROGRAM_SEED, Buffer.from('loan_vault'), marketId],
    MORPHO_PROGRAM_ID
  );
  
  return program.methods
    .supply(Array.from(marketId), assets, minShares)
    .accounts({
      supplier,
      protocolState,
      market,
      position,
      onBehalfOf,
      supplierTokenAccount,
      loanVault,
      loanMint: marketAccount.loanMint,
      tokenProgram: TOKEN_PROGRAM_ID,
    })
    .instruction();
}

export async function buildWithdrawInstruction(
  program: Program,
  marketId: Buffer,
  caller: PublicKey,
  positionOwner: PublicKey,
  receiver: PublicKey,
  assets: BN,
  shares: BN,
  authorization?: PublicKey
): Promise<TransactionInstruction> {
  // Similar structure to supply
  // Key difference: assets OR shares (not both)
  // Include authorization account if caller != positionOwner
  
  return program.methods
    .withdraw(Array.from(marketId), assets, shares)
    .accounts({
      caller,
      protocolState,
      market,
      position,
      authorization: authorization || null,
      receiverTokenAccount,
      loanVault,
      loanMint,
      tokenProgram: TOKEN_PROGRAM_ID,
    })
    .instruction();
}
```

```typescript
// lib/anchor/instructions/borrow.ts
export async function buildBorrowInstruction(
  program: Program,
  marketId: Buffer,
  caller: PublicKey,
  positionOwner: PublicKey,
  receiver: PublicKey,
  assets: BN,
  maxShares: BN,
  oracle: PublicKey,
  authorization?: PublicKey
): Promise<TransactionInstruction> {
  const [market] = getMarketPDA(/* ... */);
  const [position] = getPositionPDA(marketId, positionOwner);
  
  const marketAccount = await program.account.market.fetch(market);
  
  return program.methods
    .borrow(Array.from(marketId), assets, maxShares)
    .accounts({
      caller,
      protocolState,
      market,
      position,
      authorization: authorization || null,
      oracle,
      receiverTokenAccount,
      loanVault,
      loanMint: marketAccount.loanMint,
      tokenProgram: TOKEN_PROGRAM_ID,
    })
    .instruction();
}

export async function buildRepayInstruction(
  program: Program,
  marketId: Buffer,
  repayer: PublicKey,
  onBehalfOf: PublicKey,
  assets: BN,
  shares: BN
): Promise<TransactionInstruction> {
  // Similar to withdraw: assets OR shares
  
  return program.methods
    .repay(Array.from(marketId), assets, shares)
    .accounts({
      repayer,
      market,
      position,
      onBehalfOf,
      repayerTokenAccount,
      loanVault,
      loanMint,
      tokenProgram: TOKEN_PROGRAM_ID,
    })
    .instruction();
}
```

```typescript
// lib/anchor/instructions/flashLoan.ts
export async function buildFlashLoanInstruction(
  program: Program,
  marketId: Buffer,
  borrower: PublicKey,
  amount: BN
): Promise<TransactionInstruction> {
  // Single-instruction flash loan
  // Repayment validated automatically via vault reload
  
  return program.methods
    .flashLoan(Array.from(marketId), amount)
    .accounts({
      borrower,
      protocolState,
      market,
      borrowerTokenAccount,
      loanVault,
      loanMint,
      tokenProgram: TOKEN_PROGRAM_ID,
    })
    .instruction();
}

export async function buildFlashLoanStartInstruction(
  program: Program,
  marketId: Buffer,
  borrower: PublicKey,
  amount: BN
): Promise<TransactionInstruction> {
  // Two-step: start (locks market, transfers out)
  
  return program.methods
    .flashLoanStart(Array.from(marketId), amount)
    .accounts({
      borrower,
      protocolState,
      market,
      borrowerTokenAccount,
      loanVault,
      loanMint,
      tokenProgram: TOKEN_PROGRAM_ID,
    })
    .instruction();
}

export async function buildFlashLoanEndInstruction(
  program: Program,
  marketId: Buffer,
  borrower: PublicKey,
  borrowedAmount: BN
): Promise<TransactionInstruction> {
  // Two-step: end (validates repayment, unlocks market)
  
  return program.methods
    .flashLoanEnd(Array.from(marketId), borrowedAmount)
    .accounts({
      borrower,
      market,
      borrowerTokenAccount,
      loanVault,
      loanMint,
      tokenProgram: TOKEN_PROGRAM_ID,
    })
    .instruction();
}
```

### Step 3: Position Auto-Creation

```typescript
// lib/utils/transaction.ts
export async function ensurePositionExists(
  program: Program,
  marketId: Buffer,
  owner: PublicKey
): Promise<TransactionInstruction | null> {
  const [position] = getPositionPDA(marketId, owner);
  
  try {
    await program.account.position.fetch(position);
    return null; // Position exists
  } catch (e) {
    // Position doesn't exist, create it
    return program.methods
      .createPosition(Array.from(marketId))
      .accounts({
        payer: owner,
        owner,
        market: getMarketPDA(/* ... */)[0],
        position,
        systemProgram: SystemProgram.programId,
      })
      .instruction();
  }
}

// Usage in any instruction that needs position
export async function buildSupplyTransactionWithPosition(
  program: Program,
  marketId: Buffer,
  supplier: PublicKey,
  onBehalfOf: PublicKey,
  assets: BN,
  minShares: BN
): Promise<TransactionInstruction[]> {
  const instructions: TransactionInstruction[] = [];
  
  // Prepend create_position if needed
  const createPosIx = await ensurePositionExists(program, marketId, onBehalfOf);
  if (createPosIx) {
    instructions.push(createPosIx);
  }
  
  // Add supply instruction
  const supplyIx = await buildSupplyInstruction(
    program,
    marketId,
    supplier,
    onBehalfOf,
    assets,
    minShares
  );
  instructions.push(supplyIx);
  
  return instructions;
}
```

### Step 4: React Hooks for Data Fetching

```typescript
// lib/hooks/useMarkets.ts
import { useQuery } from '@tanstack/react-query';
import { useConnection } from '@solana/wallet-adapter-react';

export function useMarkets() {
  const { connection } = useConnection();
  
  return useQuery({
    queryKey: ['markets'],
    queryFn: async () => {
      const program = getMorphoProgram(connection, /* ... */);
      
      // Fetch all Market accounts
      const markets = await program.account.market.all();
      
      // Enrich with APY calculations, TVL, etc.
      return Promise.all(
        markets.map(async (m) => {
          const supplyAPY = await calculateSupplyAPY(m.account);
          const borrowAPY = await calculateBorrowAPY(m.account);
          const tvl = calculateTVL(m.account);
          
          return {
            publicKey: m.publicKey,
            account: m.account,
            supplyAPY,
            borrowAPY,
            tvl,
          };
        })
      );
    },
    refetchInterval: 10_000, // Refresh every 10s
  });
}

// lib/hooks/usePosition.ts
export function usePosition(marketId: Buffer, owner?: PublicKey) {
  const { connection } = useConnection();
  const { publicKey } = useWallet();
  
  const positionOwner = owner || publicKey;
  
  return useQuery({
    queryKey: ['position', marketId.toString('hex'), positionOwner?.toString()],
    queryFn: async () => {
      if (!positionOwner) return null;
      
      const program = getMorphoProgram(connection, /* ... */);
      const [position] = getPositionPDA(marketId, positionOwner);
      
      try {
        const account = await program.account.position.fetch(position);
        
        // Fetch parent market for calculations
        const [market] = getMarketPDA(/* ... */);
        const marketAccount = await program.account.market.fetch(market);
        
        // Calculate current values
        const supplyAssets = toAssetsDown(
          account.supplyShares,
          marketAccount.totalSupplyAssets,
          marketAccount.totalSupplyShares
        );
        
        const borrowAssets = toAssetsUp(
          account.borrowShares,
          marketAccount.totalBorrowAssets,
          marketAccount.totalBorrowShares
        );
        
        // Calculate health factor
        const healthFactor = calculateHealthFactor(
          account.collateral,
          borrowAssets,
          marketAccount.lltv,
          oraclePrice // fetch from oracle
        );
        
        return {
          publicKey: position,
          account,
          supplyAssets,
          borrowAssets,
          healthFactor,
        };
      } catch (e) {
        return null; // Position doesn't exist
      }
    },
    enabled: !!positionOwner,
    refetchInterval: 5_000,
  });
}
```

### Step 5: WebSocket Subscriptions

```typescript
// lib/utils/websocket.ts
import { Connection, PublicKey } from '@solana/web3.js';

export function subscribeToPosition(
  connection: Connection,
  positionPubkey: PublicKey,
  callback: (accountInfo: any) => void
): number {
  return connection.onAccountChange(
    positionPubkey,
    (accountInfo) => {
      callback(accountInfo);
    },
    'confirmed'
  );
}

// Usage in React component
export function usePositionSubscription(positionPubkey?: PublicKey) {
  const { connection } = useConnection();
  const queryClient = useQueryClient();
  
  useEffect(() => {
    if (!positionPubkey) return;
    
    const subscriptionId = subscribeToPosition(
      connection,
      positionPubkey,
      () => {
        // Invalidate query to refetch
        queryClient.invalidateQueries(['position', positionPubkey.toString()]);
      }
    );
    
    return () => {
      connection.removeAccountChangeListener(subscriptionId);
    };
  }, [positionPubkey, connection, queryClient]);
}
```

### Step 6: Math Libraries (Client-side)

```typescript
// lib/math/shares.ts
import BN from 'bn.js';

const VIRTUAL_SHARES = new BN(1_000_000); // 1e6
const VIRTUAL_ASSETS = new BN(1);

export function toSharesDown(
  assets: BN,
  totalAssets: BN,
  totalShares: BN
): BN {
  // shares = assets * (totalShares + VIRTUAL_SHARES) / (totalAssets + VIRTUAL_ASSETS)
  const numerator = assets.mul(totalShares.add(VIRTUAL_SHARES));
  const denominator = totalAssets.add(VIRTUAL_ASSETS);
  return numerator.div(denominator);
}

export function toSharesUp(
  assets: BN,
  totalAssets: BN,
  totalShares: BN
): BN {
  const numerator = assets.mul(totalShares.add(VIRTUAL_SHARES));
  const denominator = totalAssets.add(VIRTUAL_ASSETS);
  
  // Ceiling division: (a + b - 1) / b
  return numerator.add(denominator).sub(new BN(1)).div(denominator);
}

export function toAssetsDown(
  shares: BN,
  totalAssets: BN,
  totalShares: BN
): BN {
  // assets = shares * (totalAssets + VIRTUAL_ASSETS) / (totalShares + VIRTUAL_SHARES)
  const numerator = shares.mul(totalAssets.add(VIRTUAL_ASSETS));
  const denominator = totalShares.add(VIRTUAL_SHARES);
  return numerator.div(denominator);
}

export function toAssetsUp(
  shares: BN,
  totalAssets: BN,
  totalShares: BN
): BN {
  const numerator = shares.mul(totalAssets.add(VIRTUAL_ASSETS));
  const denominator = totalShares.add(VIRTUAL_SHARES);
  
  return numerator.add(denominator).sub(new BN(1)).div(denominator);
}

// lib/math/health.ts
export function calculateHealthFactor(
  collateral: BN,
  borrowAssets: BN,
  lltv: number, // basis points
  oraclePrice: BN // scaled 1e36
): number {
  if (borrowAssets.isZero()) return Infinity;
  
  // maxBorrow = collateral * price * lltv / 1e36 / 10000
  const maxBorrow = collateral
    .mul(oraclePrice)
    .mul(new BN(lltv))
    .div(new BN(10).pow(new BN(36)))
    .div(new BN(10000));
  
  // healthFactor = maxBorrow / borrowAssets
  return maxBorrow.mul(new BN(1000)).div(borrowAssets).toNumber() / 1000;
}

export function isLiquidatable(
  collateral: BN,
  borrowShares: BN,
  totalBorrowAssets: BN,
  totalBorrowShares: BN,
  oraclePrice: BN,
  lltv: number
): boolean {
  const borrowAssets = toAssetsUp(borrowShares, totalBorrowAssets, totalBorrowShares);
  const healthFactor = calculateHealthFactor(collateral, borrowAssets, lltv, oraclePrice);
  return healthFactor < 1.0;
}

// lib/math/liquidation.ts
export function calculateLIF(lltv: number): number {
  // LIF = min(1.15, 1 / (1 - 0.3 * (1 - lltv/10000)))
  const lltvDecimal = lltv / 10000;
  const baseLIF = 1 / (1 - 0.3 * (1 - lltvDecimal));
  return Math.min(1.15, baseLIF);
}

export function calculateSeizedCollateral(
  seizedAssets: BN,
  oraclePrice: BN, // 1e36
  lif: number
): BN {
  // seizedCollateral = seizedAssets * LIF * 1e36 / price
  const lifScaled = new BN(Math.floor(lif * 1000)); // Scale LIF by 1000
  
  return seizedAssets
    .mul(lifScaled)
    .mul(new BN(10).pow(new BN(36)))
    .div(oraclePrice)
    .div(new BN(1000));
}
```

## Component Implementation Examples

### Supply Tab

```typescript
// components/market/tabs/SupplyTab.tsx
'use client';

import { useState } from 'react';
import { BN } from '@coral-xyz/anchor';
import { useWallet } from '@solana/wallet-adapter-react';
import { Input } from '@/components/ui/input';
import { Button } from '@/components/ui/button';
import { buildSupplyTransactionWithPosition } from '@/lib/anchor/instructions/supply';
import { toSharesDown } from '@/lib/math/shares';

export function SupplyTab({ marketId, market }: Props) {
  const { publicKey, sendTransaction } = useWallet();
  const [amount, setAmount] = useState('');
  const [loading, setLoading] = useState(false);
  
  const handleSupply = async () => {
    if (!publicKey || !amount) return;
    
    setLoading(true);
    try {
      const assets = new BN(parseFloat(amount) * 10 ** market.loanDecimals);
      
      // Calculate min shares with 1% slippage
      const expectedShares = toSharesDown(
        assets,
        market.totalSupplyAssets,
        market.totalSupplyShares
      );
      const minShares = expectedShares.mul(new BN(99)).div(new BN(100));
      
      // Build transaction with auto position creation
      const instructions = await buildSupplyTransactionWithPosition(
        program,
        marketId,
        publicKey,
        publicKey, // on_behalf_of
        assets,
        minShares
      );
      
      const tx = new Transaction().add(...instructions);
      const signature = await sendTransaction(tx, connection);
      
      await connection.confirmTransaction(signature, 'confirmed');
      
      toast.success('Supply successful!');
    } catch (error) {
      console.error(error);
      toast.error('Supply failed');
    } finally {
      setLoading(false);
    }
  };
  
  return (
    <div className="space-y-4">
      <div>
        <label>Amount to Supply</label>
        <Input
          type="number"
          value={amount}
          onChange={(e) => setAmount(e.target.value)}
          placeholder="0.00"
        />
        <div className="text-sm text-muted-foreground mt-1">
          Balance: {userBalance} {market.loanSymbol}
        </div>
      </div>
      
      <div className="border rounded-lg p-4 space-y-2">
        <div className="flex justify-between">
          <span>You'll receive</span>
          <span className="font-mono">
            {expectedShares.toString()} shares
          </span>
        </div>
        <div className="flex justify-between">
          <span>Supply APY</span>
          <span className="text-green-600">{supplyAPY}%</span>
        </div>
      </div>
      
      <Button
        onClick={handleSupply}
        disabled={loading || !amount}
        className="w-full"
      >
        {loading ? 'Supplying...' : 'Supply'}
      </Button>
    </div>
  );
}
```

### Health Factor Component

```typescript
// components/position/HealthFactor.tsx
export function HealthFactorBar({ healthFactor }: { healthFactor: number }) {
  const getColor = (hf: number) => {
    if (hf > 1.5) return 'bg-green-500';
    if (hf > 1.2) return 'bg-yellow-500';
    if (hf > 1.05) return 'bg-orange-500';
    return 'bg-red-500';
  };
  
  const getLabel = (hf: number) => {
    if (hf > 1.5) return 'Safe';
    if (hf > 1.2) return 'Caution';
    if (hf > 1.05) return 'Warning';
    return 'Critical';
  };
  
  const percentage = Math.min((healthFactor / 2) * 100, 100);
  
  return (
    <div className="space-y-2">
      <div className="flex justify-between items-center">
        <span className="text-sm font-medium">Health Factor</span>
        <span className="font-mono text-lg">{healthFactor.toFixed(2)}</span>
      </div>
      
      <div className="relative h-2 bg-gray-200 rounded-full overflow-hidden">
        <div
          className={`absolute h-full ${getColor(healthFactor)} transition-all`}
          style={{ width: `${percentage}%` }}
        />
      </div>
      
      <div className="flex justify-between text-xs text-muted-foreground">
        <span>{getLabel(healthFactor)}</span>
        <span>Liquidation at &lt;1.0</span>
      </div>
    </div>
  );
}
```

### Authorization Tab

```typescript
// components/market/tabs/AuthorizationTab.tsx
export function AuthorizationTab() {
  const { publicKey } = useWallet();
  const [authorized, setAuthorized] = useState('');
  const [expiresAt, setExpiresAt] = useState<Date | null>(null);
  const [neverExpires, setNeverExpires] = useState(false);
  
  const { data: authorizations } = useAuthorizations(publicKey);
  
  const handleGrant = async () => {
    if (!publicKey || !authorized) return;
    
    const expiryTimestamp = neverExpires
      ? Number.MAX_SAFE_INTEGER
      : Math.floor((expiresAt?.getTime() || Date.now()) / 1000);
    
    const ix = await buildSetAuthorizationInstruction(
      program,
      publicKey,
      new PublicKey(authorized),
      true,
      new BN(expiryTimestamp)
    );
    
    // Send transaction...
  };
  
  const handleRevoke = async (authPubkey: PublicKey) => {
    const ix = await buildRevokeAuthorizationInstruction(
      program,
      publicKey,
      authPubkey
    );
    
    // Send transaction...
  };
  
  return (
    <div className="space-y-6">
      <Card>
        <CardHeader>
          <CardTitle>Grant New Authorization</CardTitle>
        </CardHeader>
        <CardContent className="space-y-4">
          <div>
            <label>Authorized Address</label>
            <Input
              value={authorized}
              onChange={(e) => setAuthorized(e.target.value)}
              placeholder="Enter Solana address"
            />
          </div>
          
          <div>
            <label>Expiry Date</label>
            <div className="space-y-2">
              <Checkbox
                checked={neverExpires}
                onCheckedChange={(checked) => setNeverExpires(checked as boolean)}
              >
                Never expires
              </Checkbox>
              {!neverExpires && (
                <DatePicker
                  value={expiresAt}
                  onChange={setExpiresAt}
                  minDate={new Date()}
                />
              )}
            </div>
          </div>
          
          <Button onClick={handleGrant} className="w-full">
            Grant Authorization
          </Button>
        </CardContent>
      </Card>
      
      <Card>
        <CardHeader>
          <CardTitle>Active Authorizations</CardTitle>
        </CardHeader>
        <CardContent>
          {authorizations?.map((auth) => (
            <div key={auth.publicKey.toString()} className="border-b py-4">
              <div className="flex justify-between items-start">
                <div>
                  <p className="font-mono text-sm">
                    {auth.account.authorized.toString()}
                  </p>
                  <p className="text-xs text-muted-foreground">
                    {auth.account.isRevoked ? (
                      <span className="text-red-500">Revoked ×</span>
                    ) : (
                      <span className="text-green-500">Active ✓</span>
                    )}
                  </p>
                  <p className="text-xs text-muted-foreground">
                    Expires: {formatDate(auth.account.expiresAt)}
                  </p>
                </div>
                
                {!auth.account.isRevoked && (
                  <Button
                    variant="destructive"
                    size="sm"
                    onClick={() => handleRevoke(auth.publicKey)}
                  >
                    Revoke
                  </Button>
                )}
              </div>
            </div>
          ))}
        </CardContent>
      </Card>
    </div>
  );
}
```

## Critical Implementation Notes

### 1. Assets vs Shares Flexibility

```typescript
// withdraw() and repay() accept EITHER assets OR shares
// UI should provide toggle:

function WithdrawTab() {
  const [mode, setMode] = useState<'assets' | 'shares'>('assets');
  const [amount, setAmount] = useState('');
  
  const handleWithdraw = async () => {
    const assets = mode === 'assets' ? new BN(amount) : new BN(0);
    const shares = mode === 'shares' ? new BN(amount) : new BN(0);
    
    const ix = await buildWithdrawInstruction(
      program,
      marketId,
      publicKey,
      publicKey,
      publicKey,
      assets,
      shares
    );
    
    // Send...
  };
  
  return (
    <div>
      <Tabs value={mode} onValueChange={setMode}>
        <TabsList>
          <TabsTrigger value="assets">By Amount</TabsTrigger>
          <TabsTrigger value="shares">By Shares</TabsTrigger>
        </TabsList>
      </Tabs>
      
      <Input
        value={amount}
        onChange={(e) => setAmount(e.target.value)}
        placeholder={mode === 'assets' ? 'Amount' : 'Shares'}
      />
    </div>
  );
}
```

### 2. Flash Loan Lock Warning

```typescript
// When building flash loan transactions, warn user:

function FlashLoanTab() {
  return (
    <Alert variant="warning">
      <AlertTitle>Flash Loan Active</AlertTitle>
      <AlertDescription>
        During a flash loan, the market is LOCKED (flash_loan_lock = 1).
        No other operations can occur until the loan is repaid and lock released.
        
        Single-instruction mode: Repayment is automatic via vault reload.
        Two-step mode: You MUST call flash_loan_end() to unlock.
      </AlertDescription>
    </Alert>
  );
}
```

### 3. Authorization Validation

```typescript
// Before allowing delegated operations, check authorization:

async function checkAuthorization(
  program: Program,
  caller: PublicKey,
  owner: PublicKey
): Promise<boolean> {
  if (caller.equals(owner)) return true;
  
  const [authPDA] = getAuthorizationPDA(owner, caller);
  
  try {
    const auth = await program.account.authorization.fetch(authPDA);
    const now = Math.floor(Date.now() / 1000);
    
    return (
      auth.isAuthorized &&
      !auth.isRevoked &&
      auth.expiresAt > now
    );
  } catch {
    return false;
  }
}

// Usage in withdraw:
function WithdrawTab({ positionOwner }) {
  const { publicKey } = useWallet();
  const canWithdraw = await checkAuthorization(program, publicKey, positionOwner);
  
  if (!canWithdraw) {
    return <div>You don't have permission to withdraw from this position</div>;
  }
  
  // Render withdraw UI...
}
```

### 4. Admin Access Control

**CRITICAL: Admin routes must verify wallet = protocol owner**

```typescript
// lib/hooks/useProtocolOwner.ts
import { useQuery } from '@tanstack/react-query';
import { useConnection } from '@solana/wallet-adapter-react';
import { PublicKey } from '@solana/web3.js';

export function useProtocolOwner() {
  const { connection } = useConnection();
  
  return useQuery({
    queryKey: ['protocol-owner'],
    queryFn: async () => {
      const program = getMorphoProgram(connection);
      const [protocolState] = getProtocolStatePDA();
      const state = await program.account.protocolState.fetch(protocolState);
      return state.owner as PublicKey;
    },
    staleTime: 60_000, // Cache for 1 minute
  });
}

// lib/hooks/useIsAdmin.ts
import { useMemo } from 'react';
import { useWallet } from '@solana/wallet-adapter-react';
import { useProtocolOwner } from './useProtocolOwner';

export function useIsAdmin(): boolean | undefined {
  const { publicKey } = useWallet();
  const { data: owner, isLoading } = useProtocolOwner();
  
  return useMemo(() => {
    if (isLoading) return undefined; // Loading state
    if (!publicKey || !owner) return false;
    return publicKey.equals(owner);
  }, [publicKey, owner, isLoading]);
}

// app/(admin)/admin/layout.tsx - Admin Route Wrapper
'use client';

import { useWallet } from '@solana/wallet-adapter-react';
import { useIsAdmin } from '@/lib/hooks/useIsAdmin';
import { useProtocolOwner } from '@/lib/hooks/useProtocolOwner';
import { useRouter } from 'next/navigation';
import { useEffect } from 'react';
import { AlertTriangle, Lock } from 'lucide-react';

export default function AdminLayout({ children }: { children: React.ReactNode }) {
  const { publicKey } = useWallet();
  const isAdmin = useIsAdmin();
  const { data: owner } = useProtocolOwner();
  const router = useRouter();
  
  useEffect(() => {
    if (publicKey && isAdmin === false) {
      // Not admin, redirect to home
      router.push('/');
    }
  }, [publicKey, isAdmin, router]);
  
  // No wallet connected
  if (!publicKey) {
    return (
      <div className="flex items-center justify-center min-h-screen bg-gray-50">
        <div className="text-center max-w-md">
          <Lock className="w-16 h-16 mx-auto mb-4 text-gray-400" />
          <h2 className="text-2xl font-bold mb-2">Admin Access Required</h2>
          <p className="text-gray-600 mb-4">
            Please connect your wallet to access the admin panel.
          </p>
        </div>
      </div>
    );
  }
  
  // Loading owner check
  if (isAdmin === undefined) {
    return (
      <div className="flex items-center justify-center min-h-screen bg-gray-50">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600 mx-auto mb-4" />
          <p className="text-gray-600">Verifying admin access...</p>
        </div>
      </div>
    );
  }
  
  // Not an admin
  if (!isAdmin) {
    return (
      <div className="flex items-center justify-center min-h-screen bg-gray-50">
        <div className="text-center max-w-md">
          <AlertTriangle className="w-16 h-16 mx-auto mb-4 text-red-500" />
          <h2 className="text-2xl font-bold mb-2 text-red-600">Access Denied</h2>
          <p className="text-gray-600 mb-4">
            Only the protocol owner can access the admin panel.
          </p>
          <div className="bg-gray-100 rounded-lg p-4 mb-4">
            <p className="text-xs text-gray-500 mb-1">Protocol Owner:</p>
            <p className="text-sm font-mono break-all">{owner?.toString()}</p>
          </div>
          <p className="text-xs text-gray-500">
            Your wallet: {publicKey.toString()}
          </p>
        </div>
      </div>
    );
  }
  
  // Admin verified - render admin pages
  return (
    <div className="min-h-screen bg-gray-50">
      {children}
    </div>
  );
}

// components/layout/Header.tsx - Conditional Admin Button
import { Shield } from 'lucide-react';
import { useIsAdmin } from '@/lib/hooks/useIsAdmin';
import Link from 'next/link';

export function Header() {
  const isAdmin = useIsAdmin();
  
  return (
    <header className="bg-white border-b">
      <nav className="container mx-auto px-4 py-4">
        <div className="flex items-center gap-4">
          <Link href="/">Home</Link>
          <Link href="/markets">Markets</Link>
          <Link href="/dashboard">Dashboard</Link>
          <Link href="/liquidations">Liquidations</Link>
          
          {/* Only show admin link if user is owner */}
          {isAdmin && (
            <Link 
              href="/admin" 
              className="flex items-center gap-2 text-blue-600 font-semibold"
            >
              <Shield className="w-4 h-4" />
              Admin
            </Link>
          )}
        </div>
      </nav>
    </header>
  );
}

// app/(admin)/admin/page.tsx - Admin Dashboard
'use client';

import { useProtocolOwner } from '@/lib/hooks/useProtocolOwner';
import { useWallet } from '@solana/wallet-adapter-react';

export default function AdminDashboard() {
  const { publicKey } = useWallet();
  const { data: owner } = useProtocolOwner();
  
  return (
    <div className="container mx-auto px-4 py-8">
      <div className="mb-6">
        <h1 className="text-3xl font-bold mb-2">Admin Dashboard</h1>
        <p className="text-gray-600">
          Protocol owner controls • 9 admin instructions
        </p>
      </div>
      
      <div className="bg-green-50 border border-green-200 rounded-lg p-4 mb-6">
        <p className="text-sm text-green-800">
          ✓ Authenticated as protocol owner
        </p>
        <p className="text-xs text-green-600 mt-1 font-mono">
          {publicKey?.toString()}
        </p>
      </div>
      
      {/* Admin panels here */}
    </div>
  );
}
```

**Security Checklist:**
- [x] Admin layout wraps all admin routes
- [x] Owner check happens on every admin page load  
- [x] Admin button only visible to owner
- [x] Failed auth redirects to home
- [x] Loading state while checking ownership
- [x] Clear error message for unauthorized users
- [x] All admin instructions verify signer = owner on-chain

**Folder Structure:**
```
app/
├── (user)/                   # Public routes
│   ├── markets/
│   ├── dashboard/
│   └── liquidations/
└── (admin)/                  # Protected routes
    └── admin/
        ├── layout.tsx        # Auth wrapper (checks owner)
        ├── page.tsx
        ├── protocol/
        ├── markets/
        └── whitelist/
```

### 5. Fee Claiming

```typescript
// Fee recipient must have a Position account to receive fee shares:

async function claimFees(
  program: Program,
  marketId: Buffer,
  feeRecipient: PublicKey
) {
  // Ensure fee recipient has position
  const createPosIx = await ensurePositionExists(
    program,
    marketId,
    feeRecipient
  );
  
  const claimIx = program.methods
    .claimFees(Array.from(marketId))
    .accounts({
      protocolState,
      market,
      feePosition: getPositionPDA(marketId, feeRecipient)[0],
    })
    .instruction();
  
  const tx = new Transaction();
  if (createPosIx) tx.add(createPosIx);
  tx.add(claimIx);
  
  return tx;
}
```

## Testing Strategy

### Unit Tests (lib/math)
```typescript
// Test share calculations match contract
describe('shares.ts', () => {
  it('should calculate shares correctly', () => {
    const assets = new BN(1000);
    const totalAssets = new BN(10000);
    const totalShares = new BN(10000);
    
    const shares = toSharesDown(assets, totalAssets, totalShares);
    expect(shares.toString()).toBe('999'); // Due to rounding
  });
});
```

### Integration Tests (instruction builders)
```typescript
// Test instruction building on devnet
describe('buildSupplyInstruction', () => {
  it('should build valid supply instruction', async () => {
    const ix = await buildSupplyInstruction(
      program,
      marketId,
      supplier,
      onBehalfOf,
      assets,
      minShares
    );
    
    expect(ix.programId).toEqual(MORPHO_PROGRAM_ID);
    expect(ix.keys).toHaveLength(9); // Check account count
  });
});
```

### E2E Tests (Playwright)
```typescript
// Test full user flows
test('user can supply and withdraw', async ({ page }) => {
  await page.goto('/markets');
  await page.click('text=SOL/USDC');
  await page.click('text=Supply');
  await page.fill('input[placeholder="0.00"]', '100');
  await page.click('button:has-text("Supply")');
  
  // Wait for wallet approval
  await page.waitForSelector('text=Supply successful');
  
  // Verify position
  await page.goto('/dashboard');
  expect(await page.textContent('.supply-amount')).toContain('100');
});
```

## Performance Optimization

### 1. Batch RPC Calls
```typescript
// Fetch multiple accounts in single RPC call
async function fetchMultiplePositions(
  connection: Connection,
  positionPubkeys: PublicKey[]
): Promise<Position[]> {
  const accounts = await connection.getMultipleAccountsInfo(positionPubkeys);
  
  return accounts.map((account, i) => {
    if (!account) return null;
    return program.coder.accounts.decode('position', account.data);
  }).filter(Boolean);
}
```

### 2. Cache Market Data
```typescript
// Use React Query with longer stale times for static data
const { data: markets } = useQuery(['markets'], fetchMarkets, {
  staleTime: 30_000, // 30 seconds
  cacheTime: 5 * 60_000, // 5 minutes
});
```

### 3. Virtualized Lists
```typescript
// Use react-window for large lists
import { FixedSizeList } from 'react-window';

function MarketsList({ markets }) {
  return (
    <FixedSizeList
      height={600}
      itemCount={markets.length}
      itemSize={100}
    >
      {({ index, style }) => (
        <div style={style}>
          <MarketCard market={markets[index]} />
        </div>
      )}
    </FixedSizeList>
  );
}
```

## Deployment Checklist

- [ ] Update program ID in constants
- [ ] Configure RPC endpoints (mainnet, devnet)
- [ ] Add token metadata (logos, names)
- [ ] Set up monitoring (Sentry, Analytics)
- [ ] Configure CORS for RPC calls
- [ ] Add rate limiting for RPC requests
- [ ] Test on mainnet-beta with real tokens
- [ ] Security audit of client-side math
- [ ] Load testing with high traffic
- [ ] Mobile responsiveness testing
- [ ] Wallet adapter testing (all wallets)
- [ ] Browser compatibility (Chrome, Firefox, Safari)

## Common Pitfalls

1. **Forgetting Position Creation**: Always check if position exists before supply/borrow/collateral operations
2. **Wrong Rounding Direction**: Client calculations must match contract (DOWN for supply/withdraw, UP for borrow/repay)
3. **u128 Overflow**: Use BN for all calculations, never JavaScript numbers for token amounts
4. **Authorization Expiry**: Check timestamp before allowing delegated operations
5. **Flash Loan Lock**: Warn users about market lock during flash loans
6. **Assets vs Shares**: UI must clearly indicate which unit is being used
7. **Slippage**: Always include min_shares/max_shares for price protection
8. **Health Factor**: Real-time oracle price fetch for accurate HF display
9. **Revoked Auth**: Cannot re-enable authorization after revoke (is_revoked = true)
10. **Fee Claiming**: Fee recipient needs Position account to receive shares

## Reference Links

- **Morpho Blue Docs**: https://docs.morpho.org
- **Kamino Finance**: https://kamino.finance (UI reference)
- **Jupiter Wallet Adapter**: https://github.com/solana-labs/wallet-adapter
- **Anchor Docs**: https://www.anchor-lang.com
- **Solana Cookbook**: https://solanacookbook.com

## Need Help?

Use the `morpho-solana-builder` skill for contract-level questions and the Solana MCP tools for Anchor/Solana specific issues:
- `Ask_Solana_Anchor_Framework_Expert` - Anchor syntax and patterns
- `Solana_Documentation_Search` - Solana concepts
- `Solana_Expert__Ask_For_Help` - General Solana development

This skill provides complete coverage of all 26 Morpho instructions with production-ready patterns, math libraries, and UI components. Follow the implementation guide step-by-step for a robust lending protocol frontend.
