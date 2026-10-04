---
name: Balancer V3 Hooks
description: This skill should be used when the user asks about "Balancer hooks", "IHooks", "BaseHooks", "onBeforeSwap", "onAfterSwap", "dynamic swap fee", "hook adjusted amounts", "pool customization", or needs to understand the Balancer V3 hooks system.
version: 0.1.0
---

# Balancer V3 Hooks System

Hooks provide a powerful extensibility mechanism for Balancer V3 pools, allowing custom logic at key points in swap and liquidity operations.

## Overview

```
┌──────────────────────────────────────────────────────────────┐
│                    HOOKS FLOW                                │
├──────────────────────────────────────────────────────────────┤
│                                                              │
│  ┌─────────────┐    ┌─────────────┐    ┌─────────────┐      │
│  │ onBefore*   │ => │   VAULT     │ => │  onAfter*   │      │
│  │   hooks     │    │  OPERATION  │    │   hooks     │      │
│  └─────────────┘    └─────────────┘    └─────────────┘      │
│                                                              │
│  • Validation       • Core logic      • Amount adjustment   │
│  • State updates    • Math            • Fee collection      │
│  • Rate changes     • Accounting      • Events              │
│                                                              │
└──────────────────────────────────────────────────────────────┘
```

## IHooks Interface

```solidity
interface IHooks {
    // REGISTRATION
    function onRegister(
        address factory,
        address pool,
        TokenConfig[] memory tokenConfig,
        LiquidityManagement calldata liquidityManagement
    ) external returns (bool success);

    function getHookFlags() external view returns (HookFlags memory);

    // INITIALIZATION
    function onBeforeInitialize(uint256[] memory exactAmountsIn, bytes memory userData)
        external returns (bool success);

    function onAfterInitialize(
        uint256[] memory exactAmountsIn,
        uint256 bptAmountOut,
        bytes memory userData
    ) external returns (bool success);

    // ADD LIQUIDITY
    function onBeforeAddLiquidity(
        address router,
        address pool,
        AddLiquidityKind kind,
        uint256[] memory maxAmountsInScaled18,
        uint256 minBptAmountOut,
        uint256[] memory balancesScaled18,
        bytes memory userData
    ) external returns (bool success);

    function onAfterAddLiquidity(
        address router,
        address pool,
        AddLiquidityKind kind,
        uint256[] memory amountsInScaled18,
        uint256[] memory amountsInRaw,
        uint256 bptAmountOut,
        uint256[] memory balancesScaled18,
        bytes memory userData
    ) external returns (bool success, uint256[] memory hookAdjustedAmountsInRaw);

    // REMOVE LIQUIDITY
    function onBeforeRemoveLiquidity(
        address router,
        address pool,
        RemoveLiquidityKind kind,
        uint256 maxBptAmountIn,
        uint256[] memory minAmountsOutScaled18,
        uint256[] memory balancesScaled18,
        bytes memory userData
    ) external returns (bool success);

    function onAfterRemoveLiquidity(
        address router,
        address pool,
        RemoveLiquidityKind kind,
        uint256 bptAmountIn,
        uint256[] memory amountsOutScaled18,
        uint256[] memory amountsOutRaw,
        uint256[] memory balancesScaled18,
        bytes memory userData
    ) external returns (bool success, uint256[] memory hookAdjustedAmountsOutRaw);

    // SWAP
    function onBeforeSwap(PoolSwapParams calldata params, address pool)
        external returns (bool success);

    function onAfterSwap(AfterSwapParams calldata params)
        external returns (bool success, uint256 hookAdjustedAmountCalculatedRaw);

    // DYNAMIC FEE
    function onComputeDynamicSwapFeePercentage(
        PoolSwapParams calldata params,
        address pool,
        uint256 staticSwapFeePercentage
    ) external view returns (bool success, uint256 dynamicSwapFeePercentage);
}
```

## HookFlags

```solidity
struct HookFlags {
    bool enableHookAdjustedAmounts;      // Allow hooks to modify calculated amounts
    bool shouldCallBeforeInitialize;
    bool shouldCallAfterInitialize;
    bool shouldCallComputeDynamicSwapFee;
    bool shouldCallBeforeSwap;
    bool shouldCallAfterSwap;
    bool shouldCallBeforeAddLiquidity;
    bool shouldCallAfterAddLiquidity;
    bool shouldCallBeforeRemoveLiquidity;
    bool shouldCallAfterRemoveLiquidity;
}
```

## BaseHooks

```solidity
abstract contract BaseHooks is IHooks, VaultGuard {
    constructor(IVault vault) VaultGuard(vault) {}

    // Only the Vault can call hook functions
    modifier onlyVault() {
        if (msg.sender != address(_vault)) revert SenderIsNotVault(msg.sender);
        _;
    }

    // Default implementations (return true, no changes)
    function onRegister(...) external virtual returns (bool) { return true; }
    function onBeforeInitialize(...) external virtual returns (bool) { return false; }
    function onAfterInitialize(...) external virtual returns (bool) { return false; }
    // ... etc
}
```

## Dynamic Swap Fees

```solidity
// Example: Time-weighted dynamic fee
function onComputeDynamicSwapFeePercentage(
    PoolSwapParams calldata params,
    address pool,
    uint256 staticSwapFeePercentage
) external view override onlyVault returns (bool, uint256) {
    // Increase fee during high volatility
    uint256 priceImpact = _calculatePriceImpact(params);

    if (priceImpact > HIGH_IMPACT_THRESHOLD) {
        return (true, staticSwapFeePercentage * 2);  // Double the fee
    }

    return (true, staticSwapFeePercentage);
}
```

