---
name: facial-performance
description: >-
  面部微表情与肌肉张力控制。针对特写镜头进行精准眼睑收缩、视线焦点与微表情抑制。
---

# Facial Performance Skill (面部微表情与肌肉控制)

`skills/facial-performance.md` 针对 AI 视频模型最容易“翻车”的面部生成痛点（如嘴部抽搐、假笑变形、五官漂移、双眼乱晃），提供专业的面部解构与克制化控制指南。

---

## 1. 面部微动作解构体系

人类面部有 40 多块微小肌肉。在电影摄影机前，最高级的表演永远是**克制的微变化**：

1. **眼神与眼睑 (Eyes & Eyelids)**：
   - 眨眼频率 (Blink Rate)：焦虑时高频微眨；极度专注或震惊压抑时数秒不眨眼；
   - 视线动线 (Gaze Vector)：避让直视（低头看地面 15 度）、眼神聚焦（定点于对方右眼）、涣散与失焦（陷入回忆）；
   - 下眼睑张力：轻微眯眼表明警惕或审视，眼睑肌肉松垮表明疲惫与释然。
2. **下颌与咬肌 (Jaw & Masseter)**：
   - 咬肌轻微隆起收缩（Clenched jaw）：表达极度克制的愤怒或隐忍；
   - 下巴微扬：傲慢、挑衅、防备；
   - 喉结滑动（Swallowing）：生理性紧张的无可辩驳证据。
3. **嘴角与唇部 (Mouth & Lips)**：
   - 单侧嘴角上提不到一毫米（Smirk）：轻蔑、自嘲；
   - 嘴唇微张（Parted lips）且呼吸可闻：脆弱、无言以对、被击中痛处；
   - 严禁双唇紧抿拉成长条状（AI 假人抽搐）。

---

## 2. 针对 AI 模型的防畸变约束

AI 视频大模型在处理面部时具有内在缺陷，必须通过明确的英文修饰词加以抑制：

| 常见模型缺陷 | 抑制词与提示词对策 (Compiler Directives) |
| :--- | :--- |
| **过度咧嘴笑 (Perma-smile)** | `neutral expression`, `composed facial muscles`, `no smiling` |
| **突然大哭流泪** | `dry eyes`, `restrained emotion`, `no overt weeping` |
| **左右面部肌肉不对称扭曲** | `natural facial symmetry`, `subtle micro-expressions` |
| **嘴唇说话时融化/漂移** | `subtle mouth articulation`, `controlled lip movement` |
| **双眼无神或翻白眼** | `focused steady gaze`, `eye contact tracking naturally` |

---

## 3. 面部微表情指令范例

### 范例 1：被心爱之人当面说谎
```text
Her eyes remain steady on him, but her lower eyelids tighten almost imperceptibly. 
Her blink rate drops. 
The corners of her mouth remain neutral, showing no dramatic frown, yet her jaw muscle flexes once as she swallows. 
A faint, restrained micro-expression of quiet disillusionment, captured in sharp focus.
```

### 范例 2：在审讯中强装无辜
```text
He maintains soft eye contact without staring. 
A faint, polite half-smile that does not reach his eyes. 
His breathing is steady, but his gaze occasionally flickers downward to the table edge for less than a quarter of a second before returning. 
Controlled, composed facial tension.
```
