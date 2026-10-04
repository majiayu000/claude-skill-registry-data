---
name: Uniswap V4 Pools
description: This skill should be used when the user asks about "PoolKey", "PoolId", "Slot0", "pool state", "pool initialization", "Currency", or needs to understand pool identification and state management.
version: 0.1.0
---

# Uniswap V4 Pools

## Overview

In V4, pools are internal mappings within the PoolManager rather than separate contracts. Each pool is identified by a PoolKey (struct) and indexed by PoolId (hash of PoolKey).

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                         POOL IDENTIFICATION                                  │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│  PoolKey (struct identifying a unique pool):                                │
│  ┌──────────────────────────────────────────────────────────────────────┐   │
│  │  currency0: Currency     // First token (numerically lower address)  │   │
│  │  currency1: Currency     // Second token (numerically higher)        │   │
│  │  fee: uint24             // LP fee in hundredths of bps              │   │
│  │  tickSpacing: int24      // Minimum tick interval for positions      │   │
│  │  hooks: IHooks           // Hook contract (address encodes perms)    │   │
│  └──────────────────────────────────────────────────────────────────────┘   │
│                              │                                               │
│                              │ keccak256(abi.encode(...))                    │
│                              ▼                                               │
│  ┌──────────────────────────────────────────────────────────────────────┐   │
│  │  PoolId: bytes32         // Hash used as mapping key                 │   │
│  └──────────────────────────────────────────────────────────────────────┘   │
│                              │                                               │
│                              │ _pools[id]                                    │
│                              ▼                                               │
│  ┌──────────────────────────────────────────────────────────────────────┐   │
│  │  Pool.State:             // Internal pool state                      │   │
│  │    slot0                 // Packed: sqrtPrice, tick, protocolFee...  │   │
│  │    feeGrowthGlobal0X128  // Accumulated fees for token0              │   │
│  │    feeGrowthGlobal1X128  // Accumulated fees for token1              │   │
│  │    liquidity             // Total active liquidity                   │   │
│  │    ticks                 // Tick state mapping                       │   │
│  │    tickBitmap            // Initialized tick bitmap                  │   │
│  │    positions             // Position state mapping                   │   │
│  └──────────────────────────────────────────────────────────────────────┘   │
│                                                                              │
└─────────────────────────────────────────────────────────────────────────────┘
```

## PoolKey

```solidity
struct PoolKey {
    /// @notice The lower currency of the pool, sorted numerically
    Currency currency0;

    /// @notice The higher currency of the pool, sorted numerically
    Currency currency1;

    /// @notice The pool LP fee, capped at 1_000_000 (100%)
    /// If the highest bit is 1, the pool has a dynamic fee
    uint24 fee;

    /// @notice Tick spacing for the pool
    /// Ticks can only be used at multiples of this value
    int24 tickSpacing;

    /// @notice The hooks contract for the pool
    IHooks hooks;
}
```

### PoolId

```solidity
/// @notice PoolId wraps bytes32 for type safety
type PoolId is bytes32;

library PoolIdLibrary {
    /// @notice Compute the PoolId from a PoolKey
    function toId(PoolKey memory key) internal pure returns (PoolId poolId) {
        assembly {
            // Hash the entire PoolKey struct (5 slots = 160 bytes)
            poolId := keccak256(key, mul(32, 5))
        }
    }
}
```

## Currency Type

```solidity
/// @notice Currency wraps address for type safety
/// address(0) represents native currency (ETH)
type Currency is address;

