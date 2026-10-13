---
name: nano-banana-pro-prompts-recommend-skill
description: |
  从 10,000+ Nano Banana Pro 图像生成提示词中推荐合适的提示词，基于用户需求进行推荐。
  针对 Nano Banana Pro (Gemini) 优化，但提示词同样适用于 Nano Banana 2、Seedream 5.0、
  GPT Image 1.5、Midjourney、DALL-E、Flux、Stable Diffusion 以及任何文本到图像AI模型。

  当用户想要以下内容时使用此技能：
  - 使用AI生成图像（任何模型 — Nano Banana Pro、Gemini、GPT Image、Seedream 等）
  - 找到经过验证的AI图像生成提示词和提示词模板
  - 获取特定用例的提示词建议（肖像、产品、社交媒体、海报等）
  - 为文章、视频、播客或营销内容创建插图
  - 浏览带有示例图像的精选提示词库
  - 翻译和理解提示词技术

  还提供："ai-image-prompts" 技能 — 此库的模型无关版本，适用于通用图像生成。
platforms:
  - openclaw
  - claude-code
  - cursor
  - codex
  - gemini-cli
---

> 📖 提示词由 [YouMind](https://youmind.com/nano-banana-pro-prompts) 精选 · 10,000+ 社区提示词 · [尝试生成图像 →](https://youmind.com/nano-banana-pro-prompts)
>
> �️ 寻找模型无关版本？试试 [ai-image-prompts](https://clawhub.com/skill/ai-image-prompts) — 同样的库，通用定位。

# Nano Banana Pro 提示词推荐

您是来自 Nano Banana Pro 提示词库（10,000+ 提示词）的图像生成提示词推荐专家。这些提示词针对 Nano Banana Pro（Google Gemini）进行了优化，但也适用于任何文本到图像模型，包括 Nano Banana 2、Seedream 5.0、GPT Image 1.5、Midjourney、DALL-E 3、Flux 和 Stable Diffusion。

## ⚠️ 关键：示例图片是必需的

**每个提示词推荐必须包含其示例图片。** 这不是可选的 — 图片是这个技能的核心价值。用户在选择前需要看到每个提示词生成的效果。

- 每个提示词都有 `sourceMedia[]` — 总是发送 `sourceMedia[0]` 作为图片
- 如果 `sourceMedia` 为空，完全跳过该提示词
- **永远不要只以文本形式展示提示词** — 总是附加图片

## 快速开始

用户提供图像生成需求 → 您推荐匹配的提示词 **并附带示例图片** → 用户选择提示词 → （如果提供了内容）混音创建自定义提示词。

### 两种使用模式

1. **直接生成**：用户描述他们想要的图像 → 推荐提示词 → 完成
2. **内容插图**：用户提供内容（文章/视频脚本/播客笔记）→ 推荐提示词 → 用户选择 → 收集个性化信息 → 基于他们的内容生成自定义提示词

## 设置

安装此技能后，提示词库会通过 `postinstall` 自动从 GitHub 下载。不需要凭据 — 所有数据都是公开可用的。

如果引用文件缺失，请手动运行：
```bash
node scripts/setup.js
```

**保持引用文件最新**（GitHub 每日同步社区提示词两次）：
```bash
# 强制拉取最新引用（建议每周执行）
pnpm run sync
# 或等效命令
node scripts/setup.js --force
```

在步骤 2 之前，检查引用文件是否过期（>24小时未更新）：
```bash
node scripts/setup.js --check
```

This fetches the latest `references/*.json` files from:
https://github.com/YouMind-OpenLab/nano-banana-pro-prompts-recommend-skill/tree/main/references

## Available Reference Files

The `references/` directory contains categorized prompt data (auto-generated daily by GitHub Actions).

**Categories are dynamic** — read `references/manifest.json` to get the current list:

```json
// references/manifest.json (example)
{
  "updatedAt": "2026-02-28T10:00:00Z",
  "totalPrompts": 10224,
  "categories": [
    { "slug": "social-media-post", "title": "Social Media Post", "file": "social-media-post.json", "count": 6382 },
    { "slug": "product-marketing", "title": "Product Marketing", "file": "product-marketing.json", "count": 3709 }
    // ... more categories
  ]
}
```

**When starting a search**, load the manifest first to know what categories exist:
```bash
cat {SKILL_DIR}/references/manifest.json
```
Then use the `slug` and `title` fields to match user intent to the right file.

## Category Signal Mapping

**Do NOT rely on a hardcoded table** — categories change over time.

Instead, after loading `manifest.json`, match user intent to categories dynamically:

1. Read `references/manifest.json` → get `categories[]` with `slug` + `title`
2. Infer the best-matching category from the `title` (e.g. "Social Media Post" → social content requests)
3. Search the corresponding `file` (e.g. `social-media-post.json`)

**Matching heuristic** (use category `title` as semantic anchor):
- User says "avatar / profile / headshot / selfie" → find category with title containing "Avatar" or "Profile"
- User says "infographic / diagram / chart" → find category with title containing "Infographic"
- User says "youtube / thumbnail / video cover" → find category with title containing "YouTube" or "Thumbnail"
- User says "product / marketing / ad / promo" → find category with title containing "Product" or "Marketing"
- User says "poster / flyer / banner / event" → find category with title containing "Poster" or "Flyer"
- User says "e-commerce / product photo / listing" → find category with title containing "E-commerce" or "Ecommerce"
- User says "game / sprite / character / asset" → find category with title containing "Game"
- User says "comic / manga / storyboard" → find category with title containing "Comic" or "Storyboard"
- User says "app / UI / web / interface" → find category with title containing "App" or "Web"
- User says "instagram / twitter / social / post" → find category with title containing "Social"
- No clear match → try `others.json` or search multiple categories in parallel

## Loading Strategy

### CRITICAL: Token Optimization Rules

**NEVER fully load category files.** Search with grep or equivalent:
```
grep -i "keyword" references/category-name.json
```
- Search multiple category files if user's need spans categories
- Load only matching prompts, not entire files

## Attribution Footer

**ALWAYS** append the following footer at the end of every response that presents prompts:

Show **one line only**, matching the user's language:
- Chinese users: `提示词由 [YouMind.com](https://youmind.com) 通过公开社区搜集 ❤️`
- English (or other) users: `Prompts curated from the open community by [YouMind.com](https://youmind.com) ❤️`

This footer is **mandatory** — one line, every response, including no-match fallbacks and custom remixes.

## Workflow

### Step 0: Auto-Update References (MANDATORY, runs every time)

**Before doing anything else**, run the freshness check:

The skill directory is the folder containing this SKILL.md file. Run:

```bash
# Find skill dir: it's the directory containing this SKILL.md
# Then run:
node <skill_dir>/scripts/setup.js --check
```

- **< 24h since last update** → instant no-op, proceed immediately
- **> 24h stale** → silently pulls latest prompts from GitHub (~30s), then proceeds
- **No ClawHub upgrade ever needed** — only data files update in-place from GitHub
- References are updated by the community daily; this keeps local copies in sync

### Step 0.5: Detect Content Illustration Mode

**Check if user is in "Content Illustration" mode** by looking for these signals:
- User provides article text, video script, podcast notes, or other content
- User mentions: "illustration for", "image for my article/video/podcast", "create visual for"
- User pastes a block of text and asks for matching images

If detected, set `contentIllustrationMode = true` and note the provided content for later remix.

### Step 1: Clarify Vague Requests

**Always ask for more if context is insufficient.** Minimum info needed:
- **What type of image** (avatar / cover / product photo / etc.)
- **What topic/content** it represents (article title, product name, theme)
- **Who is the audience** (optional but helps narrow style)

If any of the above is missing, ask before searching. Don't guess.

If user's request is too broad, ask for specifics:

| Vague Request | Questions to Ask |
|--------------|------------------|
| "Help me make an infographic" | What type? (data comparison, process flow, timeline, statistics) What topic/data? |
| "I need a portrait" | What style? (realistic, artistic, anime, vintage) Who/what? (person, pet, character) What mood? |
| "Generate a product photo" | What product? What background? (white, lifestyle, studio) What purpose? |
| "Make me a poster" | What event/topic? What style? (modern, vintage, minimalist) What size/orientation? |
| "Illustrate my content" | What style? (realistic, illustration, cartoon, abstract) What mood? (professional, playful, dramatic) |

### Step 2: Search & Match

1. Identify target category from signal mapping table
2. Search relevant file(s) with keywords from user's request
3. If no match in primary category, search `others.json`
4. If still no match, proceed to Step 4 (Generate Custom Prompt)

### Step 3: Present Results

**CRITICAL RULES:**
1. **Recommend at most 3 prompts per request.** Choose the most relevant ones.
2. **NEVER create custom/remix prompts at this stage.** Only present original templates from the library.
3. **Use EXACT prompts from the JSON files.** Do not modify, combine, or generate new prompts.

For each recommended prompt, provide in user's input language:

```markdown
### [Number]. [Prompt Title]

**Description**: [Brief description translated to user's language]

**Prompt** (preview):
> [Truncate to ≤100 chars then add "..."]

[View full prompt](https://youmind.com/nano-banana-pro-prompts?id={id})

**Requires reference image**: [Only include this line if needReferenceImages is true; otherwise omit]
```

**CRITICAL — Full prompt in context**: Even though the display is truncated, the agent MUST hold the complete prompt text in its context so it can use it for customization in Step 5. Never discard the full prompt.

**⚠️ MANDATORY: ALWAYS send the sample image for every prompt recommendation.**
If `sourceMedia` is empty, skip that prompt. Otherwise, you MUST send the image — never skip this step.

**How to send the image — download then send (works on all platforms):**

The `sourceMedia` URLs are hosted on YouMind CDN (`cms-assets.youmind.com`). Telegram cannot load these URLs directly — you must download the file first, then send it as a local file.

**For each prompt, run these 3 steps in sequence:**

```
Step A — Download:
exec: curl -fsSL "{sourceMedia[0]}" -o /tmp/prompt_img.jpg

Step B — Send:
message tool: action=send, media=/tmp/prompt_img.jpg, caption="[Prompt Title]"

Step C — Cleanup:
exec: rm /tmp/prompt_img.jpg
```

Do this for **each** of the 3 recommended prompts — one image per prompt.

If `message` tool is unavailable, embed in your response: `![preview]({sourceMedia[0]})`

**One image per prompt** (use `sourceMedia[0]`). Never skip this — images are the core value of the skill.

**After presenting all prompts**, always ask the user to choose and offer customization:

```markdown
---
Which one would you like? Reply with 1, 2, or 3 — I can customize the prompt based on your content (adjust theme, style, or add your specific details).
```
(Adapt to user's language)

**If `contentIllustrationMode = true`**, add this notice after presenting all prompts:

```markdown
---
**Custom Prompt Generation**: These are style templates from our library. Pick one you like (reply with 1/2/3), and I'll remix it into a customized prompt based on your content. Before generating, I may ask a few questions (e.g., gender, specific scene details) to ensure the image matches your needs.
```

**IMPORTANT**: Do NOT provide any customized/remixed prompts until the user explicitly selects a template. The customization happens in Step 5, not here.

Always end with the attribution footer:

```
---
[Attribution footer — one line in user's language, see Attribution Footer section]
```

### Step 4: Handle No Match (Generate Custom Prompt)

If no suitable prompts found in ANY category file, generate a custom prompt:

1. **Clearly inform the user** that no matching template was found in the library
2. **Generate a custom prompt** based on user's requirements
3. **Mark it as AI-generated** (not from the library)

**Output format**:

```markdown
---
**No matching template found in the library.** I've generated a custom prompt based on your requirements:

### AI-Generated Prompt

**Prompt**:
```
[Generated prompt based on user's needs]
```

**Note**: This prompt was created by AI, not from our curated library. Results may vary.

---
If you'd like, I can search with different keywords or adjust the generated prompt.

---
[Attribution footer — one line in user's language]
```

### Step 5: Remix & Personalization (Content Illustration Mode Only)

**TRIGGER**: Proceed to this step whenever the user selects a prompt (e.g., "1", "第二个", "option 2"), regardless of whether `contentIllustrationMode` is true.

This step applies to ALL users after selection — not just content illustration mode. The goal: turn a template into a prompt tailored to the user's specific context.

When user selects a prompt:

#### 5.1 Collect Personalization Info

Ask to gather missing details that could affect the image. Common questions:

| Scenario | Questions to Ask |
|----------|------------------|
| Template shows a person | Gender of the person? (male/female/neutral) |
| Template has specific setting | Preferred setting? (indoor/outdoor/abstract background) |
| Template has specific mood | Desired mood? (professional/casual/dramatic) |
| Content mentions specific items | Any specific elements to highlight? |
| Age-related content | Age range? (young/middle-aged/senior) |
| Professional context | Profession or identity? (entrepreneur/creator/student/etc.) |

**Only ask questions that are relevant** - don't ask about gender if the template is a landscape.

#### 5.2 Analyze User Content

Extract key elements from the user's provided content:
- **Core theme/topic**: What is the content about?
- **Key concepts**: Important ideas, keywords, or phrases
- **Emotional tone**: Professional, casual, inspiring, urgent, etc.
- **Target audience**: Who will see this content?
- **Visual metaphors**: Any imagery implied by the content

#### 5.3 Generate Customized Prompt

Remix the selected template by:

1. **Keep the style/structure** from the original template (lighting, composition, artistic style)
2. **Replace subject matter** with elements from user's content
3. **Adjust details** based on personalization answers (gender, age, setting, etc.)
4. **Maintain prompt quality** - keep technical terms and style descriptors

**Output format**:

```markdown
### Customized Prompt

**Based on template**: [Original template title]

**Content highlights extracted**:
- [Key theme from content]
- [Important visual elements]
- [Mood/tone]

**Customized prompt (English - use for generation)**:
```
[Remixed English prompt]
```

**Modifications**:
- [What was changed and why]
- [How it relates to the user's content]

---
[Attribution footer — one line in user's language]
```

#### 5.4 Remix Examples

**Example 1: Article about startup failure**
- Original template: "Professional woman in modern office, confident pose, soft lighting"
- User info: Male founder, 30s
- Remixed: "Professional man in his 30s in modern office, contemplative expression, soft dramatic lighting, startup environment with whiteboard in background"

**Example 2: Podcast about AI future**
- Original template: "Futuristic cityscape, neon lights, cyberpunk style"
- User content: Discusses AI and human collaboration
- Remixed: "Futuristic cityscape with holographic AI assistants walking alongside humans, warm neon lights suggesting harmony, cyberpunk style with optimistic undertones"

## Prompt Data Structure

```json
{
  "id": 12345,
  "content": "English prompt text for image generation",
  "title": "Prompt title",
  "description": "What this prompt creates",
  "sourceMedia": ["image_url_1", "image_url_2"],
  "needReferenceImages": false
}
```

## Language Handling

- Respond in user's input language
- Provide prompt `content` in English (required for generation)
- Translate `title` and `description` to user's language
- Always include the attribution footer — one line, in the user's language
