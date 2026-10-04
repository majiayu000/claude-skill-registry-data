---
name: Slipstream Fee Mechanics
description: This skill should be used when the user asks about "fees", "fee tier", "swap fee", "unstaked fee", "staked fee", "fee growth", "gaugeFees", "split fees", or needs to understand how fees work in Slipstream.
version: 0.1.0
---

# Slipstream Fee Mechanics

Slipstream has a sophisticated fee system that splits fees between staked and unstaked liquidity positions, with configurable fee tiers.

## Overview

```
┌──────────────────────────────────────────────────────────────┐
│                    FEE DISTRIBUTION                          │
├──────────────────────────────────────────────────────────────┤
│                                                              │
│  Swap Fee Collected                                          │
│       │                                                      │
│       ▼                                                      │
│  ┌─────────────────────────────────────────────────────────┐ │
│  │                   splitFees()                           │ │
│  │                                                         │ │
│  │  Total Fee = Base Fee from Swap                         │ │
│  │       │                                                 │ │
│  │       ├─► Staked Portion (by liquidity ratio)           │ │
│  │       │   └─► gaugeFees (to gauge for distribution)     │ │
│  │       │                                                 │ │
│  │       └─► Unstaked Portion                              │ │
│  │           ├─► Unstaked Fee % ─► To Staked LPs           │ │
│  │           └─► Remainder ─► feeGrowthGlobal (to LPs)     │ │
│  │                                                         │ │
│  └─────────────────────────────────────────────────────────┘ │
│                                                              │
│  Staked LPs:                                                 │
│  ├── Get proportional share of swap fees                     │
│  └── Get bonus from unstaked fee (incentive to stake)        │
│                                                              │
│  Unstaked LPs:                                               │
│  ├── Get proportional share minus unstaked fee               │
│  └── Can collect via position.collect()                      │
│                                                              │
└──────────────────────────────────────────────────────────────┘
```

## Fee Tiers

```solidity
// CLFactory.sol

// Tick spacing determines fee tier
mapping(int24 tickSpacing => uint24 fee) public tickSpacingToFee;

// Common configurations:
// tickSpacing: 1    → fee: 100    (0.01%) - Stable pairs
// tickSpacing: 50   → fee: 500    (0.05%) - Low volatility
// tickSpacing: 100  → fee: 500    (0.05%) - Standard
// tickSpacing: 200  → fee: 3000   (0.30%) - Medium volatility
// tickSpacing: 2000 → fee: 10000  (1.00%) - High volatility

// Fee is in hundredths of a basis point
// 100 = 0.01% = 1 bip
// 500 = 0.05% = 5 bips
// 3000 = 0.30% = 30 bips
// 10000 = 1.00% = 100 bips

// Maximum fee allowed
uint24 public constant MAX_FEE = 30000;  // 3%
```

## Pool Fee Storage

```solidity
// CLPool.sol

uint24 public fee;  // Swap fee in hundredths of bips

// Gauge fees accumulated (for staked LP distribution)
struct GaugeFees {
    uint128 token0;
    uint128 token1;
}
GaugeFees public gaugeFees;

// Fee growth accumulators (for unstaked LP distribution)
uint256 public feeGrowthGlobal0X128;  // Token0 fees per unit liquidity
uint256 public feeGrowthGlobal1X128;  // Token1 fees per unit liquidity

// Unstaked fee rate (penalty for not staking)
uint24 public unstakedFee;  // Default: 100000 = 10%
```

## Fee Splitting Logic

```solidity
// CLPool.sol

/// @notice Split fees between staked and unstaked liquidity
/// @param feeAmount Total fee collected
/// @param _liquidity Total active liquidity
/// @param _stakedLiquidity Staked portion of liquidity
/// @return unstakedFeeAmount Fees going to unstaked LPs
/// @return stakedFeeAmount Fees going to gauge (staked LPs)
function splitFees(
    uint256 feeAmount,
    uint128 _liquidity,
    uint128 _stakedLiquidity
) internal view returns (uint256 unstakedFeeAmount, uint256 stakedFeeAmount) {
    if (_stakedLiquidity == 0) {
        // No staked liquidity - all fees to unstaked
        return (feeAmount, 0);
    }

    if (_stakedLiquidity == _liquidity) {
        // All liquidity staked - all fees to gauge
        return (0, feeAmount);
    }

    // Calculate unstaked liquidity
    uint128 unstakedLiquidity = _liquidity - _stakedLiquidity;

    // Base allocation by liquidity ratio
    uint256 unstakedFeeBase = FullMath.mulDiv(feeAmount, unstakedLiquidity, _liquidity);
    uint256 stakedFeeBase = feeAmount - unstakedFeeBase;

    // Apply unstaked fee penalty
    // Portion of unstaked fees redirected to staked LPs
    uint256 unstakedFeePenalty = FullMath.mulDiv(unstakedFeeBase, unstakedFee, 1e6);

    unstakedFeeAmount = unstakedFeeBase - unstakedFeePenalty;
    stakedFeeAmount = stakedFeeBase + unstakedFeePenalty;
}
```

