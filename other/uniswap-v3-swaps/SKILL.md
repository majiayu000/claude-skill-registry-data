---
name: Uniswap V3 Swaps
description: This skill should be used when the user asks about "swap", "SwapRouter", "exactInput", "exactOutput", "multi-hop", "swap callback", "sqrtPriceLimit", or needs to understand swap execution and routing.
version: 0.1.0
---

# Uniswap V3 Swaps

## Overview

Uniswap V3 supports both single-pool swaps and multi-hop swaps through the SwapRouter periphery contract. The core swap logic is in the pool contract, which uses a callback pattern for token transfers.

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                           SWAP ARCHITECTURE                                  │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│  User/Contract                                                               │
│       │                                                                      │
│       │  exactInputSingle() / exactOutputSingle()                           │
│       ▼                                                                      │
│  ┌─────────────────────────────────────────────────────────────────────┐    │
│  │                         SwapRouter                                   │    │
│  │  - Wraps pool swap calls                                            │    │
│  │  - Handles multi-hop routing                                        │    │
│  │  - Manages callbacks and token transfers                            │    │
│  │  - Enforces slippage protection                                     │    │
│  └──────────────────────────────┬──────────────────────────────────────┘    │
│                                 │                                            │
│                                 │ swap(zeroForOne, amountSpecified, ...)    │
│                                 ▼                                            │
│  ┌─────────────────────────────────────────────────────────────────────┐    │
│  │                        UniswapV3Pool                                 │    │
│  │  ┌────────────────────────────────────────────────────────────┐     │    │
│  │  │ Swap Loop:                                                  │     │    │
│  │  │ 1. Compute swap within current tick                        │     │    │
│  │  │ 2. If more to swap, cross tick → update liquidity          │     │    │
│  │  │ 3. Repeat until amount exhausted or price limit            │     │    │
│  │  └────────────────────────────────────────────────────────────┘     │    │
│  │                                                                      │    │
│  │  uniswapV3SwapCallback(amount0Delta, amount1Delta, data)            │    │
│  └──────────────────────────────┬──────────────────────────────────────┘    │
│                                 │                                            │
│                                 ▼                                            │
│  ┌─────────────────────────────────────────────────────────────────────┐    │
│  │                        SwapRouter Callback                           │    │
│  │  - Decodes callback data                                            │    │
│  │  - Transfers input tokens to pool                                   │    │
│  │  - For multi-hop: initiates next swap                              │    │
│  └─────────────────────────────────────────────────────────────────────┘    │
│                                                                              │
└─────────────────────────────────────────────────────────────────────────────┘
```

## Core Pool Swap

### Swap Function

```solidity
function swap(
    address recipient,
    bool zeroForOne,            // Direction: true = token0→token1
    int256 amountSpecified,     // Positive = exact input, Negative = exact output
    uint160 sqrtPriceLimitX96,  // Price limit for slippage protection
    bytes calldata data         // Callback data
) external lock returns (int256 amount0, int256 amount1) {
    require(amountSpecified != 0, 'AS');

    Slot0 memory slot0Start = slot0;
    require(slot0Start.unlocked, 'LOK');

    // Validate price limit
    require(
        zeroForOne
            ? sqrtPriceLimitX96 < slot0Start.sqrtPriceX96 && sqrtPriceLimitX96 > TickMath.MIN_SQRT_RATIO
            : sqrtPriceLimitX96 > slot0Start.sqrtPriceX96 && sqrtPriceLimitX96 < TickMath.MAX_SQRT_RATIO,
        'SPL'
    );

    slot0.unlocked = false;

    SwapCache memory cache = SwapCache({
        liquidityStart: liquidity,
        blockTimestamp: _blockTimestamp(),
        feeProtocol: zeroForOne ? (slot0Start.feeProtocol % 16) : (slot0Start.feeProtocol >> 4),
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
        protocolFee: 0,
        liquidity: cache.liquidityStart
    });

    // SWAP LOOP - continues until amount exhausted or price limit reached
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
        if (step.tickNext < TickMath.MIN_TICK) step.tickNext = TickMath.MIN_TICK;
        if (step.tickNext > TickMath.MAX_TICK) step.tickNext = TickMath.MAX_TICK;

        step.sqrtPriceNextX96 = TickMath.getSqrtRatioAtTick(step.tickNext);

        // Compute swap step
        (state.sqrtPriceX96, step.amountIn, step.amountOut, step.feeAmount) = SwapMath.computeSwapStep(
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
            state.feeGrowthGlobalX128 += FullMath.mulDiv(step.feeAmount, FixedPoint128.Q128, state.liquidity);
        }

        // Cross tick if reached
        if (state.sqrtPriceX96 == step.sqrtPriceNextX96) {
            if (step.initialized) {
                int128 liquidityNet = ticks.cross(
                    step.tickNext,
                    (zeroForOne ? state.feeGrowthGlobalX128 : feeGrowthGlobal0X128),
                    (zeroForOne ? feeGrowthGlobal1X128 : state.feeGrowthGlobalX128),
                    cache.secondsPerLiquidityCumulativeX128,
                    cache.tickCumulative,
                    cache.blockTimestamp
                );

                // Update liquidity for new tick range
                if (zeroForOne) liquidityNet = -liquidityNet;
                state.liquidity = LiquidityMath.addDelta(state.liquidity, liquidityNet);
            }

            state.tick = zeroForOne ? step.tickNext - 1 : step.tickNext;
        } else if (state.sqrtPriceX96 != step.sqrtPriceStartX96) {
            state.tick = TickMath.getTickAtSqrtRatio(state.sqrtPriceX96);
        }
    }

    // Update pool state
    // ... oracle update, fee growth update, etc.

    // Calculate final amounts
    (amount0, amount1) = zeroForOne == exactInput
        ? (amountSpecified - state.amountSpecifiedRemaining, state.amountCalculated)
        : (state.amountCalculated, amountSpecified - state.amountSpecifiedRemaining);

    // Transfer output tokens
    if (zeroForOne) {
        if (amount1 < 0) TransferHelper.safeTransfer(token1, recipient, uint256(-amount1));

        uint256 balance0Before = balance0();
        IUniswapV3SwapCallback(msg.sender).uniswapV3SwapCallback(amount0, amount1, data);
        require(balance0Before.add(uint256(amount0)) <= balance0(), 'IIA');
    } else {
        if (amount0 < 0) TransferHelper.safeTransfer(token0, recipient, uint256(-amount0));

        uint256 balance1Before = balance1();
        IUniswapV3SwapCallback(msg.sender).uniswapV3SwapCallback(amount0, amount1, data);
        require(balance1Before.add(uint256(amount1)) <= balance1(), 'IIA');
    }

    emit Swap(msg.sender, recipient, amount0, amount1, state.sqrtPriceX96, state.liquidity, state.tick);
}
```

### SwapMath Library

```solidity
library SwapMath {
    /// @notice Computes the result of swapping some amount in/out
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
            uint256 amountRemainingLessFee = FullMath.mulDiv(
                uint256(amountRemaining),
                1e6 - feePips,
                1e6
            );

            amountIn = zeroForOne
                ? SqrtPriceMath.getAmount0Delta(sqrtRatioTargetX96, sqrtRatioCurrentX96, liquidity, true)
                : SqrtPriceMath.getAmount1Delta(sqrtRatioCurrentX96, sqrtRatioTargetX96, liquidity, true);

            if (amountRemainingLessFee >= amountIn) {
                sqrtRatioNextX96 = sqrtRatioTargetX96;
            } else {
                sqrtRatioNextX96 = SqrtPriceMath.getNextSqrtPriceFromInput(
                    sqrtRatioCurrentX96,
                    liquidity,
                    amountRemainingLessFee,
                    zeroForOne
                );
            }
        } else {
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

        bool max = sqrtRatioTargetX96 == sqrtRatioNextX96;

        // Calculate amounts based on whether we hit target
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

        // Cap output at remaining amount for exact output swaps
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
}
```

## SwapRouter (Periphery)

### Single-Hop Swaps

```solidity
struct ExactInputSingleParams {
    address tokenIn;
    address tokenOut;
    uint24 fee;
    address recipient;
    uint256 deadline;
    uint256 amountIn;
    uint256 amountOutMinimum;
    uint160 sqrtPriceLimitX96;
}

