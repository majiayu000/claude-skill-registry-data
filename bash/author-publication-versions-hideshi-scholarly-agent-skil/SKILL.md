---
name: author-publication-versions
version: 1.0.0
description: 著者自身の公開済み論文（Zenodo）の版系譜を取得し、リポジトリ横断の現行 DOI 台帳へ記録するスキル。自著引用・関連識別子の DOI 確定時、版上げ後、マトリクスの自著行更新時に発動する
---

# 自著公開版台帳スキル (Author Publication Versions)

## 目的
著者の公開済み成果（v1 は Zenodo）について、**概念 DOI** と **各版 DOI** を一次 API から取得し、リポジトリ横断の台帳に記録する。引用・`deposit-metadata` の関連識別子・文献マトリクスの自著行では **Current** の版 DOI だけを使う（旧版 DOI の誤用を防ぐ）。

## 発動タイミング
- 自著を引用・関連識別子に載せる直前（DOI の確定）
- Zenodo で版を上げた直後（台帳の再取得）
- 文献マトリクスの自著行（P1 / P2 / …）を更新する時
- ユーザーが「自著の版」「Zenodo の現行 DOI」を求めた時

## 前提
- 連絡先メール: `export SCHOLARLY_CONTACT_EMAIL="..."`（polite pool。未設定ならスクリプトは HTTP 前に停止）
- 入力一覧: [`config/author_publications.json`](../../../config/author_publications.json)（`works[].zenodo` に DOI またはレコード ID）
- v1 スコープ: **Zenodo のみ**（arXiv 版履歴・ORCID 全列挙は対象外）

## 実行手順

### Step 1: 入力の確認
1. `config/author_publications.json` の `works` に自著 DOI があるか確認する
2. 無い場合は DOI を追記するか、CLI の `--doi` で渡す
3. 出力先は **論文リポジトリのルート相対** `docs/literature/author-publication-versions.md`（paper-id 配下ではない。横断台帳）

### Step 2: 版系譜の取得
論文リポジトリ（例: `academic-papers`）をカレントにして実行する：

```bash
# サブモジュール導入時
python3 .scholarly-agent-skills/scripts/fetch_publication_versions.py

# スキル集リポジトリ直下、またはシンボリックリンク経由
python3 scripts/fetch_publication_versions.py

# 追加 DOI のみ / ドライラン
python3 scripts/fetch_publication_versions.py --doi 10.5281/zenodo.22065716 --dry-run
```

> 同一概念の複数版 DOI を渡しても、概念 ID で重複排除する。

### Step 3: 台帳の反映と下流の揃え
1. 生成された `docs/literature/author-publication-versions.md` を読む
2. **Cite targets** の現行 DOI を正とする
3. 必要なら次を現行 DOI に揃える（エージェントが勝手にコミットしない）:
   - 各論文の `literature/literature-matrix.md` の自著行
   - `design/deposit-metadata.md` の関連識別子（旧版 DOI を残さない）
   - 本文参考文献の自著エントリ

### Step 4: 旧版 DOI の扱い
- 台帳に旧版が載っていても、**引用・関連識別子の既定は Current のみ**
- 旧版 DOI を使うのは「特定版への歴史的言及」など明示理由がある場合に限る
- 概念 DOI（`conceptdoi`）は最新版へ解決されることがある。厳密な版固定が必要なら **版 DOI** を書く

## 成果物
- `docs/literature/author-publication-versions.md`（リポジトリ横断。Summary / Cite targets / 版テーブル）
- （任意）マトリクス・deposit-metadata・参考文献の DOI 同期差分（著者確認後）

## 関連スキル
- [`submission-venue-advisor`](../submission-venue-advisor/SKILL.md) — 公開メタデータの関連識別子草案
- [`literature-search`](../literature-search/SKILL.md) — 他者文献の検索（自著版台帳とは別）
- [`citation-traceability-audit`](../citation-traceability-audit/SKILL.md) — 本文引用と DOI の照合
- [`pdf-paper-ingestion`](../pdf-paper-ingestion/SKILL.md) — 現行版 PDF の再取得が必要な時
