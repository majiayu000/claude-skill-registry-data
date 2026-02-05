---
name: wordpress-magic-seo-frontend-2026
description: Create cutting-edge WordPress plugin admin interfaces using 2026 design trends for AI-powered SEO tools. Use this skill when building WordPress admin dashboards, settings pages, or React-based plugin UIs. Implements fluid organic layouts, glassmorphism effects, Transformative Teal color theory, micro-delight interactions, and spatial depth. Optimized for AI-first experiences with humanized design elements that avoid generic AI aesthetics. Generates production-ready WordPress admin code following 2026 frontend best practices.
---

# WordPress Magic SEO Frontend Design Skill (2026 Edition)

This skill guides creation of next-generation WordPress plugin admin interfaces using 2026 design trends: fluid organic layouts, glassmorphism depth, earth-first color palettes, kinetic typography, micro-delight animations, and AI-contextual personalization. Built for AI-powered SEO automation tools that feel human, intelligent, and environmentally conscious.

## 2026 Design Philosophy: "Transformative Intelligence"

**Core Principles:**
- **Fluid Organic Layouts**: Break free from rigid grids—use asymmetric compositions, flowing shapes, soft borders
- **Glassmorphism Depth**: Frosted glass surfaces with blur, transparency, and layered spatial hierarchy
- **Earth-First Color Theory**: Transformative Teal (2026 Color of the Year) with earthy naturals and vibrant accent pops
- **Micro-Delight Interactions**: Purposeful animations that reduce cognitive load and create memorable moments
- **Humanized AI**: Hand-drawn accents, imperfect elements, warmth that contrasts AI precision
- **Accessible by Default**: WCAG AAA compliance, dark mode support, reduced motion options

**NEVER:**
- Use outdated purple gradients (2020-2024 AI cliché)
- Apply rigid grid systems without fluid elements
- Create flat, lifeless interfaces without depth
- Ignore accessibility for aesthetic appeal
- Use generic system fonts (Inter, Roboto, Arial)
- Apply solid colors without considering transparency and layering

## User Context

**Target User:** WordPress niche site owners
- Managing content websites with SEO focus
- Limited technical expertise but high content/marketing savvy
- Want powerful automation without complexity
- Expect modern, consumer-app-like experiences

**Key Tasks:**
1. Run AI content optimizations on existing posts
2. Generate/regenerate images using AI
3. Monitor content health metrics from GSC data
4. Configure API connections (Anthropic, Google, Vercel)
5. Review before/after comparisons

## WordPress Integration Requirements

### Technical Constraints

**Framework Options:**
1. **React with @wordpress/element** (Preferred for complex UIs)
   - Use WordPress's built-in React
   - Enqueue with `wp_enqueue_script()` dependency: `['wp-element', 'wp-components']`
   - Mount to `<div id="magic-seo-root"></div>`

2. **Vanilla JS + WordPress Admin Classes** (For simpler interfaces)
   - Use standard WordPress admin markup patterns
   - Leverage `.wrap`, `.card`, `.notice` classes
   - Enhance with custom CSS and vanilla JS

**Code Structure:**
```php
// Main admin page callback
function magic_seo_admin_page() {
    ?>
    <div class="wrap magic-seo-dashboard">
        <div id="magic-seo-root"></div>
    </div>
    <?php
}

// Enqueue React app
function magic_seo_enqueue_scripts($hook) {
    if ($hook !== 'toplevel_page_magic-seo') return;
    
    wp_enqueue_script(
        'magic-seo-app',
        plugins_url('build/app.js', __FILE__),
        ['wp-element', 'wp-components', 'wp-api-fetch'],
        '1.0.0',
        true
    );
    
    wp_enqueue_style(
        'magic-seo-styles',
        plugins_url('build/app.css', __FILE__),
        [],
        '1.0.0'
    );
}
```

### AJAX/API Patterns

**WordPress REST API Integration:**
```javascript
// Use wp.apiFetch for WordPress REST calls
wp.apiFetch({
    path: '/magic-seo/v1/optimize',
    method: 'POST',
    data: {
        post_id: 123,
        keyword: 'target keyword',
        options: ['fix_title', 'enhance_content', 'generate_image']
    }
}).then(response => {
    // Handle success
}).catch(error => {
    // Handle error
});
```

**External API Calls (Python backend via Vercel):**
```javascript
// Direct fetch to Vercel endpoint
const response = await fetch('https://magic-seo.vercel.app/api/generate', {
    method: 'POST',
    headers: {
        'Content-Type': 'application/json',
        'X-Magic-SEO-Key': wpApiSettings.nonce
    },
    body: JSON.stringify({
        action: 'title_rewrite',
        content: currentContent,
        keyword: targetKeyword
    })
});
```

## Component Design Patterns (2026)

### 1. Glassmorphic Dashboard Cards

**Visual Design:**
- Frosted glass surface with backdrop blur
- Subtle transparency revealing background gradients
- Soft border glow
- Floating shadow for depth
- Fluid, organic corner radius (not uniform)

**Code Pattern:**
```jsx
const GlassCard = ({ value, label, icon, trend }) => (
    <div className="glass-card">
        <div className="glass-card__background"></div>
        <div className="glass-card__content">
            <div className="glass-card__icon">{icon}</div>
            <div className="glass-card__value">{value}</div>
            <div className="glass-card__label">{label}</div>
            {trend && (
                <div className="glass-card__trend">
                    <TrendIndicator value={trend} />
                </div>
            )}
        </div>
    </div>
);

/* CSS - Glassmorphism 2026 */
.glass-card {
    position: relative;
    background: rgba(255, 255, 255, 0.08);
    backdrop-filter: blur(12px) saturate(180%);
    -webkit-backdrop-filter: blur(12px) saturate(180%);
    border: 1px solid rgba(255, 255, 255, 0.18);
    border-radius: 24px 28px 24px 32px; /* Organic, asymmetric */
    padding: clamp(20px, 4vw, 32px);
    box-shadow: 
        0 8px 32px rgba(0, 168, 150, 0.08),
        inset 0 1px 0 rgba(255, 255, 255, 0.25);
    transition: all 0.4s cubic-bezier(0.23, 1, 0.32, 1);
    overflow: hidden;
}

.glass-card::before {
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    height: 1px;
    background: linear-gradient(
        90deg, 
        transparent, 
        rgba(255, 255, 255, 0.4), 
        transparent
    );
}

.glass-card:hover {
    transform: translateY(-4px) scale(1.01);
    border-color: rgba(0, 168, 150, 0.3);
    box-shadow: 
        0 16px 48px rgba(0, 168, 150, 0.15),
        inset 0 1px 0 rgba(255, 255, 255, 0.4);
}

.glass-card__background {
    position: absolute;
    inset: 0;
    background: radial-gradient(
        circle at 120% 20%,
        rgba(0, 168, 150, 0.12) 0%,
        transparent 50%
    );
    opacity: 0;
    transition: opacity 0.4s ease;
}

.glass-card:hover .glass-card__background {
    opacity: 1;
}

.glass-card__value {
    font-family: var(--font-display);
    font-size: var(--text-4xl);
    font-weight: 700;
    line-height: 1;
    background: linear-gradient(135deg, var(--teal-600), var(--teal-400));
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    margin: 12px 0 8px;
}

.glass-card__label {
    font-family: var(--font-accent);
    font-size: var(--text-xs);
    text-transform: uppercase;
    letter-spacing: 0.08em;
    color: var(--warm-gray-500);
    font-weight: 500;
}

/* Accessibility: Reduced motion */
@media (prefers-reduced-motion: reduce) {
    .glass-card {
        transition: none;
    }
    .glass-card:hover {
        transform: none;
    }
}
```

