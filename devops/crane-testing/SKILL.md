---
name: crane-testing
description: "Write Crane production-first tests with CraneTest, TestBases, Behavior libraries, handlers, fuzzing and invariants."
license: MIT
---

# Crane Testing Patterns

Crane uses structured testing patterns with TestBase contracts, Behavior libraries, and Handler contracts for comprehensive coverage. All patterns must comply with LR-7 (see PRD) and LR-1 (NatSpec on test code).

## Production-first testing (read this first)

**Prefer production code and production deploy paths. Do not invent mocks for the subject under test (SUT).**

Generic Foundry skills that show `MockOracle`, `vm.mockCall`, or `new MyContract()` are **subordinate** to this skill for Crane work.

### Ladder (use the highest step that fits)

1. **Real production contracts**, deployed via `CraneTest` factories (`create3Factory`, `diamondPackageFactory`) — same path as production. No `address(0)` facets in DFPkg init.
2. **Existing `TestBase_*` chains**. Search `contracts/**/TestBase_*.sol` before writing setup from scratch.
3. **External protocols**: **protocol ports** under `contracts/protocols/.../stubs/` (real/protocol-faithful code for hermetic deploy) **or** fork bases (`TestBase_*Fork` + live addresses). Do not invent interface mocks when a TestBase already deploys the protocol.
4. **Harness doubles outside the SUT** only when they implement real interfaces and add controllability (mintable ERC20, reentrancy token, Behavior targets like `ERC20TargetStub`).
5. **`vm.mockCall` / fake contracts** only for non-SUT isolation, failure modes production cannot express cheaply, or documented oracle/VRF harnesses — **SUT remains real**.

### Forbidden for SUT

- Mocking facets, DFPkgs, diamond proxies, Create3/diamond factories, or registries under test
- Replacing a protocol integration with a canned mock when `TestBase_*` + protocol ports or forks exist
- Deploying production Crane facets/DFPkgs with `new` (use factories; protocol *ports* in TestBases may use `new` for the ported protocol code only)

### Terminology (do not conflate)

| Term | Meaning |
|------|---------|
| **Protocol port (`*/stubs/`)** | Real/protocol-faithful implementation for hermetic local deploy (e.g. `CamelotFactory`) — **not** a fake |
| **Harness / mintable stub** | Minimal ERC20/target with test hooks |
| **Mock / test double** | Canned dependency behavior; last resort; never the SUT |
| **Handler** | Fuzz/invariant wrapper around a **real** SUT |

See also `docs/development/testing.md` and consumer project AGENTS (e.g. IndexedEx `indexedex-testing`) for layered registry rules.

**Critical Alignment Requirements (LR-3):**
- Skills reflect finalized standards: full initialization, exact value assertions, mandatory Behavior library usage (not ad-hoc asserts), Facet + Package declaration tests, correct CraneTest/TestBase_* setUp() call order, NatSpec on all test surfaces (TestBase, Behavior, Handler, *.t.sol per LR-1 scope).
- Ties to central NatSpec process: use `CENTRALLY_COMPUTED_NATSPEC_VALUES.md` exclusively for any example selectors/interfaceIds (e.g. IFacet: facetName 0x5b6f4d01, facetInterfaces 0x2ea80826, facetFuncs 0x574a4cff, facetMetadata 0xf10d7a75, supportsInterface 0x01ffc9a7). Values originate from dedicated Foundry Script verification (not ad-hoc cast). See crane-natspec skill + `docs/development/natspec.md`.
- ERC1967 awareness: tests involving storage (multi-instance, custom slots) must respect correct `bytes32(uint256(keccak256(abi.encode("name"))) - 1)` DEFAULT_SLOT/STORAGE_SLOT pattern (see crane-architecture skill, LR-6).
- References GitBook / LR-2 required content: cross-link `docs/development/testing.md`; tests must cover required LR-2 areas (registry population assertions, protocol TestBase usage for ports, utility libs like Sets + ConstProdUtils in integration tests).

## Test Directory Structure

Test infrastructure lives in `contracts/`, test specs live in `test/`:

```
contracts/                              # Test infrastructure WITH the code
├── access/ERC8023/
│   ├── MultiStepOwnableRepo.sol
│   ├── MultiStepOwnableFacet.sol
│   └── TestBase_IMultiStepOwnable.sol  # TestBase next to implementation
├── introspection/ERC165/
│   ├── ERC165Facet.sol
│   ├── TestBase_IERC165.sol            # Behavior testing
│   └── Behavior_IERC165.sol            # Validation library
└── test/
    ├── stubs/                          # Small harnesses / examples (not protocol ports)
    ├── comparators/                    # Assertion helpers
    └── behaviors/                      # Shared behavior utilities

# Protocol ports (real protocol code for hermetic deploy) live under:
# contracts/protocols/.../stubs/  — e.g. CamelotFactory, not interface mocks

test/foundry/spec/                      # Actual test specs mirror contracts/
├── access/ERC8023/
│   └── MultiStepOwnable.t.sol
└── introspection/ERC165/
    └── ERC165Facet.t.sol
```

## TestBase Pattern

Two types of TestBase contracts exist. All TestBases **MUST** follow LR-7 rules.

### Correct CraneTest / TestBase Inheritance and Initialization Order (LR-7)
- Always inherit `CraneTest` (or a TestBase_* chain that ultimately inherits it) for factory bootstrap.
- Call parent `setUp()` via `Super.setUp()` (or explicit parent) **first** in override.
- **Full and Correct Initialization required**: Never pass `address(0)` for facet addresses in DFPkg construction or package deployment. The subject under test must reach a production-like, fully-initialized state before any assertions (see `InitDevService`, `CraneTest.setUp()`).
- Deploy only if not already present (idempotent guards) to support inheritance chains.

### Protocol Setup TestBase

Sets up protocol infrastructure with inheritance chains. `new CamelotFactory` / `new CamelotRouter` here deploy **protocol ports** (production-faithful code under `protocols/.../stubs/`), not canned mocks. Crane facets/DFPkgs under test still go through factories.

```solidity
abstract contract TestBase_CamelotV2 is TestBase_Weth9 {
    ICamelotFactory internal camelotV2Factory;
    ICamelotV2Router internal camelotV2Router;

    function setUp() public virtual override {
        TestBase_Weth9.setUp();  // Call parent setUp FIRST (CraneTest provides factories)
        if (address(camelotV2Factory) == address(0)) {
            // Protocol port under contracts/protocols/dexes/camelot/v2/stubs/
            camelotV2Factory = new CamelotFactory(feeToSetter);
        }
        if (address(camelotV2Router) == address(0)) {
            camelotV2Router = new CamelotRouter(address(camelotV2Factory), address(weth));
        }
    }
}
```

See GitBook LR-2 content: `docs/development/testing.md` (Setup TestBases) and protocol docs for how TestBases enable testing of ported protocols (e.g. Balancer, Camelot) + utility usage.

### Behavior TestBase

Defines expected behavior via virtual functions. Used for declaration tests:

```solidity
abstract contract TestBase_IFacet is Test {
    IFacet internal testFacet;

    function setUp() public virtual {
        testFacet = facetTestInstance();  // Must be fully initialized instance (no 0 addr)
    }

    // Virtual functions - inheritors return expected (control) values
    function facetTestInstance() public virtual returns (IFacet);
    function controlFacetName() public view virtual returns (string memory);
    function controlFacetInterfaces() public view virtual returns (bytes4[] memory);
    function controlFacetFuncs() public view virtual returns (bytes4[] memory);

    // Test functions validate actual vs expected using Behavior (exact)
    function test_IFacet_facetName() public view {
        assertTrue(Behavior_IFacet.areValid_IFacet_facetName(testFacet, controlFacetName(), testFacet.facetName()));
    }

    function test_IFacet_FacetInterfaces() public {
        bytes4[] memory expected = controlFacetInterfaces();
        bytes4[] memory actual = testFacet.facetInterfaces();
        assertEq(actual.length, expected.length, "count mismatch");
        assertTrue(Behavior_IFacet.areValid_IFacet_facetInterfaces(testFacet, expected, actual));
    }

    function test_IFacet_FacetFunctions() public {
        // ... similar exact length + Behavior
    }

    function test_IFacet_FacetMetadata_Consistency() public {
        assertTrue(Behavior_IFacet.isValid_IFacet_facetMetadata_consistency(testFacet));
    }
}
```

