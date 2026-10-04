---
license: Apache-2.0
name: web-sales-design
description: High-converting web design techniques that dazzle and persuade. Covers social proof design, pricing page architecture, CTA optimization, scroll-driven persuasion, interactive demos, trust signals, and the visual craft behind sites that sell. Activate on 'sales page design', 'conversion design', 'high-converting', 'landing page that sells', 'pricing page design', 'social proof', 'dazzle', 'wow factor', 'persuasive design', 'conversion rate', 'make it sell'. NOT for copywriting (use marketing copywriting skills), not for A/B testing setup (use frontend-developer), not for paid ad creative (use marketing skills).
allowed-tools: Read,Write,Edit,Glob,Grep,WebSearch,WebFetch
metadata:
  category: Design & UX
  tags:
    - sales
    - conversion
    - persuasion
    - landing-page
    - pricing
    - social-proof
    - cta
    - trust
  pairs-with:
    - skill: hero-section-design
      reason: Hero is the first sales moment — sets conversion trajectory
    - skill: web-design-expert
      reason: General design foundation that sales design builds upon
    - skill: product-appeal-analyzer
      reason: Evaluates whether the design actually creates desire
    - skill: ux-friction-analyzer
      reason: Removes barriers between desire and action
    - skill: motion-design-web
      reason: Animations that demonstrate, reveal, and persuade
    - skill: webapp-paywall-implementation
      reason: The actual gate after the design has done its job
category: Design & Creative
tags:
  - sales-page
  - web-design
  - conversion
  - landing-page
  - marketing
---

# Web Sales Design

The craft of building websites that sell. Not marketing strategy, not copywriting, not A/B test infrastructure — the actual **design patterns, visual systems, and interactive techniques** that turn visitors into customers.

**Core principle**: The best sales design is invisible. Visitors don't think "this is selling to me." They think "this is exactly what I need." Every pixel, every scroll reveal, every social proof placement either builds trust and desire or erodes it. There is no neutral.

---

## When to Use

**Use for:**
- Designing landing pages that need to convert visitors to signups/purchases
- Building pricing pages with effective tier architecture
- Placing and designing social proof (testimonials, logos, case studies)
- Crafting CTA buttons that get clicked (size, color, copy, placement)
- Structuring long-form sales pages (problem-agitate-solve scroll sequences)
- Adding trust signals (security badges, guarantees, human faces)
- Creating interactive product demos and feature tours
- Building "wow moments" — scroll-triggered reveals, before/after comparisons
- Auditing existing pages for conversion design weaknesses

**Do NOT use for:**
- Copywriting and messaging strategy → use **product-appeal-analyzer** or copywriting skills
- A/B test implementation → use **frontend-developer**
- Paid ad creative → use marketing skills
- UX friction audits → use **ux-friction-analyzer** (complementary — run both)
- General web design → use **web-design-expert**
- Payment/subscription implementation → use **webapp-paywall-implementation**

---

## The Scroll-Driven Sales Page Blueprint

The modern long-form sales page follows a psychological arc. Each section has a job. Skip a section and the page leaks visitors.

### The 8-Section Structure

```
┌─────────────────────────────────────────────┐
│  1. HERO — Promise + Identity Signal        │  ← 0-5 seconds
│     "This is for people like me"            │
├─────────────────────────────────────────────┤
│  2. LOGO BAR — Social Proof Shortcut        │  ← 5-10 seconds
│     "Trusted by names I recognize"          │
├─────────────────────────────────────────────┤
│  3. PROBLEM — Pain Acknowledged             │  ← 10-30 seconds
│     "They understand my situation"          │
├─────────────────────────────────────────────┤
│  4. AGITATE — Consequences of Inaction      │  ← 30-60 seconds
│     "This is worse than I thought"          │
├─────────────────────────────────────────────┤
│  5. SOLUTION — Product as Resolution        │  ← 1-2 minutes
│     "Here's how it works + demo"            │
├─────────────────────────────────────────────┤
│  6. PROOF — Deep Social Proof               │  ← 2-3 minutes
│     "Real people, real results"             │
├─────────────────────────────────────────────┤
│  7. PRICING — Offer Architecture            │  ← 3-4 minutes
│     "Clear value, obvious choice"           │
├─────────────────────────────────────────────┤
│  8. FINAL CTA — Urgency + Guarantee         │  ← Decision point
│     "Risk-free, act now"                    │
└─────────────────────────────────────────────┘
```

### Section-by-Section Implementation

#### Section 1: Hero (The 5-Second Verdict)

The hero decides if visitors stay or leave. Every element must earn its pixel.

**Layout pattern — the converging hero:**

```tsx
function HeroSection() {
  return (
    <section className="hero">
      {/* Eyebrow — credibility in a whisper */}
      <p className="hero-eyebrow">Trusted by 2,400+ engineering teams</p>

      {/* Headline — one promise, benefit-driven */}
      <h1 className="hero-headline">
        Ship features in hours,<br />not sprints
      </h1>

      {/* Subheadline — how, in one sentence */}
      <p className="hero-subheadline">
        AI-powered workflow automation that turns your backlog
        into deployed code — reviewed, tested, and ready.
      </p>

      {/* CTA cluster — primary + low-commitment secondary */}
      <div className="hero-cta-cluster">
        <a href="/signup" className="cta-primary">
          Start building free
        </a>
        <a href="/demo" className="cta-secondary">
          Watch 2-min demo
        </a>
      </div>

      {/* Visual proof — product in action, not a screenshot */}
      <div className="hero-visual">
        <video autoPlay muted loop playsInline>
          <source src="/demo-clip.mp4" type="video/mp4" />
        </video>
      </div>
    </section>
  );
}
```

