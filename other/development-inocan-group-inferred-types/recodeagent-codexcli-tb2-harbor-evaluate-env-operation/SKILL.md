---
name: ReCodeAgent-CodexCLI-TB2-Harbor-Evaluate-ENV-Operation
description: Guide for running ReCodeAgent-Codex-TB2 Harbor ENV Run terminal-bench-2 BENCHMARK Evaluate TASKs Operation Guide
---

# ReCodeAgent-Codex-TB2 Harbor ENV Run terminal-bench-2 BENCHMARK Evaluate TASKs Operation Guide

> **版本**: v0.2.0
> **更新日期**: 2025-11-22
> **作者**: ReCodeAgent Team

---

## 目录

1. [环境架构](#1-环境架构)
2. [Rust Core 构建](#2-rust-core-构建)
3. [Docker 镜像配置与构建](#3-docker-镜像配置与构建)
4. [Prompt 模板同步机制](#4-prompt-模板同步机制)
5. [Harbor Agent 集成机制](#5-harbor-agent-集成机制)
6. [Harbor Run 命令参数说明](#6-harbor-run-命令参数说明)
7. [开发环境修改与同步测试流程](#7-开发环境修改与同步测试流程)
8. [实时遥测与监控](#8-实时遥测与监控)
9. [任务结果分析](#9-任务结果分析)

---

## 1. 环境架构

### 1.1 整体架构图

```text
┌─────────────────────────────────────────────────────────────────────────┐
│                     macOS 开发环境 (Host)                               │
├─────────────────────────────────────────────────────────────────────────┤
│  ReCodeAgent 开发仓库                                                   │
│  /Users/arthur/dev-space/ReCodeAgent/                                   │
│  ├── recode-core/           # Rust 核心实现                             │
│  │   ├── src/               # 源代码                                    │
│  │   ├── templates/         # Jinja2 Prompt 模板 (源)                   │
│  │   └── Cargo.toml         # Rust 依赖配置                             │
│  └── scripts/               # Python 桥接脚本                           │
│      └── terminal_bench_bridge.py                                       │
├─────────────────────────────────────────────────────────────────────────┤
│  Harbor 安装目录 (uv tools)                                             │
│  /Users/arthur/.local/share/uv/tools/harbor/                            │
│  └── lib/python3.13/site-packages/harbor/agents/installed/              │
│      ├── recode_agent.py           # Harbor Agent 定义                  │
│      ├── install-recode-agent.sh.j2 # 安装脚本模板                      │
│      └── recode-assets/            # 资产目录                           │
│          ├── recode-agent          # Linux x86_64 二进制                │
│          ├── templates/            # Jinja2 模板 (部署)                 │
│          └── scripts/              # Python 桥接脚本                    │
├─────────────────────────────────────────────────────────────────────────┤
│  Harbor Workspace                                                       │
│  /Users/arthur/harbor-workspace/                                        │
│  └── jobs/                   # 任务执行结果存储                         │
│      └── YYYY-MM-DD__HH-MM-SS/                                          │
│          └── task-name__ID/  # 每个任务的独立目录                       │
└─────────────────────────────────────────────────────────────────────────┘
                                    │
                                    │ Docker Volume Mount
                                    │ ${HOME}/.codex:/tmp/host-codex:ro
                                    ▼
┌─────────────────────────────────────────────────────────────────────────┐
│                 Docker Container (Terminal-Bench 2.0)                   │
├─────────────────────────────────────────────────────────────────────────┤
│  /app/                        # 工作目录 (Harbor 标准)                  │
│  ├── recode-agent             # ReCodeAgent Rust 二进制                 │
│  ├── AGENTS.md                # 渲染后的系统提示 (Codex 自动加载)       │
│  ├── instruction.md           # 任务指令文件                            │
│  ├── templates/               # Jinja2 模板                             │
│  ├── scripts/                 # Python 桥接脚本                         │
│  │   └── terminal_bench_bridge.py                                       │
│  └── .codex/                  # Codex CLI 配置                          │
│      ├── auth.json            # 认证信息 (从 Host 复制)                 │
│      └── config.toml          # 配置文件 (模型设置等)                   │
├─────────────────────────────────────────────────────────────────────────┤
│  /installed-agent/            # Harbor 上传的资产                       │
│  ├── recode-agent             # 二进制                                  │
│  ├── templates/               # 模板                                    │
│  ├── scripts/                 # 脚本                                    │
│  └── install.sh               # 安装脚本                                │
├─────────────────────────────────────────────────────────────────────────┤
│  系统组件                                                               │
│  ├── Node.js 22 + npm         # Codex CLI 依赖                          │
│  ├── Codex CLI (@openai/codex) # LLM 交互                               │
│  └── Python 3.12              # 桥接脚本运行时                          │
└─────────────────────────────────────────────────────────────────────────┘
```

### 1.2 执行流程

```text
Harbor Run CMD
     │
     ▼
┌─────────────────┐
│ 1. 上传资产     │  recode-agent, templates/, scripts/
└───────┬─────────┘
        │
        ▼
┌─────────────────┐
│ 2. 运行安装脚本 │  install-recode-agent.sh.j2
└───────┬─────────┘
        │
        ▼
┌─────────────────┐
│ 3. 执行步骤     │  command-0 → command-1 → command-2 → command-3
└───────┬─────────┘
        │
        ├──▶ Step 1: 设置 Codex 认证 (复制 auth.json, config.toml)
        │
        ├──▶ Step 2: 渲染 AGENTS.md (从 Jinja2 模板)
        │
        ├──▶ Step 3: 执行任务 (recode-agent execute + codex exec)
        │
        └──▶ Step 4: 清理 (删除 auth.json)
```

---

## 2. Rust Core 构建

### 2.1 源代码位置

```tree
/Users/arthur/dev-space/ReCodeAgent/recode-core/
├── Cargo.toml              # 依赖配置
├── src/
│   ├── main.rs             # CLI 入口
│   ├── lib.rs              # 库入口
│   ├── codex/              # Codex CLI 集成
│   │   └── thread_manager.rs
│   ├── execution/          # Python 代码执行
│   │   ├── python_executor.rs  # ⚠️ 包含 import re, os 修复
│   │   └── env_adapter.rs
│   ├── orchestrator/       # DFS 树执行引擎
│   │   ├── engine.rs
│   │   └── runtime.rs
│   └── tree/               # 决策树结构
│       └── node.rs
└── templates/              # Jinja2 Prompt 模板 (源)
```

### 2.2 构建命令

#### 本地 macOS 构建 (开发测试)

```bash
cargo build --release --manifest-path recode-core/Cargo.toml
# 输出: recode-core/target/release/recode-core
```

#### Linux x86_64 构建 (Harbor 容器)

```bash
# 使用 Docker 交叉编译
docker build --platform linux/amd64 -f Dockerfile.build-x86 -t recode-builder .

# 提取二进制
docker create --name recode-extract recode-builder
docker cp recode-extract:/build/recode-core/target/release/recode-core ./recode-agent-linux-x86_64
docker rm recode-extract

# 验证
file ./recode-agent-linux-x86_64
# 应输出: ELF 64-bit LSB pie executable, x86-64...
```

### 2.3 Dockerfile.build-x86 内容

```dockerfile
FROM --platform=linux/amd64 rust:1.83-bookworm

WORKDIR /build

RUN apt-get update && apt-get install -y \
    build-essential \
    pkg-config \
    libssl-dev \
    && rm -rf /var/lib/apt/lists/*

COPY . .

RUN cargo build --release --manifest-path recode-core/Cargo.toml

RUN ls -lh recode-core/target/release/recode-core && \
    file recode-core/target/release/recode-core
```

### 2.4 关键依赖

| 依赖 | 版本 | 用途 |
|------|------|------|
| tokio | 1.35 | 异步运行时 |
| clap | 4.4 | CLI 参数解析 |
| serde/serde_json | 1.0 | JSON 序列化 |
| tree-sitter | 0.20 | Python AST 解析 |
| minijinja | 2.12 | Jinja2 模板渲染 |
| tracing | 0.1 | 日志追踪 |

---

## 3. Docker 镜像配置与构建

### 3.1 Dockerfile 位置与内容

```bash
/Users/arthur/dev-space/ReCodeAgent/recode-core/Dockerfile
```

```dockerfile
# ReCodeAgent-Codex-TB2 Container Unified Architecture
FROM node:20-slim

# 安装 Python 和系统依赖
RUN apt-get update && apt-get install -y \
    python3 python3-pip python3-venv curl ca-certificates \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# 安装 Codex CLI
RUN npm install -g @openai/codex@latest

# 复制 ReCodeAgent 二进制和模板
COPY target/release/recode-core /app/recode-agent
RUN chmod +x /app/recode-agent
COPY templates/ /app/templates/

# Python 依赖
RUN pip3 install --no-cache-dir --break-system-packages anthropic requests

# Codex 配置目录 (运行时通过 Volume Mount 填充)
RUN mkdir -p /app/.codex

ENV CODEX_HOME=/app/.codex
ENV PATH="/app:${PATH}"
ENV RUST_LOG=info

CMD ["/bin/bash"]

LABEL architecture="linux/amd64"
LABEL version="0.2.0"
```

### 3.2 构建 Docker 镜像 (可选, Harbor 不直接使用)

```bash
cd /Users/arthur/dev-space/ReCodeAgent/recode-core

# 先构建 Linux 二进制
docker build --platform linux/amd64 -f ../Dockerfile.build-x86 -t recode-builder ..
docker create --name tmp recode-builder
docker cp tmp:/build/recode-core/target/release/recode-core target/release/recode-core
docker rm tmp

# 构建最终镜像
docker build --platform linux/amd64 -t recode-agent-codex-tb2:latest .
```

> **注意**: Harbor 不直接使用此 Docker 镜像。Harbor 使用 Terminal-Bench 2.0 的基础镜像，然后通过 `install-recode-agent.sh.j2` 脚本在运行时安装 ReCodeAgent 组件。

---

## 4. Prompt 模板同步机制

### 4.1 模板流转路径

```text
开发环境 (源)                          Harbor 资产目录 (部署)                    容器内 (运行时)
─────────────────                      ──────────────────────                    ─────────────────
recode-core/templates/                 recode-assets/templates/                  /app/templates/
├── recode_tb2_agents_md.jinja2   ──▶  ├── recode_tb2_agents_md.jinja2   ──▶    ├── *.jinja2
├── recode_tb2_prompt.jinja2           ├── recode_tb2_prompt.jinja2             │
├── recode_microtexecute_tb2_...       ├── recode_microtexecute_tb2_...         │
└── ...                                └── ...                                  │
                                                                                │
                                                                                ▼
                                                                            /app/AGENTS.md
                                                                            (渲染后的最终结果)
```

### 4.2 同步命令

```bash
# 从开发环境同步模板到 Harbor 资产目录
cp -r recode-core/templates/*.jinja2 \
  /Users/arthur/.local/share/uv/tools/harbor/lib/python3.13/site-packages/harbor/agents/installed/recode-assets/templates/

# 同步 fewshots 子目录
cp -r recode-core/templates/fewshots/* \
  /Users/arthur/.local/share/uv/tools/harbor/lib/python3.13/site-packages/harbor/agents/installed/recode-assets/templates/fewshots/
```

### 4.3 模板渲染流程

1. **Harbor 上传**: `recode_agent.py` 将 `recode-assets/templates/` 上传到容器 `/installed-agent/templates/`
2. **安装脚本复制**: `install-recode-agent.sh.j2` 将模板复制到 `/app/templates/`
3. **运行时渲染**: `recode-agent render-template` 命令渲染 AGENTS.md

```bash
# 容器内执行 (Step 2)
/app/recode-agent render-template \
    --template "$TEMPLATE_NAME" \        # e.g., recode_tb2_agents_md.jinja2
    --output /app/AGENTS.md \
    --task-name "$TASK_NAME" \
    --instruction-path /app/instruction.md
```

### 4.4 可用模板列表

| 模板文件 | 用途 | 大小 |
|---------|------|------|
| `recode_tb2_agents_md.jinja2` | **默认** - AGENTS.md 系统提示 | ~21KB |
| `recode_tb2_prompt.jinja2` | TB2 任务 Prompt | ~20KB |
| `recode_microtexecute_tb2_prompt.jinja2` | Codex 扩展用微执行 Prompt | ~25KB |
| `recode_system_prompt.jinja2` | 基础系统提示 | ~4KB |
| `recode_tb2_checkpoint_minimal.jinja2` | Checkpoint 验证 | ~5KB |

---

## 5. Harbor Agent 集成机制

### 5.1 文件结构

```tree
/Users/arthur/.local/share/uv/tools/harbor/lib/python3.13/site-packages/harbor/agents/installed/
├── recode_agent.py              # Harbor Agent 定义 (Python)
├── install-recode-agent.sh.j2   # 安装脚本模板 (Jinja2)
└── recode-assets/               # 资产目录
    ├── recode-agent             # Linux x86_64 二进制 (~7.8MB)
    ├── templates/               # Jinja2 模板
    │   ├── *.jinja2
    │   └── fewshots/
    └── scripts/
        └── terminal_bench_bridge.py  # Python 桥接脚本
```

### 5.2 ReCodeAgent 类核心结构

```python
# recode_agent.py
class ReCodeAgent(BaseInstalledAgent):
    _OUTPUT_FILENAME = "recode.txt"
    _AGENTS_MD_FILENAME = "AGENTS.md"

    def __init__(self, *args, **kwargs):
        self._template = kwargs.get("template", "recode_tb2_agents_md.jinja2")
        self._max_steps = kwargs.get("max_steps", 99999)

    @staticmethod
    def name() -> str:
        return "recode-agent"  # Harbor 识别名称

    async def setup(self, environment):
        # 1. 上传二进制 → /installed-agent/recode-agent
        # 2. 上传模板 → /installed-agent/templates/
        # 3. 上传脚本 → /installed-agent/scripts/
        # 4. 运行安装脚本

    def create_run_agent_commands(self, instruction):
        # 返回 4 个 ExecInput 命令:
        # Step 1: 设置 Codex 认证
        # Step 2: 渲染 AGENTS.md
        # Step 3: 执行任务
        # Step 4: 清理
```

### 5.3 打包与安装流程

#### 方法 A: 手动同步到 uv 安装目录

```bash
# 同步二进制
cp ./recode-agent-linux-x86_64 \
  /Users/arthur/.local/share/uv/tools/harbor/lib/python3.13/site-packages/harbor/agents/installed/recode-assets/recode-agent

# 同步模板
cp -r recode-core/templates/*.jinja2 \
  /Users/arthur/.local/share/uv/tools/harbor/lib/python3.13/site-packages/harbor/agents/installed/recode-assets/templates/

# 同步脚本
cp scripts/terminal_bench_bridge.py \
  /Users/arthur/.local/share/uv/tools/harbor/lib/python3.13/site-packages/harbor/agents/installed/recode-assets/scripts/
```

#### 方法 B: 从 Harbor 开发仓库安装

```bash
# 如果修改了 recode_agent.py 或其他 Harbor 代码
cd /Users/arthur/dev-space/harbor
uv pip install -e .
```

---

## 6. Harbor Run 命令参数说明

### 6.1 基础语法

```bash
harbor run [OPTIONS]
```

### 6.2 ReCodeAgent 相关参数

| 参数 | 简写 | 说明 | 示例 |
|------|------|------|------|
| `--dataset` | `-d` | 数据集名称@版本 | `terminal-bench@2.0` |
| `--task` | `-t` | 任务名称 | `regex-log`, `password-recovery` |
| `--agent` | `-a` | Agent 名称 | `recode-agent` |
| `--agent-kwarg` | | Agent 参数 (可多次使用) | `template=recode_tb2_prompt.jinja2` |
| `--n-concurrent` | `-n` | 并发数 | `4` |
| `--jobs-dir` | `-o` | 结果存储目录 | `jobs` |
| `--timeout-multiplier` | | 超时倍数 | `1.5` |
| `--debug` | | 启用调试日志 | |
| `--disable-verification` | | 跳过验证 | |

### 6.3 完整命令示例

```bash
# 基础运行 (使用默认模板)
cd /Users/arthur/harbor-workspace
harbor run -d terminal-bench@2.0 -t regex-log -a recode-agent

# 指定模板
harbor run -d terminal-bench@2.0 -t regex-log -a recode-agent \
  --agent-kwarg template=recode_tb2_prompt.jinja2

# 限制最大步数
harbor run -d terminal-bench@2.0 -t regex-log -a recode-agent \
  --agent-kwarg max_steps=100

# 组合多个参数
harbor run -d terminal-bench@2.0 -t password-recovery -a recode-agent \
  --agent-kwarg template=recode_tb2_agents_md.jinja2 \
  --agent-kwarg max_steps=50 \
  --timeout-multiplier 2.0 \
  --debug

# 批量运行所有任务
harbor run -d terminal-bench@2.0 -a recode-agent -n 4
```

### 6.4 环境变量 (容器内)

| 变量 | 说明 |
|------|------|
| `CODEX_HOME` | Codex 配置目录 (`/app/.codex`) |
| `TASK_NAME` | 任务名称 |
| `TEMPLATE_NAME` | 使用的模板文件名 |
| `MAX_STEPS` | DFS 树最大步数 |
| `INSTRUCTION` | 任务指令文本 |
| `RUST_LOG` | Rust 日志级别 (`info`) |

---

## 7. 开发环境修改与同步测试流程

### 7.1 快速同步脚本

创建 `sync-to-harbor.sh`:

```bash
#!/bin/bash
# sync-to-harbor.sh - 同步开发环境修改到 Harbor

set -e

RECODE_DIR="/Users/arthur/dev-space/ReCodeAgent"
HARBOR_ASSETS="/Users/arthur/.local/share/uv/tools/harbor/lib/python3.13/site-packages/harbor/agents/installed/recode-assets"

echo "=== 1. 构建 Linux x86_64 二进制 ==="
cd "$RECODE_DIR"
docker build --platform linux/amd64 -f Dockerfile.build-x86 -t recode-builder .
docker create --name recode-extract recode-builder 2>/dev/null || true
docker cp recode-extract:/build/recode-core/target/release/recode-core "$HARBOR_ASSETS/recode-agent"
docker rm recode-extract 2>/dev/null || true
chmod +x "$HARBOR_ASSETS/recode-agent"
echo "✓ 二进制已同步"

echo ""
echo "=== 2. 同步模板 ==="
cp -r "$RECODE_DIR/recode-core/templates/"*.jinja2 "$HARBOR_ASSETS/templates/"
cp -r "$RECODE_DIR/recode-core/templates/fewshots/"* "$HARBOR_ASSETS/templates/fewshots/" 2>/dev/null || true
echo "✓ 模板已同步"

echo ""
echo "=== 3. 同步桥接脚本 ==="
cp "$RECODE_DIR/scripts/terminal_bench_bridge.py" "$HARBOR_ASSETS/scripts/"
echo "✓ 脚本已同步"

echo ""
echo "=== 同步完成 ==="
ls -la "$HARBOR_ASSETS"
```

### 7.2 开发-测试循环

```bash
# 1. 修改 Rust 代码
vim recode-core/src/execution/python_executor.rs

# 2. 本地快速测试 (macOS)
cargo run --release --manifest-path recode-core/Cargo.toml -- \
  execute --task-name test --instruction "test task" --working-dir /tmp --max-steps 5

# 3. 同步到 Harbor
./sync-to-harbor.sh

# 4. Harbor 测试
cd /Users/arthur/harbor-workspace
harbor run -d terminal-bench@2.0 -t regex-log -a recode-agent --debug

# 5. 检查结果
cat jobs/latest/*/agent/command-2/stdout.txt
```

### 7.3 仅同步模板 (快速)

```bash
# 修改模板后快速同步
cp recode-core/templates/recode_tb2_agents_md.jinja2 \
  /Users/arthur/.local/share/uv/tools/harbor/lib/python3.13/site-packages/harbor/agents/installed/recode-assets/templates/

# 立即测试
harbor run -d terminal-bench@2.0 -t regex-log -a recode-agent
```

---

## 8. 实时遥测与监控

### 8.1 本地开发环境实时输出

```bash
# 本地运行时直接看到输出
cargo run --release --manifest-path recode-core/Cargo.toml -- \
  execute --task-name test --instruction "..." --working-dir . --max-steps 50

# 输出示例:
# 2025-11-22T10:00:00Z INFO recode_core::orchestrator::runtime: Executing pending node...
# 2025-11-22T10:00:01Z INFO recode_core::codex::thread_manager: Codex exec spawned...
```

### 8.2 Harbor 容器内实时监控

#### 方法 A: 使用 docker logs

```bash
# 找到运行中的容器
docker ps | grep terminal-bench

# 实时查看日志
docker logs -f <container-id>
```

#### 方法 B: 使用 docker exec 进入容器

```bash
# 进入容器
docker exec -it <container-name>-main-1 /bin/bash

# 查看实时输出
tail -f /app/recode.txt

# 查看 AGENTS.md
cat /app/AGENTS.md | head -50
```

#### 方法 C: 等待任务完成后查看日志

```bash
# 任务完成后查看详细输出
cat /Users/arthur/harbor-workspace/jobs/YYYY-MM-DD__HH-MM-SS/task-name__ID/agent/command-2/stdout.txt
```

### 8.3 启用详细日志

`RUST_LOG=info` 已在 `recode_agent.py` 中默认启用，会输出:

- 节点执行状态 (`Executing pending node`)
- Codex API 调用 (`Codex exec process spawned`)
- 执行结果 (`Execution successful`)
- 任务完成信号 (`task_completed signal detected`)

---

## 9. 任务结果分析

### 9.1 结果目录结构

```tree
/Users/arthur/harbor-workspace/jobs/2025-11-22__18-03-20/regex-log__532fPEU/
├── config.json           # 任务配置 (包含 kwargs)
├── result.json           # 最终结果 (reward, tokens, etc.)
├── trial.log             # Harbor 试验日志
├── agent/                # Agent 执行日志
│   ├── install.sh        # 渲染后的安装脚本
│   ├── command-0/        # Step 1: Codex 认证设置
│   │   ├── command.txt   # 执行的命令
│   │   ├── stdout.txt    # 标准输出
│   │   └── return-code.txt
│   ├── command-1/        # Step 2: AGENTS.md 渲染
│   ├── command-2/        # Step 3: 任务执行 (主要日志)
│   └── command-3/        # Step 4: 清理
└── verifier/             # 验证结果
    ├── ctrf.json         # 测试框架结果
    ├── reward.txt        # 奖励值 (0.0 或 1.0)
    └── test-stdout.txt   # pytest 输出
```

### 9.2 关键文件分析

#### config.json - 检查参数是否正确传递

```bash
cat config.json | jq '.agent.kwargs'
# 输出: {"template": "recode_tb2_prompt.jinja2"}
```

#### result.json - 检查最终结果

```bash
cat result.json | jq '{reward, n_input_tokens, n_output_tokens}'
```

#### command-2/stdout.txt - 分析执行过程

```bash
# 检查是否有错误
grep -i "ERROR\|NameError\|failed" agent/command-2/stdout.txt

# 检查任务是否完成
grep "task_completed" agent/command-2/stdout.txt

# 检查执行步数
grep "Total steps" agent/command-2/stdout.txt
```

#### verifier/test-stdout.txt - 分析验证失败原因

```bash
# 查看 pytest 输出
cat verifier/test-stdout.txt | tail -30

# 常见失败原因:
# - AssertionError: 输出不匹配预期
# - FileNotFoundError: 未创建预期文件
```

### 9.3 常见问题排查

| 问题 | 检查位置 | 可能原因 |
|------|----------|----------|
| Mean: 0.000 | verifier/test-stdout.txt | LLM 解答错误 |
| Errors: 1 | agent/install.sh + trial.log | 安装脚本超时/OOM |
| 无输出 | agent/command-2/stdout.txt | Codex 认证失败 |
| NameError: 're' | agent/command-2/stdout.txt | 旧版二进制 (已修复) |
| Exec format error | trial.log | macOS 二进制而非 Linux |

### 9.4 批量分析脚本

```bash
# 统计所有任务的 reward
for dir in jobs/2025-11-22__*/*/; do
  task=$(basename "$dir")
  reward=$(cat "$dir/verifier/reward.txt" 2>/dev/null || echo "N/A")
  echo "$task: $reward"
done

# 找出所有失败的任务
find jobs/ -name "reward.txt" -exec grep -l "0.0" {} \; | \
  xargs -I {} dirname {} | xargs -I {} dirname {}
```

---

## 附录 A: 快速参考卡

### 常用命令

```bash
# 构建 Linux 二进制
docker build --platform linux/amd64 -f Dockerfile.build-x86 -t recode-builder .

# 同步到 Harbor
cp ./recode-agent-linux-x86_64 /Users/arthur/.local/share/uv/tools/harbor/.../recode-assets/recode-agent

# 运行任务
harbor run -d terminal-bench@2.0 -t regex-log -a recode-agent

# 查看最新结果
cat jobs/$(ls -t jobs | head -1)/*/agent/command-2/stdout.txt | tail -50
```

### 关键路径

| 描述 | 路径 |
|------|------|
| Rust 源码 | `recode-core/src/` |
| 模板源 | `recode-core/templates/` |
| Harbor 二进制 | `~/.local/share/uv/tools/harbor/.../recode-assets/recode-agent` |
| Harbor 模板 | `~/.local/share/uv/tools/harbor/.../recode-assets/templates/` |
| 任务结果 | `~/harbor-workspace/jobs/` |

---

## 附录 B: 故障排除

### B.1 "Exec format error"

**原因**: 使用了 macOS 二进制而非 Linux x86_64 二进制

**解决**:

```bash
# 重新构建 Linux 二进制
docker build --platform linux/amd64 -f Dockerfile.build-x86 -t recode-builder .
# 提取并部署...
```

### B.2 "NameError: name 're' is not defined"

**原因**: 旧版 `python_executor.rs` 未导入 `re` 模块

**解决**: 已在 `python_executor.rs:228` 修复:

```rust
script.push_str("import json, sys, re, os\n");
```

### B.3 "Install script failed with return code 137"

**原因**: 容器 OOM 或超时

**解决**:

1. 重试运行 (可能是瞬态问题)
2. 增加超时: `--timeout-multiplier 2.0`
3. 检查 Docker 资源限制

### B.4 "No auth.json found"

**原因**: Codex 认证未挂载到容器

**解决**: 确保 `docker-compose-prebuilt.yaml` 包含:

```yaml
volumes:
  - ${HOME}/.codex:/tmp/host-codex:ro
```

---

END OF FILE