**Facet Declaration Tests (mandatory LR-7)**: Every deployed Facet must be tested via `facetInterfaces()`, `facetFuncs()`, `facetName()`, `facetMetadata()` matching expected (via Behavior + control fns). Use central IFacet selectors when asserting or documenting.

**Package Declaration Tests (mandatory LR-7)**: DFPkgs must be tested for `packageName()`, `facetAddresses()`, `facetCuts()`, `diamondConfig()`, `calcSalt(...)`, `processArgs(...)`, `initAccount(...)`, `postDeploy(...)`. End-to-end via real factory delegatecall for `initAccount`.

### Surface completeness matrix (mandatory — prevents silent dead API)

**Known failure class:** implementors omit selectors from `facetFuncs()`; declaration tests pass because controls were copied from the incomplete Facet; packages never cut those selectors onto proxies; product functions exist only on the implementation address.

| Layer | Required |
|-------|----------|
| **Target / product interface** | Enumerate all money-moving + documented view entrypoints |
| **controlFacetFuncs / controlFacetInterfaces** | Built from Target/interface (**not** by reading Facet.sol alone) |
| **Facet `facetFuncs()`** | Exact match to controls via `Behavior_IFacet` |
| **DFPkg `facetCuts()`** | Every facet selector appears in a cut |
| **Live proxy** | After factory/registry deploy: `facetAddress(sel) != 0` and smoke call on **proxy** |

Minimum tests:

1. Declaration (Behavior_IFacet) with Target-derived controls.
2. Package cuts include all declared facet selectors.
3. Post-deploy loupe + at least one real call per product selector on the diamond proxy (success or exact access/guard revert — never unknown selector).

See adversarial catalog **J1–J4** and `crane-adversarial-testing/references/implementation-test-dod.md`.

### Accounting / trust-flag tests (mandatory when applicable)

If the SUT accepts `pretransferred`, Permit2, or credits inbound assets:

1. Happy path with real transfer.
2. **Negative:** claim pretransferred / amount without transferring while vault already holds inventory → **no free shares** (exact revert or zero credit). Absolute `balanceOf(vault) >= amount` is **not** sufficient production logic.
3. Short delivery vs claimed amount → exact selector revert.
4. Credit uses observed **delta**, not caller claim alone (fee-on-transfer included).

See adversarial **I1–I5**, **K**, and `docs/NEGATIVE_TEST_COVERAGE_REPORT.md` patterns in consumer repos.

See `TestBase_IFacet` + `Behavior_IFacet` (contracts/factories/diamondPkg/). Similar for IDiamondFactoryPackage.

## Behavior Libraries (`Behavior_*.sol`)

**Mandatory LR-7 Rule**: Standard interfaces and patterns (**IFacet**, **IDiamondFactoryPackage**, protocol interfaces) **MUST** be validated using the appropriate `Behavior_*` libraries (e.g. `Behavior_IFacet`, `Behavior_IERC165`, `Behavior_IDiamondFactoryPackage`). Hand-written assertions or direct `assertEq` on these surfaces are insufficient and non-compliant.

Libraries encapsulate validation logic for interface compliance. Named `Behavior_I{Interface}`:

