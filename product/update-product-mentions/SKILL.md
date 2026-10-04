---
name: update-product-mentions
description: Find brand products that should be added to an existing article. Compares the article's current product mentions to the brand-config product list and proposes natural insertion points.
allowed-tools: Read, Write
---

# Update Product Mentions Skill

Old articles often pre-date current products. This skill compares the brand's current product catalog to what the article actually mentions, and proposes where new products could be added naturally.

## Input

`/update-product-mentions <slug>`

Reads:
- `content-pipeline/updates/1-extracted/{slug}.md` (with "Mentioned products" + body)
- `brand-config.md` (current product list)
- `content-pipeline/updates/0-guidance/{slug}.md` (if exists)

## Process

1. **Read the brand product catalog** from `brand-config.md`. Note each product's `status` field.
2. **Filter to eligible products:**
   - **`live`** → eligible for any update
   - **`coming-soon`** → only eligible if user `--context` explicitly says to add coming-soon teasers (e.g., "Add a roadmap mention for the new Phone Call feature")
   - **`roadmap`** → never recommend in updates (too far out; articles will go stale before launch)
3. **Read the article's mentioned products** from the extract.
4. **Identify the gap:** products in the eligible set NOT in the article.
4. **For each missing product, walk the article's H2 list:**
   - Is there an H2 where this product would fit naturally?
   - What's the surrounding context — does the section discuss a problem this product solves?
   - Apply the same "show, don't sell" test as `/product-mentions`:
     - The mention should help the reader, not pitch
     - The product must genuinely solve or demonstrate what the section covers
5. **For each natural fit, propose:**
   - Which H2 to add the mention to
   - The annotation type (walkthrough / inline / tip box)
   - 1–2 sentences of suggested text
6. **For products with no natural fit, flag** — sometimes a product belongs in a section the article doesn't have. Note this; the topic-gaps audit may suggest the missing section separately.
7. **Write the audit** to `content-pipeline/updates/3-update-product-mentions/{slug}.md`:

```markdown
# Product mentions audit: {slug}

## Currently mentioned products
- ProductA (in section "...")

## Missing products to add

### ProductB
- **Best section to mention:** "How to do X"
- **Annotation type:** walkthrough
- **Suggested addition:** "..."
- **Reason it fits:** ...

### ProductC
- **No natural fit in current sections**
- **Suggested action:** consider adding a new section on Y (see topic-gaps audit)

## Existing mentions to update
- ProductA in section "..." — currently mentioned but feature description is outdated. Update to reflect [new feature].
```

## Output

`content-pipeline/updates/3-update-product-mentions/{slug}.md`

A list of specific product additions / updates for `update-draft` to apply.

## Quality checklist

- [ ] Every `live` product from brand-config is accounted for (mentioned, suggested addition, or "no fit")
- [ ] Each suggested addition specifies the section AND the annotation
- [ ] No forced mentions — sections that don't naturally fit a product are left alone
- [ ] Existing mentions checked for accuracy (feature names, value props)
- [ ] **No `coming-soon` or `roadmap` additions suggested** unless user context authorizes them
- [ ] If existing article mentions a product that has shipped new sub-features since publication, flag for update

## When all products already fit

If the article already mentions every relevant product, the audit is short. State that. Move on.
