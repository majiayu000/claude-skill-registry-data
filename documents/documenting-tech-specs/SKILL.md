---
name: documenting-tech-specs
description: |-
  技術 spec (tech_specs) のテンプレートとガイドラインを提供する。feature の技術設計とテスト設計（`docs.lineup` が single なら TECH_DESIGN / TEST_PLAN、layered なら API_DESIGN / SCREEN_DESIGN / API_TEST_DESIGN / SCREEN_TEST_DESIGN / TEST_DESIGN）と、common 階層の ARCHITECTURE / TABLE_DEFINITION / API_SPEC / DESIGN を扱う。「技術設計（How）」の SSoT。要件は documenting-requirements を使う。
when_to_use: |-
  「技術設計」「API 設計」「画面設計」「テスト設計」「テスト戦略」「レスポンスコード」「画面項目定義」「TECH_DESIGN」「ARCHITECTURE」「テーブル定義」「API 仕様」「DESIGN.md」に関する作業のとき。業務・機能・非機能要件は documenting-requirements を使う。
allowed-tools: Read, Write, Edit, Glob, Grep
---

# 技術 spec (tech_specs) の作成

STDD（Spec and Test Driven Development）方法論に従って、技術系の設計書（総称 **技術 spec / tech_specs**）を作成・更新します。
構成の考え方は方法論の [`spec-lineup.md`](../../../packages/core/docs/spec-lineup.md) にあります。

> **前提**: 技術設計は REQUIREMENTS.md（要件）が確定していることを前提とする。要件の作成は [documenting-requirements Skill](../documenting-requirements/SKILL.md) を使う。**SSOT原則・要確認マーカーのSSoTも documenting-requirements にある**ため、本スキルでもそれに従う（後述「絶対ルール」参照）。

## Quick Start

書き始める前に [guides/writing-procedure.md](guides/writing-procedure.md)（前提・読むもの・追記か新規か・書かないもの・構成ごとの書く順序）を確かめる。

### 1. 構成（ラインナップ）を確かめる

feature の技術 spec の構成は `.stdd.config.yml` の `docs.lineup` で決まる（省略時は `single`）。配置は `docs.layout.*` に従う。

| `docs.lineup` | feature の技術 spec | テンプレート |
| --- | --- | --- |
| `single` | `TECH_DESIGN.md`（技術設計）/ `TEST_PLAN.md`（テスト戦略） | [tech-design](templates/tech-design.md) / [test-plan](templates/test-plan.md) |
| `layered` | バックエンド: `API_DESIGN.md` / `API_TEST_DESIGN.md` | [api-design](templates/api-design.md) / [api-test-design](templates/api-test-design.md) |
| | フロントエンド: `SCREEN_DESIGN.md` / `SCREEN_TEST_DESIGN.md` | [screen-design](templates/screen-design.md) / [screen-test-design](templates/screen-test-design.md) |
| | 機能全体のテストの担保: `TEST_DESIGN.md` | [test-design](templates/test-design.md) |

- `layered` で API を持たない機能は API の 2 本を、画面を持たない機能は画面の 2 本を作らない。
- 各テンプレートは、記法ルール・記載基準のチェックリスト・書かない内容（ほかの文書との分担）・更新履歴を持つ。
  書いた文書の末尾には、基づいたテンプレートの版（`テンプレート版: X.Y`）を残す。
- 章名・表の列名は [references/doc-structure.json](references/doc-structure.json) が既定で、`docs.structure` で上書きできる。
  検査はこの名前で章と表を見分けるので、テンプレートにない番号付きの章を足したり、列名を言い換えたりしない。
- API を持つ構成では、[レスポンスコード体系](guides/response-codes.md)に従う（帯・1 分岐 1 コード・共通コード。`response_codes` で上書き可）。

### 2. 新機能の技術 spec を作成する

REQUIREMENTS.md（要件）が確定している前提で、構成ごとに [writing-procedure.md §6](guides/writing-procedure.md) の順に書く。

- **トレーサビリティ ID を貫通させる**: 要件 ID（`UC-<feature>-NN`）を設計書（TECH_DESIGN §1.1 ／ API_DESIGN・SCREEN_DESIGN の基本情報表）と
  テスト計画（TEST_PLAN ／ TEST_DESIGN）に載せ、その他処理フロー `FL-<feature>-NN` は設計書（TECH_DESIGN §4.2 ／ API_DESIGN 章 4）で宣言する。
  抜け漏れは `bash .claude/hooks/trace-audit.sh` で機械検知する。
- データ構造は common の `TABLE_DEFINITION.md`、API の形は common の `API_SPEC.md` を**参照**する（再定義しない）。
  新規テーブル / API が生じたら common を更新し、feature からは参照する。

### 3. common 階層の技術ドキュメントを作成する

```
docs/common/ARCHITECTURE.md / TABLE_DEFINITION.md / API_SPEC.md / DESIGN.md
```

- **ARCHITECTURE.md**: システム概要（構成 / スタック / 連携 / セキュリティ / インフラ）。データモデル・API は持たない。[テンプレート](templates/architecture-common.md)
- **TABLE_DEFINITION.md**: 全テーブル定義のSSoT（カード形式・ER 図なし）。feature が参照する。[テンプレート](templates/table-definition-common.md)
- **API_SPEC.md**: API 契約（形）のSSoT（OpenAPI 風 Markdown）。feature が参照する。[テンプレート](templates/api-spec-common.md)
- **DESIGN.md**（任意）: デザイン標準。[テンプレート](templates/design-common.md)

