---
name: Comet Bulker
description: This skill should be used when the user asks about "Bulker", "batch operations", "invoke", "native token", "wrap ETH", "multicall", or needs to understand Comet's batching functionality.
version: 0.1.0
---

# Comet Bulker

The Bulker contract allows users to batch multiple Comet operations in a single transaction, including wrapping/unwrapping native tokens (ETH) and claiming rewards.

## Overview

```
┌──────────────────────────────────────────────────────────────┐
│                      BULKER OPERATIONS                       │
├──────────────────────────────────────────────────────────────┤
│                                                              │
│  Bulker.invoke([actions], [data])                            │
│  ┌─────────────────────────────────────────────────────────┐ │
│  │                                                         │ │
│  │  ACTION_SUPPLY_ASSET ──► Supply ERC20 to Comet          │ │
│  │  ACTION_SUPPLY_NATIVE_TOKEN ──► Wrap ETH + Supply       │ │
│  │  ACTION_TRANSFER_ASSET ──► Transfer within Comet        │ │
│  │  ACTION_WITHDRAW_ASSET ──► Withdraw ERC20 from Comet    │ │
│  │  ACTION_WITHDRAW_NATIVE_TOKEN ──► Withdraw + Unwrap ETH │ │
│  │  ACTION_CLAIM_REWARD ──► Claim COMP rewards             │ │
│  │                                                         │ │
│  └─────────────────────────────────────────────────────────┘ │
│                                                              │
│  Key: User must first call comet.allow(bulker, true)         │
│                                                              │
└──────────────────────────────────────────────────────────────┘
```

## BaseBulker Contract

```solidity
// contracts/bulkers/BaseBulker.sol
contract BaseBulker {
    address public admin;
    address payable public immutable wrappedNativeToken;  // WETH

    // Action identifiers
    bytes32 public constant ACTION_SUPPLY_ASSET = "ACTION_SUPPLY_ASSET";
    bytes32 public constant ACTION_SUPPLY_NATIVE_TOKEN = "ACTION_SUPPLY_NATIVE_TOKEN";
    bytes32 public constant ACTION_TRANSFER_ASSET = "ACTION_TRANSFER_ASSET";
    bytes32 public constant ACTION_WITHDRAW_ASSET = "ACTION_WITHDRAW_ASSET";
    bytes32 public constant ACTION_WITHDRAW_NATIVE_TOKEN = "ACTION_WITHDRAW_NATIVE_TOKEN";
    bytes32 public constant ACTION_CLAIM_REWARD = "ACTION_CLAIM_REWARD";

    // Receive ETH from WETH unwrap
    receive() external payable {}
}
```

## Invoke Function

```solidity
/// @notice Execute a list of actions in order
/// @param actions List of action identifiers
/// @param data ABI-encoded parameters for each action
function invoke(bytes32[] calldata actions, bytes[] calldata data) external payable {
    if (actions.length != data.length) revert InvalidArgument();

    uint unusedNativeToken = msg.value;

    for (uint i = 0; i < actions.length; ) {
        bytes32 action = actions[i];

        if (action == ACTION_SUPPLY_ASSET) {
            (address comet, address to, address asset, uint amount) =
                abi.decode(data[i], (address, address, address, uint));
            supplyTo(comet, to, asset, amount);

        } else if (action == ACTION_SUPPLY_NATIVE_TOKEN) {
            (address comet, address to, uint amount) =
                abi.decode(data[i], (address, address, uint));
            uint256 nativeTokenUsed = supplyNativeTokenTo(comet, to, amount);
            unusedNativeToken -= nativeTokenUsed;

        } else if (action == ACTION_TRANSFER_ASSET) {
            (address comet, address to, address asset, uint amount) =
                abi.decode(data[i], (address, address, address, uint));
            transferTo(comet, to, asset, amount);

        } else if (action == ACTION_WITHDRAW_ASSET) {
            (address comet, address to, address asset, uint amount) =
                abi.decode(data[i], (address, address, address, uint));
            withdrawTo(comet, to, asset, amount);

        } else if (action == ACTION_WITHDRAW_NATIVE_TOKEN) {
            (address comet, address to, uint amount) =
                abi.decode(data[i], (address, address, uint));
            withdrawNativeTokenTo(comet, to, amount);

        } else if (action == ACTION_CLAIM_REWARD) {
            (address comet, address rewards, address src, bool shouldAccrue) =
                abi.decode(data[i], (address, address, address, bool));
            claimReward(comet, rewards, src, shouldAccrue);

        } else {
            handleAction(action, data[i]);  // For extension
        }

        unchecked { i++; }
    }

    // Refund unused ETH
    if (unusedNativeToken > 0) {
        (bool success, ) = msg.sender.call{ value: unusedNativeToken }("");
        if (!success) revert FailedToSendNativeToken();
    }
}
```

