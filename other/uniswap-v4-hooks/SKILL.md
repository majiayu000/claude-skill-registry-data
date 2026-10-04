---
name: Uniswap V4 Hooks
description: This skill should be used when the user asks about "hooks", "beforeSwap", "afterSwap", "hook permissions", "BaseHook", "hook callbacks", "HookMiner", or needs to understand the V4 hook system.
version: 0.1.0
---

# Uniswap V4 Hooks

## Overview

Hooks are external contracts that receive callbacks at key points in pool operations. They enable developers to customize pool behavior—implementing custom fees, access control, oracles, and more.

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                            HOOK SYSTEM                                       │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│  Permission Encoding (in hook address least significant bits):              │
│  ┌──────────────────────────────────────────────────────────────────────┐   │
│  │  Bit 13: BEFORE_INITIALIZE                                           │   │
│  │  Bit 12: AFTER_INITIALIZE                                            │   │
│  │  Bit 11: BEFORE_ADD_LIQUIDITY                                        │   │
│  │  Bit 10: AFTER_ADD_LIQUIDITY                                         │   │
│  │  Bit  9: BEFORE_REMOVE_LIQUIDITY                                     │   │
│  │  Bit  8: AFTER_REMOVE_LIQUIDITY                                      │   │
│  │  Bit  7: BEFORE_SWAP                                                 │   │
│  │  Bit  6: AFTER_SWAP                                                  │   │
│  │  Bit  5: BEFORE_DONATE                                               │   │
│  │  Bit  4: AFTER_DONATE                                                │   │
│  │  Bit  3: BEFORE_SWAP_RETURNS_DELTA                                   │   │
│  │  Bit  2: AFTER_SWAP_RETURNS_DELTA                                    │   │
│  │  Bit  1: AFTER_ADD_LIQUIDITY_RETURNS_DELTA                           │   │
│  │  Bit  0: AFTER_REMOVE_LIQUIDITY_RETURNS_DELTA                        │   │
│  └──────────────────────────────────────────────────────────────────────┘   │
│                                                                              │
│  Example Address: 0x...00000000000000000000000000000000000000C0              │
│                   (binary: ...11000000)                                      │
│                   = BEFORE_SWAP (bit 7) + AFTER_SWAP (bit 6) enabled        │
│                                                                              │
└─────────────────────────────────────────────────────────────────────────────┘
```

## Hook Interface

```solidity
interface IHooks {
    /// @notice Called before pool initialization
    function beforeInitialize(address sender, PoolKey calldata key, uint160 sqrtPriceX96)
        external
        returns (bytes4);

    /// @notice Called after pool initialization
    function afterInitialize(address sender, PoolKey calldata key, uint160 sqrtPriceX96, int24 tick)
        external
        returns (bytes4);

    /// @notice Called before adding liquidity
    function beforeAddLiquidity(
        address sender,
        PoolKey calldata key,
        IPoolManager.ModifyLiquidityParams calldata params,
        bytes calldata hookData
    ) external returns (bytes4);

    /// @notice Called after adding liquidity
    function afterAddLiquidity(
        address sender,
        PoolKey calldata key,
        IPoolManager.ModifyLiquidityParams calldata params,
        BalanceDelta delta,
        BalanceDelta feesAccrued,
        bytes calldata hookData
    ) external returns (bytes4, BalanceDelta hookDelta);

    /// @notice Called before removing liquidity
    function beforeRemoveLiquidity(
        address sender,
        PoolKey calldata key,
        IPoolManager.ModifyLiquidityParams calldata params,
        bytes calldata hookData
    ) external returns (bytes4);

    /// @notice Called after removing liquidity
    function afterRemoveLiquidity(
        address sender,
        PoolKey calldata key,
        IPoolManager.ModifyLiquidityParams calldata params,
        BalanceDelta delta,
        BalanceDelta feesAccrued,
        bytes calldata hookData
    ) external returns (bytes4, BalanceDelta hookDelta);

    /// @notice Called before a swap
    function beforeSwap(
        address sender,
        PoolKey calldata key,
        IPoolManager.SwapParams calldata params,
        bytes calldata hookData
    ) external returns (bytes4, BeforeSwapDelta, uint24 lpFeeOverride);

