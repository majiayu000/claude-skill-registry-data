---
name: aws-community-builder
description: >
  AWS Community Builder（AI Engineeringカテゴリ）としての活動を包括的に支援するスキル。
  最新AWS情報のキャッチアップ、技術ブログネタ提案、活動計画策定、継続審査対策を提供。
  Use when: (1) AWS最新情報をキャッチアップしたい, (2) 技術ブログのネタを探したい,
  (3) Community Builder活動の計画・振り返りをしたい, (4) LT・登壇ネタを考えたい,
  (5) 継続審査に向けた活動実績を整理したい
---

# AWS Community Builder Activity Support

AI Engineering カテゴリで選出された AWS Community Builder の活動を包括的に支援するスキル。

## 起動時アクション

このスキルが呼び出されたら、以下を順番に実行する：

### Step 1: 今やるべきことダッシュボード

現在の日付から逆算して、以下のタイムラインに基づき「今すぐやるべきこと」を表示する。

**年間タイムライン（重要イベント）：**

| 時期 | イベント | アクション |
|------|---------|-----------|
| 1-2月 | 新年度 Community Builder 選出発表 | 新メンバーへの歓迎・ネットワーキング |
| 3-4月 | AWS Summit シーズン開始 | CFP提出、登壇準備、参加計画 |
| 5-6月 | 中間期 | 活動実績の棚卸し、ブログ本数確認 |
| 7-8月 | re:Invent CFP 締切期 | re:Invent 登壇応募、旅行計画 |
| 9-10月 | 更新審査準備期 | 実績まとめ、不足活動の補完 |
| 11-12月 | AWS re:Invent / 更新申請期 | re:Invent参加、更新申請書作成・提出 |

### Step 2: AWS最新情報キャッチアップ

RSSフィードから最新情報を取得し、AI Engineering カテゴリに特に関連する情報をハイライトする。
詳細は [references/rss-feeds.md](references/rss-feeds.md) を参照。

**優先フィード（AI Engineering向け）：**
1. AWS Machine Learning Blog - 最重要
2. AWS Blog（メイン） - 新サービス発表
3. What's New with AWS - 全般的な新着情報
4. AWS Japan Blog - 日本語での情報
5. 週刊AWS - 週次まとめ
6. AWS Developer Blog - 開発者向け情報

WebSearchツールを使って以下のクエリで最新情報を検索する：
- `AWS new service announcement {current_month} {current_year}`
- `AWS AI ML new features {current_month} {current_year}`
- `Amazon Bedrock updates {current_year}`
- `Amazon SageMaker updates {current_year}`
- `AWS generative AI {current_year}`

### Step 3: ブログネタ提案

AI Engineering カテゴリに適したブログネタを提案する。詳細は [references/blog-ideas.md](references/blog-ideas.md) を参照。

### Step 4: 活動サマリー & 次のアクション

ユーザーに以下を確認し、具体的な次のアクションを提示する：
- 今月のブログ執筆本数
- 直近の登壇予定
- コミュニティ活動の状況

---

## 継続審査（Renewal）対策

### 更新に必要な実績

AWS Community Builder の継続には **毎年の再申請** が必要。以下が評価される：

1. **コンテンツ発信（最重要）**
   - 技術ブログ記事（年間最低6-8本推奨、理想は月2本以上）
   - 動画コンテンツ（YouTube、勉強会録画）
   - OSS コントリビューション

2. **登壇・プレゼンテーション**
   - JAWS-UG / コミュニティ勉強会でのLT
   - AWS Summit / re:Invent での登壇
   - 社内外の勉強会開催

3. **コミュニティ参加**
   - Community Builders Slack での活動
   - 週次ウェビナーへの参加
   - 他メンバーのコンテンツへのフィードバック
   - JAWS-UG などのユーザーグループ参加

4. **英語での活動（加点要素）**
   - 英語ブログ記事（dev.to、Medium など）
   - 国際的なディスカッションへの参加

### 年間活動目標（推奨）

| 活動 | 最低ライン | 推奨 | ストレッチ |
|------|-----------|------|-----------|
| ブログ記事 | 6本/年 | 12本/年 | 24本/年 |
| 登壇・LT | 2回/年 | 4回/年 | 8回/年 |
| コミュニティイベント参加 | 4回/年 | 8回/年 | 12回/年 |
| OSS貢献 | - | 2件/年 | 6件/年 |

