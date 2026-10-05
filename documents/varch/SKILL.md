---
name: varch
description: Decompose an IP requirement into submodules, define interfaces, and generate an architecture document plus per-module requirement files and a top-level skeleton
allowed-tools: Read, Write, Glob, Grep
---

# Verilog Architect

## Overview

This guide defines the workflow for decomposing a top-level IP requirement into submodules, defining their interfaces, and capturing the result in an architecture document that drives the per-submodule requirement files (ready for `vdesign`) and the top-level skeleton.

The input is a top-level IP requirement `.md` file. The outputs are:

1. An architecture document `./ddoc/<ip>_arch.md` — the canonical structural source (decomposition, block diagram, interface table, parameter propagation map). This is the one file the user edits to change the architecture and re-run.
2. One requirement `.md` file per submodule in `./ddoc/`, derived from the architecture document
3. A top-level integration skeleton in `./rtl/`, derived from the architecture document

`varch` is **idempotent and architecture-document-driven**: on a re-run, `./ddoc/<ip>_arch.md` is the source of truth and the requirement files and skeleton are regenerated from it (see Step 6). On the first run the document does not exist yet, so Steps 1–2 create it.

> **Re-run:** if `./ddoc/<ip>_arch.md` already exists, it is authoritative. Read it instead of re-deriving the decomposition from scratch, apply whatever the user changed in it (or asks for), then go to Step 6 (regenerate), which ends in the Step 5 self-check. Steps 1–4 below describe the first run that builds the document.

## Step 1 - Analyze Requirements and Propose Decomposition

Read the top-level IP requirement `.md` file and extract the design intent.

Before proposing a new decomposition, check `./lib` for any existing library modules that already cover part of the required functionality. Read each candidate's `<module>.md` documentation to understand its interface and behaviour — the docs follow the `ModuleDocContract` and are usable without reading the RTL, so there is no need to run `vexplain`. Only fall back to reading the source (or `vexplain`) if a lib module's doc is missing or does not state its ports/parameters. Reuse such modules rather than redesigning.

Based on the requirements, propose a module decomposition. The proposal must include:

- A list of submodules, each with:
  - Name
  - Single-sentence responsibility
  - Key inputs and outputs
- A block diagram showing submodule connections, drawn in mermaid format
- Justification for any module boundary decision that is non-obvious

If an existing library module covers a required function, include it in the block diagram as-is. A reused library module gets **no `_req.md`** (it is already designed and documented) **but is still instantiated in the skeleton** and appears in the interface table like any other submodule. `vdesign`/`vfill` simply skip it — there is no req file to drive them.

## Step 2 - Define Interfaces

For each connection between submodules shown in the block diagram, define the interface in detail:

- Net name (following the inter-module net convention in `CodingStyle.md §3.3`: `<master>2<slave>_<bus>`, or the simplified `<master>_<bus>`)
- The master port (`m_*`) and slave port (`s_*`) it connects, per module
- Signal width and type
- Protocol or handshake description if applicable

Present the interface definitions as a table for each inter-module connection.

### Write the architecture document

Persist Steps 1–2 to `./ddoc/<ip>_arch.md`. This is the canonical structural source — keep it to structure and connectivity; per-module detail belongs in the requirement files, not here. It must contain:

- IP name and a one- to two-line intent
- Top-level port table (the source for the skeleton header)
- IP parameter table and a **propagation map**: which submodules receive which parameters, including `RS_LV` for every clocked module
- Submodule table: `name | one-line responsibility | type (new / lib-reuse) | source`. The `source` column applies to `lib-reuse` rows only — record the library module's path (e.g. `lib/foo_fifo/foo_fifo.v`) so re-runs and the skeleton instantiation resolve to its fixed interface without re-searching.
- Block diagram (mermaid)
- Inter-module interface table: `net (§3.3) | master.port | slave.port | width | protocol`
- Justification for any non-obvious module-boundary decision

