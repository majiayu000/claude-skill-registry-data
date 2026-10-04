---
name: Aerodrome Router
description: This skill should be used when the user asks about "router", "swap", "addLiquidity", "removeLiquidity", "zap", "multi-hop", or needs to understand Aerodrome's Router operations.
version: 0.1.0
---

# Aerodrome Router

The Router handles multi-pool swaps, liquidity deposits/withdrawals, and zapping operations. It provides a UniswapV2-like interface with additional features.

## Overview

```
┌──────────────────────────────────────────────────────────────┐
│                      ROUTER OPERATIONS                       │
├──────────────────────────────────────────────────────────────┤
│                                                              │
│  Swaps:                                                      │
│  ┌─────────────────────────────────────────────────────────┐ │
│  │ swapExactTokensForTokens                                │ │
│  │ swapExactETHForTokens                                   │ │
│  │ swapExactTokensForETH                                   │ │
│  │ swapExactTokensForTokensSupportingFeeOnTransferTokens   │ │
│  └─────────────────────────────────────────────────────────┘ │
│                                                              │
│  Liquidity:                                                  │
│  ┌─────────────────────────────────────────────────────────┐ │
│  │ addLiquidity / addLiquidityETH                          │ │
│  │ removeLiquidity / removeLiquidityETH                    │ │
│  │ quoteAddLiquidity / quoteRemoveLiquidity                │ │
│  └─────────────────────────────────────────────────────────┘ │
│                                                              │
│  Zapping:                                                    │
│  ┌─────────────────────────────────────────────────────────┐ │
│  │ zapIn ──► Convert any token to LP + optional stake      │ │
│  │ zapOut ─► Convert LP to any token                       │ │
│  └─────────────────────────────────────────────────────────┘ │
│                                                              │
└──────────────────────────────────────────────────────────────┘
```

## Route Structure

```solidity
struct Route {
    address from;      // Input token
    address to;        // Output token
    bool stable;       // Pool type (true = stable, false = volatile)
    address factory;   // Pool factory (address(0) for default)
}
```

## Swap Operations

### Basic Swap

```solidity
function swapExactTokensForTokens(
    uint256 amountIn,
    uint256 amountOutMin,
    Route[] calldata routes,
    address to,
    uint256 deadline
) external ensure(deadline) returns (uint256[] memory amounts) {
    amounts = getAmountsOut(amountIn, routes);
    if (amounts[amounts.length - 1] < amountOutMin) revert InsufficientOutputAmount();

    _safeTransferFrom(
        routes[0].from,
        _msgSender(),
        poolFor(routes[0].from, routes[0].to, routes[0].stable, routes[0].factory),
        amounts[0]
    );
    _swap(amounts, routes, to);
}
```

### Multi-Hop Swap Execution

```solidity
function _swap(uint256[] memory amounts, Route[] memory routes, address _to) internal virtual {
    uint256 _length = routes.length;
    for (uint256 i = 0; i < _length; i++) {
        (address token0, ) = sortTokens(routes[i].from, routes[i].to);
        uint256 amountOut = amounts[i + 1];

        (uint256 amount0Out, uint256 amount1Out) = routes[i].from == token0
            ? (uint256(0), amountOut)
            : (amountOut, uint256(0));

        // Next hop destination or final recipient
        address to = i < routes.length - 1
            ? poolFor(routes[i + 1].from, routes[i + 1].to, routes[i + 1].stable, routes[i + 1].factory)
            : _to;

        IPool(poolFor(routes[i].from, routes[i].to, routes[i].stable, routes[i].factory))
            .swap(amount0Out, amount1Out, to, new bytes(0));
    }
}
```

### ETH Swaps

