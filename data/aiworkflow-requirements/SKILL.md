---
name: aiworkflow-requirements
description: |
  AIWorkflowOrchestratorプロジェクトの仕様管理スキル。
  仕様書を検索・参照するためのインターフェース。
  references/配下に全仕様を格納し、キーワード検索で必要な情報に素早くアクセス。

  Anchors:
  • Specification-Driven Development / 適用: 仕様書正本 / 目的: 実装との一貫性
  • Progressive Disclosure / 適用: 検索→詳細参照 / 目的: コンテキスト効率化
  • MECE原則 / 適用: トピック分類 / 目的: 漏れなく重複なく

  Trigger:
  プロジェクト仕様の検索、アーキテクチャ確認、API設計参照、セキュリティ要件確認、テスト戦略参照を行う場合に使用。
  仕様, 要件, アーキテクチャ, API, データベース, セキュリティ, UI/UX, デプロイ, Claude Code, テスト, MSW, カバレッジ, PermissionStore, 権限永続化, rememberChoice
allowed-tools:
  - Read
  - Glob
  - Grep
  - Bash
---

# AIWorkflow Requirements Manager

## 概要

AIWorkflowOrchestratorプロジェクトの全仕様を管理するスキル。
**このスキルが仕様の正本**であり、references/配下のドキュメントを直接編集・参照する。

## クイックスタート

### 仕様を探す

```bash
# キーワード検索（推奨）
node scripts/search-spec.js "認証" -C 5

# または resource-map.md でタスク種別から逆引き
```

### 仕様を読む

1. **まず [resource-map.md](indexes/resource-map.md) を確認** - タスク種別に応じた読み込みファイルを特定
2. 該当ファイルを `Read` ツールで参照
3. 詳細行番号が必要な場合は [topic-map.md](indexes/topic-map.md) を参照

### 仕様を作成・更新

1. `assets/` 配下の該当テンプレートを使用
2. `references/spec-guidelines.md` の命名規則に従う
3. 編集後は `node scripts/generate-index.js` を実行

## ワークフロー

```
                    ┌→ search-spec ────┐
user-request → ┼                       ┼→ read-reference → apply-to-task
                    └→ browse-index ───┘
                              ↓
                    (仕様変更が必要な場合)
                              ↓
              ┌→ create-spec ──────────┐
              ┼                         ┼→ update-index → validate-structure
              └→ update-spec ──────────┘
```

## Task仕様ナビ

| Task               | 責務           | 起動タイミング     | 入力         | 出力             |
| ------------------ | -------------- | ------------------ | ------------ | ---------------- |
| search-spec        | 仕様検索       | 仕様確認が必要な時 | キーワード   | ファイルパス一覧 |
| browse-index       | 全体像把握     | 構造理解が必要な時 | なし         | トピック構造     |
| read-reference     | 仕様参照       | 詳細確認が必要な時 | ファイルパス | 仕様内容         |
| create-spec        | 新規作成       | 新機能追加時       | 要件         | 新規仕様ファイル |
| update-spec        | 既存更新       | 仕様変更時         | 変更内容     | 更新済みファイル |
| update-index       | インデックス化 | 見出し変更後       | references/  | indexes/         |
| validate-structure | 構造検証       | 週次/リリース前    | 全体         | 検証レポート     |

## リソース参照

### 仕様ファイル一覧

See [indexes/resource-map.md](indexes/resource-map.md)（読み込み条件付き）

詳細セクション・行番号: [indexes/topic-map.md](indexes/topic-map.md)

| カテゴリ         | 主要ファイル                                                         |
| ---------------- | -------------------------------------------------------------------- |
| 概要・品質       | overview.md, quality-requirements.md                                 |
| アーキテクチャ   | **architecture-overview.md**, architecture-patterns.md, arch-\*.md   |
| インターフェース | interfaces-agent-sdk.md, llm-\*.md, rag-search-\*.md                 |
| API設計          | api-endpoints.md, api-ipc-\*.md                                      |
| データベース     | database-schema.md, database-implementation.md                       |
| UI/UX            | ui-ux-components.md, ui-ux-design-principles.md, ui-history-\*.md    |
| セキュリティ     | security-principles.md, security-electron-ipc.md, security-\*.md     |
| 技術スタック     | technology-core.md, technology-frontend.md, technology-desktop.md    |
| Claude Code      | claude-code-overview.md, claude-code-skills-\*.md                    |
| デプロイ・運用   | deployment.md, deployment-electron.md, environment-variables.md      |
| ガイドライン     | spec-guidelines.md, development-guidelines.md, architecture-implementation-patterns.md, rag-\*.md |

