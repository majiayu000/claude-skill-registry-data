---
name: docs-consistency
description: Verify and fix documentation to match implementation. Use when updating docs, releasing versions, or when user mentions 'docs consistency', 'docs update', 'docs verify', 'ドキュメント更新', '最新にして', 'docsを直して'. Extracts design intent, investigates implementation, then updates docs accordingly.
allowed-tools: [Read, Edit, Grep, Glob, Bash, Write]
---

ドキュメントが実装と乖離するのを防ぐため、設計意図→実装調査→差分検出→更新の順で整合性を確保する。設計ドキュメントは変更しない。

## フェーズ

1. **設計意図抽出** — `docs/internal/` を読み、`tmp/docs-review/{feature}-intent.md` にWhat/Why/制約を記録
2. **実装調査** — 実装ファイル・API・デフォルト値・エッジケースを `tmp/docs-review/{feature}-implementation.md` に記録
3. **差分検出** — intent + implementation と現行docsを比較し、差分テーブルを作成
4. **更新** — README.md → README.ja.md → docs/guides/ → --help の優先順で更新（設計docsは読み取り専用）
5. **検証** — `deno task verify-docs`。ファイル追加・削除時は `deno task generate-docs-manifest`
6. **言語** — `*.md` は英語必須、`*.ja.md` は日本語（JSR配布対象外）

## メモの後処理

低価値→`tmp/docs-review/` 削除。PR背景に有用→PR引用。設計記録として保存→`docs/internal/changes/` に昇格。

詳細は SEMANTIC-CHECK.md, IMPLEMENTATION-CHECK.md, operational-guide.md を参照。
