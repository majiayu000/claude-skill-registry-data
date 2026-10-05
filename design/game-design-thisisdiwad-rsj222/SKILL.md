---
name: game-design
description: "遊戲設計理論、機制設計與玩家體驗"
---

# 遊戲設計 Game Design

> 創造有趣且令人沉浸的遊戲體驗

## 適用場景

- 遊戲概念設計與 GDD 撰寫
- 核心機制設計與迭代
- 數值系統設計與平衡
- 關卡設計與節奏控制
- 玩家體驗優化

## MDA 框架

**Mechanics -> Dynamics -> Aesthetics** (設計師角度 -> 玩家角度)

- 跳躍 + 平台 -> 時機判斷挑戰 -> 成就感、挑戰
- 資源 + 交易 -> 市場博弈 -> 策略、社交

## 核心知識

### 8 種美學體驗

| 美學 | 說明 | 遊戲範例 |
|------|------|----------|
| Sensation | 感官刺激 | 音樂遊戲、VR |
| Fantasy | 幻想角色扮演 | RPG、模擬人生 |
| Narrative | 故事體驗 | 視覺小說、冒險 |
| Challenge | 挑戰克服 | Dark Souls |
| Fellowship | 社交互動 | MMO、派對遊戲 |
| Discovery | 探索發現 | 開放世界 |
| Expression | 自我表達 | Minecraft |
| Submission | 消遣放鬆 | 農場遊戲 |

### 核心循環

**目標 -> 挑戰(難度曲線) -> 行動(玩家輸入) -> 反饋(獎勵系統) -> 重複**

### 難度曲線

波浪式難度：每個高峰後有喘息空間、新機制引入後給練習時間、Boss 前設置檢查點

## 最佳實踐

1. **先好玩後完整** - 核心機制要先驗證有趣
2. **快速原型** - 盡早做出可玩版本測試
3. **玩家測試** - 觀察玩家行為，不要只聽意見
4. **減法設計** - 刪掉不必要的功能
5. **心流設計** - 挑戰與能力匹配

## 常見錯誤

| 錯誤 | 正確做法 |
|------|----------|
| 堆砌功能 | 專注核心體驗 |
| 只聽玩家說什麼 | 觀察玩家做什麼 |
| 一開始就做完整 | 快速原型迭代 |
| 難度線性增加 | 波浪式難度曲線 |

## Sharp Edges

