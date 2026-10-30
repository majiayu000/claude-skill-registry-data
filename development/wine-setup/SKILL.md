---
name: wine-setup
description: "Full Wine setup on Fedora for Windows games and repacks: install wine/winetricks + missing components (MFC42, VC++ runtimes, DirectX, corefonts, d3dx), map a folder as an extra drive (D:/E: → the configured mount point via dosdevices symlinks), and diagnose/fix broken installers (Inno Setup/xatab repacks: \"MFC42.DLL not found\", isskin.dll, silent exit of setup.exe). Use when the user says wine won't run, a game setup.exe doesn't start, a repack fails, needs to install to another drive, or \"the game won't install\", \"in Wine\"."
---


# Wine setup & game install fixes (Fedora)

Goal: get Windows game installers (especially Russian repacks: xatab,
R.G. Mechanics, etc.) running under Wine on Fedora.

## 1. Baseline install (if wine/winetricks missing)

```bash
sudo dnf install wine winetricks
```

Check state: `wine --version`, `ls ~/.wine/drive_c/windows/system32/`.
Default prefix is `~/.wine`. For games, consider a dedicated prefix:
`WINEPREFIX=~/Games/wine-games` (its own `dosdevices/`, `drive_c/`).
Components are installed per-prefix — if a game fails, the component was
installed into the WRONG prefix (or the default one you don't use).

## 2. Mapping an extra drive (D:, E:, ...) — install games to DATA

Wine drives are symlinks in `~/.wine/dosdevices/`. `C:` → `../drive_c` by
default. Any Linux folder can become a drive:

```bash
cd ~/.wine/dosdevices
ln -s <path-to-disk> d:   # for example /run/media/$USER/DATA      # install games to D:\Games\...
```

Rules:

- A drive symlink whose target does not exist/is not a directory confuses
  installers (they only offer C:). Fix by remapping, not by "choosing C:".
- Existing `d:` may point to a raw device (e.g. `/dev/sdc`) — dead mapping;
  remove and re-link to the real folder.
- Multiple data folders: add more (e: → <another-folder>, etc.).
- Verify: `wine cmd /c dir d:\` or `ls -la ~/.wine/dosdevices/d:`.
- NTFS/FAT data drives mounted by the system work too — the symlink just
  points at the mountpoint (e.g. `/run/media/$USER/DATA`).

## 3. Diagnosing a setup.exe that won't run

Run in terminal, capture stderr:

```bash
cd "/path/to/repack" && wine setup.exe 2>&1 | grep -iE "err|not found|fixme:module"
```

Known failure signature (xatab/Inno Setup repacks with skins):

```
err:module:import_dll Library MFC42.DLL (which is needed by L"...
\Temp\is-XXXX.tmp\isskin.dll") not found
```

→ Inno Setup skin (`isskin.dll`) needs the ancient VC6 runtime `MFC42.DLL`.
The installer silently dies → "setup.exe won't start/nothing happens".
Fix:

```bash
winetricks -q mfc42    # installs mfc42.dll into system32/syswow64
```

(winetricks downloads from Microsoft; needs internet. Requires wine prefix
closed during install — run `wineserver -k` first if needed.)

Re-run setup.exe and verify the error is gone. If MFC42 was already there,
check next missing DLL in the same error line and add it
(`winetricks -q vcrun2008 vcrun2010 vcrun2019` etc.).

## 4. Missing component catalog (winetricks names)

Common game/repack needs:

- `mfc42` — VC6 MFC runtime (Inno Setup skins: isskin.dll, xatab repacks)
- `vcrun6 vcrun2005 vcrun2008 vcrun2010 vcrun2013 vcrun2019` — MSVC runtimes
- `d3dx9 d3dx10 d3dx11_43` — DirectX 9/10/11 DLLs
- `dxvk` — Vulkan translation for D3D9-11 (big perf win; needs Vulkan drivers)
- `corefonts` — Times/Comic etc. (text/menus invisible fix)
- `directx9` — full DirectX 9 end-user runtime (old games)
- `dotnet48` — .NET Framework (needed by some installers/launchers)
- `physx` — PhysX runtime (old games need DLLs)

One-liner for a typical "old game repack":

```bash
winetricks -q mfc42 corefonts vcrun2008 d3dx9
```

## 5. After installing the game

- Install path on D: survives; game data lives outside the prefix.
- Run the game with the same prefix as setup used (default `~/.wine`).
- Check `winecfg` → Graphics for desktop emulation/override if fullscreen
  games fail; `winetricks dxvk` for 3D games if stutter/low FPS.
- Restart wine between component installs and game launches
  (`wineserver -k` if a process hangs).

## This box's facts (verified 2026-08)

- wine-11.0 (Staging), winetricks 20260125, default prefix `~/.wine`.
- `D:` was remapped from a dead raw device to the data drive (install games
  to `D:\`).
- xatab GTA IV repack fix used: `winetricks -q mfc42`.


---


