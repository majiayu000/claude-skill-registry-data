---
name: changelog-from-commits
description: Generate a user-facing CHANGELOG entry from raw git log output. Use when the user is preparing a release, says "what changed since last version", asks to write release notes, or wants to summarize a batch of commits for end users.
---

# Changelog from Commits / 提交转更新日志

## When to use

- The user is cutting a release and needs **user-facing** release notes.
- There is a clear range: a tag, a date, or a commit SHA to diff from.
- The audience is **users**, not contributors (Conventional Commits already exists for the latter).

## When NOT to use

- The repo has **no user-facing surface** (internal libraries, scripts) — a commit log is fine.
- The range covers **months of work**. Break it into smaller releases first.
- The user wants a **marketing post** — that's [launch-tweet](../launch-tweet/SKILL.md), not a changelog.

## Approach

1. Get the raw commit list:
   ```bash
   git log <prev-tag>..HEAD --pretty=format:"%h %s%n%b" --no-merges
   ```
2. **Group** commits into three buckets, in this order:
   - **Added** — net-new user-visible capability.
   - **Changed / Fixed** — behavior that users would notice.
   - **Internal** — refactors, deps, docs (collapse into a single line at the bottom).
3. **Translate from dev-speak to user-speak.**
   - ❌ "refactor: extract validation middleware"
   - ✅ (skip — internal)
   - ❌ "fix: handle null in payment.processor"
   - ✅ "Fixed a crash when applying coupons to gift cards."
4. **Drop noise.** Typo fixes, README tweaks, CI tweaks, version bumps → cut.
5. Each bullet is **one sentence**, past tense, user perspective.
6. If a bullet needs more than one sentence, it deserves its own blog post — link out.

## Output format

```markdown
## v<version> — YYYY-MM-DD

### Added
- <bullet>

### Changed
- <bullet>

### Fixed
- <bullet>

### Internal
- <one-line summary>: deps bumped, tests added, docs polished.
```

Skip empty sections entirely.

## Worked example

**Input commits:**
```
a1b2c3d feat: add CSV export to reports
e4f5g6h fix: correct rounding in monthly totals
1a2b3c4 chore: bump axios to 1.7.5
9z8y7x6 refactor: split UserService
5d4c3b2 docs: fix typo in README
abcdef0 feat: dark mode toggle
```

**Output:**
```markdown
## v1.4.0 — 2026-04-30

### Added
- CSV export for any report — find it in the report toolbar.
- Dark mode toggle in Settings → Appearance.

### Fixed
- Monthly totals now round consistently with daily totals (off-by-1¢ on edge cases).

### Internal
- Dependency updates and a service refactor; no user impact expected.
```

## Hard rules

- **Past tense.** "Added X", not "Adds X".
- **One bullet, one sentence.** If you need a second sentence, you're explaining implementation.
- **Link to docs/blog if a feature needs context.** Don't inline tutorials.

---

## 中文版

### 何时使用

- 用户在发布版本，需要**面向用户**的更新说明。
- 有明确的范围（上个 tag、某个日期、某个 SHA）。
- 受众是**用户**，不是贡献者（Conventional Commits 给后者用）。

### 何时不使用

- 仓库**无用户访问面**（内部库 / 脚本），commit 日志够了。
- 范围跨度**几个月**——先拆成小版本。
- 用户其实想要**营销稿**——那是 launch-tweet 的活。

### 步骤

1. 拿提交列表：
   ```bash
   git log <prev-tag>..HEAD --pretty=format:"%h %s%n%b" --no-merges
   ```
2. **分三组**：
   - **新增（Added）**——新功能。
   - **变更/修复（Changed/Fixed）**——用户能感知的行为变化。
   - **内部（Internal）**——重构、依赖、文档——折叠成一行。
3. **翻译成用户能懂的话。**
4. **过滤噪声**：错别字、CI 调整、版本号 bump → 删掉。
5. 每条**一句话**，过去时，从用户视角写。

### 硬规则

- **过去时**。
- **一条一句**。需要两句说明你在解释实现细节，删掉。
- **复杂功能链接到博客或文档**，不要在 changelog 里写教程。
