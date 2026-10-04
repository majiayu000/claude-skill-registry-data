---
name: Aave V4 Spoke
description: This skill should be used when the user asks about "Spoke contract", "Spoke.sol", "Aave V4 supply", "Aave V4 borrow", "Aave V4 repay", "Aave V4 withdraw", "reserve", "user position", or needs to understand Spoke operations.
version: 0.1.0
---

# Aave V4 Spoke

Spokes are upgradeable contracts that handle user-facing operations in Aave V4. They manage reserves, user positions, risk parameters, and interact with the Hub for liquidity.

## Overview

```
┌──────────────────────────────────────────────────────────────┐
│                         SPOKE                                │
├──────────────────────────────────────────────────────────────┤
│                                                              │
│  User Operations          Risk Management                    │
│  ───────────────          ───────────────                    │
│  • supply()               • Collateral Risk                  │
│  • withdraw()             • Dynamic Config                   │
│  • borrow()               • Health Factor                    │
│  • repay()                • Liquidation                      │
│  • liquidationCall()                                         │
│                                                              │
│  Reserves                 User Positions                     │
│  ────────                 ──────────────                     │
│  reserveId=0 → USDC       user → reserveId → position        │
│  reserveId=1 → WETH                                          │
│                                                              │
└──────────────────────────────────────────────────────────────┘
```

## Spoke Contract

```solidity
abstract contract Spoke is ISpoke, Multicall, NoncesKeyed, AccessManagedUpgradeable, EIP712 {
    address public immutable ORACLE;

    uint64 internal constant HEALTH_FACTOR_LIQUIDATION_THRESHOLD = 1e18;  // 1.0

    // Storage
    uint256 internal _reserveCount;
    mapping(uint256 reserveId => Reserve) internal _reserves;
    mapping(address user => mapping(uint256 reserveId => UserPosition)) internal _userPositions;
    mapping(address user => PositionStatus) internal _positionStatus;
    mapping(address positionManager => PositionManagerConfig) internal _positionManager;
    mapping(uint256 reserveId => mapping(uint24 configKey => DynamicReserveConfig)) internal _dynamicConfig;
    LiquidationConfig internal _liquidationConfig;
}
```

## Data Structures

### Reserve

```solidity
struct Reserve {
    address underlying;          // Underlying token address
    IHubBase hub;               // Associated Hub
    uint16 assetId;             // Asset ID in Hub
    uint8 decimals;             // Token decimals
    uint24 dynamicConfigKey;    // Current active config key
    uint24 collateralRisk;      // Risk premium factor (0-1000_00 BPS)
    ReserveFlags flags;         // paused, frozen, borrowable, liquidatable
}
```

### UserPosition

```solidity
struct UserPosition {
    uint256 suppliedShares;     // User's supply shares
    uint256 drawnShares;        // User's borrow shares
    uint256 premiumSharesRay;   // Premium shares (RAY precision)
    uint256 premiumOffsetRay;   // Premium offset (RAY precision)
    uint24 dynamicConfigKey;    // Position's bound config key
}
```

### PositionStatus

```solidity
struct PositionStatus {
    uint256 usingAsCollateralBitmap;    // Which reserves are collateral
    uint256 borrowingBitmap;            // Which reserves have borrows
}
```

### Dynamic Reserve Config

```solidity
struct DynamicReserveConfig {
    uint16 collateralFactor;    // CF: max borrow power (BPS)
    uint16 maxLiquidationBonus; // Max LB (> 100_00)
    uint16 liquidationFee;      // Protocol fee on liquidation (BPS)
}
```

## Core Operations

### supply()

