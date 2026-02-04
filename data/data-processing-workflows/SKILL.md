---
name: data-processing-workflows
description: Polibaseのデータ処理ワークフローとパイプラインを説明します。議事録処理、Web scraping、政治家データ収集、話者マッチングなどの処理フロー、依存関係、実行順序を理解する際にアクティベートされます。
---

# Data Processing Workflows（データ処理ワークフロー）

## 目的
Polibaseの各種データ処理ワークフロー、パイプライン、システム設計原則を理解し、正しい順序で処理を実行できるようにします。

## いつアクティベートするか
このスキルは以下の場合に自動的にアクティベートされます：
- `src/minutes_divide_processor/`, `src/web_scraper/`, `src/party_member_extractor/` ディレクトリでの作業時
- ユーザーが「処理フロー」「パイプライン」「ワークフロー」「データ処理」と言った時
- 処理の順序や依存関係に関する質問時
- 議事録処理、スクレイピング、話者マッチングの実装・修正時

## システム設計原則

Polibaseは以下の6つの設計原則に基づいています：

### 1. 政治家情報は政党Webサイトから取得
- 政治家データは政党の公式Webサイトから取得
- 定期的に更新して最新情報を維持
- 名前、役職、選挙区などを構造化して抽出

### 2. 話者と発言内容は議事録から抽出
- 話者名と発言内容を議事録から抽出
- 会話のコンテキストと順序を維持
- `conversations` と `speakers` テーブルに構造化データとして保存

### 3. 話者-政治家マッチングはLLMを活用
- 名前のバリエーションや敬称の処理にLLMを使用
- ルールベース + LLMのハイブリッドアプローチ
- `speakers` と `politicians` の高精度なリンク

### 4. 議員団（Parliamentary Groups）管理
- 議員団は会議内の投票ブロックを表現
- 役職（団長、幹事長など）付きのグループメンバーシップ履歴を追跡
- 提案の投票を個々の政治家とグループの両方にリンク

### 5. 会議メンバー抽出は段階的処理
- `members_introduction_url` から段階的にメンバーを抽出
- 中間データ用のステージングテーブル（`extracted_conference_members`）
- 信頼度スコア付きのLLMベースファジーマッチング
- 最終所属作成前の手動レビュー機能

### 6. データ入力はStreamlit UIから
- 政党メンバーリストURLをWeb UIで管理
- 議事録URLの登録と管理
- 会議メンバー紹介URLの管理
- すべてのデータ入力をユーザーフレンドリーなインターフェースで

## 処理パイプライン

### 標準フロー（PDFから）

```
PDF議事録
  ↓
[1] Minutes Divider
  ↓ 個別の発言に分割
Conversations
  ↓
[2] Speaker Extraction
  ↓ 話者情報を抽出
Speakers
  ↓
[3] Speaker Matching
  ↓ 政治家とマッチング
Linked Conversations
```

#### ステップ1: Minutes Divider
**ファイル:** `src/minutes_divide_processor/`

**処理内容:**
- PDF議事録をLangGraphの状態管理とGemini APIで処理
- 個別の発言に分割して抽出

**入力:** PDF議事録
**出力:** `conversations` テーブルのレコード

#### ステップ2: Speaker Extraction
**ファイル:** `src/extract_speakers_from_minutes.py`

**処理内容:**
- 会話から話者情報を抽出
- 話者レコードを作成

**入力:** `conversations` テーブル
**出力:** `speakers` テーブルのレコード

#### ステップ3: Speaker Matching
**ファイル:** `update_speaker_links_llm.py`

**処理内容:**
- ルールベース + LLMのハイブリッドマッチング
- 会話を話者レコードにリンク

**入力:** `speakers`, `politicians` テーブル
**出力:** リンク済み `conversations`

#### ステップ4: Politician Data Collection
**コマンド:** `sagebase scrape-politicians`

**処理内容:**
- 政党Webサイトから最新の政治家情報を取得

**入力:** `political_parties.members_list_url`
**出力:** `politicians` テーブルのレコード

### Web Scraping フロー（GCS統合）

```
議会Webサイト
  ↓
[1] Web Scraper (--upload-to-gcs)
  ↓ GCSにアップロード
GCS Storage (gs://bucket/...)
  ↓ URI保存
Meetings Table (gcs_pdf_uri, gcs_text_uri)
  ↓
[2] Minutes Divider (--meeting-id)
  ↓ GCSから直接取得
標準フローに合流
```

#### ステップ1: Web Scraper
**ファイル:** `src/web_scraper/`

**処理内容:**
- 議会Webサイトから議事録を抽出
- kaigiroku.netシステムに対応（多くの日本の地方議会で使用）
- JavaScriptベースサイト用にPlaywrightを使用
- `--upload-to-gcs` フラグでGCSに自動アップロード
- GCS URIを `meetings` テーブルに保存