```solidity
// ETH → Tokens
function swapExactETHForTokens(
    uint256 amountOutMin,
    Route[] calldata routes,
    address to,
    uint256 deadline
) external payable ensure(deadline) returns (uint256[] memory amounts) {
    if (routes[0].from != address(weth)) revert InvalidPath();
    amounts = getAmountsOut(msg.value, routes);
    if (amounts[amounts.length - 1] < amountOutMin) revert InsufficientOutputAmount();

    weth.deposit{value: amounts[0]}();
    assert(weth.transfer(poolFor(routes[0].from, routes[0].to, routes[0].stable, routes[0].factory), amounts[0]));
    _swap(amounts, routes, to);
}

// Tokens → ETH
function swapExactTokensForETH(
    uint256 amountIn,
    uint256 amountOutMin,
    Route[] calldata routes,
    address to,
    uint256 deadline
) external ensure(deadline) returns (uint256[] memory amounts) {
    if (routes[routes.length - 1].to != address(weth)) revert InvalidPath();
    amounts = getAmountsOut(amountIn, routes);
    if (amounts[amounts.length - 1] < amountOutMin) revert InsufficientOutputAmount();

    _safeTransferFrom(
        routes[0].from,
        _msgSender(),
        poolFor(routes[0].from, routes[0].to, routes[0].stable, routes[0].factory),
        amounts[0]
    );
    _swap(amounts, routes, address(this));

    weth.withdraw(amounts[amounts.length - 1]);
    _safeTransferETH(to, amounts[amounts.length - 1]);
}
```

## Liquidity Operations

### Add Liquidity

```solidity
function addLiquidity(
    address tokenA,
    address tokenB,
    bool stable,
    uint256 amountADesired,
    uint256 amountBDesired,
    uint256 amountAMin,
    uint256 amountBMin,
    address to,
    uint256 deadline
) public ensure(deadline) returns (uint256 amountA, uint256 amountB, uint256 liquidity) {
    (amountA, amountB) = _addLiquidity(
        tokenA, tokenB, stable,
        amountADesired, amountBDesired,
        amountAMin, amountBMin
    );

    address pool = poolFor(tokenA, tokenB, stable, defaultFactory);
    _safeTransferFrom(tokenA, _msgSender(), pool, amountA);
    _safeTransferFrom(tokenB, _msgSender(), pool, amountB);
    liquidity = IPool(pool).mint(to);
}

function _addLiquidity(
    address tokenA,
    address tokenB,
    bool stable,
    uint256 amountADesired,
    uint256 amountBDesired,
    uint256 amountAMin,
    uint256 amountBMin
) internal returns (uint256 amountA, uint256 amountB) {
    // Create pool if it doesn't exist
    address _pool = IPoolFactory(defaultFactory).getPool(tokenA, tokenB, stable);
    if (_pool == address(0)) {
        _pool = IPoolFactory(defaultFactory).createPool(tokenA, tokenB, stable);
    }

    (uint256 reserveA, uint256 reserveB) = getReserves(tokenA, tokenB, stable, defaultFactory);

    if (reserveA == 0 && reserveB == 0) {
        // First deposit - use desired amounts
        (amountA, amountB) = (amountADesired, amountBDesired);
    } else {
        // Subsequent deposits - maintain ratio
        uint256 amountBOptimal = quoteLiquidity(amountADesired, reserveA, reserveB);
        if (amountBOptimal <= amountBDesired) {
            if (amountBOptimal < amountBMin) revert InsufficientAmountB();
            (amountA, amountB) = (amountADesired, amountBOptimal);
        } else {
            uint256 amountAOptimal = quoteLiquidity(amountBDesired, reserveB, reserveA);
            if (amountAOptimal < amountAMin) revert InsufficientAmountA();
            (amountA, amountB) = (amountAOptimal, amountBDesired);
        }
    }
}
```

### Remove Liquidity

```solidity
function removeLiquidity(
    address tokenA,
    address tokenB,
    bool stable,
    uint256 liquidity,
    uint256 amountAMin,
    uint256 amountBMin,
    address to,
    uint256 deadline
) public ensure(deadline) returns (uint256 amountA, uint256 amountB) {
    address pool = poolFor(tokenA, tokenB, stable, defaultFactory);

    IERC20(pool).safeTransferFrom(_msgSender(), pool, liquidity);
    (uint256 amount0, uint256 amount1) = IPool(pool).burn(to);

    (address token0, ) = sortTokens(tokenA, tokenB);
    (amountA, amountB) = tokenA == token0 ? (amount0, amount1) : (amount1, amount0);

    if (amountA < amountAMin) revert InsufficientAmountA();
    if (amountB < amountBMin) revert InsufficientAmountB();
}
```

## Zapping

### Zap Structure

```solidity
struct Zap {
    address tokenA;        // First token of the pool
    address tokenB;        // Second token of the pool
    bool stable;           // Pool type
    address factory;       // Pool factory
    uint256 amountOutMinA; // Minimum output for routesA
    uint256 amountOutMinB; // Minimum output for routesB
    uint256 amountAMin;    // Minimum tokenA for liquidity
    uint256 amountBMin;    // Minimum tokenB for liquidity
}
```

