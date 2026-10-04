---
name: Slipstream Swapping
description: This skill should be used when the user asks about "swap", "trade", "zeroForOne", "sqrtPriceLimitX96", "price impact", "tick crossing", "swap step", or needs to understand how swaps work in concentrated liquidity pools.
version: 0.1.0
---

# Slipstream Swapping

Swaps in Slipstream traverse through ticks, consuming liquidity in each price range. This skill covers the swap mechanics.

## Overview

```
┌──────────────────────────────────────────────────────────────┐
│                     SWAP EXECUTION                           │
├──────────────────────────────────────────────────────────────┤
│                                                              │
│  Price Movement During Swap                                  │
│  ┌─────────────────────────────────────────────────────────┐ │
│  │                                                         │ │
│  │  tickA        tickB        tickC        tickD           │ │
│  │    ▼           ▼           ▼           ▼               │ │
│  │  ──┬───────────┬───────────┬───────────┬──             │ │
│  │    │  Liq: 50  │  Liq: 80  │  Liq: 30  │               │ │
│  │    │           │           │           │               │ │
│  │  [START]──────────────────────────►[END]                │ │
│  │    Price moves through ticks as swap executes           │ │
│  │                                                         │ │
│  └─────────────────────────────────────────────────────────┘ │
│                                                              │
│  Swap Steps:                                                 │
│  1. Start at current tick/price                              │
│  2. Compute max amount to next initialized tick              │
│  3. Execute partial swap, collect fees                       │
│  4. If tick crossed: update liquidity, repeat                │
│  5. Continue until amount exhausted or price limit hit       │
│                                                              │
└──────────────────────────────────────────────────────────────┘
```

## Swap Function

