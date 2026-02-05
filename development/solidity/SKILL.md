---
name: solidity
description: Solidity smart contract development with Foundry. Covers writing, testing, security, deployment, and upgrades. Triggers on .sol files, contract, pragma solidity, forge.
triggers: ["\\.sol", "\\bcontract\\b", "solidity", "pragma solidity", "forge", "foundry", "hardhat"]
---

<objective>
Build secure, gas-efficient Solidity smart contracts using Foundry. This skill covers writing contracts, testing with Forge, security patterns, deployment, and upgrades.
</objective>

<mcp_first>
**CRITICAL: Use OctoCode to search OpenZeppelin and Foundry patterns.**

```
MCPSearch({ query: "select:mcp__plugin_devtools_octocode__githubSearchCode" })
MCPSearch({ query: "select:mcp__plugin_devtools_context7__query-docs" })
```

```typescript
// OpenZeppelin contracts
mcp__octocode__githubSearchCode({
  keywordsToSearch: ["Ownable", "AccessControl", "Pausable"],
  owner: "OpenZeppelin",
  repo: "openzeppelin-contracts",
  path: "contracts/access",
  mainResearchGoal: "Find OpenZeppelin access control patterns",
  researchGoal: "Get current Ownable and AccessControl implementations",
  reasoning: "Need verified security patterns"
})

// Foundry testing
mcp__context7__query_docs({
  context7CompatibleLibraryID: "/foundry-rs/book",
  topic: "forge test fuzz invariant"
})
```
</mcp_first>

<quick_start>
**Contract structure:**

```solidity
// SPDX-License-Identifier: MIT
pragma solidity 0.8.28;

import { Ownable } from "@openzeppelin/contracts/access/Ownable.sol";

/// @title MyContract
/// @notice Brief description
contract MyContract is Ownable {
    // Events
    event ActionPerformed(address indexed actor, uint256 amount);

    // Errors
    error InsufficientBalance(uint256 required, uint256 available);

    // State variables
    uint256 private _totalAmount;

    // Constructor
    constructor() Ownable(msg.sender) {}

    /// @notice Performs an action
    /// @param amount The amount to process
    function performAction(uint256 amount) external {
        // Checks
        if (amount > _totalAmount) {
            revert InsufficientBalance(amount, _totalAmount);
        }

        // Effects
        _totalAmount -= amount;

        // Interactions
        emit ActionPerformed(msg.sender, amount);
    }
}
```
</quick_start>

<cei_pattern>
**CEI Pattern (Required):**

Always order operations as:
1. **Checks** - Validate inputs and state
2. **Effects** - Update contract state
3. **Interactions** - External calls and events

```solidity
function transfer(address to, uint256 amount) external {
    // 1. Checks
    require(balances[msg.sender] >= amount, "Insufficient");

    // 2. Effects
    balances[msg.sender] -= amount;
    balances[to] += amount;

    // 3. Interactions
    emit Transfer(msg.sender, to, amount);
}
```
</cei_pattern>

<constraints>
**Banned:** `assembly {}`, `tx.origin`, `block.timestamp` for randomness, `selfdestruct`, magic numbers, functions >50 lines, >7 parameters

**Required:**
- NatSpec on all `external` functions
- Events for all state changes
- CEI pattern for external calls
- 50-slot storage gap in upgradeables
- `_disableInitializers()` in implementation constructors
- `super.hookName()` FIRST in hook overrides

**Naming:** Contracts=`PascalCase`, functions=`camelCase`, constants=`SCREAMING_SNAKE`, events=`PastTense`, errors=`NounPhrase`, private=`_underscore`
</constraints>

<commands>
```bash
forge build          # Compile contracts
forge test           # Run tests
forge test -vvv      # Verbose test output
forge coverage       # Test coverage
forge fmt            # Format code
```
</commands>

<security_checklist>
- [ ] No reentrancy vulnerabilities (CEI pattern)
- [ ] Access control on sensitive functions
- [ ] Integer overflow/underflow handled (Solidity 0.8+)
- [ ] No unchecked external calls
- [ ] Events emitted for state changes
- [ ] Storage gaps for upgradeable contracts
</security_checklist>

<success_criteria>
- [ ] OctoCode searched for OpenZeppelin patterns
- [ ] NatSpec on external functions
- [ ] CEI pattern followed
- [ ] Events for state changes
- [ ] Tests pass with good coverage
</success_criteria>
