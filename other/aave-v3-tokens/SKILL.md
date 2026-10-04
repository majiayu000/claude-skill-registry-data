---
name: Aave V3 Tokens
description: This skill should be used when the user asks about "aToken", "AToken.sol", "VariableDebtToken", "debt tokens", "scaled balance", "liquidity index", "ScaledBalanceTokenBase", or needs to understand Aave V3 token implementations.
version: 0.1.0
---

# Aave V3 Tokens

Aave V3 uses two types of tokens to track user positions: aTokens (supply positions) and Variable Debt Tokens (borrow positions). Both use scaled balances for efficient interest accrual.

## Token Overview

```
┌──────────────────────────────────────────────────────────────┐
│                      AAVE V3 TOKENS                          │
├──────────────────────────────────────────────────────────────┤
│                                                              │
│  ┌─────────────────────────────────────────────────────────┐ │
│  │                       aToken                             │ │
│  │  • Represents supplied assets + accrued interest         │ │
│  │  • 1:1 redeemable for underlying (plus interest)         │ │
│  │  • Balance automatically grows via liquidityIndex        │ │
│  │  • Transferable ERC20 (triggers collateral validation)   │ │
│  └─────────────────────────────────────────────────────────┘ │
│                                                              │
│  ┌─────────────────────────────────────────────────────────┐ │
│  │                  VariableDebtToken                       │ │
│  │  • Represents borrowed debt + accrued interest           │ │
│  │  • Balance automatically grows via variableBorrowIndex   │ │
│  │  • Non-transferable (debt is position-specific)          │ │
│  │  • Supports credit delegation                            │ │
│  └─────────────────────────────────────────────────────────┘ │
│                                                              │
└──────────────────────────────────────────────────────────────┘
```

## Scaled Balances

Both tokens use "scaled balances" for gas-efficient interest accrual:

```
┌──────────────────────────────────────────────────────────────┐
│                    SCALED BALANCE MATH                       │
├──────────────────────────────────────────────────────────────┤
│                                                              │
│  Actual Balance = Scaled Balance × Current Index             │
│                                                              │
│  For aTokens:                                                │
│    balance = scaledBalance × liquidityIndex                  │
│                                                              │
│  For Debt Tokens:                                            │
│    balance = scaledBalance × variableBorrowIndex             │
│                                                              │
│  When depositing/borrowing:                                  │
│    scaledAmount = amount / currentIndex                      │
│                                                              │
│  When withdrawing/repaying:                                  │
│    actualAmount = scaledAmount × currentIndex                │
│                                                              │
└──────────────────────────────────────────────────────────────┘
```

### Index Growth

```solidity
// Indexes are stored in "ray" (27 decimals)
// They grow over time based on interest rates

// Liquidity Index (for suppliers)
// Starts at 1e27 (1 ray)
// Grows based on currentLiquidityRate

// Variable Borrow Index (for borrowers)
// Starts at 1e27 (1 ray)
// Grows based on currentVariableBorrowRate

// Example:
// If liquidityIndex = 1.05e27
// And scaledBalance = 100e18
// Then actualBalance = 100e18 × 1.05e27 / 1e27 = 105e18
```

## AToken

### Contract Structure

```solidity
abstract contract AToken is
    VersionedInitializable,
    ScaledBalanceTokenBase,
    EIP712Base,
    IAToken
{
    using WadRayMath for uint256;

    address internal _treasury;
    address internal _underlyingAsset;

    constructor(IPool pool) ScaledBalanceTokenBase(pool, 'ATOKEN_IMPL', 'ATOKEN_IMPL', 0) {}
}
```

### Key Functions

```solidity
interface IAToken is IERC20, IScaledBalanceToken {
    /// @notice Mint aTokens to user
    /// @param caller The address performing the mint
    /// @param onBehalfOf The recipient of the aTokens
    /// @param amount The amount of underlying to mint for
    /// @param index The current liquidity index
    /// @return True if this is the first mint for onBehalfOf
    function mint(
        address caller,
        address onBehalfOf,
        uint256 amount,
        uint256 index
    ) external returns (bool);

    /// @notice Burn aTokens and transfer underlying
    /// @param from The owner of the aTokens
    /// @param receiverOfUnderlying The recipient of underlying
    /// @param amount The amount of underlying to withdraw
    /// @param index The current liquidity index
    function burn(
        address from,
        address receiverOfUnderlying,
        uint256 amount,
        uint256 index
    ) external;

    /// @notice Mint to treasury for protocol fees
    function mintToTreasury(uint256 amount, uint256 index) external;

    /// @notice Transfer aTokens during liquidation
    function transferOnLiquidation(address from, address to, uint256 value) external;

    /// @notice Transfer underlying (used for borrows)
    function transferUnderlyingTo(address target, uint256 amount) external;

    /// @notice Get the underlying asset address
    function UNDERLYING_ASSET_ADDRESS() external view returns (address);

    /// @notice Get the treasury address
    function RESERVE_TREASURY_ADDRESS() external view returns (address);
}
```

