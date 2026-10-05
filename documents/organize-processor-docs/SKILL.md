---
name: organize-processor-docs
license: MulanPSL-2.0
description: Establish, author, restructure, or audit human-first processor Architecture, Design, Research, Review, and Verification documentation. Use for progressive documentation scaffolding, authority maps, reading paths, document-type content contracts, length-budgeted splitting, or maintainability reviews. Do not use as a substitute for cycle-accurate microarchitecture analysis or RTL implementation.
metadata:
  short-description: Organize concise processor documentation
---

# Organize Processor Docs

Build a directly editable Markdown document network that a processor designer can read without Harness state, a generated renderer, or a second processor model.

## Authority

1. Read the project `AGENTS.md` first.
2. Treat explicit user decisions and the current Git authorities as authoritative. Treat a later user statement as change intent unless the user clearly supersedes an existing fact.
3. For a new project without an established mapping, keep the current document network under one project-root `doc/`, matching `bootstrap-processor-project`. Use one current `doc/Architecture/`, one current `doc/Design/`, and one current `doc/Verification/` when those domains contain real material. Use `doc/Research/` only when project-maintained research exists. An existing project's approved mapping takes precedence. Git keeps history. Research, Review, and Finding remain evidence rather than processor authority.
4. Give each normative fact one owning document. Summaries link to the owner and add no new normative detail.
5. Keep Research, reference implementations, current RTL, current proposed documents, and new recommendations distinct.
6. Do not introduce a document manifest, processor schema, renderer-owned truth, backup tree, or document workflow state.
7. Do not create empty directories, empty topic files, or speculative placeholders.
8. Explain every Chisel-facing interface in `Scala declaration -> semantics` order. Show the minimal Scala structure first, then explain fields in declaration order.
9. Outside interface declarations, use Scala only when prose, a table, or a diagram cannot express the required hardware structure precisely. Keep only the minimal decisive fragment.
10. Keep a same-stem editable source beside every explanatory raster diagram and update both in the same candidate change. Evidence captures such as waveforms and tool screenshots do not require an editable diagram source; bind them to the input commit, run or method, and evidence location.
11. Use the physical module view in `doc/Design/` as the main directory axis. Align this view as closely as possible with stable Chisel or RTL instance hierarchy and responsibility boundaries. Keep Protocols, Lifecycles, ADRs, and Verification as orthogonal views linked to that axis.

When detailed processor semantics are being designed or reviewed, also use `design-chisel-processor`. This skill owns information architecture and writing constraints; `design-chisel-processor` owns cycle-accurate correctness.

All `doc/` paths in this skill and its references describe the default layout. For an established custom layout, resolve them through the project's mapping, including domain entries and the overall reading entry. Preserve that mapping, its authority files, and its local constraints. Do not silently rewrite `AGENTS.md` or create a parallel `doc/` tree. A migration requires authorization and coordinated updates to the mapping, documents, and links.

## Select a mode

### Bootstrap

Use when a project lacks a clear document framework or when existing material must be organized. Read [references/bootstrap.md](references/bootstrap.md).

### Author

Use when creating or revising a document within an approved framework.

1. For Architecture goals and processor properties, read [references/architecture.md](references/architecture.md).
2. For Design entry, overview, topology, subsystem, or module documents, read [references/design.md](references/design.md).
3. For cross-module Protocol or Lifecycle documents, read [references/protocol-lifecycle.md](references/protocol-lifecycle.md).
4. For ADR documents, read [references/adr.md](references/adr.md).
5. For Verification documents, read [references/verification.md](references/verification.md).
6. For Research, Review, Finding, or Diagnosis documents, read [references/research-review.md](references/research-review.md).

Read only the references required for the current document types.

### Maintain

Use when auditing, splitting, merging, relocating, or pruning existing documents. Read [references/maintenance.md](references/maintenance.md) plus the references for every affected document type.

## Common workflow

1. Record the exact input commit or working-tree baseline and read the relevant authorities and evidence.
2. Identify the reader question, owning fact, and shortest valid reading path.
3. Preserve user terminology and topology unless the user approves a change.
4. Propose authority or topology changes with affected paths before editing.
5. Materialize approved work as readable Markdown and update entry maps and backlinks in the same candidate.
6. Run deterministic checks and semantic review.
7. Report changed paths, responsibility or reading-path changes, validation, and unresolved user decisions.

## Provisional length budgets

Count `effectiveChars` as non-whitespace Unicode characters and `nonBlankLines` as lines containing non-whitespace content. Count prose, tables, code blocks, links, and embedded examples. Store raw logs, full source listings, and bulk research elsewhere.

| Document kind | Target `effectiveChars` | Target `nonBlankLines` | Provisional hard `effectiveChars` | Provisional hard `nonBlankLines` |
|---|---:|---:|---:|---:|
| Entry `README.md` | 2500 | 60 | 4000 | 100 |
| Architecture topic, Design principles, Design overview | 6000 | 140 | 10000 | 200 |
| Module, Protocol, Lifecycle | 8000 | 180 | 12000 | 250 |
| ADR | 2500 | 60 | 4000 | 100 |
| Research or Review | 6000 | 150 | 10000 | 220 |
| Finding | 2500 | 60 | 4000 | 100 |
| Verification specification | 6000 | 150 | 10000 | 220 |

These budgets are a writing strategy pending validation against real processor projects. Exceeding a target produces a warning and requires a concision review. Provisional hard-limit enforcement is configurable; use blocking enforcement only when the project or evaluation protocol explicitly selects it. Reduce duplication and incidental detail before splitting. Split only at a stable responsibility, ownership, protocol, lifecycle, or independent reading boundary. Never create `Part1`, `Part2`, or size-only fragments. Preserve necessary field tables, pipeline tables, state machines, and assertions when a justified document remains above a provisional threshold.

## Human-first acceptance

1. A human can understand every document without reading machine state or generated schemas.
2. Every document opens with its responsibility, scope, and owned facts in natural language.
3. `doc/README.md` links directly to every present domain entry.
4. Any Architecture property is reachable from `doc/Architecture/README.md` within two document links.
5. Any module, Protocol, or Lifecycle is reachable from `doc/Design/README.md` within two document links.
6. The Design module view accounts for every stable implemented module responsibility and records justified differences from the Chisel or RTL instance hierarchy.
7. An implemented Design document links its relevant Source and Test locations without copying source bodies.
8. Verification material links to the Architecture property or Design invariant it checks.
9. Every explanatory raster diagram retains a same-stem editable source. Evidence captures identify their input commit, run or method, and evidence location.
10. Removing `.assistant/` leaves the formal documentation complete and readable.
11. Direct user edits remain first-class input and are not overwritten from another representation.

Use [references/maintenance.md](references/maintenance.md) for deterministic commands, semantic audit, and change-report fields.
