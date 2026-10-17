---
name: gbro-cover-design
description: Generate AI image prompts for 3:4 vertical social media cover designs with consistent face references and 10 composition styles
triggers:
  - generate a cover design prompt
  - create social media cover for this article
  - make a vertical cover image prompt
  - design a xiaohongshu cover
  - generate wechat article cover
  - create cover design from this content
  - help me make a cover image
  - design a promotional cover
---

# gbro-cover-design

> Skill by [ara.so](https://ara.so) — Design Skills collection.

Generate ready-to-use AI image prompts for 3:4 vertical cover designs (WeChat/Xiaohongshu format). The skill reads your article, asks three rounds of questions, then outputs a complete prompt with title, composition, face consistency references, and style-specific instructions.

Based on [oh-my-cover-design](https://github.com/feitangyuan/oh-my-cover-design) (MIT), optimized for three-round questioning, 10 style templates, few-shot examples, fixed 3:4 aspect ratio, and first-time setup guidance.

## Installation

Clone the complete repository (includes style templates and example library in `references/`):

```bash
git clone https://github.com/pyang5166/gbro-cover-design.git \
  ~/.claude/skills/gbro-cover-design
```

**Important**: Do NOT use SKILL.md alone. The skill requires:
- Style templates in `references/style-XX-*.md` (10 files)
- Example prompts in `references/examples.md`
- Face reference placeholder in `assets/my-face.png`

## First-Time Setup

On first trigger, the skill guides you through configuration (saved to `config.md`):

1. **Face reference image**: Place a clear front-facing photo at `assets/my-face.png` as default Image 1
2. **Image model confirmation**: Verify your model supports multi-image references (即梦/Seedream 4.0, Nano Banana, GPT-Image, etc.)

Configuration is saved in the skill directory and won't be asked again.

## How It Works

Send article content to the agent → skill asks 3 rounds of questions → outputs final prompt:

### Round 1: Style & Title
- Recommends composition style based on article content
- Asks user to confirm or choose from 10 styles
- Generates cover title (user can modify)

### Round 2: Reference Images
- Confirms face reference (use default `my-face.png` or upload new)
- Requests additional materials (product screenshots, UI images, brand assets)

### Round 3: Final Details
- Expression (smile/serious/surprised/thoughtful)
- Background tone (warm/cool/vibrant/muted)
- Font style (bold/modern/handwritten)
- Text color preference

**All Round 3 items are optional** — unspecified = model decides.

## 10 Composition Styles

| Style | File | Best For |
|-------|------|----------|
| **深色渐变风** | `style-01-dark-gradient.md` | Centered figure, large text overlay, maximum impact |
| **纯色扁平风** | `style-02-flat-solid.md` | Clean look, figure + props + solid background |
| **产品主视觉风** | `style-03-product-hero.md` | UI screenshots or product images as main focus |
| **对比卡片风** | `style-04-contrast-cards.md` | Before/after, good/bad comparisons |
| **极简留白风** | `style-05-minimal-whitespace.md` | Large negative space, title-only focus, restrained |
| **海报拼贴风** | `style-06-poster-collage.md` | Multi-layered when you have many assets |
| **人物侧置留白风** | `style-07-side-figure.md` | Figure on one side, title takes other half |
| **背影构图风** | `style-08-back-view.md` | Figure facing away, inspirational content |
| **局部出镜风** | `style-09-partial-body.md` | Only hands/partial face, product is hero |
| **正面对视风** | `style-10-direct-gaze.md` | Direct eye contact, emotional connection |

Each style template includes:
- Composition layout instructions
- Camera angle & framing
- Lighting setup
- Safe area definitions (3:4 ratio, top/bottom text zones)
- Style-specific prompt structure

## Prompt Structure

Final output follows this format:

```
[TITLE]
标题文案

[STYLE]
构图风格名称

[COMPOSITION]
3:4 vertical ratio, safe zones defined...
[specific layout instructions from style template]

[SUBJECT]
Reference Image 1 (face): [description of my-face.png]
Keep facial features consistent: [specific traits]
Expression: [user choice or model default]

[ADDITIONAL REFERENCES]
Image 2: [product screenshot/UI/asset if provided]
Image 3: [additional material if provided]

[BACKGROUND]
[Style-specific background instructions]
Tone: [user preference or model default]

[TEXT OVERLAY]
Title: [generated title]
Font: [user preference or model default]
Color: [user preference or model default]
Position: [safe zone coordinates]

[TECHNICAL]
Aspect ratio: 3:4 (1080x1440px)
Model: [user's confirmed model]
Quality: high detail, professional lighting
```

## Reference Files

### Style Templates (`references/style-XX-*.md`)

Each style file contains:
- **Trigger conditions**: When to recommend this style
- **Layout formula**: Exact composition rules
- **Safe zones**: Text placement areas for 3:4 ratio
- **Prompt template**: Fill-in-the-blank structure

Example from `style-01-dark-gradient.md`:

```markdown
## 深色渐变风

### 触发条件
- 需要冲击力、视觉张力
- 人物是核心表达
- 标题文字较长

### 构图公式
- 画幅: 3:4 竖版 (1080x1440px)
- 人物: 居中，腰部以上特写
- 标题: 大字压在人物后方，上1/3或下1/3
- 背景: 深色径向渐变 (黑→深蓝/深紫)

### 安全区
- 顶部留白: 0-180px (标题可选区)
- 主体区: 180-1080px (人物占据)
- 底部留白: 1080-1440px (标题可选区)

### 提示词模板
3:4 vertical cover, dark radial gradient background (black to [deep blue/purple]), centered medium shot portrait from waist up...
```

### Example Library (`references/examples.md`)

Contains 8 complete real-world prompts with:
- Original article summary
- Chosen style + rationale
- Full prompt text
- Reference image descriptions
- Final image preview path

Use these for few-shot learning when generating new prompts.

## Face Consistency

The skill maintains face consistency across designs:

1. **Default reference**: `assets/my-face.png` (user's prepared photo)
2. **Trait extraction**: Skill analyzes and describes key facial features
3. **Prompt injection**: Features embedded in subject description
4. **Model requirement**: Multi-image reference support mandatory

Example face description in prompt:

```
Reference Image 1 (face): assets/my-face.png
Asian male, mid-30s, short black hair, rectangular glasses, 
clean-shaven, oval face shape, warm smile.
Keep facial features consistent: eye shape, nose bridge, 
jawline, skin tone.
```

## Configuration File

`config.md` stores user preferences:

```markdown
# gbro-cover-design Configuration

## Face Reference
- Default image: assets/my-face.png
- Fallback: Ask user to upload each time

## Image Generation Model
- Confirmed model: Seedream 4.0
- Multi-image support: Yes
- Max reference images: 4

## Preferences
- Default style: auto-recommend
- Language: Chinese titles, English prompts
```

## Workflow Example

User sends article about AI agent tools:

```
User: "帮我给这篇文章设计封面：[粘贴文章内容]"

Agent: 
Round 1 - 根据你的文章内容(介绍新的AI Agent工具),推荐使用:
- 产品主视觉风 (适合展示工具界面)
- 深色渐变风 (突出科技感)

请选择构图风格,并确认标题:
建议标题: "下一代Agent来了"

User: "产品主视觉风,标题改成'3个Skills顶一个运营部'"

Agent:
Round 2 - 参考图设置:
- 图1(人脸): 使用默认 assets/my-face.png?
- 图2+: 请上传产品截图或相关素材

User: "用默认人脸,上传了agent后台截图和聊天界面"

Agent:
Round 3 - 细节调整(不说的我帮你决定):
- 表情? (微笑/严肃/惊讶/思考)
- 背景色调? (冷色科技/暖色活力)
- 字体风格? (粗体/现代/手写)
- 文字颜色?

User: "微笑,冷色科技,粗体,白色"

Agent: [生成完整提示词]
```

## Safe Zones for 3:4 Ratio

All prompts include safe zone definitions:

```
Aspect ratio: 3:4 vertical (1080x1440px)

Safe zones:
- Top text zone: 0-180px (avoid face overlap)
- Main subject: 180-1080px (figure + key elements)
- Bottom text zone: 1080-1440px (avoid cut-off)

Title placement: [style-specific position]
Ensure 40px padding from edges
```

## Common Patterns

### Auto Style Recommendation

```python
# Skill logic (internal):
article_keywords = extract_keywords(article_content)

if "产品" in keywords or "工具" in keywords:
    recommend = "产品主视觉风"
elif "对比" in keywords or "前后" in keywords:
    recommend = "对比卡片风"
elif "教程" in keywords or "步骤" in keywords:
    recommend = "海报拼贴风"
else:
    recommend = "深色渐变风"  # default
```

### Loading Style Template

```markdown
<!-- Skill reads from references/style-03-product-hero.md -->
{{ load_template(user_selected_style) }}

<!-- Extracts: -->
- composition_rules
- safe_zones
- prompt_structure
- lighting_setup
```

### Few-Shot Example Injection

```markdown
<!-- From references/examples.md -->
Example 1: "让AI做我老板"
Style: 深色渐变风
Prompt: 3:4 vertical cover, dark radial gradient...
[full example]

Example 2: "下一代Agent来了"
Style: 产品主视觉风
Prompt: 3:4 vertical cover, product screenshot占60%...
[full example]

<!-- Skill uses 2-3 most similar examples as context -->
```

## Troubleshooting

**Q: First run asks for config but I already set it up**  
A: Check `config.md` exists in skill directory. Delete and re-run if corrupted.

**Q: Face doesn't look consistent in generated images**  
A: Verify your model supports multi-image references. Update `assets/my-face.png` with clearer, front-facing photo.

**Q: Style template not loading**  
A: Ensure complete clone with `references/` directory. Single SKILL.md won't work.

**Q: Prompt too long for my model**  
A: Reduce Round 3 details (expression, tone, font). Skill will use model defaults.

**Q: Want to add custom style**  
A: Create `references/style-11-custom.md` following existing template structure. Add to style list in main logic.

**Q: Change default face reference**  
A: Replace `assets/my-face.png` OR edit `config.md` to set "Fallback: Ask user to upload each time".

## Environment Variables

No API keys required. Skill only generates prompts (text output).

Optional config file location:

```bash
# Default
~/.claude/skills/gbro-cover-design/config.md

# Custom (set in skill metadata if needed)
GBRO_CONFIG_PATH=/custom/path/config.md
```

## File Structure

```
gbro-cover-design/
├── SKILL.md                          # This file
├── config.md                         # User configuration (created on first run)
├── assets/
│   ├── my-face.png                   # Default face reference
│   └── examples/                     # Preview images
│       ├── 01-让AI做我老板.webp
│       └── ...
└── references/
    ├── style-01-dark-gradient.md     # Style template
    ├── style-02-flat-solid.md
    ├── ...
    ├── style-10-direct-gaze.md
    └── examples.md                   # Complete example prompts
```

## License

MIT License. Based on [oh-my-cover-design](https://github.com/feitangyuan/oh-my-cover-design) by feitangyuan.
