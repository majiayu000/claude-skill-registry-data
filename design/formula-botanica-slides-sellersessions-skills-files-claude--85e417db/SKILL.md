---
name: formula-botanica-slides
description: Generate professional slide decks and presentations using Formula Botanica brand guidelines - green botanical theme with Roboto Light/Thin fonts, leaf logo motifs, and clean layouts for finance processes, team presentations, and internal documentation.
---

# Formula Botanica Slide Deck Generator

## Core Principle
**Create beautiful, on-brand presentations instantly.** Generate complete HTML-based slide decks that match Formula Botanica's botanical aesthetic with zero setup required.

## When to Activate

Activate this skill when user:
- Asks to create a "presentation" or "slide deck"
- Mentions "Formula Botanica" or "botanical slides"
- Requests slides for finance processes, SOPs, or team presentations
- Wants to visualize data with charts, tables, or diagrams
- Says "create slides about [topic]"

**Do NOT ask questions about branding** - automatically apply Formula Botanica design system.

## Formula Botanica Brand System (MANDATORY)

### Brand Colors

**Primary Green Palette:**
```css
--green-primary: #009247;      /* Main brand green */
--green-accent: #8cc644;       /* Bright lime green */
--green-light: #D0E6B5;        /* Light sage green */
--green-sage: #92AC86;         /* Medium sage */
--green-dark: #273C2C;         /* Dark forest green */
```

**Supporting Colors:**
```css
--grey-light: #D9E0E3;         /* Light grey for backgrounds */
--grey-medium: #808287;        /* Medium grey for text */
--grey-dark: #515052;          /* Dark grey for headings */
--grey-darker: #383C3A;        /* Darker grey for emphasis */
--grey-darkest: #282828;       /* Almost black */
--red-cta: #C40000;            /* Bright red for CTAs/buttons */
```

