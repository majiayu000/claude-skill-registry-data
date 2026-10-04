---
name: crane-porting
description: This skill should be used when the user asks to "port a protocol", "vendor into Crane", "port code to Crane", "import upstream contracts", "remap dependencies", "contracts/external", "protocol port", "faithful port", "dedupe vendored deps", "VENDOR.md", Morpho/Ethena/Lido/Ajna port, or needs guidance on how Crane vendors DeFi protocols with shared transitive dependencies.
license: MIT
---

# Crane Protocol Porting

How to bring external DeFi protocol code into Crane as a **faithful port** with **shared, non-duplicated transitive dependencies**.

Companion skills: `crane-porting-verification` (tests/forks/DoD gates), `crane-architecture`, `crane-code-style`, `crane-testing`, `writing-skills`.

## Core principle (non-negotiable)

> **Port each protocol's own contracts faithfully; rewrite their dependency imports to Crane's already-vendored equivalents.**

| Layer | What goes here | Mutate logic? |
|-------|----------------|---------------|
| **Domain contracts** | Protocol market/AMM/vault/CDP/token logic | **No** — byte-for-logic equivalent to a pinned upstream tag |
| **Shared deps** | OZ, Solady, Solmate pieces, Permit2, forge-std, common oracles | **Do not re-vendor**; remap imports to existing `@crane/contracts/external/...` |
| **Protocol-unique math/infra** | e.g. Aave WadRayMath, Uniswap TickMath, BGD upgradeability | Stay with the protocol (not under a fake `dependencies/oz` tree) |
| **Crane wrappers** | Service / AwareRepo / Facet-Target-Repo / DFPkg / interfaces | **New** Crane-native code |

This is the difference between a useful Crane port and a bloated fork of the universe.

## Two trees (know which is which)

```
contracts/
├── external/          # Vendored upstream + shared framework deps
│   ├── openzeppelin-contracts/       # Canonical OZ (non-upgradeable)
│   ├── openzeppelin-contracts-v4/    # When v4 semantics are required
│   ├── openzeppelin-contracts-v5/
│   ├── openzeppelin-upgradeable*/    # Upgradeable OZ variants
│   ├── solady/
│   ├── solmate/
│   ├── uniswap/                      # Uni core/periphery source trees
│   ├── balancer/
│   ├── lido/                         # Protocol domain vendored here (example)
│   ├── aragon/                       # Transitive unique dep of Lido
│   └── …                             # Other shared / protocol-domain trees
│
└── protocols/         # Crane integration + wrappers + stubs + tests
    ├── dexes/{protocol}/{version}/
    ├── lending/{protocol}/{version}/
    ├── staking/{protocol}/…
    ├── tokens/…
    ├── oracles/…
    └── …
```

### `contracts/external/` — vendored source of truth

- **Shared frameworks** (OZ, Solady, Solmate, forge-std pieces): one canonical tree, many consumers.
- **Protocol domain sources** when the full tree is needed for compile/redeploy (e.g. `external/lido/`, `external/uniswap/v3-core/`).
- **Unique transitives** of a protocol (e.g. Aragon for Lido) live as their **own** top-level under `external/<name>/`, not nested inside the protocol as a private OZ clone.
- Every vendored package should have a **`VENDOR.md`** (see template below).

### `contracts/protocols/` — Crane surface

Typical layout (DEX example from AGENTS.md):

```
protocols/{category}/{protocol}/{version}/
├── interfaces/          # Crane-facing + thin I* re-exports if needed
├── services/            # Stateless *Service libraries for Diamond consumers
├── aware/               # *AwareRepo for router/factory/vault addresses
├── stubs/               # Protocol-faithful impls for hermetic local deploy (NOT mocks)
├── libraries/           # Protocol-unique shared math (only if not already in external)
├── test/bases/          # TestBase_* setup chains
└── (optional) diamond/  # Facet-Target-Repo + DFPkg when in-Diamond use is intended
```

**Do not** dump a second full OpenZeppelin under `protocols/.../dependencies/`. That pattern is legacy debt (see Aave v3.6) and is being eliminated — see `Aave_Vendored_Dependencies_Dedup_Plan.md` and `DEDUPLICATION.md`.

## Step-by-step port workflow

### 0. Gate checks (before any copy)

1. **License** — record SPDX/license. BUSL and similar need clearance before vendoring (`DEFI_PORTING_PRD.md` A.6).
2. **Upstream pin** — exact git tag or commit hash.
3. **Live deployments** — chain + addresses for fork tests (official docs/explorer).
4. **Dependency inventory** — list every import path the protocol uses; classify each as:
   - already in `contracts/external/...`
   - missing → must **expand external first**
   - protocol-unique → stays with domain code
