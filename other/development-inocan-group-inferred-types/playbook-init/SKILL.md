---
name: playbook-init
description: タスク開始フローのエントリーポイント。prompt-analyzer の分析結果を受け取り、pm SubAgent に委譲する。
---

# playbook-init Skill

> **このSkillは prompt-analyzer の分析結果を受け取る。再分析しない。**
>
> **設計原則**: 分析は Hook チェーンで完了済み。この Skill は pm への橋渡しを担当。

---

## Purpose

Hook → prompt-analyzer → Skill → SubAgent チェーンの Skill 層を担当。
**prompt-analyzer の分析結果を pm に受け渡す**（再分析しない）。

---

## When to Use

```yaml
triggers:
  - prompt-analyzer が topic_type=instruction と判定した時
  - playbook=null の状態でタスク依頼を受けた時

invocation:
  - Skill(skill='playbook-init', args='analysis_result={分析結果}')
  - /playbook-init

前提条件:
  - prompt-analyzer が既に呼び出され、分析結果が存在すること
  - topic_type が instruction であること
```

---

## Required Action

**以下のステップを順番に実行せよ。スキップ禁止。**

### Step 0: 前提チェック（自分で実行）

```bash
echo "=== 前提チェック ===" && \
echo "1. 既存 playbook:" && ls plan/playbook-*.md 2>/dev/null | head -3 || echo "(なし)" && \
echo "2. git 状態:" && git status --short && \
echo "3. ブランチ:" && git branch --show-current
```

| 条件 | 対応 |
|------|------|
| 未コミット変更がある | ユーザーに確認 |
| main ブランチにいる | 作業ブランチを作成 |
| 既存 playbook あり | ユーザーに上書き確認 |

---

### Step 1: 分析結果の確認（Hook 経由で取得済み）

**prompt-analyzer は Hook チェーンで既に呼び出されている。再呼び出し禁止。**

```yaml
入力:
  - analysis_result: Hook チェーンで取得した prompt-analyzer の出力
  - user_prompt: ユーザープロンプト原文

確認項目:
  - analysis_result が存在するか
  - topic_type が instruction であるか
  - ready_for_playbook の値

分岐:
  analysis_result が存在しない場合:
    → エラー: "prompt-analyzer が呼び出されていません"
    → Hook チェーンを確認

  ready_for_playbook: false の場合:
    → blocking_issues を解決してから次へ
    → ユーザーに確認が必要
```

**★チャット上に分析結果を表示（必須）★**:

分析完了後、以下の形式でユーザーに表示すること：

```markdown
## プロンプト分析結果

### 5W1H
| 項目 | 内容 |
|------|------|
| Who | {誰が / 誰に影響} |
| What | {何を / 具体的なタスク} |
| When | {いつまでに / タイミング} |
| Where | {どこに / 実装場所・影響範囲} |
| Why | {なぜ / 目的・課題} |
| How | {どのように / 技術・手法} |
| Missing | {不足している項目のリスト} |

### リスク
| カテゴリ | リスク内容 | severity | mitigation |
|----------|------------|----------|------------|
| technical | {技術リスク} | high/medium/low | {対策案} |
| scope | {スコープリスク} | high/medium/low | {対策案} |
| dependency | {依存リスク} | high/medium/low | {対策案} |

### 曖昧さ
| 曖昧な表現 | 明確化案 |
|------------|----------|
| {不明確な表現} | {必要な明確化} |

### 論点分解（Multi-Topic Detection）
| 論点ID | 要約 | タイプ |
|--------|------|--------|
| 1 | {論点の要約} | instruction/question/context |

- **detected**: {true/false}
- **decomposition_needed**: {true/false}
- **recommendation**: {pm への推奨アクション}

### 拡張分析

#### test_strategy
- **test_types**: [unit / integration / e2e]
- **coverage_target**: minimal / standard / comprehensive
- **edge_cases**: {検出されたエッジケース}
- **rationale**: {テスト戦略の根拠}

#### preconditions
- **existing_code**: 新規作成 / 既存修正 / リファクタリング
- **dependencies**: {インストール済み / 追加必要 / 外部サービス}
- **constraints**: {技術的 / セキュリティ / パフォーマンス制約}

#### success_criteria
- **functional**: {機能要件リスト}
- **non_functional**: {パフォーマンス / セキュリティ / 可用性 / 保守性}
- **breaking_changes**: {true/false}

#### reverse_dependencies
- **affected_components**: {影響を受けるコンポーネント}
- **risk_level**: high / medium / low

### 判定
- **confidence**: {high/medium/low}
- **ready_for_playbook**: {true/false}
- **blocking_issues**: {playbook 作成前に解決すべき問題}
```

これにより：
1. ユーザーが分析結果を確認できる
2. playbook の context セクションに埋め込まれる（永続化）

---

### Step 2: understanding-check（ユーザー確認・★必須★）

