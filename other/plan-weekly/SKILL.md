---
name: plan-weekly
description: >
  .claude/todo/{annual,monthly,weekly}.md と git log を読んで今週のタスクを優先順位付きで決定し、.claude/todo/weekly.md を直接更新する（月曜の作業開始前・todo-planner を1回起動する軽量版）。NSM/メトリクス連動の戦略的計画・weekly-review 後の翌週計画は /weekly-plan の担当で別物。Use when user asks to [今週のタスクを決めて, 今週何をすべきか, weekly.md を更新して, /plan-weekly].
domain: plan
---

## 事業レビューからの選定

`docs/strategy/01_プロダクト戦略.md`、`config/business-direction.json`、`data/business/records/` の最新週次/月次判断を先に読む。重点資格・学習上の不足・販売と運営負担に沿って選ぶ。月初は `/monthly-review` の判断で、今月やるカードの `[時期:]` を付ける・直す（monthly.md は成果目標だけ・タスク表は書かない）。施策の状態は実験台帳、単発の実装はbacklogを参照し、毎週の取得・レビューを新規backlogへ量産しない。

`todo-planner` エージェントを起動して今週の計画を立て、`.claude/todo/weekly.md` を更新する。

## 使い方

```
/plan-weekly
```

引数なし。エージェントが annual / monthly / weekly と git log を自動で読む。

## 動作

1. `todo-planner` エージェントが以下を読む:
   - `config/exam-calendar.json`（試験日。annual.md は方針の文章だけで日付を持たない）
   - `.claude/todo/monthly.md`（今月の成果目標）。候補は `[時期:]` が今月を含むカード（管理画面 計画 ＞ 月間）
   - `.claude/todo/weekly.md`（前週の完了・未完了）
   - `.claude/knowledge/reference/codex-division-of-labor.md`（Codex に振れる作業の基準）
   - `git log --oneline -20`（直近の実績）
2. 今週の優先タスクを 🔴/🟡/🟢 で決定し、Codex 候補を `[Codex候補]` で明示する
3. `.claude/todo/weekly.md` を直接書き換える（確認なし）

## 呼ぶタイミング

- 月曜の作業開始前（週の始め）
- 月次ゴールが変わったとき
- 前週の計画が大幅に未達で見直したいとき

## このスキルと `/weekly-plan` の違い

| | `/plan-weekly`（このスキル） | `/weekly-plan`（既存） |
|---|---|---|
| 目的 | `.claude/todo/` の週次計画管理 | NSM・メトリクス連動の戦略的週次計画 |
| 入力 | annual / monthly / weekly / git log | GSC・GA4・PSI メトリクス + PDCA doc |
| 出力 | `.claude/todo/weekly.md` 直接更新 | `docs/reviews/weekly/YYYY-Www.md` に追記 |
| コスト | 軽量（Sonnet 1回） | 重め（複数サブエージェント並列） |
| 使う場面 | 毎週月曜のタスク整理 | 戦略的な PDCA レビュー時 |
