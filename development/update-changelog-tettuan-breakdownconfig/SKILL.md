---
name: update-changelog
description: Use when completing features, fixes, or changes that should be recorded. Updates CHANGELOG.md with concise, searchable entries following Keep a Changelog format.
allowed-tools: [Read, Edit, Grep, Glob]
---

変更履歴を検索可能に記録するため、Keep a Changelog形式でCHANGELOG.mdを更新する。

## セクション

| セクション | 使用場面 |
|-----------|---------|
| Added | 新機能 |
| Changed | 既存動作の変更 |
| Fixed | バグ修正 |
| Removed | 機能削除 |
| Deprecated | 将来削除予定 |
| Security | セキュリティ修正 |

## 記述ルール

1行で `<What>: <影響> (`識別子`)` の形式にする。実装でなくユーザー影響を書く。検索キーワードを含める。

```markdown
## [Unreleased]

### Added
- `--verbose` flag for CLI debugging output

### Fixed
- Fixed session state loss when using `--resume` with worktree
```

**Bad**: 「New feature for agents」（曖昧）、「Refactored runIteration」（実装詳細）
**Good**: 「Agent autonomous execution with `askUserAutoResponse` config option」（具体的・検索可能）

リリース時は `[Unreleased]` のエントリを `[x.y.z] - YYYY-MM-DD` に移動する。
