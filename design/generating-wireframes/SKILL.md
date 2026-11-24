---
name: generating-wireframes
description: |-
  REQUIREMENTS.md のユースケース（振る舞い＋受入基準）から、低忠実度（low-fidelity）の HTML ワイヤーフレームを生成する。技術スタック非依存の素の HTML（CSS は各 HTML に `<style>` で埋め込み・自己完結）で、画面レイアウト・情報設計・主要文言（タイトル / ボタン / 項目ラベル）を合意形成用に可視化する。
when_to_use: |-
  「ワイヤーフレーム」「WF」「wireframe」「画面設計」「画面イメージ」「モックの前段」「UI/UX デザインのHTML化」「REQUIREMENTS の画面を作る」に関する作業のとき。
allowed-tools: Read, Write, Edit, Glob, Grep
---

# ワイヤーフレーム生成

REQUIREMENTS.md の **ユースケース**（振る舞い＋受入基準）と**画面要素**をもとに、低忠実度の HTML ワイヤーフレーム（WF）を生成する。WF は REQUIREMENTS.md の「2.4 UI/UX・画面」セクションの実体となり、ステークホルダーが画面構成・遷移・主要文言を合意するために使う。

## 何を作るか / 作らないか

| 作る | 作らない |
| ---- | -------- |
| 画面レイアウト（ヘッダー / サイドバー / 検索 / 一覧 / フォーム / カード / カンバン等） | 確定したビジュアルデザイン（ブランドカラー・余白の最終値・タイポグラフィ） |
| 主要文言（画面タイトル・ボタン文言・項目ラベル・タブ名）を**実値で** | ピクセルパーフェクトなモック |
| 状態の出し分け（通常 / 空 / エラー） | 実データ・実 API 連携・JS による挙動 |
| レスポンシブの大枠（モバイル 1 列 → デスクトップ展開） | 細かいアニメーション・トランジション |

⚠️ **低忠実度だが、文言は実値**。`[ボタン]` のようなダミーで終わらせず、合意済みの「検索」「新規登録」「保存」「キャンセル」などの実文言を入れる。色や装飾は持たせない（実装の自由度を縛らないため、かつ公開資産としてブランド中立に保つため）。

## 配置ルール

```
docs/<app>/<feature_path>/wireframes/
├── index.html           … 画面一覧（目次）
├── <screen-1>.html      … 画面ごとの WF（状態違いは <screen>-empty.html 等）
└── <screen-2>.html
```

- 各 HTML は **自己完結**（self-contained）。デザインシステムの CSS は `<head>` 内に `<style>` で**直接埋め込む**。**CSS 単体ファイル（wireframe.css 等）は作らない**。
- `<app>` / `<feature_path>` は REQUIREMENTS.md と同じ階層に合わせる（`.stdd.config.yml` の `docs.layout.wireframes` があればそれに従う。なければ上記の固定規約）。
- REQUIREMENTS.md からは **相対リンク**で `./wireframes/index.html` を指す。

## 生成手順

### 1. 入力を読む

- 対象の `REQUIREMENTS.md`（ユースケース：振る舞い＋受入基準・表示要素）
- `TECH_DESIGN.md` の画面項目定義セクション（画面 feature にあれば — フォーム項目名・選択肢・必須/任意・画面状態〔通常 / 空 / ローディング / エラー〕の出所はこれ）
- 既存の類似画面の WF（`docs/**/wireframes/` を Glob して文言・構造を踏襲）

### 2. 画面を洗い出す

ユースケースの振る舞い（手順）の各ステップが「どの画面で起きるか」を割り出し、画面のリストを作る。1 ユースケース = 複数画面のことも、複数ユースケースが 1 画面を共有することもある。各画面について必要な**状態**（通常 / 空 / エラー / ローディング）を決める。詳細は [guides/from-requirements.md](guides/from-requirements.md)。

### 3. 雛形をコピーして組む

1. `templates/screen.html` を各画面ぶんコピーする。このひな型は `<head>` 内に**デザインシステムの `<style>` を埋め込み済み**（＝デザインシステム本体）。`<body>` をコンポーネント（下表 `wf-*`）で組む。
2. `templates/index.html` をコピーし、全画面へのリンクと 1 行説明を並べる。
3. 各画面の `<title>` と `.wf-screen-label` に「画面名 / 状態名」を実値で入れる。
4. `<style>` ブロックは各画面で同一内容を保つ（デザインシステムを変えたい場合は全画面の `<style>` を揃えて更新する）。CSS 単体ファイルは作らない。

