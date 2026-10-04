---
name: Comet Rewards
description: This skill should be used when the user asks about "rewards", "COMP", "claim", "CometRewards", "baseTrackingAccrued", "trackingIndex", or needs to understand Comet's reward distribution system.
version: 0.1.0
---

# Comet Rewards

CometRewards is a separate contract that distributes COMP tokens to Comet suppliers and borrowers. Rewards accrue based on tracking indices stored in Comet.

## Overview

```
┌──────────────────────────────────────────────────────────────┐
│                    REWARDS SYSTEM                            │
├──────────────────────────────────────────────────────────────┤
│                                                              │
│  Comet Contract                    CometRewards Contract     │
│  ┌─────────────────────────────┐   ┌────────────────────────┐│
│  │                             │   │                        ││
│  │ trackingSupplyIndex ───────►│───│► Calculate rewards     ││
│  │ trackingBorrowIndex ───────►│   │                        ││
│  │                             │   │  claim(comet, user)    ││
│  │ userBasic[user]             │   │        │               ││
│  │   .baseTrackingAccrued ────►│───│────────┘               ││
│  │   .baseTrackingIndex        │   │                        ││
│  │                             │   │  COMP tokens ───► User ││
│  └─────────────────────────────┘   └────────────────────────┘│
│                                                              │
└──────────────────────────────────────────────────────────────┘
```

## Tracking Index Update (In Comet)

```solidity
// Comet.sol - Part of accrueInternal()
function accrueInternal() internal {
    uint40 now_ = getNowInternal();
    uint timeElapsed = uint256(now_ - lastAccrualTime);

    if (timeElapsed > 0) {
        // Update interest indices
        (baseSupplyIndex, baseBorrowIndex) = accruedInterestIndices(timeElapsed);

        // Update reward tracking indices
        if (totalSupplyBase >= baseMinForRewards) {
            trackingSupplyIndex += safe64(
                divBaseWei(baseTrackingSupplySpeed * timeElapsed, totalSupplyBase)
            );
        }

        if (totalBorrowBase >= baseMinForRewards) {
            trackingBorrowIndex += safe64(
                divBaseWei(baseTrackingBorrowSpeed * timeElapsed, totalBorrowBase)
            );
        }

        lastAccrualTime = now_;
    }
}
```

## User Tracking Update (In Comet)

```solidity
// Comet.sol - Called on any principal change
function updateBasePrincipal(address account, UserBasic memory basic, int104 principalNew) internal {
    int104 principal = basic.principal;
    basic.principal = principalNew;

    if (principal >= 0) {
        // User was supplying - accrue supply rewards
        uint indexDelta = uint256(trackingSupplyIndex - basic.baseTrackingIndex);
        basic.baseTrackingAccrued += safe64(
            uint104(principal) * indexDelta / trackingIndexScale / accrualDescaleFactor
        );
    } else {
        // User was borrowing - accrue borrow rewards
        uint indexDelta = uint256(trackingBorrowIndex - basic.baseTrackingIndex);
        basic.baseTrackingAccrued += safe64(
            uint104(-principal) * indexDelta / trackingIndexScale / accrualDescaleFactor
        );
    }

    // Update user's tracking index
    if (principalNew >= 0) {
        basic.baseTrackingIndex = trackingSupplyIndex;
    } else {
        basic.baseTrackingIndex = trackingBorrowIndex;
    }

    userBasic[account] = basic;
}
```

## CometRewards Contract

```solidity
// contracts/CometRewards.sol
contract CometRewards {
    struct RewardConfig {
        address token;           // Reward token (COMP)
        uint64 rescaleFactor;    // Scale conversion factor
        bool shouldUpscale;      // Direction of scaling
        uint256 multiplier;      // Reward multiplier
    }

    struct RewardOwed {
        address token;
        uint owed;
    }

    address public governor;

    // Reward config per Comet instance
    mapping(address => RewardConfig) public rewardConfig;

    // Claimed rewards per Comet and user
    mapping(address => mapping(address => uint)) public rewardsClaimed;

    uint256 internal constant FACTOR_SCALE = 1e18;
}
```

## Set Reward Configuration

