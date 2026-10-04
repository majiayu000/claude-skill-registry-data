---
name: responsive-recomposition
description: Use for dedicated mobile, tablet, ultrawide, touch, or breakpoint design passes where content priority, layout, navigation, imagery, interaction, and motion must be recomposed rather than simply resized.
metadata:
  short-description: Recompose layouts and priorities across devices
---

# Responsive Recomposition

## Principle

Responsive design is a change in priority and composition, not only width.

For each major section ask:
- What must remain above the fold on small screens?
- Which desktop relationship must become sequence, carousel, disclosure, or separate screen?
- Does imagery need a different crop or art direction?
- Does hover behavior have a touch equivalent?
- Should motion simplify or disappear?
- Does type wrapping preserve hierarchy in both Korean and English if applicable?

## Default test widths

Use the repository viewport matrix, including a 320px edge case and representative mobile/tablet/desktop widths. Add domain-specific sizes when the product requires them.

## Mobile priorities

1. identity/context;
2. primary user job/action;
3. critical information;
4. supporting imagery/story;
5. secondary evidence.

Do not preserve desktop order when it conflicts with mobile task priority.

## Touch

Ensure controls have adequate size/spacing, drag interactions have alternatives when required, sticky UI does not obscure focus/content, and thumb reach is considered for frequent primary actions.
