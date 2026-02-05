---
name: steering
description: 作業指示ごとに .steering/ 配下へ requirements/design/tasklist を作成し、tasklist.md を唯一の進捗ソースとして実装を推進する。計画（作成）/実装（ループ）/振り返り（記録）の3モードで運用。「作業を計画して」「タスクリストを作成」「steering開始」「実装を進めて」などの依頼時に使用。
allowed-tools: Read, Write, Edit, Glob, Grep, Bash
---

# Steering Skill

作業を計画・追跡・振り返りするためのワークフロー管理スキル。

## 目的

- `.steering/` に「今回の作業の要求・設計・タスク」を必ず残す
- `tasklist.md` を進捗の唯一の正（Single Source of Truth）にする

## 参照ファイル

| ファイル | 読むタイミング |
|----------|----------------|
| `references/guide.md` | 詳細ルール |
| `references/templates/requirements.md` | 要求テンプレート |
| `references/templates/design.md` | 設計テンプレート |
| `references/templates/tasklist.md` | タスクリストテンプレート |

## 入出力

- 入力: ユーザーの指示（機能名/変更内容）、既存 docs（PRD/設計/アーキ等）
- 出力:
  - `.steering/<YYYYMMDD>-<slug>/requirements.md`
  - `.steering/<YYYYMMDD>-<slug>/design.md`
  - `.steering/<YYYYMMDD>-<slug>/tasklist.md`

## モード

### 1. plan モード
3ファイル作成 + tasklist具体化

### 2. implement モード
tasklist を先頭から消化し、都度更新（未完了を残さない）

### 3. reflect モード
tasklist の振り返り欄を更新（全タスク完了後のみ）

## 手順

### plan モード
1. 既存 docs を読んで方針を掴む
2. ディレクトリを作成: `.steering/<YYYYMMDD>-<slug>/`
3. テンプレから3ファイルを生成
4. tasklist を具体的なタスクに分解

### implement モード
1. tasklist を読む
2. 未完了タスクを1つ選ぶ
3. 実装する
4. tasklist を更新
5. 1に戻る

### reflect モード
1. 全タスク完了を確認
2. 振り返りを記録
3. 学びや改善点をまとめる

## tasklist.md 形式

```markdown
# タスクリスト

## 概要
- 作業名: [作業名]
- 開始日: YYYY-MM-DD
- 状態: planning / in_progress / done

## タスク

- [ ] タスク1
- [ ] タスク2
- [x] 完了したタスク

## 振り返り

（全タスク完了後に記入）
```

## 注意事項

- implement中はtasklistを頻繁に更新する
- 1タスク完了ごとにチェックを付ける
- 新しいタスクが発生したら追加する
- スコープ外のタスクは別のsteeringセッションにする
