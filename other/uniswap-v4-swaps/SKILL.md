---
name: Uniswap V4 Swaps
description: This skill should be used when the user asks about "swap", "SwapParams", "exactInput", "exactOutput", "BeforeSwapDelta", "swap routing", or needs to understand swap execution in V4.
version: 0.1.0
---

# Uniswap V4 Swaps

## Overview

Swaps in V4 follow the same concentrated liquidity math as V3 but with key enhancements: hooks can modify swap amounts, dynamic fees are supported, and flash accounting defers settlement.

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                            SWAP FLOW                                         │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│  unlock() ──► unlockCallback() ──► swap() ──► settle/take                   │
│                                       │                                      │
│                                       ▼                                      │
│  ┌──────────────────────────────────────────────────────────────────────┐   │
│  │ 1. Validate pool is initialized                                      │   │
│  │                                                                       │   │
│  │ 2. beforeSwap hook (if enabled)                                      │   │
│  │    ├─ Can return BeforeSwapDelta (modify amounts)                    │   │
│  │    └─ Can return lpFeeOverride (dynamic fee)                         │   │
│  │                                                                       │   │
│  │ 3. Pool.swap() - core swap logic                                     │   │
│  │    ├─ Iterate through ticks                                          │   │
│  │    ├─ Calculate amounts at each step                                 │   │
│  │    └─ Update liquidity on tick crossings                             │   │
│  │                                                                       │   │
│  │ 4. afterSwap hook (if enabled)                                       │   │
│  │    └─ Can return delta in unspecified currency                       │   │
│  │                                                                       │   │
│  │ 5. Account deltas to caller                                          │   │
│  │                                                                       │   │
│  │ 6. Return BalanceDelta (caller settles/takes later)                  │   │
│  └──────────────────────────────────────────────────────────────────────┘   │
│                                                                              │
└─────────────────────────────────────────────────────────────────────────────┘
```

## SwapParams

```solidity
struct SwapParams {
    /// @notice Direction: true = token0→token1, false = token1→token0
    bool zeroForOne;

    /// @notice Amount to swap
    /// Negative = exact input (specify input amount)
    /// Positive = exact output (specify desired output)
    int256 amountSpecified;

