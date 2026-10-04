---
name: EVK Vault Operations
description: This skill should be used when the user asks about "deposit", "withdraw", "mint", "redeem", "eToken", "shares", "assets", "ERC-4626", "vault shares", or needs to understand EVault supply-side operations.
version: 0.1.0
---

# EVK Vault Operations (ERC-4626)

EVaults are ERC-4626 compliant vaults with lending functionality. This skill covers the supply-side operations: deposit, withdraw, mint, and redeem.

## Overview

```
┌──────────────────────────────────────────────────────────────┐
│                   ERC-4626 VAULT FLOW                        │
├──────────────────────────────────────────────────────────────┤
│                                                              │
│  User Assets (Underlying)                                    │
│       │                                                      │
│       ▼                                                      │
│  ┌─────────────────────────────────────────────────────────┐ │
│  │                     EVault                              │ │
│  │                                                         │ │
│  │   deposit(assets) ──► mint shares to receiver           │ │
│  │   mint(shares)   ──► pull assets for shares             │ │
│  │   withdraw(assets) ──► burn shares, send assets         │ │
│  │   redeem(shares)   ──► burn shares, send assets         │ │
│  │                                                         │ │
│  │   Shares = proportional claim on:                       │ │
│  │   ├── Cash (underlying in vault)                        │ │
│  │   ├── Borrows (outstanding loans + interest)            │ │
│  │   └── Less: Protocol fees                               │ │
│  │                                                         │ │
│  └─────────────────────────────────────────────────────────┘ │
│       │                                                      │
│       ▼                                                      │
│  User Shares (eTokens)                                       │
│                                                              │
└──────────────────────────────────────────────────────────────┘
```

## Share/Asset Conversion

```solidity
// Vault.sol - Core conversion logic

/// @notice Total assets managed by vault
/// @dev cash + totalBorrows (interest-accrued)
function totalAssets() public view returns (uint256) {
    VaultCache memory cache = loadVault();
    return cache.cash + cache.totalBorrows;
}

/// @notice Convert assets to shares
function convertToShares(uint256 assets) public view returns (uint256) {
    VaultCache memory cache = loadVault();
    uint256 totalAssetsVal = cache.cash + cache.totalBorrows;

    if (cache.totalShares == 0 || totalAssetsVal == 0) {
        return assets;  // 1:1 for empty vault
    }

    return assets.mulDiv(cache.totalShares, totalAssetsVal, Math.Rounding.Down);
}

/// @notice Convert shares to assets
function convertToAssets(uint256 shares) public view returns (uint256) {
    VaultCache memory cache = loadVault();
    uint256 totalAssetsVal = cache.cash + cache.totalBorrows;

    if (cache.totalShares == 0) {
        return shares;  // 1:1 for empty vault
    }

    return shares.mulDiv(totalAssetsVal, cache.totalShares, Math.Rounding.Down);
}
```

## Deposit

```solidity
/// @notice Deposit assets and receive shares
/// @param assets Amount of underlying to deposit
/// @param receiver Address to receive shares
/// @return shares Amount of shares minted
function deposit(uint256 assets, address receiver)
    external
    virtual
    override
    use(MODULE_VAULT)
    returns (uint256 shares)
{}

// In Vault.sol module
function deposit(uint256 assets, address receiver) external returns (uint256 shares) {
    // Initialize operation, accrue interest
    VaultCache memory cache = initOperation(OP_DEPOSIT);

    address account = msgSender();  // EVC-authenticated caller

    // Calculate shares
    shares = assets.mulDiv(
        cache.totalShares + 1,  // Virtual share for rounding
        cache.cash + cache.totalBorrows + 1,
        Math.Rounding.Down
    );

    if (shares == 0) revert InsufficientDeposit();

    // Check supply cap
    uint256 newTotalShares = cache.totalShares + shares;
    if (newTotalShares > supplyCap()) revert SupplyCapExceeded();

    // Transfer underlying from sender
    asset().safeTransferFrom(account, address(this), assets);

    // Update state
    cache.cash += assets;
    cache.totalShares = newTotalShares;
    users[receiver].balance += shares;

    updateVault(cache);

    // Schedule vault status check
    requireVaultStatusCheck();

    emit Deposit(account, receiver, assets, shares);
}
```

## Mint

