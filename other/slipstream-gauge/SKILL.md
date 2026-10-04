---
name: Slipstream Gauge & Rewards
description: This skill should be used when the user asks about "gauge", "CLGauge", "stake", "deposit", "reward", "AERO", "emissions", "getReward", or needs to understand gauge staking and reward distribution.
version: 0.1.0
---

# Slipstream Gauge & Rewards

CLGauge enables staking LP positions to earn AERO emissions while maintaining concentrated liquidity positions.

## Overview

```
┌──────────────────────────────────────────────────────────────┐
│                    GAUGE SYSTEM                              │
├──────────────────────────────────────────────────────────────┤
│                                                              │
│  Position Lifecycle with Gauge:                              │
│  ┌─────────────────────────────────────────────────────────┐ │
│  │                                                         │ │
│  │  1. User mints position via NonfungiblePositionManager  │ │
│  │     └── Gets NFT (tokenId)                              │ │
│  │                                                         │ │
│  │  2. User deposits NFT into CLGauge                      │ │
│  │     ├── gauge.deposit(tokenId)                          │ │
│  │     ├── Collects pending fees from position             │ │
│  │     ├── Updates pool.stakedLiquidity                    │ │
│  │     └── Starts earning AERO rewards                     │ │
│  │                                                         │ │
│  │  3. User earns rewards proportional to:                 │ │
│  │     ├── Their liquidity amount                          │ │
│  │     ├── Time staked                                     │ │
│  │     └── Whether position is in range                    │ │
│  │                                                         │ │
│  │  4. User claims via gauge.getReward(tokenId)            │ │
│  │                                                         │ │
│  │  5. User withdraws via gauge.withdraw(tokenId)          │ │
│  │                                                         │ │
│  └─────────────────────────────────────────────────────────┘ │
│                                                              │
└──────────────────────────────────────────────────────────────┘
```

## CLGauge Contract

```solidity
// gauge/CLGauge.sol

contract CLGauge is ICLGauge, ReentrancyGuard {
    ICLPool public pool;
    IVoter public voter;
    INonfungiblePositionManager public nft;

    address public rewardToken;     // AERO
    address public feesVotingReward;  // Voting rewards contract

    // Position tracking
    mapping(uint256 tokenId => address owner) public stakedPositions;
    mapping(uint256 tokenId => uint256 rewardGrowthInsideLastX128) public rewardGrowthInsideLast;

    // Time tracking
    uint256 public periodFinish;
    uint256 public lastUpdateTime;
}
```

## Pool Reward State

```solidity
// CLPool.sol - Reward tracking

uint256 public rewardGrowthGlobalX128;  // Accumulated rewards per unit staked liquidity
uint256 public rewardRate;               // Rewards per second
uint256 public rewardReserve;            // Unallocated rewards
uint256 public periodFinish;             // When current period ends
uint256 public lastUpdated;              // Last reward update time

// Per-tick reward tracking
struct Tick.Info {
    // ... other fields
    uint256 rewardGrowthOutsideX128;  // Rewards accumulated outside this tick
}
```

## Deposit (Stake Position)

```solidity
/// @notice Stake an LP position in the gauge
/// @param tokenId NFT token ID to stake
function deposit(uint256 tokenId) external nonReentrant {
    require(msg.sender == nft.ownerOf(tokenId), "NA");  // Not authorized

    // Get position details
    (
        ,
        ,
        address token0,
        address token1,
        int24 tickSpacing,
        int24 tickLower,
        int24 tickUpper,
        uint128 liquidity,
        ,
        ,
        ,
    ) = nft.positions(tokenId);

    // Verify position matches this gauge's pool
    require(
        pool == CLFactory(voter.factory()).getPool(token0, token1, tickSpacing),
        "PM"  // Pool mismatch
    );
    require(liquidity > 0, "LZ");  // Liquidity zero

    // Collect any pending fees before staking
    nft.collect(
        INonfungiblePositionManager.CollectParams({
            tokenId: tokenId,
            recipient: msg.sender,
            amount0Max: type(uint128).max,
            amount1Max: type(uint128).max
        })
    );

    // Transfer NFT to gauge
    nft.safeTransferFrom(msg.sender, address(this), tokenId);

    // Update staked liquidity in pool
    pool.stake(int128(liquidity));

    // Record reward growth snapshot
    rewardGrowthInsideLast[tokenId] = _getRewardGrowthInside(tickLower, tickUpper);

    stakedPositions[tokenId] = msg.sender;

    emit Deposit(msg.sender, tokenId, liquidity);
}
```