5. **Vyper / multi-pragma** — decide interfaces+fork vs full `.vy` vendoring (`DEFI_PORTING_PRD.md` A.6).

### 1. Expand shared `external/` first

Rule: **expand first, migrate second, delete last.**

- If the protocol needs OZ `AccessManager` and it is missing from `external/openzeppelin-contracts/`, **add the file(s) to external** (matching the version the protocol expects) before rewriting imports.
- Prefer the **exact version/text** the protocol compiles against when behavior depends on it.
- Preserve existing Crane adaptations already in external (e.g. SafeERC20 routing to Crane `IERC20` where intentional).

**Semantic routing (critical — learned from dedup failures):**

| Consumer needs | Import target |
|----------------|---------------|
| OZ semantics (`Context`, `_msgSender`, string reverts, upgradeable bases, `AccessManager`, classic Ownable) | `@crane/contracts/external/openzeppelin-contracts...` (correct major) |
| Crane-native Diamond code | `@crane/contracts/access/...`, `@crane/contracts/utils/...` |
| **Never** | Silently swap OZ-semantic ports onto Crane-native Ownable/Context during a "dedup" |

Crane-native and OZ-vendored libraries are **not** interchangeable even when names match.

### 2. Vendor protocol domain sources

- Copy protocol contracts into `contracts/external/<protocol>/` (or `contracts/protocols/...` only when the tree is already a Crane-shaped port — prefer external for raw upstream).
- **No new git submodules** — sources are copied in.
- Drop non-runtime bloat when safe: `certora/`, upstream `test/`, `docs/`, `scripts/`, `audits/` (do not delete until confirmed unused by compile).
- Write `contracts/external/<protocol>/VENDOR.md`.

### 3. Remap all imports

**Always use `@crane/` absolute imports** for new/edited code:

```solidity
// ✓ Correct
import {SafeCast} from "@crane/contracts/external/openzeppelin-contracts/utils/math/SafeCast.sol";
import {IERC20} from "@crane/contracts/interfaces/IERC20.sol"; // when Crane-canonical

// ✗ Forbidden for new work
import {SafeCast} from "../../../dependencies/openzeppelin/contracts/utils/math/SafeCast.sol";
import {SafeCast} from "openzeppelin-contracts/contracts/utils/math/SafeCast.sol"; // bare alias dump
```

Bulk rewrite tips (from `DEDUPLICATION.md`):

- Suffix-based rewrite of path fragments (works for both `@crane/` and relative forms).
- Grep **both** `@crane/...` absolute paths **and** relative `./` / `../` forms before deleting any file.
- Grep **inside** the vendored tree for internal consumers before deleting OZ interface files.
- After large moves: `rm -rf cache out` then `forge build`.

### 4. Crane wrapper surface

Minimum for a usable port (see `DEFI_PORTING_PRD.md` A.5):

| Piece | When |
|-------|------|
| Interfaces under `contracts/interfaces/` or `protocols/.../interfaces/` | Always for consumer-facing API |
| `*Service.sol` | Always — stateless helpers for Diamond/strategy code |
| `*AwareRepo` / Facet-Target-Repo | When state lives in a Diamond |
| `*DFPkg` | When deployable as a Diamond package |
| Protocol skill under `.claude/skills/` | After port stabilizes (`writing-skills`) |

Follow `crane-architecture` + `crane-code-style` + `crane-natspec` for wrappers. Domain contracts keep upstream NatSpec; wrappers get full Crane NatSpec + tags.

### 5. Tests and verification

**Mandatory.** Load `crane-porting-verification` and implement the full gate set. A port without tests is incomplete.

### 6. Docs and skills

- Update protocol section of `docs/CODEBASE_MAP.md` (or regenerate).
- Cross-link `docs/protocols/` if applicable.
- Add/update protocol skill(s) so future agents reuse the port.

## `VENDOR.md` template

Place at `contracts/external/<name>/VENDOR.md`:

```markdown
# <name> vendor

| Item | Value |
|------|-------|
| Upstream | org/repo |
| Pin | `<git tag or commit>` |
| Solidity files (this tree) | N |
| Copy date | YYYY-MM-DD |
| License | SPDX / note clearance if BUSL |
| Import policy | Shared OZ/Solady remapped to `@crane/contracts/external/...`; unique transitives under `contracts/external/<dep>/` |

## Adaptations
- Imports rewritten from upstream remappings to `@crane/...` paths (no new Foundry alias paths).
- Exact `pragma solidity =X.Y.Z` relaxed only where required for multi-version Foundry compile (document each).
- List any intentional Crane hooks (e.g. IERC20 path).

## Inventory
Path to inventory file or bullet list of top-level modules included/excluded.
```

