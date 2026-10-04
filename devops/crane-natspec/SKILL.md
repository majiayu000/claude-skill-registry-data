---
name: crane-natspec
description: "Crane NatSpec and AsciiDoc documentation; compute and verify selectors, event topics and interface IDs."
license: MIT
---

# Crane NatSpec & Documentation Standards

Crane uses NatSpec combined with AsciiDoc include-tags for accurate, extractable documentation.

**Critical Alignment Requirements (LR-3):**
- Skills reflect finalized standards per PRD: NatSpec verification **exclusively** uses the dedicated Foundry Script (`scripts/foundry/ComputeNatSpecValues.s.sol`) + central values file (NEVER ad-hoc `cast` or manual for authoritative @custom values).
- Use `CENTRALLY_COMPUTED_NATSPEC_VALUES.md` **exclusively** (ONLY those values) for all `@custom:selector`, `@custom:topiczero`, `@custom:interfaceid` in examples/docs.
- Full scope (LR-1): applies to **all Solidity code** including production + **every test file** (`.t.sol`, `TestBase_*.sol`, `Behavior_*.sol`, handlers, stubs, comparators, etc.).
- ERC1967: when documenting storage Repos, use/show the compliant `DEFAULT_SLOT = bytes32(uint256(keccak256(abi.encode("hier.name"))) - 1)` form (LR-6); cross-ref `crane-architecture`.
- Ties to GitBook/LR-2: accurate centrally-verified NatSpec enables required content on Create3FactoryDFPkg chain setup, reusable `DiamondPackageCallBackFactory` (interfaceId 0x949da331 from central), registries, ported protocol TestBases+Behaviors+utilities, and general utilities (Sets etc.).
- Test NatSpec (LR-7): public surfaces on test infrastructure must carry exact // tag:: + @custom using central values + Behavior declaration tests validate the documented surfaces.
- References: `docs/development/natspec.md`, PRD LR-1/LR-3/LR-7, AGENTS.md (NatSpec section), `crane-testing`/`crane-deployment` skills. Update this skill on standard evolution.

## AsciiDoc Include-Tags

Wrap documented symbols with include-tags for documentation extraction:

```solidity
// tag::MySymbol[]
/// @notice Description of the symbol
function myFunction() external { ... }
// end::MySymbol[]
```

### Tag Format Rules

- Tag markers must match exactly (no extra spaces inside `[]`)
- Tag name should match the symbol being documented
- Use PascalCase for tag names matching type names
- Use camelCase for function tag names

### Example Usage

```solidity
// tag::transfer[]
/// @notice Transfers tokens to a recipient
/// @param to_ The recipient address
/// @param amount_ The amount to transfer
/// @return success True if transfer succeeded
/// @custom:signature transfer(address,uint256)
/// @custom:selector 0xa9059cbb
function transfer(address to_, uint256 amount_) external returns (bool success);
// end::transfer[]
```

## Custom NatSpec Tags

### Functions

| Tag | Purpose | Example |
|-----|---------|---------|
| `@custom:signature` | Canonical signature string | `transfer(address,uint256)` |
| `@custom:selector` | bytes4 selector | `0xa9059cbb` |

```solidity
/// @notice Transfers tokens
/// @custom:signature transfer(address,uint256)
/// @custom:selector 0xa9059cbb
function transfer(address to_, uint256 amount_) external returns (bool);
```

### Errors

| Tag | Purpose | Example |
|-----|---------|---------|
| `@custom:signature` | Canonical error signature | `NotOwner(address)` |
| `@custom:selector` | bytes4 selector | `0x30cd7471` |

```solidity
/// @notice Thrown when caller is not the owner
/// @custom:signature NotOwner(address)
/// @custom:selector 0x30cd7471
error NotOwner(address caller);
```

### Events

| Tag | Purpose | Example |
|-----|---------|---------|
| `@custom:signature` | Canonical event signature | `Transfer(address,address,uint256)` |
| `@custom:topiczero` | bytes32 topic0 hash | `0xddf252ad...` |

```solidity
/// @notice Emitted on token transfer
/// @custom:signature Transfer(address,address,uint256)
/// @custom:topiczero 0xddf252ad1be2c89b69c2b068fc378daa952ba7f163c4a11628f55a4df523b3ef
event Transfer(address indexed from, address indexed to, uint256 amount);
```

**Note**: Events use `@custom:topiczero` (bytes32), not `@custom:selector` (bytes4).

### ERC-165 Interfaces

| Tag | Purpose | Example |
|-----|---------|---------|
| `@custom:interfaceid` | bytes4 interface ID | `0x01ffc9a7` |

```solidity
/// @title IERC165
/// @custom:interfaceid 0x01ffc9a7
interface IERC165 {
    function supportsInterface(bytes4 interfaceId) external view returns (bool);
}
```

## Full Scope (incl. Tests) and Verification Script

