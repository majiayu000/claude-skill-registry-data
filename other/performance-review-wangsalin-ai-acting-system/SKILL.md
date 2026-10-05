---
name: performance-review
description: >-
  自动化表演质量评审器。依据 16 条防假人禁忌与戏剧逻辑对表演方案进行严格自检与打分。
---

# Performance Review Skill (表演质量审查打分器)

`skills/performance-review.md` 充当表演指导与监视器（Performance Reviewer），负责在 Prompt 最终交付给视频模型之前，对表演方案进行多维度推演与严格自检。

---

## 1. 评审指标体系 (100 分制)

| 评审维度 | 满分 | 考察重点 | 扣分触发条件 |
| :--- | :--- | :--- | :--- |
| **1. Acting Logic (行动逻辑性)** | 20 | 角色动作是否有清晰的动机驱动，是否存在 Objective 与 Obstacle | 角色无目的闲逛，或情绪缺乏前置事件支撑 (-10) |
| **2. Naturalness & Subtlety (真实与克制)** | 20 | 是否避免了浮夸的 AI 假人表情（瞪眼/假笑/无故大哭） | 包含滥用情绪形容词、缺乏生理微反应 (-10) |
| **3. Subtext Quality (潜台词深度)** | 15 | 外部动作/台词与内心真实欲望是否形成戏剧张力 | 表层台词与内心完全一致、毫无言外之意 (-8) |
| **4. Camera Appropriateness (景别适配度)** | 15 | 特写镜头是否抑制了大动作，全景镜头是否强化了空间感 | 特写镜头里手势大幅挥舞、夸张摇头 (-10) |
| **5. Continuity & Momentum (连续性与余波)** | 15 | 跨镜头状态、手持道具、情绪残留衰减是否平滑 | 情绪断崖式翻转、道具凭空消失或换手 (-10) |
| **6. Prompt Executability (视频模型可执行性)** | 15 | 英文 Prompt 是否使用了具象的视觉与力学动作词汇 | 提示词塞入抽象心理散文、模型无法理解的哲学词汇 (-8) |

---

## 2. 自动化打分与返工机制

- **总分 >= 85 分**：优秀，直接批准输出最终 Prompt。
- **75 <= 总分 < 85 分**：合格但有瑕疵，系统自动给出微调优化建议。
- **总分 < 75 分**：**强制拦截**，自动触发重新编译，并列出整改清单。

---

## 3. 评审报告标准格式

```markdown
# Performance Review Report

- **Overall Score**: 92 / 100 [PASSED]
- **Dimension Breakdown**:
  - Acting Logic: 19 / 20
  - Naturalness & Subtlety: 18 / 20
  - Subtext Quality: 14 / 15
  - Camera Appropriateness: 15 / 15
  - Continuity & Momentum: 13 / 15
  - Prompt Executability: 13 / 15

### Strengths (优势)
- 特写镜头下精准抑制了肢体晃动，将全部戏剧张力集中在手指停顿和视线避让上；
- 潜台词设计与嘴上台词形成鲜明反差，层次丰富。

### Flagged Risks & Adjustments (微调建议)
- *提示词英文微调*：原句中的 `sadness` 建议替换为 `controlled gaze avoidance, slight pause in hand folding clothes`，更便于视频模型稳定采样。
```
