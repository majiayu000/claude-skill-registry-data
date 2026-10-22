---
name: hopper-debugger
description: >-
  Reverse-engineers and debugs macOS and iOS binaries with Hopper Disassembler and LLDB: ObjC/Swift
  symbols, dyld loading, framework internals, and crash investigation from disassembly. Use when
  private API behavior or a runtime crash needs to be understood at the binary level.
source: "https://github.com/steipete/agent-scripts"
attribution: "steipete/agent-scripts by Peter Steinberger"
version: "1.0.0"
platform: macos
license: MIT
---

# Hopper Debugger

> **Attribution:** Sourced from [steipete/agent-scripts](https://github.com/steipete/agent-scripts) by [Peter Steinberger](https://github.com/steipete).

Goal: use Hopper through `mcporter` as a queryable disassembler, then combine the result with local source, LLDB, logs, and focused repros.

## When to Use

- Reverse-engineering macOS/iOS binaries to understand private API behavior
- Debugging ObjC/Swift symbol resolution, dyld loading, or framework internals
- Investigating runtime crashes by inspecting disassembly and pseudo-code
- Querying Apple framework internals via Hopper + LLDB

## Quick Start

Validate the MCP server:

```bash
MCPORTER_LIST_TIMEOUT=15000 timeout 20 mcporter list hopper --brief
```

List open Hopper documents:

```bash
MCPORTER_CALL_TIMEOUT=20000 timeout 30 mcporter call hopper.list_documents --output json
```

If no document is open, open the binary/framework in Hopper first:

```bash
open -a "Hopper Disassembler" /path/to/Binary
```

Hopper may show a first-open/import dialog. Let the user click the confirmation button, then retry the MCP call. Avoid parallel Hopper MCP calls during import.

## Apple Frameworks

Prefer already extracted dyld-cache framework binaries when present:

```bash
/tmp/dsc-appkit/System/Library/Frameworks/AppKit.framework/Versions/C/AppKit
/tmp/dsc-appkit/System/Library/Frameworks/SwiftUI.framework/Versions/A/SwiftUI
```

## Query Workflow

1. Start from the local source path or runtime symbol you are trying to explain.
2. Search names/procedures/strings:

```bash
mcporter call hopper.search_procedures pattern='NSStatusBar' --output json
mcporter call hopper.search_name pattern='NSStatusBarButtonCell' --output json
mcporter call hopper.search_strings pattern='NSStatusItem' --output json
```

3. Inspect one small target at a time:

```bash
mcporter call hopper.procedure_info procedure='<symbol>' --output json
mcporter call hopper.procedure_assembly procedure='<symbol>' --output json
mcporter call hopper.procedure_pseudo_code procedure='<symbol>' --output json
mcporter call hopper.procedure_callers procedure='<symbol>' --output json
mcporter call hopper.procedure_callees procedure='<symbol>' --output json
mcporter call hopper.xrefs address=0x12345678 --output json
```

4. Summarize the relevant control flow; do not paste large decompilations.
5. Validate the hypothesis with LLDB/logging/repro before editing app code.

## Failure Handling

- Wrap Hopper calls with `timeout`; a modal/import or closed document can leave the transport stuck.
- Do not send concurrent Hopper MCP requests during import.
- If calls report `Connection closed`, check for a Hopper modal, then retry.
- If Hopper crashes, reopen a single document, wait for import/analysis, and re-run `list_documents`.
- If mcporter is wedged:

```bash
pgrep -af 'mcporter|HopperMCPServer|Hopper Disassembler'
mcporter daemon stop
mcporter daemon start
```
