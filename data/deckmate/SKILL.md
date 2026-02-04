---
name: deckmate
description: Stream Deck integration assistant for VSCode. Create, manage, and organize Stream Deck profiles, buttons, snippets, and scripts. Helps build productivity workflows for developers using Stream Deck with Claude Code and TAC (Tactical Agentic Coding) patterns.
license: MIT
version: 2.0.0
---

# DeckMate - Stream Deck Integration Assistant

DeckMate helps you create and manage Stream Deck integrations for VSCode and Claude Code workflows. It understands both the native Stream Deck profile format AND provides tooling for developer workflow integrations.

## When to Use This Skill

Use this skill when:
- Creating new Stream Deck profiles for development workflows
- Adding buttons, snippets, or scripts for Stream Deck
- Setting up TAC (Tactical Agentic Coding) integrations
- Understanding the Stream Deck profile format
- Building automation scripts triggered by Stream Deck
- Converting integration blueprints to actual profiles

## Stream Deck Profile Format (Native)

### File Structure

Stream Deck profiles are `.streamDeckProfile` files, which are **ZIP archives** containing:

```
ProfileName.streamDeckProfile (ZIP)
└── {UUID}.sdProfile/
    ├── manifest.json              # Profile metadata
    └── Profiles/
        └── {PAGE_ID}/
            ├── manifest.json      # Button/action configuration
            └── Images/
                └── *.png          # Button icons (72x72 or 144x144)
```

### Root Manifest Schema

`{UUID}.sdProfile/manifest.json`:

```json
{
  "Device": {
    "Model": "20GBD9901",
    "UUID": ""
  },
  "Name": "Profile Name",
  "Pages": {
    "Current": "page-uuid-here",
    "Pages": ["page-uuid-here", "another-page-uuid"]
  },
  "Version": "2.0"
}
```

**Device Models:**
- `20GBD9901` - Stream Deck (15 keys)
- `20GAT9901` - Stream Deck Mini (6 keys)
- `20GAV9901` - Stream Deck XL (32 keys)
- `20GBA9901` - Stream Deck + (8 keys + 4 dials)
- `20GAA9901` - Stream Deck Mobile

### Page Manifest Schema

`Profiles/{PAGE_ID}/manifest.json`:

```json
{
  "Controllers": [
    {
      "Type": "Keypad",
      "Actions": {
        "0,0": { /* Action at row 0, col 0 */ },
        "0,1": { /* Action at row 0, col 1 */ },
        "1,0": { /* Action at row 1, col 0 */ }
      }
    },
    {
      "Type": "Encoder",
      "Actions": {
        "0,0": { /* Dial 1 */ },
        "1,0": { /* Dial 2 */ }
      }
    }
  ]
}
```

### Action Schema

Each action in the `Actions` object:

```json
{
  "ActionID": "unique-uuid-here",
  "LinkedTitle": false,
  "Name": "Display Name",
  "Settings": {
    /* Action-specific settings */
  },
  "State": 0,
  "States": [
    {
      "Image": "Images/filename.png",
      "Title": "Button Label",
      "FontFamily": "",
      "FontSize": 12,
      "FontStyle": "",
      "FontUnderline": false,
      "ShowTitle": true,
      "TitleAlignment": "bottom",
      "TitleColor": "#ffffff",
      "OutlineThickness": 2
    }
  ],
  "UUID": "com.elgato.streamdeck.system.hotkey"
}
```

## Built-in Action UUIDs

### System Actions

| UUID | Name | Description |
|------|------|-------------|
| `com.elgato.streamdeck.system.hotkey` | Hotkey | Send keyboard shortcut |
| `com.elgato.streamdeck.system.hotkeyswitch` | Hotkey Switch | Toggle between two hotkeys |
| `com.elgato.streamdeck.system.open` | Open | Open file/folder/URL |
| `com.elgato.streamdeck.system.website` | Website | Open URL in browser |
| `com.elgato.streamdeck.system.text` | Text | Type text string |
| `com.elgato.streamdeck.system.multimedia` | Multimedia | Media controls |
| `com.elgato.streamdeck.profile.backtoparent` | Back | Navigate to parent folder |
| `com.elgato.streamdeck.profile.openchild` | Open Folder | Navigate to subfolder |

### Hotkey Settings

```json
{
  "Settings": {
    "Coalesce": true,
    "Hotkeys": [
      {
        "KeyCmd": false,
        "KeyCtrl": true,
        "KeyModifiers": 2,
        "KeyOption": false,
        "KeyShift": false,
        "NativeCode": 67,
        "QTKeyCode": 67,
        "VKeyCode": 67
      }
    ]
  }
}
```

