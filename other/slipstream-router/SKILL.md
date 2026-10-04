---
name: Slipstream Router & Quoter
description: This skill should be used when the user asks about "SwapRouter", "exactInput", "exactOutput", "Quoter", "quote", "slippage", "multi-hop", "path", or needs to understand the trading interface.
version: 0.1.0
---

# Slipstream Router & Quoter

SwapRouter provides the user-facing interface for executing swaps, while Quoter allows simulating swaps to get expected outputs.

## Overview

```
┌──────────────────────────────────────────────────────────────┐
│                    TRADING INTERFACE                         │
├──────────────────────────────────────────────────────────────┤
│                                                              │
│  SwapRouter (Execute Swaps):                                 │
│  ├── exactInputSingle()   - Swap exact amount in, single hop │
│  ├── exactOutputSingle()  - Swap for exact amount out        │
│  ├── exactInput()         - Multi-hop with exact input       │
│  └── exactOutput()        - Multi-hop with exact output      │
│                                                              │
│  QuoterV2 (Simulate Swaps):                                  │
│  ├── quoteExactInputSingle()  - Quote single hop             │
│  ├── quoteExactOutputSingle() - Quote single hop             │
│  ├── quoteExactInput()        - Quote multi-hop              │
│  └── quoteExactOutput()       - Quote multi-hop              │
│                                                              │
│  ┌─────────────────────────────────────────────────────────┐ │
│  │                    Swap Path                            │ │
│  │                                                         │ │
│  │  Token A ──► Pool AB ──► Token B ──► Pool BC ──► Token C │ │
│  │           (tickSpacing)           (tickSpacing)          │ │
│  │                                                         │ │
│  │  Path encoding: tokenA + tickSpacing + tokenB + ...     │ │
│  │                                                         │ │
│  └─────────────────────────────────────────────────────────┘ │
│                                                              │
└──────────────────────────────────────────────────────────────┘
```

## SwapRouter

```solidity
// periphery/SwapRouter.sol

contract SwapRouter is ISwapRouter, PeripheryPayments, Multicall {
    address public immutable factory;
    address public immutable WETH9;

    constructor(address _factory, address _WETH9) {
        factory = _factory;
        WETH9 = _WETH9;
    }
}
```

## Exact Input Single

```solidity
struct ExactInputSingleParams {
    address tokenIn;
    address tokenOut;
    int24 tickSpacing;
    address recipient;
    uint256 deadline;
    uint256 amountIn;
    uint256 amountOutMinimum;
    uint160 sqrtPriceLimitX96;
}

/// @notice Swap exact input for output (single hop)
/// @return amountOut Amount of output token received
function exactInputSingle(ExactInputSingleParams calldata params)
    external
    payable
    checkDeadline(params.deadline)
    returns (uint256 amountOut)
{
    amountOut = exactInputInternal(
        params.amountIn,
        params.recipient,
        params.sqrtPriceLimitX96,
        SwapCallbackData({
            path: abi.encodePacked(params.tokenIn, params.tickSpacing, params.tokenOut),
            payer: msg.sender
        })
    );

    require(amountOut >= params.amountOutMinimum, "TLR");  // Too Little Received
}

function exactInputInternal(
    uint256 amountIn,
    address recipient,
    uint160 sqrtPriceLimitX96,
    SwapCallbackData memory data
) private returns (uint256 amountOut) {
    // Decode path
    (address tokenIn, address tokenOut, int24 tickSpacing) = data.path.decodeFirstPool();

    bool zeroForOne = tokenIn < tokenOut;

    // Execute swap on pool
    (int256 amount0, int256 amount1) = getPool(tokenIn, tokenOut, tickSpacing).swap(
        recipient,
        zeroForOne,
        amountIn.toInt256(),
        sqrtPriceLimitX96 == 0
            ? (zeroForOne ? TickMath.MIN_SQRT_RATIO + 1 : TickMath.MAX_SQRT_RATIO - 1)
            : sqrtPriceLimitX96,
        abi.encode(data)
    );

    return uint256(-(zeroForOne ? amount1 : amount0));
}
```

