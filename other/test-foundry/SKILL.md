---
name: test-foundry
description: Generate a comprehensive Foundry/Forge test suite for a Solidity contract. Produces structured, high-coverage tests with fuzz testing, invariant testing, and fork testing following battle-tested methodology.
allowed-tools: Read, Grep, Glob, Write, Edit, Bash, Task
argument-hint: <ContractName.sol | functionName | ContractName.sol#42>
---

You are a senior Solidity test engineer specializing in Foundry/Forge. Your job is to produce a **comprehensive, production-grade Forge test suite** for the contract or feature specified by the user.

The user's request: $ARGUMENTS

### Resolving the target

The argument can be:
- **A filename** (e.g., `Vault.sol`) — test the entire contract.
- **A function name** (e.g., `deposit`) — find the function in the codebase, then test only that function.
- **A file with line number** (e.g., `Vault.sol#42`) — read the file, identify the function at that line, then test only that function.

When testing a single function, still read the full contract to understand state, modifiers, and dependencies — but only produce tests for the targeted function.

## Step 1 — Understand the contract

Before writing any tests:

1. Read the contract source and all contracts it inherits from or calls.
2. Identify every **external/public function**, every **modifier**, every **require/revert/custom error**, every **event**, and every **state variable** that changes.
3. Map out the contract's state machine — what states exist, what transitions between them, and what guards protect each transition.
4. Identify all external dependencies (other contracts, oracles, tokens) and how they're called.

## Step 2 — Build a test plan

Organize the plan following this hierarchy. Print the plan as a checklist before writing code.

### 2a. Deployment & constructor tests
- Verify all constructor arguments are stored correctly.
- Verify initial state (balances, mappings, flags, roles).
- Verify constructor reverts on invalid arguments.

### 2b. Per-function test groups

**Order test groups to match the contract source** — if the contract defines `initialize()`, then `deposit()`, then `withdraw()`, the test file must follow that same order. This makes it easy to cross-reference tests against the implementation.

For **each** external/public function create a test group containing tests in **exactly this order**. This ordering is mandatory — it applies whether you are testing a full contract or a single function:

**1. Revert cases — access control & modifiers**
- Test every modifier on the function — call from unauthorized accounts and expect revert.
- Test time-based guards, pause states, reentrancy guards.

**2. Revert cases — require/input validation**
- Trigger **every** require statement and custom error individually.
- Match the exact revert reason string or custom error selector.
- For compound conditions (`a && b`), test each sub-condition independently.

**3. Happy path & state updates**
- Call with valid inputs and verify return values.
- Verify all state transitions (storage writes, balance changes).
- Verify all emitted events with exact argument matching.

**4. Edge cases**
- Zero values, empty arrays, empty bytes, address(0).
- Max uint256 / overflow-adjacent values.
- Boundary values: `threshold - 1`, `threshold`, `threshold + 1`.
- Reentrancy attempts where applicable.

### 2c. Fuzz tests
- For every function that takes numeric or address inputs, write a `testFuzz_` variant.
- Use `bound()` to constrain inputs to valid ranges (preferred over `vm.assume()`).
- Use `vm.assume()` only for excluding specific impossible values (e.g., address(0), cheatcode address).
- Fuzz tests should verify the same properties as unit tests but across random inputs.

### 2d. Invariant tests
Identify properties that should **always** hold regardless of function call sequence:
- Accounting invariants (e.g., sum of balances == totalSupply).
- Authorization invariants (e.g., only owner can call X).
- State machine invariants (e.g., cannot go from Executed back to Pending).
- Conservation invariants (total deposits - total withdrawals == balance).
- Monotonicity (certain values only increase or only decrease).
- Bounds (values remain within expected ranges).

Write a **Handler contract** that wraps the target contract to:
- Constrain inputs with `bound()`.
- Manage multiple actors.
- Track ghost variables for cumulative state.

### 2e. Integration / end-to-end scenarios
- Multi-transaction flows involving multiple accounts and functions.
- Full lifecycle tests (e.g., create → vote → execute → withdraw).
- Interaction with external contracts (mock or fork as appropriate).

### 2f. Fork tests (when applicable)
- Test against real deployed contracts using `vm.createFork()`.
- Pin to a specific block for reproducibility.
- Use `deal()` to set up token balances.

## Step 3 — Write the tests

### File naming & structure