```css
.hero {
  padding: 5rem 2rem 4rem;
  text-align: center;
  max-width: 800px;
  margin: 0 auto;
}

.hero-eyebrow {
  font-size: 0.875rem;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.05em;
  color: var(--color-primary);
  margin-bottom: 1rem;
}

.hero-headline {
  font-size: clamp(2.25rem, 5vw, 3.75rem);
  font-weight: 800;
  line-height: 1.1;
  letter-spacing: -0.025em;
  margin-bottom: 1.25rem;
}

.hero-subheadline {
  font-size: clamp(1.125rem, 2vw, 1.375rem);
  line-height: 1.6;
  color: var(--color-text-secondary);
  max-width: 600px;
  margin: 0 auto 2rem;
}

.hero-cta-cluster {
  display: flex;
  gap: 1rem;
  justify-content: center;
  flex-wrap: wrap;
  margin-bottom: 3rem;
}
```

**What the best do differently** (Stripe, Linear, Vercel, Notion):
- **Stripe**: Animated gradient backgrounds that feel alive, not decorative. Product capability revealed through micro-interactions — you scroll and the product demos itself.
- **Linear**: Dark mode that signals "power tool for serious builders." Zero visual waste. The design IS the product promise — speed and precision.
- **Vercel**: Typography-forward hero with one line that frames the entire product. CTA is "Start Deploying" not "Sign Up" — action-oriented.
- **Notion**: Shows the product working, not a screenshot. The hero IS a mini-demo.

#### Section 2: Logo Bar (The Trust Shortcut)

4-6 recognizable logos. Not 20. Quantity dilutes; quality validates.

```tsx
function LogoBar() {
  return (
    <section className="logo-bar">
      <p className="logo-bar-label">
        Trusted by teams at
      </p>
      <div className="logo-bar-logos">
        {logos.map(logo => (
          <img
            key={logo.name}
            src={logo.src}
            alt={logo.name}
            className="logo-bar-logo"
          />
        ))}
      </div>
    </section>
  );
}
```

```css
.logo-bar {
  padding: 2rem 2rem;
  text-align: center;
  border-top: 1px solid var(--color-border-subtle);
  border-bottom: 1px solid var(--color-border-subtle);
}

.logo-bar-label {
  font-size: 0.8125rem;
  text-transform: uppercase;
  letter-spacing: 0.08em;
  color: var(--color-text-tertiary);
  margin-bottom: 1.25rem;
}

.logo-bar-logos {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 2.5rem;
  flex-wrap: wrap;
}

.logo-bar-logo {
  height: 28px;
  opacity: 0.5;
  filter: grayscale(1);
  transition: opacity 0.2s, filter 0.2s;
}

.logo-bar-logo:hover {
  opacity: 1;
  filter: grayscale(0);
}
```

**Design rules:**
- Grayscale logos by default (less visual noise, more credibility paradoxically)
- All logos same visual height (28-32px) regardless of original proportions
- 5 logos is the sweet spot — fewer feels sparse, more feels cluttered
- Label above ("Trusted by," "Used by teams at") not below
- If you don't have recognizable logos, use metrics instead: "2,400+ teams", "10M+ deploys"

#### Section 3: Problem (Pain Acknowledged)

The visitor must feel *seen*. This section validates their struggle.

**Pattern: The three-pain grid**

```tsx
function ProblemSection() {
  return (
    <section className="problem-section">
      <h2 className="section-eyebrow">Sound familiar?</h2>
      <div className="pain-grid">
        <PainCard
          icon={<ClockIcon />}
          title="Weeks lost to review cycles"
          description="PRs sit for days. Context is lost. Engineers context-switch
            between features while waiting for approvals."
        />
        <PainCard
          icon={<AlertTriangleIcon />}
          title="Bugs slip through anyway"
          description="Manual review catches style issues, not logic bugs.
            The things that break production still break production."
        />
        <PainCard
          icon={<TrendingDownIcon />}
          title="Shipping velocity flatlines"
          description="More engineers, same output. Process overhead grows
            faster than the team."
        />
      </div>
    </section>
  );
}
```

**Design rules:**
- Use the visitor's words, not your product's jargon
- 3 pain points maximum (more dilutes impact)
- Icons should reinforce the emotion, not decorate
- The section should make visitors nod, not flinch — empathy, not fear

#### Section 4: Agitate (The Cost of Doing Nothing)

This section raises the stakes. Not with fear — with clarity about what the problem actually costs.

**Pattern: The consequence cascade**

Show escalating consequences: time wasted, money lost, opportunity missed, team morale eroded. Use real numbers when possible ("The average team loses 14 hours/week to code review overhead").

**Design approach**: Darker background, slightly tighter typography, optional animated counter showing accumulating waste. This section is visually "heavier" than the problem section — it's the low point before the solution arrives.

#### Section 5: Solution (Product as Resolution)

The emotional pivot. The page shifts from problem to possibility.

**Pattern: Feature showcase with scroll-triggered reveals**

```tsx
function SolutionSection() {
  return (
    <section className="solution-section">
      <h2>Here's how it works</h2>
      <div className="feature-showcase">
        {features.map((feature, i) => (
          <FeatureRow
            key={feature.id}
            reverse={i % 2 === 1}  /* alternating layout */
            title={feature.title}
            description={feature.description}
            visual={feature.visual}  /* video, animation, or interactive */
          />
        ))}
      </div>
    </section>
  );
}

function FeatureRow({ reverse, title, description, visual }) {
  const ref = useRef(null);
  const isVisible = useIntersectionObserver(ref, { threshold: 0.3 });

  return (
    <div
      ref={ref}
      className={`feature-row ${reverse ? 'reverse' : ''}`}
      style={{
        opacity: isVisible ? 1 : 0,
        transform: isVisible ? 'translateY(0)' : 'translateY(2rem)',
        transition: 'opacity 0.6s ease, transform 0.6s ease',
      }}
    >
      <div className="feature-text">
        <h3>{title}</h3>
        <p>{description}</p>
      </div>
      <div className="feature-visual">
        {visual}
      </div>
    </div>
  );
}
```

