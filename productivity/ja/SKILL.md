---
name: dev-cycle
version: 1.1.0
type: protocol
author: Lukas Geiger
created: 2026-03-12
updated: 2026-06-13
description: 8フェーズの開発サイクル：機能リクエスト、現状確認、機能計画、フロントエンド、バックエンド計画、バックエンドコード、テスト、ユースケース。体系的なソフトウェア開発のための反復フレームワーク。

standalone: true
anthropic_compatible: true
bach_compatible: false
bach_origin: true
category: dev
tags: [development, dev-cycle, phases, workflow, systematic, iterative]
language: ja
status: active
dependencies: {'tools': [], 'services': [], 'protocols': [], 'python': []}
provenance: {'origin': 'bach', 'origin_path': 'system/skills/workflows/dev-zyklus.md', 'origin_version': '1.0.0', 'origin_repo': 'github.com/ellmos-ai/bach', 'last_sync_from_origin': '2026-03-12', 'last_sync_to_origin': None, 'local_changes_since_sync': True}
---

<img src="../banner.png" width="100%" alt="dev-cycle banner">

> **日本語** — `dev-cycle` の公式日本語版。


# 開発サイクル (Dev Cycle) (日本語)

> **目的:** 機能リクエストから検証済みシステムに至る構造化プロセス。
> すべての開発は以下の8つのフェーズを通過します。

---

## 概要と目的

```
  +--------------------------------------------------------------+
  |                    DEVELOPMENT CYCLE                         |
  +--------------------------------------------------------------+
  |                                                              |
  |  Phase 1   Feature Requests (functional requirements)        |
  |     |                                                        |
  |     v                                                        |
  |  Phase 2   Check Current State (What already exists?)        |
  |     |                                                        |
  |     v                                                        |
  |  Phase 3   Functional Planning                               |
  |            (Workflows, Agents, Experts, Skills, Services)    |
  |     |                                                        |
  |     v                                                        |
  |  Phase 4   Implement Functional Frontend                     |
  |            (Skill files, workflow markdown, agent profiles)   |
  |     |                                                        |
  |     v                                                        |
  |  Phase 5   Plan and Align Backend                            |
  |            (CLI handlers, DB schema, API endpoints)          |
  |     |                                                        |
  |     v                                                        |
  |  Phase 6   Implement Backend Tasks                           |
  |            (Python code, tools, DB migrations)               |
  |     |                                                        |
  |     v                                                        |
  |  Phase 7   Technical Tests and Bugfixes                      |
  |            (B/O/E tests, bugfix protocol)                    |
  |     |                                                        |
  |     v                                                        |
  |  Phase 8   Functional and Feature Test: USE CASES            |
  |            (End-to-end validation from user perspective)      |
  |                                                              |
  +--------------------------------------------------------------+

  Core principles throughout:
  - Functional description first (before code)
  - CLI First (everything controllable via terminal)
  - Clear separation of user data and system data
```

---

## フェーズ 1: 機能リクエスト (機能要件)

**内容:** 機能要件の収集および策定。

**入力:**
- ユーザーの要望、アイデア、課題
- パートナーからの提案（LLMアシスタント）
- ユースケースからの知見（フィードバックループ！）

**出力:**
- タスク管理システム内のタスク（例：Issue、チケット、TODOリストとして）
- 要件は「何を行いたいか」(WHAT) を記述し、「どのように行うか」(HOW) は記述しない

**ルール:**
- 要件は常に機能的に記述する（「ユーザーがXを行える」）
- 技術的に記述しない（「XのためのRESTエンドポイントを実装する」など）
- ユースケースを要件のソースとして活用する（フェーズ 8 -> フェーズ 1）

---

## フェーズ 2: 現状確認

**内容:** 既存機能のインベントリ調査。

**チェックリスト:**
```
  [ ] Search existing tools/scripts
  [ ] Check documentation/help on the topic
  [ ] Check existing skills/agents/services
  [ ] Check DB schema (if relevant)
  [ ] Check use cases - has something similar been tested?
```

**出力:**
- 既存のもの、不足しているもの、拡張が必要なもののドキュメント化
- 重複作業の回避

---

## フェーズ 3: 機能計画

**内容:** 機能レベルでの計画 — すぐにコードを書かないこと。

**計画レベル:**

| レベル | 問い | 成果物 |
|-------|----------|----------|
| Workflow | いつ/どのように調整を行うか？ | workflows/*.md |
| Agent | 誰が実行するか？ | agents/*.txt |
| Expert | 誰がドメイン知識を持っているか？ | experts/*/ |
| Skill | 何を行うか？ | skills/*.md |
| Service | 技術的にどのように実現するか？ | services/*/ |

**ルール:**
- まず機能的に考え、次に技術的に考える
- ワークフローはプロセスを記述し、実装の詳細には触れない
- すべてのアジエントには明確なプロフィールが必要
- サービスはユーザーデータなしで機能しなければならない

---

## フェーズ 4: 機能フロントエンドの実装

**内容:** スキルファイル、ワークフローのMarkdown、エージェントプロフィールの作成。

