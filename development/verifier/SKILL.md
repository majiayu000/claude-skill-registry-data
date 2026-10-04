---
name: verifier
description: verifier. Use when you need help with verifier.
license: CC-BY-NC-SA-4.0
metadata:
  risk: unknown
  source: community
  kind: mode
  category: workflows
---

# Verifier Guide

Use this file for verifier failures, pointer-class reasoning, and constraint-aware program design.

## When to Use This File

- verifier rejects the program
- the user shares a verifier log
- loops, stack usage, packet parsing, or map value access are failing
- the user asks how to write code that the verifier will accept

## Verifier Working Style

When a verifier error appears:

1. Identify the failing pointer class:
   - packet pointer
   - map value pointer
   - stack pointer
   - nullable helper result
   - context-derived pointer
2. Reduce to the smallest bad path.
3. Add the missing proof the verifier needs.
4. Re-run with logs and inspect the exact failing register state.

Do not answer with generic folklore if the user provided a real verifier log. Explain the failing path in that log.

## Common Error Patterns

| Error | Usual Cause | Default Fix |
|-------|-------------|-------------|
| `invalid indirect read from stack` | uninitialized stack passed to helper | zero-init local buffers |
| `R0 invalid mem access 'scalar'` | nullable result used unchecked | add `if (!ptr) return ...` |
| `math between pkt pointer and unbounded register` | packet offset not proven safe | bounds-check against `data_end` |
| `back-edge from insn X to Y` | unverifiable loop | unroll or use bounded loop with constant limit |
| `register R1 type=map_value expected=fp` | wrong helper argument shape | use the helper's expected pointer type and stage through locals |
| `invalid stack type` | stack escape the verifier cannot model | simplify locals and pass stable stack addresses only |
| `too many instructions` | oversized program | split with tail calls or subprograms |

## Proofs the Verifier Usually Needs

### Packet Access

Every dereference needs a prior bound:

```c
void *data = (void *)(long)ctx->data;
void *data_end = (void *)(long)ctx->data_end;
struct ethhdr *eth = data;

if ((void *)(eth + 1) > data_end)
    return XDP_DROP;
```

### Nullable Map Lookups

```c
u64 *val = bpf_map_lookup_elem(&my_map, &key);
if (!val)
    return 0;

__sync_fetch_and_add(val, 1);
```

### Stack Initialization

```c
char buf[64] = {};
bpf_get_current_comm(buf, sizeof(buf));
```

### Bounded Loops

```c
#pragma unroll
for (int i = 0; i < 4; i++) {
    // ...
}
```

Or, on newer kernels:

```c
static long cb(u32 i, void *ctx) {
    return 0;
}

bpf_loop(128, cb, NULL, 0);
```

## Design Rules That Avoid Verifier Pain

- keep helpers close to the proof that justifies their arguments
- use local temporaries when helper argument shapes are subtle
- make bounds and NULL checks happen before branching complexity explodes
- keep loops obviously bounded
- prefer simpler control flow during early bring-up
- compile with `-g` so source lines appear in logs

## Minimal Verifier Debug Flow

```bash
mount -t bpf bpffs /sys/fs/bpf
bpftool prog load prog.bpf.o /sys/fs/bpf/test
export LIBBPF_LOG_LEVEL=debug
```

If the user has a libbpf log, explain:
- which instruction failed
- what the register type was at that point
- what proof was missing
- the smallest code change likely to satisfy the verifier

## Related Features

- `bpf_loop` reduces the need for manual unrolling on newer kernels
- tail calls help with instruction-limit pressure
- per-CPU maps often simplify shared-state proofs
- object storage maps can be easier to reason about than pointer-keyed hash tables
