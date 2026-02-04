---
name: start-services
description: Intelligently start project services (backend, frontend) with automatic port conflict detection and resolution
---

# Start Services - Intelligent Service Launcher

This skill helps you start project services (backend API, frontend server) with automatic detection and resolution of port conflicts. Optimized for Python/FastAPI backend and static frontend projects.

## When to Use This Skill

- **User explicitly asks**: "start services", "start the server", "run the app", "launch backend/frontend"
- **After session recovery**: When recovering context with `/recover-context`
- **After git pull**: When starting work after pulling latest changes
- **Development workflow**: Beginning a development session
- **After dependency installation**: When setting up environment for first time

## Common Port Conflicts Observed

From real-world usage, common conflicts include:
1. **Port 8000**: Often occupied by MCP servers (workspace-mcp), uvicorn instances, other FastAPI apps
2. **Port 8080**: Often occupied by previous http.server instances, other web servers
3. **Port 3000**: Often occupied by React dev servers, Node.js apps
4. **Port 5000**: Often occupied by Flask apps, other Python servers

## Instructions

### Step 1: Check Project Structure

Determine what services exist in the project:

```bash
# Check for backend (FastAPI/Flask)
ls -la src/api/main.py 2>/dev/null && echo "Backend exists" || echo "Backend not implemented yet"

# Check for frontend
ls -la frontend/index.html 2>/dev/null && echo "Frontend exists" || echo "Frontend not found"

# Check for requirements.txt
ls -la requirements.txt 2>/dev/null && echo "Requirements file exists" || echo "No requirements.txt"

# Check for virtual environment
ls -la venv/ 2>/dev/null && echo "venv exists" || echo "venv not created"
```

### Step 2: Detect Port Conflicts

**CRITICAL**: Always check for port conflicts BEFORE attempting to start services.

```bash
# Check common ports for conflicts
lsof -i :8000 -i :8080 -i :3000 -i :5000 || echo "All common ports are available"
```

**If ports are occupied**, identify what's using them:

```bash
# For each occupied port, check the process
lsof -i :8000 | grep LISTEN  # Backend port
lsof -i :8080 | grep LISTEN  # Frontend port

# Get detailed process info
ps -p <PID> -o pid,ppid,command
```

### Step 3: Resolve Port Conflicts

**Decision Tree for Port Conflicts**:

#### If port is occupied by same project (previous session):
```bash
# Kill the old process gracefully
kill <PID>

# Verify port is released
lsof -i :<PORT> || echo "Port <PORT> is now available"
```

#### If port is occupied by MCP server or system service:
```bash
# DO NOT KILL - Choose alternative port instead
# For backend: Use 8001, 8002, etc.
# For frontend: Use 8081, 8082, etc.

# Report to user that alternative port will be used
echo "Port 8000 occupied by MCP server, using port 8001 instead"
```

#### If port is occupied by unknown process:
```bash
# Ask user before killing
# Use AskUserQuestion tool to confirm:
# - Show process details (PID, command)
# - Ask if safe to kill
# - Offer alternative port option
```

### Step 4: Setup Virtual Environment (Python Projects)

**CRITICAL**: ALWAYS use virtual environment for Python dependencies (per CLAUDE.md instructions).

```bash
# Check if venv exists
if [ ! -d venv ]; then
    echo "Creating virtual environment..."
    python -m venv venv
fi

# Activate venv (macOS/Linux)
source venv/bin/activate

# Verify activation
which python  # Should point to venv/bin/python

# Install dependencies if requirements.txt exists
if [ -f requirements.txt ]; then
    pip install -r requirements.txt
fi
```

**Windows activation**:
```bash
venv\Scripts\activate
```

### Step 5: Start Backend Service (if exists)

**Only if src/api/main.py exists**:

```bash
# Activate venv first (if not already active)
source venv/bin/activate

# Start FastAPI with uvicorn
uvicorn src.api.main:app --reload --port 8000 &

# Or if port 8000 is occupied, use alternative:
uvicorn src.api.main:app --reload --port 8001 &

# Capture background process ID
BACKEND_PID=$!
echo "Backend started with PID: $BACKEND_PID on port 8000"
```

**Verify backend is running**:
```bash
sleep 2  # Give it time to start
lsof -i :8000 | grep LISTEN && echo "✅ Backend running on port 8000"
```

### Step 6: Start Frontend Service (if exists)

**Only if frontend/index.html exists**:

```bash
# Navigate to frontend directory and start simple HTTP server
cd frontend && python -m http.server 8080 &

# Or if port 8080 is occupied:
cd frontend && python -m http.server 8081 &

# Capture background process ID
FRONTEND_PID=$!
echo "Frontend started with PID: $FRONTEND_PID on port 8080"
```

