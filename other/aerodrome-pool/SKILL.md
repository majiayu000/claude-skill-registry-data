---
name: Aerodrome Pool
description: This skill should be used when the user asks about "pool", "AMM", "swap", "liquidity", "stable pool", "volatile pool", "sAMM", "vAMM", "constant product", or needs to understand Aerodrome's pool mechanics.
version: 0.1.0
---

# Aerodrome Pool

Aerodrome pools are AMM constant-product implementations similar to Uniswap V2, with support for both stable and volatile pool types.

## Overview

```
┌──────────────────────────────────────────────────────────────┐
│                     POOL ARCHITECTURE                        │
├──────────────────────────────────────────────────────────────┤
│                                                              │
│  ┌─────────────────────────────────────────────────────────┐ │
│  │                      Pool.sol                           │ │
│  ├─────────────────────────────────────────────────────────┤ │
│  │  token0, token1        ─ Pair tokens                    │ │
│  │  stable                ─ Pool type (stable or volatile) │ │
│  │  reserve0, reserve1    ─ Token reserves                 │ │
│  │  poolFees              ─ PoolFees contract              │ │
│  │                                                          │ │
│  │  mint() ─────────────► Add liquidity, get LP tokens     │ │
│  │  burn() ─────────────► Remove liquidity, get tokens     │ │
│  │  swap() ─────────────► Exchange tokens                  │ │
│  │  claimFees() ────────► Claim accrued trading fees       │ │
│  └─────────────────────────────────────────────────────────┘ │
│                              │                               │
│                              ▼                               │
│  ┌─────────────────────────────────────────────────────────┐ │
│  │                   PoolFees.sol                          │ │
│  │  Stores trading fees separate from reserves             │ │
│  └─────────────────────────────────────────────────────────┘ │
│                                                              │
└──────────────────────────────────────────────────────────────┘
```

## Pool Types

### Volatile Pool (vAMM)
Standard `x * y = k` constant product formula:

```solidity
// Volatile pool naming
_name = "Volatile AMM - TOKEN0/TOKEN1";
_symbol = "vAMM-TOKEN0/TOKEN1";

// Invariant calculation
function _k(uint256 x, uint256 y) internal view returns (uint256) {
    if (!stable) {
        return x * y;  // Simple xy = k
    }
    // ...stable calculation
}

// Price calculation for volatile
function _getAmountOut(uint256 amountIn, address tokenIn, uint256 _reserve0, uint256 _reserve1)
    internal view returns (uint256)
{
    if (!stable) {
        (uint256 reserveA, uint256 reserveB) = tokenIn == token0
            ? (_reserve0, _reserve1)
            : (_reserve1, _reserve0);
        return (amountIn * reserveB) / (reserveA + amountIn);
    }
    // ...stable calculation
}
```

### Stable Pool (sAMM)
Uses the `x³y + y³x = k` curve for low-slippage swaps between correlated assets:

```solidity
// Stable pool naming
_name = "Stable AMM - TOKEN0/TOKEN1";
_symbol = "sAMM-TOKEN0/TOKEN1";

// Invariant calculation for stable
function _k(uint256 x, uint256 y) internal view returns (uint256) {
    if (stable) {
        uint256 _x = (x * 1e18) / decimals0;
        uint256 _y = (y * 1e18) / decimals1;
        uint256 _a = (_x * _y) / 1e18;
        uint256 _b = ((_x * _x) / 1e18 + (_y * _y) / 1e18);
        return (_a * _b) / 1e18;  // x³y + y³x >= k
    }
    return x * y;
}
```

## Pool Initialization

```solidity
contract Pool is IPool, ERC20Permit, ReentrancyGuard {
    uint256 internal constant MINIMUM_LIQUIDITY = 10 ** 3;
    uint256 internal constant MINIMUM_K = 10 ** 10;

    function initialize(address _token0, address _token1, bool _stable) external {
        if (factory != address(0)) revert FactoryAlreadySet();
        factory = _msgSender();
        _voter = IPoolFactory(factory).voter();
        (token0, token1, stable) = (_token0, _token1, _stable);
        poolFees = address(new PoolFees(_token0, _token1));

        string memory symbol0 = ERC20(_token0).symbol();
        string memory symbol1 = ERC20(_token1).symbol();

        if (_stable) {
            _name = string(abi.encodePacked("Stable AMM - ", symbol0, "/", symbol1));
            _symbol = string(abi.encodePacked("sAMM-", symbol0, "/", symbol1));
        } else {
            _name = string(abi.encodePacked("Volatile AMM - ", symbol0, "/", symbol1));
            _symbol = string(abi.encodePacked("vAMM-", symbol0, "/", symbol1));
        }

        decimals0 = 10 ** ERC20(_token0).decimals();
        decimals1 = 10 ** ERC20(_token1).decimals();
    }
}
```

