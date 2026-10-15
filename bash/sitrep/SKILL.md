---
name: sitrep
description: Generate a situational report from live system state. READ-ONLY — no writes, no fixes. Trigger when user asks for status, "what's going on?", "where are we?", or "catch me up".
version: 1.1.0
execution-mode: advisory
argument-hint: "[--brief]"
category: fleet-ops
status: candidate
providers:
  required: [python]
---

# sitrep

Generate a situational report from live system state. READ-ONLY — no writes, no fixes.

## Trigger

User types `/sitrep` or asks for status, "what's going on?", "where are we?", or "catch me up".

## Usage

```
/sitrep              # Full report (default)
/sitrep --brief      # Alerts only, one-line summary per section
```

> **Note**: `--since` is not yet implemented. Use git log or bus tail manually for deltas.

## Modes

### Full mode (default)
Run all data collection sections and emit the complete formatted report.

### Brief mode (`--brief`)
Skip detailed per-section output. Emit only:
- Machine identity line
- Branch + dirty count
- Bus entry count + blocker count
- Service status table
- Disk line with alert badge
- Alerts section (this is the primary output in brief mode)

When `--brief` is passed, the agent should print the alerts section first, then the one-line summaries, then exit. No process lists, no commit details, no bus message content.

## Protocol

1. Gather state from multiple sources (parallel where possible).
2. Never fabricate output — run actual commands.
3. Never write to disk, post to bus, or kill processes.
4. If a command fails, report the failure inline.
5. Flag disk > 85% as WARN, > 92% as CRIT.
6. Ollama on a GPU host (Workstation) is expected UP; on non-GPU hosts flag as WARN if down.

## Platform Detection

Detect platform before running commands. The fleet has three OS targets:

| Machine | OS | Shell | Canonical `$HOME` |
|---------|----|-------|-------------------|
| Workstation | Windows 11 | git-bash + PowerShell | `$HOME` |
| Huxley | macOS 13 | zsh | `/Users/owner` |
| remote-node (dormant since 2026-07-01) | macOS 15 | zsh | `$REMOTE_HOST` |

Use this guard pattern at the top of every `/sitrep` invocation:

```python
import platform, os, sys

PLATFORM = platform.system().lower()  # "windows", "darwin", "linux"
IS_MSYS = os.environ.get("MSYSTEM") is not None or sys.platform == "msys"
HOME = os.path.expanduser("~")
```

All shell snippets below are written with platform branches.

---

## Data Collection

Run every section. If a probe fails, report `ERR: <message>`.

### 1. Project Root Discovery

```python
import subprocess, os, pathlib

def find_project_root():
    # 1. Cwd if inside a git repo
    try:
        out = subprocess.check_output(
            ["git", "rev-parse", "--show-toplevel"],
            stderr=subprocess.DEVNULL,
            text=True,
        ).strip()
        if out:
            return pathlib.Path(out)
    except Exception:
        pass
    # 2. CORPUS_ROOT env var
    if os.environ.get("CORPUS_ROOT"):
        return pathlib.Path(os.environ["CORPUS_ROOT"])
    # 3. PROJECTS_DIR env var + hummbl-governance
    base = os.environ.get("PROJECTS_DIR") or os.path.expanduser("~/PROJECTS")
    for candidate in ["hummbl-governance", "corpus"]:
        p = pathlib.Path(base) / candidate
        if (p / ".git").exists() or (p / "manifest.json").exists():
            return p
    return None

PROJECT_ROOT = find_project_root()
```

### 2. Git State

**Windows (PowerShell via `agent-powershell.ps1` or direct `pwsh`):**
```powershell
$branch = git -C "$PROJECT_ROOT" rev-parse --abbrev-ref HEAD 2>$null
if (-not $branch) { $branch = "unknown" }
git -C "$PROJECT_ROOT" log --oneline -5
git -C "$PROJECT_ROOT" status --short | Measure-Object -Line
```

**Unix (bash/zsh):**
```bash
branch=$(git -C "$PROJECT_ROOT" rev-parse --abbrev-ref HEAD 2>/dev/null || echo "unknown")
git -C "$PROJECT_ROOT" log --oneline -5
git -C "$PROJECT_ROOT" status --short | wc -l | tr -d ' '
```

