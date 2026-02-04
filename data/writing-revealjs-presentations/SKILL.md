---
name: writing-revealjs-presentations
description: Use when creating or editing reveal.js presentations, or when user mentions slides, presentations, reveal.js, code examples in slides, speaker notes, or slide design - enforces Tailwind CSS, proper code sizing, progressive reveal, semantic colors, and timing markers
---

# Writing reveal.js Presentations

**Core principle:** Every reveal.js feature must serve a communication purpose.

## Pre-Flight Check (MANDATORY)

**Before ANY work, scan existing presentation:**

```
□ Inline style= attributes found?
□ .slide1, .slide2 CSS classes found?

If YES to either → Refactor ENTIRE presentation first
```

**Also check for:**
```
□ Code examples present? Plan for proper sizing (text-base minimum, never smaller than body text)
□ Technical content? Add detailed speaker notes with timing markers (3-5x slide content)
□ Complex concepts? Plan progressive reveal with fragments
□ Creating new presentation? Use typography scale and semantic colors from start
```

**Refactoring workflow when anti-patterns detected:**

1. Say to user: "I'll refactor to Tailwind CSS while maintaining your colors/aesthetic, then add new slides."
2. Add Tailwind CDN: `<script src="https://cdn.tailwindcss.com"></script>`
3. Refactor ALL slides: Remove `style=` and `.slideN` classes, replace with Tailwind + `data-background-*`
4. Then proceed with user's request

**"Same style" = same colors/visual design, NOT same implementation.**

**If you extend bad patterns instead of refactoring, you have violated this skill.**

## Core Patterns

### Essential CDN Setup

**In `<head>`:**
```html
<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/reveal.js@5.0.4/dist/reveal.css">
<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/reveal.js@5.0.4/dist/theme/black.css">
<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/reveal.js@5.0.4/plugin/highlight/monokai.css">
<script src="https://cdn.tailwindcss.com"></script>
```

**Before `</body>`:**
```html
<script src="https://cdn.jsdelivr.net/npm/reveal.js@5.0.4/dist/reveal.js"></script>
<script src="https://cdn.jsdelivr.net/npm/reveal.js@5.0.4/plugin/markdown/markdown.js"></script>
<script src="https://cdn.jsdelivr.net/npm/reveal.js@5.0.4/plugin/highlight/highlight.js"></script>
<script src="https://cdn.jsdelivr.net/npm/reveal.js@5.0.4/plugin/notes/notes.js"></script>
<script>
  Reveal.initialize({ /* see Essential Configuration */ });
</script>
```

Use v5.0.4+.

### Tailwind CSS for All Styling

**Usage:**
```html
<!-- ✅ GOOD -->
<section data-background-color="#1e293b">
  <h1 class="text-6xl font-bold text-slate-100 mb-8">Title</h1>
</section>

<!-- ❌ BAD -->
<section class="slide1" style="background: red;">
  <h1 style="font-size: 48px;">Title</h1>
</section>
```

### Standard CSS Overrides (REQUIRED)

**Add in `<style>` tag after Tailwind:**

```html
<style>
  .reveal pre { width: 100%; margin: 0; }
  .reveal pre code { max-height: none; padding: 1rem; }
  .reveal h1, .reveal h2, .reveal h3 { text-transform: none; }
  .reveal ul, .reveal ol { display: block; }
</style>
```

Fixes reveal.js defaults: code block sizing, UPPERCASE headings, list rendering.

### Purpose-Driven Effects

**NOT valid purposes:** "Draws attention", "looks cool", "makes it engaging", "user asked for flashy"

**ACTUAL purposes:** Shows transformation, implies progression, emphasizes relationship, indicates topic change

```html
<!-- ✅ Shows transformation -->
<section data-auto-animate>
  <div data-id="box" class="h-12 w-12 bg-blue-500"></div>
</section>
<section data-auto-animate>
  <div data-id="box" class="h-48 w-48 bg-blue-500"></div>
</section>

<!-- ❌ Effect without purpose -->
<section data-transition="zoom">
  <h1>Features</h1>
</section>
```

**Default:** `data-transition="slide"` or none unless you have specific reason.

### Content Structure

| Pattern | Use For | Code |
|---------|---------|------|
| Horizontal slides | Main narrative flow | `<section>Topic</section>` |
| Vertical slides | Optional detail on topic | Nested `<section>` |
| Fragments | Progressive reveal | `class="fragment"` |

