---
name: documenting-requirements
description: |-
  REQUIREMENTS.md（業務要件・機能要件・非機能要件）を、feature 階層と common 階層の両方について作成・更新するためのテンプレートとガイドラインを提供する。STDD 方法論における「要件（What & Why）」のSSoTを担い、SSOT 原則・要確認マーカーのSSoTもここに置く。技術設計（TECH_DESIGN / ARCHITECTURE 等）は documenting-tech-specs を使う。
when_to_use: |-
  「requirements」「要件定義」「REQUIREMENTS.md」「ユースケース」「受入基準」「業務要件」「機能要件」「非機能要件」「common 要件」に関する作業のとき。技術設計・テーブル定義・API 仕様・テスト戦略は documenting-tech-specs を使う。
allowed-tools: Read, Write, Edit, Glob, Grep
---

# 要件定義書（REQUIREMENTS.md）の作成

STDD（Spec and Test Driven Development）方法論に従って、REQUIREMENTS.md（feature / common 両階層）を作成・更新します。
要件（What & Why）を確定したら、技術設計は [documenting-tech-specs Skill](../documenting-tech-specs/SKILL.md) に引き継ぎます。

## Quick Start

書き始める前に [guides/writing-procedure.md](guides/writing-procedure.md)（読むもの・追記か新規か・書かないもの）を確かめる。

### 新機能の要件定義書を作成する場合

1. **REQUIREMENTS.md を作成**

   ```
   docs/<app>/<path>/REQUIREMENTS.md
   ```

   - **業務要件 → 機能要件 → 非機能要件** の3層で記述（機能要件のコア・拡張の章立て、ユースケースの ID・振る舞い・受入基準・Priority の書き方は下記「基本原則」）
   - 指標を持つ機能は §2.3 指標定義表を埋める（算出ロジック・データソース・代理注記）
   - [テンプレート（feature）](templates/requirements.md) を参照

2. **ワイヤーフレーム（WF）を生成**（UI を持つ機能の場合）

   ```
   docs/<app>/<path>/wireframes/
   ```

   - REQUIREMENTS.md のユースケースから HTML ワイヤーフレームを生成（低忠実度・主要文言は実値）
   - [generating-wireframes Skill](../generating-wireframes/SKILL.md) を参照
   - 生成後、REQUIREMENTS.md「2.4 UI/UX・画面」から `./wireframes/index.html` にリンクする

3. **技術設計に進む** → [documenting-tech-specs Skill](../documenting-tech-specs/SKILL.md)（`docs.lineup` の構成の技術 spec）

### 既存機能の要件定義書を更新する場合

1. 対応する REQUIREMENTS.md を確認
2. 変更内容に応じて更新（ユースケース・受入基準・非機能要件）
3. 技術設計・テスト戦略に波及する場合は documenting-tech-specs へ引き継ぐ

## Spec の 2 階層構造（common / feature）

要件は feature 階層（機能単位）と common 階層（プロジェクト全体）の2層で扱う。

| 階層      | REQUIREMENTS の位置づけ | 配置例 |
| ----------- | --- | --- |
| **common**  | サービス全体の業務要件・横断業務ルール・非機能要件・用語のSSoT | `docs/common/REQUIREMENTS.md` |
| **feature** | 機能単位の業務要件・機能要件・機能固有の非機能要件 | `docs/<app>/<feature>/REQUIREMENTS.md` |

- feature の REQUIREMENTS は common 階層（サービス目的・アクター・横断業務ルール・非機能要件）を**前提とし、参照する**。common と矛盾しないこと。
- 非機能要件・横断業務ルール・用語は common に集約し、feature は「common 準拠」で参照する。
- common テンプレート: [`requirements-common.md`](templates/requirements-common.md)。既存実装からの common 要件作成は `reverse-engineering-common-spec` スキルを参照。

## ドキュメント配置ルール

配置先は `.stdd.config.yml` の `docs.layout.requirements` テンプレートに、対象アプリの `app`（`apps[].id`）と `feature_path` を適用して決定する。

**例**: 実装 `<app.path>/app/login/page.tsx` → `docs/<app.id>/login/REQUIREMENTS.md`、コンポーネント `<app.path>/components/<name>.tsx` → `docs/<app.id>/components/<name>/REQUIREMENTS.md`

## 絶対ルール: SSOT原則（最優先）

⚠️ **Specドキュメントは「現在の最新仕様」だけを記述するSingle Source of Truth（SSOT）である**。履歴・経緯・対応中のissue・「今回の変更」は一切書かないこと。読者は「いま何が正しいか」だけを知りたい。履歴はgit log・PR description・issueに任せる。

> このセクションは STDD 全体の **SSOT原則のSSoT**。REQUIREMENTS / TECH_DESIGN / TEST_PLAN / common 各種、すべての spec ドキュメントに適用される。documenting-tech-specs・各 reverse-engineering スキルはここを参照する。

### 禁止事項

