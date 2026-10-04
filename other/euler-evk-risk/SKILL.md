---
name: EVK Risk Management
description: This skill should be used when the user asks about "LTV", "loan-to-value", "collateral factor", "supply cap", "borrow cap", "IRM", "interest rate model", "oracle", "risk parameters", or needs to understand EVault risk configuration.
version: 0.1.0
---

# EVK Risk Management

EVaults have comprehensive risk configuration including LTV settings, supply/borrow caps, interest rate models, and oracle integration.

## Overview

```
┌──────────────────────────────────────────────────────────────┐
│                   RISK CONFIGURATION                         │
├──────────────────────────────────────────────────────────────┤
│                                                              │
│  Per-Collateral Settings (LTV):                              │
│  ┌─────────────────────────────────────────────────────────┐ │
│  │  Collateral Vault A:                                    │ │
│  │  ├── borrowLTV: 80%     (max LTV for new borrows)       │ │
│  │  ├── liquidationLTV: 85% (trigger for liquidation)      │ │
│  │  └── rampDuration: 7 days (for LTV changes)             │ │
│  │                                                         │ │
│  │  Collateral Vault B:                                    │ │
│  │  ├── borrowLTV: 75%                                     │ │
│  │  ├── liquidationLTV: 80%                                │ │
│  │  └── rampDuration: 7 days                               │ │
│  └─────────────────────────────────────────────────────────┘ │
│                                                              │
│  Vault-Level Settings:                                       │
│  ├── Supply Cap: 10M USDC                                    │
│  ├── Borrow Cap: 8M USDC                                     │
│  ├── Interest Rate Model: Kink IRM                           │
│  ├── Oracle: EulerRouter                                     │
│  ├── Max Liquidation Discount: 15%                           │
│  └── Interest Fee: 10% (protocol take)                       │
│                                                              │
└──────────────────────────────────────────────────────────────┘
```

## LTV Configuration

```solidity
// RiskManager.sol

struct LTVConfig {
    uint16 borrowLTV;              // Max LTV for borrowing (basis points, 10000 = 100%)
    uint16 liquidationLTV;         // LTV at which liquidation is allowed
    uint16 initialLiquidationLTV;  // Used during ramp period
    uint48 targetTimestamp;        // When ramp completes
    uint32 rampDuration;           // Time to ramp LTV changes
}

// Storage: collateral vault => LTV config
mapping(address => LTVConfig) internal ltvLookup;

/// @notice Set LTV for a collateral vault
/// @param collateral The collateral vault address
/// @param borrowLTV Max LTV for new borrows
/// @param liquidationLTV LTV threshold for liquidation
/// @param rampDuration Time to ramp changes (0 for immediate)
function setLTV(
    address collateral,
    uint16 borrowLTV,
    uint16 liquidationLTV,
    uint32 rampDuration
) external onlyGovernor {
    // Validation
    require(borrowLTV <= liquidationLTV, "borrowLTV > liquidationLTV");
    require(liquidationLTV <= 10000, "liquidationLTV > 100%");

    LTVConfig storage config = ltvLookup[collateral];

    if (rampDuration > 0) {
        // Ramp from current to new over rampDuration
        config.initialLiquidationLTV = getCurrentLiquidationLTV(collateral);
        config.targetTimestamp = uint48(block.timestamp + rampDuration);
    }

    config.borrowLTV = borrowLTV;
    config.liquidationLTV = liquidationLTV;
    config.rampDuration = rampDuration;

    emit SetLTV(collateral, borrowLTV, liquidationLTV, rampDuration);
}

/// @notice Get current liquidation LTV (accounts for ramp)
function getCurrentLiquidationLTV(address collateral) public view returns (uint16) {
    LTVConfig memory config = ltvLookup[collateral];

    if (block.timestamp >= config.targetTimestamp) {
        return config.liquidationLTV;
    }

    // Linear interpolation during ramp
    uint256 elapsed = block.timestamp - (config.targetTimestamp - config.rampDuration);
    uint256 progress = elapsed * 1e18 / config.rampDuration;

    int256 diff = int256(uint256(config.liquidationLTV)) - int256(uint256(config.initialLiquidationLTV));

    return uint16(uint256(int256(uint256(config.initialLiquidationLTV)) + diff * int256(progress) / 1e18));
}

/// @notice Clear LTV for a collateral (disable as collateral)
function clearLTV(address collateral) external onlyGovernor {
    delete ltvLookup[collateral];
    emit ClearLTV(collateral);
}
```

## Supply and Borrow Caps

