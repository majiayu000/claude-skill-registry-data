---
name: forge-testing
description: Foundry cheatcodes, assertions, and forge test CLI. Use for vm.prank, expectRevert, verbosity, and general Foundry mechanics. For Crane/IndexedEx protocol and Diamond tests, prefer crane-testing and production-first deploy paths over mocks.
---

# Forge Testing

Write native Solidity tests using Foundry's testing framework.

## Crane / IndexedEx note (read first)

In this monorepo, **prefer production contracts and factory/TestBase deploy paths**. Do not invent mocks for facets, DFPkgs, vaults, or managers.

- **Crane:** use `crane-testing` + inherit `CraneTest` (not `new` for production Crane contracts).
- **IndexedEx:** use `indexedex-testing` + `IndexedexTest` / protocol TestBases.
- This skill covers **Foundry mechanics** (cheatcodes, asserts, CLI). Its generic `new MyContract()` / mock examples are **not** the preferred pattern for Crane or IndexedEx features.

## When to Use

- Foundry cheatcodes, assertions, verbosity, CLI filters
- Debugging failing tests with traces
- Fork/select fork mechanics (combined with project TestBases)
- Not the primary skill for Diamond/DFPkg/vault test design — use `crane-testing` / `indexedex-testing`

## Quick Start (generic Foundry)

For Crane work, replace `new MyContract()` with factory/TestBase setup from `crane-testing`.

```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

import {Test, console} from "forge-std/Test.sol";
import {MyContract} from "../src/MyContract.sol";

contract MyContractTest is Test {
    MyContract public target;

    function setUp() public {
        // Generic example only. Crane: inherit CraneTest + factories.
        target = new MyContract();
    }

    function test_BasicFunction() public {
        uint256 result = target.doSomething();
        assertEq(result, 42);
    }

    function testFail_ShouldRevert() public {
        target.functionThatReverts();
    }
}
```

## Test Naming Conventions

| Prefix | Behavior |
|--------|----------|
| `test_` or `test` | Expected to pass |
| `testFail_` or `testFail` | Expected to revert |
| `testFuzz_` | Fuzz test with random inputs |

## Running Tests

```bash
# Run all tests
forge test

# Run specific test contract
forge test --match-contract MyContractTest

# Run specific test function
forge test --match-test test_BasicFunction

# Run with verbosity (show logs)
forge test -vvv

# Watch mode
forge test --watch
```

## Verbosity Levels

| Flag | Output |
|------|--------|
| (none) | Summary only |
| `-vv` | Logs and assertion failures |
| `-vvv` | Stack traces for failures |
| `-vvvv` | Setup traces for failures |
| `-vvvvv` | All traces including setup |

## Essential Cheatcodes

See [cheatcodes.md](cheatcodes.md) for the complete reference.

### State Manipulation

```solidity
// Set caller for next call
vm.prank(address(0x123));

// Set caller for multiple calls
vm.startPrank(address(0x123));
// ... calls as 0x123
vm.stopPrank();

// Give ETH to address
vm.deal(address(0x123), 1 ether);

// Set block timestamp
vm.warp(block.timestamp + 1 days);

// Set block number
vm.roll(block.number + 100);
```

### Expecting Reverts

```solidity
// Expect any revert
vm.expectRevert();
target.functionThatReverts();

// Expect specific error
vm.expectRevert("Insufficient balance");
target.withdraw(1000);

// Expect custom error
vm.expectRevert(InsufficientBalance.selector);
target.withdraw(1000);
```

### Expecting Events

```solidity
// Expect event (check all indexed topics + data)
vm.expectEmit(true, true, true, true);
emit Transfer(from, to, amount);
target.transfer(to, amount);
```

## Assertions

See [assertions.md](assertions.md) for the complete reference.

```solidity
// Equality
assertEq(a, b);
assertEq(a, b, "custom error message");

// Comparisons
assertGt(a, b);  // a > b
assertGe(a, b);  // a >= b
assertLt(a, b);  // a < b
assertLe(a, b);  // a <= b

// Approximate equality (for decimals)
assertApproxEqAbs(a, b, maxDelta);
assertApproxEqRel(a, b, maxPercentDelta);

// Boolean
assertTrue(condition);
assertFalse(condition);
```

## Console Logging

```solidity
import {console} from "forge-std/Test.sol";

console.log("Value:", someValue);
console.log("Address:", someAddress);
console.logBytes32(someHash);
```

## Common Patterns

See [patterns.md](patterns.md) for detailed examples.

### Testing as Different Users

```solidity
address alice = makeAddr("alice");
address bob = makeAddr("bob");

vm.deal(alice, 10 ether);
vm.prank(alice);
target.deposit{value: 1 ether}();
```

### Fork Testing

```solidity
function setUp() public {
    vm.createSelectFork("mainnet");
}

function test_InteractWithMainnet() public {
    IERC20 dai = IERC20(0x6B175474E89094C44Da98b954EesdfeCaE69310);
    // Test against real mainnet state
}
```

### Storage Manipulation

```solidity
// Write to specific storage slot
vm.store(address(target), bytes32(uint256(0)), bytes32(uint256(100)));

// Read from storage slot
bytes32 value = vm.load(address(target), bytes32(uint256(0)));
```
