---
name: ux-wireframing
description: Create ASCII wireframes for web and mobile apps before development. Use when designing screens, visualizing UI flows, creating mockups for user approval, planning layouts, or explaining UI ideas without design tools. Triggers on wireframe, mockup, UI design, screen layout, prototype, ASCII art, user flow diagram.
---

# UX Wireframing Skill

Create beautiful ASCII art wireframes for web and mobile applications. Use this skill whenever you need to visualize UI screens before development, create mockups for user approval, design interaction flows, or communicate UI ideas quickly without graphic design tools. Especially useful during requirements gathering, sprint planning, or when explaining features to stakeholders.

## Capabilities

### 1. Screen Wireframes
- Desktop/Web layouts (responsive breakpoints)
- Mobile app screens (iOS/Android)
- Tablet layouts
- Component-level mockups

### 2. Interaction Flows
- User journey diagrams
- Screen-to-screen navigation
- State changes (hover, active, disabled)
- Modal/popup overlays

### 3. ASCII Art Techniques

#### Box Drawing Characters
```
┌─┬─┐  ╔═╦═╗  ┏━┳━┓  ╭───╮
│ │ │  ║ ║ ║  ┃ ┃ ┃  │   │
├─┼─┤  ╠═╬═╣  ┣━╻━┫  │   │
│ │ │  ║ ║ ║  ┃ ┃ ┃  │   │
└─┴─┘  ╚═╩═╝  ┗━┻━┛  ╰───╯
```

#### UI Elements Library

**Buttons:**
```
[  Button  ]    [ Primary ]    [ ✓ Save ]    [ ✕ Cancel ]
                 ══════════
```

**Input Fields:**
```
┌──────────────────────────┐
│ Placeholder text...      │
└──────────────────────────┘

Email: [_____________________]
Password: [••••••••••••••••••]
```

**Checkboxes & Radio:**
```
☐ Unchecked    ☑ Checked    ◯ Radio off    ◉ Radio on
```

**Icons (Unicode):**
```
🏠 Home    👤 User    ⚙️ Settings    🔔 Notification
➕ Add     ✏️ Edit    🗑️ Delete      🔍 Search
📁 Folder  📄 File    💾 Save        ↩️ Back
⬆️ Up      ⬇️ Down    ◀️ Left        ▶️ Right
❤️ Like    💬 Comment  🔄 Share      ⭐ Star
```

**Progress & Loading:**
```
[████████░░░░░░░░] 50%
[▓▓▓▓▓▓▓▓▓▓░░░░░░] Loading...
◐ ◓ ◑ ◒ (spinning)
```

**Navigation:**
```
┌─────────────────────────────────────┐
│  🏠 Home  │  📊 Dashboard  │  ⚙️    │
└─────────────────────────────────────┘

[ Tab 1 ]  [ Tab 2 ]  [ Tab 3 ]
════════
```

**Cards:**
```
╭─────────────────────────────╮
│  📷 Image Area              │
│  ┌───────────────────────┐  │
│  │                       │  │
│  │      [Thumbnail]      │  │
│  │                       │  │
│  └───────────────────────┘  │
│                             │
│  Title Here                 │
│  Description text goes      │
│  here with details...       │
│                             │
│  [ Action ]  [ More ]       │
╰─────────────────────────────╯
```

**Tables:**
```
┌──────────┬──────────┬──────────┐
│  Header  │  Header  │  Header  │
├──────────┼──────────┼──────────┤
│  Cell    │  Cell    │  Cell    │
│  Cell    │  Cell    │  Cell    │
└──────────┴──────────┴──────────┘
```

**Mobile Phone Frame:**
```
╭─────────────────────────────╮
│ ▪️▪️▪️▪️▪️    9:41    📶 🔋 │
├─────────────────────────────┤
│                             │
│         Screen              │
│         Content             │
│                             │
├─────────────────────────────┤
│    🏠      🔍      👤       │
╰─────────────────────────────╯
```