## Withdraw (Unstake Position)

```solidity
/// @notice Unstake an LP position from the gauge
/// @param tokenId NFT token ID to unstake
function withdraw(uint256 tokenId) external nonReentrant {
    require(stakedPositions[tokenId] == msg.sender, "NA");

    // Get position liquidity
    (
        ,
        ,
        ,
        ,
        ,
        int24 tickLower,
        int24 tickUpper,
        uint128 liquidity,
        ,
        ,
        ,
    ) = nft.positions(tokenId);

    // Claim pending rewards
    _getReward(tokenId, msg.sender);

    // Update staked liquidity in pool
    pool.stake(-int128(liquidity));

    // Return NFT to owner
    delete stakedPositions[tokenId];
    nft.safeTransferFrom(address(this), msg.sender, tokenId);

    emit Withdraw(msg.sender, tokenId, liquidity);
}
```

## Get Reward

```solidity
/// @notice Claim accumulated rewards for a position
/// @param tokenId NFT token ID
function getReward(uint256 tokenId) external nonReentrant {
    require(stakedPositions[tokenId] == msg.sender, "NA");
    _getReward(tokenId, msg.sender);
}

function _getReward(uint256 tokenId, address owner) internal {
    (
        ,
        ,
        ,
        ,
        ,
        int24 tickLower,
        int24 tickUpper,
        uint128 liquidity,
        ,
        ,
        ,
    ) = nft.positions(tokenId);

    // Get current reward growth inside position's range
    uint256 rewardGrowthInsideX128 = _getRewardGrowthInside(tickLower, tickUpper);

    // Calculate rewards earned
    uint256 reward = FullMath.mulDiv(
        rewardGrowthInsideX128 - rewardGrowthInsideLast[tokenId],
        liquidity,
        FixedPoint128.Q128
    );

    // Update snapshot
    rewardGrowthInsideLast[tokenId] = rewardGrowthInsideX128;

    if (reward > 0) {
        IERC20(rewardToken).safeTransfer(owner, reward);
        emit ClaimRewards(owner, reward);
    }
}
```

## Earned Calculation

```solidity
/// @notice Calculate pending rewards for a position
/// @param tokenId NFT token ID
/// @return reward Amount of rewards earned
function earned(uint256 tokenId) external view returns (uint256 reward) {
    if (stakedPositions[tokenId] == address(0)) return 0;

    (
        ,
        ,
        ,
        ,
        ,
        int24 tickLower,
        int24 tickUpper,
        uint128 liquidity,
        ,
        ,
        ,
    ) = nft.positions(tokenId);

    // Get reward growth inside range
    uint256 rewardGrowthInsideX128 = _getRewardGrowthInside(tickLower, tickUpper);

    // Include pending rewards not yet distributed
    uint256 _rewardGrowthGlobalX128 = pool.rewardGrowthGlobalX128();
    uint128 stakedLiquidity = pool.stakedLiquidity();

    if (stakedLiquidity > 0) {
        uint256 lastUpdated = pool.lastUpdated();
        uint256 timeDelta = _blockTimestamp() - lastUpdated;

        if (timeDelta > 0 && pool.rewardReserve() > 0) {
            uint256 reward = Math.min(pool.rewardRate() * timeDelta, pool.rewardReserve());
            _rewardGrowthGlobalX128 += FullMath.mulDiv(
                reward,
                FixedPoint128.Q128,
                stakedLiquidity
            );
        }
    }

    // Recalculate inside growth with updated global
    rewardGrowthInsideX128 = _getRewardGrowthInsideWithGlobal(
        tickLower,
        tickUpper,
        _rewardGrowthGlobalX128
    );

    reward = FullMath.mulDiv(
        rewardGrowthInsideX128 - rewardGrowthInsideLast[tokenId],
        liquidity,
        FixedPoint128.Q128
    );
}
```

## Reward Growth Inside Range

