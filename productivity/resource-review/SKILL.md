---
name: resource-review
description: Top-level memory- and resource-safety code review for modern C/C++ (C++17), including Node.js native addons (node-addon-api / Node-API). Use when the user asks to "review C++/C for memory safety", "find a memory leak", "why does this segfault", "check for use-after-free / double-free / buffer overflow / data race", "resource/handle/fd leak", "review this native addon", "N-API / node-addon-api review", or to check native code with AddressSanitizer/UBSan/TSan/Valgrind. Reports only defects backed by a sanitizer trace, reproducer, or fully traced lifetime. Do not restart the full workflow for a delegated leaf validation task.
metadata:
  website: "https://photostructure.com/coding/"
---

# C/C++ Resource & Memory Review

## Leaf-mode guard

If the task identifies your role as `leaf-reviewer` or sets
`delegation-budget: 0`, read and follow
[`references/validation-pass.md`](./references/validation-pass.md), validate only
the supplied candidates, return the verdicts to the caller, and stop before the
full workflow below.

Identify **provable** memory- and resource-safety defects in modern C/C++ (C++17),
including Node.js native addons built with node-gyp and node-addon-api. Reason about
object lifetimes and resource ownership the way an AddressSanitizer report would — then
report only what you can back with concrete proof. Signal over noise.

This skill finds *defects* (a leak, a use-after-free, a race that actually exists). For
"is this project set up with the right hardening flags, sanitizers, CI, and conventions?"
use the `project-setup` skill, which assesses preventive controls, not exploitable bugs. A
missing hardening flag is not a defect; a heap-buffer-overflow is.

## Scope

**In scope:** C and C++ translation units (`.c/.cc/.cpp/.cxx/.h/.hpp`), especially
Node.js native addons (`Napi::ObjectWrap`, `AsyncWorker`, `ThreadSafeFunction`,
finalizers), the C ABI boundary between C++ and C libraries, and the `binding.gyp`
defines that change runtime behavior.

**Out of scope:** the surrounding JavaScript/TypeScript (defer to
the `web-security-review` skill), and pure build-hardening/convention gaps (defer to
the `project-setup` skill).

### Report vs. research — the prime directive

- **Report on:** only the file, diff, or path the user asked about.
- **Research:** the *entire* module to establish the facts — who allocates, who frees,
  which thread touches what, when a destructor or finalizer actually runs, and what the
  C library's ownership contract says.

A native defect is almost never visible in one function. Trace the allocation to its
free, the handle to its `close`, the pointer to the object's real lifetime, and the
`napi_value` to the call that created it. **Never report on pattern-match alone.**

## Reporting gate: proof, not probability

Report a finding only when you can **construct concrete proof**. If you cannot describe
how the defect actually manifests at runtime, it is not a finding. Use one of these proof
shapes:

- **Dynamic proof (strongest):** a sanitizer or Valgrind report with a stack trace —
  ASan (use-after-free, heap/stack-buffer-overflow, double-free), LSan (leak), UBSan
  (signed overflow, misaligned access, invalid cast), TSan (data race), or Valgrind
  memcheck/helgrind. Reproduce it when a toolchain is available.
- **Reproducer proof:** a concrete, deterministic sequence of calls (or inputs from JS)
  that drives the code to the defect, with the exact lifetime step that goes wrong.
- **Traced-lifetime proof:** the full ownership path in code — the allocation/acquisition
  site, every branch to release, and the specific path that double-frees, leaks, frees
  early, or reads freed/uninitialized memory — with `file:line` for each step.

Every shape must establish the **trigger** (what sequence or input reaches it), the
**mechanism** (the exact lifetime error), and the **impact** (crash, corruption, leak,
disclosure). Prefer to miss a theoretical issue than to flood the report.

Do **not** assign confidence percentages or 1–10 scores — the complete proof is the
evidence. Every candidate is in exactly one state:

| State           | You have…                                                                 | Action                                          |
| --------------- | ------------------------------------------------------------------------- | ----------------------------------------------- |
| **Proven**      | one complete proof shape above, with the lifetime error described concretely | **Report**, with that proof in the finding   |
| **Lead**        | a suspicious lifetime, ownership ambiguity, or static-analyzer hit with a missing proof element | List under **"Needs verification"** as a question |
| **Theoretical** | a pattern match, style nit, or missing hardening control with no demonstrable error | **Drop** (hardening belongs to the `project-setup` skill) |

