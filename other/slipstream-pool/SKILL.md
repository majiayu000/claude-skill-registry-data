---
name: Slipstream Pool Operations
description: This skill should be used when the user asks about "mint", "burn", "position", "liquidity", "provide liquidity", "add liquidity", "remove liquidity", "CLPool", or needs to understand pool-level liquidity operations.
version: 0.1.0
---

# Slipstream Pool Operations

CLPool is the core contract for concentrated liquidity. This skill covers minting and burning liquidity at the pool level.

## Overview

```
┌──────────────────────────────────────────────────────────────┐
│                   POOL OPERATIONS                            │
├──────────────────────────────────────────────────────────────┤
│                                                              │
│  mint() - Add Liquidity                                      │
│  ┌─────────────────────────────────────────────────────────┐ │
│  │ 1. Calculate token amounts for liquidity                │ │
│  │ 2. Update tick data (liquidityGross, liquidityNet)      │ │
│  │ 3. Initialize ticks if needed (tickBitmap)              │ │
│  │ 4. Update position (fee snapshots)                      │ │
│  │ 5. If in range: add to global liquidity                 │ │
│  │ 6. Callback to receive tokens                           │ │
│  └─────────────────────────────────────────────────────────┘ │
│                                                              │
│  burn() - Remove Liquidity                                   │
│  ┌─────────────────────────────────────────────────────────┐ │
│  │ 1. Update position (calculate fees owed)                │ │
│  │ 2. Update tick data (reduce liquidity)                  │ │
│  │ 3. Clear ticks if liquidityGross == 0                   │ │
│  │ 4. If in range: subtract from global liquidity          │ │
│  │ 5. Store tokens owed for later collect()                │ │
│  └─────────────────────────────────────────────────────────┘ │
│                                                              │
│  collect() - Withdraw Tokens                                 │
│  └── Withdraw tokensOwed0/tokensOwed1 from position         │
│                                                              │
└──────────────────────────────────────────────────────────────┘
```

## Position Structure

```solidity
// Position.sol

struct Info {
    uint128 liquidity;                    // Position's liquidity
    uint256 feeGrowthInside0LastX128;    // Fee snapshot for token0
    uint256 feeGrowthInside1LastX128;    // Fee snapshot for token1
    uint128 tokensOwed0;                  // Uncollected token0 fees
    uint128 tokensOwed1;                  // Uncollected token1 fees
    uint256 rewardGrowthInsideLastX128;  // Reward snapshot for gauge
}

// Position key = keccak256(owner, tickLower, tickUpper)
mapping(bytes32 => Position.Info) public positions;

function positionKey(
    address owner,
    int24 tickLower,
    int24 tickUpper
) internal pure returns (bytes32) {
    return keccak256(abi.encodePacked(owner, tickLower, tickUpper));
}
```

## Mint (Add Liquidity)

```solidity
// CLPool.sol

/// @notice Add liquidity to a position
/// @param recipient Owner of the position
/// @param tickLower Lower tick boundary
/// @param tickUpper Upper tick boundary
/// @param amount Liquidity to add
/// @param data Callback data for token transfer
/// @return amount0 Token0 amount required
/// @return amount1 Token1 amount required
function mint(
    address recipient,
    int24 tickLower,
    int24 tickUpper,
    uint128 amount,
    bytes calldata data
) external lock returns (uint256 amount0, uint256 amount1) {
    require(amount > 0, "amount = 0");

    // 1. Calculate amounts and update position
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

    // 2. Callback to receive tokens
    ICLMintCallback(msg.sender).uniswapV3MintCallback(amount0, amount1, data);

    // 3. Verify tokens received
    if (amount0 > 0) require(balance0Before + amount0 <= balance0(), "M0");
    if (amount1 > 0) require(balance1Before + amount1 <= balance1(), "M1");

    emit Mint(msg.sender, recipient, tickLower, tickUpper, amount, amount0, amount1);
}
```

## Modify Position (Internal)

