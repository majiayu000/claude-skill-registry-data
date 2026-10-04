---
name: Balancer V3 Vault Operations
description: This skill should be used when the user asks about "Balancer V3 swap", "add liquidity Balancer", "remove liquidity Balancer", "VaultSwapParams", "AddLiquidityParams", "RemoveLiquidityParams", "settlement", "unlock callback", or needs to understand the core Vault operations.
version: 0.1.0
---

# Balancer V3 Vault Operations

This skill covers the core operations of the Balancer V3 Vault: swaps, adding liquidity, and removing liquidity.

## The Unlock Pattern

All state-changing operations must occur within an `unlock()` context:

```solidity
// Router calls unlock, passing encoded callback data
function unlock(bytes calldata data) external transient returns (bytes memory result) {
    return (msg.sender).functionCall(data);
}
```

The `transient` modifier:
1. Sets `isUnlocked = true`
2. Executes the callback
3. Verifies `nonZeroDeltaCount == 0` (all balances settled)
4. Reverts with `BalanceNotSettled()` if not settled

## Swap Operations

### VaultSwapParams

```solidity
struct VaultSwapParams {
    SwapKind kind;       // EXACT_IN or EXACT_OUT
    address pool;        // Pool to swap through
    IERC20 tokenIn;      // Token entering Vault
    IERC20 tokenOut;     // Token leaving Vault
    uint256 amountGivenRaw;  // Amount in native decimals
    uint256 limitRaw;    // Min out (EXACT_IN) or max in (EXACT_OUT)
    bytes userData;      // Optional hook data
}
```

### Swap Flow

```
┌─────────────────────────────────────────────────────────────────┐
│                         SWAP FLOW                               │
├─────────────────────────────────────────────────────────────────┤
│ 1. Load pool data (balances, rates, fees)                       │
│ 2. Call beforeSwap hook (if enabled)                            │
│ 3. Compute dynamic swap fee (if enabled)                        │
│ 4. Scale amounts to 18 decimals                                 │
│ 5. Call pool.onSwap() for amount calculation                    │
│ 6. Apply swap fees                                              │
│ 7. Update credits/debts via _takeDebt/_supplyCredit             │
│ 8. Update pool balances                                         │
│ 9. Call afterSwap hook (if enabled)                             │
│ 10. Emit Swap event                                             │
└─────────────────────────────────────────────────────────────────┘
```

### PoolSwapParams (passed to pool)

```solidity
struct PoolSwapParams {
    SwapKind kind;
    uint256 amountGivenScaled18;   // Scaled to 18 decimals
    uint256[] balancesScaled18;    // Current pool balances
    uint256 indexIn;               // Token index (not address)
    uint256 indexOut;
    address router;                // Router that initiated
    bytes userData;
}
```

### Swap Fee Handling

```solidity
// EXACT_IN: fee deducted from amountIn before pool math
totalSwapFeeAmountScaled18 = amountGivenScaled18.mulUp(swapFeePercentage);
amountGivenScaled18 -= totalSwapFeeAmountScaled18;

// EXACT_OUT: fee added to amountIn after pool math
// fee = amountCalculated * fee% / (100% - fee%)
totalSwapFeeAmountScaled18 = amountCalculatedScaled18.mulDivUp(
    swapFeePercentage,
    swapFeePercentage.complement()
);
```

## Add Liquidity

### AddLiquidityParams

```solidity
struct AddLiquidityParams {
    address pool;
    address to;              // Recipient of BPT
    uint256[] maxAmountsIn;  // Maximum tokens to deposit
    uint256 minBptAmountOut; // Minimum BPT to receive
    AddLiquidityKind kind;
    bytes userData;
}

enum AddLiquidityKind {
    PROPORTIONAL,             // Exact BPT out, proportional tokens in
    UNBALANCED,               // Exact tokens in, variable BPT out
    SINGLE_TOKEN_EXACT_OUT,   // Single token, exact BPT out
    DONATION,                 // Tokens in, no BPT out (gifts to LPs)
    CUSTOM                    // Pool-defined logic
}
```

### Add Liquidity Flow

```
┌─────────────────────────────────────────────────────────────────┐
│                     ADD LIQUIDITY FLOW                          │
├─────────────────────────────────────────────────────────────────┤
│ 1. Load pool data with yield fee updates                        │
│ 2. Call beforeAddLiquidity hook (if enabled)                    │
│ 3. Calculate amounts based on kind:                             │
│    - PROPORTIONAL: computeProportionalAmountsIn()               │
│    - UNBALANCED: computeAddLiquidityUnbalanced()                │
│    - SINGLE_TOKEN: computeAddLiquiditySingleTokenExactOut()     │
│ 4. Take debt for each token via _takeDebt()                     │
│ 5. Compute and charge aggregate fees                            │
│ 6. Update pool balances                                         │
│ 7. Mint BPT to recipient                                        │
│ 8. Call afterAddLiquidity hook (if enabled)                     │
│ 9. Emit LiquidityAdded event                                    │
└─────────────────────────────────────────────────────────────────┘
```

