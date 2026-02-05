---
name: downloading-figma-assets
description: Downloads images, icons, and SVGs from Figma designs. Use when extracting visual assets from Figma for implementation.
---

# Figmaアセットダウンロード

FigmaデザインからPNG画像、SVGアイコン、その他のビジュアルアセットを抽出・ダウンロードする手順。

## 目次

- [Workflow](#workflow)
- [前提条件](#前提条件)
- [方法1: MCP経由でアセットURL取得（推奨）](#方法1-mcp経由でアセットurl取得推奨)
- [方法2: Figma API経由でSVGエクスポート](#方法2-figma-api経由でsvgエクスポート)
- [方法3: スクリーンショットスクリプト](#方法3-スクリーンショットスクリプト)
- [SVGの後処理](#svgの後処理)
- [よくあるアセットタイプ](#よくあるアセットタイプ)
- [トラブルシューティング](#トラブルシューティング)

## Workflow

Copy this checklist:

```
Asset Download Progress:
- [ ] Step 1: アセットタイプを特定
- [ ] Step 2: 取得方法を選択
- [ ] Step 3: アセットをダウンロード
- [ ] Step 4: SVG後処理（必要な場合）
- [ ] Step 5: 出力を確認
```

**Step 1: アセットタイプを特定**

| タイプ | 推奨方法 |
|--------|----------|
| アイコン（SVG）※HTMLに`data-figma-icon-svg`あり | Figma API（方法2）★優先 |
| アイコン（SVG）※`data-figma-asset-url`あり | MCP経由（方法1） |
| 写真・画像 | MCP経由（方法1） |
| イラスト | Figma API（方法2） |
| スクリーンショット | スクリプト（方法3） |

> **⚠️ 重要**: `data-figma-icon-svg` には親ノードIDが指定されている場合があります。
> 複数のSVGパーツを1つのアイコンとしてダウンロードするため、Figma APIでの取得を優先してください。

**Step 2: 取得方法を選択**

- **方法2（優先）**: Figma API - `data-figma-icon-svg`属性がある場合
- **方法1**: MCP経由 - `data-figma-asset-url`属性がある場合
- **方法3**: スクリーンショット - 特定ビューが必要な場合

**Step 3-5**: 選択した方法のセクションに従って実行

If SVG icons appear white on white background, proceed to [SVGの後処理](#svgの後処理).

## 前提条件

- Figma MCP接続が有効
- FIGMA_TOKEN（API経由でエクスポートする場合）

## 方法1: MCP経由でアセットURL取得（推奨）

### Step 1: デザインコンテキスト取得

```bash
mcp__figma__get_design_context(fileKey, nodeId, clientLanguages="html,css")
```

### Step 2: アセットURLの抽出

レスポンスから `https://www.figma.com/api/mcp/asset/` で始まるURLを抽出：

```javascript
// レスポンス例
const imgHome = "https://www.figma.com/api/mcp/asset/4e601326-51bf-43b1-aa59-a0273109c3db";
const imgNotification = "https://www.figma.com/api/mcp/asset/d10837ed-2c6c-4dcd-96c4-b0b9e39efb79";
```

### Step 3: ダウンロードスクリプト

```javascript
const https = require('https');
const fs = require('fs');
const path = require('path');

const assets = {
  'icon-name': 'https://www.figma.com/api/mcp/asset/xxxxx',
  // 他のアセット
};

const outDir = './icons';

function download(name, url) {
  return new Promise((resolve, reject) => {
    const file = fs.createWriteStream(path.join(outDir, name + '.svg'));
    https.get(url, (res) => {
      if (res.statusCode === 302 || res.statusCode === 301) {
        download(name, res.headers.location).then(resolve).catch(reject);
        return;
      }
      res.pipe(file);
      file.on('finish', () => { file.close(); resolve(); });
    }).on('error', reject);
  });
}

async function main() {
  fs.mkdirSync(outDir, { recursive: true });
  for (const [name, url] of Object.entries(assets)) {
    await download(name, url);
    console.log('Downloaded:', name);
  }
}

main();
```

**注意**: MCPアセットURLは実際にはSVG形式で返されることが多い（拡張子に関わらず）。

## 方法2: Figma API経由でSVGエクスポート（★アイコン推奨）

> **この方法を優先する理由**:
> - `data-figma-icon-svg` には**親ノードID**が指定されている場合がある
> - 親ノードを指定することで、複数のSVGパーツを1つのアイコンとして取得可能
> - Figma APIは指定ノード配下の全要素を含むSVGを返す

### Step 1: ノードIDの特定

**HTMLから抽出する場合（推奨）:**

HTMLの `data-figma-icon-svg` 属性にはノードIDが格納されている：

```html
<!-- 単一ノードの例 -->
<span class="icon" data-figma-icon-svg="3428:18627" data-figma-node="3428:18627"></span>

<!-- 親ノードが指定されている例（複数パーツで構成されるアイコン） -->
<div class="icon-container" 
     data-figma-node="2348:3191" 
     data-figma-icon-svg="2348:3191">
  <!-- 内部に複数のSVG要素が含まれる -->
</div>
```

```bash
# HTMLからノードIDを抽出
grep -oP 'data-figma-icon-svg="\K[^"]+' dashboard.html | sort -u
# 出力: 3428:18627, 491:2101, 2348:3191, ...
```

**Figma MCPから取得する場合:**

```bash
mcp__figma__get_metadata(fileKey, nodeId)
```

### Step 2: SVGエクスポートAPI呼び出し

```javascript
const https = require('https');

const TOKEN = process.env.FIGMA_TOKEN;
const FILE_KEY = 'your-file-key';
const NODE_IDS = '123:456,789:012'; // カンマ区切り

const url = `https://api.figma.com/v1/images/${FILE_KEY}?ids=${encodeURIComponent(NODE_IDS)}&format=svg`;

https.get(url, { headers: { 'X-Figma-Token': TOKEN } }, (res) => {
  let data = '';
  res.on('data', chunk => data += chunk);
  res.on('end', () => {
    const response = JSON.parse(data);
    console.log(response.images);
    // { "123:456": "https://...", "789:012": "https://..." }
  });
});
```

**注意**: インスタンスノードやラスター画像を含むノードは`null`が返される場合がある。

## 方法3: スクリーンショットスクリプト

`~/.agents/scripts/html-screenshot/figma-screenshot.js` を使用：

```bash
node figma-screenshot.js --file-key=xxx --node-id=123:456 --token=$FIGMA_TOKEN output.png
```

## SVGの後処理

Figmaからエクスポートされたアイコンには複数の問題が含まれることがある。

### 問題1: アスペクト比の崩れ（⚠️ 重要）

**症状**: アイコンが引き伸ばされて歪む

**原因**: Figma APIが以下の属性を含むSVGを返す：
```xml
<svg preserveAspectRatio="none" width="100%" height="100%" overflow="visible" style="display: block;" ...>
```

| 問題の属性 | 影響 |
|-----------|------|
| `preserveAspectRatio="none"` | アスペクト比を無視して引き伸ばす |
| `width="100%" height="100%"` | 親コンテナに合わせて伸縮 |

**解決**: 固定サイズに修正

```bash
cd icons/
for f in *.svg; do
  # preserveAspectRatio="none" を削除
  sed -i '' 's/ preserveAspectRatio="none"//g' "$f"
  # width="100%" height="100%" を viewBox から計算した値に置換
  # 例: viewBox="0 0 20 20" → width="20" height="20"
  sed -i '' 's/ width="100%" height="100%"//g' "$f"
  # overflow と style も削除
  sed -i '' 's/ overflow="visible"//g' "$f"
  sed -i '' 's/ style="display: block;"//g' "$f"
done
```

**修正例**:
```xml
<!-- Before (問題あり) -->
<svg preserveAspectRatio="none" width="100%" height="100%" overflow="visible" style="display: block;" viewBox="0 0 20 20" ...>

<!-- After (修正後) -->
<svg width="20" height="20" viewBox="0 0 20 20" ...>
```

### 問題2: 白いfill

**症状**: 白背景でアイコンが見えない

**原因**: `fill="var(--fill-0, white)"` を含む

**解決**: currentColorに置換

```bash
cd icons/
for f in *.svg; do
  sed -i '' 's/fill="var(--fill-0, white)"/fill="currentColor"/g' "$f"
done
```

### 問題3: CSS変数のfill

**症状**: SVGの色が変わらない、または透明になる

**原因**: `fill="var(--fill-0, #XXXXXX)"` 形式

**解決**: CSS変数を実際の色に置換

```bash
cd icons/
for f in *.svg; do
  # var(--fill-0, #color) を #color に置換
  sed -i '' 's/fill="var(--fill-0, \([^)]*\))"/fill="\1"/g' "$f"
done
```

### currentColorの利点

```html
<!-- 親要素のcolorを継承 -->
<span style="color: #0b41a0;">
  <svg>...</svg>
</span>
```

## よくあるアセットタイプ

| タイプ | 取得方法 | 形式 | 備考 |
|--------|----------|------|------|
| アイコン（`data-figma-icon-svg`あり） | Figma API export ★ | SVG | 親ノード指定で複数パーツを統合 |
| アイコン（`data-figma-asset-url`あり） | MCP asset URL | SVG | 単一アセットの場合 |
| 写真/画像 | MCP asset URL | PNG/JPG | - |
| イラスト | Figma API export | SVG | - |
| スクリーンショット | figma-screenshot.js | PNG | - |

## トラブルシューティング

| 問題 | 原因 | 解決策 |
|------|------|--------|
| **アイコンが歪む** | `preserveAspectRatio="none"` | 属性を削除、固定サイズに修正 |
| **アイコンが不完全** | 子ノードIDを指定している | `data-figma-icon-svg`の親ノードIDでFigma API取得 |
| SVGが白く表示 | `fill="white"` | `currentColor`に置換 |
| SVGの色がおかしい | `fill="var(--fill-0, ...)"` | CSS変数を実際の色に置換 |
| API exportがnull | ラスター含むノード | MCP asset URLを使用 |
| ダウンロード失敗 | リダイレクト未対応 | 302/301をフォロー |
| トークンエラー | FIGMA_TOKEN未設定 | 環境変数またはオプションで指定 |

### 親ノードIDについて

Figmaのアイコンは複数のレイヤーで構成されることがあります：

```
Circle/Ai (親ノード: 2348:3191) ← data-figma-icon-svg に指定
├── Background (子ノード: 2348:3192)
├── Ellipse (子ノード: 2348:3195)
└── Icon (子ノード: 2348:3196)
```

この場合、親ノードID `2348:3191` をFigma APIに渡すことで、全パーツを含む完全なSVGを取得できます。

## 出力例

```
project/
└── icons/
    ├── home.svg
    ├── notification.svg
    ├── all-courses.svg
    ├── my-courses.svg
    ├── mypage.svg
    ├── todo-plan.svg
    ├── circle-check.svg
    ├── info.svg
    └── forward.svg
```

## 関連スキル

- [converting-figma-to-html](../converting-figma-to-html/SKILL.md): HTML変換
- [extracting-design-tokens](../extracting-design-tokens/SKILL.md): デザイントークン抽出
