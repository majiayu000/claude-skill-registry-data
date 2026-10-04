---
name: scan-code-duplication
description: >-
  Scans a codebase for duplicated blocks, ranks clusters, and proposes DRY
  refactors (extract function, shared hook, utility module). Use when the user
  asks to find duplicate code, reduce repetition, DRY violations, copy-paste,
  or run a duplication audit.
---

# Scan Code Duplication

## Quick start

1. **Run the scanner** from the project root (the app repo, not only `.agents`):

```bash
python .agents/skills/scan-code-duplication/scripts/scan_duplication.py .
```

If `.agents` is not the submodule path:

```bash
python skills/scan-code-duplication/scripts/scan_duplication.py <project-root>
```

2. Read `duplication-report.md` (or pass `--stdout` for terminal-only).
3. **Triage** clusters by impact (lines × occurrences × spread across files).
4. **Refactor** top clusters using [reference.md](reference.md); re-run scanner to confirm reduction.

## When user wants fixes, not just a report

After the report:

1. Pick **1–3 highest-impact** clusters (do not refactor everything at once).
2. For each cluster, open all cited locations and confirm duplication is **logical** (not accidental similar names).
3. Apply one refactor pattern from reference.md; keep behavior identical.
4. Re-run scanner with same `--min-lines`; duplicated line count should drop.
5. Run existing tests / typecheck for touched areas.

Add `duplication-report.md` to the app repo `.gitignore` if scans run often (report is regenerated each run).

## Scanner options

| Flag | Default | Purpose |
|------|---------|---------|
| `--min-lines` | `6` | Minimum consecutive normalized lines per duplicate block |
| `--min-tokens` | `0` | Extra filter: min whitespace-split tokens in block |
| `--extensions` | common set | Comma list, e.g. `py,ts,tsx` |
| `--exclude` | see script | Extra dir names to skip |
| `--json` | off | Machine-readable output |
| `--stdout` | off | Print to terminal only (no report file) |
| `--top` | `30` | Max clusters in human report |

## Optional: jscpd (deeper token-level scan)

If Node is available and user wants industry-standard CPD-style results:

```bash
npx jscpd . --min-lines 6 --min-tokens 50 --reporters console,markdown -o ./duplication-jscpd
```

Use jscpd when: many languages, need token threshold, or Python scanner noise is high. Merge findings with the Python report; prefer clusters both tools flag.

## Agent workflow checklist

```
- [ ] Confirm project root (where package.json / pyproject / go.mod lives)
- [ ] Run scan_duplication.py on that root
- [ ] Summarize: total clusters, top 5 by duplicated lines, worst files
- [ ] For each recommended fix: pattern name + target file for new shared code
- [ ] Implement refactors only if user asked to fix (not report-only)
- [ ] Re-scan and note delta
```

## Report interpretation

- **Same file, two regions** → extract local private function or collapse with loop/data table.
- **Same module, different exports** → shared internal helper in same file or `utils/` sibling.
- **Cross-feature folders** → `lib/`, `shared/`, `utils/`, or domain package — match existing project layout.
- **Cross-language duplicates** → usually not mergeable; document as intentional or extract code generation.

**False positives to skip:** generated files, license headers, boilerplate imports, test snapshot strings, repeated JSX layout with different business logic.

## Output template (for user-facing summary)

```markdown
## Duplication audit

**Scope:** `<root>` | **Threshold:** `<min-lines>` lines

| Rank | Lines × copies | Files | Snippet hint |
|------|----------------|-------|--------------|
| 1 | … | … | … |

### Recommended refactors
1. **Cluster 1:** Extract `functionName` → `path/to/shared.ts` (reason)
2. …

### Next run
`python …/scan_duplication.py . --min-lines 6`
```

## Additional resources

- Refactor patterns and decision tree: [reference.md](reference.md)
