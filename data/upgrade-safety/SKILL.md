---
name: upgrade-safety
description: Safe upgrade practices for upgradeable smart contracts. Use when planning or executing contract upgrades.
---

# Upgrade Safety Skill

Reference skill for safe upgrade practices. Detailed upgrade security checklist is in the `security-audit` skill.

## When to Use

Use this skill when:
- Planning contract upgrades
- Executing upgrades
- Reviewing upgrade implementations
- Testing upgrade scenarios

## Related Skills

For comprehensive upgrade security, see:
- **security-audit**: `checklists/upgrade-checklist.md` - Complete upgrade security checklist
- **proxy-patterns**: Proxy pattern selection and implementation
- **contract-patterns**: `patterns/upgradeable-contracts.md` and `examples/upgradeable-example.sol`

## Upgrade Safety Rules

### Storage Layout Safety

**Never:**
- Delete state variables
- Change variable types
- Change variable order
- Reorder inherited contracts

**Always:**
- Add new variables at the end
- Use storage gaps
- Document storage layout
- Test storage compatibility

**Example:**
```solidity
// V1
contract V1 {
    uint256 public value;
    address public owner;
    uint256[48] private __gap;  // Reserve space
}

// V2 - ✅ Safe
contract V2 {
    uint256 public value;
    address public owner;
    uint256 public newValue;    // Added at end
    uint256[47] private __gap;  // Reduced gap
}
```

### Initializer Safety

**Always:**
- Use `_disableInitializers()` in constructor
- Use `initializer` modifier for init function
- Use `reinitializer(version)` for upgrade init
- Call parent initializers

**Example:**
```solidity
contract MyContract is Initializable, UUPSUpgradeable {
    constructor() {
        _disableInitializers();  // ✅ Required
    }

    function initialize() public initializer {
        __UUPSUpgradeable_init();
    }

    function initializeV2() public reinitializer(2) {
        // V2 initialization
    }
}
```

### Authorization Safety

**UUPS:**
- Always keep `_authorizeUpgrade` function
- Use appropriate access control
- Consider timelock for critical upgrades

```solidity
function _authorizeUpgrade(address) internal override onlyOwner {}
```

**Never remove this function in UUPS upgrades!**

## Upgrade Process

### Pre-Upgrade Checklist

- [ ] Storage layout verified compatible
- [ ] New implementation tested
- [ ] Initializers properly protected
- [ ] Authorization functions present
- [ ] Tests passing
- [ ] Storage verification tool run
- [ ] Deployment addresses verified
- [ ] Backup plan prepared

### Verification Tools

**Foundry:**
```bash
# Check storage layout
forge inspect MyContract storage-layout

# Compare layouts
forge inspect MyContractV1 storage-layout > v1.json
forge inspect MyContractV2 storage-layout > v2.json
diff v1.json v2.json
```

**Hardhat:**
```bash
# Validate upgrade
npx hardhat verify-upgrade <PROXY> <NEW_IMPL>
```

**Slither:**
```bash
# Check upgradeability
slither-check-upgradeability . MyContract
```

### During Upgrade

1. **Pause if applicable**
2. **Deploy new implementation**
3. **Verify implementation**
4. **Execute upgrade**
5. **Verify proxy points to new implementation**
6. **Test critical functions**
7. **Unpause if paused**

### Post-Upgrade

- [ ] Verify implementation address
- [ ] Test all critical functions
- [ ] Monitor for issues
- [ ] Document changes
- [ ] Update documentation

## Testing Upgrades

### Storage Preservation Test

```solidity
function test_UpgradePreservesStorage() public {
    // Deploy V1
    MyContractV1 v1 = new MyContractV1();
    v1.initialize(owner);
    v1.setValue(42);

    // Deploy V2 implementation
    MyContractV2 implementation = new MyContractV2();

    // Simulate upgrade (actual upgrade depends on proxy pattern)
    // ...

    // Cast to V2 interface
    MyContractV2 v2 = MyContractV2(address(v1));

    // Verify storage preserved
    assertEq(v2.getValue(), 42);
    assertEq(v2.owner(), owner);
}
```

### Fork Testing

```solidity
function test_UpgradeOnFork() public {
    // Fork mainnet
    vm.createSelectFork(vm.envString("MAINNET_RPC_URL"));

    // Get existing proxy
    MyContract proxy = MyContract(PROXY_ADDRESS);

    // Deploy new implementation
    MyContract newImpl = new MyContract();

    // Upgrade
    vm.prank(OWNER);
    proxy.upgradeTo(address(newImpl));

    // Verify
    assertEq(proxy.version(), 2);
}
```

## Common Upgrade Mistakes

### ❌ 1. Storage Collision

```solidity
// V1
contract V1 {
    uint256 public value;
}

// V2 - ❌ Wrong!
contract V2 {
    address public owner;   // Overwrites value!
    uint256 public value;
}
```

### ❌ 2. Uninitialized Implementation

```solidity
// ❌ Missing constructor protection
contract MyContract {
    function initialize() public initializer {
        // Attacker can initialize implementation!
    }
}
```

### ❌ 3. Removed Authorization

```solidity
// V1
contract V1 is UUPSUpgradeable {
    function _authorizeUpgrade(address) internal override onlyOwner {}
}

// V2 - ❌ Removed authorization!
contract V2 is UUPSUpgradeable {
    // Missing _authorizeUpgrade - contract is now non-upgradeable!
}
```

### ❌ 4. Selfdestruct in Implementation

```solidity
// ❌ Never use selfdestruct in upgradeable contracts
function destroy() public {
    selfdestruct(payable(owner));  // Kills implementation for all proxies!
}
```

## Security Considerations

1. **Multi-sig for upgrades** - Never use single key in production
2. **Timelock delays** - Give users time to exit before upgrade
3. **Pause before upgrade** - Prevent state changes during upgrade
4. **Test on testnet** - Always test upgrades before mainnet
5. **Emergency procedures** - Have rollback plan ready

## Best Practices

1. **Always use OpenZeppelin upgradeable contracts**
2. **Test upgrades on fork before mainnet**
3. **Use storage gaps (50 slots) in base contracts**
4. **Document storage layout changes**
5. **Never remove _authorizeUpgrade in UUPS**
6. **Use reinitializer for upgrade initialization**
7. **Verify storage compatibility with tools**
8. **Multi-sig + timelock for production**
9. **Monitor after upgrade**
10. **Have rollback plan**

## Tools

| Tool | Purpose | Command |
|------|---------|---------|
| Foundry | Storage layout | `forge inspect Contract storage-layout` |
| Hardhat | Verify upgrade | `npx hardhat verify-upgrade` |
| Slither | Check upgrade safety | `slither-check-upgradeability` |
| OpenZeppelin Defender | Upgrade automation | Web interface |

## Related Documentation

- **Detailed checklist:** `security-audit/checklists/upgrade-checklist.md`
- **Proxy patterns:** `proxy-patterns/SKILL.md`
- **Implementation examples:** `contract-patterns/patterns/upgradeable-contracts.md`
- **Example contract:** `contract-patterns/examples/upgradeable-example.sol`

---

**Note:** This is a reference skill. For the complete upgrade security checklist, see `security-audit/checklists/upgrade-checklist.md`.