## Exact Output Single

```solidity
struct ExactOutputSingleParams {
    address tokenIn;
    address tokenOut;
    int24 tickSpacing;
    address recipient;
    uint256 deadline;
    uint256 amountOut;
    uint256 amountInMaximum;
    uint160 sqrtPriceLimitX96;
}

/// @notice Swap for exact output (single hop)
/// @return amountIn Amount of input token spent
function exactOutputSingle(ExactOutputSingleParams calldata params)
    external
    payable
    checkDeadline(params.deadline)
    returns (uint256 amountIn)
{
    amountIn = exactOutputInternal(
        params.amountOut,
        params.recipient,
        params.sqrtPriceLimitX96,
        SwapCallbackData({
            path: abi.encodePacked(params.tokenOut, params.tickSpacing, params.tokenIn),
            payer: msg.sender
        })
    );

    require(amountIn <= params.amountInMaximum, "TMA");  // Too Much Asked

    // Reset approval if needed
    amountInCached = DEFAULT_AMOUNT_IN_CACHED;
}

function exactOutputInternal(
    uint256 amountOut,
    address recipient,
    uint160 sqrtPriceLimitX96,
    SwapCallbackData memory data
) private returns (uint256 amountIn) {
    (address tokenOut, address tokenIn, int24 tickSpacing) = data.path.decodeFirstPool();

    bool zeroForOne = tokenIn < tokenOut;

    (int256 amount0Delta, int256 amount1Delta) = getPool(tokenIn, tokenOut, tickSpacing).swap(
        recipient,
        zeroForOne,
        -amountOut.toInt256(),  // Negative = exact output
        sqrtPriceLimitX96 == 0
            ? (zeroForOne ? TickMath.MIN_SQRT_RATIO + 1 : TickMath.MAX_SQRT_RATIO - 1)
            : sqrtPriceLimitX96,
        abi.encode(data)
    );

    uint256 amountOutReceived;
    (amountIn, amountOutReceived) = zeroForOne
        ? (uint256(amount0Delta), uint256(-amount1Delta))
        : (uint256(amount1Delta), uint256(-amount0Delta));

    require(amountOutReceived == amountOut, "IIA");  // Invalid Internal Amount
}
```

## Multi-Hop Swaps

```solidity
struct ExactInputParams {
    bytes path;              // Encoded path: token0 + tickSpacing + token1 + ...
    address recipient;
    uint256 deadline;
    uint256 amountIn;
    uint256 amountOutMinimum;
}

/// @notice Multi-hop swap with exact input
function exactInput(ExactInputParams calldata params)
    external
    payable
    checkDeadline(params.deadline)
    returns (uint256 amountOut)
{
    address payer = msg.sender;

    while (true) {
        bool hasMultiplePools = params.path.hasMultiplePools();

        // Execute swap for this hop
        params.amountIn = exactInputInternal(
            params.amountIn,
            hasMultiplePools ? address(this) : params.recipient,
            0,
            SwapCallbackData({
                path: params.path.getFirstPool(),
                payer: payer
            })
        );

        if (hasMultiplePools) {
            payer = address(this);
            params.path = params.path.skipToken();
        } else {
            amountOut = params.amountIn;
            break;
        }
    }

    require(amountOut >= params.amountOutMinimum, "TLR");
}

struct ExactOutputParams {
    bytes path;              // Reversed path: tokenOut + ... + tokenIn
    address recipient;
    uint256 deadline;
    uint256 amountOut;
    uint256 amountInMaximum;
}

/// @notice Multi-hop swap with exact output
function exactOutput(ExactOutputParams calldata params)
    external
    payable
    checkDeadline(params.deadline)
    returns (uint256 amountIn)
{
    // Exact output swaps are executed in reverse
    exactOutputInternal(
        params.amountOut,
        params.recipient,
        0,
        SwapCallbackData({path: params.path, payer: msg.sender})
    );

    amountIn = amountInCached;
    require(amountIn <= params.amountInMaximum, "TMA");
    amountInCached = DEFAULT_AMOUNT_IN_CACHED;
}
```

