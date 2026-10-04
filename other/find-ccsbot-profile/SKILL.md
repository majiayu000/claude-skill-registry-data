---
name: find-CCSBot_Profile
description: |
  Locate CCSBot::Profile in CS2 server.dll / libserver.so via IDA Pro MCP and emit a fresh, minimal-unique
  signature or offset for the local gamedata entry "CCSBot::Profile" (symbol CCSBot_Profile). This is a STRUCT MEMBER OFFSET (schema netvar), not a function. Resolve the
  CCSBot class layout via the schema/network system; the member must satisfy
  natural alignment. Cross-check with functions that dereference the member.
  Do not switch output schema: emit the structmember fields below even if the
  class turns out to be polymorphic - a func_*/vfunc_* payload for this symbol
  is rejected by canonical_symbol_yaml_bytes.
  Trigger: CCSBot_Profile, CCSBot::Profile
disable-model-invocation: true
---

# Find CCSBot_Profile

Target: `CCSBot::Profile` (structmember) in the CS2 server module.

> Do NOT anchor on raw byte patterns from older releases - they shift. Use anchors only to *locate*
> the function, then generate a fresh minimal-unique function-head signature with relocated bytes
> wildcarded. Produce ONLY the output file(s) listed in this skill's expected outputs, for the binary
> loaded in THIS session (one platform per run). NEVER open or analyze the other platform's binary.

## Method

This is a STRUCT MEMBER OFFSET (schema netvar), not a function. Resolve the
CCSBot class layout via the schema/network system; the member must satisfy
natural alignment. Cross-check with functions that dereference the member.
Do not switch output schema: emit the structmember fields below even if the
class turns out to be polymorphic - a func_*/vfunc_* payload for this symbol
is rejected by canonical_symbol_yaml_bytes.

## Mandatory self-check before emitting

The pipeline re-reads the bytes at your `func_va` and deterministically regenerates `func_sig` from
them - if your `func_sig` does not match those bytes EXACTLY (with `??` matching anything), the run
aborts. Therefore:

1. After picking the function, read the actual bytes at `func_va` via the IDA MCP.
2. Derive `func_sig` FROM those bytes: keep stable opcode bytes literally, wildcard relocated or
   variable operands as `??`.
3. `func_sig` MUST start at `func_va` (the true function head).
4. Only then write the YAML. A mismatch is always a bug in YOUR output, never in the pipeline.

## Output schema (STRICT)

Write the YAML file `<symbol>.{platform}.yaml` with EXACTLY these fields:
```yaml
struct_name: CCSBot
member_name: m_profile
offset: "<hex byte offset as string>"
size: <member size in bytes, decimal>
offset_sig: "<short byte pattern of an instruction touching the offset>"
```
NEVER include func_* or vfunc_* fields.

## Verification

1. Decompile the candidate and confirm the behavior matches the purpose above (not a caller or callee).
2. Confirm uniqueness: the generated pattern must match exactly one location in the loaded binary.
3. If a candidate cannot be confirmed, report the shortlist instead of guessing - a skipped symbol is
   safer than a wrong signature.
