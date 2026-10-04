---
name: Aave V4 Hub
description: This skill should be used when the user asks about "Hub contract", "Hub.sol", "liquidity hub", "add liquidity", "draw liquidity", "restore", "asset management", or needs to understand Aave V4 Hub operations.
version: 0.1.0
---

# Aave V4 Hub

The Hub is the immutable central coordinator for liquidity management in Aave V4. It manages assets, tracks shares, and enforces accounting invariants.

## Overview

```
┌──────────────────────────────────────────────────────────────┐
│                         HUB                                  │
├──────────────────────────────────────────────────────────────┤
│                                                              │
│  Assets                     Spokes                           │
│  ───────                    ──────                           │
│  USDC (id=0) ◄──────────── Spoke A (crypto)                  │
│                      └──── Spoke B (RWA)                     │
│                                                              │
│  WETH (id=1) ◄──────────── Spoke A (crypto)                  │
│                                                              │
│  Operations (Spoke → Hub):                                   │
│  • add()     - Supply liquidity                              │
│  • remove()  - Withdraw liquidity                            │
│  • draw()    - Borrow liquidity                              │
│  • restore() - Repay liquidity                               │
│                                                              │
└──────────────────────────────────────────────────────────────┘
```

## Hub Contract

```solidity
contract Hub is IHub, AccessManaged {
    using EnumerableSet for EnumerableSet.AddressSet;
    using AssetLogic for Asset;
    using SharesMath for uint256;

    uint8 public constant MAX_ALLOWED_UNDERLYING_DECIMALS = 18;
    uint8 public constant MIN_ALLOWED_UNDERLYING_DECIMALS = 6;
    uint40 public constant MAX_ALLOWED_SPOKE_CAP = type(uint40).max;

    // Asset storage
    uint256 internal _assetCount;
    mapping(uint256 assetId => Asset) internal _assets;

    // Spoke storage
    mapping(uint256 assetId => mapping(address spoke => SpokeData)) internal _spokes;
    mapping(uint256 assetId => EnumerableSet.AddressSet) internal _assetToSpokes;

    // Underlying tracking
    EnumerableSet.AddressSet internal _underlyingAssets;
}
```

## Asset Structure

```solidity
struct Asset {
    uint256 liquidity;           // Total underlying in Hub
    uint256 deficitRay;          // Bad debt (scaled by RAY)
    uint256 swept;               // Amount sent to reinvestment controller

    // Share accounting
    uint256 addedShares;         // Total supply shares
    uint256 drawnShares;         // Total borrow shares
    uint256 premiumShares;       // Risk premium shares
    uint256 premiumOffsetRay;    // Premium offset for accounting

    // Index and rates
    uint120 drawnIndex;          // Borrow index (RAY)
    uint96 drawnRate;            // Current borrow rate
    uint40 lastUpdateTimestamp;

    // Asset info
    address underlying;
    uint8 decimals;

    // Configuration
    address irStrategy;          // Interest rate strategy
    address feeReceiver;         // Protocol fee receiver
    address reinvestmentController;
    uint16 liquidityFee;         // Fee on liquidity (BPS)
    uint256 realizedFees;        // Accumulated fees
}
```

## Spoke Data

```solidity
struct SpokeData {
    uint256 addedShares;    // Spoke's supply shares
    uint256 drawnShares;    // Spoke's borrow shares
    uint256 premiumShares;  // Spoke's premium shares
    uint40 addCap;          // Max supply cap
    uint40 drawCap;         // Max borrow cap
    bool active;            // Is spoke active
    bool paused;            // Is spoke paused
}
```

## Core Operations

### add() - Supply Liquidity

Spokes call `add()` when users supply assets:

```solidity
/// @notice Add asset on behalf of user.
/// @dev Only callable by active spokes.
/// @dev Underlying assets must be transferred to the Hub before invocation.
function add(uint256 assetId, uint256 amount) external returns (uint256 shares) {
    require(assetId < _assetCount, AssetNotListed());
    Asset storage asset = _assets[assetId];
    SpokeData storage spoke = _spokes[assetId][msg.sender];

    require(spoke.active && !spoke.paused, SpokeNotActive());
    asset.accrue();  // Update indexes

    // Calculate shares
    shares = amount.toAddShares(asset.addedShares, asset.liquidity);

    // Validate cap
    uint256 newAddedShares = spoke.addedShares + shares;
    require(newAddedShares <= spoke.addCap || spoke.addCap == 0, AddCapExceeded());

    // Update state
    spoke.addedShares = newAddedShares;
    asset.addedShares += shares;
    asset.liquidity += amount;

    asset.updateDrawnRate(assetId);

    emit Add(assetId, msg.sender, shares, amount);
}
```

### remove() - Withdraw Liquidity

Spokes call `remove()` when users withdraw:

```solidity
/// @notice Remove added asset on behalf of user.
/// @dev Only callable by active spokes.
function remove(
    uint256 assetId,
    uint256 amount,
    address to
) external returns (uint256 shares) {
    require(assetId < _assetCount, AssetNotListed());
    Asset storage asset = _assets[assetId];
    SpokeData storage spoke = _spokes[assetId][msg.sender];

    require(spoke.active && !spoke.paused, SpokeNotActive());
    asset.accrue();

    // Calculate shares needed
    shares = amount.toRemoveShares(asset.addedShares, asset.liquidity);

    // Validate available liquidity
    uint256 availableLiquidity = asset.liquidity - asset.swept;
    require(amount <= availableLiquidity, InsufficientLiquidity());

    // Update state
    spoke.addedShares -= shares;
    asset.addedShares -= shares;
    asset.liquidity -= amount;

    // Transfer underlying
    IERC20(asset.underlying).safeTransfer(to, amount);

    asset.updateDrawnRate(assetId);

    emit Remove(assetId, msg.sender, shares, amount);
}
```

### draw() - Borrow Liquidity

Spokes call `draw()` when users borrow:

```solidity
/// @notice Draw assets on behalf of user.
/// @dev Only callable by active spokes.
function draw(
    uint256 assetId,
    uint256 amount,
    address to
) external returns (uint256 shares) {
    require(assetId < _assetCount, AssetNotListed());
    Asset storage asset = _assets[assetId];
    SpokeData storage spoke = _spokes[assetId][msg.sender];

    require(spoke.active && !spoke.paused, SpokeNotActive());
    asset.accrue();

    // Calculate debt shares
    shares = amount.toDrawShares(asset.drawnShares, asset.getDrawn());

    // Validate caps
    uint256 newDrawnShares = spoke.drawnShares + shares;
    require(newDrawnShares <= spoke.drawCap || spoke.drawCap == 0, DrawCapExceeded());

    uint256 availableLiquidity = asset.liquidity - asset.swept;
    require(amount <= availableLiquidity, InsufficientLiquidity());

    // Update state
    spoke.drawnShares = newDrawnShares;
    asset.drawnShares += shares;

    // Transfer underlying
    IERC20(asset.underlying).safeTransfer(to, amount);

    asset.updateDrawnRate(assetId);

    emit Draw(assetId, msg.sender, shares, amount);
}
```

### restore() - Repay Liquidity

Spokes call `restore()` when users repay:

```solidity
/// @notice Restore assets on behalf of user.
/// @dev Only callable by active spokes.
/// @dev Interest is always paid off first from premium, then from drawn.
/// @dev Underlying assets must be transferred to the Hub before invocation.
function restore(
    uint256 assetId,
    uint256 drawnAmount,
    PremiumDelta calldata premiumDelta
) external returns (uint256 drawnShares) {
    require(assetId < _assetCount, AssetNotListed());
    Asset storage asset = _assets[assetId];
    SpokeData storage spoke = _spokes[assetId][msg.sender];

    require(spoke.active && !spoke.paused, SpokeNotActive());
    asset.accrue();

    // Calculate and restore drawn shares
    drawnShares = drawnAmount.toRestoreShares(asset.drawnShares, asset.getDrawn());
    spoke.drawnShares -= drawnShares;
    asset.drawnShares -= drawnShares;

    // Apply premium delta
    _applyPremiumDelta(asset, spoke, premiumDelta);

    // Increase liquidity (underlying already transferred)
    uint256 premiumAmount = premiumDelta.restoredPremiumRay.rayToFloor();
    asset.liquidity += drawnAmount + premiumAmount;

    asset.updateDrawnRate(assetId);

    emit Restore(assetId, msg.sender, drawnShares, premiumDelta, drawnAmount, premiumAmount);
}
```

## Share Mathematics

```solidity
library SharesMath {
    /// @notice Convert assets to add shares (supply)
    /// @dev Rounds down
    function toAddShares(
        uint256 assets,
        uint256 totalShares,
        uint256 totalAssets
    ) internal pure returns (uint256) {
        if (totalShares == 0) return assets;
        return assets.mulDiv(totalShares, totalAssets);
    }

    /// @notice Convert shares to assets for removal (withdraw)
    /// @dev Rounds down
    function toRemoveAssets(
        uint256 shares,
        uint256 totalShares,
        uint256 totalAssets
    ) internal pure returns (uint256) {
        if (totalShares == 0) return 0;
        return shares.mulDiv(totalAssets, totalShares);
    }

    /// @notice Convert assets to draw shares (borrow)
    /// @dev Rounds up to ensure debt coverage
    function toDrawShares(
        uint256 assets,
        uint256 totalShares,
        uint256 totalDrawn
    ) internal pure returns (uint256) {
        if (totalShares == 0) return assets;
        return assets.mulDivUp(totalShares, totalDrawn);
    }
}
```

## Interest Accrual

