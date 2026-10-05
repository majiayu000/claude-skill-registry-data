---
name: bump-version
description: Bump the project version for release
---

リリース時にバージョンを更新するため、`scripts/bump_version.sh` を実行する（`release/*` ブランチ名から自動検出、または引数で明示指定）。

`deno.json` のみ更新しコミットする。tagは作成しない（mainで `scripts/create_release_tag.sh` を使う）。

デフォルトはpatch。minorはユーザーの明示指示時のみ。明示的に指示された時のみ実行する。
