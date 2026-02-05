---
name: ngx-design-system
description: "Premium dark mode design system for NGX Genesis. Use when creating web interfaces, landing pages, dashboards, React components, or any UI for the NGX ecosystem. Includes color tokens, glassmorphism effects, neon glow buttons, depth cards, and all brand visual effects. The style is 80% effects and 20% colors - requires transparencies, backdrop-blur, multiple shadows, and subtle gradients."
---

# NGX Design System

Premium dark mode design system for NGX Genesis. Focus: 80% effects, 20% colors.

**Brand**: "Rinde hoy. Vive mejor mañana."

## ⛔ ABSOLUTE PROHIBITIONS

### 1. NEVER USE EMOJIS AS ICONS
```jsx
// ❌ PROHIBITED - NEVER DO THIS
<div className="card-icon">🔥</div>
<div className="card-icon">🧠</div>
<span>✓</span>

// ✅ REQUIRED - ALWAYS USE LUCIDE-REACT SVGs
import { Flame, Brain, Check } from 'lucide-react';
<Flame className="w-6 h-6 text-[#6D00FF]" />
<Brain className="w-6 h-6 text-[#6D00FF]" />
<Check className="w-5 h-5 text-green-500" />
```

### 2. NEVER USE GRADIENT TEXT ON HEADINGS
```css
/* ❌ PROHIBITED - NEVER DO THIS ON TITLES */
h1 span {
  background: linear-gradient(...);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
}

/* ✅ REQUIRED - CLEAN SOLID COLORS */
h1 { color: #FFFFFF; }
h1 .accent { color: #6D00FF; }  /* If accent needed */
```

### 3. PROHIBITED COLORS
```css
/* ❌ NEVER USE THESE */
--cyan: #00D4FF;      /* PROHIBITED */
--cyan-alt: #06B6D4;  /* PROHIBITED */
--cyan-light: #22D3EE;/* PROHIBITED */
--blue: #3B82F6;      /* PROHIBITED */
```

## Icons: Lucide React Only

ALWAYS import from lucide-react. Common icons for NGX:

```jsx
import { 
  Flame,        // BLAZE - training
  Map,          // ATLAS - planning  
  Brain,        // SAGE - biohacking
  Clock,        // TEMPO - time
  Waves,        // WAVE - recovery
  Activity,     // METABOL - metabolism
  Apple,        // MACRO - nutrition
  Sparkles,     // NOVA - optimization
  Zap,          // SPARK - energy
  Star,         // STELLA - performance
  Moon,         // LUNA - women's health
  BookOpen,     // LOGOS - education
  LayoutGrid,   // NEXUS - orchestrator
  Check,        // Checkmarks
  ChevronRight, // Arrows
  ArrowRight,
  Menu,
  X
} from 'lucide-react';
```

Icon styling pattern:
```jsx
// Standard icon in card
<Flame className="w-6 h-6 text-[#6D00FF]" />

// Icon with glow container
<div className="w-14 h-14 rounded-xl bg-[#6D00FF]/10 border border-[#6D00FF]/20 
  flex items-center justify-center">
  <Flame className="w-7 h-7 text-[#6D00FF]" />
</div>

// Checkmark in lists
<Check className="w-5 h-5 text-green-500 flex-shrink-0" />
```

## Core Principle

NGX's visual identity comes from **effects**, not just colors:
- Glassmorphism with backdrop-blur
- Multiple layered shadows
- Subtle gradients (backgrounds only, NOT text)
- Neon glow on interactive elements
- Depth through transparency
- Clean, solid color typography

## Color Tokens

### Primary Palette

