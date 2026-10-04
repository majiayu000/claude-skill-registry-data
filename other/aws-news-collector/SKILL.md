---
name: aws-news-collector
description: >
  AWSの最新情報を公式RSSフィード・ブログ・コミュニティサイトから網羅的に収集し、
  カテゴリ別に日本語で要約・リンク付きで出力するスキル。
  AWS Community Builder活動に必要な情報収集を一括で実施し、ブログネタ候補も提案する。
  Use when: (1) AWSの最新ニュースを知りたい, (2) 今週のAWSアップデートをまとめたい,
  (3) AWSの新サービスや機能追加を確認したい, (4) ブログネタを探したい,
  (5) AWS Community Builder活動の情報収集をしたい, (6) 特定AWSサービスの最新動向を調べたい,
  (7) re:Inventや重要イベントの発表を追いたい, (8) AWS障害情報を確認したい。
  このスキルは「AWS 最新情報」「AWS ニュース」「AWS アップデート」「今週のAWS」
  「AWSブログ」「What's New」などのキーワードで呼び出す。
---

# AWS News Collector

AWS Community Builderとしての継続的な情報発信を支えるために、AWSの最新情報を網羅的に収集し、
わかりやすく要約してリンク付きで出力する情報収集特化スキル。

## 引数

スキル呼び出し時に以下の引数を受け取る（すべてオプション）：

- **days**: 取得する日数（デフォルト: 7）。例: `aws-news-collector 3` で過去3日分
- **category**: 特定カテゴリのみ取得。指定可能な値:
  `all` | `new-services` | `updates` | `security` | `ai-ml` | `containers` | `serverless` | `japan` | `incidents` | `community`
- **focus**: 特に注目したいサービス名。例: `focus:bedrock`, `focus:lambda,ecs`

## 実行手順

このスキルが呼び出されたら、以下の手順を**そのまま順番に**実行する。

### Step 1: 引数の解析

ユーザーの入力から `days`, `category`, `focus` を解析する。
指定がなければデフォルト値（days=7, category=all, focus=なし）を使う。

### Step 2: RSSフィードの並列取得

WebFetchツールを使って、以下のフィードグループから**並列で**最新記事を取得する。
取得対象のフィード一覧は [references/feeds.md](references/feeds.md) を参照。

並列取得は**3グループに分けて**実行する（1回のツール呼び出しで複数URLを取得）：

**グループ1: コアフィード（毎回必須）**
- AWS News Blog RSS
- AWS What's New RSS
- AWS Japan Blog RSS

**グループ2: サービス別ブログ**
- Architecture, Compute, Security, Database, DevOps, ML, Containers, Serverless 各Blog RSS

**グループ3: コミュニティ・障害情報**
- AWS Open Source Blog RSS
- AWS Service Health Dashboard RSS
- AWS Startup Blog RSS

各フィードはXML形式で返ってくるため、`<item>` タグ内の `<title>`, `<link>`, `<pubDate>`, `<description>` を解析する。

`days` 引数で指定された日数以内の記事のみを抽出する。

### Step 3: 記事の分類

取得した全記事を以下のカテゴリに分類する。1つの記事が複数カテゴリに該当する場合は、最も関連性の高いカテゴリに分類する。

| カテゴリ | 判定基準 |
|---------|---------|
| 新サービス発表 | タイトルに「Announcing」「launches」「introduces」「new」を含む |
| 機能アップデート | タイトルに「now supports」「adds」「updates」「enhanced」を含む |
| セキュリティ | Security Blog由来、またはセキュリティ関連キーワード |
| AI/ML | ML Blog由来、Bedrock/SageMaker/Amazon Q/Generative AI関連 |
| コンテナ | Containers Blog由来、ECS/EKS/Fargate関連 |
| サーバーレス | Serverless Blog由来、Lambda/Step Functions/API Gateway関連 |
| 日本関連 | Japan Blog由来、日本リージョン・日本語記事 |
| 障害情報 | Health Dashboard由来 |
| コミュニティ | Open Source Blog、re:Post由来 |
| その他 | 上記に該当しないもの |