function exactInputSingle(ExactInputSingleParams calldata params)
    external payable
    checkDeadline(params.deadline)
    returns (uint256 amountOut)
{
    amountOut = exactInputInternal(
        params.amountIn,
        params.recipient,
        params.sqrtPriceLimitX96,
        SwapCallbackData({
            path: abi.encodePacked(params.tokenIn, params.fee, params.tokenOut),
            payer: msg.sender
        })
    );
    require(amountOut >= params.amountOutMinimum, 'Too little received');
}

struct ExactOutputSingleParams {
    address tokenIn;
    address tokenOut;
    uint24 fee;
    address recipient;
    uint256 deadline;
    uint256 amountOut;
    uint256 amountInMaximum;
    uint160 sqrtPriceLimitX96;
}

function exactOutputSingle(ExactOutputSingleParams calldata params)
    external payable
    checkDeadline(params.deadline)
    returns (uint256 amountIn)
{
    amountIn = exactOutputInternal(
        params.amountOut,
        params.recipient,
        params.sqrtPriceLimitX96,
        SwapCallbackData({
            path: abi.encodePacked(params.tokenOut, params.fee, params.tokenIn),
            payer: msg.sender
        })
    );
    require(amountIn <= params.amountInMaximum, 'Too much requested');
}
```

### Multi-Hop Swaps

```solidity
struct ExactInputParams {
    bytes path;                  // Encoded path: token0, fee0, token1, fee1, token2, ...
    address recipient;
    uint256 deadline;
    uint256 amountIn;
    uint256 amountOutMinimum;
}

