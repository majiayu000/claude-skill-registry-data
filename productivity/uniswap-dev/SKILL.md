---
name: uniswap-dev
description: >
  Comprehensive development support for Uniswap Protocol (v2/v3/v4), SDK integration, Subgraph API,
  and smart contract development. Use when building DeFi applications with Uniswap including - (1) Token
  swaps and routing, (2) Liquidity provision and management, (3) Custom hooks and AMM logic (v4),
  (4) Subgraph data queries and analytics, (5) Contract integration and testing, (6) Version selection
  and migration, (7) Security best practices implementation. Covers SDK usage (TypeScript/JavaScript),
  smart contract development (Solidity), API integration (GraphQL), and protocol-specific features like
  concentrated liquidity (v3) and hooks (v4).
---

# Uniswap Development Support

Comprehensive toolkit for building applications with Uniswap Protocol across all versions (v2, v3, v4) and UniswapX.

## Quick Start

### Version Selection

Always start by choosing the right version. See [version-guide.md](references/version-guide.md) for detailed comparison.

**Quick decision**:
- New project with custom AMM logic → **v4** (hooks, gas efficiency)
- Production DeFi integration → **v3** (battle-tested, mature ecosystem)
- Simple swaps, legacy → **v2** (simple, stable)
- End-user trading interface → **UniswapX** (MEV protection, gasless)

### Common Tasks

**1. Implement a swap**:
- Review [swap_v4_example.ts](scripts/swap_v4_example.ts) for v4 implementation
- Key points: slippage protection, deadline, proper token approval
- See [security.md](references/security.md) for critical security patterns

**2. Query pool data**:
- Use [subgraph_query.py](scripts/subgraph_query.py) for analytics
- See [subgraph-schema.md](references/subgraph-schema.md) for query patterns

**3. Create custom hook (v4)**:
- Start with [hook-template.sol](assets/hook-template.sol)
- Read [v4-hooks.md](references/v4-hooks.md) for patterns and lifecycle
- Mine hook address with correct permission bits

**4. Security implementation**:
- Review [security.md](references/security.md) before any production deployment
- Implement slippage protection, deadline, TWAP oracles
- Never skip security checklist

## Core Workflows

### Swap Implementation

```typescript
// 1. Setup SDK and tokens
import { CurrencyAmount, Token, Percent } from '@uniswap/sdk-core';
import { Pool, Route, Trade } from '@uniswap/v4-sdk';

// 2. Get pool state from PoolManager
const poolState = await poolManager.getPool(...);

// 3. Create trade with slippage protection
const slippageTolerance = new Percent(50, 10000); // 0.5%
const minimumAmountOut = trade.minimumAmountOut(slippageTolerance);

// 4. Execute with deadline
const deadline = Math.floor(Date.now() / 1000) + 60 * 20; // 20 min
```

See [swap_v4_example.ts](scripts/swap_v4_example.ts) for complete implementation.

### Liquidity Provision (v3)

```solidity
// Add liquidity with concentrated range
INonfungiblePositionManager.MintParams memory params =
    INonfungiblePositionManager.MintParams({
        token0: token0,
        token1: token1,
        fee: 3000,  // 0.3%
        tickLower: -887220,
        tickUpper: 887220,
        amount0Desired: amount0,
        amount1Desired: amount1,
        amount0Min: amount0 * 95 / 100,  // Slippage protection
        amount1Min: amount1 * 95 / 100,
        recipient: msg.sender,
        deadline: deadline
    });

positionManager.mint(params);
```

### Custom Hook Development (v4)

```solidity
// 1. Extend BaseHook
contract MyHook is BaseHook {
    constructor(IPoolManager _poolManager) BaseHook(_poolManager) {}

    // 2. Declare permissions
    function getHookPermissions() public pure override
        returns (Hooks.Permissions memory) {
        return Hooks.Permissions({
            beforeSwap: true,
            afterSwap: true,
            // ... other permissions
        });
    }

    // 3. Implement hook logic
    function beforeSwap(...) external override returns (...) {
        // Custom logic
        return (this.beforeSwap.selector, BeforeSwapDelta.ZERO, dynamicFee);
    }
}
```

See [v4-hooks.md](references/v4-hooks.md) for patterns and [hook-template.sol](assets/hook-template.sol) for template.

### Subgraph Queries

```python
from subgraph_query import UniswapSubgraph

subgraph = UniswapSubgraph()

# Get pool data
pool = subgraph.get_pool("0x88e6a0c2ddd26feeb64f039a2c41296fcb3f5640")
print(f"TVL: ${pool['totalValueLockedUSD']}")

# Track recent swaps
swaps = subgraph.get_recent_swaps(pool_address, limit=100)

# User positions
positions = subgraph.get_user_positions(user_address)
```

See [subgraph_query.py](scripts/subgraph_query.py) and [subgraph-schema.md](references/subgraph-schema.md).

## Critical Security Requirements

**Never deploy without**:

1. **Slippage protection**: Always set `amountOutMinimum` or `amountInMaximum`
2. **Deadline protection**: Set realistic deadlines (e.g., 20 minutes)
3. **TWAP for oracles**: Never use spot prices for critical decisions
4. **Callback validation**: Verify callbacks are from legitimate pools (v3/v4)
5. **Reentrancy guards**: Protect state-changing functions

See [security.md](references/security.md) for complete checklist and examples.

## Architecture Patterns

### v4 Singleton Architecture

All pools exist in a single `PoolManager` contract:
- Massive gas savings (no per-pool deployment)
- Flash accounting for efficient batch operations
- Hooks attached at pool creation

