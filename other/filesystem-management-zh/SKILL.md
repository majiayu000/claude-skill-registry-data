---
name: filesystem-management-zh
description: 高级文件系统操作——文件列表、搜索、批量处理和目录分析，专为 AI 智能体优化
homepage: https://github.com/gtrusler/clawdbot-filesystem
metadata: {"clawdbot":{"emoji":"📁","requires":{"bins":["node"]}}}
---

# 📁 文件系统管理

面向 AI 智能体的高级文件系统操作工具。提供全面的文件和目录操作能力，包括智能过滤、搜索和批量处理功能。

## 功能特性

### 📋 **智能文件列表**
- **高级过滤** — 按文件类型、模式、大小和日期过滤
- **递归遍历** — 深度目录扫描，支持深度控制
- **丰富格式** — 表格、树形和 JSON 输出格式
- **排序选项** — 按名称、大小、日期或类型排序

### 🔍 **强大搜索**
- **模式匹配** — 支持 Glob 模式和正则表达式
- **内容搜索** — 文件内全文搜索
- **多条件组合** — 同时按文件名和内容搜索
- **上下文显示** — 显示匹配行及其上下文

### 🔄 **批量操作**
- **安全复制** — 基于模式的文件复制，带验证机制
- **预览模式** — 执行前预览操作结果
- **进度追踪** — 实时操作进度显示
- **错误处理** — 优雅的故障恢复机制

### 🌳 **目录分析**
- **树形可视化** — ASCII 树形结构展示
- **统计信息** — 文件计数、大小分布、类型分析
- **空间分析** — 识别大文件和大目录
- **性能指标** — 操作计时和优化建议

## 快速开始

```bash
# 带过滤的文件列表
filesystem list --path ./src --recursive --filter "*.js"

# 搜索文件内容
filesystem search --pattern "TODO" --path ./src --content

# 安全批量复制
filesystem copy --pattern "*.log" --to ./backup/ --dry-run

# 显示目录树
filesystem tree --path ./ --depth 3

# 分析目录结构
filesystem analyze --path ./logs --stats
```

## 命令参考

### `filesystem list`
带高级过滤选项的文件和目录列表。

**参数说明：**
- `--path, -p <目录>` — 目标目录（默认：当前目录）
- `--recursive, -r` — 包含子目录
- `--filter, -f <模式>` — 按模式过滤文件
- `--details, -d` — 显示详细信息
- `--sort, -s <字段>` — 排序方式：name|size|date
- `--format <类型>` — 输出格式：table|json|list

### `filesystem search`
按文件名模式或内容搜索文件。

**参数说明：**
- `--pattern <模式>` — 搜索模式（glob 或正则表达式）
- `--path, -p <目录>` — 搜索目录
- `--content, -c` — 搜索文件内容
- `--context <行数>` — 显示上下文行数
- `--include <模式>` — 包含的文件模式
- `--exclude <模式>` — 排除的文件模式

### `filesystem copy`
带模式匹配和安全检查的批量文件复制。

**参数说明：**
- `--pattern <glob>` — 源文件模式
- `--to <目录>` — 目标目录
- `--dry-run` — 仅预览，不执行
- `--overwrite` — 允许覆盖文件
- `--preserve` — 保留时间戳和权限

### `filesystem tree`
以树形结构显示目录。

**参数说明：**
- `--path, -p <目录>` — 根目录
- `--depth, -d <数字>` — 最大深度
- `--dirs-only` — 仅显示目录
- `--size` — 显示文件大小
- `--no-color` — 禁用彩色输出

### `filesystem analyze`
分析目录结构并生成统计信息。

**参数说明：**
- `--path, -p <目录>` — 目标目录
- `--stats` — 显示详细统计
- `--types` — 分析文件类型
- `--sizes` — 显示大小分布
- `--largest <数量>` — 显示最大的 N 个文件

## 安装

```bash
# 通过 ClawdHub 安装
clawdhub install filesystem

# 或手动克隆
cd ~/.openclaw/skills
git clone <filesystem-skill-repo>

# 设置可执行权限
chmod +x filesystem/filesystem
```

## 配置说明

通过 `config.json` 自定义行为：

```json
{
  "defaultPath": "./",
  "maxDepth": 10,
  "defaultFilters": ["*"],
  "excludePatterns": ["node_modules", ".git", ".DS_Store"],
  "outputFormat": "table",
  "dateFormat": "YYYY-MM-DD HH:mm:ss",
  "sizeFormat": "human",
  "colorOutput": true
}
```

## 使用示例

### 开发工作流
```bash
# 查找 src 目录下所有 JavaScript 文件
filesystem list --path ./src --recursive --filter "*.js" --details

# 搜索 TODO 注释
filesystem search --pattern "TODO|FIXME" --path ./src --content --context 2

# 复制所有日志到备份目录
filesystem copy --pattern "*.log" --to ./backup/logs/ --preserve

# 分析项目结构
filesystem tree --path ./ --depth 2 --size
```

### 系统管理
```bash
# 查找大文件
filesystem analyze --path /var/log --sizes --largest 10

# 列出最近修改的文件
filesystem list --path /tmp --sort date --details

# 清理临时文件
filesystem list --path /tmp --filter "*.tmp" --older-than 7d
```

## 安全特性

- **路径验证** — 防止目录遍历攻击
- **权限检查** — 操作前验证读写权限
- **预览模式** — 预览破坏性操作
- **备份提示** — 覆盖前建议备份
- **错误恢复** — 优雅处理权限错误

## 集成

与其他工具无缝协作：
- **安全技能** — 验证所有文件系统操作
- **Git 操作** — 尊重 .gitignore 规则
- **备份工具** — 集成备份工作流
- **日志分析** — 完美支持日志文件管理

## 许可证

MIT 许可证 — 个人和商业使用均免费。
