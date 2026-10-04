---
name: magical-translation
description: Translate, interpret, and localize user-facing text using the deterministic translation locale from the Grimoire session config cache.
---

# Magical Translation

Translate or interpret text using the Grimoire session translation locale. Use
this when a user asks for translation, localized explanation, or when another
skill needs user-facing text in the configured Grimoire locale.

## Locale

Before translating, resolve the target locale with the bundled script:

```bash
python3 <skill-dir>/scripts/resolve_translation_locale.py --format json
```

Use the returned `locale` as the translation target. Do not infer the target
language from conversation prose, source text, repository language, or host
locale when the script cannot read the session cache. If the script fails, tell
the user the Grimoire session config cache is unavailable or invalid and ask for
an explicit target language before translating.

## Translation Rules

- Preserve code, commands, file paths, branch names, issue or PR numbers,
  commit SHAs, API names, config keys, error strings, and quoted identifiers
  unless the user explicitly asks to translate them.
- Translate meaning, not just words. Explain implied intent, risk, and nuance
  when the task asks for interpretation.
- Keep source excerpts short. Summarize long source text instead of copying it.
- Redact secrets, credentials, tokens, private emails, customer data, signed URL
  query strings, and other sensitive values before echoing source details.
- Match the user's requested output shape when provided. Otherwise prefer
  concise prose or a compact table for multi-item interpretation.

## Use From Other Skills

When another skill delegates translation here, first run the locale script, then
apply these translation rules inside that skill's workflow. Return control to
the calling skill after translation or interpretation is complete.