```solidity
// Pool identified by PoolKey
PoolKey memory key = PoolKey({
    currency0: token0,
    currency1: token1,
    fee: 3000,
    tickSpacing: 60,
    hooks: IHooks(hookAddress)
});

poolManager.initialize(key, sqrtPriceX96);
```

### v3 Concentrated Liquidity

Provide liquidity in specific price ranges for capital efficiency:

```solidity
// Concentrated range: 1 ETH = $1800-$2200
int24 tickLower = getTickAtPrice(1800);
int24 tickUpper = getTickAtPrice(2200);

positionManager.mint(token0, token1, fee, tickLower, tickUpper, ...);
```

## Development Setup

### Dependencies

**v4 Development**:
```bash
npm install @uniswap/v4-sdk @uniswap/v4-core @uniswap/v4-periphery
npm install @uniswap/sdk-core ethers
```

**v3 Development**:
```bash
npm install @uniswap/v3-sdk @uniswap/v3-core @uniswap/v3-periphery
```

**Subgraph Queries**:
```bash
# TypeScript
npm install graphql graphql-request

# Python
pip install requests
```

### Contract Addresses

**v4 (Mainnet)**:
- PoolManager: `0x...` (Check latest deployment)

**v3 (Mainnet)**:
- Factory: `0x1F98431c8aD98523631AE4a59f267346ea31F984`
- SwapRouter: `0xE592427A0AEce92De3Edee1F18E0157C05861564`
- NonfungiblePositionManager: `0xC36442b4a4522E871399CD717aBDD847Ab11FE88`
- Quoter: `0xb27308f9F90D607463bb33eA1BeBb41C27CE5AB6`

**v2 (Mainnet)**:
- Factory: `0x5C69bEe701ef814a2B6a3EDD4B1652CB9cc5aA6f`
- Router: `0x7a250d5630B4cF539739dF2C5dAcb4c659F2488D`

## Testing

### Foundry Testing (Recommended for v4)

```solidity
import {Test} from "forge-std/Test.sol";
import {PoolManager} from "v4-core/PoolManager.sol";
import {MyHook} from "../src/MyHook.sol";

contract MyHookTest is Test {
    PoolManager poolManager;
    MyHook hook;

    function setUp() public {
        poolManager = new PoolManager(500000);
        hook = new MyHook(poolManager);
    }

    function testSwapTriggersHook() public {
        // Initialize pool with hook
        PoolKey memory key = PoolKey({...});
        poolManager.initialize(key, SQRT_PRICE_1_1);

        // Execute swap
        poolManager.swap(key, params, hookData);

        // Verify hook was called
        assertEq(hook.swapCount(), 1);
    }
}
```

### SDK Testing

```typescript
import { expect } from 'chai';
import { Trade, Route } from '@uniswap/v4-sdk';

describe('Swap Integration', () => {
  it('should calculate correct minimum output', async () => {
    const slippage = new Percent(50, 10000);
    const minOut = trade.minimumAmountOut(slippage);

    expect(minOut.lessThan(trade.outputAmount)).to.be.true;
  });
});
```

## Common Pitfalls

1. **No slippage protection**: Vulnerable to sandwich attacks
2. **Spot price oracles**: Manipulable via flash loans - use TWAP
3. **Missing deadline**: Stale transactions can execute at bad prices
4. **Wrong token ordering**: Uniswap orders by address, not your preference
5. **Unchecked callbacks**: Validate pool callbacks in v3/v4
6. **Hook address mining**: v4 hooks must have correct permission bits in address
7. **Gas estimation failures**: Always handle estimation errors gracefully

## Resources

### Documentation
- **v4 Docs**: https://docs.uniswap.org/contracts/v4/
- **v3 Docs**: https://docs.uniswap.org/contracts/v3/
- **SDK Docs**: https://docs.uniswap.org/sdk/
- **Subgraph Docs**: https://docs.uniswap.org/api/subgraph/

### Code Examples
- **v4 Template**: https://github.com/Uniswap/v4-template
- **v4 Periphery**: https://github.com/Uniswap/v4-periphery
- **v3 Examples**: https://github.com/Uniswap/examples

### Support
- **Discord**: https://discord.gg/uniswap
- **GitHub**: https://github.com/Uniswap
- **Forum**: https://gov.uniswap.org

## Bundled Resources

### Scripts
- **[swap_v4_example.ts](scripts/swap_v4_example.ts)**: Complete v4 swap implementation with security
- **[subgraph_query.py](scripts/subgraph_query.py)**: Comprehensive Subgraph query examples

### References
- **[version-guide.md](references/version-guide.md)**: Version comparison and selection guide
- **[v4-hooks.md](references/v4-hooks.md)**: Deep dive into v4 hooks system
- **[security.md](references/security.md)**: Security best practices and checklist
- **[subgraph-schema.md](references/subgraph-schema.md)**: Complete Subgraph API reference

### Assets
- **[hook-template.sol](assets/hook-template.sol)**: Production-ready hook template

## Support Context7 Integration

When the user needs up-to-date documentation or specific implementation details not covered in this skill:

1. Identify the library needed (e.g., "@uniswap/v4-sdk", "@uniswap/v3-sdk")
2. Use Context7 MCP tools to query latest documentation
3. Combine Context7 results with this skill's guidance

Example:
```
User: "How do I use the new v4 SDK hook features?"
→ Use Context7: resolve-library-id("@uniswap/v4-sdk")
→ Then query-docs with specific hook questions
→ Apply security patterns from security.md
```
