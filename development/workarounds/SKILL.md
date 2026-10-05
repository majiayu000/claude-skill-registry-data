---
name: workarounds
description: Registry of deliberate, non-ideal workarounds currently live in tt-emule (hacks we accepted to make something pass, NOT normal development practice). Read this before adding any new workaround, and when touching code that carries one — each entry records what the hack is, why it is not the right fix, the real root cause, and the path to removing it.
---

# Workarounds registry

This file is the **single, explicit list of deliberate workarounds** in tt-emule.

A workaround here is a change we knowingly accepted that is **not** the correct
fix — it papers over a problem to make a test pass while the real fix lives
elsewhere (usually an upstream kernel, a tt-metal runtime bug, or a missing emule
model we did not have time to build properly).

**These entries are not a template for how to develop.** They exist precisely so
that a hack does **not** silently become precedent. The default tt-emule rules
still hold (see `.claude/CLAUDE.md`): be faithful to silicon, keep a single code
path, and **surface caller bugs rather than mask them**. Every entry below
violates one of those on purpose, is documented as such, and has a tracked path
to removal.

## Rules for this registry

- **Adding a workaround is a last resort.** First try the faithful fix (model the
  real behavior; fix the actual bug upstream). Only fall back to a workaround when
  that is blocked, and say so explicitly in review.
- **Every workaround must be registered here** with: what it is, why it is a hack
  (how it can fail / what rule it bends), the real root cause (file + line), the
  proper fix, and a tracking link (issue/PR).
- **Link from the code to this file.** The workaround's code site must carry a
  comment pointing here (e.g. `// WORKAROUND: see .claude/skills/workarounds`), so
  anyone editing it knows it is a known hack, not load-bearing design.
- **Workarounds are removed, not grown.** When the real fix lands, delete the
  workaround and its entry. Do not extend one hack to cover a new case — add the
  faithful fix instead.

---

## WA-1 — fabric mux kernel replaced with a no-op (n300/p300 CCL)

**Code site:** `tt-metal …/impl/emulation/emulated_program_runner.cpp`,
`jit_compile_kernel` preprocess step — when the kernel source basename is
`tt_fabric_mux.cpp`, emule writes a no-op `kernel_main` instead of compiling the
real source (search "emule no-op stub for tt_fabric_mux.cpp").

**What it does:** the fabric MUX kernel (a persistent worker-side kernel that
aggregates worker packets onto ethernet links and forwards them) is not compiled
or run. The CCL workers' `WorkerToFabricMuxSender` teleports each packet straight
to its final destination instead (the same direct path the no-mux
`num_workers_per_link=1` configuration uses).

**Why it is a workaround (bends a rule):**
- It special-cases a specific kernel **by filename** and substitutes a no-op,
  rather than modeling the kernel or providing a general "transport kernel" hook.
- It is functionally faithful (the data + semaphore effects are identical — the
  teleport delivers to the same destination the mux would have forwarded to), but
  it does **not** model the mux's flow-control / buffer back-pressure. emule is a
  functional (not cycle-accurate) emulator, so this is acceptable for correctness,
  but it is a divergence from the silicon code path.

**Real root cause (emule scope, not a bug):** the mux is part of the fabric
*transport* layer (worker → mux → ethernet → router → dest), which emule
deliberately collapses into the synchronous teleport (see
`docs/fabric-ccl-emulation.md`). The real mux additionally pulls in
erisc firmware headers emule does not model and is a persistent loop that would
never terminate under emule's run-to-completion join.

**Proper fix (removes this workaround):** if mux fidelity is ever required (e.g.
modeling link contention), model the mux faithfully — workers write packets into
the mux core's L1 channels and a mux execution context drains + teleports them —
behind a general transport-kernel mechanism rather than a filename special-case.
Until then the no-op stub is the correct functional model.

**Tracking:** [#227](https://github.com/tenstorrent/tt-emule/issues/227) (WA-1 faithful-transport
removal path) and [#231](https://github.com/tenstorrent/tt-emule/issues/231) (reduce the fabric shim
surface: real packet header + faithful mux); also documented in `docs/fabric-ccl-emulation.md`.
