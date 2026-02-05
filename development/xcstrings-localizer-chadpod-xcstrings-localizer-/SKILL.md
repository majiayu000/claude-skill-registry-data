---
name: xcstrings-localizer
description: Localize Xcode .xcstrings files. Use when the user asks to "localize", "translate strings", "add translations", or mentions .xcstrings files. Supports scoped translation by file, folder, target, or string pattern.
---

# XCStrings Localizer

Translate Xcode String Catalog (.xcstrings) files directly in Claude Code.

## When to Activate

Use this skill when the user says things like:
- "localize my app"
- "translate my strings"
- "add Spanish translations"
- "translate Localizable.xcstrings"
- "find untranslated strings"
- "add German to the Widget strings"
- "translate strings in the Login folder"
- "translate error messages only"

## Workflow

### 1. Determine Scope

Ask the user to clarify scope if not specified:

| Scope Type | Example Request | How to Filter |
|------------|-----------------|---------------|
| All files | "localize my app" | Find all `**/*.xcstrings` |
| Single file | "translate Localizable.xcstrings" | Use that specific file |
| By folder | "translate strings in Source/Login/" | Glob `Source/Login/**/*.xcstrings` |
| By target | "translate Widget strings" | Check Xcode project for target membership |
| By pattern | "translate error messages" | Filter string keys matching pattern |
| By language | "add Spanish only" | Only add missing Spanish translations |

### 2. Find .xcstrings Files

```bash
# Find all xcstrings files in project
find . -name "*.xcstrings" -type f
```

Or use Glob: `**/*.xcstrings`

### 3. Read Target Languages

Check the Xcode project for configured languages:

```bash
grep -A 30 "knownRegions" *.xcodeproj/project.pbxproj | grep -E '^\s+"[a-z]{2}(-[A-Z]{2})?"'
```

Common language codes:
- `en` - English (usually source)
- `es` - Spanish
- `fr` - French
- `de` - German
- `ja` - Japanese
- `zh-Hans` - Chinese Simplified
- `zh-Hant` - Chinese Traditional
- `ko` - Korean
- `pt-BR` - Portuguese (Brazil)
- `it` - Italian

### 4. Understand XCStrings JSON Structure

An `.xcstrings` file is JSON with this structure:

```json
{
  "sourceLanguage": "en",
  "version": "1.0",
  "strings": {
    "string_key": {
      "extractionState": "manual",
      "localizations": {
        "en": {
          "stringUnit": {
            "state": "translated",
            "value": "English text"
          }
        },
        "es": {
          "stringUnit": {
            "state": "translated",
            "value": "Texto en español"
          }
        }
      }
    }
  }
}
```

**Key fields:**
- `sourceLanguage`: The base language (usually "en")
- `strings`: Object keyed by string key
- `localizations`: Object keyed by language code
- `stringUnit.state`: Translation state
- `stringUnit.value`: The translated text

**Translation states:**
- `translated` - Has a valid translation
- `new` - Newly added, needs translation
- `needs_review` - Source changed, translation may be stale
- `stale` - Marked as outdated

**Special metadata:**
- `shouldTranslate: false` - Skip this string (e.g., brand names)
- `comment` - Context for translators

### 5. Identify Strings Needing Translation

A string needs translation if:
1. The target language is missing from `localizations`
2. The state is `new` or `needs_review`
3. `shouldTranslate` is NOT `false`

### 6. Preserve Format Specifiers

**CRITICAL**: Format specifiers must be preserved exactly in translations.

| Specifier | Meaning | Example |
|-----------|---------|---------|
| `%@` | Object/String | "Hello %@" → "Hola %@" |
| `%d`, `%i` | Integer | "%d items" → "%d elementos" |
| `%ld`, `%lld` | Long integer | Same as %d |
| `%f` | Float | "%.2f miles" → "%.2f millas" |
| `%1$@`, `%2$@` | Positional args | "%1$@ sent %2$@" → "%2$@ enviado por %1$@" |
| `%#@count@` | Plural reference | Keep exactly as-is |
| `%%` | Literal % | Keep as %% |

**Positional arguments**: Languages may reorder arguments. Use positional form (`%1$@`) to allow reordering.

### 7. Handle Pluralization

Plural strings have a special structure:

```json
{
  "item_count": {
    "localizations": {
      "en": {
        "variations": {
          "plural": {
            "one": {
              "stringUnit": {
                "state": "translated",
                "value": "%d item"
              }
            },
            "other": {
              "stringUnit": {
                "state": "translated",
                "value": "%d items"
              }
            }
          }
        }
      }
    }
  }
}
```

**Plural categories by language:**
- English: `one`, `other`
- French: `one`, `many`, `other`
- Russian: `one`, `few`, `many`, `other`
- Arabic: `zero`, `one`, `two`, `few`, `many`, `other`

### 8. Translation Process

1. **Report findings first**:
   ```
   Found 3 .xcstrings files:
   - Localizable.xcstrings (245 strings, missing: es 12, fr 245)
   - InfoPlist.xcstrings (5 strings, fully translated)
   - Widget.xcstrings (18 strings, missing: es 3, fr 18)

   Target languages from project: en, es, fr

   Which would you like to translate?
   ```

2. **Confirm target language(s)** if not specified

3. **Translate in batches** (suggest 10-20 strings at a time for large files)

4. **Show translations for review** before writing:
   ```
   "welcome_message":
     en: "Welcome back, %@!"
     es: "¡Bienvenido de nuevo, %@!"

   "item_count" (plural):
     en.one: "%d item"
     en.other: "%d items"
     es.one: "%d elemento"
     es.other: "%d elementos"
   ```

5. **Write back** with state set to `translated`

### 9. Writing Back

When updating the file:
- Preserve the original JSON structure and ordering
- Set `state: "translated"` for new translations
- Keep existing translations unless explicitly updating
- Maintain proper JSON formatting (2-space indent)

## Tips for Quality Translations

1. **Read the app context**: Look at surrounding code to understand usage
2. **Check for comments**: The `comment` field provides translator context
3. **Maintain consistency**: Use same terminology across strings
4. **Respect placeholders**: Never translate `%@`, `%d`, etc.
5. **Handle HTML/Markdown**: If strings contain markup, preserve it
6. **Consider length**: Some languages expand significantly (German ~30% longer)

## Example Session

User: "Add Spanish translations to my app"

1. Find .xcstrings files: `Localizable.xcstrings`
2. Check knownRegions: `en`, `es`, `fr`
3. Read file, find 15 strings missing Spanish
4. Show: "Found 15 strings needing Spanish translation. Shall I translate them?"
5. Translate with format specifiers preserved
6. Show translations for review
7. Write back on approval