**注記**: 18-skills.md（Skill層仕様書）は `skill-creator` スキルで管理。

### scripts/

| スクリプト              | 用途                | 使用例                                        |
| ----------------------- | ------------------- | --------------------------------------------- |
| `search-spec.js`        | キーワード検索      | `node scripts/search-spec.js "認証" -C 5`     |
| `list-specs.js`         | ファイル一覧        | `node scripts/list-specs.js --topics`         |
| `generate-index.js`     | インデックス再生成  | `node scripts/generate-index.js`              |
| `validate-structure.js` | 構造検証            | `node scripts/validate-structure.js`          |
| `select-template.js`    | テンプレート選定    | `node scripts/select-template.js "IPC仕様"`   |
| `split-reference.js`    | 大規模ファイル分割  | `node scripts/split-reference.js <file>`      |
| `remove-heading-numbers.js` | 見出し番号削除  | `node scripts/remove-heading-numbers.js`      |
| `log_usage.js`          | 使用状況記録        | `node scripts/log_usage.js --result success`  |

### agents/

| エージェント       | 用途         | 対応Task           | 主な機能                        |
| ------------------ | ------------ | ------------------ | ------------------------------- |
| `create-spec.md`   | 新規仕様作成 | create-spec        | テンプレート対応、重複チェック   |
| `update-spec.md`   | 既存仕様更新 | update-spec        | テンプレート準拠、分割ガイド    |
| `validate-spec.md` | 仕様検証     | validate-structure | resource-map登録確認、サイズ検証 |

### indexes/

| ファイル             | 内容                                       | 用途                  |
| -------------------- | ------------------------------------------ | --------------------- |
| `quick-reference.md` | キー情報の即時アクセス（推奨・最初に読む） | パターン/型/IPC早見表 |
| `resource-map.md`    | リソースマップ（読み込み条件付き）         | タスク種別→ファイル   |
| `topic-map.md`       | トピック別マップ（セクション・行番号詳細） | セクション直接参照    |
| `keywords.json`      | キーワード索引（自動生成）                 | スクリプト検索用      |

> **Progressive Disclosure**: まずresource-map.mdでタスクに必要なファイルを特定し、必要なファイルのみを読み込む。

### templates/

新規仕様書作成時のテンプレート。`node scripts/select-template.js` で自動選定可能。

| ファイル                   | 用途                           | 対象カテゴリ     |
| -------------------------- | ------------------------------ | ---------------- |
| `spec-template.md`         | 汎用仕様テンプレート           | 概要・品質       |
| `interfaces-template.md`   | インターフェース仕様           | インターフェース |
| `architecture-template.md` | アーキテクチャ仕様             | アーキテクチャ   |
| `api-template.md`          | API設計                        | API設計          |
| `ipc-channel-template.md`  | Electron IPC                   | IPC通信          |
| `react-hook-template.md`   | React Hook                     | カスタムフック   |
| `service-template.md`      | サービス層                     | ビジネスロジック |
| `database-template.md`     | データベース仕様               | データベース     |
| `ui-ux-template.md`        | UI/UX仕様                      | UI/UX            |
| `security-template.md`     | セキュリティ仕様               | セキュリティ     |
| `testing-template.md`      | テスト仕様                     | テスト戦略       |

> **注記**: 詳細はtemplates/配下を直接参照。追加テンプレートが必要な場合は `agents/create-spec.md` を参照。

### references/（ガイドライン）

| ファイル                       | 内容                           |
| ------------------------------ | ------------------------------ |
| `spec-guidelines.md`           | 命名規則・記述ガイドライン     |
| `spec-splitting-guidelines.md` | 大規模ファイル分割ガイドライン |

### 連携スキル

| スキル                       | 用途                                                   |
| ---------------------------- | ------------------------------------------------------ |
| `task-specification-creator` | タスク仕様書作成、Phase 12での仕様更新ワークフロー管理 |

**Phase 12 仕様更新時**: `.claude/skills/task-specification-creator/references/spec-update-workflow.md` を参照

### 運用ファイル

