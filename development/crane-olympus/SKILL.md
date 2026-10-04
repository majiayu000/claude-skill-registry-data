---
name: crane-olympus
description: This skill should be used when the user asks about "Crane Olympus", "Olympus port", "FOUNDRY_PROFILE=olympus_v3_port", "integrate Olympus Kernel", "Olympus Diamond strategy", "Olympus TestBase", "olympus hermetic tests", building Crane integrations against the Olympus Default Framework port, or writing Foundry tests for Olympus under tokens/stable/olympus/v3.
license: MIT
---

# Crane Olympus Integration

How to **build on** and **test** Olympus using Crane’s port (not general Olympus product UX — see operations; not Kernel theory — see architecture).

## Layout

| Layer | Path |
|-------|------|
| Domain | `contracts/protocols/tokens/stable/olympus/v3/` |
| Pin | `…/olympus/v3/VENDOR.md` (upstream pin, AGPL-3.0-only) |
| Hermetic tests | `test/foundry/spec/protocols/tokens/stable/olympus/v3/` |
| Service | `…/olympus/v3/services/OlympusKernelService.sol` |
| Aware | `…/olympus/v3/aware/OlympusKernelAwareRepo.sol` |
| TestBase | `…/olympus/v3/test/bases/TestBase_OlympusV3.sol` |
| Behavior | `…/olympus/v3/Behavior_IKernel.sol` |
| Quabi (FFI) | test lib `…/v3/lib/quabi/{path,jq}.sh` + `Quabi.sol` |
| Profile | `FOUNDRY_PROFILE=olympus_v3_port` in `foundry.toml` |
| Out / cache | `out_olympus_v3_port` / `cache_olympus_v3_port` |

**Diamond Facet-Target-Repo / DFPkg** for Kernel is not required; use Service + Aware + TestBase for strategy/Diamond consumers. Domain types remain importable via `@crane/…`.

### Legacy v2 research tree

| Item | Path |
|------|------|
| Domain / tests | `olympus/v2/` + `FOUNDRY_PROFILE=olympus_port` |
| Archived skills | `docs/archive/skills/olympus-v2/` |

## Quick start: compose a policy against the port

```solidity
import {Kernel, Policy, Permissions, Keycode, toKeycode} from
    "@crane/contracts/protocols/tokens/stable/olympus/v3/Kernel.sol";
import {MINTRv1} from
    "@crane/contracts/protocols/tokens/stable/olympus/v3/modules/MINTR/MINTR.v1.sol";
import {ROLESv1} from
    "@crane/contracts/protocols/tokens/stable/olympus/v3/modules/ROLES/ROLES.v1.sol";
import {RolesConsumer} from
    "@crane/contracts/protocols/tokens/stable/olympus/v3/modules/ROLES/OlympusRoles.sol";

contract StrategyPolicy is Policy, RolesConsumer {
    MINTRv1 internal MINTR;

    constructor(Kernel k) Policy(k) {}

    function configureDependencies() external override returns (Keycode[] memory deps) {
        deps = new Keycode[](2);
        deps[0] = toKeycode("MINTR");
        deps[1] = toKeycode("ROLES");
        MINTR = MINTRv1(getModuleAddress(deps[0]));
        ROLES = ROLESv1(getModuleAddress(deps[1]));
    }

    function requestPermissions() external view override returns (Permissions[] memory req) {
        req = new Permissions[](2);
        req[0] = Permissions(toKeycode("MINTR"), MINTR.mintOhm.selector);
        req[1] = Permissions(toKeycode("MINTR"), MINTR.increaseMintApproval.selector);
    }
}
```

**Deploy order:** Kernel → modules (`InstallModule`) → your policy (`ActivatePolicy`) → grant ROLES if needed.

## Testing ladder

| Layer | Command / pattern |
|-------|-------------------|
| Domain + suite compile | `FOUNDRY_PROFILE=olympus_v3_port forge build` |
| Full hermetic suite | `FOUNDRY_PROFILE=olympus_v3_port forge test` |
| Path match | `… forge test --match-path 'test/foundry/spec/protocols/tokens/stable/olympus/v3/**'` |
| Kernel unit | `Kernel.t.sol` — real Kernel install/activate |
| Module permissions | `modules/MINTR.t.sol` etc. — Quabi godmode fixtures need **ffi + ast** |

Profile sets `ffi=true`, `ast=true`, `src`/`test` scoped to olympus, `out_olympus_v3_port`.

## Production-first rules

- Never mock Kernel / modules / policies under test — deploy real ported contracts.
- Godmode fixtures use Quabi → AST artifacts; rebuild with `olympus_v3_port` so AST is present.
- Do not call module `permissioned` functions from tests as random EOAs without activating a fixture policy.
- Shared deps: OZ v4/v5, solmate, clones-with-immutable-args under `contracts/external/` — **never** nest private OZ under olympus.
- **Do not** change `contracts/external/uniswap/v3-periphery/.../TransferHelper.sol` IERC20 path to OZ v4 — breaks Fraxswap co-import with Crane IERC20.

## Navigation

| Topic | File |
|-------|------|
| Profile, commands, gotchas | `references/commands.md` |
| Integration patterns (Diamond/strategy) | `references/integration-patterns.md` |
| Protocol meaning | `skill:olympus-architecture` |
| User/operator flows | `skill:olympus-operations` |

## Key files

- `Kernel.sol`, `modules/*`, `policies/*`, `external/OlympusERC20.sol`, `external/cooler/*`
- Wrappers: `services/OlympusKernelService.sol`, `aware/OlympusKernelAwareRepo.sol`, `test/bases/TestBase_OlympusV3.sol`
- Tests: `test/foundry/spec/protocols/tokens/stable/olympus/v3/Kernel.t.sol`, `modules/*.t.sol`, `services/OlympusKernelService.t.sol`
- `foundry.toml` → `[profile.olympus_v3_port]`

## See also

- `skill:crane-testing`, `skill:crane-porting`, `skill:crane-porting-verification`
- `skill:crane-architecture` (when wrapping as Facet-Target-Repo later)
- Archived v2 skills: `docs/archive/skills/olympus-v2/`