## Fee Growth Accounting

```solidity
// During swap, after fee calculation:

if (state.liquidity > 0) {
    (uint256 unstakedFeeAmount, uint256 stakedFeeAmount) = splitFees(
        step.feeAmount,
        state.liquidity,
        state.stakedLiquidity
    );

    // Unstaked fees: Add to fee growth (per unit unstaked liquidity)
    uint128 unstakedLiquidity = state.liquidity - state.stakedLiquidity;
    if (unstakedLiquidity > 0 && unstakedFeeAmount > 0) {
        state.feeGrowthGlobalX128 += FullMath.mulDiv(
            unstakedFeeAmount,
            FixedPoint128.Q128,  // 2^128
            unstakedLiquidity
        );
    }

    // Staked fees: Add to gauge fees
    if (stakedFeeAmount > 0) {
        if (zeroForOne) {
            gaugeFees.token0 += uint128(stakedFeeAmount);
        } else {
            gaugeFees.token1 += uint128(stakedFeeAmount);
        }
    }
}
```

## Position Fee Calculation

```solidity
// Position.sol

/// @notice Calculate fees owed to a position
function feesOwed(
    Position.Info memory self,
    uint256 feeGrowthInside0X128,
    uint256 feeGrowthInside1X128
) internal pure returns (uint128 tokensOwed0, uint128 tokensOwed1) {
    // Fees = liquidity * (currentFeeGrowth - lastFeeGrowth) / 2^128
    tokensOwed0 = uint128(
        FullMath.mulDiv(
            feeGrowthInside0X128 - self.feeGrowthInside0LastX128,
            self.liquidity,
            FixedPoint128.Q128
        )
    );

    tokensOwed1 = uint128(
        FullMath.mulDiv(
            feeGrowthInside1X128 - self.feeGrowthInside1LastX128,
            self.liquidity,
            FixedPoint128.Q128
        )
    );
}
```

## Fee Growth Inside Range

```solidity
/// @notice Get fee growth inside a tick range
function getFeeGrowthInside(
    int24 tickLower,
    int24 tickUpper
) internal view returns (uint256 feeGrowthInside0X128, uint256 feeGrowthInside1X128) {
    Tick.Info storage lower = ticks[tickLower];
    Tick.Info storage upper = ticks[tickUpper];

    int24 tickCurrent = slot0.tick;

    // Below lower tick
    uint256 feeGrowthBelow0X128;
    uint256 feeGrowthBelow1X128;
    if (tickCurrent >= tickLower) {
        feeGrowthBelow0X128 = lower.feeGrowthOutside0X128;
        feeGrowthBelow1X128 = lower.feeGrowthOutside1X128;
    } else {
        feeGrowthBelow0X128 = feeGrowthGlobal0X128 - lower.feeGrowthOutside0X128;
        feeGrowthBelow1X128 = feeGrowthGlobal1X128 - lower.feeGrowthOutside1X128;
    }

    // Above upper tick
    uint256 feeGrowthAbove0X128;
    uint256 feeGrowthAbove1X128;
    if (tickCurrent < tickUpper) {
        feeGrowthAbove0X128 = upper.feeGrowthOutside0X128;
        feeGrowthAbove1X128 = upper.feeGrowthOutside1X128;
    } else {
        feeGrowthAbove0X128 = feeGrowthGlobal0X128 - upper.feeGrowthOutside0X128;
        feeGrowthAbove1X128 = feeGrowthGlobal1X128 - upper.feeGrowthOutside1X128;
    }

    // Inside = global - below - above
    feeGrowthInside0X128 = feeGrowthGlobal0X128 - feeGrowthBelow0X128 - feeGrowthAbove0X128;
    feeGrowthInside1X128 = feeGrowthGlobal1X128 - feeGrowthBelow1X128 - feeGrowthAbove1X128;
}
```

