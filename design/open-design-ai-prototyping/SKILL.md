---
name: open-design-ai-prototyping
description: Local-first AI design tool that turns coding agents into design engines with 31 skills, 129 design systems, and multi-format export
triggers:
  - "set up Open Design for AI-driven prototyping"
  - "create a web prototype using Open Design with Claude"
  - "generate a pitch deck with Open Design agent skills"
  - "use Open Design to build a SaaS landing page"
  - "configure Open Design with my coding agent CLI"
  - "export Open Design artifacts to HTML and PDF"
  - "integrate Open Design design systems into my project"
  - "run Open Design locally with sandboxed preview"
---

# Open Design AI Prototyping

> Skill by [ara.so](https://ara.so) — Design Skills collection.

**Open Design** is a local-first, open-source alternative to Claude Design that transforms coding agents (Claude Code, Cursor, Codex, Gemini CLI, etc.) into design engines. It provides 31 composable skills, 129 brand-grade design systems, and a sandboxed preview environment with HTML/PDF/PPTX/MP4 export capabilities.

## What It Does

- **Agent-Native Design**: Detects 16 coding agent CLIs on your PATH and uses them as the design execution engine
- **Skill-Driven Workflow**: 31 built-in skills across web prototypes, decks, dashboards, mobile apps, marketing materials, and more
- **Design Systems Library**: 129 pre-built design systems (Linear, Stripe, Vercel, Airbnb, Tesla, Notion, etc.)
- **Multi-Format Export**: HTML, PDF, PPTX, MP4, ZIP, Markdown from a single artifact
- **Local-First**: SQLite persistence, on-disk project folders, no cloud lock-in
- **BYOK Support**: OpenAI/Anthropic/Azure/Google-compatible API proxy when no CLI is available

## Installation

### Quick Start (Local Development)

```bash
# Clone the repository
git clone https://github.com/nexu-io/open-design.git
cd open-design

# Install dependencies
pnpm install

# Start daemon + web interface
pnpm tools-dev
```

This boots:
- Daemon on `http://localhost:3001`
- Web UI on `http://localhost:3000`
- Auto-detects coding agents on your `PATH`

### Desktop App

Download pre-built installers from [open-design.ai](https://open-design.ai):
- macOS (Apple Silicon): `.dmg`
- Windows (x64): `.exe`

### Vercel Deployment (Web Layer Only)

```bash
# Deploy web interface (daemon runs separately)
vercel deploy

# Set environment variables in Vercel dashboard:
# - DAEMON_URL=your-daemon-endpoint
# - ANTHROPIC_API_KEY (optional, for BYOK)
# - OPENAI_API_KEY (optional, for BYOK)
```

## Project Structure

```
open-design/
├── apps/
│   ├── daemon/          # Core agent orchestration service
│   │   ├── src/
│   │   │   ├── prompts/ # Discovery, directions, critique prompts
│   │   │   ├── agents/  # CLI adapters (claude-code, cursor, etc.)
│   │   │   └── routes/  # API endpoints
│   │   └── package.json
│   ├── web/             # Next.js frontend
│   │   ├── app/
│   │   ├── components/
│   │   └── lib/
│   └── desktop/         # Electron wrapper (optional)
├── skills/              # 31 built-in skills
│   ├── web-prototype/
│   ├── guizang-ppt/     # Magazine-style decks
│   ├── saas-landing/
│   └── ...
├── design-systems/      # 129 design systems
│   ├── linear/
│   ├── stripe/
│   └── ...
└── prompt-templates/    # Media generation gallery (93 prompts)
```

## Key Commands

### Tools CLI

```bash
# Start all services
pnpm tools-dev

# Check system status
pnpm tools-dev status

# View daemon logs
pnpm tools-dev logs

# Inspect desktop (if Electron running)
pnpm tools-dev inspect desktop screenshot

# Stop all services
pnpm tools-dev stop

# Health check
pnpm tools-dev check
```

### Development

```bash
# Run daemon only
cd apps/daemon
pnpm dev

# Run web only
cd apps/web
pnpm dev

# Build for production
pnpm build

# Run tests
pnpm test
```

## Configuration

### Agent Detection

The daemon auto-detects CLIs on your `PATH`:

```typescript
// Supported agents (auto-detected)
const AGENTS = [
  'claude-code',      // Claude Code
  'codex',            // Codex CLI
  'devin',            // Devin for Terminal
  'cursor-agent',     // Cursor Agent
  'gemini',           // Gemini CLI
  'opencode',         // OpenCode
  'qwen-code',        // Qwen Code
  'qoder',            // Qoder CLI
  'gh-copilot',       // GitHub Copilot CLI
  'hermes',           // Hermes (ACP)
  'kimi',             // Kimi CLI (ACP)
  'pi',               // Pi (RPC)
  'kiro',             // Kiro CLI (ACP)
  'kilo',             // Kilo (ACP)
  'mistral-vibe',     // Mistral Vibe CLI
  'deepseek-tui'      // DeepSeek TUI
];
```

### BYOK Configuration (No CLI)

When no agent CLI is detected, configure API proxy:

```bash
# Environment variables
ANTHROPIC_API_KEY=your_key_here
OPENAI_API_KEY=your_key_here
AZURE_OPENAI_KEY=your_key_here
AZURE_OPENAI_ENDPOINT=https://your-resource.openai.azure.com
GOOGLE_API_KEY=your_key_here
```

### Database

SQLite configuration (`.od/app.sqlite`):

```typescript
// apps/daemon/src/db/schema.ts
export const projects = sqliteTable('projects', {
  id: text('id').primaryKey(),
  name: text('name').notNull(),
  skill: text('skill').notNull(),
  designSystem: text('design_system'),
  direction: text('direction'),
  createdAt: integer('created_at', { mode: 'timestamp' }),
  updatedAt: integer('updated_at', { mode: 'timestamp' })
});

export const conversations = sqliteTable('conversations', {
  id: text('id').primaryKey(),
  projectId: text('project_id').notNull().references(() => projects.id),
  messages: text('messages', { mode: 'json' }),
  artifacts: text('artifacts', { mode: 'json' })
});
```

## API Reference

### Daemon Endpoints

#### Start Agent Session

```typescript
// POST /api/agent/start
const response = await fetch('http://localhost:3001/api/agent/start', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    projectId: 'proj_123',
    skill: 'web-prototype',
    designSystem: 'linear',
    direction: 'modern-minimal',
    prompt: 'Create a SaaS dashboard with user analytics'
  })
});

const { sessionId, status } = await response.json();
```

#### Stream Agent Response

```typescript
// GET /api/agent/stream/:sessionId (SSE)
const eventSource = new EventSource(
  `http://localhost:3001/api/agent/stream/${sessionId}`
);

eventSource.addEventListener('message', (event) => {
  const data = JSON.parse(event.data);
  console.log(data); // { type: 'delta', content: '...' }
});

eventSource.addEventListener('artifact', (event) => {
  const artifact = JSON.parse(event.data);
  console.log(artifact); // { type: 'html', content: '...', title: '...' }
});

eventSource.addEventListener('tool_call', (event) => {
  const tool = JSON.parse(event.data);
  console.log(tool); // { name: 'Write', args: { path: '...', content: '...' } }
});
```

#### Export Artifacts

```typescript
// POST /api/export
const response = await fetch('http://localhost:3001/api/export', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    projectId: 'proj_123',
    format: 'pdf', // 'html' | 'pdf' | 'pptx' | 'zip' | 'mp4' | 'markdown'
    artifactId: 'art_456'
  })
});

