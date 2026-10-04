---
name: crane-deployment
description: "Deploy Crane facets and diamond packages with CREATE3, FactoryService and deterministic factory workflows."
license: MIT
---

# Crane Deployment Patterns

Crane uses a two-factory system for deterministic cross-chain deployments of Diamond proxies.

## Factory Hierarchy

```
Create3Factory                    # Deploys facets, packages, and any contract
    └── DiamondPackageCallBackFactory   # Deploys Diamond proxy instances from packages
```

## Reusability of DiamondPackageCallBackFactory

The `DiamondPackageCallBackFactory` (which implements `IDiamondPackageCallBackFactory`, interfaceId `0x949da331` per central values) is **deployed once per chain/setup** via `Create3Factory.create3WithArgs(...)` (see `InitDevService.initDiamondFactory`).

```solidity
// From central computed values
// interfaceId: 0x949da331
// deploy(IDiamondFactoryPackage,bytes) selector: 0xe97fac05
// calcAddress(...) : 0x33a41d70
```

From implementation NatSpec:

> @dev Deployed once via Create3Factory (see Create3Factory.diamondPackageFactory()). Safe and intended for reuse by any consumer on any chain.

From `IDiamondPackageCallBackFactory` interface:

> @dev Deployed once and reused (see implementation and deployment docs).

**You do not deploy a new `DiamondPackageCallBackFactory` per project, per DFPkg, or per chain.** Obtain its address from any `ICreate3Factory` via `diamondPackageFactory()`. It installs base facets (ERC165, DiamondLoupe, ERC8109, post-deploy hook) on every proxy and delegates to the provided `IDiamondFactoryPackage` (interfaceId computed via XOR of selectors; see central and IDiamondFactoryPackage.sol) for `facetCuts`, `initAccount`, and `postDeploy`.

See deployment docs: `docs/deployment/create3.md` (critical reuse note) and `docs/deployment/dfpkg.md`.

This enables the core value: facets/packages deployed once (amortized cost + security via reuse of verified code), proxies are cheap and identical.

## Chain Bootstrap with Create3FactoryDFPkg

To stand up a Crane presence on a new chain (GitBook/LR-2 requirement):

1. Bootstrap an initial `Create3Factory` (this is a special entrypoint that supports `ICreate3FactoryProxy` and bootstrap methods for canonical facets):
   ```solidity
   // As in InitDevService.initFactory (uses CREATE2 for first instance)
   factory = ICreate3FactoryProxy(address(new Create3Factory{salt: salt}(owner)));
   ```
   Then deploy its core facets (DiamondCut, MultiStepOwnable, Operable, Create3FactoryFacet, registry facets, etc.) via its bootstrap, and the shared `DiamondPackageCallBackFactory`.

2. Use the `Create3FactoryDFPkg` (which implements `ICREATE3DFPkg` extending `IDiamondFactoryPackage`) to deploy additional configured `Create3Factory` proxy instances:
   ```solidity
   // PkgInit and PkgArgs are defined on the INTERFACE (critical rule)
   // (see central and source for selectors e.g. packageName(): 0xabc8b346)
   ICREATE3DFPkg create3Pkg = ...;  // obtained via registry or direct deploy

   ICreate3FactoryProxy myCreate3 = create3Pkg.deployCreate3Factory(owner);
   // Internally: DIAMOND_FACTORY.deploy(SELF, abi.encode(PkgArgs({owner: owner})))
   ```

   This deploys a full Create3Factory Diamond (with Cut, ownership, operable, create3 facet + registries for facet/package/callTarget) at a deterministic address.

See `Create3FactoryDFPkg.sol` for `PkgInit` (diamondCutFacet etc + the reusable diamondFactory), `facetInterfaces()`, `facetCuts()`, `initAccount` (sets MultiStepOwnable), `calcSalt(bytes)` (hashes pkgArgs).

The shared `DiamondPackageCallBackFactory` is obtained or passed in; it is NOT redeployed.

See: `docs/deployment/create3.md`, `InitDevService.sol`, and `Create3FactoryDFPkg.sol` (exact tags and NatSpec).

