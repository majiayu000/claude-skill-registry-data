---
name: docs
description: Bilingual documentation (EN/UK), MkDocs, Ukrainian plurals for Pulse Radar.
---

# Documentation Skill

## Structure
```
docs/content/
├── en/              # Primary (28 files)
│   ├── index.md
│   ├── guides/
│   ├── architecture/
│   └── features/
└── uk/              # Mirror (23 files)
    └── (same structure)
```

## Sync Gap
Missing in UK:
- guides/keyboard-navigation.md
- guides/automation-quickstart.md
- guides/automation-configuration.md
- guides/automation-troubleshooting.md
- guides/automation-best-practices.md

## Ukrainian Plurals (CRITICAL)
```typescript
// 3 forms, not 2 like English!
function plural(n: number, forms: [string, string, string]): string {
  const lastTwo = n % 100;
  const lastOne = n % 10;

  if (lastTwo >= 11 && lastTwo <= 19) return forms[2];  // 11-19: "повідомлень"
  if (lastOne === 1) return forms[0];                    // 1, 21: "повідомлення"
  if (lastOne >= 2 && lastOne <= 4) return forms[1];     // 2-4: "повідомлення"
  return forms[2];                                        // 0, 5+: "повідомлень"
}

// Examples:
// 0 повідомлень, 1 повідомлення, 2 повідомлення, 5 повідомлень
// 11 повідомлень, 21 повідомлення, 22 повідомлення, 25 повідомлень
```

## Translation Rules
**DO:**
- Keep technical terms: API, endpoint, webhook
- Adapt examples: "John" → "Іван"
- Use established translations: bug → баг

**DON'T:**
- Literal: "This is" → "Це" (not "Це є")
- Calque: "I have question" → "У мене є питання" (not "Я маю питання")
- Translate names: Pulse Radar, TaskIQ, shadcn

## MkDocs Config
```yaml
plugins:
  - i18n:
      docs_structure: folder
      languages: [en, uk]
```

## Preview
```bash
just docs  # http://localhost:8081
```

## References
- @references/mkdocs.md — Full configuration
- @references/ukrainian-grammar.md — Gender, cases, common mistakes