**Verify frontend is running**:
```bash
sleep 2
lsof -i :8080 | grep LISTEN && echo "✅ Frontend running on port 8080"
```

### Step 7: Report Service Status to User

Provide a clear summary with URLs and PIDs:

```markdown
✅ Services Started Successfully!

**Backend Service** (if applicable):
- Status: ✅ Running
- Port: 8000 (or alternative if conflict)
- PID: <process_id>
- URL: http://localhost:8000
- API Docs: http://localhost:8000/docs (FastAPI)
- Health Check: http://localhost:8000/health

**OR**:
- Status: ⚠️ Not implemented yet (src/api/ not found)
- Next Step: Implement Phase 2 backend

**Frontend Service**:
- Status: ✅ Running
- Port: 8080 (or alternative if conflict)
- PID: <process_id>
- URL: http://localhost:8080
- Dashboard: http://localhost:8080/index.html

**OR**:
- Status: ❌ Frontend not found

**Port Conflicts Resolved**:
- Port 8000: Was occupied by <process_name> (PID <pid>) → Killed/Alternative port used
- Port 8080: Was occupied by previous http.server → Killed and restarted

**Virtual Environment**:
- Status: ✅ Activated (venv/bin/python)
- Dependencies: ✅ Installed from requirements.txt

**Quick Links**:
- Frontend Dashboard: http://localhost:8080
- Backend API Docs: http://localhost:8000/docs
- Health Check: http://localhost:8000/health

**To Stop Services**:
```bash
# Stop backend
kill <BACKEND_PID>

# Stop frontend
kill <FRONTEND_PID>

# Or kill all Python servers
pkill -f "python -m http.server"
pkill -f "uvicorn"
```

**Next Steps**:
1. Open http://localhost:8080 in browser
2. Test frontend visualization with playback controls
3. [Project-specific next steps]
```

## Edge Cases & Error Handling

### Case 1: Virtual Environment Not Activated
```bash
# Check if venv is active
if [ -z "$VIRTUAL_ENV" ]; then
    echo "⚠️ Virtual environment not activated"
    source venv/bin/activate
fi
```

### Case 2: Dependencies Not Installed
```bash
# Check if FastAPI/uvicorn installed
python -c "import uvicorn" 2>/dev/null || {
    echo "⚠️ Dependencies not installed"
    pip install -r requirements.txt
}
```

### Case 3: Backend Crashes on Startup
```bash
# Capture startup errors
uvicorn src.api.main:app --reload --port 8000 2>&1 | tee backend.log &

# Check for errors after 2 seconds
sleep 2
if ! lsof -i :8000 | grep LISTEN; then
    echo "❌ Backend failed to start. Check backend.log"
    cat backend.log
fi
```

### Case 4: Port Already in Use (Cannot Kill)
```bash
# If lsof shows port occupied but kill fails
# Offer alternative port automatically
BACKEND_PORT=8000
while lsof -i :$BACKEND_PORT; do
    BACKEND_PORT=$((BACKEND_PORT + 1))
done
echo "Using alternative port: $BACKEND_PORT"
uvicorn src.api.main:app --reload --port $BACKEND_PORT &
```

### Case 5: Multiple Project Servers Running
```bash
# If user has multiple projects with servers running
# Show all Python servers and ask which to kill
echo "Found multiple Python servers:"
lsof -i :8000 -i :8080 -i :3000 -i :5000

# Use AskUserQuestion to confirm which to kill
```

## Project-Specific Patterns

### Pattern 1: Aviation Safety Monitor (This Project)
```bash
# Frontend only (backend not implemented yet in Phase 1)
cd frontend && python -m http.server 8080 &
echo "Frontend running at http://localhost:8080"
echo "Open dashboard at http://localhost:8080/index.html"
```

### Pattern 2: FastAPI + Frontend
```bash
# Start both services
source venv/bin/activate
uvicorn src.api.main:app --reload --port 8000 &
cd frontend && python -m http.server 8080 &
```

### Pattern 3: Flask Backend
```bash
source venv/bin/activate
python src/app.py &  # or flask run
```

### Pattern 4: Node.js Frontend
```bash
cd frontend
npm install  # if needed
npm start &  # Usually starts on port 3000
```

## Observability & Monitoring

### Health Checks
```bash
# Backend health check (if implemented)
curl http://localhost:8000/health

# Frontend availability
curl -I http://localhost:8080

# Check if services are responsive
curl -s http://localhost:8000/health | grep -q "ok" && echo "✅ Backend healthy" || echo "❌ Backend unhealthy"
```

