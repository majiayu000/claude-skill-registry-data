---
name: refactoring
description: Use when refactoring code, reorganizing modules, renaming types, deleting old paths, or migrating architecture. MUST read before any structural code change. Prevents incomplete refactoring that silently breaks downstream consumers.
allowed-tools: [Read, Glob, Grep, Edit, Write, Bash, Task]
---

新パスが旧パスの全契約を継承したことを証明してから削除する。証明できなければ削除しない。

## 過去の事故

| 事故 | 原因 |
|------|------|
| ハンドラがthrowスタブ化 | 旧パス削除時に新パス未実装 |
| キャッシュが古いバージョンを返す | `--reload` 未実行 |
| importエラー | アダプタ未作成でV1 export削除 |
| 設定互換性喪失 | 移行猶予なくレガシーエイリアス削除 |

## Phase 1: 棚卸し

1. **削除対象の一覧** — 何を削除するか、誰が消費しているか、どのパラメータを受けるかを列挙する
2. **ゲートウェイ監査** — エントリ→フィルタ→ランナー→ハンドラの経路を追跡し、新パスが全パラメータを通すことを確認する
3. **消費者監査** — `grep` で全import/呼び出し箇所を特定し、移行先を決める。移行先のない消費者がいれば削除不可

## Phase 2: 契約と検証設計

4. **Before/After表** — 旧パスの各動作に対し、新パスでの実現方法を記述する。After列が空なら未完了
5. **検証設計** — パス特性に応じ、直線→コードレビュー / 分岐・フィルタ→自動テスト / 外部依存→E2Eで証明する

## Phase 3: 実行

1コミット=1関心事（新パス追加→消費者移行→旧パス削除→docs更新）。各コミットでCI通過必須。デッドコードは同一PRで削除する。

## Phase 4: 検証

```bash
deno cache --reload <entry-point>                          # キャッシュクリア
grep -r "OldName" --include='*.ts' | grep -v test          # 消費者の残存確認（空であること）
grep -r "OldName" --include='*.md'                         # docs内の参照確認（空であること）
```

## アンチパターン

| Bad | Good |
|-----|------|
| 旧パス削除→新パスは後で | 新パス完成→旧パス削除 |
| 「誰も使ってない」と推測 | grepで消費者を証拠確認 |
| リファクタと機能追加を同一PR | bisect可能に分離 |

関連: `/fix-checklist`（根本原因分析）、`/docs-consistency`（Phase 4のdocs更新）