```solidity
// CLPool.sol

/// @notice Execute a swap
/// @param recipient Address to receive output tokens
/// @param zeroForOne Direction: true = token0→token1, false = token1→token0
/// @param amountSpecified Amount (positive = exact input, negative = exact output)
/// @param sqrtPriceLimitX96 Price limit to stop swap
/// @param data Callback data
/// @return amount0 Token0 delta (negative = sent, positive = received)
/// @return amount1 Token1 delta (negative = sent, positive = received)
function swap(
    address recipient,
    bool zeroForOne,
    int256 amountSpecified,
    uint160 sqrtPriceLimitX96,
    bytes calldata data
) external lock returns (int256 amount0, int256 amount1) {
    require(amountSpecified != 0, "AS");

    Slot0 memory slot0Start = slot0;
    require(slot0Start.unlocked, "LOK");

    // Validate price limit
    require(
        zeroForOne
            ? sqrtPriceLimitX96 < slot0Start.sqrtPriceX96 && sqrtPriceLimitX96 > MIN_SQRT_RATIO
            : sqrtPriceLimitX96 > slot0Start.sqrtPriceX96 && sqrtPriceLimitX96 < MAX_SQRT_RATIO,
        "SPL"
    );

    slot0.unlocked = false;

    // Initialize swap state
    SwapCache memory cache = SwapCache({
        liquidityStart: liquidity,
        blockTimestamp: _blockTimestamp(),
        feeProtocol: zeroForOne ? slot0Start.feeProtocol % 16 : slot0Start.feeProtocol >> 4,
        secondsPerLiquidityCumulativeX128: 0,
        tickCumulative: 0,
        computedLatestObservation: false
    });

    bool exactInput = amountSpecified > 0;

    SwapState memory state = SwapState({
        amountSpecifiedRemaining: amountSpecified,
        amountCalculated: 0,
        sqrtPriceX96: slot0Start.sqrtPriceX96,
        tick: slot0Start.tick,
        feeGrowthGlobalX128: zeroForOne ? feeGrowthGlobal0X128 : feeGrowthGlobal1X128,
        liquidity: cache.liquidityStart,
        stakedLiquidity: stakedLiquidity
    });

    // Execute swap loop
    while (state.amountSpecifiedRemaining != 0 && state.sqrtPriceX96 != sqrtPriceLimitX96) {
        StepComputations memory step;

        step.sqrtPriceStartX96 = state.sqrtPriceX96;

        // Find next initialized tick
        (step.tickNext, step.initialized) = tickBitmap.nextInitializedTickWithinOneWord(
            state.tick,
            tickSpacing,
            zeroForOne
        );

        // Clamp to valid tick range
        if (step.tickNext < MIN_TICK) step.tickNext = MIN_TICK;
        else if (step.tickNext > MAX_TICK) step.tickNext = MAX_TICK;

        step.sqrtPriceNextX96 = TickMath.getSqrtRatioAtTick(step.tickNext);

        // Compute swap step
        (state.sqrtPriceX96, step.amountIn, step.amountOut, step.feeAmount) = SwapMath
            .computeSwapStep(
                state.sqrtPriceX96,
                (zeroForOne ? step.sqrtPriceNextX96 < sqrtPriceLimitX96 : step.sqrtPriceNextX96 > sqrtPriceLimitX96)
                    ? sqrtPriceLimitX96
                    : step.sqrtPriceNextX96,
                state.liquidity,
                state.amountSpecifiedRemaining,
                fee
            );

        // Update amounts
        if (exactInput) {
            state.amountSpecifiedRemaining -= (step.amountIn + step.feeAmount).toInt256();
            state.amountCalculated = state.amountCalculated.sub(step.amountOut.toInt256());
        } else {
            state.amountSpecifiedRemaining += step.amountOut.toInt256();
            state.amountCalculated = state.amountCalculated.add((step.amountIn + step.feeAmount).toInt256());
        }

        // Update fee growth
        if (state.liquidity > 0) {
            // Split fees between staked and unstaked
            (uint256 unstakedFeeAmount, uint256 stakedFeeAmount) = splitFees(
                step.feeAmount,
                state.liquidity,
                state.stakedLiquidity
            );

            // Unstaked fees go to fee growth
            state.feeGrowthGlobalX128 += FullMath.mulDiv(
                unstakedFeeAmount,
                FixedPoint128.Q128,
                state.liquidity - state.stakedLiquidity
            );

            // Staked fees go to gauge
            if (stakedFeeAmount > 0) {
                gaugeFees.token0 += zeroForOne ? uint128(stakedFeeAmount) : 0;
                gaugeFees.token1 += zeroForOne ? 0 : uint128(stakedFeeAmount);
            }
        }

        // Cross tick if reached
        if (state.sqrtPriceX96 == step.sqrtPriceNextX96) {
            if (step.initialized) {
                // Update oracle if needed
                if (!cache.computedLatestObservation) {
                    (cache.tickCumulative, cache.secondsPerLiquidityCumulativeX128) =
                        observations.observeSingle(...);
                    cache.computedLatestObservation = true;
                }

                // Cross tick - update liquidity
                int128 liquidityNet = ticks.cross(
                    step.tickNext,
                    zeroForOne ? state.feeGrowthGlobalX128 : feeGrowthGlobal0X128,
                    zeroForOne ? feeGrowthGlobal1X128 : state.feeGrowthGlobalX128,
                    ...
                );

                // Update liquidity
                if (zeroForOne) liquidityNet = -liquidityNet;
                state.liquidity = LiquidityMath.addDelta(state.liquidity, liquidityNet);

                // Update staked liquidity similarly
                int128 stakedLiquidityNet = ...;
                state.stakedLiquidity = LiquidityMath.addDelta(state.stakedLiquidity, stakedLiquidityNet);
            }

            state.tick = zeroForOne ? step.tickNext - 1 : step.tickNext;
        } else if (state.sqrtPriceX96 != step.sqrtPriceStartX96) {
            state.tick = TickMath.getTickAtSqrtRatio(state.sqrtPriceX96);
        }
    }

    // Write oracle observation if tick changed
    if (state.tick != slot0Start.tick) {
        (slot0.sqrtPriceX96, slot0.tick, slot0.observationIndex, slot0.observationCardinality) =
            (
                state.sqrtPriceX96,
                state.tick,
                observations.write(...),
                cache.observationCardinalityNext
            );
    } else {
        slot0.sqrtPriceX96 = state.sqrtPriceX96;
    }

    // Update global state
    if (cache.liquidityStart != state.liquidity) liquidity = state.liquidity;
    if (zeroForOne) feeGrowthGlobal0X128 = state.feeGrowthGlobalX128;
    else feeGrowthGlobal1X128 = state.feeGrowthGlobalX128;

    // Calculate final amounts
    (amount0, amount1) = zeroForOne == exactInput
        ? (amountSpecified - state.amountSpecifiedRemaining, state.amountCalculated)
        : (state.amountCalculated, amountSpecified - state.amountSpecifiedRemaining);

    // Transfer tokens
    if (zeroForOne) {
        if (amount1 < 0) TransferHelper.safeTransfer(token1, recipient, uint256(-amount1));

        uint256 balance0Before = balance0();
        ISwapCallback(msg.sender).uniswapV3SwapCallback(amount0, amount1, data);
        require(balance0Before.add(uint256(amount0)) <= balance0(), "IIA");
    } else {
        if (amount0 < 0) TransferHelper.safeTransfer(token0, recipient, uint256(-amount0));

        uint256 balance1Before = balance1();
        ISwapCallback(msg.sender).uniswapV3SwapCallback(amount0, amount1, data);
        require(balance1Before.add(uint256(amount1)) <= balance1(), "IIA");
    }

    slot0.unlocked = true;

    emit Swap(msg.sender, recipient, amount0, amount1, state.sqrtPriceX96, state.liquidity, state.tick);
}
```