### SE-1: 經濟系統膨脹
- **嚴重度**: critical
- **情境**: 遊戲內貨幣隨時間失去價值，玩家對獎勵無感
- **原因**: 貨幣流入 > 流出，沒有有效的消耗機制 (Sink)
- **症狀**: 老玩家囤積大量貨幣、新玩家難以追上、獎勵數值不斷膨脹
- **解決**: 設計有效的 Sink（強化失敗、修理費）、限制每日獲取上限、流入/流出比例目標 1:1
- 完整 checklist -> [extended/checklists.md#economy-balance-checklist]

### SE-2: 功能堆砌 (Feature Creep)
- **嚴重度**: high
- **情境**: 遊戲功能越加越多，但核心體驗沒有變好
- **原因**: 每個功能單獨看都「不錯」，但累積起來讓遊戲失焦
- **症狀**: 玩家不知道「這遊戲在玩什麼」、教學時間過長、每個系統都很淺
- **解決**: 定義核心體驗（一句話說明）、每個新功能問「如何增強核心體驗？」、學會說「不」

### SE-3: Pay-to-Win 設計
- **嚴重度**: critical
- **情境**: 付費玩家獲得明顯的競爭優勢，傷害免費玩家體驗
- **原因**: 短期收入優先於長期留存
- **症狀**: 免費玩家大量流失、遊戲評價極低、只剩「鯨魚」在玩
- **解決**: 付費內容限於外觀/便利性、付費加速但不能跳過、競技模式數值標準化

### SE-4: 數值溢出風險
- **嚴重度**: high
- **情境**: 後期數值爆炸，出現「億萬傷害」或計算錯誤
- **原因**: 成長曲線設計不當（通常是指數成長）
- **症狀**: 傷害數字看不清楚、整數溢出導致 Bug、平衡越來越難調整
- **解決**: 使用對數或軟上限曲線，避免純指數成長
- 程式碼範例 -> [extended/examples.md#number-overflow-fix]

### SE-5: 忽略玩家行為只聽玩家意見
- **嚴重度**: medium
- **情境**: 根據玩家問卷/論壇意見改設計，但結果更差
- **原因**: 玩家說的和做的經常不一致
- **症狀**: 玩家說「太難」但數據顯示通關率正常、玩家要求的功能加了但沒人用
- **解決**: 觀察玩家「做什麼」比「說什麼」重要、用數據驗證假設（A/B 測試）、理解抱怨背後的真正問題

## 數值設計快速參考

**成長曲線**: 玩家屬性用對數、升級經驗用指數、解鎖內容用 S 曲線
- 完整公式 -> [extended/examples.md#growth-curve-formulas]

**傷害計算**: 基礎傷害 = 攻擊力 x (100 / (100 + 防禦力))
- 詳細範例 -> [extended/examples.md#damage-calculation]

## 玩家心理學

### 行為激勵

| 激勵類型 | 說明 | 應用 |
|----------|------|------|
| 外在獎勵 | 物質回報 | 金幣、裝備、經驗 |
| 內在獎勵 | 成就感 | 挑戰克服、技能提升 |
| 社交獎勵 | 認同感 | 排行榜、成就展示 |
| 隨機獎勵 | 驚喜感 | 抽卡、掉落 |

### Hook Model

**Trigger -> Action -> Variable Reward -> Investment -> (循環)**

範例（手遊）：推播通知 -> 登入遊戲 -> 每日抽獎 -> 累積天數

## 遊戲類型設計要點

| 類型 | 核心要素 | 詳細設計 |
|------|----------|----------|
| 動作 | 操作手感、打擊感、敵人可讀性 | [extended/templates.md#action-game-design] |
| RPG | 角色成長、戰鬥系統、世界觀 | [extended/templates.md#RPG-system-design] |
| Roguelike | 隨機性平衡、Meta 進度、Build 設計 | [extended/templates.md#roguelike-design] |
| 解謎 | 漸進複雜度、公平性、提示系統 | [extended/templates.md#puzzle-game-design] |
| 手遊 | 操作限制、碎片化、變現設計 | [extended/templates.md#mobile-game-design] |

## 關卡與敘事

- 關卡設計 checklist -> [extended/checklists.md#level-design-checklist]
- 教學設計金字塔 -> [extended/checklists.md#tutorial-pyramid]
- 敘事結構類型 -> [extended/templates.md#narrative-structure]

## 多人遊戲

- 網路模型比較 -> [extended/templates.md#multiplayer-design]
- 防作弊 checklist -> [extended/checklists.md#anti-cheat-checklist]

## 測試與營運

- 玩家測試問卷 -> [extended/checklists.md#playtest-questionnaire]
- 觀察重點 -> [extended/checklists.md#playtest-observation]
- Live Service 設計 -> [extended/templates.md#live-service-design]
- 開發流程 -> [extended/templates.md#development-workflow]

## 模板與工具

- GDD 模板 -> [extended/templates.md#GDD-template]
- **引擎**: Unity / Unreal
- **經濟模擬**: Machinations
- **UI/UX**: Figma
- **文檔管理**: Notion

## 相關資源

- [GDC Vault](https://www.gdcvault.com/)
- [Game Developer](https://www.gamedeveloper.com/)
- [Game Maker's Toolkit](https://www.youtube.com/@GMTK)

## 相關領域

- [[storytelling]] - 遊戲敘事與劇本
- [[visual-media]] - 遊戲美術與動畫
- [[ui-ux-design]] - 遊戲 UI/UX
