---
name: Translate
description: Translate text between languages via LibreTranslate or DeepL.
requires:
  bins: []
  env: []
---

# Translate

Translate arbitrary text. Backed by the `translate` extension which supports
two providers:

- **LibreTranslate** (default) — self-hostable, free. Set `LIBRETRANSLATE_URL`
  to your instance (defaults to the public `libretranslate.com`; note the
  public endpoint often requires a key).
- **DeepL** — higher quality, paid. Set `TRANSLATE_PROVIDER=deepl` and
  `DEEPL_API_KEY`. Free-tier keys ending in `:fx` hit the free endpoint
  automatically.

## Use when

- "Translate this to Spanish/English/..."
- Preparing multilingual replies in WhatsApp/Telegram
- Normalizing foreign-language inputs before calling other tools

## Do not use when

- The source is already a proper noun / code / URL — don't over-translate
- Large batch documents — hit the provider directly with a streaming pipeline

## Tools

- `status` — which provider is active + key presence
- `languages` — supported codes
- `translate` — `text`, `target`; optional `source` (default `auto`), `format` (`text`/`html`)
- `detect` — language detection (LibreTranslate only)

## Env

| Var | Default | Notes |
|-----|---------|-------|
| `TRANSLATE_PROVIDER` | `libretranslate` | `libretranslate` or `deepl` |
| `LIBRETRANSLATE_URL` | `https://libretranslate.com` | prefer your own self-hosted instance |
| `LIBRETRANSLATE_API_KEY` | — | required by the public endpoint |
| `DEEPL_API_KEY` | — | required when provider is `deepl` |
| `DEEPL_URL` | auto (free vs pro) | override only if routing through a proxy |
