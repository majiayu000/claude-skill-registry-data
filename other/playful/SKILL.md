---
name: playful
description: Bouncy animations, rounded everything, toy-like joy, and unapologetic fun.
---
# Playful
## Mission
Build interfaces that spark delight — every scroll bounces, every button wants to be pressed, and formality is left at the door.
## Brand
### Colors
- `#FFF9E6` — Background (warm sunshine)
- `#FF6B6B` — Primary (coral pop)
- `#4ECDC4` — Secondary (teal bounce)
- `#FFE66D` — Accent (sunny yellow)
- `#A18CD1` — Surface (soft purple)
- `#2D3436` — Text (warm charcoal)
### Typography
- Headings: **Fredoka One** (rounded, bouncy display)
- Body: **Nunito** (rounded sans-serif, warm)
- Scale: xs 0.75rem / sm 0.875rem / base 1rem / lg 1.25rem / xl 1.5rem / 2xl 2rem / 3xl 2.5rem
### Spacing
- 8px grid, but elements can break alignment for playful effect
- Section padding: 5rem vertical, 2rem horizontal
- Card gaps: 2rem
- Max content width: 65rem
### Components
- **Buttons**: Fully rounded (50px), bouncy hover (scale 1.05 with cubic-bezier bounce), colorful fill, subtle shadow
- **Cards**: Rounded (20px), tilted slightly (-1deg to +1deg random at load), colorful top border, hover lifts and straightens
- **Nav**: Sticky, colorful bg, rounded pill-shaped links, logo with bounce animation
- **Hero**: Large playful illustration or emoji-scale typography, wavy divider, upbeat CTA
- **Footer**: Wavy top divider, colorful bg, social links as large rounded icons
### Accessibility
- Contrast ratio >= 4.5:1 for body text (verify colorful combinations)
- Focus ring: 3px dashed #FF6B6B with 3px offset, fully rounded
- Reduced motion: disable all bounce, wobble, and scale animations
- Minimum font size: 0.875rem
- Fun display fonts only for headings >= 1.5rem
### Writing Tone
Enthusiastic, casual, inviting. Emojis encouraged. Contractions everywhere. "Hey!" and "Wahoo!" energy. Never serious, never sarcastic.
## Do / Don't
### Do
- Use CSS keyframes with bounce steps (0%-50%-80%-100%) for elastic effects
- Rotate cards slightly with CSS transform:rotate(-1deg) for hand-made feel
- Add micro-interactions to every interactive element (hover, focus, active)
- Use wavy SVG or border-radius dividers between sections
- Make CTA buttons large, colorful, and impossible to miss
### Don't
- Use sharp corners — minimum radius 12px everywhere
- Use dark mode (playfulness lives in light)
- Animate with linear timing functions — always use ease-out or cubic-bezier
- Use gray or muted hues — every color should feel saturated
- Make any interaction feel like a chore — forms, checkouts, and errors should still spark joy
## Quality Gates
- [ ] All interactive elements have hover and focus animations
- [ ] At least 3 @keyframes animations defined
- [ ] No sharp corners — every component has border-radius
- [ ] No gray/muted colors in palette — all colors are saturated
- [ ] Focus states are visible, dashed, and fully rounded
- [ ] Page works at 320px with bouncing animations simplified
