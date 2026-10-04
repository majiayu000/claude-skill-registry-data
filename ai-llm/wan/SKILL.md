---
name: Wan 视频生成
description: 使用 Wan 2.6 模型生成视频。当用户想要图生视频、图片动起来、参考视频生成、视频中主体一致性，或提到 wan、Wan 2.6 时使用此 skill。
category: video
tags: [视频生成, 图生视频, 参考视频, Wan, Flash, 多镜头, 主体一致性]
featured: true
---

# Wan 2.6

Wan 2.6 是一款先进的视频生成模型，支持图生视频和参考视频生成。能够将静态图片转化为动态视频，或使用多个参考视频保持主体一致性生成新视频。

## 可用模型

| 模型 ID | 功能 | 分辨率 | 说明 |
|--------|------|--------|------|
| `wan/v2.6/image-to-video` | 图生视频 | 720p/1080p | **标准版**，画质更优，适合高质量创作 |
| `wan/v2.6/image-to-video/flash` | 图生视频 | 720p/1080p | Flash 版本，高性价比 |
| `wan/v2.6/reference-to-video` | 参考视频生成 | 720p/1080p | **R2V**，使用参考视频保持主体一致性 |

## 计费方式

### 标准版 & 参考视频生成 (wan/v2.6/image-to-video & wan/v2.6/reference-to-video)

| 分辨率 | 单价 | 5秒 | 10秒 |
|--------|------|-----|------|
| 720p | 40积分/秒 | 200 | 400 |
| 1080p | 60积分/秒 | 300 | 600 |

> 注：参考视频生成 (R2V) 仅支持 5 秒或 10 秒时长

### Flash 版 (wan/v2.6/image-to-video/flash)

| 分辨率 | 单价 | 5秒 | 10秒 | 15秒 |
|--------|------|-----|------|------|
| 720p | 20积分/秒 | 100 | 200 | 300 |
| 1080p | 30积分/秒 | 150 | 300 | 450 |

## 工作流

### 1. 调用 submit_task

使用 MCP 工具 `submit_task` 提交任务。

---

### 参考视频生成 (Reference to Video)

使用 1-3 个参考视频中的主体（人物、动物、物体），生成保持主体一致性的新视频。

#### 基础示例

```json
{
  "model_id": "wan/v2.6/reference-to-video",
  "parameters": {
    "prompt": "Dance battle between @Video1 and @Video2.",
    "video_urls": [
      "https://v3b.fal.media/files/b/0a86742f/9rVJtQ2ukp9cid8lheutF_output.mp4",
      "https://v3b.fal.media/files/b/0a867424/30OqWXFgHWqOwcP2OUwRx_output.mp4"
    ],
    "duration": "5",
    "resolution": "1080p"
  }
}
```

#### 完整参数示例

```json
{
  "model_id": "wan/v2.6/reference-to-video",
  "parameters": {
    "prompt": "@Video1 在咖啡馆里悠闲地喝咖啡，阳光透过窗户洒进来",
    "video_urls": [
      "https://example.com/character-video.mp4"
    ],
    "aspect_ratio": "16:9",
    "duration": "10",
    "resolution": "1080p",
    "negative_prompt": "low resolution, error, worst quality, low quality, defects",
    "enable_prompt_expansion": true,
    "multi_shots": true
  }
}
```

#### R2V 参数说明

| 参数 | 类型 | 必填 | 默认值 | 说明 |
|-----|------|-----|-------|------|
| prompt | string | **是** | - | 使用 @Video1/@Video2/@Video3 引用主体（最大 800 字符） |
| video_urls | array | **是** | - | 参考视频 URL 列表（1-3 个，帧率需 ≥16 FPS） |
| aspect_ratio | string | 否 | "16:9" | 宽高比：16:9/9:16/1:1/4:3/3:4 |
| duration | string | 否 | "5" | 视频时长：**仅 5/10 秒** |
| resolution | string | 否 | "1080p" | 分辨率：720p / 1080p |
| negative_prompt | string | 否 | "" | 负面提示词（最大 500 字符） |
| enable_prompt_expansion | boolean | 否 | true | LLM 优化提示词 |
| multi_shots | boolean | 否 | true | 多镜头分割 |
| seed | integer | 否 | - | 随机种子 |

---

### 图生视频 (Image to Video)

#### 标准版示例（高画质）

适合追求高质量画面的创作：

```json
{
  "model_id": "wan/v2.6/image-to-video",
  "parameters": {
    "prompt": "镜头缓缓推进，人物微微转头，露出温暖的微笑，微风轻轻吹过发丝，电影级画质",
    "image_url": "https://v3b.fal.media/files/b/0a8673dd/m9EV5W9aSqg8J7rb-18TK.png",
    "duration": "10",
    "resolution": "1080p",
    "enable_prompt_expansion": true
  }
}
```

#### Flash 版示例（高性价比）

适合快速预览或对成本敏感的场景：

