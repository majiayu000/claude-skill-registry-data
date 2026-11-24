---
name: reverse-engineering-feature-spec
description: |-
  既存の機能/ページの実装から feature 階層の Spec ドキュメント（REQUIREMENTS.md + TECH_DESIGN.md + TEST_PLAN.md）とテスト（E2E / Unit / Integration）をリバースエンジニアリングで作成するためのガイドライン。新規機能の仕様策定ではなく、既に動いている機能を正確にドキュメント化・テスト化する場合に使う。プロジェクト全体（common 階層）のリバースには reverse-engineering-common-spec を使用する。
when_to_use: |-
  「リバースエンジニアリング」「既存コードからspec」「既存機能のドキュメント化」「機能のドキュメント化」「実装からテスト作成」「specカバー率向上」に関する作業のとき。
allowed-tools: Read, Write, Edit, Glob, Grep, Bash
---

# feature spec のリバースエンジニアリング

既に動いている **機能 / ページ単位**の実装コードを精読し、その挙動を正確に反映した feature 階層の Spec ドキュメント（REQUIREMENTS.md + TECH_DESIGN.md + TEST_PLAN.md）とテスト（E2E / Unit / Integration）を作成する。

> **前提（推奨）**: プロジェクト全体の **common 階層**（`docs/common/REQUIREMENTS.md` + `ARCHITECTURE.md` + `TABLE_DEFINITION.md` + `API_SPEC.md`）が未作成なら、先に `reverse-engineering-common-spec` スキルで作成しておくと、レイヤ規約・共有ドメインモデル・テーブル定義・API 契約を踏まえられて精度が上がる。既にある場合は本スキルから始める。データモデル・API は common 階層が SSoT のため、feature 側では common の `TABLE_DEFINITION.md` / `API_SPEC.md` を参照する。

## 最重要原則

### Specに記載する文言は正確に実装を反映すること

リバースエンジニアリングでは、**実装が真実（Source of Truth）**である。Specは実装の挙動を忠実にドキュメント化したものであり、理想論や推測で書いてはならない。

一般常識（例: 電話番号は10〜11桁）や似た文言（例: 実際は「前へ」なのに「戻る」）で書かず、必ず実装を確認してから書く。

**具体的な確認項目**（「確認元」は**ソースの種別**。括弧内は代表スタックでの一例なので、採用スタックに読み替えること）:

| 項目 | 確認元（ソースの種別） | よくある間違い |
|------|--------|--------------|
| ボタンラベル | ビュー/テンプレート内のテキスト（例: JSX） | 「送信」と書いたが実際は「保存」 |
| バリデーションルール | バリデーション定義（例: Zod スキーマ `schema.ts`） | 桁数・形式を想像で書く |
| エラーメッセージ | バリデーション定義のメッセージ（例: Zod の message） | 一般的なメッセージを推測で書く |
| フォーム項目名 | ラベル要素（例: `<label>` / `getByLabel` / `aria-label`） | 項目名を想像で書く |
| ページ遷移先 | ルーティング/リダイレクト（例: `router.push()` / `redirect()`） | パスを想像で書く |
| API呼び出し | ハンドラ/通信層（例: Server Actions / fetch） | エンドポイントを想像で書く |
| DB操作 | データアクセス層のメソッド（例: repository 層） | テーブル名・カラム名を想像で書く |
| 型定義 | ドメインモデルの型（例: `domain/models` 配下） | フィールド名を想像で書く |

カテゴリ別の確認ポイント・よくある間違い・検証方法（grep での文言一致確認など）は [正確性ガイド](guides/accuracy.md) を参照。

---

## Quick Start

### 前提条件

- 対象機能が既に動いている実装コードがある
- 対応するSpecドキュメント（REQUIREMENTS.md / TECH_DESIGN.md / TEST_PLAN.md）が存在しない、または不十分

### 作業フロー

各フェーズの番号は下の Phase 見出しに対応する。

1. 実装コードリーディング（精読）
2. REQUIREMENTS.md 作成（ユーザー視点の挙動を記述）
3. Playwright MCP で UI キャプチャ → Figma ファイル作成
4. TECH_DESIGN.md 作成（ロジック設計中心。データモデル / API は common 参照）／4.5 TEST_PLAN.md 作成（テスト戦略）
5. テスト作成（E2E、必要に応じて Unit / Integration）
6. `/verifying-consistency` で整合性チェックし、不整合は Spec を実装に合わせて直す

---

## Phase 1: 実装コードリーディング

ページ/画面（エントリーポイント）→ クライアント/UI コンポーネント → バリデーション定義 → ハンドラ/ビジネスロジック層 → ドメイン層 → DB スキーマ の順に精読し、機能の全体像を把握する。UI テキスト・バリデーションの具体値・エラーメッセージ・テーブル名とカラム名は**正確に**読み取る。

