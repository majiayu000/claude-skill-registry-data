---
name: prism-launcher
description: Interact with, control, launch, and automate Minecraft instances via the Prism Launcher Command Line Interface (CLI). Use when launching instances, connecting to test servers on launch, importing packs/zips, selecting accounts/profiles, opening instance settings windows, locating instance IDs/folders, or automating game testing and development workflows with Prism Launcher.
---

# Prism Launcher CLI

A runbook and reference guide for automating and operating Minecraft instances using the Prism Launcher Command Line Interface (`prismlauncher`), based on the official documentation at https://prismlauncher.org/wiki/getting-started/command-line-interface/.

## When to use

- Launching a local Minecraft instance directly from the terminal or an agent workflow.
- Automating packwiz modpack testing by synchronizing configs/scripts and booting the client.
- Connecting automatically to a development or staging server (e.g., `localhost:25565`) upon launch.
- Importing instance zip archives, CurseForge packages, Modrinth `.mrpack` files, or MultiMC/Prism export archives via local path or URL.
- Selecting specific Minecraft profiles/accounts for launch.
- Opening an instance configuration and settings window without starting the game.
- Scripting health checks and process readiness using the `--alive` status beacon.

---

## Binary Resolution Across Operating Systems

Depending on your platform and installation method, resolve the executable using the following locations:

### Windows
- **Per-user install (default)**: `"$env:LOCALAPPDATA\Programs\PrismLauncher\prismlauncher.exe"`
- **System-wide install**: `"C:\Program Files\PrismLauncher\prismlauncher.exe"`
- **Scoop install**: `"$env:USERPROFILE\scoop\apps\prismlauncher\current\prismlauncher.exe"`
- **Portable**: `<portable_directory>\prismlauncher.exe`
- **PATH**: If Prism Launcher is added to system or user `PATH`, `prismlauncher` can be invoked directly.

> [!NOTE]
> On Windows, `prismlauncher.exe` is compiled as a Windows GUI subsystem application (`/SUBSYSTEM:WINDOWS`). In PowerShell, invoking it directly (`prismlauncher.exe ...`) spawns the process asynchronously in the background. To wait for the process to terminate, use `Start-Process prismlauncher -ArgumentList "..." -Wait`.
> Also note that `--help` on Windows may display a modal Qt message box dialog rather than printing to stdout.

### Linux
- **Native package (Arch, RPM, DEB, AUR)**: `prismlauncher`
- **Flatpak**: `flatpak run org.prismlauncher.PrismLauncher`
- **AppImage**: `./PrismLauncher-Linux-x86_64.AppImage`

### macOS
- **Application bundle**: `"/Applications/Prism Launcher.app/Contents/MacOS/prismlauncher"`
- **Homebrew**: `prismlauncher` (if symlinked into `/usr/local/bin` or `/opt/homebrew/bin`)

---

## Command Syntax & Options Reference

```sh
prismlauncher [-h] [-v] [-d dir] [-l launch] [-s server] [-a profile] [-I import] [--show show] [--alive] [--help-all]
```

### Full Options Matrix

| Flag / Option | Argument | Description | Requirements / Notes |
| :--- | :--- | :--- | :--- |
| `-l`, `--launch` | `<instance>` | Launch the specified instance by its **Instance ID**. | Must match the folder name under `instances/`. |
| `-s`, `--server` | `<address>` | Join the specified server address (host:port) on launch. | **Only valid in combination with `-l` / `--launch`.** |
| `-a`, `--profile` | `<profile>` | Use the account specified by its Minecraft profile name. | **Only valid in combination with `-l` / `--launch`.** Must already be authenticated in GUI. |
| `-I`, `--import` | `<file_or_url>` | Import an instance from a specified `.zip` or `.mrpack`. | Can be a local filesystem path or an HTTP/HTTPS URL. |
| `--show` | `<instance>` | Opens the Prism Launcher GUI window focused on the instance. | Opens the instance window; does not launch the game. |
| `-d`, `--dir` | `<directory>` | Use a custom directory path as the application root data directory. | Use `.` for the current working directory, or a custom folder path. |
| `--alive` | *(none)* | Writes a small `live.check` file after the launcher starts. | Useful for health checks, process readiness, and automation. |
| `-v`, `--version` | *(none)* | Displays Prism Launcher version information. | Exits after printing version. |
| `-h`, `--help` | *(none)* | Displays help on command-line options. | Exits after display. On Windows, opens a message dialog. |
| `--help-all` | *(none)* | Displays help including generic Qt toolkit options (e.g. `-platform`, `-style`). | Detailed GUI / framework options. |

---

## Instance IDs and Discovery

### What is an Instance ID?
An **Instance ID** is the exact folder name containing the instance data inside Prism Launcher's `instances/` directory. It is **not** necessarily identical to the display name if the instance was renamed or imported with special characters, though Prism frequently defaults them to match.

### Instance Directory Locations