### 3. Bus Activity

Scan multiple candidate paths. The canonical bus was retired 2026-04-21; live paths vary by machine.

**Candidates (checked in order):**
1. `$CORPUS_ROOT/_state/coordination/messages.tsv`
2. `$PROJECT_ROOT/hummbl_governance/_state/coordination/messages.tsv`
3. `$HOME/.agents/bus/messages.tsv`
4. `$HOME/_state/coordination/messages.tsv`
5. remote-node bridge: `python $HOME/bin/bus-global.py list --limit 5` (if SSH/remote-node reachable — **remote-node dormant since 2026-07-01, expected UNREACHABLE**)

**Windows:**
```powershell
$busPaths = @(
    "$env:CORPUS_ROOT\_state\coordination\messages.tsv",
    "$env:PROJECT_ROOT\hummbl_governance\_state\coordination\messages.tsv",
    "$HOME\.agents\bus\messages.tsv",
    "$HOME\_state\coordination\messages.tsv"
)
$foundBus = $null
foreach ($p in $busPaths) {
    if (Test-Path $p) { $foundBus = $p; break }
}
if ($foundBus) {
    (Get-Content $foundBus).Count
    Get-Content $foundBus | Select-Object -Last 5
} else {
    echo "Bus: no local TSV found"
}
```

**Unix:**
```bash
bus_paths=(
    "${CORPUS_ROOT:-}/_state/coordination/messages.tsv"
    "${PROJECT_ROOT:-}/hummbl_governance/_state/coordination/messages.tsv"
    "$HOME/.agents/bus/messages.tsv"
    "$HOME/_state/coordination/messages.tsv"
)
found_bus=""
for p in "${bus_paths[@]}"; do
    if [ -f "$p" ]; then found_bus="$p"; break; fi
done
if [ -n "$found_bus" ]; then
    wc -l < "$found_bus"
    tail -5 "$found_bus"
else
    echo "Bus: no local TSV found"
fi
```

**Blockers:** Search last 10 lines for `BLOCKED` type.

### 4. Services

**Discovery approach:** Check configurable ports via `netstat` / `Get-NetTCPConnection` / `lsof`. Do NOT assume hardcoded ports are correct on every machine.

**Port map (read from env first, fallback to known defaults):**

| Service | Env Var | Default | Machine Context |
|---------|---------|---------|-----------------|
| Ollama | `OLLAMA_HOST` | `localhost:11434` | Workstation (GPU host) = expected; others = optional |
| Gitea | `GITEA_URL` | `localhost:3030` | Workstation only |
| remote-node bus bridge | `BUS_BRIDGE` | `maks-mac-mini:18790` | Mesh-wide (remote-node dormant since 2026-07-01 — use Workstation as bus authority) |
| Tailscale | — | `tailscaled` daemon | Mesh-wide |

**Windows probe:**
```powershell
function Test-Port($hostName, $port) {
    try {
        $conn = Test-NetConnection -ComputerName $hostName -Port $port -WarningAction SilentlyContinue
        if ($conn.TcpTestSucceeded) { "UP" } else { "DOWN" }
    } catch { "ERR" }
}
Test-Port "localhost" 11434
Test-Port "localhost" 3030
Test-Port "maks-mac-mini" 18790  # remote-node dormant since 2026-07-01 — expected DOWN
```

**Unix probe:**
```bash
test_port() {
    timeout 2 bash -c "</dev/tcp/$1/$2" 2>/dev/null && echo "UP" || echo "DOWN"
}
test_port localhost 11434
test_port localhost 3030
test_port maks-mac-mini 18790  # remote-node dormant since 2026-07-01 — expected DOWN
```

**Ollama policy:**
- If machine hostname is `workstation` OR `nvidia-smi` is available → Ollama expected UP. Flag as WARN if DOWN.
- Otherwise Ollama is optional. Flag as INFO if DOWN.

### 5. Running Agents / Processes

