---
name: project-creator
description: Creates new projects from BUILDER stack template. Auto-triggers on Dashboard "New Project" button or API call /api/projects/create. Handles clone, port assignment, PM2 setup, deployment.
allowed-tools: Read, Write, Bash, Glob
---

# Skill: Project Creator

> **Auto-loaded by**: EXECUTOR when Dashboard API calls project creation
> **Purpose**: Create new project from BUILDER stack, deploy automatically
> **Version**: 1.0.0

---

## Trigger Conditions

**EXECUTOR charges ce skill quand:**
- API call: `POST /api/projects/create`
- Dashboard button: "+ New Project"
- Command: `create-project [name]` (via Dashboard terminal)

---

## Workflow (STRICT - 5 Steps)

### Step 1: Validate Project Name

```typescript
// OBLIGATOIRE avant toute création

function validateProjectName(name: string): boolean {
  // Règles:
  // - Kebab-case uniquement (lowercase + hyphens)
  // - 3-50 caractères
  // - Pas de caractères spéciaux
  // - Pas de doublon (check si existe déjà)

  const REGEX = /^[a-z0-9-]{3,50}$/

  if (!REGEX.test(name)) {
    throw new Error(`Invalid project name: ${name}. Must be kebab-case.`)
  }

  const projectPath = `/home/pilote/projet/secondaire/${name}`
  if (fs.existsSync(projectPath)) {
    throw new Error(`Project ${name} already exists.`)
  }

  return true
}
```

---

### Step 2: Clone BUILDER Stack

```bash
#!/bin/bash

PROJECT_NAME="$1"
PROJECT_PATH="/home/pilote/projet/secondaire/$PROJECT_NAME"
BUILDER_STACK="/home/pilote/projet/primaire/BUILDER/.stack"

echo "📦 Cloning BUILDER stack..."

# Create project directory
mkdir -p "$PROJECT_PATH"

# Clone stack (57 shadcn components + Next.js 16)
cp -r "$BUILDER_STACK"/* "$PROJECT_PATH"/

# Verify clone succeeded
if [ ! -f "$PROJECT_PATH/package.json" ]; then
  echo "❌ Clone failed"
  exit 1
fi

echo "✅ Stack cloned"
```

**Fichiers clonés:**
```
projet/secondaire/mon-app/
├── components/ui/      (57 composants shadcn)
├── app/
│   ├── globals.css
│   ├── themes.css
│   └── layout.tsx
├── lib/utils.ts
├── package.json
├── tsconfig.json
├── next.config.ts
└── tailwind.config.ts
```

---

### Step 3: Initialize .build/ Structure

```bash
echo "📋 Initializing .build/..."

mkdir -p "$PROJECT_PATH/.build/decisions"

# context.md
cat > "$PROJECT_PATH/.build/context.md" << 'EOF'
# Project Context

## Stack Technique
- Frontend: Next.js 16 + shadcn/ui (57 components)
- Styling: Tailwind CSS v4
- Dark mode: Included (themes.css)

## Architecture Actuelle
(Will be populated after first features)

## Conventions Établies
- Components: components/ui/ (shadcn)
- Pages: app/
- Utils: lib/utils.ts
EOF

# timeline.md
cat > "$PROJECT_PATH/.build/timeline.md" << EOF
# Timeline

## $(date +"%Y-%m-%d %H:%M") - Project Initialization

**Type**: Setup
**Status**: ✓ Completed
**Source**: Dashboard GUI

### Changes
- Project created via Dashboard
- BUILDER stack cloned (57 shadcn components)
- .build/ structure initialized
- Deployed to PM2

### Notes
- Ready for feature development
- Preview: http://89.116.27.88:[PORT]
EOF

# tasks.md, issues.md, specs.md (templates vides)
touch "$PROJECT_PATH/.build/tasks.md"
touch "$PROJECT_PATH/.build/issues.md"
touch "$PROJECT_PATH/.build/specs.md"

echo "✅ .build/ initialized"
```

---

### Step 4: Install Dependencies + Build

```bash
echo "📥 Installing dependencies..."

cd "$PROJECT_PATH"

# Install (silent mode)
npm install --silent

# Verify install succeeded
if [ ! -d "node_modules" ]; then
  echo "❌ npm install failed"
  exit 1
fi

echo "✅ Dependencies installed"

echo "📦 Building production..."

# Clean old builds
rm -rf .next

# Build production
npm run build

# Verify build succeeded
if [ ! -f ".next/BUILD_ID" ]; then
  echo "❌ Build failed"
  exit 1
fi

echo "✅ Production build ready"
```

---

### Step 5: Deploy to PM2 (Auto Port Assignment)

