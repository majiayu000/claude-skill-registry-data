---
name: reverse-engineering-common-spec
description: |-
  既存プロジェクトに STDD を導入する際、コードベース全体をリバースエンジニアリングして common 階層の Spec（docs/common/REQUIREMENTS.md + ARCHITECTURE.md（システム概要）+ TABLE_DEFINITION.md（テーブル定義）+ API_SPEC.md（API がある場合））を作成する。サービス概要・システム構成・リポジトリ構成・レイヤ規約・データモデル・API 契約を俯瞰する SSoT を、導入時に一度だけ生成する。機能/ページ単位のリバースエンジニアリングには reverse-engineering-feature-spec を使用する。
when_to_use: |-
  「STDD導入」「stdd導入」「共通spec生成」「common階層」「プロジェクト全体のリバースエンジニアリング」「ARCHITECTURE.md作成」「アーキテクチャのドキュメント化」「既存プロジェクトにstdd」に関する作業のとき。
allowed-tools: Read, Write, Edit, Glob, Grep, Bash
---

# common spec のリバースエンジニアリング

既存（稼働中）プロジェクトに STDD を導入する際、コードベース全体を input にして **common 階層**の Spec を作成する。

| 出力 | 内容 |
| ---- | ---- |
| `docs/common/REQUIREMENTS.md` | サービス概要・登場アクター・アプリ構成（プロジェクト全体のビジネス要件） |
| `docs/common/ARCHITECTURE.md` | システム概要（システム構成・リポジトリ構成・レイヤ規約・スタック・連携・セキュリティ・インフラ。データモデル/API は持たない） |
| `docs/common/TABLE_DEFINITION.md` | 全テーブル定義の SSoT（カード形式・ER図なし） |
| `docs/common/API_SPEC.md` | API 契約の SSoT（OpenAPI 風 Markdown。API がある場合） |

このうち `ARCHITECTURE.md` / `TABLE_DEFINITION.md` / `API_SPEC.md` は技術 spec (tech_specs) の common 分にあたる（→ `stdd-methodology.md` §3）。テンプレートは `../documenting-requirements/templates/requirements-common.md`（REQUIREMENTS）/ `../documenting-tech-specs/templates/architecture-common.md`（ARCHITECTURE。TABLE_DEFINITION / API_SPEC も同ディレクトリ）を参照する。

## 位置づけ — 導入時に一度だけ

common 階層はプロジェクト全体で 1 組しか存在しない SSoT であり、本スキルは **STDD 導入時に一度だけ**実行する想定。
作成後の更新（アーキテクチャ変更時など）は本スキルではなく、通常の Spec 更新として `documenting-requirements`（要件）／ `documenting-tech-specs`（ARCHITECTURE 等の技術設計）で扱う。

```
STDD 導入フロー（既存プロジェクト）

1. reverse-engineering-common-spec  ← 本スキル（一度だけ）
        ↓  common 階層が揃う
2. reverse-engineering-feature-spec ← 機能ごとに繰り返す
        ↓
3. auto-implement                    ← 以降の新機能は順行 STDD
```

**順序の理由**: 先に common 階層（レイヤ規約・共有ドメインモデル・テーブル定義・API 契約）を固定しておくと、後続の機能単位リバース（`reverse-engineering-feature-spec`）の精度と速度が上がる。

---

## 最重要原則 — 実装・設定が真実

common 階層でも **実装が真実（Source of Truth）** である。推測や理想論で書かず、必ず一次情報を確認してから書く。
feature 階層と違い、確認する一次情報は **UI 文言ではなく構成・設定・型定義** である。

| 記述する内容 | 確認元（一次情報） | よくある間違い |
| ------------ | ------------------ | -------------- |
| アプリ構成・責務 | トップレベルディレクトリ / README | 想像でアプリ名・責務を書く |
| パッケージ分割 | `package.json` の workspaces / 依存定義 | モジュール境界を推測で書く |
| レイヤ規約・依存方向 | `domain/` 配下の実構成・lint ルール | 一般論の Clean Architecture を書く |
| 外部サービス連携 | 環境変数・SDK の import 箇所 | 使っていないサービスを書く／使用中を漏らす |
| テーブル一覧（TABLE_DEFINITION） | 生成された DB 型定義（`database.types.ts` 等） | テーブル名・カラム名を想像で書く |
| デプロイ・環境 | CI/CD 設定（`.github/workflows` 等） | ブランチ→環境マッピングを推測で書く |

---

## 読む順序とチェックリスト

`ARCHITECTURE.md`（システム概要）の目次がそのまま読む順序になる。データモデルは `TABLE_DEFINITION.md`、API 契約は `API_SPEC.md` に分離する。