function exactInput(ExactInputParams memory params)
    external payable
    checkDeadline(params.deadline)
    returns (uint256 amountOut)
{
    address payer = msg.sender;

    while (true) {
        bool hasMultiplePools = params.path.hasMultiplePools();

        params.amountIn = exactInputInternal(
            params.amountIn,
            hasMultiplePools ? address(this) : params.recipient,
            0,  // No price limit for intermediate swaps
            SwapCallbackData({
                path: params.path.getFirstPool(),
                payer: payer
            })
        );

        if (hasMultiplePools) {
            payer = address(this);  // Subsequent swaps use router's tokens
            params.path = params.path.skipToken();
        } else {
            amountOut = params.amountIn;
            break;
        }
    }

    require(amountOut >= params.amountOutMinimum, 'Too little received');
}
```

### Path Encoding

```solidity
library Path {
    uint256 private constant ADDR_SIZE = 20;
    uint256 private constant FEE_SIZE = 3;
    uint256 private constant NEXT_OFFSET = ADDR_SIZE + FEE_SIZE;
    uint256 private constant POP_OFFSET = NEXT_OFFSET + ADDR_SIZE;
    uint256 private constant MULTIPLE_POOLS_MIN_LENGTH = POP_OFFSET + NEXT_OFFSET;

    /// @notice Returns true if path contains two or more pools
    function hasMultiplePools(bytes memory path) internal pure returns (bool) {
        return path.length >= MULTIPLE_POOLS_MIN_LENGTH;
    }

    /// @notice Decodes the first pool in path
    function decodeFirstPool(bytes memory path)
        internal pure
        returns (address tokenA, address tokenB, uint24 fee)
    {
        tokenA = path.toAddress(0);
        fee = path.toUint24(ADDR_SIZE);
        tokenB = path.toAddress(NEXT_OFFSET);
    }

    /// @notice Returns the first pool's data
    function getFirstPool(bytes memory path) internal pure returns (bytes memory) {
        return path.slice(0, POP_OFFSET);
    }

    /// @notice Skips a token + fee from the beginning of the path
    function skipToken(bytes memory path) internal pure returns (bytes memory) {
        return path.slice(NEXT_OFFSET, path.length - NEXT_OFFSET);
    }
}
```

### Swap Callback

```solidity
function uniswapV3SwapCallback(
    int256 amount0Delta,
    int256 amount1Delta,
    bytes calldata _data
) external override {
    require(amount0Delta > 0 || amount1Delta > 0);
    SwapCallbackData memory data = abi.decode(_data, (SwapCallbackData));
    (address tokenIn, address tokenOut, uint24 fee) = data.path.decodeFirstPool();
    CallbackValidation.verifyCallback(factory, tokenIn, tokenOut, fee);

    (bool isExactInput, uint256 amountToPay) =
        amount0Delta > 0
            ? (tokenIn < tokenOut, uint256(amount0Delta))
            : (tokenOut < tokenIn, uint256(amount1Delta));

    if (isExactInput) {
        pay(tokenIn, data.payer, msg.sender, amountToPay);
    } else {
        // For exact output, path is reversed
        if (data.path.hasMultiplePools()) {
            data.path = data.path.skipToken();
            exactOutputInternal(amountToPay, msg.sender, 0, data);
        } else {
            amountInCached = amountToPay;
            tokenIn = tokenOut;
            pay(tokenIn, data.payer, msg.sender, amountToPay);
        }
    }
}
```

## Quoter (Price Quotes)

```solidity
interface IQuoter {
    function quoteExactInputSingle(
        address tokenIn,
        address tokenOut,
        uint24 fee,
        uint256 amountIn,
        uint160 sqrtPriceLimitX96
    ) external returns (uint256 amountOut);

    function quoteExactInput(bytes memory path, uint256 amountIn)
        external returns (uint256 amountOut);

    function quoteExactOutputSingle(
        address tokenIn,
        address tokenOut,
        uint24 fee,
        uint256 amountOut,
        uint160 sqrtPriceLimitX96
    ) external returns (uint256 amountIn);

    function quoteExactOutput(bytes memory path, uint256 amountOut)
        external returns (uint256 amountIn);
}
```

The Quoter simulates swaps and reverts to return the quote without actually executing.

## Swap Events

```solidity
event Swap(
    address indexed sender,
    address indexed recipient,
    int256 amount0,          // Positive = received by pool, Negative = sent by pool
    int256 amount1,
    uint160 sqrtPriceX96,    // Price after swap
    uint128 liquidity,       // Liquidity after swap
    int24 tick               // Tick after swap
);
```

## Reference Files

### v3-core
- `contracts/UniswapV3Pool.sol` - Core swap implementation
- `contracts/libraries/SwapMath.sol` - Single-step swap computation
- `contracts/libraries/SqrtPriceMath.sol` - Price delta calculations

### v3-periphery
- `contracts/SwapRouter.sol` - User-facing swap router
- `contracts/lens/Quoter.sol` - Price quote simulation
- `contracts/libraries/Path.sol` - Multi-hop path encoding
- `contracts/libraries/CallbackValidation.sol` - Callback security
