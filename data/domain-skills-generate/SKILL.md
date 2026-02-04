---
name: domain-skills-generate
description: "ドメイン要件と業界標準フレームワークに基づき、対象エージェント用のSkills群（SKILL.md/assets/evaluation/questions）を設計・生成する。「Skills作成」「ワークフロー群生成」「機能実装」を依頼されたときに使用する。"
---

# Domain Skills Generate Workflow

任意ドメイン向けSkills群生成ワークフロー。主成果物はoutput/{domain}_agent/.claude/skills/配下のSkills一式。

## Instructions

### 1. Preflight（事前確認）
- `./assets/skills_design_guide.md` を先に読み、Skills設計原則を確認する。
- draft_requirements.md を参照し、以下を確認する:
  - ドメイン名、必須機能一覧、成功基準
  - 対象ユーザー、利用シナリオ
- framework_research.md を参照し、業界標準フレームワークを確認する。
- `./questions/domain_skills_questions.md` で追加情報を収集する。

### 2. Skills設計
- 以下の観点でSkills群を設計する:
  1. **機能分解**: 必須機能を1WF=1Skillに分解
  2. **業界標準マッピング**: フレームワークの各プロセスをSkillに対応付け
  3. **依存関係整理**: Skills間の実行順序・依存を明確化
  4. **共通パターン抽出**: 複数Skillで共通するassets/evaluationを特定

- Skills設計書を生成する（`./assets/skills_design_template.md`に従う）:
  - Skill一覧（名前、説明、主成果物）
  - 実行フロー図（Phase別）
  - 各Skillの概要設計

### 3. Skills生成
- 設計書に基づき、各Skillを生成する:
  ```
output/{domain}_agent/.claude/skills/{skill-name}/
├── SKILL.md           # 統一フォーマット準拠
├── assets/            # テンプレート、チェックリスト
│   └── {name}_template.md
├── evaluation/        # 評価指標
│   └── {name}_criteria.md
├── questions/         # 質問リスト（必要な場合）
│   └── {name}_questions.md
└── triggers/          # 必須: Next Action 起動条件
    └── next_action_triggers.md

  ```

- SKILL.md統一フォーマット必須項目:
  - frontmatter: name, description
  - 見出し: # XXX Workflow, ## Instructions, ## Resources, ## Next Action
  - Instructions: Preflight, 生成, QC（必須）, バックログ反映
  - 必須ブロック: subagent_policy, recommended_subagents

**重要: recommended_subagentsの設計ルール**
- 単なる評価軸チェック（チェックリスト確認等）→ `evaluation/*.md` で対応、agents/*.md不要
- 以下の場合のみ agents/*.md を作成:
  - コンテキスト不要で独立実行可能
  - Web検索・外部情報取得が必要
  - アイデア出し・ブレスト（複数観点の並列生成）
  - 仮説立案・検証（独立した思考プロセス）
  - 専門知識・Skills携帯が必要なフィードバック

- ドメイン固有の内容を反映:
  - 業界用語、専門概念
  - 標準的なワークフロー
  - 品質基準、成功指標
  - 必須チェック項目

### 4. QC（必須）
- `recommended_subagents` のQC Subagent（`qa-skill-qc`）に評価を委譲する。
- Subagentは `./evaluation/domain_skills_criteria.md` をReadし、QCを実施する。
- チェック項目:
  - 全必須機能がSkillとしてカバーされているか
  - 各SkillがSKILL.md統一フォーマットに準拠しているか
  - assets/evaluationが適切に同梱されているか
  - 業界標準フレームワークが反映されているか
- 指摘を最小差分で反映する（最大3回）。
- 指摘に対し「修正した/しない」と理由を成果物に残す。

### 5. 統合・検証
- 生成したSkillsをワークフロー索引（CLAUDE.md）へ追記する。
- Skills間の依存関係が正しく設定されているか確認する。
- 各SkillのNext Action triggersが適切にチェーンしているか確認する。

### 6. バックログ反映
- 生成完了をタスクリストに記録する。
- 未実装の将来機能をバックログへ追記する。
- 次アクション（検証、ブラッシュアップ等）を明示する。

subagent_policy:
  - 品質ループ（QC/チェック/フィードバック）は必ずサブエージェントへ委譲する
  - サブエージェントの指摘を反映し、反映結果（修正有無/理由）を成果物に残す
  - 業界標準フレームワーク調査はSubagentで並列実行可能

recommended_subagents:
  - qa-skill-qc: Skills網羅性、フォーマット準拠、業界標準反映、依存関係整合を検査
  - research-framework: 業界標準フレームワークの調査・要約を並列実行

## Resources
- questions: ./questions/domain_skills_questions.md
- assets: ./assets/skills_design_guide.md
- assets: ./assets/skills_design_template.md
- assets: ./assets/skill_skeleton.md
- assets: ./assets/evaluation_skeleton.md
- assets: ./assets/industry_frameworks.md
- evaluation: ./evaluation/domain_skills_criteria.md
- triggers: ./triggers/next_action_triggers.md

## Next Action
- triggers: ./triggers/next_action_triggers.md

起動条件に従い、条件を満たすSkillを自動実行する。
