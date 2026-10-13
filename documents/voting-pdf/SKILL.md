---
name: voting-pdf
description: 【川崎版から継承・新宿区では未対応】川崎市議会の議決結果PDFから会派賛否データを抽出し、DBと比較する。議決結果の登録チェックや新規定例会の賛否データ取り込み時に使う。
---

# 議決結果PDF読み取りスキル

> **新宿区では使わない。** このスキルは川崎市議会の PDF 形式を前提にしている。新宿区の会派賛否は「議案の概要と審議結果」PDF（`pdftotext -bbox` で会派列の座標を確認）と会議録（kaigiroku tenant 211）から取る。手順は [docs/20260925_1330_会派賛否データ投入計画.md](../../../docs/20260925_1330_会派賛否データ投入計画.md) と `packages/seed/main/faction-stances-r8-1-data.ts` を参照。

川崎市議会の公式サイトで公開される議決結果PDF（Excel→PDF形式）からテーブルデータを抽出し、本番DBの `faction_stances` と突合する。

## 前提

- Python + `pdfplumber` ライブラリを使用（`pip install pdfplumber`）
- Windows環境では `PYTHONIOENCODING=utf-8` が必須
- PDFは `WebFetch` で取得すると自動保存される（バイナリ読み取りは不可なので `pdfplumber` でパースする）

## PDFの種類と取得先

川崎市議会の議決結果ページ（例: `https://www.city.kawasaki.jp/980/page/0000XXXXXX.html`）には以下のPDFがリンクされている:

| PDF | 内容 | ファイル名パターン |
|---|---|---|
| 市長提出議案 | 第1号〜第N号 | `0318sityou.pdf` |
| 動議 | 動議第N号 | `0318dougi.pdf` |
| 附帯決議案 | 附帯決議案 | `0318hutaiketugian.pdf` |
| 意見書案 | 意見書案第N号 | `0318ikensyoan.pdf` |
| 請願 | 請願第N号 | `0318seigan.pdf` |

PDFのURLは `WebFetch` でページ内のリンクを抽出して特定する。

## テーブル構造

### 市長提出議案・意見書案・請願（14列）

```
[番号, 件名, 議決年月日, 議決結果, 自民党, みらい, 公明党, 共産党, 維新, 無所属×5]
```
- 会派賛否は **index 4〜8**（自民, みらい, 公明, 共産, 維新）

### 動議・附帯決議案（13列、番号列なし）

```
[件名, 議決年月日, 議決結果, 自民党, みらい, 公明党, 共産党, 維新, 無所属×5]
```
- 会派賛否は **index 3〜7**（自民, みらい, 公明, 共産, 維新）

## 抽出コード例

```python
import pdfplumber

PYTHONIOENCODING=utf-8  # 環境変数として設定すること

def extract_stances_from_sityou(pdf_path):
    """市長提出議案PDF（14列）から会派賛否を抽出"""
    results = {}
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            for table in page.extract_tables():
                for row in table:
                    if (row[0] and row[0].replace('\n','').startswith('第')
                        and row[3] and row[3] not in ['議決結果']):
                        bn = row[0].replace('\n','')
                        results[bn] = {
                            'jimin':  row[4].replace('\n','') if row[4] else '-',
                            'mirai':  row[5].replace('\n','') if row[5] else '-',
                            'komei':  row[6].replace('\n','') if row[6] else '-',
                            'kyosan': row[7].replace('\n','') if row[7] else '-',
                            'ishin':  row[8].replace('\n','') if row[8] else '-',
                        }
    return results

def extract_stances_from_dougi_or_hutai(pdf_path, keyword, bill_number):
    """動議・附帯決議PDF（13列、番号列なし）から会派賛否を抽出"""
    results = {}
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            for table in page.extract_tables():
                for row in table:
                    if (row[0] and keyword in row[0]
                        and row[2] and row[2] in ['否決', '原案可決']):
                        results[bill_number] = {
                            'jimin':  row[3].replace('\n','') if row[3] else '-',
                            'mirai':  row[4].replace('\n','') if row[4] else '-',
                            'komei':  row[5].replace('\n','') if row[5] else '-',
                            'kyosan': row[6].replace('\n','') if row[6] else '-',
                            'ishin':  row[7].replace('\n','') if row[7] else '-',
                        }
    return results

def extract_stances_from_ikensyo_or_seigan(pdf_path, prefix):
    """意見書案・請願PDF（14列）から会派賛否を抽出。prefixで議案番号に接頭辞を付与"""
    results = {}
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            for table in page.extract_tables():
                for row in table:
                    if (row[0] and row[0].replace('\n','').startswith('第')
                        and row[3] and row[3] not in ['議決結果']):
                        bn = prefix + row[0].replace('\n','')
                        if bn not in results:
                            results[bn] = {
                                'jimin':  row[4].replace('\n','') if row[4] else '-',
                                'mirai':  row[5].replace('\n','') if row[5] else '-',
                                'komei':  row[6].replace('\n','') if row[6] else '-',
                                'kyosan': row[7].replace('\n','') if row[7] else '-',
                                'ishin':  row[8].replace('\n','') if row[8] else '-',
                            }
    return results
```

## DB比較の手順

1. `WebFetch` で議決結果ページのPDFリンクを取得
2. 各PDFを `WebFetch` でダウンロード（自動保存される）
3. `pdfplumber` で会派賛否を抽出
4. `db-access` スキルに従い本番DBの `faction_stances` を取得
5. PDF側の `賛成/反対` → DB側の `for/against` にマッピングして突合

```python
stance_map = {'賛成': 'for', '反対': 'against'}
```

## 会派マスタ（factions テーブル）

| name | display_name | 列ヘッダー |
|---|---|---|
| jimin | 自由民主党川崎市議会議員団 | 自民党 |
| mirai | みらい川崎市議会議員団 | みらい |
| komei | 公明党川崎市議会議員団 | 公明党 |
| kyosan | 日本共産党川崎市議会議員団 | 共産党 |
| ishin | あしたの川崎・日本維新の会川崎市議会議員団 | 川崎・維新 |

## 注意事項

- ヘッダー行は各ページに繰り返し出現するため、データ行だけをフィルタすること
- `\n` が改行として含まれるので `.replace('\n','')` が必要
- 報告（報告第N号）には賛否がないため比較対象外
- 人事案件（選任・任命・推薦）はPDFに賛否が載る場合と載らない場合がある
