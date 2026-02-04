---
name: youtube-uploader
description: YouTube Data API v3を使用して動画をYouTubeにアップロードします。このスキルは、(1) Manimで作成した動画のYouTubeへのアップロード、(2) 動画メタデータ（タイトル、説明、タグ）の設定、(3) プライバシー設定（公開、限定公開、非公開）、(4) 予約投稿、(5) プレイリストへの追加に使用します。
---

# YouTube動画アップローダー

YouTube Data API v3を使用して、作成した動画をYouTubeにプログラマティックにアップロードします。

---

## 前提条件

### 初回セットアップ（ユーザーが行う）

以下のセットアップはユーザー自身が行う必要があります。セットアップが完了していない場合は、このスキルの「初回セットアップガイド」セクションを参照するよう案内してください。

1. Google Cloud Consoleでプロジェクトを作成
2. YouTube Data API v3を有効化
3. OAuth 2.0認証情報を作成
4. `credentials.json` をダウンロード

### 依存パッケージ

```bash
pip3 install google-auth-oauthlib google-api-python-client
```

---

## credentials.json の配置場所

**重要**: `credentials.json` は以下の優先順位で自動検索されます。明示的に `--credentials` オプションを指定しなくても、以下の場所に配置されていれば自動的に使用されます。

### 検索優先順位

| 優先度 | 場所 | パス |
|--------|------|------|
| 1 | 明示的指定 | `--credentials /path/to/credentials.json` |
| 2 | プロジェクトディレクトリ | `./credentials.json` |
| 3 | ホームディレクトリ | `~/credentials.json` |
| 4 | 設定ディレクトリ | `~/.config/youtube/credentials.json` |
| 5 | プラグインディレクトリ | `${CLAUDE_PLUGIN_ROOT}/credentials.json` |

### 推奨配置場所

```bash
# 個人用（全プロジェクト共通）- 推奨
~/.config/youtube/credentials.json

# または
~/credentials.json

# プロジェクト固有の認証情報
./credentials.json
```

### 注意事項

- `token.json`（認証トークン）は `credentials.json` と同じディレクトリに自動生成されます
- `.gitignore` に `credentials.json` と `token.json` を追加してください
- 複数の場所に `credentials.json` がある場合、優先度の高い場所のファイルが使用されます

---

## アップロード前の確認事項

動画をアップロードする前に、以下を確認してください：

```
1. 動画ファイルの確認
   - ファイルパスが正しいか
   - MP4形式であるか
   - ファイルが存在するか

2. 認証情報の確認
   - credentials.json が存在するか
   - 初回実行時はブラウザ認証が必要

3. メタデータの準備
   - タイトル（必須）
   - 説明（推奨）
   - タグ（推奨）
   - カテゴリ（デフォルト: 22 = People & Blogs）
   - プライバシー設定（デフォルト: private）
```

---

## 使用方法

### スクリプトの場所

アップロードスクリプトは以下の場所にあります：
`${CLAUDE_PLUGIN_ROOT}/skills/youtube-uploader/scripts/youtube_uploader.py`

### 基本的なアップロード

```bash
python3 ${CLAUDE_PLUGIN_ROOT}/skills/youtube-uploader/scripts/youtube_uploader.py \
  /path/to/video.mp4 \
  --title "動画タイトル" \
  --credentials /path/to/credentials.json
```

### フルオプションでのアップロード

```bash
python3 ${CLAUDE_PLUGIN_ROOT}/skills/youtube-uploader/scripts/youtube_uploader.py \
  /path/to/video.mp4 \
  --title "動画タイトル" \
  --description "動画の詳細な説明文" \
  --tags "manim,アニメーション,解説" \
  --privacy private \
  --category 27 \
  --credentials /path/to/credentials.json
```

### Manimで作成した動画のアップロード例

```bash
# Manimの出力動画をアップロード
python3 ${CLAUDE_PLUGIN_ROOT}/skills/youtube-uploader/scripts/youtube_uploader.py \
  ./media/videos/scene/1080p60/MyScene.mp4 \
  --title "Manimで作成した解説動画" \
  --description "Manim Community ライブラリで作成したアニメーション" \
  --tags "manim,animation,python,math" \
  --privacy unlisted \
  --category 27 \
  --credentials ~/credentials.json
```

---

## コマンドラインオプション

| オプション | 必須 | 説明 | デフォルト |
|------------|------|------|------------|
| `file` | 必須 | アップロードするMP4動画のパス | - |
| `--title` | 必須 | 動画タイトル | - |
| `--description` | 任意 | 動画の説明文 | 空 |
| `--tags` | 任意 | カンマ区切りのタグ | 空 |
| `--privacy` | 任意 | `private`, `unlisted`, `public` | `private` |
| `--category` | 任意 | YouTubeカテゴリID | `22` |
| `--credentials` | 任意 | credentials.jsonのパス | `credentials.json` |
| `--playlist` | 任意 | 追加先プレイリストID | - |
| `--publish-at` | 任意 | 予約投稿日時（ISO 8601形式） | - |

---

## YouTubeカテゴリID