After bootstrap, use `IFacetRegistry(address(factory)).canonicalFacet(type(IFoo).interfaceId)` to resolve facets without hard addresses.

## Registries Explanation

Crane auto-maintains registries populated during CREATE3 deployments (via `Create3Factory._registerFacet` / `_registerPackage` which call the Repos using facet/package metadata):

- **FacetRegistry** (`IFacetRegistry`): Tracks all deployed facets by name, interfaceId, function selector. Key methods (use canonical for overrides):
  - `canonicalFacet(bytes4 interfaceId)`
  - `facetsOfInterface(bytes4)`, `allFacets()`, `registerFacet(...)`, `setCanonicalFacet(...)`
  - Used in packages, InitDev, FactoryServices to resolve e.g. `IFacetRegistry(...).canonicalFacet(type(IDiamondCut).interfaceId)`

- **DiamondFactoryPackageRegistry** (`IDiamondFactoryPackageRegistry`): Similar for DFPkgs.
  - `canonicalPackage(bytes4 interfaceId)`
  - `packagesByInterface`, `packagesByFacet(IFacet)`, `registerPackage`, `deploy*Package*`

- **CallTarget Registry** (query + management): Controls allowed external call targets (for metatx/relayers etc.).

Registries are populated automatically on every `deployFacet` / `deployPackage*` through the Create3Factory. Consumers query for canonical implementations rather than hardcoding.

See full details in docs (GitBook target) and `docs/deployment/create3.md`, source `FacetRegistryRepo.sol` etc., and `Create3Factory.sol` registration logic.

This supports discovery, override for canonicals, and verification of deployed components.

## Deployment Flow

### Step 1: Initialize Factories

In test `setUp()` or deployment scripts (via CraneTest or direct; provides fully initialized factories + registries):

```solidity
// Typically from CraneTest: create3Factory, diamondPackageFactory already set by InitDevService.initEnv
(ICreate3FactoryProxy create3Factory, IDiamondPackageCallBackFactory diamondFactory) =
    InitDevService.initEnv(address(this));
```

### Step 2: Deploy Facets

Use Create3Factory to deploy facets with deterministic addresses:

```solidity
IFacet erc20Facet = factory.deployFacet(
    type(ERC20Facet).creationCode,
    abi.encode(type(ERC20Facet).name)._hash()  // Salt from name hash
);
```

### Step 3: Deploy Package

Deploy package with facet references in constructor:

```solidity
IERC20DFPkg erc20Pkg = IERC20DFPkg(address(
    factory.deployPackageWithArgs(
        type(ERC20DFPkg).creationCode,
        abi.encode(IERC20DFPkg.PkgInit({ erc20Facet: erc20Facet })),  // Constructor args
        abi.encode(type(ERC20DFPkg).name)._hash()  // Salt
    )
));
```

### Step 4: Deploy Diamond Proxy Instances

```solidity
// Option A: Via package's deploy() helper
IERC20 token = erc20Pkg.deploy(diamondFactory, "Token", "TKN", 18, 1000e18, recipient, bytes32(0));

// Option B: Via factory directly
address proxy = diamondFactory.deploy(pkg, abi.encode(pkgArgs));
```

## Key Components

| Component | Purpose |
|-----------|---------|
| `Create3Factory` | Deploys any contract with deterministic addresses via CREATE3; auto-populates registries |
| `DiamondPackageCallBackFactory` | Reusable (deploy once): deploys Diamond proxies via CREATE2 + delegatecall `initAccount` (interfaceId 0x949da331) |
| `IDiamondFactoryPackage` | Interface for packages (see central for selectors e.g. 0xabc8b346 packageName, 0x870d4838 initAccount) - bundles facets + init logic. Pkg* structs MUST be in the interface. |
| `InitDevService` | Library to bootstrap the factory system in tests (full init + registries) |
| `Create3FactoryDFPkg` | DFPkg for deploying your own Create3Factory instance(s) |

## Create3Factory Methods

### `deployFacet()`

Deploy a facet (no constructor args):

```solidity
IFacet facet = factory.deployFacet(
    type(MyFacet).creationCode,
    salt
);
```