```solidity
library Behavior_IERC165 {
    using UInt256 for uint256;
    Vm constant vm = Vm(VM_ADDRESS);

    function _Behavior_IERC165Name() internal pure returns (string memory) {
        return type(Behavior_IERC165).name;
    }

    // expect_* - Store expected values in ComparatorRepo (use before subject calls in tests)
    function expect_IERC165_supportsInterface(IERC165 subject, bytes4[] memory expectedInterfaces_) public {
        console.logBehaviorEntry(_Behavior_IERC165Name(), "expect_IERC165_supportsInterface");
        Bytes4SetComparatorRepo._recExpectedBytes4(
            address(subject), IERC165.supportsInterface.selector, expectedInterfaces_
        );
        console.logBehaviorExit(_Behavior_IERC165Name(), "expect_IERC165_supportsInterface");
    }

    // isValid_* / areValid_* - Compare expected vs actual directly (preferred in declaration tests)
    function isValid_IERC165_supportsInterfaces(IERC165 subject, bool expected, bool actual)
        public view returns (bool valid)
    {
        valid = expected == actual;
        if (!valid) {
            console.logBehaviorError(...);
        }
        return valid;
    }

    // hasValid_* - Validate against stored expectations (for post-action checks)
    function hasValid_IERC165_supportsInterface(IERC165 subject) public view returns (bool isValid_) {
        console.logBehaviorEntry(_Behavior_IERC165Name(), "hasValid_IERC165_supportsInterface");
        // ... iteration over expectations
        console.logBehaviorExit(_Behavior_IERC165Name(), "hasValid_IERC165_supportsInterface");
    }
}
```

### Behavior Function Types

| Pattern | Purpose | Example |
|---------|---------|---------|
| `expect_*` | Store expected values | `expect_IERC165_supportsInterface(subject, interfaces)` |
| `isValid_*` / `areValid_*` | Compare expected vs actual directly (exact match) | `isValid_IERC165_supportsInterfaces(subject, true, actual)` |
| `hasValid_*` | Validate against stored expectations | `hasValid_IERC165_supportsInterface(subject)` |

Behavior libs produce structured console logs (`logBehavior*`) for debugging mismatches. They are used in both unit declaration tests and inside Handlers.

See GitBook: `docs/development/testing.md` (Behavior Libraries) + LR-2 protocol/utility test coverage. Also `Behavior_IFacet` for facet declaration (uses central IFacet values 0x5b6f4d01 etc.). Cross-ref crane-natspec for NatSpec on Behavior public helpers.

## Handler Pattern (Invariant Testing)

For fuzz/invariant testing, use a Handler + TestBase pattern per LR-7.

### Handler Contract

Wraps Subject Under Test (SUT), exposes fuzzable operations, tracks expected state. **Must use exact assertions + declared expectations**:

- Always use `vm.expectRevert(...)` (selector + typed form where possible; match NatSpec selector) and `vm.expectEmit` **before** state changes.
- Track precise expected state (e.g. `_expectedAllowance`).
- Normalize seeds to small address set via `addrFromSeed`.
- SUT must be attached in fully initialized state (production-like).

```solidity
contract ERC20TargetStubHandler is Test {
    IERC20 public sut;
    mapping(bytes32 => uint256) internal _expectedAllowance;  // exact tracked state

    function transfer(uint256 ownerSeed, uint256 toSeed, uint256 amount) external {
        address owner = addrFromSeed(ownerSeed);  // Normalize fuzz input
        address to = addrFromSeed(toSeed);

        uint256 bal = sut.balanceOf(owner);
        vm.prank(owner);

        if (amount > bal) {
            vm.expectRevert(IERC20Errors.ERC20InsufficientBalance.selector);  // exact
            sut.transfer(to, amount);
            return;
        }

        vm.expectEmit(true, true, false, true);  // precise topics + data
        emit IERC20.Transfer(owner, to, amount);
        sut.transfer(to, amount);
        // handler would update its _expected* here for invariants
    }
}
```

### Invariant TestBase

Declares invariants and virtual deployment functions. Invariants use **exact** `assertEq` (no "changed" checks):