| ファイル     | 用途                         |
| ------------ | ---------------------------- |
| `EVALS.json` | スキルレベル・メトリクス管理 |
| `LOGS.md`    | 使用履歴・フィードバック記録 |

## ベストプラクティス

### すべきこと

- キーワード検索で情報を素早く特定
- 編集後は `node scripts/generate-index.js` を実行
- 500行超過時はインデックス+サブファイル形式に手動分割

### 避けるべきこと

- references/以外に仕様情報を分散
- インデックス更新を忘れる
- 詳細ルールをSKILL.mdに追加（→ spec-guidelines.md へ）

**詳細ルール**: See [references/spec-guidelines.md](references/spec-guidelines.md)

## 変更履歴

| Version | Date       | Changes                                                                                                                                                                                                                                                        |
| ------- | ---------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| 8.6.0   | 2026-01-26 | **仕様ガイドライン完全準拠**: 全134ファイル（133ファイルコードブロック除去完了、spec-guidelines.md除く）のspec-guidelines.md準拠修正。82参照ファイルのTypeScript/JSON/SQL/ASCIIダイアグラムを表形式・文章に変換                                               |
| 8.5.0   | 2026-01-26 | **仕様ガイドライン準拠修正**: architecture-overview.md/technology-desktop.md（ディレクトリ構造を表形式化）、development-guidelines.md/architecture-implementation-patterns.md（コード例を表形式・文章に変換）、templates全11種（コード例を表形式に変換）     |
| 8.4.0   | 2026-01-26 | **実装パターン総合ガイド追加**: architecture-implementation-patterns.md新規作成（フロントエンド/バックエンド/デスクトップ/パフォーマンス/セキュリティ/テスト/アクセシビリティ実装パターン網羅）                                                                |
| 8.3.0   | 2026-01-26 | **開発ガイドライン拡充**: development-guidelines.md v1.1.0（命名規則、デバッグガイド、リリースプロセス、バックアップ・リカバリ、環境構築ガイド追加）                                                                                                             |
| 8.2.0   | 2026-01-26 | **UX法則・開発ガイドライン追加**: ui-ux-design-principles.mdにUXデザイン法則（Fitts, Hick, Jakob, Miller, Gestalt, Progressive Disclosure等）追加、development-guidelines.md新規作成（ロギング、キャッシング、マイグレーション、コードレビュー、i18n）          |
| 8.1.0   | 2026-01-26 | **アーキテクチャ総論追加**: architecture-overview.md新規作成、technology-frontend.md/technology-desktop.md追加、templates/ディレクトリ新設（テンプレート11種）                                                                                                |
| 8.0.0   | 2026-01-26 | **大規模リファクタリング**: 94→129ファイル拡張（+35分割ファイル）、resource-map.md全ファイル網羅（v1.2.0）、エージェント3件v2.1.0更新、Progressive Disclosure原則に基づくインデックス最適化                                                                    |
| 7.2.0   | 2026-01-26 | **エージェント改善**: create-spec/update-spec/validate-spec v2.0.0更新（16テンプレート対応、select-template.js統合、quick-reference.md/resource-map.md参照追加、テンプレート準拠検証ワークフロー追加）                                                         |
| 7.1.0   | 2026-01-26 | **追加最適化**: 16種テンプレート（ipc-channel, react-hook, service, error-handling, testing追加）、quick-reference.md新設、indexes/セクション強化                                                                                                              |
| 7.0.0   | 2026-01-26 | **スキルリファクタリング**: 11種テンプレート追加、interfaces-agent-sdk.md分割（6ファイル）、resource-map.md新設（読み込み条件付き）、spec-splitting-guidelines.md追加、SKILL.mdクイックスタート追加。94ファイル・11カテゴリ構成に拡張                          |
| 6.31.0  | 2026-01-26 | TASK-3-1-E完了: security-skill-execution.mdにPermission Storeセクション追加、ui-ux-settings.mdにPermissionSettings UI追加、interfaces-agent-sdk.md更新。159テスト・96%カバレッジ達成                                                                           |
| 6.30.0  | 2026-01-26 | TASK-4-2完了: interfaces-agent-sdk.md v2.2.0更新（PermissionResolver IPC Handlers完了記録、IPCチャンネル2種、Preload API、usePermissionDialog Hook、PermissionDialog）、security-api-electron.md更新（Permission IPCセキュリティ）。93テスト・94.67%カバレッジ |
| 6.29.0  | 2026-01-26 | TASK-3-1-D完了: interfaces-agent-sdk.md v2.3.0更新（skillAPI.onPermission/respondPermission、useSkillPermission Hook、型定義）、security-api-electron.md更新（IPC channels、テストカバレッジ）。124テスト・100%カバレッジ                                      |
| 6.28.0  | 2026-01-25 | TASK-3-2完了: security-api-electron.mdにSkill Execution Preload APIセキュリティセクション追加（IPCチャンネル4種、ホワイトリスト、ストリーミングセキュリティ、React Hook統合）。138テスト・100%カバレッジ                                                       |
| 6.27.0  | 2026-01-25 | UI-CONV-HISTORY-001完了: interfaces-chat-history.md v1.2.0更新（Renderer Process型定義、Preload API、React Hooks、UIコンポーネント構成、アクセシビリティ対応）。280テスト・98.66%カバレッジ達成                                                                |
| 6.26.0  | 2026-01-24 | UT-LLM-HISTORY-001完了: interfaces-llm.md（Conversation/Message型、IPC契約7種）、architecture-patterns.md（会話履歴永続化パターン〜100行）追加。114テスト・100%カバレッジ達成                                                                                  |
| 6.25.0  | 2026-01-24 | TASK-2B SkillImportStore追加: interfaces-agent-sdk.mdに「SkillImportStore（TASK-2B）」セクション新設（スキーマ・API・セキュリティ・テスト仕様詳細約230行）、SkillImportManagerとの差分表追加                                                                   |
| 6.24.0  | 2026-01-24 | スキル実行セキュリティ追加（TASK-2C完了）: security-skill-execution.md新規作成（危険コマンド24パターン、保護パス25、許可ツール11）、security-implementation.mdにリンク追加、91ファイル構成                                                                     |
| 6.23.0  | 2026-01-24 | SkillScanner将来改善ロードマップ追加: architecture-patterns.md（3件の未タスク仕様書記録：キャッシュ/増分スキャン/ページネーション、想定追加型定義）                                                                                                            |
| 6.22.0  | 2026-01-24 | TASK-2A（SkillScanner実装）完了: interfaces-agent-sdk.md（ScannedSkillMetadata/SkillScannerOptions型、完了記録）、architecture-patterns.md（SkillScannerサブセクション追加：API/定数/セキュリティ/データフロー）                                               |
| 6.21.0  | 2026-01-23 | Workspace Chat Edit追加: interfaces-llm.md（FileContext/EditCommand/GeneratedResult型）、architecture-patterns.md（chatEditSliceパターン）、api-endpoints.md（chat-edit IPCチャネル4種）追加、89ファイル構成                                                   |
| 6.20.0  | 2026-01-23 | TASK-1-1型定義追加: interfaces-agent-sdk.mdに「Skill Import Agent System 型定義（TASK-1-1）」セクション新設（16型詳細仕様）、連携スキル参照追加、88ファイル構成に拡張                                                                                          |
| 6.19.0  | 2026-01-22 | React Context DI追加（UT-006完了）: architecture-chat-history.mdにUI Layerセクション追加（ChatHistoryContext/Provider/useChatHistory/MockProvider）、topic-map.md更新、8アーキテクチャファイル構成                                                             |
| 6.18.0  | 2026-01-22 | Drizzle Repository実装追加: architecture-chat-history.md更新（DrizzleChatSessionRepository/DrizzleChatMessageRepository、エラーハンドリング、テスト構成）                                                                                                      |
| 6.17.0  | 2026-01-21 | スキル管理IPC整合性修正: interfaces-agent-sdk.mdのIPCチャンネル名を実装に合わせて更新（`skill:list`→`skill:list-imported`等）、戻り値型を`OperationResult`に統一                                                                                               |
| 6.16.0  | 2026-01-21 | 統計更新: ファイル数85、行数約20,000行に更新。CONV-06-04（NER）/CONV-07-02（FTS5）完了反映                                                                                                                                                                     |
| 6.15.0  | 2026-01-19 | NER仕様独立化&FTS5詳細化: interfaces-rag-entity-extraction.md新規作成、interfaces-rag-search.md FTS5/BM25詳細追加（テーブル構造、クエリパターン、データフロー）、85ファイル構成に拡張                                                                          |
| 6.14.0  | 2026-01-19 | スキル実行機能追加: interfaces-agent-sdk.mdに`skill:execute`IPC/`skillAPI.execute`/`SkillRunResult`型/`OperationResult`型追加、関連ドキュメントリンク追加                                                                                                      |
| 6.13.0  | 2026-01-19 | CONV-06-04完了: エンティティ抽出サービス(NER) Phase 12完了。interfaces-rag.md/architecture-rag.md更新（224テスト、97.1%カバレッジ、96.8%品質スコア）                                                                                                           |
| 6.12.0  | 2026-01-18 | SECURITY-001完了: interfaces-chat-history.md v2.0.0更新（認可セクション追加、requestUserIdパラメータ、BR-SESSION-005）、error-handling.md更新（ERR_2006 UNAUTHORIZED、UnauthorizedErrorクラス詳細）                                                            |
| 6.11.0  | 2026-01-17 | architecture-patterns.md更新: IPC Handler Registration Pattern追加（SKILL-IPC-001完了記録、登録パターン3種の文書化、セキュリティ要件）                                                                                                                         |
| 6.10.0  | 2026-01-14 | ui-ux-settings.md新規追加: スライド出力ディレクトリ設定機能のUI/UX仕様・IPC API仕様・セキュリティ要件（slideSettingsAPI）                                                                                                                                      |
| 6.9.0   | 2026-01-13 | Knowledge Graph Store実装完了: interfaces-rag-knowledge-graph-store.md v1.0.1更新、実装詳細追加（Entity/Relation CRUD、グラフ探索、バッチ操作）、カバレッジ86.98%達成                                                                                          |
| 6.8.0   | 2026-01-13 | AgentSDKPage Postrelease Testing仕様追加: interfaces-agent-sdk.mdに約150行追加（AGENT-005-POST）                                                                                                                                                               |
| 6.7.0   | 2026-01-12 | 未タスク指示書3件作成（renderer-build-fix、history-gui-manual-test、error-i18n-support）、ui-ux-history-panel.md v1.6.0更新                                                                                                                                    |
| 6.6.1   | 2026-01-12 | history-service-db-integration実装内容追加: architecture-file-conversion.md、api-internal-conversion.mdにElectron統合セクション追加                                                                                                                            |
| 6.6.0   | 2026-01-12 | VectorSearchStrategy仕様追加: interfaces-rag-search.mdにISearchStrategy実装一覧/Result型/フィルタ対応表/CachedVectorSearchStrategy追加、architecture-rag.mdにVectorSearchStrategyセクション追加                                                                |
| 6.5.0   | 2026-01-12 | Agent Execution UI仕様追加（AGENT-004）: interfaces-agent-sdk.md/ui-ux-components.mdに約550行追加、topic-map.md更新                                                                                                                                            |
| 6.4.0   | 2026-01-12 | GraphRAGクエリサービス仕様追加: interfaces-rag-graphraph-query.md新規、architecture-rag.md更新、topic-map.md更新                                                                                                                                               |
| 6.3.0   | 2026-01-11 | コミュニティ要約仕様追加: interfaces-rag-community-summarization.md新規、interfaces-rag-community-detection.md更新（v1.1.0）、topic-map.md更新                                                                                                                 |
| 6.2.0   | 2026-01-10 | コミュニティ検出（Leiden）仕様追加: interfaces-rag-community-detection.md新規、interfaces-rag.md/architecture-rag.md/topic-map.md更新                                                                                                                          |
| 6.1.0   | 2026-01-06 | 500行超過ファイル分割（9ファイル→インデックス化）、70ファイル構成に拡張                                                                                                                                                                                        |
| 6.0.0   | 2026-01-06 | skill-creator準拠: agents/をTask仕様書テンプレート化、EVALS.json/LOGS.md/log_usage.js追加                                                                                                                                                                      |
| 5.0.0   | 2026-01-04 | SKILL.md軽量化、詳細をindexes/references/へ分離                                                                                                                                                                                                                |
| 4.0.0   | 2026-01-03 | kebab-case化、大ファイル分割、47ファイル構成                                                                                                                                                                                                                   |
| 3.0.0   | 2026-01-03 | 仕様正本化、検索中心に再設計                                                                                                                                                                                                                                   |
