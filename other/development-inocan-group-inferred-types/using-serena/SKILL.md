---
name: using-serena
description: Enables token-efficient structured development via /serena command. Use for component development, API implementation, system design, test creation, bug fixes, and optimization. Available for Claude Code and all Agents.
---

# Serena Expert スキルガイド

## 📑 目次

- **SKILL.md** (このファイル): 概要と使用タイミング
- **[COMMANDS.md](./COMMANDS.md)**: /serenaコマンドの詳細使用法
- **[PATTERNS.md](./PATTERNS.md)**: 問題タイプ別の自動選択パターン

## 🎯 概要

`/serena` コマンドを使用した、トークン効率の高い構造化開発。
**Claude Code本体、Tachikoma、その他すべてのAgentで活用可能。**

## 📋 使用タイミング（自動トリガー）

- **コンポーネント開発**: UI作成、状態管理、ライブラリ統合
- **API開発**: REST/GraphQL、認証、スキーマ設計
- **システム実装**: アーキテクチャ、デザインパターン、リアルタイム機能
- **テスト**: テストスイート、モック、E2E、CI/CD
- **バグ修正・最適化**: エラー解決、パフォーマンス改善
- **複雑な問題の段階的解決**: 構造化された思考プロセス

## 🚀 クイックスタート

```bash
/serena "ログインバグ修正"           # シンプルな問題解決
/serena "検索フィルター追加" -q      # 高速実装
/serena "クエリ最適化" -c            # コード重視
/serena "認証システム設計" -d -r     # 詳細分析+リサーチ
```

詳細: [COMMANDS.md](./COMMANDS.md) 参照

## 🎯 活用推奨

| 場面 | 推奨 |
|------|------|
| Tachikoma実装作業 | `/serena`積極活用 |
| Claude Code直接作業 | `/serena`活用可 |
| 複雑な問題解決 | `/serena -d -r`推奨 |

## 🔗 関連スキル

- **implementing-as-tachikoma**: Tachikoma Agentでの活用
- **applying-solid-principles**: コード品質基準
