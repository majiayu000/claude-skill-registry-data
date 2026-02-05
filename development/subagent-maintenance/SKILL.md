---
name: subagent-maintenance
description: "Subagent（{{AGENT_CONFIG_DIR}}/agents/*.md）の作成・更新・削除を対話で行い、フロントマター仕様と品質を維持したまま反映する。Subagent作成、agent追加、subagent updateを依頼されたときに使用する。"
---

# Subagent Maintenance Workflow

## Subagent設計原則

**Agents/に作成すべきSubagent:**
- コンテキストを保持せずに実行することに意義があるもの
- 例: 並列処理、WEB検索、アイデア出し、仮説立て、フィードバック収集
- Subagentは `skills:` フィールドで1つ以上のSkillを携える
- Skill経由で実行された場合、そのSkillsは全てSubagent内で実行される

**Agents/に作成不要なもの:**
- 単なる評価軸チェックのためだけの個別 `qa-xxx` サブエージェント
- → QCは共通Subagent `qa-skill-qc` を使用し、各Skillの `./evaluation/evaluation_criteria.md` に基づいて評価する

## Instructions
1. Preflight:
   - ドキュメント精査原則（Preflight必須）：テンプレート確認後、生成前に必ず以下を実施すること。
     - 依頼文に記載された参照資料を全て読み込む。
     - 既存の`{{AGENT_CONFIG_DIR}}/agents/`配下のエージェントファイルを確認する。
     - 確認できなかった資料は「未参照一覧」として成果物に明記する。
     - これらを完了するまで生成を開始しない。
   - 変更対象（operation=create/edit/delete）、対象エージェントファイル、変更範囲、期待成果、理由を確認する（推測しない）。
   - 既存エージェントを読み、フロントマター/構造を把握する（テンプレートファースト）。
   - `./assets/agent_template.md` を参照する。
   - `{{AGENT_CONFIG_DIR}}` は実行環境に応じて決定:
     - Cursor: `.cursor`
     - Claude Code: `.claude`
     - Codex: `.codex`

2. Subagent作成判断:
   - 以下の条件を満たす場合のみAgents/にSubagentを作成する:
     - **コンテキスト非依存**: 親コンテキストを保持せずに実行する意義がある
     - **Skill携帯**: 1つ以上のSkillを `skills:` で指定できる
     - **独立性**: 並列実行、バックグラウンド処理、外部検索等で価値を発揮
   - 単なる評価・チェックのみが目的の場合は作成しない（Skill内評価で対応）

3. 生成:
   - `./questions/subagent_maintenance_questions.md` に従い入力を確定する。
   - 公式仕様に従ったフロントマター形式を維持する。
   - エージェントの必須セクション区切りを崩さない。

4. Subagent新規作成時のフォーマット:
   - 新規Subagent作成時は以下の形式に従う:
     ```markdown
     ---
     name: agent-name
     description: "エージェントの専門領域と自動委譲のトリガー説明"
     skills: skill1, skill2, skill3
     ---

     # Agent Name

     エージェントの詳細な役割、専門性、いつClaudeが呼び出すべきかの説明。

     ## Expertise Overview
     - 専門領域1
     - 専門領域2
     - 専門領域3

     ## Critical First Step
     タスク実行前に必ず行うべき手順（ドキュメント取得など）

     ## Domain Coverage
     - 対応可能なタスク1
     - 対応可能なタスク2

     ## Response Format
     期待される出力形式と引用要件

     ## Quality Assurance
     検証ステップとエラーハンドリング
     ```
   - 保存先: `{{AGENT_CONFIG_DIR}}/agents/{agent-name}.md`
   - **必須**: `skills:` フィールドに1つ以上のSkillを指定すること

5. skillsを使うSubagentの場合:
   - `skills:` フィールドに指定するSkillが存在することを確認する
   - 該当Skillに `## Subagent Execution` セクションが必要であることを伝える（サブエージェントパス、用途、入出力を明記）
   - Skill側の更新が必要な場合は skill-maintenance ワークフローで対応する

6. CLAUDE.md / AGENTS.md への追記:
   - 新規Subagent作成時は以下を確認・追記すること:
     - **ワークフロー索引**: 該当フェーズに追記（必要な場合）
     - **パス辞書**: 必要なパスパターンがあれば `patterns:` セクションに追記
   - 追記後、`python3 scripts/update_agent_master.py --source cursor --force` で3環境同期を実施する。

7. 検証:
   - フロントマターの必須フィールド（name, description, skills）が存在することを確認する。
   - 必要に応じて `./assets/agent_check_report_template.md` 形式で検証ログを作成する。

8. QC（必須）:
   - 共通QC Subagent（`qa-skill-qc`）に評価・チェックを委譲する。
   - `qa-skill-qc` は最初に `./evaluation/evaluation_criteria.md` をReadし、以下を中心にQCを実施する:
     - フロントマター仕様準拠
     - 必須セクション維持
     - skills整合性（指定Skillが存在するか）
     - Subagent設計原則への適合
   - 評価結果を成果物末尾に追記する（修正有無/理由）。
   - 重大な問題がある場合は修正し、再度 `qa-skill-qc` でQCする（最大3回）。

9. バックログ反映:
   - 次アクション（3環境同期、レビュー依頼、ロールバック準備等）を抽出しバックログへ反映する。
   - 反映先・編集制約・差分提示は AGENTS.md / CLAUDE.md の全体ルールに従う。

subagent_policy:
  - Agents/に作成するSubagentは「コンテキスト非依存 + Skill携帯」が条件
  - 単なる評価目的のためだけの個別 `qa-xxx` サブエージェントは Agents/ に作成しない
  - QCは共通Subagent `qa-skill-qc` を使用し、各Skillの `./evaluation/evaluation_criteria.md` に基づいて評価する

recommended_subagents:
  - qa-skill-qc: フロントマター仕様、skills整合、Subagent設計原則への適合を検査

## Resources
- questions: ./questions/subagent_maintenance_questions.md
- assets: ./assets/agent_template.md
- assets: ./assets/subagent_maintenance_log_template.md
- assets: ./assets/agent_check_report_template.md
- evaluation: ./evaluation/evaluation_criteria.md
- triggers: ./triggers/next_action_triggers.md
- scripts: ./scripts/update_agent_master.py

## Next Action
- triggers: ./triggers/next_action_triggers.md

起動条件に従い、条件を満たすSkillを自動実行する。