## Minting Liquidity

```solidity
function mint(address to) external nonReentrant returns (uint256 liquidity) {
    (uint256 _reserve0, uint256 _reserve1) = (reserve0, reserve1);
    uint256 _balance0 = IERC20(token0).balanceOf(address(this));
    uint256 _balance1 = IERC20(token1).balanceOf(address(this));
    uint256 _amount0 = _balance0 - _reserve0;
    uint256 _amount1 = _balance1 - _reserve1;

    uint256 _totalSupply = totalSupply();
    if (_totalSupply == 0) {
        // First deposit: liquidity = sqrt(amount0 * amount1) - MINIMUM_LIQUIDITY
        liquidity = Math.sqrt(_amount0 * _amount1) - MINIMUM_LIQUIDITY;
        _mint(address(1), MINIMUM_LIQUIDITY);  // Lock minimum liquidity forever

        if (stable) {
            // Stable pools require equal value deposits initially
            if ((_amount0 * 1e18) / decimals0 != (_amount1 * 1e18) / decimals1)
                revert DepositsNotEqual();
            if (_k(_amount0, _amount1) <= MINIMUM_K) revert BelowMinimumK();
        }
    } else {
        // Subsequent deposits: proportional to existing liquidity
        liquidity = Math.min(
            (_amount0 * _totalSupply) / _reserve0,
            (_amount1 * _totalSupply) / _reserve1
        );
    }

    if (liquidity == 0) revert InsufficientLiquidityMinted();
    _mint(to, liquidity);
    _update(_balance0, _balance1, _reserve0, _reserve1);

    emit Mint(_msgSender(), _amount0, _amount1);
}
```

## Burning Liquidity

```solidity
function burn(address to) external nonReentrant returns (uint256 amount0, uint256 amount1) {
    (uint256 _reserve0, uint256 _reserve1) = (reserve0, reserve1);
    uint256 _balance0 = IERC20(token0).balanceOf(address(this));
    uint256 _balance1 = IERC20(token1).balanceOf(address(this));
    uint256 _liquidity = balanceOf(address(this));

    uint256 _totalSupply = totalSupply();
    // Pro-rata distribution
    amount0 = (_liquidity * _balance0) / _totalSupply;
    amount1 = (_liquidity * _balance1) / _totalSupply;

    if (amount0 == 0 || amount1 == 0) revert InsufficientLiquidityBurned();

    _burn(address(this), _liquidity);
    IERC20(token0).safeTransfer(to, amount0);
    IERC20(token1).safeTransfer(to, amount1);

    _update(
        IERC20(token0).balanceOf(address(this)),
        IERC20(token1).balanceOf(address(this)),
        _reserve0,
        _reserve1
    );

    emit Burn(_msgSender(), to, amount0, amount1);
}
```

## Swapping

```solidity
function swap(uint256 amount0Out, uint256 amount1Out, address to, bytes calldata data)
    external nonReentrant
{
    if (IPoolFactory(factory).isPaused()) revert IsPaused();
    if (amount0Out == 0 && amount1Out == 0) revert InsufficientOutputAmount();

    (uint256 _reserve0, uint256 _reserve1) = (reserve0, reserve1);
    if (amount0Out >= _reserve0 || amount1Out >= _reserve1) revert InsufficientLiquidity();

    // Optimistically transfer tokens
    if (amount0Out > 0) IERC20(token0).safeTransfer(to, amount0Out);
    if (amount1Out > 0) IERC20(token1).safeTransfer(to, amount1Out);

    // Flash loan callback
    if (data.length > 0) IPoolCallee(to).hook(_msgSender(), amount0Out, amount1Out, data);

    uint256 _balance0 = IERC20(token0).balanceOf(address(this));
    uint256 _balance1 = IERC20(token1).balanceOf(address(this));

    uint256 amount0In = _balance0 > _reserve0 - amount0Out
        ? _balance0 - (_reserve0 - amount0Out) : 0;
    uint256 amount1In = _balance1 > _reserve1 - amount1Out
        ? _balance1 - (_reserve1 - amount1Out) : 0;

    if (amount0In == 0 && amount1In == 0) revert InsufficientInputAmount();

    // Accrue fees (moved to PoolFees)
    if (amount0In > 0) _update0((amount0In * IPoolFactory(factory).getFee(address(this), stable)) / 10000);
    if (amount1In > 0) _update1((amount1In * IPoolFactory(factory).getFee(address(this), stable)) / 10000);

    _balance0 = IERC20(token0).balanceOf(address(this));
    _balance1 = IERC20(token1).balanceOf(address(this));

    // Verify invariant
    if (_k(_balance0, _balance1) < _k(_reserve0, _reserve1)) revert K();

    _update(_balance0, _balance1, _reserve0, _reserve1);
    emit Swap(_msgSender(), to, amount0In, amount1In, amount0Out, amount1Out);
}
```

