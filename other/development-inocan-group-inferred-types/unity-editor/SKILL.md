---
name: unity-editor
description: Remote control Unity Editor via CLI using unityctl. Use when working with Unity projects to enter/exit play mode, compile scripts, view console logs, load scenes, run tests, capture screenshots, or execute C# code for debugging. Activate when user mentions Unity, play mode, compilation, or needs to interact with a running Unity Editor.
---

# unityctl - Unity Editor Remote Control

Control a running Unity Editor from the command line without batch mode.

## Instructions

### Setup (Required First)

1. Start the bridge daemon: `unityctl bridge start` (make sure to background this or it will time out)
2. Open the Unity project in Unity Editor
3. Verify connection: `unityctl status`

### Critical: Compile Before Play Mode

After modifying ANY C# scripts, you MUST compile before entering play mode:

```bash
unityctl compile scripts
```

This refreshes assets and triggers compilation. Play mode will use stale code otherwise.

### Common Commands

**Status & Bridge:**
```bash
unityctl status           # Check Unity running, bridge, and connection status
unityctl bridge start     # Start bridge daemon (runs in background)
unityctl bridge stop      # Stop bridge
```

**Play Mode:**
```bash
unityctl play enter       # Enter play mode
unityctl play exit        # Exit play mode
unityctl play toggle      # Toggle play mode
```

**Console:**
```bash
unityctl console tail              # Show recent logs (default: 10 entries)
unityctl console tail --count 100  # More log entries
unityctl console tail --stack      # Include stack traces
unityctl console clear             # Clear the console log buffer
```

**Scenes:**
```bash
unityctl scene list                            # List scenes
unityctl scene load Assets/Scenes/Main.unity   # Load scene
```

**Testing:**
```bash
unityctl test run                    # Run edit mode tests
unityctl test run --mode playmode    # Play mode tests
```

**Screenshots:**
```bash
unityctl screenshot capture          # Capture screenshot
```

### Script Execution (Debugging Power Tool)

Execute arbitrary C# in the running editor via Roslyn. Invaluable for debugging and automation.

```bash
unityctl script execute -c "using UnityEngine; public class Script { public static object Main() { return Application.version; } }"
```

### Getting Help

```bash
unityctl --help              # List all commands
unityctl <command> --help    # Command-specific help
```

## Examples

**Workflow: Edit script, compile, and test:**
```bash
# After editing C# files...
unityctl compile scripts
unityctl play enter
unityctl console tail --count 50
unityctl play exit
```

**Debug: Find all GameObjects in scene:**
```bash
unityctl script execute -c "using UnityEngine; public class Script { public static object Main() { return GameObject.FindObjectsOfType<GameObject>().Length; } }"
```

**Debug: Inspect Player position:**
```bash
unityctl script execute -c "using UnityEngine; public class Script { public static object Main() { var go = GameObject.Find(\"Player\"); return go?.transform.position.ToString() ?? \"not found\"; } }"
```

**Debug: Log message to Unity console:**
```bash
unityctl script execute -c "using UnityEngine; public class Script { public static object Main() { Debug.Log(\"Hello from CLI\"); return \"logged\"; } }"
```

## Best Practices

- Run `unityctl status` to check overall project status before running commands
- Always run `unityctl compile scripts` after modifying C# files before entering play mode
- Use `unityctl console tail` to monitor logs after compiling and during play mode
- Script execution requires a class with a static method; return values are JSON-serialized
- Domain reload after compilation is normal; the bridge auto-reconnects

## Troubleshooting

Run `unityctl status` first to diagnose issues.

| Problem | Solution |
|---------|----------|
| Bridge not responding | `unityctl bridge stop` then `unityctl bridge start` |
| Commands timing out | Ensure Unity Editor is responsive |
| Connection lost after compile | Normal - domain reload. Auto-reconnects. |
| "Project not found" | Run from project directory or use `--project` flag |
