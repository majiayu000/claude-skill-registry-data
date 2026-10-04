---
name: playwright-qa
description: Playwright MCP を使ってUIをブラウザで動作確認・テスト・動画録画する。「動作確認して」「テストして」「動画撮って」「Figmaと比較して」「受け入れ条件テストして」などのリクエストに反応する。
tools:
  - Bash
---

# Playwright QA Skill

Playwright MCP を使ってUIのブラウザ動作確認・スクリーンショット比較・動画録画・受け入れ条件テストを行う。

**重要: Playwright は専用のブラウザインスタンスを使うこと。デフォルトブラウザ（Arc等）のプロファイルを使うと、Google アカウントがログアウトされて Slack・Jira 等に再ログインが必要になる。**

---

## 1. dev server URL の特定

以下の優先順位で動作中の dev server URL を特定する。

```bash
# 1. Next.js / Vite 等のプロセスのポートを検出
lsof -i -P | grep LISTEN | grep node

# 2. .env.local / .env の PORT= を確認
grep -E '^PORT=' .env.local .env 2>/dev/null

# 3. package.json の dev スクリプトに --port があるか確認
cat package.json | grep '"dev"'
```

- 見つかったポートを使って `http://localhost:<PORT>` にアクセス
- 見つからなければデフォルト `http://localhost:3000` を試みる
- 接続できなければユーザーに確認する

---

## 2. ログイン手順

開発環境の認証フロー:

1. `browser_navigate` でログインページへ移動
2. `browser_snapshot` で現在の状態を確認
3. メールアドレス欄に入力: `browser_type`
4. パスワード欄に入力
5. ログインボタンをクリック: `browser_click`
6. `browser_snapshot` でログイン後の状態を確認
7. 認証情報が不明な場合はユーザーに確認する

---

## 3. 動作確認フロー

基本的な動作確認の手順:

```
1. browser_navigate        -> 対象ページへ移動
2. browser_snapshot        -> アクセシビリティツリーで構造確認
3. browser_take_screenshot -> 画面キャプチャ
4. browser_click / browser_type -> 操作実行
5. browser_snapshot / browser_take_screenshot -> 結果確認
6. browser_wait_for        -> 非同期処理の完了待ち（必要に応じて）
```

複数ステップの操作は都度スナップショットを撮って状態変化を記録する。

---

## 4. Jira 受け入れ条件テスト

チケット番号（例: VOC-1046）が与えられた場合:

1. **Jira MCP でチケット取得**
   - `mcp__mcp-atlassian__jira_get_issue` でチケット詳細を取得
   - 受け入れ条件（Acceptance Criteria）セクションを抽出

2. **条件を一覧化**
   - 各条件に番号を振り、テスト計画を立てる

3. **Playwright で各条件を検証**
   - 条件ごとにブラウザ操作・スナップショット・スクリーンショットで確認
   - PASS / FAIL を判定

4. **結果をテーブルでレポート**

```markdown
| # | 受け入れ条件 | 結果 | 備考 |
|---|------------|------|------|
| 1 | ○○ができる | PASS | スクリーンショット確認済み |
| 2 | △△が表示される | FAIL | エラーメッセージが表示 |
```

---

## 5. Figma デザイン比較

Figma URL またはノードIDが与えられた場合:

1. **Figma MCP でスクリーンショット取得**
   - `mcp__figma__get_screenshot` でデザインキャプチャ
   - `mcp__figma__get_design_context` でデザイン詳細を取得

2. **Playwright で実装画面を撮影**
   - 同じコンポーネント・ページを `browser_take_screenshot` で撮影

3. **差異をコメント**
   - 色・余白・フォントサイズ・レイアウトの差異を具体的に指摘
   - 「デザイン通り」または「要修正」の判定を行う

---

## 6. 動画録画

動画録画が必要な場合:

1. **録画スクリプトを `/tmp/pw-record/` に作成**

```bash
mkdir -p /tmp/pw-record

cat > /tmp/pw-record/record.mjs << 'EOF'
import { chromium } from 'playwright';

const outputDir = '/tmp/pw-record';
const browser = await chromium.launch({ headless: false });
const context = await browser.newContext({
  recordVideo: {
    dir: outputDir,
    size: { width: 1280, height: 720 }
  }
});

const page = await context.newPage();

// --- 操作を記述 ---
await page.goto('http://localhost:3000');
// await page.click('...');
// await page.fill('...', '...');
// ----------------

await page.waitForTimeout(2000);
await context.close();
await browser.close();

console.log('録画完了:', outputDir);
EOF

npx playwright install chromium 2>/dev/null
node /tmp/pw-record/record.mjs
```

2. **webm -> mp4 変換してデスクトップに保存**

```bash
WEBM_FILE=$(ls /tmp/pw-record/*.webm | head -1)
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
OUTPUT="$HOME/Desktop/recording_${TIMESTAMP}.mp4"

ffmpeg -i "$WEBM_FILE" -c:v libx264 -preset fast "$OUTPUT" 2>/dev/null && \
  echo "保存完了: $OUTPUT" || \
  (cp "$WEBM_FILE" "$HOME/Desktop/recording_${TIMESTAMP}.webm" && \
   echo "保存完了 (webm): $HOME/Desktop/recording_${TIMESTAMP}.webm")
```

3. 録画ファイルのパスをユーザーに報告する

---

## Tips

- `browser_snapshot` はインタラクティブ要素のロール・名前・状態を返すため、クリック対象の特定に活用する
- `browser_console_messages` で JS エラーを確認できる
- `browser_network_requests` で API リクエスト・レスポンスを確認できる
- 操作が見つからない場合は `browser_evaluate` で DOM を直接調査する
- ヘッドレスモードでは動画録画できないため、録画時は `headless: false` を使う

## 7. 後処理

動作確認・テスト完了後、以下のクリーンアップを必ず実行する:

1. **スクリーンショットの削除**: 作業中に保存した `.png` / `.jpeg` ファイルを削除
2. **Playwright ログの削除**: `.playwright-mcp/` ディレクトリを削除
3. **ブラウザを閉じる**: `browser_close` でブラウザインスタンスを終了

```bash
# スクリーンショット削除
rm -f *.png *.jpeg

# Playwright MCP のログ削除
rm -rf .playwright-mcp/
```

---

## 注意事項

- Playwright は独自のブラウザインスタンスを起動する。**絶対にデフォルトブラウザのプロファイルを共有しないこと**
- 録画スクリプトでは `chromium.launch()` を使い、Arc や Chrome のユーザープロファイルは指定しない
- テスト完了後は必ず「7. 後処理」を実行する
