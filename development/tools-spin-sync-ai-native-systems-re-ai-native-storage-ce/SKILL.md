---
name: tools-spin-sync
description: Synchronize Spin/Promela models with current source code and re-verify
argument-hint: "[model-name | all]"
---

Ensure that existing Spin/Promela models in `modelling/spin/` accurately reflect the current source code, then re-run model checking to confirm the properties still hold.

## Input

The user provides one of:
- A specific model name (subdirectory under `modelling/spin/`, e.g. `write-before-evict`, `no-lost-extents`)
- `all` — synchronize every model found in `modelling/spin/`
- No argument — present the list of available models and ask the user to choose one or all

## Steps

### Step 1: Discover models

List all subdirectories under `modelling/spin/` that contain a `.pml` file and a `README.md`. Each such directory is a model.

If no argument was provided, present the list and ask:

> Which model(s) would you like to synchronize?
> 1. write-before-evict
> 2. no-lost-extents
> 3. (other models...)
> A. All of the above

### Step 2: For each selected model, perform the synchronization

#### 2a. Read the model's README.md

Extract from the README:
- The **"Correspondence to Source Code"** table — this maps model locations to source files and line ranges
- The **"Properties Verified"** table — the invariants the model checks
- The **"System Abstraction"** table — how real components map to Promela processes
- The **"Assumptions / Stubs"** section — what is abstracted away

#### 2b. Read the current source code

For each entry in the Correspondence table, read the referenced source file and the indicated line range (plus ~50 lines of context on each side to detect if the logic has shifted).

#### 2c. Read the existing .pml model

Read the full Promela specification to understand the current model logic.

#### 2d. Identify divergences

Compare the model against the source and look for:

1. **Structural changes** — The source code logic has been refactored, moved to different functions/files, or the control flow has changed in ways the model doesn't capture.
2. **New states or transitions** — New code paths have been added (e.g., a new error handling branch, a new concurrent actor, a new state in an enum) that the model doesn't cover.
3. **Removed paths** — Code paths the model exercises no longer exist in the source.
4. **Semantic changes** — The synchronization protocol has changed (e.g., lock ordering, channel semantics, atomic sections) but the model still uses the old protocol.
5. **Line range drift** — The code is substantively the same but has shifted to different line numbers (cosmetic — update the README only).

#### 2e. Report findings

For each model, report one of:

- **IN SYNC** — The model accurately reflects the current source. No changes needed. (Proceed directly to Step 3.)
- **LINE DRIFT ONLY** — The logic is unchanged but line numbers in the Correspondence table are stale. Update the README table. (Proceed to Step 3.)
- **MODEL UPDATE REQUIRED** — The source has diverged materially. List the specific divergences found.

#### 2f. Update the model (if required)

If the model requires updating:

1. **Explain the divergence** to the user: what changed in the source, and how the model must adapt.
2. **Update the .pml file** to reflect the new source code logic. Preserve the existing model's style and conventions:
   - Keep the same parameter names and sizes (unless the change requires new parameters)
   - Keep the same property IDs (P1, P2, ...) where they still apply
   - Add new properties if new invariants are now relevant
   - Remove properties if they no longer apply (explain why)
   - Maintain the header comment block format
3. **Update the README.md** — refresh the Correspondence table with correct line ranges, update Properties Verified if changed, update System Abstraction if new processes were added/removed.

### Step 3: Run model checking

For each model (whether updated or unchanged):

```bash
cd modelling/spin/<model-name>
make clean
make
```

Report the results:
- **PASS**: errors = 0, state count, depth reached, unreached states
- **FAIL**: assertion violation or invalid end-state found. In this case:
  1. Run `spin -t -p <model>.pml` to get the error trail
  2. Analyze the counterexample
  3. Determine if the model is wrong (fix it) or if a real bug was found (report it to the user with the trail)
  4. Re-run verification after fixes

If Spin is not installed (`/usr/local/bin/spin` missing), warn the user and skip verification.

### Step 4: Summary report

Present a final summary table:

| Model | Status | Divergences | Verification | States | Unreached |
|-------|--------|-------------|--------------|--------|-----------|
| write-before-evict | IN SYNC | — | PASS | 12345 | 0 |
| no-lost-extents | UPDATED | new abort path | PASS | 67890 | 0 |

## Notes

- Models are always found at `modelling/spin/<name>/<name_underscored>.pml` (name uses hyphens for the directory, underscores for the .pml filename).
- The Makefile in each model directory provides the `make`/`make clean` targets.
- If a model update introduces new processes or significantly changes the state space, re-tune the parameters to keep verification tractable (<10M states). Document parameter changes in the README.
- Never delete existing properties unless the invariant is provably no longer meaningful. If unsure, keep it and note it as "legacy — source no longer exercises this path directly."
- If the source change reveals a potential real concurrency bug (model finds a valid counterexample that corresponds to reachable code), halt the sync and report the finding prominently to the user.
