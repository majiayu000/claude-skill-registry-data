---
name: figma-use-cli
description: Control Figma from command line with 100+ commands for AI agents to create shapes, text, components, set styles, and export designs
triggers:
  - create a figma frame with layout
  - generate figma components from jsx
  - export figma designs to code
  - automate figma design changes
  - build figma prototypes programmatically
  - import icons into figma
  - analyze figma design patterns
  - convert figma nodes to jsx
---

# Figma Use CLI

> Skill by [ara.so](https://ara.so) — Design Skills collection.

Control Figma from the command line with full read/write access. Create shapes, text, components, set styles, export images, and render JSX declaratively. Designed for AI agents to automate design workflows.

## Installation

```bash
npm install -g figma-use
```

Start Figma with remote debugging:

```bash
# macOS
open -a Figma --args --remote-debugging-port=9222

# Windows
"%LOCALAPPDATA%\Figma\Figma.exe" --remote-debugging-port=9222

# Linux
figma --remote-debugging-port=9222
```

Verify connection:

```bash
figma-use status
```

**Note:** Figma 126+ blocks remote debugging. Use `figma-use daemon start --pipe` as alternative.

## Two Approaches

### Imperative Commands

Execute individual operations:

```bash
# Create styled frame
figma-use create frame --width 400 --height 300 --fill "#FFF" --radius 12 --layout VERTICAL --gap 16

# Add text
figma-use create text --content "Hello World" --size 24 --weight bold --color "#000"

# Create icon from Iconify
figma-use create icon lucide:star --size 48 --color "#F59E0B"
```

### Declarative JSX

Describe structure and render:

```bash
echo '<Frame style={{p: 24, gap: 16, flex: "col", bg: "#FFF", rounded: 12}}>
  <Text style={{size: 24, weight: "bold", color: "#000"}}>Card Title</Text>
  <Text style={{size: 14, color: "#666"}}>Description</Text>
</Frame>' | figma-use render --stdin --x 100 --y 200
```

## Core Commands

### Creating Elements

```bash
# Shapes
figma-use create frame --width 200 --height 100 --fill "#3B82F6"
figma-use create rectangle --width 100 --height 100 --fill "#10B981" --radius 8
figma-use create ellipse --width 50 --height 50 --fill "#F59E0B"
figma-use create text --content "Button" --size 16 --color "#FFF"

# Icons (150k+ from Iconify)
figma-use create icon mdi:home --size 32 --color "#3B82F6"
figma-use create icon lucide:settings --size 24

# Images
figma-use create image --url "https://example.com/photo.jpg" --width 200 --height 150
```

### Modifying Nodes

```bash
# Set properties
figma-use set fill <node-id> --color "#FF6B6B"
figma-use set size <node-id> --width 300 --height 200
figma-use set position <node-id> --x 100 --y 150
figma-use set radius <node-id> --value 16
figma-use set opacity <node-id> --value 0.8

# Layout
figma-use set layout <node-id> --mode VERTICAL --gap 16 --padding 24
figma-use set layout <node-id> --mode GRID --cols "1fr 1fr 1fr" --gap 16
```

### Inspection

```bash
# View hierarchy
figma-use node tree

# Get node details
figma-use node get <node-id>

# Query with XPath
figma-use query "//FRAME[@width < 300]"
figma-use query "//COMPONENT[starts-with(@name, 'Button')]"
figma-use query "//FRAME[contains(@name, 'Card')]"
```

### Export

```bash
# Export images
figma-use export png <node-id> --output design.png --scale 2
figma-use export svg <node-id> --output icon.svg

# Export to JSX
figma-use export jsx <node-id> --pretty
figma-use export jsx <node-id> --match-icons --prefer-icons lucide

# Export to Storybook
figma-use export storybook --out ./stories
```

## JSX Rendering

### Basic Elements

Available elements: `Frame`, `Rectangle`, `Ellipse`, `Text`, `Line`, `Star`, `Polygon`, `Vector`, `Group`, `Icon`, `Image`

```tsx
import { Frame, Text, Icon, Image } from 'figma-use/render'

export default () => (
  <Frame style={{ w: 400, h: 300, bg: '#FFF', rounded: 12, p: 24, gap: 16, flex: 'col' }}>
    <Frame style={{ flex: 'row', gap: 8 }}>
      <Icon icon="lucide:star" size={24} color="#F59E0B" />
      <Text style={{ size: 18, weight: 'bold', color: '#000' }}>Card Title</Text>
    </Frame>
    <Text style={{ size: 14, color: '#666', lineHeight: 1.5 }}>
      This is a description with multiple lines of text.
    </Text>
    <Image src="https://example.com/image.jpg" w={352} h={200} />
  </Frame>
)
```

### Style Properties

```typescript
// Size
w: 200, h: 100
minW: 100, maxW: 400
minH: 50, maxH: 300

// Colors
bg: '#3B82F6'
fill: 'var:Colors/Primary'  // Bind to Figma variable
stroke: '#000'
strokeWidth: 2

// Layout
flex: 'row' | 'col'
gap: 16
p: 24  // padding all sides
px: 16, py: 24  // horizontal/vertical
pt: 8, pr: 8, pb: 8, pl: 8  // individual sides

// Display
display: 'grid'
cols: '1fr 1fr 1fr'
rows: 'auto auto'
colGap: 16, rowGap: 16

// Shape
rounded: 12  // all corners
roundedTL: 12, roundedTR: 12, roundedBR: 12, roundedBL: 12

// Text
size: 16
weight: 'normal' | 'bold' | 'medium' | 'semibold'
align: 'left' | 'center' | 'right'
color: '#000'
lineHeight: 1.5
letterSpacing: 0.5

// Effects
opacity: 0.8
blur: 4
shadow: '0 4px 6px rgba(0,0,0,0.1)'
```

### Components

Create reusable component definitions:

```tsx
import { defineComponent, Frame, Text, Icon } from 'figma-use/render'

const Button = defineComponent(
  'Button',
  <Frame style={{ px: 16, py: 12, bg: '#3B82F6', rounded: 8, flex: 'row', gap: 8 }}>
    <Icon icon="lucide:save" size={18} color="#FFF" />
    <Text style={{ size: 16, weight: 'medium', color: '#FFF' }}>Save</Text>
  </Frame>
)

export default () => (
  <Frame style={{ gap: 16, flex: 'col' }}>
    <Button />
    <Button />
    <Button />
  </Frame>
)
```

Render the file:

```bash
figma-use render button.figma.tsx --x 100 --y 100
```

### Component Variants

Define component sets with all variant combinations:

```tsx
import { defineComponentSet, Frame, Text } from 'figma-use/render'

const Button = defineComponentSet(
  'Button',
  {
    variant: ['Primary', 'Secondary', 'Outline'] as const,
    size: ['Small', 'Medium', 'Large'] as const,
    state: ['Default', 'Hover', 'Disabled'] as const
  },
  ({ variant, size, state }) => {
    const bgColors = {
      Primary: state === 'Disabled' ? '#9CA3AF' : '#3B82F6',
      Secondary: state === 'Disabled' ? '#E5E7EB' : '#10B981',
      Outline: 'transparent'
    }
    
    const padding = size === 'Large' ? 16 : size === 'Medium' ? 12 : 8
    
    return (
      <Frame
        style={{
          px: padding * 2,
          py: padding,
          bg: bgColors[variant],
          rounded: 8,
          stroke: variant === 'Outline' ? '#3B82F6' : undefined,
          strokeWidth: variant === 'Outline' ? 2 : 0
        }}
      >
        <Text
          style={{
            size: size === 'Large' ? 18 : size === 'Medium' ? 16 : 14,
            color: variant === 'Primary' ? '#FFF' : '#111'
          }}
        >
          {variant} {size}
        </Text>
      </Frame>
    )
  }
)

export default () => (
  <Frame style={{ gap: 16, flex: 'col' }}>
    <Button variant="Primary" size="Large" state="Default" />
    <Button variant="Secondary" size="Medium" state="Hover" />
    <Button variant="Outline" size="Small" state="Default" />
  </Frame>
)
```

### Grid Layouts

CSS Grid for 2D layouts:

```tsx
<Frame
  style={{
    display: 'grid',
    cols: '100px 1fr 100px',
    rows: 'auto auto',
    gap: 16,
    w: 600,
    h: 400
  }}
>
  <Frame style={{ bg: '#FF6B6B' }} />
  <Frame style={{ bg: '#4ECDC4' }} />
  <Frame style={{ bg: '#45B7D1' }} />
  <Frame style={{ bg: '#96CEB4' }} />
  <Frame style={{ bg: '#FFEAA7' }} />
  <Frame style={{ bg: '#DDA0DD' }} />
</Frame>
```

Calendar example:

```tsx
<Frame
  style={{
    display: 'grid',
    cols: 'repeat(7, 1fr)',
    rows: 'repeat(5, 1fr)',
    gap: 8,
    w: 400,
    h: 300
  }}
>
  {Array.from({ length: 35 }, (_, i) => (
    <Frame
      key={i}
      style={{
        bg: i % 7 === 0 || i % 7 === 6 ? '#F3F4F6' : '#FFF',
        rounded: 8,
        p: 8
      }}
    >
      <Text style={{ size: 14, color: '#000' }}>{i + 1}</Text>
    </Frame>
  ))}
</Frame>
```

### Design Tokens with Variables

Bind colors to Figma variables:

```tsx
import { defineVars, Frame, Text } from 'figma-use/render'

const colors = defineVars({
  bg: { name: 'Colors/Gray/50', value: '#F8FAFC' },
  text: { name: 'Colors/Gray/900', value: '#0F172A' },
  primary: { name: 'Colors/Blue/500', value: '#3B82F6' },
  secondary: { name: 'Colors/Green/500', value: '#10B981' }
})

export default () => (
  <Frame style={{ bg: colors.bg, p: 24, gap: 16, flex: 'col' }}>
    <Text style={{ color: colors.text, size: 24 }}>Bound to variables</Text>
    <Frame style={{ bg: colors.primary, p: 16, rounded: 8 }}>
      <Text style={{ color: '#FFF', size: 16 }}>Primary Button</Text>
    </Frame>
  </Frame>
)
```

## Advanced Features

### Icons from Iconify

150,000+ icons available without downloads:

```bash
# Browse at https://icon-sets.iconify.design/

figma-use create icon mdi:home
figma-use create icon lucide:star --size 48 --color "#F59E0B"
figma-use create icon heroicons:check-circle --size 32
```

In JSX:

```tsx
<Frame style={{ flex: 'row', gap: 12 }}>
  <Icon icon="mdi:home" size={24} color="#3B82F6" />
  <Icon icon="lucide:star" size={24} color="#F59E0B" />
  <Icon icon="heroicons:check-circle" size={24} color="#10B981" />
</Frame>
```

### Diffs and Patches

Compare nodes and generate patches:

```bash
# Create diff
figma-use diff create --from 123:456 --to 789:012

# Visual diff (highlights changes in red)
figma-use diff visual --from 49:275096 --to 49:280802 --output diff.png

# Compare as JSX
figma-use diff jsx 123:456 789:012
```

### Analysis Tools

Discover patterns and inconsistencies:

```bash
# Find repeated patterns (potential components)
figma-use analyze clusters

# Color usage analysis
figma-use analyze colors
figma-use analyze colors --show-similar

# Typography audit
figma-use analyze typography
figma-use analyze typography --group-by size

# Spacing consistency
figma-use analyze spacing --grid 8

# Accessibility tree
figma-use analyze snapshot
figma-use analyze snapshot <node-id> -i
```

### Linting

Check design consistency:

```bash
figma-use lint
figma-use lint --page "Components"
figma-use lint --preset strict
figma-use lint --preset accessibility
figma-use lint -v  # verbose with fix suggestions
```

### Canvas Organization

Arrange nodes automatically:

```bash
# Grid layout (default)
figma-use arrange

# Horizontal row
figma-use arrange --mode row --gap 60

# Smart packing for mixed sizes
figma-use arrange --mode squarify --gap 60

# Binary tree packing
figma-use arrange --mode binary --gap 40
```

### Vector Path Manipulation

Work with SVG paths:

```bash
# Get path data
figma-use path get <node-id>

# Set path
figma-use path set <node-id> "M 0 0 L 100 100 Z"

# Transform
figma-use path scale <node-id> --factor 1.5
figma-use path translate <node-id> --x 10 --y 20
figma-use path flip <node-id> --axis x
figma-use path rotate <node-id> --angle 45
```

## Practical Examples

### Design System Button Variants

```tsx
import { defineComponentSet, Frame, Text, Icon } from 'figma-use/render'

const Button = defineComponentSet(
  'Button',
  {
    variant: ['Primary', 'Secondary', 'Ghost'] as const,
    size: ['SM', 'MD', 'LG'] as const,
    icon: ['None', 'Left', 'Right'] as const
  },
  ({ variant, size, icon }) => {
    const sizeMap = { SM: { px: 12, py: 6, text: 14 }, MD: { px: 16, py: 10, text: 16 }, LG: { px: 20, py: 14, text: 18 } }
    const colorMap = {
      Primary: { bg: '#3B82F6', text: '#FFF' },
      Secondary: { bg: '#E5E7EB', text: '#111' },
      Ghost: { bg: 'transparent', text: '#3B82F6' }
    }
    
    const s = sizeMap[size]
    const c = colorMap[variant]
    
    return (
      <Frame style={{ px: s.px, py: s.py, bg: c.bg, rounded: 8, flex: 'row', gap: 8 }}>
        {icon === 'Left' && <Icon icon="lucide:arrow-left" size={s.text} color={c.text} />}
        <Text style={{ size: s.text, weight: 'medium', color: c.text }}>Button</Text>
        {icon === 'Right' && <Icon icon="lucide:arrow-right" size={s.text} color={c.text} />}
      </Frame>
    )
  }
)

export default () => (
  <Frame style={{ gap: 24, flex: 'col', p: 40 }}>
    <Button variant="Primary" size="LG" icon="Right" />
    <Button variant="Secondary" size="MD" icon="None" />
    <Button variant="Ghost" size="SM" icon="Left" />
  </Frame>
)
```

### Calendar UI

```tsx
import { Frame, Text } from 'figma-use/render'

const days = ['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat']
const daysInMonth = 31

export default () => (
  <Frame style={{ w: 400, p: 24, bg: '#FFF', rounded: 16, gap: 16, flex: 'col' }}>
    <Text style={{ size: 20, weight: 'bold', color: '#000' }}>January 2024</Text>
    
    <Frame style={{ display: 'grid', cols: 'repeat(7, 1fr)', gap: 8 }}>
      {days.map(day => (
        <Text key={day} style={{ size: 12, weight: 'medium', color: '#666', align: 'center' }}>
          {day}
        </Text>
      ))}
    </Frame>
    
    <Frame style={{ display: 'grid', cols: 'repeat(7, 1fr)', rows: 'repeat(5, 1fr)', gap: 4 }}>
      {Array.from({ length: daysInMonth }, (_, i) => (
        <Frame
          key={i}
          style={{
            bg: i === 14 ? '#3B82F6' : '#F9FAFB',
            rounded: 8,
            p: 8,
            flex: 'col'
          }}
        >
          <Text
            style={{
              size: 14,
              color: i === 14 ? '#FFF' : '#000',
              align: 'center'
            }}
          >
            {i + 1}
          </Text>
        </Frame>
      ))}
    </Frame>
  </Frame>
)
```

### Dashboard Layout

```tsx
import { Frame, Text, Icon } from 'figma-use/render'

const StatCard = ({ title, value, icon, color }: { title: string; value: string; icon: string; color: string }) => (
  <Frame style={{ bg: '#FFF', rounded: 12, p: 20, gap: 12, flex: 'col' }}>
    <Frame style={{ flex: 'row', gap: 8 }}>
      <Frame style={{ w: 40, h: 40, bg: color + '20', rounded: 8, flex: 'row' }}>
        <Icon icon={icon} size={24} color={color} />
      </Frame>
      <Frame style={{ flex: 'col', gap: 4 }}>
        <Text style={{ size: 14, color: '#666' }}>{title}</Text>
        <Text style={{ size: 24, weight: 'bold', color: '#000' }}>{value}</Text>
      </Frame>
    </Frame>
  </Frame>
)

export default () => (
  <Frame style={{ w: 1200, p: 40, bg: '#F9FAFB', gap: 24, flex: 'col' }}>
    <Text style={{ size: 28, weight: 'bold', color: '#000' }}>Dashboard</Text>
    
    <Frame style={{ display: 'grid', cols: '1fr 1fr 1fr 1fr', gap: 20 }}>
      <StatCard title="Total Users" value="12,543" icon="lucide:users" color="#3B82F6" />
      <StatCard title="Revenue" value="$45,231" icon="lucide:dollar-sign" color="#10B981" />
      <StatCard title="Orders" value="1,234" icon="lucide:shopping-cart" color="#F59E0B" />
      <StatCard title="Growth" value="+23%" icon="lucide:trending-up" color="#8B5CF6" />
    </Frame>
  </Frame>
)
```

## Troubleshooting

### Connection Issues

If `figma-use status` fails:

1. Ensure Figma is running with `--remote-debugging-port=9222`
2. Check no other process uses port 9222
3. For Figma 126+, use pipe mode:

```bash
figma-use daemon start --pipe
```

### Render Failures

If JSX rendering fails:

```bash
# Check syntax
figma-use render file.figma.tsx --validate

# Verbose output
figma-use render file.figma.tsx --verbose

# Test with simple example first
echo '<Frame style={{w: 100, h: 100, bg: "#FF0000"}} />' | figma-use render --stdin
```

### Variable Binding Issues

If variables don't bind:

```bash
# List available variables
figma-use variables list

# Use exact variable name
figma-use create frame --fill "var:Colors/Primary/500"

# Or reference by ID
figma-use create frame --fill "$abc123"
```

### Node ID Format

Node IDs are in format `pageId:nodeId`:

```bash
# Get current page ID
figma-use page current

# Use full ID
figma-use node get 0:123

# Or just node ID if on current page
figma-use node get 123
```

### Export Issues

If exports fail:

```bash
# Check node exists
figma-use node get <node-id>

# Try different format
figma-use export png <node-id> --scale 1 --output test.png

# Check permissions
ls -la $(pwd)
```

## Environment Variables

```bash
# Custom debugging port
FIGMA_DEBUG_PORT=9222

# Custom timeout for operations (ms)
FIGMA_TIMEOUT=30000

# Log level
FIGMA_LOG_LEVEL=debug
```

## Best Practices

1. **Use JSX for complex layouts** — easier to visualize and maintain than sequential commands
2. **Define components once** — first render creates master, subsequent renders create instances
3. **Bind to variables** — use `var:` prefix for colors to maintain design system consistency
4. **Query before modify** — use XPath queries to find nodes before batch operations
5. **Export to JSX for templates** — capture existing designs as code for reuse
6. **Arrange after bulk creation** — use `figma-use arrange` to organize canvas automatically
7. **Lint regularly** — catch inconsistencies early with `figma-use lint`
8. **Use icons by name** — avoid manual imports, let Iconify handle the library