```css
:root {
  /* Primary */
  --primary: #6D00FF;           /* Electric Violet - main brand */
  --primary-hover: #7D1AFF;     /* Violet Hover - interactive states */
  --primary-deep: #5B21B6;      /* Deep Purple - secondary */
  
  /* Backgrounds */
  --background: #050505;        /* True dark - base */
  --surface: #0A0A0A;           /* Elevated surface */
  --surface-elevated: #111111;  /* Cards, modals */
  
  /* Borders */
  --border: rgba(255, 255, 255, 0.06);
  --border-glass: rgba(255, 255, 255, 0.1);
  --border-hover: rgba(109, 0, 255, 0.3);
  
  /* Text */
  --text-primary: #FFFFFF;
  --text-secondary: rgba(255, 255, 255, 0.7);
  --text-muted: rgba(255, 255, 255, 0.5);
  
  /* States */
  --success: #22C55E;
  --warning: #F59E0B;
  --error: #EF4444;
}
```

### PROHIBITED COLORS

```css
/* ❌ NEVER USE THESE */
--cyan: #00D4FF;      /* PROHIBITED */
--cyan-alt: #06B6D4;  /* PROHIBITED */
--cyan-light: #22D3EE;/* PROHIBITED */
--blue: #3B82F6;      /* PROHIBITED */
```

## Typography

### Font Stack

```css
/* Body - Clean, modern */
--font-body: 'DM Sans', system-ui, sans-serif;

/* Modern Headlines - Tech feel */
--font-modern: 'Geist', 'DM Sans', sans-serif;

/* Impact Headlines - Bold statements */
--font-display: 'United Sans Condensed', 'DM Sans', sans-serif;

/* Metrics/Code - Monospace */
--font-mono: 'JetBrains Mono', 'Geist Mono', monospace;
```

### Usage Guidelines

| Context | Font | Weight | Size |
|---------|------|--------|------|
| Body | DM Sans | 400 | 16px |
| Headlines | Geist | 600 | 32-48px |
| Impact | United Sans | 700 | 48-72px |
| Metrics | Mono | 500 | 14-24px |
| UI Labels | DM Sans | 500 | 14px |

## Effects Library

### Glassmorphism Card

```css
.card-glass {
  background: rgba(10, 10, 10, 0.8);
  backdrop-filter: blur(20px);
  -webkit-backdrop-filter: blur(20px);
  border: 1px solid rgba(255, 255, 255, 0.1);
  border-radius: 16px;
  box-shadow: 
    0 4px 30px rgba(0, 0, 0, 0.3),
    inset 0 1px 0 rgba(255, 255, 255, 0.05);
}

.card-glass:hover {
  transform: translateY(-8px) scale(1.02);
  border-color: rgba(109, 0, 255, 0.3);
  box-shadow: 
    0 20px 40px rgba(109, 0, 255, 0.15),
    0 8px 16px rgba(0, 0, 0, 0.4);
  transition: all 0.6s cubic-bezier(0.4, 0, 0.2, 1);
}
```

### Primary Button with Shimmer

```css
.btn-primary {
  background: linear-gradient(135deg, #6D00FF 0%, #5B21B6 100%);
  color: white;
  padding: 12px 24px;
  border: none;
  border-radius: 8px;
  font-weight: 600;
  position: relative;
  overflow: hidden;
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}

.btn-primary::after {
  content: '';
  position: absolute;
  top: 0;
  left: -100%;
  width: 100%;
  height: 100%;
  background: linear-gradient(
    90deg,
    transparent,
    rgba(255, 255, 255, 0.2),
    transparent
  );
  animation: shimmer 2s infinite;
}

.btn-primary:hover {
  background: #7D1AFF;
  box-shadow: 0 0 30px rgba(109, 0, 255, 0.5);
  transform: translateY(-2px);
}

@keyframes shimmer {
  100% { left: 100%; }
}
```

### Outline Button

```css
.btn-outline {
  background: transparent;
  color: #6D00FF;
  padding: 12px 24px;
  border: 1px solid rgba(109, 0, 255, 0.5);
  border-radius: 8px;
  font-weight: 500;
  transition: all 0.3s ease;
}

.btn-outline:hover {
  background: rgba(109, 0, 255, 0.1);
  border-color: #6D00FF;
  box-shadow: 0 0 20px rgba(109, 0, 255, 0.3);
}
```

