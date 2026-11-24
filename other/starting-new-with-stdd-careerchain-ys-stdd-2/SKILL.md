---
name: starting-new-with-stdd
description: |-
  新規（コードがまだ無い）プロジェクトを STDD で立ち上げる作業を、エージェントのセッションで段階的に駆動する。立ち上げガイドに従い、アプリ骨組み生成→common 階層の前方設計→最初の feature→フォーマット策定→feature ループ→通常運用への移行までを、要件・技術設計・ワイヤーフレーム・フォーマット策定・PLAN・実装・整合性確認の各スキルを順に呼びながら進める。進捗は立ち上げPLANで保持し、セッションを跨いで再開できる。既に稼働しているコードへの導入は introducing-stdd を使う。
when_to_use: |-
  新規（コードがまだ無い）プロジェクトの立ち上げを進める／再開するとき。「新規プロジェクトをstddで立ち上げる」「立ち上げの続き」「greenfield stdd」など、新規フローと確定している場合。新規/既存が未確定の最初の入口は setup-stdd（ルーター）が判定して本スキルへ委譲する。
allowed-tools: Read, Write, Edit, Glob, Grep, Bash
---

# STDD 立ち上げドライバー（新規プロジェクト）

新規プロジェクトの STDD 立ち上げを、セッションで 1 ステップずつ進めるための**薄い駆動役**。
自前の実装ロジックは持たず、各ステップで**既存スキルを順に呼び**、人間判断ポイントで停止し、進捗を**立ち上げPLAN**に記録する。

> 「なぜ」「各ステップで何を判断するか」は [`guide-for-new-project.md`](../../../packages/core/docs/guide-for-new-project.md) を参照。
> 本スキルはその operational な実行役。既存（稼働中）プロジェクトへの導入は [`introducing-stdd`](../introducing-stdd/SKILL.md)。

## 設計方針（重要）

- **agent オーケストレーションはしない**。エージェントがメインセッションで手順を進める軽量ドライバー。
- 立ち上げは判断主体のため、**人間を常にループに入れる**（アーキ判断・フォーマット策定・粒度は必ず確認）。
- 状態は立ち上げPLAN（`docs/common/plans/stdd-bootstrap.md`）にのみ持つ。本スキルはステートレス。
- 新規は**最初から順行**（Spec → Test → 実装）。`reverse-engineering-*`（遡行）は使わない。

---

## 起動時の動作

### 1. 立ち上げPLAN の有無を確認

```
docs/common/plans/stdd-bootstrap.md
```

- **無い場合 → 初回**: 下記「初回フロー」を実行し、立ち上げPLAN を作成する。
- **ある場合 → 再開**: 立ち上げPLAN を読み、最初の未チェック項目（`- [ ]`）を「次にやること」として提示し、該当ステップを実行する。

### 2. 設定確認

`.stdd.config.yml` を読み、`apps[]` / `commands` / `docs.layout`（`common_requirements` / `common_architecture` 含む）を把握する。
`npx @careerchain/stdd init` で導入済みなら揃っている。無ければ step 0 を案内する。

---

## ステップ実行表

各ステップは「呼ぶスキル」と「停止して人間に確認すること」を持つ。

| step | 実行内容 | 呼ぶスキル | ★停止して確認 |
| ---- | -------- | ---------- | ------------- |
| 0 | scaffold / `.stdd.config.yml` 点検（common 階層前提） | — | 構成（単一/複数アプリ・パス規約） |
| 1 | **プロダクトコンセプトのヒアリング**（下記「step 1」詳細） | — | ★ どんなアプリ／要件の概要（最低 1 レスポンス） |
| 2 | **アプリ骨組みを対話駆動**（stack 固有） | （stack 手順へ委譲。下記「step 2」詳細） | ★ 構成・コマンド疎通 |
| 3 | **common 階層を前方設計**（docs/common を埋める） | `documenting-requirements`（REQUIREMENTS）→ `documenting-tech-specs`（ARCHITECTURE 等） | ★ 目的・アクター・初期アーキ |
| 4 | 最初の feature を順行 spec 化（P0 コアから 1 本） | `documenting-requirements` → `generating-wireframes` → `documenting-tech-specs` | ★ Spec 粒度・スコープ |
| 5 | フォーマット策定 → テンプレ特化 | `tailoring-spec-format` | ★★ フォーマット決定 |
| 6 | feature を順行 STDD でループ | `documenting-plans` → `auto-implement` | ★ 機能ごとの粒度 |
| 7 | 通常運用へ移行 | `auto-implement`（以降） | 立ち上げ完了の確認 |