### `deployPackageWithArgs()`

Deploy a package with constructor arguments:

```solidity
// Selectors from central CENTRALLY_COMPUTED_NATSPEC_VALUES.md e.g.:
// packageName(): 0xabc8b346 ; facetCuts(): 0xa4b3ad35 ; diamondConfig(): 0x65d375b3
// initAccount(bytes): 0x870d4838 ; postDeploy(address): 0x70068fcf
IDiamondFactoryPackage pkg = IDiamondFactoryPackage(address(
    factory.deployPackageWithArgs(
        type(MyPkg).creationCode,
        abi.encode(IMyPkg.PkgInit({ ... })),  // Constructor args
        salt
    )
));
```

**Important**: `PkgInit` (and `PkgArgs`) must be defined in the interface `IMyPkg`, not the contract. This is required so that `IMyPkg.PkgInit` can be used in `abi.encode(...)` and FactoryServices. See `crane-architecture` skill → `references/dfpkg-pattern.md`. All NatSpec uses verified Foundry-computed values + exact tag:: wrappers.

### `deploy()`

Deploy any contract:

```solidity
address deployed = factory.deploy(
    creationCode,
    salt
);
```

## Salt Calculation

Always derive salt from type name for deterministic addresses:

```solidity
using BetterEfficientHashLib for bytes;

bytes32 salt = abi.encode(type(MyContract).name)._hash();
```

This ensures:
- Same address across all EVM chains
- Predictable deployment addresses
- No salt collision between different contracts

## DiamondPackageCallBackFactory Flow

See full diagram + NatSpec in `/contracts/interfaces/IDiamondPackageCallBackFactory.sol` (and impl).

1. User calls `factory.deploy(pkg, pkgArgs)` (selector 0xe97fac05)
2. Factory delegatecalls `pkg.calcSalt(pkgArgs)` (0xd82be56e)
3. Factory deploys `MinimalDiamondCallBackProxy` via CREATE2 (using PROXY_INIT_HASH 0x1c8b7630)
4. Proxy callbacks to `initAccount(pkg, pkgArgs)` (0x8e85783e)
5. Applies cuts from `pkg.diamondConfig()` / `facetCuts()`, delegatecalls `pkg.initAccount(initArgs)`
6. Calls `pkg.postDeploy(account)` (0x70068fcf); also base post hook.

Full flow emits DiamondCut; supports `calcAddress` for prediction. The factory itself declares IFacet surface for metadata.

## FactoryService Pattern

Group related deployments in FactoryService libraries (see crane-architecture for more):

```solidity
library MyFeatureFactoryService {
    using BetterEfficientHashLib for bytes;
    Vm constant vm = Vm(VM_ADDRESS);

    function deployMyFacet(ICreate3Factory factory) internal returns (IFacet) {
        IFacet facet = factory.deployFacet(
            type(MyFacet).creationCode,
            abi.encode(type(MyFacet).name)._hash()
        );
        vm.label(address(facet), type(MyFacet).name);  // Always label!
        return facet;
    }
}
```

See `references/factory-service-examples.md` for complete examples (Access, Introspection etc.). Always label and use typed deploy* helpers.

## Test Setup Pattern (LR-7 Compliant)

Per LR-7 testing rules: full initialization before assertions (never pass `address(0)` facets into DFPkgs or packages); exact value assertions (not just "changed"); use `Behavior_*` libraries (e.g. `Behavior_IFacet`, `Behavior_IDiamondFactoryPackage`) for declaration and compliance (never hand-rolled asserts for standard surfaces); assert registry population, salt determinism, and full DFPkg lifecycle (calcSalt, processArgs, initAccount via delegatecall, postDeploy); inherit CraneTest/TestBase properly and call parent setUp in order; use `vm.expectEmit` + exact deltas. **Tests should use the same factory/DFPkg deploy path as production** (prefer production code over mocks for the SUT — see `crane-testing`).