## Action Implementations

### Supply Asset

```solidity
/// @notice Supply an ERC20 asset to Comet
/// @dev Bulker must have permission to manage msg.sender's account
function supplyTo(address comet, address to, address asset, uint amount) internal {
    CometInterface(comet).supplyFrom(msg.sender, to, asset, amount);
}
```

### Supply Native Token (ETH)

```solidity
/// @notice Wrap ETH and supply to Comet
function supplyNativeTokenTo(address comet, address to, uint amount) internal returns (uint256) {
    uint256 supplyAmount = amount;

    // If base token is WETH and amount is max, repay full borrow
    if (wrappedNativeToken == CometInterface(comet).baseToken()) {
        if (amount == type(uint256).max) {
            supplyAmount = CometInterface(comet).borrowBalanceOf(msg.sender);
        }
    }

    // Wrap ETH to WETH
    IWETH9(wrappedNativeToken).deposit{ value: supplyAmount }();

    // Approve Comet to spend WETH
    IWETH9(wrappedNativeToken).approve(comet, supplyAmount);

    // Supply from Bulker to recipient
    CometInterface(comet).supplyFrom(address(this), to, wrappedNativeToken, supplyAmount);

    return supplyAmount;
}
```

### Transfer Asset

```solidity
/// @notice Transfer asset within Comet
function transferTo(address comet, address to, address asset, uint amount) internal {
    CometInterface(comet).transferAssetFrom(msg.sender, to, asset, amount);
}
```

### Withdraw Asset

```solidity
/// @notice Withdraw ERC20 from Comet
function withdrawTo(address comet, address to, address asset, uint amount) internal {
    CometInterface(comet).withdrawFrom(msg.sender, to, asset, amount);
}
```

### Withdraw Native Token (ETH)

```solidity
/// @notice Withdraw WETH and unwrap to ETH
function withdrawNativeTokenTo(address comet, address to, uint amount) internal {
    uint256 withdrawAmount = amount;

    // If base token is WETH and amount is max, withdraw full balance
    if (wrappedNativeToken == CometInterface(comet).baseToken()) {
        if (amount == type(uint256).max) {
            withdrawAmount = CometInterface(comet).balanceOf(msg.sender);
        }
    }

    // Withdraw WETH to Bulker
    CometInterface(comet).withdrawFrom(msg.sender, address(this), wrappedNativeToken, withdrawAmount);

    // Unwrap WETH to ETH
    IWETH9(wrappedNativeToken).withdraw(withdrawAmount);

    // Send ETH to recipient
    (bool success, ) = to.call{ value: withdrawAmount }("");
    if (!success) revert FailedToSendNativeToken();
}
```

### Claim Rewards

```solidity
/// @notice Claim COMP rewards
function claimReward(address comet, address rewards, address src, bool shouldAccrue) internal {
    IClaimable(rewards).claim(comet, src, shouldAccrue);
}

interface IClaimable {
    function claim(address comet, address src, bool shouldAccrue) external;
    function claimTo(address comet, address src, address to, bool shouldAccrue) external;
}
```

## MainnetBulker Extensions

Additional actions for mainnet-specific operations:

