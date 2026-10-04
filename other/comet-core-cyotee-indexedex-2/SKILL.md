---
name: Comet Core Operations
description: This skill should be used when the user asks about "supply", "withdraw", "borrow", "repay", "transfer", "supplyTo", "withdrawFrom", or needs to understand Comet's core user operations.
version: 0.1.0
---

# Comet Core Operations

Comet provides supply, withdraw, and transfer operations for both the base token (e.g., USDC) and collateral assets. A single principal value tracks supply/borrow positions.

## Overview

```
┌──────────────────────────────────────────────────────────────┐
│                   CORE OPERATIONS FLOW                       │
├──────────────────────────────────────────────────────────────┤
│                                                              │
│  Supply Base Token:                                          │
│  User ──► supply(amount) ──► Positive principal (earn yield) │
│                                                              │
│  Borrow Base Token:                                          │
│  User ──► withdraw(amount) ──► Negative principal (pay interest)│
│                                                              │
│  Supply Collateral:                                          │
│  User ──► supply(asset, amount) ──► Enable borrowing power   │
│                                                              │
│  The key insight: Supply and borrow of base token are        │
│  handled by a single signed principal value!                 │
│                                                              │
└──────────────────────────────────────────────────────────────┘
```

## Supply Operations

### Supply Base Token

```solidity
/// @notice Supply base token to your own account
function supply(address asset, uint amount) external {
    supplyInternal(msg.sender, msg.sender, msg.sender, asset, amount);
}

/// @notice Supply base token to another account
function supplyTo(address dst, address asset, uint amount) external {
    supplyInternal(msg.sender, msg.sender, dst, asset, amount);
}

/// @notice Supply from another account (requires permission)
function supplyFrom(address from, address dst, address asset, uint amount) external {
    supplyInternal(msg.sender, from, dst, asset, amount);
}
```

### Supply Base Internal Logic

```solidity
function supplyBase(address from, address dst, uint256 amount) internal {
    // Transfer tokens in (handles fee tokens correctly)
    amount = doTransferIn(baseToken, from, amount);

    // Accrue interest before modifying state
    accrueInternal();

    // Get current principal and calculate new balance
    UserBasic memory dstUser = userBasic[dst];
    int104 dstPrincipal = dstUser.principal;
    int256 dstBalance = presentValue(dstPrincipal) + signed256(amount);
    int104 dstPrincipalNew = principalValue(dstBalance);

    // Calculate repay vs supply amounts
    (uint104 repayAmount, uint104 supplyAmount) = repayAndSupplyAmount(
        dstPrincipal,
        dstPrincipalNew
    );

    // Update global totals
    totalSupplyBase += supplyAmount;
    totalBorrowBase -= repayAmount;  // Repaying reduces borrows

    // Update user principal and tracking
    updateBasePrincipal(dst, dstUser, dstPrincipalNew);

    emit Supply(from, dst, amount);
}
```

### Supply Collateral

```solidity
function supplyCollateral(address from, address dst, address asset, uint128 amount) internal {
    // Transfer collateral in
    amount = safe128(doTransferIn(asset, from, amount));

    // Get asset info and check supply cap
    AssetInfo memory assetInfo = getAssetInfoByAddress(asset);
    TotalsCollateral memory totals = totalsCollateral[asset];
    totals.totalSupplyAsset += amount;
    if (totals.totalSupplyAsset > assetInfo.supplyCap) revert SupplyCapExceeded();

    // Update user collateral balance
    uint128 dstCollateral = userCollateral[dst][asset].balance;
    uint128 dstCollateralNew = dstCollateral + amount;
    totalsCollateral[asset] = totals;
    userCollateral[dst][asset].balance = dstCollateralNew;

    // Update assetsIn bit vector
    updateAssetsIn(dst, assetInfo, dstCollateral, dstCollateralNew);

    emit SupplyCollateral(from, dst, asset, amount);
}
```

## Withdraw Operations

### Withdraw Base Token

```solidity
/// @notice Withdraw base token to your own account
function withdraw(address asset, uint amount) external {
    withdrawInternal(msg.sender, msg.sender, msg.sender, asset, amount);
}

/// @notice Withdraw base token to another account
function withdrawTo(address to, address asset, uint amount) external {
    withdrawInternal(msg.sender, msg.sender, to, asset, amount);
}

/// @notice Withdraw from another account (requires permission)
function withdrawFrom(address src, address to, address asset, uint amount) external {
    withdrawInternal(msg.sender, src, to, asset, amount);
}
```

