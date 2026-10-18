---
name: getskill
description: 用于 OpenClaw 的技能管理工具，支持从 getskill.work 仓库搜索、下载和更新技能文件。提供 CLI 和编程接口，通过 API 搜索技能、通过 Git 克隆仓库、将技能目录复制到 OpenClaw skills 目录，并提供 Git 安装引导。
license: MIT
compatibility: 需要 Node.js >= 12 和 Git 命令行工具。支持 Windows、macOS 和 Linux 跨平台。
metadata:
  author: workskills.store
  version: "1.1.4"
  category: cli-tool
---

# GetSkill

## 何时使用此 Skill

当你需要以下功能时使用此 skill：
- 从 getskill.work 仓库搜索 OpenClaw 技能
- 向 OpenClaw 环境安装新技能
- 更新现有技能到最新版本
- 管理 `~/.openclaw/skills` 目录中的技能文件
- 为技能仓库配置自定义 API 端点

## 指令

### OpenClaw 首次启动：先安装 getskill CLI

当 OpenClaw 首次启动且尚未安装 getskill CLI 时，按以下流程执行：

1. 先测试 `getskill` 是否可用：
   ```bash
   getskill --help
   ```

2. 如果不可用，安装 CLI（任选其一）：
   ```bash
   pnpm i -g @workskills/getskill
   ```
   或
   ```bash
   npm i -g @workskills/getskill
   ```

3. 安装完成后即可运行 getskill 命令：
   ```bash
   getskill search <关键词>
   ```

### 搜索技能

1. 使用搜索命令并传入关键词：
   ```bash
   getskill search <关键词>
   ```

2. 工具查询 API 并返回匹配的技能，包含：
   - 技能名称和描述
   - Git 仓库 URL

### 安装技能

1. 首先确保系统已安装 Git（如未安装，工具会引导安装）

2. 运行安装命令：
   ```bash
   getskill install <技能名称>
   ```

3. 工具执行以下操作：
   - 克隆 Git 仓库到 `~/.openclaw/skills-cache/<技能名称>`
   - 将整个技能目录复制到 `~/.openclaw/skills/<本地技能目录名>`（排除 `.git`）
   - 返回已复制目录列表

### 更新技能

1. 运行更新命令：
   ```bash
   getskill update <技能名称>
   ```

2. 工具会：
   - 检查技能是否存在于缓存目录
   - 执行 `git pull` 获取最新变更
   - 重新复制技能目录到 skills 目录

### 列出本地技能

```bash
getskill list
```

返回 skills 目录中当前所有技能目录名称。

### 查看目录路径

```bash
getskill path
```

显示：
- 技能目录：`~/.openclaw/skills`
- 缓存目录：`~/.openclaw/skills-cache`

### 配置 API 端点

查看当前端点：
```bash
getskill config get
```

设置自定义端点：
```bash
getskill config set https://your-custom-api.com
```

### 清理缓存

```bash
getskill clean
```

移除所有 Git 仓库缓存，不影响已安装的技能。

## 示例

### 搜索示例

**输入：** 用户想查找与 commit 相关的技能

**命令：**
```bash
getskill search commit
```

**输出：**
```
找到 3 个技能：

1. commit-helper
   描述: 帮助生成规范的 git commit 信息
   Git: https://getskill.work/skills/commit-helper.git
```

### 安装示例

**输入：** 用户想安装 commit-helper 技能

**命令：**
```bash
getskill install commit-helper
```

**操作：**
1. `git clone` 到 `~/.openclaw/skills-cache/commit-helper`
2. 复制整个目录到 `~/.openclaw/skills/commit-helper`

**输出：**
```
技能已安装到 skills 目录:
   - ~/.openclaw/skills/commit-helper
```

### 更新示例

**输入：** 用户想更新已有技能

**命令：**
```bash
getskill update commit-helper
```

**操作：**
1. `cd ~/.openclaw/skills-cache/commit-helper`
2. `git pull`
3. 重新复制技能目录到 skills 目录

## 边缘情况

### Git 未安装

**场景：** 用户在没有 Git 的系统上运行 install/update 命令

**处理：**
- Windows：自动下载 Git 安装程序并启动安装向导
- macOS：提示通过 Homebrew 安装（`brew install git`）
- Linux：提供包管理器命令（apt-get、yum、dnf、pacman）

### 技能未找到

**场景：** API 返回 404 表示请求的技能不存在

**处理：** 显示清晰的错误信息："技能不存在: {skill-name}"

### 仓库无技能文件

**场景：** 克隆的仓库中不包含技能 `.md` 文件（除 README 外）

**处理：** 抛出错误："在仓库中未找到技能 .md 文件"

### 网络错误

**场景：** 由于网络问题导致 API 请求失败

**处理：**
- 主机未找到："无法连接到服务器，请检查网络或 API 地址配置"
- 超时："请求超时，请稍后重试"
- 连接被拒绝："服务器拒绝连接，请检查 API 地址是否正确"

### 技能名称重复

**场景：** 仓库中有多个名称相似的 `.md` 文件

**处理：** 将技能目录整体复制到 skills 目录（排除 `.git`）

## 关键规则

- 在执行 clone/pull 操作前始终验证 Git 安装
- 复制整个技能目录到 `skills/<技能名>`，并排除 `.git` 目录
- 清理时绝不删除 skills 目录内容 - 只移除缓存
- 支持通过环境变量 `GETSKILL_BASE_URL` 使用自定义端点
- 自动处理 API 重定向（最多 5 次）
- API 请求 60 秒后超时
- 如果目录不存在则递归创建
- 搜索失败时返回空数组（而不是抛出异常）以防止程序崩溃
- 在调用 API 前验证所有用户输入