const blob = await response.blob();
// Save or download the exported file
```

#### Import Claude Design Export

```typescript
// POST /api/import/claude-design
const formData = new FormData();
formData.append('file', claudeDesignZip);

const response = await fetch('http://localhost:3001/api/import/claude-design', {
  method: 'POST',
  body: formData
});

const { projectId, conversationId } = await response.json();
```

### BYOK Proxy Endpoints

```typescript
// POST /api/proxy/anthropic/stream
const response = await fetch('http://localhost:3001/api/proxy/anthropic/stream', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
    'Authorization': `Bearer ${process.env.ANTHROPIC_API_KEY}`
  },
  body: JSON.stringify({
    model: 'claude-3-5-sonnet-20241022',
    messages: [{ role: 'user', content: 'Design a landing page' }],
    max_tokens: 4096
  })
});

// SSE stream normalized to Open Design chat protocol
```

## Working Code Examples

### Creating a Web Prototype with Design System

```typescript
// apps/web/lib/create-prototype.ts
import { useAgent } from '@/hooks/use-agent';

export function usePrototypeCreation() {
  const { startSession, streamResponse } = useAgent();

  async function createPrototype(prompt: string) {
    const session = await startSession({
      skill: 'web-prototype',
      designSystem: 'stripe', // Use Stripe design system
      direction: 'modern-minimal',
      prompt: `
        ${prompt}
        
        Requirements:
        - Use Stripe's color palette and typography
        - Include responsive navigation
        - Add interactive components
        - Follow accessibility best practices
      `
    });

    for await (const chunk of streamResponse(session.id)) {
      if (chunk.type === 'artifact') {
        // Artifact ready for sandboxed preview
        renderInIframe(chunk.content);
      }
      if (chunk.type === 'tool_call' && chunk.name === 'Write') {
        // Agent writing to project folder
        console.log(`Writing: ${chunk.args.path}`);
      }
    }
  }

  return { createPrototype };
}
```

### Using Skills Programmatically

```typescript
// apps/daemon/src/skills/loader.ts
import { loadSkill } from './skills-registry';