```css
.feature-row {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 4rem;
  align-items: center;
  padding: 4rem 0;
}

.feature-row.reverse {
  direction: rtl;
}

.feature-row.reverse > * {
  direction: ltr;
}

.feature-text h3 {
  font-size: 1.5rem;
  font-weight: 700;
  margin-bottom: 0.75rem;
}

.feature-text p {
  font-size: 1.125rem;
  line-height: 1.7;
  color: var(--color-text-secondary);
}

@media (max-width: 768px) {
  .feature-row {
    grid-template-columns: 1fr;
    gap: 2rem;
  }
  .feature-row.reverse {
    direction: ltr;
  }
}
```

**What makes this sell:**
- Alternating layout prevents scroll monotony
- Visuals are interactive or animated — not static images
- Each feature is framed as a benefit ("Ship 3x faster") not a capability ("Automated CI/CD")
- Scroll-triggered reveals create discovery moments — the page "unfolds" as they read
- 3-5 features maximum. More than that and you're listing, not selling.

#### Section 6: Proof (Deep Social Proof)

Testimonials, case studies, metrics. This is where skepticism dies.

```tsx
function ProofSection() {
  return (
    <section className="proof-section">
      <h2>Teams ship faster with us</h2>

      {/* Metrics bar — hard numbers */}
      <div className="metrics-bar">
        <Metric value="73%" label="faster review cycles" />
        <Metric value="2.4x" label="more deploys per week" />
        <Metric value="89%" label="fewer production bugs" />
      </div>

      {/* Featured testimonial — one powerful quote with face */}
      <blockquote className="featured-testimonial">
        <img src="/testimonials/sarah.jpg" alt="Sarah Chen" />
        <div>
          <p className="quote">
            "We went from shipping once a month to shipping daily.
            The team actually enjoys the review process now."
          </p>
          <cite>
            <strong>Sarah Chen</strong>
            <span>VP Engineering, Acme Corp</span>
          </cite>
        </div>
      </blockquote>

      {/* Testimonial grid — breadth of proof */}
      <div className="testimonial-grid">
        {testimonials.map(t => (
          <TestimonialCard key={t.id} {...t} />
        ))}
      </div>
    </section>
  );
}
```

```css
.metrics-bar {
  display: flex;
  justify-content: center;
  gap: 4rem;
  padding: 3rem 0;
}

.metric-value {
  font-size: 3rem;
  font-weight: 800;
  color: var(--color-primary);
  line-height: 1;
}

.metric-label {
  font-size: 0.9375rem;
  color: var(--color-text-secondary);
  margin-top: 0.5rem;
}

.featured-testimonial {
  display: flex;
  gap: 2rem;
  align-items: flex-start;
  padding: 2.5rem;
  background: var(--color-surface-elevated);
  border-radius: 1rem;
  border: 1px solid var(--color-border-subtle);
  margin: 3rem 0;
}

.featured-testimonial img {
  width: 64px;
  height: 64px;
  border-radius: 50%;
  object-fit: cover;
  flex-shrink: 0;
}

.featured-testimonial .quote {
  font-size: 1.25rem;
  line-height: 1.6;
  font-style: italic;
  margin-bottom: 1rem;
}

.testimonial-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 1.5rem;
}
```

**Social proof hierarchy** (strongest to weakest):
1. **Named person + photo + company + role + specific result** ("Sarah Chen, VP Eng at Acme — 73% faster reviews")
2. **Named person + photo + company** ("John at Stripe")
3. **Company logo + metric** ("Used by Stripe — 10k+ deploys/day")
4. **Anonymous quote with role** ("VP Engineering at a Fortune 500")
5. **Star rating + count** ("4.9/5 from 2,400 reviews")
6. **User count alone** ("50,000+ users") — weakest but still useful

**Design rules for testimonials:**
- Human faces increase trust 30%+ — always include photos
- Specific results beat vague praise ("73% faster" beats "game-changer")
- 3 testimonials is the sweet spot for a section; link to more
- Video testimonials convert 2x better than text — use when available
- Place the strongest testimonial closest to the CTA

#### Section 7: Pricing (See dedicated section below)

#### Section 8: Final CTA (The Close)

```tsx
function FinalCTA() {
  return (
    <section className="final-cta">
      <h2>Ready to ship faster?</h2>
      <p>
        Start free. No credit card required.
        Cancel anytime.
      </p>
      <a href="/signup" className="cta-primary cta-large">
        Start building free
      </a>
      <p className="guarantee">
        30-day money-back guarantee. No questions asked.
      </p>
    </section>
  );
}
```

**Design rules:**
- Repeat the primary CTA from the hero — same words, same style
- Add risk-reduction copy: "No credit card", "Cancel anytime", "30-day guarantee"
- Visually distinct section (different background, generous padding)
- This is the ONLY place mild urgency is acceptable ("Join 200+ teams who started this week")
- Never pressure. Reassure.

---

## Pricing Page Architecture

The pricing page is where desire meets deliberation. It must make the choice feel obvious.

### The Three-Tier Pattern

The most proven pricing page structure in SaaS:

```
┌──────────────┐  ┌──────────────────┐  ┌──────────────┐
│    Starter    │  │   Pro ← BEST     │  │  Enterprise  │
│              │  │   VALUE BADGE     │  │              │
│   $0/mo      │  │   $29/mo         │  │   Custom     │
│              │  │   HIGHLIGHTED     │  │              │
│  For trying  │  │  For building    │  │  For scaling │
│              │  │                  │  │              │
│  [Start free]│  │  [Get started]   │  │  [Contact us]│
└──────────────┘  └──────────────────┘  └──────────────┘
```

### Implementation

```tsx
function PricingSection() {
  const [annual, setAnnual] = useState(true);

  return (
    <section className="pricing-section">
      <h2>Simple, transparent pricing</h2>
      <p className="pricing-subtitle">
        Start free, scale as you grow. No surprises.
      </p>

      {/* Billing toggle */}
      <div className="billing-toggle">
        <span className={!annual ? 'active' : ''}>Monthly</span>
        <button
          className="toggle-switch"
          onClick={() => setAnnual(!annual)}
          aria-label={`Switch to ${annual ? 'monthly' : 'annual'} billing`}
        >
          <span className={`toggle-knob ${annual ? 'right' : 'left'}`} />
        </button>
        <span className={annual ? 'active' : ''}>
          Annual <span className="save-badge">Save 20%</span>
        </span>
      </div>

      {/* Tier cards */}
      <div className="pricing-grid">
        <PricingCard
          name="Starter"
          price={0}
          period="forever"
          description="For individuals and side projects"
          features={[
            'Up to 3 projects',
            '1,000 builds/month',
            'Community support',
          ]}
          cta="Start free"
          ctaVariant="secondary"
        />
        <PricingCard
          name="Pro"
          price={annual ? 29 : 36}
          period="/month"
          description="For teams shipping production software"
          features={[
            'Unlimited projects',
            '10,000 builds/month',
            'Priority support',
            'Advanced analytics',
            'Team management',
          ]}
          cta="Get started"
          ctaVariant="primary"
          highlighted={true}
          badge="Most popular"
        />
        <PricingCard
          name="Enterprise"
          price="Custom"
          description="For organizations at scale"
          features={[
            'Everything in Pro',
            'Unlimited builds',
            'SSO & SAML',
            'Dedicated support',
            'SLA guarantee',
            'Custom integrations',
          ]}
          cta="Contact sales"
          ctaVariant="secondary"
        />
      </div>

      {/* Feature comparison table */}
      <FeatureComparisonTable tiers={tiers} />
    </section>
  );
}
```

```css
.pricing-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 1.5rem;
  max-width: 1100px;
  margin: 3rem auto;
  align-items: start;
}

.pricing-card {
  padding: 2rem;
  border-radius: 1rem;
  border: 1px solid var(--color-border-subtle);
  background: var(--color-surface);
}

.pricing-card.highlighted {
  border-color: var(--color-primary);
  border-width: 2px;
  box-shadow: 0 8px 32px rgba(59, 130, 246, 0.12);
  position: relative;
  /* Subtle upward shift to draw the eye */
  transform: translateY(-0.5rem);
}

.pricing-card .badge {
  position: absolute;
  top: -0.75rem;
  left: 50%;
  transform: translateX(-50%);
  background: var(--color-primary);
  color: white;
  font-size: 0.75rem;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.05em;
  padding: 0.25rem 1rem;
  border-radius: 2rem;
}

.pricing-card .price {
  font-size: 3rem;
  font-weight: 800;
  line-height: 1;
  margin: 1rem 0 0.25rem;
}

.pricing-card .price-currency {
  font-size: 1.5rem;
  vertical-align: super;
}

.pricing-card .price-period {
  font-size: 1rem;
  font-weight: 400;
  color: var(--color-text-secondary);
}

.billing-toggle {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.75rem;
  margin: 2rem 0;
}

.save-badge {
  background: var(--color-success-subtle);
  color: var(--color-success);
  font-size: 0.75rem;
  font-weight: 700;
  padding: 0.125rem 0.5rem;
  border-radius: 2rem;
  margin-left: 0.25rem;
}

@media (max-width: 768px) {
  .pricing-grid {
    grid-template-columns: 1fr;
    max-width: 400px;
  }
  .pricing-card.highlighted {
    transform: none;
    order: -1; /* Move highlighted plan to top on mobile */
  }
}
```

### Pricing Psychology (What the Best Do)

**Anchoring (Vercel pattern)**: Enterprise tier with "Custom" pricing appears first or last, anchoring the Pro tier as reasonable by comparison.

**Decoy pricing**: The Starter tier exists partly to make Pro look like a bargain. If Starter has 3 projects and Pro has unlimited, the $29 gap feels trivial.

**Annual nudge (Stripe pattern)**: Default to annual billing with a visible "Save 20%" badge. Monthly option available but not default. The toggle defaults to the position that benefits both parties.

**Feature comparison table (Vercel pattern)**: Sticky header with plan names. Checkmarks and dashes (not just text). The highlighted column stays visually distinct as you scroll. Group features by category with section dividers.

**What to learn from each:**

| Company | Pricing Strength | Design Technique |
|---------|-----------------|------------------|
| **Stripe** | Radical transparency | Usage-based pricing with calculators, no hidden fees |
| **Linear** | Simplicity | Two tiers, no feature matrix clutter |
| **Vercel** | Developer trust | Dark mode, technical detail, code-native feel |
| **Notion** | Accessibility | Free tier generous enough to hook, paid tier for teams |
| **Framer** | Visual proof | Pricing page itself demonstrates the product's capabilities |

---

## CTA Button Design

The CTA button is the single most revenue-critical element on any page. Every property matters.

### Anatomy of a High-Converting CTA