**Desktop Browser Frame:**
```
┌─────────────────────────────────────────────────────┐
│ ● ● ●  │  ◀ ▶ ↻  │  🔒 https://app.example.com │ ≡ │
├─────────────────────────────────────────────────────┤
│                                                     │
│                  Page Content                       │
│                                                     │
└─────────────────────────────────────────────────────┘
```

### 4. Interaction Flow Notation

**Screen Flow:**
```
┌─────────┐         ┌─────────┐         ┌─────────┐
│ Login   │ ──────▶ │ Feed    │ ──────▶ │ Detail  │
└─────────┘  tap    └─────────┘  tap    └─────────┘
                         │
                         │ swipe
                         ▼
                    ┌─────────┐
                    │ Profile │
                    └─────────┘
```

**State Changes:**
```
[ Button ]  ───hover───▶  [ Button ]  ───click───▶  [ Button ]
  normal                   ════════                   Loading...
                            hover                       active
```

**Modal Overlay:**
```
┌─────────────────────────────────┐
│░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░│
│░░░┌───────────────────────┐░░░░░│
│░░░│      Modal Title      │░░░░░│
│░░░│                       │░░░░░│
│░░░│   Modal content...    │░░░░░│
│░░░│                       │░░░░░│
│░░░│  [ Cancel ] [ OK ]    │░░░░░│
│░░░└───────────────────────┘░░░░░│
│░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░│
└─────────────────────────────────┘
```

## Output Format

Wireframes should be saved to:
```
.project/wireframes/
├── README.md           # Overview & screen list
├── 01-login.md         # Login screen
├── 02-home.md          # Home screen
├── 03-detail.md        # Detail screen
├── flows.md            # Interaction flows
└── components.md       # Reusable components
```

Each screen file should include:
1. Screen name & purpose
2. ASCII wireframe (mobile + desktop if relevant)
3. Component descriptions
4. Interaction notes
5. Different states (empty, loading, error, success)

## Best Practices

1. **Consistency**: Use same box-drawing style throughout
2. **Annotations**: Add numbered callouts for complex areas
3. **Responsive**: Show mobile + desktop when relevant
4. **States**: Show different states (empty, loading, error, success)
5. **Accessibility**: Note contrast, touch targets, screen reader text
6. **Localization**: Support international characters properly

## Examples: Famous App Patterns

### Instagram-style Feed (Mobile)
```
╭─────────────────────────────╮
│ 📷 Instagram    💬    📤   │
├─────────────────────────────┤
│ ○ ○ ○ ○ ○ ○ ○ ○ ○          │  ← Stories
├─────────────────────────────┤
│ 👤 username          ⋯     │
│ ┌───────────────────────┐   │
│ │                       │   │
│ │      [Photo]          │   │
│ │                       │   │
│ └───────────────────────┘   │
│ ❤️ 💬 📤          🔖       │
│ 1,234 likes                 │
│ username Caption text...    │
│ View all 56 comments        │
├─────────────────────────────┤
│  🏠    🔍    ➕    ❤️   👤  │
╰─────────────────────────────╯
```

### Spotify-style Player (Mobile)
```
╭─────────────────────────────╮
│ ◂      Now Playing          │
├─────────────────────────────┤
│                             │
│   ┌───────────────────┐     │
│   │                   │     │
│   │   [Album Art]     │     │
│   │                   │     │
│   └───────────────────┘     │
│                             │
│       Song Title            │
│       Artist Name           │
│                             │
│   ●━━━━━━━━━━━━━━○━━━━━━━  │
│   1:23            3:45      │
│                             │
│     ⏮️    ▶️    ⏭️          │
│                             │
│   🔀      🔁      ❤️        │
│                             │
├─────────────────────────────┤
│  🏠    🔍    📚    ⚙️       │
╰─────────────────────────────╯
```

