---
name: resupply-rewards
description: This skill should be used when the user asks about "rewards", "RewardHandler", "claim rewards", "RSUP emissions", "reward distribution", "multi-epoch rewards", "protocol emissions", or needs to understand Resupply's reward system.
---

# Resupply Reward System

The reward system distributes RSUP emissions and protocol fees across lending pairs, insurance pool, and stakers. Key contracts in `/src/protocol/RewardHandler.sol`, `/src/protocol/RewardDistributorMultiEpoch.sol`, and `/src/dao/emissions/EmissionsController.sol`.

## Reward Architecture Overview

```
                    ┌─────────────────────┐
                    │ EmissionsController │
                    │   (RSUP minting)    │
                    └─────────┬───────────┘
                              │
                    ┌─────────▼───────────┐
                    │    RewardHandler    │
                    │ (distribution hub)  │
                    └─────────┬───────────┘
                              │
        ┌─────────────────────┼─────────────────────┐
        │                     │                     │
        ▼                     ▼                     ▼
┌───────────────┐   ┌─────────────────┐   ┌─────────────────┐
│ Lending Pairs │   │ Insurance Pool  │   │   GovStaker     │
│  (borrowers)  │   │   (reIP holders)│   │ (RSUP stakers)  │
└───────────────┘   └─────────────────┘   └─────────────────┘
```

## RewardHandler Contract

Central hub for reward distribution (`/src/protocol/RewardHandler.sol`):

```solidity
contract RewardHandler {
    // Distribution weights (in basis points, 10000 = 100%)
    uint256 public pairWeight;        // e.g., 7000 (70%)
    uint256 public insuranceWeight;   // e.g., 1000 (10%)
    uint256 public stakerWeight;      // e.g., 2000 (20%)

    // Reward token tracking
    address[] public rewardTokens;

    // Distribution function
    function distributeRewards() external;
    function notifyReward(address token, uint256 amount) external;
}
```

### Distribution Flow

```solidity
function distributeRewards() external {
    for (uint256 i = 0; i < rewardTokens.length; i++) {
        address token = rewardTokens[i];
        uint256 balance = IERC20(token).balanceOf(address(this));

        if (balance > 0) {
            // Calculate splits
            uint256 toPairs = balance * pairWeight / 10000;
            uint256 toInsurance = balance * insuranceWeight / 10000;
            uint256 toStakers = balance - toPairs - toInsurance;

            // Distribute to pairs (proportional to debt)
            _distributeToPairs(token, toPairs);

            // Send to insurance pool
            _sendToInsurance(token, toInsurance);

            // Send to staker rewards
            _sendToStakers(token, toStakers);
        }
    }
}
```

## Multi-Epoch Reward Distribution

Base reward tracking (`/src/protocol/RewardDistributorMultiEpoch.sol`):

```solidity
contract RewardDistributorMultiEpoch {
    // Per-epoch reward accumulation
    mapping(address token => mapping(uint256 epoch => uint256 rewards)) public epochRewards;

    // Cumulative reward tracking
    mapping(address token => uint256) public rewardIntegral;
    mapping(address user => mapping(address token => uint256)) public userRewardIntegral;
    mapping(address user => mapping(address token => uint256)) public claimableRewards;

    // Checkpoint user rewards
    function _checkpoint(address _user) internal;

    // Calculate earned rewards
    function earned(address _user, address _token) public view returns (uint256);
}
```

### Reward Integral Math

```solidity
// When rewards are added:
function _notifyReward(address _token, uint256 _amount) internal {
    uint256 supply = totalSupply();
    if (supply > 0) {
        // Increase reward per token
        rewardIntegral[_token] += (_amount * 1e18) / supply;
    }
    epochRewards[_token][getEpoch()] += _amount;
}

// When user checkpoints:
function _checkpoint(address _user) internal {
    uint256 balance = balanceOf(_user);

    for (uint256 i = 0; i < rewardTokens.length; i++) {
        address token = rewardTokens[i];
        uint256 integral = rewardIntegral[token];
        uint256 userIntegral = userRewardIntegral[_user][token];

        // Calculate new rewards since last checkpoint
        uint256 newRewards = (balance * (integral - userIntegral)) / 1e18;
        claimableRewards[_user][token] += newRewards;
        userRewardIntegral[_user][token] = integral;
    }
}
```

