---
name: enforcing-doc-hierarchy
description: Audit documentation against its declared hierarchy — broken links, duplicates, misplaced content, stale references, single-source-of-truth enforcement. Use for doc health reviews.
compatibility: Designed for Claude Code
metadata:
  argument-hint: [file-directory-or-full]
  allowed-tools: Read, Grep, Glob, Edit, Bash
  stability: stable
  content-hash: sha256:383614403588863ce9c72a4d41628573c7e17debf41c6a11b30c0538baa6e2b2
---

# Enforce Documentation Hierarchy

**Scope**: $ARGUMENTS

Audits documentation against the project's declared hierarchy, then aligns
violations with user approval.

## Phase 1: Discover

The authoritative hierarchy lives where the
[qte77 doc-structure canon](https://github.com/qte77/qte77/blob/main/docs/doc-structure.md)
(SoT) places it: `CONTRIBUTING.md`'s `## Documentation hierarchy` statement. The canon's model is
`README` = the project contract, `CONTRIBUTING` = conventions + the hierarchy statement,
`AGENTS` = behavioural rules, `CLAUDE` = a one-line `@AGENTS.md` pointer (never a copy).

Read the project's declaration, looking in order:

1. `CONTRIBUTING.md` — `## Documentation hierarchy` section (canonical location; table or list)
2. `AGENTS.md` — "Key references" or "Information sources" section
3. `README.md` — "Documentation" / "Refs" section (links to authoritative docs)

Extract:

- **Entry points**: which docs are human vs agent entry points
- **Authority map**: which doc owns which content type
- **Anti-redundancy rule**: stated or implied (default: no duplication across docs)

If no hierarchy is declared, report that as the first finding and stop. Treat the canon model above
as the expected baseline and flag deviations from it.

## Phase 2: Audit

Detect violations across the scope. For each finding, record:

| Source File | Line | Type | Description |
|-------------|------|------|-------------|
| path | Lnn | type | what's wrong |

### Violation Types

- **broken-link**: Reference target does not exist (moved, renamed, deleted, wrong case)
- **duplicate**: Same content (3+ lines) appears in both an authority doc and a dependent doc
- **misplaced**: Content is in the wrong doc per the discovered authority map, OR a doc in the hierarchy is not referenced by its parent
- **lint-compat**: HTML comments before frontmatter
- **config-drift**: Inline `<!-- markdownlint-disable/enable -->` for a rule already disabled in `.markdownlint.json`. These are dead code that causes false positives when the enable directive re-activates a globally-disabled rule
- **unused-link-def**: `[key]: url` link definition with no corresponding `[text][key]` or `[key]` reference in the file

### Audit Procedure

1. **Determine scope** from `$ARGUMENTS`:
   - File: audit that file's outbound references and content placement
   - Directory: audit all `.md` files in that directory
   - `full` or empty: audit every `.md` file in the repo

2. **Check links**: For each `[text](path)` and `@file` reference, verify the
   target exists. Check case sensitivity.

3. **Check duplicates**: For each authority doc, search dependent docs for
   substantial repeated content (3+ lines or identical tables).

4. **Check placement**: For each doc, verify its content matches its declared
   authority. Flag content that belongs in a different doc per the authority map.

5. **Check chain**: Verify each doc in the hierarchy is referenced by at least
   one parent doc. Flag orphaned docs.

6. **Run markdownlint** (preferred) or manual lint check (fallback):

   **a) If `markdownlint-cli` is available** (`npx markdownlint-cli --version`
   succeeds): run it with the project config and parse output:

   ```bash
   npx markdownlint-cli -c .markdownlint.json <scope> 2>&1
   ```

   Map results to violation types: MD012 → double blanks (fix during align),
   MD053 → `unused-link-def`, MD022/MD058 → spacing issues from prior
   directive removal. Report rule ID + line + message.

   **b) Fallback** (no markdownlint available): read `.markdownlint.json`
   (or `.markdownlintrc`, `.markdownlint.yaml`) to get globally-disabled
   rules, then manually:
   - Flag files with HTML comments before frontmatter on line 1 (`lint-compat`)
   - Flag inline `<!-- markdownlint-disable/enable MDXXX -->` where MDXXX is
     already disabled in the config file (`config-drift`)
   - Grep for `[key]: url` definitions with no corresponding reference
     (`unused-link-def`)

   **In both paths**: read the lint config to detect `config-drift` — even
   markdownlint doesn't flag dead inline directives for globally-disabled
   rules. See `frontmatter-convention.md` rule for the required config
   template.

7. **Output findings table** sorted by type, then file.

## Phase 3: Align

Resolve findings with user confirmation. Propose each fix and wait for approval.

| Violation | Fix |
|-----------|-----|
| **broken-link** | Update path. If target deleted, remove reference. |
| **duplicate** | Keep in authority doc, replace in dependent doc with reference link. |
| **misplaced** | Move content to authority doc, replace original with reference link. |
| **lint-compat** | Remove HTML comments before frontmatter. |
| **config-drift** | Delete the inline directive — the rule is already handled by `.markdownlint.json`. Do NOT collapse surrounding blank lines (they may be required spacing around headings/tables). |
| **unused-link-def** | Add inline reference, or remove the definition if it serves no purpose. |

### Rules

- Fix the **authority doc first**, then fix dependents
- Never duplicate — replace with a reference
- Confirm each fix before applying
- Keep edits minimal
- **Read `.markdownlint.json` before adding any inline lint directives** — if a
  rule is globally disabled, inline toggles are dead code that causes false
  positives when the enable half re-activates the rule
- **When removing inline directives, delete only the directive line** — do NOT
  collapse surrounding blank lines (use Edit tool, not greedy `sed`)
- **Commit content changes before repo-wide lint cleanup** — never mix content
  additions with formatting passes in the same uncommitted state

### References

- `rules/frontmatter-convention.md` — required `.markdownlint.json` config
  template and anti-patterns for inline directives
