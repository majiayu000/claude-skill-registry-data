---
name: Uniswap V3 Ticks
description: This skill should be used when the user asks about "ticks", "tick spacing", "TickMath", "tick bitmap", "price levels", "tick crossing", or needs to understand the tick system and price discretization.
version: 0.1.0
---

# Uniswap V3 Ticks

## Overview

Uniswap V3 discretizes prices into "ticks" where each tick represents a 0.01% (1 basis point) price increment. This enables efficient storage and gas-optimized operations for concentrated liquidity positions.

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                         TICK SYSTEM OVERVIEW                                 │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│  Price = 1.0001^tick                                                        │
│                                                                              │
│  ◄───────────────────────────────────────────────────────────────────────►  │
│  MIN_TICK                         tick = 0                      MAX_TICK    │
│  -887272                          price = 1                     887272      │
│  price ≈ 0                                                      price ≈ ∞   │
│                                                                              │
│  Tick Spacing (determines which ticks can be initialized):                  │
│  ┌──────────────────────────────────────────────────────────────────────┐   │
│  │  Fee Tier    │  Tick Spacing  │  Price Step   │  Use Case           │   │
│  ├──────────────┼────────────────┼───────────────┼─────────────────────│   │
│  │  0.01%       │       1        │    0.01%      │  Very stable pairs  │   │
│  │  0.05%       │      10        │    0.10%      │  Stable pairs       │   │
│  │  0.30%       │      60        │    0.60%      │  Standard pairs     │   │
│  │  1.00%       │     200        │    2.00%      │  Volatile pairs     │   │
│  └──────────────┴────────────────┴───────────────┴─────────────────────┘   │
│                                                                              │
└─────────────────────────────────────────────────────────────────────────────┘
```

## Tick Math

### Core Formulas

```solidity
// Price from tick
price = 1.0001^tick

// Tick from price
tick = log(price) / log(1.0001)
     = log(price) / 0.0000999950003...
     ≈ log(price) * 10000

// Sqrt price (what's actually stored)
sqrtPriceX96 = sqrt(1.0001^tick) * 2^96
             = 1.0001^(tick/2) * 2^96
```

### TickMath Library

```solidity
library TickMath {
    /// @dev The minimum tick that can be used
    int24 internal constant MIN_TICK = -887272;

    /// @dev The maximum tick that can be used
    int24 internal constant MAX_TICK = -MIN_TICK;

    /// @dev The minimum sqrt ratio (at MIN_TICK)
    uint160 internal constant MIN_SQRT_RATIO = 4295128739;

    /// @dev The maximum sqrt ratio (at MAX_TICK)
    uint160 internal constant MAX_SQRT_RATIO = 1461446703485210103287273052203988822378723970342;

    /// @notice Calculates sqrt(1.0001^tick) * 2^96
    /// @dev Uses precomputed magic numbers for gas efficiency
    function getSqrtRatioAtTick(int24 tick) internal pure returns (uint160 sqrtPriceX96) {
        uint256 absTick = tick < 0 ? uint256(-int256(tick)) : uint256(int256(tick));
        require(absTick <= uint256(int256(MAX_TICK)), 'T');

        // Start with base ratio
        uint256 ratio = absTick & 0x1 != 0
            ? 0xfffcb933bd6fad37aa2d162d1a594001
            : 0x100000000000000000000000000000000;

        // Multiply by precomputed constants for each bit set in absTick
        if (absTick & 0x2 != 0) ratio = (ratio * 0xfff97272373d413259a46990580e213a) >> 128;
        if (absTick & 0x4 != 0) ratio = (ratio * 0xfff2e50f5f656932ef12357cf3c7fdcc) >> 128;
        if (absTick & 0x8 != 0) ratio = (ratio * 0xffe5caca7e10e4e61c3624eaa0941cd0) >> 128;
        // ... continues for all 20 bits

        // Invert if tick is negative
        if (tick > 0) ratio = type(uint256).max / ratio;

        // Round up and cast to uint160
        sqrtPriceX96 = uint160((ratio >> 32) + (ratio % (1 << 32) == 0 ? 0 : 1));
    }

    /// @notice Calculates the greatest tick value such that getRatioAtTick(tick) <= ratio
    function getTickAtSqrtRatio(uint160 sqrtPriceX96) internal pure returns (int24 tick) {
        require(sqrtPriceX96 >= MIN_SQRT_RATIO && sqrtPriceX96 < MAX_SQRT_RATIO, 'R');

        uint256 ratio = uint256(sqrtPriceX96) << 32;

        // Binary search using log2
        uint256 r = ratio;
        uint256 msb = 0;

        // Find most significant bit
        assembly {
            let f := shl(7, gt(r, 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF))
            msb := or(msb, f)
            r := shr(f, r)
        }
        // ... continues for all bits

        // Refine with log base 1.0001
        int256 log_sqrt10001 = log_2 * 255738958999603826347141; // log(sqrt(1.0001))

        int24 tickLow = int24((log_sqrt10001 - 3402992956809132418596140100660247210) >> 128);
        int24 tickHi = int24((log_sqrt10001 + 291339464771989622907027621153398088495) >> 128);

        tick = tickLow == tickHi ? tickLow :
            getSqrtRatioAtTick(tickHi) <= sqrtPriceX96 ? tickHi : tickLow;
    }
}
```

## Tick Data Structure

```solidity
library Tick {
    struct Info {
        // Total liquidity that references this tick
        uint128 liquidityGross;

        // Net liquidity change when tick is crossed left→right
        // Positive when entering range, negative when exiting
        int128 liquidityNet;

        // Fee growth per unit of liquidity on the outside of this tick
        // "Outside" is relative to the current tick
        uint256 feeGrowthOutside0X128;
        uint256 feeGrowthOutside1X128;

        // Cumulative tick value on the outside (for oracle)
        int56 tickCumulativeOutside;

        // Seconds per liquidity on the outside (for oracle)
        uint160 secondsPerLiquidityOutsideX128;

        // Seconds spent on the outside (for oracle)
        uint32 secondsOutside;

        // Whether this tick is initialized
        bool initialized;
    }
}
```

## Tick Crossing

When the price crosses a tick during a swap, liquidity is added or removed from the active range.

```
Swap Direction: Token0 → Token1 (price decreasing, tick decreasing)

