---
name: branch-management
description: Review and guide branch strategy when creating PRs, merging, or creating branches involving main, develop, and release branches
allowed-tools: [Bash, Read, Grep, Glob]
---

ブランチ戦略を管理し、誤った直接pushやマージを防ぐ。リリースフロー全体は `/release-procedure`、CI実行は `/local-ci` を参照。

## ブランチ構造

| ブランチ | 役割 | 派生元 |
|---------|------|--------|
| `main` | 本番リリース（tag対象） | - |
| `develop` | 開発統合 | - |
| `release/*` | リリース準備 | develop |
| `feature/*`, `fix/*`, `refactor/*`, `docs/*` | 作業 | develop |

```
feature/fix/refactor/* → develop → release/* → develop → main → tag
```

## ルール

| 操作 | 許可 | 禁止 |
|------|------|------|
| main変更 | developからのPRマージのみ | 直接push |
| develop変更 | 作業/releaseブランチからのPRマージ | 直接push |
| release作成 | developから派生 | main等から派生 |
| 作業ブランチ作成 | developから派生 | mainから派生 |

## マージ方法

| マージ先 | 方法 |
|---------|------|
| 作業→develop | `gh pr merge --squash` |
| release→develop / develop→main | `gh pr merge --merge` |

## クイックリファレンス

```bash
git checkout develop && git pull origin develop && git checkout -b feature/my-work  # 作業開始
gh pr create --base develop                                                          # PR作成
# 完全リリースフローは /release-procedure を参照
```