### 2. Fluid Organic "Optimization Station"

**Visual Design (2026 Update):**
- Asymmetric layout with flowing shapes
- Glassmorphic input fields
- Morphing toggle switches with liquid animation
- Segmented control with sliding glass indicator
- Primary CTA: Teal gradient with mesh texture overlay

**Code Pattern:**
```jsx
const OptimizationStation = () => {
    const [url, setUrl] = useState('');
    const [keyword, setKeyword] = useState('');
    const [options, setOptions] = useState({
        fixTitle: true,
        enhanceContent: true,
        generateImage: true
    });
    const [style, setStyle] = useState('authentic');
    const [isRunning, setIsRunning] = useState(false);

    return (
        <div className="optimization-station">
            <div className="station-blob-bg">
                <div className="blob blob-1"></div>
                <div className="blob blob-2"></div>
            </div>
            
            <h2 className="station-title">
                ✨ Optimization Station
            </h2>
            
            <div className="station-inputs">
                <GlassInput
                    type="url"
                    placeholder="https://griddleking.com/my-post..."
                    value={url}
                    onChange={setUrl}
                    icon="🔗"
                />
                <GlassInput
                    type="text"
                    placeholder="target keyword"
                    value={keyword}
                    onChange={setKeyword}
                    icon="🎯"
                />
            </div>

            <div className="station-options">
                <LiquidToggle
                    label="Fix Title (High CTR)"
                    checked={options.fixTitle}
                    onChange={v => setOptions({...options, fixTitle: v})}
                />
                <LiquidToggle
                    label="Enhance Content"
                    checked={options.enhanceContent}
                    onChange={v => setOptions({...options, enhanceContent: v})}
                />
                <LiquidToggle
                    label="Generate Visuals"
                    checked={options.generateImage}
                    onChange={v => setOptions({...options, generateImage: v})}
                />
            </div>

            <FluidSegmentedControl
                options={[
                    { value: 'authentic', label: 'Authentic' },
                    { value: 'professional', label: 'Pro' },
                    { value: 'viral', label: 'Viral' }
                ]}
                value={style}
                onChange={setStyle}
            />

            <button
                className="btn-transformative"
                onClick={handleOptimize}
                disabled={isRunning}
            >
                {isRunning ? (
                    <>
                        <LiquidSpinner /> Transforming...
                    </>
                ) : (
                    <>
                        <SparkleIcon /> Run Optimization
                    </>
                )}
            </button>
        </div>
    );
};

/* CSS - Organic fluid station */
.optimization-station {
    position: relative;
    background: var(--cream);
    border-radius: 32px 40px 32px 36px;
    padding: clamp(32px, 5vw, 48px);
    box-shadow: 
        0 20px 60px rgba(0, 0, 0, 0.06),
        0 0 0 1px var(--warm-gray-200);
}

.station-blob-bg {
    position: absolute;
    inset: 0;
    overflow: hidden;
    border-radius: inherit;
    z-index: 0;
}

.blob {
    position: absolute;
    border-radius: 40% 60% 70% 30% / 40% 50% 60% 50%;
    filter: blur(40px);
    opacity: 0.15;
    animation: blob-morph 20s ease-in-out infinite;
}

.blob-1 {
    width: 300px;
    height: 300px;
    background: var(--teal-300);
    top: -150px;
    right: -100px;
}

.blob-2 {
    width: 250px;
    height: 250px;
    background: var(--mint);
    bottom: -100px;
    left: -80px;
    animation-delay: -10s;
}

@keyframes blob-morph {
    0%, 100% {
        border-radius: 40% 60% 70% 30% / 40% 50% 60% 50%;
        transform: rotate(0deg);
    }
    50% {
        border-radius: 70% 30% 50% 50% / 30% 60% 40% 70%;
        transform: rotate(180deg);
    }
}

/* Transformative CTA Button */
.btn-transformative {
    position: relative;
    background: linear-gradient(135deg, var(--teal-500) 0%, var(--teal-700) 100%);
    color: white;
    border: none;
    border-radius: 16px;
    padding: 18px 36px;
    font-family: var(--font-display);
    font-size: var(--text-lg);
    font-weight: 600;
    cursor: pointer;
    transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
    box-shadow: 
        0 8px 24px rgba(0, 168, 150, 0.25),
        inset 0 1px 0 rgba(255, 255, 255, 0.2);
    overflow: hidden;
}

.btn-transformative::before {
    content: '';
    position: absolute;
    inset: 0;
    background: url("data:image/svg+xml,%3Csvg width='100' height='100' xmlns='http://www.w3.org/2000/svg'%3E%3Cfilter id='noise'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.9' numOctaves='4' /%3E%3C/filter%3E%3Crect width='100' height='100' filter='url(%23noise)' opacity='0.05'/%3E%3C/svg%3E");
    opacity: 0.3;
    mix-blend-mode: overlay;
}

.btn-transformative:hover:not(:disabled) {
    transform: translateY(-2px);
    box-shadow: 
        0 12px 32px rgba(0, 168, 150, 0.35),
        inset 0 1px 0 rgba(255, 255, 255, 0.3);
}

.btn-transformative:active:not(:disabled) {
    transform: translateY(0);
}

.btn-transformative:disabled {
    opacity: 0.6;
    cursor: not-allowed;
}
```