以下は **すべての spec ドキュメント（REQUIREMENTS / TECH_DESIGN / TEST_PLAN / common 各種）で禁止**:

1. **issueへの言及**: `issue #123 で対応`, `#456 にて追加`, `本issueでは`, `Closes #...` 等
2. **経緯・履歴の記載**: `変更前` / `変更後` / `更新前` / `更新後` / `変更理由` / `削除理由` / `旧仕様` / `〜だったが〜に変更` 等
3. **過程に関する記載**: `今回追加`, `今回変更`, `新たに`, `既存`, `実装済み`, `新規追加`, `今回のスコープ`, `本対応で` 等
4. **作成プロセスの注記**: `このドキュメントはリバースエンジニアリングで作成`, `〜を参考に作成`, `下記をベースに作成` 等
5. **比較形式の記述**: `Before / After`, `旧 / 新`, `変更前後の差分` の形式
6. **転記**: ほかの文書の件数・一覧・しきい値の書き写し、作成状況の断定（`N 画面中 M 画面は未作成`）。正本を参照する

### 違反例と修正例

違反例と修正例（履歴の記述・issue への言及・テストケースの除去など）は [STDD違反例と対策「具体例」](guides/stdd-violations.md) を参照。

### Self-check（コミット前に必ず実行）

書き終えたら以下の禁止語を grep し、ヒットしたら必ず除去すること:

```
# 履歴・経緯・過程の記述
今回 | 既存 | 新規追加 | 実装済み | 変更前 | 変更後 | 更新前 | 更新後
変更理由 | 削除理由 | 旧仕様 | issue # | Closes # | リバースエンジニアリング
本対応 | 本issue | 今回のスコープ | 今回の変更

# テスト/ユースケース再構成の履歴を暗示するフレーミング
に統合 | を統合 | に集約 | を集約 | にまとめ | をまとめ | にマージ | をマージ
別テストに分割 | テストを分けた | 元々は | 当初は | 以前は
```

転記は `bash <skill_dir>/scripts/state-claims.sh <書いた文書>` で探す。

「ユースケース名」や「アーキテクチャ判断の理由」など現在仕様の説明として正当な「理由」は問題ない。禁止しているのは**変更そのものの理由**（なぜ仕様を変えたか）と、**過去構成からの再編を暗示するフレーミング**。

> 作成前に [STDD違反例と対策](guides/stdd-violations.md)（SSOT原則の詳細）を必ず読む。

---

## 要確認マーカー（不明点は仮説とセットで明示する）

Spec を書く過程で、確信が持てない／ユーザーに確定してもらう必要がある箇所は、**章を省略したり空欄にしたりせず**、その箇所に **要確認マーカー** を置く。テンプレートの章構成は常に維持し、埋められない部分も「仮説＋要確認」で埋めることで spec の**網羅性を担保**する。

> このマーカーは STDD 全体で**唯一の確認用マーカー**であり、ここがそのSSoT。前方設計（新規・`starting-new-with-stdd`）／逆生成（既存・`reverse-engineering-*`）／技術設計（`documenting-tech-specs`）でも同じ構文を使い、各スキルはここを参照する。

### 唯一の構文（可視インライン）

- 標準形（箇条書き・段落の直下）:

  ```markdown
  **⚠️要確認**｜仮説: <現時点で最も妥当と考える答え>／確認: <ユーザーに是非を確かめたいこと>
  ```

- 表・行内の短縮形:

  ```markdown
  | 認証 | Supabase Auth ⚠️要確認(仮説: メール＋OAuth で足りる / 確認: SSO 要件の有無) |
  ```

旧来の `<!-- 未決: ... -->` / `<!-- 要確認: ... -->` / `※要確認` は**使わない**。マーカーは要確認マーカーに一本化する。

### 3 つのルール

1. **必ず仮説とセット**。「要確認」だけを単独で置かない。不明点はまず現時点で最も妥当な**仮説**を立て、その**是非をユーザーに確認させる**形にする（深掘りヒアリングの代わりに、仮説提示で前進する）。
2. **章は省略しない**。テンプレートの構成を維持し、情報が無い箇所も仮説＋要確認マーカーで埋める。空欄・章削除による「見かけ上の完成」を作らない。
3. **可視・一時的**。マーカーはレンダリングで見える一時注記。ユーザーが是非を確定したら、仮説を確定値に書き換えてマーカーを除去する。確定済み spec にマーカーを残さない（SSoT 原則）。

例（良い例・悪い例）は [STDD違反例と対策「要確認マーカーの例」](guides/stdd-violations.md) を参照。

---

## 基本原則: REQUIREMENTS.md（要件定義書）

**目的**: 機能の要件を「業務要件 → 機能要件 → 非機能要件」の3層で定義し、後続（TECH_DESIGN / テスト / コード）の一次インプットにする

**章立ての3層**:

| 層 | 答える問い | 書くもの |
| --- | --- | --- |
| **業務要件** | なぜ作るか（Why） | ビジネス課題・目標・KPI・対象ユーザー・利用シーン |
| **機能要件** | 何が見える/できるか（What） | **コア**: ユースケース（振る舞い〔手順〕＋受入基準〔EARS〕）・業務ルール ／ **拡張（該当機能のみ。無ければ章ごと省略）**: 指標定義・UI/UX・外部IF |
| **非機能要件** | どれだけうまく（How well） | 性能・可用性・セキュリティ・アクセシビリティ（機能固有のみ。共通は common §6 を参照） |

**記法**:

- 各ユースケースは **振る舞い（番号付き手順）＋ 受入基準（EARS）** の2部構成で記述する
- **振る舞い → 番号付き手順**（1. 2. 3. …）。各ステップの主語を明示（「ユーザーは〜」「システムは〜」）し、ユーザー操作とシステム応答の主要フロー（ハッピーパス＋主要分岐）を表す。E2E テストの骨格になる。抽象（ビジネス言語）に保ち、テストデータ・セレクタはテストコード側に置く
- **受入基準・業務ルール → EARS**（常時 / WHEN / WHILE / IF / WHERE）。フローが満たすべき詳細条件・例外・データ制約を網羅。手順と重複させず、エッジケースは IF / WHERE で統合

**記述しない内容**:

- データモデル・集計実装・API・画面項目 → TECH_DESIGN.md（データ構造・API は common の TABLE_DEFINITION / API_SPEC）
- 実装ファイルへの参照・関数名・クラス名、テスト実装の詳細

**ユースケース見出しのフォーマット**: ユースケースの見出しには `UC1.` `J1.` 等のID連番を**付けない**。テンプレート通り `#### [ユースケース名]` の形式で、内容を表す日本語の説明テキストのみを使う。既存 REQUIREMENTS に追記する場合は既存の見出しフォーマットに合わせる。

**トレーサビリティ ID は見出しではなく見出し直下の `**ID**:` 行に置く**（例: `**ID**: UC-<feature>-01 ／ **Priority**: P0`）。見出しは説明テキストのみのまま、ID `UC-<feature>-NN` を名前と分離して安定させ、TECH_DESIGN / TEST_PLAN / テスト / 実装へ貫通させる（→ 方法論「トレーサビリティ」）。ID は連番の**見出し名**ではないため、上記「見出しに連番を付けない」と両立する。

### Priority（優先度）ガイドライン

| Priority | 定義                                                     | テスト戦略                 |
| -------- | -------------------------------------------------------- | -------------------------- |
| **P0**   | Critical Path - ビジネスに直結、高頻度、複数システム統合 | E2E 必須 + Integration     |
| **P1**   | Important - 重要だが Critical Path ではない              | E2E 検討、Integration 必須 |
| **P2**   | Nice to Have - エッジケース、低頻度                      | Integration または Unit    |

## 次のステップ

REQUIREMENTS.md の作成・レビュー（人間レビュー含む）が済んだら、技術設計（[documenting-tech-specs](../documenting-tech-specs/SKILL.md)）→ PLAN（[documenting-plans](../documenting-plans/SKILL.md)）へ進む。

## When NOT to Use This Skill

- **技術設計のみ**: TECH_DESIGN / TEST_PLAN / ARCHITECTURE / TABLE_DEFINITION / API_SPEC → documenting-tech-specs
- **単純なバグ修正 / リファクタリング**: 要件（外部から見える挙動）が変わらない場合
- **ドキュメント修正のみ**: README や AGENTS.md / CLAUDE.md の更新

## チェックリスト

### REQUIREMENTS.md 作成時

```
□ 業務要件・機能要件・非機能要件の3層が揃っている（非機能が「common 準拠」でも明記）
□ 各記述が3層のいずれかに分類されている（フラットな未分類項目が無い）
□ 全ユースケースに Priority＋振る舞い（番号付き手順）＋受入基準（EARS）がある
□ 振る舞い手順は主要フロー（抽象）に保たれ、テストデータ・セレクタが混入していない
□ 受入基準（EARS）が詳細条件・例外・データ制約を網羅している（エッジケースは IF/WHERE）
□ 指標を持つ機能は §2.3 指標定義表が埋まっている（算出/データソース/代理注記）
□ 近似・代理指標は「注記表示=必須」が明記されている
□ UI/UX デザイン（HTML ワイヤーフレームを生成し「2.4 UI/UX・画面」からリンク）→ generating-wireframes Skill
□ 受入基準に曖昧語（適切に/正しく）が無い／How（テーブル名・関数・API）が混入していない
□ ユースケース見出しが `#### [ユースケース名]` 形式（UC1./J1. 等のID連番なし）／トレーサビリティ ID は見出し直下の `**ID**: UC-<feature>-NN` 行に付与
□ スコープ外
□ SSOT原則の禁止語が含まれていない（Self-check 通過）
```
