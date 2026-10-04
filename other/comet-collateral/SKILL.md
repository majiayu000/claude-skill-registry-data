---
name: Comet Collateral
description: This skill should be used when the user asks about "collateral", "collateral factor", "borrowCollateralFactor", "liquidateCollateralFactor", "assetsIn", "supplyCap", or needs to understand Comet's collateral system.
version: 0.1.0
---

# Comet Collateral System

Comet supports up to 12 collateral assets per market. Each collateral has its own price feed, collateral factors, and supply cap. Users must supply collateral to borrow the base token.

## Overview

```
┌──────────────────────────────────────────────────────────────┐
│                   COLLATERAL SYSTEM                          │
├──────────────────────────────────────────────────────────────┤
│                                                              │
│  User Collateral Flow:                                       │
│  ┌─────────────────────────────────────────────────────────┐ │
│  │                                                         │ │
│  │  Supply Collateral ──► assetsIn bit set ──► Borrow Power│ │
│  │                                                         │ │
│  │  Collateral Value × BorrowCF = Max Borrow Amount       │ │
│  │                                                         │ │
│  │  Collateral Value × LiquidateCF = Liquidation Threshold│ │
│  │                                                         │ │
│  └─────────────────────────────────────────────────────────┘ │
│                                                              │
│  Key Insight: BorrowCF < LiquidateCF provides safety buffer  │
│                                                              │
└──────────────────────────────────────────────────────────────┘
```

## Asset Configuration

```solidity
// CometConfiguration.sol
struct AssetConfig {
    address asset;                      // Collateral token address
    address priceFeed;                  // Chainlink price feed
    uint8 decimals;                     // Token decimals
    uint64 borrowCollateralFactor;      // CF for borrowing (e.g., 82.5%)
    uint64 liquidateCollateralFactor;   // CF for liquidation (e.g., 85%)
    uint64 liquidationFactor;           // Value recovered at liquidation
    uint128 supplyCap;                  // Maximum supply allowed
}

// AssetInfo returned by getAssetInfo()
struct AssetInfo {
    uint8 offset;                       // Index in asset array (0-11)
    address asset;
    address priceFeed;
    uint64 scale;                       // 10 ** decimals
    uint64 borrowCollateralFactor;
    uint64 liquidateCollateralFactor;
    uint64 liquidationFactor;
    uint128 supplyCap;
}
```

## Packed Asset Storage

Assets are stored packed in immutable slots for gas efficiency:

```solidity
contract Comet {
    // Each asset uses 2 uint256 slots
    uint256 internal immutable asset00_a;  // asset + borrowCF + liquidateCF + liquidationFactor
    uint256 internal immutable asset00_b;  // priceFeed + decimals + supplyCap

    uint256 internal immutable asset01_a;
    uint256 internal immutable asset01_b;
    // ... up to asset11_a, asset11_b (12 assets max)

    uint8 public immutable numAssets;

    function getAssetInfo(uint8 i) public view returns (AssetInfo memory) {
        if (i >= numAssets) revert BadAsset();

        uint256 word_a;
        uint256 word_b;

        if (i == 0) {
            word_a = asset00_a;
            word_b = asset00_b;
        } else if (i == 1) {
            word_a = asset01_a;
            word_b = asset01_b;
        }
        // ... etc

        // Unpack values
        address asset = address(uint160(word_a & type(uint160).max));
        uint64 borrowCollateralFactor = uint64(((word_a >> 160) & type(uint16).max) * rescale);
        uint64 liquidateCollateralFactor = uint64(((word_a >> 176) & type(uint16).max) * rescale);
        uint64 liquidationFactor = uint64(((word_a >> 192) & type(uint16).max) * rescale);

        address priceFeed = address(uint160(word_b & type(uint160).max));
        uint8 decimals_ = uint8(((word_b >> 160) & type(uint8).max));
        uint128 supplyCap = uint128(((word_b >> 168) & type(uint64).max) * scale);

        return AssetInfo({...});
    }
}
```

## AssetsIn Bit Vector