ここでの「フロントエンド」とは機能記述層を指します：
- ワークフローファイル (.md)
- エージェントプロフィール (.txt)
- 専門家知識 (Expert knowledge)
- サービス記述
- ヘルプファイル

**出力:**
- すべての機能記述が存在する
- LLMパートナーがワークフローを読み込み理解できる
- 機能層が完全にドキュメント化されている

---

## フェーズ 5: バックエンドの計画と調整

**内容:** 技術アーキテクチャを機能フロントエンドに合わせる。

**計画領域:**

| 領域 | 問い | 配置場所 |
|------|----------|----------|
| CLI Handlers | どのコマンドか？ | handlers/*.py |
| DB Schema | どのテーブル/カラムか？ | schema/*.sql |
| API Endpoints | どのGUIエンドポイントか？ | server.py |
| Tools | どのPythonスクリプトか？ | tools/*.py |

**出力:**
- 機能フロントエンドに合わせた技術計画
- データベーススキーマ設計
- CLIコマンド構造

---

## フェーズ 6: バックエンドタスクの実装

**内容:** Pythonコード、DBマイグレーション、CLIハンドラーの記述。

**チェックリスト（タスクごと）:**
```
  [ ] Works without user data (empty DB)?
  [ ] CLI command available?
  [ ] Input can come from files/folders?
  [ ] Output goes to structured DB?
  [ ] Scan/import is repeatable (idempotent)?
  [ ] No hardcoded path?
  [ ] Tool registered and documented?
  [ ] Help file created?
```

---

## フェーズ 7: 技術テストとバグ修正

**内容:** 技術的な正確性の確保。

**テスト種別 (B/O/E):**

| 種別 | 視点 | 説明 |
|------|-------------|-------------|
| B-Tests | 外部/自動化 | 自動テスト、CI/CD |
| O-Tests | 機能的 (入力->出力) | 手動での機能検証 |
| E-Tests | 主観的/体験 | UX評価、エルゴノミクス |

**バグ発生時:**
- バグ修正プロトコル (bugfix protocol) を適用する
- 20分ルールを守る（20分経過しても解決しない場合はアプローチを変更）
- 学んだ教訓 (lessons learned) を記録する

---

## フェーズ 8: 機能およびフィーチャーテスト — ユースケース

**内容:** ユーザー視点からのエンドツーエンド (End-to-end) 検証。

**ユースケースは両方の目的を果たします:**
1. **機能の指標** — 何が求められているか？何が可能であるべきか？
2. **テストシナリオ** — AからZまで実際に機能するか？

**ユースケースフォーマット:**
```
  USECASE_NNN: Short Title

  PRECONDITION: What must be in place?
  INPUT:        What does the user enter / what data?
  EXPECTED:     What should the result be?
  TESTS:        Which components are tested?
```

**フィードバックループ:**
- 失敗したユースケース -> フェーズ 1 の新しいタスクへ
- 成功したユースケース -> 検証済み機能へ
- 新しいユースケースのアイデア -> タスクとして記録

---

## まとめ: サイクル

```
  Phase 8 (Use Cases)
       |
       | New requirements / bugs
       v
  Phase 1 (Feature Requests)  -->  Phase 2 (Current State)
       ^                                    |
       |                                    v
  Phase 7 (Tests/Bugs)         Phase 3 (Functional Planning)
       ^                                    |
       |                                    v
  Phase 6 (Backend Code)       Phase 4 (Functional Frontend)
       ^                                    |
       |                                    v
       +──────────────────── Phase 5 (Backend Planning)
```

サイクルはループです: ユースケースによって機能が検証されると同時に、新たな要件が生成されます。

---

## フェーズ固有のスキル

| フェーズ | 専門スキル | トリガー |
|-------|-------------------|---------|
| フェーズ 1-3 | Project bootstrapper (利用可能な場合) | 新規プロジェクトの作成 (新規開発 / greenfield) |
| フェーズ 2 | [project-onboarding](../../project-onboarding/SKILL.en.md) | 既存プロジェクトの引き継ぎ |
| フェーズ 2-3 | [docs-analysis](../../docs-analysis/SKILL.en.md) | 要件定義書とコードの照合 |
| フェーズ 5-6 | [pipeline-optimizer](../../pipeline-optimizer/SKILL.en.md) | 既存構造の刷新・リファクタリング |
| フェーズ 7 | [bugfix-protocol](../../bugfix-protocol/SKILL.en.md) | 体系的な6段階デバッグ |
| フェーズ 7-8 | [bugsweep](../../bugsweep/SKILL.en.md) | リリース前の収束型バグスイープ |

スキルコレクションにスキルインデックスがある場合は、より多くのフェーズ固有スキルを検索してください。

---

## 変更履歴

### 1.1.0 (2026-06-13)
- project-onboarding, docs-analysis, pipeline-optimizer, bugfix-protocol, bugsweep への参照を含む「フェーズ固有のスキル」テーブルを新規追加

### 1.0.0 (2026-03-12)
- BACH (dev-zyklus v1.0.0) より移植

---

*作成日: 2026-01-28 | 移植日: 2026-03-12*