```css
.cta-primary {
  /* Size — large enough to tap, prominent enough to find */
  display: inline-flex;
  align-items: center;
  justify-content: center;
  min-height: 48px;          /* Google Material minimum touch target */
  padding: 0.875rem 2rem;    /* Generous horizontal padding */

  /* Typography — confident, readable */
  font-size: 1rem;
  font-weight: 600;
  letter-spacing: 0.01em;
  line-height: 1;

  /* Color — high contrast against page background */
  background-color: #2563eb;      /* Blue-600: trust + action */
  color: #ffffff;
  border: none;
  border-radius: 0.5rem;

  /* Interaction — responsive, alive */
  cursor: pointer;
  transition: background-color 0.15s ease, transform 0.15s ease,
              box-shadow 0.15s ease;
}

.cta-primary:hover {
  background-color: #1d4ed8;      /* Blue-700: darker on hover */
  transform: translateY(-1px);
  box-shadow: 0 4px 12px rgba(37, 99, 235, 0.3);
}

.cta-primary:active {
  transform: translateY(0);
  box-shadow: none;
}

/* Large variant — for hero and final CTA sections */
.cta-large {
  min-height: 56px;
  padding: 1rem 2.5rem;
  font-size: 1.125rem;
}

/* Secondary CTA — lower commitment option */
.cta-secondary {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  min-height: 48px;
  padding: 0.875rem 2rem;
  font-size: 1rem;
  font-weight: 600;
  background: transparent;
  color: var(--color-text-primary);
  border: 1.5px solid var(--color-border);
  border-radius: 0.5rem;
  cursor: pointer;
  transition: border-color 0.15s ease, background-color 0.15s ease;
}

.cta-secondary:hover {
  border-color: var(--color-primary);
  background-color: var(--color-primary-subtle);
}
```

### CTA Color Psychology

Color choice for CTAs is not arbitrary — it must contrast with the page palette while matching the emotional register of the action.

| Color | Hex Range | Emotional Register | Best For |
|-------|-----------|-------------------|----------|
| **Blue** | `#2563eb` - `#1d4ed8` | Trust, reliability, professionalism | SaaS signups, B2B, finance |
| **Green** | `#16a34a` - `#15803d` | Safety, go, affirmation | Free trials, "safe" actions, eco products |
| **Orange** | `#ea580c` - `#c2410c` | Energy, warmth, urgency (mild) | E-commerce, limited offers, creative tools |
| **Purple** | `#7c3aed` - `#6d28d9` | Premium, creative, innovative | Design tools, premium tiers, creative SaaS |
| **Black** | `#18181b` - `#09090b` | Authority, premium, confidence | Luxury, developer tools, minimalist brands |
| **Red** | `#dc2626` - `#b91c1c` | Urgency, importance, stop-and-look | USE SPARINGLY — cancellations, warnings only |

**The real rule**: Your CTA must be the **highest-contrast interactive element** on the page. If your page is blue-themed, a blue CTA disappears. Use the complementary color or a warm accent.

### CTA Copy That Converts

| Weak (Generic) | Strong (Specific) | Why It Works |
|----------------|-------------------|--------------|
| Submit | Get my free report | Specific outcome |
| Sign Up | Start building free | Action + benefit + risk removal |
| Learn More | See how it works | Lower commitment, higher curiosity |
| Buy Now | Secure my spot | Ownership + mild urgency |
| Get Started | Launch my first project | Visualizable action |
| Download | Get the playbook | Named deliverable |

**Rules:**
- First person when possible ("Start **my** free trial" outperforms "Start **your** free trial")
- 2-5 words maximum
- Verb-first (action-oriented)
- Benefit-laden, not task-describing
- Never "Submit" — that is not a human word

### CTA Placement Strategy

```
┌─────────────────────────────────────┐
│  Hero CTA                           │  ← For visitors who arrive ready
│  (Primary + Secondary)              │
├─────────────────────────────────────┤
│  ...content...                      │
├─────────────────────────────────────┤
│  Mid-page CTA                       │  ← After the solution section
│  (Inline, less prominent)           │     For visitors convinced midway
├─────────────────────────────────────┤
│  ...more content...                 │
├─────────────────────────────────────┤
│  Sticky CTA (optional)              │  ← Appears after hero scrolls
│  (Compact bar, top or bottom)       │     out of view
├─────────────────────────────────────┤
│  Final CTA                          │  ← After all proof is delivered
│  (Large, with guarantee text)       │     For visitors who read everything
└─────────────────────────────────────┘
```

**Sticky CTA pattern** (use sparingly):

```css
.sticky-cta-bar {
  position: fixed;
  bottom: 0;
  left: 0;
  right: 0;
  padding: 0.75rem 2rem;
  background: var(--color-surface);
  border-top: 1px solid var(--color-border-subtle);
  display: flex;
  align-items: center;
  justify-content: space-between;
  transform: translateY(100%);
  transition: transform 0.3s ease;
  z-index: 50;
  backdrop-filter: blur(12px);
}

.sticky-cta-bar.visible {
  transform: translateY(0);
}
```

Show the sticky bar only after the hero CTA scrolls out of view. Hide it when the final CTA section comes into view. This ensures there is always a CTA available without being obnoxious.

---

## Social Proof Design Patterns

Social proof is the single highest-leverage conversion element after the hero. Placement and design matter as much as the content.

### The Social Proof Pyramid

Layer different types of proof throughout the page:

```
                    CASE STUDIES
                  (deepest proof, highest effort)
                  ─────────────────
               TESTIMONIALS + PHOTOS
             (personal, emotional, relatable)
             ──────────────────────────
          METRICS + NUMBERS
        (scale, velocity, reliability)
        ───────────────────────────────
     LOGOS + BADGES
   (instant recognition, zero reading)
   ────────────────────────────────────
  SOCIAL COUNTERS + ACTIVITY FEEDS
(volume, momentum, "everyone's doing it")
───────────────────────────────────────────
```