### 3. iOS-Style Toggle Switch

**Code Pattern:**
```jsx
const ToggleSwitch = ({ checked, onChange, label }) => (
    <label className="toggle-wrapper">
        <input
            type="checkbox"
            checked={checked}
            onChange={e => onChange(e.target.checked)}
            className="toggle-input"
        />
        <span className="toggle-slider"></span>
        <span className="toggle-label">{label}</span>
    </label>
);

// CSS
.toggle-wrapper {
    display: flex;
    align-items: center;
    gap: 12px;
    cursor: pointer;
    user-select: none;
}

.toggle-input {
    position: absolute;
    opacity: 0;
    width: 0;
    height: 0;
}

.toggle-slider {
    position: relative;
    display: inline-block;
    width: 48px;
    height: 28px;
    background: #e5e7eb;
    border-radius: 14px;
    transition: background 0.3s ease;
}

.toggle-slider::after {
    content: '';
    position: absolute;
    width: 24px;
    height: 24px;
    left: 2px;
    top: 2px;
    background: white;
    border-radius: 50%;
    transition: transform 0.3s ease;
    box-shadow: 0 2px 4px rgba(0,0,0,0.1);
}

.toggle-input:checked + .toggle-slider {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
}

.toggle-input:checked + .toggle-slider::after {
    transform: translateX(20px);
}

.toggle-label {
    font-size: 14px;
    color: #374151;
}
```

### 4. Progress Stepper (Loading State)

**Visual Design:**
- Horizontal stepper with animated progress
- Purple gradient for active/completed steps
- Smooth transitions between steps
- Spinner animation for current step

**Code Pattern:**
```jsx
const ProgressStepper = ({ currentStep, steps }) => (
    <div className="progress-stepper">
        {steps.map((step, idx) => (
            <div
                key={idx}
                className={`step ${
                    idx < currentStep ? 'step--completed' :
                    idx === currentStep ? 'step--active' :
                    'step--pending'
                }`}
            >
                <div className="step-indicator">
                    {idx < currentStep ? (
                        <CheckIcon />
                    ) : idx === currentStep ? (
                        <Spinner />
                    ) : (
                        idx + 1
                    )}
                </div>
                <div className="step-label">{step}</div>
                {idx < steps.length - 1 && (
                    <div className="step-connector" />
                )}
            </div>
        ))}
    </div>
);

// Usage
<ProgressStepper
    currentStep={2}
    steps={[
        'Reading Content',
        'Claude is Thinking',
        'Imagen is Painting',
        'Finalizing'
    ]}
/>
```

### 5. Before/After Comparison Card

**Code Pattern:**
```jsx
const ComparisonCard = ({ before, after, label }) => (
    <div className="comparison-card">
        <div className="comparison-header">{label}</div>
        <div className="comparison-panels">
            <div className="comparison-panel comparison-panel--before">
                <div className="comparison-label">Before</div>
                <div className="comparison-content">{before}</div>
            </div>
            <div className="comparison-divider">→</div>
            <div className="comparison-panel comparison-panel--after">
                <div className="comparison-label">After</div>
                <div className="comparison-content">{after}</div>
            </div>
        </div>
    </div>
);

// CSS
.comparison-card {
    background: white;
    border-radius: 12px;
    padding: 24px;
    box-shadow: 0 2px 8px rgba(0,0,0,0.04);
}

.comparison-panels {
    display: grid;
    grid-template-columns: 1fr auto 1fr;
    gap: 16px;
    margin-top: 16px;
}

.comparison-panel {
    background: #f9fafb;
    border-radius: 8px;
    padding: 16px;
}

.comparison-panel--after {
    background: linear-gradient(135deg, #f3f4f6 0%, #e5e7eb 100%);
}

.comparison-label {
    font-size: 11px;
    text-transform: uppercase;
    letter-spacing: 0.5px;
    color: #6b7280;
    margin-bottom: 8px;
}

.comparison-divider {
    display: flex;
    align-items: center;
    color: #667eea;
    font-size: 24px;
}
```

## Typography: Variable Fonts + Kinetic Type (2026)

**Font Stack - Beyond System Defaults:**
```css
:root {
    /* Display: Variable font for kinetic effects */
    --font-display: 'Outfit Variable', 'Plus Jakarta Sans', system-ui, sans-serif;
    
    /* Body: Humanist sans-serif, warm and readable */
    --font-body: 'Satoshi', 'DM Sans', -apple-system, BlinkMacSystemFont, sans-serif;
    
    /* Accent: Slightly condensed for density */
    --font-accent: 'Manrope Variable', 'Inter', sans-serif;
    
    /* Mono: For code/technical content */
    --font-mono: 'JetBrains Mono', 'Cascadia Code', 'SF Mono', monospace;
    
    /* Variable font settings */
    --font-weight-light: 300;
    --font-weight-regular: 400;
    --font-weight-medium: 500;
    --font-weight-semibold: 600;
    --font-weight-bold: 700;
}

/* Load modern variable fonts */
@import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300..700&display=swap');
@import url('https://api.fontshare.com/v2/css?f[]=satoshi@400,500,700&display=swap');

body.magic-seo-page {
    font-family: var(--font-body);
    font-optical-sizing: auto;
    -webkit-font-smoothing: antialiased;
    -moz-osx-font-smoothing: grayscale;
    font-feature-settings: 'kern' 1, 'liga' 1, 'calt' 1;
}
```

