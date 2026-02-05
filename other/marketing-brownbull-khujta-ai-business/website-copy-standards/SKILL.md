---
name: website-copy-standards
description: |
  Comprehensive skill for writing high-converting, AI-optimised website copy that combines Generative Engine Optimization (GEO) with strategic copywriting psychology. Use when: (1) Writing new website copy, landing pages, or marketing content, (2) Performing SEO audits or content reviews, (3) Optimising content for AI Answer Engines (Google AI, Perplexity, ChatGPT), (4) Implementing Schema markup (JSON-LD structured data), (5) Writing B2B or B2C-specific copy, (6) Creating About Us pages or brand storytelling content, (7) Writing microcopy, error messages, or UX text, (8) Ensuring accessibility and inclusive language.

  Invoke with: /write-website-copy, /audit-seo, /generate-schema, /validate-content, or say "use the website-copy-standards skill to..."
---

# Website Copy Standards

Write website copy that converts humans AND gets cited by AI.

## Design Philosophy

### The Dual Audience Reality

Every piece of web copy has two readers: humans and machines. Write only for humans, and AI Answer Engines will never cite you. Write only for machines, and humans will bounce. The art is writing content that serves both simultaneously.

### The Citation Economy

SEO was about ranking. GEO is about citation. When Perplexity or ChatGPT answers a user's question, they cite sources. Your content either contributes facts to that answer or it doesn't exist. There is no "page 2" in AI responses.

### Answer First, Story Second

Traditional copywriting builds toward a conclusion. GEO copywriting leads with the conclusion. The first 50 words after a question heading ARE the answer. Everything else is supporting detail for humans who want to go deeper.

### Entity Thinking

Keywords are dead. Entities are alive. An entity is a thing in the world with attributes and relationships. "Nike Air Max 2025" is an entity. "Best running shoes" is a keyword. AI understands entities; it matches keywords. Write about things, not phrases.

### Ethical Persuasion

This skill could teach manipulation. It doesn't. Dark patterns work short-term and destroy trust long-term. Empowerment marketing builds loyalty. Pain-point agitation is replaced by potential-highlighting.

---

## Anti-Patterns: Copy That Fails

### The Keyword Stuffer
**Symptom:** "Our best running shoes are the best running shoes for runners who want the best."
**Problem:** AI detects keyword spam. Humans detect desperation.
**Solution:** Say it once, clearly. Use entity attributes instead of repeating the keyword.

### The Wall of Text
**Symptom:** Dense paragraphs without headers, bullets, or visual breaks.
**Problem:** 73% of users skim. Walls of text trigger immediate bounce.
**Solution:** Short paragraphs (3-4 sentences max), bullets for lists, bold key phrases.

### The "Click Here" Linker
**Symptom:** "To learn more, click here."
**Problem:** Screen readers announce links without context. "Click here" is meaningless.
**Solution:** "Read our guide to Schema Markup" — descriptive link text.

### The Feature Fetishist
**Symptom:** "64GB storage, 120Hz display, A17 Bionic chip..."
**Problem:** Features don't sell. Benefits do. Nobody buys a 120Hz display; they buy smooth scrolling.
**Solution:** Lead with benefit, support with feature: "Buttery-smooth scrolling (120Hz display)."

### The Dark Pattern User
**Symptom:** "No thanks, I don't care about saving money" (confirmshaming)
**Problem:** Short-term conversions, long-term reputation damage, potential legal issues.
**Solution:** Neutral opt-out language: "No thanks" or "Maybe later."

---

## Copy Style Selection

Choose your baseline voice before writing:

### B2B Enterprise
- **Tone:** Confident, evidence-based, ROI-focused
- **Proof:** Case studies, metrics, industry recognition
- **CTA:** Consultative ("Schedule a demo", "Talk to an expert")
- **Reference:** See [b2b-b2c-methodology.md](references/b2b-b2c-methodology.md)

### B2C Consumer
- **Tone:** Friendly, benefit-driven, emotionally resonant
- **Proof:** Reviews, social proof, before/after
- **CTA:** Action-oriented ("Get started", "Try free")
- **Reference:** See [b2b-b2c-methodology.md](references/b2b-b2c-methodology.md)

### SaaS Product
- **Tone:** Clear, value-first, low-friction
- **Proof:** Free trial, feature tours, comparison tables
- **CTA:** Low commitment ("Start free trial", "See how it works")

### Service Business
- **Tone:** Trustworthy, relationship-focused, expertise-demonstrating
- **Proof:** Testimonials, credentials, process transparency
- **CTA:** Engagement-focused ("Get a quote", "Book a call")

---

## Quick Start Checklist

Before publishing any web copy, verify:

| Category | Check |
|----------|-------|
| **SEO** | Entities mapped (not just keywords) |
| **SEO** | Question H2s with concise answers (<40 words) |
| **UX** | Scannable: bullets, bold, short paragraphs |
| **UX** | Accessible: alt text, descriptive links |
| **Tone** | Conversational (read aloud to test) |
| **Value** | Benefit-first headlines (not features) |
| **Ethics** | Claims provable, pain used responsibly |
| **AI** | Hallucinations removed, sentence rhythm varied |

---

## Writing Workflow

### Step 1: Identify Audience
- **B2B?** → Read [b2b-b2c-methodology.md](references/b2b-b2c-methodology.md)
- **B2C?** → Read [b2b-b2c-methodology.md](references/b2b-b2c-methodology.md)

### Step 2: Map Entities
Define primary entities (not keywords) the content covers.
- What things, people, places, concepts?
- What are their attributes and relationships?
- See [geo-technical.md](references/geo-technical.md) → Entity-Based SEO

