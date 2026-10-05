---
name: update-docs
description: Use when implementing new features, changing behavior, or modifying CLI options. Documents changes in README, related docs, and --help output. Determines appropriate documentation scope based on change type.
allowed-tools: [Read, Edit, Grep, Glob, Bash]
---

ユーザー向け変更を漏れなくドキュメント化するため、変更種別に応じて更新先を判断する。

## 更新先の判断

| 変更種別 | 必須更新先 | 任意 |
|---------|-----------|------|
| CLIオプション追加 | `--help`出力 | README（頻用なら） |
| 新機能 | README（簡潔な説明+例） | `docs/`（複雑なら） |
| 動作変更 | README該当箇所、CHANGELOG | 移行ガイド（破壊的なら） |
| 設定追加 | スキーマ、README/docs | `--help`（CLI関連なら） |
| 内部変更 | CLAUDE.md（開発影響ありなら） | なし |

## 手順

1. `git diff --name-only HEAD~1` で変更ファイル特定
2. 上表で更新先を判断
3. ドキュメント更新（簡潔に、例示優先、検索可能なキーワードを含める）
4. README.md と README.ja.md の同期確認

内部実装詳細・一時的ワークアラウンド・デバッグ専用オプションはドキュメント化しない。