```solidity
/// @notice Mint exact shares by depositing assets
/// @param shares Exact amount of shares to mint
/// @param receiver Address to receive shares
/// @return assets Amount of underlying deposited
function mint(uint256 shares, address receiver)
    external
    virtual
    override
    use(MODULE_VAULT)
    returns (uint256 assets)
{}

// In Vault.sol module
function mint(uint256 shares, address receiver) external returns (uint256 assets) {
    VaultCache memory cache = initOperation(OP_MINT);

    address account = msgSender();

    // Calculate assets needed (round up)
    assets = shares.mulDiv(
        cache.cash + cache.totalBorrows + 1,
        cache.totalShares + 1,
        Math.Rounding.Up
    );

    // Check supply cap
    uint256 newTotalShares = cache.totalShares + shares;
    if (newTotalShares > supplyCap()) revert SupplyCapExceeded();

    // Transfer underlying
    asset().safeTransferFrom(account, address(this), assets);

    // Update state
    cache.cash += assets;
    cache.totalShares = newTotalShares;
    users[receiver].balance += shares;

    updateVault(cache);
    requireVaultStatusCheck();

    emit Deposit(account, receiver, assets, shares);
}
```

## Withdraw

```solidity
/// @notice Withdraw exact assets by burning shares
/// @param assets Exact amount of underlying to withdraw
/// @param receiver Address to receive assets
/// @param owner Owner of shares to burn
/// @return shares Amount of shares burned
function withdraw(uint256 assets, address receiver, address owner)
    external
    virtual
    override
    use(MODULE_VAULT)
    returns (uint256 shares)
{}

// In Vault.sol module
function withdraw(uint256 assets, address receiver, address owner)
    external
    returns (uint256 shares)
{
    VaultCache memory cache = initOperation(OP_WITHDRAW);

    address account = msgSender();

    // Calculate shares to burn (round up)
    shares = assets.mulDiv(
        cache.totalShares,
        cache.cash + cache.totalBorrows,
        Math.Rounding.Up
    );

    // Check liquidity
    if (assets > cache.cash) revert InsufficientCash();

    // Handle allowance if caller != owner
    if (account != owner) {
        uint256 allowed = allowance[owner][account];
        if (allowed != type(uint256).max) {
            if (allowed < shares) revert InsufficientAllowance();
            allowance[owner][account] = allowed - shares;
        }
    }

    // Check balance
    if (users[owner].balance < shares) revert InsufficientBalance();

    // Update state
    users[owner].balance -= shares;
    cache.totalShares -= shares;
    cache.cash -= assets;

    updateVault(cache);

    // Transfer underlying to receiver
    asset().safeTransfer(receiver, assets);

    // Schedule checks
    requireAccountStatusCheck(owner);  // Owner might be borrower
    requireVaultStatusCheck();

    emit Withdraw(account, receiver, owner, assets, shares);
}
```

## Redeem

```solidity
/// @notice Redeem exact shares for assets
/// @param shares Exact amount of shares to burn
/// @param receiver Address to receive assets
/// @param owner Owner of shares to burn
/// @return assets Amount of underlying received
function redeem(uint256 shares, address receiver, address owner)
    external
    virtual
    override
    use(MODULE_VAULT)
    returns (uint256 assets)
{}

// In Vault.sol module
function redeem(uint256 shares, address receiver, address owner)
    external
    returns (uint256 assets)
{
    VaultCache memory cache = initOperation(OP_REDEEM);

    address account = msgSender();

    // Calculate assets (round down - favorable to vault)
    assets = shares.mulDiv(
        cache.cash + cache.totalBorrows,
        cache.totalShares,
        Math.Rounding.Down
    );

    // Check liquidity
    if (assets > cache.cash) revert InsufficientCash();

    // Handle allowance if caller != owner
    if (account != owner) {
        uint256 allowed = allowance[owner][account];
        if (allowed != type(uint256).max) {
            if (allowed < shares) revert InsufficientAllowance();
            allowance[owner][account] = allowed - shares;
        }
    }

    // Check balance
    if (users[owner].balance < shares) revert InsufficientBalance();

    // Update state
    users[owner].balance -= shares;
    cache.totalShares -= shares;
    cache.cash -= assets;

    updateVault(cache);

    // Transfer underlying
    asset().safeTransfer(receiver, assets);

    // Schedule checks
    requireAccountStatusCheck(owner);
    requireVaultStatusCheck();

    emit Withdraw(account, receiver, owner, assets, shares);
}
```

## Max Functions