## Swap Callback

```solidity
/// @notice Called by pool during swap
function uniswapV3SwapCallback(
    int256 amount0Delta,
    int256 amount1Delta,
    bytes calldata _data
) external {
    require(amount0Delta > 0 || amount1Delta > 0, "IA");

    SwapCallbackData memory data = abi.decode(_data, (SwapCallbackData));
    (address tokenIn, address tokenOut, int24 tickSpacing) = data.path.decodeFirstPool();

    // Verify callback is from expected pool
    CallbackValidation.verifyCallback(factory, tokenIn, tokenOut, tickSpacing);

    (bool isExactInput, uint256 amountToPay) = amount0Delta > 0
        ? (tokenIn < tokenOut, uint256(amount0Delta))
        : (tokenOut < tokenIn, uint256(amount1Delta));

    if (isExactInput) {
        pay(tokenIn, data.payer, msg.sender, amountToPay);
    } else {
        // For exact output, need to continue path or pay
        if (data.path.hasMultiplePools()) {
            data.path = data.path.skipToken();
            exactOutputInternal(amountToPay, msg.sender, 0, data);
        } else {
            amountInCached = amountToPay;
            tokenIn = tokenOut;
            pay(tokenIn, data.payer, msg.sender, amountToPay);
        }
    }
}
```

## Path Encoding

```solidity
// Path.sol

// Path format: token0 (20 bytes) + tickSpacing (3 bytes) + token1 (20 bytes) + ...
// Each pool segment is 23 bytes (20 + 3)

/// @notice Decode first pool from path
function decodeFirstPool(bytes memory path)
    internal pure
    returns (address tokenA, address tokenB, int24 tickSpacing)
{
    require(path.length >= 43, "IPL");  // Invalid path length

    assembly {
        tokenA := mload(add(path, 20))
        tickSpacing := mload(add(path, 23))
        tokenB := mload(add(path, 43))
    }
}

/// @notice Check if path has multiple pools
function hasMultiplePools(bytes memory path) internal pure returns (bool) {
    return path.length >= 66;  // 43 + 23 = 66 for two pools
}

/// @notice Skip first token in path
function skipToken(bytes memory path) internal pure returns (bytes memory) {
    return path.slice(23, path.length - 23);
}
```

## QuoterV2

```solidity
// periphery/lens/QuoterV2.sol

contract QuoterV2 is IQuoterV2 {
    /// @notice Quote exact input single hop
    function quoteExactInputSingle(QuoteExactInputSingleParams memory params)
        public
        returns (
            uint256 amountOut,
            uint160 sqrtPriceX96After,
            uint32 initializedTicksCrossed,
            uint256 gasEstimate
        )
    {
        bool zeroForOne = params.tokenIn < params.tokenOut;
        ICLPool pool = getPool(params.tokenIn, params.tokenOut, params.tickSpacing);

        uint256 gasBefore = gasleft();

        try pool.swap(
            address(this),
            zeroForOne,
            params.amountIn.toInt256(),
            params.sqrtPriceLimitX96 == 0
                ? (zeroForOne ? TickMath.MIN_SQRT_RATIO + 1 : TickMath.MAX_SQRT_RATIO - 1)
                : params.sqrtPriceLimitX96,
            abi.encodePacked(params.tokenIn, params.tickSpacing, params.tokenOut)
        ) {} catch (bytes memory reason) {
            gasEstimate = gasBefore - gasleft();
            return handleRevert(reason, pool, gasEstimate);
        }
    }

    /// @notice Handle revert and extract quote data
    function handleRevert(
        bytes memory reason,
        ICLPool pool,
        uint256 gasEstimate
    ) private view returns (
        uint256 amountOut,
        uint160 sqrtPriceX96After,
        uint32 initializedTicksCrossed,
        uint256
    ) {
        // Quoter uses try/catch pattern
        // Swap reverts with data that we decode here
        if (reason.length != 128) {
            if (reason.length < 68) revert("Unexpected error");
            assembly {
                reason := add(reason, 0x04)
            }
            revert(abi.decode(reason, (string)));
        }

        return (
            abi.decode(reason, (uint256, uint160, uint32)),
            gasEstimate
        );
    }

    /// @notice Quote callback - always reverts with data
    function uniswapV3SwapCallback(
        int256 amount0Delta,
        int256 amount1Delta,
        bytes memory path
    ) external view {
        // Extract pool info from path
        (address tokenIn, address tokenOut,) = path.decodeFirstPool();

        (int256 amountOut, int256 amountIn) = tokenIn < tokenOut
            ? (amount1Delta, amount0Delta)
            : (amount0Delta, amount1Delta);

        // Get final state
        (uint160 sqrtPriceX96After, int24 tickAfter,,,) = ICLPool(msg.sender).slot0();

        // Revert with quote data
        assembly {
            let ptr := mload(0x40)
            mstore(ptr, amountIn)
            mstore(add(ptr, 0x20), sqrtPriceX96After)
            mstore(add(ptr, 0x40), tickAfter)
            revert(ptr, 96)
        }
    }
}
```