```solidity
// RiskManager.sol

/// @notice Set supply cap for the vault
/// @param newSupplyCap Maximum supply in asset units (0 = unlimited)
function setSupplyCap(uint256 newSupplyCap) external onlyGovernor {
    uint256 oldCap = vaultStorage.supplyCap;
    vaultStorage.supplyCap = newSupplyCap;
    emit SetSupplyCap(oldCap, newSupplyCap);
}

/// @notice Set borrow cap for the vault
/// @param newBorrowCap Maximum borrows in asset units (0 = unlimited)
function setBorrowCap(uint256 newBorrowCap) external onlyGovernor {
    uint256 oldCap = vaultStorage.borrowCap;
    vaultStorage.borrowCap = newBorrowCap;
    emit SetBorrowCap(oldCap, newBorrowCap);
}

/// @notice Get current supply cap
function supplyCap() public view returns (uint256) {
    return vaultStorage.supplyCap == 0 ? type(uint256).max : vaultStorage.supplyCap;
}

/// @notice Get current borrow cap
function borrowCap() public view returns (uint256) {
    return vaultStorage.borrowCap == 0 ? type(uint256).max : vaultStorage.borrowCap;
}

// Checked during operations
function deposit(...) external {
    // ...
    if (cache.totalShares > supplyCap()) revert SupplyCapExceeded();
}

function borrow(...) external {
    // ...
    if (cache.totalBorrows > borrowCap()) revert BorrowCapExceeded();
}
```

## Interest Rate Model

```solidity
// RiskManager.sol

/// @notice Set interest rate model
/// @param newInterestRateModel Address of IRM contract
function setInterestRateModel(address newInterestRateModel) external onlyGovernor {
    address oldIRM = vaultStorage.interestRateModel;
    vaultStorage.interestRateModel = newInterestRateModel;
    emit SetInterestRateModel(oldIRM, newInterestRateModel);
}

// IRM Interface
interface IIRM {
    /// @notice Calculate borrow rate
    /// @param vault The vault address
    /// @param cash Available cash
    /// @param borrows Total borrows
    /// @return Borrow rate per second (scaled by 1e27)
    function computeInterestRate(
        address vault,
        uint256 cash,
        uint256 borrows
    ) external view returns (uint256);

    /// @notice Same but for view context
    function computeInterestRateView(
        address vault,
        uint256 cash,
        uint256 borrows
    ) external view returns (uint256);
}
```

## Kink Interest Rate Model

```solidity
// Common IRM implementation

contract KinkIRM is IIRM {
    // Rate parameters (per second, scaled by 1e27)
    uint256 public immutable baseRate;
    uint256 public immutable slope1;        // Below kink
    uint256 public immutable slope2;        // Above kink
    uint256 public immutable kink;          // Utilization kink (scaled by 1e18)

    constructor(
        uint256 _baseRate,
        uint256 _slope1,
        uint256 _slope2,
        uint256 _kink
    ) {
        baseRate = _baseRate;
        slope1 = _slope1;
        slope2 = _slope2;
        kink = _kink;
    }

    function computeInterestRate(
        address,
        uint256 cash,
        uint256 borrows
    ) external view returns (uint256) {
        if (borrows == 0) return baseRate;

        // Utilization = borrows / (cash + borrows)
        uint256 utilization = borrows * 1e18 / (cash + borrows);

        if (utilization <= kink) {
            // Linear increase up to kink
            return baseRate + utilization * slope1 / 1e18;
        } else {
            // Steeper increase above kink
            uint256 rateAtKink = baseRate + kink * slope1 / 1e18;
            uint256 excessUtilization = utilization - kink;
            return rateAtKink + excessUtilization * slope2 / 1e18;
        }
    }
}
```

## Oracle Configuration

```solidity
// Base.sol - Oracle is immutable

address public immutable oracle;
address public immutable unitOfAccount;

// Oracle interface
interface IPriceOracle {
    /// @notice Get quote (amount of quoteToken for baseToken amount)
    function getQuote(
        uint256 amount,
        address base,
        address quote
    ) external view returns (uint256);

    /// @notice Get quotes with separate bid/ask
    function getQuotes(
        uint256 amount,
        address base,
        address quote
    ) external view returns (uint256 bidOut, uint256 askOut);
}

// Usage in health check
function getAccountDebtValue(address account) internal view returns (uint256) {
    uint256 debtAssets = debtOf(account);
    if (debtAssets == 0) return 0;

    // Convert debt to unit of account using oracle
    return IPriceOracle(oracle).getQuote(
        debtAssets,
        asset(),           // base (debt asset)
        unitOfAccount      // quote (common denominator)
    );
}

function getCollateralValue(address account, address collateral) internal view returns (uint256) {
    uint256 shares = IEVault(collateral).balanceOf(account);
    if (shares == 0) return 0;

    uint256 assets = IEVault(collateral).convertToAssets(shares);

    return IPriceOracle(oracle).getQuote(
        assets,
        IEVault(collateral).asset(),  // base (collateral asset)
        unitOfAccount                  // quote
    );
}
```

## Liquidation Parameters

