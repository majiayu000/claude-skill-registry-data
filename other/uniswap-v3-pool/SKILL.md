---
name: Uniswap V3 Pool
description: This skill should be used when the user asks about "UniswapV3Pool", "pool contract", "slot0", "pool state", "pool liquidity", "pool initialization", or needs to understand the core pool mechanics.
version: 0.1.0
---

# Uniswap V3 Pool

## Overview

The UniswapV3Pool contract is the core AMM implementation that manages liquidity positions, executes swaps, handles fee collection, and maintains oracle observations for a single token pair at a specific fee tier.

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                          UniswapV3Pool State                                │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│  IMMUTABLES                          SLOT0 (packed storage)                 │
│  ┌────────────────────┐              ┌──────────────────────────────────┐   │
│  │ factory            │              │ sqrtPriceX96    (160 bits)       │   │
│  │ token0             │              │ tick            (24 bits)        │   │
│  │ token1             │              │ observationIndex (16 bits)       │   │
│  │ fee                │              │ observationCardinality (16 bits) │   │
│  │ tickSpacing        │              │ observationCardinalityNext       │   │
│  │ maxLiquidityPerTick│              │ feeProtocol     (8 bits)         │   │
│  └────────────────────┘              │ unlocked        (1 bit)          │   │
│                                      └──────────────────────────────────┘   │
│                                                                              │
│  GLOBAL STATE                        PER-TICK STATE                         │
│  ┌────────────────────┐              ┌──────────────────────────────────┐   │
│  │ feeGrowthGlobal0   │              │ ticks[tick] → Tick.Info          │   │
│  │ feeGrowthGlobal1   │              │   liquidityGross                 │   │
│  │ protocolFees       │              │   liquidityNet                   │   │
│  │ liquidity          │              │   feeGrowthOutside0X128          │   │
│  └────────────────────┘              │   feeGrowthOutside1X128          │   │
│                                      │   tickCumulativeOutside          │   │
│  ORACLE                              │   secondsPerLiquidityOutside     │   │
│  ┌────────────────────┐              │   secondsOutside                 │   │
│  │ observations[]     │              │   initialized                    │   │
│  │ (ring buffer)      │              └──────────────────────────────────┘   │
│  └────────────────────┘                                                     │
│                                      TICK BITMAP                            │
│  POSITIONS                           ┌──────────────────────────────────┐   │
│  ┌────────────────────┐              │ tickBitmap[wordPos] → 256 bits   │   │
│  │ positions[key] →   │              │ (packed initialized tick flags)  │   │
│  │   Position.Info    │              └──────────────────────────────────┘   │
│  └────────────────────┘                                                     │
└─────────────────────────────────────────────────────────────────────────────┘
```

## Slot0 Structure

The most frequently accessed state is packed into a single storage slot for gas efficiency.

```solidity
struct Slot0 {
    // Current sqrt(token1/token0) price in Q64.96 format
    uint160 sqrtPriceX96;

    // Current tick (derived from sqrtPriceX96)
    int24 tick;

    // Index of most recent oracle observation
    uint16 observationIndex;

    // Current maximum number of observations
    uint16 observationCardinality;

    // Next maximum (grows when requested)
    uint16 observationCardinalityNext;

    // Protocol fee: lower 4 bits for token0, upper 4 bits for token1
    // Each value 0-10 means 0%, 10%, 20%, ..., 100% of LP fee
    uint8 feeProtocol;

