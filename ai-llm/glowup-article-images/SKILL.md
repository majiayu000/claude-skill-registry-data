---
name: glowup-article-images
description: "產生 Glow Up 保養專欄文章的封面圖（assets/articles/*.webp）。務必在使用者提到「文章配圖」「封面圖」「生圖」「幫這篇文章配一張圖」，或新增文章卻沒有 image 欄位時觸發，引導 Claude Code 用專案自己的 Maxora 生圖工具產生跟現有文章一致風格的圖，而不是因為找不到圖片生成工具就卡住或叫使用者自己想辦法。"
---

# Glow Up 文章封面圖生成

這個專案有自己的生圖 API 可以用（**Maxora**），憑證跟一支小工具都已經放在專案裡了，
**不需要任何額外的 MCP 圖片生成工具**——過去發生過「Claude Code 換了 session/帳號後
找不到生圖工具，就以為這個能力不見了」的情況，其實只是沒人把用法寫進專案本身。

## 憑證在哪裡

`.env` 裡的 `CF_ID` / `CF_SECRET`（Cloudflare Access service token，不是一般 API Key）。
如果 `.env` 裡這兩個值是空的，去 `/Users/eugeneyu/Desktop/Content Farm/Old_Content_Farm/.env`
抄一份過來（同一組憑證，這個專案借用 Old_Content_Farm 原本申請的額度）。
完整 API 說明（非同步模式、多圖合成、參數表、錯誤碼）在
`/Users/eugeneyu/Desktop/Content Farm/Old_Content_Farm/API-USAGE.md`。

## 怎麼用

專案根目錄已經有 `generate_article_image.py`，直接呼叫（**用 `/usr/bin/python3`**，
因為 anaconda 預設的 python3 沒裝 `python-dotenv`；`requests`/`dotenv` 兩個套件
`/usr/bin/python3` 都已經有，不需要額外安裝）：

```bash
/usr/bin/python3 generate_article_image.py "<英文 prompt>" assets/articles/<article-id>.webp \
  --negative_prompt "text, logo, watermark, letters, typography"
```

- 輸出檔名慣例：跟文章 `id` 同名（`assets/articles/<id>.webp`），也可以取更描述性的名字
  （現有文章有兩種都有，例如 `serum-am-pm-guide` 這篇的圖檔其實叫
  `serum-am-pm-skincare.webp`，只要 `articles.json` 的 `image` 欄位指對就好）。
- 預設 `--size 1:1`（1024×1024），跟目前所有文章封面圖尺寸一致，不要改。
- 生一張大約需要 10~30 秒（同步阻塞），不需要用非同步模式。

## Prompt 怎麼寫

### 基本規則（不分風格都要守）

- **英文 prompt**，效果比中文好。
- **主題是產品本身的意象合成圖**，不是人物、不是品牌商標、不是任何真實品牌的包裝設計——
  瓶罐/管子/盒子上的字樣要嘛留白、要嘛是無法辨識的假字，**絕對不要寫出真實品牌名稱**
  （這個網站評比的是各品牌真實商品，封面圖只是文章主題的意象圖，扯上特定品牌會有商標
  疑慮，也會誤導讀者以為那罐圖就是某品牌產品）。
- 攝影風格關鍵字打底：`professional studio product photography`、`soft shadows`。
- 用 2~4 個同類商品並排或稍微錯落的構圖（呼應文章「比較 N 款」的性質），不要只放單一
  瓶罐（除非文章主題就是單一產品類型且不強調比較）。
- **這個生圖模型文字渲染不可靠**，瓶身標籤只要寫了看起來像字的東西，常會生出無法辨識
  的亂碼假字（不是清晰的品牌字，但看起來「壞掉」）。除了 prompt 裡寫
  `blank unreadable labels` / `plain blank white label, no text, no logo`，
  **一定要加 `--negative_prompt "text, logo, watermark, letters, typography"`**
  來降低機率。如果目視檢查發現亂碼很明顯，就重生一張（可以換 `--seed`）。
  這個限制也代表：**不要嘗試用生圖做「條列式圖解」「表格圖解」這種需要精準文字/
  勾選符號的資訊圖**——AI 生圖畫不出乾淨的文字排版，做出來只會是看起來壞掉的圖。
  如果之後真的要那種效果，得另外做 HTML/CSS 版型疊圖（背景用生圖的產品意象圖，
  文字用真正的網頁文字渲染），不是這支工具能單獨做到的，先跟使用者確認要不要做
  這個額外的版型工程。

### 依文章標籤（tag）選色調 + 道具 + 風格（避免每篇都長得一樣）