### Ghost Button

```css
.btn-ghost {
  background: transparent;
  color: rgba(255, 255, 255, 0.7);
  padding: 12px 24px;
  border: none;
  border-radius: 8px;
  font-weight: 500;
  transition: all 0.3s ease;
}

.btn-ghost:hover {
  color: white;
  background: rgba(255, 255, 255, 0.05);
}
```

### Ambient Glow / Spotlight

```css
.spotlight {
  position: relative;
}

.spotlight::before {
  content: '';
  position: absolute;
  top: -50%;
  left: 50%;
  transform: translateX(-50%);
  width: 300px;
  height: 300px;
  background: radial-gradient(
    circle,
    rgba(109, 0, 255, 0.15) 0%,
    transparent 70%
  );
  pointer-events: none;
  z-index: 0;
}
```

### Border Gradient Effect

```css
.border-gradient {
  position: relative;
  background: #0A0A0A;
  border-radius: 16px;
}

.border-gradient::before {
  content: '';
  position: absolute;
  inset: 0;
  border-radius: 16px;
  padding: 1px;
  background: linear-gradient(
    135deg,
    rgba(109, 0, 255, 0.5),
    transparent 50%,
    rgba(109, 0, 255, 0.2)
  );
  -webkit-mask: 
    linear-gradient(#fff 0 0) content-box,
    linear-gradient(#fff 0 0);
  mask: 
    linear-gradient(#fff 0 0) content-box,
    linear-gradient(#fff 0 0);
  -webkit-mask-composite: xor;
  mask-composite: exclude;
}
```

## Selection & Scrollbar

```css
::selection {
  background: rgba(109, 0, 255, 0.3);
  color: white;
}

::-webkit-scrollbar {
  width: 8px;
}

::-webkit-scrollbar-track {
  background: #050505;
}

::-webkit-scrollbar-thumb {
  background: rgba(109, 0, 255, 0.3);
  border-radius: 4px;
}

::-webkit-scrollbar-thumb:hover {
  background: rgba(109, 0, 255, 0.5);
}
```

## Component Patterns

### Pricing Card

```jsx
import { Check } from 'lucide-react';

<div className="bg-[#0A0A0A]/80 backdrop-blur-xl border border-white/10 
  rounded-2xl p-8 hover:border-[#6D00FF]/30 hover:-translate-y-2 
  hover:shadow-[0_20px_40px_rgba(109,0,255,0.15)] 
  transition-all duration-600 ease-[cubic-bezier(0.4,0,0.2,1)]">
  <h3 className="text-2xl font-semibold text-white">ASCEND</h3>
  <p className="text-4xl font-bold text-[#6D00FF] mt-4">$99<span className="text-lg text-white/50">/mes</span></p>
  <ul className="mt-6 space-y-3 text-white/70">
    <li className="flex items-center gap-3">
      <Check className="w-5 h-5 text-green-500 flex-shrink-0" />
      13 agentes de IA
    </li>
    <li className="flex items-center gap-3">
      <Check className="w-5 h-5 text-green-500 flex-shrink-0" />
      Programación personalizada
    </li>
    <li className="flex items-center gap-3">
      <Check className="w-5 h-5 text-green-500 flex-shrink-0" />
      Ajustes en tiempo real
    </li>
  </ul>
  <button className="mt-8 w-full py-3 bg-gradient-to-r from-[#6D00FF] to-[#5B21B6] 
    rounded-lg font-semibold hover:shadow-[0_0_30px_rgba(109,0,255,0.5)] 
    transition-all duration-300">
    Comenzar
  </button>
</div>
```

### Feature Card with Lucide Icon

