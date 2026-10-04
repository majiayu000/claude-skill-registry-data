---
name: yuque-lakebook-export-cn
description: 当用户需要将语雀或 .lakebook 内容导出为本地 Markdown，用于 Obsidian 迁移或整理时使用。
license: MIT
---

# 语雀 Lakebook 导出

## Overview

将语雀知识库、语雀文档或 `.lakebook` 文件导出并转换为本地 Markdown 目录，优先适配 Obsidian 使用。流程支持单个或批量导出，并处理常见迁移问题，如图片缺失、裁剪图不匹配、内部链接损坏、目录层级错误和 Markdown 表格渲染异常。

## 何时使用

当用户需要以下能力时使用本技能：

- 导出一个或多个语雀 `.lakebook`
- 将语雀知识库转换为 Markdown
- 将语雀内容迁移到 Obsidian
- 修复语雀导出后的图片、裁剪图、内部链接、目录层级、表格渲染问题

## 不要使用

不要将本技能用于：

- 与语雀或 `.lakebook` 无关的普通 Markdown 编辑
- 网页抓取任务
- 非语雀来源的导出转换任务

## 使用说明

1. 优先使用非交互模式，便于 Agent 稳定执行。
2. Agent 在执行任何非交互导出前，必须先向用户确认输出根目录，不能自行决定输出目录。
3. 如果用户还没有明确给出输出目录，就先用一句简短问题询问，等用户答复后再执行导出。
4. 统一优先使用 `uv`，不要在任务目录里临时创建 `.venv`、`.yuque-export-venv` 这类环境。
5. 在执行任何 `uv` 命令前，先检查当前环境是否可用 `uv`。
6. 如果 `uv` 未安装，或者不在 `PATH` 中，Agent 必须先征求用户确认是否安装 `uv`，不能直接静默安装。
7. 在执行 `uv sync` 或 `uv run python scripts/cli.py ...` 前，必须先切换到当前已安装 skill 的工具目录，也就是包含本 `SKILL.md`、`pyproject.toml`、`uv.lock` 和 `scripts/` 的那个目录。不要在 `.lakebook` 所在目录、目标输出目录、或用户当前工作区根目录直接执行这些命令。
8. Agent 执行时使用下面这个入口：

```bash
uv run python scripts/cli.py
```

9. 首次使用前同步依赖：

```bash
uv sync
```

10. 推荐执行顺序：

```bash
cd /path/to/installed-skill-root
uv sync
uv run python scripts/cli.py ...
```

11. 单文件执行：

```bash
uv run python scripts/cli.py -l "/path/to/your_file.lakebook" -o "/target/root"
```

12. 批量执行：

```bash
uv run python scripts/cli.py -l "/path/to/your_file_1.lakebook" "/path/to/your_file_2.lakebook" -o "/target/root"
```

13. 虽然 `scripts/cli.py` 仍然保留了给人类终端手工使用的交互选择能力，但 Agent 不应依赖交互模式，因为无法稳定获取终端交互状态。执行时始终显式传入 `-l` 和 `-o` 参数。
14. 不要在当前工作目录、用户下载目录、或任意任务目录里手动创建临时虚拟环境；依赖应由 skill 工具目录中的 `uv` 环境统一管理。
15. 已知有些语雀导出的文档正文会包含 `<!doctype lake>`，旧实现可能导出成 `lake## 标题`；当前技能内置实现已经处理这个问题。
16. 导出完成后检查：
- `.md` 文件是否生成
- 同名 `.assets` 目录是否生成
- 内部链接是否转为相对 Markdown 路径
- 图片是否能在 Obsidian 中正常显示
- 文档首行是否存在异常的 `lake##` 前缀

17. 如果导出失败，优先查看输入 `.lakebook` 同目录下生成的批量日志。

详细行为、输出规则和排查说明见 `references/usage.md`。