Read [`references/proof-and-tooling.md`](./references/proof-and-tooling.md) before
reporting anything — it defines how to obtain each proof and the false-positive
discipline (a static-analyzer warning is a Lead, not a finding; a sanitizer suppression
may be hiding the very bug you are looking for).

## Review workflow

Run these steps in order. Load reference files as each step needs them.

### 1. Scope resolution

- If a path/diff was given, review only that. Otherwise review the working changes,
  including untracked files:
  ```bash
  if git rev-parse --verify --quiet origin/HEAD >/dev/null; then
    git diff --merge-base origin/HEAD
  else
    git diff HEAD
  fi
  git ls-files --others --exclude-standard
  ```
- Establish the toolchain and shape: language standard and defines from `binding.gyp` /
  `CMakeLists.txt`, node-addon-api and `NAPI_VERSION`, whether `NAPI_CPP_EXCEPTIONS` is
  set, target OSes/arches, and any vendored C sources. This tells you which classes are
  reachable and whether you can build a sanitized reproducer.

### 2. Map the defect surface

For each file, decide which defect classes are even reachable, then load the matching
sections of [`references/defect-classes.md`](./references/defect-classes.md):

| Code under review                                   | Primary classes to check                                              |
| --------------------------------------------------- | --------------------------------------------------------------------- |
| Manual `new`/`delete`, `malloc`/`free`, owning raw pointers | leaks, use-after-free, double/mismatched free                  |
| OS handles / fds / sockets / library handles        | resource/handle/fd leaks, use-after-close                             |
| Buffers, arrays, pointer arithmetic, `memcpy`/`strcpy` | heap/stack overflow, out-of-bounds read/write                      |
| Size/length math, casts between int widths/signs    | integer overflow/truncation → under-allocation                        |
| Uninitialized locals/members, partial construction  | uninitialized reads                                                   |
| Filesystem path checks then use                     | TOCTOU                                                                 |
| Threads, `AsyncWorker::Execute`, shared mutable state | data races, lock-ordering, atomics misuse                           |
| `Napi::ObjectWrap`, `Reference`, `ThreadSafeFunction`, finalizers | Node-API lifetime — see `napi-resource-model.md`          |

For any addon code, load
[`references/napi-resource-model.md`](./references/napi-resource-model.md): the
addon-specific hazards a general C++ reviewer misses (call-scoped `napi_value` stored
too long, reference/handle-scope leaks, finalizers that run late or under restricted API
rules, threadsafe-function acquire/release imbalance, exceptions crossing the C ABI).

### 3. Deep lifetime scan

The core pass. **Reason about ownership; do not grep-and-report.** For each allocation or
acquisition, answer: who owns it, is release guaranteed on every path (including
exceptions and early returns), can it be released twice, and can anyone use it after
release? For each buffer, answer: is every index and length bound-checked against the
real allocation size, computed without overflow? Apply the detection signals and safe
patterns in `defect-classes.md`.

### 4. Cross-boundary lifetime analysis

Step back and trace lifetimes *across* function, thread, and language boundaries — where
the real defects hide:

- **C++ ↔ C library:** does the code honor the library's ownership contract (which
  allocator frees it, required teardown order, when error accessors are still valid)?
- **Native ↔ JS:** does a JS object outlive the native resource it wraps, or vice versa?
  Is a `napi_value`, `Reference`, or `ObjectWrap` pointer used after the object is gone?
- **Thread ↔ thread:** is every field touched from a worker thread and the main thread
  synchronized or atomic? Does `Execute()` touch `napi_env`/`napi_value` (forbidden)?
- **Teardown:** what runs during environment/process teardown, and in what order — can a
  finalizer, cleanup hook, or destructor touch something already freed?

### 5. Obtain proof

Promote each surviving candidate to Proven or drop it. When a toolchain is available,
build a sanitized target and drive the path (see `proof-and-tooling.md`) — an ASan/UBSan/
TSan/LSan or Valgrind trace is the gold standard. When you cannot build, construct a
complete traced-lifetime proof with `file:line` for every step, or downgrade it to a Lead.

### 6. Adversarial self-verification

For each surviving candidate, **try to refute it** before it makes the report.
For a non-trivial finding set, use at most **two** leaf validation tasks total.
Partition or batch the candidates between them; never launch one task per
candidate or a second validation round.

Prefer the tool-restricted `cpp:reviewer` agent when the host exposes it;
otherwise use a general task-local subagent. Start every prompt with
`role: leaf-reviewer` and `delegation-budget: 0`, omit workflow skill names, and
point it at the resolved path of
`<plugin-root>/skills/resource-review/references/validation-pass.md`. When
context inheritance is configurable, do not pass the surrounding conversation.
Ask each reviewer to disprove its assigned candidates using
`references/proof-and-tooling.md`:

- Re-read the lifetime with fresh eyes. Is release *actually* missing, or is there an
  RAII guard, `unique_ptr`, tracking set, or cleanup hook that handles it?
- Is the pointer really used after free, or was ownership transferred/nulled first?
- Is the buffer access truly unbounded, or is there an upstream length/`SafeCast` check?
- Is the "race" real, or is the state single-threaded by construction / mutex-protected?
- Is the "leak" first-party, or a one-time library init that a suppression legitimately
  covers?

Drop anything without a complete applicable proof after refutation.

### 7. Report

Emit the report in the structure defined by
[`references/report-format.md`](./references/report-format.md): a severity summary table,
then findings grouped by defect class, each with location, proof (sanitizer trace /
reproducer / traced lifetime), a plain-English trigger, impact, and a minimal fix. If
nothing survives, say so explicitly and state what was scanned — "No proven memory/resource
defects identified in <scope>."

### 8. Propose fixes (do not auto-apply)

For each Critical/High finding, propose a concrete, minimal patch (vulnerable → fixed),
preserving surrounding style and names, and prefer the RAII/ownership fix that removes the
class of bug (see the `project-setup` skill's `modern-cpp-conventions.md`) over a one-off
patch. State plainly: **"Review each patch before applying — nothing has been changed."**
Never edit files as part of the review unless the user explicitly asks.

## Severity

| Severity     | Impact                                          | Native examples                                                                                   |
| ------------ | ----------------------------------------------- | ------------------------------------------------------------------------------------------------- |
| **Critical** | Memory corruption reachable from untrusted input | Heap-buffer-overflow or use-after-free driven by attacker-influenced JS input; write past a buffer |
| **High**     | Corruption/crash under realistic conditions      | Use-after-free on a teardown/close race; double-free; unbounded write with a plausible trigger     |
| **Medium**   | Real defect, bounded or conditional impact        | Out-of-bounds *read*; integer truncation feeding a size; leak on a hot path; data race on non-critical state |
| **Low**      | Demonstrable but limited                          | One-time leak only at process exit; missing `close` on a rare error path with small impact          |

Rate by demonstrated impact and trigger reachability, not by how alarming the class
sounds. A theoretical overflow with no reachable trigger is not a finding at all.

## Output rules

- Lead with a findings **summary table** (counts by severity).
- **Group by defect class**, not by file.
- Every finding: `file:line`, an evidence snippet, its **proof** (the applicable shape), a
  plain-English trigger scenario, impact, and a fix.
- Never auto-apply patches — present them for human review.
- A clean result is a valid result: say what was scanned and that nothing was proven.

## Reference files

Load on demand — keep SKILL.md context lean.

| File                                                                       | Load during   | Covers                                                                                                                                    |
| -------------------------------------------------------------------------- | ------------- | ---------------------------------------------------------------------------------------------------------------------------------------- |
| [`references/defect-classes.md`](./references/defect-classes.md)           | steps 2, 3    | Per-class detection signals, safe patterns, CWE/CERT mapping, and which sanitizer proves each: UAF, double/mismatched free, leaks, OOB, uninitialized reads, integer overflow/truncation, TOCTOU, data races |
| [`references/napi-resource-model.md`](./references/napi-resource-model.md) | steps 2, 4    | Node-API / node-addon-api lifetime hazards: call-scoped handles, handle scopes, reference RAII, ObjectWrap finalizer timing and API restrictions, ThreadSafeFunction/AsyncWorker ownership, exceptions across the C ABI, context-aware instance data |
| [`references/proof-and-tooling.md`](./references/proof-and-tooling.md)     | steps 5, 6    | The proof hierarchy; running ASan/UBSan/TSan/LSan/Valgrind against a Node addon; what each tool misses; legitimate vs. bug-masking suppressions; the Proven/Lead/Theoretical gate |
| [`references/report-format.md`](./references/report-format.md)             | step 7        | Output template and finding card                                                                                                          |

## Adapting for your project

Point this skill at `AGENTS.md` and optional `CLAUDE.md` for the module's threading model,
ownership conventions, and known-safe patterns. Record the project's real invariants (for
example "statements are single-threaded by construction", "explicit close orders native
teardown before finalization") in `references/napi-resource-model.md` so the review credits them
instead of re-flagging them, and add any project-specific RAII wrappers to
`references/defect-classes.md` so their release contracts are understood.
