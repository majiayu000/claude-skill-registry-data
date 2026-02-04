---
name: core-rule-maintenance
description: "CLAUDE.md/AGENTS.md等のコアルールファイルの保守・更新を対話で行い、3環境同期と整合性を維持したまま反映する。CLAUDE.md更新、コアルール変更、ルール追加、パス辞書更新、ワークフロー索引更新を依頼されたときに使用する。"
---

# Core Rule Maintenance Workflow

## 対象ファイル

| ファイル | 役割 | 同期先 |
|----------|------|--------|
| CLAUDE.md | コア原則、成果物タイプ、品質ゴール、Skill選択ポリシー、WF索引、パス辞書 | .cursor/.claude/.codex |
| AGENTS.md | エージェント定義（Cursor専用、非同期） | .cursor のみ |

## Instructions

1. Preflight:
   - ドキュメント精査原則（Preflight必須）：変更前に必ず以下を実施すること。
     - 現在のCLAUDE.md/AGENTS.mdを全て読み込む。
     - 変更依頼の背景・理由・期待される効果を確認する。
     - 影響を受けるSkills/Subagentsを特定する。
     - これらを完了するまで変更を開始しない。
   - 変更対象（section=コア原則/成果物タイプ/品質ゴール/WF索引/パス辞書等）、変更範囲、理由を確認する（推測しない）。
   - `./assets/claude_md_structure.md` を参照し、CLAUDE.mdの構造を把握する（テンプレートファースト）。

2. 変更種別の判断:
   - 以下の変更種別を特定し、それぞれの手順に従う:
     - **Section 1-5 変更**: コア原則/成果物タイプ/品質ゴール/Skill選択ポリシー/成果物分類
     - **Section 6 変更**: ワークフロー索引（WF連携マップ）
     - **Section 7 変更**: パス辞書（root/dirs/patterns/meta）
     - **複合変更**: 複数セクションにまたがる変更

3. 生成（変更実施）:
    - `./questions/core_rule_maintenance_questions.md` に従い入力を確定する。
    - 既存の構造・フォーマットを崩さない（最小差分で修正）。
    - CLAUDE.mdの必須セクション区切りを維持する。
    - 変更内容:
      - **WF索引変更時**: 該当フェーズに追記/修正、矢印（→）で連携を表現
      - **パス辞書変更時**: dirs/patterns/metaの適切な箇所に追記、変数参照の整合性を確認
      - **コア原則変更時**: 全Skillsへの影響を確認し、必要なら各SKILL.mdとtriggersも更新する
      - **Skill運用ルール変更時**: 「Skillは原則必須」「どうしてもskillsに該当がない場合のみ省略可」「Skill完了後はtriggersで次へ必ず進む」などの運用原則は、必ずCLAUDE.mdの `## 1. コア原則` に記載する（Section 4だけに置かない）

4. 整合性チェック:
   - パス辞書変更時:
     - 変数参照（`{{patterns.xxx}}`等）が正しく解決されることを確認
     - 循環参照がないことを確認
     - 実際のファイルパスとして有効であることを確認
   - WF索引変更時:
     - 参照先Skillが存在することを確認
     - 連携フロー（→）の整合性を確認
     - 各SkillのNext Action triggersと整合していることを確認

5. 3環境同期:
    - CLAUDE.md変更後は `python3 scripts/update_agent_master.py --source claude --force` で同期を実施する（Claude起点）。
    - 同期内容: CLAUDE.mdからAGENTS.md等の派生ルールを再生成し、`.claude/skills` / `.claude/commands` を各環境へ同期する。
    - 備考: AGENTS.mdは生成対象だが、Cursor専用の運用ファイルとして扱う（手動で直接編集しない）。

6. QC（必須）:
   - `recommended_subagents` のQC Subagent（`qa-skill-qc`）に評価・チェックを委譲する。
   - Subagentは `./evaluation/evaluation_criteria.md` をReadし、QCを実施する。
   - チェック項目:
     - 必須セクション維持
     - パス辞書の変数参照整合性
     - WF索引とSkillsのNext Action triggers整合性
     - 3環境同期の実施
   - 指摘を最小差分で反映する（最大3回）。
   - 指摘に対し「修正した/しない」と理由を成果物に残す。

7. バックログ反映:
   - 次アクション（影響Skillsの更新、レビュー依頼等）を抽出しバックログへ反映する。
   - 反映先・編集制約・差分提示は AGENTS.md / CLAUDE.md の全体ルールに従う。

subagent_policy:
  - 品質ループ（QC/チェック/フィードバック）は必ずサブエージェントへ委譲する
  - サブエージェントの指摘を反映し、反映結果（修正有無/理由）を成果物に残す

recommended_subagents:
  - qa-skill-qc: 必須セクション維持、WF索引/triggers整合、パス辞書参照の破綻を検査

## Resources
- questions: ./questions/core_rule_maintenance_questions.md
- assets: ./assets/claude_md_structure.md
- assets: ./assets/path_dictionary_guide.md
- assets: ./assets/workflow_index_guide.md
- evaluation: ./evaluation/evaluation_criteria.md
- triggers: ./triggers/next_action_triggers.md
- scripts: scripts/update_agent_master.py

## Next Action
- triggers: ./triggers/next_action_triggers.md

起動条件に従い、条件を満たすSkillを自動実行する。
