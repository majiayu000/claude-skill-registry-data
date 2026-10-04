---
name: primary-data-integration
version: 1.0.0
description: 独自調査データ (実験ログ・アンケート・インタビュー逐語録) の受入時・分析前に、AI Ignore・PII匿名化ファイル指定・構造化を行い本文に結合するスキル
---

# 独自調査資料・一次データ統合スキル (Primary Data Integration)

## 目的
研究者自身が採取・観測・収集した独自の調査資料（実験ログ、アンケート集計、インタビュー逐語録、未公開史料、現場観察ノート等）を安全に構造化・インデックス化（`docs/data/research-data-index.md`）し、個人情報保護・AIインデックス除外（AI Ignore）およびPIIマスキングを実施した上で、論文の主張（Claim）と直接バインド・分析を行う。

## 発動タイミング
- 実験ログ・アンケート結果・インタビュー逐語録・未公開史料等の調査データを入手・整理した時
- 本文の主張（Claim）に一次データを結合・引用する段階

## セキュリティ＆プライバシー設定 (Privacy & PII Protection)

生の調査データや非匿名化インタビュー記録を AI Agent に直接読み込ませないため、以下の2段階の保護を実施する：

### 1. 生データフォルダの AI Agent 除外 (AI Ignore)
同梱スクリプト [`scripts/setup_ai_ignore.py`](../../../scripts/setup_ai_ignore.py) を実行し、生の調査データフォルダ（`raw_data/`, `transcripts_raw/` 等）を AI のインデックス対象から一括除外する：
```bash
# 基本実行 (サブモジュール導入時: python3 .scholarly-agent-skills/scripts/setup_ai_ignore.py)
python3 scripts/setup_ai_ignore.py
```
（`.cursorignore`, `.claudeignore`, `.agentsignore`, `.ignore` が自動生成・更新されます）

### 2. 個人情報（PII）の自動マスキング・匿名化
実名がシェル履歴やプロセス一覧に遺留するのを防ぐため、置換マップファイル（`mapping.json` など）を指定して PII マスキングを行う：
```bash
# マッピングファイル (mapping.json) を作成して指定実行
python3 scripts/mask_pii_data.py data/raw_interview.txt --names-file mapping.json
```
※ `mapping.json` 例: `{"山田太郎": "調査対象者A", "佐藤花子": "調査対象者B"}` （`.gitignore` や AI Ignore 対象に設定することを推奨）
（匿名化されたファイルが `data/anonymized/` 配下に保存され、安全にAI分析へ利用可能になります）

> [!NOTE]
> サブモジュール導入先のリポジトリから実行する場合は、スクリプトパス頭に `.scholarly-agent-skills/` を付与してください。

## 処理手順

### Step 1: 調査資料インベントリの作成 (`docs/data/research-data-index.md`)
匿名化済みの調査資料を以下のように一意のIDでカタログ化する：

```markdown
### 資料ID: [例: DATA-2024-01]
- **資料名称**: 2024年夏季・地方都市商店街意識調査アンケート（匿名化済み）
- **データ種別**: 定量データ (N=350, 有効回答率82%)
- **収集方法・時期**: 2024年7月〜8月 / 訪問面接調査
- **保管パス**: `data/anonymized/2024_summer_survey.csv`

### 資料ID: [例: INTERVIEW-03]
- **資料名称**: A社開発責任者への深層インタビュー逐語録（PIIマスキング済み）
- **データ種別**: 定性データ (文字起こし / 氏名・電話番号匿名化済み)
- **保管パス**: `data/anonymized/transcript_B.md`
```

### Step 2: 主張（Claim）と自説データのバインド
論文の本文を執筆する際、AIは `docs/data/research-data-index.md` の資料IDを参照し、主張の直後に自説データをエビデンスとして埋め込む。

### Step 3: 質的引用（Blockquote）と解釈のフォーマット
匿名化済みのインタビュー発言や歴史史料テキストを、学術的ブロック引用形式でフォーマットし、その直後に解釈を記述する。

## 成果物
- `.cursorignore`, `.claudeignore`, `.agentsignore`, `.ignore` (AI Ignore設定)
- `data/anonymized/` (PIIマスキング済み安全データ)
- `docs/data/research-data-index.md` (調査資料インベントリ)