Do **not** put full functional descriptions, full per-module port docs, algorithms, or integration/synthesis detail here — those live in the requirement files (`vdesign`'s input) and downstream docs, and duplicating them invites drift.

## Step 3 - Generate Submodule Requirement Files

For each new submodule (excluding reused library modules), generate a requirement `.md` file in the `./ddoc/` folder.

Output file rules:

- Use the submodule name with a `_req` suffix as the file name
- Use the `.md` extension

Example:

- submodule `foo_ctrl` → `./ddoc/foo_ctrl_req.md`

### Required Content for Each Requirement File

Each requirement file has two parts, separated by the marker line `<!-- functional-spec: hand-owned below this line -->`. This split is what makes re-runs safe (Step 6).

**Generated structural section** (above the marker) — derived from the architecture document and regenerated on every re-run:

- Module overview and responsibility
- Parameter descriptions, if applicable
- Input/Output port descriptions with signal names and widths from the interface table in the architecture document
- Interface protocol description for each port, if applicable

**Hand-owned functional section** (below the marker) — `## Functional Description`: what the module must do, not how. `varch` seeds it on first creation, then **preserves it verbatim** across re-runs.

The requirement file is the direct input to `vdesign`. It must be self-contained and unambiguous.

## Step 4 - Generate Top-Level Integration Skeleton

Create a top-level Verilog skeleton file in the `./rtl/` folder.

Output file rules:

- Use the IP name as the file name with `_top` suffix
- Use the `.v` extension

Example:

- IP `foo` → `./rtl/foo_top.v`

### Skeleton Structure

The skeleton must include:

- Module declaration with the IP-level ports from the requirement
- `wire` declarations for all inter-module interfaces from the interface table in the architecture document
- One instantiation stub per submodule with port connections wired up — **both new submodules and reused `lib` modules.** A reused module is a real part of the IP hierarchy and must appear in the skeleton.
- `//@` comments on any connection or signal that requires special attention during integration

No logic implementation — only port declarations, wire declarations, and instantiation stubs.

**Reused library modules.** The port names, widths, and parameters of a reused `lib` module are **fixed by the existing library module** — take them from its `<module>.md` documentation (read in Step 1; fall back to the source only if the doc lacks them), never invent or rename them. Where an IP net does not line up with the library port's name or width, wire it through and mark the adaptation with a `//@` note rather than renaming the library port.

Bind only the parameters the library module actually declares. A reused module may not expose `RS_LV` (or may use a different reset convention) — do not add parameters to its instantiation that it does not define. Note any reset-convention mismatch with a `//@` comment.

Example skeleton structure:

```verilog
module foo_top #(
    parameter DATA_W = 8,
    parameter RS_LV  = 0        // reset active level (last param), passed down
) (
    input  wire              clk,
    input  wire              rst_n,
    input  wire [DATA_W-1:0] s_data,
    input  wire              s_valid,
    output wire [DATA_W-1:0] m_data,
    output wire              m_valid
);

//==============================================================================
// Inter-module interfaces
//==============================================================================

wire [DATA_W-1:0] ctl2prc_data;
wire              ctl2prc_valid;

//==============================================================================
// Submodule Instantiations
//==============================================================================

foo_ctrl #(
    .DATA_W (DATA_W),
    .RS_LV  (RS_LV)
) u_foo_ctrl (
    .clk      (clk),
    .rst_n    (rst_n),
    .s_data   (s_data),
    .s_valid  (s_valid),
    .m_data   (ctl2prc_data),
    .m_valid  (ctl2prc_valid)
);

foo_proc #(
    .DATA_W (DATA_W),
    .RS_LV  (RS_LV)
) u_foo_proc (
    .clk      (clk),
    .rst_n    (rst_n),
    .s_data   (ctl2prc_data),
    .s_valid  (ctl2prc_valid),
    .m_data   (m_data),
    .m_valid  (m_valid)
);

endmodule
```

## Step 5 - Self-check the decomposition

Before finishing, verify the three outputs agree with each other. This is a
structural gate: every interface must trace cleanly from the architecture
document's interface table, through the skeleton wiring, to a port on both
endpoint modules. Walk each row of that interface table and confirm:

| Check | Pass condition |
|-------|----------------|
| Net exists | The interface appears as a `wire` in `<ip>_top.v`, named per §3.3 (`<master>2<slave>_<bus>` or `<master>_<bus>`). |
| Two endpoints | The net is driven by exactly one master port (`m_*`) and consumed by at least one slave port (`s_*`). No net is driven by two masters or left unconnected. |
| Ports match | Both endpoint ports exist with the same width and the direction implied by the table — in the `_req.md` for a new submodule, or in the `<module>.md` documentation for a reused `lib` module (which has no `_req.md`). |
| Widths agree | The wire width, both port widths, and the interface-table width are identical (or resolve to the same parameter expression). |

Then check coverage in both directions:

| Check | Pass condition |
|-------|----------------|
| Every submodule placed | Each block in the decomposition is either a new submodule with a `_req.md` file, or a reused `lib` module — and each is instantiated in `<ip>_top.v`. |
| Every IP port wired | Each top-level port from the IP requirement appears in the skeleton header and is connected to at least one submodule. |
| Params propagate | Each IP-level parameter the submodules depend on (including `RS_LV` for clocked modules) is declared on `<ip>_top.v` and passed down by name to every submodule that declares it. A reused `lib` module that does not expose a given parameter is not a failure — bind only what it declares. |

If any check fails, fix the offending artifact and re-run the check — do not leave
the skeleton, the requirement files, and the interface table in disagreement. The
skeleton, the `_req.md` files, and the architecture document's interface table are
the contract `vdesign` and `vfill` build against; a mismatch here surfaces as a
wiring bug three phases later.

## Step 6 - Regenerate on re-run

This step runs whenever `./ddoc/<ip>_arch.md` already exists and the user has edited it (or asked for an architecture change). The architecture document is the source; the skeleton and requirement files are derived from it. Regenerate only what changed.

**Skeleton — always regenerated.** `<ip>_top.v` is purely structural (no hand-written logic), so rebuild it in full from the architecture document. Overwriting it is safe **as long as it is still a pure skeleton** — but it is not always so: during IP integration (Phase 3) its `//@` notes get resolved and connections may be hand-wired. A full rebuild discards those edits. Before regenerating, check whether `<ip>_top.v` has diverged from a pure skeleton (resolved `//@` notes, added logic); if it has, **warn the user and confirm** before overwriting. The safe path is to re-run `varch` before integration begins; after that, architecture changes must be reconciled into `<ip>_top.v` by hand.

**Requirement files — regenerate only the change set.** Touching a `_req.md` invalidates its downstream proposal/backbone, so do not rewrite files that did not change. A submodule is **in the change set** when, compared against what its current `_req.md` reflects, any of these differ:

- its row in the submodule table (responsibility, type), **or**
- **any interface-table row where it is an endpoint** (master *or* slave), **or**
- any parameter in its propagation map.

The second condition is the one to get right: if one net's width changes, **both** endpoint modules are in the change set even though only one table row was edited. Compute the change set from the connectivity graph, never from "which line the user typed" — under-regenerating leaves the other endpoint stale, which is exactly the drift Step 5 exists to prevent.

To detect change without a state file: for each submodule, derive its structural section from the current architecture document and compare it (whitespace-insensitive) against the structural section in the existing `_req.md`. Differ → in the change set.

If an existing `_req.md` has **no marker line** (e.g. it predates this convention or was hand-created), do not regenerate it — treat the whole file as hand-owned and leave it untouched, then flag it so the user can add the marker (or split it) manually. Never clobber a marker-less file.

Then, per submodule:

| Case | Action |
|------|--------|
| In change set, `_req.md` exists | Regenerate the structural section (above the marker); **preserve the `## Functional Description` section verbatim**. |
| New submodule (no `_req.md`) | Create the file; seed both sections. |
| Removed from the architecture document | **Flag the orphaned `_req.md` and stop for confirmation — do not auto-delete.** Its proposal/backbone and other downstream outputs may depend on it. |
| Switched `new` → `lib-reuse` | Still in the architecture document but no longer owns a `_req.md` — treat as removed: flag the now-orphaned `_req.md` for confirmation, do not auto-delete. |
| Not in change set | Leave the file untouched. |

**Report the change set explicitly** so the user has the downstream re-run list without diffing by hand, e.g.:

```text
regenerated: ctl, prc      (need to re-run vdesign/vfill)
unchanged:   arb, fifo
orphaned:    legacy_mux    (confirm before deleting)
```

Then run the Step 5 self-check as the regeneration gate.
