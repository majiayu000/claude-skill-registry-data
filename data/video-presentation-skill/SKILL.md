---
name: video-presentation-skill
description: Generate interactive HTML presentations for ANY video type (tutorials, comparisons, fact-checks, explainers, etc.). Creates self-contained, screen-recording-optimized slides with various content types including comparisons, steps, code blocks, calculators, and verdicts. Use when user wants visual aids for their videos.
---

# Video Presentation Generator

## Overview

This skill creates self-contained HTML presentations optimized for screen recording in YouTube videos. Works for ANY video type - tutorials, comparisons, fact-checks, reviews, explainers, and more.

**Key Features:**
- Single HTML file (no external dependencies)
- Click anywhere or press any key to advance
- Multiple theme options
- Various slide types for different content needs
- Optimized for 1080p screen recording
- Progressive reveal animations

---

## When to Use

Invoke this skill when:
- User says "create a presentation", "make slides", "I need visual aids"
- After generating any video script that would benefit from on-screen graphics
- When a script has comparison sections, step-by-step processes, or data to display
- User wants professional-looking slides for screen recording

---

## Workflow

### Step 1: Gather Context

If not already known, ask:

**Question 1: Video Context**
```
"What type of video is this presentation for?"
Header: "Video Type"
Options:
- Tutorial / How-to
- Comparison / Review
- Fact-check / Debunk
- Explainer / Educational
```

### Step 2: Design Preferences

**Question 2: Visual Theme**
```
"What visual theme do you want?"
Header: "Theme"
Options:
- Dark Tech (teal accent) [Recommended for tech/AI content]
- Dark Finance (green accent) [Recommended for finance content]
- Dark Creative (purple accent)
- Light Clean (blue accent)
- Warm (amber accent)
```

### Step 3: Slide Content

**Question 3: Slide Types (Multi-Select)**
```
"What slide types do you need?"
Header: "Slides"
Options (multi-select):
- Title slide
- Text/bullet points
- Comparison (A vs B, Before/After, Claims vs Reality)
- Steps/Process (numbered walkthrough)
- Statistics/Numbers (animated reveal)
- Code blocks (syntax highlighted)
- Calculator (step-by-step math)
- Quote slide
- Verdict/Conclusion (with icon)
- Source citations
- Call-to-action
```

### Step 4: Animation Style

**Question 4: Reveal Style**
```
"How should content reveal?"
Header: "Animations"
Options:
- Progressive reveal (one element per click) [Recommended]
- Full slide at once
- Typewriter effect for text
```

### Step 5: Gather Specific Content

Based on selected slide types, ask for:
- Title slide: Main title, subtitle, label text
- Comparison: Left side content, right side content, headers
- Steps: List of steps with descriptions
- Statistics: Numbers, labels, whether to animate
- Code: Code snippet, language for highlighting
- Calculator: Steps of calculation, final result
- Quote: Quote text, attribution
- Verdict: TRUE/FALSE/MISLEADING, explanation

### Step 6: Generate HTML Presentation

Use the template at `~/YT/_Templates/video-presentation-template.html` as the base and customize:
- Apply selected theme colors
- Insert slide content
- Configure animations
- Set up navigation

Save to the video project's `04_Assets/Graphics/` folder.

### Step 7: Provide Usage Instructions

```
Your presentation is ready at:
[path]/presentation.html

To use in your recording:
1. Open the HTML file in Chrome
2. Press F11 for fullscreen
3. Start your screen recording
4. Click anywhere or press any key to advance
5. Press 'N' to toggle presenter notes (won't show in recording)
```

---

## Slide Types Reference

### Title Slide
```html
<div class="slide title-slide">
  <p class="slide-label">[LABEL TEXT]</p>
  <h1>[MAIN TITLE with <span class="highlight">highlighted</span> words]</h1>
  <p class="subtitle">[Subtitle text]</p>
</div>
```

### Text/Points Slide
```html
<div class="slide">
  <p class="slide-label">[SECTION LABEL]</p>
  <h2>[Section Title]</h2>
  <ul class="points-list">
    <li class="point-item">
      <div class="point-icon">[EMOJI]</div>
      <div class="point-content">
        <h3>[Point Title]</h3>
        <p>[Point description]</p>
      </div>
    </li>
    <!-- More points -->
  </ul>
</div>
```