2026-08 之前的做法是所有文章都套同一組「暖白/裸粉/淺藍 + minimalist flatlay」
（呼應網站主色 `#f2a7b5`），結果所有封面圖看起來都很像。現在改成：**主色 + 副色/
點綴色 + 一個具象道具元素 + 風格關鍵字**，依文章的 `tag` 換一套組合，同分類內部
好辨認、跨分類又有明顯差異。標記「✓ 已實測」的是驗證過效果不錯、可以直接照抄的；
沒標記的是同一套邏輯延伸出的建議組合，還沒實測，用起來如果效果不好可以調整
（例如發現色調跟某篇已發表文章太像，就換一個未用過的點綴色或道具）。

| tag（子分類） | 主色 + 副色/點綴 | 道具/具象元素 | 風格關鍵字 |
|---|---|---|---|
| 卸妝（卸妝膏/卸妝油/眼唇卸妝液）| ✓ 冷藍灰 + 白 | 水滴、水波紋 | spa 般的冷靜簡約，soft diffused lighting |
| 洗面乳、去角質 | 薄荷/海藻綠 + 白 | 泡泡、泡沫質感 | 清新乾淨，bright airy lighting |
| 乳液、面霜 | 奶油白 + 暖杏色 | 乳液流動/滴落瞬間 | 柔焦、舒適溫暖 |
| 精華液 | 鼠尾草綠 + 白 | 葉片、單顆水珠特寫 | 乾淨的實驗室美學，clinical minimalist |
| 化妝水 | 淺藍 + 銀白 | 水花噴濺、薄霧 | 清透水感，dewy fresh |
| 面膜 | 薰衣草紫/粉 + 白 | 面膜片材質紋理、蒸氣感 | spa 放鬆感 |
| 防曬 | 天空藍 + 沙白 | 陽光光斑、光暈 | 夏日輕盈感 |
| 眼霜 | 冷灰紫 + 白 | 極微距單顆露珠 | 精緻細膩 |
| 底妝（粉底/氣墊/妝前乳/定妝）| ✓ 暖杏色 + 奶油白 + 玫瑰金點綴 | 飄浮蜜粉塵 | 柔焦 bokeh 背景，warm diffused lighting |
| 唇妝（唇膏/唇蜜/護唇膏）| ✓ 黑底 + 酒紅或珊瑚色點綴光束 | 唇膏/唇蜜特寫、光澤反射 | 高對比、編輯感／雜誌封面風 |
| 腮紅、修容 | 焦糖棕 + 黑 | 腮紅粉末暈染質感 | 溫暖高對比 |
| 眼妝（睫毛膏/眼線筆）| 深藏青/炭灰 + 金屬金點綴 | 液狀眼線劃過的線條感 | 精準、圖像感強烈 |
| 眉妝 | 大地棕 + 奶白 | 眉刷刷毛質感特寫 | 溫潤自然 |
| 遮瑕 | 淺桃色 + 白 | 光影對比（象徵遮蓋暗沉） | 柔和明亮 |
| 妝容趨勢/情境類（非產品推薦文）| 霧灰玫瑰 + 灰 | 柔和電影感光線 | 氛圍感、muted cinematic |

範例（✓ 已實測，效果不錯）：

- 卸妝：`"professional studio product photography, two generic unbranded skincare
  cleansing balm jars in cool blue-grey tones with white accents, dynamic water
  droplets and a gentle ripple splash frozen in motion around the products, blank
  unreadable labels, minimalist spa-like composition, soft diffused lighting, clean
  light grey background"` + `--negative_prompt "text, logo, watermark, letters"`
- 底妝：`"professional studio product photography, two generic unbranded foundation
  bottles in warm apricot and cream tones with rose gold caps, soft floating powder
  dust particles suspended in the air, blank unreadable labels, soft focus bokeh
  background, warm diffused studio lighting, minimalist beauty flatlay"`
- 唇妝/腮紅：`"professional studio product photography, a generic unbranded lipstick
  and blush compact on a matte black background, single bold wine-red accent light
  streak across the scene, high contrast dramatic lighting, glossy reflective
  surface, blank unreadable labels, editorial magazine style macro shot, minimalist"`

舊的「暖白/裸粉/淺藍 + minimalist flatlay」公式（乳液文章用過）還是有效，
但現在對應到上表的「乳液、面霜」那一格即可，不要再當成所有文章的預設公式。

## 完成後

1. 用 Read 工具打開產生的圖，目視確認沒有變形的手指/文字、沒有意外冒出可辨識的真實
   品牌標誌（生圖模型偶爾會學到品牌識別度很高的瓶型或字體，抽到的話重生一張）。
2. 把路徑填進 `articles.json` 該篇文章的 `image` 欄位。
3. 照 `glowup-article-seo-links` skill 的收尾步驟：bump `articles.json` 版本號、
   開瀏覽器確認圖片有正常顯示，再 commit + push。
