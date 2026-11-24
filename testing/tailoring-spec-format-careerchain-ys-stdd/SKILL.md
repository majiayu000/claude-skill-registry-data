---
name: tailoring-spec-format
description: |-
  このプロジェクト固有の spec フォーマット / ラインナップを策定し、テンプレートや設定へ反映する。STDD 導入（既存）・立ち上げ（新規）の初期フォーマット策定と、運用中のブラッシュアップの両方を担う。common spec と最初の feature spec を素材に、必須/任意の spec ファイル構成・固有セクション・docs.layout・Priority 基準・テスト層責務・命名を決め、決定を導入PLAN / 立ち上げPLANに記録してテンプレ/設定へ反映する。個別機能の spec 作成は documenting-requirements（要件）／ documenting-tech-specs（技術設計）を使う。
when_to_use: |-
  「specフォーマット策定」「テンプレ特化」「テーラリング」「spec構成を決める」「specフォーマットのブラッシュアップ」「STDDをプロジェクトに合わせる」に関する作業のとき。
allowed-tools: Read, Write, Edit, Glob, Grep, Bash
---

# spec フォーマットのテーラリング

STDD のテンプレートを**このプロジェクト固有**に仕立て直す（テーラリング）。
STDD 導入（既存プロジェクト, step 3-4）・立ち上げ（新規プロジェクト, step 4）の **初期フォーマット策定** と、運用中の **ブラッシュアップ**（step 7）を担う。

> 導入/立ち上げフロー全体は [`guide-for-existing-project.md`](../../../packages/core/docs/guide-for-existing-project.md) / [`guide-for-new-project.md`](../../../packages/core/docs/guide-for-new-project.md)、
> 駆動役は [`introducing-stdd`](../introducing-stdd/SKILL.md)（既存）/ [`starting-new-with-stdd`](../starting-new-with-stdd/SKILL.md)（新規）を参照。本スキルは単体でも呼べる。

## 設計方針（重要）

- **フォーマットの決定そのものは人間**（ビジネス・チーム判断）。本スキルはそれを**促し・記録し・反映する**手続きに徹する。
- **agent オーケストレーションはしない**。エージェントがメインセッションで決定ポイントを 1 つずつ提示し、人間に決めてもらう。
- 決定は **導入PLAN / 立ち上げPLAN の「フォーマット決定ログ」** に集約（SSOT）。spec 本体に経緯・履歴を書かない。

## 前提（素材）

- **初期**: `docs/common/`（common spec）と最初の feature spec 1 つが既にある（既存導入なら reverse、新規立ち上げなら順行で作成）。
- **ブラッシュアップ**: 既に複数の feature spec が運用されている。

---

## 手順

### 1. 素材レビュー

現状を把握する。

```
□ docs/common/REQUIREMENTS.md / ARCHITECTURE.md（common 階層の構成）
□ 代表 feature spec（REQUIREMENTS.md / TECH_DESIGN.md / TEST_PLAN.md）の実物
□ 現在の .stdd.config.yml（docs.layout / apps / commands）
□ 利用中のテンプレ（`.claude/skills/documenting-requirements/templates/`・`.claude/skills/documenting-tech-specs/templates/` または プロジェクト側コピー）
□ (step 7 のみ) 運用中の全 feature spec のばらつき・過不足
```

### 2. 決定ポイントを 1 つずつ提示（★人間が決める）

各項目について **現状 → 選択肢 → 推奨** を提示し、ユーザーに決めてもらう。一度に押し付けない。

