---
name: ai-image-gen
author: 雪见
description: Generate AI images using ModelScope's Tongyi Wanxiang (通义万相) model. Use this skill whenever the user asks to generate an image, create a picture, draw something, or mentions AI image generation - even if they don't explicitly say "generate image". Triggers on phrases like "画一张图", "生成图片", "create an image", "draw me", "generate a picture", "make an illustration", etc.
---

# AI Image Generator

Generate high-quality AI images using ModelScope's Tongyi Wanxiang (通义万相) model.

## When to use this skill

Use this skill when the user wants to:
- Generate an AI image from a text description
- Create artwork or illustrations
- Visualize concepts or ideas
- Generate photos or pictures

**Trigger phrases (examples):**
- "生成一张图片" / "画一张图"
- "Create an image of..."
- "Draw me a..."
- "Generate a picture showing..."
- "Make an illustration of..."
- "我想要一张...的图"

## How to use

### Step 1: Understand the user's request

Extract the image description from the user's request. If the description is vague, ask clarifying questions:
- What style? (realistic, cartoon, oil painting, etc.)
- What mood? (bright, dark, dramatic, etc.)
- Any specific details? (colors, composition, etc.)

### Step 2: Enhance the prompt (optional but recommended)

For better results, you can enhance the user's prompt with additional details:
- Add style modifiers (e.g., "in the style of...", "photorealistic", "digital art")
- Add quality modifiers (e.g., "highly detailed", "4k", "professional")
- Keep the prompt in English for best results with the model

### Step 3: Run the generation script

Execute the image generation script:

```bash
python ${CLAUDE_SKILL_DIR}/scripts/generate_image.py "your enhanced prompt" --output <output-path>
```

**Parameters:**
- `prompt` (required): Text description of the image
- `--output, -o`: Output file path (default: generated_image.jpg)
- `--model, -m`: Model ID (default: Tongyi-MAI/Z-Image-Turbo)

**Example:**
```bash
python ${CLAUDE_SKILL_DIR}/scripts/generate_image.py \
  "A majestic golden cat sitting on a velvet throne, photorealistic, dramatic lighting" \
  --output ./cat_throne.jpg
```

### Step 4: Show the result

After generation:
1. Confirm the image was saved successfully
2. Use the Read tool to display the image to the user
3. Ask if they want any modifications or additional images

## Prerequisites

**Required environment variable:**
```bash
export MODELSCOPE_API_KEY='your-modelscope-api-key'
```

The user needs a ModelScope API key. If not set, the script will prompt the user to configure it.

**Required Python packages:**
- `requests`
- `Pillow` (PIL)

Install with:
```bash
pip install requests Pillow
```

## Available models

| Model ID | Description |
|----------|-------------|
| `Tongyi-MAI/Z-Image-Turbo` | Fast generation (default) |
| `Tongyi-MAI/Z-Image` | Higher quality, slower |

## Tips for better results

1. **Be specific**: "A golden retriever puppy playing in autumn leaves" > "a dog"
2. **Add style**: "in the style of Studio Ghibli", "photorealistic", "oil painting"
3. **Include details**: lighting, mood, composition, colors
4. **Use English**: The model works best with English prompts
5. **Avoid negative phrasing**: Say what you want, not what you don't want

## Example workflow

**User:** "帮我画一只在月亮上的猫"

**Your response:**
1. Enhance prompt: "A fluffy white cat sitting on the crescent moon, starry night sky background, dreamy atmosphere, digital art style"
2. Run script:
   ```bash
   python ${CLAUDE_SKILL_DIR}/scripts/generate_image.py \
     "A fluffy white cat sitting on the crescent moon, starry night sky background, dreamy atmosphere, digital art style" \
     --output moon_cat.jpg
   ```
3. Show the generated image to the user
4. Ask: "这是生成的图片，你觉得怎么样？需要调整吗？"

---

## About Author

### 雪见
📍 坐标：四川成都

**身份标签：**
- 5万多人 AI 社群多期精英教练（RPA + Agent）
- AI 应用工程师
- 风变 AI 编程讲师
- 深耕 RPA自动化 + AI智能体工作流 2年+

**我能提供：**
AIP、RPA自动化、Coze/N8N、小龙虾（OpenClaw）等应用落地交流

**想和大家说的话：**
> 干就完了，多用 AI 提效，多用 AI 编程。

---

### 2026 AI 陪伴群（付费）

雪见运营着一个 **付费 AI 陪伴群**，每天分享 AI 技术与实战干货：

**群内分享内容包括：**
- AI 行业资讯与前沿动态
- RPA 机器人流程自动化
- Coze / N8N 工作流实战
- OpenClaw 小龙虾落地应用
- 其他 AI 技术干货（不局限于小龙虾）

**额外福利：**
- GPT、Claude、Gemini、Claude Code 等 AI 工具 **低价优惠购买**
- 比官方便宜几十块完全没问题

---

### 联系方式

| 渠道 | 信息 |
|------|------|
| 微信 | `soraaigc`（欢迎链接）|
| 公众号 | **雪见AI编程**（欢迎关注）|

### 推荐链接

| 平台 | 链接 | 说明 |
|------|------|------|
| 知识星球 | https://t.zsxq.com/mC8bP | ⭐ **限时免费** 加入 |
| AI编程平台 | https://aigocode.com/invite/JHK8VZAQ | 🚀 AI编程 + OpenClaw 必备，强烈推荐！ |
| 飞书文档 | https://my.feishu.cn/wiki/XkNawOgzjiK4zektG6dcD4zXnxd | 📚 录播视频 + 文档教程 |

> 💡 雪见日常使用的大模型：[aigocode.com](https://aigocode.com/invite/JHK8VZAQ) - 搞 AI 编程、玩转 OpenClaw 首选！

> 感兴趣的朋友欢迎加微信 `soraaigc` 咨询交流~
