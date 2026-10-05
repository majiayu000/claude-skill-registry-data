---
name: ai-vibe-slides
description: "Create beautiful, professional HTML or React slide decks ready for fullscreen presentation. Use this skill when the user wants to: create a PPT/slide/presentation from an idea or outline; build a visually stunning slide deck from existing content; generate an HTML presentation that can be projected fullscreen; convert a document into a presentation. Trigger when you hear: 'create slides', 'make a PPT', 'presentation', 'slide deck', 'pitch deck', 'vibe ppt', 'make a talk', or any request to create a presentation. This skill produces a single self-contained HTML/React artifact — no backend, no installation, no dependencies."
---

# AI Vibe Slides — Beautiful HTML Slide Decks, Ready to Present

## Goal

Produce **a single HTML or React artifact file** containing a complete slide deck that can:

- Present fullscreen directly in the browser
- Navigate via arrow keys, spacebar, or click
- Look professional, polished, and stylistically consistent
- Print or export to PDF when needed

Inspired by [banana-slides](https://github.com/Anionex/banana-slides): a 3-step pipeline of **Idea → Outline → Finished Slides**, but the output is a self-contained HTML file instead of a fullstack application.

---

## Slide Creation Pipeline

### Step 1: Understand the Request → Build an Outline

When the user provides a request, first **build an outline mentally** (no need to display it unless the user asks):

1. Identify the **main topic** and **target audience** (students, business, tech talk...)
2. Break it into **logical sections**:
   - Slide 1: Cover (title + subtitle + author)
   - Slides 2-3: Introduction / context
   - Middle slides: Core content (one key idea per slide)
   - Final slide: Conclusion / Call to action / Thank you
3. Each slide should have: a title, 2-5 bullet points or visual content, and a layout type

If the user only gives a short sentence (e.g., "create slides about AI in healthcare"), automatically expand it into 8-12 slides with a logical structure.

### Step 2: Choose a Design Direction

Based on context, commit to **one clear design direction**:

| Context                | Suggested Style                                       |
| ---------------------- | ----------------------------------------------------- |
| Startup pitch deck     | Bold, dark theme, gradient accents, strong sans-serif |
| Academic / education   | Clean, light, diagram-heavy, readable fonts           |
| Tech talk / conference | Modern dark, code-style typography, neon accents      |
| Corporate / report     | Minimal, professional, navy/white, serif headings     |
| Creative / marketing   | Colorful, asymmetric layout, bold typography          |
| Kids / early education | Pastel, rounded corners, playful icons, large text    |

General rules:

- **Pick 2-3 primary colors** and use them consistently across the entire deck
- **1 heading font + 1 body font** (use Google Fonts)
- **Minimal text, generous whitespace** — max 5-6 lines per slide
- **Clear visual hierarchy**: large title → medium content → small notes

### Step 3: Generate the HTML/React Slide Deck

Create **a single file** (`.html` or `.jsx`) containing everything:

---

## HTML Slide Deck Structure

```html
<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>{Presentation Title}</title>
    <link
      href="https://fonts.googleapis.com/css2?family={Font1}&family={Font2}&display=swap"
      rel="stylesheet"
    />
    <style>
      /* === RESET + BASE === */
      * {
        margin: 0;
        padding: 0;
        box-sizing: border-box;
      }

      /* === SLIDE CONTAINER === */
      .slide-deck {
        width: 100vw;
        height: 100vh;
        overflow: hidden;
        position: relative;
      }
      .slide {
        width: 100%;
        height: 100%;
        display: none;
        flex-direction: column;
        justify-content: center;
        padding: 60px 80px;
        position: absolute;
        top: 0;
        left: 0;
      }
      .slide.active {
        display: flex;
      }

      /* === TYPOGRAPHY === */
      h1 {
        font-family: "{Font1}", sans-serif;
        font-size: 3.2rem;
        margin-bottom: 1rem;
      }
      h2 {
        font-family: "{Font1}", sans-serif;
        font-size: 2.4rem;
        margin-bottom: 1.5rem;
      }
      p,
      li {
        font-family: "{Font2}", sans-serif;
        font-size: 1.4rem;
        line-height: 1.8;
      }

      /* === THEME COLORS === */
      :root {
        --bg-primary: #0f172a;
        --bg-slide: #1e293b;
        --text-primary: #f8fafc;
        --text-secondary: #94a3b8;
        --accent: #3b82f6;
        --accent-2: #8b5cf6;
      }

      /* === NAVIGATION UI === */
      .nav-hint {
        position: fixed;
        bottom: 20px;
        right: 30px;
        font-size: 0.8rem;
        color: var(--text-secondary);
        opacity: 0.5;
      }
      .slide-counter {
        position: fixed;
        bottom: 20px;
        left: 30px;
        font-size: 0.8rem;
        color: var(--text-secondary);
      }

      /* === TRANSITIONS === */
      .slide {
        animation: fadeIn 0.4s ease;
      }
      @keyframes fadeIn {
        from {
          opacity: 0;
          transform: translateY(10px);
        }
        to {
          opacity: 1;
          transform: translateY(0);
        }
      }

      /* === LAYOUT VARIANTS === */
      .slide.cover {
        justify-content: center;
        align-items: center;
        text-align: center;
      }
      .slide.two-column {
        flex-direction: row;
        gap: 60px;
        align-items: center;
      }
      .slide.two-column .col {
        flex: 1;
      }
      .slide.centered {
        align-items: center;
        text-align: center;
      }

      /* === VISUAL ELEMENTS === */
      .card {
        background: rgba(255, 255, 255, 0.05);
        border-radius: 12px;
        padding: 24px;
        margin: 8px 0;
      }
      .badge {
        display: inline-block;
        background: var(--accent);
        color: white;
        padding: 4px 14px;
        border-radius: 20px;
        font-size: 0.85rem;
      }
      .divider {
        width: 60px;
        height: 4px;
        background: var(--accent);
        border-radius: 2px;
        margin: 16px 0;
      }
      .icon-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
        gap: 20px;
      }

      /* === PRINT / PDF EXPORT === */
      @media print {
        .slide {
          page-break-after: always;
          display: flex !important;
          position: relative;
        }
        .nav-hint,
        .slide-counter {
          display: none;
        }
      }
    </style>
  </head>
  <body>
    <div class="slide-deck" id="deck">
      <!-- SLIDE 1: COVER -->
      <div
        class="slide cover active"
        style="background: linear-gradient(135deg, var(--bg-primary), #1a1a2e);"
      >
        <div class="badge">Topic</div>
        <h1 style="font-size: 3.8rem; margin-top: 20px;">Main Title</h1>
        <p
          style="color: var(--text-secondary); font-size: 1.3rem; margin-top: 12px;"
        >
          Short subtitle description
        </p>
        <div class="divider" style="margin: 20px auto;"></div>
        <p style="color: var(--text-secondary); font-size: 1rem;">
          Author — Date
        </p>
      </div>

      <!-- SLIDE 2+: CONTENT -->
      <div class="slide">
        <h2>Slide Title</h2>
        <div class="divider"></div>
        <ul>
          <li>Key point 1</li>
          <li>Key point 2</li>
          <li>Key point 3</li>
        </ul>
      </div>

      <!-- ... more slides ... -->
    </div>

    <div class="slide-counter">
      <span id="current">1</span> / <span id="total"></span>
    </div>
    <div class="nav-hint">← → or click to navigate</div>

    <script>
      const slides = document.querySelectorAll(".slide");
      let currentSlide = 0;
      document.getElementById("total").textContent = slides.length;

      function showSlide(n) {
        slides[currentSlide].classList.remove("active");
        currentSlide = (n + slides.length) % slides.length;
        slides[currentSlide].classList.add("active");
        document.getElementById("current").textContent = currentSlide + 1;
      }

      document.addEventListener("keydown", (e) => {
        if (e.key === "ArrowRight" || e.key === " ")
          showSlide(currentSlide + 1);
        if (e.key === "ArrowLeft") showSlide(currentSlide - 1);
        if (e.key === "f") document.documentElement.requestFullscreen?.();
        if (e.key === "Escape") document.exitFullscreen?.();
      });

      document.querySelector(".slide-deck").addEventListener("click", (e) => {
        const x = e.clientX / window.innerWidth;
        x > 0.5 ? showSlide(currentSlide + 1) : showSlide(currentSlide - 1);
      });
    </script>
  </body>
</html>
```

---

## Slide Layout Types

Each slide should use the layout that best fits its content:

### 1. Cover Slide

- Centered, extra-large font, gradient background
- Topic badge + main title + subtitle + author

### 2. Section Divider

- Only section title + number, accent color background
- Used to separate major sections of the presentation

### 3. Content + Bullets

- Left-aligned title + list of key points
- Use icons/emoji at the start of each bullet instead of plain dots

### 4. Two-Column

- `.two-column` layout: text on left, visuals/list/cards on right
- Great for comparisons, before-after, text+illustration

### 5. Cards Grid

- 2-3 column grid, each card containing icon + title + short description
- Great for features, benefits, team members

### 6. Big Number / Statistic

- Huge number in the center (font-size: 5rem+) + small label below
- Great for data points, KPIs, impact numbers

### 7. Quote / Highlight

- Large text, centered, with decorative quotation marks
- Different background (light accent color)

### 8. Timeline / Steps

- Horizontal or vertical flexbox, dots connecting each step
- Great for processes, roadmaps, history

### 9. Thank You / CTA

- Centered, simple, contact info or call to action

---

## MANDATORY Design Rules

1. **16:9 aspect ratio**: Always use `width: 100vw; height: 100vh` — each slide fills the entire screen
2. **Minimal text**: Maximum 6 lines per slide. If content is long → split into multiple slides
3. **Large font sizes**: Heading ≥ 2.4rem, body ≥ 1.3rem — must be readable on a projector
4. **High contrast**: Text must be clearly legible against its background. Verify visually
5. **Consistency**: Same fonts, same color palette, same spacing throughout the entire deck
6. **No placeholder images**: Never use `<img src="placeholder">`. Replace with CSS shapes, gradients, icons (emoji or Lucide for React), or inline SVGs
7. **Subtle animation**: Only fadeIn on slide transition. No complex animations that distract
8. **Responsive fullscreen**: Must work well at all screen sizes
9. **Print-ready**: Include `@media print` rules so each slide becomes one printed page

---

## When Using React (.jsx) Instead of HTML

If creating a React artifact, use this pattern:

```jsx
import { useState, useEffect, useCallback } from "react";

const slides = [
  { type: "cover", title: "...", subtitle: "..." },
  { type: "content", title: "...", points: ["...", "..."] },
  { type: "twoColumn", title: "...", left: "...", right: "..." },
  // ...
];

export default function SlideDeck() {
  const [current, setCurrent] = useState(0);

  const next = useCallback(
    () => setCurrent((c) => (c + 1) % slides.length),
    [],
  );
  const prev = useCallback(
    () => setCurrent((c) => (c - 1 + slides.length) % slides.length),
    [],
  );

  useEffect(() => {
    const handleKey = (e) => {
      if (e.key === "ArrowRight" || e.key === " ") next();
      if (e.key === "ArrowLeft") prev();
      if (e.key === "f") document.documentElement.requestFullscreen?.();
    };
    window.addEventListener("keydown", handleKey);
    return () => window.removeEventListener("keydown", handleKey);
  }, [next, prev]);

  const renderSlide = (slide) => {
    switch (slide.type) {
      case "cover":
        return /* cover layout */;
      case "content":
        return /* content layout */;
      case "twoColumn":
        return /* two-column layout */;
      // ...
    }
  };

  return (
    <div
      className="w-screen h-screen overflow-hidden relative"
      onClick={(e) => (e.clientX > window.innerWidth / 2 ? next() : prev())}
      style={{ fontFamily: "'Outfit', sans-serif" }}
    >
      {renderSlide(slides[current])}
      <div className="fixed bottom-5 left-8 text-sm opacity-40">
        {current + 1} / {slides.length}
      </div>
    </div>
  );
}
```

Advantages of React: Tailwind CSS utilities, Lucide icons, more complex logic, recharts for charts.

---

## Pre-Delivery Checklist

- [ ] Correct number of slides (cover + content + closing)
- [ ] Arrow keys ← → work, click navigates
- [ ] Counter displays correct "X / N"
- [ ] Press F for fullscreen
- [ ] All text is readable with sufficient contrast
- [ ] No broken images or placeholders
- [ ] Google Fonts load correctly (or good fallback)
- [ ] Print/PDF exports properly (`@media print`)
- [ ] Consistent style throughout the entire deck
- [ ] Each slide has exactly one key idea, not overloaded with text

---

## Natural Language Editing

After initial creation, the user can request modifications:

- "Switch to a light theme" → update CSS variables
- "Add 2 slides about case studies" → insert slides into the array
- "Slide 3 has too much text, split it" → refactor content across slides
- "Change the font to Playfair Display" → update Google Fonts link + CSS
- "Add a chart to slide 5" → use CSS chart or recharts (React)

On each edit, keep unchanged slides intact and only update what the user requested.