A `uint16` tracks which collateral assets a user has supplied:

```solidity
struct UserBasic {
    int104 principal;
    uint64 baseTrackingIndex;
    uint64 baseTrackingAccrued;
    uint16 assetsIn;        // Bit vector: bit 0 = asset 0, bit 1 = asset 1, etc.
    uint8 _reserved;
}

/// @dev Check if user has asset at offset
function isInAsset(uint16 assetsIn, uint8 assetOffset) internal pure returns (bool) {
    return (assetsIn & (uint16(1) << assetOffset) != 0);
}

/// @dev Update assetsIn when user enters or exits an asset
function updateAssetsIn(
    address account,
    AssetInfo memory assetInfo,
    uint128 initialUserBalance,
    uint128 finalUserBalance
) internal {
    if (initialUserBalance == 0 && finalUserBalance != 0) {
        // User entered this asset
        userBasic[account].assetsIn |= (uint16(1) << assetInfo.offset);
    } else if (initialUserBalance != 0 && finalUserBalance == 0) {
        // User exited this asset
        userBasic[account].assetsIn &= ~(uint16(1) << assetInfo.offset);
    }
}
```

## Collateral Storage

```solidity
struct UserCollateral {
    uint128 balance;
    uint128 _reserved;
}

struct TotalsCollateral {
    uint128 totalSupplyAsset;
    uint128 _reserved;
}

// User collateral balance by asset
mapping(address => mapping(address => UserCollateral)) public userCollateral;

// Total collateral by asset
mapping(address => TotalsCollateral) public totalsCollateral;
```

## Collateralization Checks

### Borrow Collateralization

Uses `borrowCollateralFactor` to check if account can borrow:

```solidity
/// @notice Check if account can borrow (has enough collateral)
function isBorrowCollateralized(address account) public view returns (bool) {
    int104 principal = userBasic[account].principal;

    // If not borrowing, always collateralized
    if (principal >= 0) {
        return true;
    }

    uint16 assetsIn = userBasic[account].assetsIn;

    // Start with negative borrow value
    int liquidity = signedMulPrice(
        presentValue(principal),          // Negative
        getPrice(baseTokenPriceFeed),
        uint64(baseScale)
    );

    // Add collateral value × borrowCollateralFactor
    for (uint8 i = 0; i < numAssets; ) {
        if (isInAsset(assetsIn, i)) {
            if (liquidity >= 0) {
                return true;  // Early exit
            }

            AssetInfo memory asset = getAssetInfo(i);
            uint newAmount = mulPrice(
                userCollateral[account][asset.asset].balance,
                getPrice(asset.priceFeed),
                asset.scale
            );
            liquidity += signed256(mulFactor(
                newAmount,
                asset.borrowCollateralFactor  // e.g., 82.5%
            ));
        }
        unchecked { i++; }
    }

    return liquidity >= 0;
}
```

### Liquidation Check

Uses `liquidateCollateralFactor` to determine if account is liquidatable:

```solidity
/// @notice Check if account can be liquidated
function isLiquidatable(address account) public view returns (bool) {
    int104 principal = userBasic[account].principal;

    // If not borrowing, not liquidatable
    if (principal >= 0) {
        return false;
    }

    uint16 assetsIn = userBasic[account].assetsIn;

    int liquidity = signedMulPrice(
        presentValue(principal),
        getPrice(baseTokenPriceFeed),
        uint64(baseScale)
    );

    for (uint8 i = 0; i < numAssets; ) {
        if (isInAsset(assetsIn, i)) {
            if (liquidity >= 0) {
                return false;  // Early exit
            }

            AssetInfo memory asset = getAssetInfo(i);
            uint newAmount = mulPrice(
                userCollateral[account][asset.asset].balance,
                getPrice(asset.priceFeed),
                asset.scale
            );
            liquidity += signed256(mulFactor(
                newAmount,
                asset.liquidateCollateralFactor  // e.g., 85%
            ));
        }
        unchecked { i++; }
    }

    return liquidity < 0;  // Liquidatable if still negative
}
```

