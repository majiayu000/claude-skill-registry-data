---
name: resupply-lending
description: This skill should be used when the user asks about "ResupplyPair", "lending pair", "borrow reUSD", "add collateral", "remove collateral", "repay debt", "interest rates", "leveraged positions", or needs to understand Resupply's core lending mechanics.
---

# Resupply Lending System

The lending system is built around ResupplyPair contracts that enable users to deposit ERC4626 vault tokens as collateral and borrow reUSD stablecoins.

## ResupplyPair Contract

Located at `/src/protocol/ResupplyPair.sol` with core logic in `/src/protocol/pair/ResupplyPairCore.sol`.

### State Structure

```solidity
// Collateral tracking
mapping(address => uint256) public userCollateralBalance;  // User → collateral amount
uint256 public totalCollateral;

// Borrow tracking (share-based for interest accrual)
mapping(address => uint256) public userBorrowShares;       // User → borrow shares
uint256 public totalBorrowShares;
uint256 public totalBorrowAmount;                          // Actual debt amount

// Configuration
address public collateralContract;    // ERC4626 vault token
address public asset;                 // reUSD stablecoin
uint256 public maxLTV;                // e.g., 95_000 (95% with LTV_PRECISION)
uint256 public liquidationFee;        // e.g., 5_000 (5%)
uint256 public borrowLimit;           // Maximum borrowable amount
```

## Core Operations

### Adding Collateral

Deposit ERC4626 vault tokens as collateral:

```solidity
function addCollateralVault(uint256 _collateralAmount, address _borrower) external {
    // Transfer vault tokens from caller
    IERC20(collateralContract).safeTransferFrom(msg.sender, address(this), _collateralAmount);

    // Update balances
    userCollateralBalance[_borrower] += _collateralAmount;
    totalCollateral += _collateralAmount;
}
```

### Removing Collateral

Withdraw collateral (must maintain health factor):

```solidity
function removeCollateralVault(uint256 _collateralAmount, address _receiver) external {
    // Update balances
    userCollateralBalance[msg.sender] -= _collateralAmount;
    totalCollateral -= _collateralAmount;

    // Verify position remains healthy
    require(_isSolvent(msg.sender), "Position unhealthy");

    // Transfer vault tokens
    IERC20(collateralContract).safeTransfer(_receiver, _collateralAmount);
}
```

### Borrowing

Mint reUSD against deposited collateral:

```solidity
function borrow(
    uint256 _borrowAmount,
    uint256 _underlyingAmount,  // For minting to underlying protocols
    address _receiver
) external returns (uint256 shares) {
    // Accrue interest first
    _accrue();

    // Calculate borrow shares
    shares = totalBorrowShares == 0
        ? _borrowAmount
        : (_borrowAmount * totalBorrowShares) / totalBorrowAmount;

    // Update state
    userBorrowShares[msg.sender] += shares;
    totalBorrowShares += shares;
    totalBorrowAmount += _borrowAmount;

    // Verify solvency
    require(_isSolvent(msg.sender), "Position unhealthy");

    // Mint reUSD
    IStablecoin(asset).mint(_receiver, _borrowAmount);
}
```

### Repaying

Burn reUSD to reduce debt:

```solidity
function repay(uint256 _shares, address _borrower) external returns (uint256 amountRepaid) {
    _accrue();

    // Calculate amount from shares
    amountRepaid = (_shares * totalBorrowAmount) / totalBorrowShares;

    // Update state
    userBorrowShares[_borrower] -= _shares;
    totalBorrowShares -= _shares;
    totalBorrowAmount -= amountRepaid;

    // Burn reUSD from caller
    IStablecoin(asset).burn(msg.sender, amountRepaid);
}
```

## Interest Rate Model

Interest accrues per-second based on utilization:

```solidity
// InterestRateCalculator interface
function getNewRate(
    uint256 _currentRate,
    uint256 _utilization,    // totalBorrow / borrowLimit
    uint256 _deltaTime
) external view returns (uint256 newRate);
```

**Utilization calculation:**
```solidity
uint256 utilization = (totalBorrowAmount * 1e18) / borrowLimit;
```

**Interest accrual:**
```solidity
function _accrue() internal {
    uint256 deltaTime = block.timestamp - lastAccrueTime;
    uint256 interestEarned = (totalBorrowAmount * currentRate * deltaTime) / RATE_PRECISION;
    totalBorrowAmount += interestEarned;
    lastAccrueTime = block.timestamp;
}
```

## Collateral Valuation

The oracle converts vault tokens to asset value:

```solidity
// BasicVaultOracle
function getPrice(address collateral) external view returns (uint256) {
    // Get ERC4626 exchange rate
    uint256 assetsPerShare = IERC4626(collateral).convertToAssets(1e18);
    return assetsPerShare;
}
```

**Solvency check:**
```solidity
function _isSolvent(address _borrower) internal view returns (bool) {
    uint256 collateralValue = (userCollateralBalance[_borrower] * oracle.getPrice(collateralContract)) / EXCHANGE_PRECISION;
    uint256 borrowValue = (userBorrowShares[_borrower] * totalBorrowAmount) / totalBorrowShares;

    // LTV check: borrowValue <= collateralValue * maxLTV / LTV_PRECISION
    return borrowValue * LTV_PRECISION <= collateralValue * maxLTV;
}
```

## Advanced Operations

### Leveraged Positions

Increase exposure in a single transaction:

```solidity
function leveragedPosition(
    address _swapperAddress,
    uint256 _borrowAmount,
    uint256 _minCollateralReceived,
    bytes calldata _swapData
) external returns (uint256 collateralReceived);
```

**Flow:**
1. Borrow reUSD
2. Swap reUSD → collateral via swapper
3. Add swapped collateral to position

### Repay with Collateral

Reduce debt using collateral:

```solidity
function repayWithCollateral(
    address _swapperAddress,
    uint256 _collateralToSwap,
    uint256 _minAssetReceived,
    bytes calldata _swapData
) external returns (uint256 assetReceived);
```

**Flow:**
1. Remove collateral
2. Swap collateral → reUSD via swapper
3. Repay debt with swapped reUSD

## Pair Configuration

Pairs are deployed with specific parameters:

```solidity
struct ConfigData {
    address oracle;              // Price oracle
    address rateCalculator;      // Interest rate model
    uint256 maxLTV;              // e.g., 95_000 (95%)
    uint256 initialBorrowLimit;  // e.g., 1_000_000e18
    uint256 liquidationFee;      // e.g., 5_000 (5%)
    uint256 mintFee;             // Borrow fee
    uint256 protocolRedemptionFee;
}
```

## Reward Distribution

Pairs distribute multiple reward tokens to borrowers:

```solidity
// Claim rewards
function getReward(address _account, address _forwardTo) external;

// Reward tokens can include: RSUP, CRV, CVX
```

## Additional Resources

For the complete IResupplyPair interface with all functions and events, see **`references/pair-interface.md`**.