**Type Scale (Fluid Typography):**
```css
:root {
    /* Responsive type scale using clamp() */
    --text-xs: clamp(0.69rem, 0.66rem + 0.17vw, 0.75rem);      /* 11-12px */
    --text-sm: clamp(0.83rem, 0.78rem + 0.24vw, 0.94rem);      /* 13-15px */
    --text-base: clamp(1rem, 0.93rem + 0.33vw, 1.13rem);       /* 16-18px */
    --text-lg: clamp(1.2rem, 1.09rem + 0.47vw, 1.41rem);       /* 19-23px */
    --text-xl: clamp(1.44rem, 1.28rem + 0.68vw, 1.76rem);      /* 23-28px */
    --text-2xl: clamp(1.73rem, 1.5rem + 0.98vw, 2.2rem);       /* 28-35px */
    --text-3xl: clamp(2.07rem, 1.76rem + 1.37vw, 2.75rem);     /* 33-44px */
    --text-4xl: clamp(2.49rem, 2.05rem + 1.87vw, 3.43rem);     /* 40-55px */
}

/* Typography hierarchy */
.heading-hero {
    font-family: var(--font-display);
    font-size: var(--text-4xl);
    font-weight: var(--font-weight-bold);
    line-height: 1.1;
    letter-spacing: -0.02em;
    font-variation-settings: 'wght' 700, 'wdth' 100;
}

.heading-section {
    font-family: var(--font-display);
    font-size: var(--text-2xl);
    font-weight: var(--font-weight-semibold);
    line-height: 1.3;
    letter-spacing: -0.01em;
}

.metric-value {
    font-family: var(--font-display);
    font-size: var(--text-4xl);
    font-weight: var(--font-weight-bold);
    line-height: 1;
    font-variant-numeric: tabular-nums;
    letter-spacing: -0.03em;
}

.label-caps {
    font-family: var(--font-accent);
    font-size: var(--text-xs);
    font-weight: var(--font-weight-medium);
    text-transform: uppercase;
    letter-spacing: 0.08em;
    color: var(--warm-gray-500);
}

.body-text {
    font-family: var(--font-body);
    font-size: var(--text-base);
    font-weight: var(--font-weight-regular);
    line-height: 1.6;
    color: var(--warm-gray-700);
}
```

**Kinetic Typography (2026 Trend):**
```jsx
// Animated weight shift on hover
const KineticButton = ({ children }) => (
    <button className="kinetic-btn">
        {children}
    </button>
);

/* CSS with variable font animation */
.kinetic-btn {
    font-family: var(--font-display);
    font-weight: 500;
    font-variation-settings: 'wght' 500;
    transition: font-variation-settings 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}

.kinetic-btn:hover {
    font-variation-settings: 'wght' 700;
}

/* Scroll-reactive heading weight */
.hero-title {
    font-variation-settings: 'wght' var(--scroll-weight);
    transition: font-variation-settings 0.1s ease-out;
}

/* JavaScript to animate based on scroll */
window.addEventListener('scroll', () => {
    const scrollPercent = window.scrollY / 500;
    const weight = Math.min(300 + (scrollPercent * 400), 700);
    document.documentElement.style.setProperty('--scroll-weight', weight);
});
```

**Typography Best Practices:**
- Use variable fonts for smooth weight transitions
- Implement fluid type scale with `clamp()` for true responsive typography
- Apply kinetic effects sparingly (hero sections, primary CTAs)
- Maintain WCAG AAA contrast ratios (7:1 for normal text, 4.5:1 for large)
- Use tabular numerals for metric displays
- Enable OpenType features: ligatures, kerning, contextual alternates

## 2026 Color Palette: Transformative Teal + Earth-First System

**Primary Palette:**
```css
:root {
    /* Transformative Teal (2026 Color of Year) - Coloro 092-37-14 */
    --teal-50: #e6f7f5;
    --teal-100: #b3e8e1;
    --teal-200: #80d9cd;
    --teal-300: #4dcab9;
    --teal-400: #26b8a3;
    --teal-500: #00a896;  /* Primary - Transformative Teal */
    --teal-600: #00968a;
    --teal-700: #007a6e;
    --teal-800: #005f52;
    --teal-900: #004436;
    
    /* Complementary Vibrant Accents (WGSN S/S 2026) */
    --fuchsia: #e91e63;     /* Electric Fuchsia - urgent actions */
    --amber: #ffb74d;       /* Amber Haze - warnings, highlights */
    --mint: #81c784;        /* Jelly Mint - success states */
    --coral: #ff6b6b;       /* Coral-orange - complementary to teal */
    
    /* Earth Tones (grounding, natural) */
    --terracotta: #d4826f;
    --clay: #c4a68a;
    --sand: #e8d9c3;
    --stone: #9e9e9e;
    
    /* Neutrals - Warm bias for humanization */
    --cream: #faf8f5;       /* Backgrounds - not pure white */
    --off-white: #f5f3f0;
    --warm-gray-100: #ebe9e5;
    --warm-gray-200: #d6d4cf;
    --warm-gray-300: #b8b5ae;
    --warm-gray-500: #7a7770;
    --warm-gray-700: #4a4741;
    --warm-gray-900: #2b2825;
    
    /* Glassmorphism overlays */
    --glass-white: rgba(255, 255, 255, 0.15);
    --glass-blur: 12px;
    --glass-border: rgba(255, 255, 255, 0.25);
    
    /* Semantic colors - tied to teal system */
    --success: var(--mint);
    --warning: var(--amber);
    --error: var(--coral);
    --info: var(--teal-400);
}
```

**Color Usage Philosophy:**

1. **Transformative Teal** (Primary):
   - Main CTAs, AI-powered features
   - Active states, selected items
   - Progress indicators, data visualizations
   - Links and interactive elements
   - Psychology: Trust + Innovation + Eco-consciousness

2. **Vibrant Accents** (Strategic pops):
   - Fuchsia: High-urgency actions, notifications
   - Amber: Warnings, important highlights
   - Mint: Success confirmations, positive feedback
   - Coral: Delete actions, critical warnings

3. **Earth Tones** (Grounding):
   - Secondary cards and panels
   - Dividers and subtle backgrounds
   - Illustrative elements
   - Creates warmth and authenticity

