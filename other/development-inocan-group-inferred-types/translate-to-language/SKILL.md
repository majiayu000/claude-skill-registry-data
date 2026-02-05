---
name: translate_to_language
description: Translate English text to a target language while preserving placeholders and formatting. Use when translating UI strings, i18n values, or localizing content.
---

# Translate to Language

Translate English text to a specified target language while preserving placeholders, formatting, and tone.

## Inputs

- **source_text**: The English text to translate
- **target_language_code**: ISO language code (e.g., `es`, `fr`, `de`, `zh-CN`)
- **target_language_name**: Full language name (e.g., `Spanish`, `French`, `German`)
- **context_key** (optional): The i18n key name to inform tone and context

## Output

Return the translated string only.

## Process

### Step 1: Identify Placeholders

Extract all placeholders from the source text. Common patterns:

| Pattern | Example | Description |
|---------|---------|-------------|
| `{{var}}` | `{{count}}`, `{{name}}` | Angular/i18n interpolation |
| `{var}` | `{username}`, `{0}` | General interpolation |
| `${var}` | `${total}` | Template literals |
| `%s`, `%d`, `%f` | `%s items` | Printf-style |
| `%{var}` | `%{count}` | Ruby-style |
| `[[var]]` | `[[user]]` | Custom brackets |
| `<n>` | `<0>`, `<1>` | Numbered tags |

Record each placeholder and its position for verification.

### Step 2: Analyze Formatting

Note these characteristics of the source text:

- **Capitalization style**:
  - Title Case: "Delete Selected Items"
  - Sentence case: "Delete selected items"
  - UPPERCASE: "WARNING"
  - lowercase: "loading..."

- **Punctuation**:
  - Trailing punctuation: `.`, `!`, `?`, `:`
  - Ellipsis: `...` or `…`
  - Colons for labels: "Name:"

- **HTML entities**: `&nbsp;`, `&amp;`, `&lt;`, `&gt;`, `&quot;`

- **Special characters**: `\n`, `\t`, quotes

- **Length constraints**: Note if text appears to be a button label (keep concise)

### Step 3: Determine Tone from Context

Use the context_key to infer appropriate tone:

| Key Pattern | Tone | Example |
|-------------|------|---------|
| `error.*`, `*.error` | Formal, clear | Error messages |
| `warning.*` | Cautionary, clear | Warning messages |
| `button.*`, `*.button` | Concise, action-oriented | Button labels |
| `tooltip.*`, `*.tooltip` | Helpful, explanatory | Tooltips |
| `title.*`, `*.title` | Formal, prominent | Page/dialog titles |
| `placeholder.*` | Instructive, brief | Input placeholders |
| `label.*` | Concise, descriptive | Form labels |
| `confirm.*` | Clear, question form | Confirmation dialogs |
| `success.*` | Positive, affirming | Success messages |
| `help.*`, `*.hint` | Helpful, guiding | Help text |

### Step 4: Translate

Translate the text following these rules:

1. **Preserve placeholders exactly**: Do not translate, reorder, or modify placeholder syntax
2. **Match formality**: Use formal/informal forms appropriate to the context
3. **Maintain length**: Keep similar length when possible (especially for UI elements)
4. **Preserve formatting**: Match capitalization style, punctuation, and spacing
5. **Use natural phrasing**: Prefer natural target language expressions over literal translations
6. **Handle gender/plurals**: Use appropriate grammatical forms for the target language

### Step 5: Verify

Before returning, verify:

- [ ] All placeholders from source appear in translation unchanged
- [ ] Placeholder order is logical for target language grammar
- [ ] Capitalization style matches source
- [ ] Trailing punctuation is preserved
- [ ] HTML entities are preserved
- [ ] No extra spaces or formatting changes

## Language-Specific Guidelines

### Spanish (es)
- Use formal "usted" for UI text unless context suggests informal
- Inverted punctuation for questions/exclamations: ¿...? ¡...!
- Accents are critical: sí, está, información

### French (fr)
- Use spaces before `:`, `;`, `!`, `?`
- Use formal "vous" for UI text
- Proper accents: é, è, ê, ë, à, ù, ç

### German (de)
- Capitalize all nouns
- Use formal "Sie" for UI text
- Compound words are common: Benutzereinstellungen

### Chinese (zh-CN)
- No spaces between characters
- Use Chinese punctuation: ，。？！
- Keep numbers in Arabic numerals

### Japanese (ja)
- Mix of kanji, hiragana, katakana appropriate to context
- Polite form (です/ます) for UI text
- Use Japanese punctuation: 、。

### Arabic (ar)
- Right-to-left text direction (handled by UI)
- Placeholder positions may differ grammatically
- Use appropriate Arabic numerals or keep Western numerals for technical contexts

### Hebrew (he)
- Right-to-left text direction
- Keep placeholders in logical order for RTL

### Russian (ru)
- Use formal "вы" for UI text
- Proper case endings matter
- Cyrillic quotation marks: «...»

## Examples

### Basic Translation

```
Input:
  source_text: "Delete"
  target_language_code: "es"
  target_language_name: "Spanish"

Output: "Eliminar"
```

### With Placeholder

```
Input:
  source_text: "Hello {{name}}, welcome back!"
  target_language_code: "fr"
  target_language_name: "French"
  context_key: "greeting.welcome"

Output: "Bonjour {{name}}, bienvenue !"
```

### With Multiple Placeholders

```
Input:
  source_text: "{{count}} items selected"
  target_language_code: "de"
  target_language_name: "German"
  context_key: "selection.count"

Output: "{{count}} Elemente ausgewählt"
```

### Preserving Formatting

```
Input:
  source_text: "Are you sure you want to delete \"{{name}}\"?"
  target_language_code: "es"
  target_language_name: "Spanish"
  context_key: "confirm.delete"

Output: "¿Está seguro de que desea eliminar \"{{name}}\"?"
```

### Error Message Context

```
Input:
  source_text: "Failed to save. Please try again."
  target_language_code: "ja"
  target_language_name: "Japanese"
  context_key: "error.save_failed"

Output: "保存に失敗しました。もう一度お試しください。"
```

### Label with Colon

```
Input:
  source_text: "Email Address:"
  target_language_code: "fr"
  target_language_name: "French"
  context_key: "label.email"

Output: "Adresse e-mail :"
```

## Common Pitfalls to Avoid

1. **Translating placeholders**: `{{name}}` must remain `{{name}}`, not `{{nombre}}`
2. **Changing placeholder syntax**: `{{var}}` must not become `{var}` or `[[var]]`
3. **Losing punctuation**: If source ends with `.`, translation should too
4. **Inconsistent formality**: Don't mix formal/informal forms
5. **Over-translating**: Keep technical terms if they're commonly used in English in the target locale
6. **Breaking HTML**: Preserve `&nbsp;`, tags, and entities exactly
