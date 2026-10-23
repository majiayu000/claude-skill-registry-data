---
name: polish-design-system
description: "Find hard-coded colours, propose tokens, apply them once approved. Use when the user says \"polish the design system\", \"audit tokens\" or \"hardcoded colors\"."
license: MIT
metadata:
  author: Tony Gorb
  source: https://github.com/tonygorb/skills
  category: design-systems
  cover: "0 hex"
---

# Polish a design system

Audit the tokens, propose, wait for a yes, apply everywhere at once, then update the docs.

## The rule underneath

Two layers. **Primitives** are raw values (`olive-400`, `#7a8a3c`). **Semantic tokens** say what a
value is for (`text-primary`, `bg-surface`) and point at a primitive. Components use semantic
tokens (and component tokens, where a system has them), never primitives and never raw values. The same rule holds in Figma: primitive
variables hold the raw values, semantic variables alias them, with a Light and a Dark mode.

## Steps

### 1. Audit

Search the component code for raw values. For a React and Tailwind project:

```bash
grep -rn --include="*.tsx" -E "#([0-9a-fA-F]{8}|[0-9a-fA-F]{6}|[0-9a-fA-F]{3,4})\b" src/  # hex (skip anchors like href="#add")
grep -rn --include="*.tsx" -E "style=.*(background|color|border)" src/ # inline colour styles
grep -rn --include="*.tsx" -E "(bg|text|border)-\[" src/              # arbitrary bracket values
grep -rn --include="*.tsx" -E "\b(bg|text|border|ring|fill|stroke)-(slate|gray|zinc|neutral|stone|red|orange|amber|yellow|lime|green|emerald|teal|cyan|sky|blue|indigo|violet|purple|fuchsia|pink|rose)-[0-9]{2,3}\b" src/  # raw palette classes
```

Record each hit: file, line, value, the token it should be.

### 2. Sort every hit into one of four

- **A token already exists:** swap in the semantic class.
- **The token is missing:** propose a semantic token, and the primitive it points at.
- **Design drift:** the design file has a value the code doesn't. Port it: primitive first, then semantic.
- **Bespoke on purpose:** rare. Leave it, and write down why.

### 3. Propose, then stop

```
Audit: <N> hard-coded values in <M> files
Drift from the design file: <list, or "none">
New primitives: <name> (<value>)
New semantic tokens: <name> → <primitive>
Renames and deprecations: <list>
Apply?
```

Wait for the user's yes.

### 4. Apply

1. Add the primitives and semantic tokens to the theme file (for example the `@theme` block).
2. Replace the raw values, file by file.
3. Build, then look at the changed screens at phone, tablet and desktop widths.

### 5. Document

Update the design-system doc: new primitives under their family, new semantic tokens under their
group, renames and deprecations noted, and the date of this pass at the top.

### 6. Flag the design file

If code gained tokens, list them for the user to add to the design file. Don't edit the design file
from this skill.

## Don't

- Add a colour family on a whim. Most products need fewer than ten.
- Change the radius or type scale without asking: those are brand decisions.
- Unify tokens across separate products that differ on purpose.