```solidity
function supply(
    uint256 reserveId,
    uint256 amount,
    address onBehalfOf
) external onlyPositionManager(onBehalfOf) returns (uint256 shares, uint256 suppliedAmount) {
    Reserve storage reserve = _getReserve(reserveId);
    _validateNotPausedNotFrozen(reserve);

    // Transfer underlying from caller to Hub
    IERC20(reserve.underlying).safeTransferFrom(msg.sender, address(reserve.hub), amount);

    // Add to Hub
    shares = reserve.hub.add(reserve.assetId, amount);
    suppliedAmount = amount;

    // Update user position
    UserPosition storage position = _userPositions[onBehalfOf][reserveId];
    position.suppliedShares += shares;

    // Auto-enable as collateral if first supply
    if (_isFirstSupply(onBehalfOf, reserveId)) {
        _enableUsingAsCollateral(onBehalfOf, reserveId);
    }

    emit Supply(reserveId, msg.sender, onBehalfOf, shares, suppliedAmount);
}
```

### withdraw()

```solidity
function withdraw(
    uint256 reserveId,
    uint256 amount,
    address onBehalfOf
) external onlyPositionManager(onBehalfOf) returns (uint256 shares, uint256 withdrawnAmount) {
    Reserve storage reserve = _getReserve(reserveId);
    _validateNotPaused(reserve);

    UserPosition storage position = _userPositions[onBehalfOf][reserveId];

    // Calculate max withdrawable
    uint256 maxWithdrawable = _getMaxWithdrawable(onBehalfOf, reserveId);
    withdrawnAmount = amount > maxWithdrawable ? maxWithdrawable : amount;

    // Calculate shares to burn
    shares = reserve.hub.previewRemoveByAssets(reserve.assetId, withdrawnAmount);

    // Update position
    position.suppliedShares -= shares;

    // Remove from Hub (sends to caller)
    reserve.hub.remove(reserve.assetId, withdrawnAmount, msg.sender);

    // Update dynamic config (risk-decreasing action)
    _updateUserDynamicConfigIfHealthy(onBehalfOf);

    // Validate health factor
    _validateHealthFactor(onBehalfOf);

    emit Withdraw(reserveId, msg.sender, onBehalfOf, shares, withdrawnAmount);
}
```

### borrow()

```solidity
function borrow(
    uint256 reserveId,
    uint256 amount,
    address onBehalfOf
) external onlyPositionManager(onBehalfOf) returns (uint256 shares, uint256 borrowedAmount) {
    Reserve storage reserve = _getReserve(reserveId);
    _validateNotPausedNotFrozen(reserve);
    _validateBorrowable(reserve);

    borrowedAmount = amount;

    // Update user's risk premium before borrow
    _updateUserRiskPremium(onBehalfOf);

    // Draw from Hub (sends to caller)
    shares = reserve.hub.draw(reserve.assetId, amount, msg.sender);

    // Update user position
    UserPosition storage position = _userPositions[onBehalfOf][reserveId];
    position.drawnShares += shares;

    // Add premium shares based on user's risk premium
    uint256 riskPremium = _getUserRiskPremium(onBehalfOf);
    _addPremiumShares(position, shares, riskPremium);

    // Update dynamic config snapshot (risk-increasing action)
    _refreshUserDynamicConfig(onBehalfOf);

    // Validate health factor
    _validateHealthFactor(onBehalfOf);

    emit Borrow(reserveId, msg.sender, onBehalfOf, shares, borrowedAmount);
}
```

### repay()

```solidity
function repay(
    uint256 reserveId,
    uint256 amount,
    address onBehalfOf
) external onlyPositionManager(onBehalfOf) returns (uint256 shares, uint256 repaidAmount) {
    Reserve storage reserve = _getReserve(reserveId);
    _validateNotPaused(reserve);

    UserPosition storage position = _userPositions[onBehalfOf][reserveId];

    // Calculate total debt
    (uint256 drawnDebt, uint256 premiumDebt) = _getUserDebt(reserveId, onBehalfOf);
    uint256 totalDebt = drawnDebt + premiumDebt;

    // Cap repayment at total debt
    repaidAmount = amount > totalDebt ? totalDebt : amount;

    // Calculate how much goes to premium vs drawn
    uint256 premiumRepaid = repaidAmount > premiumDebt ? premiumDebt : repaidAmount;
    uint256 drawnRepaid = repaidAmount - premiumRepaid;

    // Transfer underlying to Hub
    IERC20(reserve.underlying).safeTransferFrom(msg.sender, address(reserve.hub), repaidAmount);

    // Calculate premium delta
    IHubBase.PremiumDelta memory premiumDelta = _calculatePremiumDelta(
        position,
        premiumRepaid
    );

    // Restore to Hub
    shares = reserve.hub.restore(reserve.assetId, drawnRepaid, premiumDelta);

    // Update position
    position.drawnShares -= shares;
    _applyPremiumDelta(position, premiumDelta);

    emit Repay(reserveId, msg.sender, onBehalfOf, shares, repaidAmount, premiumDelta);
}
```

