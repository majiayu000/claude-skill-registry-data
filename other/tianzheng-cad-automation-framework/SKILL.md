---
name: tianzheng-cad-automation-framework
description: Apply the documented Tianzheng/AutoCAD full-drawing-set automation framework to design controller contracts, native-object gates, and acceptance evidence. Use for architecture and workflow design rather than as a plug-and-play CAD executor.
---

# Tianzheng CAD automation framework

Use this framework to connect a planning controller to a local Tianzheng/AutoCAD adapter while keeping drawings editable as native Tianzheng objects. It describes architecture, workflow stages, request contracts, and acceptance gates. This framework directory is a method guide; the companion `tianzheng-batch-polyline-dimension/runtime` in the same release contains native annotation and control source. No author production drawings, company identifiers or live project state are included. Read the companion migration guide for implementation and runtime boundaries.

## Read the relevant layer

- Start with [README.md](README.md) for scope and non-goals.
- For the full drawing-set flow, read [docs/framework.md](docs/framework.md).
- For what is currently automated versus only designed, read [docs/capabilities.md](docs/capabilities.md).
- Before claiming delivery, read [docs/acceptance.md](docs/acceptance.md).
- To implement controller/adapter messaging, read [docs/automation-contracts.md](docs/automation-contracts.md).
- For current native topology, display/collision, plot, checkpoint and window-cleanup practices, read [docs/recent-practices.md](docs/recent-practices.md). These are scoped methods, not a claim of arbitrary-DWG acceptance; execution code is in the companion runtime, not duplicated here.

## Operating rules

1. Treat a native command return as execution evidence, not delivery. Require object audit, visual review, and save-close-reopen evidence.
2. Protect the source drawing. Write to an isolated working drawing unless in-place mutation is explicitly authorized.
3. Prefer semantic discovery and native commands over fixed handles, coordinates, or blind GUI replay.
4. Adapt every contract to the installed Tianzheng/AutoCAD release, company review process, and security policy before production use.
5. Do not convert a failed native operation into text or image-only output while claiming native completion.
6. Keep run directories, drawings, screenshots, logs, accounts, and identifiers out of this packaged framework.