    /// @notice Price limit for slippage protection
    /// For zeroForOne: must be less than current price
    /// For oneForZero: must be greater than current price
    uint160 sqrtPriceLimitX96;
}
```

## PoolManager.swap()

```solidity
function swap(PoolKey memory key, SwapParams memory params, bytes calldata hookData)
    external
    onlyWhenUnlocked
    noDelegateCall
    returns (BalanceDelta swapDelta)
{
    if (params.amountSpecified == 0) {
        SwapAmountCannotBeZero.selector.revertWith();
    }

    PoolId id = key.toId();
    Pool.State storage pool = _pools[id];
    pool.checkPoolInitialized();

    // Determine fee
    uint24 lpFee = key.fee.isDynamicFee() ? _fetchDynamicLPFee(key) : key.fee.getStaticFee();

    BeforeSwapDelta beforeSwapDelta;
    {
        // Call beforeSwap hook if enabled
        int256 amountToSwap = params.amountSpecified;
        uint24 lpFeeOverride;

        if (key.hooks.hasPermission(Hooks.BEFORE_SWAP_FLAG)) {
            bytes4 selector;
            (selector, beforeSwapDelta, lpFeeOverride) = key.hooks.beforeSwap(
                msg.sender, key, params, hookData
            );

            if (selector != IHooks.beforeSwap.selector) {
                Hooks.InvalidHookResponse.selector.revertWith();
            }

            // If hook returns delta, modify amount to swap
            if (key.hooks.hasPermission(Hooks.BEFORE_SWAP_RETURNS_DELTA_FLAG)) {
                amountToSwap += beforeSwapDelta.getSpecifiedDelta();
            }

            // If hook returns fee override
            if (lpFeeOverride.isOverride()) {
                lpFee = lpFeeOverride.removeOverrideFlag();
            }
        }

        // Execute core swap
        (BalanceDelta delta, uint24 swapFee, Pool.SwapState memory state) = pool.swap(
            Pool.SwapParams({
                tickSpacing: key.tickSpacing,
                zeroForOne: params.zeroForOne,
                amountSpecified: amountToSwap,
                sqrtPriceLimitX96: params.sqrtPriceLimitX96,
                lpFeeOverride: lpFee
            })
        );

        // Combine pool delta with hook's before delta
        swapDelta = delta;
        if (!beforeSwapDelta.isZero()) {
            swapDelta = swapDelta + toBalanceDelta(
                beforeSwapDelta.getSpecifiedDelta(),
                beforeSwapDelta.getUnspecifiedDelta()
            );
        }

        emit Swap(
            id, msg.sender,
            swapDelta.amount0(), swapDelta.amount1(),
            state.sqrtPriceX96, state.liquidity, state.tick, swapFee
        );
    }

    // Call afterSwap hook if enabled
    if (key.hooks.hasPermission(Hooks.AFTER_SWAP_FLAG)) {
        (bytes4 selector, int128 hookDeltaUnspecified) = key.hooks.afterSwap(
            msg.sender, key, params, swapDelta, hookData
        );

        if (selector != IHooks.afterSwap.selector) {
            Hooks.InvalidHookResponse.selector.revertWith();
        }

        // Apply hook's after delta to unspecified currency
        if (key.hooks.hasPermission(Hooks.AFTER_SWAP_RETURNS_DELTA_FLAG)) {
            if (params.zeroForOne) {
                swapDelta = swapDelta + toBalanceDelta(0, hookDeltaUnspecified);
            } else {
                swapDelta = swapDelta + toBalanceDelta(hookDeltaUnspecified, 0);
            }

            // Account hook's delta
            _accountDelta(
                params.zeroForOne ? key.currency1 : key.currency0,
                -hookDeltaUnspecified,
                address(key.hooks)
            );
        }
    }

    // Account caller's delta
    _accountPoolBalanceDelta(key, swapDelta, msg.sender);

    return swapDelta;
}
```

## BeforeSwapDelta

Hooks can modify swap amounts via BeforeSwapDelta:

```solidity
/// @notice Packed delta returned by beforeSwap
/// Upper 128 bits: delta in specified currency (input for exactIn)
/// Lower 128 bits: delta in unspecified currency (output for exactIn)
type BeforeSwapDelta is int256;