4. **Warm Neutrals** (Base):
   - Cream/off-white backgrounds (never pure #ffffff)
   - Text hierarchy from warm-gray-900 to warm-gray-500
   - Subtle borders and dividers
   - Humanizes the digital space

**Accessibility Requirements:**
- Teal-500 on cream background: 5.2:1 contrast (AA+ for large text)
- Warm-gray-900 on cream: 9.8:1 contrast (AAA compliant)
- All interactive elements: minimum 3:1 contrast ratio
- Dark mode: Invert to dark-teal-900 base with teal-300 accents

## Animation & Micro-Delight (2026)

**Principles - Functional Animation:**
- **Purposeful motion** reduces cognitive load, not just decoration
- **Micro-delight** creates memorable moments through subtle unexpected behavior
- **Natural easing** mimics physics: spring animations, bounce, elastic
- **Performance-first** uses transform/opacity only, GPU-accelerated
- **Respects preferences** honors `prefers-reduced-motion`

**Spring-Based Easing (2026 Standard):**
```css
:root {
    /* Spring physics easing curves */
    --ease-spring: cubic-bezier(0.68, -0.55, 0.265, 1.55);
    --ease-bounce: cubic-bezier(0.68, -0.6, 0.32, 1.6);
    --ease-elastic: cubic-bezier(0.87, -0.41, 0.19, 1.44);
    --ease-smooth: cubic-bezier(0.4, 0, 0.2, 1);
    
    /* Duration tokens */
    --duration-instant: 100ms;
    --duration-quick: 200ms;
    --duration-normal: 300ms;
    --duration-slow: 500ms;
    --duration-slower: 700ms;
}
```

**Micro-Delight Examples:**

1. **Liquid Toggle Switch** (Beyond iOS):
```jsx
const LiquidToggle = ({ checked, onChange, label }) => {
    return (
        <label className="liquid-toggle">
            <input
                type="checkbox"
                checked={checked}
                onChange={e => onChange(e.target.checked)}
                className="liquid-toggle__input"
            />
            <div className="liquid-toggle__track">
                <div className="liquid-toggle__thumb">
                    <div className="liquid-toggle__liquid"></div>
                </div>
            </div>
            <span className="liquid-toggle__label">{label}</span>
        </label>
    );
};

/* CSS - Liquid morphing animation */
.liquid-toggle {
    display: flex;
    align-items: center;
    gap: 12px;
    cursor: pointer;
    user-select: none;
}

.liquid-toggle__input {
    position: absolute;
    opacity: 0;
    width: 0;
    height: 0;
}

.liquid-toggle__track {
    position: relative;
    width: 56px;
    height: 32px;
    background: var(--warm-gray-200);
    border-radius: 16px;
    transition: background 0.4s var(--ease-smooth);
}

.liquid-toggle__thumb {
    position: absolute;
    width: 28px;
    height: 28px;
    left: 2px;
    top: 2px;
    background: white;
    border-radius: 50%;
    transition: transform 0.5s var(--ease-elastic);
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.15);
    overflow: hidden;
}

.liquid-toggle__liquid {
    position: absolute;
    inset: 0;
    background: radial-gradient(circle, var(--teal-400), var(--teal-600));
    border-radius: 50%;
    transform: scale(0);
    transition: transform 0.6s var(--ease-elastic);
}

.liquid-toggle__input:checked + .liquid-toggle__track {
    background: var(--teal-100);
}

.liquid-toggle__input:checked + .liquid-toggle__track .liquid-toggle__thumb {
    transform: translateX(24px);
}

.liquid-toggle__input:checked + .liquid-toggle__track .liquid-toggle__liquid {
    transform: scale(1);
}

/* Squish effect on press */
.liquid-toggle__input:active + .liquid-toggle__track .liquid-toggle__thumb {
    transform: scaleX(1.2) scaleY(0.9);
}

.liquid-toggle__input:checked:active + .liquid-toggle__track .liquid-toggle__thumb {
    transform: translateX(24px) scaleX(1.2) scaleY(0.9);
}
```

2. **Button with Haptic Feedback Feel**:
```jsx
const HapticButton = ({ children, onClick, ...props }) => {
    const [isPressed, setIsPressed] = useState(false);
    
    return (
        <button
            className={`haptic-btn ${isPressed ? 'is-pressed' : ''}`}
            onMouseDown={() => setIsPressed(true)}
            onMouseUp={() => setIsPressed(false)}
            onMouseLeave={() => setIsPressed(false)}
            onClick={onClick}
            {...props}
        >
            <span className="haptic-btn__bg"></span>
            <span className="haptic-btn__content">{children}</span>
        </button>
    );
};

/* CSS */
.haptic-btn {
    position: relative;
    border: none;
    background: transparent;
    padding: 14px 28px;
    border-radius: 12px;
    cursor: pointer;
    font-family: var(--font-display);
    font-weight: 600;
    overflow: hidden;
    transition: transform 0.2s var(--ease-spring);
}

.haptic-btn__bg {
    position: absolute;
    inset: 0;
    background: var(--teal-500);
    border-radius: inherit;
    transition: transform 0.3s var(--ease-elastic);
}

.haptic-btn__content {
    position: relative;
    z-index: 1;
    color: white;
    display: flex;
    align-items: center;
    gap: 8px;
}

.haptic-btn:hover .haptic-btn__bg {
    transform: scale(1.05);
}

.haptic-btn.is-pressed .haptic-btn__bg {
    transform: scale(0.95);
}

.haptic-btn:active {
    transform: scale(0.98);
}
```

3. **Morphing Progress Indicator**:
```jsx
const MorphingProgress = ({ steps, currentStep }) => {
    return (
        <div className="morphing-progress">
            {steps.map((step, idx) => (
                <div
                    key={idx}
                    className={`morph-step ${
                        idx < currentStep ? 'is-complete' :
                        idx === currentStep ? 'is-active' :
                        'is-pending'
                    }`}
                >
                    <div className="morph-step__dot">
                        {idx < currentStep && (
                            <svg className="morph-step__check" viewBox="0 0 16 16">
                                <path
                                    d="M3 8l3 3 7-7"
                                    fill="none"
                                    stroke="currentColor"
                                    strokeWidth="2"
                                    strokeLinecap="round"
                                />
                            </svg>
                        )}
                        {idx === currentStep && (
                            <div className="morph-step__ripple"></div>
                        )}
                    </div>
                    <div className="morph-step__label">{step}</div>
                    {idx < steps.length - 1 && (
                        <div className="morph-connector">
                            <div 
                                className="morph-connector__fill"
                                style={{ 
                                    width: idx < currentStep ? '100%' : '0%' 
                                }}
                            ></div>
                        </div>
                    )}
                </div>
            ))}
        </div>
    );
};

/* CSS */
.morph-step__dot {
    width: 32px;
    height: 32px;
    border-radius: 50%;
    background: var(--warm-gray-200);
    display: flex;
    align-items: center;
    justify-content: center;
    position: relative;
    transition: all 0.5s var(--ease-spring);
}

.morph-step.is-complete .morph-step__dot {
    background: var(--teal-500);
    transform: rotate(360deg);
}

.morph-step.is-active .morph-step__dot {
    background: var(--teal-400);
    transform: scale(1.15);
}

.morph-step__check {
    width: 16px;
    height: 16px;
    color: white;
    animation: check-draw 0.5s var(--ease-spring);
}

@keyframes check-draw {
    0% {
        stroke-dasharray: 0 20;
    }
    100% {
        stroke-dasharray: 20 20;
    }
}

.morph-step__ripple {
    position: absolute;
    inset: 0;
    border-radius: 50%;
    border: 2px solid var(--teal-400);
    animation: ripple-pulse 2s var(--ease-smooth) infinite;
}

@keyframes ripple-pulse {
    0% {
        transform: scale(1);
        opacity: 1;
    }
    100% {
        transform: scale(1.8);
        opacity: 0;
    }
}

.morph-connector {
    flex: 1;
    height: 2px;
    background: var(--warm-gray-200);
    position: relative;
    margin: 0 8px;
}

.morph-connector__fill {
    position: absolute;
    inset: 0;
    background: linear-gradient(90deg, var(--teal-500), var(--teal-400));
    transition: width 0.8s var(--ease-smooth);
}
```

4. **Scroll-Triggered Reveal Animations**:
```jsx
// Use Intersection Observer for performance
const useScrollReveal = (threshold = 0.1) => {
    const [isVisible, setIsVisible] = useState(false);
    const ref = useRef(null);
    
    useEffect(() => {
        const observer = new IntersectionObserver(
            ([entry]) => {
                if (entry.isIntersecting) {
                    setIsVisible(true);
                }
            },
            { threshold }
        );
        
        if (ref.current) {
            observer.observe(ref.current);
        }
        
        return () => observer.disconnect();
    }, [threshold]);
    
    return [ref, isVisible];
};

// Component usage
const RevealCard = ({ children, delay = 0 }) => {
    const [ref, isVisible] = useScrollReveal();
    
    return (
        <div
            ref={ref}
            className={`reveal-card ${isVisible ? 'is-visible' : ''}`}
            style={{ '--reveal-delay': `${delay}ms` }}
        >
            {children}
        </div>
    );
};

/* CSS */
.reveal-card {
    opacity: 0;
    transform: translateY(30px);
    transition: 
        opacity 0.6s var(--ease-smooth) var(--reveal-delay),
        transform 0.6s var(--ease-spring) var(--reveal-delay);
}

.reveal-card.is-visible {
    opacity: 1;
    transform: translateY(0);
}
```

**Accessibility & Performance:**
```css
/* Respect user preferences */
@media (prefers-reduced-motion: reduce) {
    *,
    *::before,
    *::after {
        animation-duration: 0.01ms !important;
        animation-iteration-count: 1 !important;
        transition-duration: 0.01ms !important;
    }
    
    .liquid-toggle__thumb {
        transition: transform 0.2s ease;
    }
    
    .reveal-card {
        opacity: 1;
        transform: none;
    }
}

/* GPU acceleration */
.gpu-accelerated {
    will-change: transform;
    transform: translateZ(0);
}

/* Remove will-change after animation */
.gpu-accelerated:not(:hover):not(.is-animating) {
    will-change: auto;
}
```

## Settings Page Pattern

For the "Settings & Connections" tab:

```jsx
const SettingsPage = () => {
    const [apiKeys, setApiKeys] = useState({
        anthropic: '',
        gemini: '',
        openai: ''
    });
    
    return (
        <div className="settings-page">
            <div className="settings-section">
                <h3 className="settings-section-title">API Connections</h3>
                <p className="settings-section-desc">
                    Connect the AI services that power your content optimization.
                </p>
                
                <div className="settings-fields">
                    <ApiKeyField
                        label="Anthropic API Key"
                        value={apiKeys.anthropic}
                        onChange={v => setApiKeys({...apiKeys, anthropic: v})}
                        placeholder="sk-ant-..."
                        helpText="Used for Claude-powered title and content optimization"
                    />
                    
                    <ApiKeyField
                        label="Google Gemini API Key"
                        value={apiKeys.gemini}
                        onChange={v => setApiKeys({...apiKeys, gemini: v})}
                        placeholder="AIza..."
                        helpText="Used for Imagen 4 image generation"
                    />
                </div>
                
                <button className="btn-save">
                    Save Settings
                </button>
            </div>
        </div>
    );
};

const ApiKeyField = ({ label, value, onChange, placeholder, helpText }) => (
    <div className="field">
        <label className="field-label">{label}</label>
        <input
            type="password"
            className="field-input field-input--secret"
            value={value}
            onChange={e => onChange(e.target.value)}
            placeholder={placeholder}
        />
        {helpText && (
            <p className="field-help">{helpText}</p>
        )}
    </div>
);
```

## Media Studio Pattern

Grid layout with asset cards:

```jsx
const MediaStudio = () => {
    const [assets, setAssets] = useState([]);
    const [generating, setGenerating] = useState(false);
    
    return (
        <div className="media-studio">
            <div className="studio-generator">
                <input
                    type="text"
                    placeholder="Describe the image you want to generate..."
                    className="studio-input"
                />
                <select className="studio-style-select">
                    <option value="authentic">Authentic Griddle</option>
                    <option value="cinematic">Cinematic Macro</option>
                    <option value="landscape">Wide Landscape</option>
                </select>
                <button className="btn-magic" disabled={generating}>
                    {generating ? 'Generating...' : 'Generate Image'}
                </button>
            </div>
            
            <div className="asset-grid">
                {assets.map(asset => (
                    <AssetCard key={asset.id} asset={asset} />
                ))}
            </div>
        </div>
    );
};

const AssetCard = ({ asset }) => (
    <div className="asset-card">
        <img src={asset.url} alt={asset.prompt} />
        <div className="asset-actions">
            <button className="asset-btn">Download</button>
            <button className="asset-btn">To Media Library</button>
            <button className="asset-btn asset-btn--danger">Delete</button>
        </div>
    </div>
);

// CSS
.asset-grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
    gap: 20px;
    margin-top: 32px;
}

.asset-card {
    background: white;
    border-radius: 12px;
    overflow: hidden;
    box-shadow: 0 2px 8px rgba(0,0,0,0.04);
}

.asset-card img {
    width: 100%;
    height: 200px;
    object-fit: cover;
}

.asset-actions {
    padding: 12px;
    display: flex;
    gap: 8px;
}

.asset-btn {
    flex: 1;
    padding: 8px;
    font-size: 12px;
    border-radius: 6px;
    border: 1px solid var(--gray-300);
    background: white;
    cursor: pointer;
    transition: all 0.2s ease;
}

.asset-btn:hover {
    background: var(--gray-50);
}

.asset-btn--danger {
    color: var(--error);
    border-color: var(--error);
}
```

## WordPress Admin Integration

**Registering the Admin Page:**
```php
add_action('admin_menu', 'magic_seo_register_admin_page');

function magic_seo_register_admin_page() {
    add_menu_page(
        'Magic SEO',           // Page title
        'Magic SEO',           // Menu title
        'manage_options',      // Capability
        'magic-seo',           // Menu slug
        'magic_seo_render_page', // Callback
        'dashicons-superhero', // Icon (or custom SVG)
        30                     // Position
    );
}

function magic_seo_render_page() {
    ?>
    <div class="wrap magic-seo-wrap">
        <div id="magic-seo-root"></div>
    </div>
    <?php
}
```

**Loading Custom Fonts:**
```php
function magic_seo_enqueue_fonts() {
    // Load Inter for number displays
    wp_enqueue_style(
        'google-fonts-inter',
        'https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap',
        [],
        null
    );
}
add_action('admin_enqueue_scripts', 'magic_seo_enqueue_fonts');
```

## Humanization Elements (2026 Anti-AI-Slop)

**Philosophy:**
As AI-generated content floods the web, users crave authenticity. Humanization elements signal "real people made this" and create emotional connection.

**Techniques:**

1. **Hand-Drawn Accents** (SVG):
```jsx
// Underline effect - imperfect, organic
const HandDrawnUnderline = () => (
    <svg className="hand-underline" viewBox="0 0 200 10" preserveAspectRatio="none">
        <path
            d="M 0 5 Q 50 3, 100 5 T 200 5"
            stroke="var(--teal-400)"
            strokeWidth="2"
            fill="none"
            strokeLinecap="round"
        />
    </svg>
);

.hand-underline {
    position: absolute;
    bottom: -4px;
    left: 0;
    width: 100%;
    height: 10px;
    opacity: 0.6;
}

// Handwritten labels
.handwritten-note {
    font-family: 'Caveat', 'Permanent Marker', cursive;
    color: var(--teal-600);
    transform: rotate(-2deg);
    position: relative;
}
```

2. **Organic Shapes & Blobs**:
```css
/* Asymmetric, natural shapes */
.organic-panel {
    border-radius: 
        32% 68% 68% 32% / 
        52% 32% 68% 48%;
    background: linear-gradient(135deg, 
        var(--teal-50), 
        var(--cream)
    );
}

/* Animated morphing blob */
@keyframes morph {
    0%, 100% {
        border-radius: 60% 40% 30% 70% / 60% 30% 70% 40%;
    }
    50% {
        border-radius: 30% 60% 70% 40% / 50% 60% 30% 60%;
    }
}

.blob-accent {
    animation: morph 8s ease-in-out infinite;
}
```

3. **Imperfect Grids**:
```css
/* Fluid grid with intentional breaks */
.organic-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
    gap: clamp(16px, 3vw, 32px);
}

.organic-grid > :nth-child(3n) {
    grid-column: span 2;
}

.organic-grid > :nth-child(5n) {
    transform: translateY(20px);
}
```

4. **Textured Backgrounds** (Subtle noise):
```css
.textured-surface {
    background-image: 
        radial-gradient(circle at 20% 50%, var(--teal-50) 0%, transparent 50%),
        radial-gradient(circle at 80% 80%, var(--mint) 0%, transparent 50%),
        url("data:image/svg+xml,%3Csvg viewBox='0 0 200 200' xmlns='http://www.w3.org/2000/svg'%3E%3Cfilter id='noise'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.65' numOctaves='3' /%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23noise)' opacity='0.03'/%3E%3C/svg%3E");
    background-blend-mode: soft-light;
}
```

5. **Doodle Icons** (Instead of perfect SVGs):
```jsx
// Wobbly circle icon
const DoodleCircle = () => (
    <svg viewBox="0 0 100 100" className="doodle-icon">
        <path
            d="M 95 50 Q 95 20, 70 8 Q 50 0, 25 8 Q 5 20, 5 50 Q 5 75, 25 90 Q 50 100, 70 90 Q 95 75, 95 50"
            fill="none"
            stroke="var(--teal-500)"
            strokeWidth="3"
            strokeLinecap="round"
        />
    </svg>
);

.doodle-icon {
    width: 24px;
    height: 24px;
    filter: url(#rough);
}

/* SVG filter for hand-drawn effect */
<defs>
    <filter id="rough">
        <feTurbulence 
            type="turbulence" 
            baseFrequency="0.05" 
            numOctaves="2" 
            result="turbulence"
        />
        <feDisplacementMap 
            in2="turbulence" 
            in="SourceGraphic" 
            scale="2"
        />
    </filter>
</defs>
```

## Critical Guidelines (2026)

## Critical Guidelines (2026)

**DO:**
- Use Transformative Teal as primary color (not purple/indigo)
- Apply glassmorphism to create depth and hierarchy
- Implement fluid, organic layouts (break the grid intentionally)
- Add hand-drawn accents and imperfect elements for warmth
- Use variable fonts with kinetic typography effects
- Animate with spring physics (elastic, bounce easing)
- Implement micro-delight interactions that surprise
- Respect `prefers-reduced-motion` for accessibility
- Use warm neutral backgrounds (cream, not pure white)
- Layer transparent elements with backdrop-filter blur
- Create asymmetric, natural border-radius values
- Implement scroll-triggered reveals with Intersection Observer
- Test dark mode with proper contrast ratios
- Use gradient text for emphasis (background-clip: text)
- Add subtle texture/noise to surfaces
- Animate progress with morphing shapes

**DON'T:**
- Use outdated purple/indigo gradients (2020-2024 AI cliché)
- Create flat interfaces without depth/transparency
- Apply rigid 12-column grid systems without breaks
- Use generic system fonts (Inter, Roboto, Arial)
- Ignore glassmorphism accessibility (text must be readable)
- Animate everything (purposeful motion only)
- Use pure white (#ffffff) backgrounds
- Create uniform border-radius (16px on all corners)
- Forget about backdrop-filter browser support fallbacks
- Use low-contrast neumorphism (accessibility issue)
- Apply animations without performance consideration
- Ignore environmental sustainability (optimize assets)
- Use solid colors without transparency layers
- Create generic, template-like designs
- Overuse blur effects (performance impact)

**2026-Specific Principles:**

1. **Machine Experience (MX) Awareness**: While designing for humans, ensure semantic HTML and proper structure for AI agents that may parse the interface

2. **Performance = Sustainability**: Lighter code = less energy consumption. Optimize images, use modern formats (WebP, AVIF), lazy load

3. **Accessibility = Baseline**: WCAG AAA contrast ratios, keyboard navigation, screen reader support, focus indicators

4. **Dark Mode Native**: Design in dark mode first, then adapt to light mode (not reverse)

5. **Fluid Everything**: Use clamp() for typography, spacing, sizing. No fixed pixel values

6. **Component Composition**: Build with atomic design - small, reusable components that combine

7. **Progressive Enhancement**: Core functionality works without JavaScript, enhance with interactions

## Responsive Considerations

**Breakpoints:**
```css
/* Mobile first approach */
.dashboard-cards {
    display: grid;
    grid-template-columns: 1fr;
    gap: 16px;
}

/* Tablet */
@media (min-width: 768px) {
    .dashboard-cards {
        grid-template-columns: repeat(2, 1fr);
    }
}

/* Desktop */
@media (min-width: 1024px) {
    .dashboard-cards {
        grid-template-columns: repeat(3, 1fr);
        gap: 20px;
    }
}
```

## Success State Example

When "Run Magic Optimization" completes:

```jsx
const SuccessState = ({ results }) => (
    <div className="success-state">
        <div className="success-icon">✨</div>
        <h3 className="success-title">Optimization Complete!</h3>
        
        <ComparisonCard
            label="Title Optimization"
            before={results.title.before}
            after={results.title.after}
        />
        
        {results.image && (
            <div className="success-image">
                <img src={results.image.url} alt="Generated featured image" />
                <p className="image-caption">AI-generated featured image</p>
            </div>
        )}
        
        <div className="success-actions">
            <button className="btn-primary">Publish Changes</button>
            <button className="btn-secondary">Generate Again</button>
        </div>
    </div>
);
```

## Implementation Checklist (2026)

When implementing a WordPress plugin frontend using this skill:

### Phase 1: Foundation
1. ✅ Choose React (@wordpress/element) vs Vanilla JS
2. ✅ Set up proper WordPress script enqueueing with dependencies
3. ✅ Define Transformative Teal color system with CSS custom properties
4. ✅ Load variable fonts (Outfit, Satoshi, or similar)
5. ✅ Implement fluid type scale with clamp()
6. ✅ Set up dark mode color tokens

### Phase 2: Layout & Structure
7. ✅ Create fluid, organic grid system (not rigid)
8. ✅ Design glassmorphic card components
9. ✅ Implement backdrop-filter with fallbacks
10. ✅ Add asymmetric border-radius patterns
11. ✅ Create blob background animations
12. ✅ Build responsive breakpoint system

### Phase 3: Interactions
13. ✅ Implement liquid toggle switches
14. ✅ Create haptic-feel button components
15. ✅ Add morphing progress indicators
16. ✅ Set up scroll-triggered reveals (Intersection Observer)
17. ✅ Apply spring-based easing functions
18. ✅ Add micro-delight animations

### Phase 4: Humanization
19. ✅ Add hand-drawn SVG accents
20. ✅ Implement organic shape patterns
21. ✅ Create textured backgrounds with noise
22. ✅ Design doodle-style icons
23. ✅ Add warm neutral color adjustments

### Phase 5: Polish & Optimization
24. ✅ Test glassmorphism text contrast (WCAG AAA)
25. ✅ Implement `prefers-reduced-motion` support
26. ✅ Optimize animations for 60fps
27. ✅ Test dark mode thoroughly
28. ✅ Add keyboard navigation
29. ✅ Test with screen readers
30. ✅ Optimize image formats (WebP, AVIF)
31. ✅ Implement lazy loading
32. ✅ Test across WordPress versions (6.4+)
33. ✅ Validate semantic HTML structure (for AI/MX)
34. ✅ Check Core Web Vitals scores

### Phase 6: WordPress Integration
35. ✅ Integrate with WordPress REST API
36. ✅ Handle authentication/nonces properly
37. ✅ Implement error boundaries (React)
38. ✅ Add loading states for async operations
39. ✅ Test AJAX fallbacks for non-REST environments
40. ✅ Ensure RTL language support if needed

### Performance Targets (2026)
- **Lighthouse Score**: 95+ performance, 100 accessibility
- **Core Web Vitals**: 
  - LCP < 2.5s
  - FID < 100ms
  - CLS < 0.1
- **Bundle Size**: < 150KB gzipped for main JS
- **First Paint**: < 1.5s
- **Carbon Footprint**: Grade A on Website Carbon Calculator

## Example: Complete Dashboard Component

```jsx
import { useState, useEffect } from '@wordpress/element';
import apiFetch from '@wordpress/api-fetch';

const MagicSEODashboard = () => {
    const [metrics, setMetrics] = useState(null);
    const [loading, setLoading] = useState(true);
    
    useEffect(() => {
        apiFetch({ path: '/magic-seo/v1/metrics' })
            .then(data => {
                setMetrics(data);
                setLoading(false);
            });
    }, []);
    
    if (loading) {
        return <SkeletonLoader />;
    }
    
    return (
        <div className="magic-seo-dashboard">
            <header className="dashboard-header">
                <h1>Magic SEO Command Center</h1>
                <StatusIndicator status="online" />
            </header>
            
            <div className="dashboard-metrics">
                <MetricCard
                    value={metrics.quickWins}
                    label="Quick Wins Available"
                    icon="🚀"
                />
                <MetricCard
                    value={`${metrics.decaying}/${metrics.dominating}`}
                    label="Decaying / Dominating"
                    icon="📉"
                />
                <MetricCard
                    value="Claude 4.5 / Imagen 4"
                    label="Active AI Models"
                    icon="🧠"
                />
            </div>
            
            <OptimizationStation />
        </div>
    );
};

// Mount to WordPress
const root = document.getElementById('magic-seo-root');
if (root) {
    wp.element.render(<MagicSEODashboard />, root);
}
```

This skill will guide you to create a modern, distinctive WordPress plugin admin interface that feels premium, performs well, and delights users with its "Apple meets Outdoor Vlogging" aesthetic.