### Step 3: Structure for Skimmers
73% of users skim. Format for scannable reading:
- Short paragraphs (3-4 sentences max)
- Bullet points for lists
- Bold key phrases
- Question H2s for voice search
- See [cognitive-copywriting.md](references/cognitive-copywriting.md) → Skimming

### Step 4: Write Emotion-First
80% of decisions start emotional, then rationalise.
- Headlines: visceral appeal (safety, status, belonging)
- Body: logical support (features, specs, ROI)
- See [cognitive-copywriting.md](references/cognitive-copywriting.md) → Neuro-Copywriting

### Step 5: Apply Answer-First Structure
For AI citation and voice search:
```
<h2>How does X work?</h2>     <!-- Question trigger -->
<p>X works by... [40-60 words]</p>  <!-- Direct answer -->
<p>This is because...</p>     <!-- Supporting detail -->
```
See [geo-technical.md](references/geo-technical.md) → Answer-First

### Step 6: Implement Schema
Use `scripts/generate_schema.py` to create JSON-LD:
```bash
python scripts/generate_schema.py --type faqpage --interactive
python scripts/generate_schema.py --type article --input data.json
```
Or copy templates from `assets/schema-templates/`

---

## Audit Workflow

### Step 1: Run Validator
```bash
python scripts/validate_content.py --file page.html
python scripts/validate_content.py --url https://example.com --json
```

Checks: H1 count, heading hierarchy, semantic HTML, Schema presence, readability score, scannability, link text, alt text.

### Step 2: Review GEO Technical
Against [geo-technical.md](references/geo-technical.md):
- [ ] Single H1 with primary entity
- [ ] Heading hierarchy (no skipped levels)
- [ ] Semantic elements (article, section, aside)
- [ ] JSON-LD Schema present
- [ ] Answer blocks after question H2s

### Step 3: Evaluate Cognitive Load
Against [cognitive-copywriting.md](references/cognitive-copywriting.md):
- [ ] 8-second headline test (clear value?)
- [ ] Grade 8 reading level
- [ ] Sentence rhythm (varied lengths)
- [ ] Specific > generic claims

### Step 4: Verify Accessibility
Against [ux-accessibility.md](references/ux-accessibility.md):
- [ ] All images have alt text
- [ ] No "click here" links
- [ ] Proper heading hierarchy
- [ ] Dark mode considerations

---

## Scripts

### generate_schema.py
Generate JSON-LD Schema markup.

```bash
# Interactive mode
python scripts/generate_schema.py --type faqpage --interactive
python scripts/generate_schema.py --type article --interactive
python scripts/generate_schema.py --type organization --interactive
python scripts/generate_schema.py --type product --interactive

# From JSON file
python scripts/generate_schema.py --type article --input data.json --output schema.json
```

### validate_content.py
Validate HTML against GEO and copywriting standards.

```bash
# Validate local file
python scripts/validate_content.py --file index.html

# Validate URL
python scripts/validate_content.py --url https://example.com

# JSON output for CI/CD
python scripts/validate_content.py --file page.html --json
```

---

## Reference Navigation

Choose based on your task:

| Task | Reference |
|------|-----------|
| Technical SEO, Schema, Entity mapping | [geo-technical.md](references/geo-technical.md) |
| Psychology, headlines, AI humanisation | [cognitive-copywriting.md](references/cognitive-copywriting.md) |
| Microcopy, accessibility, voice search | [ux-accessibility.md](references/ux-accessibility.md) |
| Landing pages, CTAs, conversion | [landing-pages.md](references/landing-pages.md) |
| B2B vs B2C tone and strategy | [b2b-b2c-methodology.md](references/b2b-b2c-methodology.md) |
| About pages, origin stories | [brand-storytelling.md](references/brand-storytelling.md) |
| Ethics, inclusivity, dark patterns | [ethics-inclusivity.md](references/ethics-inclusivity.md) |

---

## Key Principles

### GEO: Write for AI Citation
- Content must contribute facts AI uses to construct answers
- Goal is citation, not just ranking
- Use Schema markup for explicit machine understanding
- Include original data, stats, quotes (Information Gain)

### Psychology: Emotion First
- 80% emotional, then rationalised
- 8-second headline window
- 73% of users skim
- Reduce cognitive load

### Structure: Answer First
- Question H2s for voice search
- Direct answer in 40-60 words
- Then supporting detail
- Each block must stand alone (Pinball Pattern)

### Ethics: Empower, Don't Manipulate
- Highlight potential, not inadequacy
- No dark patterns
- Inclusive language
- Provable claims only

---

## External Resources

- **Google GEO Guidance:** [Search Central on AI Overviews](https://developers.google.com/search/docs/appearance/ai-overviews) — Official guidance on AI-generated search results
- **Schema.org:** [Schema Types Reference](https://schema.org/docs/full.html) — Authoritative schema type definitions
- **W3C WCAG:** [Web Content Accessibility Guidelines](https://www.w3.org/WAI/standards-guidelines/wcag/) — Accessibility standards
- **Nielsen Norman Group:** [UX Research](https://www.nngroup.com/articles/) — Evidence-based usability guidance
- **Hemingway App:** [Readability Checker](https://hemingwayapp.com/) — Grade-level analysis

---

## Your Mission

You are writing for the future of search. Every answer engine that emerges tomorrow will evaluate content created today. Your copy is not just marketing; it is the source material from which AI constructs the world's knowledge.

Write as if your content will be cited a million times. Because it might be.
