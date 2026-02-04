---
name: docusaurus-initializer
version: 1.0
description: This skill should be used when initializing a new Docusaurus documentation site with TypeScript and custom dark mode theme. Provides basic setup with pnpm, theme installation, and configuration templates for technical documentation.
---

# Docusaurus Initializer

Initialize and configure Docusaurus documentation sites with TypeScript and custom dark mode theme.

## What This Skill Does

1. **Project Initialization** - Scaffold new Docusaurus projects with pnpm and TypeScript
2. **Custom Theme Installation** - Apply dark mode optimized theme for technical content
3. **Configuration Templates** - Provide annotated configuration files for quick setup

## When to Use This Skill

Initialize a new Docusaurus site when:
- Starting a new documentation project
- Need a dark mode optimized theme for technical content
- Want TypeScript setup with proper configuration
- Prefer pnpm as the package manager

## How to Use This Skill

Follow the **4-step initialization** workflow:

### Step 1: Initialize Docusaurus Project with pnpm

Create a new Docusaurus project:

```bash
pnpm create docusaurus@latest my-website classic --typescript
cd my-website
```

This creates:
```
my-website/
├── docs/                    # Documentation files
├── blog/                    # Blog posts
├── src/                     # Custom pages
├── static/                  # Static assets
├── docusaurus.config.ts     # Main configuration
├── sidebars.ts             # Navigation structure
└── package.json            # Dependencies
```

Verify installation:

```bash
pnpm install
pnpm run build
```

For detailed setup guidance, see `references/initialization-guide.md`.

### Step 2: Install Custom Theme

Apply the dark mode optimized custom theme:

```bash
bash scripts/install-robotics-theme.sh
```

This:
- Copies custom CSS from `assets/robotics-theme/custom.css`
- Creates `src/css/` directory if needed
- Applies theme to development server

### Step 3: Configure Site Settings

Copy the configuration template:

```bash
cp assets/config-templates/docusaurus.config.template.ts docusaurus.config.ts
```

Edit `docusaurus.config.ts` with your site details:

```typescript
export default {
  title: 'Your Site Title',           // Change this
  url: 'https://example.com',        // Your domain
  baseUrl: '/',                       // / for root, /project/ for subdirectory
  favicon: 'img/favicon.ico',        // Your favicon
  // ... other config
};
```

Key configuration options:

| Option | Purpose | Example |
|--------|---------|---------|
| `title` | Browser tab title | "My Documentation" |
| `url` | Production domain | "https://docs.example.com" |
| `baseUrl` | URL path | "/" or "/docs/" |
| `favicon` | Tab icon | "img/favicon.ico" |

For detailed configuration help, see `references/theming-guide.md`.

### Step 4: Test and Verify

Build and test locally:

```bash
# Type check
pnpm run typecheck

# Build production bundle
pnpm run build

# Start development server
pnpm run start
```

Expected results:
- ✅ Build completes in < 30 seconds
- ✅ Development server starts on http://localhost:3000
- ✅ Dark theme applied correctly
- ✅ All pages load without errors

## Bundled Resources

### Scripts

- `scripts/install-robotics-theme.sh` - Theme installer script

### Theme

- `assets/robotics-theme/custom.css` - Dark mode optimized stylesheet with:
  - Color palette for dark mode
  - Typography configuration
  - Code block styling
  - Table and list formatting
  - Responsive design
  - Admonition styles (note, warning, danger)

### Configuration Template

- `assets/config-templates/docusaurus.config.template.ts` - Fully annotated configuration with:
  - Required fields (title, url, baseUrl)
  - Optional metadata
  - Theme configuration
  - Navbar and footer setup
  - Search configuration
  - Deployment target examples

### Reference Guides

- `references/initialization-guide.md` - Complete Docusaurus setup walkthrough
- `references/theming-guide.md` - Custom CSS and theme customization
- `references/troubleshooting-init.md` - Common issues and solutions

## Customization

### Change Color Scheme

Edit `src/css/custom.css`:

```css
:root {
  --primary-color: #3b82f6;      /* Change to your brand color */
  --primary-dark: #1e40af;
  --primary-light: #60a5fa;
}
```

Then rebuild:

```bash
pnpm run clear
pnpm run start
```

### Add Navigation Links

Edit `docusaurus.config.ts` navbar section:

```typescript
navbar: {
  items: [
    { to: '/docs/intro', label: 'Docs', position: 'left' },
    { href: 'https://github.com', label: 'GitHub', position: 'right' },
  ],
}
```

### Enable Search

Option 1: Local search (no setup needed)

```typescript
plugins: [
  [
    require.resolve("@easyops-cn/docusaurus-search-local"),
    { hashed: true },
  ],
],
```

Option 2: Algolia DocSearch (requires API key)

```typescript
algolia: {
  appId: 'YOUR_APP_ID',
  apiKey: 'YOUR_API_KEY',
  indexName: 'YOUR_INDEX',
},
```

## Next Steps

After initialization:

1. **Add Content** - Create documentation files in `docs/`
2. **Customize Navigation** - Update `sidebars.ts` for your structure
3. **Adjust Theme** - Modify `src/css/custom.css` for your branding
4. **Deploy** - Use `docusaurus-deployer` skill to publish to GitHub Pages

## Troubleshooting

Common issues:

**Port 3000 already in use**
```bash
pnpm start -- --port 3001
```

**Changes not reflecting**
```bash
pnpm run clear
pnpm start
```

**Build fails**
```bash
pnpm run typecheck        # Check for TypeScript errors
rm -rf node_modules       # Reinstall if corrupted
pnpm install
pnpm run build
```

For more solutions, see `references/troubleshooting-init.md`.

## Performance Targets

- **Initialization time**: < 2 minutes
- **Development server start**: < 10 seconds
- **Build time**: < 30 seconds
- **Page load**: < 3 seconds

## Tools Used

- **Node.js** (v18+) - JavaScript runtime
- **pnpm** (v8+) - Fast package manager
- **TypeScript** (v5+) - Type safety
- **Docusaurus** (v3.x) - Static site generator
- **Bash** - Script execution

## Integration with docusaurus-deployer

This skill prepares your site for deployment with `docusaurus-deployer`:

1. Initialize with this skill
2. Add your content
3. Use `docusaurus-deployer` to publish to GitHub Pages

Workflow:
```
docusaurus-initializer → Add content → docusaurus-deployer
        ↓                                       ↓
    Setup + Theme                        Live on GitHub Pages
```

## Resources

- [Docusaurus Official Docs](https://docusaurus.io/docs)
- [MDX Documentation](https://mdxjs.com/)
- See bundled reference guides for detailed help