**KeyModifiers Bitmask:**
- 1 = Shift
- 2 = Ctrl
- 4 = Alt/Option
- 8 = Cmd/Win

**Common VKeyCodes:**
- A-Z: 65-90
- 0-9: 48-57
- F1-F12: 112-123
- Enter: 13
- Tab: 9
- Space: 32
- Escape: 27

### Open Action Settings

```json
{
  "Settings": {
    "openInBrowser": false,
    "path": "/path/to/file/or/folder"
  }
}
```

### Text Action Settings

```json
{
  "Settings": {
    "text": "Text to type"
  }
}
```

### Website Action Settings

```json
{
  "Settings": {
    "openInBrowser": true,
    "url": "https://example.com"
  }
}
```

## Developer Integration Files

For complex developer workflows, DeckMate uses **Integration Definition** files (JSON) that serve as blueprints. These are NOT native Stream Deck profiles but documentation/configuration that can be used to:

1. Document intended integrations
2. Generate scripts and snippets
3. Provide context for manual Stream Deck setup
4. Track TAC leverage points

### Integration Definition Structure

```
streamdeck/
├── profiles/                    # Integration blueprints (NOT native profiles)
│   └── tac-lesson4-integrations.json
├── snippets/                    # Text content for Text actions
│   └── piter-framework.md
├── scripts/                     # Shell scripts for hotkey-triggered terminals
│   └── adw-plan-build.sh
└── vscode/
    └── snippets.code-snippets   # VSCode autocomplete snippets
```

### Integration Definition Schema

```json
{
  "name": "Integration Set Name",
  "description": "What this set provides",
  "version": "1.0.0",
  "source_lesson": "lessons/lesson-N.md",
  "buttons": [
    {
      "position": 0,
      "name": "Button Name",
      "icon": "emoji-hint",
      "type": "hotkey|text|open|website|script",
      "action": {
        /* Type-specific configuration */
      },
      "leverage_point": "TAC LP reference",
      "priority": "high|medium|low"
    }
  ],
  "snippets": [
    {
      "name": "Snippet Name",
      "file": "snippets/filename.ext",
      "trigger": "vscode-prefix"
    }
  ]
}
```

## Creating Stream Deck Actions for Developers

### Terminal Command via Hotkey + Script

1. Create a shell script in `streamdeck/scripts/`:
```bash
#!/bin/bash
# my-command.sh
claude "/chore $1"
```

2. Create a keyboard shortcut in your terminal app to run the script

3. Configure Stream Deck hotkey to trigger that shortcut

### Text Injection (Snippets)

Use the `com.elgato.streamdeck.system.text` action:

```json
{
  "UUID": "com.elgato.streamdeck.system.text",
  "Settings": {
    "text": "## PITER Framework\n\n### P - Prompt Input\n..."
  }
}
```

### Open VSCode Folder

Use the `com.elgato.streamdeck.system.open` action:

```json
{
  "UUID": "com.elgato.streamdeck.system.open",
  "Settings": {
    "openInBrowser": false,
    "path": "/path/to/project/specs"
  }
}
```

### Launch Terminal with Command

**Option 1: Using Open action with terminal app**
```json
{
  "UUID": "com.elgato.streamdeck.system.open",
  "Settings": {
    "path": "/usr/bin/wt",
    "arguments": "-w 0 nt claude"
  }
}
```

