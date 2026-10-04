---
name: adapter-drift-audit
description: Use when checking whether an IronLint adapter still matches its coding harness's current contract — auditing adapter/harness drift, verifying hook payload shapes, plugin manifest schemas, lifecycle events, or tool names are up to date, or doing periodic adapter maintenance. Takes a harness name (claude-code, codex, pi, opencode) as argument.
---

# Adapter Drift Audit

Audit an IronLint adapter against its coding harness's **current** contract and report drift.

**Read-only.** You produce findings and recommendations. You do NOT edit adapter files, you do NOT write the watermark, and you do NOT audit `ironlint` core. The maintainer reads the report and decides what to change.

## When to use

- "Is the claude-code adapter still up to date with Claude Code's hooks?"
- Periodic adapter maintenance / contract-drift sweeps.
- After a harness ships a new version and you want to know what the adapter missed.

## Inputs

A harness name as the invocation argument: `claude-code`, `codex`, `pi`, or `opencode`. Each maps to `references/<harness>.md`. Only harnesses with a reference file can be audited.

### Codex specifics

Codex is a `PreToolUse`-hook harness like claude-code, but its own docs frame the hook as a *guardrail*, not a hard enforcement boundary — factor that into impact judgments (a codex drift degrades a guardrail; the same drift on claude-code degrades the enforcement point itself).

- **Doc sources**: `developers.openai.com/codex/hooks` (hooks reference) and the `codex-rs/hooks/` source tree (ground truth for the exit/JSON decision contract — re-audit for the selected version; current implementation details are in `adapters/codex/README.md`).
- **Re-verify first**: the `tool_input.command` `apply_patch` envelope shape (`*** Begin Patch` / `*** Add File:` / `*** Update File:` / `*** Delete File:` / `*** End Patch`) that `adapters/codex/hooks/hook.sh`'s python3 parser depends on. This is the single most drift-prone contract in the codex adapter — the parser fails closed (deny) on an envelope it doesn't recognize, so drift here surfaces as edits getting wrongly blocked rather than silently let through, but it's still the first thing to re-check.

## Procedure

### 0. Resolve target

Read the invocation argument as the harness name. Load `references/<harness>.md`. If no argument was given, list the harnesses that have a reference file under `references/` and stop — ask which one.

### 1. Read the watermark

The reference's **Watermark** section gives the baseline version / changelog date the adapter was last verified against. Note it; it scopes the changelog read in step 2.

### 2. Fetch current truth

For each entry in the reference's **Doc sources**, in this order:

1. **Context7 first** (repo + global convention). The reference's **Doc sources** pin exact library IDs (`/websites/code_claude`, `/anthropics/claude-code`), so skip `resolve-library-id` — the global "always resolve first" rule doesn't apply when the ID is already known. Call `query-docs` directly on each pinned ID for the contracts under audit.
2. **GitHub `CHANGELOG.md` since the watermark** — the primary signal for *what changed*. Fetch the changelog and read entries newer than the watermark.
3. **Web docs** — fallback / cross-check for any contract Context7 didn't cover.

If a source is unreachable, note it; the affected contracts become ❓ unverifiable in the report rather than silently ✅.

### 3. Compare each contract

For every row in the reference's **Contract surface map**: read the cited adapter `file:line`, compare it to the fetched truth, and classify:

- ✅ **in-sync** — adapter matches the current contract.
- ⚠️ **drift** — the contract changed; the adapter is stale.
- ❓ **unverifiable** — couldn't fetch authoritative truth this run (say which source failed).
- ✨ **new-capability-not-adopted** — the harness now offers something relevant the adapter doesn't use. A best-practice gap, not a bug.

Re-read the adapter file rather than trusting the line number — anchors drift as the adapter changes.

### 4. Emit the report

Use the **Report format** below exactly.

### 5. Propose a watermark bump

Print the suggested new `Last verified` line under a **Proposed watermark** heading. Do NOT write it into the reference file — the maintainer updates it when they act on the report. This keeps the audit read-only.

## Report format

```
# Adapter drift audit — <harness> (<date>)
Baseline: <watermark>   Current: <version / changelog date observed>

## Drift (⚠️)
- [contract #N: <name>] <adapter file:line>
  now: <current-truth summary>   (source: <doc link / Context7 id>)
  was: <what the adapter assumes>
  recommend: <concrete change>

## New capabilities not adopted (✨)
- <name> — <what it enables> (source: …) — adapter still correct.

## Unverifiable (❓)
- [contract #N] <which source was unreachable>

## In sync (✅)
- <contract #N>, <contract #M>, …

## Proposed watermark
Last verified: <date> against <harness> <version> (changelog entry: <ref>)
```

## Rules

- **Read-only**: never edit adapter files or the watermark; only report.
- **Context7 first** for schema shape; **GitHub `CHANGELOG.md`** is canonical for *what changed and when*.
- **Impact over difference**: use the reference's Thesis to judge whether a drift actually breaks gating, or is cosmetic.
- **No silent ✅**: a contract you couldn't verify is ❓, not ✅.
- **Omit empty sections** (⚠️ / ✨ / ❓) from the report; always show the ✅ summary and the Proposed watermark.
