---
name: vitepress-doc-sync
description: Analyze recent git commits and codebase changes to update, synchronize, and align VitePress documentation (docs/user/ and website/). Use when the user requests to update documentation from git diffs, sync VitePress docs, audit doc gaps, or update user guides after code changes. Triggers on "vitepress 문서 현행화", "git 변경사항으로 문서 업데이트", "최신 git commit 반영하여 docs 업데이트", "vitepress-doc-sync", "sync docs with git", "update vitepress docs", "doc sync".
---

# VitePress Doc Sync

Analyze recent Git commits, PRs, and codebase diffs to detect outdated, missing, or inconsistent user-facing documentation in VitePress (`docs/user/` and `website/`), and synchronize them to reflect the latest state of the codebase.

---

## Workflow Decision Tree

```
1. Run Gap Analysis Script
   └─ python .agents/skills/vitepress-doc-sync/scripts/detect_doc_gaps.py --since <GIT_REF>
2. Inspect Code Changes
   └─ Review git log / diff & consult references/git_diff_analysis_guide.md
3. Update Target Docs
   └─ Edit corresponding Korean (docs/user/*.md) and English (docs/user/en/*.md) pages
4. Sync VitePress Config
   └─ If new files added, update website/.vitepress/config.ts (koSidebar & enSidebar)
5. Build & Validate
   └─ Run pnpm --filter website build or pnpm refactor:validate
```

---

## Step 1: Detect Documentation Gaps

Run the automated gap detection script to inspect recent git commits and find unindexed markdown files:

```bash
python .agents/skills/vitepress-doc-sync/scripts/detect_doc_gaps.py --since HEAD~10
```

This generates `.agents/skills/vitepress-doc-sync/doc_gaps_report.json` summarizing:

- Changed codebase areas (MCP tools, Rust backend, frontend UI, skills, etc.)
- Markdown files in `docs/user/` that are not listed in the VitePress sidebar navigation.

---

## Step 2: Analyze Git Diffs & Map to Docs

Inspect changed codebase files and map them to their target documentation files:

1. **Consult Mapping Guide**: Read [references/git_diff_analysis_guide.md](references/git_diff_analysis_guide.md) for domain-specific mappings (e.g. MCP tools → `guides/builtin-tools.md`, Skills → `guides/skills.md`).
2. **Identify Impact**:
   - Added features or parameters → Add explanations to user docs.
   - Deprecated or renamed APIs/CLI flags → Update existing references.
   - New configuration options → Update configuration guides or FAQ.

---

## Step 3: Edit & Update Documentation Pages

Follow VitePress formatting guidelines in [references/vitepress_formatting_guide.md](references/vitepress_formatting_guide.md):

- Update both **Korean docs** (`docs/user/*.md`) and **English docs** (`docs/user/en/*.md`) to maintain language parity.
- Add page frontmatter (`title`, `description`) if missing.
- Use VitePress custom containers (`::: tip`, `::: info`, `::: warning`, `::: danger`) for callouts and notes.
- Ensure code block snippets use accurate syntax highlighting and valid parameters.

---

## Step 4: Sync VitePress Sidebar & Navigation

If new `.md` files were created in `docs/user/` or existing files were reorganized:

1. Open `website/.vitepress/config.ts`.
2. Register the new page under the appropriate category in `koSidebar`:
   ```typescript
   { text: '새 기능 제목', link: '/guides/new-feature' }
   ```
3. Register the corresponding English page in `enSidebar`:
   ```typescript
   { text: 'New Feature Title', link: '/en/guides/new-feature' }
   ```

---

## Step 5: Validate VitePress Site Build

Verify that VitePress compiles cleanly without dead links or syntax errors:

```bash
pnpm --filter website build
```

Or perform full project validation:

```bash
pnpm refactor:validate
```