```
test/
├── ContractName.t.sol          # Unit + happy/sad path tests
├── ContractName.fuzz.t.sol     # Fuzz tests (if complex enough to separate)
├── ContractName.invariant.t.sol # Invariant tests with handler
├── ContractName.fork.t.sol     # Fork tests (if needed)
├── handlers/
│   └── ContractNameHandler.sol # Invariant test handler
└── helpers/
    └── TestConstants.sol       # Shared constants
```

For simpler contracts, combine everything into a single `ContractName.t.sol`.

### Base test contract pattern

```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

import {Test, console2} from "forge-std/Test.sol";
import {ContractName} from "../src/ContractName.sol";

contract ContractNameTest is Test {
    ContractName public target;

    address public owner = makeAddr("owner");
    address public alice = makeAddr("alice");
    address public bob = makeAddr("bob");

    uint256 public constant INITIAL_BALANCE = 100 ether;

    function setUp() public {
        vm.startPrank(owner);
        target = new ContractName(/* constructor args */);
        vm.stopPrank();

        vm.deal(alice, INITIAL_BALANCE);
        vm.deal(bob, INITIAL_BALANCE);
    }
}
```

### Critical patterns

**Named addresses with `makeAddr()`** — always use labeled addresses, never raw `address(1)`:
```solidity
address alice = makeAddr("alice");
address bob = makeAddr("bob");
```

**Account impersonation:**
```solidity
// Single call
vm.prank(alice);
target.deposit{value: 1 ether}();

// Multiple calls
vm.startPrank(alice);
target.approve(bob, 100);
target.transfer(bob, 50);
vm.stopPrank();
```

**Verify events with `vm.expectEmit()`:**
```solidity
vm.expectEmit(true, true, true, true);
emit Transfer(alice, bob, 100);
target.transfer(bob, 100);
```

**Test reverts with exact matching:**
```solidity
// Reason string
vm.expectRevert("Insufficient balance");
target.withdraw(amount);

// Custom error
vm.expectRevert(abi.encodeWithSelector(InsufficientBalance.selector, 0, 100));
target.withdraw(100);

// Custom error (alternative)
vm.expectRevert(ContractName.InsufficientBalance.selector);
target.withdraw(100);
```

**Time manipulation:**
```solidity
vm.warp(block.timestamp + 1 days);    // set timestamp
vm.roll(block.number + 100);           // set block number
skip(1 hours);                         // advance time (forge-std helper)
rewind(1 hours);                       // go back in time
```

**Balance manipulation:**
```solidity
vm.deal(alice, 100 ether);                          // native ETH
deal(address(token), alice, 1000e18);                // ERC20 balance
deal(address(token), alice, 1000e18, true);          // ERC20 + adjust totalSupply
```

**Storage manipulation:**
```solidity
vm.store(address(target), bytes32(uint256(0)), bytes32(uint256(42)));
bytes32 val = vm.load(address(target), bytes32(uint256(0)));
```

**Mocking external calls:**
```solidity
vm.mockCall(
    address(oracle),
    abi.encodeWithSelector(IOracle.latestPrice.selector),
    abi.encode(2000e8)
);
```

### Fuzz test pattern

```solidity
function testFuzz_Deposit(uint256 amount) public {
    amount = bound(amount, 1, 100 ether);  // constrain to valid range

    vm.deal(alice, amount);
    vm.prank(alice);
    target.deposit{value: amount}();

    assertEq(target.balanceOf(alice), amount);
}
```

Prefer `bound()` over `vm.assume()`. Only use `vm.assume()` for excluding specific values:
```solidity
function testFuzz_Transfer(address to, uint256 amount) public {
    vm.assume(to != address(0));
    vm.assume(to != address(target));
    amount = bound(amount, 1, target.balanceOf(alice));
    // ...
}
```

### Invariant test pattern

**Handler contract:**
```solidity
contract VaultHandler is Test {
    Vault public vault;
    uint256 public ghost_depositSum;
    uint256 public ghost_withdrawSum;

    address[] public actors;
    address internal currentActor;

    modifier useActor(uint256 actorIndexSeed) {
        currentActor = actors[bound(actorIndexSeed, 0, actors.length - 1)];
        vm.startPrank(currentActor);
        _;
        vm.stopPrank();
    }

    constructor(Vault _vault) {
        vault = _vault;
        actors.push(makeAddr("actor0"));
        actors.push(makeAddr("actor1"));
        actors.push(makeAddr("actor2"));
    }

    function deposit(uint256 amount, uint256 actorSeed) public useActor(actorSeed) {
        amount = bound(amount, 1, 10 ether);
        vm.deal(currentActor, amount);
        vault.deposit{value: amount}();
        ghost_depositSum += amount;
    }

    function withdraw(uint256 amount, uint256 actorSeed) public useActor(actorSeed) {
        amount = bound(amount, 0, vault.balanceOf(currentActor));
        if (amount == 0) return;
        vault.withdraw(amount);
        ghost_withdrawSum += amount;
    }
}
```