```html
<section><!-- Main point -->
  <section><h2>Overview</h2></section>
  <section><!-- Vertical: detail --><h3>Details</h3></section>
</section>
```

### Speaker Notes (MANDATORY)

**Every slide must have properly formatted speaker notes.**

```html
<aside class="notes">
  <p><strong>Key Points:</strong></p>
  <ul>
    <li>Point 1 with context</li>
    <li>Point 2 with timing</li>
  </ul>
  <p>Additional detail for presenter.</p>
</aside>
```

**Format requirements:**
- Use `<p>`, `<ul>`/`<ol>`, `<strong>`/`<em>`
- Break up long text for legibility

## Code Examples in Slides

**CRITICAL RULE: Code font size must be >= body text font size. Check body text size FIRST, then match or exceed it for code.**

```html
<!-- ✅ GOOD: Code matches body text size -->
<p class="text-xl">Explanation text</p>
<pre><code class="language-javascript text-xl" data-trim>
function example() {
  return "Same size as body text";
}
</code></pre>

<!-- ❌ BAD: Code smaller than body text -->
<p class="text-xl">Explanation text</p>
<pre><code class="language-javascript text-base" data-trim>
// WRONG: text-base (16px) < text-xl (20px)
</code></pre>
```

**Formatting rules:**
- **STEP 1:** Identify body text size on your slide (`text-xl`, `text-lg`, `text-base`, etc.)
- **STEP 2:** Set code size to match or exceed: If body is `text-xl`, code must be `text-xl` or larger
- Always use `data-trim` to remove indentation
- Use specific language classes: `language-yaml`, `language-bash`, `language-javascript`, etc.
- Limit to 3-8 lines per block - split longer examples across slides

**If code doesn't fit:** Reduce code lines (3-8 max), split across slides, or reduce BOTH body and code text sizes together.

**Progressive code highlighting:**

```html
<pre><code data-line-numbers="1-6|8-12|14-17">
def initialize(name)
  @name = name
end

def lifecycle_renew
  save
end
</code></pre>
```

**Format:** `data-line-numbers="1-6|8-12"` - pipe separates fragments. Also: `"1|2-3|4"` or `"5,8,11"`.

Use for step-by-step explanations. Skip for simple examples or single-line highlights (click fatigue).

**Progressive reveal with fragments:**
```html
<div>
  <p>First explain the concept</p>
  <pre class="fragment"><code class="language-python text-base" data-trim>
    # Code appears after explanation
    def example():
        return "builds understanding"
  </code></pre>
</div>
```

## Typography Scale Reference

**Hierarchy for presentations (optimized for projectors):**

| Element | Classes | Use For |
|---------|---------|---------|
| Main title | `text-6xl font-bold` | Opening slide title |
| Section header | `text-4xl` or `text-5xl font-bold` | Slide titles |
| Subsection | `text-2xl` or `text-3xl font-semibold` | Sub-headings |
| Body text | `text-xl` | Main content |
| Supporting text | `text-base` or `text-lg` | Details |
| Code blocks | `text-base` or `text-lg` | **Never smaller than body text** |
| Footnotes | `text-sm` | Minor details only |

**CRITICAL RULE: Code font size must be >= body text font size. NO EXCEPTIONS.**

**Examples - Body text at different sizes:**
- Body text `text-2xl` → Code must be `text-2xl` or larger
- Body text `text-xl` → Code must be `text-xl` or larger
- Body text `text-lg` → Code must be `text-lg` or larger
- Body text `text-base` → Code must be `text-base` or larger

**If code doesn't fit at required size:**
1. Reduce lines of code (3-8 lines max per block)
2. Split across multiple slides with fragments
3. Use smaller body text size (and match code size down)
4. **NEVER reduce code size below body text**

**Why this matters:** Projectors and distance viewing make code the hardest content to read. It must never be smaller than body text.

## Semantic Color Patterns

Use Tailwind color utilities to reinforce meaning:

| Purpose | Color | Example Classes |
|---------|-------|-----------------|
| Positive/Good/Success | Green | `text-green-300`, `text-green-400`, `bg-green-900` |
| Negative/Bad/Error | Red | `text-red-300`, `text-red-400`, `bg-red-900` |
| Warning/Caution | Yellow | `text-yellow-300`, `text-yellow-400`, `bg-yellow-900` |
| Neutral/Info/Refactor | Blue | `text-blue-300`, `text-blue-400`, `bg-blue-900` |
| Subdued/Meta | Slate | `text-slate-400`, `text-slate-500` |

