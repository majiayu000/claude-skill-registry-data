---
name: introducing-stdd
description: |-
  既存（稼働中）プロジェクトへの STDD 導入を、エージェントのセッションで段階的に駆動する。導入ガイドに従い、共通spec生成→機能インベントリ→代表機能リバース→フォーマット策定→機能ループ→順行運用への移行までを、既存スキル（reverse-engineering-common-spec / reverse-engineering-feature-spec / auto-implement / verifying-consistency）を順に呼びながら進める。進捗は導入PLANで保持し、セッションを跨いで再開できる。単一機能のリバースのみなら reverse-engineering-feature-spec を直接使う。
when_to_use: |-
  既存（稼働中）プロジェクトへの STDD 導入を進める／再開するとき。「既存プロジェクトにstddを入れる」「導入の続き」「導入ブートストラップ」など、既存フローと確定している場合。新規/既存が未確定の最初の入口は setup-stdd（ルーター）が判定して本スキルへ委譲する。
allowed-tools: Read, Write, Edit, Glob, Grep, Bash
---

# STDD 導入ドライバー（既存プロジェクト）

既存プロジェクトへの STDD 導入を、セッションで 1 ステップずつ進めるための**薄い駆動役**。
自前の実装ロジックは持たず、各ステップで**既存スキルを順に呼び**、人間判断ポイントで停止し、進捗を**導入PLAN**に記録する。

> 「なぜ」「各ステップで何を判断するか」は [`guide-for-existing-project.md`](../../../packages/core/docs/guide-for-existing-project.md) を参照。
> 本スキルはその operational な実行役。

## 設計方針（重要）

- **agent オーケストレーションはしない**。エージェントがメインセッションで手順を進める軽量ドライバー。
- 導入は一度きり・判断主体のため、**人間を常にループに入れる**（フォーマット策定・優先順・粒度は必ず確認）。
- 状態は導入PLAN（`docs/common/plans/stdd-introduction.md`）にのみ持つ。本スキルはステートレス。

---

## 起動時の動作

### 1. 導入PLAN の有無を確認

```
docs/common/plans/stdd-introduction.md
```

- **無い場合 → 初回**: 下記「初回フロー」を実行し、導入PLAN を作成する。
- **ある場合 → 再開**: 導入PLAN を読み、最初の未チェック項目（`- [ ]`）を「次にやること」として提示し、該当ステップを実行する。

### 2. 設定確認

`.stdd.config.yml` を読み、`apps[]` / `docs.layout`（`common_requirements` / `common_architecture` 含む）を把握する。無ければ **step 0（対話的セットアップ）** を実行する（下記「step 0」詳細）。

---

## ステップ実行表

各ステップは「呼ぶスキル」と「停止して人間に確認すること」を持つ。

| step | 実行内容 | 呼ぶスキル | ★停止して確認 |
| ---- | -------- | ---------- | ------------- |
| 0 | `.stdd.config.yml` を対話的に作成（下記「step 0」詳細）/ テンプレ・skill 配置 | — | 構成（単一/複数アプリ・パス規約） |
| 1 | common 階層生成 | `reverse-engineering-common-spec` | 生成後の**要確認マーカー**一覧 |
| 1.5 | 機能インベントリ + 優先順 → 導入PLAN へ記載 | — | ★ 機能一覧と優先順（P0 から） |
| 2 | 代表機能 1 つをリバース | `reverse-engineering-feature-spec` | ★ Spec 粒度・スコープ |
| 3-4 | フォーマット策定 → テンプレ特化 | `tailoring-spec-format` | ★★ フォーマット決定（テーラリング） |
| 5 | 残り機能を優先順でループ | `reverse-engineering-feature-spec` | ★ 機能ごとの粒度 |
| 6 | 順行運用へ移行 | `auto-implement`（以降） | 導入完了の確認 |

各機能リバース後は `verifying-consistency` で spec ⇔ test ⇔ 実装 の整合を確認する。

---

## 初回フロー（導入PLAN が無いとき）

1. **プロジェクト点検**: ディレクトリ構成・`package.json`・ルーティングをざっと把握。
2. **step 0（対話的セットアップ）**: `.stdd.config.yml` が無ければ、下記「step 0」手順で 点検 → 草案 → 確認 → 書き込み を対話的に行う。
3. **step 1 実行**: `reverse-engineering-common-spec` を呼び、common 階層を生成。**要確認マーカー**（仮説つき）を一覧化して人間に提示。
4. **step 1.5（★人間判断）**: ルーティング・主要ドメインから機能を洗い出し、**優先順をユーザーと合意**。
5. **導入PLAN 生成**: `templates/introduction-plan.md` を雛形に `docs/common/plans/stdd-introduction.md` を作成し、機能を優先順で並べる。
6. 「次は step 2（代表機能のリバース）」を提示して停止。

---

## 再開フロー（導入PLAN があるとき）

1. 導入PLAN を読み、完了済み（`- [x]`）と未着手（`- [ ]`）を把握。
2. 最初の未着手項目を「次にやること」として 1 つ提示。
3. ユーザーの了承後、該当ステップのスキルを呼んで実行。
4. 完了したら導入PLAN の該当項目を `- [x]` に更新し、フォーマット決定があれば「決定ログ」に追記。
5. 次の未着手を提示して停止（**一度に 1 ステップ**。バッチ全自動にしない）。

---

## step 0: 対話的セットアップ（詳細）

