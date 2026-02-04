---
name: dev:feedback
description: |
  実装完了後、学んだことをDESIGN.mdに蓄積。スキル/ルールの自己改善も提案。
  PR作成・Worktreeクリーンアップまで実行。ストーリー駆動開発の終点。
  「フィードバック」「/dev:feedback」で起動。

  Trigger:
  フィードバック, 学習事項蓄積, /dev:feedback, feedback, design update
allowed-tools:
  - Read
  - Write
  - Edit
  - Bash
  - Glob
  - Grep
  - Task
  - AskUserQuestion
---

# フィードバック → 仕様書蓄積（dev:feedback）

## 概要

実装完了後、学んだことをシステム仕様書（DESIGN.md）に蓄積。
繰り返しパターンはスキル/ルール化を提案し、meta-skill-creatorと連携。

## 入力

- feature-slug, story-slug
- 実装済みコード（git diff）
- output/フォルダのレポート（あれば）

## 出力

- `docs/features/{feature-slug}/DESIGN.md` に追記
- `docs/features/DESIGN.md`（総合設計）にも反映
- スキル/ルール化の提案

---

## ワークフロー

```
Phase 1: 変更内容の収集
    → agents/analyze-changes.md [sonnet]
    → 変更ファイル・学習事項を抽出
        ↓
Phase 2: 仕様書更新
    → agents/update-design.md [opus]
    → DESIGN.mdに設計判断を追記
        ↓
Phase 3: パターン検出
    → agents/detect-patterns.md [haiku]
    → 繰り返しパターンを検出
        ↓
Phase 4: 改善提案
    → agents/propose-improvement.md [opus]
    → スキル化/ルール化を提案
    → ユーザー承認後、meta-skill-creatorを呼び出し
        ↓
Phase 5: PR作成・Worktreeクリーンアップ
    → PR作成（gh pr create）
    → マージ後、Worktree削除
```

---

## Phase 1: 変更内容の収集

```bash
git diff --stat HEAD~5
git log --oneline -10
```

```javascript
Task({
  description: "変更分析",
  prompt: `git diffから以下を抽出してください:

1. 変更されたファイル一覧
2. 追加された機能
3. 設計判断（なぜこの構造にしたか）
4. 技術的な発見
5. 注意点・ハマりどころ

出力形式: JSON`,
  subagent_type: "general-purpose",
  model: "sonnet"
})
```

→ 詳細: [agents/analyze-changes.md](.claude/skills/dev/feedback/agents/analyze-changes.md)

---

## Phase 2: 仕様書更新

既存のDESIGN.mdがあれば追記、なければ新規作成。

```javascript
Task({
  description: "仕様書更新",
  prompt: `DESIGN.mdを更新してください。

追記内容:
- 設計判断（なぜこの構造にしたか）
- 技術的な発見
- 注意点・ハマりどころ

フォーマット: references/update-format.md を参照`,
  subagent_type: "general-purpose",
  model: "opus"
})
```

→ 詳細: [agents/update-design.md](.claude/skills/dev/feedback/agents/update-design.md)
→ テンプレート: [references/design-template.md](.claude/skills/dev/feedback/references/design-template.md)

### 更新先

| ファイル | スコープ | 更新内容 |
|----------|----------|----------|
| `docs/features/{feature-slug}/DESIGN.md` | 機能単位 | ストーリーからの学習事項 |
| `docs/features/DESIGN.md` | プロジェクト全体 | 重要な設計判断のみ |

### 更新フォーマット

```markdown
## 更新履歴

### 2024-01-21: {story-slug}

**設計判断**:
- JWTではなくセッションベース認証を採用（理由: ...）
- バリデーションはZodを使用

**学んだこと**:
- React Hook Formとの連携でのポイント
- エラーハンドリングのパターン

**注意点**:
- 〇〇の場合は△△に注意
```

---

## Phase 3: パターン検出

```javascript
Task({
  description: "パターン検出",
  prompt: `実装履歴から繰り返しパターンを検出してください。

検出対象:
- 3回以上使用したパターン
- 同じ構造のコード
- 共通の設計判断

出力形式: JSON（patterns配列）`,
  subagent_type: "general-purpose",
  model: "haiku"
})
```

→ 詳細: [agents/detect-patterns.md](.claude/skills/dev/feedback/agents/detect-patterns.md)

---

## Phase 4: 改善提案

