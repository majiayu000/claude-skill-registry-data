---
name: "Data Manager"
description: "PB-000の成果物をファイルベースで保存・管理。フォルダ作成、ファイル存在確認、実行履歴管理を担当。データ管理、ファイル操作で必ず使用。"
---

# Data Manager Skill

## 概要

このSkillは、PB-000の成果物をファイルシステムで構造化管理し、各フェーズの実行状況を追跡します。新規実行のセットアップ、ファイル存在確認、実行履歴管理、Git管理を担当します。

## 機能

### 1. フォルダ構造作成
- 新規実行用のディレクトリ構造セットアップ
- Phase1-5の各フォルダ自動生成
- シンボリックリンク（latest）の作成
- テンプレートからのファイルコピー

### 2. ファイル存在確認
- 各エージェントが成果物を正しく保存したか確認
- 必須ファイル12個の存在チェック
- ファイルサイズ・更新日時の確認

### 3. 実行履歴管理
- 過去の実行履歴の記録と検索
- 実行ID（タイムスタンプ）による管理
- 実行完了状況のトラッキング

### 4. Git管理
- バージョン管理とバックアップ
- 成果物のコミット
- ブランチ管理

## 使用方法

### Claude Codeでの自然言語リクエスト

```
data-managerエージェントを使用して、実行ID「2024-12-20_14-30」でPB-000用フォルダ構造を作成してください。
```

```
Phase1の成果物ファイルが正常に保存されているか確認してください：
- pb000_deliverables/executions/2024-12-20_14-30/phase1_persona/persona_analysis.md
- pb000_deliverables/executions/2024-12-20_14-30/phase1_persona/instagram_data.md
```

```
実行ID「2024-12-20_14-30」の全フェーズ完了確認。必須ファイル12個がすべて存在することを確認してください。
```

## 管理対象フォルダ構造

```
pb000_deliverables/
├── executions/
│   ├── 2024-12-20_14-30/          # 実行ID別フォルダ
│   │   ├── phase1_persona/
│   │   │   ├── persona_analysis.md
│   │   │   ├── instagram_data.md
│   │   │   └── quality_check_report.md
│   │   ├── phase2_issues/
│   │   │   ├── issue_analysis.md
│   │   │   ├── assumptions_list.md
│   │   │   └── quality_check_report.md
│   │   ├── phase3_ideas/
│   │   │   ├── generated_ideas.md
│   │   │   ├── evaluation_matrix.md
│   │   │   └── quality_check_report.md
│   │   ├── phase4_competitive/
│   │   │   ├── competitive_analysis.md
│   │   │   ├── market_research.md
│   │   │   └── quality_check_report.md
│   │   ├── phase5_positioning/
│   │   │   ├── stp_positioning.md
│   │   │   ├── lp_elements.md
│   │   │   └── quality_check_report.md
│   │   └── final_summary/
│   │       ├── gate1_handover.md
│   │       ├── executive_summary.md
│   │       └── final_quality_report.md
│   └── latest -> 2024-12-20_14-30/
├── quality_standards/
│   ├── phase1_checklist.md
│   ├── phase2_checklist.md
│   ├── phase3_checklist.md
│   ├── phase4_checklist.md
│   └── phase5_checklist.md
└── templates/
    └── execution_template/
```

## 出力

### フォルダ作成完了レスポンス

```markdown
✅ **PB-000実行用フォルダ作成完了**

実行ID: 2024-12-20_14-30
ベースパス: pb000_deliverables/executions/2024-12-20_14-30/

作成完了フォルダ:
- phase1_persona/
- phase2_issues/
- phase3_ideas/
- phase4_competitive/
- phase5_positioning/
- final_summary/

シンボリックリンク作成: latest -> 2024-12-20_14-30/

**次のステップ**: Phase1のpersona-analyzerエージェントを実行してください。
```

### ファイル存在確認レスポンス

```markdown
📋 **PB-000実行完了確認結果**

実行ID: 2024-12-20_14-30
確認日時: 2024-12-20 18:00

**必須ファイル確認結果（12/12完了）**:
✅ phase1_persona/persona_analysis.md (25.3 KB, 2024-12-20 14:35)
✅ phase1_persona/quality_check_report.md (8.7 KB, 2024-12-20 14:40)
✅ phase2_issues/issue_analysis.md (18.2 KB, 2024-12-20 15:10)
✅ phase2_issues/quality_check_report.md (7.1 KB, 2024-12-20 15:15)
✅ phase3_ideas/generated_ideas.md (32.5 KB, 2024-12-20 15:45)
✅ phase3_ideas/quality_check_report.md (9.3 KB, 2024-12-20 15:50)
✅ phase4_competitive/competitive_analysis.md (28.7 KB, 2024-12-20 16:30)
✅ phase4_competitive/quality_check_report.md (8.9 KB, 2024-12-20 16:35)
✅ phase5_positioning/stp_positioning.md (21.4 KB, 2024-12-20 17:15)
✅ phase5_positioning/lp_elements.md (15.8 KB, 2024-12-20 17:20)
✅ final_summary/gate1_handover.md (45.2 KB, 2024-12-20 17:50)
✅ final_summary/final_quality_report.md (12.6 KB, 2024-12-20 17:55)

**完了ステータス**: ✅ 全フェーズ完了（Gate1引き継ぎ準備完了）
**総データサイズ**: 233.7 KB
**実行時間**: 3時間25分（14:30 - 17:55）

**次のステップ**: Gate1（ランディングページ検証）に進行可能です。
```