### Twitter/X-style Tweet (Desktop)
```
┌─────────────────────────────────────────────────────────────────────┐
│ ● ● ●  │  ◀ ▶ ↻  │  🔒 https://twitter.com                    │ ≡ │
├─────────────────────────────────────────────────────────────────────┤
│ ┌─────────┐                                                         │
│ │ 🏠 Home │ 🔍 Explore │ 🔔 Notif │ ✉️ Messages │ 👤 Profile       │
│ └─────────┘                                                         │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│  ╭─────────────────────────────────────────────────────────────╮   │
│  │ 👤  @username · 2h                                      ⋯   │   │
│  │                                                              │   │
│  │ This is a sample post that shows what a typical social      │   │
│  │ media post looks like in wireframe format. You can use      │   │
│  │ this pattern for any feed-based application.                │   │
│  │                                                              │   │
│  │ ┌────────────────────────────────────────────────────────┐  │   │
│  │ │                  [Embedded Media]                      │  │   │
│  │ └────────────────────────────────────────────────────────┘  │   │
│  │                                                              │   │
│  │   💬 24        🔄 156        ❤️ 1.2K        📤             │   │
│  ╰─────────────────────────────────────────────────────────────╯   │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘
```

### E-commerce Product Page (Desktop)
```
┌─────────────────────────────────────────────────────────────────────┐
│ ● ● ●  │  ◀ ▶ ↻  │  🔒 https://shop.example.com              │ ≡ │
├─────────────────────────────────────────────────────────────────────┤
│  🛒 SHOP        [Search...]                  🛒 Cart (3)  👤 Login │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│  ┌────────────────────────┐  ┌────────────────────────────────────┐│
│  │                        │  │ Product Name                       ││
│  │                        │  │ ⭐⭐⭐⭐☆ (124 reviews)             ││
│  │    [Product Image]     │  │                                    ││
│  │                        │  │ $99.99  ̶$̶1̶4̶9̶.̶9̶9̶  -33%             ││
│  │                        │  │                                    ││
│  │                        │  │ Color: ○ ○ ● ○                     ││
│  └────────────────────────┘  │ Size:  [S] [M] [L] [XL]            ││
│   ○  ○  ●  ○  ○              │                                    ││
│                              │ Qty:  [ − ]  1  [ + ]              ││
│                              │                                    ││
│                              │ ┌──────────────────────────────┐   ││
│                              │ │       🛒 ADD TO CART         │   ││
│                              │ │       ════════════════       │   ││
│                              │ └──────────────────────────────┘   ││
│                              │                                    ││
│                              │ ❤️ Add to Wishlist                 ││
│                              └────────────────────────────────────┘│
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘
```

### Dashboard Layout (Desktop)
```
┌─────────────────────────────────────────────────────────────────────┐
│ ● ● ●  │  ◀ ▶ ↻  │  🔒 https://dashboard.example.com         │ ≡ │
├─────────────────────────────────────────────────────────────────────┤
│ ┌──────────┐                                                        │
│ │ 📊 Logo  │                                            👤 Admin ▼ │
│ ├──────────┤────────────────────────────────────────────────────────┤
│ │          │  📈 Dashboard Overview                                 │
│ │ 🏠 Home  │                                                        │
│ │          │  ╭──────────╮ ╭──────────╮ ╭──────────╮ ╭──────────╮  │
│ │ 📊 Stats │  │ 📈 Sales │ │ 👥 Users │ │ 📦 Orders│ │ 💰 Revenue│  │
│ │          │  │  $12,345 │ │   1,234  │ │    567   │ │  $45,678 │  │
│ │ 👥 Users │  │  ↑ 12%   │ │  ↑ 8%    │ │  ↓ 3%    │ │  ↑ 15%   │  │
│ │          │  ╰──────────╯ ╰──────────╯ ╰──────────╯ ╰──────────╯  │
│ │ ⚙️ Config│                                                        │
│ │          │  ╭────────────────────────────────────────────────────╮│
│ │          │  │                                                    ││
│ │          │  │              [Line Chart - Sales Trend]            ││
│ │          │  │                                                    ││
│ │          │  ╰────────────────────────────────────────────────────╯│
│ │          │                                                        │
│ └──────────┘                                                        │
└─────────────────────────────────────────────────────────────────────┘
```

## Related Skills

- `frontend-design` - Implementation after wireframe approval
- `business-analysis` - Requirements that inform wireframes
- `react-expert` - React component implementation
- `swift-expert` - iOS native implementation