```jsx
import { Flame } from 'lucide-react';

<div className="bg-[#0A0A0A]/80 backdrop-blur-xl border border-white/10 
  rounded-2xl p-8 hover:border-[#6D00FF]/30 hover:-translate-y-2 
  hover:shadow-[0_20px_40px_rgba(109,0,255,0.15)] 
  transition-all duration-600 ease-[cubic-bezier(0.4,0,0.2,1)]">
  <div className="w-14 h-14 rounded-xl bg-[#6D00FF]/10 border border-[#6D00FF]/20 
    flex items-center justify-center mb-5">
    <Flame className="w-7 h-7 text-[#6D00FF]" />
  </div>
  <h3 className="text-xl font-semibold text-white mb-3">BLAZE</h3>
  <p className="text-white/70 leading-relaxed">
    Optimización de entrenamientos y periodización inteligente.
  </p>
</div>
```

### Metric Display

```jsx
<div className="flex items-baseline gap-2">
  <span className="text-5xl font-mono font-bold text-white">+12</span>
  <span className="text-xl text-[#6D00FF]">kg</span>
  <span className="text-sm text-white/50">músculo</span>
</div>
```

## Quick Reference

| Element | Value |
|---------|-------|
| Primary Color | #6D00FF |
| Hover Color | #7D1AFF |
| Background | #050505 |
| Border Radius | 8px (buttons), 16px (cards) |
| Transition | 0.3-0.6s cubic-bezier(0.4, 0, 0.2, 1) |
| Card Hover | translateY(-8px) scale(1.02) |
| Glow Shadow | 0 0 30px rgba(109, 0, 255, 0.5) |

## HTML Template Pattern (PRODUCTION REFERENCE)

This is the EXACT template used in NGX Transform. Copy this structure for all HTML artifacts:

### Complete Base Template

```html
<!DOCTYPE html>
<html lang="es">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>NGX — Title</title>
  <link href="https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=JetBrains+Mono:wght@400;500;600;700&display=swap" rel="stylesheet">
  <style>
    /*══════════════════════════════════════════════════════════════════
      NGX DESIGN SYSTEM - PALETA CORRECTA
      
      Background: #050505
      Primary: #6D00FF
      Primary Hover: #7D1AFF
      Accent: #5B21B6
      Border Glass: rgba(255,255,255,0.1)
      
      SIN CYAN. SIN EXCEPCIONES.
    ══════════════════════════════════════════════════════════════════*/
    
    * { margin: 0; padding: 0; box-sizing: border-box; }
    
    :root {
      --background: #050505;
      --primary: #6D00FF;
      --primary-hover: #7D1AFF;
      --accent: #5B21B6;
      --foreground: #e6e6e6;
      --border-glass: rgba(255,255,255,0.1);
      --text-muted: #a3a3a3;
      --text-dim: #737373;
      --text-disabled: #525252;
    }
    
    ::selection { background: #6D00FF; color: white; }
    
    body {
      font-family: 'DM Sans', -apple-system, sans-serif;
      background: #050505;
      color: #e6e6e6;
      min-height: 100vh;
      -webkit-font-smoothing: antialiased;
      overflow-x: hidden;
    }
    
    ::-webkit-scrollbar { width: 6px; }
    ::-webkit-scrollbar-track { background: #0a0a0a; }
    ::-webkit-scrollbar-thumb { background: #6D00FF; border-radius: 9999px; }
  </style>
</head>
<body>
  <!-- Background Effects -->
  <div class="grid-bg"></div>
  <div class="orb orb-1"></div>
  <div class="orb orb-2"></div>
  <div class="orb orb-3"></div>
  
  <div class="container">
    <!-- Content -->
  </div>
</body>
</html>
```

### Background Effects (MANDATORY)

