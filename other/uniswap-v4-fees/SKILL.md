---
name: Uniswap V4 Fees
description: This skill should be used when the user asks about "fees", "LP fee", "dynamic fees", "protocol fees", "fee override", "LPFeeLibrary", or needs to understand the V4 fee system.
version: 0.1.0
---

# Uniswap V4 Fees

## Overview

V4 supports both static and dynamic LP fees, plus protocol fees. Dynamic fees enable hooks to implement custom fee logic—TWAP-based fees, volume-responsive fees, time-weighted fees, and more.

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                            FEE SYSTEM                                        │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│  Fee Types:                                                                 │
│  ┌──────────────────────────────────────────────────────────────────────┐   │
│  │  1. Static LP Fee                                                    │   │
│  │     - Set in PoolKey.fee at initialization                           │   │
│  │     - Cannot be changed after pool creation                          │   │
│  │     - Range: 0 to 1,000,000 (0% to 100%)                             │   │
│  │                                                                       │   │
│  │  2. Dynamic LP Fee                                                   │   │
│  │     - Enabled by setting fee = 0x800000 (DYNAMIC_FEE_FLAG)           │   │
│  │     - Hook controls fee via:                                         │   │
│  │       a) beforeSwap return value (per-swap override)                 │   │
│  │       b) updateDynamicLPFee() call (persistent update)               │   │
│  │                                                                       │   │
│  │  3. Protocol Fee                                                     │   │
│  │     - Percentage of LP fee taken by protocol                         │   │
│  │     - Set by protocol fee controller                                 │   │
│  │     - Stored in Slot0 (12 bits per direction)                        │   │
│  └──────────────────────────────────────────────────────────────────────┘   │
│                                                                              │
│  Fee Flow:                                                                  │
│  ┌──────────────────────────────────────────────────────────────────────┐   │
│  │  Swap Amount In                                                      │   │
│  │        │                                                              │   │
│  │        ├──► LP Fee (e.g., 0.3%)                                      │   │
│  │        │         │                                                    │   │
│  │        │         ├──► Protocol Fee (e.g., 10% of LP fee)             │   │
│  │        │         │         = 0.03% of swap                           │   │
│  │        │         │                                                    │   │
│  │        │         └──► LPs receive remainder                          │   │
│  │        │               = 0.27% of swap                                │   │
│  │        │                                                              │   │
│  │        └──► Remaining goes to swap output                            │   │
│  └──────────────────────────────────────────────────────────────────────┘   │
│                                                                              │
└─────────────────────────────────────────────────────────────────────────────┘
```

## LP Fee Library

```solidity
library LPFeeLibrary {
    /// @notice Maximum LP fee: 100% (1,000,000 in hundredths of bips)
    uint24 public constant MAX_LP_FEE = 1_000_000;

    /// @notice Flag indicating dynamic fee (highest bit set)
    uint24 public constant DYNAMIC_FEE_FLAG = 0x800000;

    /// @notice Flag for overriding fee in beforeSwap
    uint24 public constant OVERRIDE_FEE_FLAG = 0x400000;

    /// @notice Check if fee represents a dynamic fee pool
    function isDynamicFee(uint24 fee) internal pure returns (bool) {
        return fee == DYNAMIC_FEE_FLAG;
    }

    /// @notice Get the static fee value (removes flags)
    function getStaticFee(uint24 fee) internal pure returns (uint24) {
        return fee & ~(DYNAMIC_FEE_FLAG | OVERRIDE_FEE_FLAG);
    }

    /// @notice Check if fee has override flag
    function isOverride(uint24 fee) internal pure returns (bool) {
        return fee & OVERRIDE_FEE_FLAG != 0;
    }

    /// @notice Remove override flag from fee
    function removeOverrideFlag(uint24 fee) internal pure returns (uint24) {
        return fee & ~OVERRIDE_FEE_FLAG;
    }

    /// @notice Validate fee is within bounds
    function validate(uint24 fee) internal pure {
        if (fee > MAX_LP_FEE) {
            LPFeeTooLarge.selector.revertWith(fee);
        }
    }
}
```

## Static Fees

Set at pool initialization via PoolKey.fee:

```solidity
// Create a pool with 0.3% fee
PoolKey memory key = PoolKey({
    currency0: currency0,
    currency1: currency1,
    fee: 3000,  // 0.3% = 3000 hundredths of bips
    tickSpacing: 60,
    hooks: IHooks(address(0))
});