**対応システム:**
- kaigiroku.net（日本の地方議会で広く使用）

**オプション:**
- `--upload-to-gcs`: GCSにアップロード

#### ステップ2: GCS-based Processing
**コマンド:** `sagebase process-minutes --meeting-id <id>`

**処理内容:**
- Minutes Dividerが `--meeting-id` パラメータでGCSからデータを直接取得

#### ステップ3: 以降の処理
標準フロー（話者抽出、話者マッチング）と同じ

### Conference Member Extraction フロー（段階的処理）

```
Conference members_introduction_url
  ↓
[1] Extract Conference Members
  ↓ スクレイピング + LLM抽出
Staging Table (extracted_conference_members: status='pending')
  ↓
[2] Match with Politicians
  ↓ LLMファジーマッチング
Staging Table (status='matched'/'needs_review'/'no_match')
  ↓
[3] Create Affiliations
  ↓ status='matched' のみ処理
politician_affiliations
```

#### ステップ1: Extract Conference Members
**コマンド:** `sagebase extract-conference-members`

**処理内容:**
- 会議URLからメンバー情報をスクレイピング
- Playwright + LLMでメンバー名、役職、政党所属を抽出
- ステージングテーブル `extracted_conference_members` に status='pending' で保存

**入力:** `conferences.members_introduction_url`
**出力:** `extracted_conference_members` (status='pending')

#### ステップ2: Match with Politicians
**コマンド:** `sagebase match-conference-members`

**処理内容:**
- LLMベースのファジーマッチング
- 名前と政党で既存の政治家を検索
- LLMで名前のバリエーションを処理して最適なマッチを決定
- マッチングステータスを更新:
  - `matched` (信頼度 ≥ 0.7)
  - `needs_review` (信頼度 0.5-0.7)
  - `no_match` (信頼度 < 0.5)

**入力:** `extracted_conference_members`, `politicians`
**出力:** `extracted_conference_members` (status更新)

#### ステップ3: Create Affiliations
**コマンド:** `sagebase create-affiliations`

**処理内容:**
- 最終的な政治家-会議の関係を作成
- `matched` ステータスのレコードのみ処理
- 役職付きで `politician_affiliations` にエントリを作成

**入力:** `extracted_conference_members` (status='matched')
**出力:** `politician_affiliations`

## 処理順序のチェックリスト

### 議事録処理の場合
- [ ] **ステップ1**: Minutes Divider で議事録を分割
- [ ] **ステップ2**: Speaker Extraction で話者を抽出
- [ ] **ステップ3**: Speaker Matching で政治家とマッチング
- [ ] **順序厳守**: この順序を変更しないこと

### Web Scrapingの場合
- [ ] **GCS認証**: `gcloud auth application-default login` を実行済み
- [ ] **アップロード**: `--upload-to-gcs` フラグを使用
- [ ] **URI確認**: `meetings` テーブルに `gcs_pdf_uri` / `gcs_text_uri` が保存されているか
- [ ] **処理実行**: `--meeting-id` で処理を実行

### Conference Member Extractionの場合
- [ ] **ステップ1**: `extract-conference-members` でスクレイピング
- [ ] **ステップ2**: `match-conference-members` でマッチング
- [ ] **ステップ3**: `create-affiliations` で所属作成
- [ ] **レビュー**: `needs_review` ステータスのレコードを手動確認

## 追加コンポーネント

### Meeting Management UI
**場所:** `src/interfaces/web/streamlit/`

**機能:**
- URLルーティング付きStreamlitベースWebインターフェース
- 会議、政党、会議、その他の管理

### Party Member Extractor
**場所:** `src/party_member_extractor/`

**機能:**
- LLMベースで政党メンバーリストページから政治家情報を抽出
- Gemini APIでHTMLから構造化データを抽出
- 複数ページのメンバーリストのページネーション対応
- 重複レコード作成を防ぐ重複チェック実装

### Conference Member Extractor
**場所:** `src/conference_member_extractor/`

**機能:**
- 会議メンバーの段階的抽出とマッチング
- 中間データレビュー用ステージングテーブル
- 手動レビュー機能付き信頼度ベースマッチング

## 詳細リファレンス

詳細なデータフロー図と実装ガイドは [reference.md](reference.md) を参照してください。

## ダイアグラム

視覚的なフロー図：
- [Minutes Processing Flow](../../../docs/diagrams/data-flow-minutes-processing.mmd)
- [Speaker Matching Flow](../../../docs/diagrams/data-flow-speaker-matching.mmd)
- [Politician Scraping Flow](../../../docs/diagrams/data-flow-politician-scraping.mmd)