```css
.grid-bg {
  position: fixed;
  inset: 0;
  background-image: 
    linear-gradient(rgba(109,0,255,0.03) 1px, transparent 1px),
    linear-gradient(90deg, rgba(109,0,255,0.03) 1px, transparent 1px);
  background-size: 60px 60px;
  mask-image: radial-gradient(ellipse 80% 50% at 50% 50%, black 40%, transparent 100%);
  -webkit-mask-image: radial-gradient(ellipse 80% 50% at 50% 50%, black 40%, transparent 100%);
  pointer-events: none;
}

.orb {
  position: fixed;
  border-radius: 50%;
  filter: blur(80px);
  pointer-events: none;
  opacity: 0.15;
  animation: float 8s ease-in-out infinite;
}

.orb-1 { width: 500px; height: 500px; background: #6D00FF; top: 10%; left: 10%; }
.orb-2 { width: 400px; height: 400px; background: #5B21B6; bottom: 20%; right: 10%; animation-delay: 2s; }
.orb-3 { width: 300px; height: 300px; background: #6D00FF; top: 60%; left: 50%; animation-delay: 4s; }

@keyframes float {
  0%, 100% { transform: translate(0, 0); }
  25% { transform: translate(10px, -10px); }
  50% { transform: translate(20px, 0); }
  75% { transform: translate(10px, 10px); }
}
```

### Layout Container

```css
.container {
  position: relative;
  z-index: 10;
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 48px 16px;
}

.content {
  width: 100%;
  max-width: 512px;
}
```

### Glass Card

```css
.glass-card {
  background: linear-gradient(135deg, rgba(255,255,255,0.1), rgba(109,0,255,0.05));
  backdrop-filter: blur(16px) saturate(180%);
  -webkit-backdrop-filter: blur(16px) saturate(180%);
  border: 1px solid rgba(255,255,255,0.1);
  border-radius: 20px;
  padding: 32px;
  box-shadow: 
    0 30px 60px rgba(0,0,0,0.5),
    0 10px 20px rgba(109,0,255,0.15),
    inset 0 1px 1px rgba(255,255,255,0.1);
}

.card-title {
  font-size: 24px;
  font-weight: 600;
  color: #ffffff;
  margin-bottom: 8px;
  letter-spacing: -0.02em;
}

.card-subtitle {
  color: #a3a3a3;
  font-size: 15px;
  margin-bottom: 24px;
}
```

### Primary Button (with shimmer)

```css
.btn-primary {
  position: relative;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  padding: 16px 32px;
  border-radius: 12px;
  font-size: 15px;
  font-weight: 500;
  color: #ffffff;
  background: #6D00FF;
  border: none;
  cursor: pointer;
  overflow: hidden;
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  box-shadow: 0 0 15px -5px rgba(109,0,255,0.3);
  letter-spacing: 0.02em;
}

.btn-primary:hover {
  background: #7D1AFF;
  transform: translateY(-2px);
  box-shadow: 0 0 30px -5px rgba(109,0,255,0.5);
}

.btn-primary::after {
  content: '';
  position: absolute;
  inset: 0;
  background: linear-gradient(90deg, transparent, rgba(255,255,255,0.2), transparent);
  transform: translateX(-100%);
  transition: transform 0.7s ease-in-out;
}

.btn-primary:hover::after {
  transform: translateX(100%);
}

.btn-primary:disabled {
  background: #3d3d3d;
  cursor: not-allowed;
  opacity: 0.5;
  transform: none;
  box-shadow: none;
}
```

### Option Buttons (for quizzes/forms)

```css
.options {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.option-btn {
  width: 100%;
  padding: 16px 20px;
  border-radius: 12px;
  font-size: 15px;
  font-weight: 500;
  font-family: inherit;
  color: #d4d4d4;
  background: rgba(255,255,255,0.05);
  border: 1px solid rgba(255,255,255,0.1);
  cursor: pointer;
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  text-align: left;
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.option-btn:hover {
  transform: translateX(4px);
  border-color: rgba(109,0,255,0.3);
}

.option-btn.selected {
  color: #ffffff;
  background: linear-gradient(135deg, #6D00FF, #5B21B6);
  border: 1px solid rgba(109,0,255,0.5);
  box-shadow: 0 0 20px -5px rgba(109,0,255,0.5);
}

.option-check {
  width: 20px;
  height: 20px;
  border-radius: 50%;
  background: rgba(255,255,255,0.2);
  display: flex;
  align-items: center;
  justify-content: center;
}
```