Per LR-1:
- **Scope**: All Solidity code: interfaces, contracts, libraries (Repos, Targets, Services, Facets, DFPkgs, AwareRepos), **and all test files** (TestBase_*, Behavior_*, IHandler, handlers, stubs, comparators, *.t.sol etc.).
- Test code that exposes public APIs must receive the same NatSpec + exact // tag::[] + @custom:* (using ONLY central values) as production code (see LR-7 point 10).
- Declaration tests (Behavior_IFacet etc.) must validate the documented values (e.g. `facetInterfaces()` returns selectors matching the @custom ones tagged in the interface/impl).

The verification script (`scripts/foundry/ComputeNatSpecValues.s.sol`) is the committed tool for this (see run instructions above). It itself uses // tag::ComputeNatSpecValues[] etc. and documents the process.

## NatSpec on Test Code (LR-1 + LR-7)

Example for a Behavior or TestBase public surface (use central IFacet values):

```solidity
// tag::Behavior_IFacet[]
/// @title Behavior_IFacet
/// @notice Validation helpers for IFacet (see central for selectors e.g. facetInterfaces 0x2ea80826)
library Behavior_IFacet {
    // tag::areValid_IFacet_facetInterfaces[]
    /// @notice ...
    /// @custom:signature areValid_IFacet_facetInterfaces(IFacet,bytes4[],bytes4[])
    /// @custom:selector 0x... (use central or script)
    function areValid_IFacet_facetInterfaces(...) public view returns (bool) { ... }
    // end::areValid_IFacet_facetInterfaces[]
}
// end::Behavior_IFacet[]
```

## Verification Script and Central Values Process (Mandatory per LR-1)

**Primary method**: Use the dedicated **Foundry Script** (committed in repo) for all authoritative values. Run:

```bash
forge script scripts/foundry/ComputeNatSpecValues.s.sol --sig "run()" -vvv
```

- This script uses compiler (`type(IInterface).interfaceId` for IDs; Solidity `keccak256` for selectors/topic0) -- reproducible, CI-auditable.
- Output the exact bytes; copy to `CENTRALLY_COMPUTED_NATSPEC_VALUES.md` (single source of truth) and/or into `@custom:*` tags.
- Helper `scripts/compute_natspec_values.sh` exists for quick exploration (uses cast internally) but **always verify final values via the Foundry Script**.
- Re-run after any interface/symbol addition or change.

**Central Values Rule (use ONLY)**:
- Always pull `@custom:selector` / `@custom:topiczero` / `@custom:interfaceid` **exclusively** from `docs/reports/gap/CENTRALLY_COMPUTED_NATSPEC_VALUES.md`.
- Current central pass date: 2026-07-02 (example values below; always consult the file).
- Subagents must follow strict read order before work: gap report + CENTRALLY... + PRD (LR sections) + AGENTS.md + source files.

Examples of central values (use ONLY from the file, do not recompute):

- IFacet interface surface (selectors):
  - `facetName()` : 0x5b6f4d01
  - `facetInterfaces()` : 0x2ea80826
  - `facetFuncs()` : 0x574a4cff
  - `facetMetadata()` : 0xf10d7a75
  - `supportsInterface(bytes4)` : 0x01ffc9a7

- IDiamondPackageCallBackFactory (interfaceId 0x949da331 from central):
  - `deploy(address,bytes)` : 0xe97fac05
  - `initAccount(address,bytes)` : 0x8e85783e
  - ...

- IOperable (interfaceId 0xa7f11160):
  - `isOperator(address)` : 0x6d70f7ae
  - `NotOperator(address)` selector: 0x76c6c93a
  - `NewGlobalOperatorStatus(address,bool)` topic0: 0x26ba28058a3c072a70c8fd315037fe9b3957237cef5c61a9652a8da41c673daa
  - ...

See `docs/development/natspec.md` "Verification Script Requirement" and "Central Values Process" + the script itself (which carries NatSpec + tags using the process).

## Computing Values (for exploration only)

`cast` (or manual) may be used for quick local checks, but final authoritative values for code/docs **must** come from the Foundry Script + CENTRALLY_COMPUTED... (cast matches keccak for selectors/topics but the script is the required verifier).

### Function Selector (bytes4)

```bash
cast sig "transfer(address,uint256)"
# Output: 0xa9059cbb
```

### Error Selector (bytes4)

```bash
cast sig "NotOwner(address)"
# Output: 0x30cd7471
```

### Event Topic0 (bytes32)

```bash
cast keccak "Transfer(address,address,uint256)"
# Output: 0xddf252ad1be2c89b69c2b068fc378daa952ba7f163c4a11628f55a4df523b3ef
```

### Interface ID (bytes4)

For interface IDs, prefer the script or:

```solidity
bytes4 interfaceId = type(IMyInterface).interfaceId;
```

Or compute manually by XOR-ing all function selectors (cross-check with script output).

## Complete Documentation Example

Use exact values from `CENTRALLY_COMPUTED_NATSPEC_VALUES.md` (ONLY). Gold standard tag formats use hyphenated params for overload disambiguation (see AGENTS.md + ERC8023 examples).

