---
name: deskhub-installer
description: 从 DeskHub（skills.deskclaw.me）搜索和安装技能到 Nanobot Workspace。当用户提到"DeskHub"、"SkillsHub"、"技能市场"、"去市场下载"、"安装技能"、"搜技能"时触发。使用 skillshub CLI 完成全部操作，禁止使用其他工具替代。
slug: deskhub-installer
version: 1.2.1
displayName: DeskHub 技能管理器（DeskHub Installer）
summary: 从 DeskHub 技能市场搜索、安装、更新技能到 Nanobot Workspace Skills 目录。
tags: deskhub, skillshub, install, marketplace, skills, nanobot
---

# DeskHub 技能安装器

从 **DeskHub**（https://skills.deskclaw.me）搜索、安装和管理技能。

## 前置检查（每次必做）

执行任何操作前，先确认 `skillshub` CLI 可用：

```bash
which skillshub && skillshub --version
```

**如果 `skillshub` 不存在，必须先安装：**

```bash
npm install -g @nodeskai/skillshub
skillshub config --api-url https://skills.deskclaw.me
```

> **⛔ 严格禁止**：当 `skillshub` 不可用时，**禁止使用 `npx clawhub`、`clawhub` 或任何其他工具/命令来替代**。这些替代方案会导致安装路径错误和长时间卡顿。唯一正确的做法是先安装 `skillshub`。

## 认证规则

DeskClaw 客户端预装了 `skillshub` CLI 并自动配置了认证（`~/.skillshub/config.json`）。从客户端触发本技能时，**认证已就绪，无需手动登录**。

### 读操作（搜索 / 查看 / 安装 / 更新 / 卸载）

直接执行，不需要提前验证 token。公开技能不需要任何认证；组织/私有技能的认证由 CLI 自动携带。

### 写操作（发布 / 同步 / 删除 / Star）

通常认证也已就绪。仅当 `skillshub whoami` 失败时，才向用户索取 API token（`sk-` 开头）：

```bash
skillshub whoami
# 如果未登录：
skillshub login <token>
```

### 安装的两条路径

1. **CLI 安装**（优先）：`skillshub install <slug>`，Agent 直接执行
2. **网页手动安装**（兜底）：通过 `deskclaw://install-skill/{slug}` 唤起客户端，需要 SkillsHub 网页登录态（从客户端进入技能广场时已自动携带）

## 触发场景

以下任何一种情况都应触发本技能：

- 用户说"去 DeskHub / SkillsHub 下载/安装/搜索"
- 用户说"技能市场里有没有 xxx"
- 用户说"帮我装一个 xxx 技能"并且提到了 DeskHub 或 SkillsHub
- 用户说"帮我搜一下有没有 xxx skill"
- 用户说"更新一下技能" / "看看有没有更新"

## 命令速查

### 读操作（无需 token）

| 操作 | 命令 |
|------|------|
| 搜索 | `skillshub search "<关键词>"` |
| 详情 | `skillshub inspect <slug>` |
| 安装 | `skillshub install <slug>` |
| 安装指定版本 | `skillshub install <slug> -v <版本号>` |
| 已安装列表 | `skillshub list` |
| 检查更新 | `skillshub outdated` |
| 更新单个 | `skillshub update <slug>` |
| 更新全部 | `skillshub update --all` |
| 卸载 | `skillshub uninstall <slug>` |

### 写操作（需要 sk- token）

| 操作 | 命令 |
|------|------|
| 发布 | `skillshub publish [dir]` |
| 同步 | `skillshub sync [dir]` |
| 删除 | `skillshub delete <slug>` |
| 收藏 | `skillshub star <slug>` |
| 取消收藏 | `skillshub unstar <slug>` |

## 示例

用户说："帮我找一下有没有搜索相关的技能"

```bash
skillshub search "search"
```

找到 `bing-search` 后安装：

```bash
skillshub install bing-search
```

用户说："帮我看看 DeskHub 上的竞品周报技能"

```bash
skillshub inspect product-competitor-analysis
```

确认后安装：

```bash
skillshub install product-competitor-analysis
```

## 安装目标路径

技能统一安装到 **Nanobot Workspace Skills 目录**。安装后技能自动生效，无需重启。

## 注意事项

- 用户说模糊的名字时，先用 `skillshub search` 搜索确认，再安装
- DeskHub 和 ClawHub 是两个不同的技能库；本技能仅管理 DeskHub 上的技能
- 不要尝试用 ClawHub 的内置安装命令来安装 DeskHub 技能
- 搜索、安装等读操作**直接执行**，不要先跑 `whoami` 检查登录——浪费时间且阻断流程
