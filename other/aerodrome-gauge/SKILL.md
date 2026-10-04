---
name: Aerodrome Gauge
description: This skill should be used when the user asks about "gauge", "staking", "LP staking", "deposit", "emissions", "getReward", or needs to understand Aerodrome's gauge mechanics.
version: 0.1.0
---

# Aerodrome Gauge

Gauges distribute AERO emissions to liquidity providers who stake their LP tokens. LPs forgo their trading fee claims in exchange for proportional AERO emissions.

## Overview

```
┌──────────────────────────────────────────────────────────────┐
│                      GAUGE FLOW                              │
├──────────────────────────────────────────────────────────────┤
│                                                              │
│  ┌─────────────┐                      ┌─────────────┐        │
│  │     LP      │    Stake LP Tokens   │             │        │
│  │   Provider  │─────────────────────►│    Gauge    │        │
│  └─────────────┘                      └──────┬──────┘        │
│        ▲                                     │               │
│        │                                     ▼               │
│        │      Claim AERO            ┌─────────────────┐      │
│        └────────────────────────────│  AERO Rewards   │      │
│                                     └─────────────────┘      │
│                                              ▲               │
│                                              │               │
│                                     ┌─────────────────┐      │
│                                     │     Voter       │      │
│                                     │  (Emissions)    │      │
│                                     └─────────────────┘      │
│                                                              │
│  Trading Fees ──────────────────────► FeesVotingReward       │
│                                       (For veNFT voters)     │
│                                                              │
└──────────────────────────────────────────────────────────────┘
```

## Gauge Contract

```solidity
contract Gauge is IGauge, ERC2771Context, ReentrancyGuard {
    address public immutable stakingToken;    // LP token
    address public immutable rewardToken;     // AERO
    address public immutable feesVotingReward;// Fee reward contract
    address public immutable voter;
    address public immutable ve;
    bool public immutable isPool;             // Is this for a pool?

    uint256 internal constant DURATION = 7 days;
    uint256 internal constant PRECISION = 10 ** 18;

    uint256 public periodFinish;
    uint256 public rewardRate;
    uint256 public lastUpdateTime;
    uint256 public rewardPerTokenStored;
    uint256 public totalSupply;

    mapping(address => uint256) public balanceOf;
    mapping(address => uint256) public userRewardPerTokenPaid;
    mapping(address => uint256) public rewards;
    mapping(uint256 => uint256) public rewardRateByEpoch;

    uint256 public fees0;  // Accumulated token0 fees
    uint256 public fees1;  // Accumulated token1 fees
}
```

## Staking Operations

### Deposit LP Tokens

```solidity
/// @notice Stake LP tokens
function deposit(uint256 _amount) external {
    _depositFor(_amount, _msgSender());
}

/// @notice Stake LP tokens for another address
function deposit(uint256 _amount, address _recipient) external {
    _depositFor(_amount, _recipient);
}

function _depositFor(uint256 _amount, address _recipient) internal nonReentrant {
    if (_amount == 0) revert ZeroAmount();
    if (!IVoter(voter).isAlive(address(this))) revert NotAlive();

    address sender = _msgSender();
    _updateRewards(_recipient);

    IERC20(stakingToken).safeTransferFrom(sender, address(this), _amount);
    totalSupply += _amount;
    balanceOf[_recipient] += _amount;

    emit Deposit(sender, _recipient, _amount);
}
```

### Withdraw LP Tokens

```solidity
/// @notice Withdraw staked LP tokens
function withdraw(uint256 _amount) external nonReentrant {
    address sender = _msgSender();

    _updateRewards(sender);

    totalSupply -= _amount;
    balanceOf[sender] -= _amount;
    IERC20(stakingToken).safeTransfer(sender, _amount);

    emit Withdraw(sender, _amount);
}
```

## Reward Mechanics

### Reward Per Token

```solidity
/// @notice Get reward per token stored
function rewardPerToken() public view returns (uint256) {
    if (totalSupply == 0) {
        return rewardPerTokenStored;
    }
    return rewardPerTokenStored +
        ((lastTimeRewardApplicable() - lastUpdateTime) * rewardRate * PRECISION) / totalSupply;
}

/// @notice Get last time rewards are applicable
function lastTimeRewardApplicable() public view returns (uint256) {
    return Math.min(block.timestamp, periodFinish);
}
```

### Calculate Earned Rewards

```solidity
/// @notice Calculate earned but unclaimed rewards
function earned(address _account) public view returns (uint256) {
    return (balanceOf[_account] * (rewardPerToken() - userRewardPerTokenPaid[_account])) / PRECISION
        + rewards[_account];
}
```

### Claim Rewards

```solidity
/// @notice Claim AERO rewards
function getReward(address _account) external nonReentrant {
    address sender = _msgSender();
    if (sender != _account && sender != voter) revert NotAuthorized();

    _updateRewards(_account);

    uint256 reward = rewards[_account];
    if (reward > 0) {
        rewards[_account] = 0;
        IERC20(rewardToken).safeTransfer(_account, reward);
        emit ClaimRewards(_account, reward);
    }
}
```

### Update Rewards State

```solidity
function _updateRewards(address _account) internal {
    rewardPerTokenStored = rewardPerToken();
    lastUpdateTime = lastTimeRewardApplicable();
    rewards[_account] = earned(_account);
    userRewardPerTokenPaid[_account] = rewardPerTokenStored;
}
```

## Emission Notification

### From Voter

```solidity
/// @notice Receive emissions from Voter
function notifyRewardAmount(uint256 _amount) external nonReentrant {
    address sender = _msgSender();
    if (sender != voter) revert NotVoter();
    if (_amount == 0) revert ZeroAmount();

    _claimFees();  // Claim trading fees first
    _notifyRewardAmount(sender, _amount);
}
```

