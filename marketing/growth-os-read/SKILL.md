---
name: growth-os-read
description: Use this when you need to read or update marketing memory for chrisscho.uk, Total Audio Promo, NewsJack, or SpotCheck. The private growth-os repo (github.com/chrisschouk/growth-os) is the marketing memory—customer intel, what the market is telling us, eval corrections, and brand rules. This public skill pack is recipes only; growth-os is the data.
---

# Growth OS Read

The [growth-os](https://github.com/chrisschouk/growth-os) private repo is the marketing memory for all Chris Schofield brands. This skill documents how to read and update it.

## Repo structure

```
growth-os/
├── brands/
│   ├── chrisschouk/      # cafe owner intel, local SEO notes, Brighton contacts
│   ├── tap/              # artist excludes, pack pricing, Liberty recap evidence
│   ├── newsjack/         # product roadmap, launch notes
│   └── spotcheck/        # playlist audit client notes
├── notes/                # daily scratchpad, meeting notes, market observations
├── eval/
│   └── corrections.md    # what agents got wrong + how to fix it
└── what_the_market_is_telling_us.md   # synthesis of customer feedback
```

## When to read

Before writing any customer-facing copy, outreach message, or brand-specific content:

1. Check `brands/{brand}/` for excludes, pricing, voice notes
2. Check `what_the_market_is_telling_us.md` for current market intel
3. Check `eval/corrections.md` if you're repeating a task that failed before

## When to update

After customer conversations, failed outreach attempts, or when you spot a pattern:

1. **Corrections**: `eval/corrections.md` — what went wrong + root cause + fix
2. **Market intel**: `what_the_market_is_telling_us.md` — customer quote + source + date
3. **Brand notes**: `brands/{brand}/notes.md` — context that doesn't fit elsewhere

## Writing style for growth-os

- Terse bullet points, not essays
- Customer quotes verbatim in "quotes"
- Source path or date for every claim
- UK spelling
- No AI fluff

## What NOT to copy into growth-os

- Generic marketing frameworks
- Copy-pasted playbooks
- Anything already in this public skills pack
- API keys or credentials (use your harness's secrets/environment variables)

## Related

- This public skill pack: recipes and frameworks
- growth-os: memory and data