```solidity
contract MyTest is CraneTest {
    IFacet myFacet;
    IMyDFPkg myPkg;

    function setUp() public override {
        super.setUp();  // Initializes factories via InitDevService (full non-zero facets)

        // Deploy facet
        myFacet = create3Factory.deployFacet(
            type(MyFacet).creationCode,
            abi.encode(type(MyFacet).name)._hash()
        );
        vm.label(address(myFacet), "MyFacet");

        // Deploy package - PkgInit from INTERFACE only
        myPkg = IMyDFPkg(address(
            create3Factory.deployPackageWithArgs(
                type(MyDFPkg).creationCode,
                abi.encode(IMyDFPkg.PkgInit({ myFacet: myFacet })),
                abi.encode(type(MyDFPkg).name)._hash()
            )
        ));
        vm.label(address(myPkg), "MyDFPkg");

        // LR-7: verify registry population after deploy
        // assertTrue( IFacetRegistry(address(create3Factory)).facetsOfInterface(type(IMyIFace).interfaceId).length > 0 );
    }
}
```

## Test Setup and Inheritance

Always inherit from `CraneTest` (see `crane-testing` skill) for factory bootstrap:

```solidity
contract MyTest is CraneTest {
    // ...
    function setUp() public virtual override {
        super.setUp();  // Provides create3Factory + diamondPackageFactory via InitDevService.initEnv
        // Now deploy using the factories...
    }
}
```

`CraneTest` calls `InitDevService.initEnv(address(this))` to set up the two factories (including wiring canonicals in registries).

For interface compliance and package metadata (per LR-7 + NatSpec):
- Use `Behavior_IFacet.areValid_IFacet_...` and `Behavior_IDiamondFactoryPackage`
- Explicitly test facet declaration: `facetName()`, `facetInterfaces()`, `facetFuncs()`, `facetMetadata()` match expected (use central selectors e.g. facetInterfaces(): 0x2ea80826)
- Test full package surface: `packageName()` (0xabc8b346), `facetAddresses()` (0x52ef6b2c), `facetCuts()` (0xa4b3ad35), `diamondConfig()` (0x65d375b3), `calcSalt`, `processArgs`, `initAccount`, `postDeploy`.

See `crane-testing` skill for Behavior + Handler details. Tests must also have NatSpec + tags (LR-1).

## Common Anti-Patterns (Avoid These)

- `new MyFacet()` or `new MyDFPkg(...)` — breaks determinism and CREATE3 guarantees.
- Calling `diamondPackageFactory.deploy(...)` for packages that a consumer project expects to be registered through its own manager/registry.
- Forgetting `vm.label(...)` after deployments (hurts debugging).
- Using raw `create3Factory.deploy(creationCode, salt)` instead of typed `deployFacet` / FactoryService helpers.
- Bypassing `InitDevService` or `CraneTest` in tests.
- Passing `address(0)` for any facet in PkgInit (violates LR-7 full init).
- Hand-asserting `facetInterfaces()` / `packageName()` etc. instead of `Behavior_IFacet` / `Behavior_IDiamondFactoryPackage` + declaration tests.
- Weak assertions (e.g., "balance changed") instead of exact deltas + `vm.expectEmit`.
- Ignoring registries or failing to assert population after factory deploys.
- Using non-ERC1967 slot forms in any Repos (see crane-architecture; `DEFAULT_SLOT = bytes32(uint256(keccak256(abi.encode("name"))) - 1)`).

## Consumer / Application Layers

Crane provides the core primitives. Some consuming projects introduce additional registry, manager, or authorization layers on top (for example, requiring certain packages to be registered before they can create instances, or routing deployments through a central manager for discovery and access control). The built-in registries (Facet, Package, CallTarget) are always populated automatically by Create3Factory deployments.

When working in such a project:
- Use Crane's core patterns for facets and generic packages.
- Follow the consuming project's documentation and TestBases for any registry/manager-specific deployment paths.
- The `crane-deployment` skill and this repo's docs describe the *foundational* CREATE3 + DFPkg behavior (including reuse of DiamondPackageCallBackFactory and Create3FactoryDFPkg for chain bootstrap).

See the consuming project's AGENTS.md for project-specific rules. See root AGENTS.md and `docs/` for Crane navigation.

## For AI Agents: Reusable, Low-Cost Deployments