繰り返しパターンを検出し、スキル/ルール化を提案。

```javascript
Task({
  description: "改善提案",
  prompt: `検出されたパターンをスキル/ルール化する提案を生成してください。

提案形式:
- ルール化候補: .claude/rules/ に保存
- スキル化候補: .claude/skills/ に保存

各提案に以下を含める:
- パターン名
- 適用条件
- 期待される効果`,
  subagent_type: "general-purpose",
  model: "opus"
})
```

→ 詳細: [agents/propose-improvement.md](.claude/skills/dev/feedback/agents/propose-improvement.md)
→ パターン基準: [references/improvement-patterns.md](.claude/skills/dev/feedback/references/improvement-patterns.md)

### 提案フォーマット

```markdown
💡 改善提案を検出しました

1. **ルール化候補**:
   - Zodバリデーションパターンを3回使用
   → `.claude/rules/languages/typescript/validation.md` として保存？

2. **スキル化候補**:
   - 認証フロー実装で同じ手順を実行
   → `.claude/skills/dev/auth-setup/SKILL.md` として抽出？
```

### ユーザー確認

```javascript
AskUserQuestion({
  questions: [{
    question: "これらのパターンをルール/スキルとして保存しますか？",
    header: "自己改善",
    options: [
      { label: "保存する", description: "meta-skill-creatorでルール/スキルを作成" },
      { label: "今回はスキップ", description: "保存しない" }
    ],
    multiSelect: false
  }]
})
```

**「保存する」を選択された場合**:
- meta-skill-creatorを呼び出してスキル/ルールを作成

---

## フィードバック記録

meta-skill-creatorの機構を活用:

| ファイル | 用途 | 更新タイミング |
|----------|------|----------------|
| LOGS.md | 実行記録 | 毎回実行後 |
| EVALS.json | メトリクス | 毎回実行後 |
| patterns.md | 成功/失敗パターン | パターン発見時 |

→ 詳細: [references/feedback-loop.md](.claude/skills/dev/feedback/references/feedback-loop.md)

---

## Phase 5: PR作成・Worktreeクリーンアップ

### 5.1 PR作成確認

```javascript
AskUserQuestion({
  questions: [{
    question: "PRを作成しますか？",
    header: "PR作成",
    options: [
      { label: "PRを作成", description: "gh pr create でPRを作成" },
      { label: "後で手動で作成", description: "今回はスキップ" }
    ],
    multiSelect: false
  }]
})
```

### 5.2 PR作成（選択時）

```bash
# 変更をプッシュ
git push -u origin HEAD

# PRを作成
gh pr create --title "{story-slug}" --body "$(cat <<'EOF'
## Summary
- {実装内容のサマリー}

## Changes
- {変更ファイル一覧}

## Test plan
- [ ] テストが通ること
- [ ] 動作確認

🤖 Generated with Claude Code
EOF
)"
```

### 5.3 Worktreeクリーンアップ

PRがマージされた後のクリーンアップ手順を案内:

```markdown
📋 **PR作成完了**

PRがマージされたら、以下のコマンドでWorktreeを削除してください:

\`\`\`bash
# メインブランチに戻る
cd /path/to/main/repo

# Worktreeを削除
git worktree remove ../{branch-name}

# ブランチを削除（オプション）
git branch -d {branch-name}
\`\`\`
```

**自動クリーンアップ（オプション）**:

```javascript
AskUserQuestion({
  questions: [{
    question: "PRマージ後にWorktreeを自動削除しますか？",
    header: "クリーンアップ",
    options: [
      { label: "自動削除", description: "マージ確認後にWorktreeとブランチを削除" },
      { label: "手動で削除", description: "削除コマンドを表示のみ" }
    ],
    multiSelect: false
  }]
})
```

---

## 完了条件

- [ ] 変更内容が分析された
- [ ] DESIGN.mdが更新された
- [ ] パターン検出が実行された
- [ ] 改善提案が表示された（該当あれば）
- [ ] PR作成が完了した（または手動作成を選択）
- [ ] Worktreeクリーンアップ手順を案内した

## 関連スキル

- **dev:story-to-tasks**: 次のストーリーのタスク生成
- **meta-skill-creator**: スキル/ルール作成（改善提案時に連携）

## 参照

- DESIGN.mdは「実装の記録」として育てていく
- 仕様書を最初に作るのではなく、**実装後のフィードバックで徐々に蓄積・更新**
