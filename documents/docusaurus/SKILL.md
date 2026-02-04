---
name: docusaurus
description: Manages Docusaurus documentation sites. Use this skill when the user wants to create a new Docusaurus project, start/stop the development server, or perform common Docusaurus operations.
---

# Docusaurus Site Management Skill

This skill helps you manage Docusaurus documentation sites including scaffolding, development server management, and common operations.

## When to use this skill

Use this skill when the user asks to:
- Create or scaffold a new Docusaurus project
- Start the Docusaurus development server
- Stop the Docusaurus development server
- Build or deploy a Docusaurus site
- Work with Docusaurus configuration

## Prerequisites

Before using this skill, verify:
- Node.js version 18.0 or higher is installed
- npm or yarn is available

Check with: `node --version && npm --version`

## Available Scripts

This skill includes the following helper scripts:

### 1. scaffold.sh - Create a new Docusaurus project

**Usage:**
```bash
bash .claude/skills/docusaurus/scaffold.sh <project-name> [typescript]
```

**Examples:**
```bash
# Create a JavaScript project
bash .claude/skills/docusaurus/scaffold.sh my-docs-site

# Create a TypeScript project
bash .claude/skills/docusaurus/scaffold.sh my-docs-site typescript
```

**What it does:**
- Creates a new Docusaurus project with the classic template
- Optionally adds TypeScript support
- Installs dependencies
- Shows the created project structure

**Project structure created:**
```
<project-name>/
├── blog/              # Blog posts
├── docs/              # Documentation pages
├── src/
│   ├── components/    # React components
│   ├── css/          # CSS styles
│   └── pages/        # Static pages
├── static/           # Static assets (images, etc.)
├── docusaurus.config.js  # Main configuration
├── package.json
└── sidebars.js       # Sidebar navigation config
```

### 2. start-dev.sh - Start the development server

**Usage:**
```bash
bash .claude/skills/docusaurus/start-dev.sh [project-dir] [options]
```

**Examples:**
```bash
# Start in current directory on default port (3000)
bash .claude/skills/docusaurus/start-dev.sh

# Start in specific project directory
bash .claude/skills/docusaurus/start-dev.sh ./my-docs-site

# Start on custom port
bash .claude/skills/docusaurus/start-dev.sh . --port 9000

# Start with network access
bash .claude/skills/docusaurus/start-dev.sh . --host 0.0.0.0

# Combine options
bash .claude/skills/docusaurus/start-dev.sh ./my-docs-site "--port 9000 --host 0.0.0.0"
```

**What it does:**
- Navigates to the project directory
- Starts the Docusaurus development server
- Enables hot-reload (automatic refresh on file changes)
- Opens the site at http://localhost:3000 (or specified port)

**Note:** Use the Bash tool with `run_in_background: true` to start the server in the background.

### 3. stop-dev.sh - Stop the development server

**Usage:**
```bash
bash .claude/skills/docusaurus/stop-dev.sh [port]
```

**Examples:**
```bash
# Stop server on default port (3000)
bash .claude/skills/docusaurus/stop-dev.sh

# Stop server on specific port
bash .claude/skills/docusaurus/stop-dev.sh 9000
```

**What it does:**
- Finds the Docusaurus/Node process running on the specified port
- Gracefully stops the development server
- Verifies the server has stopped

**Alternative methods:**
- If server is running in foreground: Press `Ctrl+C`
- If server has a known shell_id: Use the `KillShell` tool
- Manual kill: `pkill -f "docusaurus start"`

## Common Workflows

### First time setup
```bash
# 1. Create project
bash .claude/skills/docusaurus/scaffold.sh tep-oncology-site

# 2. Navigate to project
cd tep-oncology-site

# 3. Start development server
bash .claude/skills/docusaurus/start-dev.sh
```

### Daily development
```bash
# Start server
bash .claude/skills/docusaurus/start-dev.sh

# Make changes to files in docs/, blog/, src/
# Changes will hot-reload automatically

# Stop server when done
bash .claude/skills/docusaurus/stop-dev.sh
```

### Build and deploy
```bash
# Build for production
npm run build

# Test production build locally
npm run serve

# Deploy (if configured)
npm run deploy
```

## Additional Commands

Beyond the provided scripts, you can use these npm commands directly:

**Build production version:**
```bash
npm run build
```

**Serve production build locally:**
```bash
npm run serve
```

**Clear cache (useful for troubleshooting):**
```bash
npm run clear
```

**Deploy (requires configuration in docusaurus.config.js):**
```bash
npm run deploy
```

## Configuration

The main configuration file is `docusaurus.config.js` in the project root. Key settings include:

- **Site metadata**: title, tagline, URL
- **Theme configuration**: colors, fonts, navbar, footer
- **Plugins**: additional functionality
- **Deployment settings**: GitHub Pages, etc.

## Content Management

**Documentation pages**: Add Markdown files to `docs/`
- Supports MDX (Markdown + React components)
- Frontmatter for metadata
- Automatic sidebar generation via `sidebars.js`

**Blog posts**: Add Markdown files to `blog/`
- Filename format: `YYYY-MM-DD-title.md`
- Supports authors, tags, and categories

**Custom pages**: Create React components in `src/pages/`
- Routes automatically generated from filename
- Full React capabilities

**Static assets**: Place in `static/`
- Images, PDFs, fonts, etc.
- Accessible at `/filename` in production

## Troubleshooting

**Port already in use:**
```bash
bash .claude/skills/docusaurus/start-dev.sh . --port 3001
```

**Cache issues:**
```bash
npm run clear
rm -rf node_modules .docusaurus
npm install
```

**Missing dependencies:**
```bash
npm install
```

**Build errors:**
```bash
npm run clear
npm run build
```

## Tips

- **Hot reload**: Changes reflect instantly without restart
- **Markdown features**: Docusaurus supports tabs, code blocks with highlighting, admonitions, and more
- **React components**: Mix React components directly in Markdown files (MDX)
- **Versioning**: Built-in support for versioned documentation
- **i18n**: Built-in internationalization support
- **Search**: Can integrate with Algolia DocSearch or local search

## Resources

- Official docs: https://docusaurus.io/docs
- GitHub repo: https://github.com/facebook/docusaurus
- Community plugins: https://docusaurus.io/community/resources
