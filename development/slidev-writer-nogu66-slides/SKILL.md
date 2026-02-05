---
name: slidev-writer
description: "Create engaging technical presentation slides using Slidev format, focusing on visual clarity, narrative flow, and problem-solving narratives"
---

# Slidev Presentation Writer

This skill enables Claude to create high-quality technical presentation slides using the Slidev framework. Slides should be visually engaging, easy to follow, and complement technical articles.

## Author Introduction

**こんにちは、noguです。**

X (Twitter): https://x.com/_nogu66

## Core Philosophy

**Visual storytelling makes complex topics accessible.**

Like Zenn articles, presentation slides should focus on: **"This solution solves this problem" > "This technology is amazing"**

### Target Audience

The most important target audience is **"people who need to understand this quickly"**. Design slides as if presenting to:
- Conference attendees who want the big picture
- Workshop participants who will try it themselves
- Team members who need context before reading the full article

## When to Use This Skill

Use this skill when:
- Creating presentation slides for a technical topic
- The user asks to create Slidev slides or a presentation
- Preparing materials for talks, workshops, or demos
- Creating visual companion to a Zenn article

## Slide Structure

**スライドの詳細な構造とテンプレートは `SLIDE_TEMPLATE.md` を参照してください。**

このテンプレートには以下が含まれています:
- スライドの完全な構成（タイトル、自己紹介、アジェンダ、問題提起、解決策、結果、まとめ）
- 各スライドタイプの具体的なレイアウトと例
- 必須チェックリスト
- よく使うコンポーネント集

### スライド構成の概要

1. **Title Slide (タイトルスライド)**: 問題と解決策を示す魅力的なタイトル
2. **Self Introduction (自己紹介)**: noguの紹介とXリンク
3. **Agenda (アジェンダ)**: 今日話す内容の全体像
4. **Problem Statement (問題提起)**: 共感できる具体的な課題
5. **Solution Overview (解決策の概要)**: 技術の簡潔な紹介
6. **Detailed Explanation (詳細説明)**: 実装ステップとコード例
7. **Results/Impact (結果・インパクト)**: 実際の成果と数値
8. **Key Takeaways (重要ポイント)**: 3つの持ち帰り
9. **Conclusion (まとめ)**: Thank you、記事へのリンク、フォローCTA（必須）

### 重要なポイント

- 1スライド1メッセージを徹底すること
- テキストは最小限に、ビジュアルを活用すること
- コード例は読みやすく、ハイライトで焦点を明確にすること
- スライドの最後に必ずフォローCTAと記事リンクを含めること

## Slidev Format Basics

### Frontmatter (First Slide)
```yaml
---
theme: default
background: https://source.unsplash.com/collection/94734566/1920x1080
class: text-center
highlighter: shiki
lineNumbers: false
info: |
  ## Presentation Title
  Brief description
drawings:
  persist: false
transition: slide-left
title: Presentation Title
mdc: true
---
```

### Common Layouts

**Cover Layout** - タイトルスライド
```markdown
---
layout: cover
---
# Title
## Subtitle
```

**Center Layout** - 中央揃えコンテンツ
```markdown
---
layout: center
---
# Centered Content
```

**Image Right Layout** - 右側に画像
```markdown
---
layout: image-right
image: /path/to/image
---
# Content
```

**Two Columns Layout** - 2カラム
```markdown
---
layout: two-cols
---
# Left
::right::
# Right
```

**Fact Layout** - 大きな数値や重要な事実
```markdown
---
layout: fact
---
# 80% Faster
Description
```

## Writing Style Guidelines

### Visual Rules

1. **One Idea Per Slide**
   - Each slide conveys a single concept
   - If explaining two ideas, use two slides

2. **Minimal Text**
   - Maximum 5-7 bullet points per slide
   - Use keywords, not full sentences (except for quotes)

3. **Visual Hierarchy**
   - Title: What this slide is about
   - Content: Supporting points
   - Action: What to remember/do

4. **Code Readability**
   - Show only relevant code snippets
   - Use syntax highlighting
   - Highlight key lines with `{line-numbers}`
   - Add explanatory comments

### Tone

- Professional but approachable
- Energetic and engaging
- Clear and concise
- Encouraging and inspiring

### Common Patterns

**Problem introduction**:
```markdown
# こんな経験ありませんか？

<v-clicks>

- 問題点1
- 問題点2
- 問題点3

</v-clicks>
```

**Solution introduction**:
```markdown
# The Solution

**Technology Name** solves this by:

<v-clicks>

- ✅ Benefit 1
- ✅ Benefit 2
- ✅ Benefit 3

</v-clicks>
```

