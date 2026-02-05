---
name: update-theme
description: Update the Warm Graphite color theme for lsd and vivid terminal tools. Use when modifying colors, refreshing the palette, or adjusting file type styling.
---

# Update lsd/vivid Theme

Update the Warm Graphite theme for lsd and vivid.

## References

- **lsd**: https://github.com/lsd-rs/lsd
- **vivid**: https://github.com/sharkdp/vivid
- **vivid themes**: https://github.com/sharkdp/vivid/tree/master/themes

## Getting Documentation

Clone repos for reference when needed:

```bash
git clone --depth 1 https://github.com/lsd-rs/lsd.git /tmp/lsd-repo
git clone --depth 1 https://github.com/sharkdp/vivid.git /tmp/vivid-repo
```

Key reference files:
- `/tmp/lsd-repo/doc/samples/colors-sample.yaml` - lsd color config example
- `/tmp/lsd-repo/doc/colors.md` - lsd color documentation
- `/tmp/vivid-repo/themes/` - vivid theme examples

## File Locations

**Master files (edit these):**
- `lsd/colors.yaml` - UI metadata colors (user, group, permissions, dates, git status)
- `lsd/config.yaml` - lsd layout and behavior settings
- `vivid/themes/warm-graphite.yml` - file type colors via LS_COLORS

**Installed locations:**
- `~/.config/lsd/colors.yaml`
- `~/.config/lsd/config.yaml`
- `~/.config/vivid/themes/warm-graphite.yml`

## Color Palette (ANSI 256)

| Code | Name | Hex | Used For |
|------|------|-----|----------|
| 140 | mauve | `#af87d7` | user, symlinks, renamed (lavender) |
| 243 | gray | `#767676` | group, unmodified |
| 245 | light gray | `#8a8a8a` | permissions, older dates |
| 240 | dark gray | `#585858` | no-access, ignored, tree-edge |
| 223 | peach | `#ffd7af` | hour-old dates, highlights |
| 174 | rose | `#d78787` | day-old dates, media (salmon) |
| 186 | tan | `#d7d787` | large files, markup (chartreuse) |
| 107 | sage | `#87af5f` | executables, git new, source code (lime) |
| 178 | gold | `#d7af00` | git modified, config, archives (cleaner) |
| 173 | coral | `#d7875f` | errors, deleted, conflicts (terracotta) |
| 73 | teal | `#5fafaf` | directories, links, tooling (richer) |

## Workflow

1. **Edit** the master files in this repo
2. **Install**: `just install`
3. **Reload**: `source ~/.zshrc`
4. **Test**: `just test`
5. **Commit** changes to git if satisfied

## Testing Colors

To verify ANSI codes are being applied correctly (since terminal output may strip colors):

```bash
lsd -la --color=always | head -3 | cat -v
```

This shows raw ANSI escape codes like `^[[38;5;251m` (color 251) so you can verify the config is loaded.

## Color Formats

- **lsd colors.yaml**: ANSI 256 codes (numbers) or named colors
- **vivid warm-graphite.yml**: Hex colors without # prefix (e.g., "d7af5f")

## Common Tasks

### Change a specific color
1. Find the element in the appropriate file
2. Update the color code/hex value
3. Run `just install && source ~/.zshrc && just test`

### Add a new accent color to vivid
1. Add to `colors:` section in warm-graphite.yml
2. Reference it in the appropriate category (core, text, programming, etc.)
