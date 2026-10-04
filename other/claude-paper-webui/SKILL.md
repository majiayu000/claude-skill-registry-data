---
name: claude-paper-webui
description: Start the Claude Paper web viewer to browse and study papers
allowed-tools: Bash
---

## Cross-Agent Compatibility

> This file is generated from the existing Claude Paper Skill. Its workflow and output requirements are unchanged; only equivalent host metadata, the plugin-root variable, and cross-skill invocation are adapted.

Resolve `CLAUDE_PAPER_PLUGIN_ROOT` to the absolute `plugin/` directory in this package before each shell invocation. From this `SKILL.md`, that directory is `../../plugin`.
Treat every `${CLAUDE_PAPER_PLUGIN_ROOT}` reference below as that resolved absolute directory. Do not substitute the current workspace root.

When this workflow asks to launch the viewer, load and follow the `claude-paper-webui` skill.

---

# Start Web UI

This skill starts the Claude Paper web viewer using the production Nuxt.js server.

## Step 1: Check and Install Dependencies (First Run Only)

Check if web dependencies are installed (with corruption check):
```bash
cd "${CLAUDE_PAPER_PLUGIN_ROOT}/src/web"

if [ ! -d "node_modules" ]; then
  echo "First run - installing web dependencies..."
  npm ci
  echo "Web dependencies installed!"
elif [ ! -f "node_modules/.package-lock.json" ] || [ ! -d "node_modules/nuxt" ]; then
  echo "ERROR: node_modules is corrupted, performing clean install..."
  rm -rf node_modules
  npm ci
  echo "Web dependencies installed!"
else
  echo "Dependencies already installed"
fi
```

## Step 2: Build Production Server (auto-rebuilds on plugin update)

Build if needed or if plugin version changed:
```bash
cd ${CLAUDE_PAPER_PLUGIN_ROOT}/src/web

PLUGIN_VERSION=$(node -e "console.log(require('${CLAUDE_PAPER_PLUGIN_ROOT}/.claude-plugin/plugin.json').version)")
BUILD_VERSION=""
if [ -f ".output/.build-version" ]; then
  BUILD_VERSION=$(cat ".output/.build-version")
fi

if [ ! -f ".output/server/index.mjs" ] || [ "$PLUGIN_VERSION" != "$BUILD_VERSION" ]; then
  echo "Building production server (v${PLUGIN_VERSION})..."
  npm run build
  echo "$PLUGIN_VERSION" > .output/.build-version
  echo "Build complete!"
else
  echo "Production build is up to date (v${BUILD_VERSION})"
fi
```

## Step 3: Check Port Availability

Ensure port 5815 is available (with version check restart):
```bash
# Get version info for comparison
PLUGIN_VERSION=$(node -e "console.log(require('${CLAUDE_PAPER_PLUGIN_ROOT}/.claude-plugin/plugin.json').version)")
BUILD_VERSION=""
if [ -f ".output/.build-version" ]; then
  BUILD_VERSION=$(cat ".output/.build-version")
fi

if lsof -i :5815 > /dev/null 2>&1; then
  echo "INFO: Port 5815 is already in use"
  PID_FILE="/tmp/claude-paper-webui.pid"
  if [ -f "$PID_FILE" ] && kill -0 $(cat "$PID_FILE") 2>/dev/null; then
    # Check version match - restart if plugin was updated
    if [ "$PLUGIN_VERSION" = "$BUILD_VERSION" ]; then
      echo "Claude Paper web UI is already running (version ${PLUGIN_VERSION})"
      echo "Access it at: http://localhost:5815"
      exit 0
    else
      echo "Version mismatch: running ${BUILD_VERSION}, need ${PLUGIN_VERSION}"
      echo "Stopping old server..."
      kill $(cat "$PID_FILE") 2>/dev/null
      sleep 2
      rm -f "$PID_FILE"
      echo "Old server stopped, will restart with new version"
    fi
  else
    echo "ERROR: Port 5815 is occupied by another process"
    exit 1
  fi
fi
```

## Step 4: Start Production Server

Start the server in background:
```bash
HOST=127.0.0.1 PORT=5815 node .output/server/index.mjs &
SERVER_PID=$!

# Save PID for later cleanup
echo $SERVER_PID > /tmp/claude-paper-webui.pid
echo "Server PID: $SERVER_PID"
```

## Step 5: Verify Server Health

Wait for server to be ready:
```bash
timeout=10
while [ $timeout -gt 0 ]; do
  if curl -s http://localhost:5815/api/papers > /dev/null 2>&1; then
    echo "Server is ready!"
    break
  fi
  sleep 1
  timeout=$((timeout - 1))
done

if [ $timeout -eq 0 ]; then
  echo "ERROR: Server failed to start properly"
  kill $SERVER_PID 2>/dev/null
  rm -f /tmp/claude-paper-webui.pid
  exit 1
fi
```

## Step 6: Inform User

Tell the user the web viewer is available and provide cleanup instructions:
```
Claude Paper web UI is now running!

Access it at: http://localhost:5815

To stop the server, run:
  kill $(cat /tmp/claude-paper-webui.pid)
```
