---
name: smart-contract
description: |
  Multi-chain smart contract development skill for Ethereum, Solana, and Move-based chains.
  This skill should be used when: writing smart contracts (ERC20/ERC721/ERC1155/esToken/custom),
  auditing contract security vulnerabilities, generating Foundry test cases, optimizing gas usage,
  or automating deployment workflows. Triggers on queries like "write a contract", "audit this contract",
  "generate tests", "optimize gas", or "deploy contract".
---

# Smart Contract Development Skill

Multi-chain smart contract development with security-first approach.

## Capabilities

| Capability | Description |
|------------|-------------|
| Contract Writing | ERC20, ERC721, ERC1155, esToken (vesting/locking), custom logic |
| Security Audit | Reentrancy, overflow, access control, flash loan attacks, etc. |
| Test Generation | Foundry test cases with fuzz testing and invariant tests |
| Gas Optimization | Storage packing, calldata optimization, assembly tricks |
| Deployment | Multi-chain deployment scripts with verification |

## Supported Chains

- **EVM**: Ethereum, Polygon, Arbitrum, Optimism, BSC, Avalanche
- **Solana**: Anchor framework
- **Move**: Aptos, Sui

## Workflow

### Contract Development

1. Clarify requirements (token type, features, chain)
2. Load appropriate template from `assets/templates/`
3. Implement with OpenZeppelin base contracts where applicable
4. Apply gas optimizations from `references/gas-optimization.md`
5. Generate Foundry tests using patterns from `references/foundry-patterns.md`

### Security Audit

1. Run `scripts/security_scan.py` for automated detection
2. Manual review using `references/vulnerabilities.md` checklist
3. Report findings with severity levels (Critical/High/Medium/Low/Info)
4. Suggest fixes with code examples

### Test Generation

1. Identify contract functions and state transitions
2. Apply patterns from `references/foundry-patterns.md`
3. Include fuzz tests for numeric inputs
4. Include invariant tests for protocol properties

## Resources

### References (load as needed)

| File | Purpose | When to load |
|------|---------|--------------|
| `references/vulnerabilities.md` | Common vulnerability patterns | During security audits |
| `references/best-practices.md` | Solidity/Rust best practices | During contract writing |
| `references/gas-optimization.md` | Gas optimization techniques | When optimizing contracts |
| `references/foundry-patterns.md` | Test patterns and examples | When generating tests |

### Templates (copy and modify)

| Template | Use Case |
|----------|----------|
| `assets/templates/erc20-base.sol` | Fungible token contracts |
| `assets/templates/erc721-base.sol` | NFT contracts |
| `assets/templates/estoken-base.sol` | Vesting/locking token (esToken) |
| `assets/templates/test-base.t.sol` | Foundry test scaffold |

### Scripts

| Script | Purpose |
|--------|---------|
| `scripts/security_scan.py` | Automated vulnerability detection |

## Security Audit Checklist

When auditing, check each category from `references/vulnerabilities.md`:

1. **Reentrancy**: External calls before state updates
2. **Access Control**: Missing modifiers, centralization risks
3. **Integer Issues**: Overflow/underflow (pre-0.8.0), division by zero
4. **Flash Loan Attacks**: Price manipulation, governance attacks
5. **Front-running**: MEV vulnerabilities, commit-reveal patterns
6. **Logic Errors**: Off-by-one, incorrect comparisons
7. **Denial of Service**: Unbounded loops, block gas limit

## Output Format

> Claude responds in Chinese per CLAUDE.md.

### Audit Report Structure

```markdown
## Security Audit Report

### Summary
- Contracts audited: [list]
- Lines of code: [count]
- Findings: [X Critical, Y High, Z Medium, W Low]

### Findings

#### [C-01] Critical: [Title]
- **Location**: `Contract.sol:L42`
- **Impact**: [description]
- **Proof of Concept**: [code]
- **Recommendation**: [fix]
```

### Contract Delivery Structure

```markdown
## Contract: [Name]

### Features
- [list features]

### Deployment
1. [steps]

### Files
- `src/[Contract].sol` - Main contract
- `test/[Contract].t.sol` - Tests
- `script/Deploy[Contract].s.sol` - Deployment script
```

## Gas Optimization Priority

Apply optimizations in this order (from `references/gas-optimization.md`):

1. Storage layout (packing, cold/warm slots)
2. Calldata vs memory
3. Unchecked blocks for safe math
4. Custom errors vs require strings
5. Assembly for critical paths (last resort)