### Withdraw Base Internal Logic

```solidity
function withdrawBase(address src, address to, uint256 amount) internal {
    accrueInternal();

    UserBasic memory srcUser = userBasic[src];
    int104 srcPrincipal = srcUser.principal;
    int256 srcBalance = presentValue(srcPrincipal) - signed256(amount);
    int104 srcPrincipalNew = principalValue(srcBalance);

    // Calculate withdraw vs borrow amounts
    (uint104 withdrawAmount, uint104 borrowAmount) = withdrawAndBorrowAmount(
        srcPrincipal,
        srcPrincipalNew
    );

    // Update global totals
    totalSupplyBase -= withdrawAmount;
    totalBorrowBase += borrowAmount;  // Borrowing increases borrows

    updateBasePrincipal(src, srcUser, srcPrincipalNew);

    // If user now has negative balance, check collateralization
    if (srcBalance < 0) {
        if (uint256(-srcBalance) < baseBorrowMin) revert BorrowTooSmall();
        if (!isBorrowCollateralized(src)) revert NotCollateralized();
    }

    // Transfer tokens out
    doTransferOut(baseToken, to, amount);

    emit Withdraw(src, to, amount);
}
```

### Withdraw Collateral

```solidity
function withdrawCollateral(address src, address to, address asset, uint128 amount) internal {
    uint128 srcCollateral = userCollateral[src][asset].balance;
    uint128 srcCollateralNew = srcCollateral - amount;

    // Update totals and user balance
    totalsCollateral[asset].totalSupplyAsset -= amount;
    userCollateral[src][asset].balance = srcCollateralNew;

    // Update assetsIn bit vector
    AssetInfo memory assetInfo = getAssetInfoByAddress(asset);
    updateAssetsIn(src, assetInfo, srcCollateral, srcCollateralNew);

    // Check collateralization (BorrowCF < LiquidationCF provides buffer)
    if (!isBorrowCollateralized(src)) revert NotCollateralized();

    doTransferOut(asset, to, amount);

    emit WithdrawCollateral(src, to, asset, amount);
}
```

## Transfer Operations

### Transfer Base Token (ERC20 Compatible)

```solidity
/// @notice ERC20-compatible transfer
function transfer(address dst, uint amount) external returns (bool) {
    transferInternal(msg.sender, msg.sender, dst, baseToken, amount);
    return true;
}

/// @notice ERC20-compatible transferFrom
function transferFrom(address src, address dst, uint amount) external returns (bool) {
    transferInternal(msg.sender, src, dst, baseToken, amount);
    return true;
}

/// @notice Transfer any asset
function transferAsset(address dst, address asset, uint amount) external {
    transferInternal(msg.sender, msg.sender, dst, asset, amount);
}

/// @notice Transfer any asset from another account
function transferAssetFrom(address src, address dst, address asset, uint amount) external {
    transferInternal(msg.sender, src, dst, asset, amount);
}
```

### Transfer Base Internal Logic

```solidity
function transferBase(address src, address dst, uint256 amount) internal {
    accrueInternal();

    UserBasic memory srcUser = userBasic[src];
    UserBasic memory dstUser = userBasic[dst];

    int104 srcPrincipal = srcUser.principal;
    int104 dstPrincipal = dstUser.principal;
    int256 srcBalance = presentValue(srcPrincipal) - signed256(amount);
    int256 dstBalance = presentValue(dstPrincipal) + signed256(amount);
    int104 srcPrincipalNew = principalValue(srcBalance);
    int104 dstPrincipalNew = principalValue(dstBalance);

    // Calculate all changes
    (uint104 withdrawAmount, uint104 borrowAmount) = withdrawAndBorrowAmount(srcPrincipal, srcPrincipalNew);
    (uint104 repayAmount, uint104 supplyAmount) = repayAndSupplyAmount(dstPrincipal, dstPrincipalNew);

    // Update totals (add before subtract to avoid underflow)
    totalSupplyBase = totalSupplyBase + supplyAmount - withdrawAmount;
    totalBorrowBase = totalBorrowBase + borrowAmount - repayAmount;

    updateBasePrincipal(src, srcUser, srcPrincipalNew);
    updateBasePrincipal(dst, dstUser, dstPrincipalNew);

    // Check source collateralization if borrowing
    if (srcBalance < 0) {
        if (uint256(-srcBalance) < baseBorrowMin) revert BorrowTooSmall();
        if (!isBorrowCollateralized(src)) revert NotCollateralized();
    }
}
```

