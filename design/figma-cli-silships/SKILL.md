---
name: "Figma CLI"
description: "Control Figma Desktop directly via CLI — create components, design tokens, layouts, icons, and export designs. No API key needed."
alwaysAllow: ["Bash"]
targets: [claude, codex, droid, cursor, copilot, Craft-MyWorkspace, Craft-Brown, hermes]
---

# figma-ds-cli

CLI that controls Figma Desktop directly. No API key needed.

## Setup

The CLI must be installed from git:
```bash
git clone https://github.com/silships/figma-cli.git
cd figma-cli && npm install
```

Known install locations:
- **MacBook**: `/tmp/figma-cli` or check `~/.figma-cli/config.json`
- **Mac Studio**: `~/Tools/figma-cli`

Set `FIGMA_CLI` to the repo path, then all commands are: `node $FIGMA_CLI/src/index.js <command>`

## Connection (REQUIRED FIRST)

```bash
# Yolo Mode (recommended)
node src/index.js connect

# Safe Mode (no Figma patching)
node src/index.js connect --safe
# Then user must: Plugins → Development → FigCli
```

## Quick Reference

| User says | Command |
|-----------|---------|
| "connect to figma" | `node src/index.js connect` |
| "add shadcn colors" | `node src/index.js tokens preset shadcn` |
| "add tailwind colors" | `node src/index.js tokens tailwind` |
| "show colors on canvas" | `node src/index.js var visualize` |
| "create dashboard" | `node src/index.js blocks create dashboard-01` |
| "list blocks" | `node src/index.js blocks list` |
| "create cards/buttons" | `render-batch` + `node to-component` |
| "create a rectangle/frame" | `node src/index.js render '<Frame>...'` |
| "convert to component" | `node src/index.js node to-component "ID"` |
| "list variables" | `node src/index.js var list` |
| "find nodes named X" | `node src/index.js find "X"` |
| "what's on canvas" | `node src/index.js canvas info` |
| "export as PNG/SVG" | `node src/index.js export png` |
| "show all variants" | `node src/index.js combos` |
| "create a slot" | `node src/index.js slot create "Name"` |
| "verify creation" | `node src/index.js verify` |
| "add shadcn components" | `node src/index.js shadcn add --all` |

**Full command reference:** See REFERENCE.md in the repo.

## AI Verification

After creating any component, run `verify` to get a small screenshot for validation:

```bash
node src/index.js verify              # Screenshot of selection
node src/index.js verify "123:456"    # Screenshot of specific node
```

Returns JSON with base64 image (max 2000px, auto-scaled).

**Always verify after:** `render`, `render-batch`, `node to-component`, or any visual creation.

## Design Tokens

```bash
node src/index.js tokens preset shadcn   # 244 primitives + 32 semantic (Light/Dark)
node src/index.js tokens tailwind        # 242 Tailwind color palette
node src/index.js tokens ds              # IDS Base colors
node src/index.js var delete-all         # Delete all variables
```

## Variable Binding (var: syntax)

Use `var:name` to bind variables at creation time:

```bash
# In create commands
node src/index.js create rect "Card" --fill "var:card" --stroke "var:border"

# In JSX render
node src/index.js render '<Frame bg="var:card" stroke="var:border" rounded={12} p={24}>
  <Text color="var:foreground" size={18}>Title</Text>
</Frame>'

# In set commands
node src/index.js set fill "var:primary"
```

**shadcn variables:** `background`, `foreground`, `card`, `primary`, `secondary`, `muted`, `accent`, `border`, `input`, `ring` (and `-foreground` variants)

## Connection Modes

### Yolo Mode (Recommended)
Patches Figma once, then connects directly. Fully automatic.
- Requires Full Disk Access on macOS (one-time)

### Safe Mode
Uses plugin, no Figma modification. Start plugin each session.
- **CRITICAL: `render-batch` does NOT render text properly in Safe Mode!**
- Use `eval` with direct Figma API for components with text in Safe Mode

## Creating Components (Safe Mode)

**DO NOT use render-batch for components with text in Safe Mode.** Use `eval` with native Figma API:

```javascript
node src/index.js eval "(async () => {
  await figma.loadFontAsync({ family: 'Inter', style: 'Bold' });
  await figma.loadFontAsync({ family: 'Inter', style: 'Regular' });

  const card = figma.createFrame();
  card.name = 'Card';
  card.resize(340, 1);
  card.layoutMode = 'HORIZONTAL';
  card.primaryAxisSizingMode = 'FIXED';
  card.counterAxisSizingMode = 'AUTO';
  card.paddingTop = card.paddingBottom = card.paddingLeft = card.paddingRight = 20;
  card.cornerRadius = 12;
  card.fills = [{ type: 'SOLID', color: { r: 0.094, g: 0.094, b: 0.106 } }];

  const title = figma.createText();
  title.fontName = { family: 'Inter', style: 'Bold' };
  title.characters = 'Title';
  title.fontSize = 14;
  card.appendChild(title);
  title.layoutSizingHorizontal = 'FILL';

  const comp = figma.createComponentFromNode(card);
  return { id: comp.id, name: comp.name };
})()"
```

**Auto-Layout Rules (Text Cut-Off Prevention):**
1. Parent: `resize(WIDTH, 1)` + `primaryAxisSizingMode = 'FIXED'`
2. Children: `layoutSizingHorizontal = 'FILL'` AFTER `appendChild`
3. ALL text nodes: `layoutSizingHorizontal = 'FILL'` AFTER `appendChild`

## JSX Syntax (render command)

```jsx
// Layout
flex="row"              // or "col"
gap={16}                // spacing
p={24}                  // padding all sides
px={16} py={8}          // padding x/y

// Alignment
justify="center"        // main axis: start, center, end, between
items="center"          // cross axis: start, center, end

// Size
w={320} h={200}         // fixed
w="fill" h="fill"       // fill parent
grow={1}                // expand to fill

// Appearance
bg="#fff"               // fill color
bg="var:card"           // bind to variable
stroke="var:border"     // stroke variable
rounded={16}            // corners
shadow="4px 4px 12px rgba(0,0,0,0.25)"
opacity={0.8}
overflow="hidden"

// Text
<Text size={18} weight="bold" color="var:foreground" w="fill">Title</Text>

// Icons (Lucide via Iconify — real SVG, not placeholders)
<Icon name="lucide:home" size={20} color="var:foreground" />
```

**Common mistakes (silently ignored!):**
```
WRONG                    RIGHT
layout="horizontal"   →  flex="row"
padding={24}          →  p={24}
fill="#fff"           →  bg="#fff"
cornerRadius={12}     →  rounded={12}
fontSize={18}         →  size={18}
fontWeight="bold"     →  weight="bold"
```

## Common Pitfalls

**1. Text gets cut off:**
- ALL text needs `w="fill"` and parent needs `flex="col"` or `flex="row"` with width

**2. Toggle switches:** Use `flex` + `justify`, not absolute positioning

**3. Buttons:** Need `flex="row" justify="center" items="center"` for centered text

**4. No emojis:** Use `<Icon name="lucide:home" />` instead

**5. Three-dot menu:**
```jsx
<Frame flex="row" gap={3}>
  <Frame w={4} h={4} bg="#52525b" rounded={2} />
  <Frame w={4} h={4} bg="#52525b" rounded={2} />
  <Frame w={4} h={4} bg="#52525b" rounded={2} />
</Frame>
```

## Slots

```bash
node src/index.js slot create "Content" --flex col --gap 8
node src/index.js slot list
node src/index.js slot convert "frame-id" --name "SlotName"
```

**CRITICAL: `isSlot = true` does NOT work in eval!** Use `slot convert` command instead.

JSX: `<Slot name="Content" flex="col" gap={8} w="fill" />`

## Key Rules

1. **Always use `render`** for frames — has smart positioning
2. **Never use `eval` to create** — no positioning, overlaps at (0,0)
3. **For multiple frames:** Use `render-batch`
4. **Convert to components:** `node to-component` after creation
5. **Never delete existing nodes** without user confirmation
6. **Always verify** after visual creation

## Blocks (Pre-built Layouts)

```bash
node src/index.js blocks list
node src/index.js blocks create dashboard-01
```

## Export

```bash
node src/index.js export png           # Export as PNG
node src/index.js export svg           # Export as SVG
node src/index.js export jsx           # Export as React JSX
node src/index.js export storybook     # Export Storybook stories
node src/index.js var export css       # Variables as CSS
node src/index.js var export tailwind  # Variables as Tailwind config
```

## Website Recreation

```bash
node src/index.js recreate-url "https://example.com" --name "Page"
node src/index.js screenshot-url "https://example.com"
```
