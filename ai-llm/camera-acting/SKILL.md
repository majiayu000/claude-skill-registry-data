---
name: camera-acting
description: >-
  镜头景别与表演幅度适配。依据大特写到全景的不同景别，动态调节演员物理动作幅度。
---

# Camera Acting Skill (镜头景别与表演适配)

`skills/camera-acting.md` 负责根据摄像机镜头景别（Extreme Close-Up、Close-Up、Medium Shot、Full Shot）动态调节表演的物理幅度与注意力焦点。

---

## 1. 核心铁律：景别越近，幅度越小

> **“舞台表演需要放大到最后排观众能看清；而电影特写镜头中，哪怕睫毛的一次轻颤都是雷霆万钧。”**

在 AI 视频生成中，许多提示词在特写镜头里命令人物“痛苦地挥手、夸张摇头”，导致画面严重撕裂和角色失真。

---

## 2. 四大景别调校矩阵

| 景别类型 | 英文词汇 | 允许的核心动作 | 绝对禁止的动作 | 推荐表演强度 (1-5) |
| :--- | :--- | :--- | :--- | :--- |
| **大特写** | `Extreme Close-Up (ECU)` | 眼神视线转折、瞳孔微聚、下眼睑微抽动、喉部微小吞咽、鼻翼微颤。 | 严禁大幅度摆头、严禁手部入画乱动、严禁剧烈面部表情。 | **强度 1** (极度克制) |
| **特写 / 近景** | `Close-Up (CU)` / `Medium Close-Up (MCU)` | 头部微转（<15度）、嘴角微抿、下颌咬肌收缩、呼吸起伏、眼神交锋。 | 严禁双手在胸前剧烈比划、严禁夸张大笑或大哭。 | **强度 1 - 2** (克制到自然) |
| **中景** | `Medium Shot (MS)` | 手部道具交互（拿烟、倒水、翻书）、上身坐姿重心切换、双臂抱胸或下垂。 | 严禁无依托的悬空抽搐手势，必须与环境道具产生关系。 | **强度 2 - 3** (自然到生动) |
| **全景 / 远景** | `Full Shot (FS)` / `Long Shot (LS)` | 步态与步速变化、空间距离变化、身体朝向（背影、侧影）、驻足停顿。 | 无需关注面部微表情，严禁将 Prompt 算力浪费在远景睫毛/眼泪上。 | **强度 3 - 4** (重体态空间感) |

---

## 3. 景别驱动的 Prompt 生成转换案例

以“得知爱人意外身亡”为例：

### 1. 全景镜头 (Full Shot)
```text
Full shot, cinematic wide angle. The man stands alone in the vast, dimly lit hospital corridor. Upon receiving the phone call, his walking pace abruptly halts. His shoulders drop visibly by two inches, his body remaining perfectly motionless against the sterile white wall, dwarfed by the empty architectural space. High depth of field.
```

### 2. 特写镜头 (Close-Up)
```text
Close-up, 85mm portrait lens, shallow depth of field. The man holds the phone against his ear. His eyes are wide but dry, fixed unblinkingly on an empty point in space. His breathing becomes noticeably shallow. The jaw muscle tightens once. No crying, no weeping, no dramatic hand gestures—only pure, stunned paralysis captured in the micro-tension around his eyes and mouth.
```
