---
name: Euler Oracle System
description: This skill should be used when the user asks about "oracle", "EulerRouter", "price feed", "Chainlink", "Uniswap TWAP", "Pyth", "Chronicle", "adapter", "quote", "bid/ask", or needs to understand Euler's modular oracle infrastructure.
version: 0.1.0
---

# Euler Oracle System

Euler uses a modular oracle system with EulerRouter as the central coordinator. The router resolves pricing through adapters supporting Chainlink, Uniswap V3 TWAP, Pyth, Chronicle, and more.

## Overview

```
┌──────────────────────────────────────────────────────────────┐
│                   EULER ORACLE ARCHITECTURE                  │
├──────────────────────────────────────────────────────────────┤
│                                                              │
│                    ┌─────────────────┐                       │
│                    │  EulerRouter    │                       │
│                    │  (Coordinator)  │                       │
│                    └────────┬────────┘                       │
│                             │                                │
│           ┌─────────────────┼─────────────────┐              │
│           │                 │                 │              │
│     ┌─────▼─────┐    ┌──────▼──────┐   ┌──────▼──────┐       │
│     │ Chainlink │    │ Uniswap V3  │   │   Pyth      │       │
│     │ Adapter   │    │ TWAP Adapter│   │  Adapter    │       │
│     └───────────┘    └─────────────┘   └─────────────┘       │
│                                                              │
│     ┌───────────┐    ┌─────────────┐   ┌─────────────┐       │
│     │ Chronicle │    │   Redstone  │   │   Custom    │       │
│     │ Adapter   │    │   Adapter   │   │   Adapter   │       │
│     └───────────┘    └─────────────┘   └─────────────┘       │
│                                                              │
│  Key Features:                                               │
│  ├── Asset → Unit of Account pricing                         │
│  ├── Bid/Ask spread support                                  │
│  ├── Fallback oracle support                                 │
│  └── Cross routing for derived prices                        │
│                                                              │
└──────────────────────────────────────────────────────────────┘
```

## EulerRouter

```solidity
// euler-price-oracle/src/EulerRouter.sol

contract EulerRouter is Governable {
    // Oracle configuration per base/quote pair
    mapping(address base => mapping(address quote => address oracle)) internal configs;

    // Fallback oracles
    mapping(address base => mapping(address quote => address fallback)) internal fallbacks;

    /// @notice Get a quote for converting amount of base to quote
    /// @param amount Amount of base token
    /// @param base Base token address
    /// @param quote Quote token address
    /// @return outAmount Amount in quote token
    function getQuote(
        uint256 amount,
        address base,
        address quote
    ) external view returns (uint256 outAmount) {
        (outAmount,) = _getQuote(amount, base, quote);
    }

    /// @notice Get quotes with bid/ask spread
    /// @return bidOutAmount Bid price (sell base for quote)
    /// @return askOutAmount Ask price (buy base with quote)
    function getQuotes(
        uint256 amount,
        address base,
        address quote
    ) external view returns (uint256 bidOutAmount, uint256 askOutAmount) {
        return _getQuotes(amount, base, quote);
    }

    function _getQuote(
        uint256 amount,
        address base,
        address quote
    ) internal view returns (uint256 outAmount, bool usedFallback) {
        if (base == quote) return (amount, false);
        if (amount == 0) return (0, false);

        // Try primary oracle
        address oracle = configs[base][quote];
        if (oracle != address(0)) {
            try IPriceOracle(oracle).getQuote(amount, base, quote) returns (uint256 result) {
                return (result, false);
            } catch {}
        }

        // Try fallback
        address fallbackOracle = fallbacks[base][quote];
        if (fallbackOracle != address(0)) {
            return (IPriceOracle(fallbackOracle).getQuote(amount, base, quote), true);
        }

        // Try inverse pair
        oracle = configs[quote][base];
        if (oracle != address(0)) {
            uint256 inverseAmount = IPriceOracle(oracle).getQuote(
                10 ** IERC20Metadata(quote).decimals(),
                quote,
                base
            );
            return (amount * 10 ** IERC20Metadata(quote).decimals() / inverseAmount, false);
        }

        revert PriceOracle_NotConfigured(base, quote);
    }
}
```

## Router Configuration

```solidity
// EulerRouter.sol - Admin functions

/// @notice Set oracle for a base/quote pair
/// @param base Base token
/// @param quote Quote token
/// @param oracle Oracle adapter address
function setConfig(
    address base,
    address quote,
    address oracle
) external onlyGovernor {
    configs[base][quote] = oracle;
    emit ConfigSet(base, quote, oracle);
}

/// @notice Set fallback oracle
function setFallback(
    address base,
    address quote,
    address fallbackOracle
) external onlyGovernor {
    fallbacks[base][quote] = fallbackOracle;
    emit FallbackSet(base, quote, fallbackOracle);
}

/// @notice Batch configuration
function setConfigs(
    address[] calldata bases,
    address[] calldata quotes,
    address[] calldata oracles
) external onlyGovernor {
    require(bases.length == quotes.length && quotes.length == oracles.length);
    for (uint i = 0; i < bases.length; i++) {
        configs[bases[i]][quotes[i]] = oracles[i];
        emit ConfigSet(bases[i], quotes[i], oracles[i]);
    }
}

/// @notice Get current config
function getConfig(address base, address quote) external view returns (address) {
    return configs[base][quote];
}
```