## EmissionsController

Controls RSUP token emissions (`/src/dao/emissions/EmissionsController.sol`):

```solidity
contract EmissionsController {
    // Emission schedule (per year)
    uint256[] public yearlyEmissions;
    // Year 1: 50M RSUP
    // Year 2: 40M RSUP
    // Year 3: 30M RSUP
    // Year 4: 20M RSUP
    // Year 5+: 10M RSUP (tail emissions)

    uint256 public startTime;
    uint256 public lastMintTime;

    // Mint pending emissions
    function mint() external returns (uint256 minted);
}
```

### Emission Schedule

```solidity
function getEmissionRate() public view returns (uint256 perSecond) {
    uint256 year = (block.timestamp - startTime) / 365 days;
    uint256 yearlyAmount;

    if (year < yearlyEmissions.length) {
        yearlyAmount = yearlyEmissions[year];
    } else {
        yearlyAmount = tailEmissionRate;  // Perpetual tail
    }

    perSecond = yearlyAmount / 365 days;
}

function mint() external returns (uint256 minted) {
    uint256 elapsed = block.timestamp - lastMintTime;
    uint256 rate = getEmissionRate();

    minted = elapsed * rate;
    lastMintTime = block.timestamp;

    IGovToken(govToken).mint(rewardHandler, minted);
}
```

## Reward Sources

### 1. RSUP Emissions

Protocol inflation distributed to participants:

```
Total RSUP Supply: 1,000,000,000
Year 1 emissions: 50,000,000 (5%)
Year 2 emissions: 40,000,000 (4%)
...
Tail emissions: 10,000,000/year (1%)
```

### 2. Interest Fees

Fee split from borrower interest payments:

```solidity
// When interest accrues in pair:
function _accrue() internal {
    uint256 interest = calculateInterest();
    uint256 protocolFee = interest * protocolFeeRate / 1e18;

    // Send fee to reward handler
    IRewardHandler(rewardHandler).notifyReward(asset, protocolFee);
}
```

### 3. Redemption Fees

Fees from collateral redemptions:

```solidity
// In RedemptionHandler:
function _distributeFees(uint256 fee) internal {
    uint256 protocolShare = fee * protocolRedemptionFee / 1e18;
    IRewardHandler(rewardHandler).notifyReward(asset, protocolShare);
}
```

### 4. External Rewards (CRV, CVX)

From Convex integration:

```solidity
// Pairs with Convex integration receive:
// - CRV rewards
// - CVX rewards
// Distributed to pair depositors
```

## Claiming Rewards

### From Lending Pairs

```solidity
// Claim all rewards from a pair
IResupplyPair(pair).getReward(userAddress, forwardTo);
```

### From Insurance Pool

```solidity
// Claim insurance pool rewards
IInsurancePool(insurancePool).getReward(userAddress);
```

### From Staking

```solidity
// Claim staking rewards
IGovStaker(staker).getReward(userAddress);
```

### Multi-Claim Helper

```solidity
function claimAll(address _user) external {
    // Claim from all pairs
    address[] memory pairs = registry.getAllPairs();
    for (uint256 i = 0; i < pairs.length; i++) {
        IResupplyPair(pairs[i]).getReward(_user, _user);
    }

    // Claim from insurance
    insurancePool.getReward(_user);

    // Claim from staking
    staker.getReward(_user);
}
```

## Fee Distribution Split

Default distribution weights:

| Recipient | Weight | Description |
|-----------|--------|-------------|
| Borrowers (pairs) | 70% | Proportional to debt |
| Stakers | 20% | RSUP staking rewards |
| Insurance | 10% | reIP holder rewards |

## Events

```solidity
event RewardDistributed(
    address indexed token,
    uint256 toPairs,
    uint256 toInsurance,
    uint256 toStakers
);

event RewardClaimed(
    address indexed user,
    address indexed token,
    uint256 amount
);

event EmissionsMinted(
    uint256 amount,
    uint256 epoch
);
```