**Usage Guidelines:**
- Primary text: Dark grey (#515052) - NOT green (makes text harder to read)
- Headings: Use green (#009247 or #8cc644) for visual impact
- Backgrounds: White or light grey (#D9E0E3) with green accents
- Buttons/CTAs: Bright red (#C40000) for high click-through rates
- Offset greenery with lighter and darker greys

### Typography

**Primary Fonts (Google Fonts):**
```html
<link href="https://fonts.googleapis.com/css2?family=Roboto:wght@300;400&family=Futura+PT:wght@700&family=Lovelo:wght@900&display=swap" rel="stylesheet">
```

**Font Hierarchy:**
```css
/* Logo & Course Covers */
font-family: 'Roboto', sans-serif;
font-weight: 300; /* Light */
font-weight: 400; /* Thin */

/* Body Text (Written Materials) */
font-family: 'Roboto', sans-serif;
font-weight: 400;

/* Fallback Sans-Serif */
font-family: Arial, sans-serif;

/* Website Headings (ALL-CAPS ONLY) */
font-family: 'Futura PT', sans-serif; /* If unavailable, use Arial */
text-transform: uppercase;

/* Canva Headers & Quotes (ALL-CAPS ONLY) */
font-family: 'Lovelo', sans-serif;
text-transform: uppercase;
font-weight: 900;
/* NOT for body text */

/* Botanical Table of Elements (Sans Serif) */
font-family: 'Century Gothic', sans-serif;
```

**Typography Rules:**
- **NEVER use Lovelo for body text** - headers and quotes only
- **ALWAYS use ALL-CAPS** for Futura PT and Lovelo headings
- Body text: Roboto 400 (regular), dark grey color
- Slide titles: Lovelo 900, all-caps, green (#009247)
- Subtitles: Futura PT, all-caps, medium grey

### Logo Usage

**Two Main Logos:**

1. **Main Logo (Horizontal)**
   - Two green colors: #009247 (dark green) and #8cc644 (bright lime)
   - White background
   - Text: "FORMULA BOTANICA" (grey + green two-tone lettering)
   - Botanical leaf star motif above text

2. **Social Media Logo (Circular)**
   - Two green colors: #009247 and #8cc644
   - White background
   - Circular botanical leaf star motif
   - No text version for icons

**Logo Placement:**
- Footer: Bottom right or bottom center of every slide
- Use as SVG/CSS recreation (no external image dependencies)
- Maintain aspect ratio
- Minimum clear space around logo

### Slide Structure

**Standard Slide Layout:**
```html
<section class="slide">
    <!-- Decorative botanical element (optional) -->
    <div class="botanical-accent"></div>

    <!-- Slide header -->
    <h1 class="slide-title">SLIDE TITLE IN ALL-CAPS</h1>
    <h2 class="slide-subtitle">Optional Subtitle</h2>

    <!-- Content area -->
    <div class="slide-content">
        <!-- Text, charts, tables, images -->
    </div>

    <!-- Footer with logo -->
    <footer class="slide-footer">
        <div class="fb-logo"></div>
    </footer>
</section>
```

**Slide Types:**

1. **Title Slide**
   - Large title (Lovelo, all-caps, green)
   - Subtitle/description
   - Large botanical background motif
   - Logo bottom right

2. **Content Slide**
   - Title (Lovelo, all-caps, green)
   - Bullet points or paragraphs (Roboto, dark grey)
   - Optional chart or image
   - Logo footer

3. **Chart/Data Slide**
   - Title
   - Chart visualization (bar, pie, line, flow diagram)
   - Data table below (optional)
   - Logo footer

4. **Process Flow Slide**
   - Title
   - Step-by-step boxes with arrows
   - Green accents on active steps
   - Logo footer

5. **Section Divider Slide**
   - Large section title
   - Full botanical background
   - Minimal text
   - Logo footer

## Complete CSS Template (Use This Exactly)

```css
/* === FORMULA BOTANICA SLIDE DECK STYLES === */

/* Google Fonts */
@import url('https://fonts.googleapis.com/css2?family=Roboto:wght@300;400;700&display=swap');

/* Root Variables */
:root {
    /* Brand Colors */
    --green-primary: #009247;
    --green-accent: #8cc644;
    --green-light: #D0E6B5;
    --green-sage: #92AC86;
    --green-dark: #273C2C;

    --grey-light: #D9E0E3;
    --grey-medium: #808287;
    --grey-dark: #515052;
    --grey-darker: #383C3A;
    --grey-darkest: #282828;

    --red-cta: #C40000;

    /* Typography */
    --font-body: 'Roboto', Arial, sans-serif;
    --font-heading: 'Roboto', Arial, sans-serif;
}

/* Global Styles */
* {
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}

body {
    font-family: var(--font-body);
    background: var(--grey-light);
    color: var(--grey-dark);
    line-height: 1.6;
    overflow-x: hidden;
}

/* Slide Container */
.slide-deck {
    width: 100%;
    max-width: 1200px;
    margin: 0 auto;
}

/* Individual Slide */
.slide {
    background: white;
    width: 100%;
    min-height: 600px;
    padding: 60px 80px;
    margin-bottom: 40px;
    position: relative;
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
    border-radius: 8px;
    display: flex;
    flex-direction: column;
    page-break-after: always;
}

/* Botanical Accent Elements */
.botanical-accent {
    position: absolute;
    top: 20px;
    right: 20px;
    width: 120px;
    height: 120px;
    background: radial-gradient(circle, var(--green-accent) 0%, var(--green-primary) 100%);
    opacity: 0.1;
    border-radius: 50%;
    z-index: 0;
}

.botanical-accent::before {
    content: '';
    position: absolute;
    top: 50%;
    left: 50%;
    transform: translate(-50%, -50%);
    width: 80%;
    height: 80%;
    background: var(--green-light);
    border-radius: 50%;
    opacity: 0.5;
}

/* Slide Titles */
.slide-title {
    font-family: var(--font-heading);
    font-weight: 700;
    font-size: 48px;
    color: var(--green-primary);
    text-transform: uppercase;
    letter-spacing: 2px;
    margin-bottom: 16px;
    z-index: 1;
}

.slide-subtitle {
    font-family: var(--font-heading);
    font-weight: 400;
    font-size: 24px;
    color: var(--grey-medium);
    text-transform: uppercase;
    letter-spacing: 1px;
    margin-bottom: 32px;
    z-index: 1;
}

/* Content Area */
.slide-content {
    flex: 1;
    z-index: 1;
    margin-bottom: 40px;
}

/* Typography */
.slide-content h3 {
    font-size: 28px;
    color: var(--green-primary);
    margin-top: 24px;
    margin-bottom: 12px;
    text-transform: uppercase;
}

.slide-content p {
    font-size: 18px;
    line-height: 1.8;
    margin-bottom: 16px;
    color: var(--grey-dark);
}

.slide-content ul,
.slide-content ol {
    margin-left: 32px;
    margin-bottom: 16px;
}

.slide-content li {
    font-size: 18px;
    line-height: 1.8;
    margin-bottom: 12px;
    color: var(--grey-dark);
}

.slide-content strong {
    color: var(--green-primary);
    font-weight: 700;
}

/* Tables */
table {
    width: 100%;
    border-collapse: collapse;
    margin: 24px 0;
}

thead {
    background: var(--green-primary);
    color: white;
}

th {
    padding: 16px;
    text-align: left;
    font-weight: 700;
    text-transform: uppercase;
    font-size: 14px;
    letter-spacing: 1px;
}

td {
    padding: 12px 16px;
    border-bottom: 1px solid var(--grey-light);
}

tbody tr:hover {
    background: rgba(140, 198, 68, 0.05);
}

/* Buttons/CTAs */
.cta-button {
    background: var(--red-cta);
    color: white;
    padding: 16px 32px;
    border: none;
    border-radius: 4px;
    font-size: 18px;
    font-weight: 700;
    text-transform: uppercase;
    cursor: pointer;
    transition: all 0.3s ease;
    display: inline-block;
    text-decoration: none;
}

.cta-button:hover {
    background: #a00000;
    transform: translateY(-2px);
    box-shadow: 0 4px 12px rgba(196, 0, 0, 0.3);
}

/* Footer */
.slide-footer {
    display: flex;
    justify-content: center;
    align-items: center;
    padding-top: 24px;
    border-top: 2px solid var(--grey-light);
}

/* Formula Botanica Logo (CSS Recreation) */
.fb-logo {
    font-family: var(--font-heading);
    font-weight: 300;
    font-size: 18px;
    color: var(--grey-medium);
    letter-spacing: 2px;
    display: flex;
    align-items: center;
    gap: 12px;
}

.fb-logo::before {
    content: '';
    width: 40px;
    height: 40px;
    background: radial-gradient(circle, var(--green-accent) 0%, var(--green-primary) 100%);
    border-radius: 50%;
    display: inline-block;
    position: relative;
}

.fb-logo::after {
    content: 'FORMULA BOTANICA';
    color: var(--grey-dark);
    font-weight: 700;
}

/* Process Flow Boxes */
.process-flow {
    display: flex;
    gap: 24px;
    align-items: center;
    margin: 32px 0;
    flex-wrap: wrap;
}

.process-step {
    flex: 1;
    min-width: 200px;
    padding: 24px;
    background: white;
    border: 3px solid var(--green-light);
    border-radius: 8px;
    text-align: center;
    position: relative;
}

.process-step.active {
    border-color: var(--green-primary);
    background: rgba(0, 146, 71, 0.05);
}

.process-step h4 {
    font-size: 20px;
    color: var(--green-primary);
    margin-bottom: 8px;
    text-transform: uppercase;
}

.process-step p {
    font-size: 14px;
    color: var(--grey-dark);
}

.process-arrow {
    font-size: 32px;
    color: var(--green-accent);
}

/* Chart Styles */
.chart-container {
    width: 100%;
    max-width: 800px;
    margin: 32px auto;
    padding: 24px;
    background: white;
    border-radius: 8px;
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
}

/* Highlight Boxes */
.highlight-box {
    background: rgba(140, 198, 68, 0.1);
    border-left: 4px solid var(--green-accent);
    padding: 20px;
    margin: 24px 0;
    border-radius: 4px;
}

.highlight-box h4 {
    color: var(--green-primary);
    margin-bottom: 8px;
    text-transform: uppercase;
}

/* Title Slide Specific */
.slide.title-slide {
    justify-content: center;
    text-align: center;
    background: linear-gradient(135deg, rgba(140, 198, 68, 0.1) 0%, rgba(0, 146, 71, 0.05) 100%);
}

.slide.title-slide .slide-title {
    font-size: 64px;
    margin-bottom: 24px;
}

.slide.title-slide .botanical-accent {
    width: 300px;
    height: 300px;
    opacity: 0.15;
}

/* Section Divider Slide */
.slide.section-divider {
    justify-content: center;
    text-align: center;
    background: var(--green-primary);
    color: white;
}

.slide.section-divider .slide-title {
    color: white;
    font-size: 56px;
}

/* Print Styles */
@media print {
    .slide {
        margin-bottom: 0;
        box-shadow: none;
    }

    body {
        background: white;
    }
}

/* Responsive */
@media (max-width: 768px) {
    .slide {
        padding: 40px 32px;
        min-height: auto;
    }

    .slide-title {
        font-size: 36px;
    }

    .process-flow {
        flex-direction: column;
    }
}
```

## Slide Generation Process

### 1. Understand User Request
- Topic/content for presentation
- Target audience (team, stakeholders, etc.)
- Presentation type (finance SOP, process flow, data analysis, etc.)

### 2. Auto-Generate Slide Structure

**For Finance SOPs:**
```
Slide 1: Title Slide - "FINANCE PROCESS OVERVIEW"
Slide 2: Process Summary - Key points
Slide 3: Step-by-Step Flow - Process diagram
Slide 4-N: Individual Process Details - One per major step
Slide N+1: Key Metrics/Data - Charts if applicable
Slide N+2: Action Items/Next Steps
```

**For Team Presentations:**
```
Slide 1: Title Slide - Topic name
Slide 2: Agenda/Overview
Slide 3-N: Content slides - Main points
Slide N+1: Key Takeaways
Slide N+2: Q&A or Next Steps
```

**For Data Analysis:**
```
Slide 1: Title Slide - Analysis topic
Slide 2: Executive Summary
Slide 3-N: Data visualization slides - Charts/graphs
Slide N+1: Insights & Recommendations
Slide N+2: Action Plan
```

### 3. Apply Brand Styling Automatically
- All titles: Lovelo-style (bold Roboto 700), all-caps, green
- All body text: Roboto 400, dark grey
- Charts: Green color scheme with grey accents
- Tables: Green headers, white/light grey alternating rows
- CTAs: Red buttons (#C40000)
- Footer: Formula Botanica logo on every slide

### 4. Include Visuals

**Charts (Use Chart.js or CSS-based visuals):**
```html
<!-- Bar Chart Example -->
<canvas id="barChart" width="400" height="200"></canvas>
<script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
<script>
new Chart(document.getElementById('barChart'), {
    type: 'bar',
    data: {
        labels: ['Q1', 'Q2', 'Q3', 'Q4'],
        datasets: [{
            label: 'Revenue',
            data: [12, 19, 3, 5],
            backgroundColor: '#009247'
        }]
    },
    options: {
        responsive: true,
        plugins: {
            legend: { display: true }
        }
    }
});
</script>
```

**Process Flow Diagrams:**
```html
<div class="process-flow">
    <div class="process-step active">
        <h4>Step 1</h4>
        <p>Initial Setup</p>
    </div>
    <div class="process-arrow">→</div>
    <div class="process-step">
        <h4>Step 2</h4>
        <p>Data Collection</p>
    </div>
    <div class="process-arrow">→</div>
    <div class="process-step">
        <h4>Step 3</h4>
        <p>Analysis</p>
    </div>
</div>
```

## Complete HTML Template

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Presentation Title - Formula Botanica</title>
    <link href="https://fonts.googleapis.com/css2?family=Roboto:wght@300;400;700&display=swap" rel="stylesheet">
    <style>
        /* [Complete CSS from above] */
    </style>
</head>
<body>
    <div class="slide-deck">

        <!-- ========== TITLE SLIDE ========== -->
        <section class="slide title-slide">
            <div class="botanical-accent"></div>
            <h1 class="slide-title">PRESENTATION TITLE</h1>
            <h2 class="slide-subtitle">Subtitle or Description</h2>
            <footer class="slide-footer">
                <div class="fb-logo"></div>
            </footer>
        </section>

        <!-- ========== CONTENT SLIDE ========== -->
        <section class="slide">
            <div class="botanical-accent"></div>
            <h1 class="slide-title">SLIDE TITLE</h1>

            <div class="slide-content">
                <p>Content goes here...</p>
                <ul>
                    <li>Bullet point 1</li>
                    <li>Bullet point 2</li>
                    <li>Bullet point 3</li>
                </ul>
            </div>

            <footer class="slide-footer">
                <div class="fb-logo"></div>
            </footer>
        </section>

        <!-- ========== PROCESS FLOW SLIDE ========== -->
        <section class="slide">
            <div class="botanical-accent"></div>
            <h1 class="slide-title">PROCESS OVERVIEW</h1>

            <div class="slide-content">
                <div class="process-flow">
                    <div class="process-step active">
                        <h4>Step 1</h4>
                        <p>Description</p>
                    </div>
                    <div class="process-arrow">→</div>
                    <div class="process-step">
                        <h4>Step 2</h4>
                        <p>Description</p>
                    </div>
                    <div class="process-arrow">→</div>
                    <div class="process-step">
                        <h4>Step 3</h4>
                        <p>Description</p>
                    </div>
                </div>
            </div>

            <footer class="slide-footer">
                <div class="fb-logo"></div>
            </footer>
        </section>

        <!-- ========== SECTION DIVIDER ========== -->
        <section class="slide section-divider">
            <h1 class="slide-title">SECTION TITLE</h1>
            <footer class="slide-footer">
                <div class="fb-logo"></div>
            </footer>
        </section>

    </div>

    <!-- Navigation (Optional) -->
    <script>
        // Add keyboard navigation
        let currentSlide = 0;
        const slides = document.querySelectorAll('.slide');

        document.addEventListener('keydown', (e) => {
            if (e.key === 'ArrowRight' && currentSlide < slides.length - 1) {
                currentSlide++;
                slides[currentSlide].scrollIntoView({ behavior: 'smooth' });
            }
            if (e.key === 'ArrowLeft' && currentSlide > 0) {
                currentSlide--;
                slides[currentSlide].scrollIntoView({ behavior: 'smooth' });
            }
        });
    </script>
</body>
</html>
```

## File Naming Convention

```
[topic]-slides-[date].html

Examples:
- finance-sop-slides-2025-10-19.html
- team-quarterly-review-slides-2025-10-19.html
- process-documentation-slides-2025-10-19.html
```

## Quality Checklist

**Before delivering, verify:**
- ✅ All titles in ALL-CAPS (Lovelo style with bold Roboto)
- ✅ Green color scheme (#009247 primary, #8cc644 accent)
- ✅ Dark grey body text (#515052) - NOT green
- ✅ Roboto font family for all text
- ✅ Formula Botanica logo in footer of every slide
- ✅ Botanical accent elements (circles/leaves) for visual interest
- ✅ Red CTA buttons if applicable (#C40000)
- ✅ Charts use green color palette
- ✅ Tables have green headers
- ✅ Process flows have green borders and accents
- ✅ Responsive layout (works on mobile)
- ✅ Print-friendly styles included
- ✅ Keyboard navigation (arrow keys)
- ✅ Standalone HTML (no external dependencies except Google Fonts)

## Success Criteria

This skill works correctly when:
- ✅ User requests slides → Full branded presentation generated
- ✅ All slides match Formula Botanica brand guidelines exactly
- ✅ No questions asked about fonts/colors (auto-applied)
- ✅ Process flows, charts, tables styled correctly
- ✅ Presentation opens in browser and is immediately usable
- ✅ Can be printed or exported to PDF
- ✅ Keyboard navigation works (arrow keys)
- ✅ Logo appears on every slide
- ✅ Content is clear, well-structured, and professional