## Helper Functions

### Repay and Supply Amount

```solidity
/// @dev Splits a principal increase into repay and supply components
function repayAndSupplyAmount(int104 oldPrincipal, int104 newPrincipal)
    internal pure returns (uint104, uint104)
{
    if (newPrincipal < oldPrincipal) return (0, 0);

    if (newPrincipal <= 0) {
        // Still in borrow, all goes to repay
        return (uint104(newPrincipal - oldPrincipal), 0);
    } else if (oldPrincipal >= 0) {
        // Was supplying, all goes to supply
        return (0, uint104(newPrincipal - oldPrincipal));
    } else {
        // Crossed from borrow to supply
        return (uint104(-oldPrincipal), uint104(newPrincipal));
    }
}
```

### Withdraw and Borrow Amount

```solidity
/// @dev Splits a principal decrease into withdraw and borrow components
function withdrawAndBorrowAmount(int104 oldPrincipal, int104 newPrincipal)
    internal pure returns (uint104, uint104)
{
    if (newPrincipal > oldPrincipal) return (0, 0);

    if (newPrincipal >= 0) {
        // Still in supply, all comes from withdraw
        return (uint104(oldPrincipal - newPrincipal), 0);
    } else if (oldPrincipal <= 0) {
        // Was borrowing, all comes from borrow
        return (0, uint104(oldPrincipal - newPrincipal));
    } else {
        // Crossed from supply to borrow
        return (uint104(oldPrincipal), uint104(-newPrincipal));
    }
}
```

### Safe Token Transfers

```solidity
/// @dev Transfer tokens in, handling fee tokens
function doTransferIn(address asset, address from, uint amount) internal returns (uint) {
    uint256 preTransferBalance = IERC20NonStandard(asset).balanceOf(address(this));
    IERC20NonStandard(asset).transferFrom(from, address(this), amount);
    // Handle non-standard ERC20 tokens
    bool success;
    assembly {
        switch returndatasize()
        case 0 { success := not(0) }
        case 32 { returndatacopy(0, 0, 32) success := mload(0) }
        default { revert(0, 0) }
    }
    if (!success) revert TransferInFailed();
    // Return actual amount received (handles fee tokens)
    return IERC20NonStandard(asset).balanceOf(address(this)) - preTransferBalance;
}

/// @dev Transfer tokens out
function doTransferOut(address asset, address to, uint amount) internal {
    IERC20NonStandard(asset).transfer(to, amount);
    // Similar non-standard handling...
}
```

## Max Value Handling

Special handling for `uint256.max`:

```solidity
// In supplyInternal
if (asset == baseToken) {
    if (amount == type(uint256).max) {
        amount = borrowBalanceOf(dst);  // Repay entire borrow
    }
}

// In withdrawInternal
if (asset == baseToken) {
    if (amount == type(uint256).max) {
        amount = balanceOf(src);  // Withdraw entire supply
    }
}
```

## Events

```solidity
event Supply(address indexed from, address indexed dst, uint256 amount);
event SupplyCollateral(address indexed from, address indexed dst, address indexed asset, uint128 amount);
event Withdraw(address indexed src, address indexed to, uint256 amount);
event WithdrawCollateral(address indexed src, address indexed to, address indexed asset, uint128 amount);
event Transfer(address indexed from, address indexed to, uint256 amount);
event TransferCollateral(address indexed from, address indexed to, address indexed asset, uint128 amount);
```

## Usage Examples

```solidity
// Supply USDC (base token)
comet.supply(usdcAddress, 1000e6);

// Supply to another account
comet.supplyTo(recipientAddress, usdcAddress, 500e6);

// Supply collateral (WETH)
comet.supply(wethAddress, 1e18);

// Borrow USDC (withdraw more than you have)
comet.withdraw(usdcAddress, 5000e6);  // Creates negative principal

// Repay borrow (supply reduces negative principal)
comet.supply(usdcAddress, 2000e6);

// Repay entire borrow
comet.supply(usdcAddress, type(uint256).max);

// Withdraw entire supply
comet.withdraw(usdcAddress, type(uint256).max);
```

## Reference Files

- `contracts/Comet.sol:835-1151` - Supply/withdraw implementations
- `contracts/Comet.sol:604-633` - repayAndSupplyAmount, withdrawAndBorrowAmount
- `contracts/Comet.sol:786-828` - doTransferIn, doTransferOut
