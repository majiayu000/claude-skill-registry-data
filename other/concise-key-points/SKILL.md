---
name: concise-key-points
description: Compress answers to the highest practical information density with minimal wording while preserving essential meaning. Use when the user asks for 言簡意賅, 講重點, Concise, 精簡回答, 簡潔回答, 只講重點, 直接回答, brief, TL;DR, or otherwise requests a concise key-points response.
---

# 言簡意賅｜講重點｜Concise

## 核心規格

- 預設將一般回答縮短 70%，保留至少 95% 的必要資訊。
- 先給結論，再列 3–5 個重點；僅在必要時補充。
- 優先用條列；每點只表達一個概念，並盡量控制在一行。
- 以資訊密度為第一優先，不為追求短而刪除關鍵限制、風險或行動項目。

## 刪減規則

- 刪除寒暄、客套、自我描述、冗詞與重複敘述。
- 刪除非必要背景、例子、轉場與推理過程。
- 合併同義內容，但保留不同條件、數字、結論與例外。
- 可直接回答時，只輸出答案，不加前言或結語。

## 輸出順序

1. 結論。
2. 三至五個核心重點。
3. 必要的限制、風險或下一步。

## 邊界

- 遵守使用者明確指定的格式、字數與詳細程度；其指示優先。
- 對高風險、技術或精確性要求高的內容，保留必要警示、條件、來源與驗證資訊。
- 程式碼、命令、資料與引用不得因壓縮而失真或無法使用。
- 若 30% 長度無法保留 95% 資訊，優先保留資訊完整性。
