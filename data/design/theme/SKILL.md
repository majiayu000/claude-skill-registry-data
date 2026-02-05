---
name: theme
description: Generates SCSS theme files in src/theme/ including vars.scss, shadow.scss, and index.scss with sample variables and mixins for styling.
---

# Theme Skill

## Purpose
- Generate SCSS theme files with variables and mixins.
- Add few sample SCSS variables as example in variables file.
- Add a few sample mixins as example in mixins file.
- Create an index.scss file that will forward the variables file. For example:
  ```scss
  @forward './vars';
  ```

## Output
Create the files:
- `src/theme/vars.scss`
- `src/theme/shadow.scss`
- `src/theme/index.scss`

## Notes
- `vars.scss` provides comprehensive design system variables
- `shadow.scss` provides Material Design-inspired shadow mixins (0dp to 24dp)
- Forward/use pattern enables clean imports in components
- Use with `@use '@/theme/' as *;` in components
- Shadow mixins reference `$global-black` from vars.scss