### Inputs

```css
.input-group {
  display: flex;
  flex-direction: column;
  gap: 16px;
  margin-bottom: 24px;
}

.input {
  width: 100%;
  padding: 16px;
  border-radius: 12px;
  font-size: 15px;
  font-family: inherit;
  color: #ffffff;
  background: rgba(255,255,255,0.05);
  border: 1px solid rgba(255,255,255,0.1);
  outline: none;
  backdrop-filter: blur(20px);
  -webkit-backdrop-filter: blur(20px);
  transition: all 0.3s ease;
}

.input:focus {
  border-color: rgba(109,0,255,0.5);
  box-shadow: 0 0 0 2px rgba(109,0,255,0.2);
}

.input::placeholder { color: #525252; }

textarea.input {
  min-height: 120px;
  resize: none;
  line-height: 1.6;
}
```

### Progress Dots

```css
.progress-dots {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  margin-bottom: 32px;
}

.progress-dot {
  width: 8px;
  height: 8px;
  border-radius: 4px;
  background: rgba(255,255,255,0.1);
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}

.progress-dot.active {
  width: 24px;
  background: #6D00FF;
}

.progress-dot.completed {
  background: #6D00FF;
}
```

### Spots Badge (urgency element)

```css
.spots-badge {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  padding: 8px 16px;
  border-radius: 9999px;
  background: rgba(109,0,255,0.1);
  border: 1px solid rgba(109,0,255,0.3);
  margin-bottom: 24px;
}

.spots-dot {
  width: 8px;
  height: 8px;
  border-radius: 50%;
  background: #6D00FF;
  box-shadow: 0 0 10px #6D00FF;
  animation: pulse 2s ease-in-out infinite;
}

@keyframes pulse {
  0%, 100% { transform: scale(1); opacity: 1; }
  50% { transform: scale(1.2); opacity: 0.8; }
}

.spots-text {
  color: #fff;
  font-size: 13px;
  font-weight: 600;
}
```

### Hero Text

```css
.pre-title {
  color: #6D00FF;
  font-size: 14px;
  font-weight: 600;
  letter-spacing: 0.05em;
  margin-bottom: 12px;
}

.title {
  font-size: 48px;
  font-weight: 600;
  color: #ffffff;
  letter-spacing: -0.03em;
  line-height: 1.1;
  margin-bottom: 16px;
  text-shadow: 0 0 40px rgba(109,0,255,0.3);
}

/* GRADIENT TEXT - Only for accent words, NOT full titles */
.title-gradient {
  background: linear-gradient(90deg, #6D00FF, #7D1AFF);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

.subtitle {
  font-size: 17px;
  color: #a3a3a3;
  line-height: 1.6;
  margin-bottom: 32px;
}
```

### Social Proof

```css
.social-proof {
  display: flex;
  align-items: center;
  gap: 12px;
  margin-bottom: 32px;
}

.avatars {
  display: flex;
  margin-left: 8px;
}

.avatar {
  width: 32px;
  height: 32px;
  border-radius: 50%;
  border: 2px solid #050505;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 10px;
  font-weight: 600;
  color: #fff;
  margin-left: -8px;
}

.avatar:nth-child(1) { background: linear-gradient(135deg, #6D00FF, #5B21B6); }
.avatar:nth-child(2) { background: linear-gradient(135deg, #7D1AFF, #6D00FF); }
.avatar:nth-child(3) { background: linear-gradient(135deg, #5B21B6, #6D00FF); }
.avatar:nth-child(4) { background: linear-gradient(135deg, #6D00FF, #7D1AFF); }
.avatar:nth-child(5) { background: linear-gradient(135deg, #7D1AFF, #5B21B6); }

.social-text { color: #a3a3a3; font-size: 13px; }
.social-highlight { color: #fff; font-weight: 600; }
```