```solidity
/// @notice Maximum assets that can be deposited
function maxDeposit(address) public view returns (uint256) {
    if (vaultStorage.supplyCap == type(uint256).max) {
        return type(uint256).max;
    }

    VaultCache memory cache = loadVault();
    uint256 suppliedAssets = convertToAssets(cache.totalShares);
    uint256 cap = supplyCap();

    if (suppliedAssets >= cap) return 0;
    return cap - suppliedAssets;
}

/// @notice Maximum shares that can be minted
function maxMint(address receiver) public view returns (uint256) {
    uint256 maxAssets = maxDeposit(receiver);
    if (maxAssets == type(uint256).max) return type(uint256).max;
    return convertToShares(maxAssets);
}

/// @notice Maximum assets that can be withdrawn
function maxWithdraw(address owner) public view returns (uint256) {
    VaultCache memory cache = loadVault();
    uint256 ownerAssets = convertToAssets(users[owner].balance);

    // Limited by available cash
    return ownerAssets < cache.cash ? ownerAssets : cache.cash;
}

/// @notice Maximum shares that can be redeemed
function maxRedeem(address owner) public view returns (uint256) {
    VaultCache memory cache = loadVault();
    uint256 ownerShares = users[owner].balance;
    uint256 cashInShares = convertToShares(cache.cash);

    return ownerShares < cashInShares ? ownerShares : cashInShares;
}
```

## Preview Functions

```solidity
/// @notice Preview deposit - shares for given assets
function previewDeposit(uint256 assets) public view returns (uint256) {
    return convertToShares(assets);  // Round down
}

/// @notice Preview mint - assets needed for shares
function previewMint(uint256 shares) public view returns (uint256) {
    VaultCache memory cache = loadVault();
    return shares.mulDiv(
        cache.cash + cache.totalBorrows + 1,
        cache.totalShares + 1,
        Math.Rounding.Up
    );
}

/// @notice Preview withdraw - shares burned for assets
function previewWithdraw(uint256 assets) public view returns (uint256) {
    VaultCache memory cache = loadVault();
    return assets.mulDiv(
        cache.totalShares,
        cache.cash + cache.totalBorrows,
        Math.Rounding.Up
    );
}

/// @notice Preview redeem - assets for shares
function previewRedeem(uint256 shares) public view returns (uint256) {
    return convertToAssets(shares);  // Round down
}
```

## SKim (Donation Handling)

```solidity
/// @notice Skim excess underlying to receiver
/// @dev Handles donations or accidental transfers
function skim(uint256 amount, address receiver) external {
    VaultCache memory cache = initOperation(OP_SKIM);

    address account = msgSender();

    // Calculate actual cash from balance
    uint256 actualCash = asset().balanceOf(address(this));
    uint256 excess = actualCash - cache.cash;

    if (amount > excess) revert InsufficientExcess();
    if (amount == 0) amount = excess;

    // Transfer excess to receiver
    asset().safeTransfer(receiver, amount);

    emit Skim(account, receiver, amount);
}
```

## EVC Integration

```solidity
// Vault operations go through EVC for authenticated caller
// Example: deposit via EVC.call()

BatchItem[] memory items = new BatchItem[](1);
items[0] = BatchItem({
    targetContract: vault,
    onBehalfOfAccount: myAccount,
    value: 0,
    data: abi.encodeCall(IEVault.deposit, (amount, myAccount))
});
evc.batch(items);

// Direct call also works (EVC handles auth via msgSender())
vault.deposit(amount, receiver);
```

## Share Value Accrual

```solidity
// Share value increases as interest accrues

// Time 0:
// totalShares = 100, totalAssets = 100 USDC
// 1 share = 1 USDC

// After interest accrual:
// totalShares = 100, totalAssets = 110 USDC (10 USDC interest)
// 1 share = 1.1 USDC

// Depositor who redeems gets more than deposited
// (assuming no withdrawals/deposits in between)
```

## Events

```solidity
// Standard ERC-4626 events
event Deposit(address indexed sender, address indexed owner, uint256 assets, uint256 shares);
event Withdraw(address indexed sender, address indexed receiver, address indexed owner, uint256 assets, uint256 shares);

// EVault-specific
event Skim(address indexed sender, address indexed receiver, uint256 amount);
```

## Reference Files

- `euler-vault-kit/src/EVault/modules/Vault.sol` - Vault module
- `euler-vault-kit/src/EVault/shared/AssetTransfers.sol` - Transfer helpers
- `euler-vault-kit/src/EVault/shared/BalanceUtils.sol` - Balance utilities
