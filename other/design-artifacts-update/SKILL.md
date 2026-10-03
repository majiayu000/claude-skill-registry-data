---
name: design-artifacts-update
description: Update or create design artifacts for a certus-server-yaml profile
argument-hint: "[profile-name]"
---

Create or update architectural design documents for a specific certus-server-yaml profile. Design files are stored per-profile at `/home/dwaddington/certus/design/profiles/<profile-name>/`.

## Interactive Configuration

Before starting, ask the user which **profile** to generate design artifacts for.

Available profiles can be listed from `apps/certus-server-yaml/profiles/` (e.g., `full`, `full-p2p`, `full-remote`, `full-fs-block`, `full-kernel-block`, `minimal`).

If the user provided a profile name as an argument, use that. Otherwise, present the available profiles and ask.

## Design Artifacts

Each profile directory contains markdown documents and their corresponding visual diagrams:

| File | Purpose |
|------|---------|
| `SYSTEM.md` | Master architecture reference — components, interfaces, data flows, concurrency model, design decisions |
| `certus-server-deployment.md` | Component topology diagram — receptacles, wiring, initialization order |
| `certus-server-deployment.puml` | PlantUML source for the deployment diagram |
| `certus-server-deployment.svg` | Rendered SVG of the deployment diagram |
| `design-spec-put-flow.md` | Populate/write data path (GPU → DRAM → SSD) |
| `design-spec-put-flow.svg` | Flow diagram for the put path |
| `design-spec-hit-flow.md` | Lookup/read data paths (warm: DRAM → GPU, cold: SSD → DRAM → GPU) |
| `design-spec-hit-flow.svg` | Flow diagram for the hit path |

## Workflow

### 1. Read the Profile YAML

Read `apps/certus-server-yaml/profiles/<profile-name>.yaml` to understand which components are composed for this profile — what dispatcher variant is used, which block device backend, what optional features are enabled.

### 2. Gather Current Code State

Read the following source files to establish ground truth:

**Interface definitions** (canonical method signatures):
- `components/interfaces/src/idispatcher.rs` — `IDispatcher` trait
- `components/interfaces/src/idispatch_map.rs` — `IDispatchMap` trait
- `components/interfaces/src/imemory_tier.rs` — `IMemoryTier` trait
- `components/interfaces/src/iblock_device.rs` — `IBlockDevice` trait
- `components/interfaces/src/iextent_manager.rs` — `IExtentManager` trait
- `components/interfaces/src/igpu_services.rs` — `IGpuServices` trait
- `components/interfaces/src/ispdk_env.rs` — `ISPDKEnv` trait
- `components/interfaces/src/lib.rs` — Re-exports and shared types

**Component implementations** relevant to the profile (fields, receptacles, internal structure):
- `components/dispatcher/src/lib.rs` — `define_component!` block and core logic
- `components/dispatcher-p2p/src/lib.rs` — P2P variant (if profile uses it)
- `components/dispatch-map/src/lib.rs`
- `components/memory-tier/src/lib.rs`
- `components/block-device-spdk-nvme/src/lib.rs` — (if profile uses SPDK NVMe)
- `components/block-device-filesys/src/lib.rs` — (if profile uses filesystem backend)
- `components/block-device-kernel/src/lib.rs` — (if profile uses kernel backend)
- `components/extent-manager/src/lib.rs`
- `components/gpu-services/src/lib.rs`
- `components/spdk-env/src/lib.rs`
- `components/eviction-policy-lru/src/lib.rs`
- `components/remote-lookup/src/lib.rs`

**Server / integration layer**:
- `apps/certus-server/src/service.rs` — gRPC service (RPCs, IPC handle management)
- `apps/certus-server-yaml/src/main.rs` — YAML-configured server entry point

**Workspace structure**:
- Root `Cargo.toml` — workspace members and default-members

### 3. Check for Existing Design Files

If `/home/dwaddington/certus/design/profiles/<profile-name>/` already exists, read the existing `.md` files and update them in place (preserving structure and style). If the directory does not exist, create it and generate the four design files from scratch based on the profile's component composition.

### 4. Identify Drift (update mode)

When updating existing files, compare the design documents against the code and note discrepancies:

- **Interface changes**: Methods added, removed, or renamed; signature changes (parameters, return types); new error variants
- **Component changes**: New/removed fields or receptacles in `define_component!` blocks; new components added to the workspace
- **Data flow changes**: Steps in the put/get paths that no longer match the implementation (e.g., new intermediate steps, removed steps, changed ordering)
- **Topology changes**: New components, changed wiring, new background threads/workers
- **Build/feature changes**: New cargo features, profiles, or conditional compilation gates