### Trust Badges

```css
.trust-badges {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 24px;
  margin-top: 48px;
  color: #525252;
  font-size: 12px;
}

.trust-item {
  display: flex;
  align-items: center;
  gap: 8px;
}
```

### Result States

```css
.result-icon {
  width: 80px;
  height: 80px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  margin: 0 auto 24px;
  font-size: 40px;
}

.result-icon.approved {
  background: linear-gradient(135deg, #6D00FF, #7D1AFF);
  box-shadow: 0 0 40px rgba(109,0,255,0.5);
}

.result-icon.waitlist {
  background: linear-gradient(135deg, #525252, #3d3d3d);
}

.result-title {
  font-size: 28px;
  font-weight: 600;
  color: #ffffff;
  margin-bottom: 8px;
  letter-spacing: -0.02em;
}

.result-description {
  color: #a3a3a3;
  font-size: 15px;
  margin-bottom: 24px;
  max-width: 360px;
  margin-left: auto;
  margin-right: auto;
}

.score-display {
  display: inline-flex;
  align-items: center;
  gap: 12px;
  padding: 12px 24px;
  border-radius: 9999px;
  background: rgba(255,255,255,0.05);
  border: 1px solid rgba(255,255,255,0.1);
  margin-bottom: 32px;
}

.score-label { color: #737373; font-size: 14px; }
.score-value { font-size: 24px; font-weight: 700; font-family: 'JetBrains Mono', monospace; }
.score-value.approved { color: #6D00FF; }
.score-value.waitlist { color: #a3a3a3; }
.score-max { color: #525252; font-size: 14px; }
```

### Success State (green only for success)

```css
.referral-success {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 8px 16px;
  border-radius: 8px;
  background: rgba(34, 197, 94, 0.1);
  border: 1px solid rgba(34, 197, 94, 0.3);
  color: #22c55e;
  font-size: 13px;
}
```

### Animations

```css
@keyframes fadeIn {
  from { opacity: 0; transform: translateY(10px); }
  to { opacity: 1; transform: translateY(0); }
}

.animate-in {
  animation: fadeIn 0.4s ease forwards;
}

.hidden { display: none !important; }
.text-center { text-align: center; }
.mt-8 { margin-top: 32px; }
.mb-4 { margin-bottom: 16px; }
```

### SVG Icons (Inline - NEVER use emojis)

```html
<!-- Sparkle -->
<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
  <path d="M12 3l1.5 4.5L18 9l-4.5 1.5L12 15l-1.5-4.5L6 9l4.5-1.5L12 3z"/>
  <path d="M5 19l.5 1.5L7 21l-1.5.5L5 23l-.5-1.5L3 21l1.5-.5L5 19z"/>
</svg>

<!-- Arrow Right -->
<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
  <path d="M5 12h14M12 5l7 7-7 7"/>
</svg>

<!-- Check -->
<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5">
  <polyline points="20 6 9 17 4 12"/>
</svg>

<!-- Shield -->
<svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
  <path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/>
</svg>

<!-- Clock -->
<svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
  <circle cx="12" cy="12" r="10"/>
  <polyline points="12 6 12 12 16 14"/>
</svg>

<!-- Bolt/Lightning -->
<svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
  <polygon points="13 2 3 14 12 14 11 22 21 10 12 10 13 2"/>
</svg>
```

### Responsive

```css
@media (max-width: 640px) {
  .title { font-size: 36px; }
  .trust-badges { flex-wrap: wrap; gap: 16px; }
  .glass-card { padding: 24px; }
}
```