    /// @notice Called after a swap
    function afterSwap(
        address sender,
        PoolKey calldata key,
        IPoolManager.SwapParams calldata params,
        BalanceDelta delta,
        bytes calldata hookData
    ) external returns (bytes4, int128 hookDeltaUnspecified);

    /// @notice Called before a donation
    function beforeDonate(
        address sender,
        PoolKey calldata key,
        uint256 amount0,
        uint256 amount1,
        bytes calldata hookData
    ) external returns (bytes4);

    /// @notice Called after a donation
    function afterDonate(
        address sender,
        PoolKey calldata key,
        uint256 amount0,
        uint256 amount1,
        bytes calldata hookData
    ) external returns (bytes4);
}
```

## Permission Flags

```solidity
library Hooks {
    uint160 internal constant BEFORE_INITIALIZE_FLAG = 1 << 13;
    uint160 internal constant AFTER_INITIALIZE_FLAG = 1 << 12;
    uint160 internal constant BEFORE_ADD_LIQUIDITY_FLAG = 1 << 11;
    uint160 internal constant AFTER_ADD_LIQUIDITY_FLAG = 1 << 10;
    uint160 internal constant BEFORE_REMOVE_LIQUIDITY_FLAG = 1 << 9;
    uint160 internal constant AFTER_REMOVE_LIQUIDITY_FLAG = 1 << 8;
    uint160 internal constant BEFORE_SWAP_FLAG = 1 << 7;
    uint160 internal constant AFTER_SWAP_FLAG = 1 << 6;
    uint160 internal constant BEFORE_DONATE_FLAG = 1 << 5;
    uint160 internal constant AFTER_DONATE_FLAG = 1 << 4;
    uint160 internal constant BEFORE_SWAP_RETURNS_DELTA_FLAG = 1 << 3;
    uint160 internal constant AFTER_SWAP_RETURNS_DELTA_FLAG = 1 << 2;
    uint160 internal constant AFTER_ADD_LIQUIDITY_RETURNS_DELTA_FLAG = 1 << 1;
    uint160 internal constant AFTER_REMOVE_LIQUIDITY_RETURNS_DELTA_FLAG = 1 << 0;

    /// @notice Check if hook has a specific permission
    function hasPermission(IHooks self, uint160 flag) internal pure returns (bool) {
        return uint160(address(self)) & flag != 0;
    }

    /// @notice Validate hook address matches intended permissions
    function validateHookPermissions(IHooks hookAddress, PoolKey memory key) internal pure {
        // Hooks contract is responsible for validating its own address
        // matches getHookPermissions() in constructor
    }
}
```

## BaseHook (Periphery)

The recommended base contract for implementing hooks:

```solidity
abstract contract BaseHook is IHooks, SafeCallback {
    error HookNotImplemented();

    constructor(IPoolManager _manager) SafeCallback(_manager) {
        validateHookAddress(this);
    }

    /// @dev Override to define which callbacks this hook uses
    function getHookPermissions() public pure virtual returns (Hooks.Permissions memory);

    /// @dev Validates the deployed address matches intended permissions
    function validateHookAddress(BaseHook _this) internal pure virtual {
        Hooks.Permissions memory permissions = _this.getHookPermissions();
        // Check each permission flag matches address encoding
        // Reverts if mismatch
    }

    // Default implementations revert - override what you need

    function beforeInitialize(address, PoolKey calldata, uint160) external virtual returns (bytes4) {
        revert HookNotImplemented();
    }

    function afterInitialize(address, PoolKey calldata, uint160, int24) external virtual returns (bytes4) {
        revert HookNotImplemented();
    }

    function beforeAddLiquidity(address, PoolKey calldata, IPoolManager.ModifyLiquidityParams calldata, bytes calldata)
        external virtual returns (bytes4)
    {
        revert HookNotImplemented();
    }

    function afterAddLiquidity(
        address,
        PoolKey calldata,
        IPoolManager.ModifyLiquidityParams calldata,
        BalanceDelta,
        BalanceDelta,
        bytes calldata
    ) external virtual returns (bytes4, BalanceDelta) {
        revert HookNotImplemented();
    }

    // ... similar for other callbacks
}
```

## Implementing a Hook

### Example: Swap Fee Hook

```solidity
contract DynamicFeeHook is BaseHook {
    using PoolIdLibrary for PoolKey;

    mapping(PoolId => uint24) public poolFees;

    constructor(IPoolManager _manager) BaseHook(_manager) {}

    function getHookPermissions() public pure override returns (Hooks.Permissions memory) {
        return Hooks.Permissions({
            beforeInitialize: false,
            afterInitialize: true,
            beforeAddLiquidity: false,
            afterAddLiquidity: false,
            beforeRemoveLiquidity: false,
            afterRemoveLiquidity: false,
            beforeSwap: true,
            afterSwap: false,
            beforeDonate: false,
            afterDonate: false,
            beforeSwapReturnDelta: false,
            afterSwapReturnDelta: false,
            afterAddLiquidityReturnDelta: false,
            afterRemoveLiquidityReturnDelta: false
        });
    }

    function afterInitialize(
        address,
        PoolKey calldata key,
        uint160,
        int24
    ) external override returns (bytes4) {
        // Set initial fee
        poolFees[key.toId()] = 3000; // 0.3%
        return IHooks.afterInitialize.selector;
    }

    function beforeSwap(
        address,
        PoolKey calldata key,
        IPoolManager.SwapParams calldata,
        bytes calldata
    ) external override returns (bytes4, BeforeSwapDelta, uint24) {
        // Return dynamic fee with override flag
        uint24 fee = poolFees[key.toId()] | LPFeeLibrary.OVERRIDE_FEE_FLAG;

        return (
            IHooks.beforeSwap.selector,
            BeforeSwapDeltaLibrary.ZERO_DELTA,
            fee
        );
    }

    // Admin function to update fee
    function setFee(PoolKey calldata key, uint24 newFee) external onlyOwner {
        poolFees[key.toId()] = newFee;
    }
}
```

### Example: Access Control Hook

```solidity
contract WhitelistHook is BaseHook {
    mapping(address => bool) public whitelist;

    constructor(IPoolManager _manager) BaseHook(_manager) {}

    function getHookPermissions() public pure override returns (Hooks.Permissions memory) {
        return Hooks.Permissions({
            beforeInitialize: false,
            afterInitialize: false,
            beforeAddLiquidity: true,
            afterAddLiquidity: false,
            beforeRemoveLiquidity: false,
            afterRemoveLiquidity: false,
            beforeSwap: true,
            afterSwap: false,
            beforeDonate: false,
            afterDonate: false,
            beforeSwapReturnDelta: false,
            afterSwapReturnDelta: false,
            afterAddLiquidityReturnDelta: false,
            afterRemoveLiquidityReturnDelta: false
        });
    }

    function beforeAddLiquidity(
        address sender,
        PoolKey calldata,
        IPoolManager.ModifyLiquidityParams calldata,
        bytes calldata
    ) external view override returns (bytes4) {
        require(whitelist[sender], "Not whitelisted");
        return IHooks.beforeAddLiquidity.selector;
    }

    function beforeSwap(
        address sender,
        PoolKey calldata,
        IPoolManager.SwapParams calldata,
        bytes calldata
    ) external view override returns (bytes4, BeforeSwapDelta, uint24) {
        require(whitelist[sender], "Not whitelisted");
        return (IHooks.beforeSwap.selector, BeforeSwapDeltaLibrary.ZERO_DELTA, 0);
    }
}
```

## HookMiner

To deploy a hook to a specific address with correct permission bits:

```solidity
library HookMiner {
    /// @notice Find a salt that produces a hook address with desired flags
    /// @param deployer The address that will deploy the hook
    /// @param flags The desired permission flags
    /// @param creationCode The hook contract creation code
    /// @param constructorArgs The encoded constructor arguments
    /// @return hookAddress The computed hook address
    /// @return salt The salt to use with CREATE2
    function find(
        address deployer,
        uint160 flags,
        bytes memory creationCode,
        bytes memory constructorArgs
    ) internal pure returns (address hookAddress, bytes32 salt) {
        bytes memory initCodeHash = abi.encodePacked(creationCode, constructorArgs);
        bytes32 initCodeHashBytes = keccak256(initCodeHash);

        // Brute force search for valid salt
        for (uint256 i = 0; i < type(uint256).max; i++) {
            salt = bytes32(i);
            hookAddress = computeAddress(deployer, salt, initCodeHashBytes);

            // Check if address has correct flags
            if (uint160(hookAddress) & flags == flags) {
                // Also check no unwanted flags are set
                if (uint160(hookAddress) & ~flags == 0) {
                    return (hookAddress, salt);
                }
            }
        }
        revert("No valid salt found");
    }

    function computeAddress(address deployer, bytes32 salt, bytes32 initCodeHash)
        internal
        pure
        returns (address)
    {
        return address(
            uint160(
                uint256(
                    keccak256(
                        abi.encodePacked(bytes1(0xff), deployer, salt, initCodeHash)
                    )
                )
            )
        );
    }
}
```

### Deploying a Hook

```solidity
// Find salt for desired permissions
uint160 flags = Hooks.BEFORE_SWAP_FLAG | Hooks.AFTER_SWAP_FLAG;
(address hookAddress, bytes32 salt) = HookMiner.find(
    address(this),
    flags,
    type(MyHook).creationCode,
    abi.encode(poolManager)
);