library BeforeSwapDeltaLibrary {
    BeforeSwapDelta public constant ZERO_DELTA = BeforeSwapDelta.wrap(0);

    function getSpecifiedDelta(BeforeSwapDelta delta) internal pure returns (int128) {
        return int128(BeforeSwapDelta.unwrap(delta) >> 128);
    }

    function getUnspecifiedDelta(BeforeSwapDelta delta) internal pure returns (int128) {
        return int128(BeforeSwapDelta.unwrap(delta));
    }

    function toBeforeSwapDelta(int128 specifiedDelta, int128 unspecifiedDelta)
        internal pure returns (BeforeSwapDelta)
    {
        return BeforeSwapDelta.wrap(
            (int256(specifiedDelta) << 128) | int256(uint256(uint128(unspecifiedDelta)))
        );
    }

    function isZero(BeforeSwapDelta delta) internal pure returns (bool) {
        return BeforeSwapDelta.unwrap(delta) == 0;
    }
}
```

### Hook Modifying Swap Amount

```solidity
contract SwapTaxHook is BaseHook {
    uint256 public constant TAX_BPS = 100; // 1% tax

    function beforeSwap(
        address,
        PoolKey calldata key,
        IPoolManager.SwapParams calldata params,
        bytes calldata
    ) external override returns (bytes4, BeforeSwapDelta, uint24) {
        // Calculate tax on input amount
        int128 tax;
        if (params.amountSpecified < 0) {
            // Exact input: tax reduces the swap input
            tax = int128(-params.amountSpecified * int256(TAX_BPS) / 10000);
        }

        // Return delta: specified -= tax (less goes into swap)
        // Hook keeps the tax via its own delta accounting
        BeforeSwapDelta delta = toBeforeSwapDelta(-tax, 0);

        return (IHooks.beforeSwap.selector, delta, 0);
    }
}
```

## Pool.swap() (Core Logic)

```solidity
library Pool {
    struct SwapParams {
        int24 tickSpacing;
        bool zeroForOne;
        int256 amountSpecified;
        uint160 sqrtPriceLimitX96;
        uint24 lpFeeOverride;
    }

    struct SwapState {
        int256 amountSpecifiedRemaining;
        int256 amountCalculated;
        uint160 sqrtPriceX96;
        int24 tick;
        uint256 feeGrowthGlobalX128;
        uint128 liquidity;
    }

    function swap(State storage self, SwapParams memory params)
        internal
        returns (BalanceDelta delta, uint24 swapFee, SwapState memory state)
    {
        Slot0 slot0 = self.slot0;
        bool exactInput = params.amountSpecified < 0;

        state = SwapState({
            amountSpecifiedRemaining: params.amountSpecified,
            amountCalculated: 0,
            sqrtPriceX96: slot0.sqrtPriceX96(),
            tick: slot0.tick(),
            feeGrowthGlobalX128: params.zeroForOne
                ? self.feeGrowthGlobal0X128
                : self.feeGrowthGlobal1X128,
            liquidity: self.liquidity
        });

        swapFee = slot0.lpFee();
        if (params.lpFeeOverride != 0) {
            swapFee = params.lpFeeOverride;
        }

        // Swap loop
        while (
            state.amountSpecifiedRemaining != 0 &&
            state.sqrtPriceX96 != params.sqrtPriceLimitX96
        ) {
            StepComputations memory step;
            step.sqrtPriceStartX96 = state.sqrtPriceX96;

            // Find next initialized tick
            (step.tickNext, step.initialized) = self.tickBitmap
                .nextInitializedTickWithinOneWord(
                    state.tick,
                    params.tickSpacing,
                    params.zeroForOne
                );

            // Clamp to valid range
            if (step.tickNext < TickMath.MIN_TICK) step.tickNext = TickMath.MIN_TICK;
            if (step.tickNext > TickMath.MAX_TICK) step.tickNext = TickMath.MAX_TICK;

            step.sqrtPriceNextX96 = TickMath.getSqrtPriceAtTick(step.tickNext);

            // Compute swap step
            (state.sqrtPriceX96, step.amountIn, step.amountOut, step.feeAmount) =
                SwapMath.computeSwapStep(
                    state.sqrtPriceX96,
                    (params.zeroForOne
                        ? step.sqrtPriceNextX96 < params.sqrtPriceLimitX96
                        : step.sqrtPriceNextX96 > params.sqrtPriceLimitX96)
                        ? params.sqrtPriceLimitX96
                        : step.sqrtPriceNextX96,
                    state.liquidity,
                    state.amountSpecifiedRemaining,
                    swapFee
                );

            // Update amounts
            if (exactInput) {
                state.amountSpecifiedRemaining += (step.amountIn + step.feeAmount).toInt256();
                state.amountCalculated -= step.amountOut.toInt256();
            } else {
                state.amountSpecifiedRemaining -= step.amountOut.toInt256();
                state.amountCalculated += (step.amountIn + step.feeAmount).toInt256();
            }

            // Update fee growth
            if (state.liquidity > 0) {
                state.feeGrowthGlobalX128 += FullMath.mulDiv(
                    step.feeAmount,
                    FixedPoint128.Q128,
                    state.liquidity
                );
            }

            // Cross tick if necessary
            if (state.sqrtPriceX96 == step.sqrtPriceNextX96 && step.initialized) {
                int128 liquidityNet = self.ticks.cross(
                    step.tickNext,
                    (params.zeroForOne ? state.feeGrowthGlobalX128 : self.feeGrowthGlobal0X128),
                    (params.zeroForOne ? self.feeGrowthGlobal1X128 : state.feeGrowthGlobalX128)
                );

                if (params.zeroForOne) liquidityNet = -liquidityNet;
                state.liquidity = state.liquidity.addDelta(liquidityNet);
            }

            state.tick = params.zeroForOne ? step.tickNext - 1 : step.tickNext;
        }

        // Update storage
        self.slot0 = slot0.setSqrtPriceX96(state.sqrtPriceX96).setTick(state.tick);

        if (params.zeroForOne) {
            self.feeGrowthGlobal0X128 = state.feeGrowthGlobalX128;
        } else {
            self.feeGrowthGlobal1X128 = state.feeGrowthGlobalX128;
        }

        if (state.liquidity != self.liquidity) {
            self.liquidity = state.liquidity;
        }

        // Calculate final delta
        (int256 amount0, int256 amount1) = params.zeroForOne == exactInput
            ? (params.amountSpecified - state.amountSpecifiedRemaining, state.amountCalculated)
            : (state.amountCalculated, params.amountSpecified - state.amountSpecifiedRemaining);

        delta = toBalanceDelta(amount0.toInt128(), amount1.toInt128());
    }
}
```

## V4Router (Periphery)

```solidity
contract V4Router is IV4Router, BaseActionsRouter {
    /// @notice Swap exact input for single hop
    function _swapExactInputSingle(ExactInputSingleParams calldata params)
        internal
        returns (uint256 amountOut)
    {
        BalanceDelta delta = poolManager.swap(
            params.poolKey,
            IPoolManager.SwapParams({
                zeroForOne: params.zeroForOne,
                amountSpecified: -int256(params.amountIn),
                sqrtPriceLimitX96: params.sqrtPriceLimitX96
            }),
            params.hookData
        );

        amountOut = uint256(
            -(params.zeroForOne ? delta.amount1() : delta.amount0())
        );

        if (amountOut < params.amountOutMinimum) {
            TooLittleReceived.selector.revertWith();
        }
    }

    /// @notice Swap exact output for single hop
    function _swapExactOutputSingle(ExactOutputSingleParams calldata params)
        internal
        returns (uint256 amountIn)
    {
        BalanceDelta delta = poolManager.swap(
            params.poolKey,
            IPoolManager.SwapParams({
                zeroForOne: params.zeroForOne,
                amountSpecified: int256(params.amountOut),
                sqrtPriceLimitX96: params.sqrtPriceLimitX96
            }),
            params.hookData
        );

        amountIn = uint256(
            params.zeroForOne ? delta.amount0() : delta.amount1()
        );

        if (amountIn > params.amountInMaximum) {
            TooMuchRequested.selector.revertWith();
        }
    }
}
```

## Multi-Hop Swaps

```solidity
struct PathKey {
    Currency intermediateCurrency;
    uint24 fee;
    int24 tickSpacing;
    IHooks hooks;
    bytes hookData;
}