```solidity
/// @notice Get reward growth inside a tick range
function _getRewardGrowthInside(
    int24 tickLower,
    int24 tickUpper
) internal view returns (uint256) {
    return pool.getRewardGrowthInside(tickLower, tickUpper, pool.slot0().tick);
}

// In CLPool.sol
function getRewardGrowthInside(
    int24 tickLower,
    int24 tickUpper,
    int24 tickCurrent
) external view returns (uint256 rewardGrowthInsideX128) {
    Tick.Info storage lower = ticks[tickLower];
    Tick.Info storage upper = ticks[tickUpper];

    // Below lower tick
    uint256 rewardGrowthBelowX128;
    if (tickCurrent >= tickLower) {
        rewardGrowthBelowX128 = lower.rewardGrowthOutsideX128;
    } else {
        rewardGrowthBelowX128 = rewardGrowthGlobalX128 - lower.rewardGrowthOutsideX128;
    }

    // Above upper tick
    uint256 rewardGrowthAboveX128;
    if (tickCurrent < tickUpper) {
        rewardGrowthAboveX128 = upper.rewardGrowthOutsideX128;
    } else {
        rewardGrowthAboveX128 = rewardGrowthGlobalX128 - upper.rewardGrowthOutsideX128;
    }

    // Inside = global - below - above
    rewardGrowthInsideX128 = rewardGrowthGlobalX128 - rewardGrowthBelowX128 - rewardGrowthAboveX128;
}
```

## Notify Reward

```solidity
/// @notice Notify gauge of new reward deposit
/// @param amount Amount of reward tokens
function notifyRewardAmount(uint256 amount) external nonReentrant {
    require(msg.sender == voter, "NV");  // Not voter

    // Transfer rewards from voter
    IERC20(rewardToken).safeTransferFrom(msg.sender, address(pool), amount);

    // Update pool's reward state
    pool.syncReward(amount);

    emit NotifyReward(msg.sender, amount);
}

// In CLPool.sol
function syncReward(uint256 amount) external {
    require(msg.sender == gauge, "NG");

    _updateRewardsGrowthGlobal();

    if (block.timestamp >= periodFinish) {
        // New period - set new rate
        rewardRate = amount / WEEK;
    } else {
        // Add to existing period
        uint256 remaining = (periodFinish - block.timestamp) * rewardRate;
        rewardRate = (remaining + amount) / WEEK;
    }

    rewardReserve += amount;
    lastUpdated = block.timestamp;
    periodFinish = block.timestamp + WEEK;

    emit SyncReward(amount, rewardRate);
}
```

## Update Rewards Growth

```solidity
// CLPool.sol

function _updateRewardsGrowthGlobal() internal {
    if (stakedLiquidity == 0) {
        lastUpdated = block.timestamp;
        return;
    }

    uint256 timeDelta = block.timestamp - lastUpdated;
    if (timeDelta == 0) return;

    uint256 reward = Math.min(rewardRate * timeDelta, rewardReserve);

    if (reward > 0) {
        rewardGrowthGlobalX128 += FullMath.mulDiv(
            reward,
            FixedPoint128.Q128,
            stakedLiquidity
        );
        rewardReserve -= reward;
    }

    lastUpdated = block.timestamp;
}
```

## CLGaugeFactory

```solidity
// gauge/CLGaugeFactory.sol

contract CLGaugeFactory is ICLGaugeFactory {
    IVoter public voter;
    INonfungiblePositionManager public nft;

    /// @notice Create a gauge for a CL pool
    function createGauge(
        address pool,
        address rewardToken,
        address feesVotingReward,
        bool isPool
    ) external returns (address gauge) {
        require(msg.sender == address(voter), "NV");

        gauge = address(new CLGauge(pool, voter, nft, rewardToken, feesVotingReward));

        // Set gauge in pool
        ICLPool(pool).setGauge(gauge);

        emit GaugeCreated(pool, gauge, rewardToken);
    }
}
```

## Events

```solidity
event Deposit(address indexed owner, uint256 indexed tokenId, uint128 liquidity);
event Withdraw(address indexed owner, uint256 indexed tokenId, uint128 liquidity);
event ClaimRewards(address indexed owner, uint256 reward);
event ClaimFees(address indexed owner, uint256 claimed0, uint256 claimed1);
event NotifyReward(address indexed from, uint256 amount);
```

## Reference Files

- `contracts/gauge/CLGauge.sol` - Main gauge contract
- `contracts/gauge/CLGaugeFactory.sol` - Gauge factory
- `contracts/core/CLPool.sol` - Pool reward logic
- `contracts/core/libraries/Tick.sol` - Reward growth tracking