// Deploy with CREATE2
MyHook hook = new MyHook{salt: salt}(poolManager);
require(address(hook) == hookAddress, "Address mismatch");
```

## BeforeSwapDelta

Hooks can modify swap amounts via `beforeSwap`:

```solidity
/// @notice Packed delta for beforeSwap modifications
/// Upper 128 bits: delta in specified currency (input for exactIn, output for exactOut)
/// Lower 128 bits: delta in unspecified currency
type BeforeSwapDelta is int256;

library BeforeSwapDeltaLibrary {
    BeforeSwapDelta public constant ZERO_DELTA = BeforeSwapDelta.wrap(0);

    function getSpecifiedDelta(BeforeSwapDelta delta) internal pure returns (int128) {
        return int128(BeforeSwapDelta.unwrap(delta) >> 128);
    }

    function getUnspecifiedDelta(BeforeSwapDelta delta) internal pure returns (int128) {
        return int128(BeforeSwapDelta.unwrap(delta));
    }
}
```

## Hook Callback Flow

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                         SWAP HOOK FLOW                                       │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│  1. PoolManager.swap() called                                               │
│     │                                                                        │
│     ▼                                                                        │
│  2. Check BEFORE_SWAP_FLAG in hook address                                  │
│     │                                                                        │
│     ├─ If set: call hook.beforeSwap(sender, key, params, hookData)          │
│     │          │                                                             │
│     │          ├─ Returns: (selector, BeforeSwapDelta, lpFeeOverride)       │
│     │          │                                                             │
│     │          └─ If BEFORE_SWAP_RETURNS_DELTA_FLAG:                        │
│     │               Hook delta applied to swap                               │
│     │                                                                        │
│     ▼                                                                        │
│  3. Pool.swap() executes core swap logic                                    │
│     │                                                                        │
│     ▼                                                                        │
│  4. Check AFTER_SWAP_FLAG in hook address                                   │
│     │                                                                        │
│     └─ If set: call hook.afterSwap(sender, key, params, delta, hookData)    │
│                │                                                             │
│                ├─ Returns: (selector, hookDeltaUnspecified)                 │
│                │                                                             │
│                └─ If AFTER_SWAP_RETURNS_DELTA_FLAG:                         │
│                     Hook delta applied to unspecified currency               │
│                                                                              │
└─────────────────────────────────────────────────────────────────────────────┘
```

## Reference Files

### v4-core
- `src/interfaces/IHooks.sol` - Hook interface
- `src/libraries/Hooks.sol` - Permission handling

### v4-periphery
- `src/base/BaseHook.sol` - Hook base contract
- `src/utils/HookMiner.sol` - Address mining