poolManager.initialize(key, sqrtPriceX96);
```

Common fee tiers:
- 100 = 0.01% (stablecoins)
- 500 = 0.05% (stable pairs)
- 3000 = 0.30% (standard)
- 10000 = 1.00% (volatile)

## Dynamic Fees

### Enabling Dynamic Fees

```solidity
// Create a pool with dynamic fees
PoolKey memory key = PoolKey({
    currency0: currency0,
    currency1: currency1,
    fee: LPFeeLibrary.DYNAMIC_FEE_FLAG,  // 0x800000
    tickSpacing: 60,
    hooks: myDynamicFeeHook
});
```

### Method 1: beforeSwap Override

Return fee with override flag from beforeSwap:

```solidity
contract DynamicFeeHook is BaseHook {
    function beforeSwap(
        address,
        PoolKey calldata key,
        IPoolManager.SwapParams calldata params,
        bytes calldata
    ) external override returns (bytes4, BeforeSwapDelta, uint24) {
        // Calculate dynamic fee based on conditions
        uint24 fee = calculateFee(key, params);

        // Return fee with OVERRIDE_FEE_FLAG
        return (
            IHooks.beforeSwap.selector,
            BeforeSwapDeltaLibrary.ZERO_DELTA,
            fee | LPFeeLibrary.OVERRIDE_FEE_FLAG
        );
    }

    function calculateFee(PoolKey calldata key, IPoolManager.SwapParams calldata params)
        internal view returns (uint24)
    {
        // Example: Higher fee for larger swaps
        uint256 swapSize = params.amountSpecified < 0
            ? uint256(-params.amountSpecified)
            : uint256(params.amountSpecified);

        if (swapSize > 1_000_000e18) {
            return 10000; // 1% for large swaps
        } else if (swapSize > 100_000e18) {
            return 5000;  // 0.5% for medium swaps
        } else {
            return 3000;  // 0.3% for small swaps
        }
    }
}
```

### Method 2: Persistent Update

Call `updateDynamicLPFee` to change the stored fee:

```solidity
contract TWAPFeeHook is BaseHook {
    mapping(PoolId => uint24) public currentFees;

    // Called periodically to update fees
    function updateFeeBasedOnVolatility(PoolKey calldata key) external {
        uint24 newFee = calculateFeeFromVolatility(key);
        currentFees[key.toId()] = newFee;

        // Update the pool's stored dynamic fee
        poolManager.updateDynamicLPFee(key, newFee);
    }

    function beforeSwap(...) external override returns (bytes4, BeforeSwapDelta, uint24) {
        // No need to override - pool uses stored dynamic fee
        return (IHooks.beforeSwap.selector, BeforeSwapDeltaLibrary.ZERO_DELTA, 0);
    }
}
```

### PoolManager.updateDynamicLPFee

```solidity
/// @notice Update the dynamic LP fee for a pool
/// @dev Only callable by the hook contract
function updateDynamicLPFee(PoolKey memory key, uint24 newDynamicLPFee) external {
    if (!key.fee.isDynamicFee()) {
        NotDynamicFeePool.selector.revertWith();
    }
    if (msg.sender != address(key.hooks)) {
        UnauthorizedDynamicLPFeeUpdate.selector.revertWith();
    }

    newDynamicLPFee.validate();

    PoolId id = key.toId();
    _pools[id].setLPFee(newDynamicLPFee);

    emit DynamicLPFeeUpdated(id, newDynamicLPFee);
}
```

## Protocol Fees

Protocol fees are a percentage of LP fees taken by the protocol.

### Protocol Fee Encoding

```solidity
library ProtocolFeeLibrary {
    /// @notice Maximum protocol fee: 0.1% (1000 in ten-thousandths)
    uint16 public constant MAX_PROTOCOL_FEE = 1000;

    /// @notice Protocol fee is stored as two 12-bit values packed into 24 bits
    /// Lower 12 bits: fee for swaps 0→1
    /// Upper 12 bits: fee for swaps 1→0

    function getZeroForOneFee(uint24 protocolFee) internal pure returns (uint16) {
        return uint16(protocolFee & 0xFFF);
    }

    function getOneForZeroFee(uint24 protocolFee) internal pure returns (uint16) {
        return uint16(protocolFee >> 12);
    }

    function packFees(uint16 fee0, uint16 fee1) internal pure returns (uint24) {
        return uint24(fee0) | (uint24(fee1) << 12);
    }

    /// @notice Calculate protocol fee amount from LP fee
    /// @param lpFeeAmount The LP fee collected
    /// @param protocolFee The protocol fee rate (in ten-thousandths)
    function calculateProtocolFee(uint256 lpFeeAmount, uint16 protocolFee)
        internal pure returns (uint256)
    {
        return lpFeeAmount * protocolFee / 10000;
    }
}
```

### Setting Protocol Fees

```solidity
contract ProtocolFees is IProtocolFees {
    address public protocolFeeController;

    /// @notice Set the protocol fee controller
    function setProtocolFeeController(address controller) external {
        // Only governance/owner can set
        protocolFeeController = controller;
        emit ProtocolFeeControllerUpdated(controller);
    }

    /// @notice Set protocol fee for a pool
    function setProtocolFee(PoolKey memory key, uint24 newProtocolFee) external {
        if (msg.sender != protocolFeeController) {
            InvalidCaller.selector.revertWith();
        }

        // Validate fee bounds
        uint16 fee0 = ProtocolFeeLibrary.getZeroForOneFee(newProtocolFee);
        uint16 fee1 = ProtocolFeeLibrary.getOneForZeroFee(newProtocolFee);

        if (fee0 > ProtocolFeeLibrary.MAX_PROTOCOL_FEE ||
            fee1 > ProtocolFeeLibrary.MAX_PROTOCOL_FEE) {
            ProtocolFeeTooLarge.selector.revertWith(newProtocolFee);
        }

        PoolId id = key.toId();
        _pools[id].setProtocolFee(newProtocolFee);

        emit ProtocolFeeUpdated(id, newProtocolFee);
    }

    /// @notice Collect accumulated protocol fees
    function collectProtocolFees(address recipient, Currency currency, uint256 amount)
        external
        returns (uint256 amountCollected)
    {
        if (msg.sender != protocolFeeController) {
            InvalidCaller.selector.revertWith();
        }

        amountCollected = amount == 0 ? protocolFeesAccrued[currency] : amount;

        protocolFeesAccrued[currency] -= amountCollected;
        currency.transfer(recipient, amountCollected);
    }
}
```

## Fee Calculation in Swaps

```solidity
// In SwapMath.computeSwapStep
function computeSwapStep(
    uint160 sqrtPriceCurrentX96,
    uint160 sqrtPriceTargetX96,
    uint128 liquidity,
    int256 amountRemaining,
    uint24 feePips
) internal pure returns (
    uint160 sqrtPriceNextX96,
    uint256 amountIn,
    uint256 amountOut,
    uint256 feeAmount
) {
    bool exactIn = amountRemaining < 0;
    bool zeroForOne = sqrtPriceCurrentX96 >= sqrtPriceTargetX96;

    if (exactIn) {
        // Calculate amount after fee
        uint256 amountRemainingLessFee = FullMath.mulDiv(
            uint256(-amountRemaining),
            1e6 - feePips,
            1e6
        );

        // ... compute swap ...

        // Fee is the difference
        feeAmount = uint256(-amountRemaining) - amountIn;
    } else {
        // Exact output: fee applied to input
        // ... compute swap ...
        feeAmount = FullMath.mulDivRoundingUp(amountIn, feePips, 1e6 - feePips);
    }
}
```

## Fee Growth Tracking

```solidity
// In Pool.swap
if (state.liquidity > 0) {
    // Calculate fee per unit of liquidity
    uint256 feeGrowthDelta = FullMath.mulDiv(
        step.feeAmount,
        FixedPoint128.Q128,
        state.liquidity
    );

    // Update global fee growth
    state.feeGrowthGlobalX128 += feeGrowthDelta;
}
```

## Dynamic Fee Examples

### Volume-Based Fee

```solidity
contract VolumeFeeHook is BaseHook {
    mapping(PoolId => uint256) public dailyVolume;
    mapping(PoolId => uint256) public lastUpdateTime;

    function beforeSwap(...) external override returns (bytes4, BeforeSwapDelta, uint24) {
        PoolId id = key.toId();

        // Reset daily volume
        if (block.timestamp > lastUpdateTime[id] + 1 days) {
            dailyVolume[id] = 0;
            lastUpdateTime[id] = block.timestamp;
        }

        // Higher volume = lower fee (incentivize volume)
        uint24 fee;
        if (dailyVolume[id] > 10_000_000e18) {
            fee = 1000;  // 0.1%
        } else if (dailyVolume[id] > 1_000_000e18) {
            fee = 2000;  // 0.2%
        } else {
            fee = 3000;  // 0.3%
        }

        // Update volume
        dailyVolume[id] += uint256(params.amountSpecified < 0
            ? -params.amountSpecified
            : params.amountSpecified);

        return (IHooks.beforeSwap.selector, BeforeSwapDeltaLibrary.ZERO_DELTA, fee | OVERRIDE_FEE_FLAG);
    }
}
```

### Time-Based Fee

```solidity
contract TimeFeeHook is BaseHook {
    function beforeSwap(...) external override returns (bytes4, BeforeSwapDelta, uint24) {
        uint24 fee;

        // Higher fees during peak hours (13:00-17:00 UTC)
        uint256 hour = (block.timestamp % 1 days) / 1 hours;
        if (hour >= 13 && hour < 17) {
            fee = 5000;  // 0.5% peak
        } else {
            fee = 3000;  // 0.3% off-peak
        }

        return (IHooks.beforeSwap.selector, BeforeSwapDeltaLibrary.ZERO_DELTA, fee | OVERRIDE_FEE_FLAG);
    }
}
```

## Reference Files

### v4-core
- `src/libraries/LPFeeLibrary.sol` - LP fee utilities
- `src/libraries/ProtocolFeeLibrary.sol` - Protocol fee utilities
- `src/ProtocolFees.sol` - Protocol fee management
- `src/libraries/SwapMath.sol` - Fee calculation in swaps
