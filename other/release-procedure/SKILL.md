---
name: release-procedure
description: Use when user says 'release', 'リリース', 'deploy', 'publish', 'vtag', 'version up', 'バージョンアップ', or discusses merging to main/develop. Guides through version bump and release flow.
allowed-tools: [Bash, Read, Edit, Grep, Glob]
---

リリースフロー全体を管理する。ブランチ戦略は `/branch-management`、CI実行は `/local-ci` を参照。

バージョンは `deno.json` の `version` フィールドのみで管理する。

## フロー

```
develop → release/x.y.z → (bump & CI) → PR→develop → PR→main → tag → JSR publish
```

## 手順

1. `git checkout develop && git pull origin develop && git checkout -b release/x.y.z`
2. `scripts/bump_version.sh` でバージョン更新（`grep '"version"' deno.json` で確認）
3. `deno task ci` でCI確認
4. `git push -u origin release/x.y.z`
5. `gh pr create --base develop` → CI通過後 `gh pr merge --merge`
6. `gh pr create --base main --head develop` → CI通過後 `gh pr merge --merge`
7. `git checkout main && git pull origin main && scripts/create_release_tag.sh`
8. `git branch -d release/x.y.z && git push origin --delete release/x.y.z`

## 連続マージ禁止

各PRマージ後、必ずユーザーの明示的指示を待つ。独自判断でdevelop→mainマージやtag作成をしない。

## トラブルシューティング

| 問題 | 原因と対処 |
|------|-----------|
| JSR publishスキップ | deno.jsonバージョンが既存と同じ → bump再実行 |
| CIバージョンチェック失敗 | deno.jsonとブランチ名不一致 → `scripts/bump_version.sh` 再実行 |
| tagが古いコミット | `git tag -d vx.y.z && git push origin :refs/tags/vx.y.z` → `scripts/create_release_tag.sh` |
