---
name: ui-design-brain-cursor-skill
description: Cursor skill that gives AI agents production-grade UI component knowledge with best practices, layout patterns, and design-system conventions for 60+ interface components
triggers:
  - "build a UI component following best practices"
  - "create a settings page with proper layout"
  - "design a dashboard with modern patterns"
  - "generate production-ready interface code"
  - "implement a data table with proper structure"
  - "build a form with accessibility standards"
  - "create a navigation component following conventions"
  - "design a modal dialog with best practices"
---

# UI Design Brain Cursor Skill

> Skill by [ara.so](https://ara.so) — Design Skills collection.

This skill gives Cursor AI real UI component knowledge — curated best practices, proven layout patterns, and design-system conventions for 60+ interface components — so it generates production-grade UI instead of generic output.

## What This Skill Provides

**Component Knowledge Base**: 60 production-ready component patterns sourced from [component.gallery](https://component.gallery) with:

- **Best practices** per component (accessibility, sizing, behavior)
- **Common layouts** — proven arrangements
- **Aliases** — recognizes components by any name
- **Anti-patterns** — specific things to avoid
- **Design philosophy** — modern, minimal, SaaS-quality standards

**Design Directions**: 5 built-in style presets:
- Modern SaaS (default) — clean, spacious, professional
- Apple-level Minimal — ultra-clean with generous whitespace
- Enterprise/Corporate — information-dense, keyboard-navigable
- Creative/Portfolio — bold, expressive, editorial
- Data Dashboard — optimized for scannability

## Installation

### Option A: Personal Skill (All Projects)

```bash
git clone https://github.com/carmahhawwari/ui-design-brain.git \
  ~/.cursor/skills/ui-design-brain
```

### Option B: Project Skill (Shared with Team)

```bash
git clone https://github.com/carmahhawwari/ui-design-brain.git \
  .cursor/skills/ui-design-brain
```

### Option C: Manual Installation

Copy `SKILL.md` and `components.md` into:
- `~/.cursor/skills/ui-design-brain/` (personal), or
- `.cursor/skills/ui-design-brain/` (project)

## How to Use

Once installed, the skill activates automatically when you ask Cursor to build UI. **No explicit reference needed.**

### Basic Usage

Ask naturally — the skill identifies components and applies best practices:

```
Build a settings page with sidebar navigation, toggle preferences, and profile section
```

```
Create a data table with search, filters, sortable columns, and pagination
```

```
Design a SaaS dashboard with KPI cards, chart area, and activity feed
```

### Requesting Specific Design Directions

```
Build a pricing page with Apple-minimal aesthetic
```

```
Create an enterprise dashboard with dense information layout
```

```
Design a creative portfolio hero section
```

## Component Coverage (60 Components)

| Category | Components |
|----------|-----------|
| **Input** | Button, Checkbox, Radio button, Text input, Textarea, Select, Combobox, Date input, Datepicker, File upload, Search input, Slider, Toggle, Color picker, Rich text editor |
| **Navigation** | Navigation, Breadcrumbs, Tabs, Pagination, Stepper, Skip link, Tree view |
| **Layout** | Card, Stack, Separator, Header, Footer, Drawer, Modal, Popover |
| **Content** | Heading, Image, Video, Quote, List, Table, Hero |
| **Feedback** | Alert, Toast, Progress bar, Progress indicator, Spinner, Skeleton, Empty state, Tooltip |
| **Data** | Badge, Avatar, Rating, Icon |
| **Forms** | Form, Fieldset, Label, Button group, Segmented control |
| **Advanced** | Accordion, Carousel, Dropdown menu, Visually hidden |

## Key Patterns & Best Practices

### Accessibility-First Approach

The skill enforces:

```tsx
// Modal — focus trapping
function Modal({ isOpen, onClose, children }) {
  const firstFocusableRef = useRef(null);
  
  useEffect(() => {
    if (isOpen) {
      firstFocusableRef.current?.focus();
      // Trap focus within modal
      document.body.style.overflow = 'hidden';
    }
    return () => {
      document.body.style.overflow = '';
    };
  }, [isOpen]);

  return (
    <div 
      role="dialog" 
      aria-modal="true"
      className={isOpen ? 'modal-open' : 'modal-closed'}
    >
      <button ref={firstFocusableRef} onClick={onClose} aria-label="Close">
        ×
      </button>
      {children}
    </div>
  );
}
```

```tsx
// Button — accessible states
<button
  type="button"
  disabled={isLoading}
  aria-busy={isLoading}
  aria-label={isLoading ? 'Loading...' : 'Submit'}
  className="btn-primary"
>
  {isLoading ? <Spinner /> : 'Submit'}
</button>
```

### Component Composition Patterns

**Data Table with Full Features**:

```tsx
function DataTable({ data, columns }) {
  const [sortConfig, setSortConfig] = useState({ key: null, direction: 'asc' });
  const [filters, setFilters] = useState({});
  const [page, setPage] = useState(1);
  const [searchQuery, setSearchQuery] = useState('');

  const filteredData = useMemo(() => {
    return data
      .filter(row => 
        Object.entries(filters).every(([key, value]) => 
          !value || row[key] === value
        )
      )
      .filter(row =>
        !searchQuery || 
        Object.values(row).some(val => 
          String(val).toLowerCase().includes(searchQuery.toLowerCase())
        )
      );
  }, [data, filters, searchQuery]);

  const sortedData = useMemo(() => {
    if (!sortConfig.key) return filteredData;
    return [...filteredData].sort((a, b) => {
      if (a[sortConfig.key] < b[sortConfig.key]) {
        return sortConfig.direction === 'asc' ? -1 : 1;
      }
      if (a[sortConfig.key] > b[sortConfig.key]) {
        return sortConfig.direction === 'asc' ? 1 : -1;
      }
      return 0;
    });
  }, [filteredData, sortConfig]);

  const paginatedData = sortedData.slice(
    (page - 1) * PAGE_SIZE,
    page * PAGE_SIZE
  );

  return (
    <div className="data-table-container">
      <div className="table-controls">
        <SearchInput 
          value={searchQuery}
          onChange={setSearchQuery}
          placeholder="Search..."
        />
        <FilterBar filters={filters} onChange={setFilters} />
      </div>
      
      <table role="table" aria-label="Data table">
        <thead>
          <tr>
            {columns.map(col => (
              <th 
                key={col.key}
                onClick={() => handleSort(col.key)}
                aria-sort={sortConfig.key === col.key ? sortConfig.direction : 'none'}
              >
                {col.label}
                <SortIcon direction={sortConfig.key === col.key ? sortConfig.direction : null} />
              </th>
            ))}
          </tr>
        </thead>
        <tbody>
          {paginatedData.map(row => (
            <tr key={row.id}>
              {columns.map(col => (
                <td key={col.key}>{row[col.key]}</td>
              ))}
            </tr>
          ))}
        </tbody>
      </table>
      
      <Pagination
        currentPage={page}
        totalPages={Math.ceil(sortedData.length / PAGE_SIZE)}
        onPageChange={setPage}
      />
    </div>
  );
}
```

**Settings Page Layout**:

```tsx
function SettingsPage() {
  return (
    <div className="settings-layout">
      <aside className="settings-sidebar">
        <nav aria-label="Settings navigation">
          <a href="#profile" className="active">Profile</a>
          <a href="#security">Security</a>
          <a href="#notifications">Notifications</a>
          <a href="#billing">Billing</a>
        </nav>
      </aside>
      
      <main className="settings-content">
        <section id="profile">
          <Heading level={2}>Profile Settings</Heading>
          
          <Form onSubmit={handleSubmit}>
            <Fieldset legend="Personal Information">
              <Label htmlFor="name">Full Name</Label>
              <TextInput id="name" name="name" required />
              
              <Label htmlFor="email">Email</Label>
              <TextInput id="email" type="email" name="email" required />
              
              <Label htmlFor="avatar">Profile Picture</Label>
              <FileUpload 
                id="avatar" 
                accept="image/*"
                maxSize={5 * 1024 * 1024}
              />
            </Fieldset>
            
            <Fieldset legend="Preferences">
              <Toggle
                id="newsletter"
                label="Subscribe to newsletter"
                checked={preferences.newsletter}
                onChange={handleToggle}
              />
              
              <Toggle
                id="dark-mode"
                label="Enable dark mode"
                checked={preferences.darkMode}
                onChange={handleToggle}
              />
            </Fieldset>
            
            <Button type="submit" variant="primary">
              Save Changes
            </Button>
          </Form>
        </section>
      </main>
    </div>
  );
}
```

**Dashboard with KPIs**:

```tsx
function Dashboard() {
  return (
    <div className="dashboard-grid">
      <header className="dashboard-header">
        <Heading level={1}>Analytics Dashboard</Heading>
        <DateRangePicker onChange={handleDateChange} />
      </header>
      
      <section className="kpi-cards">
        <Card>
          <div className="kpi-value">$24,532</div>
          <div className="kpi-label">Revenue</div>
          <div className="kpi-change positive">+12.5%</div>
        </Card>
        
        <Card>
          <div className="kpi-value">1,243</div>
          <div className="kpi-label">New Users</div>
          <div className="kpi-change positive">+8.2%</div>
        </Card>
        
        <Card>
          <div className="kpi-value">89.2%</div>
          <div className="kpi-label">Conversion Rate</div>
          <div className="kpi-change negative">-2.1%</div>
        </Card>
      </section>
      
      <Card className="chart-area">
        <Heading level={2}>Revenue Trend</Heading>
        <LineChart data={revenueData} />
      </Card>
      
      <aside className="activity-feed">
        <Heading level={2}>Recent Activity</Heading>
        <List>
          {activities.map(activity => (
            <li key={activity.id}>
              <Avatar src={activity.user.avatar} size="sm" />
              <div>
                <div className="activity-text">{activity.text}</div>
                <time className="activity-time">{activity.timestamp}</time>
              </div>
            </li>
          ))}
        </List>
      </aside>
    </div>
  );
}
```

## Anti-Patterns to Avoid

The skill enforces avoidance of:

1. **Generic div soup** — Use semantic HTML (`<nav>`, `<main>`, `<article>`)
2. **Missing ARIA labels** — All interactive elements must be labeled
3. **Non-keyboard-accessible custom controls** — Handle Enter, Space, Arrow keys
4. **Hardcoded breakpoints without mobile-first** — Use responsive design
5. **Loading states without feedback** — Always show spinners/skeletons
6. **Forms without validation feedback** — Show errors inline
7. **Modals without focus management** — Trap and restore focus
8. **Tables without sortable headers** — Data tables should be interactive
9. **Missing empty states** — Handle zero-data scenarios gracefully
10. **Inconsistent spacing** — Use design token system

## Design System Tokens

The skill assumes you have CSS variables or a token system:

```css
/* Spacing scale */
--space-xs: 0.25rem;   /* 4px */
--space-sm: 0.5rem;    /* 8px */
--space-md: 1rem;      /* 16px */
--space-lg: 1.5rem;    /* 24px */
--space-xl: 2rem;      /* 32px */
--space-2xl: 3rem;     /* 48px */

/* Typography scale */
--text-xs: 0.75rem;    /* 12px */
--text-sm: 0.875rem;   /* 14px */
--text-base: 1rem;     /* 16px */
--text-lg: 1.125rem;   /* 18px */
--text-xl: 1.25rem;    /* 20px */
--text-2xl: 1.5rem;    /* 24px */
--text-3xl: 1.875rem;  /* 30px */

/* Colors */
--color-primary: #3b82f6;
--color-success: #10b981;
--color-warning: #f59e0b;
--color-error: #ef4444;
--color-neutral-50: #f9fafb;
--color-neutral-900: #111827;

/* Border radius */
--radius-sm: 0.25rem;
--radius-md: 0.375rem;
--radius-lg: 0.5rem;
--radius-full: 9999px;
```

## Troubleshooting

### Skill Not Activating

1. **Check installation path**:
   ```bash
   ls ~/.cursor/skills/ui-design-brain/
   # Should show: SKILL.md, components.md, README.md
   ```

2. **Restart Cursor** after installation

3. **Verify skill is loaded** — check Cursor's skill settings

### Generic Output Still Generated

**Be explicit in your request**:
```
Build a production-ready settings page with proper accessibility
```

Instead of:
```
Make a settings page
```

### Missing Component Knowledge

If a component isn't covered, reference it explicitly:
```
Build a notification center using toast patterns and empty state best practices
```

### Style Conflicts

If generated styles conflict with your design system:
```
Build this form using our existing Tailwind classes and design tokens
```

## Advanced Usage

### Custom Component Extensions

Ask the agent to extend existing patterns:

```
Create a multi-step wizard using stepper, form, and button group patterns with validation
```

```
Build a kanban board using card, drag-and-drop, and empty state patterns
```

### Framework-Specific Generation

Specify your stack:

```
Build a Next.js server component data table with React Server Actions for mutations
```

```
Create a Vue 3 composition API modal with TypeScript and proper teleport usage
```

### Performance Optimization

```
Generate a virtualized table for 10,000+ rows using windowing techniques
```

```
Create a lazy-loaded image gallery with progressive enhancement
```

## File Structure

```
ui-design-brain/
├── SKILL.md          # Main AI agent instructions
├── components.md     # 60-component reference
├── LICENSE.txt       # MIT license
└── README.md         # Human documentation
```

## Contributing

To extend component coverage:

1. Edit `components.md` following existing format:
   - Component name
   - Aliases
   - Description
   - Best practices (bullet list)
   - Common layouts (with code examples)

2. Add to quick reference in `SKILL.md` if commonly used

3. Keep total lines under 500 in `SKILL.md`

## License

MIT — See LICENSE.txt

Component data sourced from [component.gallery](https://component.gallery)

---

**Quick Reference Card**

| Task | Natural Prompt |
|------|---------------|
| Settings page | "Build settings page with sidebar nav and toggles" |
| Data table | "Create sortable table with search and filters" |
| Dashboard | "Design SaaS dashboard with KPIs and chart area" |
| Form | "Build multi-step form with validation" |
| Modal | "Create accessible modal dialog" |
| Navigation | "Build responsive header with dropdown menu" |