**分析結果をユーザーに提示し、承認を得る。**

```python
# AskUserQuestion を使用して確認
AskUserQuestion({
  questions: [
    {
      question: "以下の理解で正しいですか？\n\n{analysis_result.5w1h の要約}",
      header: "理解確認",
      options: [
        { label: "はい、進めてください", description: "この内容で playbook を作成します" },
        { label: "修正が必要", description: "修正点を入力してください" }
      ],
      multiSelect: false
    }
  ]
})
```

**ユーザーが「修正が必要」を選択した場合**:
- 修正内容を聞き、Step 1 に戻る
- または修正内容を反映して Step 3 へ

---

### Step 3: pm SubAgent に委譲（分析結果を渡す）

**分析済みデータを pm に渡す。pm は解釈しない。**

```python
Task(
  subagent_type='pm',
  prompt='''
  ■ ユーザー要求（原文）:
  「{ユーザープロンプト原文}」

  ■ 分析結果（prompt-analyzer から）:
  {analysis_result をそのまま貼り付け}

  ■ ユーザー承認:
  - 承認日時: {timestamp}
  - 承認内容: {ユーザーが承認した内容}

  ■ 実行指示:
  1. 上記の分析結果に基づいて playbook を作成（再解釈禁止）
  2. reviewer 検証（PASS まで）
  3. state.md 更新 & ブランチ作成

  ★重要: pm は分析結果を再解釈しない。そのまま使用すること。
  '''
)
```

---

## Prohibited

```yaml
禁止:
  - Step 1 (prompt-analyzer) をスキップして pm を呼ぶ
  - Step 2 (ユーザー確認) をスキップ
  - pm に「解釈して」と指示する
  - 分析結果を改変して pm に渡す

必須:
  - Step 1 → Step 2 → Step 3 の順序
  - 各ステップの出力を次のステップに渡す
  - ユーザー承認を得てから pm を呼ぶ
```

---

## Chain Position（修正後）

```
Hook(prompt.sh)
    │
    │ 「全プロンプトで prompt-analyzer を呼べ」と指示
    │
    ▼
Task(prompt-analyzer)  ← ★全プロンプトで実行★
    │
    │ 分析結果 + topic_type を返す
    │
    ├─→ topic_type=instruction → Skill(playbook-init) を呼ぶ
    ├─→ topic_type=question    → 直接回答（分析結果を活用）
    └─→ topic_type=context     → 現在タスクに統合

    ▼ (instruction の場合)
Skill(playbook-init)  ← このファイル
    │
    │ 分析結果を受け取る（再分析しない）
    │
    ├─→ Step 1: 分析結果の確認
    ├─→ Step 2: AskUserQuestion（ユーザー確認）
    │       ↓ ユーザー承認
    └─→ Step 3: Task(pm) ← 分析結果を渡す
            │
            ├─→ playbook 作成（分析結果に基づく）
            ├─→ reviewer 検証
            └─→ state.md 更新
```

**なぜこの設計か**:
```
問題: 質問/タスクの判定が LLM 任せで、分析がスキップされることがある

解決: 全プロンプトで prompt-analyzer を呼ぶ
     → primary_topic_type で分岐（instruction/question/context）
     → playbook-init は分析結果を受け取るだけ（再分析しない）
```

---

## Hook → Skill チェーンの保証について

```yaml
設計上の制約:
  - Hook の messages は「強制」ではなく「指示」
  - Claude Code が Skill を呼び出すかどうかは LLM の判断に依存
  - 100% の保証は技術的に不可能

2層防御による対策:
  layer_1:
    name: "UserPromptSubmit Hook (prompt.sh)"
    role: "タスク依頼パターン検出時に Skill 呼び出しを指示"
    enforcement: "ヒント（指示）"
    effectiveness: "高（デバッグログで Skill 呼び出しを確認）"

  layer_2:
    name: "PreToolUse Guard (playbook-guard.sh)"
    role: "playbook なしで Edit/Write をブロック"
    enforcement: "強制（ブロック）"
    effectiveness: "100%（Hook がスキップされても保護）"

結論:
  - Layer 1 で Skill 呼び出しを促す
  - Layer 2 で実装前にブロック
  - この2層で十分なセーフティネットを提供
```

---

## Related Files

| ファイル | 役割 |
|----------|------|
| CLAUDE.md | Core Contract 定義（Golden Path） |
| .claude/hooks/prompt.sh | 導火線（State Injection） |
| .claude/skills/prompt-analyzer/agents/prompt-analyzer.md | プロンプト分析 SubAgent |
| .claude/skills/golden-path/agents/pm.md | pm SubAgent（分析結果を受け取る） |
| .claude/skills/understanding-check/SKILL.md | 理解確認フレームワーク |
| .claude/skills/quality-assurance/agents/reviewer.md | reviewer SubAgent |