async function executeSkillWithAgent(
  skillName: string,
  userPrompt: string,
  agentCli: string
) {
  const skill = await loadSkill(skillName);
  
  // Combine skill prompt + user prompt
  const fullPrompt = `
${skill.systemPrompt}

## User Request
${userPrompt}

## Design System
${await loadDesignSystem('linear')}

## Visual Direction
${await loadDirection('modern-minimal')}

## Pre-flight Checklist
${skill.checklist.join('\n')}
`;

  // Spawn agent CLI
  const process = spawn(agentCli, ['--prompt-file', 'prompt.txt'], {
    cwd: projectPath,
    env: { ...process.env }
  });

  // Stream response
  process.stdout.on('data', (chunk) => {
    const artifact = parseArtifact(chunk.toString());
    if (artifact) {
      emit('artifact', artifact);
    }
  });
}
```

### Custom Skill Definition

```typescript
// skills/custom-portfolio/skill.json
{
  "name": "custom-portfolio",
  "displayName": "Portfolio Website",
  "scenario": "personal",
  "description": "Personal portfolio with project showcase",
  "mode": "prototype",
  "template": "portfolio-base",
  "checklist": [
    "Hero section with name and tagline",
    "Project grid with hover states",
    "About section with bio",
    "Contact form with validation",
    "Responsive mobile layout"
  ],
  "systemPrompt": "You are building a personal portfolio...",
  "palette": ["oklch(0.95 0.02 200)", "oklch(0.2 0.05 250)"],
  "fonts": {
    "heading": "Inter",
    "body": "Inter"
  }
}
```

### Export Pipeline

```typescript
// apps/daemon/src/export/pdf.ts
import puppeteer from 'puppeteer';

