---
name: retro-css-generator
description: Generate retro-styled CSS for WordPress login page. Use when creating custom login page designs.
---

# Retro CSS Generator

## Instructions

When creating retro login page styles:

1. **Use CSS custom properties** for colors and fonts
2. **Target login-specific selectors** (`.login`, `#loginform`)
3. **Apply retro effects subtly** - prioritize accessibility
4. **Keep styles isolated** - login page doesn't load theme styles

## Retro Style Elements

| Element       | CSS Selector        | Notes               |
| ------------- | ------------------- | ------------------- |
| Page wrapper  | `.login`            | Main container      |
| Login form    | `#loginform`        | Form element        |
| Logo area     | `.login h1 a`       | WordPress logo      |
| Error box     | `.login .message`   | Info/error messages |
| Submit button | `.wp-submit-button` | Login button        |
| Footer        | `.login footer`     | Footer area         |

## Example Pattern

```css
:root {
	--retro-bg: #2d1b4e;
	--retro-primary: #ff6b9d;
	--retro-text: #c8d6e5;
	--retro-font: 'Press Start 2P', monospace;
}

.login {
	background: var(--retro-bg);
	font-family: var(--retro-font);
}

#loginform {
	background: rgba(255, 255, 255, 0.05);
	border: 2px solid var(--retro-primary);
	border-radius: 4px;
}

.wp-submit-button {
	background: var(--retro-primary);
	color: var(--retro-bg);
	border: none;
}
```

## Guidelines

-   Define colors as `:root` variables for easy theming
-   Test contrast ratios for accessibility
-   Use subtle animations (scanlines, glow)
-   Don't modify core WordPress functionality
-   Keep CSS minimal - login page should load fast
