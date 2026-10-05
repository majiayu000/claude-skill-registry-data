---
name: icu-messageformat
description: This skill should be used when the user mentions "i18n", "internationalization", "ICU", "MessageFormat", "pluralization", "plural", "plural rules", "selectordinal", "gender select", "translation", "locale", "formatMessage", or getting number/date/plural agreement right across languages. It provides ICU MessageFormat correctness for pluralization, gender/select, and inline formatting.
---

# ICU MessageFormat

## Purpose
Provide a standardized reference for writing *correct* ICU MessageFormat, the syntax used by FormatJS/react-intl, react-i18next, vue-i18n, next-intl, and MessageFormat.js, so that translated strings agree grammatically in every target language. The single most common i18n bug is a sentence built by concatenation (`count + ' items'`); it is untranslatable because other languages inflect the noun, reorder the clause, or need more than two plural forms. ICU solves this by putting the grammar *inside* the message where translators can adapt it.

## The Core Rule: One Message, One Argument
Never split a sentence across strings or build it with `+`. A quantity, a name, or a gendered choice becomes an *argument* inside a single message, so the translator controls word order and agreement:

```
Bad:   t('cart.count') + ' ' + t('cart.items')          // untranslatable
Good:  {count, plural, one {# item} other {# items}}     // translator owns the plural
```

## Argument Types

| Form | Shape | Use for |
|---|---|---|
| Simple | `{name}` | interpolate a value verbatim |
| `plural` | `{count, plural, one {…} other {…}}` | count-based noun agreement (cardinal) |
| `selectordinal` | `{n, selectordinal, one {#st} two {#nd} few {#rd} other {#th}}` | ranks: "1st", "2nd" |
| `select` | `{gender, select, male {he} female {she} other {they}}` | gender or any enumerated branch |
| `number` | `{price, number, currency}` | locale-formatted numbers/currency/percent |
| `date` / `time` | `{when, date, medium}` | locale-formatted dates/times |

## Pluralization Is Not Two Forms
English has two cardinal forms (`one`/`other`); most languages do not. Arabic uses six (`zero`, `one`, `two`, `few`, `many`, `other`), Polish and Russian use four, Japanese and Chinese use one. You **must** author every category the *source* language needs, and never assume other locales copy English's `one`/`other`. The `#` token prints the count in the locale's number format. See `references/pluralization-rules.md`.

## The `other` Branch Is Mandatory
Every `plural`, `selectordinal`, and `select` must include an `other` branch, it is the required fallback when no category matches. A `select` on gender without `other` breaks for non-binary/unknown values.

## Escaping and Nesting
- A literal brace or `#` inside plural text is escaped with single quotes: `'{'`, `'#'`, `''` for a literal apostrophe.
- Arguments nest, a `plural` branch can contain a `select`, and both can contain `{name}`: but keep nesting shallow; deeply nested ICU is a translator burden. See `references/icu-syntax.md`.

## Additional Resources
### Reference Files
- **`references/icu-syntax.md`**: full ICU syntax with worked examples: `plural` (with `offset:` and `=0`/`=1` exact matches), `selectordinal`, `select`, `number`/`date`/`time` skeletons, nested arguments, and escaping rules.
- **`references/pluralization-rules.md`**: the CLDR plural categories (`zero`/`one`/`two`/`few`/`many`/`other`) and a language-to-categories table so you author exactly the branches each locale requires.
