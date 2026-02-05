---
name: validate_translation
description: Validate that a translation is acceptable by checking placeholder preservation, length, encoding, and common errors. Use when reviewing translations or validating i18n file updates.
---

# Validate Translation

Validate that a translated string meets quality requirements and preserves required elements from the original.

## Inputs

- **original_text**: The original English text
- **translated_text**: The translated text to validate
- **target_language_code**: ISO language code (e.g., `es`, `fr`, `de`)

## Output

Return a validation result object:

```json
{
  "valid": true,
  "issues": [],
  "warnings": []
}
```

Or with problems:

```json
{
  "valid": false,
  "issues": [
    "Missing placeholder: {{name}}"
  ],
  "warnings": [
    "Translation is 2.8x longer than original"
  ]
}
```

- **valid**: `false` if any blocking issues exist, `true` otherwise
- **issues**: Blocking problems that must be fixed (array of strings)
- **warnings**: Non-blocking concerns to review (array of strings)

## Validation Checks

### 1. Placeholder Preservation (Blocking)

Extract all placeholders from the original text and verify they exist in the translation.

**Placeholder patterns to check:**

| Pattern | Regex | Example |
|---------|-------|---------|
| Double braces | `\{\{[\w.]+\}\}` | `{{name}}`, `{{user.email}}` |
| Single braces | `\{[\w]+\}` | `{count}`, `{0}` |
| Dollar braces | `\$\{[\w]+\}` | `${total}` |
| Printf style | `%[sd]` | `%s`, `%d` |
| Percent braces | `%\{[\w]+\}` | `%{count}` |
| Double brackets | `\[\[[\w]+\]\]` | `[[user]]` |
| Numbered tags | `<\d+>` | `<0>`, `<1>` |

**Checks:**
- All placeholders from original must appear in translation
- No extra placeholders should be added
- Placeholder syntax must be preserved exactly (e.g., `{{name}}` not `{name}`)

**Issues (blocking):**
- `"Missing placeholder: {{name}}"`
- `"Extra placeholder in translation: {{unknown}}"`
- `"Placeholder syntax modified: {{name}} changed to {name}"`

### 2. Empty or Whitespace (Blocking)

Check that the translation is not empty or only whitespace.

**Issue (blocking):**
- `"Translation is empty or whitespace only"`

### 3. Untranslated Markers (Blocking)

Check for common markers indicating incomplete translation.

**Patterns to detect:**
- `TRANSLATE_ME`
- `TODO`
- `[TODO]`
- `FIXME`
- `XXX`
- `UNTRANSLATED`
- `NEEDS_TRANSLATION`
- `TBD`

**Issue (blocking):**
- `"Contains untranslated marker: [TODO]"`

### 4. Still in English Check (Warning)

Perform a basic check to see if the text might still be in English when it shouldn't be.

**Logic:**
- If original and translated are identical AND original has 3+ words
- AND target language is not English
- This suggests the text wasn't translated

**Warning:**
- `"Translation appears identical to English original"`

**Exceptions (do not warn):**
- Single words (might be proper nouns, technical terms)
- URLs, email addresses, technical identifiers
- Text that's mostly placeholders

### 5. Length Ratio Check (Warning)

Compare the length of translation to original.

**Acceptable ratios by language family:**

| Language | Min Ratio | Max Ratio | Notes |
|----------|-----------|-----------|-------|
| German (de) | 0.8 | 1.5 | Compound words, but efficient |
| French (fr) | 0.9 | 1.4 | Slightly longer than English |
| Spanish (es) | 0.9 | 1.4 | Slightly longer than English |
| Italian (it) | 0.9 | 1.4 | Similar to Spanish |
| Portuguese (pt) | 0.9 | 1.4 | Similar to Spanish |
| Russian (ru) | 0.8 | 1.5 | Cyrillic, varies |
| Chinese (zh) | 0.3 | 0.8 | Much more compact |
| Japanese (ja) | 0.4 | 1.0 | More compact |
| Korean (ko) | 0.5 | 1.0 | More compact |
| Arabic (ar) | 0.8 | 1.4 | Varies |
| Hebrew (he) | 0.7 | 1.2 | Generally shorter |
| Hindi (hi) | 0.9 | 1.5 | Can be longer |
| Thai (th) | 0.8 | 1.3 | Generally similar |
| Default | 0.5 | 3.0 | Permissive fallback |