### Comparison Slide
```html
<div class="slide comparison-slide">
  <p class="slide-label">[LABEL]</p>
  <h2>[Title]</h2>
  <div class="comparison-container">
    <div class="comparison-side left [warning/neutral]">
      <div class="comparison-header">
        <span class="comparison-icon">[ICON]</span>
        <h3>[Left Header]</h3>
      </div>
      <ul class="comparison-points">
        <li>[Point 1]</li>
        <li>[Point 2]</li>
      </ul>
    </div>
    <div class="comparison-divider">
      <span class="vs-badge">VS</span>
    </div>
    <div class="comparison-side right [success/neutral]">
      <div class="comparison-header">
        <span class="comparison-icon">[ICON]</span>
        <h3>[Right Header]</h3>
      </div>
      <ul class="comparison-points">
        <li>[Point 1]</li>
        <li>[Point 2]</li>
      </ul>
    </div>
  </div>
</div>
```

### Steps/Process Slide
```html
<div class="slide steps-slide">
  <p class="slide-label">[LABEL]</p>
  <h2>[Title]</h2>
  <div class="steps-container">
    <div class="step-item">
      <div class="step-number">1</div>
      <div class="step-content">
        <h3>[Step Title]</h3>
        <p>[Step description]</p>
      </div>
    </div>
    <!-- More steps -->
  </div>
</div>
```

### Statistics/Numbers Slide
```html
<div class="slide stats-slide">
  <p class="slide-label">[LABEL]</p>
  <h2>[Title]</h2>
  <div class="stats-grid">
    <div class="stat-card" data-animate="true" data-target="87" data-suffix="%">
      <div class="stat-number">0%</div>
      <p class="stat-label">[Description of stat]</p>
    </div>
    <!-- More stat cards -->
  </div>
</div>
```

### Code Slide
```html
<div class="slide code-slide">
  <p class="slide-label">[LABEL]</p>
  <h2>[Title]</h2>
  <div class="code-container">
    <div class="code-header">
      <span class="code-lang">[language]</span>
      <span class="code-filename">[filename.ext]</span>
    </div>
    <pre class="code-block"><code>[code content with syntax classes]</code></pre>
  </div>
</div>
```

### Calculator Slide
```html
<div class="slide calculator-slide">
  <p class="slide-label">[LABEL]</p>
  <h2>[Title]</h2>
  <div class="calculator-steps">
    <div class="calc-step" data-step="1">
      <span class="calc-expression">[expression]</span>
      <span class="calc-result">= [result]</span>
    </div>
    <!-- More steps - each reveals on click -->
    <div class="calc-final">
      <span class="final-label">[Label]</span>
      <span class="final-value">[Final Value]</span>
    </div>
  </div>
</div>
```

### Quote Slide
```html
<div class="slide quote-slide">
  <div class="quote-container">
    <div class="quote-icon">"</div>
    <blockquote class="quote-text">[Quote text]</blockquote>
    <p class="quote-attribution">— [Attribution]</p>
    <p class="quote-source">[Source if applicable]</p>
  </div>
</div>
```

### Verdict Slide
```html
<div class="slide verdict-slide verdict-[true/false/misleading/info]">
  <div class="verdict-container">
    <div class="verdict-icon-wrapper">
      <span class="verdict-icon">[✓/✗/⚠/ℹ]</span>
    </div>
    <h2 class="verdict-label">[TRUE/FALSE/MISLEADING/INFO]</h2>
    <h3 class="verdict-title">[Claim or Topic]</h3>
    <p class="verdict-explanation">[Explanation text]</p>
  </div>
</div>
```

### Source Citation Slide
```html
<div class="slide source-slide">
  <p class="slide-label">Source</p>
  <h2>[Source Title]</h2>
  <div class="source-container">
    <div class="source-icon">🔗</div>
    <p class="source-url">[Shortened URL for display]</p>
    <p class="source-note">[Additional context about the source]</p>
  </div>
</div>
```

### Call-to-Action Slide
```html
<div class="slide cta-slide">
  <p class="slide-label">[LABEL]</p>
  <h1>[CTA Headline with <span class="highlight">highlight</span>]</h1>
  <p class="subtitle">[Supporting text]</p>
  <div class="cta-buttons">
    <button class="cta-btn primary">[Primary Action]</button>
    <button class="cta-btn secondary">[Secondary Action]</button>
  </div>
</div>
```

---

## Theme Colors

### Dark Tech (Default)
```css
--bg-dark: #0a0a0f;
--bg-card: #12121a;
--accent-primary: #00d4aa;    /* Teal */
--accent-secondary: #7c3aed;  /* Purple */
--text-primary: #f0f0f5;
--text-secondary: #9090a0;
```

### Dark Finance
```css
--bg-dark: #0a0a0f;
--bg-card: #12121a;
--accent-primary: #22c55e;    /* Green */
--accent-secondary: #10b981;  /* Emerald */
--text-primary: #f0f0f5;
--text-secondary: #9090a0;
```

### Dark Creative
```css
--bg-dark: #0a0a0f;
--bg-card: #12121a;
--accent-primary: #8b5cf6;    /* Purple */
--accent-secondary: #ec4899;  /* Pink */
--text-primary: #f0f0f5;
--text-secondary: #9090a0;
```