Reference example: `contracts/external/lido/VENDOR.md`.

## Dependency substitution map (default)

| Upstream dependency | Crane target | Notes |
|--------------------|--------------|-------|
| OZ ERC20 / Ownable / AccessControl / SafeERC20 / … | `external/openzeppelin-contracts/` (match major) | OZ semantics only |
| OZ upgradeable | `external/openzeppelin-upgradeable*` | Do not mix majors blindly |
| Solady | `external/solady/` | Expand external if symbol missing |
| Solmate | `external/solmate/` | Uni V4-style use is OK when intentional |
| Permit2 | `protocols/utils/permit2/` + Aware layer | Already ported |
| Chainlink / Pyth / RedStone | `external/` + `protocols/oracles/` | Reuse adapters |
| EVC | Euler port under `protocols/lending/euler/` | Reuse, do not re-vendor |
| forge-std | project `lib/forge-std` / external stub policy | Do not nest private forge-std |

Full program map: `DEFI_PORTING_PRD.md` Part B.

## Import & remapping rules

1. **Primary form:** `@crane/contracts/...` only for Crane work.
2. **Do not** add new Foundry remapping aliases for each ported protocol.
3. **Do not** edit `foundry.toml` / `remappings.txt` unless explicitly required and approved.
4. Existing convenience remaps (e.g. `@openzeppelin/` → external) may be used when they already point at the canonical external tree — prefer `@crane/contracts/external/...` in new code for clarity.
5. Relative imports inside a freshly vendored tree should be converted to `@crane/` during cleanup (at least for cross-package edges).

## Anti-patterns (reject these)

- New `protocols/.../dependencies/openzeppelin*` or `.../dependencies/solady*` trees.
- Replacing OZ Ownable with Crane Solady Ownable "to dedupe" (behavior change).
- Bumping OZ major as part of a port without an explicit version decision + tests.
- Inventing interface mocks for the protocol SUT when stubs/ports or forks exist.
- Porting without fork addresses, VENDOR.md, or tests.
- `new` for production Crane facets/DFPkgs in tests (use factories); protocol ports in TestBases may use `new` for the **ported protocol** only.
- Leaving dead relative imports after a move (grep both forms).

## Definition of done (port complete)

A protocol port is **done** only when all hold:

1. Domain sources under the correct `external/` and/or `protocols/` paths, pinned in `VENDOR.md`.
2. Shared deps remapped to `@crane/contracts/external/...` (no private OZ/Solady clones for new work).
3. No new git submodules; no unauthorized remapping edits.
4. Crane wrapper surface: interfaces + Service (minimum); Aware/FTR/DFPkg as designed.
5. **Verification gates from `crane-porting-verification` all green.**
6. Docs/CODEBASE_MAP updated; protocol skill added or scheduled.
7. Task/PRD section updated if part of `DEFI_PORTING_*` program.

## Key reference files

```
DEFI_PORTING_PRD.md
DEFI_PORTING_PRIORITIZATION.md
DEFI_PORTING_GAP_ANALYSIS.md
DEDUPLICATION.md
Aave_Vendored_Dependencies_Dedup_Plan.md
contracts/external/lido/VENDOR.md
contracts/StyleGuide.sol
AGENTS.md
docs/CODEBASE_MAP.md
docs/concepts/building-with-crane.md
```

## Exemplar ports (study these)

| Protocol | Domain / external | Crane wrappers |
|----------|-------------------|----------------|
| Lido | `external/lido/` + `external/aragon/` | `protocols/staking/ethereum/lido/` |
| Uniswap V2 | `external/uniswap/v2-*` | `protocols/dexes/uniswap/v2/{services,aware,stubs,test}` |
| Balancer V3 | `external/balancer/` | `protocols/dexes/balancer/v3/` + diamond routers |
| Aave v4 | under `protocols/lending/aave/v4/` (large) | Services + full test tree under `test/foundry/spec/protocols/lending/aave/v4/` |
| Aave v3.6 deps cleanup | still has legacy `dependencies/` | Migration target is external OZ — follow dedup plan |

## See also

- `skill:crane-porting-verification` — mandatory tests, fork parity, Behavior, DoD checklist
- `skill:crane-testing` — TestBase / Behavior / Handler patterns
- `skill:crane-architecture` — wrappers Facet-Target-Repo / DFPkg
- `skill:crane-code-style` — imports, headers, naming
- `skill:crane-adversarial-testing` — abuse suite for wrappers that hold value
- `skill:writing-skills` — ship a protocol skill after the port
- Agent: `crane-porter` — specialized agent identity for this work
