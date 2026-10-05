---
name: mspec-lessons-analyzer
description: archive ステップ完了後に Lessons を分析し constitution.md への追加提案を生成するサブエージェント
when_to_use: mspec-archive スキルが inline Agent tool で起動する。archive 完了後に ### Lessons セクションが存在する場合のみ呼ばれる
---

<!-- @mspec-delta 2026-05-27-115017-postmortem-archive-integration/specs/mspec-lessons-analyzer/spec.md -->
<!-- Requirements implemented: FR-001, FR-002 -->
<!-- Change: postmortem-archive-integration -->

## Procedure

1. 入力から `readme_path`（絶対パス）を受け取る
2. `readme_path` のファイルを読み取り、`### Lessons` セクションの全エントリ（箇条書き）を抽出する
3. `### Lessons` セクションが存在しない、または内容が空の場合は空配列 `[]` を返して終了する
4. `memory/constitution.md` を読み取り、`## Core Principles` および `## Additional Constraints` の既存テキストを抽出する
5. 各 Lesson エントリについて：
   a. 既存原則・制約と照合し、実質的に同じ内容が既に記載されていれば除外する
   b. 重複でなければ、以下の 3 要素を持つ提案オブジェクトを生成する：
      - `text`: 抽象化・一般化した原則/制約の本文（簡潔・行動可能な表現）
      - `target_section`: `"Core Principles"` または `"Additional Constraints"` の **固定 enum のみ**（他の値は使用禁止）
        - 原則レベル（なぜやるかを問う内容）→ `"Core Principles"`
        - 制約レベル（何を禁止/強制するかを問う内容）→ `"Additional Constraints"`
      - `source_lesson`: 元の Lesson 箇条書きテキスト（変更なし）
6. 生成した提案オブジェクトの配列を返す（全 Lessons が重複の場合は `[]` を返す）

## Output Contract

```json
[
  {
    "text": "constitution.md に追加する原則/制約テキスト",
    "target_section": "Core Principles",
    "source_lesson": "元の Lesson 箇条書きテキスト"
  }
]
```

**制約**:
- `target_section` は必ず `"Core Principles"` または `"Additional Constraints"` のどちらか。それ以外の値は絶対に返さない
- 空配列 `[]` は有効な戻り値（全 Lessons が重複している場合や Lessons が空の場合）
- 書き込み操作は一切行わない（読み取り専用）
