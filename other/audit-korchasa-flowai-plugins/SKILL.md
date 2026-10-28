---
name: audit
description: >-
  Use when the user asks to audit a memex (long-term knowledge bank for AI
  agents) for orphans, dead SALP REFs, missing sections, contradictions or index
  drift. Runs a structural check, layers LLM-judgement findings, auto-fixes
  trivia with `--fix`.
argument-hint: '[--fix]'
---

# Memex Audit

Health check for the memex (long-term knowledge bank for AI agents). Runs a deterministic script first, then layers LLM-judgement checks on top.

## When to invoke

Invoked when the user wants a memex health check (e.g., "audit my memex", "check the memex for dead links", `/flowai-memex:audit` for audit-only or `/flowai-memex:audit --fix` to apply trivial auto-fixes).

## Memex Resolution

Same protocol as the other memex skills:
1. `--memex <path>` flag → use that path.
2. Walk up from cwd looking for an ancestor with both `AGENTS.md` and `pages/`.
3. Otherwise stop with: `No memex found. Pass --memex <path> or cd into a memex directory.`

Read `<memex-root>/AGENTS.md` for the schema.

## Audit Steps

### 1. Run the deterministic check

Run the audit script bundled with this skill:

```bash
deno run --allow-read scripts/audit.ts <memex-root>/pages/
```

(The path is relative to this skill's installed directory — `<ide-config-dir>/skills/audit/scripts/audit.ts`, e.g. `.codex/skills/audit/scripts/audit.ts` or `.claude/skills/audit/scripts/audit.ts`. Run it from the project root with that path, or pass an absolute path.)

The script parses SALP REFs (`[REF:mx-<type>:<slug>]`). It reports five issue kinds, one per line:
- `DEAD_LINK: [REF:mx-*:<target>] in <file>` — SALP REF points to a non-existent page.
- `ORPHAN: <file> has no inbound [REF:mx-*:...]` — page is not linked from anywhere except itself.
- `MISSING_SECTION: <file> (concept) lacks 'Counter-Arguments and Gaps'` — concept page missing the gaps section.
- `INDEX_MISSING: <file> not listed in index.md` / `INDEX_DEAD: index.md references [REF:mx-*:<slug>] which has no file` — drift between filesystem and `pages/index.md`.
- `MALFORMED_REF: <file>:<line>: <raw>` — `[REF:...]` token that violates the `mx-<type>:<slug>` grammar (wrong namespace, empty slug, etc.).

### 2. Layer LLM-judgement checks

The script handles structure. The following require reading content:

- **Contradictions**: `grep -rln "\[!WARNING\]" <memex-root>/pages/` to find every callout marker. List them — these need human resolution.
- **Stale claims**: read each page with `date` older than 6 months. Flag any whose claims are likely outdated (rapidly-changing fields).
- **Unlinked concept mentions**: scan page bodies for proper nouns and technical terms that appear in prose without a SALP REF even though a corresponding page exists. Add `[REF:mx-<type>:<slug>]` at the first natural mention if `--fix`, else just suggest.
- **Coverage gaps**: read `index.md` and identify domains with only 1–2 pages. Suggest 3–5 questions the memex cannot yet answer well — candidates for `ask` or further `save`.

### 3. Apply auto-fixes (only if `--fix`)

For each issue with a trivial deterministic fix, apply it:

| Issue | Auto-Fix |
|---|---|
| `DEAD_LINK` | Create stub page at the link target with the closest matching template (default: concept). Stub body: `# <Slug as Title> [ANC:mx-concept:<slug>]\n\n_Stub created by audit. Needs content from a source._\n\n## See Also\n- [REF:mx-concept:<page that linked to it>]`. |
| `MISSING_SECTION` | Append empty `## Counter-Arguments and Gaps\n\n_None recorded yet._` to the concept page. |
| `INDEX_MISSING` | Add the page to `index.md` under a domain derived from its `tags` frontmatter. |
| `INDEX_DEAD` | Remove the dead row from `index.md`. |
| `ORPHAN` | NOT auto-fixed — finding a sensible inbound page requires judgement. List it for the user. |
| `[!WARNING]` contradiction | NOT auto-fixed — surface for human review. |
| Stale-claim suspicion | NOT auto-fixed — surface for human review. |
| Unlinked concept mention | Add `[REF:mx-<type>:<slug>]` at the first natural mention only when `--fix` is set AND the target page exists. Otherwise just suggest. |
| `MALFORMED_REF` | NOT auto-fixed — surface for human review (typically requires choosing the right `mx-<type>` namespace). |

### 4. Write an audit report

Write `<memex-root>/outputs/reports/YYYY-MM-DD-audit.md` (create `outputs/reports/` if missing):

```markdown
# Memex Audit Report — YYYY-MM-DD

**Memex:** <memex-root> | **Issues:** N | **Auto-fixed:** M

## Critical
- DEAD_LINK: ... (auto-fixed: stub created at <path>)
- ...

## Warnings
- ORPHAN: ... — suggest linking from <candidate>
- ...

## Suggestions
- 3–5 questions the memex cannot yet answer:
  1. ...
  2. ...

## Contradictions
- <file>:<line>: <one-line summary> — needs human resolution
```

### 5. Append `log.md`

```
## [YYYY-MM-DD] audit | <total> issues, <fixed> auto-fixed
<one-line summary of the worst class of issue>
```

### 6. Report to user

Print a compact summary:
- Total issues by severity.
- Auto-fixed count and what kinds.
- Path to the full report under `outputs/reports/`.
- The 3–5 suggested research questions (so the user sees them without opening the report).

## Constraints

- Never auto-delete pages — `INDEX_DEAD` removes index rows, but the underlying file (if it exists) stays.
- Never auto-resolve contradictions — they need human judgement.
- Never auto-rewrite the body of an existing page — only append (e.g., the missing-section fix appends a new section). Other body changes must be human-reviewed.
- Use `Read`, `Glob`, `Grep`, `Bash` (for the deterministic script and for `grep`), `Edit` (for `index.md`, `log.md`, and append-only fixes), `Write` (for stub pages and the audit report).
- Without `--fix`, the audit skill is read-only on the memex except for the report file and `log.md`.