各層で確かめること（代表スタックでのファイルの位置の例を含む）と、読みながら控える項目（ルーティング・画面遷移・フォーム項目・ボタンラベル・条件分岐・エラーメッセージ・DB・外部連携）は [コードリーディングガイド](guides/code-reading.md) を読みながら進める。

---

## Phase 2: REQUIREMENTS.md作成

`documenting-requirements` skillのテンプレートに従って作成する。

### リバースエンジニアリング固有のルール

**1. ユースケース（振る舞い＋受入基準）は実装の挙動から抽出する**

実装コードの条件分岐・状態遷移を元に、ユーザーが辿るパスを網羅的に洗い出す。主要フローは振る舞い（番号付き手順・主語明示）に、例外・境界・分岐は受入基準（EARS）に落とす。

**各ユースケースにはトレーサビリティ ID `UC-<feature>-NN` を付与する**（見出し直下の `**ID**:` 行。TECH_DESIGN §1.1 / TEST_PLAN の対象ID・作成テストのタイトルタグ `[UC-<feature>-NN]` まで貫通させる）。リバース対象の既存テストにも同じ ID タグを付け、`bash .claude/hooks/trace-audit.sh` で要件⇄設計⇄テスト⇄実装の抜け漏れが無いことを確認する。

```
# コードの条件分岐 → ユースケースの振る舞い / 受入基準
if (form.isValid) → 正常系の振る舞い（手順）
if (error.type === 'validation') → 受入基準（IF：バリデーションエラー時）
if (error.type === 'network') → 受入基準（IF：ネットワークエラー時）
```

**2. UIテキストは実装から正確に転記する**

ボタンラベル等は略さず実装のとおりに書く（例: 実装が「保存して次へ」なら「次へ」と書かない）。→ [正確性ガイド §1](guides/accuracy.md)

**3. Priority判定の基準**

リバースエンジニアリングの場合、以下の基準でPriorityを判断する:

| Priority | 判断基準 |
|----------|---------|
| P0 | 主要な正常系フロー、ビジネスの中核機能 |
| P1 | 重要なエラーハンドリング、バリデーション |
| P2 | エッジケース、低頻度の操作 |

**4. 「備考」セクションにリバースエンジニアリングの注記を追加**

```markdown
## 5. 備考

このドキュメントは既存実装からリバースエンジニアリングで作成されました。

**確認が必要な項目**:
- [ ] ビジネス目標がビジネス要件と合致しているか
- [ ] Priority判断がビジネス優先度と合っているか
```

---

## Phase 3: UIキャプチャ → Figmaファイル作成

REQUIREMENTS.md作成後、Playwright MCPを使って実装済みUIのスクリーンショットを取得し、Figmaデザインファイルとして整理する。

手順は [Figmaキャプチャガイド](guides/figma-capture.md) に従う: キャプチャ計画（キャプチャすべき画面と状態の一覧）→ テストユーザーでログインして各画面を操作・取得 → ログアウト → Figma にフレームとして整理 → REQUIREMENTS.md の「UI/UXデザイン」に node-id 付きリンクを記載 → スクリーンショットを削除（git にはコミットしない）。洗い出すべき画面状態（初期・データあり・フォーム・モーダル・操作結果・レスポンシブ）と記載フォーマットもガイドにある。

---

## Phase 4: TECH_DESIGN.md作成

`documenting-tech-specs` skillのテンプレートに従って作成する。`docs.lineup: layered` では、Phase 4 で API_DESIGN.md / SCREEN_DESIGN.md、Phase 4.5 で層別のテスト設計と TEST_DESIGN.md を作る（以下の TECH_DESIGN / TEST_PLAN は読み替える）。章構成は **1.概要 / 2.主要な設計判断(任意) / 3.画面項目定義(画面 feature のみ必須) / 4.ロジック設計(コア) / 5.エラーハンドリング戦略 / 6.非機能要件(任意)**。

> TECH_DESIGN のコアはロジック設計。データモデル / API は common 階層が SSoT（規則 4）。テスト戦略は別ファイル `TEST_PLAN.md`（Phase 4.5）。

### リバースエンジニアリング固有のルール

**1. 型定義は実装から正確にコピーする**

ドメインモデルの型（例: domain/models 配下の Entity 型）やスキーマの型をそのまま記載し、転記元のファイルを添える。推測で型を書かない（フィールドの分割・nullable の見落としに注意）。→ [正確性ガイド §6](guides/accuracy.md)

**2. バリデーションルールはバリデーション定義（例: Zod スキーマ）から正確に転記する**

桁数・上限・形式パターンの具体値と、エラーメッセージの文言をそのまま書く。→ [正確性ガイド §2](guides/accuracy.md)

**3. ロジック設計は実装のフローを正確に反映する**

入力 → バリデーション → ビジネスロジック → 永続化 → 出力 の流れを、実装のハンドラ/ビジネスロジック層（例: Server Actions / service 層）から正確に書き起こす。

