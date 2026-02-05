---
name: post-loop
description: playbook 完了後のブロック解除と次タスク導出を実行。
---

# post-loop

> **POST_LOOP - playbook 完了後の後処理**

---

## トリガー

### 1. pending-guard.sh によるブロック（Edit/Write が BLOCK された時）

```
🚨 post-loop 未実行 - Edit/Write ブロック中
  必須アクション:
    Skill(skill='post-loop') を呼び出してください。
```

### 2. Stop Hook によるブロック（Stop が BLOCK された時）

```
🛑 Stop ブロック: post-loop 未実行
  必須アクション:
    Skill(skill='post-loop') を今すぐ呼び出してください。
```

> **Note**: Stop Hook でのブロックは 2026-01-07 に追加されました（post-loop-fix playbook）。
> これにより、Claude が post-loop を呼ばずに終了することが防止されます。

---

## 前提条件

archive-playbook.sh（PostToolUse:Edit フック または SubagentStop 経由）が以下を自動実行済み:

> **Note**: SubAgent 内での Edit は PostToolUse:Edit Hook を発火させないため、
> SubagentStop Hook (M089) で archive-playbook.sh を補完呼び出しします。
> デバッグログ: `.claude/logs/archive-playbook.log`
- 自動コミット（最終 Phase 分）
- Push & PR 作成
- playbook アーカイブ + コミット + Push（state.md 更新前）
- state.md 更新 + コミット + Push（全アーカイブ完了後）
- PR マージ & main 同期
- pending ファイル作成（`.claude/session-state/post-loop-pending`）

---

## 行動

```yaml
1. ブロック解除（必須・最初に実行）:
   - handlers/complete.sh を実行
   - pending ファイルを削除
   - Edit/Write が再び使用可能になる

2. /clear アナウンス:
   - playbook 完了時にユーザーに以下を案内:
     ```
     [playbook 完了]
     playbook-{name} が全 Phase 完了しました。

     コンテキスト使用率を確認し、必要に応じて /clear を実行してください。
     /context で確認 → /clear で リセット可能です。
     ```

3. 次タスクの導出（計画の連鎖）★pm 経由必須:
   - pm SubAgent を呼び出す
   - pm がユーザー要求を確認
   - pm が新 playbook を作成

4. 残タスクあり:
   - ブランチ作成: `git checkout -b feat/{next-task}`
   - pm が playbook 作成: play/{id}/plan.json + play/{id}/progress.json
   - pm が state.md 更新: playbook.active を更新
   - 即座に LOOP に入る

5. 残タスクなし:
   - 「全タスク完了。次の指示を待ちます。」
```

---

## 実行方法

```bash
# Step 1: complete.sh を実行（ブロック解除）
bash .claude/skills/post-loop/handlers/complete.sh

# Step 2: 次タスク導出（pm SubAgent 経由）
# pending ステータスに応じて:
#   success: 直接 pm 呼び出し
#   partial: 手動確認後に pm 呼び出し
```

---

## 自動化フロー（archive-playbook.sh 担当）

```yaml
# PostToolUse:Edit で archive-playbook.sh が以下を自動実行:
Phase 完了検出:
  - playbook 解析（全 Phase が done か判定）

Step 1-2: 自動コミット & Push:
  - git status --porcelain で未コミット変更を確認
  - 変更あり → git add -A && git commit
  - git push origin {branch}

Step 3: PR 作成:
  - create-pr.sh を実行

Step 4-6: 自動アーカイブ（state.md 更新前）:
  - mkdir -p play/archive && mv play/{id} play/archive/
  - アーカイブのコミット（playbook 移動のみ）
  - Push（アーカイブ分）

Step 7-9: state.md 更新（全コミット後）:
  - state.md の playbook.active を null に更新
  - state.md 更新のコミット
  - Push（state.md 分）

Step 10-11: 自動マージ & 同期:
  - merge-pr.sh を実行
  - git checkout main && git pull

Step 12: pending ファイル作成:
  - .claude/session-state/post-loop-pending を作成
  - ステータス（success/partial）を記録
```

---

## pending ファイル

```yaml
location: .claude/session-state/post-loop-pending
purpose: Edit/Write ブロック制御

content_example:
  status: success  # または partial
  playbook: playbook-example
  timestamp: 2025-12-25T10:00:00Z

lifecycle:
  created_by: archive-playbook.sh
  detected_by: pending-guard.sh
  deleted_by: complete.sh
```

---

## 禁止

```yaml
- 「報告して待つ」パターン（残タスクがあるのに止まる）
- ユーザーに「次は何をしますか？」と聞く
- complete.sh を実行せずに次タスクに進む
```