When an agent is building features for users:

- Always route deployments through the two-factory system and DFPkgs. Never redeploy `DiamondPackageCallBackFactory`.
- Emit clear `vm.label` calls — it helps all agents debugging traces.
- After creating a new reusable package or service, update or create a skill documenting the pattern so other agents discover and reuse it.
- The economic pitch of Crane is **amortized cost + security**: facets and packages are deployed once; every consumer's proxy is cheap and identical across chains. **Security benefit**: reuse of already-deployed/verified code eliminates new bugs (esp. important for agent-written code). **Cost benefit**: do not redeploy logic on every project/chain.
- Bootstrap new chains with `Create3FactoryDFPkg` + shared callback factory (see dedicated section above).
- All NatSpec values (selectors, interfaceids, topic0) **must** come from the central `CENTRALLY_COMPUTED_NATSPEC_VALUES.md` or the committed Foundry Script verifier (`scripts/compute_natspec_values.sh`); never ad-hoc `cast`. Wrap with exact `// tag::Symbol[] ... // end::Symbol[]` (LR-1). Include full scope (incl. tests).
- Follow LR-7: full init, Behaviors for validation, exact asserts, registry checks, salt determinism, proper TestBase order.
- Use ERC1967 slot form in any storage Repos touched.

Prefer composing existing Crane ports (via *AwareRepo + *Service) over writing raw external calls.

See the new `docs/concepts/building-with-crane.md` for a step-by-step agent workflow and `crane-architecture` for the patterns. Update skills on any standard evolution (NatSpec process, ERC1967, LR-7, GitBook topics).

## Additional Resources

### Reference Files

- **`references/factory-service-examples.md`** - Complete FactoryService examples
- See Crane AGENTS.md for high-level navigation and required reading (explicitly calls out `crane-deployment` for CREATE3/DFPkgs/FactoryService/Diamond proxy).
- `docs/concepts/building-with-crane.md`, `docs/deployment/create3.md`, `docs/deployment/dfpkg.md`, `docs/deployment/battlechain.md`, and `docs/deployment/factory-services.md`

### GitBook / Required Content Links (LR-2)

- Chain setup / bootstrap: `docs/deployment/create3.md`
- Reusable DiamondPackageCallBackFactory: `docs/deployment/create3.md` and `docs/deployment/dfpkg.md`
- Registries (Facet/Package/CallTarget): explained in `docs/deployment/create3.md`; query via IFacetRegistry etc. populated by Create3Factory
- Full protocol + utility details live in their skills + `docs/`

### Key Files (accurate to current sources)

- `/contracts/factories/create3/Create3Factory.sol` - CREATE3 factory (auto registers to repos; see _register*)
- `/contracts/factories/create3/Create3FactoryDFPkg.sol` - For deploying Create3Factory instances (PkgInit/PkgArgs on ICREATE3DFPkg interface; deployCreate3Factory)
- `/contracts/factories/diamondPkg/DiamondPackageCallBackFactory.sol` - Reusable Diamond factory (NatSpec + tags use central values e.g. interfaceId 0x949da331)
- `/contracts/InitDevService.sol` - Factory + package bootstrap (wires diamondFactory, canonicals, multiple DFPkgs incl. Create3 and registries)
- `/contracts/interfaces/IDiamondFactoryPackage.sol` - Core package interface (DiamondConfig, all tagged methods with selectors from central: packageName 0xabc8b346, facetCuts 0xa4b3ad35, initAccount 0x870d4838, postDeploy 0x70068fcf etc.; flow diagram in comment)
- `/contracts/interfaces/IDiamondPackageCallBackFactory.sol` - Reusable factory surface + callback flow diagram
- Registries: `contracts/registries/facet/IFacetRegistry.sol`, `contracts/registries/package/IDiamondFactoryPackageRegistry.sol`
- Consult the `crane-deployment`, `crane-architecture`, and `crane-testing` skills for implementation guidance.
- Central NatSpec source: `docs/reports/gap/CENTRALLY_COMPUTED_NATSPEC_VALUES.md` (use ONLY these values; verify via Foundry script)