```solidity
/// @notice Configure rewards for a Comet instance
/// @param comet The Comet contract address
/// @param token The reward token (COMP)
/// @param multiplier Multiplier for reward calculation
function setRewardConfigWithMultiplier(address comet, address token, uint256 multiplier) public {
    if (msg.sender != governor) revert NotPermitted(msg.sender);
    if (rewardConfig[comet].token != address(0)) revert AlreadyConfigured(comet);

    uint64 accrualScale = CometInterface(comet).baseAccrualScale();
    uint8 tokenDecimals = ERC20(token).decimals();
    uint64 tokenScale = safe64(10 ** tokenDecimals);

    // Determine scaling direction
    if (accrualScale > tokenScale) {
        rewardConfig[comet] = RewardConfig({
            token: token,
            rescaleFactor: accrualScale / tokenScale,
            shouldUpscale: false,
            multiplier: multiplier
        });
    } else {
        rewardConfig[comet] = RewardConfig({
            token: token,
            rescaleFactor: tokenScale / accrualScale,
            shouldUpscale: true,
            multiplier: multiplier
        });
    }
}

/// @notice Configure rewards with default multiplier (1x)
function setRewardConfig(address comet, address token) external {
    setRewardConfigWithMultiplier(comet, token, FACTOR_SCALE);
}
```

## Get Reward Owed

```solidity
/// @notice Calculate unclaimed rewards for an account
/// @param comet The Comet contract
/// @param account The account to check
function getRewardOwed(address comet, address account) external returns (RewardOwed memory) {
    RewardConfig memory config = rewardConfig[comet];
    if (config.token == address(0)) revert NotSupported(comet);

    // Trigger accrual in Comet
    CometInterface(comet).accrueAccount(account);

    // Calculate owed
    uint claimed = rewardsClaimed[comet][account];
    uint accrued = getRewardAccrued(comet, account, config);
    uint owed = accrued > claimed ? accrued - claimed : 0;

    return RewardOwed(config.token, owed);
}

/// @dev Get total accrued rewards
function getRewardAccrued(
    address comet,
    address account,
    RewardConfig memory config
) internal view returns (uint) {
    uint accrued = CometInterface(comet).baseTrackingAccrued(account);

    // Scale to token decimals
    if (config.shouldUpscale) {
        accrued *= config.rescaleFactor;
    } else {
        accrued /= config.rescaleFactor;
    }

    // Apply multiplier
    return accrued * config.multiplier / FACTOR_SCALE;
}
```

## Claim Rewards

```solidity
/// @notice Claim rewards to your own address
/// @param comet The Comet contract
/// @param src The account to claim for
/// @param shouldAccrue Whether to accrue interest first
function claim(address comet, address src, bool shouldAccrue) external {
    claimInternal(comet, src, src, shouldAccrue);
}

/// @notice Claim rewards to a different address
/// @param comet The Comet contract
/// @param src The account to claim for
/// @param to The recipient of rewards
function claimTo(address comet, address src, address to, bool shouldAccrue) external {
    // Must have permission to claim for src
    if (!CometInterface(comet).hasPermission(src, msg.sender)) revert NotPermitted(msg.sender);
    claimInternal(comet, src, to, shouldAccrue);
}

/// @dev Internal claim logic
function claimInternal(address comet, address src, address to, bool shouldAccrue) internal {
    RewardConfig memory config = rewardConfig[comet];
    if (config.token == address(0)) revert NotSupported(comet);

    if (shouldAccrue) {
        CometInterface(comet).accrueAccount(src);
    }

    uint claimed = rewardsClaimed[comet][src];
    uint accrued = getRewardAccrued(comet, src, config);

    if (accrued > claimed) {
        uint owed = accrued - claimed;
        rewardsClaimed[comet][src] = accrued;
        doTransferOut(config.token, to, owed);

        emit RewardClaimed(src, to, config.token, owed);
    }
}
```

## Governor Functions