| 決定ポイント | 論点 | 反映先 |
| ------------ | ---- | ------ |
| **spec ファイル構成** | feature の技術 spec のラインナップ（`single`: TECH_DESIGN / TEST_PLAN ／ `layered`: API_DESIGN・SCREEN_DESIGN と層別のテスト設計・TEST_DESIGN。新規導入の既定は `layered`）・任意（wireframes）と common（技術 spec: TABLE_DEFINITION / API_SPEC / DESIGN）をどう組むか | `.stdd.config.yml` の `docs.lineup`・プロジェクトのテンプレ |
| **common 固有セクション** | common ARCHITECTURE に足す横断トピック（認証・認可 / RLS・権限 / 通知 / 監査ログ 等） | `docs/common/ARCHITECTURE.md` |
| **docs.layout パス規約** | 単一/複数アプリ、`feature_path` の切り方、common の置き場 | `.stdd.config.yml` の `docs.layout` |
| **Priority 基準** | このプロジェクトでの P0/P1/P2 の具体定義（何を Critical とするか） | テンプレ注記 + 決定ログ |
| **テスト層の責務分担** | E2E/Integration/Unit の線引き（既存テスト資産に合わせる） | TEST_PLAN テンプレのテスト戦略節 |
| **命名・用語** | プロジェクト固有語彙（アクター名・ドメイン用語）、テンプレのプレースホルダ実値化 | テンプレ・common spec |

### 3. 決定を記録

`docs/common/plans/` の PLAN（既存導入: `stdd-introduction.md` / 新規立ち上げ: `stdd-bootstrap.md`）の **「フォーマット決定ログ」** に各決定を追記する。
PLAN が無い文脈（ブラッシュアップ単体実行など）では、プロジェクトの spec 規約ドキュメント（例: `docs/common/SPEC_CONVENTIONS.md`）に記録してよい。

### 4. テンプレ・設定へ反映（機械的）

決定に従って、**プロジェクト側**の成果物を更新する（STDD core の `.claude/skills/*/templates/` 本体は壊さない）。

```
□ .stdd.config.yml の docs.lineup / docs.layout を更新（必要なら common_* を追加/変更）。章名・列名を変えるなら docs.structure、レスポンスコードの機能略号・共通コードを変えるなら response_codes に書く
□ docs/common/ARCHITECTURE.md に固有セクションを追加
□ プロジェクト側テンプレ（コピーを持つ場合）の不要セクション削除 / 固有セクション追加 / プレースホルダ実値化
□ プロジェクト側テンプレを持たない場合は、決定ログに「次に作る feature spec へ適用する方針」として明記
```

### 5. （step 7 のみ）既存 spec への影響を洗い出す

フォーマットを変えた場合、運用中の feature spec に差分が出る。影響範囲を一覧化してユーザーに提示し、修正は別タスク（必要なら PLAN を切る）として扱う。一括自動修正はしない。

---

## 守ること

- **決定は人間**。skill は選択肢提示・記録・反映に徹する。
- 一度に全項目を片付けず、**決定ポイントごとに合意**を取る。
- **STDD core テンプレ（`.claude/skills/*/templates/`）を直接編集しない**。反映先はプロジェクト側。
- 決定は決定ログに集約し、spec 本体に経緯・「変更前/後」を書かない（SSOT）。

---

## When NOT to Use This Skill

- **個別機能の spec を書く**: `documenting-requirements`（要件）／ `documenting-tech-specs`（技術設計）を使う
- **既存実装から spec を起こす**: `reverse-engineering-feature-spec` / `reverse-engineering-common-spec` を使う
- **導入フロー全体を進める**: `introducing-stdd`（本スキルを step 3-4 / 7 で呼ぶ）

---

## 参照ファイル

- **導入ガイド（なぜ/判断基準）**: [guide-for-existing-project.md](../../../packages/core/docs/guide-for-existing-project.md) §step 3-4
- **導入ドライバー**: [introducing-stdd skill](../introducing-stdd/SKILL.md)
- **spec テンプレ**: `../documenting-requirements/templates/`（REQUIREMENTS: feature / common） / `../documenting-tech-specs/templates/`（TECH_DESIGN・TEST_PLAN、API_DESIGN・SCREEN_DESIGN と各テスト設計、common 技術階層） / `../documenting-plans/templates/`（PLAN）
- **spec 作成スキル**: [documenting-requirements skill](../documenting-requirements/SKILL.md)（要件）／ [documenting-tech-specs skill](../documenting-tech-specs/SKILL.md)（技術設計）
- **設定スキーマ**: `packages/core/schema/.stdd.config.schema.json`
