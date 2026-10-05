---
name: ui
description: "Builds UI components, landing page sections, hero sections, and contact forms. Use when creating front-end visual elements."
when_to_use: "UI component, hero section, landing page, contact form, front-end, visual elements, feedback form"
allowed-tools: ["Read", "Write", "Edit", "Bash"]
user-invocable: false
---

# UI Skills

A group of skills responsible for generating UI components and forms.

## Constraint Priority and Application Conditions

1. By default, apply constraints from `${CLAUDE_SKILL_DIR}/references/ui-skills.md` with highest priority.
2. Apply `${CLAUDE_SKILL_DIR}/references/frontend-design.md` only when "edgy/unique/expressive/brand-enhancing" styles are **explicitly** requested.
3. UI Skills MUST/NEVER rules are maintained by default. However, the following exceptions are permitted **only when explicitly requested by the user**:
   - Gradients, glows, heavy decorations
   - Animations (additions/enhancements)
   - Custom easing

## Feature Details

| Feature | Details |
|---------|---------|
| **Constraint set** | See [references/ui-skills.md](${CLAUDE_SKILL_DIR}/references/ui-skills.md) / [references/frontend-design.md](${CLAUDE_SKILL_DIR}/references/frontend-design.md) |
| **Component generation** | See [references/component-generation.md](${CLAUDE_SKILL_DIR}/references/component-generation.md) |
| **Feedback forms** | See [references/feedback-forms.md](${CLAUDE_SKILL_DIR}/references/feedback-forms.md) |

## Execution Steps

1. **Apply constraint set** (following priority order)
2. **Quality gate** (Step 0)
3. Classify the user's request
4. Read the appropriate reference file from "Feature Details" above
5. Generate according to its content

### Step 0: Quality Gate (a11y Checklist)

Ensure accessibility when generating UI components:

```markdown
♿ Accessibility Checklist

Generated UI should meet the following:

### Required Items
- [ ] Set alt attributes on images
- [ ] Associate labels with form elements
- [ ] Keyboard navigable (Tab for focus movement)
- [ ] Focus state is visually distinguishable

### Recommended Items
- [ ] Do not rely on color alone for conveying information
- [ ] Contrast ratio 4.5:1 or higher (text)
- [ ] Appropriate use of aria-label / aria-describedby
- [ ] Heading structure (h1 -> h2 -> h3) is logical

### Interactive Elements
- [ ] Appropriate labels on buttons ("View product details" instead of "Details")
- [ ] Focus trap for modals/dialogs
- [ ] Error messages are read by screen readers
```

### For VibeCoders

```markdown
♿ Making Designs Accessible to Everyone

1. **Add descriptions to images**
   - Instead of "product image", use "red sneakers, front view"

2. **Make clickable areas keyboard-navigable too**
   - Navigate with Tab key, confirm with Enter

3. **Don't rely on color alone for judgment**
   - Not just red=error, but also icon+text
```