```solidity
/// @notice Migrate existing claimed amounts (for upgrades)
function setRewardsClaimed(
    address comet,
    address[] calldata users,
    uint[] calldata claimedAmounts
) external {
    if (msg.sender != governor) revert NotPermitted(msg.sender);
    if (users.length != claimedAmounts.length) revert BadData();

    for (uint i = 0; i < users.length; ) {
        rewardsClaimed[comet][users[i]] = claimedAmounts[i];
        emit RewardsClaimedSet(users[i], comet, claimedAmounts[i]);
        unchecked { i++; }
    }
}

/// @notice Withdraw tokens from contract
function withdrawToken(address token, address to, uint amount) external {
    if (msg.sender != governor) revert NotPermitted(msg.sender);
    doTransferOut(token, to, amount);
}

/// @notice Transfer governor rights
function transferGovernor(address newGovernor) external {
    if (msg.sender != governor) revert NotPermitted(msg.sender);

    address oldGovernor = governor;
    governor = newGovernor;
    emit GovernorTransferred(oldGovernor, newGovernor);
}
```

## Reward Configuration Parameters

From Comet:

```solidity
// Reward tracking speeds (per second, scaled by trackingIndexScale)
uint64 public immutable baseTrackingSupplySpeed;   // Supply reward rate
uint64 public immutable baseTrackingBorrowSpeed;   // Borrow reward rate

// Minimum base for rewards (prevents division issues)
uint104 public immutable baseMinForRewards;

// Scale for tracking indices
uint64 public immutable trackingIndexScale;        // Usually 1e15

// From CometExt.sol
function baseTrackingAccrued(address account) external view returns (uint64) {
    return userBasic[account].baseTrackingAccrued;
}
```

## Reward Math

```
┌──────────────────────────────────────────────────────────────┐
│                  REWARD CALCULATION                          │
├──────────────────────────────────────────────────────────────┤
│                                                              │
│  Per-Second Index Update:                                    │
│  ─────────────────────────                                   │
│  trackingSupplyIndex += (supplySpeed × time) / totalSupply   │
│                                                              │
│  User Reward Accrual:                                        │
│  ────────────────────                                        │
│  indexDelta = currentIndex - userLastIndex                   │
│  rewards = principal × indexDelta / trackingIndexScale       │
│                                                              │
│  Example:                                                    │
│  - baseTrackingSupplySpeed = 1e15 per second                 │
│  - totalSupplyBase = 100_000e6 (100K USDC principal)         │
│  - timeElapsed = 1 day = 86400 seconds                       │
│  - User principal = 1000e6 (1K USDC)                         │
│                                                              │
│  indexDelta = (1e15 × 86400) / 100_000e6                     │
│             = 864e12 / 1e11                                  │
│             = 864e1 = 8640                                   │
│                                                              │
│  userReward = 1000e6 × 8640 / 1e15                           │
│             = 8.64e9 / 1e15                                  │
│             = 8.64e-6 COMP (scaled by accrualDescale)        │
│                                                              │
└──────────────────────────────────────────────────────────────┘
```

## Events

```solidity
event GovernorTransferred(address indexed oldGovernor, address indexed newGovernor);
event RewardsClaimedSet(address indexed user, address indexed comet, uint256 amount);
event RewardClaimed(address indexed src, address indexed recipient, address indexed token, uint256 amount);
```

## Usage Examples

```solidity
// Check pending rewards
CometRewards.RewardOwed memory owed = cometRewards.getRewardOwed(cometAddress, userAddress);
console.log("Pending COMP:", owed.owed);

// Claim rewards (triggers accrual)
cometRewards.claim(cometAddress, msg.sender, true);

// Claim to different address
cometRewards.claimTo(cometAddress, msg.sender, recipientAddress, true);

// Batch claim via Bulker
bytes32[] memory actions = new bytes32[](1);
bytes[] memory data = new bytes[](1);

actions[0] = bulker.ACTION_CLAIM_REWARD();
data[0] = abi.encode(cometAddress, rewardsAddress, msg.sender, true);

bulker.invoke(actions, data);
```

## Reference Files

- `contracts/CometRewards.sol` - Reward distribution contract
- `contracts/Comet.sol:419-431` - Tracking index updates
- `contracts/Comet.sol:761-780` - User tracking update
- `contracts/CometExt.sol:122-124` - baseTrackingAccrued getter