## Swap State

```solidity
struct SwapState {
    int256 amountSpecifiedRemaining;  // Amount left to swap
    int256 amountCalculated;          // Output amount accumulated
    uint160 sqrtPriceX96;             // Current sqrt price
    int24 tick;                       // Current tick
    uint256 feeGrowthGlobalX128;      // Fee growth accumulator
    uint128 liquidity;                // Current liquidity
    uint128 stakedLiquidity;          // Current staked liquidity
}

struct StepComputations {
    uint160 sqrtPriceStartX96;  // Price at step start
    int24 tickNext;             // Next initialized tick
    bool initialized;           // Is tickNext initialized
    uint160 sqrtPriceNextX96;   // Price at tickNext
    uint256 amountIn;           // Input amount in this step
    uint256 amountOut;          // Output amount in this step
    uint256 feeAmount;          // Fee collected in this step
}
```

## Swap Math

```solidity
// SwapMath.sol

/// @notice Compute amounts for a single swap step
function computeSwapStep(
    uint160 sqrtRatioCurrentX96,
    uint160 sqrtRatioTargetX96,
    uint128 liquidity,
    int256 amountRemaining,
    uint24 feePips
) internal pure returns (
    uint160 sqrtRatioNextX96,
    uint256 amountIn,
    uint256 amountOut,
    uint256 feeAmount
) {
    bool zeroForOne = sqrtRatioCurrentX96 >= sqrtRatioTargetX96;
    bool exactIn = amountRemaining >= 0;

    if (exactIn) {
        // Calculate max input after fee
        uint256 amountRemainingLessFee = FullMath.mulDiv(
            uint256(amountRemaining),
            1e6 - feePips,
            1e6
        );

        // Calculate input amount to reach target price
        amountIn = zeroForOne
            ? SqrtPriceMath.getAmount0Delta(sqrtRatioTargetX96, sqrtRatioCurrentX96, liquidity, true)
            : SqrtPriceMath.getAmount1Delta(sqrtRatioCurrentX96, sqrtRatioTargetX96, liquidity, true);

        if (amountRemainingLessFee >= amountIn) {
            // Can reach target price
            sqrtRatioNextX96 = sqrtRatioTargetX96;
        } else {
            // Partial fill
            sqrtRatioNextX96 = SqrtPriceMath.getNextSqrtPriceFromInput(
                sqrtRatioCurrentX96,
                liquidity,
                amountRemainingLessFee,
                zeroForOne
            );
        }
    } else {
        // Exact output
        amountOut = zeroForOne
            ? SqrtPriceMath.getAmount1Delta(sqrtRatioTargetX96, sqrtRatioCurrentX96, liquidity, false)
            : SqrtPriceMath.getAmount0Delta(sqrtRatioCurrentX96, sqrtRatioTargetX96, liquidity, false);

        if (uint256(-amountRemaining) >= amountOut) {
            sqrtRatioNextX96 = sqrtRatioTargetX96;
        } else {
            sqrtRatioNextX96 = SqrtPriceMath.getNextSqrtPriceFromOutput(
                sqrtRatioCurrentX96,
                liquidity,
                uint256(-amountRemaining),
                zeroForOne
            );
        }
    }

    // Calculate final amounts
    bool max = sqrtRatioTargetX96 == sqrtRatioNextX96;

    if (zeroForOne) {
        amountIn = max && exactIn
            ? amountIn
            : SqrtPriceMath.getAmount0Delta(sqrtRatioNextX96, sqrtRatioCurrentX96, liquidity, true);
        amountOut = max && !exactIn
            ? amountOut
            : SqrtPriceMath.getAmount1Delta(sqrtRatioNextX96, sqrtRatioCurrentX96, liquidity, false);
    } else {
        amountIn = max && exactIn
            ? amountIn
            : SqrtPriceMath.getAmount1Delta(sqrtRatioCurrentX96, sqrtRatioNextX96, liquidity, true);
        amountOut = max && !exactIn
            ? amountOut
            : SqrtPriceMath.getAmount0Delta(sqrtRatioCurrentX96, sqrtRatioNextX96, liquidity, false);
    }

    // Cap output at exact output amount
    if (!exactIn && amountOut > uint256(-amountRemaining)) {
        amountOut = uint256(-amountRemaining);
    }

    // Calculate fee
    if (exactIn && sqrtRatioNextX96 != sqrtRatioTargetX96) {
        feeAmount = uint256(amountRemaining) - amountIn;
    } else {
        feeAmount = FullMath.mulDivRoundingUp(amountIn, feePips, 1e6 - feePips);
    }
}
```

