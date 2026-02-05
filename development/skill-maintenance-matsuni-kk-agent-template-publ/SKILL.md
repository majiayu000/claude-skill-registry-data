---
name: skill-maintenance
description: "Skill（SKILL.md）の保守・更新・新規作成を対話で行い、整合性と検証手順を維持したまま反映する。Skill更新、skill update、Skillメンテナンス、Skill追加を依頼されたときに使用する。"
---

# Skill Maintenance Workflow

## Subagent連携の原則

**SkillとSubagentの関係:**
- Subagentのフロントマターに `skills: skill1, skill2` と記載
- そのSubagentが呼び出されると、指定Skillsは全てSubagent内で実行される
- Skillは単独実行も可能だが、Subagent経由ならコンテキスト分離で並列処理等が可能

**Subagentを作るべきSkill:**
- 並列処理、WEB検索、アイデア出し、仮説立て等、コンテキスト非依存で価値があるもの
- 作成時は subagent-maintenance ワークフローを使用

**Subagent不要なSkill:**
- 単なる評価軸チェック用のためだけの個別 `qa-xxx` は原則作成しない（QCは共通Subagent `qa-skill-qc` を使用）

## Instructions
1. Preflight:
   - ドキュメント精査原則（Preflight必須）：テンプレート確認後、生成前に必ず以下を実施すること。
     - アジェンダ・依頼文に記載された参照資料を全て読み込む。
     - Flow/Stock配下の関連資料（前回議事録・要望リスト・プロジェクトREADME等）を網羅的に検索・確認する。
     - 確認できなかった資料は「未参照一覧」として成果物に明記する。
     - これらを完了するまで生成を開始しない。
   - 変更対象（operation=edit/add）、対象Skillファイル、変更範囲、期待成果、理由、検証手順を確認する（推測しない）。
   - 既存Skillを読み、必須セクション/テンプレート構造を把握する（テンプレートファースト）。
   - `./assets/skill_skeleton_template.md` を参照する。
2. 生成:
   - `./questions/skill_maintenance_questions.md` に従い入力を確定し、最小差分で修正する。
   - 既存機能・ロジック・定義を欠損させない。
   - Skillの必須セクション区切りを崩さない。
3. Skill新規作成時のアセット設置:
   - 新規Skill作成時は以下のフォルダ構造を作成すること:
     ```
     {{AGENT_CONFIG_DIR}}/skills/{skill-name}/
     ├── SKILL.md                    # 必須: Skill定義
     ├── assets/                     # 必須: テンプレート
     │   └── {name}_template.md
     ├── questions/                  # 必須: 質問リスト
     │   └── {name}_questions.md
     ├── evaluation/                 # 必須: 評価指標
     │   └── evaluation_criteria.md
     ├── triggers/                   # 必須: WF連携の起動条件
     │   └── next_action_triggers.md
     └── scripts/                    # 任意: 検証/自動化スクリプト
         └── {script_name}.py
     ```
   - `{{AGENT_CONFIG_DIR}}` は実行環境に応じて決定:
     - Cursor: `.cursor`
     - Claude Code: `.claude`
     - Codex: `.codex`
   - evaluation_criteria.md は既存Skillの評価指標を参考に作成する。
   - SKILL.md の Resources セクションに全アセットを明記する。
4. Subagentとして独立実行されるSkillの場合:
   - `## Subagent Execution` セクションをSKILL.md末尾に追加し、以下を明記する:
     - サブエージェント: 対応するagents/*.mdのパス
     - 用途: 並列処理、バックグラウンド実行等の具体的用途
     - 入力: 期待されるパラメータ
     - 出力: 処理結果の形式
   - 対応するSubagentの `skills:` フィールドにこのSkill名を追加する

5. triggers/next_action_triggers.md の作成（必須）:
   - 新規Skill作成時は必ず`triggers/next_action_triggers.md`を作成する。
   - `./assets/next_action_triggers_spec.md` の仕様に従って起動条件を定義する。
   - 起動条件は**検証可能な形式**で記載する（曖昧表現NG）:
     - NG: 「〜が必要なら」「〜したい場合」
     - OK: 「成果物に〜セクションが存在する」「〜が未作成（ファイル不存在）」
   - SKILL.mdのResourcesセクションに`- triggers: ./triggers/next_action_triggers.md`を追加する。
   - SKILL.mdのNext Actionセクションを以下の形式に更新する:
     ```markdown
     ## Next Action
     - triggers: ./triggers/next_action_triggers.md

     起動条件に従い、条件を満たすSkillを自動実行する。
     ```

6. CLAUDE.md / AGENTS.md への追記:
   - 新規Skill作成時は以下を確認・追記すること:
     - **ワークフロー索引**: 該当フェーズ（Initiating/Planning/Executing等）に追記
     - **パス辞書**: 必要なパスパターンがあれば `patterns:` セクションに追記
   - 追記フォーマット:
     ```yaml
     # ワークフロー索引の例（CLAUDE.md Section 6）
     ### Executing（実行）
     new-workflow-name → next-workflow-name

     # パス辞書の例（CLAUDE.md Section 7 patterns:）
     new_template:    "{{patterns.flow_date}}/new_template.md"
     ```
   - 追記後、`python3 scripts/update_agent_master.py --source cursor --force` で3環境同期を実施する。
7. 検証:
   - 必要に応じて `./assets/skill_check_report_template.md` 形式で検証ログを作成する。
8. QC（必須）:
   - 共通QC Subagent（`qa-skill-qc`）に評価・チェックを委譲する。
   - `qa-skill-qc` は最初に `./evaluation/evaluation_criteria.md` をReadし、以下の観点を中心にQCを実施する:
     - 必須セクション維持
     - 機能欠損がないか
     - 差分最小
     - 検証手順の不足
     - triggers/next_action_triggers.md が作成されているか
     - 起動条件が検証可能な形式か
   - 評価結果を成果物末尾に追記する（修正有無/理由）。
   - 重大な問題がある場合は修正し、再度 `qa-skill-qc` でQCする（最大3回）。
9. バックログ反映:
   - 次アクション（3環境同期、レビュー依頼、ロールバック準備等）を抽出しバックログへ反映する。
   - 反映先・編集制約・差分提示は AGENTS.md / CLAUDE.md の全体ルールに従う。

subagent_policy:
  - 単なる評価目的のためだけの個別 `qa-xxx` サブエージェントは Agents/ に作成しない
  - QCは共通Subagent `qa-skill-qc` を使用し、各Skillの `./evaluation/evaluation_criteria.md` に基づいて評価する
  - Subagentが必要なSkillは subagent-maintenance で作成し、skills: フィールドで連携

recommended_subagents:
  - qa-skill-qc: 必須セクション維持、差分最小、triggers作成/参照を検査

## Resources
- questions: ./questions/skill_maintenance_questions.md
- questions: ./questions/path_update_questions.md
- questions: ./questions/skill_check_questions.md
- assets: ./assets/skill_skeleton_template.md
- assets: ./assets/skill_maintenance_log_template.md
- assets: ./assets/skill_check_report_template.md
- assets: ./assets/skills_official_alignment_conversion.md
- assets: ./assets/next_action_triggers_spec.md
- evaluation: ./evaluation/evaluation_criteria.md
- triggers: ./triggers/next_action_triggers.md
- scripts: ./scripts/update_agent_master.py
- scripts: ./scripts/lint_skills.py

## Next Action
- triggers: ./triggers/next_action_triggers.md

起動条件に従い、条件を満たすSkillを自動実行する。
