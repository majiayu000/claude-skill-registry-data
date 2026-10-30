---
name: paper-triage
description: 拿到一篇新論文（標題＋摘要）時，用六個C快速判斷它跟油污偵測研究（Sentinel-2/Landsat等多光譜光學影像、無監督異常偵測方法不限、可能搭配分割的兩階段管線）的相關程度，輸出「核心相關／邊緣相關／不相關」三選一。判斷時重可能性、不嚴格比對方法名稱。在主對話中執行，因為使用者通常會立刻針對判斷結果追問。觸發詞：使用者貼上新論文、說「這篇論文相關嗎」、「幫我初篩」。
---

# Stage 0：六個C快速初篩

我會貼上一篇論文的標題與摘要（或全文）。請依照以下六個 C 幫我快速判斷，
每項用 1-2 句話回答，不要展開細節：

1. **Category（類型）**：這是方法論文、應用論文、survey、benchmark資料集論文，還是其他？

2. **Context（脈絡）**：它跟以下哪些既有方法/概念有關聯？
   （無監督異常偵測 / RX detector / Isolation Forest / VAE、VQ-VAE 重建誤差法 /
   語意分割 DeepLabV3+、SegFormer / SAR 或光學遙測影像 / 影像諧和化 / domain adaptation）

3. **Correctness（假設合理性）**：論文有什麼隱含假設？這些假設站得住腳嗎？

4. **Contributions（核心貢獻）**：用一句話講最關鍵的 1-2 個貢獻。

5. **Clarity（可重現性）**：方法描述得夠清楚到可以重現嗎，還是含糊不清？

6. **Connection to my research（與我研究的交集）**：重點是「有沒有可能性」，不是嚴格比對
   方法名稱，寧可寬鬆放過，不要太早排除：
   - 用的是「光學影像」(Sentinel-2 / Landsat 或其他多光譜衛星) 還是 SAR？光學影像優先留意，
     但 SAR 論文也可能有可借鏡的概念，不直接排除。
   - 是否處理無監督異常偵測？方法不限——RX detector、Isolation Forest、
     reconstruction-based方法（VAE/VQ-VAE等）、其他統計或深度學習方法都算，
     不要因為「不是用VAE」就判定不相關。
   - 是否處理跨感測器（例如同時使用 Landsat 與 Sentinel-2）的光學影像分析或資料諧和化？
     問的是「多感測器整合」這個問題本身，不是有沒有用 Sen2Like 這個特定工具。
   - 跟「光學影像油污偵測」「optical domain adaptation」這些研究缺口有沒有交集？

最後給一個總結判斷（三選一）：
- 【核心相關】直接碰到研究方法或研究缺口 → 建議呼叫 paper-extractor subagent 做 Stage 1a
- 【邊緣相關】跟領域有關但不直接碰到方法 → 存查備用，先不深讀
- 【不相關】沒有實質交集 → 略過

並用一句話說明為什麼。