export async function exportToPDF(
  htmlContent: string,
  options: { format?: 'A4' | 'Letter' }
) {
  const browser = await puppeteer.launch({ headless: true });
  const page = await browser.newPage();
  
  await page.setContent(htmlContent, {
    waitUntil: 'networkidle0'
  });
  
  const pdf = await page.pdf({
    format: options.format || 'A4',
    printBackground: true,
    margin: { top: '20px', bottom: '20px' }
  });
  
  await browser.close();
  return pdf;
}
```

### Media Generation (Image)

```typescript
// apps/daemon/src/media/image.ts
export async function generateImage(prompt: string) {
  const response = await fetch('https://api.openai.com/v1/images/generations', {
    method: 'POST',
    headers: {
      'Authorization': `Bearer ${process.env.OPENAI_API_KEY}`,
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({
      model: 'dall-e-3',
      prompt: prompt,
      size: '1792x1024',
      quality: 'hd',
      n: 1
    })
  });

  const { data } = await response.json();
  return data[0].url; // Download and save to project workspace
}
```

## Common Patterns

### Interactive Question Form Before Generation

```typescript
// apps/web/components/question-form.tsx
export function QuestionForm({ skill, onSubmit }) {
  const questions = skill.discoveryQuestions || [
    { id: 'purpose', text: 'What is the main purpose?' },
    { id: 'audience', text: 'Who is the target audience?' },
    { id: 'tone', text: 'What tone should it have?' }
  ];

  const [answers, setAnswers] = useState({});

  function handleSubmit() {
    const enrichedPrompt = `
User Request: ${originalPrompt}

Discovery Answers:
${Object.entries(answers).map(([k, v]) => `- ${k}: ${v}`).join('\n')}
`;
    onSubmit(enrichedPrompt);
  }

  return <form>...</form>;
}
```

### Five-Dimensional Self-Critique

```typescript
// apps/daemon/src/prompts/critique.ts
export const CRITIQUE_DIMENSIONS = [
  {
    name: 'Visual Hierarchy',
    criteria: 'Clear focal point, logical reading flow, proper emphasis'
  },
  {
    name: 'Brand Consistency',
    criteria: 'Design system palette used, fonts match spec, no arbitrary colors'
  },
  {
    name: 'Responsive Design',
    criteria: 'Mobile breakpoints defined, touch targets 44px+, no horizontal scroll'
  },
  {
    name: 'Accessibility',
    criteria: 'WCAG AA contrast, semantic HTML, keyboard navigation'
  },
  {
    name: 'Polish',
    criteria: 'No placeholder content, real copy, production-ready assets'
  }
];

export function buildCritiquePrompt(artifact: string) {
  return `
## Self-Critique

Review your output against these dimensions:

${CRITIQUE_DIMENSIONS.map(d => `
### ${d.name}
${d.criteria}
Score (1-5): _____
Issues: _____
`).join('\n')}

If any dimension scores below 4, revise before emitting final artifact.
`;
}
```

### Sandboxed Iframe Rendering

```typescript
// apps/web/components/artifact-preview.tsx
import { useEffect, useRef } from 'react';

export function ArtifactPreview({ html }: { html: string }) {
  const iframeRef = useRef<HTMLIFrameElement>(null);

  useEffect(() => {
    const iframe = iframeRef.current;
    if (!iframe) return;

    const doc = iframe.contentDocument;
    if (!doc) return;

    doc.open();
    doc.write(`
<!DOCTYPE html>
<html>
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <style>
    * { margin: 0; padding: 0; box-sizing: border-box; }
  </style>
</head>
<body>
  ${html}
</body>
</html>
    `);
    doc.close();
  }, [html]);

  return (
    <iframe
      ref={iframeRef}
      sandbox="allow-scripts allow-same-origin"
      style={{ width: '100%', height: '100%', border: 'none' }}
    />
  );
}
```

### PATH Agent Detection

```typescript
// apps/daemon/src/agents/detect.ts
import { exec } from 'child_process';
import { promisify } from 'util';

const execAsync = promisify(exec);

export async function detectAgents(): Promise<string[]> {
  const candidates = [
    'claude-code',
    'cursor-agent',
    'codex',
    'gemini',
    'gh-copilot'
  ];

  const detected: string[] = [];

  for (const cmd of candidates) {
    try {
      await execAsync(`which ${cmd}`, { timeout: 1000 });
      detected.push(cmd);
    } catch {
      // Not on PATH
    }
  }

  return detected;
}
```

## Troubleshooting

### Agent Not Detected

**Problem**: Daemon starts but shows "No agent CLI detected"

**Solution**:
```bash
# Verify CLI is on PATH
which claude-code
which cursor-agent

# Add to PATH if missing (macOS/Linux)
export PATH="$PATH:/path/to/agent/bin"

# Restart daemon
pnpm tools-dev stop
pnpm tools-dev
```

### Windows ENAMETOOLONG Errors

**Problem**: Long prompts fail on Windows

**Solution**: The daemon automatically falls back to stdin/prompt-file mode on Windows:

```typescript
// apps/daemon/src/agents/spawn.ts
if (process.platform === 'win32' && promptLength > 8191) {
  // Use prompt file instead of command line arg
  await fs.writeFile(promptFilePath, prompt);
  spawn(agentCli, ['--prompt-file', promptFilePath]);
}
```

### Artifact Not Rendering

**Problem**: Generated HTML shows blank iframe

**Check**:
1. Browser console for CSP errors
2. Artifact contains valid HTML structure
3. No external resource blocking (CORS)

```typescript
// Debug artifact content
console.log('Artifact HTML:', artifact.content.substring(0, 500));

// Check iframe sandbox
const iframe = document.querySelector('iframe');
console.log('Sandbox:', iframe.getAttribute('sandbox'));
```

### Export Fails

**Problem**: PDF/PPTX export returns 500 error

**Solution**:
```bash
# Install Puppeteer dependencies (Linux)
sudo apt-get install -y \
  chromium-browser \
  fonts-liberation \
  libnss3 \
  libxss1

# macOS (ensure Chromium is available)
brew install chromium

# Verify export endpoint
curl -X POST http://localhost:3001/api/export \
  -H "Content-Type: application/json" \
  -d '{"projectId":"test","format":"pdf","artifactId":"art_1"}'
```

### SQLite Lock Errors

**Problem**: `database is locked` during concurrent operations

**Solution**:
```typescript
// apps/daemon/src/db/client.ts
import Database from 'better-sqlite3';

export const db = new Database('.od/app.sqlite', {
  timeout: 5000, // Wait up to 5s for lock
  verbose: console.log
});

// Enable WAL mode for better concurrency
db.pragma('journal_mode = WAL');
```

### BYOK Proxy SSRF Protection

**Problem**: Custom baseURL rejected

**Expected**: Daemon blocks internal IPs for security:

```typescript
// apps/daemon/src/proxy/validate.ts
const BLOCKED_RANGES = [
  '127.0.0.0/8',
  '10.0.0.0/8',
  '172.16.0.0/12',
  '192.168.0.0/16'
];

export function validateBaseUrl(url: string) {
  const hostname = new URL(url).hostname;
  if (isPrivateIP(hostname)) {
    throw new Error('SSRF blocked: internal IP detected');
  }
}
```

## Resources

- **Documentation**: [QUICKSTART.md](https://github.com/nexu-io/open-design/blob/main/QUICKSTART.md)
- **Skills Guide**: [skills/README.md](https://github.com/nexu-io/open-design/tree/main/skills)
- **Design Systems**: [design-systems/README.md](https://github.com/nexu-io/open-design/tree/main/design-systems)
- **Discord Community**: [discord.gg/qhbcCH8Am4](https://discord.gg/qhbcCH8Am4)
- **Twitter**: [@nexudotio](https://x.com/nexudotio)
- **Discussions**: [GitHub Discussions](https://github.com/nexu-io/open-design/discussions)

## License

Apache-2.0 — see [LICENSE](https://github.com/nexu-io/open-design/blob/main/LICENSE)