library CurrencyLibrary {
    Currency public constant ADDRESS_ZERO = Currency.wrap(address(0));

    function isAddressZero(Currency currency) internal pure returns (bool) {
        return Currency.unwrap(currency) == address(0);
    }

    function toId(Currency currency) internal pure returns (uint256) {
        return uint160(Currency.unwrap(currency));
    }

    function fromId(uint256 id) internal pure returns (Currency) {
        return Currency.wrap(address(uint160(id)));
    }

    function balanceOfSelf(Currency currency) internal view returns (uint256) {
        if (currency.isAddressZero()) {
            return address(this).balance;
        }
        return IERC20Minimal(Currency.unwrap(currency)).balanceOf(address(this));
    }

    function transfer(Currency currency, address to, uint256 amount) internal {
        if (currency.isAddressZero()) {
            (bool success,) = to.call{value: amount}("");
            require(success);
        } else {
            IERC20Minimal(Currency.unwrap(currency)).transfer(to, amount);
        }
    }
}
```

## Pool State

```solidity
library Pool {
    struct State {
        Slot0 slot0;
        uint256 feeGrowthGlobal0X128;
        uint256 feeGrowthGlobal1X128;
        uint128 liquidity;
        mapping(int24 tick => TickInfo) ticks;
        mapping(int16 wordPos => uint256) tickBitmap;
        mapping(bytes32 positionKey => Position.State) positions;
    }
}
```

## Slot0 (Packed State)

All frequently-accessed pool state is packed into a single 256-bit slot:

```solidity
/// @notice Slot0 packs multiple values into one storage slot
/// Layout (right to left, LSB first):
///   160 bits: sqrtPriceX96
///    24 bits: tick
///    12 bits: protocolFee (token0 → token1)
///    12 bits: protocolFee (token1 → token0)
///    24 bits: lpFee
///    24 bits: unused

struct Slot0 {
    uint160 sqrtPriceX96;
    int24 tick;
    uint24 protocolFee;  // Packed: upper 12 bits = 1→0, lower 12 bits = 0→1
    uint24 lpFee;
}

library Slot0Library {
    uint160 internal constant MASK_160_BITS = 0x00FFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF;
    uint24 internal constant MASK_24_BITS = 0xFFFFFF;

    function sqrtPriceX96(Slot0 self) internal pure returns (uint160) {
        return uint160(Slot0.unwrap(self) & MASK_160_BITS);
    }

    function tick(Slot0 self) internal pure returns (int24) {
        return int24(int256(Slot0.unwrap(self) >> 160));
    }

    function protocolFee(Slot0 self) internal pure returns (uint24) {
        return uint24((Slot0.unwrap(self) >> 184) & MASK_24_BITS);
    }

    function lpFee(Slot0 self) internal pure returns (uint24) {
        return uint24((Slot0.unwrap(self) >> 208) & MASK_24_BITS);
    }

    function setTick(Slot0 self, int24 newTick) internal pure returns (Slot0) {
        // Clear old tick bits and set new
        uint256 slot = Slot0.unwrap(self);
        slot = (slot & ~(uint256(MASK_24_BITS) << 160)) | (uint256(uint24(newTick)) << 160);
        return Slot0.wrap(slot);
    }

    function setSqrtPriceX96(Slot0 self, uint160 newPrice) internal pure returns (Slot0) {
        uint256 slot = Slot0.unwrap(self);
        slot = (slot & ~uint256(MASK_160_BITS)) | uint256(newPrice);
        return Slot0.wrap(slot);
    }
}
```

## Pool Initialization

```solidity
library Pool {
    /// @notice Initialize a pool with a starting price
    function initialize(
        State storage self,
        uint160 sqrtPriceX96,
        uint24 protocolFee,
        uint24 lpFee
    ) internal returns (int24 tick) {
        if (self.slot0.sqrtPriceX96() != 0) {
            PoolAlreadyInitialized.selector.revertWith();
        }

        tick = TickMath.getTickAtSqrtPrice(sqrtPriceX96);

        self.slot0 = Slot0.wrap(0)
            .setSqrtPriceX96(sqrtPriceX96)
            .setTick(tick)
            .setProtocolFee(protocolFee)
            .setLpFee(lpFee);
    }

    /// @notice Check that a pool is initialized
    function checkPoolInitialized(State storage self) internal view {
        if (self.slot0.sqrtPriceX96() == 0) {
            PoolNotInitialized.selector.revertWith();
        }
    }
}
```

## BalanceDelta

Packed representation of two token amounts:

```solidity
/// @notice Packed delta: upper 128 bits = amount0, lower 128 bits = amount1
type BalanceDelta is int256;