## Tick Crossing

```solidity
// Tick.sol

/// @notice Cross a tick, updating state
function cross(
    mapping(int24 => Tick.Info) storage self,
    int24 tick,
    uint256 feeGrowthGlobal0X128,
    uint256 feeGrowthGlobal1X128,
    uint256 rewardGrowthGlobalX128,
    uint160 secondsPerLiquidityCumulativeX128,
    int56 tickCumulative,
    uint32 time
) internal returns (int128 liquidityNet, int128 stakedLiquidityNet) {
    Tick.Info storage info = self[tick];

    // Flip "outside" values
    // "Outside" means the side of the tick where current price is NOT
    info.feeGrowthOutside0X128 = feeGrowthGlobal0X128 - info.feeGrowthOutside0X128;
    info.feeGrowthOutside1X128 = feeGrowthGlobal1X128 - info.feeGrowthOutside1X128;
    info.rewardGrowthOutsideX128 = rewardGrowthGlobalX128 - info.rewardGrowthOutsideX128;

    info.secondsPerLiquidityOutsideX128 =
        secondsPerLiquidityCumulativeX128 - info.secondsPerLiquidityOutsideX128;
    info.tickCumulativeOutside = tickCumulative - info.tickCumulativeOutside;
    info.secondsOutside = time - info.secondsOutside;

    liquidityNet = info.liquidityNet;
    stakedLiquidityNet = info.stakedLiquidityNet;
}
```

## Swap Direction

```solidity
// zeroForOne = true:  Selling token0 for token1 (price decreases)
// zeroForOne = false: Selling token1 for token0 (price increases)

// Example: ETH/USDC pool (token0=USDC, token1=ETH)
// Buying ETH with USDC: zeroForOne = true
// Selling ETH for USDC: zeroForOne = false

// Amount specification:
// amountSpecified > 0: Exact input (selling exactly this much)
// amountSpecified < 0: Exact output (buying exactly this much)
```

## Events

```solidity
event Swap(
    address indexed sender,
    address indexed recipient,
    int256 amount0,
    int256 amount1,
    uint160 sqrtPriceX96,
    uint128 liquidity,
    int24 tick
);
```

## Reference Files

- `contracts/core/CLPool.sol` - swap() function
- `contracts/core/libraries/SwapMath.sol` - Swap step calculations
- `contracts/core/libraries/SqrtPriceMath.sol` - Amount calculations
- `contracts/core/libraries/Tick.sol` - Tick crossing