```solidity
struct ModifyPositionParams {
    address owner;
    int24 tickLower;
    int24 tickUpper;
    int128 liquidityDelta;  // Positive for mint, negative for burn
}

function _modifyPosition(ModifyPositionParams memory params)
    private
    returns (Position.Info storage position, int256 amount0, int256 amount1)
{
    // Validate tick boundaries
    checkTicks(params.tickLower, params.tickUpper);

    Slot0 memory _slot0 = slot0;

    // 1. Update position and get fee/reward growth
    position = _updatePosition(
        params.owner,
        params.tickLower,
        params.tickUpper,
        params.liquidityDelta,
        _slot0.tick
    );

    // 2. Calculate token amounts if liquidity changes
    if (params.liquidityDelta != 0) {
        if (_slot0.tick < params.tickLower) {
            // Current price below range - only token0 needed
            amount0 = SqrtPriceMath.getAmount0Delta(
                TickMath.getSqrtRatioAtTick(params.tickLower),
                TickMath.getSqrtRatioAtTick(params.tickUpper),
                params.liquidityDelta
            );
        } else if (_slot0.tick < params.tickUpper) {
            // Current price in range - both tokens needed
            amount0 = SqrtPriceMath.getAmount0Delta(
                _slot0.sqrtPriceX96,
                TickMath.getSqrtRatioAtTick(params.tickUpper),
                params.liquidityDelta
            );
            amount1 = SqrtPriceMath.getAmount1Delta(
                TickMath.getSqrtRatioAtTick(params.tickLower),
                _slot0.sqrtPriceX96,
                params.liquidityDelta
            );

            // Update global liquidity
            liquidity = LiquidityMath.addDelta(liquidity, params.liquidityDelta);
        } else {
            // Current price above range - only token1 needed
            amount1 = SqrtPriceMath.getAmount1Delta(
                TickMath.getSqrtRatioAtTick(params.tickLower),
                TickMath.getSqrtRatioAtTick(params.tickUpper),
                params.liquidityDelta
            );
        }
    }
}
```

## Update Position

```solidity
function _updatePosition(
    address owner,
    int24 tickLower,
    int24 tickUpper,
    int128 liquidityDelta,
    int24 tick
) private returns (Position.Info storage position) {
    position = positions[positionKey(owner, tickLower, tickUpper)];

    // Get current fee growth inside range
    (
        uint256 feeGrowthInside0X128,
        uint256 feeGrowthInside1X128
    ) = getFeeGrowthInside(tickLower, tickUpper);

    // Get reward growth inside range
    uint256 rewardGrowthInsideX128 = getRewardGrowthInside(tickLower, tickUpper, tick);

    // Calculate fees owed since last update
    uint128 tokensOwed0;
    uint128 tokensOwed1;
    if (position.liquidity > 0) {
        tokensOwed0 = uint128(
            FullMath.mulDiv(
                feeGrowthInside0X128 - position.feeGrowthInside0LastX128,
                position.liquidity,
                FixedPoint128.Q128
            )
        );
        tokensOwed1 = uint128(
            FullMath.mulDiv(
                feeGrowthInside1X128 - position.feeGrowthInside1LastX128,
                position.liquidity,
                FixedPoint128.Q128
            )
        );
    }

    // Update ticks if liquidity changes
    if (liquidityDelta != 0) {
        bool flippedLower = ticks.update(
            tickLower,
            tick,
            liquidityDelta,
            feeGrowthGlobal0X128,
            feeGrowthGlobal1X128,
            rewardGrowthGlobalX128,
            secondsPerLiquidityCumulativeX128,
            tickCumulative,
            time,
            false,  // lower tick
            maxLiquidityPerTick
        );

        bool flippedUpper = ticks.update(
            tickUpper,
            tick,
            liquidityDelta,
            feeGrowthGlobal0X128,
            feeGrowthGlobal1X128,
            rewardGrowthGlobalX128,
            secondsPerLiquidityCumulativeX128,
            tickCumulative,
            time,
            true,  // upper tick
            maxLiquidityPerTick
        );

        // Update tick bitmap if tick was initialized/cleared
        if (flippedLower) tickBitmap.flipTick(tickLower, tickSpacing);
        if (flippedUpper) tickBitmap.flipTick(tickUpper, tickSpacing);
    }

    // Update position state
    position.feeGrowthInside0LastX128 = feeGrowthInside0X128;
    position.feeGrowthInside1LastX128 = feeGrowthInside1X128;
    position.rewardGrowthInsideLastX128 = rewardGrowthInsideX128;

    if (liquidityDelta < 0) {
        position.tokensOwed0 += tokensOwed0;
        position.tokensOwed1 += tokensOwed1;
    }

    position.liquidity = LiquidityMath.addDelta(position.liquidity, liquidityDelta);
}
```

## Burn (Remove Liquidity)