### From Team (Without Fee Claim)

```solidity
/// @notice Receive rewards without claiming fees (team only)
function notifyRewardWithoutClaim(uint256 _amount) external nonReentrant {
    address sender = _msgSender();
    if (sender != IVotingEscrow(ve).team()) revert NotTeam();
    if (_amount == 0) revert ZeroAmount();

    _notifyRewardAmount(sender, _amount);
}
```

### Internal Reward Notification

```solidity
function _notifyRewardAmount(address sender, uint256 _amount) internal {
    rewardPerTokenStored = rewardPerToken();
    uint256 timestamp = block.timestamp;
    uint256 timeUntilNext = ProtocolTimeLibrary.epochNext(timestamp) - timestamp;

    if (timestamp >= periodFinish) {
        // New period
        IERC20(rewardToken).safeTransferFrom(sender, address(this), _amount);
        rewardRate = _amount / timeUntilNext;
    } else {
        // Add to existing period
        uint256 _remaining = periodFinish - timestamp;
        uint256 _leftover = _remaining * rewardRate;
        IERC20(rewardToken).safeTransferFrom(sender, address(this), _amount);
        rewardRate = (_amount + _leftover) / timeUntilNext;
    }

    rewardRateByEpoch[ProtocolTimeLibrary.epochStart(timestamp)] = rewardRate;
    if (rewardRate == 0) revert ZeroRewardRate();

    // Sanity check
    uint256 balance = IERC20(rewardToken).balanceOf(address(this));
    if (rewardRate > balance / timeUntilNext) revert RewardRateTooHigh();

    lastUpdateTime = timestamp;
    periodFinish = timestamp + timeUntilNext;

    emit NotifyReward(sender, _amount);
}
```

## Fee Collection and Distribution

When LP tokens are staked in a gauge, trading fees go to veNFT voters instead of LPs:

```solidity
function _claimFees() internal returns (uint256 claimed0, uint256 claimed1) {
    if (!isPool) {
        return (0, 0);
    }

    // Claim fees from the pool
    (claimed0, claimed1) = IPool(stakingToken).claimFees();

    if (claimed0 > 0 || claimed1 > 0) {
        uint256 _fees0 = fees0 + claimed0;
        uint256 _fees1 = fees1 + claimed1;
        (address _token0, address _token1) = IPool(stakingToken).tokens();

        // Distribute to FeesVotingReward if above threshold
        if (_fees0 > DURATION) {
            fees0 = 0;
            IERC20(_token0).safeApprove(feesVotingReward, _fees0);
            IReward(feesVotingReward).notifyRewardAmount(_token0, _fees0);
        } else {
            fees0 = _fees0;
        }

        if (_fees1 > DURATION) {
            fees1 = 0;
            IERC20(_token1).safeApprove(feesVotingReward, _fees1);
            IReward(feesVotingReward).notifyRewardAmount(_token1, _fees1);
        } else {
            fees1 = _fees1;
        }

        emit ClaimFees(_msgSender(), claimed0, claimed1);
    }
}
```

## View Functions

```solidity
/// @notice Get remaining rewards in current period
function left() external view returns (uint256) {
    if (block.timestamp >= periodFinish) return 0;
    uint256 _remaining = periodFinish - block.timestamp;
    return _remaining * rewardRate;
}
```

## Emission Distribution Flow

```
┌──────────────────────────────────────────────────────────────┐
│                 EMISSION DISTRIBUTION                        │
├──────────────────────────────────────────────────────────────┤
│                                                              │
│  1. Minter.updatePeriod()                                    │
│     └──► Mints weekly AERO                                   │
│          └──► Sends to Voter.notifyRewardAmount()            │
│                                                              │
│  2. Voter updates index                                      │
│     └──► index += (amount * 1e18) / totalWeight              │
│                                                              │
│  3. Voter.distribute(gauges)                                 │
│     └──► For each gauge:                                     │
│         └──► _updateFor(gauge)                               │
│             └──► claimable[gauge] += share based on weight   │
│         └──► gauge.notifyRewardAmount(claimable)             │
│                                                              │
│  4. Gauge distributes over epoch                             │
│     └──► rewardRate = amount / timeUntilNextEpoch            │
│     └──► LPs earn proportionally to their stake              │
│                                                              │
│  5. LPs claim via getReward()                                │
│     └──► reward = balanceOf * (rewardPerToken - paid) / 1e18 │
│                                                              │
└──────────────────────────────────────────────────────────────┘
```

## Events

```solidity
event Deposit(address indexed from, address indexed to, uint256 amount);
event Withdraw(address indexed from, uint256 amount);
event NotifyReward(address indexed from, uint256 amount);
event ClaimFees(address indexed from, uint256 claimed0, uint256 claimed1);
event ClaimRewards(address indexed from, uint256 amount);
```

## Usage Example

```solidity
// 1. Get LP tokens from pool
router.addLiquidity(tokenA, tokenB, stable, amountA, amountB, minA, minB, user, deadline);

// 2. Approve gauge
IERC20(pool).approve(gauge, lpAmount);

// 3. Stake in gauge
IGauge(gauge).deposit(lpAmount);

// 4. Wait for emissions...

// 5. Check earned rewards
uint256 pending = IGauge(gauge).earned(user);

// 6. Claim rewards
IGauge(gauge).getReward(user);

// 7. Withdraw LP tokens
IGauge(gauge).withdraw(lpAmount);
```

## Reference Files

- `contracts/gauges/Gauge.sol` - Gauge implementation
- `contracts/interfaces/IGauge.sol` - Gauge interface
- `contracts/Voter.sol` - Emission distribution
