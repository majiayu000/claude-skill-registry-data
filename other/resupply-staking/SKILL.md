---
name: resupply-staking
description: This skill should be used when the user asks about "staking RSUP", "GovStaker", "voting power", "cooldown period", "stake tokens", "unstake", "staking rewards", or needs to understand Resupply's governance staking system.
---

# Resupply Staking System

The staking system allows RSUP token holders to stake for voting power and rewards. Located in `/src/dao/staking/GovStaker.sol` with escrow functionality in `/src/dao/staking/GovStakerEscrow.sol`.

## GovStaker Contract

```solidity
contract GovStaker is MultiRewardsDistributor {
    // Staking state
    mapping(address => uint256) public balanceOf;      // Staked balance
    uint256 public totalSupply;                         // Total staked

    // Cooldown configuration
    uint256 public cooldownEpochs;                      // Default: 2 epochs

    // Cooldown tracking
    struct CooldownData {
        uint256 amount;
        uint256 epoch;      // Epoch when cooldown started
    }
    mapping(address => CooldownData) public cooldowns;

    // Voting weight tracking
    mapping(address => mapping(uint256 => uint256)) public epochWeights;
}
```

## Staking RSUP

Deposit RSUP tokens to receive voting power:

```solidity
function stake(uint256 _amount) external {
    require(_amount > 0, "Cannot stake 0");

    // Transfer RSUP from staker
    IERC20(govToken).safeTransferFrom(msg.sender, address(this), _amount);

    // Update balances
    balanceOf[msg.sender] += _amount;
    totalSupply += _amount;

    // Checkpoint for rewards
    _checkpoint(msg.sender);

    // Update voting weight for current epoch
    _updateWeight(msg.sender);

    emit Staked(msg.sender, _amount);
}
```

## Voting Power

Voting power is determined by staked balance:

```solidity
function getWeight(address _account) public view returns (uint256) {
    return balanceOf[_account];  // 1:1 with staked amount
}

function getWeightAt(address _account, uint256 _epoch) public view returns (uint256) {
    return epochWeights[_account][_epoch];
}

function getTotalWeight() public view returns (uint256) {
    return totalSupply;
}

function getTotalWeightAt(uint256 _epoch) public view returns (uint256) {
    return epochTotalWeights[_epoch];
}
```

### Epoch-Based Weight Tracking

Weights are checkpointed per epoch for governance:

```solidity
function _updateWeight(address _account) internal {
    uint256 currentEpoch = getEpoch();
    uint256 weight = balanceOf[_account];

    epochWeights[_account][currentEpoch] = weight;
    epochTotalWeights[currentEpoch] = totalSupply;
}
```

## Cooldown System

Unstaking requires a cooldown period (default 2 epochs):

### Initiating Cooldown

```solidity
function cooldown(address _account, uint256 _amount) external {
    require(msg.sender == _account || isApproved[_account][msg.sender], "Not authorized");
    require(balanceOf[_account] >= _amount, "Insufficient balance");

    // Record cooldown
    cooldowns[_account] = CooldownData({
        amount: cooldowns[_account].amount + _amount,
        epoch: getEpoch()
    });

    emit CooldownStarted(_account, _amount, getEpoch());
}
```

### Completing Unstake

```solidity
function unstake(address _receiver) external returns (uint256 amount) {
    CooldownData memory cd = cooldowns[msg.sender];
    require(cd.amount > 0, "No cooldown active");

    // Check cooldown elapsed
    uint256 currentEpoch = getEpoch();
    require(currentEpoch >= cd.epoch + cooldownEpochs, "Cooldown not complete");

    amount = cd.amount;

    // Clear cooldown
    delete cooldowns[msg.sender];

    // Update balances
    balanceOf[msg.sender] -= amount;
    totalSupply -= amount;

    // Checkpoint
    _checkpoint(msg.sender);
    _updateWeight(msg.sender);

    // Transfer RSUP
    IERC20(govToken).safeTransfer(_receiver, amount);

    emit Unstaked(msg.sender, _receiver, amount);
}
```

### Cooldown Timing

```
Epoch 0: Stake 1000 RSUP
Epoch 5: Initiate cooldown
Epoch 7+: Can unstake (after 2 epoch cooldown)
```

## Staking Rewards

Stakers earn multiple reward tokens:

### Reward Sources

1. **RSUP emissions**: Governance token inflation
2. **Protocol fees**: Share of interest/redemption fees
3. **Partner rewards**: CRV, CVX from Convex integration

### Multi-Reward Distribution

```solidity
contract MultiRewardsDistributor {
    address[] public rewardTokens;
    mapping(address => RewardData) public rewardData;

    struct RewardData {
        uint256 rewardRate;         // Rewards per second
        uint256 rewardPerTokenStored;
        uint256 lastUpdateTime;
        uint256 periodFinish;
    }

    mapping(address => mapping(address => uint256)) public userRewardPerTokenPaid;
    mapping(address => mapping(address => uint256)) public rewards;
}
```

### Claiming Rewards

```solidity
function getReward(address _account) external {
    _checkpoint(_account);

    for (uint256 i = 0; i < rewardTokens.length; i++) {
        address token = rewardTokens[i];
        uint256 reward = rewards[_account][token];

        if (reward > 0) {
            rewards[_account][token] = 0;
            IERC20(token).safeTransfer(_account, reward);
            emit RewardPaid(_account, token, reward);
        }
    }
}
```

### Reward Calculation

```solidity
function earned(address _account, address _rewardToken) public view returns (uint256) {
    uint256 balance = balanceOf[_account];
    uint256 rewardPerToken = rewardPerTokenStored[_rewardToken];
    uint256 userPaid = userRewardPerTokenPaid[_account][_rewardToken];

    return (balance * (rewardPerToken - userPaid) / 1e18) + rewards[_account][_rewardToken];
}
```

## GovStakerEscrow

For locked staking positions (`/src/dao/staking/GovStakerEscrow.sol`):

```solidity
contract GovStakerEscrow {
    struct LockData {
        uint256 amount;
        uint256 unlockTime;
    }
    mapping(address => LockData[]) public locks;

    // Create locked stake
    function stakeLocked(uint256 _amount, uint256 _duration) external;

    // Unlock when duration passed
    function unlock(uint256 _lockIndex) external;
}
```

## PermaStaker

Permanent staking for protocol/foundation (`/src/dao/tge/PermaStaker.sol`):

```solidity
contract PermaStaker {
    // Permanently staked - no unstaking allowed
    // Still earns rewards and has voting power

    function stake(uint256 _amount) external;
    function getReward() external;
    // No unstake function
}
```

## Key Parameters

| Parameter | Default | Description |
|-----------|---------|-------------|
| `cooldownEpochs` | 2 | Epochs before unstake |
| Epoch length | 1 week | Time per epoch |
| Weight ratio | 1:1 | Voting power per RSUP |

## Events

```solidity
event Staked(address indexed user, uint256 amount);
event CooldownStarted(address indexed user, uint256 amount, uint256 epoch);
event Unstaked(address indexed user, address indexed receiver, uint256 amount);
event RewardPaid(address indexed user, address indexed token, uint256 amount);
```