- **Windows**: `"$env:APPDATA\PrismLauncher\instances\"` (e.g. `C:\Users\<User>\AppData\Roaming\PrismLauncher\instances\`)
- **Linux Native**: `~/.local/share/PrismLauncher/instances/`
- **Linux Flatpak**: `~/.var/app/org.prismlauncher.PrismLauncher/data/PrismLauncher/instances/`
- **macOS**: `~/Library/Application Support/PrismLauncher/instances/`

### Finding an Instance ID

1. **Via the GUI**:
   - Right-click the instance icon in Prism Launcher.
   - Click **Instance Folder** in the context menu.
   - The name of the opened folder is your Instance ID (e.g. `Perf-Shaders 1.21.1`).
2. **Via PowerShell (Windows)**:
   ```powershell
   Get-ChildItem "$env:APPDATA\PrismLauncher\instances" | Where-Object { $_.PSIsContainer } | Select-Object Name
   ```
3. **Via Python**:
   ```python
   import os
   from pathlib import Path

   appdata = os.environ.get("APPDATA")
   instances_dir = Path(appdata) / "PrismLauncher/instances"
   for inst in instances_dir.iterdir():
       if inst.is_dir():
           cfg = inst / "instance.cfg"
           name = inst.name
           if cfg.exists():
               for line in cfg.read_text(encoding="utf-8").splitlines():
                   if line.startswith("name="):
                       name = line.split("=", 1)[1]
                       break
           print(f"ID: {inst.name} | Display Name: {name}")
   ```

---

## Common Workflows & Recipes

### 1. Launching an Instance
Always wrap the instance ID in quotes if it contains spaces:

```sh
# Windows PowerShell
& "$env:LOCALAPPDATA\Programs\PrismLauncher\prismlauncher.exe" --launch "Perf-Shaders 1.21.1"

# Linux
prismlauncher --launch "Perf-Shaders 1.21.1"

# Linux (Flatpak)
flatpak run org.prismlauncher.PrismLauncher --launch "Perf-Shaders 1.21.1"

# macOS
"/Applications/Prism Launcher.app/Contents/MacOS/prismlauncher" --launch "Perf-Shaders 1.21.1"
```

### 2. Launching and Auto-Connecting to a Development Server
Ideal for testing pack multiplayer or dedicated servers (such as a local Docker test server):

```sh
# Connect to local test server on default port
prismlauncher -l "Poiesis Modded dev" -s "localhost:25565"

# Connect to a remote test server
prismlauncher -l "Poiesis Modded dev" -s "mc.example.com:25565"
```

### 3. Launching with a Specific Minecraft Account
If multiple accounts are configured in Prism Launcher:

```sh
prismlauncher -l "Poiesis Modded dev" -a "PlayerOne"
```

> [!WARNING]
> `--profile` requires the account to already have been authenticated through the Prism Launcher GUI. The CLI does not handle interactive OAuth login.

### 4. Importing Modpacks and Instance Archives
Prism Launcher can import local `.zip` or `.mrpack` files, as well as remote download URLs:

```sh
# Import local export zip
prismlauncher -I "C:\Users\User\Downloads\modpack-export.zip"

# Import from a remote URL (direct download link)
prismlauncher -I "https://example.com/builds/my-pack.mrpack"
```

### 5. Inspecting an Instance in the GUI
To open the Prism Launcher configuration / instance edit dialog directly without starting Minecraft:

```sh
prismlauncher --show "Perf-Shaders 1.21.1"
```

### 6. Using a Custom Data Directory
For portable installations or running against isolated test environments:

```sh
# Use current working directory as data root
prismlauncher -d . -l "TestInstance"

# Use explicit portable directory
prismlauncher -d "D:\PrismPortableData" -l "TestInstance"
```

### 7. Process Health / Readiness with `--alive`
When automating launcher invocations in scripts or CI:

```sh
prismlauncher --alive -l "TestInstance"
```
Prism Launcher will create a `live.check` file in the application data directory once initialization completes. Scripts can poll for this file to verify the launcher has booted.

---

## Integration with this Packwiz Repository

In this repository, local testing typically follows this cycle:

1. **Synchronize Repository Overrides to the Local Instance**:
   Run the sync script to copy `config/ftbquests`, `kubejs`, and `datapacks` into the local Prism instance:
   ```sh
   python scripts/sync_to_instance.py
   ```
2. **Launch the Instance via CLI**:
   Launch the target instance directly:
   ```powershell
   & "$env:LOCALAPPDATA\Programs\PrismLauncher\prismlauncher.exe" -l "Poiesis Modded (dev)"
   ```
3. **Test Dedicated Server Connectivity**:
   If testing a local server via `docker-compose up`:
   ```powershell
   & "$env:LOCALAPPDATA\Programs\PrismLauncher\prismlauncher.exe" -l "Poiesis Modded (dev)" -s "localhost:25565"
   ```

---

## Quirks, Pitfalls & Known Behaviors

### 1. Launcher Re-Opening After Minecraft Closes
**Symptom**: When closing Minecraft after launching via CLI, the Prism Launcher main GUI window unexpectedly pops up.
**Cause**: The setting *"Close Prism Launcher after game window opens"* causes Prism Launcher to reopen after Minecraft exits, even when the instance was invoked headlessly via the CLI.
**Fix**:
1. Open Prism Launcher **Settings**.
2. Select **Minecraft**.
3. Uncheck **Close Prism Launcher after game window opens**, or check **Quit the launcher after game window closes**.

### 2. PowerShell / Command Prompt Non-Blocking Execution
On Windows, executing `prismlauncher.exe` inside PowerShell or CMD will immediately return the command prompt because it is a GUI subsystem binary. If your script or agent needs to block until Minecraft exits:
```powershell
Start-Process -FilePath "$env:LOCALAPPDATA\Programs\PrismLauncher\prismlauncher.exe" -ArgumentList "-l", "Poiesis Modded (dev)" -Wait
```

### 3. Whitespace in Instance Names
Instance IDs frequently contain spaces (e.g. `Perf-Shaders 1.21.1`). Always quote the argument to `-l`, `--launch`, and `--show`:
```sh
# Correct
prismlauncher -l "Perf-Shaders 1.21.1"

# Incorrect (will attempt to launch 'Perf-Shaders' and fail)
prismlauncher -l Perf-Shaders 1.21.1
```
