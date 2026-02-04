---
name: figlet-typography
description: Generate ASCII art typography using pyfiglet. Use when user asks for ASCII art text, banners, headers, logo text, terminal art, or decorative typography. Curated whitelist of 24 display fonts available, agent can also use any of 500+ pyfiglet fonts.
allowed-tools: Bash, Write, Read
---

# Figlet ASCII Art Typography

Generate stylised ASCII art text using pyfiglet. This skill is for creating banners, headers, logos, and decorative terminal typography.

## Usage

Run the wrapper script or call pyfiglet directly:

```bash
# Using wrapper script
python .claude/skills/figlet-typography/figlet_gen.py "Your Text" larry3d

# Or directly with pyfiglet
python -c "import pyfiglet; print(pyfiglet.figlet_format('Your Text', font='larry3d'))"
```

## Curated Font Whitelist

These fonts have been tested and produce excellent results:

| Font | Style | Best For |
|------|-------|----------|
| `larry3d` | 3D block letters | Headers, logos |
| `doh` | Large bubble | Big impact banners |
| `isometric1` | 3D isometric | Technical/sci-fi |
| `impossible` | Impossible geometry | Creative headers |
| `3d_diagonal` | Diagonal 3D | Stylised text |
| `chiseled` | Carved stone | Elegant titles |
| `poison` | Gothic/punk | Dark themes |
| `sub-zero` | Clean geometric | Modern look |
| `keyboard` | Keyboard keys | UI/interactive |
| `smkeyboard` | Small keyboard | Compact UI |
| `dotmatrix` | LED display | Retro/digital |
| `modular` | Block modules | Technical |
| `lean` | Slanted minimal | Fast/dynamic |
| `bell` | Classic serif | Traditional |
| `acrobatic` | Stick figures | Playful |
| `ghoulish` | Spooky curves | Halloween/horror |
| `muzzle` | Minimal | Compact spaces |
| `pawp` | Bubble lowercase | Cute/casual |
| `peaks` | Mountain peaks | Nature themes |
| `ticks` | Slashes/ticks | Matrix style |
| `ticksslant` | Slanted ticks | Italic matrix |
| `catwalk` | Underscore style | Fashion/sleek |
| `defleppard` | Rock band style | Music/energy |
| `merlin1` | Wizard/magical | Fantasy |

## Font Selection Guidelines

Choose fonts based on context:
- **Headers/Logos**: `larry3d`, `doh`, `isometric1`, `impossible`
- **Technical/Sci-fi**: `dotmatrix`, `modular`, `isometric1`, `ticks`
- **Playful/Casual**: `acrobatic`, `pawp`, `bell`
- **Dark/Gothic**: `poison`, `ghoulish`, `defleppard`
- **Compact**: `muzzle`, `smkeyboard`, `lean`
- **Fantasy**: `merlin1`, `chiseled`

## All Available Fonts

The agent can use ANY pyfiglet font. List all available:

```bash
python -c "import pyfiglet; print('\n'.join(pyfiglet.FigletFont.getFonts()))"
```

## Output Options

### Direct console output
```bash
python .claude/skills/figlet-typography/figlet_gen.py "TEXT" font_name
```

### Save to file
```bash
python .claude/skills/figlet-typography/figlet_gen.py "TEXT" font_name > output.txt
```

### Custom width (default 200)
```bash
python .claude/skills/figlet-typography/figlet_gen.py "TEXT" font_name 80
```

## Examples

**User:** "Create an ASCII banner for WIBWOB"
**Action:** Generate using a suitable font like `larry3d` or `doh`

**User:** "Make a retro terminal header"
**Action:** Use `dotmatrix` or `ticks` font

**User:** "I need a gothic title for a horror section"
**Action:** Use `poison` or `ghoulish`

## Notes

- Fonts render best in monospace terminals/editors
- Very long text may wrap poorly - use shorter strings
- Some fonts are very tall (like `doh`) - consider context
- Preview fonts in `fonts-preview.md` before choosing
- If a font isn't installed, pyfiglet will error - fall back to `standard`
