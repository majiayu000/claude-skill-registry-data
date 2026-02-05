---
name: skeleton-generate
description: "Skills版エージェント骨格（CLAUDE.md, .codex/skills/, .codex/等）を生成し、初期設定を完了する。「スケルトン生成」「エージェント生成」「骨格作成」を依頼されたときに使用する。"
---

# Skeleton Generate Workflow

Skills版エージェント骨格生成ワークフロー。主成果物はoutput/{domain}_agent/ディレクトリ一式（CLAUDE.md, .codex/skills/, .codex/含む）。

## Instructions

### 1. Preflight（事前確認）
- `./assets/generate_checklist.md` を先に読み、必須項目を確認する。
- draft_requirements.md を参照し、以下を確認する:
  - ドメイン名（スネークケース）
  - エージェント表示名
  - 説明文（1-2文）
  - 準拠フレームワーク
  - **ディレクトリパターン（Business/Coding/Data/DevOps/Minimal）**
- framework_research.md が存在し、framework_research_done=true が記録されているか確認する。
- **要件定義へのユーザー承認が得られているか確認する。未承認なら生成しない。**
- output/配下に同名エージェントが存在しないか確認する。

### 2. ディレクトリパターン選択
- `./assets/directory_patterns.md` を参照し、用途に応じたパターンを選択する:
  - **Business**: Flow/Stock/Archived（ビジネス/ドキュメント管理）
  - **Coding**: src/tests/docs（ソフトウェア開発）
  - **Data**: data/notebooks/src/models（データ分析/ML）
  - **DevOps**: infra/scripts/configs（インフラ/運用）
  - **Minimal**: src/scripts（最小構成）
- ユーザーに確認し、パターンを確定する。

### 3. ディレクトリ構造生成
- 選択したパターンに応じてディレクトリを作成する。
- 共通構造（全パターン必須）:
  ```bash
  mkdir -p output/{domain}_agent/.claude/{skills,agents,commands}
  mkdir -p output/{domain}_agent/.codex/{skills,agents,prompts}
  mkdir -p output/{domain}_agent/.cursor/rules
  mkdir -p output/{domain}_agent/.github/{skills,prompts}
  mkdir -p output/{domain}_agent/.gemini
  mkdir -p output/{domain}_agent/.kiro/steering
  mkdir -p output/{domain}_agent/scripts
  ```
- パターン別構造を追加（例: Business）:
  ```bash
  mkdir -p output/{domain}_agent/Flow
  mkdir -p output/{domain}_agent/Stock/programs/core/{documents,images}
  mkdir -p output/{domain}_agent/Archived
  ```
- 空ディレクトリに .gitkeep を配置する。

### 4. マスターファイル生成
- `./assets/claude_md_template.md` を使用して以下を生成する（テンプレートにはWF自動継続/テンプレートファースト/Next Action triggers参照ルールを含める）:
  1. `CLAUDE.md` - プレースホルダを置換して生成
  2. `AGENTS.md` - CLAUDE.mdと同内容
  3. `.github/copilot-instructions.md` - CLAUDE.mdと同内容
  4. `.gemini/GEMINI.md` - CLAUDE.mdと同内容
  5. `.kiro/steering/KIRO.md` - CLAUDE.mdと同内容
- `./assets/readme_template.md` を使用して `README.md` を生成する。
- 元資料にない項目は省略せず「未記載」と明記する。

### 5. スクリプト・共通Skillsコピー
- `./assets/common_skills_template.md` に従い、以下をコピーする:
  ```bash
  # スクリプト
  cp scripts/validate_skills.py output/{domain}_agent/scripts/
  cp scripts/update_agent_master.py output/{domain}_agent/scripts/

  # 共通Skills（必須）
  cp -r .codex/skills/skill-maintenance output/{domain}_agent/.codex/skills/
  cp -r .codex/skills/subagent-maintenance output/{domain}_agent/.codex/skills/

  # 共通サブエージェント（推奨）
  cp .claude/agents/skill-builder.md output/{domain}_agent/.claude/agents/
  cp .claude/agents/skill-validator.md output/{domain}_agent/.claude/agents/
  cp .claude/agents/qa-skill-qc.md output/{domain}_agent/.claude/agents/
  cp .codex/agents/qa-skill-qc.md output/{domain}_agent/.codex/agents/
  cp .claude/agents/qa-skeleton-generate.md output/{domain}_agent/.claude/agents/
  ```

### 6. 初期Skills準備
- domain-skills-generate へ進む準備をする。
- ドメイン固有のSkillsは次工程で作成。

### 7. QC（必須）
- `recommended_subagents` のQC Subagent（`qa-skill-qc`）に評価を委譲する。
- Subagentは `./evaluation/skeleton_criteria.md` をReadし、QCを実施する。
- 指摘を最小差分で反映する（最大3回）。
- 指摘に対し「修正した/しない」と理由を成果物に残す。

### 8. バックログ反映
- 次アクション（Skills作成、バリデーション）をタスクリストへ追記する。
- 生成完了を記録する。

subagent_policy:
  - 品質ループ（QC/チェック/フィードバック）は必ずサブエージェントへ委譲する
  - サブエージェントの指摘を反映し、反映結果（修正有無/理由）を成果物に残す

recommended_subagents:
  - qa-skill-qc: ディレクトリ構造、CLAUDE.md、マルチプラットフォームファイル、スクリプト配置を検査

## Resources
- assets: ./assets/generate_checklist.md
- assets: ./assets/directory_patterns.md
- assets: ./assets/common_skills_template.md
- assets: ./assets/claude_md_template.md
- assets: ./assets/skills_structure_template.md
- assets: ./assets/readme_template.md
- evaluation: ./evaluation/skeleton_criteria.md
- scripts: scripts/validate_skills.py
- scripts: scripts/update_agent_master.py
- triggers: ./triggers/next_action_triggers.md

## Next Action
- triggers: ./triggers/next_action_triggers.md

起動条件に従い、条件を満たすSkillを自動実行する。