### Balance Calculation

```solidity
/// @notice Returns the actual balance including accrued interest
function balanceOf(address user) public view override returns (uint256) {
    return super.balanceOf(user).rayMul(POOL.getReserveNormalizedIncome(_underlyingAsset));
}

/// @notice Returns total supply including accrued interest
function totalSupply() public view override returns (uint256) {
    uint256 currentSupplyScaled = super.totalSupply();
    if (currentSupplyScaled == 0) {
        return 0;
    }
    return currentSupplyScaled.rayMul(POOL.getReserveNormalizedIncome(_underlyingAsset));
}
```

### Transfer Validation

aToken transfers trigger health factor validation:

```solidity
function _transfer(address from, address to, uint256 amount, bool validate) internal virtual {
    address underlyingAsset = _underlyingAsset;
    uint256 index = POOL.getReserveNormalizedIncome(underlyingAsset);

    uint256 fromBalanceBefore = super.balanceOf(from).rayMul(index);
    uint256 toBalanceBefore = super.balanceOf(to).rayMul(index);

    super._transfer(from, to, amount, index);

    // Validate health factor if needed
    if (validate) {
        POOL.finalizeTransfer(underlyingAsset, from, to, amount, fromBalanceBefore, toBalanceBefore);
    }

    emit BalanceTransfer(from, to, amount.rayDiv(index), index);
}
```

## VariableDebtToken

### Contract Structure

```solidity
abstract contract VariableDebtToken is
    DebtTokenBase,
    ScaledBalanceTokenBase,
    IVariableDebtToken
{
    using WadRayMath for uint256;

    constructor(IPool pool) ScaledBalanceTokenBase(pool, 'VARIABLE_DEBT_TOKEN_IMPL', 'VARIABLE_DEBT_TOKEN_IMPL', 0) {}
}
```

### Key Functions

```solidity
interface IVariableDebtToken is IScaledBalanceToken {
    /// @notice Mint debt tokens
    /// @param user The address initiating the borrow
    /// @param onBehalfOf The recipient of the debt
    /// @param amount The amount of debt to mint
    /// @param index The current variable borrow index
    /// @return True if this is first borrow, scaled amount minted
    function mint(
        address user,
        address onBehalfOf,
        uint256 amount,
        uint256 index
    ) external returns (bool, uint256);

    /// @notice Burn debt tokens when repaying
    /// @param from The address repaying
    /// @param amount The amount to burn
    /// @param index The current variable borrow index
    /// @return The scaled amount burned
    function burn(address from, uint256 amount, uint256 index) external returns (uint256);

    /// @notice Get the underlying asset
    function UNDERLYING_ASSET_ADDRESS() external view returns (address);
}
```

### Non-Transferability

```solidity
/// @notice Debt tokens cannot be transferred
function transfer(address, uint256) external pure override returns (bool) {
    revert(Errors.OPERATION_NOT_SUPPORTED);
}

function transferFrom(address, address, uint256) external pure override returns (bool) {
    revert(Errors.OPERATION_NOT_SUPPORTED);
}

function approve(address, uint256) external pure override returns (bool) {
    revert(Errors.OPERATION_NOT_SUPPORTED);
}
```

## Credit Delegation

Debt tokens support credit delegation, allowing one user to borrow on behalf of another:

```solidity
interface ICreditDelegationToken {
    /// @notice Delegate borrowing power to another address
    /// @param delegatee The address receiving delegation
    /// @param amount The maximum amount they can borrow
    function approveDelegation(address delegatee, uint256 amount) external;

    /// @notice Check delegation allowance
    function borrowAllowance(address fromUser, address toUser) external view returns (uint256);
}

// Borrow with delegation
function borrow(
    address asset,
    uint256 amount,
    uint256 interestRateMode,
    uint16 referralCode,
    address onBehalfOf  // Can be different from msg.sender if delegated
) external;
```

## ScaledBalanceTokenBase

Base contract for scaled balance tokens:

```solidity
abstract contract ScaledBalanceTokenBase is IncentivizedERC20, IScaledBalanceToken {
    /// @notice Returns the scaled balance (excluding interest)
    function scaledBalanceOf(address user) external view override returns (uint256) {
        return super.balanceOf(user);
    }

    /// @notice Returns the scaled total supply
    function scaledTotalSupply() public view virtual override returns (uint256) {
        return super.totalSupply();
    }

    /// @notice Returns scaled balance and supply for snapshot
    function getScaledUserBalanceAndSupply(address user) external view override returns (uint256, uint256) {
        return (super.balanceOf(user), super.totalSupply());
    }

    /// @notice Mint scaled tokens
    function _mintScaled(
        address caller,
        address onBehalfOf,
        uint256 amount,
        uint256 index
    ) internal returns (bool) {
        uint256 amountScaled = amount.rayDiv(index);
        require(amountScaled != 0, Errors.INVALID_MINT_AMOUNT);

        uint256 scaledBalance = super.balanceOf(onBehalfOf);
        uint256 balanceIncrease = scaledBalance.rayMul(index) -
            scaledBalance.rayMul(_userState[onBehalfOf].additionalData);

        _userState[onBehalfOf].additionalData = index.toUint128();
        _mint(onBehalfOf, amountScaled.toUint128());

        emit Transfer(address(0), onBehalfOf, amount);
        emit Mint(caller, onBehalfOf, amount, balanceIncrease, index);

        return scaledBalance == 0;  // True if first mint
    }

    /// @notice Burn scaled tokens
    function _burnScaled(
        address user,
        address target,
        uint256 amount,
        uint256 index
    ) internal {
        uint256 amountScaled = amount.rayDiv(index);
        require(amountScaled != 0, Errors.INVALID_BURN_AMOUNT);

        uint256 scaledBalance = super.balanceOf(user);
        uint256 balanceIncrease = scaledBalance.rayMul(index) -
            scaledBalance.rayMul(_userState[user].additionalData);

        _userState[user].additionalData = index.toUint128();
        _burn(user, amountScaled.toUint128());

        emit Transfer(user, address(0), amount);
        emit Burn(user, target, amount, balanceIncrease, index);
    }
}
```

## WadRayMath

Math library for interest calculations:

```solidity
library WadRayMath {
    uint256 internal constant WAD = 1e18;
    uint256 internal constant RAY = 1e27;

    /// @notice Multiply in ray precision
    function rayMul(uint256 a, uint256 b) internal pure returns (uint256) {
        return (a * b + RAY / 2) / RAY;
    }

    /// @notice Divide in ray precision
    function rayDiv(uint256 a, uint256 b) internal pure returns (uint256) {
        return (a * RAY + b / 2) / b;
    }

    /// @notice Convert wad to ray
    function wadToRay(uint256 a) internal pure returns (uint256) {
        return a * (RAY / WAD);
    }

    /// @notice Convert ray to wad
    function rayToWad(uint256 a) internal pure returns (uint256) {
        return (a + RAY / WAD / 2) / (RAY / WAD);
    }
}
```

## Token Initialization

Tokens are initialized when a reserve is listed:

```solidity
function initialize(
    IPool initializingPool,
    address treasury,
    address underlyingAsset,
    IAaveIncentivesController incentivesController,
    uint8 aTokenDecimals,
    string calldata aTokenName,
    string calldata aTokenSymbol,
    bytes calldata params
) public virtual;
```

## Events

```solidity
// aToken events
event Mint(address indexed caller, address indexed onBehalfOf, uint256 value, uint256 balanceIncrease, uint256 index);
event Burn(address indexed from, address indexed target, uint256 value, uint256 balanceIncrease, uint256 index);
event BalanceTransfer(address indexed from, address indexed to, uint256 value, uint256 index);

// Debt token events
event Mint(address indexed caller, address indexed onBehalfOf, uint256 value, uint256 balanceIncrease, uint256 index);
event Burn(address indexed from, address indexed target, uint256 value, uint256 balanceIncrease, uint256 index);
event BorrowAllowanceDelegated(address indexed fromUser, address indexed toUser, address indexed asset, uint256 amount);
```

## Reference Files

- `src/contracts/protocol/tokenization/AToken.sol` - aToken implementation
- `src/contracts/protocol/tokenization/VariableDebtToken.sol` - Debt token implementation
- `src/contracts/protocol/tokenization/base/ScaledBalanceTokenBase.sol` - Scaled balance base
- `@crane/contracts/external/aave-v3-origin/contracts/protocol/tokenization/base/IncentivizedERC20.sol` - ERC20 with incentives
- `src/contracts/protocol/libraries/math/WadRayMath.sol` - Math library
- `@crane/contracts/external/aave-v3-origin/contracts/extensions/stata-token/interfaces/IAToken.sol` - aToken interface
- `@crane/contracts/external/aave-v3-origin/contracts/interfaces/IVariableDebtToken.sol` - Debt token interface