```solidity
// contracts/bulkers/MainnetBulker.sol
contract MainnetBulker is BaseBulker {
    bytes32 public constant ACTION_SUPPLY_STETH = "ACTION_SUPPLY_STETH";
    bytes32 public constant ACTION_WITHDRAW_STETH = "ACTION_WITHDRAW_STETH";

    function handleAction(bytes32 action, bytes calldata data) override internal {
        if (action == ACTION_SUPPLY_STETH) {
            (address comet, address to, uint amount) =
                abi.decode(data, (address, address, uint));
            supplyStEthTo(comet, to, amount);
        } else if (action == ACTION_WITHDRAW_STETH) {
            (address comet, address to, uint amount) =
                abi.decode(data, (address, address, uint));
            withdrawStEthTo(comet, to, amount);
        } else {
            revert UnhandledAction();
        }
    }

    // Wrap stETH to wstETH and supply
    function supplyStEthTo(address comet, address to, uint stEthAmount) internal;

    // Withdraw wstETH and unwrap to stETH
    function withdrawStEthTo(address comet, address to, uint wstEthAmount) internal;
}
```

## Admin Functions

```solidity
/// @notice Sweep accidental ERC20 transfers
function sweepToken(address recipient, address asset) external {
    if (msg.sender != admin) revert Unauthorized();

    uint256 balance = IERC20NonStandard(asset).balanceOf(address(this));
    doTransferOut(asset, recipient, balance);
}

/// @notice Sweep accidental ETH transfers
function sweepNativeToken(address recipient) external {
    if (msg.sender != admin) revert Unauthorized();

    uint256 balance = address(this).balance;
    (bool success, ) = recipient.call{ value: balance }("");
    if (!success) revert FailedToSendNativeToken();
}

/// @notice Transfer admin rights
function transferAdmin(address newAdmin) external {
    if (msg.sender != admin) revert Unauthorized();
    if (newAdmin == address(0)) revert InvalidAddress();

    address oldAdmin = admin;
    admin = newAdmin;
    emit AdminTransferred(oldAdmin, newAdmin);
}
```

## Usage Examples

### Batch Supply Collateral + Borrow

```solidity
// Step 1: Approve Bulker to manage your Comet account
comet.allow(bulkerAddress, true);

// Step 2: Approve tokens for Bulker
IERC20(weth).approve(bulkerAddress, wethAmount);

// Step 3: Batch operations
bytes32[] memory actions = new bytes32[](2);
bytes[] memory data = new bytes[](2);

// Supply WETH as collateral
actions[0] = bulker.ACTION_SUPPLY_ASSET();
data[0] = abi.encode(cometAddress, msg.sender, wethAddress, wethAmount);

// Withdraw USDC (borrow)
actions[1] = bulker.ACTION_WITHDRAW_ASSET();
data[1] = abi.encode(cometAddress, msg.sender, usdcAddress, borrowAmount);

bulker.invoke(actions, data);
```

### Supply ETH and Claim Rewards

```solidity
bytes32[] memory actions = new bytes32[](2);
bytes[] memory data = new bytes[](2);

// Supply ETH (wraps to WETH)
actions[0] = bulker.ACTION_SUPPLY_NATIVE_TOKEN();
data[0] = abi.encode(cometAddress, msg.sender, ethAmount);

// Claim COMP rewards
actions[1] = bulker.ACTION_CLAIM_REWARD();
data[1] = abi.encode(cometAddress, rewardsAddress, msg.sender, true);

bulker.invoke{ value: ethAmount }(actions, data);
```

### Repay All and Withdraw Collateral

```solidity
bytes32[] memory actions = new bytes32[](2);
bytes[] memory data = new bytes[](2);

// Repay full borrow balance
actions[0] = bulker.ACTION_SUPPLY_ASSET();
data[0] = abi.encode(cometAddress, msg.sender, usdcAddress, type(uint256).max);

// Withdraw all ETH collateral
actions[1] = bulker.ACTION_WITHDRAW_NATIVE_TOKEN();
data[1] = abi.encode(cometAddress, msg.sender, type(uint256).max);

bulker.invoke(actions, data);
```

## Events

```solidity
event AdminTransferred(address indexed oldAdmin, address indexed newAdmin);
```

## Reference Files

- `contracts/bulkers/BaseBulker.sol` - Base bulker implementation
- `contracts/bulkers/MainnetBulker.sol` - Mainnet-specific extensions
- `contracts/IWETH9.sol` - WETH interface