```solidity
abstract contract TestBase_ERC20 is Test {
    ERC20TargetStubHandler public handler;

    function _deployToken(ERC20TargetStubHandler handler_) internal virtual returns (IERC20);

    function setUp() public virtual {
        handler = new ERC20TargetStubHandler();
        IERC20 token = _deployToken(handler);  // full init, no bypass
        handler.attachToken(token);

        targetContract(address(handler));
        targetSelector(FuzzSelector({
            addr: address(handler),
            selectors: [handler.transfer.selector, handler.approve.selector]
        }));
    }

    // Invariant: exact equality
    function invariant_totalSupply_equals_sumBalances() public view {
        address[] memory addrs = handler.asAddresses();
        uint256 sum = 0;
        for (uint256 i = 0; i < addrs.length; i++) {
            sum += handler.balanceOf(addrs[i]);
        }
        assertEq(sum, handler.totalSupply(), "exact totalSupply invariant");
    }

    // Preview parity example (LR-7 for vaults/etc.): assert exact match preview vs execute
    // function test_preview_matches_execute() ... { uint256 p = vault.previewX(..); ... assertEq(p, actual); }
}
```

**Additional LR-7 invariants expectations**:
- CREATE3/salt determinism assertions (same inputs => same addr).
- Registry population assertions after deployments (FacetRegistry etc. contain expected).
- Storage isolation proofs for multi-instance.
- Full access-control + reentrancy matrix using actual guards (if using Operable/Reentrancy).
- Fork parity for protocol ports (compare outputs to live on-chain).
- Preview function exact parity for all preview* (deposit/mint/withdraw/redeem etc.).

## TestBase Inheritance Chain

```
CraneTest                          # Factory setup via InitDevService (create3Factory, diamondPackageFactory) - call setUp() first
    └── TestBase_Weth9             # WETH deployment
        └── TestBase_CamelotV2     # Camelot factory + router
            └── TestBase_CamelotV2_Pools  # Pool creation helpers
                └── YourTest.t.sol  # Actual test contract
```

**Rule (LR-7 + CraneTest order)**: Inheritors must call the parent setUp in correct order. `CraneTest.setUp` bootstraps via `InitDevService.initEnv` (provides create3Factory + diamondPackageFactory). See `crane-deployment` skill for CraneTest + factory usage inside tests. Never `new` real production Crane contracts in tests (use factories + packages).

See GitBook LR-2: `docs/development/testing.md` + deployment docs for registry + protocol TestBase usage.

## Key Conventions (LR-7)

- **Production-first**: real contracts + factories; no mocks for SUT (see top of this skill).
- **Full init only**: SUTs (especially via DFPkgs) use real non-zero facet addresses; no bypass.
- Handler normalizes fuzz inputs: `addrFromSeed(seed)` maps to small address set.
- Handler tracks expected state: `_expectedAllowance`, `_seen`, etc.
- **Exact assertions always**: `assertEq(expected, actual)` (precise deltas), never "changed" checks. Use `vm.expectEmit` with full topics/data.
- Invariant functions named `invariant_*` for Foundry discovery.
- Use `vm.expectRevert` (selector + typed) / `vm.expectEmit` to declare expected behavior. Match NatSpec selectors.
- TestBase declares virtual `_deploy*` functions for SUT injection.
- **Mandatory Behaviors** for IFacet / IDiamondFactoryPackage / standards (see above).
- **Declaration tests** for every Facet + Package.
- **Preview parity** exhaustive where applicable.
- **Registry + CREATE3 determinism + storage isolation** assertions required after relevant ops.
- **NatSpec on test code** (LR-1 scope): public APIs on TestBase_*, Behavior_*, IHandler, handlers, stubs, comparators, *.t.sol must use // tag:: + @custom:selector etc. Use ONLY central values.

## Additional Resources

### Reference Files

- **`references/behavior-library.md`** - Complete Behavior library guide
- **`references/handler-pattern.md`** - Invariant testing with Handlers

### Key Files (cross-ref AGENTS.md)

- `/contracts/test/CraneTest.sol` - Base with factory infrastructure (via InitDevService)
- `/contracts/factories/diamondPkg/TestBase_IFacet.sol` + `/contracts/factories/diamondPkg/Behavior_IFacet.sol` - Facet declaration + Behavior
- `/contracts/introspection/ERC165/Behavior_IERC165.sol` + `TestBase_IERC165.sol`
- `/contracts/tokens/ERC20/TestBase_ERC20.sol` + handler - Invariant example
- `/contracts/test/comparators/Bytes4SetComparator.sol` + other comparators
- `/contracts/test/behaviors/BehaviorUtils.sol`
- Protocol: `contracts/protocols/.../test/bases/TestBase_*.sol`
- Also see `IHandler.sol`, stubs under `contracts/test/`

