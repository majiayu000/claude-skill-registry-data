---
name: laohan-gengxin
version: 1.0
description: 工具版本检查与更新，扫描 npm/brew/pip/uv/GitHub/plugins/skills 逐项对比已装和最新版本，生成带编号报告，确认后才执行更新。Use when 用户说"检查更新""工具版本""看看哪些该更新了""brew有没有过期的""opencli是不是该更新了"或提到工具版本/环境更新。
---

# 工具版本检查与更新

扫描所有常用工具的版本状态，生成编号报告，等待选择后逐项更新。

## 核心理念

只检查不自动更新——报告给用户看，确认后才动。因为盲目更新可能破坏环境（openclaw 升级后需补装依赖、插件升级后需重启），每次更新都要用户知情。

## 不适用场景

- 只检查单个工具版本 → 直接跑 `--version` 或 `npm view <pkg> version`，不需要本 skill
- 安装新工具 → 用 `brew install` / `npm install` / `uv tool install`，不走更新流程

## 工作流程

### 第0步：发现遗漏

跑 `scripts/discover.sh`，全量扫描系统（npm/brew/pip/uv/conda/local-bin），过滤依赖库后与 tools.json 做差集。如果有新发现的工具，报告给用户确认是否加入。

发现方法论的完整说明见 `references/scan-methodology.md`。

### 第1步：读取工具清单

读取 `references/tools.json`，获取所有工具的检查方式和更新命令。

### 第2步：逐项检查版本

按分类并行执行检查命令，对比已装版本和最新版本。检查逻辑：

| 检查源 | 命令 | 说明 |
|--------|------|------|
| npm | `npm view <pkg> version` | npm registry 最新版 |
| brew | `brew outdated --json=v2` | Homebrew 过期检查 |
| pip | `pip3 index versions <pkg>` | PyPI 最新版 |
| uv | `pip3 index versions <pkg>` | PyPI（uv tool 安装的也能查） |
| gh release | `gh api repos/<owner>/<repo>/releases/latest --jq .tag_name` | GitHub release |
| claude plugins | `claude plugins list --json` | 插件市场版本 |

### 第3步：生成编号报告

**固定格式，每条一行**：

```
[编号] [分类] [状态标记] [名字]
  已装: x.x.x → 最新: y.y.y
  作用: 中文说明
  频繁度: 高/中/低 | 推荐更新: 是/否 | 推荐卸载: 是/否
  更新方式: 具体命令
  重大变化: (如果有)
```

**状态标记**：
- ✅ 最新
- ⬆️ 落后（推荐更新）
- ⚠️ 落后很多（跨大版本）
- ❓ 未知（检查失败）

**分类**：核心平台 | npm包 | Homebrew | Python | uv工具 | 插件 | Skills | 运行时

### 第4步：等待用户选择

报告末尾提示：
```
输入要更新的编号（用逗号或空格分隔），或输入 "all" 全部更新，"q" 退出：
```

### 第5步：执行更新

用户给出编号后，按编号顺序逐项执行对应的更新命令。每项更新完成后报告结果（成功/失败）。

**注意事项**：
- openclaw 更新后需跑维护清单（见下方）
- brew 用 `brew reinstall` 不用 `brew upgrade`（国内镜像缓存同步延迟）
- npm 更新后不用 `--force`
- pip 用 `pip3 install --upgrade` 或 `uv pip install --upgrade`
- 插件更新后需重启 Claude Code session
- skills 用 `npx skills update -g -y` 全量更新（不支持单个更新）

### openclaw 更新后维护清单

如果用户更新了 openclaw，提醒执行：
```bash
# 1. 健康检查超时补丁
~/.openclaw/scripts/patch-health-timeout.sh

# 2. 补装 memory 依赖
DEPS_DIR=$(ls -td ~/.openclaw/plugin-runtime-deps/openclaw-*/ | head -1)
cd "$DEPS_DIR" && npm install node-llama-cpp@3.18.1 sqlite-vec

# 3. 重启 gateway
launchctl kickstart -k gui/$(id -u)/ai.openclaw.gateway

# 4. 等60秒冷启动后验证
sleep 60 && openclaw status
```

## 工具清单维护

`references/tools.json` 记录所有工具的元数据。新增工具时往 JSON 里加一条即可。

## 脚本

`scripts/check.sh` — 自动化版本检查脚本，输出 JSON 格式结果供 skill 解析生成报告。