**4. データモデル / API は common を参照する**

テーブル定義・ER 図・API 設計を TECH_DESIGN に書かない（common と二重管理になる）。common の `TABLE_DEFINITION.md` / `API_SPEC.md` を参照し、生成された DB 型定義（例: Supabase の `supabase/generated/database.types.ts`）と一致させる。

---

## Phase 4.5: TEST_PLAN.md作成

テスト戦略は feature 単位の `TEST_PLAN.md` に記述する（TECH_DESIGN には書かない）。`documenting-tech-specs` skillのテンプレートに従う。

**テスト総数は作成後に正確にカウントする**

TEST_PLAN.mdにはテスト総数を記載するが、テストを実際に書いた後にitブロック数を正確にカウントして更新する。

```
# 例: Jest でのカウント方法（テストフレームワークに合わせて読み替える）
grep -c "it(" path/to/test.test.tsx

# 例: Playwright でのカウント方法
grep -c "test(" e2e/tests/user-app/feature.spec.ts
```

---

## Phase 5: テスト作成

### E2Eテスト

`e2e-testing` skillに従い、TEST_PLAN.mdのテスト戦略に基づいて作成する。

**リバースエンジニアリング固有のポイント**:

1. **実際の画面を操作して動作確認してからテストを書く**
   - テストデータ（seedデータ）がどのユーザー・どの状態で入っているか確認
   - 実際のUI操作で画面遷移・表示を確認

2. **Locatorは実装のビュー/テンプレート（例: JSX）から正確に取得する**（例: 実装のボタンテキストが「保存して次へ」なら `getByRole('button', { name: '保存して次へ' })`）

3. **テストデータはseedファイルから確認する**
   ```
   # 例: Supabase の seed での一例
   supabase/seeds/*.sql
   ```

### Unit / Integrationテスト

TEST_PLAN.mdのテスト戦略で定めたテストレベルに従って作成する。

---

## Phase 6: 整合性チェック

### `/verifying-consistency` の実行

すべてのドキュメント・テスト作成後、`/verifying-consistency` コマンドで整合性を確認する。

### 不整合発見時の修正方針

リバースエンジニアリングの場合、**Specを実装に合わせる**のが原則。

```
❌ 実装をSpecに合わせて変更する（リバースエンジニアリングでは原則禁止）
✅ Specを実装の実際の挙動に合わせて修正する
```

**例外**: 実装に明らかなバグがある場合は、バグとして記録し別途修正する。

---

## Spec粒度の基本方針

| 原則 | ルール | 例 |
|------|--------|------|
| **A: 1フロー = 1 Spec** | 開始〜完了まで一連の操作は1 Spec | パスワードリセット、新規登録 |
| **B: 関連画面はまとめる** | 同一データの一覧+詳細等は1 Spec | 通知一覧+詳細 |
| **C: 複雑時はサブ分割** | ユースケース 7つ以上 or 実装1000行超で分割 | ダッシュボード（タブ別） |
| **D: 機能追加は独立Spec可** | 既存画面への追加機能は独立Specとして配置可 | 評価ボタン追加 |

**⚠️ 作業開始前の確認**: 上記方針を踏まえたうえで、必ず開発者にSpec粒度（どの画面・機能を1 Specにまとめるか）とスコープ（どこまでを対象とするか）を確認してから作業を開始すること。

---

## チェックリスト

各フェーズ（コードリーディング・REQUIREMENTS.md・UIキャプチャ・TECH_DESIGN.md・TEST_PLAN.md・テスト・最終確認）を終えるたびに、[フェーズ別チェックリスト](guides/checklists.md) の該当する節で確かめる。

---

## When NOT to Use This Skill

以下の場合はこのスキルを使用しない:

- **プロジェクト全体 / common 階層のリバース**（STDD 導入時の `docs/common/` 作成）: `reverse-engineering-common-spec` skillを使用
- **新規機能の仕様策定**: `documenting-requirements`（要件）／ `documenting-tech-specs`（技術設計）skillを使用
- **実装タスクの計画**: `documenting-plans` skillを使用
- **E2Eテストのみの作成**（Specドキュメントが既に存在する場合）: `e2e-testing` skillを使用
- **バグ修正**: リバースエンジニアリングではなく直接修正

---

## 参照ファイル

本文中で挙げたもの（common spec のリバース・要件と技術設計の skill・本 skill の各ガイド）のほかに:

- **E2Eテストガイド**: [e2e-testing skill](../../../plugins/playwright/skills/e2e-testing/SKILL.md)（`playwright` プラグイン）
- **PLANドキュメント**: [documenting-plans skill](../documenting-plans/SKILL.md)
- **STDD違反例**: [stdd-violations guide](../documenting-requirements/guides/stdd-violations.md)
- **DB型定義**: 生成された DB 型定義（例: Supabase の `supabase/generated/database.types.ts`）