## Hook Adjusted Amounts

When `enableHookAdjustedAmounts = true`, after hooks can modify amounts:

```solidity
// Example: Take an extra fee in afterSwap
function onAfterSwap(
    AfterSwapParams calldata params
) external override onlyVault returns (bool, uint256) {
    // Take 0.1% hook fee
    uint256 hookFee = params.amountCalculatedRaw / 1000;
    uint256 adjustedAmount = params.amountCalculatedRaw - hookFee;

    // Transfer hook fee somewhere
    _collectFee(params.tokenOut, hookFee);

    return (true, adjustedAmount);
}
```

**Important**: If `enableHookAdjustedAmounts = true`, the pool MUST set `disableUnbalancedLiquidity = true` for safety.

## Hook Registration

```solidity
// During pool registration, hook is validated
function onRegister(
    address factory,
    address pool,
    TokenConfig[] memory tokenConfig,
    LiquidityManagement calldata liquidityManagement
) external override onlyVault returns (bool) {
    // Validate this hook should work with this factory/pool
    if (factory != EXPECTED_FACTORY) {
        return false;
    }

    // Validate configuration
    if (tokenConfig.length < MIN_TOKENS) {
        return false;
    }

    // Setup hook state for this pool
    _registeredPools[pool] = true;

    return true;
}
```

## Common Hook Patterns

### 1. Access Control Hook

```solidity
contract WhitelistHook is BaseHooks {
    mapping(address => bool) public whitelist;

    function onBeforeSwap(PoolSwapParams calldata params, address pool)
        external override onlyVault returns (bool)
    {
        if (!whitelist[params.router]) {
            revert NotWhitelisted(params.router);
        }
        return true;
    }
}
```

### 2. Oracle Integration Hook

```solidity
contract OracleHook is BaseHooks {
    function onBeforeSwap(PoolSwapParams calldata params, address pool)
        external override onlyVault returns (bool)
    {
        // Update TWAP oracle
        _updateOracle(pool, params);
        return true;
    }

    function onAfterSwap(AfterSwapParams calldata params)
        external override onlyVault returns (bool, uint256)
    {
        // Record price after swap
        _recordPrice(params.pool, params.tokenIn, params.tokenOut);
        return (true, params.amountCalculatedRaw);
    }
}
```

### 3. Fee Distribution Hook

```solidity
contract PartnerFeeHook is BaseHooks {
    mapping(address => address) public poolPartners;

    function onAfterSwap(AfterSwapParams calldata params)
        external override onlyVault returns (bool, uint256)
    {
        address partner = poolPartners[params.pool];
        if (partner != address(0)) {
            // Send portion of swap to partner
            uint256 partnerFee = params.amountCalculatedRaw / 100; // 1%
            _sendFee(partner, params.tokenOut, partnerFee);
            return (true, params.amountCalculatedRaw - partnerFee);
        }
        return (true, params.amountCalculatedRaw);
    }
}
```

### 4. Surge Pricing Hook

```solidity
contract SurgeHook is BaseHooks {
    function onComputeDynamicSwapFeePercentage(
        PoolSwapParams calldata params,
        address pool,
        uint256 staticSwapFeePercentage
    ) external view override onlyVault returns (bool, uint256) {
        // Increase fee when balance is low
        uint256 balance = params.balancesScaled18[params.indexOut];
        uint256 amountOut = _estimateAmountOut(params);

        if (amountOut > balance / 10) {
            // More than 10% of balance - surge pricing
            return (true, staticSwapFeePercentage * 3);
        }

        return (true, staticSwapFeePercentage);
    }
}
```

## AfterSwapParams

```solidity
struct AfterSwapParams {
    SwapKind kind;
    IERC20 tokenIn;
    IERC20 tokenOut;
    uint256 amountInScaled18;
    uint256 amountOutScaled18;
    uint256 tokenInBalanceScaled18;
    uint256 tokenOutBalanceScaled18;
    uint256 amountCalculatedScaled18;
    uint256 amountCalculatedRaw;
    address router;
    address pool;
    bytes userData;
}
```

## Hook Storage

Hooks can maintain their own state:

```solidity
contract StatefulHook is BaseHooks {
    // Per-pool data
    mapping(address => uint256) public lastSwapTimestamp;
    mapping(address => uint256) public swapCount;

    function onAfterSwap(AfterSwapParams calldata params)
        external override onlyVault returns (bool, uint256)
    {
        lastSwapTimestamp[params.pool] = block.timestamp;
        swapCount[params.pool]++;
        return (true, params.amountCalculatedRaw);
    }
}
```

## Security Considerations

1. **Only Vault**: All hook functions must verify `msg.sender == vault`
2. **Reentrancy**: Hooks are called mid-operation - be careful with external calls
3. **Gas Limits**: Hooks add gas cost to every operation
4. **State Changes**: beforeSwap hooks can modify pool rates/balances
5. **Amount Adjustment**: Only enabled when explicitly configured

## Reference Files

- `pkg/interfaces/contracts/vault/IHooks.sol` - Interface definition
- `pkg/vault/contracts/BaseHooks.sol` - Base implementation
- `pkg/pool-hooks/` - Example hook implementations
  - `MevCaptureHook.sol` - MEV protection
  - `SurgeHook.sol` - Dynamic fee based on pool stress
