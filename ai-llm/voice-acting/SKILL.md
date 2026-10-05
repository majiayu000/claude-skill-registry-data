---
name: voice-acting
description: >-
  台词声音、重音、气口与呼吸控制。指导配音与 lip-sync，消除机械朗诵感。
---

# Voice Acting Skill (台词声音、重音与呼吸)

`skills/voice-acting.md` 负责指导配音模型（如 ElevenLabs、ChatTTS、CosyVoice）及视频 lip-sync 驱动所需的语音语调特征，消除 AI 语音朗诵感与机械腔。

---

## 1. 核心声音维度

1. **Volume & Resonance (音量与共鸣)**：
   - 耳语 (Whisper, 压低声带，极度亲密或暗中密谋)
   - 气声 (Breathy voice, 疲惫或情感崩溃前夕)
   - 胸腔共鸣 (Resonant, 权势者自信宣布)
2. **Tempo & Rhythm (语速与节奏)**：
   - 均速是 AI 最大的敌人。真人说话必然有**起伏、突进与拉长**；
   - 紧张时：词汇突然密集倾泻，随后骤停；
   - 权谋时：字句极慢，句间留白给对方施压。
3. **Breathing Patterns (呼吸声与气口)**：
   - 话前吸气 (Pre-speech breath)
   - 话中气竭 (Breath-holding)
   - 话后长吁 (Release of breath)
4. **Emphasis (非预期重音)**：
   - 改变一句话中重音的位置，意思完全颠覆：
     - “*我* 没说他拿了钱”（是别人说的）
     - “我 *没* 说他拿了钱”（我坚决否认我说过）
     - “我没说 *他* 拿了钱”（是另一个人拿的）
     - “我没说他拿了 *钱*”（他拿的是别的重要东西）

---

## 2. 结构化输出规范

```json
{
  "dialogue_line": "你真的觉得……我们之间还有可能吗？",
  "acoustic_profile": {
    "volume": "低音量，略带沙哑的喉底音",
    "tempo": "前半句缓慢犹豫，在省略号处停顿 1.2 秒，后半句语速稍快但音量衰减",
    "breathing": "在说出'我们之间'之前，有一次明显的深吸气声",
    "emphasis": ["真的", "我们之间"],
    "delivery_style": "脆弱而试探，尾音微微颤抖但没有哭腔",
    "tts_prompt_tags": "[sigh] [softly] [pause=1.2s] [whisper] [trembling breath]"
  }
}
```