Place the base layers (logos, counters) near the top. Place deeper proof (testimonials, case studies) further down where visitors are making decisions.

### Animated Social Proof (The "Live" Effect)

```tsx
function LiveActivityFeed() {
  const [activities, setActivities] = useState(initialActivities);

  useEffect(() => {
    const interval = setInterval(() => {
      setActivities(prev => {
        const next = [...prev];
        next.pop();
        next.unshift(getRandomActivity());
        return next;
      });
    }, 4000);
    return () => clearInterval(interval);
  }, []);

  return (
    <div className="activity-feed" aria-live="polite">
      {activities.map((activity, i) => (
        <div
          key={activity.id}
          className="activity-item"
          style={{
            opacity: 1 - (i * 0.2),
            transform: `translateY(${i * 48}px)`,
          }}
        >
          <img src={activity.avatar} alt="" className="activity-avatar" />
          <span>
            <strong>{activity.name}</strong> from {activity.company}{' '}
            {activity.action}
          </span>
          <time>{activity.timeAgo}</time>
        </div>
      ))}
    </div>
  );
}
```

**ETHICAL CONSTRAINT**: These must be real events, not fabricated. If you have actual signups, show them (with privacy consent). If not, use aggregated metrics instead. See the Anti-Patterns section for why fake activity feeds are harmful.

### Before/After Comparisons

One of the most powerful proof patterns — tangible transformation.

```tsx
function BeforeAfter({ before, after }) {
  const [position, setPosition] = useState(50);
  const containerRef = useRef(null);

  const handleMove = (e) => {
    const rect = containerRef.current.getBoundingClientRect();
    const x = ((e.clientX - rect.left) / rect.width) * 100;
    setPosition(Math.max(0, Math.min(100, x)));
  };

  return (
    <div
      ref={containerRef}
      className="before-after"
      onMouseMove={handleMove}
      onTouchMove={(e) => handleMove(e.touches[0])}
      role="slider"
      aria-label="Before and after comparison"
      aria-valuemin={0}
      aria-valuemax={100}
      aria-valuenow={position}
    >
      <div className="before-side" style={{ clipPath: `inset(0 ${100 - position}% 0 0)` }}>
        <img src={before.image} alt={before.alt} />
        <span className="label">Before</span>
      </div>
      <div className="after-side">
        <img src={after.image} alt={after.alt} />
        <span className="label">After</span>
      </div>
      <div className="slider-handle" style={{ left: `${position}%` }}>
        <div className="handle-line" />
        <div className="handle-grip" />
      </div>
    </div>
  );
}
```

---

## Trust Signals and Risk Reduction

Trust is not one element — it is a system woven throughout the page.

### Trust Signal Placement Map

| Signal | Where to Place | Why There |
|--------|---------------|-----------|
| Company logos | Below hero | Immediate credibility before reading |
| Security badges (SOC2, GDPR) | Near forms and pricing | Reduce anxiety at commitment points |
| Money-back guarantee | Below pricing CTA | Remove purchase risk at decision moment |
| Human faces | Testimonials, about section | Faces trigger trust response (amygdala) |
| "No credit card required" | Next to signup CTA | Eliminate the #1 signup barrier |
| Privacy policy link | Near email capture | Show respect for their data |
| Real-time user count | Hero or social bar | Demonstrate momentum and adoption |
| Press logos ("Featured in") | Below logo bar or footer | Third-party validation |
| Response time ("Reply in <1hr") | Near contact/support | Demonstrate commitment to service |

### The Guarantee Component

```tsx
function GuaranteeBlock() {
  return (
    <div className="guarantee-block">
      <ShieldCheckIcon className="guarantee-icon" />
      <div>
        <h4>30-day money-back guarantee</h4>
        <p>
          Try it risk-free. If it is not right for your team,
          email us within 30 days for a full refund. No questions,
          no hassle, no hard feelings.
        </p>
      </div>
    </div>
  );
}
```

```css
.guarantee-block {
  display: flex;
  gap: 1.25rem;
  align-items: flex-start;
  padding: 1.5rem 2rem;
  background: var(--color-success-subtle);
  border: 1px solid var(--color-success-border);
  border-radius: 0.75rem;
  max-width: 600px;
  margin: 2rem auto;
}

.guarantee-icon {
  width: 32px;
  height: 32px;
  color: var(--color-success);
  flex-shrink: 0;
}
```

---

## Interactive Product Demos (The "Wow" Factor)

The moment a visitor stops scrolling and thinks "this is legit" is the moment you win. Interactivity creates those moments.

### Patterns Ranked by Conversion Impact

| Pattern | Impact | Effort | When to Use |
|---------|--------|--------|------------|
| **Interactive playground** | Highest | High | Developer tools, design tools |
| **Video demo (autoplay, muted)** | High | Medium | Any product with visual UI |
| **Scroll-triggered animation** | High | Medium | Feature explanations, data flows |
| **Before/after slider** | High | Low | Visual transformations |
| **Animated metrics counter** | Medium | Low | Any page with impressive numbers |
| **Hover-to-reveal** | Medium | Low | Feature grids, comparison tables |
| **Lottie illustrations** | Medium | Medium | Abstract concepts, onboarding |
| **ROI calculator** | High | Medium | B2B, enterprise, cost-savings pitch |

### ROI Calculator Pattern

Nothing sells like showing the visitor their own potential savings.