## Collateral Factors Explained

```
┌──────────────────────────────────────────────────────────────┐
│             COLLATERAL FACTOR RELATIONSHIP                   │
├──────────────────────────────────────────────────────────────┤
│                                                              │
│  borrowCollateralFactor (82.5%)                              │
│  ─────────────────────────                                   │
│  Maximum borrow power from collateral                        │
│  $1000 collateral → Can borrow up to $825                    │
│                                                              │
│  liquidateCollateralFactor (85%)                             │
│  ─────────────────────────────                               │
│  Threshold for liquidation                                   │
│  $1000 collateral → Liquidated when debt exceeds $850        │
│                                                              │
│  Safety Buffer = liquidateCF - borrowCF = 2.5%               │
│  ────────────────────────────────────────                    │
│  Prevents immediate liquidation after borrowing at max       │
│                                                              │
│  liquidationFactor (93%)                                     │
│  ────────────────────                                        │
│  Amount of collateral value applied to reduce debt           │
│  $1000 collateral absorbed → $930 debt reduction             │
│  Protocol keeps 7% as fee                                    │
│                                                              │
└──────────────────────────────────────────────────────────────┘
```

## Supply Cap Enforcement

```solidity
function supplyCollateral(address from, address dst, address asset, uint128 amount) internal {
    amount = safe128(doTransferIn(asset, from, amount));

    AssetInfo memory assetInfo = getAssetInfoByAddress(asset);
    TotalsCollateral memory totals = totalsCollateral[asset];
    totals.totalSupplyAsset += amount;

    // Check supply cap
    if (totals.totalSupplyAsset > assetInfo.supplyCap) revert SupplyCapExceeded();

    uint128 dstCollateral = userCollateral[dst][asset].balance;
    uint128 dstCollateralNew = dstCollateral + amount;

    totalsCollateral[asset] = totals;
    userCollateral[dst][asset].balance = dstCollateralNew;

    updateAssetsIn(dst, assetInfo, dstCollateral, dstCollateralNew);

    emit SupplyCollateral(from, dst, asset, amount);
}
```

## Collateral Reserves

Protocol can accumulate collateral reserves from liquidations:

```solidity
/// @notice Get protocol's collateral reserves for an asset
function getCollateralReserves(address asset) public view returns (uint) {
    // Protocol reserves = balance - user deposits
    return IERC20NonStandard(asset).balanceOf(address(this)) -
           totalsCollateral[asset].totalSupplyAsset;
}
```

## View Functions

```solidity
// From CometExt.sol
function collateralBalanceOf(address account, address asset) external view returns (uint128) {
    return userCollateral[account][asset].balance;
}

// Get asset info by index
function getAssetInfo(uint8 i) public view returns (AssetInfo memory);

// Get asset info by address
function getAssetInfoByAddress(address asset) public view returns (AssetInfo memory) {
    for (uint8 i = 0; i < numAssets; ) {
        AssetInfo memory assetInfo = getAssetInfo(i);
        if (assetInfo.asset == asset) {
            return assetInfo;
        }
        unchecked { i++; }
    }
    revert BadAsset();
}
```

## Price Calculations

```solidity
/// @dev Multiply quantity by price, returning common price scale
function mulPrice(uint n, uint price, uint64 fromScale) internal pure returns (uint) {
    return n * price / fromScale;
}

/// @dev Divide common price by asset price, returning asset scale
function divPrice(uint n, uint price, uint64 toScale) internal pure returns (uint) {
    return n * toScale / price;
}

// All prices are in 8 decimals (PRICE_FEED_DECIMALS = 8)
// Example: ETH at $2000 = 2000e8 = 200000000000
```

## Reference Files

- `contracts/Comet.sol:253-390` - Asset info packing/unpacking
- `contracts/Comet.sol:524-601` - Collateralization checks
- `contracts/Comet.sol:905-925` - Supply collateral
- `contracts/CometConfiguration.sol` - AssetConfig struct
- `contracts/CometStorage.sol` - Collateral storage