`category` 引数が指定されている場合は、該当カテゴリのみ出力する。

### Step 4: focusフィルタリング

`focus` 引数が指定されている場合、タイトルと説明文に該当サービス名を含む記事にハイライトマーク（★）を付ける。フィルタリングで除外はしない（ハイライトのみ）。

### Step 5: 出力の生成

以下のフォーマットで日本語出力を生成する：

```
# AWS最新情報レポート
**期間**: {開始日} 〜 {終了日}（過去{days}日間）
**取得日時**: {現在日時}
**総記事数**: {件数}

---

## 新サービス発表
| # | タイトル | 日付 | リンク |
|---|---------|------|-------|
| 1 | [タイトルの日本語要約] | YYYY-MM-DD | [リンク] |

## 機能アップデート
...（同様のテーブル形式）

## AI/ML
...

## セキュリティ
...

（以下、記事があるカテゴリのみ表示）

---

## 注目トレンド
直近の記事群から読み取れる3〜5つのトレンドを箇条書きで解説。
- **トレンド1**: [1-2文の解説]
- **トレンド2**: ...

---

## ブログネタ候補（Community Builder活動向け）
今回の最新情報から、技術ブログ記事にしやすいトピックを5つ提案。

| # | ネタ | 種類 | 難易度 | 想定PV | 元記事 |
|---|------|------|--------|--------|--------|
| 1 | [タイトル案] | 速報/ハンズオン/比較検証 | ★〜★★★ | 高/中/低 | [元記事リンク] |

各ネタには以下を添える：
- なぜ今書くべきか（タイミングの理由）
- 想定読者
- 記事の骨子（3-4行）

---

## 参考リンク集
- AWS News Blog: https://aws.amazon.com/blogs/aws/
- AWS What's New: https://aws.amazon.com/new/
- AWS Japan Blog: https://aws.amazon.com/jp/blogs/news/
- Last Week in AWS: https://www.lastweekinaws.com/
- AWS re:Post: https://repost.aws/
```

### Step 6: WebSearchで補完

RSSフィードだけでは拾えない情報を補完するため、以下のWebSearchクエリを実行する：

```
AWS new service announcement {current_month} {current_year}
AWS {focus_service} updates {current_year}  （focus指定時のみ）
```

検索結果からRSSに含まれていない重要な情報があれば、レポートに追記する。

### Step 7: Last Week in AWSの確認（days >= 7の場合）

`days` が7以上の場合、Last Week in AWS（https://www.lastweekinaws.com/） のトップページをWebFetchで確認し、最新のニュースレター要約があれば「コミュニティの声」セクションとして追記する。

## Pythonスクリプトによる高速取得（オプション）

手動でのWebFetch並列取得が遅い場合や、定期実行したい場合は、バンドルされたPythonスクリプトを使える：

```bash
python {skill_dir}/scripts/fetch_aws_news.py --days 7 --json
```

スクリプトの詳細は [scripts/fetch_aws_news.py](scripts/fetch_aws_news.py) を参照。
出力されたJSONを読み込んで、Step 5の形式で整形する。

## 出力品質の基準

- 全てのタイトルは日本語に翻訳して要約する（原文が日本語の場合はそのまま）
- 各記事には必ずリンクを付ける
- 日付は `YYYY-MM-DD` 形式で統一する
- 同一記事が複数フィードに出現した場合は重複排除する
- 記事数が多い場合（50件超）は、各カテゴリ上位10件に絞り「他N件」と表記する

## 活用のヒント

このスキルの出力は、以下のスキルと連携して活用できる：
- `aws-community-builder`: 活動計画全体の中で、情報収集フェーズとして使う
- `technical-writing-skill` / `tech-blog-quality-review-skill`: ブログネタ候補を記事化する際に使う
- `marp-slides`: 収集した情報をLT資料にまとめる際に使う