### Proportional Add

```solidity
// BasePoolMath.computeProportionalAmountsIn
// amountsIn[i] = balance[i] * bptAmountOut / totalSupply
function computeProportionalAmountsIn(
    uint256[] memory balancesLiveScaled18,
    uint256 totalSupply,
    uint256 bptAmountOut
) internal pure returns (uint256[] memory amountsInScaled18);
```

### Unbalanced Add

```solidity
// Uses invariant ratio to compute BPT out
// Charges swap fees on the "swap equivalent" portion
function computeAddLiquidityUnbalanced(
    uint256[] memory balancesLiveScaled18,
    uint256[] memory maxAmountsInScaled18,
    uint256 totalSupply,
    uint256 swapFeePercentage,
    IBasePool pool
) internal view returns (uint256 bptAmountOut, uint256[] memory swapFeeAmounts);
```

## Remove Liquidity

### RemoveLiquidityParams

```solidity
struct RemoveLiquidityParams {
    address pool;
    address from;             // BPT holder (must approve Router)
    uint256 maxBptAmountIn;   // Maximum BPT to burn
    uint256[] minAmountsOut;  // Minimum tokens to receive
    RemoveLiquidityKind kind;
    bytes userData;
}

enum RemoveLiquidityKind {
    PROPORTIONAL,             // Exact BPT in, proportional tokens out
    SINGLE_TOKEN_EXACT_IN,    // Exact BPT in, single token out
    SINGLE_TOKEN_EXACT_OUT,   // Single token exact out, variable BPT
    CUSTOM                    // Pool-defined logic
}
```

### Round-Trip Fee Protection

```solidity
// If liquidity added AND removed in same unlock session,
// proportional removal charges swap fees as protection
if (_addLiquidityCalled().tGet(sessionId, pool)) {
    for (uint256 i = 0; i < numTokens; ++i) {
        swapFeeAmounts[i] = amountsOutScaled18[i].mulUp(swapFeePercentage);
        amountsOutScaled18[i] -= swapFeeAmounts[i];
    }
}
```

## Settlement

After all operations, deltas must be settled:

```solidity
// Pay debt: transfer tokens TO Vault
function settle(IERC20 token, uint256 amountHint) external returns (uint256 credit) {
    uint256 reservesBefore = _reservesOf[token];
    uint256 currentReserves = token.balanceOf(address(this));
    _reservesOf[token] = currentReserves;

    credit = min(currentReserves - reservesBefore, amountHint);
    _supplyCredit(token, credit);
}

// Receive credit: transfer tokens FROM Vault
function sendTo(IERC20 token, address to, uint256 amount) external {
    _takeDebt(token, amount);
    _reservesOf[token] -= amount;
    token.safeTransfer(to, amount);
}
```

## Key Events

```solidity
event Swap(
    address indexed pool,
    IERC20 indexed tokenIn,
    IERC20 indexed tokenOut,
    uint256 amountIn,
    uint256 amountOut,
    uint256 swapFeePercentage,
    uint256 swapFeeAmount
);

event LiquidityAdded(
    address indexed pool,
    address indexed liquidityProvider,
    AddLiquidityKind kind,
    uint256 totalSupply,
    uint256[] amountsAddedRaw,
    uint256[] swapFeeAmountsRaw
);

event LiquidityRemoved(
    address indexed pool,
    address indexed liquidityProvider,
    RemoveLiquidityKind kind,
    uint256 totalSupply,
    uint256[] amountsRemovedRaw,
    uint256[] swapFeeAmountsRaw
);
```

## Minimum Amounts

```solidity
// Enforced to prevent rounding exploits
uint256 internal immutable _MINIMUM_TRADE_AMOUNT;  // ~1e6 scaled18
uint256 internal immutable _MINIMUM_WRAP_AMOUNT;   // Native decimals
```

## Reference Files

For complete implementation details:
- `pkg/vault/contracts/Vault.sol` - Main swap and liquidity logic
- `pkg/vault/contracts/BasePoolMath.sol` - Invariant-based calculations
- `pkg/vault/contracts/Router.sol` - User-facing operations
