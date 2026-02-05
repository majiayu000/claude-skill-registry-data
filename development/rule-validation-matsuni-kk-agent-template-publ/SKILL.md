---
name: rule-validation
description: "validate_skills.pyを実行してSkills/Agents/Commandsの構文を検証し、エラーを修正してログを記録する。「バリデーション」「構文検証」「Skillsチェック」を依頼されたときに使用する。"
---

# Skills Validation Workflow

Skills検証ワークフロー。主成果物はskills_check_log.md（検証レポート）。

## Instructions

### 1. Preflight（事前確認）
- `./assets/validation_checklist.md` を先に読み、検証項目を確認する。
- 検証対象のSkillsフォルダ（.codex/skills/）を確認する。
- 前回の検証ログ（skills_check_*.md）があれば参照する。
- 全SKILL.mdファイルが存在することを確認する。

### 2. 生成
- 以下のコマンドを実行する:
  ```bash
  cd output/{domain}_agent
  python3 scripts/validate_skills.py
  ```
- 検証結果をskills_check_log.mdに記録する:
  - 検証日時
  - 対象Skill一覧
  - エラー内容
  - 修正内容
- エラーがあれば該当Skillを修正する。
- 修正後、再度validate_skills.pyを実行する。
- **`All skills passed validation.` が出るまで繰り返す。**
- 元資料にない項目は省略せず「未記載」と明記する。

### 3. QC（必須）
- `recommended_subagents` のQC Subagent（`qa-skill-qc`）に評価を委譲する。
- Subagentは `./evaluation/validation_criteria.md` をReadし、QCを実施する。
- 指摘を最小差分で反映する（最大3回）。
- 指摘に対し「修正した/しない」と理由を成果物に残す。

### 4. バックログ反映
- 検証結果をタスクリストに記録する。
- 残課題があればバックログへ追記する。
- validation_passed=true を記録してから次工程へ進む。

subagent_policy:
  - 品質ループ（QC/チェック/フィードバック）は必ずサブエージェントへ委譲する
  - サブエージェントの指摘を反映し、反映結果（修正有無/理由）を成果物に残す

recommended_subagents:
  - qa-skill-qc: 全Skills検証完了、エラー解消、ログ記録、再実行確認を検査

## Resources
- assets: ./assets/validation_checklist.md
- assets: ./assets/skills_check_log_template.md
- evaluation: ./evaluation/validation_criteria.md
- scripts: scripts/validate_skills.py
- triggers: ./triggers/next_action_triggers.md

## Next Action
- triggers: ./triggers/next_action_triggers.md

起動条件に従い、条件を満たすSkillを自動実行する。
