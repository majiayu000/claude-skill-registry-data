---
name: readme-showcase-sync
description: Audit and update Main README (README.md, README.ko.md) and User Project Website (docs/user/index.md, website/) to ensure newly added features, bundled skills, and tools are properly showcased. Use when the user requests to update the main README, sync landing pages, showcase new features on the project page, or "메인 README 누락 업데이트", "프로젝트 페이지 랜딩 업데이트", "쇼케이스 동기화", "신규 기능 README 반영".
---

# README & Showcase Sync

Audit the codebase against user-facing showcase surfaces—primarily the **Main README (`README.md`, `README.ko.md`)** and the **User Project Website (VitePress Landing & Navigation)**—to ensure new features and capabilities are prominently highlighted.

---

## 🎯 Purpose

When new features (e.g., Solution Recipes, Scheduled Tasks, Browser Sidecar, Session Export, Bundled Skills like `ig-cli`) are implemented, internal documentation (`docs/user/guides/`) is often created, but the **front door** of the project—the Root `README.md` and the user-facing project website landing page—lags behind.

This skill automates:

1. Detecting features implemented in code but omitted from `README.md` and `docs/user/index.md`.
2. Planning concise, high-impact showcase updates.
3. Synchronizing main English & Korean READMEs and VitePress landing pages.

---

## 🔄 Workflow

### Step 1 — Audit Showcase Surfaces

Run the automated showcase audit script:

```bash
python3 .agents/skills/readme-showcase-sync/scripts/audit_showcase.py . --output .libragent/tmp/showcase-audit.json
```

The script reports:

- Features missing in Main `README.md`
- Features missing in Korean `README.ko.md`
- Features missing in Project Website Landing (`docs/user/index.md` / `en/index.md`)
- Features missing in VitePress Navigation (`website/.vitepress/config.ts`)

### Step 2 — Review & Select High-Impact Additions

Filter the audit results by user value:

- **P0 Highlights**: Core user-facing workflows (e.g., `recipes`, `scheduled-tasks`, `browser-sidecar`, `session-export`, `ig-cli`).
- **P1 Capabilities**: System/governance features (e.g., `session-isolation`, `soul-lounge`, `compact-planning`).
- **P2 Minor/Dev tools**: Can remain in dedicated guides rather than cluttering the front landing.

### Step 3 — Propose Plan & Obtain User Approval

> [!IMPORTANT]
> **Git Protection Rule (`AGENTS.md`)**: `README*.md`, `docs/`, and `website/` are git-protected files.
> **DO NOT** modify these files without explicit user confirmation.
>
> 1. Present the list of missing features to showcase.
> 2. Show the exact proposed sections in `README.md` and `docs/user/index.md`.
> 3. Await user confirmation before writing changes.

### Step 4 — Synchronize Showcase Surfaces

1. **Main README (`README.md`)**:
   - Add to "What You Can Do in the First 10 Minutes" or "Platform Features".
   - Keep descriptions action-oriented and evidence-based.
2. **Korean README (`README.ko.md`)**:
   - Mirror the changes with natural Korean terminology.
3. **Project Website Landing (`docs/user/index.md` & `en/index.md`)**:
   - Add feature highlight cards or links under "가이드 / Features".
4. **VitePress Sidebar (`website/.vitepress/config.ts`)**:
   - Ensure corresponding guides are registered in `koSidebar` and `enSidebar`.

### Step 5 — Validate & Format

Run lightweight formatting and website build validation:

```bash
# Verify formatting
pnpm prettier --check "README.md" "README.ko.md" "docs/user/index.md" "website/.vitepress/config.ts"

# Verify VitePress builds cleanly without broken links
pnpm docs:build
```

_(Note: Never run full repository heavy pipelines like `pnpm refactor:validate` unless explicitly requested by the user.)_

---

## 📋 Guidelines

- **Concise & Scannable (KISS)**: The front door must not become an unreadable wall of text. Focus on what the user can _do_ with the feature.
- **Language Parity**: Whenever `README.md` is updated, ensure `README.ko.md` is synchronized.
- **Link Accuracy**: Every showcase feature must link directly to its deep guide in `docs/user/guides/`.