```bash
echo "🚀 Deploying to PM2..."

# Get next available port
HIGHEST_PORT=$(pm2 jlist 2>/dev/null | node -e "
  let data = '';
  process.stdin.on('data', chunk => data += chunk);
  process.stdin.on('end', () => {
    try {
      const procs = JSON.parse(data);
      const ports = procs
        .map(p => p.pm2_env.PORT)
        .filter(p => p && !isNaN(p))
        .map(Number);
      console.log(Math.max(3000, ...ports));
    } catch(e) { console.log(3000); }
  });
")

PORT=$((HIGHEST_PORT + 1))

# Save port to .env
echo "PORT=$PORT" > .env

# Create ecosystem.config.js
cat > ecosystem.config.js << EOF
module.exports = {
  apps: [{
    name: '$PROJECT_NAME',
    script: 'npm',
    args: 'start',
    cwd: '$PROJECT_PATH',
    instances: 1,
    exec_mode: 'cluster',
    env: {
      NODE_ENV: 'production',
      PORT: $PORT
    },
    error_file: '~/.pm2/logs/$PROJECT_NAME-error.log',
    out_file: '~/.pm2/logs/$PROJECT_NAME-out.log',
    merge_logs: true,
    autorestart: true,
    watch: false
  }]
}
EOF

# Start PM2
pm2 start ecosystem.config.js

# Save PM2 config (persist reboot)
pm2 save

# Health check (max 15 seconds)
echo "🔍 Health check..."

for i in {1..15}; do
  sleep 1

  # Check PM2 status
  STATUS=$(pm2 jlist 2>/dev/null | node -e "
    let data = '';
    process.stdin.on('data', chunk => data += chunk);
    process.stdin.on('end', () => {
      try {
        const procs = JSON.parse(data);
        const proc = procs.find(p => p.name === '$PROJECT_NAME');
        console.log(proc ? proc.pm2_env.status : 'not_found');
      } catch(e) { console.log('error'); }
    });
  ")

  if [ "$STATUS" == "online" ]; then
    # Check HTTP 200
    HTTP_CODE=$(curl -s -o /dev/null -w "%{http_code}" http://localhost:$PORT)

    if [ "$HTTP_CODE" == "200" ]; then
      echo "✅ Health check passed"
      break
    fi
  fi

  if [ $i -eq 15 ]; then
    echo "⚠️ Health check timeout (still starting...)"
  fi
done

echo ""
echo "✅ Project deployed successfully!"
echo ""
echo "📍 Details:"
echo "   Name: $PROJECT_NAME"
echo "   Path: $PROJECT_PATH"
echo "   Port: $PORT"
echo "   Preview: http://89.116.27.88:$PORT"
echo "   PM2: pm2 logs $PROJECT_NAME"
echo ""
```

---

### Step 6: Setup Chrome DevTools Container (Optional)

**Si tests automatiques demandés:**

```bash
# Calculate next noVNC port (6081, 6082, 6083...)
NOVNC_BASE=6080
CHROME_BASE=9223

NEXT_NOVNC=$((NOVNC_BASE + PORT - 3000))
NEXT_CHROME=$((CHROME_BASE + PORT - 3000))

# Start noVNC container for this project
docker run -d \
  --name "chrome-$PROJECT_NAME" \
  --restart=always \
  -p $NEXT_NOVNC:80 \
  -p $NEXT_CHROME:9223 \
  -e RESOLUTION=1920x1080 \
  -e VNC_PASSWORD=Voiture789 \
  --shm-size=2gb \
  dorowu/ubuntu-desktop-lxde-vnc

# Wait for container ready
sleep 5

# Start Chrome + socat in container
docker exec "chrome-$PROJECT_NAME" bash -c "
  # Install Chrome if not present
  if ! command -v google-chrome &> /dev/null; then
    wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add -
    echo 'deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main' > /etc/apt/sources.list.d/google-chrome.list
    apt-get update -qq
    apt-get install -y google-chrome-stable socat
  fi

  # Start Chrome with remote debugging
  DISPLAY=:1 google-chrome \
    --remote-debugging-port=9222 \
    --no-sandbox \
    --disable-dev-shm-usage \
    --start-maximized \
    http://89.116.27.88:$PORT &

  # Tunnel port 9222 → 9223
  socat TCP-LISTEN:9223,fork,bind=0.0.0.0 TCP:127.0.0.1:9222 &
"

echo "✅ Chrome DevTools ready"
echo "   noVNC: http://89.116.27.88:$NEXT_NOVNC"
echo "   DevTools: http://89.116.27.88:$NEXT_CHROME"
```

---

## Return Format (JSON API Response)

```json
{
  "success": true,
  "project": {
    "name": "mon-app",
    "path": "/home/pilote/projet/secondaire/mon-app",
    "port": 3004,
    "preview_url": "http://89.116.27.88:3004",
    "pm2_status": "online",
    "devtools": {
      "novnc_url": "http://89.116.27.88:6084",
      "chrome_port": 9227
    },
    "created_at": "2025-11-11T17:30:00Z"
  }
}
```

