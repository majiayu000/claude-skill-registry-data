---
name: issues-guide
description: 実装前にノウハウを確認。Tauriコマンド追加、serde、WebSocket通信、設定項目追加、UI/オーバーレイ実装、セキュリティ関連の作業時に自動的にチェックリストを提供する。
allowed-tools: Read, Glob, Grep
---

# Issues ノウハウガイド

過去のPRレビューで蓄積したノウハウを実装前に確認するスキル。

## 必須ノウハウ（7項目）

| カテゴリ | 要点 |
|---------|------|
| **Tauri invoke** | パラメータ名は `snake_case`（[007](../../issues/007_tauri-invoke-snake-case.md)） |
| **serde** | `rename_all` の適用範囲（[021](../../issues/021_serde-field-naming.md)） |
| **入力検証** | 型ガード、上下限チェック（[013](../../issues/013_pr68-accessibility-defensive-coding.md)） |
| **セキュリティ** | URL検証、XSS、深層防御（[002](../../issues/002_overlay-security.md)） |
| **定数** | マジックナンバー禁止（[020](../../issues/020_magic-number-constants.md)） |
| **WebSocket** | bfcache対応（[010](../../issues/010_pr62-websocket-manager-bfcache.md)） |
| **アニメーション** | 二重実行防止（[022](../../issues/022_animation-callback-patterns.md)） |

## 実装タイプ別チェック

**Tauriコマンド追加**: 007, 021, 013
**WebSocket/postMessage**: 010, 002, 021
**設定項目追加**: 016, 025, 020
**UI/オーバーレイ**: 001, 022, 013

## 詳細が必要な場合

[issues/INDEX.md](../../issues/INDEX.md) を参照。
