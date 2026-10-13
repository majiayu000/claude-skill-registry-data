---
name: hud
description: Configure HUD display options (layout, presets, display elements)
argument-hint: "[setup|minimal|focused|full|status]"
role: config-writer  # DOCUMENTATION ONLY - This skill writes to ~/.copilot/ paths
scope: ~/.copilot/**  # DOCUMENTATION ONLY - Allowed write scope
level: 2
---

# HUD Skill

Configure the OMC HUD (Heads-Up Display) for the statusline.

Note: All `~/.copilot/...` paths in this guide respect `COPILOT_HOME` when that environment variable is set.

## Quick Commands

| Command | Description |
|---------|-------------|
| `/oh-my-copilot:hud` | Show current HUD status (auto-setup if needed) |
| `/oh-my-copilot:hud setup` | Install/repair HUD statusline |
| `/oh-my-copilot:hud minimal` | Switch to minimal display |
| `/oh-my-copilot:hud focused` | Switch to focused display (default) |
| `/oh-my-copilot:hud full` | Switch to full display |
| `/oh-my-copilot:hud status` | Show detailed HUD status |

## Auto-Setup

When you run `/oh-my-copilot:hud` or `/oh-my-copilot:hud setup`, the system will automatically:
1. Check if `~/.copilot/hud/omg-hud.mjs` exists
2. Check if `statusLine` is configured in `~/.copilot/settings.json`
3. If missing, create the HUD wrapper script and configure settings
4. Report status and prompt to restart Claude Code if changes were made

**IMPORTANT**: If the argument is `setup` OR if the HUD script doesn't exist at `~/.copilot/hud/omg-hud.mjs`, you MUST create the HUD files directly using the instructions below.

### Setup Instructions (Run These Commands)

**Step 1:** Check if setup is needed:
```bash
node -e "const p=require('path'),f=require('fs'),d=process.env.COPILOT_HOME||p.join(require('os').homedir(),'.copilot');console.log(f.existsSync(p.join(d,'hud','omg-hud.mjs'))?'EXISTS':'MISSING')"
```

**Step 2:** Verify the plugin is installed:
```bash
node -e "const p=require('path'),f=require('fs'),d=process.env.COPILOT_HOME||p.join(require('os').homedir(),'.copilot'),b=p.join(d,'plugins','cache','omc','oh-my-copilot');try{const v=f.readdirSync(b).filter(x=>/^\d/.test(x)).sort((a,c)=>a.localeCompare(c,void 0,{numeric:true}));if(v.length===0){console.log('Plugin not installed - run: /plugin install oh-my-copilot');process.exit()}const l=v[v.length-1],h=p.join(b,l,'dist','hud','index.js');console.log('Version:',l);console.log(f.existsSync(h)?'READY':'NOT_FOUND - try reinstalling: /plugin install oh-my-copilot')}catch{console.log('Plugin not installed - run: /plugin install oh-my-copilot')}"
```

**Step 3:** If omg-hud.mjs is MISSING or argument is `setup`, install the HUD wrapper and its dependency from the canonical template:

```bash
node -e "const p=require('path'),f=require('fs'),d=process.env.COPILOT_HOME||p.join(require('os').homedir(),'.copilot'),r=process.env.CLAUDE_PLUGIN_ROOT;if(r===undefined||r===''){console.error('ERROR: CLAUDE_PLUGIN_ROOT is not set');process.exit(1)}const hud=p.join(d,'hud');f.mkdirSync(p.join(hud,'lib'),{recursive:true});f.copyFileSync(p.join(r,'scripts','lib','hud-wrapper-template.txt'),p.join(hud,'omg-hud.mjs'));f.copyFileSync(p.join(r,'scripts','lib','config-dir.mjs'),p.join(hud,'lib','config-dir.mjs'));console.log('Installed HUD wrapper to '+p.join(hud,'omg-hud.mjs'))"
```

**IMPORTANT:** Always copy from the canonical template at `scripts/lib/hud-wrapper-template.txt`. Do NOT write the wrapper content inline — the template is the single source of truth and is guarded by drift tests (`src/__tests__/hud-wrapper-template-sync.test.ts`, `src/__tests__/paths-consistency.test.ts`).

**Step 4:** Make it executable (Unix only, skip on Windows):
```bash
node -e "if(process.platform==='win32'){console.log('Skipped (Windows)')}else{require('fs').chmodSync(require('path').join(process.env.COPILOT_HOME||require('path').join(require('os').homedir(),'.copilot'),'hud','omg-hud.mjs'),0o755);console.log('Done')}"
```

**Step 5:** Update settings.json to use the HUD:

Read `${COPILOT_HOME:-~/.copilot}/settings.json`, then update/add the `statusLine` field.

**IMPORTANT:** Do not use `~` in the command. On Unix, use `$HOME` to keep the path portable across machines. On Windows, use an absolute path because Windows does not expand `~` in shell commands.

If you are on Windows, first determine the correct path:
```bash
node -e "const p=require('path').join(require('os').homedir(),'.copilot','hud','omg-hud.mjs').split(require('path').sep).join('/');console.log(JSON.stringify(p))"
```

**IMPORTANT:** The command path MUST use forward slashes on all platforms. Claude Code executes statusLine commands via bash, which interprets backslashes as escape characters and breaks the path.

Then set the `statusLine` field. On Unix it should stay portable and look like:
```json
{
  "statusLine": {
    "type": "command",
    "command": "node ${COPILOT_HOME:-$HOME/.copilot}/hud/omg-hud.mjs"
  }
}
```

On Windows the path uses forward slashes (not backslashes):
```json
{
  "statusLine": {
    "type": "command",
    "command": "node C:/Users/username/.copilot/hud/omg-hud.mjs"
  }
}
```

Use the Edit tool to add/update this field while preserving other settings.

**Step 6:** Clean up old HUD scripts (if any):
```bash
node -e "const p=require('path'),f=require('fs'),d=process.env.COPILOT_HOME||p.join(require('os').homedir(),'.copilot'),h=p.join(d,'hud'),names=['omcp-hud.mjs','omcp-hud.js','omg-hud.js','omcp-hud-cache.sh'],removed=[];for(const n of names){const t=p.join(h,n);try{if(f.existsSync(t)){f.unlinkSync(t);removed.push(n)}}catch{}}console.log(removed.length===0?'No legacy script found':'Removed legacy '+removed.join(', '))"
```

**Step 7:** Tell the user to restart Claude Code for changes to take effect.

## Display Presets

### Minimal
Shows only the essentials:
```
[OMC] ralph | todos:2/5
```

### Focused (Default)
Shows all relevant elements:
```
[OMC] branch:main | ralph:3/10 | US-002 | skill:planner | ctx:67% | agents:2 | bg:3/5 | todos:2/5
```

### Full
Shows everything including multi-line agent details:
```
[OMC] repo:oh-my-copilot branch:main | ralph:3/10 | US-002 (2/5) | ctx:[████░░]67% | agents:3 | bg:3/5 | todos:2/5
├─ O architect    2m   analyzing architecture patterns...
├─ e explore     45s   searching for test files
└─ s executor     1m   implementing validation logic
```

## Multi-Line Agent Display

When agents are running, the HUD shows detailed information on separate lines:
- **Tree characters** (`├─`, `└─`) show visual hierarchy
- **Agent code** (O, e, s) indicates agent type with model tier color
- **Duration** shows how long each agent has been running
- **Description** shows what each agent is doing (up to 45 chars)

## Display Elements

| Element | Description |
|---------|-------------|
| `[OMC]` | Mode identifier |
| `repo:name` | Git repository name (cyan) |
| `branch:name` | Git branch name (cyan) |
| `ralph:3/10` | Ralph loop iteration/max |
| `US-002` | Current PRD story ID |
| `skill:name` | Last activated skill (cyan) |
| `effort:high` | Effort level from Claude Code (dim low, cyan medium, yellow high, magenta xhigh, bold magenta max) |
| `ctx:67%` | Context window usage |
| `agents:2` | Running subagent count |
| `bg:3/5` | Background task slots |
| `todos:2/5` | Todo completion |

## Color Coding

- **Green**: Normal/healthy
- **Yellow**: Warning (context >70%, ralph >7)
- **Red**: Critical (context >85%, ralph at max)

## Configuration Location

HUD config is stored in `~/.copilot/settings.json` under the `omcHud` key (or your custom config directory if `COPILOT_HOME` is set).

Legacy config location (deprecated): `~/.claude/.omg/hud-config.json`

## Manual Configuration

You can manually edit the config file. Each option can be set individually - any unset values will use defaults.

```json
{
  "preset": "focused",
  "elements": {
    "omcLabel": true,
    "updateNotification": true,
    "ralph": true,
    "autopilot": true,
    "prdStory": true,
    "activeSkills": true,
    "lastSkill": true,
    "contextBar": true,
    "agents": true,
    "agentsFormat": "multiline",
    "backgroundTasks": true,
    "todos": true,
    "thinking": true,
    "thinkingFormat": "text",
    "effort": true,
    "permissionStatus": false,
    "apiKeySource": false,
    "profile": true,
    "promptTime": true,
    "sessionHealth": true,
    "useBars": true,
    "showCallCounts": true,
    "callCountsFormat": "auto",
    "safeMode": true,
    "maxOutputLines": 4
  },
  "thresholds": {
    "contextWarning": 70,
    "contextCompactSuggestion": 80,
    "contextCritical": 85,
    "ralphWarning": 7
  },
  "staleTaskThresholdMinutes": 30,
  "contextLimitWarning": {
    "threshold": 80,
    "autoCompact": false
  }
}
```

### callCountsFormat

Controls the call-count badge icon style:
- `"auto"` (default): emoji on macOS/Linux, ASCII on Windows/WSL
- `"emoji"`: force `🔧 🤖 ⚡`
- `"ascii"`: force `T: A: S:`

### safeMode

When `safeMode` is `true` (default), the HUD strips ANSI codes and uses ASCII-only output to prevent terminal rendering corruption during concurrent updates. This is especially important on Windows and when using terminal multiplexers.

### agentsFormat Options

- `count`: agents:2
- `codes`: agents:Oes (type-coded with model tier casing)
- `codes-duration`: agents:O(2m)es (codes with duration)
- `detailed`: agents:[architect(2m),explore,exec]
- `descriptions`: O:analyzing code | e:searching (codes + what they're doing)
- `tasks`: [analyzing code, searching...] (just descriptions)
- `multiline`: Multi-line display with full agent details on separate lines

## Troubleshooting

If the HUD is not showing:
1. Run `/oh-my-copilot:hud setup` to auto-install and configure
2. Restart Claude Code after setup completes
3. If still not working, run `/oh-my-copilot:omc-doctor` for full diagnostics

**Legacy string format migration:** Older OMC versions wrote `statusLine` as a plain string pointing at the pre-v5 wrapper name (e.g., `"~/.claude/hud/omcp-hud.mjs"`). Modern Claude Code (v2.1+) requires an object format. Running the installer or `/oh-my-copilot:hud setup` will auto-migrate legacy strings to the correct object format:
```json
{
  "statusLine": {
    "type": "command",
    "command": "node ${COPILOT_HOME:-$HOME/.copilot}/hud/omg-hud.mjs"
  }
}
```

**Upgrading from v4 (`omcp-hud.mjs` → `omg-hud.mjs`):** v5.0.0 renamed the wrapper along with the `omcp` → `omg` command, and the old file is no longer installed. A `statusLine` left over from v4 still points at `hud/omcp-hud.mjs`, so the HUD silently renders nothing after the upgrade — the command is simply missing. Re-run `/oh-my-copilot:hud setup` to rewrite the entry, or edit `~/.copilot/settings.json` by hand and replace `hud/omcp-hud.mjs` with `hud/omg-hud.mjs`. Step 6 above also clears the stale v4 files so they cannot be picked up again.

**Node 24+ compatibility:** The HUD wrapper script imports `homedir` from `node:os` (not `node:path`). If you encounter `SyntaxError: The requested module 'path' does not provide an export named 'homedir'`, re-run the installer to regenerate `omg-hud.mjs`.

Manual verification:
- HUD script: `~/.copilot/hud/omg-hud.mjs`
- Settings: `~/.copilot/settings.json` should have `statusLine` configured as an object with `type` and `command` fields

---

*The HUD updates automatically every ~300ms during active sessions.*
