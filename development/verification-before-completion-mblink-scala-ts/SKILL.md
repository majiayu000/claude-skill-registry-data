---
name: verification-before-completion
description: Use before declaring any task complete, claiming code works, or asserting changes are correct in scala-ts. Requires fresh command execution evidence before any completion claim.
---

# Verification Before Completion

<EXTREMELY-IMPORTANT>
NO COMPLETION CLAIMS WITHOUT FRESH VERIFICATION EVIDENCE.
Any claim of success requires executing the verification commands freshly, reading the
full output and the exit code, and confirming the result supports the claim.
</EXTREMELY-IMPORTANT>

## Verification hierarchy

### Always — when code changed

- `sbt Test/compile` — zero errors, zero warnings (`-Werror` makes them the same thing).
- `sbt test` — every suite passes, including the ts-node round-trip property (requires `cd tests && yarn` once).

### Conditional

- `sbt githubWorkflowCheck` — when `build.sbt` changed (CI runs it; regenerate with `sbt githubWorkflowGenerate`).
- A consumer check — when generated output changed: regenerate in BondLink against this checkout (see `CLAUDE.md` → "Using a local checkout from BondLink") and diff the affected files.

## A fix is unproven until you have seen the bug

For a change in generated output, the golden test must fail without the change (showing the old output) and pass with it. Run the suite before implementing, or lift the change out afterward, and record what the failure said.

## Claims that need specific evidence

| Claim | Required evidence | Not sufficient |
|-------|------------------|----------------|
| Compiles clean | `sbt Test/compile` output with `[success]` and no warnings | "Previous run passed" |
| Output is correct | Golden test passing, having been seen failing first | "Looks correct in the code" |
| Output type-checks | ts-node round-trip property passing for a suite whose `decode-encode.ts` imports the output | A golden-string match alone |
| No regressions | Full `sbt test` | "Only changed one renderer" |
| Consumer unaffected / fixed | A regenerated consumer file diffed against expectation | Reasoning about what the consumer does |
