---
name: source-criticism-gate
version: 1.1.0
description: 論文で引用・参照されるWebサイト・データ・文献の信頼性を評価する際、査読付き論文・公的国際機関・政府統計などの高信頼性ソース（Tier 1/Tier 2）のみを選別・監査する史料批判ゲートスキル。
---

# 情報源信頼性監査・史料批判ゲートスキル (Source Criticism Gate)

## 目的
インターネットや外部データベースから取得した情報・文献・統計データが、学術論文の引用基準（学術的客観性・再現性・査読性）を満たしているかを自動判定し、信頼性の低い不確かな情報源（ブログ・掲示板・未検証の匿名サイト）が論文本文に混入するのを未然に防ぐ。

## 判定基準（情報源の3階層評価: Hierarchy of Evidence Trustworthiness）

### 🟢 Tier 1: 最高信頼性（Peer-Reviewed Academic & International Official）
- **査読付き学術論文・リポジトリ**: OpenAlex, arXiv, Crossref, Semantic Scholar, JSTOR, ScienceDirect, Springer, NBER, RePEc
- **国際公的機関**: 世界銀行 (World Bank), アジア開発銀行 (ADB), 国連 (UN), IMF, OECD, WHO
- **国家政府統計局・中央銀行**: 各国統計局（日本 総務省統計局, 米国 Census Bureau, 各国 NSO 等）、中央銀行（日銀, FRB, ECB）

### 🟡 Tier 2: 高信頼性（Official Government & Recognized Research Institutes）
- **政府省庁公式発表**: 各国省庁（文部科学省・財務省および各国の相当機関）
- **公的独立シンクタンク・研究機関**: Brookings, RAND Corporation, RIETI, 各国の公的開発研究所
- **高等教育機関リポジトリ**: 大学公式ドメイン (`.edu`, `.ac.jp`, `.ac.uk`) の紀要・ディスカッションペーパー

### 🔴 Tier 3: 引用厳禁・低信頼性（Untrusted / Informal Sources）
- **個人ブログ・SNS・Web掲示板**: Note, Qiita (未検証記事), X (Twitter), Reddit, 2ch/5ch
- **Wikipedia / 一般百科事典**: （※直接の引用は不可。参照先の一次文献論文をたどって引用すること）
- **匿名メディア・商業広告サイト・まとめサイト**: 企業PR記事、アフィリエイト、出所不明ニュース

---

## 適用範囲の注意（Tier 1 内部の係争について）

本ゲートは**情報源の種類**の信頼性を判定するものであり、Tier 1（査読付き文献）内部の学派対立・係争状態・撤回有無は評価しない。これらは以下の役割分担で扱う：

- **対立陣営の発掘・記録**: `literature-search` Step 1.5（対立陣営探索）と `literature-matrix.md` の「立場・陣営」「係争ステータス」列
- **断定トーンの監査**: `claim-evidence-gate` の Field Disagreement 軸

---

## 処理手順

### Step 1: 情報源の信頼度判定
取得したURLまたはドメインに対して、判定スクリプトを実行する：

```bash
# スクリプトの実行
python3 scripts/evaluate_source_trust.py https://example-source.org/report.pdf
```

> サブモジュール導入先のリポジトリから実行する場合は、スクリプトパス頭に `.scholarly-agent-skills/` を付与してください。

### Step 2: 監査ログの出力と選別
判定結果に基づき、以下の処置を行う：
- **Tier 1 / Tier 2 の場合**: 合格。`docs/literature/literature-matrix.md` または `docs/data/` にデータとして保存し、論文本文からの参照を許可する。
- **Tier 3 の場合**: 却下（Rejected）。論文本文への直接引用を固く禁止し、代替となる一次文献・公的統計を再検索・指定する。

## 成果物
- `docs/design/source-criticism-report.md` (情報源信頼性・史料批判判定レポート)