### Zap In

```solidity
address public constant ETHER = 0xEeeeeEeeeEeEeeEeEeEeeEEEeeeeEeeeeeeeEEeE;

/// @notice Convert any token to LP tokens, optionally stake in gauge
function zapIn(
    address tokenIn,          // Input token (or ETHER constant)
    uint256 amountInA,        // Amount for tokenA route
    uint256 amountInB,        // Amount for tokenB route
    Zap calldata zapInPool,   // Pool parameters
    Route[] calldata routesA, // Route to get tokenA
    Route[] calldata routesB, // Route to get tokenB
    address to,               // Recipient
    bool stake                // Stake LP in gauge?
) external payable returns (uint256 liquidity) {
    uint256 amountIn = amountInA + amountInB;
    address _tokenIn = tokenIn;

    // Handle ETH input
    if (tokenIn == ETHER) {
        if (amountIn != msg.value) revert InvalidAmountInForETHDeposit();
        _tokenIn = address(weth);
        weth.deposit{value: msg.value}();
    } else {
        if (msg.value != 0) revert InvalidTokenInForETHDeposit();
        _safeTransferFrom(_tokenIn, _msgSender(), address(this), amountIn);
    }

    // Swap to pool tokens
    _zapSwap(_tokenIn, amountInA, amountInB, zapInPool, routesA, routesB);

    // Add liquidity
    _zapInLiquidity(zapInPool);

    address pool = poolFor(zapInPool.tokenA, zapInPool.tokenB, zapInPool.stable, zapInPool.factory);

    if (stake) {
        // Mint LP and stake in gauge
        liquidity = IPool(pool).mint(address(this));
        address gauge = IVoter(voter).gauges(pool);
        IERC20(pool).safeApprove(address(gauge), liquidity);
        IGauge(gauge).deposit(liquidity, to);
        IERC20(pool).safeApprove(address(gauge), 0);
    } else {
        // Just mint LP to recipient
        liquidity = IPool(pool).mint(to);
    }

    // Return any leftover tokens
    _returnAssets(tokenIn);
    _returnAssets(zapInPool.tokenA);
    _returnAssets(zapInPool.tokenB);
}
```

### Zap Out

```solidity
/// @notice Convert LP tokens to any token
function zapOut(
    address tokenOut,         // Output token (or ETHER constant)
    uint256 liquidity,        // LP tokens to burn
    Zap calldata zapOutPool,  // Pool parameters
    Route[] calldata routesA, // Route from tokenA to output
    Route[] calldata routesB  // Route from tokenB to output
) external {
    address tokenA = zapOutPool.tokenA;
    address tokenB = zapOutPool.tokenB;
    address _tokenOut = (tokenOut == ETHER) ? address(weth) : tokenOut;

    // Remove liquidity
    _zapOutLiquidity(liquidity, zapOutPool);

    // Swap tokens to output
    if (tokenA != _tokenOut) {
        uint256 balance = IERC20(tokenA).balanceOf(address(this));
        if (routesA[routesA.length - 1].to != _tokenOut) revert InvalidRouteA();
        _internalSwap(tokenA, balance, zapOutPool.amountOutMinA, routesA);
    }
    if (tokenB != _tokenOut) {
        uint256 balance = IERC20(tokenB).balanceOf(address(this));
        if (routesB[routesB.length - 1].to != _tokenOut) revert InvalidRouteB();
        _internalSwap(tokenB, balance, zapOutPool.amountOutMinB, routesB);
    }

    _returnAssets(tokenOut);
}
```

## Quote Functions

