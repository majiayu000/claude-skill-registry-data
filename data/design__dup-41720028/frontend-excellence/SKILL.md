---
name: "Frontend Excellence"
description: "Design systems, component libraries, responsive UI/UX, accessibility. Build premium interfaces that enterprise clients expect."
enabled: true
---

# FRONTEND EXCELLENCE SKILL
## Premium UI/UX Architecture for Enterprise SaaS

### 🎨 DESIGN SYSTEM PHILOSOPHY

**Rhino Brand Colors**
- Primary: Teal (#208090) - Trust, professionalism, energy
- Secondary: Slate Gray (#2F3F48) - Stability, data-driven
- Accent: Deep Red (#C01530) - Urgency, attention, risk highlighting
- Neutral: Cool Grays (#F5F5F5, #E0E0E0, #999999)
- Status: Green (success #22C55E), Amber (warning #F59E0B), Red (error #EF4444)

**Typography Hierarchy**
- H1 (32px): Page titles, major sections
- H2 (24px): Section headers
- H3 (18px): Subsection headers
- H4 (16px): Component labels
- Body (14px): Primary content
- Caption (12px): Metadata, timestamps, help text
- Monospace (13px): Code, calculations, financial values

**Spacing System** (8px grid)
- xs: 4px (tight spacing)
- sm: 8px (default gap)
- md: 16px (section spacing)
- lg: 24px (major separation)
- xl: 32px (layout sections)

### 🔧 CORE COMPONENTS

**Form Components**
- Text Input: Single line, validation states, placeholder text
- Textarea: Multi-line with char count, min/max
- Select Dropdown: Native + custom with search
- Checkbox: Single and grouped options
- Radio: Mutually exclusive selection
- Toggle Switch: On/off states with labels
- Date Picker: Calendar interface, range selection
- Number Input: Increment/decrement, min/max, precision
- File Upload: Drag-drop, file type validation

**Data Display**
- Table: Sortable columns, pagination, row selection, sticky header
- Card: Container with padding, borders, shadow on hover
- Modal: Center dialog, backdrop overlay, focus trap
- Tooltip: Hover-triggered help text
- Badge: Status indicators, counts, labels
- Progress Bar: Linear progress with percentage
- Alert: Error, warning, success, info messages

**Navigation**
- Navbar: Logo, menu items, user dropdown, search
- Sidebar: Collapsible navigation, active state highlighting
- Breadcrumbs: Path navigation with links
- Tabs: Horizontal tab navigation
- Pagination: Previous/next, page numbers, jump to page

**Financial/Data Specific**
- Number Display: Formatted currency ($M, thousands separator)
- Percentage Display: With trend indicators (up/down arrows)
- Chart Container: Responsive chart wrapper with legend
- Data Row: Key-value pair with units
- Comparison Widget: Side-by-side metric comparison

### ✨ MICRO-INTERACTIONS & ANIMATIONS

**Transitions**
- Button hover: Subtle background color shift (150ms ease)
- Link hover: Color change + underline fade in
- Form focus: Border color change + shadow glow
- Modal entrance: Fade in + slight scale up
- List item: Slide in on first load

**Loading States**
- Skeleton screens: Placeholder shapes while loading
- Progress indicators: Circular spinner for indeterminate
- Percentage progress: Bar for determinate loads
- Pulsing animation: Breathing effect on loading states

**Feedback**
- Toast notifications: Bottom-right corner, auto-dismiss
- Loading cursor: Visual feedback during processing
- Disabled state: 50% opacity, cursor-not-allowed
- Error state: Red border, icon, help text

### 📱 RESPONSIVE DESIGN

**Breakpoints**
- Mobile: < 640px (single column, stacked layout)
- Tablet: 640px - 1024px (two columns, flexible sidebar)
- Desktop: > 1024px (three columns, full navigation)

**Mobile Optimizations**
- Touch targets: Minimum 44px × 44px
- Simplified forms: Fewer fields per screen
- Bottom sheet modals: Easier thumb reach
- Vertical scrolling: Avoid horizontal where possible
- Font sizes: 16px+ for readable mobile

### ♿ ACCESSIBILITY (WCAG 2.1 AA)

**Color & Contrast**
- Text contrast: 4.5:1 for normal text, 3:1 for large text
- Don't rely on color alone: Use icons + text
- Color blindness: Avoid red-green only distinction

**Keyboard Navigation**
- Tab order: Logical left-to-right, top-to-bottom
- Focus indicators: Visible 2px outline around focused element
- Escape key: Closes modals, dropdowns
- Enter key: Submits forms, triggers actions

**Screen Readers**
- Semantic HTML: Use <button>, <nav>, <article>, not <div>
- ARIA labels: aria-label for icon buttons
- ARIA live regions: aria-live="polite" for dynamic content
- Form labels: <label> with proper for= attribute
- Link text: Descriptive "Edit Project" not "Click here"

**Motion & Animation**
- prefers-reduced-motion: Respect user's system setting
- No autoplaying videos: User control always
- Blinking/flashing: Avoid, or < 3 Hz if necessary

### 🎯 STATE MANAGEMENT PATTERNS

**React Component Structure**
```
App
├── Layout
│   ├── Navbar
│   ├── Sidebar
│   └── MainContent
│       ├── Dashboard
│       ├── ProjectList
│       └── DetailView
└── Modals
    ├── CreateProject
    └── EditMetadata
```

**Data Flow**
- Global state: Redux/Zustand for user, auth, app settings
- Page state: Local component state for UI toggles
- Server state: React Query for API data caching
- Form state: React Hook Form for form management

**Context Usage**
- ThemeContext: Dark/light mode provider
- AuthContext: User, permissions, authentication
- NotificationContext: Toast alerts, messages

### 🚀 PERFORMANCE OPTIMIZATION

**Rendering**
- Code splitting: Lazy load routes with React.lazy()
- Memoization: React.memo() for expensive components
- useMemo: Cache derived calculations
- useCallback: Stable function references

**Loading**
- Lighthouse: Target 90+ score
- First Contentful Paint (FCP): < 1.5s
- Largest Contentful Paint (LCP): < 2.5s
- Cumulative Layout Shift (CLS): < 0.1

**Bundle Size**
- Tree shaking: Remove unused code
- Image optimization: WebP format, responsive sizes
- CSS purging: Remove unused styles (Tailwind)
- Code splitting: Separate vendor bundles

### 🎭 DARK/LIGHT MODE

**Theme Implementation**
- CSS variables: --color-bg, --color-text, --color-border
- Context provider: ThemeContext wraps app
- LocalStorage persistence: Remember user preference
- System preference detection: prefers-color-scheme media query
- Smooth transition: 200ms fade between themes

**Color Mapping**
- Light mode: Light backgrounds, dark text
- Dark mode: Dark backgrounds, light text
- Both: Same semantic colors, different hex values
```