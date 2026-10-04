---
name: unity
description: "Automate Unity editor and runtime workflows with C#, Addressables, render pipelines, and batch builds."
category: game-engines
risk: safe
source: self
source_type: self
date_added: "2026-08-26"
tags: ["unity", "csharp", "editor-scripting", "urp", "addressables", "batchmode", "claude"]
tools: ["claude", "cursor", "gemini", "codex"]
---

# Unity Engine C# Editor & Runtime AI Skill Guide (Claude)

## Overview & Engine Architecture
Unity is a component-driven real-time engine with a **C# scripting layer** (Mono / IL2CPP), an **Editor extensibility surface** (`UnityEditor` namespace), and player runtimes for desktop, mobile, console, and WebGL. Projects are organized as **Scenes + Prefabs + ScriptableObjects**, with rendering via **Built-in, URP, or HDRP**. Claude operates as a Principal Unity Engineer, specializing in **Editor scripts and custom windows**, **deterministic play-mode tooling**, **Addressables content pipelines**, and **`-batchmode -quit -executeMethod` CI builds**.

### Unity Editor / Player Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                 Unity Engine Architecture                   │
│                                                             │
│  Authoring (Editor)                                         │
│  ├── UnityEditor APIs (MenuItem, EditorWindow, AssetDatabase│
│  ├── Importers, BuildPipeline, ScriptableBuildPipeline      │
│  └── Domain Reload / Enter Play Mode Options                │
│                                                             │
│  Runtime (Player)                                           │
│  ├── GameObject + MonoBehaviour / ScriptableObject          │
│  ├── SceneManager, Physics, Animation, UI Toolkit/uGUI      │
│  └── URP/HDRP Render Pipeline Asset                         │
│                                                             │
│  Content & CI                                               │
│  ├── Addressables / AssetBundles                            │
│  ├── Unity -batchmode -projectPath -executeMethod           │
│  └── IL2CPP / Mono scripting backends                       │
└─────────────────────────────────────────────────────────────┘
```

---

## Operational Capabilities & Agent Directives

1. **Editor vs Runtime Separation**: Put Editor-only code under `#if UNITY_EDITOR` or in an `Editor/` assembly; never ship `UnityEditor` references to players.
2. **AssetDatabase Hygiene**: After creating assets in Editor scripts, call `AssetDatabase.CreateAsset`, `SaveAssets`, and `Refresh` in the correct order.
3. **Build Automation**: Expose static methods for `-executeMethod` that set `BuildPlayerOptions` and return non-zero on failure via `EditorApplication.Exit(code)`.
4. **Play Mode Safety**: Avoid expensive `FindObjectOfType` loops; prefer serialized references, dependency injection, or Addressables keys.
5. **Pipeline Awareness**: Detect URP/HDRP via installed packages before recommending shader/material APIs.

---

## Production C#: Editor Menu + Batch Build Entry Point

Save as `Assets/Editor/BuildPlayerMenu.cs`:

```csharp
// ==============================================================================
// Unity Editor: menu item + CI -executeMethod build entry
// ==============================================================================
#if UNITY_EDITOR
using System.IO;
using UnityEditor;
using UnityEditor.Build.Reporting;
using UnityEngine;

public static class BuildPlayerMenu
{
    [MenuItem("Tools/Build/Windows Player")]
    public static void BuildWindowsFromMenu()
    {
        var ok = BuildWindowsInternal();
        if (!ok) Debug.LogError("Windows build failed.");
    }

    // Unity.exe -batchmode -quit -projectPath <path> -executeMethod BuildPlayerMenu.BuildWindowsCI
    public static void BuildWindowsCI()
    {
        var ok = BuildWindowsInternal();
        EditorApplication.Exit(ok ? 0 : 1);
    }

    static bool BuildWindowsInternal()
    {
        var outDir = Path.Combine("Builds", "Windows");
        Directory.CreateDirectory(outDir);

        var options = new BuildPlayerOptions
        {
            scenes = GetEnabledScenes(),
            locationPathName = Path.Combine(outDir, "Game.exe"),
            target = BuildTarget.StandaloneWindows64,
            options = BuildOptions.CompressWithLz4HC
        };

        var report = BuildPipeline.BuildPlayer(options);
        var summary = report.summary;
        Debug.Log($"Build result: {summary.result} size={summary.totalSize}");
        return summary.result == BuildResult.Succeeded;
    }

    static string[] GetEnabledScenes()
    {
        var scenes = EditorBuildSettings.scenes;
        var enabled = new System.Collections.Generic.List<string>();
        foreach (var s in scenes)
            if (s.enabled) enabled.Add(s.path);
        return enabled.ToArray();
    }
}
#endif
```

---

## Technical Troubleshooting Matrix

| Issue & Failure Signature | Root Cause Analysis | Diagnostic & Resolution Pathway |
| :--- | :--- | :--- |
| **`UnityEditor` missing in player build** | Editor script not under `Editor/` folder or asmdef. | Move to `Assets/**/Editor/` or Editor-only asmdef with `includePlatforms: Editor`. |
| **Batchmode hangs after build** | Missing `-quit` or open modal dialog. | Always pass `-quit`; avoid `EditorUtility.DisplayDialog` in CI paths. |
| **NullReference on serialized field** | Prefab/scene reference lost after reimport. | Reassign in Inspector; prefer `SerializeField` + validation `OnValidate`. |
| **Slow Enter Play Mode** | Domain reload + AssetDatabase thrash. | Enable Enter Play Mode Options; reduce static mutable state. |

---

## Essential CLI Patterns

```bash
# CI build (Windows example)
Unity.exe -batchmode -nographics -quit ^
  -projectPath "C:\work\MyGame" ^
  -executeMethod BuildPlayerMenu.BuildWindowsCI ^
  -logFile "C:\work\MyGame\Builds\build.log"
```

### Essential Paths
- **Project**: `Assets/`, `Packages/manifest.json`, `ProjectSettings/`
- **Library (generated)**: `Library/` - safe to delete to force reimport
- **Logs**: Editor.log under local AppData Unity folders

---

## Agent Operational Directive
> **MANDATORY**: Isolate Editor code from runtime assemblies. For CI, use `-batchmode -quit -executeMethod` with explicit exit codes. Prefer serialized references over scene searches in production gameplay code.
