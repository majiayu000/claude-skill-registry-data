---
name: form
description: Work on form UI components
allowed-tools: Read, Edit, Write, Grep, Glob, Bash(just css, just tailwind, just fmt), mcp__clojure-mcp__*
---

# Form UI Development

Work on form UI components. Before starting, read `docs/forms.org`.

## Physical Feedback, Not Messages

Forms communicate through physical metaphor:

- **Shake on rejection** — Invalid submission triggers shake animation
- **Color indicates state** — Ring colors show error/advisory/valid
- **Field-level feedback** — Individual validation with hint text
- **Button reflects state** — Submit styling changes based on validity

**BANNED:**

- Flash messages, banners, error boxes that shift content
- Toast notifications for form errors
- Ad-hoc flags like `form-error`, `rejected?`

## Validation Timing

| Pristine field + blur | No validation |
| Touched field + blur | Validate on blur |
| Field with error + input | Validate immediately (debounced) |
| Form submission | Validate all, shake if invalid |

## Tailwind CSS

**Use data structures for classes:**

```clojure
;; Good: Data structures with Winnow
:class (tw/merge-classes ["h-5" "flex" "items-center"
                          (if message "opacity-100" "opacity-0")])

;; Good: Use with-defaults
[:input (tw/with-defaults attrs ["w-full" "rounded-lg" ring-class])]
```

**BANNED: Hiccup class shorthand**

```clojure
;; BANNED
[:label.block.text-xs "Email"]

;; REQUIRED
[:label {:class "block text-xs"} "Email"]
```

## Regenerate CSS

After modifying `dev-resources/templates/tailwind.css.selmer`:

```bash
just css
```

Watch for class changes:

```bash
just tailwind
```

## Form Status Keywords

Always use qualified keywords:

```clojure
:bits.form/pristine
:bits.form/advisory
:bits.form/error
```

$ARGUMENTS