**Windows:**
```powershell
Get-Process | Where-Object {
    $_.ProcessName -match "claude|codex|devin|gemini|node|python|ollama"
} | Select-Object ProcessName, Id, @{N="CPU(s)";E={[math]::Round($_.CPU,1)}}, @{N="WS_MB";E={[math]::Round($_.WorkingSet/1MB,1)}}
```

**Unix:**
```bash
ps aux | grep -iE "claude|codex|devin|gemini|node|python|ollama" | grep -v grep | awk '{print $11, $2, $3, $6}'
```

### 6. Disk Pressure

**Windows:**
```powershell
Get-CimInstance Win32_LogicalDisk | Where-Object { $_.DeviceID -eq 'C:' } |
    Select-Object DeviceID,
        @{N="SizeGB";E={[math]::Round($_.Size/1GB,1)}},
        @{N="FreeGB";E={[math]::Round($_.FreeSpace/1GB,1)}},
        @{N="Used%";E={[math]::Round(($_.Size-$_.FreeSpace)/$_.Size*100,1)}}
```

**Unix:**
```bash
df -h / | tail -1 | awk '{print $5, $4}'
```

**Alert thresholds:**
- `Used% < 70%` → OK
- `Used% 70–84%` → OK (note)
- `Used% 85–91%` → WARN
- `Used% >= 92%` → CRIT

### 7. Skill / Fleet Surface (Optional but useful)

Count installed skills:

**Windows:**
```powershell
$skillRoots = @("$HOME/.devin/skills", "$HOME/.claude/skills", "$HOME/.agents/skills")
$count = 0
foreach ($r in $skillRoots) {
    if (Test-Path $r) {
        # -Depth 1 prevents recursion into nested skill subdirectories
        $count += (Get-ChildItem -Directory $r -Depth 0).Count
    }
}
$count
```

**Unix:**
```bash
find "$HOME/.devin/skills" "$HOME/.claude/skills" "$HOME/.agents/skills" -maxdepth 1 -type d 2>/dev/null | wc -l
```

---

## Output Format

```
SITREP | <YYYY-MM-DD HH:MM> <TZ>
Machine: <hostname> | <OS> | <platform>
==============================

## Git
Branch: <branch>
Project root: <path or "unknown">
Last 5 commits:
  <hash> <msg>
Dirty: <N files> [list if < 10]

## Coordination Bus
Local TSV: <path or "not found">
Entries: <N> total
Recent (last 5):
  <timestamp> <from> <to> <type> <msg_truncated>
Blockers: <N recent BLOCKED or "none">

## Services
| Service          | Target           | Status | Notes                |
|------------------|------------------|--------|----------------------|
| Ollama           | <host>:<port>    | UP/DOWN| expected/optional    |
| Gitea            | <host>:<port>    | UP/DOWN| Workstation-only           |
| Bus bridge       | <host>:<port>    | UP/DOWN| remote-node dormant since 2026-07-01 — Workstation is bus authority |
| Tailscale daemon | —                | UP/DOWN| mesh connectivity    |

Agents: <list of running agent processes or "none detected">

## Disk
<drive>: <Used%>% (<FreeGB> GB free of <SizeGB> GB) [OK/WARN/CRIT]

## Fleet Surface
Skills installed: <N>

## Alerts
- <one per line, or "All clear.">
```

## Constraints

- READ-ONLY. Never fix, never write, never post.
- If Ollama is UP on agent-node → normal. If Ollama is DOWN on agent-node → WARN.
- If bus TSV is missing → report "not configured" rather than error.
- If `git` fails inside project root → report "not a git repo" and continue.
- Do not fabricate timestamps, commit hashes, or process counts.
- Keep output scannable in < 10 seconds.

## Changelog

- 2026-06-15 v1.1 — Fixed Windows skill count recursion (`-Depth 0`). Added `--brief` mode protocol. Removed unimplemented `--since` from usage.
- 2026-06-15 v1.0 — Rewritten for cross-platform fleet (Windows/macOS/Linux). Replaced Unix-only commands with platform branches. Added bus path fallback chain. Added Ollama context-aware policy. Added project root auto-discovery.