```json
{
  "model_id": "wan/v2.6/image-to-video/flash",
  "parameters": {
    "prompt": "人物微微转头，露出温暖的微笑，微风吹动发丝",
    "image_url": "https://v3b.fal.media/files/b/0a8673dd/m9EV5W9aSqg8J7rb-18TK.png"
  }
}
```

#### 完整参数示例

```json
{
  "model_id": "wan/v2.6/image-to-video",
  "parameters": {
    "prompt": "镜头缓缓推进，人物微微转头，露出温暖的微笑，微风轻轻吹过发丝",
    "image_url": "https://v3b.fal.media/files/b/0a8673dd/m9EV5W9aSqg8J7rb-18TK.png",
    "duration": "10",
    "resolution": "1080p",
    "negative_prompt": "low resolution, error, worst quality, low quality, defects",
    "enable_prompt_expansion": true,
    "multi_shots": false
  }
}
```

#### 多镜头视频示例

适合生成电影级多镜头视频：

```json
{
  "model_id": "wan/v2.6/image-to-video/flash",
  "parameters": {
    "prompt": "Shot 1 [0-4s] 镜头从远景推进到人物面前\nShot 2 [4-8s] 切换到侧面特写，人物转头看向远方\nShot 3 [8-12s] 全景展示环境，人物慢慢走远",
    "image_url": "https://example.com/scene.jpg",
    "duration": "15",
    "resolution": "1080p",
    "enable_prompt_expansion": true,
    "multi_shots": true
  }
}
```

### 参数说明

| 参数 | 类型 | 必填 | 默认值 | 说明 |
|-----|------|-----|-------|------|
| prompt | string | **是** | - | 视频动作描述（最大 800 字符） |
| image_url | string | **是** | - | 首帧图片 URL（尺寸 240-7680） |
| duration | string | 否 | "5" | 视频时长：5/10/15 秒 |
| resolution | string | 否 | "1080p" | 分辨率：720p / 1080p |
| audio_url | string | 否 | - | 背景音乐 URL（WAV/MP3，3-30秒） |
| negative_prompt | string | 否 | "" | 负面提示词（最大 500 字符） |
| enable_prompt_expansion | boolean | 否 | true | LLM 优化提示词 |
| multi_shots | boolean | 否 | false | 多镜头分割（需 enable_prompt_expansion=true） |
| seed | integer | 否 | - | 随机种子 |
| enable_safety_checker | boolean | 否 | true | 安全检查 |

## 查询任务状态

提交任务后会返回 `task_id`，使用 `get_task` 查询结果：

```json
{
  "task_id": "返回的任务ID"
}
```

任务状态：
- `pending` - 排队中
- `processing` - 处理中
- `completed` - 完成，结果在 `result` 中
- `failed` - 失败，查看 `error` 字段

## 完整示例

**用户请求**：帮我把这张人物照片做成 10 秒的视频，让她微微转头微笑

**执行步骤**：

1. 调用 `submit_task`：

```json
{
  "model_id": "wan/v2.6/image-to-video/flash",
  "parameters": {
    "prompt": "镜头缓缓推进，女性人物优雅地微微转头，露出温暖迷人的微笑，阳光洒在脸上，微风轻轻吹动发丝，电影级画质，自然流畅的动作",
    "image_url": "用户提供的图片URL",
    "duration": "10",
    "resolution": "1080p",
    "enable_prompt_expansion": true
  }
}
```

2. 获取 `task_id` 后调用 `get_task` 查询结果

## 提示词技巧

1. **描述动作和运动**：明确描述镜头运动（推进、拉远、环绕）和主体动作（转头、挥手、微笑）
2. **使用时间标记**：对于多镜头视频，使用 `[0-4s]`、`[4-8s]` 等时间标记分割镜头
3. **设置视觉风格**：指定光线、色调、氛围（如"电影质感"、"暖色调"、"柔和光线"）
4. **使用负面提示词**：通过 `negative_prompt` 排除不想要的效果

### 提示词示例

**人像视频**：
```
女性人物优雅地转头看向镜头，露出自信的微笑，眼神温柔，微风轻轻吹动长发，
阳光柔和地洒在脸上，背景虚化，电影级画质，自然流畅的动作
```

**风景视频**：
```
镜头缓缓向前推进，穿过茂密的竹林，阳光透过竹叶洒下斑驳的光影，
微风吹动竹叶沙沙作响，景深变化自然，电影级稳定镜头
```

**多镜头叙事**：
```
Shot 1 [0-5s] 镜头从远景慢慢推进，主角站在山顶眺望远方
Shot 2 [5-10s] 切换到特写，展示主角坚定的眼神
Shot 3 [10-15s] 全景展示壮丽的山川景色，主角背影渐行渐远
```

## 注意事项

1. **图片要求**：首帧图片尺寸需在 240-7680 像素之间
2. **音频处理**：如果音频时长超过视频时长，会被截断；如果音频较短，超出部分为静音
3. **多镜头模式**：需要同时启用 `enable_prompt_expansion: true` 和 `multi_shots: true`
4. **生成时间**：视频生成需要一定时间，15秒视频可能需要数分钟
5. **分辨率影响**：1080p 比 720p 贵 50%，请根据需求选择
