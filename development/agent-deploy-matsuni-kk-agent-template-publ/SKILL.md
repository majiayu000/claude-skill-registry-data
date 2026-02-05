---
name: agent-deploy
description: "生成したエージェントをGitHubプライベートリポジトリとして公開する。「デプロイ」「リポジトリ作成」「公開」を依頼されたときに使用する。"
---

# Agent Deploy Workflow

生成したエージェントをGitHubプライベートリポジトリとして公開する。主成果物はGitHubリポジトリURL。

## Instructions

### 1. Preflight（事前確認）
- `./assets/deploy_checklist.md` を先に読み、必須項目を確認する。
- 対象エージェントのディレクトリパスを確認する（output/{agent_name}/）。
- 以下のファイルが存在するか確認する:
  - CLAUDE.md（必須）
  - README.md（必須）
  - .codex/skills/（必須）
  - scripts/（推奨）
- gh CLI が認証済みか確認する。

### 2. マルチプラットフォーム同期
- update_agent_master.py を **Claude起点で** 実行してマスターファイルを同期する:
  ```bash
  cd output/{agent_name}
  python3 scripts/update_agent_master.py --source claude --force
  ```
- 同期対象:
  - CLAUDE.md → AGENTS.md
  - CLAUDE.md → .github/copilot-instructions.md
  - CLAUDE.md → .gemini/GEMINI.md
  - CLAUDE.md → .kiro/steering/KIRO.md

### 3. .gitignore 確認
- .gitignore が存在しない場合は作成する。
- `./assets/gitignore_template.md` を参照する。
- 以下を除外対象に含める:
  - .env
  - *.log
  - node_modules/
  - .DS_Store

### 4. Git初期化・コミット
- 以下の手順でGitリポジトリを初期化する:
  ```bash
  cd output/{agent_name}
  git init
  git add .
  git commit -m "Initial release: {Agent Name}

  🤖 Generated with [Claude Code](https://claude.com/claude-code)

  Co-Authored-By: Claude <noreply@anthropic.com>"
  ```

### 5. GitHubリポジトリ作成（プライベート）
- gh CLI でプライベートリポジトリを作成する:
  ```bash
  gh repo create {agent_name} --private --source=. --push
  ```
- リポジトリURLを記録する。

### 6. QC（必須）
- `recommended_subagents` のQC Subagent（`qa-skill-qc`）に評価を委譲する。
- Subagentは `./evaluation/deploy_criteria.md` をReadし、QCを実施する。
- 指摘を最小差分で反映する（最大3回）。

### 7. バックログ反映
- リポジトリURLをタスクリストに記録する。
- deploy_done=true を記録する。

### 8. デプロイ後クリーンアップ（推奨）
- デプロイ完了（push成功 + リポジトリURL取得）後、ローカルの `output/{agent_name}/` を削除して作業生成物を片付ける。
- 破壊的操作になるため、削除前にユーザーへ削除対象パスを提示し、明示的な許可を得る。
- 可能なら `post-deploy-cleanup` Skill に委譲して実行する（対象: output/ と Flow/ などの一時ファイル）。

subagent_policy:
  - 品質ループ（QC/チェック/フィードバック）は必ずサブエージェントへ委譲する
  - サブエージェントの指摘を反映し、反映結果（修正有無/理由）を成果物に残す

recommended_subagents:
  - qa-skill-qc: 必須ファイル存在、マルチプラットフォーム同期、リポジトリ作成を検査

## Resources
- assets: ./assets/deploy_checklist.md
- assets: ./assets/gitignore_template.md
- evaluation: ./evaluation/deploy_criteria.md
- scripts: scripts/update_agent_master.py
- triggers: ./triggers/next_action_triggers.md

## Next Action
- triggers: ./triggers/next_action_triggers.md

起動条件に従い、条件を満たすSkillを自動実行する。
