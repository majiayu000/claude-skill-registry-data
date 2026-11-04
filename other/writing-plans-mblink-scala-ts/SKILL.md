---
name: writing-plans
description: Feature planning methodology using Compiler Driven Development for scala-ts. Use when designing new features or multi-step changes. Plans break work into type-first tasks with exact file paths and expected TypeScript output.
---

# Writing Plans

Plans go in the Claude plans directory as small, compiler-verifiable, type-first tasks (2–5 minutes each) with exact file paths.

## Plan structure

```markdown
# Plan: [Feature Name]
Date: YYYY-MM-DD
Status: Draft | In Progress | Complete

## Goal
## Expected output   (the exact TypeScript to be generated, before and after)
## Tasks
## Verification      (per `verification-before-completion`)
```

## Task template

```markdown
### Task N: [Name]
**Files:** Create `path` / Modify `path`
**Step 1: Define or change the type** (`TsModel` case, private ADT, `TsImports` helper)
**Step 2: Confirm compiler errors** — `sbt Test/compile`; expected errors in [files] because [reason]
**Step 3: Pin the output** — golden string in `src/test/scala/scalats/tests/<Suite>.scala`; confirm it fails
**Step 4: Implement**
**Step 5: Verify** — `sbt Test/compile` + `sbt test`
```

## Before writing tasks

- Which `TsParser.parse` branch produces the model, and which `TsGenerator` renderers consume it.
- Whether `TsImports.Available` already has the io-ts/fp-ts reference you need.
- Which existing suite covers the shape, or whether a new `CodecTest` suite is needed.
- Whether the change alters output for existing consumers (it then needs a version bump and a consumer check).

Order: model → parser → generator → tests. Split a task that touches more than 3 files or changes output for more than one model shape.

Execute via `executing-plans`.
