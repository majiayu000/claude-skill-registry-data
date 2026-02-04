---
name: Composition AI Research
description: Research product compositions using AI and web sources. Use when needing to find what products, substances, or objects are made of - including ingredients, materials, chemicals, and elements. Essential for building composition data.
---

# Composition AI Research Skill

## Purpose

This skill enables thorough research into what things are made of. Use it to gather accurate composition data for any product, substance, organism, or object.

## When to Use

- User asks to research a composition
- Building the composition database
- Verifying or updating existing composition data
- Finding sources for composition claims

## Research Process

### Step 1: Identify the Subject
Clarify exactly what we're researching:
- Product name, brand, variant (e.g., "Kellogg's Frosted Flakes 13.5oz box")
- Category (food, electronics, biological, chemical, etc.)
- Any specific version or configuration

### Step 2: Source Priority
Research in this order:

1. **Official Sources** (highest confidence)
   - Manufacturer websites
   - FDA ingredient databases
   - Safety Data Sheets (SDS/MSDS)
   - Nutrition labels
   - Patent filings

2. **Scientific Sources**
   - PubChem for chemical data
   - Scientific papers
   - MaterialsProject for materials
   - Industry technical specs

3. **Analysis Sources**
   - iFixit teardowns (electronics)
   - Independent lab testing
   - Engineering analysis sites
   - Consumer reports

4. **Secondary Sources** (verify independently)
   - Wikipedia (check sources)
   - News articles
   - Industry reports

### Step 3: Data Structure

Organize findings hierarchically:

```
Level 1: Product (iPhone 15 Pro)
  └── Level 2: Component (Battery)
        └── Level 3: Material (Lithium-ion cell)
              └── Level 4: Chemical (Lithium cobalt oxide)
                    └── Level 5: Element (Li, Co, O)
```

### Step 4: Confidence Assessment

For each data point:
- **Verified**: Direct from official source with citation
- **Estimated**: Based on similar products or industry standards
- **Speculative**: Reasonable inference when data unavailable

## Output Format

Return research as structured JSON:

```json
{
  "subject": {
    "name": "Product Name",
    "category": "Category",
    "variant": "Specific variant if applicable"
  },
  "composition": [
    {
      "name": "Component Name",
      "percentage": 45.2,
      "confidence": "verified",
      "source": "https://source-url.com",
      "type": "component",
      "children": []
    }
  ],
  "sources": [
    {
      "url": "https://...",
      "title": "Source Title",
      "type": "official|scientific|analysis|secondary",
      "accessed": "2024-01-15"
    }
  ],
  "notes": "Any caveats or limitations"
}
```

## Common Research Patterns

### Food Products
1. Start with nutrition facts label
2. FDA Food Composition Database
3. Research each ingredient's chemical makeup
4. Track to molecular/elemental level

### Electronics
1. Search for teardown reports
2. Check manufacturer sustainability reports
3. Research battery chemistry specifically
4. Patents often reveal proprietary details

### Chemicals
1. PubChem for molecular structure
2. SDS for composition percentages
3. ChemSpider for additional data
4. Scientific literature for variations

### Biological
1. Scientific databases (UniProt, NCBI)
2. Peer-reviewed papers
3. Consider hydrated vs dry weight
4. Note species-specific variations

## Quality Guidelines

1. **Always cite sources** - Every percentage needs a source
2. **Use ranges when uncertain** - "40-50%" better than guessing "45%"
3. **Note proprietary limitations** - Some data is trade secret
4. **Cross-reference multiple sources** - Don't rely on single source
5. **Date your research** - Compositions can change over time