## Chainlink Adapter

```solidity
// euler-price-oracle/src/adapter/chainlink/ChainlinkOracle.sol

contract ChainlinkOracle is IPriceOracle {
    address public immutable base;
    address public immutable quote;
    address public immutable feed;
    uint256 public immutable maxStaleness;

    constructor(
        address _base,
        address _quote,
        address _feed,
        uint256 _maxStaleness
    ) {
        base = _base;
        quote = _quote;
        feed = _feed;
        maxStaleness = _maxStaleness;
    }

    function getQuote(
        uint256 amount,
        address _base,
        address _quote
    ) external view returns (uint256) {
        require(_base == base && _quote == quote, "Invalid pair");

        (
            ,
            int256 answer,
            ,
            uint256 updatedAt,
        ) = AggregatorV3Interface(feed).latestRoundData();

        require(answer > 0, "Invalid price");
        require(block.timestamp - updatedAt <= maxStaleness, "Stale price");

        uint8 feedDecimals = AggregatorV3Interface(feed).decimals();
        uint8 baseDecimals = IERC20Metadata(base).decimals();
        uint8 quoteDecimals = IERC20Metadata(quote).decimals();

        // amount * price / 10^baseDecimals * 10^quoteDecimals / 10^feedDecimals
        return amount * uint256(answer) * 10 ** quoteDecimals / 10 ** baseDecimals / 10 ** feedDecimals;
    }
}
```

## Uniswap V3 TWAP Adapter

```solidity
// euler-price-oracle/src/adapter/uniswap/UniswapV3Oracle.sol

contract UniswapV3Oracle is IPriceOracle {
    address public immutable pool;
    address public immutable base;
    address public immutable quote;
    uint32 public immutable twapWindow;  // Seconds for TWAP

    function getQuote(
        uint256 amount,
        address _base,
        address _quote
    ) external view returns (uint256) {
        require(_base == base && _quote == quote, "Invalid pair");

        // Get time-weighted tick from pool
        uint32[] memory secondsAgos = new uint32[](2);
        secondsAgos[0] = twapWindow;
        secondsAgos[1] = 0;

        (int56[] memory tickCumulatives,) = IUniswapV3Pool(pool).observe(secondsAgos);

        int56 tickCumulativeDelta = tickCumulatives[1] - tickCumulatives[0];
        int24 arithmeticMeanTick = int24(tickCumulativeDelta / int56(uint56(twapWindow)));

        // Adjust for rounding
        if (tickCumulativeDelta < 0 && (tickCumulativeDelta % int56(uint56(twapWindow)) != 0)) {
            arithmeticMeanTick--;
        }

        // Convert tick to price
        uint160 sqrtPriceX96 = TickMath.getSqrtRatioAtTick(arithmeticMeanTick);

        // Calculate quote amount
        if (base == IUniswapV3Pool(pool).token0()) {
            return FullMath.mulDiv(
                amount,
                FullMath.mulDiv(sqrtPriceX96, sqrtPriceX96, 1 << 64),
                1 << 128
            );
        } else {
            return FullMath.mulDiv(
                amount,
                1 << 128,
                FullMath.mulDiv(sqrtPriceX96, sqrtPriceX96, 1 << 64)
            );
        }
    }
}
```

## Pyth Adapter

```solidity
// euler-price-oracle/src/adapter/pyth/PythOracle.sol

contract PythOracle is IPriceOracle {
    IPyth public immutable pyth;
    bytes32 public immutable priceId;
    address public immutable base;
    address public immutable quote;
    uint256 public immutable maxStaleness;

    function getQuote(
        uint256 amount,
        address _base,
        address _quote
    ) external view returns (uint256) {
        require(_base == base && _quote == quote, "Invalid pair");

        PythStructs.Price memory price = pyth.getPriceNoOlderThan(priceId, maxStaleness);

        require(price.price > 0, "Invalid price");

        // Pyth prices have variable exponents
        int32 expo = price.expo;
        uint64 priceVal = uint64(price.price);

        uint8 baseDecimals = IERC20Metadata(base).decimals();
        uint8 quoteDecimals = IERC20Metadata(quote).decimals();

        // Adjust for exponent and decimals
        if (expo >= 0) {
            return amount * priceVal * 10 ** uint32(expo) * 10 ** quoteDecimals / 10 ** baseDecimals;
        } else {
            return amount * priceVal * 10 ** quoteDecimals / 10 ** uint32(-expo) / 10 ** baseDecimals;
        }
    }
}
```

