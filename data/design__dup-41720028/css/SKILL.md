---
name: css
description: Use when writing CSS for Discourse core, themes, or plugins - handles BEM class naming, modifiers with double dashes, block__element structure, and is-/has- state prefixes
---

# CSS

## Overview

Discourse uses a modified BEM (Block Element Modifier) variant. Double dashes for modifiers, double underscores for elements, special prefixes for states.

## When NOT to Use BEM

**Utility classes are exempt from BEM naming.** Simple, reusable utilities use single-word names:

- `.hidden`, `.show`, `.sr-only`, `.clickable`
- Located in `common/foundation/helpers.scss`
- Use `!important` to override component styles
- Not coupled to specific components

**Use BEM for:** Component-specific styling, reusable blocks
**Skip BEM for:** Generic utilities, helpers, foundation classes

## BEM Syntax Rules

| Pattern      | Syntax                | Example                                      |
| ------------ | --------------------- | -------------------------------------------- |
| **Block**    | `.block`              | `.d-button`, `.chat-message`                 |
| **Element**  | `.block__element`     | `.chat-message__avatar`, `.user-form__input` |
| **Modifier** | `.--modifier`         | `.--cancel`, `.--highlighted`                |
| **State**    | `.is-foo`, `.has-foo` | `.is-open`, `.has-errors`                    |

**Critical differences from standard BEM:**

- Modifiers use **double dash** (`--modifier`), not single dash (`-modifier`)
- States use explicit prefixes (`is-`, `has-`), not modifiers

## Modifier Application

### Direct Modifier (on element itself)

```scss
.d-button {
  background: var(--primary);

  &.--cancel {
    background: var(--secondary);
  }

  &.--danger {
    background: var(--danger);
  }
}
```

HTML: `<button class="d-button --cancel"></button>`

### Indirect Modifier (on parent)

```scss
.user-form {
  &__input {
    border: 1px solid var(--primary-low);

    // Indirect modifier - applies when parent has --error
    .--error & {
      border-color: var(--danger);
    }
  }

  &__label {
    color: var(--primary);

    .--error & {
      color: var(--danger);
    }
  }
}
```

HTML: `<div class="user-form --error">...</div>`

**Use indirect when:** Styling multiple child elements based on parent state

## State Classes

States use `is-` or `has-` prefixes:

```scss
.modal {
  display: none;

  &.is-open {
    display: block;
  }
}

.form {
  &.has-errors {
    .form__input {
      border-color: var(--danger);
    }
  }
}
```

## Visual Nesting

Always nest related elements under block:

```scss
.chat-message {
  // block styling
  display: flex;

  &__avatar {
    // element styling
    width: 40px;
    height: 40px;
  }

  &__content {
    flex: 1;
  }

  &__username {
    font-weight: bold;
  }

  &.--highlighted {
    // direct modifier
    background: var(--highlight-bg);
  }
}
```

## Common Mistakes

| Mistake             | Correct                                  |
| ------------------- | ---------------------------------------- |
| `.block .element`   | `.block__element`                        |
| `.block-element`    | `.block__element`                        |
| `.-modifier` (dash) | `.--modifier` (double dash)              |
| `.block.error`      | `.block.has-errors` or `.block.is-error` |
| `.modifier.block`   | `.block.--modifier`                      |

## Handling Legacy Code

**Don't match incorrect patterns for "consistency."** If existing code uses wrong syntax:

```scss
// ❌ WRONG - existing legacy code
.d-button.-cancel {
}
.d-button.-primary {
}

// ✅ CORRECT - your addition
.d-button.--success {
}
```

**Best practice:** Fix legacy patterns when touching the file (low-risk CSS change)

**Minimum:** Add new code correctly; don't propagate technical debt

## Quick Checklist

Before committing CSS:

- [ ] Used double dash for modifiers (`--modifier`)
- [ ] Used double underscore for elements (`block__element`)
- [ ] Used `is-` or `has-` for states
- [ ] Visually nested elements under block
- [ ] Applied modifiers directly to elements OR indirectly via parent

## Real Example

From Discourse chat plugin loading skeleton:

```scss
.chat-skeleton {
  &__body {
    display: flex;

    &.--with-avatar {
      padding-left: 50px;
    }
  }

  &__message {
    &.is-loading {
      animation: pulse 1.5s infinite;
    }
  }
}
```