## Custom Fee Modules

```solidity
// CLFactory.sol

/// @notice Set custom swap fee for a pool
/// @param pool Pool address
/// @param fee New fee (0 to disable custom, otherwise <= MAX_FEE)
function setPoolFee(address pool, uint24 _fee) external {
    require(msg.sender == swapFeeManager, "NM");
    require(_fee <= MAX_FEE, "FTL");

    ICLPool(pool).setFee(_fee);
    emit SetPoolFee(pool, _fee);
}

/// @notice Set custom unstaked fee for a pool
function setUnstakedFee(address pool, uint24 _fee) external {
    require(msg.sender == unstakedFeeManager, "NM");
    require(_fee <= 500000, "UFM");  // Max 50%

    ICLPool(pool).setUnstakedFee(_fee);
    emit SetUnstakedFee(pool, _fee);
}
```

## Gauge Fee Collection

```solidity
// CLGauge.sol

/// @notice Collect gauge fees from pool
function claimFees() external returns (uint256 claimed0, uint256 claimed1) {
    return _claimFees();
}

function _claimFees() internal returns (uint256 claimed0, uint256 claimed1) {
    // Get accumulated fees
    (uint128 token0, uint128 token1) = pool.gaugeFees();

    if (token0 > 0 || token1 > 0) {
        // Collect from pool
        (claimed0, claimed1) = pool.collectFees(address(this), type(uint128).max, type(uint128).max);

        // Distribute to fee recipient
        if (claimed0 > 0) {
            IERC20(pool.token0()).safeTransfer(feeRecipient, claimed0);
        }
        if (claimed1 > 0) {
            IERC20(pool.token1()).safeTransfer(feeRecipient, claimed1);
        }

        emit ClaimFees(msg.sender, claimed0, claimed1);
    }
}
```

## Pool Fee Collection

```solidity
// CLPool.sol

/// @notice Collect accumulated gauge fees
/// @dev Only callable by gauge
function collectFees(
    address recipient,
    uint128 amount0Requested,
    uint128 amount1Requested
) external returns (uint128 amount0, uint128 amount1) {
    require(msg.sender == gauge, "NG");

    amount0 = amount0Requested > gaugeFees.token0 ? gaugeFees.token0 : amount0Requested;
    amount1 = amount1Requested > gaugeFees.token1 ? gaugeFees.token1 : amount1Requested;

    if (amount0 > 0) {
        gaugeFees.token0 -= amount0;
        TransferHelper.safeTransfer(token0, recipient, amount0);
    }
    if (amount1 > 0) {
        gaugeFees.token1 -= amount1;
        TransferHelper.safeTransfer(token1, recipient, amount1);
    }

    emit CollectFees(recipient, amount0, amount1);
}
```

## Fee Example

```solidity
// Example: $1000 swap in 0.3% fee pool

// Swap amount: $1000
// Fee rate: 3000 (0.30%)
// Fee collected: $1000 * 0.003 = $3.00

// Pool state:
// liquidity: 1000 units
// stakedLiquidity: 600 units (60%)
// unstakedFee: 100000 (10%)

// Fee split:
// Staked base: $3.00 * 60% = $1.80
// Unstaked base: $3.00 * 40% = $1.20

// Unstaked penalty: $1.20 * 10% = $0.12
// Final unstaked fees: $1.20 - $0.12 = $1.08
// Final staked fees: $1.80 + $0.12 = $1.92

// Result:
// Staked LPs (via gauge): $1.92 (64% of total)
// Unstaked LPs (via feeGrowth): $1.08 (36% of total)
```

## Events

```solidity
event CollectFees(address indexed recipient, uint128 amount0, uint128 amount1);
event SetFee(uint24 fee);
event SetUnstakedFee(uint24 unstakedFee);
```

## Reference Files

- `contracts/core/CLPool.sol` - Fee logic in swap
- `contracts/core/CLFactory.sol` - Fee tier configuration
- `contracts/core/libraries/Position.sol` - Position fee calculation
- `contracts/gauge/CLGauge.sol` - Gauge fee collection
