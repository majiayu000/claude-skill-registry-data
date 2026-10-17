---
name: vibefigma-figma-to-react
description: Convert Figma designs to production-ready React components with Tailwind CSS using VibeFigma
triggers:
  - convert figma design to react
  - generate react component from figma
  - import figma file as react code
  - transform figma to tailwind react
  - extract react components from figma
  - figma to code conversion
  - parse figma design into typescript
  - create react component from figma url
---

# VibeFigma - Figma to React Converter

> Skill by [ara.so](https://ara.so) — Design Skills collection.

VibeFigma is an open-source tool that transforms Figma designs into production-ready React components with Tailwind CSS. It uses the official Figma API to extract designs and generate clean, maintainable TypeScript/React code.

## Installation

VibeFigma can be used without installation via npx, or installed globally/locally:

```bash
# Run directly (recommended)
npx vibefigma

# Install globally
npm install -g vibefigma

# Install as dev dependency
npm install --save-dev vibefigma
```

## Prerequisites

You need a Figma Personal Access Token:

1. Go to https://www.figma.com/settings
2. Scroll to **Personal Access Tokens**
3. Click **Generate new token**
4. Copy the token and store it securely

Set the token as an environment variable:

```bash
export FIGMA_TOKEN=your_figma_access_token
```

Or create a `.env` file:

```env
FIGMA_TOKEN=your_figma_access_token
```

## CLI Usage

### Interactive Mode (Easiest)

```bash
npx vibefigma --interactive
```

The CLI will prompt you for:
- Figma URL
- Access token (if not in env)
- Output paths

### Direct Command

```bash
# Basic usage
npx vibefigma "https://www.figma.com/design/FILE_ID/FILE_NAME?node-id=NODE_ID"

# With explicit token
npx vibefigma "https://www.figma.com/design/FILE_ID/FILE_NAME?node-id=NODE_ID" --token YOUR_TOKEN

# Custom output paths
npx vibefigma "https://www.figma.com/design/FILE_ID/FILE_NAME?node-id=NODE_ID" \
  --component ./src/components/Hero.tsx \
  --assets ./public/images

# Force overwrite without confirmation
npx vibefigma "https://www.figma.com/design/FILE_ID/FILE_NAME?node-id=NODE_ID" --force
```

### Common Options

```bash
# Disable Tailwind CSS (generate regular CSS)
npx vibefigma [url] --no-tailwind

# Optimize generated code
npx vibefigma [url] --optimize

# Use AI code cleaner (requires GOOGLE_GENERATIVE_AI_API_KEY)
npx vibefigma [url] --clean

# Disable responsive design
npx vibefigma [url] --no-responsive

# Don't include font imports
npx vibefigma [url] --no-fonts

# Disable absolute positioning
npx vibefigma [url] --no-absolute
```

### Full CLI Options

```
Options:
  -V, --version                 Output version
  -t, --token <token>           Figma access token (overrides FIGMA_TOKEN)
  -u, --url <url>               Figma file/node URL
  -c, --component <path>        Component output path (default: ./src/components/[ComponentName].tsx)
  -a, --assets <dir>            Assets directory (default: ./public)
  --no-tailwind                 Disable Tailwind CSS
  --optimize                    Optimize components
  --clean                       Use AI code cleaner
  --no-classes                  Don't generate CSS classes
  --no-absolute                 Don't use absolute positioning
  --no-responsive               Disable responsive design
  --no-fonts                    Don't include fonts
  --interactive                 Force interactive mode
  -f, --force                   Overwrite existing files without confirmation
  -h, --help                    Display help
```

## Real-World Examples

### Example 1: Convert Login Form

```bash
# Figma URL for a login form component
npx vibefigma \
  "https://www.figma.com/design/4i8Tp5btFPRqtkYXplnfT6/50-Web-Sign-up-log-in-designs--Community-?node-id=26-2944" \
  --component ./src/components/LoginForm.tsx \
  --assets ./public/login-assets \
  --force
```

Generated output (example):

```typescript
// src/components/LoginForm.tsx
import React from 'react';

export const LoginForm: React.FC = () => {
  return (
    <div className="flex flex-col items-center justify-center min-h-screen bg-gray-50">
      <div className="w-full max-w-md p-8 space-y-6 bg-white rounded-lg shadow-md">
        <h2 className="text-2xl font-bold text-center text-gray-900">
          Sign In
        </h2>
        <form className="space-y-4">
          <div>
            <label htmlFor="email" className="block text-sm font-medium text-gray-700">
              Email
            </label>
            <input
              id="email"
              type="email"
              className="w-full px-3 py-2 mt-1 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
              placeholder="you@example.com"
            />
          </div>
          <div>
            <label htmlFor="password" className="block text-sm font-medium text-gray-700">
              Password
            </label>
            <input
              id="password"
              type="password"
              className="w-full px-3 py-2 mt-1 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
            />
          </div>
          <button
            type="submit"
            className="w-full px-4 py-2 text-white bg-blue-600 rounded-md hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-blue-500"
          >
            Sign In
          </button>
        </form>
      </div>
    </div>
  );
};
```

### Example 2: Generate Multiple Components

```bash
# Create a components directory structure
mkdir -p src/components/hero
mkdir -p public/hero-assets

# Convert hero section
npx vibefigma \
  "https://www.figma.com/design/YOUR_FILE_ID?node-id=HERO_NODE_ID" \
  --component ./src/components/hero/Hero.tsx \
  --assets ./public/hero-assets \
  --optimize
```

### Example 3: Without Tailwind (Regular CSS)

```bash
npx vibefigma \
  "https://www.figma.com/design/YOUR_FILE_ID?node-id=NODE_ID" \
  --no-tailwind \
  --component ./src/components/CustomCard.tsx
```

This generates a component with inline styles or CSS modules instead of Tailwind classes.

## API Server Usage

VibeFigma includes a REST API for programmatic conversions.

### Starting the Server

```bash
# Install dependencies
bun install

# Development mode
bun run dev

# Production mode
bun run start
```

### Configuration

Create `.env` file:

```env
GOOGLE_GENERATIVE_AI_API_KEY=your_google_ai_key_here
PORT=3000
HOST=0.0.0.0
CORS_ORIGIN=*
FIGMA_TOKEN=your_figma_token_here
```

### API Endpoint

```typescript
// POST /v1/api/vibe-figma
interface ConversionRequest {
  figmaUrl: string;
  token?: string; // Optional if FIGMA_TOKEN env var is set
  options?: {
    useTailwind?: boolean;
    optimize?: boolean;
    clean?: boolean;
    responsive?: boolean;
    includeFonts?: boolean;
  };
}

interface ConversionResponse {
  component: string; // Generated React component code
  assets: Array<{
    name: string;
    url: string;
    data?: string; // Base64 for embedded assets
  }>;
}
```

### Example API Call

```typescript
const response = await fetch('http://localhost:3000/v1/api/vibe-figma', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
  },
  body: JSON.stringify({
    figmaUrl: 'https://www.figma.com/design/FILE_ID?node-id=NODE_ID',
    token: process.env.FIGMA_TOKEN,
    options: {
      useTailwind: true,
      optimize: true,
      responsive: true,
    },
  }),
});

const { component, assets } = await response.json();

// Write component to file
await fs.writeFile('./src/components/Generated.tsx', component);

// Download assets
for (const asset of assets) {
  const assetData = await fetch(asset.url);
  await fs.writeFile(`./public/${asset.name}`, await assetData.arrayBuffer());
}
```

## Common Patterns

### Pattern 1: Batch Conversion Script

```typescript
import { execSync } from 'child_process';
import path from 'path';

interface FigmaComponent {
  name: string;
  url: string;
  outputPath: string;
}

const components: FigmaComponent[] = [
  {
    name: 'Header',
    url: 'https://www.figma.com/design/FILE_ID?node-id=HEADER_NODE',
    outputPath: './src/components/Header.tsx',
  },
  {
    name: 'Footer',
    url: 'https://www.figma.com/design/FILE_ID?node-id=FOOTER_NODE',
    outputPath: './src/components/Footer.tsx',
  },
];

for (const comp of components) {
  console.log(`Converting ${comp.name}...`);
  execSync(
    `npx vibefigma "${comp.url}" --component ${comp.outputPath} --force`,
    { stdio: 'inherit' }
  );
}
```

### Pattern 2: CI/CD Integration

```yaml
# .github/workflows/figma-sync.yml
name: Sync Figma Designs

on:
  workflow_dispatch:
  schedule:
    - cron: '0 0 * * 1' # Weekly on Mondays

jobs:
  sync:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      
      - name: Setup Node.js
        uses: actions/setup-node@v3
        with:
          node-version: '18'
      
      - name: Convert Figma to React
        env:
          FIGMA_TOKEN: ${{ secrets.FIGMA_TOKEN }}
        run: |
          npx vibefigma "${{ vars.FIGMA_URL }}" \
            --component ./src/components/DesignSystem.tsx \
            --force
      
      - name: Create Pull Request
        uses: peter-evans/create-pull-request@v5
        with:
          title: 'chore: sync Figma designs'
          branch: figma-sync
```

### Pattern 3: Custom Post-Processing

```typescript
import { execSync } from 'child_process';
import fs from 'fs/promises';

async function convertAndCustomize(figmaUrl: string, outputPath: string) {
  // Generate component
  execSync(
    `npx vibefigma "${figmaUrl}" --component ${outputPath} --force`,
    { stdio: 'inherit' }
  );

  // Read generated file
  let content = await fs.readFile(outputPath, 'utf-8');

  // Add custom imports
  content = `import { motion } from 'framer-motion';\n${content}`;

  // Replace div with motion.div for animations
  content = content.replace(
    /<div className="/g,
    '<motion.div initial={{ opacity: 0 }} animate={{ opacity: 1 }} className="'
  );
  content = content.replace(/<\/div>/g, '</motion.div>');

  // Write back
  await fs.writeFile(outputPath, content);
  
  console.log(`✅ Generated and customized: ${outputPath}`);
}

// Usage
await convertAndCustomize(
  'https://www.figma.com/design/FILE_ID?node-id=NODE_ID',
  './src/components/AnimatedHero.tsx'
);
```

## Troubleshooting

### Issue: "Invalid Figma token"

**Solution**: Verify your token is correct and not expired:

```bash
# Test token manually
curl -H "X-Figma-Token: YOUR_TOKEN" \
  https://api.figma.com/v1/me
```

### Issue: "Node not found"

**Solution**: Ensure your Figma URL includes the correct `node-id` parameter:

```bash
# Correct format
https://www.figma.com/design/FILE_ID/FILE_NAME?node-id=123-456

# You can copy this from Figma:
# Right-click frame → Copy/Paste → Copy link
```

### Issue: Generated code has inline styles instead of Tailwind

**Solution**: Ensure Tailwind is not disabled:

```bash
# Remove --no-tailwind flag
npx vibefigma [url] --component ./output.tsx

# Explicitly enable optimization
npx vibefigma [url] --component ./output.tsx --optimize
```

### Issue: Assets not downloading

**Solution**: Check asset directory permissions and path:

```bash
# Create directory first
mkdir -p ./public/assets

# Specify absolute path
npx vibefigma [url] --assets $(pwd)/public/assets
```

### Issue: Component has positioning issues

**Solution**: Try disabling absolute positioning:

```bash
npx vibefigma [url] --no-absolute --responsive
```

### Issue: Fonts not loading

**Solution**: Ensure font imports are enabled and Tailwind config includes fonts:

```typescript
// tailwind.config.js
module.exports = {
  theme: {
    extend: {
      fontFamily: {
        sans: ['Inter', 'system-ui', 'sans-serif'],
      },
    },
  },
};
```

## Integration with Development Workflow

### Next.js Integration

```bash
# Generate component in Next.js app directory
npx vibefigma [url] \
  --component ./app/components/FigmaComponent.tsx \
  --assets ./public/figma-assets
```

### Vite/React Integration

```bash
# Generate for Vite project
npx vibefigma [url] \
  --component ./src/components/FigmaComponent.tsx \
  --assets ./public/assets
```

### Storybook Integration

```typescript
// Generate component
// Then create story file

import type { Meta, StoryObj } from '@storybook/react';
import { FigmaComponent } from './FigmaComponent';

const meta: Meta<typeof FigmaComponent> = {
  title: 'Design System/FigmaComponent',
  component: FigmaComponent,
};

export default meta;
type Story = StoryObj<typeof FigmaComponent>;

export const Default: Story = {};
```

## Best Practices

1. **Version Control**: Always commit generated components to track design changes over time
2. **Naming Conventions**: Use descriptive component names that match Figma frame names
3. **Asset Management**: Organize assets in subdirectories per component
4. **Review Generated Code**: Always review and test generated components before production use
5. **Incremental Updates**: Use `--force` flag carefully; review diffs when regenerating existing components
6. **Environment Variables**: Never commit tokens; always use environment variables
7. **AI Optimization**: Use `--clean` flag only when GOOGLE_GENERATIVE_AI_API_KEY is available for better code quality

## Resources

- GitHub: https://github.com/vibeflowing-inc/vibe_figma
- NPM: https://www.npmjs.com/package/vibefigma
- Homepage: https://vibeflow.ai/
- Discord: https://discord.com/invite/Ctm2A2uEaq
- License: AGPL-3.0
