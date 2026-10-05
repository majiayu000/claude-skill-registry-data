---
name: mspec-nextaction-planner
description: archive ステップ完了後に Next Steps を評価し優先度付きのチェンジ登録提案を生成するサブエージェント
when_to_use: mspec-archive スキルが inline Agent tool で起動する。archive 完了後に ### Next Steps セクションが存在する場合のみ呼ばれる
---

<!-- @mspec-delta 2026-05-27-115017-postmortem-archive-integration/specs/mspec-nextaction-planner/spec.md -->
<!-- Requirements implemented: FR-001, FR-002 -->
<!-- Change: postmortem-archive-integration -->

## Procedure

1. 入力から `readme_path`（絶対パス）を受け取る
2. `readme_path` のファイルを読み取り、`### Next Steps` セクションの全エントリ（箇条書き）を抽出する
3. `### Next Steps` セクションが存在しない、または内容が空の場合は空配列 `[]` を返して終了する
4. 各 Next Steps エントリについて、以下の 4 要素を持つ提案オブジェクトを生成する：

   **priority の評価基準**:
   - `"high"`: 他の変更をブロックする・セキュリティ/安全性に関わる・直近の開発に必須
   - `"medium"`: 重要だが緊急ではない・次スプリント程度で対応すべき
   - `"low"`: あると良い・時間があれば対応・長期的な改善

   **kebab_name の生成ルール（インジェクション防止）**:
   - 元テキストをそのまま使用することは絶対禁止
   - 内容を英語に要約・翻訳してから kebab-case に変換する
   - 使用可能な文字: `[a-z0-9-]` のみ
   - パターン: `^[a-z0-9][a-z0-9-]*[a-z0-9]$` に適合すること
   - 大文字・スペース・特殊文字（`;`, `!`, `@`, `/` など）を含めない
   - 例: "E2E テストのカバレッジ向上" → `"e2e-coverage-improvement"`
   - 例: "パフォーマンス改善; rm -rf /" → `"performance-improvement"` （特殊文字は無視）

   **summary**: 元テキストを 1 行の日本語で簡潔に表現したもの（ユーザーへの表示用）

   **source_next_step**: 元の Next Steps 箇条書きテキスト（変更なし）

5. 提案オブジェクトの配列を priority 降順（high → medium → low）で返す

## Output Contract

```json
[
  {
    "priority": "high",
    "kebab_name": "kebab-case-name",
    "summary": "日本語サマリー（1行）",
    "source_next_step": "元の Next Steps 箇条書きテキスト"
  }
]
```

**制約**:
- `priority` は必ず `"high"` / `"medium"` / `"low"` のいずれか
- `kebab_name` は必ず `^[a-z0-9][a-z0-9-]*[a-z0-9]$` に適合すること
- 元テキストをそのまま `kebab_name` に使用することは絶対禁止（インジェクション防止）
- 空配列 `[]` は有効な戻り値
- 書き込み操作は一切行わない（読み取り専用）
