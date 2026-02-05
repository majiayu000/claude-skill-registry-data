---
name: learning
description: 學習輔助與知識管理。觸發：learn, note, knowledge, memory, review, understand, teach me, 學習, 筆記, 教我, 解釋
---

# Learning Skill

學習輔助與知識管理。

## Workflow Routing

- Create notes → [workflows/note-taking.md](workflows/note-taking.md)
- Explain concept → [workflows/explain-concept.md](workflows/explain-concept.md)

## 與 Memory 整合

### 學習新知識時
```
→ memory_search: "[主題]"
→ 找到已有的相關知識
→ 在已知基礎上建立新知識
```

### 學習完成後
```
→ 核心概念
→ memory_save:
    content: "[概念的一句話總結]"
    category: "general"
    importance: 3-4
```

### 追蹤學習進度
```
→ memory_save:
    content: "開始學習 [主題]，目標是 [...]"
    category: "event"
    importance: 3
```

## 與 Reflection 整合

### 學習後反思
- 真的理解了嗎？
- 能用自己的話解釋嗎？
- 和已知的知識有什麼連結？
- 還有什麼不清楚的？

### 間隔複習
- 學習後 1 天 → 第一次複習
- 3 天後 → 第二次複習
- 7 天 → 14 天 → 30 天

## 與 Proactive 整合

### 主動提醒
- 到了複習時間 → 提醒複習
- 發現相關主題 → 主動連結
- 學習停滯 → 建議調整方法

### 主動建議
- 根據學習歷史推薦下一步
- 發現知識空白 → 建議填補

## Learning Methods

### Feynman Technique
1. 選擇概念
2. 用簡單語言解釋（像教小孩）
3. 找出理解不足的地方
4. 回去強化並簡化

### Active Recall
- 讀完後，闔上書試著回想
- 用自己的話重述
- 找出「以為懂但其實不懂」的部分

### Spaced Repetition
- 新學：1 天後複習
- 複習過：3 天 → 7 天 → 14 天 → 30 天
- 忘記了：重新開始

## Note Format

```markdown
## [Topic Name]

### Core Concept
- 一句話解釋
- 為什麼重要

### Key Points
1. ...
2. ...
3. ...

### Connections
- 與 [X] 的關係...
- 和 [Y] 的差異...

### My Understanding
[用自己的話重述]

### To Clarify
- [ ] 還不清楚的問題
```

## Data Storage

所有學習記錄存在 `data/notes/`。
