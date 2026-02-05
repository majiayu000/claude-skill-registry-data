---
name: semantic-line-breaks
description: Provides formatting guidelines for prose. This skill's guidance is automatically applied when writing multi-line comments, commit messages, markdown, or other prose.
---

# Semantic line breaks

## Instructions

When writing long-form comments, commit messages, Markdown, or other prose:
ALWAYS use semantic line breaks to improve readability and maintainability.

### Semantic line breaks

Semantic line breaks require breaking lines at logical points in the text,
such as after punctuation marks, conjunctions, or prepositions.

- A semantic line break MUST occur after a sentence,
  as punctuated by a period (.), exclamation mark (!), or question mark (?).

    ```
    This is an example of a semantic line break.
    Here is another sentence following the break.
    ```

- A semantic line break SHOULD occur after an independent clause
  as punctuated by a comma (,), semicolon (;), colon (:), or em dash (—).

    ```
    This is an example of a semantic line break,
    which improves readability by separating clauses.
    Multiple lines make it easier to read and maintain.
    ```

- A semantic line break MAY occur after a dependent clause
  in order to clarify grammatical structure or satisfy line length constraints.

    ```
    Semantic line breaks are not strictly required here
    but using them can enhance the clarity of the text
    and keep lines within recommended length limits.
    ```

- A semantic line break MAY be used after one or more items in a list
  in order to logically group related items or satisfy line length constraints.

- A semantic line break SHOULD occur before an enumerated or itemized list.

    ```
    The following items are important:
    (a) First item; (b) Second item; and (c) Third item.
    ```

- A semantic line break MUST NOT occur within a hyphenated word.
- A semantic line break MAY occur before and after a hyperlink.
- A semantic line break MAY occur before inline markup.

### Line length

Complying with semantic line breaks is required,
but this must not violate line length guidelines.

The following guidelines apply to line lengths:

| Target               | Preferred upper limit (SHOULD) | Absolute upper limit (MUST) |
|----------------------|--------------------------------|-----------------------------|
| Commit message title | 50 characters                  | 72 characters               |
| Commit message body  | 72 characters                  | 72 characters               |
| Code comments        | 80 characters                  | 100 characters              |
| Markdown prose       | 80 characters                  | 100 characters              |

A line may exceed the maximum line length
to accommodate hyperlinks, code elements, or other markup.

## Examples

**Multiple sentences**

```
# BAD: all on one line
All human beings are born free and equal in dignity and rights. They are endowed with reason and conscience and should act towards one another in a spirit of brotherhood.

# GOOD: with semantic line breaks
All human beings are born free and equal in dignity and rights.
They are endowed with reason and conscience
and should act towards one another in a spirit of brotherhood.
```

**Long sentences**

```
# BAD: wrapped to fit line length
The quick brown fox jumps over the lazy dog, demonstrating agility and speed in
a single bound, which is a testament to its evolutionary adaptations and
survival skills.

# GOOD: with semantic line breaks
The quick brown fox jumps over the lazy dog,
demonstrating agility and speed in a single bound,
which is a testament to its evolutionary adaptations and survival skills.
```

**Hyperlinks**

```
# BAD: Hyperlink in the middle of a line forces excessive line length
For more information, visit our documentation at <https://example.com/documentation/getting-started> to get started.

# GOOD: Hyperlink on its own line
For more information, visit our documentation at
<https://example.com/documentation/getting-started>
to get started.

# Also GOOD: semantic break after the comma
For more information,
visit our documentation at <https://example.com/documentation/getting-started>
to get started.
```

**Itemized lists**

```
# BAD: list items on the same line
The following items are important: (a) First item; (b) Second item; and (c) Third item.

# GOOD: semantic line break before the list
The following items are important:
(a) First item; (b) Second item; and (c) Third item.

# ALSO GOOD: semantic line breaks after each item
The following items are important:
(a) First item;
(b) Second item; and
(c) Third item.
```

## Common mistakes

### Exceeding line length limits

Do not exceed the absolute upper limit for line lengths.

*Solution*:

- Look for clauses or phrases earlier in the sentence
  that can be used as semantic line breaks.
- If no suitable semantic break exists,
  it's okay to break at the nearest word boundary
  to satisfy line length requirements
  while still prioritizing semantic breaks where possible.

### Breaking within hyphenated words

Never break a hyphenated word across lines.

*Solution*:
Treat hyphenated words as indivisible units
and only insert line breaks before or after the entire hyphenated word.