### 1. システム構成（`REQUIREMENTS.md` のサービス概要・アクターもここで把握）

```
□ README / トップレベルディレクトリ構成 → サービスの目的・アプリ構成
□ デプロイ設定 (vercel.json / Dockerfile / .github/workflows) → 環境とブランチ戦略
□ 環境変数・SDK の import → 外部サービス連携 (認証 / DB / ストレージ / メール / 監視 等)
```

### 2. リポジトリ構成

```
□ package.json の workspaces / モジュール分割
□ 依存管理ルール (どの依存がどこに置かれているか、アプリ間 import 制限の有無)
□ 共有パッケージ (packages/shared 等) の責務
```

### 3. レイヤードアーキテクチャ

```
□ domain/ 配下の構成 (models / repository / service / ports)
□ 依存方向ルール (UI → Service → Repository → DB 等)、禁止依存
□ 代表的なデータフロー 1 本 (Server Action / API → Service → Repository)
```

### 4. データモデル・DB設計（→ `TABLE_DEFINITION.md` に記述）

```
□ 生成された DB 型定義 (database.types.ts 等) を正としてテーブルを列挙
□ ドメイングループへの分類（カード形式・ER 図は持たない）
□ 設計方針 (論理削除 / 主キー / 時系列カラム / マイグレーション規約)
```

### 5. API 契約（API がある場合 → `API_SPEC.md` に記述）

```
□ Server Actions / API Route / RPC のエンドポイントを列挙
□ 入出力（リクエスト / レスポンス）の型・契約を OpenAPI 風 Markdown で記述
```

---

## 確信が持てない箇所は要確認マーカーを残す

実装からの読み取りに確信が持てない箇所は **要確認マーカー**（可視インライン）で明示する。逆生成でも「実装からこう読めた」という**仮説とセット**で置き、その是非をユーザーに確認させる。構文の SSoT は [documenting-requirements SKILL「要確認マーカー」](../documenting-requirements/SKILL.md)。
これは**一時的な注記**であり、人間レビューで確定したらマーカーを除去する（恒久的に残さない）。SSoT 原則上、確定済みの Spec に作成プロセスや未確定メモを残してはならない。

```markdown
- **外部ウォレット連携**: 関連テーブルと RPC が存在する。⚠️要確認(仮説: 本番で有効 / 確認: 現行稼働範囲)
```

---

## 完了条件

```
□ docs/common/REQUIREMENTS.md を作成（サービス概要 / アクター / アプリ構成）
□ docs/common/ARCHITECTURE.md を作成（システム概要：システム構成 / リポジトリ / レイヤ。データモデル/API は持たない）
□ docs/common/TABLE_DEFINITION.md を作成（全テーブル定義・カード形式・ER 図なし）
□ docs/common/API_SPEC.md を作成（API がある場合・API 契約の SSoT）
□ テーブル一覧は生成された型定義ファイルと一致している
□ 固有名詞・社外秘の値を不要に含めていない（公開を想定する場合）
□ 要確認マーカーは仮説とセットになっており、「人間に確認すべき項目」としてレビュー依頼にまとめた
```

---

## When NOT to Use This Skill

- **機能 / ページ単位のリバースエンジニアリング**: `reverse-engineering-feature-spec` を使用
- **新規機能の仕様策定**: `documenting-requirements`（要件）／ `documenting-tech-specs`（技術設計）を使用
- **common 階層作成後のアーキテクチャ更新**: 通常の Spec 更新として `documenting-tech-specs`（ARCHITECTURE/TABLE/API）で扱う

---

## 次のステップ

1. **機能単位のリバース** → `reverse-engineering-feature-spec`（common 階層を前提に、機能ごとに繰り返す）
2. **新機能の実装** → `auto-implement`（以降は Spec → Test → 実装 の順行 STDD）

---

## 参照ファイル

- **common テンプレート**: `../documenting-requirements/templates/requirements-common.md`（REQUIREMENTS）/ `../documenting-tech-specs/templates/architecture-common.md`・`table-definition-common.md`・`api-spec-common.md`（技術階層）
- **2 階層構造の解説**: `packages/core/docs/stdd-methodology.md` §3.1
- **機能単位リバース**: [reverse-engineering-feature-spec skill](../reverse-engineering-feature-spec/SKILL.md)
- **要件テンプレート**: [documenting-requirements skill](../documenting-requirements/SKILL.md)
- **技術設計テンプレート**: [documenting-tech-specs skill](../documenting-tech-specs/SKILL.md)
