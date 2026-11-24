---
name: verifying-consistency
description: |-
  Spec（REQUIREMENTS.md / TECH_DESIGN.md）⇔ テスト ⇔ 実装 の整合性を機能単位でチェックする。ブランチ分岐点からの差分を抽出し、要件・設計・テスト・実装の不整合（機能漏れ、テスト漏れ、設計と実装の乖離など）を検出する。
when_to_use: |-
  「整合性チェック」「verify consistency」「Spec準拠確認」「テスト漏れ確認」「STDD整合性」「要件と実装の乖離」「Specと実装の差分」など、STDD に基づく品質確認の依頼があったとき。
allowed-tools: Read, Grep, Glob, Bash
---

# Spec・テスト・実装の整合性チェック

このセッション/ブランチで作成・修正した機能について、Spec・テスト・実装の整合性を確認する。

## 1. 対象ファイルの特定

### ブランチ分岐点からの差分を特定

`.stdd.config.yml` の `project.primary_branch`（PR/統合先ブランチ）を読み、その分岐点からの差分を特定する。

```bash
# <primary_branch> は .stdd.config.yml の project.primary_branch（例: main / develop）
git fetch origin <primary_branch>
git log --oneline origin/<primary_branch>...HEAD
git diff origin/<primary_branch>...HEAD --name-only
```

以下を特定:

- **Specドキュメント**: `docs/` 配下の `REQUIREMENTS.md`, `TECH_DESIGN.md`（`docs.lineup: layered` では `API_DESIGN.md` / `SCREEN_DESIGN.md` とテスト設計。以下の TECH_DESIGN.md / TEST_PLAN.md も同じく読み替える）
- **テスト**: `*.test.ts`, `*.test.tsx`, `e2e/tests/**/*.spec.ts`
- **実装**: `app/`, `components/`, `lib/`, `actions/`, `domain/` 配下のファイル

## 2. ID ベース・トレーサビリティ監査（機械的・最優先）

名前一致ではなく**安定 ID**（`UC-<feature>-NN` / `FL-<feature>-NN`）で 要件 → 技術設計 → テスト → 実装 を突合する。
検知は共通スキャナ `.claude/hooks/trace-audit.sh`（依存なし・pre-push / CI と同一ロジック）に委ね、
結果を解釈して報告する。設定は `.stdd.config.yml` の `traceability`（`enforce` / `patterns` / `scan` 等）。

### 2A. 順方向（抜け漏れ検知）

```bash
bash .claude/hooks/trace-audit.sh
```

- トレーサビリティ行列（ID × 設計 / テスト計画 / テスト / 実装）と抜け漏れ一覧を出力する。
- 検知する抜け漏れ: 設計漏れ / テスト計画漏れ / テスト実装漏れ / 実装漏れ（`require_impl_annotation` 時）/ 孤児参照 / ID 重複。
- `docs.lineup: layered` では「設計書の表の突合」も出す（レスポンスコード・行の ID・受入基準。一覧は方法論の `id-chain.md`）。「未実施」「対象 0 件」は合格として扱わない。
- `traceability.enforce=block` のとき、抜け漏れがあれば非ゼロ終了する（それを NG 判定に用いる）。

### 2B. 逆方向（テスト/実装起点の改修 → 影響範囲）

このセッション / ブランチの変更ファイル（§1 で取得済み）を渡し、テスト・実装起点の改修が**どの要件に波及するか**、
および**追跡不能変更**（どの ID にも紐づかないテスト / 実装変更 ＝ spec-first 逸脱の疑い）を検知する。

```bash
# <primary_branch> は .stdd.config.yml の project.primary_branch
CHANGED=$(git diff --name-only origin/<primary_branch>...HEAD)
bash .claude/hooks/trace-audit.sh --changed $CHANGED

# 特定 ID の全リンク先を辿るとき
bash .claude/hooks/trace-audit.sh --impact UC-<feature>-01
```