各 feature 実装後は `verifying-consistency` で spec ⇔ test ⇔ 実装 の整合を確認する。

---

## 初回フロー（立ち上げPLAN が無いとき）

1. **scaffold 確認**: `npx @careerchain/stdd init` の導入物（`.stdd.config.yml`・`.claude/`・`docs/`）が揃っているか点検。未導入なら `npx @careerchain/stdd init` を案内。
2. **step 1（★人間判断・最優先）**: 下記「step 1」手順で**プロダクトコンセプトをヒアリング**し、最低 1 レスポンスを得る。技術スタック等の確認より先に必ず実施する。
3. **step 2（アプリ骨組み）**: 下記「step 2」手順で stack 固有の骨組み生成を対話駆動。step 1 で得たコンセプトを stack 選定の判断材料に使う。
4. **step 3（★人間判断）**: `documenting-requirements` で `docs/common/REQUIREMENTS.md` を、`documenting-tech-specs` で `docs/common/ARCHITECTURE.md` を**前方設計**（step 1 のコンセプトを起点に、仮説として埋める）。
5. **step 4（★人間判断）**: P0 コア機能を 1 つ選び、順行で feature spec を作る。
6. **立ち上げPLAN 生成**: `templates/bootstrap-plan.md` を雛形に `docs/common/plans/stdd-bootstrap.md` を作成し、step 1 で得たコンセプトを「プロダクトコンセプト」セクションに転記、想定 feature を優先順で並べる。
7. 「次は step 5（フォーマット策定）」を提示して停止。

---

## 再開フロー（立ち上げPLAN があるとき）

1. 立ち上げPLAN を読み、完了済み（`- [x]`）と未着手（`- [ ]`）を把握。
2. 最初の未着手項目を「次にやること」として 1 つ提示。
3. ユーザーの了承後、該当ステップのスキルを呼んで実行。
4. 完了したら立ち上げPLAN の該当項目を `- [x]` に更新し、フォーマット決定があれば「決定ログ」に追記。
5. 次の未着手を提示して停止（**一度に 1 ステップ**。バッチ全自動にしない）。

---

## step 1: プロダクトコンセプトのヒアリング（詳細）

**最初に必ず実施する**。技術スタック・骨組み・common ドキュメントなどあらゆる確認の**前に**ユーザーから 1 レスポンスを得る。
ここで得た内容は step 2（stack 選定の判断材料）と step 3（common 階層の前方設計の起点）の双方に流す。

### 1-1. 何を聞くか

「**どんなシステム／アプリ／サービスを作りたいですか？要件の概要を教えてください**」を起点に、ユーザーの言葉でフリーフォームに聞く。
箇条書きやフォームを強制しない。例示として以下を添えてもよいが、回答を縛らない:

- 解決したい問題 / 想定ユーザー / 中核機能 / 想定スケール 等

### 1-2. 進める条件（重要）

- **最低 1 レスポンス**を得たら、その**詳細度に関わらず**次ステップへ進む。追加質問で深掘りしない。
- 不足は step 3（common 階層の前方設計）以降で**仮説**として補う。仮説には必ず**要確認マーカー**を添えてユーザーに是非を確認させ、feature 開発で検証して更新する（→ [要確認マーカー](../documenting-requirements/SKILL.md)）。

### 1-3. 記録

- 立ち上げPLAN（`docs/common/plans/stdd-bootstrap.md`）の「プロダクトコンセプト」セクションにユーザーの 1 レスポンスを**そのまま転記**する（要約や勝手な拡張を加えない）。
- step 3 で common `REQUIREMENTS.md` を書く際の起点になる。

---

## step 2: アプリ骨組みの対話駆動（詳細）

新規はアプリ本体がまだ無いので、stack 固有の骨組み（フレームワーク・DB・E2E）を立てる。
**本スキルは stack 非依存**なので、コマンドの実体は持たず、使用中の stack 手順を SSoT として参照・実行支援する。

### 2-1. stack の特定（ユーザーの指定で 3 分岐）

まず `.stdd.config.yml` の `plugins` / `apps[].framework` を読む。既に stack が確定していればそれに従う。
未確定なら、**ユーザーの技術スタック指定の有無・内容**で次の 3 通りに分岐する。step 1 のコンセプトを判断材料に使う。