Ties to other skills: `crane-deployment` (factories + init in tests), `crane-architecture` (DFPkg + slots), `crane-natspec` (test NatSpec + central values process), `crane-adversarial-testing` (abuse catalogs A–K, trust-flag I, surface J, hostile harnesses, P0/P1 security suites — production-first; see `references/implementation-test-dod.md`). GitBook: `docs/development/testing.md`, `docs/development/natspec.md`, deployment/ and protocols/ sections (LR-2).

## LR-7 Testing Standards (Mandatory - Full List Excerpt)

All tests (unit, behavior/declaration, invariant, fork) must satisfy (non-exhaustive per PRD):

1. **Full and Correct Initialization** - Fully initialize before assertions. Packages use real facets (no address(0)). Production-like state only. Prefer production code over mocks for the SUT.
2. **Exact Expected Value Assertions** - Precise values/deltas (e.g. `assertEq(delta, expectedAmount)`), not side-effect "changed".
3. **Preview Function Exact Match** - For previewDeposit etc., assert returned value exactly equals result of executing the action (incl. edges).
4. **Facet Declaration Tests** - Validate `facetInterfaces()`, `facetFuncs()`, `facetName()`, `facetMetadata()` using `Behavior_IFacet` + control values **derived from Target/product API**.
5. **Package Declaration Tests** - Validate all pkg metadata + `calcSalt`, `processArgs`, `initAccount` (real delegatecall), `postDeploy`.
6. **Mandatory Behavior Libraries** - Use `Behavior_*` (IFacet, IDiamondFactoryPackage, protocols) for standards compliance. No bypassing.
7. **Event + Delta Exactness** - `vm.expectEmit` + exact post-state.
8. **CREATE3 / Salt Determinism** - Assert identical inputs give identical addresses.
9. **Registry Population** - After deploy via factory/pkg, assert registries (Facet/Package/CallTarget etc.) updated correctly.
10. **Storage Isolation** - Multi-instance tests prove no leakage.
11. **Full DFPkg Lifecycle** - calcSalt, process, delegatecall initAccount, postDeploy.
12. **Error Selectors** - Test with selector and typed form; match declared NatSpec selector (use central values).
13. **Correct TestBase/CraneTest** - Proper inheritance + ordered `setUp()` calls; no duplication/bypass.
14. **NatSpec on Test Code** - Same LR-1 standard for public test APIs (tags + @custom using central).
15. **Access/Reentrancy Matrix + Fork Parity** - Full coverage for operable/reentrancy; fork tests compare key outputs to on-chain.
16. **Proxy surface completeness** - Target ↔ Facet ↔ DFPkg cuts ↔ live loupe ↔ callable on proxy (see Surface matrix above). Facet-only tests are insufficient.
17. **Trust-flag / inbound accounting** - When `pretransferred` / pull / permit exists: negative tests prove no free credit from claimed amounts or absolute balance alone; credit = observed delta.
18. **Adversarial P0 or explicit defer** - Money products need catalog coverage (or NatSpec deferral) per `crane-adversarial-testing`; happy path alone is not a security bar.

Tests violating these are insufficient. See also exact registry + fork details in PRD LR-7 and AGENTS.md.

## Central NatSpec + ERC1967 Ties for Testers

- Use `CENTRALLY_COMPUTED_NATSPEC_VALUES.md` (ONLY) when tests or Behaviors reference selectors/interfaceIds (e.g. IFacet values above).
- NatSpec verification is via committed Foundry Script (see `docs/development/natspec.md` + scripts/).
- Storage-using tests must align with ERC1967 slot standard (LR-6): `DEFAULT_SLOT = bytes32(uint256(keccak256(abi.encode("hier.name"))) - 1)`.
- This enables agent-proof reuse + GitBook areas (LR-2/LR-4): reusable factories, declared facets, testable protocols.

Update this skill (and its gap report) whenever standards evolve (LR-3).