## Collateral Management

### Enable/Disable Collateral

```solidity
function enableUsingAsCollateral(uint256 reserveId) external {
    _validateHasSupply(msg.sender, reserveId);
    _enableUsingAsCollateral(msg.sender, reserveId);

    // Refresh only this reserve's config key
    _refreshReserveDynamicConfig(msg.sender, reserveId);
}

function disableUsingAsCollateral(uint256 reserveId) external {
    _disableUsingAsCollateral(msg.sender, reserveId);

    // Risk-increasing action - refresh all config keys
    _refreshUserDynamicConfig(msg.sender);

    // Validate health factor
    _validateHealthFactor(msg.sender);
}
```

## Health Factor Calculation

```solidity
function getUserHealthFactor(address user) public view returns (uint256) {
    PositionStatus storage status = _positionStatus[user];

    uint256 totalCollateralValue = 0;
    uint256 totalDebtValue = 0;

    // Iterate over collateral reserves
    uint256 collateralBitmap = status.usingAsCollateralBitmap;
    while (collateralBitmap != 0) {
        uint256 reserveId = _getNextReserveId(collateralBitmap);
        collateralBitmap = _clearBit(collateralBitmap, reserveId);

        UserPosition storage position = _userPositions[user][reserveId];
        DynamicReserveConfig storage config = _dynamicConfig[reserveId][position.dynamicConfigKey];

        uint256 supplyValue = _getPositionSupplyValue(user, reserveId);
        uint256 collateralValue = supplyValue.percentMul(config.collateralFactor);
        totalCollateralValue += collateralValue;
    }

    // Iterate over debt reserves
    uint256 borrowBitmap = status.borrowingBitmap;
    while (borrowBitmap != 0) {
        uint256 reserveId = _getNextReserveId(borrowBitmap);
        borrowBitmap = _clearBit(borrowBitmap, reserveId);

        uint256 debtValue = _getPositionDebtValue(user, reserveId);
        totalDebtValue += debtValue;
    }

    if (totalDebtValue == 0) return type(uint256).max;

    return totalCollateralValue.wadDiv(totalDebtValue);
}

function _validateHealthFactor(address user) internal view {
    uint256 hf = getUserHealthFactor(user);
    require(hf >= HEALTH_FACTOR_LIQUIDATION_THRESHOLD, UnhealthyPosition());
}
```

## Reserve Configuration

### Adding a Reserve

```solidity
struct ReserveConfig {
    uint24 collateralRisk;      // Risk premium factor
    bool paused;
    bool frozen;
    bool borrowable;
    bool liquidatable;
    bool receiveSharesEnabled;
}

function addReserve(
    address hub,
    uint256 assetId,
    address priceSource,
    ReserveConfig calldata config,
    DynamicReserveConfig calldata dynamicConfig
) external restricted returns (uint256 reserveId) {
    require(!_reserveExists[hub][assetId], ReserveExists());

    reserveId = _reserveCount++;

    (address underlying, uint8 decimals) = IHubBase(hub).getAssetUnderlyingAndDecimals(assetId);

    _reserves[reserveId] = Reserve({
        underlying: underlying,
        hub: IHubBase(hub),
        assetId: assetId.toUint16(),
        decimals: decimals,
        dynamicConfigKey: 0,  // First config key
        collateralRisk: config.collateralRisk,
        flags: ReserveFlagsMap.create(config)
    });

    _dynamicConfig[reserveId][0] = dynamicConfig;
    _reserveExists[hub][assetId] = true;

    emit AddReserve(reserveId, assetId, hub);
}
```

