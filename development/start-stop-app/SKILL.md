---
name: Start/Stop App
description: Start or stop the user-management FastAPI app. Use when you need to tun or kill the dev server.
---

# Start/Stop App

## Tool

- tools/start.py - Start the app with uvicorn on port 8000
- tools/stop.py - Kill any running uvicorn process

## Usage

```bash
# Start the app
uv run .agent/skills/start-stop-app/tools/start.py

# Stop the app
uv run .agent/skills/start-stop-app/tools/stop.py
```