### 実行履歴一覧レスポンス

```markdown
📂 **PB-000実行履歴一覧**

確認日時: 2024-12-25 10:00

| 実行ID | 実行日時 | ステータス | 完了率 | データサイズ |
|--------|---------|----------|-------|------------|
| 2024-12-20_14-30 | 2024-12-20 14:30 | ✅ 完了 | 100% | 233.7 KB |
| 2024-12-18_09-15 | 2024-12-18 09:15 | ⚠️ Phase4で中断 | 60% | 142.3 KB |
| 2024-12-15_16-00 | 2024-12-15 16:00 | ✅ 完了 | 100% | 228.1 KB |

**最新実行**: 2024-12-20_14-30（完了）
**総実行回数**: 3回
**成功率**: 66.7%（2/3）
```

## 品質基準

### 必須フォルダ構造
- ✅ phase1_persona/
- ✅ phase2_issues/
- ✅ phase3_ideas/
- ✅ phase4_competitive/
- ✅ phase5_positioning/
- ✅ final_summary/

### 必須ファイル（12個）
- ✅ Phase1: persona_analysis.md, quality_check_report.md
- ✅ Phase2: issue_analysis.md, quality_check_report.md
- ✅ Phase3: generated_ideas.md, quality_check_report.md
- ✅ Phase4: competitive_analysis.md, quality_check_report.md
- ✅ Phase5: stp_positioning.md, lp_elements.md
- ✅ Final: gate1_handover.md, final_quality_report.md

## 実行手順

1. **実行ID生成**: タイムスタンプ形式（YYYY-MM-DD_HH-MM）で新規実行IDを生成
2. **ベースフォルダ作成**: `pb000_deliverables/executions/{実行ID}/`を作成
3. **Phase別フォルダ作成**: phase1_persona ~ final_summaryの6フォルダを作成
4. **シンボリックリンク作成**: `latest`を最新実行IDにリンク
5. **テンプレートコピー**: 必要に応じてテンプレートファイルをコピー
6. **Git初期化**: 新規実行フォルダをGit管理下に追加

## 依存関係

### 必要なツール
- **Read**: ファイル存在確認・内容確認
- **Write**: テンプレートファイルのコピー
- **Glob**: 複数ファイルの一括検索
- **Git**: バージョン管理

### モデル
- **Claude Haiku**: 高速・低コストなファイル操作に最適

### 前提条件
- `pb000_deliverables/`ディレクトリが存在すること
- 書き込み権限があること
- Gitが初期化済みであること

## トラブルシューティング

### Q1: フォルダ作成に失敗する
**A**: 親ディレクトリ`pb000_deliverables/executions/`が存在するか確認してください。存在しない場合は、先に作成してください。書き込み権限も確認してください。

### Q2: シンボリックリンク（latest）が作成されない
**A**: OSがシンボリックリンクをサポートしているか確認してください。Windowsの場合は管理者権限が必要な場合があります。代替として、テキストファイルに最新実行IDを記録する方法もあります。

### Q3: ファイル存在確認で見つからないファイルがある
**A**: 該当フェーズのエージェントが正常に実行されたか確認してください。ファイル名のスペルミス、パスの誤りも確認してください。

### Q4: 実行履歴が見つからない
**A**: `pb000_deliverables/executions/`内のフォルダ一覧を確認してください。実行IDの命名規則（YYYY-MM-DD_HH-MM）に従っているか確認してください。

### Q5: Git管理でコンフリクトが発生
**A**: 同時に複数の実行を行わないでください。実行IDが重複しないように、タイムスタンプを秒単位まで含めることを検討してください。

---

## 注意事項

- 実行IDは必ずタイムスタンプ形式（YYYY-MM-DD_HH-MM）を使用してください
- フォルダ構造は厳密に守ってください（他のエージェントがパスを参照するため）
- ファイル削除は慎重に行ってください（バックアップ推奨）
- シンボリックリンク`latest`は常に最新実行を指すように更新してください

---

*このSkillは PB-000 のファイルベースデータ管理「data-manager」として実装されています。*
