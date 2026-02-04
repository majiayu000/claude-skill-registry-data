---
name: partitaiva-style-translator
description: Transforms schematic, SEO-heavy articles into natural, conversational PartitaIVA.it style content while preserving all essential information and maintaining professional expertise
version: 1.0.0
allowed-tools: [Read, Write, Edit, Glob, Grep]
---

# PartitaIVA Style Translator

## Purpose
Transforms robotic, schematic, SEO-optimized articles into natural, conversational content that sounds like an experienced commercialista explaining concepts to a client - the PartitaIVA.it style.

## When to Use This Skill
Use when you have:
- Articles with too many tables, checklists, and bullet points
- Content that sounds like an "SEO manual" rather than expert advice
- Text that's too technical, academic, or robotic
- Articles lacking natural flow and conversational tone
- Content that needs to be more accessible to foreign professionals

## Core Transformation Process

### Phase 1: Content Analysis
1. **Identify Schematic Elements**:
   - Tables with comparison data
   - Checklists and bullet points
   - SEO-heavy schema markup
   - Keyword stuffing patterns
   - Overly technical terminology

2. **Map Essential Information**:
   - Numbers, dates, requirements that must be preserved
   - Practical examples and case studies
   - Expert tips and insights
   - Legal/tax accuracy requirements

### Phase 2: Style Transformation

#### Tables → Narrative Paragraphs
**Before:**
```markdown
| Regime | Aliquota | Limite Ricavi |
|--------|----------|---------------|
| Forfettario | 5%* | 85.000€ |
| Ordinario | 23-43% | Nessuno |
```

**After:**
```markdown
Il regime forfettario rappresenta spesso la scelta migliore per professionisti e piccole imprese: con un'imposta sostitutiva del 5% per i primi cinque anni di attività e un limite di 85.000 euro di ricavi, offre un vantaggio fiscale significativo rispetto al regime ordinario, dove le aliquote IRPEF possono arrivare fino al 43% senza limiti di fatturato.
```

#### Checklists → Integrated Advice
**Before:**
```markdown
## Passi per Aprire Partita IVA
1. ✅ Verifica requisiti
2. ✅ Richiedi codice fiscale
3. ✅ Scegli commercialista
```

**After:**
```markdown
Per avviare la tua attività, ti consiglio di seguire un percorso ordinato. Prima di tutto, verifica di avere tutti i requisiti necessari, specialmente se sei un cittadino extra-UE. Subito dopo, richiedi il codice fiscale - è il tuo identificativo fondamentale in Italia. A questo punto, il passo più importante è scegliere un buon commercialista che ti accompagni nel percorso burocratico e fiscale.
```

### Phase 3: Tone Optimization
- **Professional but Accessible**: Like a commercialista talking to a client
- **Active Voice**: Use "tu" to create personal connection
- **Natural Language**: Avoid SEO jargon, use real sector terminology
- **Narrative Flow**: Explanations that tell a story, not lists of facts
- **Practical Examples**: Real cases integrated naturally

## Style Guidelines

### Voice and Tone
- **Warm & Professional**: Like an experienced advisor
- **Clear & Direct**: No academic jargon or bureaucratic language
- **Empathetic**: Understanding foreign entrepreneurs' challenges
- **Confident**: Demonstrating real expertise through specific examples

### Structure Flow
1. **Hook**: Personal opening that addresses reader's situation
2. **Context**: Why this matters specifically for them
3. **Explanation**: Natural narrative with examples and data
4. **Practical Advice**: Actionable insights from real experience
5. **Next Steps**: Clear guidance on what to do next

### Language Patterns
- **Instead of**: "I dati indicano che..."
- **Use**: "Nella nostra esperienza con oltre 100 clienti..."

- **Instead of**: "È importante notare che..."
- **Use**: "Ti consiglio di prestare attenzione a..."

- **Instead of**: "Il processo consiste in..."
- **Use**: "Per fare questo, dovrai seguire questi passaggi..."

## Information Preservation Rules

### What to Keep (Transformed)
- ✓ All numerical data (amounts, percentages, dates)
- ✓ Legal requirements and deadlines
- ✓ Practical examples and case studies
- ✓ Expert insights and professional advice
- ✓ Step-by-step processes (as narrative)
- ✓ Cost comparisons and timelines

### What to Remove/Simplify
- ✗ Keyword stuffing and repetitive terms
- ✗ Complex schema markup (keep basic only)
- ✗ Overly technical jargon
- ✗ Generic SEO advice
- ✗ Redundant checklists
- ✗ Tables that can be narrative

## Quality Validation Checklist

### Style Validation
- [ ] Sounds like a commercialista talking to a client?
- [ ] Natural, conversational tone?
- [ ] Personal connection with reader?
- [ ] Professional expertise clearly demonstrated?
- [ ] Accessible to foreign professionals?

### Content Validation
- [ ] All essential information preserved?
- [ ] Examples practical and real?
- [ ] Numbers and requirements accurate?
- [ ] Legal information correct?
- [ ] Next steps clear and actionable?

## Before & After Examples

### Example 1: Tax Rates
**Before:**
```markdown
## Aliquote IRPEF 2024
- Fino a 28.000€: 23%
- Da 28.001€ a 50.000€: 35%
- Oltre 50.000€: 43%
```

**After:**
```markdown
Per quanto riguarda le tasse, il sistema italiano prevede tre scaglioni IRPEF. Sui primi 28.000 euro di reddito pagherai il 23%, una aliquota relativamente bassa che rende il regime forfettario molto conveniente per molti professionisti. Superata questa soglia, la percentuale sale al 35% fino a 50.000 euro, per poi arrivare al 43% per redditi superiori.
```

### Example 2: Process Timeline
**Before:**
```markdown
| Step | Timeline | Required Documents |
|------|----------|-------------------|
| Codice Fiscale | 1-2 weeks | Passport, visa |
| CCIA Registration | 2-3 weeks | Business plan, statutes |
```

**After:**
```markdown
La prima cosa di cui avrai bisogno è il codice fiscale, che richiede solitamente 1-2 settimane con il passaporto e il visto. Una volta ottenuto, puoi procedere con la registrazione alla Camera di Commercio, un processo che richiede altre 2-3 settimane e per il quale dovrai presentare il business plan e lo statuto della tua azienda.
```

## Success Metrics
Transformed content should achieve:
- Higher readability scores (>8/10)
- Increased user engagement (time on page >4 min)
- Better conversion rates (CTA clicks)
- Positive user feedback on natural tone
- Maintained SEO performance with better user metrics