既存実装からの common 技術 spec 作成は `reverse-engineering-common-spec` スキルを参照。

### 4. 既存機能の技術 spec を更新する

1. 対応する技術 spec を読み、変更が及ぶ文書をすべて特定する（`layered` では、設計書を変えたら対になるテスト設計と TEST_DESIGN も見る）
2. 変更内容に応じて更新する（テーブル・API の変更は common の TABLE_DEFINITION / API_SPEC に反映）
3. 文書が古い版のテンプレートに基づくときは、テンプレートの更新履歴の手順で新しい版に合わせる

## Spec の 2 階層構造（common / feature）

| 階層      | 技術ドキュメント | 配置例 |
| ----------- | --- | --- |
| **common**  | `ARCHITECTURE.md` / `TABLE_DEFINITION.md` / `API_SPEC.md` / `DESIGN.md`（任意） | `docs/common/` |
| **feature** | 上の「構成」の表のとおり | `docs/<app>/<feature>/` |

- feature の技術 spec は common 階層（システム構成・テーブル定義・API 仕様）を**前提とし、参照する**。**テーブル・API の形は feature で再定義しない**。
- 配置先は `.stdd.config.yml` の `docs.layout.*` に、対象アプリの `app`（`apps[].id`）と `feature_path` を適用して決める。

## 絶対ルール: SSOT原則・要確認マーカー（最優先）

⚠️ **Specドキュメントは「現在の最新仕様」だけを記述するSingle Source of Truth（SSOT）である**。履歴・経緯・対応中のissue・「今回の変更」は一切書かない。

技術設計ドキュメントでも特に出やすい違反:

- テスト戦略表で `✅ (更新に統合)` `2 ケースに集約` `1 テストにまとめる方針` のように「以前は別だったが今はまとめてある」ことを匂わせる表現
- ロジック・設計判断で `変更前/変更後` `〜だったが〜に変更した` `今回追加した設計` 等

常に**現在の構成事実のみ**を記述する。設計判断の理由は「**この構成を採る**理由」として書き、「変更そのものの理由」は書かない。
末尾の `テンプレート版: X.Y` は履歴ではなく、文書が従う書式の宣言である。

> **SSOT原則・要確認マーカーの完全な定義（禁止語リスト・Self-check・違反例・マーカー構文）は [documenting-requirements SKILL「絶対ルール: SSOT原則」「要確認マーカー」](../documenting-requirements/SKILL.md) がSSoT**。技術設計でも同じルール・同じ Self-check（禁止語 grep）を適用すること。詳細な違反例は [STDD違反例と対策](../documenting-requirements/guides/stdd-violations.md) を参照。

## 書かない内容（共通）

- 実装例・コード例（関数・メソッドの実装）。擬似コード・型 I/F・計算式は可（`layered` の API_DESIGN は手順と計算式で書く）
- テーブル・カラム定義（→ common `TABLE_DEFINITION.md`）/ API の形（→ common `API_SPEC.md`）
- 業務要件・機能要件・非機能要件（→ REQUIREMENTS.md）
- ファイル構成・実装順序（→ PLANドキュメント）

文書ごとの分担は各テンプレートの「記述しない内容」に従う。

## Priority（優先度）とテスト戦略

テスト戦略は REQUIREMENTS の Priority（P0/P1/P2）に従う。各 Priority で求めるテストレベル（P0 は E2E 必須 + Integration など）は [documenting-requirements「Priority（優先度）ガイドライン」](../documenting-requirements/SKILL.md) を正本とする。

## 次のステップ

技術 spec の作成・レビュー（人間レビュー含む）が完了したら:

1. **PLANドキュメントを作成** → [documenting-plans Skill](../documenting-plans/SKILL.md)（`docs.layout.plan` がある場合）
2. テスト作成・実装を進める

## When NOT to Use This Skill

- **要件のみ**: 業務要件・機能要件・非機能要件・ユースケース → documenting-requirements
- **単純なバグ修正 / リファクタリング**: 技術設計（外部から見える挙動）が変わらない場合
- **テストの追加のみ**: 既存仕様に基づくテスト追加（ただしテスト計画の行とテスト参照は更新する）

## チェックリスト

各テンプレートの「記載基準チェックリスト」を通す。加えて次を確かめる。

```
□ REQUIREMENTS の全ユースケースが設計書とテスト計画の両方に ID で載っている（trace-audit で抜け漏れなし）
□ 章名・表の列名がテンプレートのとおり（テンプレートにない番号付きの章を足していない）
□ テーブル・API の形を再定義していない（common の TABLE_DEFINITION / API_SPEC を参照）
□ 文書の末尾に「テンプレート版: X.Y」がある
□ SSOT原則の禁止語が含まれていない（Self-check 通過）
```

### common 階層（テーブル定義 / API 仕様）更新時

```
□ TABLE_DEFINITION.md: 新規/変更テーブルをカード形式で記載（型は論理型・FK は説明欄）
□ API_SPEC.md: 新規/変更エンドポイントを記載（レスポンス実体は TABLE_DEFINITION へリンク）
□ 参照する feature の技術 spec との整合を確認
```