### 4. REQUIREMENTS.md の「2.4 UI/UX・画面」を更新

ASCII アートは置かない。代わりに以下を書く（テンプレートは `documenting-requirements` の REQUIREMENTS テンプレートに準拠）:

- `./wireframes/index.html` へのリンク（ワイヤーフレーム一覧）
- 画面ごとに: 画面名・主な操作（ボタン文言）・表示要素の要点
- 表示要素テーブル / 空・エラー状態の説明

### 5. セルフチェック

- [ ] すべての P0 / P1 ユースケースに対応する画面が WF 化されている
- [ ] 各画面に**実文言**のタイトル・ボタン・ラベルが入っている（ダミー `[...]` が残っていない）
- [ ] 空状態・主要エラー状態の WF がある
- [ ] モバイル幅でも破綻しない（`wf-page--mobile` でプレビュー確認、または論理的に 1 列化される構造）
- [ ] `index.html` から全画面に到達できる
- [ ] 各 HTML が自己完結している（`<style>` 埋め込み・外部 CSS ファイルを参照していない）
- [ ] ブランドカラー・固有の装飾を持ち込んでいない（グレースケール維持）

## コンポーネント早見表（埋め込み `<style>` のクラス）

| 用途 | クラス |
| ---- | ------ |
| ページ枠 | `wf-page`（モバイル枠は `wf-page--mobile`） |
| グローバルヘッダー | `wf-header` / `wf-header__logo` / `wf-header__nav` / `wf-header__spacer` |
| 本体レイアウト | `wf-body` / `wf-sidebar` / `wf-sidebar__item(--active)` / `wf-main` |
| 見出し | `wf-breadcrumb` / `wf-title` / `wf-subtitle` / `wf-tabs` / `wf-tabs__item(--active)` |
| ツールバー | `wf-toolbar` / `wf-toolbar__spacer` / `wf-count` |
| 検索・フィルタ | `wf-search` / `wf-search__head` / `wf-search__body` / `wf-search__actions` |
| フォーム | `wf-form(--2col)` / `wf-field(--full)` / `wf-label(--required)` / `wf-input` / `wf-select` / `wf-textarea` / `wf-help` / `wf-error` |
| ボタン | `wf-button` / `wf-button--primary` / `wf-button--ghost` / `wf-button--sm` |
| テーブル | `wf-table-wrap` / `wf-table` / `wf-td--muted` |
| カード / グリッド | `wf-grid(--2/--3)` / `wf-card` / `wf-card__title` / `wf-card__meta` |
| カンバン | `wf-kanban(--3)` / `wf-kanban__col` / `wf-kanban__head` |
| タグ / 画像 / アバター | `wf-tag` / `wf-img` / `wf-avatar` |
| ページネーション | `wf-pagination` / `wf-pagination__item(--active)` |
| 空・エラー | `wf-empty` |
| モーダル | `wf-modal` / `wf-modal__head` / `wf-modal__body` / `wf-modal__foot` |
| 注記・ユーティリティ | `wf-note` / `wf-row` / `wf-stack` / `wf-muted` / `wf-mt` |

実例は [examples/](examples/) を参照（toC 一覧 / フォーム、toB 管理画面 一覧 / フォーム）。

## STDD フローでの位置づけ

```
REQUIREMENTS.md（ユースケース）
  └─ ワイヤーフレーム生成（本スキル）── 「2.4 UI/UX・画面」の実体に
       └─ TECH_DESIGN.md → テスト → 実装
```

- WF は **Spec の一部**。実装前のステークホルダー合意に使う（Figma 等の実画面キャプチャは実装**後**の別工程で、混同しない）。
- 仕様変更時は SSOT 原則に従い、REQUIREMENTS.md → WF の順で更新する（WF だけ先に直さない）。

## When NOT to Use This Skill

- UI を持たない機能（バッチ・API のみ・内部ロジック）
- 既存画面の文言・ロジックのみの軽微な変更（画面構成が変わらない）
- 実装後の実画面キャプチャ（それは別工程）

## 参照ファイル

- [templates/screen.html](templates/screen.html) — 画面ひな型（`<head>` に汎用デザインシステムの `<style>` を埋め込み済み＝デザインシステム本体）
- [templates/index.html](templates/index.html) — 画面一覧ひな型
- [guides/from-requirements.md](guides/from-requirements.md) — ユースケース → 画面の起こし方
- [examples/](examples/) — toC / toB のサンプル WF
- 関連: [documenting-requirements](../documenting-requirements/SKILL.md)（REQUIREMENTS テンプレート）
