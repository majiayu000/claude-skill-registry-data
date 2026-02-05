---
name: proxy-patterns
description: Proxy patterns for upgradeable smart contracts. Use when implementing or reviewing upgradeable contracts.
---

# Proxy Patterns Skill

Reference skill for proxy patterns in Solidity. Detailed proxy implementations are covered in the `contract-patterns` skill.

## When to Use

Use this skill when:
- Implementing upgradeable contracts
- Choosing proxy pattern
- Understanding proxy mechanics
- Reviewing upgrade implementations

## Related Skills

For detailed proxy implementations, see:
- **contract-patterns**: `patterns/upgradeable-contracts.md`
- **upgrade-safety**: Safe upgrade practices
- **security-audit**: `checklists/upgrade-checklist.md`

## Proxy Pattern Overview

### Pattern Comparison

| Pattern | Upgrade Location | Best For | Complexity |
|---------|-----------------|----------|------------|
| UUPS | Implementation | Most cases | Medium |
| Transparent | Proxy | Admin separation | Low |
| Beacon | Beacon contract | Multiple instances | High |
| Diamond | Facet contracts | Large contracts | Very High |

## UUPS (Universal Upgradeable Proxy Standard)

**Recommended for most use cases**

```solidity
import "@openzeppelin/contracts-upgradeable/proxy/utils/UUPSUpgradeable.sol";

contract MyContract is UUPSUpgradeable, OwnableUpgradeable {
    constructor() {
        _disableInitializers();
    }

    function initialize() public initializer {
        __Ownable_init(msg.sender);
        __UUPSUpgradeable_init();
    }

    function _authorizeUpgrade(address) internal override onlyOwner {}
}
```

**Pros:**
- Gas efficient
- Flexible upgrade authorization
- Smaller proxy contract

**Cons:**
- Can brick if _authorizeUpgrade removed
- More complex implementation

**Detailed documentation:** See `contract-patterns/patterns/upgradeable-contracts.md`

## Transparent Proxy

**Use when admin/user separation is critical**

```solidity
import "@openzeppelin/contracts/proxy/transparent/TransparentUpgradeableProxy.sol";

// Deploy
TransparentUpgradeableProxy proxy = new TransparentUpgradeableProxy(
    implementationAddress,
    adminAddress,
    initData
);
```

**Pros:**
- Clear admin/user separation
- Admin cannot call implementation functions
- Battle-tested pattern

**Cons:**
- Higher gas costs
- Larger proxy contract

**Detailed documentation:** See `contract-patterns/patterns/upgradeable-contracts.md`

## Beacon Proxy

**Use for multiple instances sharing implementation**

```solidity
import "@openzeppelin/contracts/proxy/beacon/UpgradeableBeacon.sol";
import "@openzeppelin/contracts/proxy/beacon/BeaconProxy.sol";

// Deploy beacon
UpgradeableBeacon beacon = new UpgradeableBeacon(implementationAddress);

// Deploy proxies
BeaconProxy proxy1 = new BeaconProxy(address(beacon), initData);
BeaconProxy proxy2 = new BeaconProxy(address(beacon), initData);

// Upgrade all
beacon.upgradeTo(newImplementation);
```

**Pros:**
- Upgrade multiple contracts at once
- Gas efficient for many instances
- Centralized control

**Cons:**
- All instances upgrade together
- Additional beacon contract

**Detailed documentation:** See `contract-patterns/patterns/upgradeable-contracts.md`

## Diamond Pattern (EIP-2535)

**Use for contracts exceeding size limits**

Complex pattern with multiple facets. See [EIP-2535](https://eips.ethereum.org/EIPS/eip-2535) for specification.

## Storage Layout Rules

**Critical for all proxy patterns:**

```solidity
// V1
contract V1 {
    uint256 public value;
    address public owner;
}

// V2 - ✅ Safe upgrade
contract V2 {
    uint256 public value;      // Same position
    address public owner;      // Same position
    uint256 public newValue;   // Added at end
}

// V2 - ❌ Unsafe upgrade
contract V2Bad {
    address public owner;      // ❌ Changed position
    uint256 public value;      // ❌ Changed position
}
```

**Rules:**
1. Never delete state variables
2. Never change types
3. Never change order
4. Only add at the end
5. Use storage gaps in base contracts

## Quick Pattern Selection

**Choose UUPS if:**
- You want gas efficiency
- You need flexible upgrade control
- You're comfortable with the pattern

**Choose Transparent if:**
- You need strict admin/user separation
- Gas cost is less critical
- You want simplicity

**Choose Beacon if:**
- Deploying many similar contracts
- Need to upgrade all together
- Want centralized upgrade control

**Choose Diamond if:**
- Contract exceeds 24KB limit
- Need modular functionality
- Comfortable with complexity

## Related Documentation

- **Implementation examples:** `contract-patterns/patterns/upgradeable-contracts.md`
- **Security checklist:** `security-audit/checklists/upgrade-checklist.md`
- **Upgrade safety:** `upgrade-safety/SKILL.md`
- **Example contract:** `contract-patterns/examples/upgradeable-example.sol`

---

**Note:** This is a reference skill. For detailed implementations and examples, see the `contract-patterns` skill.
