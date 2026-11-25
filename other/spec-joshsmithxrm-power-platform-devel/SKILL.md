---
name: spec
description: Create, update, reconcile, or audit a PPDS specification in specs/. Use when writing a spec for new feature work, changing what an existing spec says, aligning a spec with code that has drifted from it (--reconcile), or checking specs against code and tests without changing them (--audit). Not needed for bug fixes or small contributor changes.
---

# Spec

`$ARGUMENTS` = spec name (`connection-pooling` → `specs/connection-pooling.md`), optionally followed by `--reconcile` or `--audit`. For `--audit`, an empty name means every spec.

## Foundation

- `specs/CONSTITUTION.md`: Part 1 (architecture principles) applies to everything a spec describes; Part 2 (I3, I6, SL1–SL5) governs the spec itself.
- `specs/SPEC-TEMPLATE.md`: structure. Address every section, even if only with "N/A".
- Code-to-spec map: grep `specs/*.md` for `**Code:**` lines and match path prefixes against the code in question. This, not `specs/README.md`, is how to find governing and related specs. Several specs can share a path; consider all of them. Always treat `specs/architecture.md` as related.

## `**Code:**` frontmatter (SL4)

Relative, grep-friendly path prefixes, e.g. `[src/PPDS.Cli/Commands/PluginTraces/](../src/PPDS.Cli/Commands/PluginTraces/)`. Never prose ("Multiple — see sections") and never `None` once code exists. System-wide specs use `**Code:** System-wide`. When work adds code in a new location, add its prefix so the map keeps finding the spec.

## Modes

**Create** (spec file does not exist). Check the map and spec names for overlapping scope first; if a spec already covers the concept, ask whether to extend it (SL1: one spec per domain concept, named after the thing; SL3: surface behaviour goes in surface sections). Draft section by section with the user. Capture their intent; ask rather than invent requirements. Changelog starts with "Initial spec".

**Update** (user asks for changes). Read the spec and the code at its `Code:` paths, report any drift you see, then make the requested changes once the user agrees.

**Reconcile** (`--reconcile`, or update mode finds significant drift).
1. Extract the spec's ACs, Code paths, and described types.
2. Enumerate public types, methods, and behaviours at those paths.
3. Classify: missing ACs (code behaviour with no AC), stale ACs (behaviour the code no longer has), status drift (test result differs from the Status column).
4. Member-count check: count public types/methods and count ACs, and report the delta. Warn explicitly if ACs cover under 90% of the public surface; summaries tend to capture 70–80% and miss the rest.
5. Compare Architecture and requirement prose against the actual structure.
6. Present all proposed changes for approval before writing. If nothing drifted, say the spec is current and write nothing.

**Audit** (`--audit`). Read-only: report findings with file/test evidence and the change each one needs; fix nothing. For a full audit, glob `specs/*.md` excluding CONSTITUTION, SPEC-TEMPLATE, and README; parallel subagents per spec are fine. Per spec, check:
- **ACs**: a numbered AC table exists (I3); each referenced test exists (grep for it) and its Status is accurate. Run single tests to confirm:
  - .NET: `dotnet test PPDS.sln --filter "FullyQualifiedName~{TestMethod}" -v q`
  - Extension (vitest, from repo root): `npm test --prefix src/PPDS.Extension -- -t "{test name}"`. `-t` matches the `describe`/`it` name, not a function name; a file path in place of `-t ...` runs one file.
- **Code alignment**: requirements, architecture, and core types against the code, as matches, drifted, missing (spec claims it, code lacks it), or extra (code does it, spec is silent).
- **Constitution**: A1–A3 and R1–R3 for any spec with code; D1–D4 for Dataverse specs; SS1–SS2 for profile, environment, or MCP session specs; I1 for CLI output; S1–S3, I4, and I5 for UI specs; SL1–SL5 for every spec.
- **Cross-spec**: contradictions with the specs in its Related Specs section.

Treat audit findings with reconcile mode.

## Finish (create, update, reconcile)

1. Numbered, testable ACs (AC-01, ...), with a `Test` column (`TBD` is fine for new work) and an accurate `Status` (I3, I6).
2. Append a dated row to `## Changelog`. Update `**Last Updated:**`.
3. Regenerate the index: `python scripts/generate-spec-readme.py`. `specs/README.md` is generated; never hand-edit it.
4. Commit as `docs(specs): add|update {spec-name} specification`.