```solidity
/// @notice Preview amounts for adding liquidity
function quoteAddLiquidity(
    address tokenA,
    address tokenB,
    bool stable,
    address _factory,
    uint256 amountADesired,
    uint256 amountBDesired
) public view returns (uint256 amountA, uint256 amountB, uint256 liquidity);

/// @notice Preview amounts for removing liquidity
function quoteRemoveLiquidity(
    address tokenA,
    address tokenB,
    bool stable,
    address _factory,
    uint256 liquidity
) public view returns (uint256 amountA, uint256 amountB);

/// @notice Calculate output amounts for a route
function getAmountsOut(uint256 amountIn, Route[] memory routes)
    public view returns (uint256[] memory amounts)
{
    if (routes.length < 1) revert InvalidPath();
    amounts = new uint256[](routes.length + 1);
    amounts[0] = amountIn;

    for (uint256 i = 0; i < routes.length; i++) {
        address factory = routes[i].factory == address(0) ? defaultFactory : routes[i].factory;
        address pool = poolFor(routes[i].from, routes[i].to, routes[i].stable, factory);

        if (IPoolFactory(factory).isPool(pool)) {
            amounts[i + 1] = IPool(pool).getAmountOut(amounts[i], routes[i].from);
        }
    }
}

/// @notice Get optimal ratio for stable pool liquidity
function quoteStableLiquidityRatio(
    address tokenA,
    address tokenB,
    address _factory
) external view returns (uint256 ratio);

/// @notice Generate zap parameters
function generateZapInParams(
    address tokenA, address tokenB,
    bool stable, address _factory,
    uint256 amountInA, uint256 amountInB,
    Route[] calldata routesA, Route[] calldata routesB
) external view returns (
    uint256 amountOutMinA, uint256 amountOutMinB,
    uint256 amountAMin, uint256 amountBMin
);
```

## Helper Functions

```solidity
/// @notice Get pool address
function poolFor(address tokenA, address tokenB, bool stable, address _factory)
    public view returns (address pool)
{
    address factory = _factory == address(0) ? defaultFactory : _factory;
    if (!IFactoryRegistry(factoryRegistry).isPoolFactoryApproved(factory))
        revert PoolFactoryDoesNotExist();

    (address token0, address token1) = sortTokens(tokenA, tokenB);
    bytes32 salt = keccak256(abi.encodePacked(token0, token1, stable));
    pool = Clones.predictDeterministicAddress(IPoolFactory(factory).implementation(), salt, factory);
}

/// @notice Sort tokens
function sortTokens(address tokenA, address tokenB)
    public pure returns (address token0, address token1)
{
    if (tokenA == tokenB) revert SameAddresses();
    (token0, token1) = tokenA < tokenB ? (tokenA, tokenB) : (tokenB, tokenA);
    if (token0 == address(0)) revert ZeroAddress();
}

/// @notice Get reserves
function getReserves(address tokenA, address tokenB, bool stable, address _factory)
    public view returns (uint256 reserveA, uint256 reserveB)
{
    (address token0, ) = sortTokens(tokenA, tokenB);
    (uint256 reserve0, uint256 reserve1, ) = IPool(poolFor(tokenA, tokenB, stable, _factory)).getReserves();
    (reserveA, reserveB) = tokenA == token0 ? (reserve0, reserve1) : (reserve1, reserve0);
}
```

## Usage Examples

### Multi-hop Swap Example

```solidity
// USDC → WETH → AERO (volatile pools)
Route[] memory routes = new Route[](2);
routes[0] = Route({
    from: USDC,
    to: WETH,
    stable: false,
    factory: address(0)  // Use default factory
});
routes[1] = Route({
    from: WETH,
    to: AERO,
    stable: false,
    factory: address(0)
});

router.swapExactTokensForTokens(
    1000e6,           // 1000 USDC
    minAeroOut,       // Minimum AERO
    routes,
    recipient,
    block.timestamp + 1 hours
);
```

### Zap Into LP + Stake

```solidity
// Zap USDC into WETH/AERO LP and stake
Route[] memory routesToWETH = new Route[](1);
routesToWETH[0] = Route(USDC, WETH, false, address(0));

Route[] memory routesToAERO = new Route[](1);
routesToAERO[0] = Route(USDC, AERO, false, address(0));

Zap memory zapParams = Zap({
    tokenA: WETH,
    tokenB: AERO,
    stable: false,
    factory: address(0),
    amountOutMinA: minWETH,
    amountOutMinB: minAERO,
    amountAMin: minLiqA,
    amountBMin: minLiqB
});

router.zapIn(
    USDC,
    500e6,           // Half to WETH
    500e6,           // Half to AERO
    zapParams,
    routesToWETH,
    routesToAERO,
    recipient,
    true             // Stake in gauge
);
```

## Reference Files

- `contracts/Router.sol` - Main router implementation
- `contracts/interfaces/IRouter.sol` - Router interface
- `contracts/FactoryRegistry.sol` - Factory registry