**Code demonstration**:
````markdown
# Implementation

````md magic-move
```typescript
// Before
function oldWay() {
  // complex code
}
```

```typescript
// After: Simpler!
function newWay() {
  // clean code
}
```
````
````

## Visual Enhancement Components

### Click Animations (v-clicks)
Reveal content progressively:
```markdown
<v-clicks>

- First point (appears on click)
- Second point (appears on next click)
- Third point (appears on next click)

</v-clicks>
```

### Individual Click Animation
```markdown
<v-click>

This entire block appears on click

</v-click>
```

### Icons (UnoCSS icons)
```markdown
- <carbon:checkmark class="text-green-500"/> Success
- <carbon:warning class="text-yellow-500"/> Warning
- <carbon:information class="text-blue-500"/> Info
```

### Code Highlighting with Steps
````markdown
```typescript {2-4|6-8|all}
function example() {
  // Highlights on first click
  const a = 1;

  // Highlights on second click
  const b = 2;

  // Shows all on third click
}
```
````

### Magic Move (Smooth Code Transitions)
````markdown
````md magic-move
```typescript
// Step 1: Simple
const value = 1;
```

```typescript
// Step 2: Evolves
const value = 1;
const enhanced = value * 2;
```

```typescript
// Step 3: Complete
const value = 1;
const enhanced = value * 2;
return enhanced;
```
````
````

## Slidev-Specific Features

### Presenter Notes
Only visible in presenter mode:
```markdown
---
# Slide content
---

<!--
Notes for presenter:
- Key point to emphasize
- Demo to run
- Timing reminder
-->
```

### Custom Styling
```markdown
<style>
.custom-class {
  color: #4EC5D4;
  font-weight: bold;
}
</style>
```

### Interactive Components
```markdown
<div @click="$slidev.nav.next" class="cursor-pointer">
  Click to continue →
</div>
```

## Quality Checklist

Before completing slides, verify:

- [ ] Title slide includes problem and solution hint
- [ ] Self-introduction includes nogu profile and X link
- [ ] Agenda shows clear structure (Problem → Solution → Result)
- [ ] Problem statement is relatable and concrete
- [ ] Each slide has one clear message
- [ ] Text is minimal (keywords, not paragraphs)
- [ ] Code examples are focused and highlighted
- [ ] Visual hierarchy is clear on every slide
- [ ] Animations enhance understanding (not just decoration)
- [ ] Key takeaways are actionable (3 main points)
- [ ] Conclusion includes thank you, article link, and follow CTA
- [ ] Slides work in both presentation and handout mode

## Anti-Patterns to Avoid

**Don't**:
- Cram multiple ideas on one slide
- Use tiny fonts or too much text
- Show entire code files without highlighting
- Skip the problem statement
- Use animations excessively (distraction)
- Forget to link back to the detailed article
- Have slides with no clear purpose

**Do**:
- Keep it visual and scannable
- Use progressive disclosure (v-clicks)
- Tell a compelling narrative
- Make code readable from the back row
- Guide audience attention deliberately
- End with clear next steps and CTA
- Make slides useful even without presenter

## Integration with Zenn Articles

When creating slides for a Zenn article:

1. **Same Problem Focus**: Start with the same problem the article solves
2. **Complementary Depth**:
   - Article: Deep dive with complete code
   - Slides: High-level overview with key snippets
3. **Cross-Reference**: Include article link in conclusion
4. **Consistent Message**: Same solution, different format
5. **Visual Emphasis**: Use slides to show what article tells

## File Organization

Save presentations in:
```
Outputs/Slidev/presentations/[topic-slug]/slides.md
```

Example:
```
Outputs/Slidev/presentations/trae-cue-ai-development/slides.md
```

## Preview Slides Locally

```bash
# Navigate to presentation directory
cd Outputs/Slidev/presentations/[topic-slug]

# Start Slidev dev server
npx slidev slides.md

# Or if Slidev is installed globally
slidev slides.md
```

## Export Options

```bash
# Export to PDF
npx slidev export slides.md

# Export to single-page HTML
npx slidev build slides.md
```

## Remember

Great presentation slides are:
- **Visual**: Show, don't just tell
- **Focused**: One clear message per slide
- **Engaging**: Use animations purposefully
- **Narrative**: Tell a story with clear flow
- **Actionable**: Audience knows what to do next
- **Accessible**: Readable and understandable at a glance

The goal is to make complex technical topics memorable and actionable through visual storytelling. Slides complement articles by providing the "highlight reel" that inspires people to read the full story.