```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.30;

// tag::IOperable[]
/// @title IOperable
/// @notice Interface for operator-based access control
/// @custom:interfaceid 0xa7f11160
interface IOperable {

    // tag::NewGlobalOperatorStatus(address-bool)[]
    /// @notice Emitted when global operator status changes
    /// @param operator The operator address
    /// @param status The new status
    /// @custom:signature NewGlobalOperatorStatus(address,bool)
    /// @custom:topiczero 0x26ba28058a3c072a70c8fd315037fe9b3957237cef5c61a9652a8da41c673daa
    event NewGlobalOperatorStatus(address indexed operator, bool indexed status);
    // end::NewGlobalOperatorStatus(address-bool)[]

    // tag::NotOperator(address)[]
    /// @notice Thrown when caller is not an operator
    /// @param caller The unauthorized caller
    /// @custom:signature NotOperator(address)
    /// @custom:selector 0x76c6c93a
    error NotOperator(address caller);
    // end::NotOperator(address)[]

    // tag::isOperator(address)[]
    /// @notice Checks if an address is a global operator
    /// @param query_ The address to check
    /// @return isOperator_ True if operator
    /// @custom:signature isOperator(address)
    /// @custom:selector 0x6d70f7ae
    function isOperator(address query_) external view returns (bool isOperator_);
    // end::isOperator(address)[]

    // tag::setOperator(address-bool)[]
    /// @notice Sets operator status
    /// @param operator_ The address
    /// @param status_ The status
    /// @custom:signature setOperator(address,bool)
    /// @custom:selector 0x558a7297
    function setOperator(address operator_, bool status_) external;
    // end::setOperator(address-bool)[]
}
// end::IOperable[]
```

For IFacet (central values: facetName 0x5b6f4d01, facetInterfaces 0x2ea80826 etc):

```solidity
// tag::IFacet[]
/// @title IFacet
/// @custom:interfaceid (computed via XOR in script; see central)
interface IFacet {
    // tag::facetInterfaces()[]
    /// @notice ...
    /// @custom:signature facetInterfaces()
    /// @custom:selector 0x2ea80826
    function facetInterfaces() external view returns (bytes4[] memory);
    // end::facetInterfaces()[]
}
// end::IFacet[]
```

## Validation Checklist

For each documented symbol, verify:

- [ ] Include-tags wrap the symbol correctly (exact `// tag::Name(params)[]` ... `// end::Name(params)[]`, hyphenated params for overloads/events)
- [ ] Tag names match symbol names
- [ ] `@custom:signature` matches actual signature exactly
- [ ] `@custom:selector` / `@custom:topiczero` / `@custom:interfaceid` taken **ONLY** from `CENTRALLY_COMPUTED_NATSPEC_VALUES.md` (or freshly generated by running the Foundry Script `forge script scripts/foundry/ComputeNatSpecValues.s.sol --sig "run()" -vvv`)
- [ ] Rich NatSpec present (`@notice`, `@param`, `@return`, `@custom:emits`, `@custom:throws` as applicable)
- [ ] Repos document **both** parameterized (`_layoutStruct(bytes32)`) and default overloads with distinct tags
- [ ] Facets implement/document full `IFacet` using central values (e.g. 0x2ea80826)
- [ ] Test surfaces (Behavior, TestBase, handlers) also tagged when public

## ERC1967 in NatSpec Context (LR-6 tie-in for LR-3)

When documenting storage libraries, the NatSpec + tags must reflect the canonical ERC1967-derived slot:

```solidity
// tag::DEFAULT_SLOT[]
bytes32 internal constant DEFAULT_SLOT = bytes32(uint256(keccak256(abi.encode("crane.example.slot"))) - 1);
// end::DEFAULT_SLOT[]
```

See `crane-architecture` skill and LR-6. Old direct-keccak forms without `- 1` are non-compliant.

## Additional Resources

### Reference Files

- **`references/natspec-examples.md`** - More complete examples
- `docs/development/natspec.md` (full LR-1 details, verification script, central process, gold standard ERC8023 files)
- `scripts/foundry/ComputeNatSpecValues.s.sol` (the dedicated LR-1 Foundry Script)
- `docs/reports/gap/CENTRALLY_COMPUTED_NATSPEC_VALUES.md` (use ONLY these values)

### Quick Reference

| Symbol Type | Selector Tag | Hash Type |
|-------------|--------------|-----------|
| Function | `@custom:selector` | bytes4 |
| Error | `@custom:selector` | bytes4 |
| Event | `@custom:topiczero` | bytes32 |
| Interface | `@custom:interfaceid` | bytes4 (XOR of selectors) |

### LR Ties (for Agents)

- LR-1 primary: this process + Foundry Script + full scope (tests included) + central.
- LR-2: verified NatSpec supports GitBook extraction for chain setup (Create3FactoryDFPkg), DiamondPackageCallBackFactory reuse (0x949da331), registries, protocol utilities + TestBases, Sets/math.
- LR-3: keep this skill + others in sync; global + repo `.claude/skills/`.
- LR-4: documented, centrally-verified, reusable facets/packages enable "deploy once, attach everywhere" (security via verified reuse for agents; cost via no re-deploy).
- LR-7: declaration tests + NatSpec on test code use these values + Behaviors.

Update this skill (and its gap report) whenever standards evolve (LR-3). Always follow the strict read order for any NatSpec work.