## Fee Mechanism

Fees are separated from reserves and stored in `PoolFees`:

```solidity
// Fee accrual (in Pool.sol)
function _update0(uint256 amount) internal {
    if (amount == 0) return;
    IERC20(token0).safeTransfer(poolFees, amount);  // Move to PoolFees
    uint256 _ratio = (amount * 1e18) / totalSupply();
    if (_ratio > 0) {
        index0 += _ratio;  // Track fee index for LP claims
    }
    emit Fees(_msgSender(), amount, 0);
}

// Fee claiming
function claimFees() external returns (uint256 claimed0, uint256 claimed1) {
    address sender = _msgSender();
    _updateFor(sender);

    claimed0 = claimable0[sender];
    claimed1 = claimable1[sender];

    if (claimed0 > 0 || claimed1 > 0) {
        claimable0[sender] = 0;
        claimable1[sender] = 0;
        PoolFees(poolFees).claimFeesFor(sender, claimed0, claimed1);
        emit Claim(sender, sender, claimed0, claimed1);
    }
}
```

## Price Oracle

Pools maintain TWAP (Time-Weighted Average Price) observations:

```solidity
uint256 public constant periodSize = 1800;  // 30-minute observation period

struct Observation {
    uint256 timestamp;
    uint256 reserve0Cumulative;
    uint256 reserve1Cumulative;
}

Observation[] public observations;

function _update(uint256 balance0, uint256 balance1, uint256 _reserve0, uint256 _reserve1) internal {
    uint256 blockTimestamp = block.timestamp;
    uint256 timeElapsed = blockTimestamp - blockTimestampLast;

    if (timeElapsed > 0 && _reserve0 != 0 && _reserve1 != 0) {
        reserve0CumulativeLast += _reserve0 * timeElapsed;
        reserve1CumulativeLast += _reserve1 * timeElapsed;
    }

    Observation memory _point = lastObservation();
    timeElapsed = blockTimestamp - _point.timestamp;

    // Record new observation every 30 minutes
    if (timeElapsed > periodSize) {
        observations.push(Observation(blockTimestamp, reserve0CumulativeLast, reserve1CumulativeLast));
    }

    reserve0 = balance0;
    reserve1 = balance1;
    blockTimestampLast = blockTimestamp;
    emit Sync(reserve0, reserve1);
}

// Get TWAP quote
function quote(address tokenIn, uint256 amountIn, uint256 granularity)
    external view returns (uint256 amountOut)
{
    uint256[] memory _prices = sample(tokenIn, amountIn, granularity, 1);
    uint256 priceAverageCumulative;
    for (uint256 i = 0; i < _prices.length; i++) {
        priceAverageCumulative += _prices[i];
    }
    return priceAverageCumulative / granularity;
}
```

## PoolFactory

```solidity
contract PoolFactory is IPoolFactory {
    mapping(address => mapping(address => mapping(bool => address))) public getPool;

    function createPool(address tokenA, address tokenB, bool stable)
        external returns (address pool)
    {
        if (tokenA == tokenB) revert SameAddress();
        (address token0, address token1) = tokenA < tokenB ? (tokenA, tokenB) : (tokenB, tokenA);
        if (token0 == address(0)) revert ZeroAddress();
        if (getPool[token0][token1][stable] != address(0)) revert PoolAlreadyExists();

        bytes32 salt = keccak256(abi.encodePacked(token0, token1, stable));
        pool = Clones.cloneDeterministic(implementation, salt);
        IPool(pool).initialize(token0, token1, stable);

        getPool[token0][token1][stable] = pool;
        getPool[token1][token0][stable] = pool;
        allPools.push(pool);

        emit PoolCreated(token0, token1, stable, pool, allPools.length);
    }

    // Custom fee per pool (max 3%)
    function setFee(address pool, bool stable, uint256 fee) external {
        if (msg.sender != feeManager) revert NotFeeManager();
        if (fee > 300) revert FeeTooHigh();  // Max 3%
        _customFee[pool] = fee;
    }
}
```

## Key View Functions

```solidity
// Get current reserves
function getReserves() public view returns (uint256 _reserve0, uint256 _reserve1, uint256 _blockTimestampLast);

// Get pool metadata
function metadata() external view returns (
    uint256 dec0, uint256 dec1,
    uint256 r0, uint256 r1,
    bool st,
    address t0, address t1
);

// Get output amount for a swap
function getAmountOut(uint256 amountIn, address tokenIn) external view returns (uint256);

// Get invariant K
function getK() external nonReentrant returns (uint256);
```

## Reference Files

- `contracts/Pool.sol` - Main pool implementation
- `contracts/PoolFees.sol` - Fee storage contract
- `contracts/factories/PoolFactory.sol` - Pool creation
- `contracts/interfaces/IPool.sol` - Pool interface
