---
name: parallel-build
description: Use this skill whenever the user has multiple specs or features to build and wants to run them in parallel, build faster, run multiple agents, or batch their build session. Also trigger when the user says "I have a bunch of features to build," "can I run these at the same time?", "which of these can I build in parallel?", "I want to build all my feedback specs today," or "plan a build session for these specs." Use this even if the user only has 2-3 specs — the dependency analysis prevents conflicts regardless of batch size.
---

# Parallel Build

Help the user build multiple features simultaneously by running independent Claude Code sessions in parallel.

## Overview

This skill:
1. Reads all specs in the user's `/specs/` directory (or specs they provide)
2. Analyzes dependencies between them — which files they touch, which tables they modify, which components they share
3. Groups specs into parallel batches (specs in the same batch can run simultaneously without conflicts)
4. Generates a session plan with exact terminal commands
5. After builds complete, runs integration verification

## Before Starting

Read all spec files the user wants to build. For each spec, extract:
- Files it will create or modify (from Requirements section)
- Tables it will read from or write to (from Context section)
- Components it will use or create (from Requirements + Constraints)
- Dependencies on other specs (explicit or implied)

Then run the dependency analysis.

## Step 1: Dependency Analysis

Run `scripts/analyze_deps.py` with the paths to all spec files:

```bash
python {baseDir}/scripts/analyze_deps.py /path/to/specs/spec1.md /path/to/specs/spec2.md ...
```

Or point it at the specs directory:

```bash
python {baseDir}/scripts/analyze_deps.py --dir /path/to/specs/
```

The script outputs a JSON report with:
- Each spec's file footprint (files it creates or modifies)
- Conflicts between specs (two specs touching the same file)
- Suggested batches (groups of specs that can run in parallel)
- Recommended order (which batch goes first based on dependencies)

## Step 2: Resolve Conflicts

If the analysis finds conflicts (two specs modifying the same file), there are three resolution strategies:

**Strategy 1: Sequential** — Put conflicting specs in different batches. Spec A runs in batch 1, Spec B runs in batch 2 after A is complete. Safest option.

**Strategy 2: Split the shared file** — If two specs both modify a shared component (like a navigation file), create a mini-spec that only updates the shared file after both features are built. Run the features in parallel, then run the integration spec.

**Strategy 3: Merge specs** — If two specs are so intertwined they can't run independently, combine them into one spec. This is a sign the original decomposition was too fine-grained.

Present the conflicts and recommended strategy to the user. Let them choose.

## Step 3: Generate Session Plan

For each batch, generate:

### Terminal Commands

Tell the user exactly how to start each parallel session. For Claude Code:

```
BATCH 1 (run these simultaneously):

Terminal 1:
  cd /path/to/project
  claude "Read the spec at /specs/feature-a.md and build it. Follow all existing skills."

Terminal 2:
  cd /path/to/project
  claude "Read the spec at /specs/feature-b.md and build it. Follow all existing skills."

Terminal 3:
  cd /path/to/project
  claude "Read the spec at /specs/feature-c.md and build it. Follow all existing skills."

Wait for all three to complete before starting Batch 2.

BATCH 2 (after Batch 1 is done):

Terminal 1:
  claude "Read the spec at /specs/feature-d.md and build it. Follow all existing skills."

Terminal 2:
  claude "Read the spec at /specs/feature-e.md and build it. Follow all existing skills."
```

### Tracking Checklist

Copy `assets/parallel-tracker.md` to the project (e.g., `/docs/parallel-tracker.md`). Fill in specs per batch, mark as complete when each agent finishes.

### Time Estimates

Based on spec complexity (number of requirements, files to create):
- Simple spec (1-3 requirements, 1-2 files): ~10 min
- Medium spec (4-6 requirements, 2-4 files): ~15-20 min
- Complex spec (7+ requirements, 4+ files): ~25-30 min

Batch completion time = longest spec in the batch. With 3 parallel agents, a batch of three 15-minute specs takes 15 minutes, not 45.

## Step 4: Monitor (User's Job)

The user monitors the parallel sessions. The skill provides guidance:

**What to watch for:**
- Agent asking a question = spec was ambiguous. Answer it, note it for future specs.
- Agent stuck in a loop = kill it, check the spec, re-hand off.
- Agent finished early = review and mark complete in tracker.

**What NOT to do:**
- Don't hover over all three terminals. Check in every 5-10 minutes.
- Don't fix things in one terminal that another terminal will handle.
- Don't start Batch 2 until all of Batch 1 is reviewed and approved.

## Step 5: Integration Verification

After all batches complete, run integration verification.

Read `references/integration-checks.md` for the verification approach.

The verification checks:
1. **No overwritten files** — git diff shows only expected changes per spec
2. **No duplicate components** — two agents didn't create the same component independently
3. **Shared state works** — if multiple features read/write the same table, data flows correctly
4. **Navigation updated** — all new pages appear in navigation (if skills handle this)
5. **Build passes** — `npm run build` succeeds with all changes combined
6. **Core flow works** — the Issue 05 first-user-test still passes with all new features

If issues are found, generate a fix spec targeting only the integration problems. Hand it off as a single agent task.

## Important Principles

- **Conservative batching.** When in doubt about a conflict, put specs in separate batches. A false-negative (missed conflict) costs more than a false-positive (unnecessary sequential build).
- **Git is your safety net.** Ensure the user commits before starting a parallel session. If something goes wrong, `git stash` or `git reset` recovers clean state.
- **Two parallel agents is the practical starting point.** Three is feasible. Four or more on the same codebase creates merge pain. Start with two until the user is comfortable.
- **Review between batches, not after all batches.** Catch issues early. Batch 1 review happens before Batch 2 starts.
- **The time savings are real but modest for small batches.** Two specs in parallel saves 10-15 minutes. Five specs in two batches saves 30-40 minutes. The value compounds with batch size — this is most useful during a full build session (Issue 05 style) with 5+ specs.