### Process Monitoring
```bash
# Check if processes are still running
ps -p $BACKEND_PID && echo "Backend still running" || echo "Backend stopped"
ps -p $FRONTEND_PID && echo "Frontend still running" || echo "Frontend stopped"
```

### Log Tailing
```bash
# If logs are generated
tail -f backend.log &
tail -f frontend.log &
```

## Common Mistakes to Avoid

1. **DON'T kill MCP servers or system services** - Use alternative ports
2. **DON'T forget to activate venv** - Always source venv/bin/activate first
3. **DON'T assume ports are available** - Always check with lsof first
4. **DON'T start services in global Python** - Virtual environment required
5. **DON'T leave zombie processes** - Track PIDs and report them
6. **DON'T skip dependency installation** - Check requirements.txt

## Integration with Project Workflow

This skill works well with other project commands:

```bash
# Typical workflow
/recover-context              # Load project context
# [start-services skill runs]  # Start services
# [Development work]
/save-session                 # Save progress
/clear                        # Clear context
```

## Quality Gates

Before reporting success, verify:
- [ ] Virtual environment activated (if Python project)
- [ ] All port conflicts resolved
- [ ] Services actually listening on expected ports
- [ ] Health checks passing (if implemented)
- [ ] PIDs tracked and reported to user
- [ ] URLs accessible and correct

## Benefits of This Skill

1. **Prevents Port Conflicts**: Automatically detects and resolves conflicts
2. **Smart Process Management**: Distinguishes between project vs system processes
3. **Virtual Environment Safety**: Ensures venv is used (per CLAUDE.md)
4. **Clear Status Reporting**: User knows exactly what's running and where
5. **Error Recovery**: Handles common failure modes gracefully
6. **Time Savings**: Automates 5+ manual commands into one skill
7. **Consistency**: Same service startup process every session

## Notes

- This is a **project-agnostic skill** that adapts to project structure
- Reads project configuration (frontend/, src/api/, requirements.txt)
- Respects CLAUDE.md instruction: "ALWAYS use venv for Python dependencies"
- Handles partial implementations (frontend exists, backend doesn't)
- Safe for concurrent MCP servers on port 8000
- Works on macOS, Linux, Windows (with slight adaptations)

## Example Usage

### Example 1: User Explicitly Asks

**User**: "start the services"

**Claude**:
1. Check project structure (find frontend/, no backend yet)
2. Check port conflicts (find http.server on 8080 from previous session)
3. Kill old http.server process
4. Start frontend on port 8080
5. Report status with URL

### Example 2: After Session Recovery

**Context**: Just ran `/recover-context`

**Claude** (proactively):
"I'll start the services for you."
[Executes start-services skill]

### Example 3: Port Conflict with MCP Server

**Context**: Port 8000 occupied by workspace-mcp

**Claude**:
1. Detect port 8000 occupied by MCP server (PID 22880)
2. Recognize it's system service (not project-related)
3. Choose alternative port 8001 for backend
4. Report: "Port 8000 occupied by MCP server, using 8001 instead"

### Example 4: Fresh Project Setup

**Context**: Just cloned project, no venv yet

**Claude**:
1. Detect no venv exists
2. Create virtual environment
3. Install dependencies from requirements.txt
4. Start services
5. Report complete setup

## Critical Reminders

- **ALWAYS** check for port conflicts BEFORE starting services
- **ALWAYS** use virtual environment for Python projects
- **ALWAYS** track process IDs and report them
- **ALWAYS** verify services are actually listening before reporting success
- **NEVER** kill MCP servers or system services without user confirmation
- **NEVER** install to global Python (per CLAUDE.md)
- **NEVER** assume ports are available

## Debugging Commands

If services fail to start:

```bash
# Check what's using the ports
lsof -i :8000 -i :8080

# Check if venv is activated
echo $VIRTUAL_ENV

# Check if dependencies are installed
pip list | grep -E "fastapi|uvicorn"

# Check for Python syntax errors
python -m py_compile src/api/main.py

# Check for import errors
python -c "from src.api.main import app"

# Test backend manually
python -m uvicorn src.api.main:app --reload --port 8000

# Test frontend manually
cd frontend && python -m http.server 8080
```

## Version History

- **v1.0** (2025-11-14): Initial skill created based on real port conflict observations
  - Observed port 8000 conflict with workspace-mcp (PID 22880)
  - Observed port 8080 conflict with previous http.server (PID 91781)
  - Successfully resolved by killing project-owned process, respecting MCP server
