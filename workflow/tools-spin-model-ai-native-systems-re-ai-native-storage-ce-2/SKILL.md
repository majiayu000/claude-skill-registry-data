---
name: tools-spin-model
description: Create a new Spin/Promela formal verification model for a system property
argument-hint: "[property-number or description of property to prove]"
---

Create a new Spin/Promela specification in `modelling/spin/<name>/` to verify a concurrency property of the Certus system.

## Input

If no argument is provided, first ask the user to define the **scope**, then present the property menu.

### Step A: Scope Selection

Ask the user to choose the modeling scope:

- **Single component** — Model the internal concurrency of one component in isolation (e.g., just the dispatcher, just the extent-manager, just the block-device actor). Threads and channels within that component are modeled explicitly; interactions with other components are abstracted as nondeterministic environment stubs.
- **Whole system** — Model the interaction between multiple components as wired together in certus-server (e.g., client → dispatcher → memory-tier → block-device → extent-manager). Includes cross-component communication channels, the gRPC thread pool, and background workers.

The scope determines:
- Which source files to read (single component = one crate's `src/`; whole system = multiple crates + `apps/certus-server/`)
- How to abstract boundaries (single = environment stubs with nondeterministic responses; whole = explicit `proctype` per component role)
- Model complexity (single = fewer processes, deeper per-component detail; whole = more processes, coarser per-component abstraction)

### Step B: Property Selection

Present the full property menu and ask the user to choose. The user may also describe a custom property.

**System-level properties** (scope: whole system recommended):

1. **Reference-count balance** — Every read_ref increment has a matching decrement on all paths. No leaked refs (memory leak) or double-decrements (use-after-free).
2. **Write-before-evict** — Models the dispatcher's populate → write-through → eviction lifecycle to verify that memory-tier eviction never produces dangling SSD references.
3. **Cold-path promotion atomicity** — At most one thread succeeds in promoting a given key from SSD to memory-tier. No double-allocation or lost updates.
4. **Populate-lookup linearizability** — After populate(key) returns Ok, a concurrent lookup(key) never observes KeyNotFound unless an explicit remove or eviction intervened.
5. **Shutdown ordering** — No NVMe command is issued after its block device shuts down. Background writer drains before drives are torn down.
6. **No lost extents** — Every reserve_extent is followed by either publish() or drop (abort). No extent is permanently allocated but uncommitted.

**Component-level properties** (scope: single component recommended):

7. **Pipeline ring slot safety** — A ring buffer slot is never resubmitted for NVMe read while its CUDA DMA transfer is still in flight. (Component: dispatcher/pipeline)
8. **Starvation freedom** — No client is starved indefinitely waiting to enqueue a write job under backpressure. (Component: dispatcher/background)
9. **Eviction fairness** — An entry touched within the last N operations is never evicted while untouched entries exist. (Component: dispatcher/eviction)
10. **Actor mailbox ordering** — Messages sent to a block-device actor are processed in FIFO order; no command reordering across the channel boundary. (Component: block-device-spdk-nvme)
11. **Extent bitmap consistency** — Concurrent reserve/publish/remove never leave the bitmap in a state where an extent is both allocated and free. (Component: extent-manager)

If the user provides a number (1-11), use that property. If they provide free text, treat it as a custom property description and ask for a short kebab-case name for the subdirectory.

## Steps

1. **Determine the property and directory name.**

   Map selections to directory names:
   - 1 → `ref-count-balance`
   - 2 → `write-before-evict`
   - 3 → `promotion-atomicity`
   - 4 → `populate-lookup-linearizability`
   - 5 → `shutdown-ordering`
   - 6 → `no-lost-extents`
   - 7 → `pipeline-ring-safety`
   - 8 → `starvation-freedom`
   - 9 → `eviction-fairness`
   - 10 → `actor-mailbox-ordering`
   - 11 → `extent-bitmap-consistency`
   - Custom → ask user for a kebab-case name

2. **Read the relevant source code** to understand the real synchronization protocol.

   Key source files by property and scope:

   **Whole-system scope** (read certus-server wiring + component internals):
   - 1,4: `components/dispatcher/src/lib.rs` (populate, lookup, evict_for_space, batch_lookup)
   - 2: `components/dispatcher/src/lib.rs` + `components/dispatcher/src/background.rs`
   - 3: `components/dispatcher/src/lib.rs` (batch_lookup cold-path promotion, lines ~1045-1215)
   - 5: `components/dispatcher/src/lib.rs` (shutdown), `components/dispatcher/src/background.rs` (BackgroundWriter::shutdown), `apps/certus-server/src/main.rs` (shutdown sequence)
   - 6: `components/dispatcher/src/lib.rs` (prepare_store, commit_store, cancel_store, process_write_job)

   **Single-component scope** (read only the target component):
   - 7: `components/dispatcher/src/pipeline.rs` (PipelineRing, pipelined_ssd_to_gpu_zero_copy)
   - 8: `components/dispatcher/src/background.rs` (channel + worker_loop)
   - 9: `components/dispatcher/src/lib.rs` (evict_for_space, mt.evict_lru, mt.oldest_keys)
   - 10: `components/block-device-spdk-nvme/src/` (actor thread, command channel, completion channel)
   - 11: `components/extent-manager/src/` (bitmap allocation, reserve_extent, publish, remove_extent)

   Also reference the existing model at `modelling/spin/write-before-evict/write_before_evict.pml` for style and conventions.

3. **Create the subdirectory** `modelling/spin/<name>/`.

4. **Write the Promela specification** `modelling/spin/<name>/<name_underscored>.pml`.

   Follow these conventions (from the existing write-before-evict model):
   - Header comment block explaining what is being verified, the scope, and how to run
   - `#define` parameters section (N_CLIENTS, N_KEYS, etc.) tuned small for tractable state space
   - Per-key or per-resource state as `mtype` enums and arrays
   - `proctype` for each thread role in the system
   - `inline` helpers for shared logic (like eviction)
   - Inline `assert()` statements for safety properties
   - `init` process that starts all proctypes, waits for completion, signals shutdown, runs final invariant checks
   - Aim for 100% state coverage (no unreached states)
   - Use `atomic{}` for operations that share a mutex in the real code
   - Use `d_step{}` for deterministic sequences (scans)
   - Use generation counters to handle key reuse across lifecycles
   - Model channels as bounded `chan` (even if real code uses unbounded)

   **Scope-specific conventions:**

   For **single component** models:
   - Abstract external interfaces as nondeterministic stubs (e.g., `if :: success :: failure fi`)
   - Focus on internal thread interactions and shared state
   - Name the header comment "Component-level model: <component-name>"
   - Document which interfaces are stubbed and what assumptions are made

   For **whole system** models:
   - One `proctype` per major thread role across components
   - Use channels to model inter-component communication (gRPC, receptacles)
   - Name the header comment "System-level model: <property-name>"
   - Document the component wiring in the header

5. **Write the Makefile** `modelling/spin/<name>/Makefile`:

   ```makefile
   MODEL = <name_underscored>.pml
   PAN   = pan
   CC    = cc
   CFLAGS = -O2
   DEPTH = 200000

   .PHONY: all safety liveness clean

   all: safety

   safety: $(PAN)
   	./$(PAN) -m$(DEPTH)

   liveness: $(PAN)-live
   	./$(PAN)-live -a -m$(DEPTH)

   $(PAN): pan.c
   	$(CC) $(CFLAGS) -DSAFETY -o $@ $<

   $(PAN)-live: pan.c
   	$(CC) $(CFLAGS) -o $@ $<

   pan.c: $(MODEL)
   	spin -a $<

   clean:
   	rm -f $(PAN) $(PAN)-live pan.* *.trail
   ```

6. **Write the README.md** `modelling/spin/<name>/README.md`:

   Structure (follow the pattern in `modelling/spin/write-before-evict/README.md`):
   - Title: `# <Property Name>`
   - **Scope**: Single component (`<component-name>`) or Whole system
   - One-paragraph description of what the model verifies
   - **Properties Verified** table (ID, Property description, Type: Safety/Liveness)
   - **System Abstraction** table (Real component → Promela process)
   - **Assumptions / Stubs** section (for single-component scope: list what is abstracted away and how)
   - **Running** section with shell commands
   - **Tuning the Model** section explaining parameters
   - **Correspondence to Source Code** table (Model location → Source file → Line range)

7. **Run the verification** by executing `make` in the new directory.

   - If Spin is not installed, inform the user and skip this step.
   - If verification fails with an assertion violation, analyze the trail (`spin -t -p <file>.pml`), fix the model, and re-run until it passes.
   - Report: number of states explored, depth reached, errors found, coverage (unreached states).

8. **Report results** to the user:
   - Scope (single component or whole system)
   - Property being verified
   - Pass/fail status
   - State space size
   - Coverage (target: 0 unreached states in all proctypes)
   - Path to the new model directory

## Notes

- Spin must be installed at `/usr/local/bin/spin` (see `modelling/spin/write-before-evict/README.md` for install instructions).
- Keep parameters small (2-3 clients, 2-4 keys, pool cap < key count) to maintain tractable state spaces (<10M states).
- The model should be self-contained — no external dependencies beyond Spin and a C compiler.
- Use the generation-counter technique from the write-before-evict model to handle key reuse without conflating lifecycles.
- Single-component models are faster to verify (fewer processes) and better for finding internal races.
- Whole-system models catch cross-component protocol violations but have larger state spaces.