| カテゴリ | ID |
|---------|-----|
| Film & Animation | 1 |
| Autos & Vehicles | 2 |
| Music | 10 |
| Pets & Animals | 15 |
| Sports | 17 |
| Travel & Events | 19 |
| Gaming | 20 |
| People & Blogs | 22 |
| Comedy | 23 |
| Entertainment | 24 |
| News & Politics | 25 |
| Howto & Style | 26 |
| Education | 27 |
| Science & Technology | 28 |

**Manim動画の推奨カテゴリ:**
- 解説・教育動画: `27` (Education)
- 技術デモ: `28` (Science & Technology)
- エンターテイメント: `24` (Entertainment)

---

## 初回セットアップガイド

ユーザーがセットアップ未完了の場合、以下の手順を案内してください。

### ステップ1: Google Cloud Consoleでプロジェクト作成

1. [Google Cloud Console](https://console.cloud.google.com) にアクセス
2. 上部の「プロジェクト選択」→「新しいプロジェクト」
3. プロジェクト名を入力（例: `YouTube-Uploader`）
4. 「作成」をクリック

### ステップ2: YouTube Data API v3を有効化

1. 左メニュー →「APIとサービス」→「ライブラリ」
2. 「YouTube Data API v3」を検索
3. 「有効にする」をクリック

### ステップ3: OAuth 2.0認証情報を作成

1. 「APIとサービス」→「認証情報」
2. 「+ 認証情報を作成」→「OAuth クライアントID」

**同意画面の設定（初回のみ）:**
1. User Type:「外部」を選択
2. アプリ名: `YouTube Uploader`
3. サポートメール: 自分のメールアドレス
4. 「保存して次へ」を繰り返す
5. テストユーザーに自分のGoogleアカウントを追加

**OAuth クライアントIDの作成:**
1. アプリケーションの種類:「デスクトップアプリ」
2. 「作成」→「JSONをダウンロード」
3. ダウンロードしたファイルを `credentials.json` にリネーム

### ステップ4: 依存パッケージのインストール

```bash
pip3 install google-auth-oauthlib google-api-python-client
```

### ステップ5: 初回認証

```bash
python3 youtube_uploader.py test_video.mp4 \
  --title "Test Upload" \
  --credentials credentials.json
```

初回実行時：
1. ブラウザが自動で開く
2. Googleアカウントでログイン
3. 「許可」をクリック
4. `token.json` が自動生成される（以降の認証に使用）

---

## 予約投稿

動画を特定の日時に公開予約できます：

```bash
python3 youtube_uploader.py video.mp4 \
  --title "予約投稿動画" \
  --privacy private \
  --publish-at "2025-02-01T18:00:00Z"
```

**注意:** 予約投稿は `private` または `unlisted` の動画でのみ機能します。

---

## プレイリストへの追加

アップロードと同時にプレイリストに追加：

```bash
python3 youtube_uploader.py video.mp4 \
  --title "プレイリスト用動画" \
  --playlist "PLxxxxxxxxxxxx"
```

プレイリストIDの取得方法：
1. YouTubeで該当プレイリストを開く
2. URLから抽出: `https://www.youtube.com/playlist?list=PLxxxxxxxxxxxx`
3. `list=` の後の部分がプレイリストID

---

## トラブルシューティング

### `credentials.json` が見つからない

```bash
# 正しいパスを指定
python3 youtube_uploader.py video.mp4 \
  --title "Test" \
  --credentials ~/path/to/credentials.json
```

### 権限エラー (403)

1. `token.json` を削除
2. スクリプトを再実行して再認証
3. 「すべてを許可」をクリック

### Invalid value エラー (400)

- `--category` が1-28の範囲か確認
- `--publish-at` がISO 8601形式か確認: `2025-01-15T15:30:00Z`

### アップロードが途中で止まる

- `Ctrl+C` で中断可能
- 再実行で続行される場合あり
- ネットワーク接続を確認

---

## セキュリティ

### 認証情報ファイルの管理

```bash
# .gitignoreに追加
echo "credentials.json" >> .gitignore
echo "token.json" >> .gitignore
```

### 環境変数での管理

```bash
export YOUTUBE_CREDENTIALS_FILE="/path/to/credentials.json"

python3 youtube_uploader.py video.mp4 \
  --title "My Video" \
  --credentials $YOUTUBE_CREDENTIALS_FILE
```

---

## ワークフロー例: Manim動画作成→YouTubeアップロード

```bash
# 1. Manimで動画をレンダリング
uv run manim -qh scene.py MyScene

# 2. 音声を合成（フル版の場合）
python3 combine_final.py

# 3. YouTubeにアップロード
python3 ${CLAUDE_PLUGIN_ROOT}/skills/youtube-uploader/scripts/youtube_uploader.py \
  ./final_output.mp4 \
  --title "Manim解説動画" \
  --description "Manim Community ライブラリで作成" \
  --tags "manim,animation,python" \
  --privacy unlisted \
  --category 27 \
  --credentials ~/credentials.json
```

---

## リファレンス

- [YouTube Data API v3 公式ドキュメント](https://developers.google.com/youtube/v3)
- [動画アップロードAPI](https://developers.google.com/youtube/v3/guides/uploading_a_video)
- [Google OAuth 2.0](https://developers.google.com/identity/protocols/oauth2)