```
① ユーザーが Next.js / Supabase を明示的に指定
   → 同梱の nextjs-supabase starter / plugin に従う
     （生成元テンプレートの README「次の手順」が SSoT。playwright も同梱）

② ユーザーが Next.js/Supabase 以外の技術を明示的に指定（Rails / Django / Laravel / Vite+React など）
   → そのフレームワーク公式の scaffold 手順を汎用駆動する（2-2 ルート B）
     公式ドキュメント / 公式 CLI（例: rails new / django-admin startproject /
     npm create vite@latest 等）の記述を SSoT とし、本スキルにはコマンドを書かない

③ ユーザーが技術を指定していない
   → step 1 で得たプロダクトコンセプトを読み、適合する stack を踏み込んで提案する:
     ・コンセプトが Web アプリ寄りで素直なら「nextjs-supabase なら starter / plugin を
       同梱しているのですぐ立ち上げられます」とデフォルト候補として一押しする
     ・コンセプト上ほかの stack が明らかに適する場合（モバイル中心 / データ分析 /
       既存資産が別言語 等）は、その stack を理由つきで推奨する
   → ユーザーが nextjs-supabase を選べば①、別 stack を選べば②へ流れる
```

> nextjs-supabase は**同梱のデフォルト starter**という位置づけで、唯一の対応 stack ではない。
> ③ では押し付けず、コンセプトに最も合う選択をユーザーと決める。

### 2-2. 骨組み生成を対話駆動

選んだ stack の手順を**1つずつ提示し、ユーザーの確認のもと実行**する。具体コマンドは本スキルに持たず、参照先の記述に従う。

- **ルート A（nextjs-supabase）**: starter テンプレート README / 各プラグイン guide の「次の手順」が SSoT（例: `create-next-app` / `supabase init` / Playwright 導入）。
- **ルート B（その他あらゆる stack）**: そのフレームワーク公式の scaffold CLI を SSoT とし、初期化コマンドを 1 つずつ確認実行（例: `rails new` / `django-admin startproject` / `npm create vite@latest`）。生成後、テスト / 型チェック / ビルド等のコマンドを把握し、2-3 で `.stdd.config.yml` の `commands.*` を実体に合わせる。

### 2-3. 設定の実体合わせ（★確認）

```
□ apps[].path / apps[].port が実体と一致
□ commands.test / typecheck / build / db_* が実際に動く
```

> 骨組みが既に用意されている場合は step 2 を飛ばして step 3 へ。

---

## 守ること

- **一度に 1 ステップ**。複数 feature を無確認で連続処理しない。
- **★ポイントでは必ず停止**してユーザーに聞く（アーキ判断・粒度・フォーマット）。
- common 階層は**前方設計＝仮説**。作り込みすぎず、feature 開発で検証して更新する。確定しない箇所は**章を省略せず**、**要確認マーカー**（`**⚠️要確認**｜仮説: … ／確認: …`）を仮説とセットで置いて網羅性を保つ。構文の SSoT は [documenting-requirements SKILL「要確認マーカー」](../documenting-requirements/SKILL.md)。
- 立ち上げPLAN 以外に進捗・履歴を持たない（SSOT 原則。spec 本体に「今回」「変更前」等を書かない）。
- 遡行スキル（`reverse-engineering-*`）は使わない（新規にはコードが無い）。

---

## When NOT to Use This Skill

- **既に稼働しているコード**への STDD 導入: `introducing-stdd` を使う
- **単一機能の spec を書く / 実装する**だけ: `documenting-requirements`・`documenting-tech-specs` / `auto-implement` を直接使う
- **フォーマット策定だけ**やり直したい: `tailoring-spec-format` を直接使う

---

## 参照ファイル

- **立ち上げガイド（なぜ/判断基準）**: [guide-for-new-project.md](../../../packages/core/docs/guide-for-new-project.md)
- **立ち上げPLAN テンプレート**: [templates/bootstrap-plan.md](templates/bootstrap-plan.md)
- **common / feature 要件作成**: [documenting-requirements skill](../documenting-requirements/SKILL.md)
- **common / feature 技術設計作成**: [documenting-tech-specs skill](../documenting-tech-specs/SKILL.md)
- **ワイヤーフレーム**: [generating-wireframes skill](../generating-wireframes/SKILL.md)
- **フォーマット策定・テーラリング**: [tailoring-spec-format skill](../tailoring-spec-format/SKILL.md)
- **PLAN 作成**: [documenting-plans skill](../documenting-plans/SKILL.md)
- **順行実装**: [auto-implement skill](../auto-implement/SKILL.md)
- **整合性チェック**: [verifying-consistency skill](../verifying-consistency/SKILL.md)
- **既存プロジェクトへの導入**: [introducing-stdd skill](../introducing-stdd/SKILL.md)
