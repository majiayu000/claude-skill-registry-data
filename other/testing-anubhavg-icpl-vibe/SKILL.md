---
name: testing
description: testing. Use when you need help with testing.
license: CC-BY-NC-SA-4.0
metadata:
  risk: unknown
  source: community
  kind: mode
  category: workflows
---

# Cross-Kernel Testing

Use this file for testing whether an eBPF object loads and attaches across multiple kernel versions.

## When to Use This File

- validating kernel compatibility in CI
- checking whether a compiled object loads on older and newer kernels
- reproducing "works on my kernel only" issues
- testing feature fallback decisions against a kernel matrix

## Recommended Approach

For CI-based cross-kernel loading tests, use lightweight VMs rather than trying to swap kernels in-place on the CI runner.

The most practical pattern here is:
- use `cilium/little-vm-helper` (LVH) to boot a lightweight VM per kernel under test
- choose a prebuilt LVH image variant such as `kind`
- mount the repository or build artifacts into the guest
- run `bpftool prog load` or the userspace loader inside that guest
- treat load success or verifier failure as the compatibility signal

This is a good fit for GitHub Actions.

## Why This Pattern Works

The host runner kernel does not change during CI, so testing against multiple kernels needs virtualization. LVH gives a lightweight way to boot kernel-specific guests and run your load/attach checks inside them.

Use it when the question is:
- "does this object load on kernel X, Y, and Z?"
- "did my new helper/map/hook choice narrow compatibility?"
- "which kernel is the first one where this object stops loading?"

## Key Building Blocks

### little-vm-helper

`little-vm-helper` is a VM management tool used for kernel-dependent development and testing, including BPF-focused workflows.

What matters for this skill:
- it can boot lightweight VMs for development and testing
- it can download or build kernels
- it supports pulling images prepared by `little-vm-helper-images`

### little-vm-helper Images

LVH images are published separately and come in variants such as:
- `base`
- `kind`
- `complexity-test`

Choose based on how much userspace you need inside the guest. If unsure, `kind` is a practical default because it is relatively complete.

## Practical CI Pattern

The basic GitHub Actions approach is:

1. Build or download the `.bpf.o` artifact on the runner.
2. Create a matrix of kernel image tags.
3. Launch one LVH VM per matrix entry.
4. Mount the repository or artifact directory into the guest.
5. Inside the guest, print `uname -a`, then try `bpftool prog load`.
6. Fail the job if the load fails.

Minimal pattern:

```yaml
name: Cross Kernel Load

on:
  workflow_dispatch:

jobs:
  load-vm:
    runs-on: ubuntu-latest
    strategy:
      fail-fast: false
      matrix:
        kernel:
          - "6.6-20250616.013250-amd64"
          - "5.15-20250616.013250-amd64"
          - "5.10-20250610.043823-amd64"

    steps:
      - uses: actions/checkout@v4

      - name: Build object
        run: |
          clang -O2 -g -target bpf -D__TARGET_ARCH_x86 -I. -c program.bpf.c -o program.bpf.o

      - name: Provision LVH VM
        uses: cilium/little-vm-helper@v0.0.23
        with:
          test-name: load-test
          image: "kind"
          image-version: ${{ matrix.kernel }}
          host-mount: .
          install-dependencies: "true"
          cmd: |
            uname -a
            cd /host
            sudo bpftool prog load ./program.bpf.o /sys/fs/bpf/test
```

## What To Assert

Start with the smallest useful assertion:

- object loads successfully

Then expand only if needed:
- attach succeeds
- maps are created as expected
- the userspace loader starts correctly
- a smoke event is observed

Recommended progression:
- first gate on `bpftool prog load`
- then add attach tests
- then add behavior checks only if the project needs them

## Good Kernel Matrix Strategy

Include:
- your oldest supported kernel
- one or two common production kernels
- your newest target kernel

If the project uses newer features, make the expected cutoff explicit. Example:
- `RINGBUF` implies 5.8+
- `USER_RINGBUF` implies 6.2+
- TCX implies 6.6+

This makes CI failures informative instead of surprising.

## Failure Interpretation

If one kernel fails and another passes, classify the failure:

- unsupported helper/map/program type
- verifier rejection caused by older kernel behavior
- missing runtime config or kernel option
- image/userspace mismatch rather than BPF logic

First follow-ups:

```bash
uname -a
bpftool feature
bpftool prog load ./program.bpf.o /sys/fs/bpf/test
```

If needed, escalate to:
- verifier log inspection
- checking guest userspace packages
- comparing image variants such as `base` vs `kind`

## Practical Recommendations

- keep the first cross-kernel test focused on loadability, not full end-to-end behavior
- prefer a matrix that reflects real support policy, not every kernel you can find
- keep `fail-fast: false` so you see the whole compatibility picture
- print the guest kernel version in every run
- mount the host workspace into the guest so artifacts stay easy to inspect

## When To Mention This Workflow

Bring this file into the answer when the user asks about:
- testing on multiple kernels
- CI compatibility gates
- validating the oldest supported kernel
- loading eBPF in GitHub Actions with a kernel matrix

## References

- Blog inspiration: `https://h0x0er.github.io/blog/2025/06/21/ebpf-loading-in-different-kernels/`
- LVH project: `https://github.com/cilium/little-vm-helper`
- LVH image tags and variants: `https://github.com/cilium/little-vm-helper-images` and `https://quay.io/organization/lvh-images`