### 5. Write or Update Documents and Diagrams

Write to `/home/dwaddington/certus/design/profiles/<profile-name>/`:

**Markdown documents:**
- `SYSTEM.md` — Focus on components and data flows **specific to this profile**. Document which dispatcher variant, block device backend, and optional features are active.
- `certus-server-deployment.md` — Component topology for this profile's composition.
- `design-spec-put-flow.md` — Populate/write path as it works in this profile.
- `design-spec-hit-flow.md` — Lookup/read paths as they work in this profile.

**Diagrams (update to match any topology or flow changes):**
- `certus-server-deployment.puml` — PlantUML source reflecting the profile's component topology. Use color to distinguish component categories (see style guide below). Update component boxes, receptacle wiring, and background workers to match code.
- `certus-server-deployment.svg` — Render from `.puml` (see rendering instructions below).
- `design-spec-put-flow.svg` — Update if the put-flow steps changed.
- `design-spec-hit-flow.svg` — Update if the hit-flow steps changed.

**PlantUML rendering:**
```bash
java -jar ~/.vscode-server/data/User/globalStorage/justuskarlsson.plan-uml/plantuml-1.2025.10.jar \
    -tsvg <file>.puml -o <output-dir>/
```
The output filename is derived from the `@startuml <name>` identifier. Either use `@startuml` without a name (output matches input filename) or rename the output file afterward.

**PlantUML style guide for deployment diagrams:**

Use UML deployment diagram elements with standard skinparam:
```plantuml
@startuml
skinparam defaultTextAlignment center
skinparam padding 3
skinparam nodesep 25
skinparam ranksep 25
```

**UML element types** — use the correct shape for each concept:
- `node` — Physical/logical hosts (Client Host, Server Host, certus-server process). Renders as a 3D cube.
- `component` — Software components (DispatcherComponent, MemoryTierComponent, etc.). Renders as a rectangle with tabs.
- `database` — Storage (GPU Memory, NVMe devices). Renders as a cylinder.
- `cloud` — External/remote systems (Peer Certus Nodes).

**Color coding** (apply with `#Color` suffix for profile-specific components):
- **Remote/network** components: `#LightCoral`

**Example structure** (matches the `full` profile pattern):
```plantuml
node "Server Host" {
    node "certus-server (Rust / tokio)" {
        component "DispatcherComponent <<IDispatcher>>" as dispatcher {
            component "BackgroundWriter | BackgroundEvictor\nPipelineRing | warm_stream" as disp_bg
            component "DataDrive [0..N]\n(BlockDeviceSpdkNvme + ExtentManager)" as data_drive
        }
        component "DispatchMapComponent\n<<IDispatchMap>>" as dispatch_map
        component "RemoteLookupComponent\n<<IRemoteLookup>>" as remote_lookup #LightCoral
    }
    database "NVMe (data) [0..N]" as nvme_data
}
cloud "Peer Nodes" as peers
```

**PlantUML pitfalls to avoid:**
- Never nest `[]` inside component names — e.g., `[DataDrive[0..N]]` is invalid. Use `[DataDrive 0..N]` instead.
- Always verify the `.puml` renders without errors before reporting success.

Preserve existing writing style when updating. When creating from scratch, use the `full` profile's documents as a style reference.

**Do not** add speculative content or document unfinished/experimental features. Only document what the code currently implements for the selected profile.

### 6. Report

After completing, print a summary:

```
Design Artifacts for profile '<profile-name>':
──────────────────────────────────────────────
Directory: certus/design/profiles/<profile-name>/

SYSTEM.md:
  - [created | updated: <list of changes>]

certus-server-deployment.md:
  - [created | updated: <list of changes>]

design-spec-put-flow.md:
  - [created | updated: <list of changes>]

design-spec-hit-flow.md:
  - [created | updated: <list of changes>]
```

## Important Notes

- The design directory is at `/home/dwaddington/certus/design/`, NOT inside the main repo. It is a separate working directory.
- Each profile gets its own subdirectory under `certus/design/profiles/`.
- Preserve the existing writing style — these are human-authored design documents, not generated API docs.
- When in doubt about intent (e.g., a method exists but is clearly a placeholder/TODO), keep the existing design text and note the discrepancy in the report rather than documenting placeholder code.
- Visual artifacts (`.svg`, `.puml`) live alongside the `.md` files in each profile directory and must be updated when topology or flows change.
- If a design document section describes a future/planned feature that isn't implemented yet, leave it as-is (it represents design intent).
- Profile-specific details (e.g., P2P ring in `full-p2p`, filesystem backend in `full-fs-block`) should be prominent in that profile's docs — don't include irrelevant components.
