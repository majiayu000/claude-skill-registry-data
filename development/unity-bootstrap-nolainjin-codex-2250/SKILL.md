---
name: unity-bootstrap
description: Bootstrap a new Unity project for a 2D management/simulation game. Use when you need to create the Unity project, choose URP/UI approach, set up folder structure, gitignore, packages (Input System/TextMeshPro), and establish a minimal scene + tick loop scaffold before porting gameplay systems.
---

# Unity Bootstrap (2D Sim)

## 1) Create project (Unity Hub)

- Use latest Unity LTS.
- Template: `2D (URP)` if you want lighting/post; otherwise `2D Core`.
- Enable packages early: `Input System`, `TextMeshPro`.

## 2) Git setup checklist

- Add a Unity `.gitignore` (ignore `Library/`, `Temp/`, `obj/`, `Build/`, `Logs/`).
- Commit a clean baseline after first project creation.

## 3) Folder structure (recommended)

- `Assets/_Project/Scripts/{Core,Gameplay,UI}`
- `Assets/_Project/Scenes`
- `Assets/_Project/Prefabs`
- `Assets/_Project/Data` (ScriptableObjects)
- `Assets/_Project/Art`, `Assets/_Project/Audio`

## 4) Minimal runtime scaffold

- `BootScene`:
  - Loads config ScriptableObjects
  - Loads save (if exists) or creates new state
  - Loads `GameScene`
- `GameScene`:
  - Has `GameController` with:
    - Tick loop (1 sec) + time scale (1/2/6x)
    - Hooks for UI to call commands (build, assign, upgrade)

## 5) Next step

- After this, use `unity-migration` to map and port the existing JS systems.

