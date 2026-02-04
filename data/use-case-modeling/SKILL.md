---
name: use-case-modeling
description: |
  ユースケース駆動の要件分析スキル。
  ユーザーとシステムの対話を構造化し、ビジネスロジックを明確にします。
  アクター識別から詳細シナリオ設計まで段階的に進めます。

  Anchors:
  • 『Writing Effective Use Cases』(Alistair Cockburn) / 適用: ユースケース設計 / 目的: 要件仕様の明確化
  • 『The Pragmatic Programmer』(David Thomas, Andrew Hunt) / 適用: 要件分析 / 目的: 実践的な品質維持

  Trigger:
  ユースケースモデリング、アクター分析、システム要件定義時に使用
allowed-tools:
  - Read
  - Write
  - Edit
  - Bash
  - Glob
  - Grep
---

# Use Case Modeling

## 概要

ユースケース駆動の要件分析スキル。ユーザーとシステムの対話を構造化し、ビジネスロジックを明確にします。アクター識別から詳細シナリオ設計まで段階的に進めます。

## ワークフロー

### Phase 1: 目的と前提の整理

**目的**: タスクの目的と前提条件を明確にする

**アクション**:

1. `references/Level1_basics.md` でユースケース分析の基礎を確認
2. `references/actor-identification.md` でアクター特定の方法を学習
3. 必要なリソース・スクリプト・テンプレートを特定
4. Task「要件整理」(agents/requirement-gathering.md) を実行

### Phase 2: ユースケースモデリング

**目的**: スキルの指針に従ってユースケース分析を進める

**アクション**:

1. Task「アクター分析」(agents/actor-analysis.md) でステークホルダーとアクターを特定
2. Task「ユースケース抽出」(agents/use-case-extraction.md) で主要機能をユースケースとして整理
3. `references/scenario-patterns.md` を参照しながら基本フローを記述
4. `references/use-case-relationships.md` で関係性（包含・拡張・汎化）を整理
5. テンプレート `assets/use-case-template.md` を使用して成果物を作成

### Phase 3: 検証と記録

**目的**: 成果物の検証と実行記録の保存

**アクション**:

1. `scripts/validate-use-case.mjs` でユースケース定義の整合性を確認
2. 成果物がビジネス要件に合致するか確認
3. `scripts/log_usage.mjs` を実行してフィードバックを記録

## Task仕様ナビ

ユースケース分析は以下のTask群により段階的に実行されます。各Taskはagents/に配置されており、入力・出力・制約が明記されています。

| Task名               | ファイル                        | 目的                                                                     | 入力                                 | 出力                           | 実行タイミング     |
| -------------------- | ------------------------------- | ------------------------------------------------------------------------ | ------------------------------------ | ------------------------------ | ------------------ |
| **要件整理**         | agents/requirement-gathering.md | プロジェクト背景・制約・目標を整理                                       | 要件定義ドキュメント、ビジネスゴール | 整理されたスコープ定義         | Phase 1開始時      |
| **アクター分析**     | agents/actor-analysis.md        | システムと対話するステークホルダー・ユーザーを識別                       | スコープ定義、ビジネス背景           | アクターリスト、特性定義       | Phase 2開始時      |
| **ユースケース抽出** | agents/use-case-extraction.md   | 各アクターの目的を達成するためのシステム機能をユースケースとして洗い出す | アクターリスト、ビジネスゴール       | ユースケース一覧、概要説明     | アクター分析後     |
| **詳細シナリオ記述** | agents/scenario-writing.md      | 基本フロー・代替フロー・例外フローの詳細を記述                           | ユースケース一覧                     | 完成度の高いユースケース仕様書 | ユースケース抽出後 |
| **関係性整理**       | agents/relationship-mapping.md  | ユースケース間の包含・拡張・汎化関係を整理                               | ユースケース一覧                     | ユースケース図、関係マップ     | 詳細シナリオ後     |

## ベストプラクティス

### すべきこと

- `references/Level1_basics.md` を参照して、ユースケース分析の基本原則を確認する
- `references/actor-identification.md` で提示されるチェックリストを活用してアクターの漏れを防ぐ
- `references/scenario-patterns.md` の標準パターンに従って基本フロー・代替フロー・例外フローを構造化する
- 各Taskの入出力仕様を確認し、段階ごとに成果物を検証する
- テンプレート `assets/use-case-template.md` を活用して統一された形式で記述する
- 複雑なシナリオは `references/Level3_advanced.md` で提示される視点を参考にする

### 避けるべきこと

- ユースケースの粒度（スコープ）を混在させることを避ける（詳細は `references/Level2_intermediate.md` で解説）
- アクターとロールを混同することを避ける（アクターの定義は `references/actor-identification.md` で明確化）
- シナリオ記述時に技術的な実装詳細を含めることを避ける
- 単一のメインフローだけで完結したつもりになることを避ける（代替フロー・例外フロー も明示的に記述）
- 関係性を記述せずに大量のユースケースを列挙することを避ける

## リソース・スクリプト・アセット参照

### リソース（references/）

詳細な知識や事例パターンが必要な場合、以下を参照してください（必要時にのみ読み込み）：

- **[references/Level1_basics.md](references/Level1_basics.md)**: ユースケース分析の基礎理論、基本的なアクター・シナリオの定義
- **[references/Level2_intermediate.md](references/Level2_intermediate.md)**: 実務的なテクニック、粒度の判断、制約の扱い方
- **[references/Level3_advanced.md](references/Level3_advanced.md)**: 複雑なドメインへの応用、大規模システムの事例
- **[references/Level4_expert.md](references/Level4_expert.md)**: エキスパート向けの深掘り、業界別ベストプラクティス
- **[references/actor-identification.md](references/actor-identification.md)**: アクター特定のチェックリストと判断基準
- **[references/scenario-patterns.md](references/scenario-patterns.md)**: 基本フロー・代替フロー・例外フローのパターン集
- **[references/use-case-relationships.md](references/use-case-relationships.md)**: ユースケース間の関係性（包含・拡張・汎化）の定義と活用例

### スクリプト（scripts/）

繰り返し実行される処理をスクリプトで自動化：

- `scripts/validate-use-case.mjs`: ユースケース定義の構造と整合性を検証

  ```bash
  node .claude/skills/use-case-modeling/scripts/validate-use-case.mjs <use-case-file.md>
  ```

- `scripts/log_usage.mjs`: 実行結果とフィードバックを記録
  ```bash
  node .claude/skills/use-case-modeling/scripts/log_usage.mjs --result success --phase "Phase 2" --notes "アクター分析完了"
  ```

### アセット（assets/）

出力で直接使用するテンプレートと雛形：

- **[assets/use-case-template.md](assets/use-case-template.md)**: ユースケース仕様書の標準テンプレート
- **[assets/actor-template.md](assets/actor-template.md)**: アクター定義シートのテンプレート
- **[assets/scenario-template.md](assets/scenario-template.md)**: シナリオ記述の標準フォーマット

## 変更履歴

| Version | Date       | Changes                                                                       |
| ------- | ---------- | ----------------------------------------------------------------------------- |
| 2.0.0   | 2025-12-31 | 18-skills.md仕様に準拠。Task仕様ナビを追加、frontmatterを再設計、全て日本語化 |
| 1.0.0   | 2025-12-24 | 初期版：仕様整列と必須アーティファクト追加                                    |