- 各変更が紐づく ID と、その ID の全リンク先（対応要件・技術設計箇所・他テスト / 他実装）を列挙する。
- ID に解決しないテスト / 実装変更は **追跡不能変更**として報告し、spec-first（Spec 起点）に立ち返るよう促す。

> トレーサビリティ監査で検知した抜け漏れ・追跡不能変更は、§4 の出力にトレーサビリティ行列・影響範囲サマリとして必ず載せる。以降の §3 は ID では機械化しきれない内容（設計判断の反映・モック整合など）を人/AI が補完的に確認する。

## 3. 整合性チェック項目（補完・人/AI による確認）

### A. REQUIREMENTS.md ⇔ 実装

- [ ] REQUIREMENTS.md のユースケース（振る舞い＋受入基準）が実装で網羅されているか
- [ ] REQUIREMENTS.md の画面仕様（ボタン、フォーム、表示項目）が実装と一致しているか
- [ ] REQUIREMENTS.md に記載された機能要件が全て実装されているか

### B. TECH_DESIGN.md ⇔ 実装

- [ ] TECH_DESIGN.md の「Technical Implementation」セクションの設計方針に従っているか
- [ ] TECH_DESIGN.md の「Decision」セクションの決定事項が実装に反映されているか
- [ ] TECH_DESIGN.md に記載されたファイル構成と実際のファイル構成が一致しているか

### C. TECH_DESIGN.md ⇔ テスト

- [ ] TECH_DESIGN.md に記載されたテスト総数と、実際のテストケース数が一致しているか
- [ ] TECH_DESIGN.md の「Test Strategy」セクションに記載された全テストケースが実装されているか
- [ ] 実装されたテストで、TECH_DESIGN.md に記載されていないものがないか

### D. テスト ⇔ 実装

- [ ] テストが実装を正しく検証しているか（実装の変更でテストが壊れていないか）
- [ ] テストのモック設定が実装の実際の動作と一致しているか

## 4. 出力形式

以下の形式で結果を報告:

```
## 整合性チェック結果

### 対象機能: [機能名]

### トレーサビリティ行列（trace-audit.sh 順方向）
| ID | 種別 | 設計 | テスト計画 | テスト | 実装 |
|----|------|:---:|:---:|:---:|:---:|
| UC-<feature>-01 | UC | ✅ | ✅ | ✅ | ✅ |

### 影響範囲（trace-audit.sh 逆方向 / テスト・実装起点の変更がある場合）
- 変更 → 紐づく ID → 波及する要件・設計・他テスト/他実装
- 追跡不能変更（ID に紐づかないテスト/実装）: [あれば列挙]

### チェック結果サマリ
| 項目 | 状態 | 備考 |
|------|------|------|
| トレーサビリティ（ID 抜け漏れ） | OK / WARN / NG | trace-audit.sh の抜け漏れ件数 |
| 追跡不能変更 | OK / WARN / NG | ID に紐づかないテスト/実装変更 |
| REQUIREMENTS.md ⇔ 実装 | OK / WARN / NG | |
| TECH_DESIGN.md ⇔ 実装 | OK / WARN / NG | |
| TECH_DESIGN.md ⇔ テスト | OK / WARN / NG | |
| テスト ⇔ 実装 | OK / WARN / NG | |

### 検出された不整合
1. [不整合の内容]
   - 期待: [Specの記載内容]
   - 実際: [テスト/実装の内容]
   - 推奨アクション: [修正方法]

### 推奨事項
- [改善提案があれば記載]
```

## 5. 注意事項

- `traceability.enabled=false` / 設定が無い場合は trace-audit.sh がスキップする旨を報告し、§3 の補完チェックのみ行う
- Specドキュメントが存在しない場合は、その旨を報告
- 軽微な不整合（コメントの差異など）は WARN として報告
- 重大な不整合（機能の欠落、テスト漏れなど）は NG として報告
- 不整合が見つかった場合、修正の優先度も提示
