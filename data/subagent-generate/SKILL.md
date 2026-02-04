---
name: subagent-generate
description: "Skills群に対応するサブエージェント（.claude/agents/*.md）を設計・生成する。「サブエージェント作成」「並列処理エージェント」「専門エージェント」を依頼されたときに使用する。"
---

# Subagent Generate Workflow

Skills群に対応するサブエージェントを生成する。主成果物はoutput/{domain}_agent/.claude/agents/配下のサブエージェント定義。

## Instructions

### 1. Preflight（事前確認）
- `./assets/subagent_design_guide.md` を先に読み、サブエージェント設計原則を確認する。
- 対象エージェントの `.claude/skills/` を確認し、既存Skillsを把握する。
- 各SkillのSKILL.mdから `recommended_subagents` を抽出する。

### 2. サブエージェント判定

**重要: サブエージェント化の判定基準**

以下の条件を満たす場合のみ `.claude/agents/*.md` を作成する:

| 条件 | サブエージェント化 | 理由 |
|------|-------------------|------|
| コンテキスト不要で独立実行可能 | ✅ 必要 | 並列実行のメリットあり |
| 専門知識・Skills携帯が必要 | ✅ 必要 | 専門性の分離 |
| Web検索・外部情報取得 | ✅ 必要 | 非同期実行可能 |
| アイデア出し・ブレスト | ✅ 必要 | 複数観点の並列生成 |
| 仮説立案・検証 | ✅ 必要 | 独立した思考プロセス |
| フィードバック・レビュー | ✅ 必要 | 客観的評価 |
| 単なる評価軸チェック | ❌ 不要 | evaluation/*.mdで十分 |
| 親タスクのコンテキスト必須 | ❌ 不要 | サブエージェント化の意味なし |

**単なる評価軸の評価（チェックリスト確認等）は `evaluation/*.md` で対応し、agents/*.md は作成しない。**

### 3. サブエージェント設計

サブエージェント化が必要と判定された場合、以下を設計する:

```yaml
サブエージェント設計:
  name: "{purpose}-agent"
  type: "{research|feedback|ideation|validation|parallel-check}"
  携帯Skills:
    - "{関連skill-1}"
    - "{関連skill-2}"
  入力: "{何を受け取るか}"
  出力: "{何を返すか}"
  並列実行: "{可能/不可}"
  Web検索: "{必要/不要}"
```

### 4. サブエージェント生成

設計に基づき、各サブエージェントを生成する:

```
output/{domain}_agent/.claude/agents/{agent-name}.md
```

**サブエージェント定義フォーマット:**
```markdown
---
name: {agent-name}
description: "{説明}"
type: "{research|feedback|ideation|validation|parallel-check}"
tools: [Read, Grep, Glob, WebSearch, WebFetch]  # 必要なツール
---

# {Agent Name}

{目的と役割の説明}

## 携帯Skills

このサブエージェントは以下のSkillsを参照して実行する:

- `.claude/skills/{skill-1}/`: {説明}
- `.claude/skills/{skill-2}/`: {説明}

## 実行手順

1. {ステップ1}
2. {ステップ2}
3. {ステップ3}

## 入力

- {入力パラメータ1}: {説明}
- {入力パラメータ2}: {説明}

## 出力

- {出力形式の説明}
- {レポートフォーマット等}

## 判定基準

- {成功条件1}
- {成功条件2}
```

### 5. サブエージェントタイプ別テンプレート

**research-agent（調査系）:**
- Web検索で最新情報を収集
- 公式ドキュメント・ベストプラクティスを調査
- 携帯Skills: 対象ドメインの参照系Skills

**feedback-agent（フィードバック系）:**
- 成果物に対する客観的レビュー
- 改善提案・代替案の提示
- 携帯Skills: 評価対象のSkills + evaluation基準

**ideation-agent（アイデア出し系）:**
- 複数のアプローチを並列生成
- ブレインストーミング的発想
- 携帯Skills: ドメイン知識系Skills

**validation-agent（検証系）:**
- 仮説の妥当性検証
- 実現可能性チェック
- 携帯Skills: 技術制約系Skills

**parallel-check-agent（並列チェック系）:**
- 複数ファイルの同時チェック
- 独立した検証を並列実行
- 携帯Skills: チェック対象のSkills

### 6. QC（必須）
- `recommended_subagents` のQC Subagent（`qa-skill-qc`）に評価を委譲する。
- Subagentは `./evaluation/subagent_criteria.md` をReadし、QCを実施する。
- チェック項目:
  - サブエージェント化判定が適切か
  - 携帯Skillsが適切に設定されているか
  - 入出力定義が明確か
  - 並列実行可能性が正しく判定されているか
- 指摘を最小差分で反映する（最大3回）。

### 7. バックログ反映
- 生成したサブエージェント一覧を記録する。
- CLAUDE.mdにサブエージェント索引を追加する。
- 次アクション（テスト実行等）を明示する。

subagent_policy:
  - 品質ループ（QC/チェック/フィードバック）は必ずサブエージェントへ委譲する
  - サブエージェントの指摘を反映し、反映結果（修正有無/理由）を成果物に残す

recommended_subagents:
  - qa-skill-qc: サブエージェント化判定、携帯Skills設定、入出力定義を検査

## Resources
- assets: ./assets/subagent_design_guide.md
- assets: ./assets/subagent_template.md
- assets: ./assets/subagent_types.md
- evaluation: ./evaluation/subagent_criteria.md
- triggers: ./triggers/next_action_triggers.md

## Next Action
- triggers: ./triggers/next_action_triggers.md

起動条件に従い、条件を満たすSkillを自動実行する。