```solidity
// RiskManager.sol

/// @notice Set maximum liquidation discount
/// @param newDiscount Max discount in basis points (e.g., 1500 = 15%)
function setMaxLiquidationDiscount(uint16 newDiscount) external onlyGovernor {
    require(newDiscount <= 5000, "Discount > 50%");  // Safety cap

    uint16 oldDiscount = vaultStorage.maxLiquidationDiscount;
    vaultStorage.maxLiquidationDiscount = newDiscount;

    emit SetMaxLiquidationDiscount(oldDiscount, newDiscount);
}

/// @notice Set cool-off time between liquidations
function setLiquidationCoolOffTime(uint16 newCoolOff) external onlyGovernor {
    uint16 oldCoolOff = vaultStorage.liquidationCoolOffTime;
    vaultStorage.liquidationCoolOffTime = newCoolOff;

    emit SetLiquidationCoolOffTime(oldCoolOff, newCoolOff);
}
```

## Interest Fee

```solidity
// Governance.sol

/// @notice Set protocol interest fee
/// @param newFee Fee in basis points (e.g., 1000 = 10%)
function setInterestFee(uint16 newFee) external onlyGovernor {
    require(newFee <= 5000, "Fee > 50%");  // Safety cap

    uint16 oldFee = vaultStorage.interestFee;
    vaultStorage.interestFee = newFee;

    emit SetInterestFee(oldFee, newFee);
}

/// @notice Set fee receiver address
function setFeeReceiver(address newReceiver) external onlyGovernor {
    address oldReceiver = vaultStorage.feeReceiver;
    vaultStorage.feeReceiver = newReceiver;

    emit SetFeeReceiver(oldReceiver, newReceiver);
}

// Fee collection during interest accrual
function accrueInterest(VaultCache memory cache) internal {
    // ... calculate interest

    // Protocol fee
    uint256 feeAmount = interestEarned * cache.interestFee / 10000;

    // Mint fee shares to feeReceiver
    uint256 feeShares = feeAmount.mulDiv(
        cache.totalShares,
        cache.cash + cache.totalBorrows - feeAmount,
        Math.Rounding.Down
    );

    if (feeShares > 0) {
        users[cache.feeReceiver].balance += feeShares;
        cache.totalShares += feeShares;
    }
}
```

## Risk View Functions

```solidity
/// @notice Get LTV configuration for a collateral
function LTVConfig(address collateral) external view returns (
    uint16 borrowLTV,
    uint16 liquidationLTV,
    uint16 currentLiquidationLTV,
    uint48 targetTimestamp,
    uint32 rampDuration
) {
    LTVConfig memory config = ltvLookup[collateral];
    return (
        config.borrowLTV,
        config.liquidationLTV,
        getCurrentLiquidationLTV(collateral),
        config.targetTimestamp,
        config.rampDuration
    );
}

/// @notice Get all accepted collaterals with their LTVs
function getCollateralLTVs() external view returns (
    address[] memory collaterals,
    LTVConfig[] memory configs
);

/// @notice Current utilization ratio
function utilization() public view returns (uint256) {
    VaultCache memory cache = loadVault();
    if (cache.totalBorrows == 0) return 0;
    return cache.totalBorrows * 1e18 / (cache.cash + cache.totalBorrows);
}

/// @notice Current borrow rate
function borrowAPY() public view returns (uint256) {
    VaultCache memory cache = loadVault();
    return IIRM(cache.interestRateModel).computeInterestRateView(
        address(this),
        cache.cash,
        cache.totalBorrows
    ) * SECONDS_PER_YEAR;
}

/// @notice Current supply rate
function supplyAPY() public view returns (uint256) {
    uint256 borrowRate = borrowAPY();
    uint256 util = utilization();

    // Supply APY = borrow APY * utilization * (1 - fee)
    return borrowRate * util / 1e18 * (10000 - vaultStorage.interestFee) / 10000;
}
```

## Events

```solidity
event SetLTV(address indexed collateral, uint16 borrowLTV, uint16 liquidationLTV, uint32 rampDuration);
event ClearLTV(address indexed collateral);
event SetSupplyCap(uint256 oldCap, uint256 newCap);
event SetBorrowCap(uint256 oldCap, uint256 newCap);
event SetInterestRateModel(address indexed oldIRM, address indexed newIRM);
event SetMaxLiquidationDiscount(uint16 oldDiscount, uint16 newDiscount);
event SetLiquidationCoolOffTime(uint16 oldCoolOff, uint16 newCoolOff);
event SetInterestFee(uint16 oldFee, uint16 newFee);
event SetFeeReceiver(address indexed oldReceiver, address indexed newReceiver);
```

## Reference Files

- `euler-vault-kit/src/EVault/modules/RiskManager.sol` - Risk configuration
- `euler-vault-kit/src/EVault/modules/Governance.sol` - Fee configuration
- `euler-vault-kit/src/InterestRateModels/` - IRM implementations
- `euler-price-oracle/src/EulerRouter.sol` - Oracle router
