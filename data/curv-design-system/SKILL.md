---
name: curv-design-system
description: Apply the complete CURV Tools design system to all visual outputs - dashboards, reports, HTML artifacts, and data visualizations. Includes exact colors from production tools (rgb(3, 12, 27) dark background, rgb(157, 78, 221) purple accent), glassmorphic effects, gradient borders, header/footer templates, and animation patterns used in GL Decoder and SQPR Analyser.
---

# CURV Design System - Complete Production Specification

## Core Brand Colors (Exact from Production)

**Primary Palette:**
```css
--bg-primary: rgb(3, 12, 27);              /* Main background - deep space blue */
--bg-header: linear-gradient(180deg, 
  rgb(18, 11, 41) 0%, 
  rgb(13, 18, 41) 40%, 
  rgb(4, 16, 32) 70%, 
  rgb(3, 12, 27) 100%);                    /* Header gradient */
--bg-panel: linear-gradient(135deg, 
  rgb(18, 11, 41), 
  rgb(13, 18, 41));                        /* Panel gradient */

--accent: rgb(157, 78, 221);               /* CURV Purple - primary accent */
--accent-alpha: rgba(157, 78, 221, 0.3);   /* Transparent purple */
--accent-border: rgba(157, 78, 221, 0.5);  /* Purple borders */
--accent-light: #c084fc;                   /* Light purple for gradients */

--text-primary: #ffffff;                   /* Primary text - pure white */
--text-muted: rgba(255, 255, 255, 0.7);    /* Secondary text */
--text-secondary: rgba(255, 255, 255, 0.8); /* Subtitle text */
```

**Supporting Colors (from PDP Analyser):**
```css
--curv-primary: #2563eb;      /* Blue for primary actions */
--curv-secondary: #64748b;    /* Gray for secondary actions */
--curv-success: #10b981;      /* Green for success states */
--curv-warning: #f59e0b;      /* Orange for warnings */
--curv-error: #ef4444;        /* Red for errors */
```

**Dark Mode Neutrals:**
```css
--dark-950: #020617;
--dark-900: #0f172a;
--dark-800: #1e293b;
--dark-700: #334155;
--dark-600: #475569;
```

## Typography System

**Font Stack (Production):**
```css
font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Roboto', 'Oxygen',
  'Ubuntu', 'Cantarell', 'Fira Sans', 'Droid Sans', 'Helvetica Neue', sans-serif;
```

**Font Sizes (Production Scale):**
```css
--text-xs: 11px;      /* Footer credits */
--text-sm: 12px;      /* Footer subtitle */
--text-base: 14px;    /* Body text, buttons */
--text-md: 16px;      /* Subheadings, footer title */
--text-lg: 20px;      /* Subtitles */
--text-xl: 24px;      /* Section headers */
--text-2xl: 32px;     /* Page headers */
--text-3xl: 72px;     /* Hero titles (SQPR Analyser style) */
```

**Font Weights:**
```css
--font-normal: 400;    /* Body text */
--font-medium: 500;    /* Buttons, emphasis */
--font-semibold: 600;  /* Headers */
--font-bold: 700;      /* Hero titles */
```

**Letter Spacing:**
```css
--tracking-tight: -2px;     /* Hero titles */
--tracking-normal: 0;       /* Body text */
--tracking-wide: 0.05em;    /* Buttons, labels */
--tracking-wider: 0.5px;    /* Footer credits */
--tracking-widest: 1px;     /* Stage info */
```

