---
name: winget-release
description: GistGetのWinGetパッケージリリースを支援。(1) 新バージョンのリリース、(2) WinGetマニフェスト作成・更新、(3) winget-pkgsへのPR作成。「WinGetにリリース」「winget-pkgsにPR」「マニフェスト作成」などのキーワードで使用。
---

# GistGet WinGet リリース

GistGetをWinGetパッケージとしてリリースするためのスキル。

## クイックスタート

### リリース手順

**手順**
1. `src/GistGet/GistGet.csproj` の `<Version>` を更新
2. `CHANGELOG.md` を更新（新バージョンのエントリを追加）
3. 変更をコミット・プッシュ
4. プレビュー実行（任意）
5. `skills/winget-release/scripts/Publish-WinGet.ps1` でリリース実行

```powershell
# 1. バージョン更新
# src/GistGet/GistGet.csproj の <Version> を編集
# CHANGELOG.md にエントリを追加

# 2. コミット・プッシュ
git add .
git commit -m "chore: bump version to 1.0.7"
git push origin main

# 3. プレビュー実行（任意）
.\skills\winget-release\scripts\Publish-WinGet.ps1 -Version 1.0.7 -DryRun

# 4. フルリリースパイプライン
.\skills\winget-release\scripts\Publish-WinGet.ps1 -Version 1.0.7
```

**重要事項**:
1. 必ずバージョン更新とCHANGELOGの変更をコミット・プッシュしてからリリーススクリプトを実行してください。そうしないとタグが正しく付与されません。
2. スクリプトは日本語のリリースノートをUTF-8ファイル経由で`gh release create`に渡すため、文字化けは発生しません。

## リリースの流れ

### Publish-WinGet.ps1（唯一のリリースフロー）

PowerShell Coreスクリプト `Publish-WinGet.ps1` が以下のステップを実行します:

```
品質チェック → ビルド/ZIP/SHA256 → タグ作成/プッシュ → GitHub Release → winget-pkgs同期 → マニフェスト生成 → PR作成
```

```pwsh
.\Publish-WinGet.ps1 -Version 1.0.4
```

**重要**: Publish-WinGet.ps1が唯一のリリースフローです。GitHub Actionsのrelease.ymlは削除されました（ハッシュ不一致の問題を防ぐため）。

## PR作成

### 自動（Publish-WinGet.ps1）

スクリプトが自動でwinget-pkgsへPRを作成します。

## 参照ファイル

- **GistGet固有情報**: [references/gistget-context.md](references/gistget-context.md)
