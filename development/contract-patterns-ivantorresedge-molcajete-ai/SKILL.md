---
name: contract-patterns
description: Common Solidity design patterns and implementations for secure smart contract development. Use when implementing standard functionality like access control, upgradeability, or token standards.
---

# Contract Patterns Skill

This skill provides battle-tested patterns and examples for common smart contract functionality.

## When to Use

Use this skill when:
- Implementing access control mechanisms
- Creating upgradeable contracts
- Building token contracts (ERC20, ERC721, ERC1155)
- Adding pausability to contracts
- Protecting against reentrancy attacks
- Following established security patterns

## Pattern Categories

### 1. Access Control Patterns

See `./patterns/access-control.md` for detailed documentation.

**Common patterns:**
- **Ownable** - Single owner with privileged access
- **AccessControl** - Role-based access control (RBAC)
- **Multisig** - Multiple signatures required for actions
- **Timelock** - Delayed execution for critical functions

**When to use:**
- Ownable: Simple contracts with single admin
- AccessControl: Complex permissions with multiple roles
- Multisig: High-value contracts requiring consensus
- Timelock: Governance and critical upgrades

### 2. Upgradeable Contract Patterns

See `./patterns/upgradeable-contracts.md` for detailed documentation.

**Common patterns:**
- **Transparent Proxy** - Separate admin and user logic
- **UUPS (Universal Upgradeable Proxy Standard)** - Upgrade logic in implementation
- **Beacon Proxy** - Multiple proxies sharing same implementation
- **Diamond Pattern (EIP-2535)** - Multi-facet proxy for large contracts

**When to use:**
- Transparent: When admin and user separation is critical
- UUPS: Gas-efficient upgrades, upgrade logic in implementation
- Beacon: Deploying many instances of same logic
- Diamond: Large contracts exceeding size limits

### 3. Pausable Pattern

See `./patterns/pausable.md` for detailed documentation.

**Purpose:** Emergency stop mechanism to pause contract functionality

**When to use:**
- Contracts handling user funds
- Contracts that may need emergency stops
- Contracts under active development/monitoring

**Key features:**
- Pause/unpause functionality
- Restricted to authorized roles
- Graceful degradation of functionality

### 4. Reentrancy Guard

See `./patterns/reentrancy-guard.md` for detailed documentation.

**Purpose:** Prevent reentrancy attacks in functions that make external calls

**When to use:**
- Functions that transfer ETH
- Functions that call external contracts
- Functions that modify state after external calls

**Implementation:**
- Checks-Effects-Interactions pattern
- ReentrancyGuard modifier
- Mutex locks

### 5. Token Standards

See `./patterns/token-standards.md` for detailed documentation.

**ERC20** - Fungible tokens
- Standard interface for tokens like USDC, DAI
- Transfer, approve, transferFrom functionality
- See `./examples/ERC20-example.sol`

**ERC721** - Non-fungible tokens (NFTs)
- Unique tokens with individual ownership
- Metadata support
- See `./examples/ERC721-example.sol`

**ERC1155** - Multi-token standard
- Batch operations for fungible and non-fungible tokens
- Gas-efficient for multiple token types
- See `./examples/ERC1155-example.sol`

## Integration with Code Principles

These patterns follow the code-principles from the foundation plugin:

- **DRY**: Inherit from OpenZeppelin contracts instead of reimplementing
- **SOLID**: Single responsibility for each pattern/module
- **KISS**: Use simplest pattern that meets requirements
- **Security First**: Battle-tested implementations over custom code

**Note:** Solidity-specific security concerns take precedence over general software principles.

## OpenZeppelin Contracts

Most patterns are best implemented using OpenZeppelin contracts:

```bash
# Install OpenZeppelin
forge install OpenZeppelin/openzeppelin-contracts
# or
npm install @openzeppelin/contracts
```

**Available contracts:**
- `@openzeppelin/contracts/access/Ownable.sol`
- `@openzeppelin/contracts/access/AccessControl.sol`
- `@openzeppelin/contracts/security/Pausable.sol`
- `@openzeppelin/contracts/security/ReentrancyGuard.sol`
- `@openzeppelin/contracts/token/ERC20/ERC20.sol`
- `@openzeppelin/contracts/token/ERC721/ERC721.sol`
- `@openzeppelin/contracts/token/ERC1155/ERC1155.sol`
- `@openzeppelin/contracts/proxy/transparent/TransparentUpgradeableProxy.sol`
- `@openzeppelin/contracts/proxy/ERC1967/ERC1967Proxy.sol`

## Pattern Selection Guide