`.stdd.config.yml` が無いときは、skill 自身が **点検 → 草案 → 確認 → 書き込み** を対話的に行う（サブスキルは呼ばない）。

### 0-1. リポジトリ点検（自動）

読み取って構成を推定する:

```
□ トップレベル構成 / package.json の workspaces → apps[] 候補（id・path）
   - monorepo: workspaces 各エントリ、apps/* や packages/* 配下のアプリ
   - 単一アプリ: ルート構成（id は project 名 または "web" 等）
□ package.json の scripts → commands（test / typecheck(tsc) / lint / format）
□ DB 型生成コマンド（例: supabase gen types）→ commands.db_types 候補
□ git のデフォルトブランチ → project.primary_branch
□ framework（next / remix / vite / sveltekit 等）→ apps[].framework
□ 既存 docs/ 構成 → docs.layout のパターン推定
```

### 0-2. 草案を提示

点検結果から `.stdd.config.yml` の草案を生成して提示する。先頭に `yaml-language-server` の schema ディレクティブを付ける。**推定し切れない項目も空欄にせず、推定値（仮説）を入れた上でコメントに `# ⚠️要確認: …` を添えてユーザーに是非を尋ねる**（spec の[要確認マーカー](../documenting-requirements/SKILL.md)と同じ「仮説＋確認」の原則を config 草案にも適用）。

```yaml
# yaml-language-server: $schema=<schema の URL または相対パス>
project:
  name: <推定>
  primary_branch: <git のデフォルトブランチ>
apps:
  - id: <推定>          # ^[a-z][a-z0-9_-]*$
    path: <推定>
commands:
  typecheck: <推定>
  test: <推定>
docs:
  layout:
    common_requirements: docs/common/REQUIREMENTS.md    # common 階層を使う場合のみ
    common_architecture: docs/common/ARCHITECTURE.md
    common_table_definition: docs/common/TABLE_DEFINITION.md
    common_api_spec: docs/common/API_SPEC.md             # API がある場合
    requirements: docs/{{app.id}}/{{feature_path}}/REQUIREMENTS.md
    tech_design: docs/{{app.id}}/{{feature_path}}/TECH_DESIGN.md
    test_plan: docs/{{app.id}}/{{feature_path}}/TEST_PLAN.md
    plan: docs/{{app.id}}/{{feature_path}}/plans/{{date}}.md
```

### 0-3. ★確認（停止）

書き込み前に、特に次をユーザーに確認する:

```
□ 単一 / 複数アプリ、各アプリの id・path
□ docs.layout のパス規約（単一アプリなら {{app.id}} を省く等の調整）
□ test / typecheck コマンドが実際に動くか
□ common 階層を使うか（使うなら common_requirements / common_architecture を含める）
□ worktree / devcontainer を使うか（workflow セクションを足すか）
```

### 0-4. 書き込み & 検証

- 合意後 `.stdd.config.yml` をリポジトリルートに書き込む。
- スキーマ検証（`packages/core/README.md`「JSON Schema のローカル検証」の手順）:
  ```
  npx -y js-yaml .stdd.config.yml > /tmp/stdd.json
  npx -y ajv-cli validate -s packages/core/schema/.stdd.config.schema.json -d /tmp/stdd.json
  ```
- skill / agent / テンプレの配置（vendoring または参照）が未了なら案内する。
- 検証が通ったら step 1 へ進む。

### 完了条件

```
□ .stdd.config.yml が存在し schema 検証を通る
□ 後続ステップが参照する apps / commands / docs.layout が揃っている
```

> 配置は `npx @careerchain/stdd init`（カレントディレクトリに `.claude/` と `.stdd.config.yml` を導入）に委譲してよい。未導入なら step 0 はそれを案内する。

---

## 守ること

- **一度に 1 ステップ**。複数機能を無確認で連続処理しない。
- **★ポイントでは必ず停止**してユーザーに聞く（優先順・粒度・フォーマット）。
- 遡行フェーズでは「実装が真実」。推測で spec を書かない。
- 導入PLAN 以外に進捗・履歴を持たない（SSOT 原則。spec 本体に「今回」「変更前」等を書かない）。

---

## When NOT to Use This Skill

- **単一機能のリバースだけ**したい: `reverse-engineering-feature-spec` を直接使う
- **common 階層だけ**作りたい: `reverse-engineering-common-spec` を直接使う
- **新規機能を実装**したい（導入済みプロジェクト）: `auto-implement` を使う
- **新規プロジェクト**（コードがまだ無い）の立ち上げ: `starting-new-with-stdd` を使う

---

## 参照ファイル

- **導入ガイド（なぜ/判断基準）**: [guide-for-existing-project.md](../../../packages/core/docs/guide-for-existing-project.md)
- **導入PLAN テンプレート**: [templates/introduction-plan.md](templates/introduction-plan.md)
- **common 階層のリバース**: [reverse-engineering-common-spec skill](../reverse-engineering-common-spec/SKILL.md)
- **機能単位のリバース**: [reverse-engineering-feature-spec skill](../reverse-engineering-feature-spec/SKILL.md)
- **フォーマット策定・テーラリング（step 3-4 / 7）**: [tailoring-spec-format skill](../tailoring-spec-format/SKILL.md)
- **整合性チェック**: [verifying-consistency skill](../verifying-consistency/SKILL.md)
- **順行運用（新機能実装）**: [auto-implement skill](../auto-implement/SKILL.md)