```tsx
function ROICalculator() {
  const [teamSize, setTeamSize] = useState(10);
  const [hoursPerWeek, setHoursPerWeek] = useState(8);

  const hourlyRate = 75; // average dev hourly cost
  const efficiency = 0.65; // 65% reduction claim
  const weeklySavings = teamSize * hoursPerWeek * efficiency * hourlyRate;
  const annualSavings = weeklySavings * 52;

  return (
    <div className="roi-calculator">
      <h3>See what you could save</h3>

      <div className="roi-inputs">
        <label>
          <span>Team size</span>
          <input
            type="range"
            min={1}
            max={100}
            value={teamSize}
            onChange={e => setTeamSize(Number(e.target.value))}
          />
          <output>{teamSize} engineers</output>
        </label>

        <label>
          <span>Hours spent on reviews/week</span>
          <input
            type="range"
            min={1}
            max={40}
            value={hoursPerWeek}
            onChange={e => setHoursPerWeek(Number(e.target.value))}
          />
          <output>{hoursPerWeek} hours</output>
        </label>
      </div>

      <div className="roi-result">
        <div className="roi-annual">
          <span className="roi-label">Estimated annual savings</span>
          <span className="roi-value">
            ${annualSavings.toLocaleString()}
          </span>
        </div>
        <p className="roi-footnote">
          Based on ${hourlyRate}/hr average fully-loaded developer cost
          and {Math.round(efficiency * 100)}% efficiency improvement.
        </p>
      </div>
    </div>
  );
}
```