### Light Clean
```css
--bg-dark: #f8fafc;
--bg-card: #ffffff;
--accent-primary: #3b82f6;    /* Blue */
--accent-secondary: #06b6d4;  /* Cyan */
--text-primary: #1e293b;
--text-secondary: #64748b;
```

### Warm
```css
--bg-dark: #1c1917;
--bg-card: #292524;
--accent-primary: #f59e0b;    /* Amber */
--accent-secondary: #ef4444;  /* Red */
--text-primary: #fafaf9;
--text-secondary: #a8a29e;
```

---

## Verdict Colors

```css
/* TRUE - Green */
.verdict-true { --verdict-color: #22c55e; }

/* FALSE - Red */
.verdict-false { --verdict-color: #ef4444; }

/* MISLEADING - Amber */
.verdict-misleading { --verdict-color: #f59e0b; }

/* INFO/CONTEXT-NEEDED - Blue */
.verdict-info { --verdict-color: #3b82f6; }
```

---

## Animation Classes

### Slide Transitions
```css
.slide {
  opacity: 0;
  transform: translateX(100px);
  transition: all 0.7s cubic-bezier(0.4, 0, 0.2, 1);
}

.slide.active {
  opacity: 1;
  transform: translateX(0);
}
```

### Staggered Element Reveal
```css
.slide.active .animate-item:nth-child(1) { transition-delay: 0.2s; }
.slide.active .animate-item:nth-child(2) { transition-delay: 0.3s; }
.slide.active .animate-item:nth-child(3) { transition-delay: 0.4s; }
/* etc. */
```

### Number Counter Animation (JavaScript)
```javascript
function animateNumber(element, target, duration = 1000) {
  const start = 0;
  const increment = target / (duration / 16);
  let current = start;

  const timer = setInterval(() => {
    current += increment;
    if (current >= target) {
      element.textContent = formatNumber(target);
      clearInterval(timer);
    } else {
      element.textContent = formatNumber(Math.floor(current));
    }
  }, 16);
}
```

---

## Progressive Reveal Mode

When "Progressive reveal" is selected, the presentation works as follows:

1. First click: Slide appears with first element
2. Subsequent clicks: Each element reveals in sequence
3. When all elements shown: Next click advances to next slide

This is controlled by data attributes:
```html
<div class="slide" data-reveal="progressive" data-reveal-count="5">
  <!-- Elements with data-reveal-index="1", "2", etc. -->
</div>
```

---

## File Output

Save the generated presentation to:
```
~/YT/[Video Project]/04_Assets/Graphics/[topic]-presentation.html
```

Example:
```
~/YT/Covered Calls Fact Check/04_Assets/Graphics/covered-calls-presentation.html
```

---

## Integration with Other Skills

### From /finance-commentary

When called from finance-commentary, context is pre-filled:
- Video type: Fact-check
- Theme: Dark Finance
- Recommended slides based on script content

### From /video-research

When called after video research:
- Video type: Based on content type identified
- Theme: Dark Tech (default for this channel)
- Recommended slides based on video ideas generated

### Standalone Usage

When called directly (`/video-presentation`), ask all questions from scratch.

---

## Example Interaction

```
User: Create a presentation for my Claude Code tutorial

Claude: I'll create an interactive presentation for your tutorial.

[Asks Question 1: Video Type]
User: Tutorial / How-to

[Asks Question 2: Theme]
User: Dark Tech (teal accent)

[Asks Question 3: Slide Types]
User: Title slide, Steps/Process, Code blocks, Statistics

[Asks Question 4: Animation Style]
User: Progressive reveal

Claude: Great! Now let me gather the content for each slide type.

For the Title slide:
- What's the main title?
- Any subtitle?
- Label text (e.g., "Tutorial", "Guide")?

[Continues gathering content for each selected slide type]

[Generates HTML presentation]

Done! Your presentation is saved at:
~/YT/Claude Code Tutorial/04_Assets/Graphics/tutorial-presentation.html

**Slides created:**
1. Title: "Master Claude Code in 10 Minutes"
2. Steps: 5-step process overview
3. Code: Example configuration
4. Stats: Performance improvements

**To use:**
1. Open in Chrome → F11 fullscreen
2. Start OBS recording
3. Click to advance (14 total clicks)
4. Press 'N' for presenter notes
```

---

## Keyboard Shortcuts

| Key | Action |
|-----|--------|
| → / Space / Click | Next slide/element |
| ← | Previous slide |
| N | Toggle presenter notes |
| F11 | Fullscreen |
| 1-9 | Jump to slide number |
| Home | First slide |
| End | Last slide |
