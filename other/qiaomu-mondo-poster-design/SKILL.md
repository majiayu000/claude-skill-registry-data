---
name: qiaomu-mondo-poster-design
description: AI-powered poster and cover design tool that generates master-level artwork from natural language prompts using 20+ legendary designer styles
triggers:
  - generate a Mondo style poster for
  - create a book cover design for
  - design an album cover for
  - make a social media poster with
  - generate a movie poster in Mondo style
  - create a WeChat article cover for
  - design a Xiaohongshu image for
  - convert my image to poster style
---

# Qiaomu Mondo Poster Design

> Skill by [ara.so](https://ara.so) — Design Skills collection.

Generate professional-level posters, book covers, album art, and social media graphics from a single sentence. The AI automatically selects the best artistic style from 20 legendary poster designers (Saul Bass, Olly Moss, Chip Kidd, etc.) based on your content, handles color schemes, composition, and platform-specific aspect ratios.

## Installation

```bash
npx skills add joeseesun/qiaomu-mondo-poster-design
```

This installs the skill into your AI coding environment, enabling natural language poster generation.

## Core Capabilities

### 1. Text-to-Poster Generation

The primary function converts natural language descriptions into professional poster designs:

```python
# Basic usage - AI auto-selects style
prompt = "为《三体》设计书籍封面"
# → AI chooses Chip Kidd conceptual style with sci-fi aesthetics

prompt = "Create a poster for Interstellar movie"
# → AI chooses Kilian Eng geometric futurism with space themes

prompt = "为周杰伦《七里香》设计专辑封面"
# → AI chooses Peter Saville minimalism for album cover
```

### 2. Aspect Ratio Control

Automatically adapts to different platforms:

```python
# WeChat official account cover (ultra-wide)
--aspect-ratio 21:9

# Xiaohongshu (Little Red Book) post
--aspect-ratio 3:4

# Article featured image
--aspect-ratio 16:9

# Book cover (default)
--aspect-ratio 9:16

# Album cover (square)
--aspect-ratio 1:1
```

### 3. Style Comparison Mode

Generate multiple style variations to compare:

```python
# Compare different artistic approaches
prompt = "为《百年孤独》设计封面 --compare-styles"
# → Generates 3-5 variations in different master styles:
#   - Penguin Clothbound classic pattern
#   - Chip Kidd conceptual metaphor
#   - Alphonse Mucha art nouveau
```

### 4. Image-to-Poster Conversion

Transform existing images into stylized posters:

```python
# Upload reference image + style description
input_image = "photo.jpg"
prompt = "转换为 Saul Bass 极简主义海报风格"
# → Applies geometric minimalism to the image
```

## Natural Language Commands

### Trigger Keywords

The AI recognizes these keywords to activate poster generation:

- `Mondo风格` / `Mondo style`
- `书籍封面` / `book cover`
- `专辑封面` / `album cover`
- `海报` / `poster`
- `设计` / `design`
- `生成` / `generate`

### Command Patterns

```python
# Pattern 1: Platform-specific
"为公众号文章《人类简史》设计 21:9 封面"
# → WeChat cover, 21:9 aspect ratio, auto-style selection

# Pattern 2: Content type implicit
"为《小王子》设计读书笔记配图"
# → Detects "读书笔记" → uses literary aesthetic

# Pattern 3: Event/Activity
"为周末观影会设计海报"
# → Event poster, likely Saul Bass geometric style

# Pattern 4: Mood-based
"为《花样年华》设计观影笔记，温暖胶片感"
# → Detects mood → uses Japanese film aesthetic

# Pattern 5: Explicit style request
"用 Olly Moss 负空间风格为《盗梦空间》设计海报"
# → Uses specific designer style
```

## AI Style Selection Logic

The tool automatically maps content types to optimal designer styles:

| Content Type | Auto-Selected Style | Rationale |
|--------------|---------------------|-----------|
| WeChat reading notes | Literary aesthetic (soft watercolor) | Poetic atmosphere for deep reading |
| Xiaohongshu movie posts | Japanese film style (warm tones) | Nostalgic film grain for lifestyle |
| Xiaohongshu book shares | Korean aesthetic (pastel gradients) | Dreamy freshness for sharing |
| Literary book covers | Penguin Clothbound | Publishing-grade classic design |
| Sci-fi book covers | Chip Kidd | Random House conceptual metaphors |
| Album covers | Peter Saville / Reid Miles | Legendary record label aesthetics |
| Sci-fi movie posters | Kilian Eng | Geometric futurism |
| Art film posters | Alphonse Mucha | Art nouveau flowing lines |
| Thriller posters | Olly Moss | Negative space mystery |
| Event posters | Saul Bass | Bold geometric abstraction |

## Platform-Specific Workflows

### WeChat Official Account Covers

```python
# 21:9 ultra-wide format optimized for WeChat articles
prompt = """
为公众号文章设计封面:
标题: 《人工智能与人类的未来》
风格: 科技感但不失人文关怀
"""

# Expected output:
# - Aspect ratio: 21:9
# - Style: Kilian Eng futurism + warm accents
# - Composition: Digital brain merging with cosmic elements
# - Color: Cyber blue + warm orange contrast
```

### Xiaohongshu (Little Red Book) Posts

```python
# 3:4 vertical format for mobile feed

# Movie review post
prompt = "为《花样年华》设计观影笔记配图"
# → Japanese film aesthetic, 3:4, warm grain texture

# Book sharing post
prompt = "为《小王子》设计读书分享配图"
# → Korean aesthetic, 3:4, dreamy pink-purple gradient
```

### Book Cover Design

```python
# 9:16 classic book proportion (default)

# Literary fiction
prompt = "为《百年孤独》设计精装书封面"
# → Penguin Clothbound style, emerald green + gold butterfly pattern

# Science fiction
prompt = "为《三体》设计书籍封面"
# → Chip Kidd conceptual, distorted red sun in black void
```

### Album Art

```python
# 1:1 square format for streaming platforms

prompt = "为 Pink Floyd 《The Dark Side of the Moon》设计专辑封面"
# → Peter Saville minimalism, prism light refraction

prompt = "为爵士音乐节设计海报"
# → Reid Miles high contrast, jazz instruments in geometric composition
```

## Configuration & Parameters

### Aspect Ratio Options

```python
ASPECT_RATIOS = {
    "21:9": "WeChat official account cover (2100x900)",
    "16:9": "Article featured image / Desktop wallpaper (1920x1080)",
    "9:16": "Book cover / Movie poster / Event poster (1080x1920)",
    "3:4": "Xiaohongshu / Instagram portrait (1080x1440)",
    "1:1": "Album cover / Square social post (1080x1080)"
}
```

### Style Comparison Mode

```python
# Generate 3-5 variations in different styles
--compare-styles

# Example output:
# 1. Saul Bass geometric minimalism
# 2. Olly Moss negative space
# 3. Kilian Eng futurism
# 4. Alphonse Mucha art nouveau
# 5. Chip Kidd conceptual
```

### Prompt Optimization

The tool includes AI prompt enhancement:

```python
# User input (simple)
"为三体设计封面"

# AI optimized prompt (internal)
"""
Design a book cover for "The Three-Body Problem":
- Chip Kidd conceptual style
- Sci-fi hard science aesthetic
- Color: Deep black void with distorted red sun
- Composition: Negative space with central focal point
- Typography: Bold sans-serif, minimal text
- Mood: Cosmic horror, civilization fragility
"""
```

## Advanced Usage Patterns

### Multi-Language Support

```python
# Chinese input
"为《肖申克的救赎》设计电影海报"

# English input
"Design a movie poster for The Shawshank Redemption"

# Mixed input
"为 Pink Floyd 设计 album cover with 极简主义 style"

# All automatically processed with style matching
```

### Style Override

```python
# Let AI choose (recommended)
"为《银翼杀手》设计海报"
# → Auto: Kilian Eng futurism

# Force specific style
"用 Saul Bass 风格为《银翼杀手》设计海报"
# → Uses Saul Bass geometric instead

# Combine styles
"用 Olly Moss 负空间 + Alphonse Mucha 曲线为《盗梦空间》设计海报"
# → Hybrid style mixing
```

### Image-to-Image Conversion

```python
# Reference image + style transfer
input_image_path = "./photo.jpg"
prompt = "转换为 Mondo 海报风格，保留主体，极简化背景"

# Expected transformation:
# - Extract main subject
# - Apply geometric simplification
# - Reduce color palette to 3-5 colors
# - Add negative space
# - Apply screen print texture
```

## Design Principles (Auto-Applied)

The AI automatically applies these master-level principles:

### Negative Space
```python
# Automatically creates meaningful empty space
# Example: Bird flying out of prison bars (Shawshank)
```

### Visual Puns
```python
# One image conveys dual meaning
# Example: Joker smile forming Batman silhouette
```

### Minimalism
```python
# Maximum message with minimum elements
# Example: 12 chairs for "12 Angry Men"
```

### Dramatic Contrast
```python
# Size/color contrast for emotional impact
# Example: Tiny human vs. massive cosmic entity
```

### Color Psychology
```python
# Auto color schemes by mood:
# Sci-fi → Cyber blue + neon pink
# Literary → Beige + deep red
# Thriller → Dark tones + blood orange
# Warm story → Golden yellow + soft blue
```

## Troubleshooting

### Issue: Style Not Matching Content

```python
# Problem: Generated poster doesn't match expected aesthetic

# Solution: Add explicit style hints
# Weak prompt:
"为电影设计海报"

# Strong prompt:
"为科幻电影《星际穿越》设计海报，需要宇宙深空感和几何未来主义"
# → Explicitly triggers Kilian Eng style
```

### Issue: Wrong Aspect Ratio

```python
# Problem: Generated image doesn't fit platform

# Solution: Always specify aspect ratio for non-default use
# Default is 9:16, override with:
"为公众号文章设计封面 --aspect-ratio 21:9"
```

### Issue: Text Unreadable

```python
# Problem: Generated text in image is unclear

# Solution: Request text-free design, add text separately
"设计海报，不要包含文字，我稍后会用 Photoshop 添加标题"
# → Cleaner composition, you control typography
```

### Issue: Too Complex

```python
# Problem: Design has too many elements

# Solution: Request minimalism explicitly
"用 Saul Bass 极简主义风格，只用 2-3 个几何形状和 3 种颜色"
# → Forces radical simplification
```

### Issue: Style Mixing Unclear

```python
# Problem: Multiple style requests conflict

# Solution: Use --compare-styles to see options
"为《百年孤独》设计封面 --compare-styles"
# → Review 5 variations, choose best match
```

## Integration Examples

### With Python Image Processing

```python
from PIL import Image
import os

# Generate poster via natural language
poster_prompt = "为《三体》设计书籍封面 --aspect-ratio 9:16"
# (Tool generates image via AI)

# Post-process if needed
output_path = "generated_poster.png"
img = Image.open(output_path)

# Add text overlay programmatically
from PIL import ImageDraw, ImageFont
draw = ImageDraw.Draw(img)
font = ImageFont.truetype("Arial.ttf", 80)
draw.text((100, 100), "三体", fill="white", font=font)

img.save("final_poster.png")
```

### With Batch Generation

```python
# Generate multiple posters for a series
book_series = [
    "为《三体》设计封面",
    "为《黑暗森林》设计封面", 
    "为《死神永生》设计封面"
]

for i, prompt in enumerate(book_series):
    # Generate each with consistent style
    output_file = f"trilogy_{i+1}.png"
    # Tool processes prompt → saves to output_file
```

### With Social Media Automation

```python
# Generate platform-specific variants
platforms = {
    "wechat": "21:9",
    "xiaohongshu": "3:4", 
    "weibo": "16:9",
    "instagram": "1:1"
}

base_prompt = "为电影《流浪地球》设计海报"

for platform, ratio in platforms.items():
    prompt = f"{base_prompt} --aspect-ratio {ratio}"
    output = f"{platform}_poster.png"
    # Generate platform-optimized version
```

## Environment Variables

```bash
# API key for AI image generation (required)
export OPENAI_API_KEY=your_key_here

# Or use alternative providers
export ANTHROPIC_API_KEY=your_key_here

# Output directory (optional)
export POSTER_OUTPUT_DIR=./generated_posters

# Default aspect ratio (optional)
export DEFAULT_ASPECT_RATIO=9:16

# Language preference (optional)
export POSTER_LANG=zh-CN  # or en-US
```

## Best Practices

1. **Be specific about content, not style** - Let AI choose the artistic approach
   - Good: "为《银翼杀手》设计科幻海报，要有赛博朋克和霓虹灯感觉"
   - Avoid: "用蓝色和粉色，几何形状，未来主义..."

2. **Specify platform early** - Aspect ratio affects composition decisions
   - "为公众号文章《人工智能》设计 21:9 封面" ✓
   - Not: "设计封面" then resize later ✗

3. **Use mood descriptors** - Easier than design terminology
   - "温暖、怀旧、胶片感" > "low saturation, film grain, warm color grading"

4. **Iterate with comparison mode** - See multiple approaches
   - First pass: Use `--compare-styles`
   - Second pass: Refine chosen style with details

5. **Separate text from design** - AI-generated text often needs refinement
   - Generate text-free poster, add typography separately

This skill enables AI agents to create professional-grade poster designs from natural language, handling style selection, composition, color theory, and platform optimization automatically.