BEFORE CROSSING:                    AFTER CROSSING:

        ▲ tick                              ▲ tick
        │                                   │
    ┌───┼───┐  Position B                   │       Position B
    │   │   │  liquidity = 500          ┌───┼───┐   liquidity = 500
────┼───┼───┼────────────────       ────┼───┼───┼────────────────
    │   │   │                           │   │   │
    │   ├───┤  Current tick         ────┼───┤   │  Current tick moved
    │   │   │  (in Position A)          │   │   │  (now in B only)
    ├───┤   │  Position A               ├───┤   │  Position A (inactive)
    │   │   │  liquidity = 300          │   │   │
────┴───┴───┴────────────────       ────┴───┴───┴────────────────

Active Liquidity: 300 + 500 = 800   Active Liquidity: 500
                                    (Position A's liquidity removed)
```

### Cross Function

```solidity
function cross(
    mapping(int24 => Tick.Info) storage self,
    int24 tick,
    uint256 feeGrowthGlobal0X128,
    uint256 feeGrowthGlobal1X128,
    uint160 secondsPerLiquidityCumulativeX128,
    int56 tickCumulative,
    uint32 time
) internal returns (int128 liquidityNet) {
    Tick.Info storage info = self[tick];

    // Flip the "outside" values - they become "inside" relative to new position
    info.feeGrowthOutside0X128 = feeGrowthGlobal0X128 - info.feeGrowthOutside0X128;
    info.feeGrowthOutside1X128 = feeGrowthGlobal1X128 - info.feeGrowthOutside1X128;
    info.secondsPerLiquidityOutsideX128 = secondsPerLiquidityCumulativeX128 - info.secondsPerLiquidityOutsideX128;
    info.tickCumulativeOutside = tickCumulative - info.tickCumulativeOutside;
    info.secondsOutside = time - info.secondsOutside;

    liquidityNet = info.liquidityNet;
}
```

## Tick Bitmap

The tick bitmap is a gas-optimized data structure for finding initialized ticks during swaps.

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                         TICK BITMAP STRUCTURE                                │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│  tickBitmap: mapping(int16 => uint256)                                      │
│                                                                              │
│  Word Index = tick / (256 * tickSpacing)                                    │
│  Bit Index = (tick / tickSpacing) % 256                                     │
│                                                                              │
│  Example (tickSpacing = 60, tick = 120):                                    │
│    compressed = 120 / 60 = 2                                                │
│    wordPos = 2 >> 8 = 0                                                     │
│    bitPos = 2 % 256 = 2                                                     │
│                                                                              │
│  ┌────────────────────────────────────────────────────────────────────┐     │
│  │ Word 0 (bits 0-255):                                               │     │
│  │ [0][0][1][0][0][0][0][1][0]...[0][0][1][0]                         │     │
│  │      ▲                 ▲              ▲                            │     │
│  │      │                 │              │                            │     │
│  │   tick=120          tick=420       tick=3000                       │     │
│  │   (bit 2)           (bit 7)        (bit 50)                        │     │
│  └────────────────────────────────────────────────────────────────────┘     │
│                                                                              │
└─────────────────────────────────────────────────────────────────────────────┘
```

### TickBitmap Library

```solidity
library TickBitmap {
    /// @notice Computes the position in the mapping where the initialized bit lives
    function position(int24 tick) private pure returns (int16 wordPos, uint8 bitPos) {
        wordPos = int16(tick >> 8);
        bitPos = uint8(uint24(tick % 256));
    }

    /// @notice Flips the initialized state for a given tick
    function flipTick(
        mapping(int16 => uint256) storage self,
        int24 tick,
        int24 tickSpacing
    ) internal {
        require(tick % tickSpacing == 0); // Ensure valid tick
        (int16 wordPos, uint8 bitPos) = position(tick / tickSpacing);
        uint256 mask = 1 << bitPos;
        self[wordPos] ^= mask;
    }

    /// @notice Returns the next initialized tick within one word
    /// @param tick The starting tick
    /// @param lte Whether to search left (lte=true) or right (lte=false)
    function nextInitializedTickWithinOneWord(
        mapping(int16 => uint256) storage self,
        int24 tick,
        int24 tickSpacing,
        bool lte
    ) internal view returns (int24 next, bool initialized) {
        int24 compressed = tick / tickSpacing;

        if (lte) {
            (int16 wordPos, uint8 bitPos) = position(compressed);
            // Mask to get bits at or below current position
            uint256 mask = (1 << bitPos) - 1 + (1 << bitPos);
            uint256 masked = self[wordPos] & mask;

            initialized = masked != 0;
            next = initialized
                ? (compressed - int24(uint24(bitPos - BitMath.mostSignificantBit(masked)))) * tickSpacing
                : (compressed - int24(uint24(bitPos))) * tickSpacing;
        } else {
            (int16 wordPos, uint8 bitPos) = position(compressed + 1);
            // Mask to get bits above current position
            uint256 mask = ~((1 << bitPos) - 1);
            uint256 masked = self[wordPos] & mask;

            initialized = masked != 0;
            next = initialized
                ? (compressed + 1 + int24(uint24(BitMath.leastSignificantBit(masked) - bitPos))) * tickSpacing
                : (compressed + 1 + int24(uint24(type(uint8).max - bitPos))) * tickSpacing;
        }
    }
}
```

## Fee Growth Calculation

Fee growth must account for tick boundaries to calculate fees owed to each position.

```solidity
/// @notice Retrieves fee growth data inside a position's tick range
function getFeeGrowthInside(
    mapping(int24 => Tick.Info) storage self,
    int24 tickLower,
    int24 tickUpper,
    int24 tickCurrent,
    uint256 feeGrowthGlobal0X128,
    uint256 feeGrowthGlobal1X128
) internal view returns (uint256 feeGrowthInside0X128, uint256 feeGrowthInside1X128) {
    Tick.Info storage lower = self[tickLower];
    Tick.Info storage upper = self[tickUpper];

    // Calculate fee growth below tickLower
    uint256 feeGrowthBelow0X128;
    uint256 feeGrowthBelow1X128;
    if (tickCurrent >= tickLower) {
        feeGrowthBelow0X128 = lower.feeGrowthOutside0X128;
        feeGrowthBelow1X128 = lower.feeGrowthOutside1X128;
    } else {
        feeGrowthBelow0X128 = feeGrowthGlobal0X128 - lower.feeGrowthOutside0X128;
        feeGrowthBelow1X128 = feeGrowthGlobal1X128 - lower.feeGrowthOutside1X128;
    }

    // Calculate fee growth above tickUpper
    uint256 feeGrowthAbove0X128;
    uint256 feeGrowthAbove1X128;
    if (tickCurrent < tickUpper) {
        feeGrowthAbove0X128 = upper.feeGrowthOutside0X128;
        feeGrowthAbove1X128 = upper.feeGrowthOutside1X128;
    } else {
        feeGrowthAbove0X128 = feeGrowthGlobal0X128 - upper.feeGrowthOutside0X128;
        feeGrowthAbove1X128 = feeGrowthGlobal1X128 - upper.feeGrowthOutside1X128;
    }

    // Fee growth inside = global - below - above
    feeGrowthInside0X128 = feeGrowthGlobal0X128 - feeGrowthBelow0X128 - feeGrowthAbove0X128;
    feeGrowthInside1X128 = feeGrowthGlobal1X128 - feeGrowthBelow1X128 - feeGrowthAbove1X128;
}
```

## Max Liquidity Per Tick

To prevent overflow, there's a maximum amount of liquidity that can reference any single tick.

```solidity
/// @notice Derives max liquidity per tick from tick spacing
function tickSpacingToMaxLiquidityPerTick(int24 tickSpacing) internal pure returns (uint128) {
    int24 minTick = (TickMath.MIN_TICK / tickSpacing) * tickSpacing;
    int24 maxTick = (TickMath.MAX_TICK / tickSpacing) * tickSpacing;
    uint24 numTicks = uint24((maxTick - minTick) / tickSpacing) + 1;
    return type(uint128).max / numTicks;
}
```

## Tick Lens (Periphery)

For efficient off-chain querying of tick data.

```solidity
interface ITickLens {
    struct PopulatedTick {
        int24 tick;
        int128 liquidityNet;
        uint128 liquidityGross;
    }

    function getPopulatedTicksInWord(address pool, int16 tickBitmapIndex)
        external view returns (PopulatedTick[] memory populatedTicks);
}
```

## Reference Files

### v3-core
- `contracts/libraries/Tick.sol` - Tick data structure and operations
- `contracts/libraries/TickBitmap.sol` - Bitmap for initialized tick tracking
- `contracts/libraries/TickMath.sol` - Tick↔Price conversions

### v3-periphery
- `contracts/lens/TickLens.sol` - Off-chain tick enumeration
