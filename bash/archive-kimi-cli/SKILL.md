---
name: kimi-cli
version: 1.2.4
description: |
  使用 Kimi Code CLI 执行复杂代码任务。当用户需要：
  1. 大型代码生成（完整功能模块、多文件项目）
  2. 复杂代码重构（legacy 代码现代化、架构调整）
  3. 深度 Bug 诊断（多文件关联错误、难以定位的问题）
  4. 技术调研实现（新技术栈完整集成、PoC 开发）
  5. 长时间运行的开发任务（需要持续交互）

  适用场景：任务复杂度超出单次回复范围，需要多步骤自主执行或长时间运行时。

  技术方案：基于 OpenClaw exec 的 PTY 模式，支持伪终端交互和后台会话。
---

# Kimi CLI Skill

**版本**: 1.2.4 | **最后更新**: 2026-02-04

使用 Kimi Code CLI 作为“编码执行器”，配合会话模型做规划/验收，完成复杂代码任务。

## 架构与职责分工（重要）

> 目标：不是让会话模型（例如 GLM）直接写复杂代码，而是让它**指挥**，由 Kimi Code CLI **真正产出/修改代码文件**。

```
🧠 会话模型（规划/拆解/验收）
  ↓ 调用
📋 kimi-cli skill（exec + pty + workdir + process 控制）
  ↓ 运行
💻 Kimi Code CLI（生成/修改文件、输出步骤）
```

- **会话模型**：需求澄清、任务拆解、验收标准、结果核查、复盘总结
- **Kimi CLI**：按指令在指定目录里创建/修改文件、生成脚本/项目、给出执行步骤

---

## 两种工作模式

### 1. 快速模式 (Quick Mode)

**适用场景**：明确的单次任务，执行完即返回

**推荐执行方式（one-shot）**：
```bash
bash pty:true workdir:~/project timeout:300 command:"kimi --print -p '你的任务描述'"
```

**参数说明**：
- `pty:true` - **必需！** 分配伪终端，让 CLI 输出/交互稳定
- `workdir` - 工作目录（强烈建议使用独立目录）
- `timeout` - 超时时间（秒）
- `command` - 要执行的 Kimi 命令

**示例**：
```bash
# 创建一个完整项目
bash pty:true workdir:~/projects timeout:600 command:"kimi --print -p '创建一个 React + TypeScript 的待办事项应用'"

# 重构现有代码
bash pty:true workdir:~/my-project timeout:300 command:"kimi --print -p '重构 src/utils.py 使用现代 Python 最佳实践'"
```

> 注意：不要用 `kimi '...'` 作为 one-shot 标准写法（容易进入交互/输出不一致）。

---

### 2. 交互模式 (Interactive Mode)

**适用场景**：复杂任务需要多轮交互，或 Kimi 可能会提问确认

**启动方式**：
```bash
bash pty:true workdir:~/project background:true command:"kimi"
```

**后续控制**（使用 process 工具）：

| 操作 | 命令 |
|------|------|
| 查看输出 | `process action:log sessionId:xxx` |
| 发送输入 | `process action:submit sessionId:xxx data:"你的回答"` |
| 原始输入 | `process action:write sessionId:xxx data:"内容"` |
| 检查状态 | `process action:poll sessionId:xxx` |
| 结束会话 | `process action:kill sessionId:xxx` |

**完整示例**：
```bash
# 1. 启动后台会话
bash pty:true workdir:~/project background:true command:"kimi"
# 返回: sessionId: abc123

# 2. 查看初始输出
process action:log sessionId:abc123

# 3. Kimi 提问时，发送回答
process action:submit sessionId:abc123 data:"使用 TypeScript"

# 4. 持续监控
process action:log sessionId:abc123 limit:50

# 5. 完成或出错时结束
process action:kill sessionId:abc123
```

---

## Prompt 最佳实践

基于测试任务总结的最佳实践：

### 1. 明确指定命令版本

许多系统同时安装了 `python` 和 `python3`，但 `python` 可能不存在：

```bash
# ✅ 明确指定 python3
kimi --print -p "使用 python3 运行..."

# ❌ 不指定可能失败
kimi --print -p "使用 python 运行..."  # 可能找不到命令
```

### 2. 要求包含测试 / 验证步骤

```bash
kimi --print -p "创建一个模块，要求：1) 功能实现 2) 包含单元测试文件 3) 给出如何运行 pytest 的命令"
```

### 3. 分步骤描述需求

```bash
kimi --print -p "创建一个脚本，要求：1) 支持参数 X 2) 验证输入 3) 错误处理 4) 文档"
```

---

## 最佳实践（执行层）

### 1. 总是使用 PTY

Kimi CLI 是交互式应用，**必须**使用 `pty:true`：

```bash
# ✅ 正确
bash pty:true command:"kimi --print -p '...'"

# ❌ 错误 - 可能挂起或输出异常
bash command:"kimi --print -p '...'"
```

### 2. 使用独立工作目录（并确保目录已存在）

避免 Kimi 访问不相关文件：

```bash
bash pty:true workdir:/tmp/new-project command:"kimi --print -p '创建新项目'"
```