## Chronicle Adapter

```solidity
// euler-price-oracle/src/adapter/chronicle/ChronicleOracle.sol

contract ChronicleOracle is IPriceOracle {
    IChronicle public immutable chronicle;
    address public immutable base;
    address public immutable quote;
    uint256 public immutable maxStaleness;

    function getQuote(
        uint256 amount,
        address _base,
        address _quote
    ) external view returns (uint256) {
        require(_base == base && _quote == quote, "Invalid pair");

        (uint256 val, uint256 age) = chronicle.readWithAge();

        require(val > 0, "Invalid price");
        require(block.timestamp - age <= maxStaleness, "Stale price");

        uint8 baseDecimals = IERC20Metadata(base).decimals();
        uint8 quoteDecimals = IERC20Metadata(quote).decimals();

        // Chronicle prices are 18 decimals
        return amount * val * 10 ** quoteDecimals / 10 ** baseDecimals / 1e18;
    }
}
```

## Cross Routing

```solidity
// EulerRouter.sol - Cross routing for derived prices

contract CrossAdapter is IPriceOracle {
    address public immutable router;
    address public immutable base;
    address public immutable cross;  // Intermediate token
    address public immutable quote;

    /// @notice Get quote by routing through cross token
    /// Example: WBTC → ETH → USD
    /// 1. Get WBTC → ETH price
    /// 2. Get ETH → USD price
    /// 3. Combine
    function getQuote(
        uint256 amount,
        address _base,
        address _quote
    ) external view returns (uint256) {
        require(_base == base && _quote == quote, "Invalid pair");

        // First leg: base → cross
        uint256 crossAmount = IEulerRouter(router).getQuote(amount, base, cross);

        // Second leg: cross → quote
        return IEulerRouter(router).getQuote(crossAmount, cross, quote);
    }
}

// Example configuration:
// WBTC → USD: CrossAdapter(router, WBTC, WETH, USD)
// Router will:
// 1. WBTC → WETH via Uniswap TWAP
// 2. WETH → USD via Chainlink
```

## Bid/Ask Spread

```solidity
// Some adapters support bid/ask spreads

contract SpreadOracle is IPriceOracle {
    address public immutable baseOracle;
    uint256 public immutable spreadBps;  // Spread in basis points

    function getQuotes(
        uint256 amount,
        address base,
        address quote
    ) external view returns (uint256 bidOut, uint256 askOut) {
        uint256 midPrice = IPriceOracle(baseOracle).getQuote(amount, base, quote);

        // Apply spread
        bidOut = midPrice * (10000 - spreadBps) / 10000;  // Lower (sell price)
        askOut = midPrice * (10000 + spreadBps) / 10000;  // Higher (buy price)
    }
}

// Usage in liquidation:
// - Collateral valued at bid price (conservative)
// - Debt valued at ask price (conservative)
// This protects the protocol from oracle manipulation
```

## Staleness Protection

```solidity
// All adapters implement staleness checks

modifier checkStaleness(uint256 updatedAt) {
    require(block.timestamp - updatedAt <= maxStaleness, "Stale price");
    _;
}

// Staleness params should be:
// - Short enough to catch stale oracles
// - Long enough to handle temporary RPC issues
// - Typical: 3600s (1 hour) for Chainlink
// - Shorter for high-volatility assets
```

## Unit of Account

```solidity
// EVault uses oracle to convert to unit of account

// Common units of account:
// - USD (address(840) or dedicated stablecoin)
// - ETH (WETH address)
// - BTC (WBTC address)

// Example vault setup:
// - Asset: USDC
// - Unit of Account: USD
// - Collateral 1: WETH (need WETH/USD oracle)
// - Collateral 2: WBTC (need WBTC/USD oracle)

// All values converted to USD for comparison:
// - Debt: 1000 USDC = $1000
// - Collateral: 0.5 WETH = $1500 (at $3000/ETH)
// - Health: $1500 > $1000 ✓
```

## Events

```solidity
event ConfigSet(address indexed base, address indexed quote, address indexed oracle);
event FallbackSet(address indexed base, address indexed quote, address indexed fallback);
event OracleError(address indexed base, address indexed quote, bytes reason);
```

## Reference Files

- `euler-price-oracle/src/EulerRouter.sol` - Main router
- `euler-price-oracle/src/adapter/chainlink/` - Chainlink adapters
- `euler-price-oracle/src/adapter/uniswap/` - Uniswap TWAP adapters
- `euler-price-oracle/src/adapter/pyth/` - Pyth adapters
- `euler-price-oracle/src/adapter/chronicle/` - Chronicle adapters
- `euler-price-oracle/src/adapter/redstone/` - Redstone adapters