## Position Manager Authorization

```solidity
modifier onlyPositionManager(address onBehalfOf) {
    require(_isPositionManager(onBehalfOf, msg.sender), Unauthorized());
    _;
}

function _isPositionManager(address user, address manager) internal view returns (bool) {
    if (user == manager) return true;
    return _positionManager[manager].approvedForUser[user];
}

/// @notice Approve a position manager for user
function setUserPositionManager(address manager, bool approved) external {
    _positionManager[manager].approvedForUser[msg.sender] = approved;
    emit SetUserPositionManager(msg.sender, manager, approved);
}

/// @notice Approve via EIP-712 signature
function setUserPositionManagerWithSig(
    address manager,
    address user,
    bool approve,
    uint256 deadline,
    bytes calldata signature
) external {
    require(block.timestamp <= deadline, ExpiredSignature());

    bytes32 structHash = keccak256(abi.encode(
        SET_USER_POSITION_MANAGER_TYPEHASH,
        manager,
        user,
        approve,
        _useNonce(user),
        deadline
    ));

    require(SignatureChecker.isValidSignatureNow(user, _hashTypedData(structHash), signature));

    _positionManager[manager].approvedForUser[user] = approve;
}
```

## View Functions

```solidity
/// @notice Get user's supplied assets for a reserve
function getUserSuppliedAssets(uint256 reserveId, address user) external view returns (uint256) {
    UserPosition storage position = _userPositions[user][reserveId];
    Reserve storage reserve = _reserves[reserveId];
    return reserve.hub.previewRemoveByShares(reserve.assetId, position.suppliedShares);
}

/// @notice Get user's total debt for a reserve
function getUserTotalDebt(uint256 reserveId, address user) external view returns (uint256) {
    (uint256 drawnDebt, uint256 premiumDebt) = getUserDebt(reserveId, user);
    return drawnDebt + premiumDebt;
}

/// @notice Get user's debt breakdown
function getUserDebt(uint256 reserveId, address user) external view returns (uint256 drawn, uint256 premium) {
    UserPosition storage position = _userPositions[user][reserveId];
    Reserve storage reserve = _reserves[reserveId];

    drawn = reserve.hub.previewRestoreByShares(reserve.assetId, position.drawnShares);
    premium = _getUserPremiumDebt(position, reserve);
}

/// @notice Check if user is using reserve as collateral
function isUsingAsCollateral(address user, uint256 reserveId) external view returns (bool) {
    return _positionStatus[user].usingAsCollateralBitmap & (1 << reserveId) != 0;
}
```

## Events

```solidity
event Supply(uint256 indexed reserveId, address indexed caller, address indexed user, uint256 shares, uint256 amount);
event Withdraw(uint256 indexed reserveId, address indexed caller, address indexed user, uint256 shares, uint256 amount);
event Borrow(uint256 indexed reserveId, address indexed caller, address indexed user, uint256 shares, uint256 amount);
event Repay(uint256 indexed reserveId, address indexed caller, address indexed user, uint256 shares, uint256 amount, IHubBase.PremiumDelta premiumDelta);
event EnableUsingAsCollateral(address indexed user, uint256 indexed reserveId);
event DisableUsingAsCollateral(address indexed user, uint256 indexed reserveId);
event AddReserve(uint256 indexed reserveId, uint256 assetId, address hub);
event SetUserPositionManager(address indexed user, address indexed manager, bool approved);
```

## Reference Files

- `src/spoke/Spoke.sol` - Spoke implementation
- `src/spoke/interfaces/ISpoke.sol` - Full Spoke interface
- `src/spoke/interfaces/ISpokeBase.sol` - Base Spoke interface
- `src/spoke/libraries/UserPositionDebt.sol` - Debt calculations
- `src/spoke/libraries/PositionStatusMap.sol` - Position status utilities
