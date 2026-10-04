---
name: silicon-grade-discipline
description: Use when writing hardware, firmware, verification, or tooling code that will reach real silicon, and you face a tradeoff between shipping fast and shipping correct; covers failures-should-fail, no over-engineering, no-panic, and test coverage
---

# Silicon-Grade Discipline

## Overview

Software bugs ship a patch. Hardware bugs ship a respin, or a recall, or a dead board on a bench you can't reach. That asymmetry changes how you write code in this domain: correctness is not negotiable against speed, because the cost of wrong is measured in mask sets and weeks.

**Core principle:** A failure must be loud, a check must be honest, and a fix must address the root cause. The most dangerous output in this domain is a green checkmark over a real defect.

## When to Use

- Writing or reviewing code that drives, verifies, or generates hardware
- About to write register writes, an init sequence, or a pin map for a real part from memory instead of the datasheet
- Tempted to add a flag that makes a failing check pass
- Tempted to add recovery scaffolding for a failure mode you haven't diagnosed
- Deciding between `panic`/`assert` and returning an error
- Deciding how much test coverage is enough

This skill is the shared backbone; the domain skills (`hdl-module-design`, `tapeout-precheck`, `differential-verification`, and others) lean on it.

## Failures Should Fail

Never add a knob that converts a real failure into a pass. No `ERROR_ON_DRC=false`, no `--skip-lvs`, no `if (mismatch) verdict = pass`, no "temporarily" commented-out assertion. Those don't fix the problem; they hide it and then ship it.

- A failing check means the design or the code is wrong. Fix the thing being checked.
- A legitimate exception is explicit, recorded, and granted by the authority that owns the rule (the foundry, the spec), with its rationale written down. It is never a flag you flipped to hit a date.
- Trust the logs. Read what the tool actually reported. "0 errors" from a run that skipped the check is worse than a red failure, because it lies.

## A Capability Is Not A CLI Flag

A hardware capability is declared by the design and read by the tooling, never bolted on or stripped off by a generator flag. A `--no-paging` switch that removes the MMU from a core which advertises Sv39 is incoherent: the core says it does virtual memory, the flag says it doesn't, and now two parts of the system disagree about what the silicon is. The same goes for a flag that disables an extension a profile requires, or one that drops a peripheral the address map still references.

- The core (or tier, or profile) declares its capabilities. The generator READS them and builds accordingly. It does not BUILD a capability config and inject it, and it does not offer a knob to contradict the declaration.
- If you genuinely need a smaller variant, that is a different declared configuration (a leaner tier), not the full one with a feature flipped off at generation time. Derive the build from the declaration; do not override the declaration from the build. See `hdl-module-design` and `soc-integration` for the derive-don't-restate pattern this rests on.
- The smell to catch: the generator computing a capability from indirect inputs (deriving an MMU config from the XLEN) and injecting it, instead of the design stating the capability and the generator consuming it. The reaching-past-the-declaration is the bug, even before anyone adds a flag.

## Read The Datasheet

When code drives a real chip, a real FPGA primitive, or a real board, the datasheet is the source of truth. The JEDEC standard, the ISA manual, and the vendor user guide are datasheets too. Do not guess a register field, an opcode, or a timing parameter from memory. A guessed value configures the part wrong, and then the part reads back garbage with no error to tell you why.

- Read the datasheet before you write the register writes, the init sequence, or the pin map. Cite the table and section number for each value you take.
- Field encodings and opcodes are not guessable. A DDR3 MR1 termination bit on the wrong address line, or a ZQ-calibrate command issued with the PRECHARGE opcode, both let the init FSM complete, and both leave the part misconfigured and silent.
- Timing parameters (setup, hold, refresh, tXPR, CAS latency) come from the part's table, not a round number that looked close.
- FPGA primitives have datasheets too (the family libraries guide or architecture document). Block RAM init packing, clock-primitive phase behavior, and IO delay ranges are specified there. A primitive that ignores a control input is often a documented limitation, not a bug in your logic.
- "It configured, the done flag went high, and it still reads wrong" almost always means a value the datasheet would have corrected. Re-read the table before you reach for a scope.

## Don't Over-Engineer Recovery Hatches

Resist building preemptive save-on-failure, retry-until-it-works, or rollback scaffolding around a failure you haven't understood. That machinery hides the bug, adds surface area, and convinces you the system is robust when it is actually papering over a real defect.

- Diagnose the root cause first. A retry loop around a corruption just corrupts more slowly.
- Trust the logs and the crash. A clean fault that tells you where it broke is more valuable than a system that limps past the break.
- Build the recovery you actually need, once you understand the failure, not the recovery you imagine you might need.

## Don't Panic; Return Errors

Reserve `panic`/`abort`/unwrap-on-error for genuinely impossible states (an invariant the type system can't express, which if violated means memory is already corrupt). For everything that can fail in normal operation (bad input, a device that didn't respond, a parse that failed), return a typed error and let the caller decide.

- Library code returns typed errors (thiserror-style). User-facing layers render them nicely (color-eyre-style). Structured logging (tracing-style) records the context.
- A panic in a verification farm or a bring-up tool takes down the run and loses the diagnostic. An error propagates the context you need.

## Test Like It's Going To Silicon

Because it is.

- Exhaustive coverage per component, not just the happy path through the top level. Sweep parameters and boundaries.
- Test files mirror the source layout so every unit's test is findable.
- Cover the failure paths: assert that bad input actually errors, that validation actually rejects.
- Logic lives in the library so it's testable without a process; the CLI/daemon is a thin consumer.

## Red Flags

| Thought | Reality |
|---------|---------|
| "I'll add a flag to skip this check for now" | That flag ships a known defect. Fix the check's subject. |
| "Let me add a save/retry in case it fails" | Diagnose first. Recovery for an undiagnosed failure hides it. |
| "I'll panic here, it shouldn't happen" | If it can happen in normal operation, return an error. |
| "0 errors printed, we're good" | Confirm the check actually ran. Trust the logs, not the absence. |
| "Top-level test passes, that's enough" | Cover each component and its failure paths. |
| "It's close enough" | For silicon, close enough is a respin. |
| "I know this chip's registers" | The datasheet knows them. Cite the table and section. |

## Midstall House Style

- These rules recur across Aegis, Harbor, Heimdall, Ferrite, and the rest, because everything here is heading toward real hardware.
- No design docs for their own sake; keep reasoning in-conversation and fix the root cause.
- Write docs, comments, and commit messages in ASD-STE100 Simplified Technical English: one meaning per word, active voice, simple tenses, short sentences. The `asd-ste100` skill rewrites prose that drifts from it.
- No em dashes, no emoji, no slang. Plain, direct, honest about what works and what doesn't.