```solidity
library AssetLogic {
    /// @notice Accrue interest to update indexes
    function accrue(Asset storage self) internal {
        uint256 elapsed = block.timestamp - self.lastUpdateTimestamp;
        if (elapsed == 0) return;

        // Calculate interest
        uint256 drawn = self.getDrawn();
        if (drawn > 0) {
            // Compound interest
            uint256 interestFactor = MathUtils.calculateCompoundedInterest(
                self.drawnRate,
                self.lastUpdateTimestamp
            );

            // Update drawn index
            uint256 newIndex = self.drawnIndex.rayMul(interestFactor);
            self.drawnIndex = newIndex.toUint120();

            // Calculate fees
            uint256 interestAmount = drawn.rayMul(interestFactor - WadRayMath.RAY);
            uint256 fees = interestAmount.percentMul(self.liquidityFee);
            self.realizedFees += fees;
        }

        self.lastUpdateTimestamp = block.timestamp.toUint40();
    }

    /// @notice Get total drawn assets (debt)
    function getDrawn(Asset storage self) internal view returns (uint256) {
        if (self.drawnShares == 0) return 0;
        return self.drawnShares.rayMul(self.drawnIndex);
    }
}
```

## Asset Configuration

```solidity
/// @notice Add a new asset to the Hub
function addAsset(
    address underlying,
    uint8 decimals,
    address feeReceiver,
    address irStrategy,
    bytes calldata irData
) external restricted returns (uint256 assetId) {
    require(MIN_ALLOWED_UNDERLYING_DECIMALS <= decimals && decimals <= MAX_ALLOWED_UNDERLYING_DECIMALS);
    require(!_underlyingAssets.contains(underlying), UnderlyingAlreadyListed());

    assetId = _assetCount++;

    // Initialize interest rate
    IBasicInterestRateStrategy(irStrategy).setInterestRateData(assetId, irData);

    _assets[assetId] = Asset({
        liquidity: 0,
        deficitRay: 0,
        swept: 0,
        addedShares: 0,
        drawnShares: 0,
        premiumShares: 0,
        premiumOffsetRay: 0,
        drawnIndex: WadRayMath.RAY.toUint120(),
        underlying: underlying,
        lastUpdateTimestamp: block.timestamp.toUint40(),
        decimals: decimals,
        drawnRate: 0,
        irStrategy: irStrategy,
        realizedFees: 0,
        reinvestmentController: address(0),
        feeReceiver: feeReceiver,
        liquidityFee: 0
    });

    _underlyingAssets.add(underlying);
}
```

## Spoke Configuration

```solidity
struct SpokeConfig {
    uint40 addCap;   // Max supply (0 = unlimited)
    uint40 drawCap;  // Max borrow (0 = unlimited)
    bool active;     // Is spoke active
    bool paused;     // Is spoke paused
}

/// @notice Add a spoke for an asset
function addSpoke(
    uint256 assetId,
    address spoke,
    SpokeConfig calldata config
) external restricted {
    require(assetId < _assetCount, AssetNotListed());
    require(spoke != address(0), InvalidAddress());

    _assetToSpokes[assetId].add(spoke);
    _updateSpokeConfig(assetId, spoke, config);

    emit AddSpoke(assetId, spoke, config);
}
```

## View Functions

```solidity
/// @notice Preview add shares for given assets
function previewAddByAssets(uint256 assetId, uint256 assets) external view returns (uint256) {
    Asset storage asset = _assets[assetId];
    return assets.toAddShares(asset.addedShares, asset.liquidity);
}

/// @notice Preview remove assets for given shares
function previewRemoveByShares(uint256 assetId, uint256 shares) external view returns (uint256) {
    Asset storage asset = _assets[assetId];
    return shares.toRemoveAssets(asset.addedShares, asset.liquidity);
}

/// @notice Get asset underlying and decimals
function getAssetUnderlyingAndDecimals(uint256 assetId) external view returns (address, uint8) {
    Asset storage asset = _assets[assetId];
    return (asset.underlying, asset.decimals);
}

/// @notice Get available liquidity
function getAvailableLiquidity(uint256 assetId) external view returns (uint256) {
    Asset storage asset = _assets[assetId];
    return asset.liquidity - asset.swept;
}
```

## Events

```solidity
event Add(uint256 indexed assetId, address indexed spoke, uint256 shares, uint256 amount);
event Remove(uint256 indexed assetId, address indexed spoke, uint256 shares, uint256 amount);
event Draw(uint256 indexed assetId, address indexed spoke, uint256 drawnShares, uint256 drawnAmount);
event Restore(uint256 indexed assetId, address indexed spoke, uint256 drawnShares, PremiumDelta premiumDelta, uint256 drawnAmount, uint256 premiumAmount);
event RefreshPremium(uint256 indexed assetId, address indexed spoke, PremiumDelta premiumDelta);
event ReportDeficit(uint256 indexed assetId, address indexed spoke, uint256 drawnShares, PremiumDelta premiumDelta, uint256 deficitAmountRay);
event AddAsset(uint256 indexed assetId, address indexed underlying, uint8 decimals);
event AddSpoke(uint256 indexed assetId, address indexed spoke, SpokeConfig config);
```

## Reference Files

- `src/hub/Hub.sol` - Hub implementation
- `src/hub/interfaces/IHub.sol` - Full Hub interface
- `src/hub/interfaces/IHubBase.sol` - Base Hub interface
- `src/hub/libraries/AssetLogic.sol` - Asset logic
- `src/hub/libraries/SharesMath.sol` - Share calculations