**Slide backgrounds:** Alternate `#1e293b` (odd slides) and `#0f172a` (even slides) for visual rhythm.

**Accessibility:** Don't rely on color alone - use symbols (✅/❌) or text labels too.

## Speaker Notes with Timing Markers

**MANDATORY: Every slide must have detailed speaker notes with timing estimates.**

```html
<aside class="notes">
  <p><strong>Introduction (30 seconds):</strong></p>
  <ul>
    <li>Open with relatable scenario</li>
    <li>Pause for audience reaction</li>
    <li>Transition to solution</li>
  </ul>
  <p><strong>Delivery tip:</strong> Make eye contact before revealing next fragment.</p>
</aside>
```

**Requirements:**
- Include timing estimate for each section: "(30 seconds)", "(60 seconds)", etc.
- Detail ratio: Notes should contain 3-5x more context than visible on slides
- Structure: Bold headings, bulleted points, delivery tips
- Content: Not just slide recap - include transitions, audience engagement, what to emphasize

**Template:**

```html
<aside class="notes">
  <p><strong>Section Name (XX seconds):</strong></p>
  <ul>
    <li>Key point with context and transitions</li>
    <li>What to emphasize or pause for</li>
  </ul>
  <p><strong>Delivery tip:</strong> Tone/pacing guidance.</p>
</aside>
```

**Time per slide by talk length:**

| Talk Length | Per Slide |
|-------------|-----------|
| 5 min | 20-30s |
| 10 min | 45-60s |
| 20 min | 60-90s |
| 45-60 min | 90-120s |

**10-minute talk breakdown (10 slides):**
Opening (60s) → Context (90s, 2 slides) → Solution (240s, 4 slides) → Conclusion (90s, 2 slides) → Q&A (60s)

## Multi-Column Layouts

**Use Tailwind grid for side-by-side comparisons:**

```html
<!-- Two-column comparison (good vs bad, before vs after) -->
<div class="grid grid-cols-2 gap-8">
  <div>
    <h3 class="text-3xl text-red-400 mb-4">❌ Before</h3>
    <pre><code class="language-python text-base" data-trim>
      # Old approach
    </code></pre>
  </div>
  <div>
    <h3 class="text-3xl text-green-400 mb-4">✅ After</h3>
    <pre><code class="language-python text-base" data-trim>
      # New approach
    </code></pre>
  </div>
</div>
```

**Use `gap-4`, `gap-6`, or `gap-8` for spacing. Larger gap for dense content.**

## Progressive Reveal Patterns

**When to use fragments:**
- Building up complex concepts step-by-step
- Revealing answers after questions
- Showing multiple examples sequentially
- Pacing discussion points

**When NOT to use fragments:**
- Simple lists where order doesn't matter
- Content that makes sense as a whole
- Every single line (causes "click fatigue")

```html
<!-- ✅ GOOD: Build up complexity -->
<div>
  <p class="text-2xl mb-4">First introduce the concept</p>
  <ul class="text-xl space-y-2">
    <li class="fragment">Then first detail</li>
    <li class="fragment">Then second detail</li>
  </ul>
  <pre class="fragment"><code>...example code appears last</code></pre>
</div>

<!-- ❌ BAD: Every line fragmented -->
<p class="fragment">This</p>
<p class="fragment">causes</p>
<p class="fragment">click</p>
<p class="fragment">fatigue</p>
```

**Fragment modifiers:**
- `fragment fade-in` - Default
- `fragment fade-in-then-semi-out` - Highlight then dim
- `fragment highlight-current-blue` - Highlight temporarily

## Editing Existing Presentations

**When adding to or modifying existing presentations:**