```solidity
/// @notice Remove liquidity from a position
/// @param tickLower Lower tick boundary
/// @param tickUpper Upper tick boundary
/// @param amount Liquidity to remove
/// @return amount0 Token0 amount owed
/// @return amount1 Token1 amount owed
function burn(
    int24 tickLower,
    int24 tickUpper,
    uint128 amount
) external lock returns (uint256 amount0, uint256 amount1) {
    // Modify position with negative liquidity delta
    (Position.Info storage position, int256 amount0Int, int256 amount1Int) = _modifyPosition(
        ModifyPositionParams({
            owner: msg.sender,
            tickLower: tickLower,
            tickUpper: tickUpper,
            liquidityDelta: -int256(uint256(amount)).toInt128()
        })
    );

    amount0 = uint256(-amount0Int);
    amount1 = uint256(-amount1Int);

    // Add withdrawn amounts to tokensOwed
    if (amount0 > 0 || amount1 > 0) {
        (position.tokensOwed0, position.tokensOwed1) = (
            position.tokensOwed0 + uint128(amount0),
            position.tokensOwed1 + uint128(amount1)
        );
    }

    emit Burn(msg.sender, tickLower, tickUpper, amount, amount0, amount1);
}
```

## Collect (Withdraw Tokens)

```solidity
/// @notice Collect tokens owed from a position
/// @param recipient Address to receive tokens
/// @param tickLower Lower tick boundary
/// @param tickUpper Upper tick boundary
/// @param amount0Requested Max token0 to collect
/// @param amount1Requested Max token1 to collect
/// @return amount0 Token0 collected
/// @return amount1 Token1 collected
function collect(
    address recipient,
    int24 tickLower,
    int24 tickUpper,
    uint128 amount0Requested,
    uint128 amount1Requested
) external lock returns (uint128 amount0, uint128 amount1) {
    Position.Info storage position = positions[positionKey(msg.sender, tickLower, tickUpper)];

    // Cap at tokens owed
    amount0 = amount0Requested > position.tokensOwed0 ? position.tokensOwed0 : amount0Requested;
    amount1 = amount1Requested > position.tokensOwed1 ? position.tokensOwed1 : amount1Requested;

    // Reduce tokens owed
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

## Fee Growth Inside Range

```solidity
/// @notice Calculate fee growth inside a tick range
function getFeeGrowthInside(
    int24 tickLower,
    int24 tickUpper
) internal view returns (uint256 feeGrowthInside0X128, uint256 feeGrowthInside1X128) {
    Tick.Info storage lower = ticks[tickLower];
    Tick.Info storage upper = ticks[tickUpper];

    int24 tickCurrent = slot0.tick;

    // Calculate fee growth below lower tick
    uint256 feeGrowthBelow0X128;
    uint256 feeGrowthBelow1X128;
    if (tickCurrent >= tickLower) {
        feeGrowthBelow0X128 = lower.feeGrowthOutside0X128;
        feeGrowthBelow1X128 = lower.feeGrowthOutside1X128;
    } else {
        feeGrowthBelow0X128 = feeGrowthGlobal0X128 - lower.feeGrowthOutside0X128;
        feeGrowthBelow1X128 = feeGrowthGlobal1X128 - lower.feeGrowthOutside1X128;
    }

    // Calculate fee growth above upper tick
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

## Staking Liquidity

```solidity
/// @notice Stake/unstake liquidity in gauge
/// @dev Only callable by pool's gauge
function stake(int128 stakedLiquidityDelta) external {
    require(msg.sender == gauge, "NG");  // Not Gauge

    Slot0 memory _slot0 = slot0;

    // Update global staked liquidity if in range
    stakedLiquidity = LiquidityMath.addDelta(stakedLiquidity, stakedLiquidityDelta);

    // Update tick staked liquidity nets
    // (handled separately when position is staked/unstaked)
}
```

## Events

```solidity
event Mint(
    address sender,
    address indexed owner,
    int24 indexed tickLower,
    int24 indexed tickUpper,
    uint128 amount,
    uint256 amount0,
    uint256 amount1
);

event Burn(
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
```

## Reference Files

- `contracts/core/CLPool.sol` - Main pool contract
- `contracts/core/libraries/Position.sol` - Position accounting
- `contracts/core/libraries/Tick.sol` - Tick updates
- `contracts/core/libraries/SqrtPriceMath.sol` - Amount calculations