## Complete HTML Template (Production Standard)

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>[Tool Name] - CURV Tools</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            background: rgb(3, 12, 27);
            color: #ffffff;
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
            -webkit-font-smoothing: antialiased;
            -moz-osx-font-smoothing: grayscale;
            min-height: 100vh;
        }
        
        .container {
            max-width: 1200px;
            margin: 0 auto;
            padding: 20px;
        }
        
        /* Header Animation */
        @keyframes headerRotate {
            from { transform: rotate(0deg); }
            to { transform: rotate(360deg); }
        }
        
        /* Hero Header (SQPR Style) */
        .hero-header {
            text-align: center;
            margin: 20px 0 40px;
            padding: 40px;
            background: rgba(3, 12, 27, 0.6);
            border-radius: 20px;
            backdrop-filter: blur(10px);
            border: 1.5px solid rgba(157, 78, 221, 0.5);
            position: relative;
            overflow: hidden;
        }
        
        .hero-header::before {
            content: '';
            position: absolute;
            top: -50%;
            left: -50%;
            width: 200%;
            height: 200%;
            background: radial-gradient(circle, rgba(157, 78, 221, 0.3) 0%, transparent 70%);
            animation: headerRotate 30s linear infinite;
            opacity: 0.3;
            z-index: 0;
        }
        
        .hero-header-content {
            position: relative;
            z-index: 1;
        }
        
        .hero-title {
            font-size: 72px;
            font-weight: 700;
            margin: 0;
            color: #ffffff;
            letter-spacing: -2px;
            text-shadow: 0 0 25px rgba(255, 255, 255, 0.6), 
                         0 0 50px rgba(255, 255, 255, 0.4), 
                         0 0 100px rgba(157, 78, 221, 0.4);
        }
        
        .hero-subtitle {
            font-size: 20px;
            color: rgba(255, 255, 255, 0.8);
            margin: 12px 0 8px;
        }
        
        .hero-badge {
            font-size: 14px;
            color: rgb(157, 78, 221);
            letter-spacing: 1px;
            text-transform: uppercase;
            font-weight: 500;
            margin-top: 8px;
        }
        
        /* Standard Header (PDP Style) */
        .standard-header {
            background: white;
            box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
            border-bottom: 1px solid #e5e7eb;
            padding: 24px 0;
        }
        
        .standard-header h1 {
            font-size: 30px;
            font-weight: 700;
            color: #111827;
            margin: 0 0 4px;
        }
        
        .standard-header p {
            color: #6b7280;
            margin: 0;
        }
        
        /* Glassmorphic Panel */
        .glass-panel {
            background: rgba(0, 0, 0, 0.4);
            backdrop-filter: blur(12px);
            border: 1px solid rgba(157, 78, 221, 0.15);
            border-radius: 16px;
            padding: 24px;
            box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
        }
        
        /* Card */
        .card {
            background: rgb(3, 12, 27);
            border: 1px solid rgba(157, 78, 221, 0.5);
            border-radius: 8px;
            padding: 24px;
            box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
        }
        
        /* Gradient Border Card */
        .gradient-border-card {
            background: linear-gradient(rgb(3, 12, 27), rgb(3, 12, 27)) padding-box,
                        linear-gradient(135deg, rgb(157, 78, 221) 0%, #c084fc 100%) border-box;
            border: 2px solid transparent;
            border-radius: 16px;
            padding: 24px;
        }
        
        /* Buttons */
        .btn-primary {
            background: linear-gradient(135deg, rgb(157, 78, 221) 0%, #c084fc 100%);
            color: white;
            border: none;
            padding: 12px 24px;
            border-radius: 12px;
            font-weight: 600;
            font-size: 14px;
            cursor: pointer;
            transition: all 300ms ease-in-out;
            text-transform: uppercase;
            letter-spacing: 0.05em;
            box-shadow: 0 8px 25px rgba(157, 78, 221, 0.4), 0 0 20px rgba(157, 78, 221, 0.2);
        }
        
        .btn-primary:hover {
            transform: translateY(-2px);
            box-shadow: 0 12px 40px rgba(157, 78, 221, 0.5);
        }
        
        .btn-secondary {
            background: transparent;
            color: rgb(157, 78, 221);
            border: 1px solid rgb(157, 78, 221);
            padding: 12px 24px;
            border-radius: 12px;
            font-weight: 600;
            font-size: 14px;
            cursor: pointer;
            transition: all 300ms ease-in-out;
            text-transform: uppercase;
            letter-spacing: 0.05em;
        }
        
        .btn-secondary:hover {
            background: rgba(157, 78, 221, 0.2);
            transform: translateY(-2px);
        }
        
        /* Tabs Navigation */
        .tabs {
            display: flex;
            gap: 12px;
            justify-content: center;
            flex-wrap: wrap;
            margin: 24px 0;
        }
        
        .tab {
            padding: 12px 24px;
            background: rgba(0, 0, 0, 0.3);
            color: #ffffff;
            border: 1px solid rgba(157, 78, 221, 0.15);
            border-radius: 12px;
            font-weight: 600;
            font-size: 14px;
            cursor: pointer;
            transition: all 300ms ease-in-out;
            text-transform: uppercase;
            letter-spacing: 0.05em;
            backdrop-filter: blur(8px);
        }
        
        .tab.active {
            background: linear-gradient(135deg, rgb(157, 78, 221) 0%, #c084fc 100%);
            border-color: rgba(157, 78, 221, 0.5);
            box-shadow: 0 8px 25px rgba(157, 78, 221, 0.4);
        }
        
        .tab:hover:not(.active) {
            background: rgba(157, 78, 221, 0.2);
            color: rgb(157, 78, 221);
            transform: translateY(-2px);
        }
        
        /* Table */
        table {
            width: 100%;
            border-collapse: collapse;
            background: rgba(0, 0, 0, 0.3);
            border-radius: 8px;
            overflow: hidden;
        }
        
        th {
            background: #0f172a;
            padding: 12px 16px;
            text-align: left;
            font-weight: 600;
            color: #d1d5db;
            border-bottom: 1px solid #334155;
        }
        
        td {
            padding: 12px 16px;
            border-bottom: 1px solid #334155;
            color: rgba(255, 255, 255, 0.7);
        }
        
        tr:hover {
            background: rgba(51, 65, 85, 0.5);
        }
        
        /* Metric Card */
        .metric-card {
            background: linear-gradient(135deg, rgb(18, 11, 41), rgb(13, 18, 41));
            border-left: 4px solid rgb(157, 78, 221);
            padding: 24px;
            border-radius: 8px;
        }
        
        .metric-label {
            color: rgba(255, 255, 255, 0.7);
            font-size: 14px;
            margin-bottom: 8px;
        }
        
        .metric-value {
            color: #ffffff;
            font-size: 32px;
            font-weight: 600;
            margin: 8px 0;
        }
        
        .metric-change {
            color: #10b981;
            font-size: 14px;
        }
        
        /* Footer (SQPR Style) */
        footer {
            text-align: center;
            padding: 40px 0;
            margin-top: 60px;
            opacity: 0.6;
            border-top: 1px solid rgba(157, 78, 221, 0.5);
        }
        
        .footer-title {
            font-weight: 600;
            font-size: 16px;
            color: #ffffff;
            margin-bottom: 8px;
        }
        
        .footer-subtitle {
            font-size: 12px;
            color: rgba(255, 255, 255, 0.7);
            margin-bottom: 16px;
        }
        
        .footer-credits {
            font-size: 11px;
            color: rgba(255, 255, 255, 0.7);
            letter-spacing: 0.5px;
        }
        
        /* Purple Glow Effect */
        .purple-glow {
            box-shadow: 0 0 20px rgba(157, 78, 221, 0.4), 0 0 40px rgba(157, 78, 221, 0.2);
        }
        
        /* Animations */
        @keyframes fadeIn {
            from { opacity: 0; transform: translateY(10px); }
            to { opacity: 1; transform: translateY(0); }
        }
        
        .fade-in {
            animation: fadeIn 500ms ease-in-out;
        }
    </style>
</head>
<body>
    <div class="container">
        <!-- Hero Header Example -->
        <header class="hero-header">
            <div class="hero-header-content">
                <h1 class="hero-title">Tool Name</h1>
                <div class="hero-subtitle">
                    Tool description and purpose
                </div>
                <div class="hero-badge">
                    POWERED BY CURV
                </div>
            </div>
        </header>
        
        <!-- Main Content -->
        <main>
            <div class="glass-panel">
                <h2>Content Section</h2>
                <p>Your content here</p>
            </div>
        </main>
        
        <!-- Footer -->
        <footer>
            <div class="footer-title">Tool Name</div>
            <div class="footer-subtitle">Tool tagline or description</div>
            <div class="footer-credits">
                Produced By Danny McMillan | CURV Tools | A Seller Sessions Production 2025
            </div>
        </footer>
    </div>
</body>
</html>
```

## Component Library

### 1. Hero Header (SQPR Analyser Style)

Use for main application headers with high visual impact:

```html
<header class="hero-header">
    <div class="hero-header-content">
        <h1 class="hero-title">[Tool Name]</h1>
        <div class="hero-subtitle">[Tool Description]</div>
        <div class="hero-badge">POWERED BY CURV</div>
    </div>
</header>
```

**Features:**
- 72px hero title with glow effect
- Rotating purple radial gradient background
- Glassmorphic effect with backdrop blur
- Purple border with 1.5px thickness

### 2. Standard Header (PDP Analyser Style)

Use for simpler header layouts:

```html
<header class="standard-header">
    <div class="header-content">
        <h1>[Tool Name]</h1>
        <p>[Brief description]</p>
        <p class="stage-info">CURV Tools - [Tool Category]</p>
    </div>
</header>
```

### 3. Navigation Tabs

Production-ready tab system with active states:

```html
<div class="tabs">
    <button class="tab active">Overview</button>
    <button class="tab">Data</button>
    <button class="tab">Analysis</button>
</div>
```

### 4. Cards & Panels

**Glassmorphic Panel:**
```html
<div class="glass-panel">
    <h3>Panel Title</h3>
    <p>Panel content with blur effect</p>
</div>
```

**Standard Card:**
```html
<div class="card">
    <h3>Card Title</h3>
    <p>Card content</p>
</div>
```

**Gradient Border Card:**
```html
<div class="gradient-border-card">
    <h3>Premium Feature</h3>
    <p>Content with purple gradient border</p>
</div>
```

### 5. Metric Cards

Production pattern from SQPR Analyser:

```html
<div class="metric-card">
    <div class="metric-label">Total Revenue</div>
    <div class="metric-value">$125,000</div>
    <div class="metric-change">↑ 15% from last month</div>
</div>
```

### 6. Buttons

**Primary (Gradient):**
```html
<button class="btn-primary">Primary Action</button>
```

**Secondary (Outline):**
```html
<button class="btn-secondary">Secondary Action</button>
```

### 7. Tables

Production table styling:

```html
<table>
    <thead>
        <tr>
            <th>Column 1</th>
            <th>Column 2</th>
        </tr>
    </thead>
    <tbody>
        <tr>
            <td>Data 1</td>
            <td>Data 2</td>
        </tr>
    </tbody>
</table>
```

### 8. Footer (Standard Format)

```html
<footer>
    <div class="footer-title">[Tool Name]</div>
    <div class="footer-subtitle">[Tool Description]</div>
    <div class="footer-credits">
        Produced By Danny McMillan | CURV Tools | A Seller Sessions Production 2025
    </div>
</footer>
```

## Effects & Animations

### Purple Glow
```css
box-shadow: 0 0 20px rgba(157, 78, 221, 0.4), 0 0 40px rgba(157, 78, 221, 0.2);
```

### Hover Lift
```css
transition: all 300ms ease-in-out;
transform: translateY(-4px);
box-shadow: 0 12px 40px rgba(157, 78, 221, 0.3);
```

### Gradient Border
```css
background: linear-gradient(rgb(3, 12, 27), rgb(3, 12, 27)) padding-box,
            linear-gradient(135deg, rgb(157, 78, 221) 0%, #c084fc 100%) border-box;
border: 2px solid transparent;
```

### Fade In
```css
animation: fadeIn 500ms ease-in-out;
```

## Grid Layouts

**8-Column Grid (SQPR Style):**
```html
<div style="display: grid; grid-template-columns: repeat(8, 1fr); gap: 0;">
    <div style="grid-column: 2 / span 6;">
        <!-- Content spans columns 2-7 -->
    </div>
</div>
```

**Metric Grid:**
```html
<div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 24px;">
    <!-- Metric cards auto-layout -->
</div>
```

## Usage Rules

### ALWAYS Apply When Creating:
- Dashboards and analytics tools
- Data visualization interfaces
- HTML artifacts for CURV Tools
- Reports and presentations
- Interactive demos
- Admin interfaces

### Color Priorities:
1. **Background:** `rgb(3, 12, 27)` - Always
2. **Accent:** `rgb(157, 78, 221)` - For highlights, CTAs, borders
3. **Text:** `#ffffff` or `rgba(255, 255, 255, 0.7)` - High contrast
4. **Panels:** Glassmorphic or gradient backgrounds
5. **Interactive elements:** Purple glow on hover

### Typography Priorities:
1. System font stack (production standard)
2. 72px for hero titles with letter-spacing: -2px
3. 20px for subtitles
4. 14px for body and buttons
5. UPPERCASE + letter-spacing for labels/badges

### Effect Priorities:
1. Glassmorphic blur on panels
2. Gradient borders for premium features
3. Purple glow on hover states
4. Smooth 300ms transitions
5. Rotate animation for hero backgrounds

## Integration with Existing Skills

Works seamlessly with:
- **concise-execution-mode** - Build CURV designs efficiently
- **mcp-response-optimization** - Token-efficient + on-brand
- **curv-mermaid-diagrams** - Consistent diagram styling

## Footer Template (Required for All Tools)

```html
<footer>
    <div class="footer-title">[Tool Name]</div>
    <div class="footer-subtitle">[One-line description]</div>
    <div class="footer-credits">
        Produced By Danny McMillan | CURV Tools | A Seller Sessions Production 2025
    </div>
</footer>
```

## Success Checklist

CURV Design System is correctly applied when outputs have:
- ✅ Background: `rgb(3, 12, 27)`
- ✅ Accent: `rgb(157, 78, 221)` used for highlights
- ✅ Hero header with rotating gradient animation (if applicable)
- ✅ Glassmorphic panels with backdrop blur
- ✅ Gradient buttons with purple glow
- ✅ System font stack
- ✅ Proper footer with credits
- ✅ 300ms smooth transitions
- ✅ Purple border accents: `rgba(157, 78, 221, 0.5)`
- ✅ Responsive grid layout