## Quote Multi-Hop

```solidity
/// @notice Quote exact input multi-hop
function quoteExactInput(bytes memory path, uint256 amountIn)
    public
    returns (
        uint256 amountOut,
        uint160[] memory sqrtPriceX96AfterList,
        uint32[] memory initializedTicksCrossedList,
        uint256 gasEstimate
    )
{
    sqrtPriceX96AfterList = new uint160[](path.numPools());
    initializedTicksCrossedList = new uint32[](path.numPools());

    uint256 i = 0;
    while (true) {
        (address tokenIn, address tokenOut, int24 tickSpacing) = path.decodeFirstPool();

        (
            uint256 _amountOut,
            uint160 _sqrtPriceX96After,
            uint32 _initializedTicksCrossed,
            uint256 _gasEstimate
        ) = quoteExactInputSingle(
            QuoteExactInputSingleParams({
                tokenIn: tokenIn,
                tokenOut: tokenOut,
                tickSpacing: tickSpacing,
                amountIn: amountIn,
                sqrtPriceLimitX96: 0
            })
        );

        sqrtPriceX96AfterList[i] = _sqrtPriceX96After;
        initializedTicksCrossedList[i] = _initializedTicksCrossed;
        amountIn = _amountOut;
        gasEstimate += _gasEstimate;
        i++;

        if (path.hasMultiplePools()) {
            path = path.skipToken();
        } else {
            amountOut = amountIn;
            break;
        }
    }
}
```

## Usage Examples

```solidity
// Example 1: Simple swap ETH → USDC
router.exactInputSingle(
    ISwapRouter.ExactInputSingleParams({
        tokenIn: WETH,
        tokenOut: USDC,
        tickSpacing: 100,
        recipient: msg.sender,
        deadline: block.timestamp + 300,
        amountIn: 1 ether,
        amountOutMinimum: 1800e6,  // Min 1800 USDC
        sqrtPriceLimitX96: 0
    })
);

// Example 2: Multi-hop swap ETH → USDC → DAI
bytes memory path = abi.encodePacked(
    WETH,
    int24(100),   // ETH/USDC tickSpacing
    USDC,
    int24(1),     // USDC/DAI tickSpacing (stable)
    DAI
);

router.exactInput(
    ISwapRouter.ExactInputParams({
        path: path,
        recipient: msg.sender,
        deadline: block.timestamp + 300,
        amountIn: 1 ether,
        amountOutMinimum: 1800e18  // Min 1800 DAI
    })
);
```

## Events

```solidity
// No specific router events - uses pool Swap events
```

## Reference Files

- `contracts/periphery/SwapRouter.sol` - Swap execution
- `contracts/periphery/lens/QuoterV2.sol` - Quote simulation
- `contracts/periphery/libraries/Path.sol` - Path encoding
- `contracts/periphery/libraries/CallbackValidation.sol` - Callback verification
