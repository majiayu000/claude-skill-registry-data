---
name: themes
description: >-
  Make Linux desktop tools look like Windows 11: Dolphin file manager,
  Konsole terminal, and the omp CLI TUI — dark gray background, blue
  selection, One Half-style schemes. One contract; the parts under parts/
  carry the exact configs.
---



# themes — Windows-look theming on Linux

Small, verified config playbooks. Each part is a complete recipe: say what
you want done, load that part, apply it.

## Parts

| Part | What it covers |
|---|---|
| `parts/dolphin-windows-theme/` | Dolphin (flatpak on GNOME/Fedora) styled as Windows 11 File Explorer: dark gray #1F1F1F background, white text, blue #0078D4 selection |
| `parts/konsole-windows-theme/` | Konsole on Fedora (KDE) with a Windows Terminal-style dark theme, One Half color scheme |
| `parts/omp-windows-dark/` | omp CLI (Oh My Pi coding agent TUI) dark Windows-style theme |

## Choosing

By the tool being themed: file manager → `dolphin-windows-theme`, KDE terminal
→ `konsole-windows-theme`, omp TUI → `omp-windows-dark`.

Functional tuning of these tools (performance, extensions, behavior) belongs
to the `desktop` router.