function swapExactInput(
    Currency currencyIn,
    PathKey[] calldata path,
    uint256 amountIn,
    uint256 amountOutMinimum
) external returns (uint256 amountOut) {
    Currency currentCurrency = currencyIn;
    uint256 currentAmount = amountIn;

    for (uint i = 0; i < path.length; i++) {
        PoolKey memory key = PoolKey({
            currency0: currentCurrency < path[i].intermediateCurrency
                ? currentCurrency : path[i].intermediateCurrency,
            currency1: currentCurrency < path[i].intermediateCurrency
                ? path[i].intermediateCurrency : currentCurrency,
            fee: path[i].fee,
            tickSpacing: path[i].tickSpacing,
            hooks: path[i].hooks
        });

        bool zeroForOne = currentCurrency == key.currency0;

        BalanceDelta delta = poolManager.swap(
            key,
            IPoolManager.SwapParams({
                zeroForOne: zeroForOne,
                amountSpecified: -int256(currentAmount),
                sqrtPriceLimitX96: zeroForOne
                    ? TickMath.MIN_SQRT_PRICE + 1
                    : TickMath.MAX_SQRT_PRICE - 1
            }),
            path[i].hookData
        );

        currentAmount = uint256(-(zeroForOne ? delta.amount1() : delta.amount0()));
        currentCurrency = path[i].intermediateCurrency;
    }

    amountOut = currentAmount;
    require(amountOut >= amountOutMinimum, "Too little received");
}
```

## Reference Files

### v4-core
- `src/PoolManager.sol` - swap() function
- `src/libraries/Pool.sol` - Core swap logic
- `src/libraries/SwapMath.sol` - Step computation
- `src/types/BeforeSwapDelta.sol` - Hook delta type

### v4-periphery
- `src/V4Router.sol` - Swap routing
- `src/libraries/PathKey.sol` - Multi-hop path