| Need | Pattern | Complexity | Gas Cost | Security |
|------|---------|------------|----------|----------|
| Single admin | Ownable | Low | Low | Medium |
| Multiple roles | AccessControl | Medium | Medium | High |
| Emergency stop | Pausable | Low | Low | High |
| Prevent reentrancy | ReentrancyGuard | Low | Low | Critical |
| Fungible tokens | ERC20 | Low | Low | High |
| NFTs | ERC721 | Medium | Medium | High |
| Multi-token | ERC1155 | High | Low | High |
| Simple upgrades | UUPS | Medium | Low | High |
| Admin separation | Transparent Proxy | Medium | Medium | High |
| Multiple instances | Beacon Proxy | High | Low | High |
| Large contracts | Diamond | Very High | Medium | Medium |

## Best Practices

1. **Prefer OpenZeppelin** - Use audited implementations over custom code
2. **Combine patterns carefully** - Test interactions between patterns
3. **Follow initialization patterns** - Use proper constructor/initializer for upgradeable contracts
4. **Test thoroughly** - Each pattern has unique security considerations
5. **Document deviations** - If customizing standard patterns, document why
6. **Keep it simple** - Use simplest pattern that meets requirements
7. **Security over gas optimization** - Prioritize security when patterns conflict

## Common Combinations

### Pausable + AccessControl
```solidity
contract MyContract is Pausable, AccessControl {
    bytes32 public constant PAUSER_ROLE = keccak256("PAUSER_ROLE");

    function pause() public onlyRole(PAUSER_ROLE) {
        _pause();
    }

    function unpause() public onlyRole(PAUSER_ROLE) {
        _unpause();
    }

    function criticalFunction() public whenNotPaused {
        // Function logic
    }
}
```

### ERC20 + Ownable + Pausable
```solidity
contract MyToken is ERC20, Ownable, Pausable {
    constructor() ERC20("MyToken", "MTK") Ownable(msg.sender) {}

    function pause() public onlyOwner {
        _pause();
    }

    function _update(address from, address to, uint256 value)
        internal
        override
        whenNotPaused
    {
        super._update(from, to, value);
    }
}
```

### UUPS + AccessControl + ReentrancyGuard
```solidity
contract MyUpgradeableContract is
    UUPSUpgradeable,
    AccessControlUpgradeable,
    ReentrancyGuardUpgradeable
{
    bytes32 public constant UPGRADER_ROLE = keccak256("UPGRADER_ROLE");

    function _authorizeUpgrade(address newImplementation)
        internal
        override
        onlyRole(UPGRADER_ROLE)
    {}
}
```

## Anti-Patterns to Avoid

1. **Custom access control** - Use OpenZeppelin instead
2. **Manual reentrancy protection** - Use ReentrancyGuard
3. **Incorrect upgrade patterns** - Follow OpenZeppelin upgrade guides
4. **Mixing storage layouts** - Be careful with inheritance order
5. **Skipping initialization** - Always initialize upgradeable contracts
6. **Ignoring token standards** - Follow ERC specifications exactly

## Pattern Files

This skill provides the following pattern documentation:
- `./patterns/upgradeable-contracts.md` - Proxy patterns
- `./patterns/access-control.md` - Permission patterns
- `./patterns/pausable.md` - Emergency stop pattern
- `./patterns/reentrancy-guard.md` - Reentrancy protection
- `./patterns/token-standards.md` - ERC20/721/1155 standards

## Example Contracts

This skill provides the following examples:
- `./examples/ERC20-example.sol` - Fungible token implementation
- `./examples/ERC721-example.sol` - NFT implementation
- `./examples/ERC1155-example.sol` - Multi-token implementation
- `./examples/upgradeable-example.sol` - UUPS upgradeable contract

## Quick Reference

```solidity
// Access Control
import "@openzeppelin/contracts/access/Ownable.sol";
import "@openzeppelin/contracts/access/AccessControl.sol";

// Security
import "@openzeppelin/contracts/security/Pausable.sol";
import "@openzeppelin/contracts/security/ReentrancyGuard.sol";

// Tokens
import "@openzeppelin/contracts/token/ERC20/ERC20.sol";
import "@openzeppelin/contracts/token/ERC721/ERC721.sol";
import "@openzeppelin/contracts/token/ERC1155/ERC1155.sol";

// Upgradeability
import "@openzeppelin/contracts/proxy/utils/UUPSUpgradeable.sol";
import "@openzeppelin/contracts/proxy/transparent/TransparentUpgradeableProxy.sol";
```

---

**Remember:** Always prefer battle-tested OpenZeppelin implementations over custom patterns. Security > Gas optimization > Code elegance.