    // Reentrancy guard
    bool unlocked;
}
```

## Pool Initialization

Pools must be initialized with a starting price before any liquidity can be added.

```solidity
function initialize(uint160 sqrtPriceX96) external {
    require(slot0.sqrtPriceX96 == 0, 'AI');  // Already initialized

    int24 tick = TickMath.getTickAtSqrtRatio(sqrtPriceX96);

    // Initialize oracle
    (uint16 cardinality, uint16 cardinalityNext) = observations.initialize(_blockTimestamp());

    slot0 = Slot0({
        sqrtPriceX96: sqrtPriceX96,
        tick: tick,
        observationIndex: 0,
        observationCardinality: cardinality,
        observationCardinalityNext: cardinalityNext,
        feeProtocol: 0,
        unlocked: true
    });

    emit Initialize(sqrtPriceX96, tick);
}
```

## Core Operations

### Mint (Add Liquidity)

```solidity
function mint(
    address recipient,
    int24 tickLower,
    int24 tickUpper,
    uint128 amount,          // Liquidity amount (not token amounts)
    bytes calldata data
) external lock returns (uint256 amount0, uint256 amount1) {
    require(amount > 0);

    // Update position and tick state
    (, int256 amount0Int, int256 amount1Int) = _modifyPosition(
        ModifyPositionParams({
            owner: recipient,
            tickLower: tickLower,
            tickUpper: tickUpper,
            liquidityDelta: int256(uint256(amount)).toInt128()
        })
    );

    amount0 = uint256(amount0Int);
    amount1 = uint256(amount1Int);

    uint256 balance0Before;
    uint256 balance1Before;
    if (amount0 > 0) balance0Before = balance0();
    if (amount1 > 0) balance1Before = balance1();

    // Callback to receive tokens
    IUniswapV3MintCallback(msg.sender).uniswapV3MintCallback(amount0, amount1, data);

    // Verify tokens received
    if (amount0 > 0) require(balance0Before.add(amount0) <= balance0(), 'M0');
    if (amount1 > 0) require(balance1Before.add(amount1) <= balance1(), 'M1');

    emit Mint(msg.sender, recipient, tickLower, tickUpper, amount, amount0, amount1);
}
```

### Burn (Remove Liquidity)

```solidity
function burn(
    int24 tickLower,
    int24 tickUpper,
    uint128 amount
) external lock returns (uint256 amount0, uint256 amount1) {
    // Update position (negative liquidity delta)
    (Position.Info storage position, int256 amount0Int, int256 amount1Int) = _modifyPosition(
        ModifyPositionParams({
            owner: msg.sender,
            tickLower: tickLower,
            tickUpper: tickUpper,
            liquidityDelta: -int256(uint256(amount)).toInt128()
        })
    );

    // Amounts are negative (owed to LP)
    amount0 = uint256(-amount0Int);
    amount1 = uint256(-amount1Int);

    // Add to tokens owed (collected via collect())
    if (amount0 > 0 || amount1 > 0) {
        (position.tokensOwed0, position.tokensOwed1) = (
            position.tokensOwed0 + uint128(amount0),
            position.tokensOwed1 + uint128(amount1)
        );
    }

    emit Burn(msg.sender, tickLower, tickUpper, amount, amount0, amount1);
}
```

### Swap

```solidity
function swap(
    address recipient,
    bool zeroForOne,           // true = token0→token1, false = token1→token0
    int256 amountSpecified,    // positive = exact input, negative = exact output
    uint160 sqrtPriceLimitX96, // Price limit (slippage protection)
    bytes calldata data
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

    // ... swap loop across ticks ...

    // Update oracle observation
    (slot0.sqrtPriceX96, slot0.tick, slot0.observationIndex, slot0.observationCardinality) =
        _updateOracle(slot0Start, state.tick);

    // Callback to receive input tokens
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

### Collect (Claim Fees/Tokens)

```solidity
function collect(
    address recipient,
    int24 tickLower,
    int24 tickUpper,
    uint128 amount0Requested,
    uint128 amount1Requested
) external lock returns (uint128 amount0, uint128 amount1) {
    Position.Info storage position = positions.get(msg.sender, tickLower, tickUpper);

    // Cap at available amounts
    amount0 = amount0Requested > position.tokensOwed0 ? position.tokensOwed0 : amount0Requested;
    amount1 = amount1Requested > position.tokensOwed1 ? position.tokensOwed1 : amount1Requested;

    // Update owed amounts
    if (amount0 > 0) {
        position.tokensOwed0 -= amount0;
        TransferHelper.safeTransfer(token0, recipient, amount0);
    }
    if (amount1 > 0) {
        position.tokensOwed1 -= amount1;
        TransferHelper.safeTransfer(token1, recipient, amount1);
    }

    emit Collect(msg.sender, recipient, tickLower, tickUpper, amount0, amount1);
}
```

### Flash Loan

```solidity
function flash(
    address recipient,
    uint256 amount0,
    uint256 amount1,
    bytes calldata data
) external lock {
    uint128 _liquidity = liquidity;
    require(_liquidity > 0, 'L');

    // Calculate fees (same as swap fee)
    uint256 fee0 = FullMath.mulDivRoundingUp(amount0, fee, 1e6);
    uint256 fee1 = FullMath.mulDivRoundingUp(amount1, fee, 1e6);

    uint256 balance0Before = balance0();
    uint256 balance1Before = balance1();

    // Transfer requested amounts
    if (amount0 > 0) TransferHelper.safeTransfer(token0, recipient, amount0);
    if (amount1 > 0) TransferHelper.safeTransfer(token1, recipient, amount1);

    // Callback
    IUniswapV3FlashCallback(msg.sender).uniswapV3FlashCallback(fee0, fee1, data);

    // Verify repayment + fees
    uint256 balance0After = balance0();
    uint256 balance1After = balance1();
    require(balance0Before.add(fee0) <= balance0After, 'F0');
    require(balance1Before.add(fee1) <= balance1After, 'F1');

    // Calculate actual paid fees (may be more than required)
    uint256 paid0 = balance0After - balance0Before;
    uint256 paid1 = balance1After - balance1Before;

    // Update fee growth
    if (paid0 > 0) feeGrowthGlobal0X128 += FullMath.mulDiv(paid0, FixedPoint128.Q128, _liquidity);
    if (paid1 > 0) feeGrowthGlobal1X128 += FullMath.mulDiv(paid1, FixedPoint128.Q128, _liquidity);

    emit Flash(msg.sender, recipient, amount0, amount1, paid0, paid1);
}
```

## View Functions

### Observe (Oracle)

```solidity
function observe(uint32[] calldata secondsAgos)
    external view
    returns (int56[] memory tickCumulatives, uint160[] memory secondsPerLiquidityCumulativeX128s)
{
    return observations.observe(
        _blockTimestamp(),
        secondsAgos,
        slot0.tick,
        slot0.observationIndex,
        liquidity,
        slot0.observationCardinality
    );
}
```

### Snapshot Cumulatives Inside

```solidity
function snapshotCumulativesInside(int24 tickLower, int24 tickUpper)
    external view
    returns (
        int56 tickCumulativeInside,
        uint160 secondsPerLiquidityInsideX128,
        uint32 secondsInside
    )
{
    // Returns cumulative values within a position's tick range
    // Used for liquidity mining and other incentive programs
}
```

## Fee Growth Tracking

Fee growth is tracked globally and per-tick to enable efficient per-position fee calculation.

```
Fee Calculation Flow:
┌────────────────────────────────────────────────────────────────────┐
│                                                                    │
│  feeGrowthGlobal = total fees / total liquidity (all time)        │
│                                                                    │
│  feeGrowthOutside[tick] = fees accumulated when price was         │
│                           on the "other side" of this tick        │
│                                                                    │
│  feeGrowthInside = feeGrowthGlobal                                │
│                    - feeGrowthBelow(tickLower)                    │
│                    - feeGrowthAbove(tickUpper)                    │
│                                                                    │
│  feesOwed = (feeGrowthInside - feeGrowthInsideLast) × liquidity   │
│                                                                    │
└────────────────────────────────────────────────────────────────────┘
```

## Events

```solidity
event Initialize(uint160 sqrtPriceX96, int24 tick);

event Mint(
    address sender,
    address indexed owner,
    int24 indexed tickLower,
    int24 indexed tickUpper,
    uint128 amount,
    uint256 amount0,
    uint256 amount1
);

event Collect(
    address indexed owner,
    address recipient,
    int24 indexed tickLower,
    int24 indexed tickUpper,
    uint128 amount0,
    uint128 amount1
);

event Burn(
    address indexed owner,
    int24 indexed tickLower,
    int24 indexed tickUpper,
    uint128 amount,
    uint256 amount0,
    uint256 amount1
);

event Swap(
    address indexed sender,
    address indexed recipient,
    int256 amount0,
    int256 amount1,
    uint160 sqrtPriceX96,
    uint128 liquidity,
    int24 tick
);

event Flash(
    address indexed sender,
    address indexed recipient,
    uint256 amount0,
    uint256 amount1,
    uint256 paid0,
    uint256 paid1
);
```

## Reference Files

- `contracts/UniswapV3Pool.sol` - Main pool implementation
- `contracts/interfaces/pool/IUniswapV3PoolState.sol` - State interface
- `contracts/interfaces/pool/IUniswapV3PoolActions.sol` - Actions interface
- `contracts/interfaces/pool/IUniswapV3PoolEvents.sol` - Events interface
