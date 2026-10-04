---
name: doc-sync
description: Sync the repo's docs with a code diff — map changed paths to their owning docs, verify, fix, and stamp.
disable-model-invocation: true
---

# Doc Sync

You are a **Documentation Synchronizer**. Take a code diff and leave every doc that describes the changed code true again. Scope is a kind boundary, not a directory: docs live wherever the repo keeps them (`README.md`, `CONTEXT.md`, `MODULES.md`, `docs/**`); source code gets read, never edited.

## Protocol

1. **Survey** — establish what changed
2. **Confirm baseline** — one comparison spec, user-approved
3. **Map** — changed paths → owning docs (lookup first, discovery fallback)
4. **Verify & fix** — make each owned doc true again
5. **Stamp & report** — footers bumped, every path accounted for

## Step 1: Survey

Get the shape of the diff (`git` MCP op, or plain git): status, recent log, changed files. Done when you can list every changed source path with a one-line change kind — new capability, moved code home, renamed concept, removed behavior, changed boundary, changed config surface.

## Step 2: Confirm baseline

Confirm the comparison spec with the user before mapping. Default recommendation: merge-base with the repo's trunk (`main` unless the repo says otherwise). Alternatives: `uncommitted`, `back:N`, another branch. Done when the user has picked one.

## Step 3: Map changed paths to owning docs

Prefer **lookup over discovery**.

**Lookup** — when the repo has a module map (`MODULES.md`): resolve each changed path through **Lives in** to its owning module, then collect that module's doc set:

- the `MODULES.md` entry itself (**What**, **Boundary**, **Lives in**, **Uses**)
- its runbook (`docs/runbooks/`, or wherever the map points)
- its onboarding walkthrough (`docs/onboarding/`)
- the `CONTEXT.md` terms the change touches
- top-level orientation (README facts, system diagram) when the module's external edges changed
- its **See** ADRs — read to detect contradiction only. ADRs are historical record: a contradicted decision is flagged for the user as a candidate new ADR, and the old text stands.

**Discovery** — for unmapped paths, or repos without a map: search the docs for the changed symbols, names, and concepts (`context_builder` when available, direct search otherwise).

Done when every changed path is either mapped to its owning docs or declared doc-irrelevant with a reason (e.g. internal refactor beneath the map's coarse pointers). The doc-irrelevant list survives into the report.

## Step 4: Verify and fix

For each collected doc, check its claims about the changed code and fix what the diff falsified. Verification runs the same claim-type table as the `onboarding` skill (`~/.claude/skills/onboarding/SKILL.md`, Step 6); a repo contract like `docs/agents/onboarding.md` overrides both skills.

Repair claims, keep the curation: pitfalls, debugging lore, and rationale are accumulated human knowledge — correct the falsified claim inside them rather than regenerating the section. Fixes follow link-never-copy: a config value that moved belongs in the runbook, and the doc links it.

Done when every collected doc has either passed verification or been fixed.

## Step 5: Stamp and report

Stamp every onboarding walkthrough you verified or fixed — `Verified: <date> against <short HEAD commit>` as the doc's last line, added where missing. The stamp is the run's receipt: it lets the next sync (or a scheduled sweep) start from `git diff <stamped commit>..HEAD` over the module's code homes and skip docs whose code hasn't moved.

Report, accounting for every changed path from Step 1:

- **Fixed**: doc — what was false, now true
- **Verified clean**: docs checked, no drift
- **Doc-irrelevant**: paths, with reasons
- **For human judgment**: ADR contradictions, missing walkthroughs or runbooks, anything needing a decision rather than an edit
