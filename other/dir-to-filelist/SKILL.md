---
name: dir-to-filelist
description: Scan a directory and generate a Markdown file listing all files with their names and paths. Supports excluding specific files or directories. Use this skill when you need to create an asset list or file inventory.
---

# Dir to Filelist Skill

扫描目录下所有文件，生成 Markdown 格式的文件清单（文件名 + 路径），支持排除指定文件或文件夹。

## 使用方法

```bash
python3 .codebuddy/skills/dir-to-filelist/scripts/generate_filelist.py <target_dir> [options]
```

## 参数说明

| 参数 | 必填 | 说明 |
|------|------|------|
| `target_dir` | 是 | 要扫描的目标目录 |
| `-o`, `--output` | 否 | 输出文件路径，默认为 `<target_dir>/list.md` |
| `--exclude-dir` | 否 | 要排除的目录名（可多次指定） |
| `--exclude-file` | 否 | 要排除的文件名（可多次指定） |

## 示例

```bash
# 基础使用 - 扫描素材目录，输出到 assets/list.md
python3 .codebuddy/skills/dir-to-filelist/scripts/generate_filelist.py game-basic/assets/images -o assets/list.md

# 排除 temp 目录
python3 .codebuddy/skills/dir-to-filelist/scripts/generate_filelist.py game-basic/assets/images -o assets/list.md --exclude-dir temp

# 排除多个目录和文件
python3 .codebuddy/skills/dir-to-filelist/scripts/generate_filelist.py game-basic/assets/images -o assets/list.md --exclude-dir temp --exclude-dir raw --exclude-file .DS_Store

# 排除指定文件
python3 .codebuddy/skills/dir-to-filelist/scripts/generate_filelist.py src/ -o docs/source_files.md --exclude-file index.ts
```

## 输出格式

生成的 Markdown 文件按子目录分组，格式如下：

```markdown
# Asset List (素材清单)

> Auto-generated file list from `game-basic/assets/images`.
> **Total**: 24 files

## Characters

| File Name | Path |
| :--- | :--- |
| `player_idle.png` | `game-basic/assets/images/characters/player_idle.png` |
| `player_run_01.png` | `game-basic/assets/images/characters/player_run_01.png` |

## Environments

| File Name | Path |
| :--- | :--- |
| `bg_sky.png` | `game-basic/assets/images/environments/bg_sky.png` |

## Ui

| File Name | Path |
| :--- | :--- |
| `btn_play.png` | `game-basic/assets/images/ui/btn_play.png` |
```

## 特性

- **递归扫描**：遍历目标目录下所有子目录
- **分组展示**：按子目录自动分组
- **排除机制**：支持按目录名或文件名排除
- **自动跳过**：隐藏文件/目录（以 `.` 开头）自动跳过
- **排序输出**：目录和文件均按字母排序