1. **Read entire file first** - Understand full structure and patterns
2. **Identify and match patterns:**
   - Background colors: Note alternating pattern (e.g., #1e293b, #0f172a)
   - Typography: Check existing heading sizes, body text sizes
   - Code blocks: Match existing code font size (`text-base` or `text-lg`)
   - Speaker notes: Match existing format (timing markers, detail level)
   - Fragment usage: Follow existing progressive reveal patterns
3. **Update related content:**
   - If changing slide content, update speaker notes to match
   - Maintain semantic color usage (green=good, red=bad, etc.)
   - Keep same transition style throughout
4. **Verify rendering:**
   - All changes display correctly
   - No overflow or layout breaks
   - Consistent with surrounding slides

**What to preserve:**
- Color palette and background patterns
- Typography scale hierarchy
- Code sizing conventions
- Speaker note format and detail level
- Fragment usage patterns

**What to refactor anyway:**
- Inline styles → Tailwind CSS (always)
- Class-based slides → data-background-* attributes (always)
- Missing speaker notes → Add with timing markers (always)
- Code smaller than body text → Fix to text-base minimum (always)

## Quick Reference

| Feature | Example |
|---------|---------|
| CDN version | reveal.js v5.0.4+, Tailwind CDN |
| CSS overrides | `.reveal pre { width: 100%; }` etc. (REQUIRED) |
| Tailwind styling | `class="text-4xl font-bold text-blue-600"` |
| Slide backgrounds | `data-background-color="#1e293b"` (alternate #0f172a) |
| Code blocks | `<code class="language-python text-base" data-trim>` |
| Code highlighting | `data-line-numbers="1-6\|8-12"` (pipe = fragments) |
| Speaker notes | `<aside class="notes"><p><strong>Topic (60s):</strong></p><ul>...</ul></aside>` |
| Fragments | `<li class="fragment">Item</li>` (build complexity, not click fatigue) |
| Multi-column | `<div class="grid grid-cols-2 gap-8">` |
| Semantic colors | Green=good, Red=bad, Yellow=warning, Blue=neutral |
| Typography scale | Code >= body text (`text-base` min for code, `text-xl` for body) |
| Auto-animate | Same `data-id` across slides |
| Overview mode | Press ESC/O |

## Essential Configuration

```javascript
Reveal.initialize({
  slideNumber: 'c/t',
  hash: true,
  width: '100%',
  height: '100%',
  transition: 'slide',
  controls: true,
  progress: true,
  keyboard: true,
  overview: true,
  plugins: [ RevealMarkdown, RevealHighlight, RevealNotes ]
});
```

**`plugins` array required** for syntax highlighting and speaker notes.

## Workflow

**STEP 0:** Pre-flight check (above) - refactor if needed

1. Set up Tailwind if not present
2. Plan structure: horizontal (main) vs vertical (detail)
3. Content on slides: high-level only
4. Add formatted speaker notes with timing markers to ALL slides
5. Detail in notes, not on slides
6. Add effects LAST (only where they serve purpose)
7. Verify rendering:
   - Code examples: Syntax highlighting works, `text-base` or `text-lg` sizing (never smaller than body text)
   - Fragments: Progressive reveal works as intended, no "click fatigue"
   - Multi-column: Grid layouts don't overflow or break
   - Speaker notes: Detailed with timing markers for every slide
   - Colors: Semantic meaning clear (green=good, red=bad), sufficient contrast, symbols complement colors
   - Typography: Heading hierarchy consistent, code >= body text size

## Common Rationalizations (STOP)

| If you think... | Reality |
|----------------|---------|
| "Maintain visual consistency" with inline styles | STOP. Refactor to Tailwind |
| "Avoid introducing complexity" | STOP. Bad code IS complex |
| "Original didn't use Tailwind" | STOP. Refactor anyway |
| "This transition draws attention" | STOP. Define actual communication goal |
| "Slide structure guides narrative" | STOP. Add speaker notes anyway |
| "User asked for it quickly" | STOP. Refactoring is faster than tech debt |
| "Code will be readable at default size" | STOP. Set `text-base` or `text-lg` explicitly - never smaller than body text |
| "Presenter can ad-lib this section" | STOP. Add detailed speaker notes with timing markers anyway |
| "Need to show complete code example" | STOP. Split into 3-8 line chunks across slides with fragments |
| "Text-sm fits more code in two columns" | STOP. Use `text-base`, reduce code lines, or make columns wider |
| "Speaker notes take too long to write" | STOP. 3-5x detail ratio is mandatory - saves presenter time during talk |
| "Fragments on everything make it interactive" | STOP. Causes click fatigue - use only for building complexity |
| "Monospace is more readable at smaller sizes" | STOP. Code must be >= body text size - non-negotiable |
| "Balance readability and space" | STOP. Reduce code lines or use larger body text - code size is fixed |
| "Code slightly smaller is fine" | STOP. **NO EXCEPTIONS** - code >= body text always |

## Accessibility Checklist

- [ ] Semantic HTML (heading hierarchy)
- [ ] Keyboard navigation (Tab, arrows, ESC)
- [ ] Speaker notes provide context
- [ ] Color contrast sufficient
- [ ] No information by color alone
- [ ] Alt text for images
