---
name: eld-sense-activation
description: |
  PCE (Process-Context Engine) のアクティブコンテキスト構築スキル。タスクに最適化されたコンテキストをコンパイルし、プロセス駆動の投入物を生成する。

  トリガー条件:
  - 新しいタスクを開始する時（「この機能を実装して」）
  - AIにコード生成を依頼する時
  - 複雑な問題解決に着手する時
  - 「コンテキストを整理して」
  - 「必要な情報をまとめて」
---

# PCE Activation Skill

潜在的コンテキストプールから、目的に最適化されたアクティブコンテキストを構築する。

## アクティブコンテキストの構造

```yaml
active_context:
  goal: |
    このタスクの真の目的
    期待する成果物
    完了条件

  constraints:
    - セキュリティ要件
    - 性能要件
    - 互換性要件
    - 禁止事項
    - 期限

  references:
    - 参照すべきドキュメント
    - 関連する既存コード
    - 過去の決定事項
    - 外部仕様

  context:
    - 実行環境
    - 依存ライブラリ
    - 前提条件

  expected_output:
    format: 成果物の形式
    quality: 品質基準
    validation: 検証方法
```

## コンパイルプロセス

### 1. Goal明確化
- 「何を達成したいか」を3行以内で言語化
- 曖昧な場合はユーザーに確認

### 2. Constraints収集
- pce-memoryからプロジェクトルール取得
- CLAUDE.mdからコーディング規約取得

### 3. References選択
- 関連性の高いものから優先
- Context budget（上限）を意識
- 必要最小限に絞る

### 4. 編集・圧縮
- 冗長な情報を削除
- 欠落を埋める
- 矛盾を解消

## Context Budget管理

| 項目 | 推奨上限 |
|------|---------|
| Goal | 3行 |
| Constraints | 5項目 |
| References | 3ファイル |
| Context | 必要最小限 |

## 使用例

```
User: ユーザー認証機能を実装して

Claude:
アクティブコンテキストを構築中...

## Goal
- JWTベースのユーザー認証機能を実装
- ログイン/ログアウト/トークンリフレッシュ

## Constraints
- セキュリティ: OWASP Top 10準拠
- 性能: レスポンス < 200ms

## References
- src/models/user.ts (既存Userモデル)
- docs/adr/ADR-003.md (認証方式決定)

## Expected Output
- src/auth/ 配下に実装
- 単体テスト必須

準備完了。実装を開始します。
```