library BalanceDeltaLibrary {
    BalanceDelta public constant ZERO_DELTA = BalanceDelta.wrap(0);

    function amount0(BalanceDelta delta) internal pure returns (int128) {
        return int128(BalanceDelta.unwrap(delta) >> 128);
    }

    function amount1(BalanceDelta delta) internal pure returns (int128) {
        return int128(BalanceDelta.unwrap(delta));
    }

    function toBalanceDelta(int128 _amount0, int128 _amount1)
        internal pure returns (BalanceDelta)
    {
        return BalanceDelta.wrap(
            (int256(_amount0) << 128) | int256(uint256(uint128(_amount1)))
        );
    }

    function add(BalanceDelta a, BalanceDelta b) internal pure returns (BalanceDelta) {
        return toBalanceDelta(
            a.amount0() + b.amount0(),
            a.amount1() + b.amount1()
        );
    }

    function sub(BalanceDelta a, BalanceDelta b) internal pure returns (BalanceDelta) {
        return toBalanceDelta(
            a.amount0() - b.amount0(),
            a.amount1() - b.amount1()
        );
    }
}
```

## Tick Spacing

Controls position granularity:

```solidity
library TickSpacing {
    int24 internal constant MIN_TICK_SPACING = 1;
    int24 internal constant MAX_TICK_SPACING = 16383;

    function validateTickSpacing(int24 tickSpacing) internal pure {
        if (tickSpacing < MIN_TICK_SPACING || tickSpacing > MAX_TICK_SPACING) {
            TickSpacingError.selector.revertWith(tickSpacing);
        }
    }
}

// Common tick spacing values:
// 1    - Very stable pairs (stablecoins)
// 10   - Stable pairs
// 60   - Standard pairs (most common)
// 200  - Volatile pairs
```

## Position Identification

```solidity
library Position {
    struct State {
        uint128 liquidity;
        uint256 feeGrowthInside0LastX128;
        uint256 feeGrowthInside1LastX128;
    }
}

library PositionKey {
    /// @notice Compute position key from owner, ticks, and salt
    function compute(
        address owner,
        int24 tickLower,
        int24 tickUpper,
        bytes32 salt
    ) internal pure returns (bytes32 key) {
        assembly {
            mstore(0, owner)
            mstore(32, tickLower)
            mstore(64, tickUpper)
            mstore(96, salt)
            key := keccak256(0, 128)
        }
    }
}
```

## Pool Library Functions

```solidity
library Pool {
    /// @notice Get the current price and tick
    function getSlot0(State storage self)
        internal view returns (uint160 sqrtPriceX96, int24 tick, uint24 protocolFee, uint24 lpFee)
    {
        Slot0 slot0 = self.slot0;
        return (slot0.sqrtPriceX96(), slot0.tick(), slot0.protocolFee(), slot0.lpFee());
    }

    /// @notice Get position info
    function getPosition(State storage self, address owner, int24 tickLower, int24 tickUpper, bytes32 salt)
        internal view returns (Position.State storage position)
    {
        bytes32 key = PositionKey.compute(owner, tickLower, tickUpper, salt);
        return self.positions[key];
    }

    /// @notice Get tick info
    function getTick(State storage self, int24 tick)
        internal view returns (TickInfo storage)
    {
        return self.ticks[tick];
    }

    /// @notice Check if a tick is initialized
    function isTickInitialized(State storage self, int24 tick)
        internal view returns (bool)
    {
        (int16 wordPos, uint8 bitPos) = TickBitmap.position(tick);
        return (self.tickBitmap[wordPos] & (1 << bitPos)) != 0;
    }
}
```

## Pool State View

```solidity
// In v4-periphery: StateView.sol
contract StateView {
    IPoolManager public immutable poolManager;

    function getSlot0(PoolId poolId)
        external view returns (uint160, int24, uint24, uint24)
    {
        return poolManager.getSlot0(poolId);
    }

    function getLiquidity(PoolId poolId) external view returns (uint128) {
        return poolManager.getLiquidity(poolId);
    }

    function getPosition(PoolId poolId, address owner, int24 tickLower, int24 tickUpper, bytes32 salt)
        external view returns (uint128 liquidity, uint256 feeGrowth0, uint256 feeGrowth1)
    {
        return poolManager.getPosition(poolId, owner, tickLower, tickUpper, salt);
    }
}
```

## Reference Files

### v4-core
- `src/types/PoolKey.sol` - PoolKey struct
- `src/types/PoolId.sol` - PoolId type and library
- `src/types/Currency.sol` - Currency type
- `src/types/BalanceDelta.sol` - Packed delta type
- `src/types/Slot0.sol` - Packed slot0 type
- `src/libraries/Pool.sol` - Pool state machine

### v4-periphery
- `src/lens/StateView.sol` - Pool state queries
