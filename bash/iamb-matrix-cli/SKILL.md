---
name: iamb-matrix-cli
description: "Matrix CLI operations for iamb including account registration, token retrieval, and Space management."
---

# iamb Matrix CLI Operations

## Description
面向 `ulyssa/iamb` 的 Matrix 运维技能：补齐 iamb 原生命令之外的账户注册与 token 获取流程，并提供 Space ID 获取与空间关系维护操作。

## Activation Keywords
- iamb
- matrix cli
- matrix 注册
- 用户注册
- 获取 token
- access token
- space id
- spaces id
- iamb space

## Tools Used
- `exec`: 运行 `iamb` 与 Python 辅助脚本
- `read`: 读取 `config.toml` / `session.json` / 输出文件
- `write`: 生成或更新临时配置、结果文档

## Installation

### Prerequisites
```bash
# 1) 安装 iamb
cargo install --locked iamb

# 2) Python 3.9+
python3 --version
```

### Optional
```bash
# 如果你更偏好 requests，可自行安装
uv pip install requests
```

## Usage Patterns

### 1) 通过 Matrix API 注册用户
```bash
python collection/skills/iamb-matrix-cli/scripts/matrix_iamb_helper.py register \
  --homeserver https://matrix.example.com \
  --username alice \
  --password 'StrongPass123!'
```

### 2) 获取用户 access token（登录）
```bash
python collection/skills/iamb-matrix-cli/scripts/matrix_iamb_helper.py login \
  --homeserver https://matrix.example.com \
  --user '@alice:matrix.example.com' \
  --password 'StrongPass123!'
```

### 3) 从 iamb 会话文件提取 token
```bash
python collection/skills/iamb-matrix-cli/scripts/matrix_iamb_helper.py extract-token \
  --session-json ~/.local/share/iamb/profiles/<profile>/session.json
```

### 4) 获取 Space ID 列表
```bash
python collection/skills/iamb-matrix-cli/scripts/matrix_iamb_helper.py space-ids \
  --homeserver https://matrix.example.com \
  --access-token '<TOKEN>'
```

### 5) 在 iamb 中查看/维护 Space
```text
:spaces
:room id show
:space child set !room_id:example.com ++suggested
:space child remove
```

## Instructions for Agents

### Step 1: 先判断 iamb 原生能力边界
- iamb 支持登录（password/SSO）与会话恢复。
- iamb 支持 `:spaces`、`:room id show`、`:space child set/remove`。
- iamb **不提供显式“注册新用户”命令**，应走 Matrix Client-Server API。

### Step 2: 处理用户注册
- 调用 `matrix_iamb_helper.py register`。
- 若 homeserver 禁止 `m.login.dummy` 注册，提示管理员策略限制并转登录流程。

### Step 3: 获取 token
优先顺序：
1. 已登录 iamb：`extract-token` 读取 `session.json`。
2. 未登录：`login` 调 Matrix API 获取 token。

### Step 4: 获取 Space ID
- 先通过 `joined-rooms` 获取已加入 room 列表。
- 对每个 room 调 `m.room.create` 状态事件。
- 过滤 `type == "m.space"` 的 room，输出 Space IDs。

### Step 5: 回到 iamb 执行空间操作
- 用 `:spaces` 导航。
- 在目标空间内使用 `:space child set/remove` 维护子房间。
- 需要定位当前窗口 room id 时执行 `:room id show`。

## Error Handling

### 注册失败（401/403）
- 检查 homeserver 是否允许公开注册。
- 检查是否需要 CAPTCHA / email / token-based 注册流程。
- 无法自动化时，提示改为管理员代注册或 web 注册。

### token 无效（M_UNKNOWN_TOKEN）
- 重新登录获取新 token。
- 检查是否被服务端吊销会话。

### Space 查询为空
- 可能尚未加入任何 space。
- 先在 iamb 中 `:join <space_alias_or_id>`，再重新查询。

## Limitations
- 不同 homeserver 的注册策略差异较大，`dummy auth` 不一定可用。
- 脚本仅覆盖常见 Matrix v3 流程，不覆盖全部 UIA 交互分支。

## Best Practices
1. 优先从 `session.json` 读取 token，避免重复登录。
2. 所有输出尽量使用 JSON，便于后续 agent 自动处理。
3. 不在日志或聊天中明文回显密码。

## Examples

### Example: 注册 + 登录 + Space ID
1. 注册：`register`
2. 登录：`login`
3. 查询 Space：`space-ids`
4. 在 iamb 中执行 `:spaces` 和 `:space child set ...`

## Resources
- iamb Repo: https://github.com/ulyssa/iamb
- Matrix Client-Server API: https://spec.matrix.org/latest/client-server-api/
- iamb docs: https://iamb.chat

## Related Skills
- `chat-history-lancedb`: 保存本次排障上下文
- `skill-rag-indexer`: 将 Matrix 结果索引到可检索知识库
- `skill-extractor`: 将重复 CLI 流程沉淀为可复用模式