**Warning:**
- `"Translation is unusually short (0.3x original length)"`
- `"Translation is unusually long (2.5x original length)"`

**Exceptions (skip check):**
- Original is less than 10 characters
- Text is mostly placeholders
- Single word translations

### 6. Character Encoding (Blocking)

Check for encoding issues.

**Patterns to detect:**
- Replacement character: `�` (U+FFFD)
- Mojibake patterns: `Ã©` instead of `é`
- Null characters: `\x00`
- Control characters (except `\n`, `\t`)

**Issue (blocking):**
- `"Contains invalid character encoding (replacement character found)"`
- `"Contains suspicious encoding pattern (possible mojibake)"`

### 7. HTML/Entity Preservation (Warning)

If original contains HTML entities, check they're preserved or properly converted.

**Entities to check:**
- `&nbsp;`, `&amp;`, `&lt;`, `&gt;`, `&quot;`, `&#...;`

**Warning:**
- `"HTML entity &nbsp; in original not found in translation"`

### 8. Newline/Formatting Preservation (Warning)

Check that structural formatting is preserved.

**Check:**
- If original has `\n`, translation should have `\n`
- If original has leading/trailing whitespace, translation should match

**Warning:**
- `"Original has newlines but translation does not"`
- `"Original has trailing punctuation but translation does not"`

## Severity Classification

### Blocking Issues (valid = false)
- Missing placeholders
- Extra placeholders
- Modified placeholder syntax
- Empty translation
- Untranslated markers
- Invalid character encoding

### Warnings (valid = true, but review recommended)
- Identical to English
- Unusual length ratio
- Missing HTML entities
- Formatting differences

## Examples

### Valid Translation

```
Input:
  original_text: "Hello {{name}}, you have {{count}} messages."
  translated_text: "Hola {{name}}, tienes {{count}} mensajes."
  target_language_code: "es"

Output:
  {
    "valid": true,
    "issues": [],
    "warnings": []
  }
```

### Missing Placeholder

```
Input:
  original_text: "Welcome {{name}}!"
  translated_text: "¡Bienvenido!"
  target_language_code: "es"

Output:
  {
    "valid": false,
    "issues": ["Missing placeholder: {{name}}"],
    "warnings": []
  }
```

### Untranslated

```
Input:
  original_text: "Save changes"
  translated_text: "Save changes"
  target_language_code: "de"

Output:
  {
    "valid": true,
    "issues": [],
    "warnings": ["Translation appears identical to English original"]
  }
```

### Multiple Issues

```
Input:
  original_text: "Delete {{count}} items permanently"
  translated_text: "[TODO] Supprimer {count} éléments"
  target_language_code: "fr"

Output:
  {
    "valid": false,
    "issues": [
      "Contains untranslated marker: [TODO]",
      "Placeholder syntax modified: {{count}} changed to {count}"
    ],
    "warnings": []
  }
```

### Length Warning

```
Input:
  original_text: "OK"
  translated_text: "De acuerdo, entendido"
  target_language_code: "es"

Output:
  {
    "valid": true,
    "issues": [],
    "warnings": ["Translation is 10.5x longer than original"]
  }
```

## Implementation Notes

1. **Be permissive**: Languages vary significantly. When in doubt, warn rather than block.

2. **Context matters**: A translation that seems "wrong" might be intentional (e.g., adapting idioms).

3. **Placeholder order**: Placeholders may legitimately be reordered for grammar. Only check presence, not position.

4. **Case sensitivity**: Placeholder names are case-sensitive. `{{Name}}` ≠ `{{name}}`.

5. **Whitespace in placeholders**: `{{ name }}` ≠ `{{name}}`. Treat as different placeholders.