---

## Error Handling

### Error 1: Invalid Project Name

```json
{
  "success": false,
  "error": "INVALID_NAME",
  "message": "Project name must be kebab-case (lowercase, hyphens only)",
  "example": "my-awesome-app"
}
```

### Error 2: Project Already Exists

```json
{
  "success": false,
  "error": "PROJECT_EXISTS",
  "message": "Project 'mon-app' already exists",
  "existing_port": 3002
}
```

### Error 3: Build Failed

```json
{
  "success": false,
  "error": "BUILD_FAILED",
  "message": "Production build failed",
  "logs": "npm ERR! ..."
}
```

### Error 4: PM2 Deploy Failed

```json
{
  "success": false,
  "error": "DEPLOY_FAILED",
  "message": "PM2 deployment failed",
  "logs": "pm2 ERR! ..."
}
```

---

## Integration avec Dashboard

### Dashboard API Call

```typescript
// Dashboard: app/api/projects/create/route.ts

import { exec } from 'child_process'
import { promisify } from 'util'

const execAsync = promisify(exec)

export async function POST(req: Request) {
  const { name } = await req.json()

  try {
    // Validate name
    if (!/^[a-z0-9-]{3,50}$/.test(name)) {
      return Response.json({
        success: false,
        error: 'INVALID_NAME',
        message: 'Project name must be kebab-case'
      }, { status: 400 })
    }

    // Execute creation script (invokes EXECUTOR with this skill)
    const script = `/home/pilote/projet/primaire/BUILDER/bin/create-project-api`
    const { stdout, stderr } = await execAsync(`${script} ${name}`)

    // Parse output (JSON)
    const result = JSON.parse(stdout)

    return Response.json(result)

  } catch (error) {
    return Response.json({
      success: false,
      error: 'EXECUTION_FAILED',
      message: error.message
    }, { status: 500 })
  }
}
```

### Dashboard Frontend

```tsx
// Dashboard: components/NewProjectDialog.tsx

'use client'
import { useState } from 'react'
import { Button } from '@/components/ui/button'
import {
  Dialog,
  DialogContent,
  DialogHeader,
  DialogTitle,
  DialogTrigger,
} from '@/components/ui/dialog'
import { Input } from '@/components/ui/input'

export function NewProjectDialog({ onSuccess }: { onSuccess: () => void }) {
  const [name, setName] = useState('')
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')

  const createProject = async () => {
    setLoading(true)
    setError('')

    try {
      const res = await fetch('/api/projects/create', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ name })
      })

      const data = await res.json()

      if (data.success) {
        onSuccess() // Refresh project list
        setName('')
      } else {
        setError(data.message)
      }
    } catch (err) {
      setError('Failed to create project')
    } finally {
      setLoading(false)
    }
  }

  return (
    <Dialog>
      <DialogTrigger asChild>
        <Button>+ New Project</Button>
      </DialogTrigger>

      <DialogContent>
        <DialogHeader>
          <DialogTitle>Create New Project</DialogTitle>
        </DialogHeader>

        <div className="space-y-4">
          <Input
            placeholder="project-name (kebab-case)"
            value={name}
            onChange={(e) => setName(e.target.value)}
          />

          {error && (
            <p className="text-red-500 text-sm">{error}</p>
          )}

          <Button
            onClick={createProject}
            disabled={loading || !name}
            className="w-full"
          >
            {loading ? 'Creating...' : 'Create Project'}
          </Button>
        </div>
      </DialogContent>
    </Dialog>
  )
}
```

---

## Auto-Refresh Dashboard on New Project

```typescript
// Dashboard: hooks/useProjects.ts

'use client'
import { useState, useEffect } from 'react'

export function useProjects() {
  const [projects, setProjects] = useState([])

  const refreshProjects = async () => {
    const res = await fetch('/api/projects/list')
    const data = await res.json()
    setProjects(data.projects)
  }

  useEffect(() => {
    // Initial load
    refreshProjects()

    // Poll every 5 seconds (detect new projects)
    const interval = setInterval(refreshProjects, 5000)

    return () => clearInterval(interval)
  }, [])

  return { projects, refreshProjects }
}
```

---

## Conventions EXECUTOR

**Quand EXECUTOR reçoit cette task:**

1. **Charge skill automatiquement** (détection keyword "create project")
2. **Exécute workflow 5 steps** (validate → clone → build → deploy → devtools)
3. **Return JSON response** (succès ou erreur)
4. **Update .build/timeline.md** (log création projet)
5. **Confirme à Dashboard** via API response

**EXECUTOR ne demande PAS de validation user** (création automatique).

---

**Version**: 1.0.0
**Last updated**: 2025-11-11
**Maintainer**: BUILDER System