**注意（OpenClaw exec 的 workdir 约束）**：
- `exec` 的 `workdir` **必须在调用前就存在**，否则 OpenClaw 会回退到默认目录（并打印类似 “workdir ... is unavailable”）。
- 推荐做法：先单独创建目录，再执行 Kimi。

示例：
```bash
# 1) 先创建目录（普通 exec 即可）
mkdir -p /tmp/kimi-eval/t01

# 2) 再用该 workdir 调用 Kimi（PTY 必开）
bash pty:true workdir:/tmp/kimi-eval/t01 timeout:600 command:"kimi --print -p '...任务...'"
```

### 3. 合理设置超时

```bash
# 小任务: 5 分钟
bash pty:true timeout:300 command:"kimi --print -p '...'"

# 大任务: 10 分钟或更长
bash pty:true timeout:600 command:"kimi --print -p '...'"
```

### 4. 监控后台任务

```bash
process action:log sessionId:xxx limit:30
```

### 5. 处理 Kimi 的提问

```bash
process action:submit sessionId:xxx data:"y"
```

---

## 错误处理：429 Rate Limit（必须掌握）

当 Kimi 配额耗尽时，可能出现：

- `429 ... rate_limit_error`
- 表现为：子任务“无输出”/多次重试仍失败

**SOP：**
1. **识别**：日志/错误信息包含 `429` 或 `rate_limit_error`
2. **停止重试**：短时间重复调用只会继续失败
3. **等待**：通常按“下个计费/刷新周期”恢复（建议 60 分钟后再试）
4. **记录**：把受影响任务标注为 `blocked_by_rate_limit`，避免误判为失败
5. **恢复后补跑**：配额恢复后优先补跑被阻塞任务

> 可选降级：如果必须立刻继续推进，可由会话模型临时代写/生成草案，但要标注为“非 Kimi 产物”，配额恢复后再用 Kimi 复跑对比。

---

## 依赖要求

- Kimi Code CLI 已安装：`pip install kimi-cli`
- 已登录：`kimi /login`

---

## 版本历史

### v1.2.4 (2026-02-04)
**改进点**:
- ✅ 完成 **A03 (ACP 合规输出)**：Kimi 生成 `payload.acp`（acpVersion=2.0, signature, data），`scripts/acp_check.py` 验证通过（VALID）
- ✅ 设置每小时自动检查任务（cron job），完成上一题后自动启动下一题
- ✅ 新增 5 道探索性题目（E01-E05）：自我监控、渐进式复杂度、多语言混合、失败恢复、网络降级

### v1.2.3 (2026-02-04)
**改进点**:
- ✅ 完成 **R01 (Ralph print)** 验证：Kimi 成功生成 `summary.json` + `summary.txt`，数据一致（metric=42, status=SUCCESS），JSON 通过 `python3 -m json.tool` 校验
- ✅ 确认 Ralph-style 输出格式可被后续 agent 解析
- ✅ 完成 **S02 (Agent Swarm)**：验证 exec → config.json → swarm_consumer.py → swarm-report.md 链路

### v1.2.2 (2026-02-04)
**改进点**:
- ✅ 增补“mini_kv + pytest”完整迭代案例（T02），并记录：虚拟环境/依赖安装限制 + `pip3` + `--break-system-packages` 解决办法
- ✅ 强调 `pip install` 可能因 PEP 668/externally-managed 限制失败，需使用 `pip3` 或系统包 + `--break-system-packages` 作为备选

### v1.2.1 (2026-02-04)
**改进点**:
- ✅ 补充 `exec.workdir` 需要“目录预先存在”的注意事项与推荐流程（避免 silently fallback）

### v1.2.0 (2026-02-04)
**改进点**:
- ✅ 统一 Quick Mode 的 one-shot 命令为 `kimi --print -p "..."`（移除 `kimi '...'` 误导写法）
- ✅ 增加“会话模型 + kimi-cli + Kimi CLI”的架构与职责分工说明
- ✅ 增加 429 rate limit 的处理 SOP（识别/等待/记录/补跑）
- ✅ 更新测试计划进度（L1 已完成）

### v1.1.0 (2026-02-04)
**改进点**:
- ✅ 修正命令格式为 `kimi --print -p "prompt"`
- ✅ 添加明确指定 `python3` 的最佳实践（避免环境问题）
- ✅ 添加 Prompt 最佳实践章节
- ✅ 创建 50 任务测试套件（L1-L5）

### v1.0.0 (2026-02-04)
**初始版本**:
- 基础 PTY 模式支持
- Quick Mode 和 Interactive Mode
- 文档结构建立

---

## 测试计划（50 任务）

**目标**：50 道测试任务，迭代优化 Skill

| 阶段 | 任务数 | 状态 |
|------|--------|------|
| L1 基础 | 10 | ✅ 完成 (10/10) |
| L2 中等 | 15 | 待开始 |
| L3 复杂 | 15 | 待开始 |
| L4 交互 | 5 | 待开始 |
| L5 调试 | 5 | 待开始 |

**当前进度**：20% (10/50)