---

## React Artifacts: MANDATORY Pattern

For React artifacts to render correctly, ALWAYS use this exact pattern:

```jsx
import React, { useState, useEffect } from 'react';
import { Flame, Check, ArrowRight } from 'lucide-react';

// MANDATORY: Inject global styles
const darkStyles = `
  * { box-sizing: border-box; }
  html, body, #root { 
    margin: 0; 
    padding: 0; 
    background: #050505 !important; 
    color: #fff !important;
    min-height: 100vh;
  }
  ::selection { background: #6D00FF; color: white; }
  @keyframes shimmer { 0% { transform: translateX(-100%); } 100% { transform: translateX(100%); } }
  @keyframes pulse { 0%, 100% { opacity: 1; } 50% { opacity: 0.6; } }
  @keyframes spin { to { transform: rotate(360deg); } }
`;

export default function Component() {
  // MANDATORY: Inject styles on mount
  useEffect(() => {
    const style = document.createElement('style');
    style.textContent = darkStyles;
    document.head.appendChild(style);
    document.body.style.background = '#050505';
    document.body.style.margin = '0';
    return () => style.remove();
  }, []);

  // ALL STYLES MUST BE INLINE - NO TAILWIND ARBITRARY VALUES
  return (
    <div style={{
      minHeight: '100vh',
      background: '#050505',
      color: '#fff',
      fontFamily: "'DM Sans', system-ui, sans-serif",
    }}>
      {/* Content with inline styles only */}
    </div>
  );
}
```

### Critical Rules for Artifacts

1. **ALWAYS inject darkStyles via useEffect** - Without this, background will be white
2. **NEVER use Tailwind arbitrary values** like `bg-[#050505]` - They don't compile
3. **ALL styles must be inline** using the `style={{}}` prop
4. **Use Lucide React for icons** - Import from 'lucide-react'
5. **Define animations in darkStyles string** - Not in separate CSS

### Inline Style Objects Pattern

```jsx
const glassCard = {
  background: 'rgba(10, 10, 10, 0.8)',
  backdropFilter: 'blur(20px)',
  WebkitBackdropFilter: 'blur(20px)',
  border: '1px solid rgba(255, 255, 255, 0.1)',
  borderRadius: 16,
  padding: 32,
  boxShadow: '0 4px 30px rgba(0,0,0,0.3), inset 0 1px 0 rgba(255,255,255,0.05)',
};

const primaryBtn = {
  display: 'inline-flex',
  alignItems: 'center',
  gap: 8,
  padding: '14px 28px',
  background: 'linear-gradient(135deg, #6D00FF 0%, #5B21B6 100%)',
  color: '#fff',
  border: 'none',
  borderRadius: 8,
  fontSize: 16,
  fontWeight: 600,
  cursor: 'pointer',
};

const iconBox = {
  width: 56,
  height: 56,
  borderRadius: 12,
  background: 'rgba(109, 0, 255, 0.1)',
  border: '1px solid rgba(109, 0, 255, 0.2)',
  display: 'flex',
  alignItems: 'center',
  justifyContent: 'center',
};
```

## Checklist

Before finalizing any UI:
- ✅ Violet (#6D00FF) is primary color
- ✅ No cyan or blue colors
- ✅ Glassmorphism with backdrop-blur
- ✅ Multiple shadow layers
- ✅ Smooth transitions (cubic-bezier)
- ✅ Hover states with glow effects
- ✅ Dark background (#050505)
- ⛔ NO EMOJIS - Only Lucide React SVGs
- ⛔ NO GRADIENT TEXT on headings - Solid colors only
- ⛔ NO checkmark emojis (✓) - Use `<Check />` from lucide-react
- ⛔ NO TAILWIND ARBITRARY VALUES in artifacts - Use inline styles
- ✅ ALWAYS useEffect to inject dark mode CSS