---

## AI Engineering ブログネタ生成

### ネタ発見フレームワーク

**1. 新サービス速報型（最もPV稼ぎやすい）**
- AWSの新サービス・新機能を触ってみた系
- 「Amazon Bedrock に○○が追加されたので試してみた」
- 「SageMaker の新機能 ○○ を使ってみた」

**2. ハンズオン・チュートリアル型（継続的にPV稼げる）**
- 「Amazon Bedrock + Lambda でサーバーレスAIアプリを作る」
- 「SageMaker でカスタムモデルをデプロイする完全ガイド」
- 「Step Functions + Bedrock でAIワークフローを構築」

**3. 比較・検証型（技術力アピール）**
- 「Bedrock vs Azure OpenAI：レスポンス速度比較」
- 「SageMaker vs Vertex AI：MLOpsパイプライン比較」
- 「Claude on Bedrock vs 直接API：コスト・パフォーマンス比較」

**4. アーキテクチャ・設計型（上級者向け）**
- 「RAGアプリケーションのAWSアーキテクチャベストプラクティス」
- 「マルチモーダルAIアプリのサーバーレス設計パターン」
- 「AI Agent のための AWS インフラ設計」

**5. 業務改善・実践型（共感を得やすい）**
- 「社内ナレッジベースを Amazon Kendra + Bedrock で構築した話」
- 「コードレビューを Amazon CodeGuru + Bedrock で自動化」
- 「AWSコスト最適化にAIを活用する方法」

**6. トラブルシューティング型（検索流入に強い）**
- 「Bedrock のスロットリングエラー対策まとめ」
- 「SageMaker エンドポイントのコスト削減テクニック」
- 「Lambda + Bedrock でタイムアウトする場合の対処法」

### AI Engineering 注目サービス（2025-2026）

ブログネタの中心となるAWSサービス：

- **Amazon Bedrock** - フルマネージド基盤モデルサービス（最重要）
- **Amazon SageMaker** - MLモデルの構築・トレーニング・デプロイ
- **Amazon Q** - AIアシスタント（Developer / Business）
- **Amazon CodeWhisperer** → Amazon Q Developer
- **AWS Step Functions** - AIワークフローオーケストレーション
- **Amazon Kendra** - インテリジェント検索
- **Amazon Lex** - 会話型AI
- **Amazon Comprehend** - 自然言語処理
- **Amazon Rekognition** - 画像/動画分析
- **Amazon Textract** - ドキュメント処理
- **Amazon Transcribe** - 音声テキスト変換
- **Amazon Polly** - テキスト音声変換
- **AWS Trainium / Inferentia** - AIチップ
- **PartyRock** - ノーコード生成AIアプリ構築

---

## 特典の活用

Community Builder として提供される特典を最大限活用する：

| 特典 | 活用方法 |
|------|---------|
| AWS クレジット ($500-$1000) | 新サービスの検証・ブログネタ作成に使用 |
| 認定試験バウチャー | AWS認定取得でプロフィール強化 |
| 新サービス早期アクセス | 速報記事の執筆に活用 |
| Slack ワークスペース | ネットワーキング・情報交換 |
| re:Invent ディスカウント | 現地参加でネタ収集・登壇 |
| メンターシップ | コンテンツ品質向上・キャリア相談 |

---

## 関連リソース

- [RSSフィード一覧](references/rss-feeds.md) - AWS最新情報を取得するためのフィード一覧
- [ブログアイデア集](references/blog-ideas.md) - AI Engineering カテゴリ向けブログネタの詳細リスト
- [活動トラッカー](references/activity-tracker.md) - 年間活動実績の記録テンプレート
- [更新申請ガイド](references/renewal-guide.md) - 継続審査の申請書作成ガイド

---

## 公式リンク

- [AWS Community Builders 公式](https://aws.amazon.com/developer/community/community-builders/)
- [AWS Builder Center](https://builder.aws.com/community/community-builders)
- [AWS What's New](https://aws.amazon.com/new/)
- [AWS ブログ](https://aws.amazon.com/blogs/)
- [JAWS-UG](https://jaws-ug.jp/)
