---
name: ddc-code-repair
description: "Run one supplied-patch DDC code-repair attempt with fixed local checks and retained evidence."
operad_source_colours: ["State"]
operad_target_colour: "Receipt"
operad_arity: 1
operad_residual: "unknown"
families: [ddc, development]
---

# Bounded DDC code repair

AuthorityEffect: None.

Use a host-selected source manifest, writable-file list, fixed command argv and
one offline patch. OEOP owns the six declarations under
`operads/catalog/contracts/v1/ddc_code_repair_*.json`.
Adversary binds their executors through the existing typed workflow compiler and
native operad runner. This does not admit these operations for production.

| Move | Actual action |
| --- | --- |
| C | Verify hashes and capture a fresh working copy. |
| R | Run the fixed baseline checks. |
| E | Apply the patch within scope and repeat those checks. |
| I | Retain observations and notify injected immune/lineage ports. |
| M | Record a scoped outcome or typed refusal. |
| T | Emit the terminal result. |

From the repository root, execute the real offline example:

```text
python -m adversary.documentation.examples.code_repair
```

The existing native-host selection must be available. A caller's own request
uses `python -m adversary.entrypoints.code_repair_cli --help`.
Run output stays outside the source tree, is never overwritten, and retains
the patch, request, working copy, observations, lineage and native receipt.

Commands are trusted host inputs. A working copy is not an OS security sandbox.
The original source is not patched, and no commit or push is performed. No
provider client or publisher is configured. Checks are not network-sandboxed;
the host must choose offline commands. Passing fixed checks is not a mathematical score,
proof, immune admission or authority promotion. An unavailable executor refuses
before any operation runs. Learned observations never activate detectors.