**Option 2: Multi-action with hotkey sequence**
1. Open terminal (Ctrl+`)
2. Type command text
3. Send Enter

## TAC Leverage Points Reference

When creating integrations, tag them appropriately:

| LP | Name | Stream Deck Use Case |
|----|------|---------------------|
| 1 | Context | Open ai_docs/, load context files |
| 2 | Model | - |
| 3 | Prompt | Text injection of prompts |
| 4 | Tools | Launch Claude, terminal commands |
| 5 | Standard Out | Status posting scripts |
| 6 | Types | Open type definition files |
| 7 | Documentation | Open docs folders |
| 8 | Tests | Run test scripts |
| 9 | Architecture | Navigate project structure |
| 10 | Plans | Open specs/, create plans |
| 11 | Templates | Inject slash commands |
| 12 | ADWs | Launch ADW workflows |

## Common Developer Patterns

### Launch Claude Interactive

```json
{
  "UUID": "com.elgato.streamdeck.system.open",
  "Name": "Claude",
  "Settings": {
    "path": "/path/to/terminal",
    "arguments": "claude"
  }
}
```

### Inject Slash Command

```json
{
  "UUID": "com.elgato.streamdeck.system.text",
  "Name": "/chore",
  "Settings": {
    "text": "/chore "
  }
}
```

### Open Project Folder

```json
{
  "UUID": "com.elgato.streamdeck.system.open",
  "Name": "Specs",
  "Settings": {
    "path": "/home/user/project/specs"
  }
}
```

### Git Quick Commit (Multi-Action)

Use Stream Deck's Multi-Action to chain:
1. Hotkey: Ctrl+` (open terminal)
2. Text: `git add -A && git commit -m ""`
3. Hotkey: Left Arrow (position cursor)

## Creating a Profile Programmatically

### Python Helper

```python
import json
import zipfile
import uuid
import os

def create_profile(name: str, buttons: list, device_model: str = "20GBD9901"):
    """Create a .streamDeckProfile file."""
    profile_uuid = str(uuid.uuid4()).upper()
    page_uuid = str(uuid.uuid4())

    # Root manifest
    root_manifest = {
        "Device": {"Model": device_model, "UUID": ""},
        "Name": name,
        "Pages": {"Current": page_uuid, "Pages": [page_uuid]},
        "Version": "2.0"
    }

    # Build actions from buttons
    actions = {}
    for btn in buttons:
        pos = f"{btn['row']},{btn['col']}"
        actions[pos] = {
            "ActionID": str(uuid.uuid4()),
            "LinkedTitle": False,
            "Name": btn["name"],
            "Settings": btn.get("settings", {}),
            "State": 0,
            "States": [{
                "Title": btn["name"],
                "ShowTitle": True,
                "TitleAlignment": "bottom",
                "TitleColor": "#ffffff"
            }],
            "UUID": btn["uuid"]
        }

    # Page manifest
    page_manifest = {
        "Controllers": [{"Type": "Keypad", "Actions": actions}]
    }

    # Create ZIP
    with zipfile.ZipFile(f"{name}.streamDeckProfile", "w") as zf:
        sd_dir = f"{profile_uuid}.sdProfile"
        zf.writestr(f"{sd_dir}/manifest.json", json.dumps(root_manifest))
        zf.writestr(f"{sd_dir}/Profiles/{page_uuid}/manifest.json", json.dumps(page_manifest))

    return f"{name}.streamDeckProfile"
```

### Usage

```python
buttons = [
    {
        "row": 0, "col": 0,
        "name": "Claude",
        "uuid": "com.elgato.streamdeck.system.open",
        "settings": {"path": "/usr/bin/claude"}
    },
    {
        "row": 0, "col": 1,
        "name": "/chore",
        "uuid": "com.elgato.streamdeck.system.text",
        "settings": {"text": "/chore "}
    }
]

create_profile("TAC Developer", buttons)
```

## Workflow: From Integration Definition to Profile

1. **Define integrations** in `profiles/*.json` (blueprint)
2. **Create supporting files** (scripts, snippets)
3. **Generate or manually create** `.streamDeckProfile`
4. **Import** into Stream Deck app

## Best Practices

### Button Layout (15-key Stream Deck)

```
Row 0: [High Priority Actions - Most Used]
Row 1: [Medium Priority - Regular Use]
Row 2: [Low Priority / Navigation]
```

### Icon Guidelines

- Size: 72x72 (standard) or 144x144 (retina)
- Format: PNG with transparency
- Style: Simple, high-contrast icons
- Text: Avoid text in icons, use Title instead

### Naming Conventions

- **Buttons**: Short (1-2 words), action-oriented
- **Scripts**: `kebab-case.sh` (e.g., `run-tests.sh`)
- **Snippets**: Descriptive with extension (e.g., `piter-framework.md`)

## Troubleshooting

### Profile Won't Import

- Verify ZIP structure is correct
- Check `manifest.json` syntax
- Ensure Device Model matches your hardware

### Button Does Nothing

- Check action UUID is valid
- Verify Settings match action type
- For hotkeys, verify key codes

### Script Not Running

```bash
chmod +x scripts/my-script.sh
```

## Commands

DeckMate responds to these requests:

- "Create a Stream Deck hotkey for [shortcut]"
- "Add a text injection button for [content]"
- "Generate a profile from my integration definition"
- "What UUID do I need for [action type]?"
- "Show me the Stream Deck profile structure"
- "Create a button that opens [folder]"
- "What's the key code for [key]?"
