---
name: chromium-desktop
description: |
  GUIデスクトップ上のChromiumブラウザをxdotool/wmctrl/xclipで操作する。
  Use when the user wants Claude to control a visible Chromium browser window on the desktop,
  navigate to URLs, interact with pages, or take screenshots of the browser.
  Triggers: "Chromiumを操作して", "ブラウザで開いて", "chromium-desktop", "GUIブラウザ操作",
  "デスクトップでブラウザを開いて", "画面に表示しながらブラウザを操作"
---

# chromium-desktop

GUIデスクトップ上のChromiumをCLIツール（xdotool/wmctrl/xclip/scrot）で操作するスキル。

## 必要ツール

```bash
sudo apt-get install -y wmctrl xdotool xclip scrot
```

## 基本ワークフロー

### 1. Chromiumを起動

```bash
DISPLAY=:1 chromium-browser --new-window "https://example.com" &
sleep 3
DISPLAY=:1 wmctrl -l | grep -i chromium
```

### 2. ウィンドウをフォーカス

```bash
DISPLAY=:1 wmctrl -a "ページタイトル - Chromium"
```

### 3. URLナビゲーション

**ASCII URLの場合（xdotool type）:**
```bash
DISPLAY=:1 xdotool key ctrl+l
sleep 0.3
DISPLAY=:1 xdotool type --clearmodifiers "https://example.com"
sleep 0.3
DISPLAY=:1 xdotool key Return
```

**日本語・特殊文字を含むURLの場合（xclip経由）:**
```bash
echo -n "https://ja.wikipedia.org/wiki/東京都" | DISPLAY=:1 xclip -selection clipboard
DISPLAY=:1 xdotool key ctrl+l
sleep 0.3
DISPLAY=:1 xdotool key ctrl+a
DISPLAY=:1 xdotool key ctrl+v
sleep 0.3
DISPLAY=:1 xdotool key Return
```

### 4. スクリーンショットで確認

```bash
sleep 3
DISPLAY=:1 scrot /tmp/screenshot.png
# Read ツールで画像ファイルを読み込み、内容を目視確認する
```

## 重要なコツ（ハマりやすい落とし穴）

### コマンドは1行ずつ実行する
`&&` で繋ぐと `DISPLAY=:1` が後続コマンドに正しく渡らないことがある。
Bashツール呼び出しを分けるか、改行区切りで記述する。

```bash
# NG: 失敗することがある
DISPLAY=:1 xdotool key ctrl+l && sleep 0.3 && DISPLAY=:1 xdotool type "url"

# OK
DISPLAY=:1 xdotool key ctrl+l
sleep 0.3
DISPLAY=:1 xdotool type --clearmodifiers "url"
```

### 日本語入力は必ずxclip経由
`xdotool type` は日本語・マルチバイト文字で文字化け・欠落が発生する。
必ず `xclip -selection clipboard` → `ctrl+v` 貼り付けを使う。

### xclipのパイプ時はDISPLAY指定を忘れない
```bash
# NG
DISPLAY=:1 echo -n "text" | xclip -selection clipboard

# OK
echo -n "text" | DISPLAY=:1 xclip -selection clipboard
```

### sleepで待機を入れる
- キー操作間: `sleep 0.3`
- ページ遷移後の確認: `sleep 3`

## よく使うキー操作

```bash
DISPLAY=:1 xdotool key ctrl+l      # アドレスバーにフォーカス
DISPLAY=:1 xdotool key ctrl+t      # 新規タブ
DISPLAY=:1 xdotool key ctrl+w      # タブを閉じる
DISPLAY=:1 xdotool key ctrl+r      # リロード
DISPLAY=:1 xdotool key ctrl+f      # ページ内検索
DISPLAY=:1 xdotool key Return      # Enter
DISPLAY=:1 xdotool key Escape      # Escape
DISPLAY=:1 xdotool key space       # 下スクロール（1ページ分）
DISPLAY=:1 xdotool key ctrl+End    # ページ最下部へ
DISPLAY=:1 xdotool key ctrl+Home   # ページ最上部へ
```

## 座標クリック

スクリーンショットで座標を確認してからクリックする。

```bash
DISPLAY=:1 xdotool mousemove 960 400
DISPLAY=:1 xdotool click 1
```

## playwright-cli との使い分け

| 用途 | 推奨 |
|---|---|
| GUIで見せながら操作 | chromium-desktop（このスキル） |
| 自動テスト・スクレイピング | playwright-cli スキル |
| headlessで高速実行 | playwright-cli スキル |