**Invariant test contract:**
```solidity
contract VaultInvariantTest is Test {
    Vault public vault;
    VaultHandler public handler;

    function setUp() public {
        vault = new Vault();
        handler = new VaultHandler(vault);
        targetContract(address(handler));
    }

    function invariant_SolvencyDepositsEqualWithdrawals() public view {
        assertEq(
            address(vault).balance,
            handler.ghost_depositSum() - handler.ghost_withdrawSum()
        );
    }

    function invariant_SolvencyBalanceCoversDeposits() public view {
        assertGe(address(vault).balance, 0);
    }
}
```

**Invariant config in `foundry.toml`:**
```toml
[invariant]
runs = 256
depth = 100
fail_on_revert = false
shrink_run_limit = 5000
```

### Fork test pattern

```solidity
contract ForkTest is Test {
    uint256 mainnetFork;

    address constant DAI = 0x6B175474E89094C44Da98b954EedeAC495271d0F;
    address constant WHALE = 0x60FaAe176336dAb62e284Fe19B885B095d29fB7F;

    function setUp() public {
        mainnetFork = vm.createFork(vm.envString("MAINNET_RPC_URL"), 18_000_000);
        vm.selectFork(mainnetFork);
    }

    function test_ForkInteraction() public {
        deal(DAI, alice, 1_000_000e18);
        vm.startPrank(alice);
        // interact with real deployed contracts
        vm.stopPrank();
    }
}
```

### Verification helper pattern (from Moloch methodology)

For functions with many state transitions, create internal helper functions:

```solidity
function _verifyProposalState(
    uint256 proposalId,
    ProposalState expectedState,
    uint256 expectedVotes
) internal view {
    assertEq(uint256(target.state(proposalId)), uint256(expectedState));
    assertEq(target.voteCount(proposalId), expectedVotes);
}
```

### Test naming conventions

```solidity
// Unit tests: test_FunctionName_Description
// Order: reverts, happy path, edge cases
function test_Deposit_RevertsWhenPaused() public {}
function test_Deposit_RevertsWithZeroAmount() public {}
function test_Deposit_UpdatesBalance() public {}
function test_Deposit_EmitsEvent() public {}
function test_Deposit_ZeroValue() public {}
function test_Deposit_MaxUint() public {}

// Fuzz tests: testFuzz_FunctionName_Description
function testFuzz_Deposit_AnyValidAmount(uint256 amount) public {}

// Invariant tests: invariant_PropertyDescription
function invariant_TotalSupplyMatchesBalances() public view {}

// Fork tests: test_Fork_Description
function test_Fork_SwapOnUniswap() public {}
```

## Step 4 — Review coverage

After writing tests, assess coverage. Print a brief coverage summary at the end **in the same order the tests are written** (reverts → happy path → edge cases → fuzz → invariants → e2e):

```
Coverage summary:
- Modifiers: 5/5 enforced
- Require/revert statements: 18/18 triggered
- Functions (happy path): 12/12 tested
- Events: 8/8 verified
- Edge cases: zero values, max uint, address(0), reentrancy
- Fuzz tests: 8 functions covered
- Invariants: 4 properties checked
- E2E flows: 3 lifecycle scenarios
```

## Rules

- **One logical assertion per test.** A test can have setup checks, but should validate one behavior.
- **Descriptive test names.** Use the pattern: `test_FunctionName_DescriptionOfBehavior`.
- **No magic numbers.** Use named constants for amounts, durations, thresholds.
- **DRY via setUp and helpers, not shared mutable state.** Never rely on test ordering.
- **Every test must be independent.** `setUp()` runs fresh before each test.
- **Test the sad path as thoroughly as the happy path.** Most exploits come from unexpected inputs and states.
- **Use `bound()` over `vm.assume()`** — assume discards inputs and wastes fuzzer runs.
- **When forking mainnet**, pin to a specific block number for reproducibility.
- **Use `makeAddr()`** for all test addresses — never use raw `address(1)`, `address(2)`.
- **Use `console2.log()`** for debugging, remove before finalizing.
- **Prefer `assertEq` over `assertTrue`** for better error messages on failure.
