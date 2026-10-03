---
name: issue-trees
description: Decompose a core problem into root causes with an ASCII tree. Outputs a fenced code block using box-drawing characters. Use for root-cause analysis, drilling from a high-level problem down to testable sub-problems, or step 2 of a strategic analysis.
---

# Issue Trees

## Concept

An issue tree breaks a vague problem into progressively smaller, more concrete sub-problems until you reach something testable. Each branch is a hypothesis about why the parent problem exists. Done well, the leaves are things you can actually go investigate.

## Required output format

A fenced code block with `text` syntax. Use ASCII box-drawing characters:

- `├──` non-final child
- `│  ` vertical continuation under a non-final child
- `└──` final child at each level

````markdown
```text
Core Problem
├── Category 1
│   ├── Sub-factor A
│   └── Sub-factor B
└── Category 2
    └── Sub-factor C
```
````

## Rendering fallback

Some destinations mangle box-drawing characters — Slack, certain email clients, and some chat UIs render them as boxes or question marks. If you know the output is heading to one of those, use an indented-dash tree instead:

```text
- Core Problem
  - Category 1
    - Sub-factor A
    - Sub-factor B
  - Category 2
    - Sub-factor C
```

It loses some elegance but stays readable everywhere. Default to box-drawing; switch only when needed.

**This is "Slack mode."** When the user asks for Slack / Teams / email / plain-text output (or names that as the destination), use this indented-dash form for the whole tree by default.

## Defaults & flex points

| Default | When to flex |
|---|---|
| At least 2 levels deep | A 1-level tree is a list. Push deeper. For complex problems, 3–4 levels. |
| 3–8 words per node | Stay short — long node text destroys readability. |
| Branches MECE at each level | This one doesn't flex. |
| Stop when leaves are testable | A leaf that says "we have problems with customers" isn't done. "Onboarding completion fell to 61%" is. |

## Example — marketing / conversion

**Problem:** E-commerce site conversion rate dropped from 3.2% to 1.9% over Q3.

```text
Conversion 3.2% → 1.9%
├── Traffic mix shift
│   ├── Paid social spend redirected to top-of-funnel
│   ├── Branded search share fell
│   └── Affiliate program reduction
├── On-site experience
│   ├── Page-load time +800ms after CDN change
│   ├── New checkout layout shipped Aug 14
│   └── Mobile bounce rate climbing
├── Pricing & promotion
│   ├── Promo cadence reduced (cost-cutting)
│   ├── Free-shipping threshold raised $50 → $75
│   └── Competitor undercutting on top 20 SKUs
└── Inventory & merchandising
    ├── 12 hero SKUs out of stock
    ├── New collection launch delayed two weeks
    └── Recommendation algorithm retrained
```

Every leaf is concrete. Each one could be assigned to someone with "validate this in 3 days." That's the bar.

## Common mistakes

- **Lazy categories.** "Internal" vs. "External" is too coarse. Force specificity.
- **Mixed levels.** All children of a node should be the same kind of thing.
- **Tree as list.** One level deep = bulleted list. Push deeper.
- **Verbose nodes.** Sentences in the tree make it unreadable. Compress.

## When to use this skill alone vs. as part of the full analysis

- **Standalone:** when the user has named the problem but needs help decomposing it before going to investigate.
- **As part of full analysis:** `strategy-consultant` — issue trees are step 2 of 5. If you also want to test which branch is the actual cause, follow up with `hypothesis-driven`.

---

## Acknowledgment & License

Adapted from **Analyst Academy** on YouTube — [5 Consulting Frameworks to Solve Any Problem](https://www.youtube.com/watch?v=uCmTk06aM70). MIT-licensed; see [LICENSE](../../LICENSE).
