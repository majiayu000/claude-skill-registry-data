---
name: frontend-design
description: 引導 Claude 產出高品質的前端設計，避免 AI 生成的通用風格（AI slop）。包含字型、色彩、動態、背景的設計指引。
---

# Frontend Design — 避免 AI Slop 的設計指引

> 來源：[Improving Frontend Design Through Skills](https://claude.com/blog/improving-frontend-design-through-skills)
> 📦 離線歸檔：[`archive/articles/improving-frontend-design-through-skills.md`](https://github.com/zeuikli/claude-code-workspace/blob/blog-archive/archive/articles/improving-frontend-design-through-skills.md)

## 字型選擇

避免：Inter、Roboto、system-ui 等過度使用的預設字體
推薦搭配：
- 標題：Playfair Display、DM Serif Display、Space Grotesk
- 內文：DM Sans、Source Serif 4、JetBrains Mono（程式碼）
- 使用 Google Fonts 或 Bunny Fonts CDN

## 色彩系統

避免：漸層按鈕、藍紫配色、過度飽和
推薦：
- 選擇一個主色調，搭配中性色與一個強調色
- 使用 oklch() 色彩空間產生和諧的調色盤
- 暗色模式：降低飽和度而非反轉顏色

## 動態效果

避免：彈跳動畫、過度的 hover 效果
推薦：
- 微妙的淡入（opacity 0→1, 200-300ms）
- 使用 CSS `transition` 而非 JS 動畫
- 滾動觸發的漸進顯示（Intersection Observer）

## 背景與紋理

避免：純白背景、stock photo 背景
推薦：
- 極淡的噪點紋理（CSS noise pattern）
- 幾何網格或點陣圖案
- 玻璃擬態（backdrop-filter: blur）搭配半透明卡片

## 版面配置

- 限制最大寬度（max-width: 1200px）
- 使用 CSS Grid 搭配不等欄寬
- 留白是設計工具，不是浪費空間

## Gotcha

- **不要覆蓋已建立的設計系統**：若專案使用 Tailwind / shadcn / MUI，先遵循其約定，不要用本 skill 的偏好蓋掉。
- **品牌字型優先**：若專案有 brand identity（logo 字型、既有色盤），本 skill 的字型建議僅供參考，不要強行替換。
- **深色背景需確認可及性**：深色配淺字 contrast ratio 需 ≥ 4.5:1（WCAG AA），不要只顧美觀。
- **動態效果不是必須**：若使用者未要求動畫，不要主動加入 transition / animation，避免拖慢渲染。
