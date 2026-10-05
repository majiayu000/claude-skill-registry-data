---
name: lark-shared
version: 1.0.0
description: "飞书/Lark CLI 共享基础：应用配置初始化、认证登录（auth login）、身份切换（--as user/bot）、权限与 scope 管理、Permission denied 错误处理、安全规则。当用户需要第一次配置(`lark-cli config init`)、使用登录授权(`lark-cli auth login`)、遇到权限不足、切换 user/bot 身份、配置 scope、或首次使用 lark-cli 时触发。"
---

# lark-cli 共享规则

本技能指导你如何通过lark-cli操作飞书资源, 以及有哪些注意事项。

## 配置初始化

### 新建应用（首次使用）

首次使用、没有现成飞书应用时，运行 `lark-cli config init --new` 创建新应用：

```bash
# 发起配置（该命令会阻塞直到用户打开链接并完成操作或过期）
lark-cli config init --new
```

### 绑定已有应用（Hermes/OpenClaw 上下文）

当 Agent 已经通过 Gateway 接入了飞书（存在 `OPENCLAW_HOME` / `HERMES_HOME`），**禁止**用 `config init` 新建应用——会创建并行应用，导致冲突。

应使用 `config bind` 将 lark-cli 绑定到 Agent 现有的飞书应用：

```bash
# 查看可用 app ID
lark-cli config bind --help

# 绑定到 Hermes 已有的应用，使用用户身份
lark-cli config bind --source hermes --identity user-default

# 或仅使用 bot 身份（更安全，无法访问个人资源）
lark-cli config bind --source hermes --identity bot-only
```

**身份选择：**
| 模式 | 能力 | 限制 |
|------|------|------|
| `bot-only`（推荐默认） | 知识库、文档、任务、审批、通讯录搜索 | 不能访问个人日历/邮箱/云盘 |
| `user-default` | 同上 + 可模拟用户身份访问个人资源 | 需要用户授权，权限更大 |

**提示：** `--identity` 省略时默认为 `bot-only`。切换身份策略用 `lark-cli config strict-mode`，不需要重新 bind。

绑定成功后，继续执行 `lark-cli auth login` 完成用户身份授权。

## 认证

### 身份类型

两种身份类型，通过 `--as` 切换：

| 身份 | 标识 | 获取方式 | 适用场景 |
|------|------|---------|---------|
| user 用户身份 | `--as user` | `lark-cli auth login` 等 | 访问用户自己的资源（日历、云空间等） |
| bot 应用身份 | `--as bot` | 自动，只需 appId + appSecret | 应用级操作,访问bot自己的资源 |

### 身份选择原则

输出的 `[identity: bot/user]` 代表当前身份。bot 与 user 表现差异很大，需确认身份符合目标需求：

- **Bot 看不到用户资源**：无法访问用户的日历、云空间文档、邮箱等个人资源。例如 `--as bot` 查日程返回 bot 自己的（空）日历
- **Bot 无法代表用户操作**：发消息以应用名义发送，创建文档归属 bot
- **Bot 权限**：只需在飞书开发者后台开通 scope，无需 `auth login`
- **User 权限**：后台开通 scope + 用户通过 `auth login` 授权，两层都要满足


### 权限不足处理

遇到权限相关错误时，**根据当前身份类型采取不同解决方案**。

错误响应中包含关键信息：
- `permission_violations`：列出缺失的 scope (N选1)
- `console_url`：飞书开发者后台的权限配置链接
- `hint`：建议的修复命令

#### Bot 身份（`--as bot`）

将错误中的 `console_url` 提供给用户，引导去后台开通 scope。**禁止**对 bot 执行 `auth login`。

#### User 身份（`--as user`）

```bash
lark-cli auth login --domain <domain>           # 按业务域授权
lark-cli auth login --scope "<missing_scope>"   # 按具体 scope 授权（推荐,符合最小权限原则）
```

**规则：** auth login 必须指定范围（`--domain` 或 `--scope`）。多次 login 的 scope 会累积（增量授权）。

### Agent 代理发起认证（推荐，两步式）

作为 AI agent 需要帮用户完成飞书授权时，**不要直接用阻塞模式**。使用两步式：

**步骤 1：生成授权 URL 和二维码**

```bash
# 发起授权但不阻塞，返回 device_code 和 verification_url
lark-cli auth login --no-wait --json --domain all
```

> ⚠️ **`--no-wait --json` 必须配合 `--domain` 或 `--scope` 指定授权范围。** 单独 `--no-wait --json`（无 `--domain`/`--scope`）会报 "please specify the scopes to authorize"。也不要用 `--recommend` 代替——`--recommend` 与 `--no-wait` 组合不被接受。直接用 `--domain all` 一次性授权全部域最省事。

输出包含 `verification_url`、`device_code`、`expires_in`（通常 600 秒）。

关键规则：
- **必须生成二维码并展示**：调用 `lark-cli auth qrcode` 将 verification_url 转为二维码
  ```bash
  cd /tmp && lark-cli auth qrcode --output lark-auth-qr.png "<verification_url>"
  ```
  ⚠️ `--output` **必须是相对路径**（如 `./lark-auth-qr.png`），绝对路径（如 `/tmp/qr.png`）会报 "unsafe output path"。建议先 `cd` 到目标目录再使用相对路径。生成后把二维码图片（`MEDIA:`）和 URL 一并展示给用户。
- 使用 `--domain all` 授权全部域，或用 `--domain docs,task,base` 等限定范围
- 展示顺序：先输出 URL，再将二维码图片置于下方
- 把 URL 作为 opaque string 不做任何修改
- 把 verification_url / QR code 作为本轮最终消息发给用户并结束本轮

**步骤 2：用户告知已完成授权后，续接轮询**

```bash
lark-cli auth login --device-code "<device_code>"
```

- 上一步的 `device_code` 有效期内（10 分钟）可用
- 不要在同一轮里展示 URL 后立刻阻塞执行 `--device-code`
- 不要短 timeout 反复重试——每次重启会作废上一轮的 device code
- 如果超时，告知用户需要重新生成授权链接

#### 其他认证方式

```bash
lark-cli auth login --recommend            # 仅请求自动批准的 scope
lark-cli auth login --scope "docs:doc:readonly"   # 精确 scope
```


## 更新检查

lark-cli 命令执行后，如果检测到新版本，JSON 输出中会包含 `_notice.update` 字段（含 `message`、`command` 等）。

**当你在输出中看到 `_notice.update` 时，完成用户当前请求后，主动提议帮用户更新**：

1. 告知用户当前版本和最新版本号
2. 提议执行更新（CLI 和 Skills 需要同时更新）：
   ```bash
   npm update -g @larksuite/cli && npx skills add larksuite/cli -g -y
   ```
3. 更新完成后提醒用户：**退出并重新打开 AI Agent**以加载最新 Skills

**规则**：不要静默忽略更新提示。即使当前任务与更新无关，也应在完成用户请求后补充告知。

## 安全规则

- **禁止输出密钥**（appSecret、accessToken）到终端明文。
- **写入/删除操作前必须确认用户意图**。
- 用 `--dry-run` 预览危险请求。
