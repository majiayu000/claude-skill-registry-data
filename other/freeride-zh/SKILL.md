---
name: freeride-zh
description: 管理 OpenRouter 的免费 AI 模型为 OpenClaw 提供服务。自动按质量排名模型、配置限流故障切换、更新 openclaw.json 配置。当用户提到免费 AI、OpenRouter、模型切换、限流或想降低 AI 成本时使用此技能。
---

# FreeRide - OpenClaw 免费AI

## 这个技能的作用

配置 OpenClaw 使用 OpenRouter 的**免费** AI 模型。将最佳免费模型设置为主模型，添加排名靠前的备用模型以便在限流时不中断用户，同时保留现有配置。

## 前置条件

在运行任何 FreeRide 命令之前，请确保：

1. **OPENROUTER_API_KEY 已设置。** 使用 `echo $OPENROUTER_API_KEY` 检查。如果为空，用户需要在 https://openrouter.ai/keys 获取免费密钥并设置：
   ```bash
   export OPENROUTER_API_KEY="sk-or-v1-..."
   # 或者持久化保存：
   openclaw config set env.OPENROUTER_API_KEY "sk-or-v1-..."
   ```

2. **`freeride` CLI 已安装。** 使用 `which freeride` 检查。如果未找到：
   ```bash
   cd ~/.openclaw/skills/freeride-zh
   pip install -e .
   ```

## 主要工作流程

当用户想要免费 AI 时，按顺序执行以下步骤：

```bash
# 步骤 1：配置最佳免费模型 + 备用模型
freeride auto

# 步骤 2：重启网关以便 OpenClaw 应用更改
openclaw gateway restart
```

就这么简单。用户现在拥有了带自动故障切换的免费 AI。

通过告诉用户发送 `/status` 来验证当前使用的模型。

## 命令参考

| 命令 | 使用场景 |
|---------|----------------|
| `freeride auto` | 用户想要设置免费 AI（最常用） |
| `freeride auto -f` | 用户想要添加备用模型但保留当前主模型 |
| `freeride auto -c 10` | 用户想要更多备用模型（默认是 5 个） |
| `freeride list` | 用户想要查看可用的免费模型 |
| `freeride list -n 30` | 用户想要查看所有免费模型 |
| `freeride switch <model>` | 用户想要指定特定模型（如 `freeride switch qwen3-coder`） |
| `freeride switch <model> -f` | 仅将特定模型添加为备用 |
| `freeride status` | 检查当前 FreeRide 配置 |
| `freeride fallbacks` | 仅更新备用模型 |
| `freeride refresh` | 强制刷新缓存的模型列表 |

**任何更改配置的命令后，都要运行 `openclaw gateway restart`。**

## 它写入配置的内容

FreeRide 只更新 `~/.openclaw/openclaw.json` 中的这些键：

- `agents.defaults.model.primary` — 例如 `openrouter/qwen/qwen3-coder:free`
- `agents.defaults.model.fallbacks` — 例如 `["openrouter/free", "nvidia/nemotron:free", ...]`
- `agents.defaults.models` — 白名单，使 `/model` 命令显示免费模型

其他所有内容（网关、通道、插件、环境变量、自定义指令、命名代理）都会保留。

第一个备用模型始终是 `openrouter/free` — OpenRouter 的智能路由器，根据请求自动选择最佳可用模型。

## 监控器（可选）

对于限流时的自动轮换，用户可以运行：

```bash
freeride-watcher --daemon    # 持续监控
freeride-watcher --rotate    # 立即强制轮换
freeride-watcher --status    # 检查轮换历史
```

## 故障排除

| 问题 | 解决方案 |
|---------|-----|
| `freeride: command not found` | `cd ~/.openclaw/skills/freeride-zh && pip install -e .` |
| `OPENROUTER_API_KEY not set` | 用户需要从 https://openrouter.ai/keys 获取密钥 |
| 更改未生效 | `openclaw gateway restart` 然后使用 `/new` 开启新会话 |
| 代理显示 0 tokens | 检查 `freeride status` — 主模型应该是 `openrouter/<provider>/<model>:free` |