**Design rules for calculators:**
- Pre-filled with realistic defaults (don't start at zero — that shows zero savings)
- Sliders over text inputs (lower friction, more playful)
- Show the result updating in real-time as sliders move
- Include the assumptions transparently (builds trust)
- Always link the result to your CTA: "Save $X/year — Start free"

---

## Anti-Patterns: Dark Patterns to Avoid

This skill exists to build sites that sell through genuine value, not manipulation. The following patterns are **never acceptable**. They may boost short-term metrics but they destroy trust, increase refund rates, generate negative word-of-mouth, and in many jurisdictions are now illegal.

### 1. Fake Urgency / Countdown Timers

**What it looks like**: "Offer expires in 23:14:07!" — but the timer resets on refresh.

**Why it is wrong**: Visitors notice. They open an incognito window, see the timer reset, and never trust your brand again. The EU Digital Services Act and similar regulations are actively penalizing this pattern. Booking.com was fined for it.

**What to do instead**: If you have a genuine deadline (product launch, cohort enrollment), display the real date. "Cohort starts March 15 — 12 spots remaining" is honest urgency.

### 2. Confirmshaming

**What it looks like**: "No thanks, I don't want to grow my business" as the dismiss option.

**Why it is wrong**: It is passive-aggressive. It makes visitors feel manipulated, which is the opposite of trust. MyMedic's "No, I'd rather bleed to death" is the canonical example of how not to do this.

**What to do instead**: "No thanks" or "Maybe later" — neutral, respectful language. Treat the visitor as an adult making a rational decision.

### 3. Hidden Costs

**What it looks like**: Pricing page shows $29/mo, checkout adds $5 "platform fee" + $3 "support fee."

**Why it is wrong**: 48% of shoppers abandon carts due to unexpected costs. The damage to trust is permanent.

**What to do instead**: Show the total price upfront. If there are usage-based components, show a calculator with realistic estimates. Stripe's transparent pricing is the gold standard.

### 4. Roach Motel (Easy In, Hard Out)

**What it looks like**: One-click signup, but cancellation requires a phone call or chat with a retention agent.

**Why it is wrong**: Customers trapped by friction become hostile ex-customers. They leave 1-star reviews and warn others. This pattern is now illegal under the FTC's "Click-to-Cancel" rule (2024).

**What to do instead**: Cancellation should be as easy as signup. Offer a pause option, a downgrade path, or an "are you sure?" with genuine reasons to stay — but never block the exit.

### 5. Misdirection / Visual Manipulation

**What it looks like**: The "Accept all cookies" button is large and blue. The "Manage preferences" link is gray 12px text.

**Why it is wrong**: GDPR enforcement is catching up to this pattern. More importantly, visitors notice the asymmetry and it erodes trust in everything else on the page.

**What to do instead**: Give both options equal visual weight. If your product is good, informed consent converts better long-term.

### 6. Fake Social Proof

**What it looks like**: Fabricated testimonials, stock photo "customers," inflated user counts, fake activity feeds.

**Why it is wrong**: It is fraud. The FTC actively investigates fake reviews and has levied multi-million dollar fines. Beyond legality, one exposed fake testimonial invalidates all your real ones.

**What to do instead**: Use real testimonials with real names and real photos (with permission). If you don't have enough social proof yet, use metrics ("500+ beta users") or early-access quotes. Authenticity at low scale beats fabrication at high scale.

### 7. Forced Continuity

**What it looks like**: "Free trial!" that auto-converts to a paid plan with no warning email.

**Why it is wrong**: Surprise charges generate chargebacks, refund requests, and trust destruction. Apple and Google app stores now require explicit confirmation before paid conversions.

**What to do instead**: Send a reminder email 3 days before trial ends. Make the conversion opt-in if possible. Transparency converts better because it creates goodwill.

### The Ethical Test

Before shipping any persuasion pattern, ask:

1. **Would I screenshot this and post it on Twitter?** If the answer is "that would look bad," don't ship it.
2. **Does this work if the visitor notices the technique?** Good persuasion works when visible. Dark patterns only work when hidden.
3. **Would this cause a customer to warn others?** If yes, the lifetime cost exceeds any short-term conversion gain.
4. **Is the visitor making an informed decision?** Persuasion is helping people decide. Manipulation is deciding for them.

---

## Responsive Conversion Design

Sales pages must convert on mobile — 60%+ of traffic is mobile in 2026.

### Mobile-Specific Patterns

```css
/* Stack CTA cluster vertically on mobile */
@media (max-width: 640px) {
  .hero-cta-cluster {
    flex-direction: column;
    align-items: stretch;
  }

  /* Full-width CTAs on mobile */
  .cta-primary,
  .cta-secondary {
    width: 100%;
    justify-content: center;
  }

  /* Larger touch targets */
  .cta-primary {
    min-height: 52px;
    font-size: 1.0625rem;
  }

  /* Single-column pricing */
  .pricing-grid {
    grid-template-columns: 1fr;
    max-width: 400px;
    margin: 2rem auto;
  }

  /* Move highlighted plan first */
  .pricing-card.highlighted {
    order: -1;
  }

  /* Collapse feature comparison to accordion */
  .feature-table {
    display: none;
  }
  .feature-accordion {
    display: block;
  }

  /* Testimonial cards full-width */
  .testimonial-grid {
    grid-template-columns: 1fr;
  }
}
```

**Mobile conversion rules:**
- Thumb zone: Primary CTAs in bottom 40% of screen
- No horizontal scrolling — ever
- Pricing: Show the recommended plan first on mobile, others below
- Forms: Minimize fields. Every field costs 10-15% of completions.
- Speed: Compress images aggressively. Sub-3s load time is the conversion threshold.

---

## Performance and Speed

A 1-second delay in load time reduces conversions by 7%. Sales pages must be fast.

| Metric | Target | Why |
|--------|--------|-----|
| LCP (Largest Contentful Paint) | < 2.5s | Hero must be visible instantly |
| FID (First Input Delay) | < 100ms | CTAs must respond immediately |
| CLS (Cumulative Layout Shift) | < 0.1 | Shifting elements kill trust |
| Total page weight | < 1.5MB | Mobile networks are unforgiving |

**Quick wins:**
- Lazy-load everything below the fold
- Use `<picture>` with WebP/AVIF sources
- Preload hero image and fonts
- Inline critical CSS for above-the-fold content
- Defer non-essential JavaScript (analytics, chat widgets)

---

## Quality Checklist

Before shipping a sales page, verify:

### Hero (Section 1)
- [ ] Value proposition clear within 5 seconds
- [ ] Single primary CTA visible without scrolling
- [ ] Eyebrow or social proof signals credibility immediately
- [ ] Headline is benefit-driven, not feature-driven
- [ ] Visual supports the promise (not a raw screenshot)

### Social Proof (Sections 2 + 6)
- [ ] Logo bar uses 4-6 recognizable brands (grayscale default)
- [ ] Testimonials include real names, real photos, specific results
- [ ] Metrics are specific and verifiable ("73% faster" not "much faster")
- [ ] No fabricated or misleading social proof

### Problem/Agitate (Sections 3 + 4)
- [ ] Visitor's language used, not internal jargon
- [ ] Pain points are specific and relatable
- [ ] Agitation raises stakes without fear-mongering

### Solution (Section 5)
- [ ] Features shown as benefits with visual demos
- [ ] 3-5 features maximum (not a feature dump)
- [ ] Scroll-triggered reveals create discovery moments
- [ ] Interactive or animated, not static screenshots

### Pricing (Section 7)
- [ ] 2-3 tiers with clear differentiation
- [ ] Recommended tier visually highlighted
- [ ] Annual/monthly toggle defaults to annual with savings shown
- [ ] All costs visible — no hidden fees
- [ ] Feature comparison table available for detail-seekers

### CTAs (Throughout)
- [ ] Primary CTA color contrasts with page palette
- [ ] CTA copy is verb-first, benefit-laden, 2-5 words
- [ ] Touch targets meet minimum 48px
- [ ] CTAs placed at hero, mid-page, and final section minimum
- [ ] Sticky CTA appears only when hero CTA not visible

### Trust (Throughout)
- [ ] Security badges near forms and payment
- [ ] Guarantee displayed near pricing CTA
- [ ] "No credit card required" if applicable
- [ ] Real human faces in testimonials

### Ethics
- [ ] No fake countdown timers or artificial urgency
- [ ] No confirmshaming language
- [ ] No hidden costs or surprise fees
- [ ] Cancellation is as easy as signup
- [ ] All social proof is authentic
- [ ] Both cookie consent options have equal visual weight

### Performance
- [ ] LCP under 2.5 seconds
- [ ] Page weight under 1.5MB
- [ ] CLS under 0.1
- [ ] Images use modern formats (WebP/AVIF)
- [ ] Critical CSS inlined for above-the-fold

### Mobile
- [ ] All CTAs thumb-reachable
- [ ] Pricing stacks to single column
- [ ] No horizontal scroll anywhere
- [ ] Touch targets 48px minimum
- [ ] Load time under 3 seconds on 4G

---

## Output Format

When this skill is activated, produce:

1. **Page architecture** — Section-by-section blueprint with scroll order
2. **Component specifications** — CSS/React for key conversion elements
3. **Social proof strategy** — What proof to place where and why
4. **CTA specification** — Color, size, copy, placement for all CTAs
5. **Pricing page design** — Tier structure, highlighting, toggle behavior
6. **Trust signal map** — Which signals, where, and why
7. **Ethics review** — Confirm no dark patterns present
8. **Mobile adaptation** — How each section responds on small screens

---

*The best sales design respects the visitor enough to be honest and compelling enough to be unnecessary. If your product is genuinely good, your job is to remove the barriers between the visitor and the value — not to trick them past those barriers.*
