---
name: migrate-rename
version: 1.0.0
type: skill
author: Lukas Geiger
created: 2026-03-15
updated: 2026-03-15
description: ラッパーファイルを用いた段階的なファイル名変更。ハードブレイクのない名変更を実現 — 参照は使用を通じて自然に更新されます。

standalone: true
anthropic_compatible: true
bach_compatible: false
bach_origin: true
category: dev
tags: [migration, renaming, wrapper, evolutionary, refactoring]
language: ja
status: active
dependencies: {'tools': [], 'services': [], 'protocols': [], 'python': []}
provenance: {'origin': 'bach', 'origin_path': 'system/skills/workflows/migrate-rename.md', 'origin_version': '1.0.0', 'origin_repo': 'github.com/ellmos-ai/bach', 'last_sync_from_origin': '2026-03-15', 'last_sync_to_origin': None, 'local_changes_since_sync': True}
---

<img src="../banner.png" width="100%" alt="migrate-rename banner">

> **日本語** — `migrate-rename` の公式日本語版。


# ラッパーを使用したファイル名の変更（段階的移行）(日本語)

> ハードブレイクなしでファイル名を変更できます。参照は日常の使用を通じて自然に更新されます。

---

## 原理：段階的移行

```
BEFORE:                          AFTER:
old_file.md                      new_file.md (renamed)
   |                                |
   +-- Reference A                  +-- old_file.md (wrapper)
   +-- Reference B                         |
   +-- Reference C                         +-- Log table
                                           +-- Instructions
                                           +-- Link to new_file.md
```

誰かが古いパスにアクセスしたとき：
1. ラッパーファイルに到達する
2. ログにエントリを追加する
3. ここに誘導した参照を修正する
4. 実際のファイルに進む

---

## ステップバイステップ

### 1. ファイル名を変更する

```bash
mv old_file.md new_file.md
```

### 2. ラッパーファイルを作成する

以下の内容で `old_file.md` を作成します：

```markdown
# OLD_FILE.md - REDIRECTED (Deutsch)

**Status:** This file has been renamed to `new_file.md`

---

## Migration Log

| Date | Who | Origin | Reference corrected? |
|------|-----|--------|---------------------|
| YYYY-MM-DD | [Name] | Initial migration | n/a (wrapper created) |

---

## Instructions

1. **Leave a log entry** (in table above)
2. **Check origin**: What sent you here?
3. **Correct reference**: Change `old_file.md` -> `new_file.md`
4. **Go to the actual file**: `new_file.md`

---

**Target file:** `new_file.md`
```

### 3. 重要な参照をすぐに修正する
- ヘルプファイル（主要ドキュメント）
- システムプロンプト内の参照
- パスを直接使用する CLI コード

### 4. 残りの参照を段階的に移行する
残りの参照は使用を通じて自動的に修正されます。

---

## いつラッパー手法を使用すべきか？

**はい - ラッパーが有用な場合：**
- 多数の潜在的な参照が存在する
- ファイルがさまざまなパートナーやツールから参照されている
- 重要なシステムファイルではない

**いいえ - すべて直接変更する場合：**
- 参照が少なく、把握できている
- 重要なシステムファイル（設定、DBスキーマ）
- パフォーマンスに直結するパス

---

## クリーンアップ

約30日後、またはログに新しいエントリがなくなった場合：
1. ラッパーファイルを `_archive/deprecated/` に移動する
2. または完全に削除する（新たなエントリがない場合）

---

## 変更履歴

### 1.0.0 (2026-03-15)
- BACH v3.8.0 から移植

---

*BACH v3.8.0 から移植 | スタンドアロン版*
