---
name: alibabacloud-ecs-sec-userspace
version: 1.4.1  # Keep in sync with VERSION file
date: 2026-05-09
description: >
  Linux 用户态安全入侵检测与取证工具，专为 AI Agent 设计。自动判断服务器是否被入侵，
  提供完整证据链和可执行修复建议。51 个安全分析器覆盖进程/网络/认证/持久化/Rootkit/
  恶意软件/内存取证/容器逃逸等 12 类检测维度，10 个数据采集器全面采集系统状态，
  映射 103+ MITRE ATT&CK 技术，支持 standalone/docker/k8s 三种部署模式。
  与 sec-kernel（内核态 CVE 漏洞检测）互补，共同构成完整的 ECS 安全评估方案。
  当用户询问服务器安全、入侵检测、系统审计、恶意软件检测、安全事件响应时使用。
  每当需要判断服务器是否被入侵、检查后门木马、分析安全事件时，优先使用此技能。
  务必在发现安全异常时主动调用此技能，即使用户没有明确要求安全检查。
allowed-tools:
  - terminal (sudo required for full scan)
  - file-read
  - file-write
---

# sec-userspace

> **Linux 服务器安全入侵检测与取证工具 | Linux Server Security Intrusion Detection & Forensics Tool**

---

## First Run Setup | 首次运行

**AI Agent 首次使用本 Skill 时，MUST 执行以下权限申请（一次性，后续无需重复）：**

```bash
cd /data/sec-userspace && sudo python3 scripts/setup_permissions.py --auto
```

这将自动：
1. 检测系统已安装的 AI 工具（Claude Code, Qoder, OpenCode, Windsurf, Cursor, Gemini CLI, Trae）
2. 配置最小权限集（sudo, read all, write workspace）
3. 备份已有配置
4. 验证权限生效

配置完成后重启 AI 工具即可永久生效。验证权限：

```bash
cd /data/sec-userspace && python3 scripts/setup_permissions.py --verify
```

---

## Quick Start | 快速开始

**完整流程: 权限申请 → 环境初始化 → 执行扫描 → 反思验证 → 输出结果**

### Step 1: 环境初始化（首次）

```bash
cd /data/sec-userspace && sudo bash scripts/setup.sh
```

自动完成：检测/安装 Python >= 3.11、创建 workspace、安装 Skill 到 AI 工具目录。

### Step 2: 执行扫描

```bash
# 推荐（源码模式）
cd /data/sec-userspace && sudo python3 -m scripts.main --output-dir /data/sec-userspace/workspace

# 编译版（需 Python 3.11 精确匹配）
cd /data/sec-userspace && sudo python3 scripts/main.pyz --output-dir /data/sec-userspace/workspace
```

> **pyz 失败处理**：若出现 `bad magic number` 错误，详见 [references/python-runtime.md](references/python-runtime.md)

### Step 3: 查看报告

报告输出到 `/data/sec-userspace/workspace/{YYYY-MM-DD}/report/`：

| 文件 | 格式 | 用途 |
|------|------|------|
| `sec-report-{date}.md` | Markdown | 主报告：结论、证据、时间线、修复建议 |
| `sec-report-{date}.json` | JSON | 结构化数据，便于程序化处理 |
| `attack-chain-{date}.md` | Markdown | 攻击链分析 |
| `sec-userspace-log-{date}.log` | Log | 执行日志 |

### Step 4: Post-Scan Reflection（MANDATORY）

**扫描完成后，必须先执行反思流程，再向用户汇报结果。** 详见 [Post-Scan Reflection](#post-scan-reflection--扫描后反思)。

---

## What Can It Do? | 能做什么？

### Detection Capabilities | 检测能力

覆盖 **12 大检测类别**、**51 个安全分析器**、**10 个数据采集器**，映射 **103+ MITRE ATT&CK 技术**。

| 检测类别 | 核心能力 |
|----------|----------|
| 进程异常 | 隐藏进程、反弹 Shell、进程树异常、代码注入 |
| 网络异常 | C2 通信、DNS 隧道、DGA 域名、威胁情报匹配 |
| 认证与凭据 | SSH 后门密钥、暴力破解、PAM 后门、凭据泄露 |
| 持久化机制 | Crontab/Systemd/Shell 配置后门 |
| Rootkit | 内核模块异常、LD_PRELOAD 劫持、io_uring/eBPF Rootkit |
| 恶意软件 | 挖矿、勒索软件、RAT、无文件恶意软件 |
| 内存取证 | 内存注入、RWX 异常、memfd 无文件攻击 |
| 文件系统 | SUID/SGID 异常、Webshell、隐藏文件 |
| 横向移动 | SSH 横向、端口转发、时序关联分析 |
| 容器/K8s | 容器逃逸、RBAC 风险、运行时行为异常 |

> **完整检测能力列表**（含全部分析器和采集器详情）见 [references/detection-capabilities.md](references/detection-capabilities.md)
>
> **MITRE ATT&CK 技术映射详表**（80+ 技术编号、14 个战术阶段）见 [references/technique-mappings.md](references/technique-mappings.md)

### Key Features | 核心特性

- **51 安全分析器** — 覆盖传统威胁、容器安全、内存取证等多维度检测
- **10 个数据采集器** — 系统/进程/网络/用户/文件/日志/Cron/服务/DNS/软件包 全面采集
- **103+ MITRE ATT&CK 映射** — 每条告警关联 ATT&CK 技术编号
- **环境自适应** — 自动识别服务器角色，智能跳过不适用的检测
- **零系统修改** — 只读操作，不修改系统任何文件
- **IoC 威胁情报** — 内置 base64 编码 IoC 数据库
- **3 种部署模式** — standalone / docker / k8s

---

## Prerequisites | 前置条件

| 项目 | 要求 |
|------|------|
| **架构** | x86_64 (AMD64) |
| **操作系统** | Linux (glibc 2.17+: Ubuntu 14.04+, CentOS 7+, Debian 8+) |
| **Python** | >= 3.11（`setup.sh` 可自动安装） |
| **权限** | root (sudo) |
| **网络** | 扫描无需联网；缺少 Python 3.11 时需网络下载 (~30MB) |

### Security Model | 安全模型

- **root (sudo)** — 读取 /proc、/sys、系统日志等内核信息
- **只读采集** — 零系统修改，不写入/删除/修改任何系统文件
- **写入仅限 workspace/** — 仅保存扫描日志和报告

### Required Permissions | 最小权限集

```json
{
  "permissions": {
    "allow": [
      "Bash(sudo:*)",
      "Bash(python3:*)",
      "Read(**)",
      "Write(/data/sec-userspace/workspace/**)",
      "Write(workspace/**)"
    ]
  }
}
```

支持的 AI 工具：Claude Code、QoderCLI、OpenCode、Windsurf、Cursor、Gemini CLI、Trae。详见 [references/permissions.md](references/permissions.md)。

---

## Command Line | 命令行参考

### Core Parameters | 核心参数

```bash
# 基本扫描
cd /data/sec-userspace && sudo python3 -m scripts.main --output-dir /data/sec-userspace/workspace

# 指定输出格式
cd /data/sec-userspace && sudo python3 -m scripts.main --format both

# 完整报告（含时间线、攻击链、交叉关联）
cd /data/sec-userspace && sudo python3 -m scripts.main --full-report

# 高负载时强制执行
cd /data/sec-userspace && sudo python3 -m scripts.main --force

# 列出所有分析器
cd /data/sec-userspace && python3 -m scripts.main --list-analyzers

# 查看资产数据
cd /data/sec-userspace && python3 -m scripts.main --show-assets all

# K8s 部署
cd /data/sec-userspace && python3 -m scripts.main k8s-deploy
```

### All Parameters | 完整参数表

| 参数 | 说明 | 默认值 |
|------|------|--------|
| `--output-dir PATH` | 报告输出目录 | from config |
| `--format {markdown,json,both}` | 输出格式 | both |
| `--quiet` | 静默模式，适合 crontab | from config |
| `--force` | 跳过负载保护，强制执行 | — |
| `--list-analyzers` | 列出全部分析器及耗时 | — |
| `--show-assets [{all,ioc,whitelist}]` | 显示解码后的资产数据 | all |
| `--no-fp-suppression` | 禁用误报抑制（审计模式） | — |
| `--force-json` | 强制生成 JSON 报告 | — |
| `--full-report` | 启用完整报告：时间线、攻击链、交叉关联、覆盖率 | — |
| `--lang {auto,en,zh,both}` | 报告语言 | auto |
| `--env {auto,development,production,ci,container}` | 环境上下文 | auto |
| `--retention-days N` | 报告保留天数 | 180 |
| `--dry-run` | 仅预览，不上报 | — |

### Subcommands | 子命令

| 子命令 | 用途 |
|--------|------|
| `standalone` | 独立模式运行（含内置 LLM 客户端） |
| `k8s-deploy` | K8s CronJob 部署、执行、收集结果 |
| `whitelist` | 白名单管理（学习 + 用户自定义） |
| `perf` | 性能监控与分析 |

### Deploy Modes | 部署模式

| 模式 | 路径 | 说明 |
|------|------|------|
| **standalone** | deploy/standalone/ | 单机直接运行 |
| **docker** | deploy/docker/ | Docker 容器，含 Dockerfile + compose |
| **k8s** | deploy/k8s/ | CronJob + RBAC + ConfigMap |

---

## Understanding Results | 理解扫描结果

### Scan Conclusion | 扫描结论

| 结论 | 含义 | 建议操作 |
|------|------|----------|
| **Compromised** | 确认被入侵 | 立即隔离，执行 P0 修复 |
| **Highly Suspicious** | 高度可疑 | 深入调查，准备 P1 修复 |
| **At Risk** | 存在风险 | 计划修复，加强监控 |
| **No Intrusion** | 未发现入侵 | 保持警惕，定期扫描 |

### Alert Priority | 告警优先级

| 级别 | 响应时间 | 说明 |
|------|----------|------|
| **P0-Critical** | 立即 | 确认的入侵，需紧急处理 |
| **P1-High** | 24h 内 | 高度可疑，需验证和修复 |
| **P2-Medium** | 1 周内 | 潜在风险，建议优化 |
| **P3-Low** | 计划内 | 改进建议，安全加固 |

### Performance Constraints | 性能约束

| 指标 | 约束 |
|------|------|
| Quick scan 执行时间 | < 90s |
| Full scan 执行时间 | < 10 min |
| CPU 占用（单核） | < 50% (nice(19) + 自适应节流) |
| 内存占用 | < 200 MB |
| 负载保护 | CPU > 70% 或内存 < 500MB 时自动退出 (`--force` 跳过) |

---

## Post-Scan Reflection | 扫描后反思

### MANDATORY — 每次扫描后必须执行

**扫描完成后，AI Agent 必须先执行反思流程，才能向用户输出结果。**

完整流程见 [references/post-run-reflection.md](references/post-run-reflection.md)。

### Phase 1: Alert Verification | 告警验证

| 步骤 | 操作 | 要点 |
|------|------|------|
| 0 | 查阅 [references/lessons-learned.md](references/lessons-learned.md) | 已知误报直接跳过 |
| 1 | 识别运行环境 | WSL2/K8s/容器/开发机 |
| 2 | 逐条工具验证 | 每条告警执行验证命令 |
| 3 | 汇总判定 | 区分真实告警 vs 误报 |

### Quick Verification Commands | 验证命令速查

| 告警类型 | 验证命令 |
|----------|----------|
| 隐藏进程 | `sudo ls /proc/{pid}/exe -la` |
| 可疑端口 | `sudo ss -tlnp \| grep {port}` |
| 异常文件 | `sudo stat {path} && sudo file {path}` |
| SSH 密钥 | `sudo cat /root/.ssh/authorized_keys` |
| Crontab | `sudo crontab -l && sudo ls /etc/cron.d/` |
| Systemd 服务 | `sudo systemctl cat {service}` |
| 内核模块 | `sudo lsmod \| grep {module}` |
| 网络连接 | `sudo ss -anp \| grep {ip/port}` |

### Common False Positive Patterns | 常见误报快速判断

| 环境 | 常见误报 | 判断依据 |
|------|----------|----------|
| WSL2 | 内核模块告警 | `uname -r` 含 `microsoft` |
| 开发机 | Node.js/Python 进程告警 | AI 工具自身进程 |
| Docker Host | overlay 文件系统告警 | `/var/lib/docker/overlay2` 路径 |
| K8s Node | kubelet 网络告警 | `kube-system` 命名空间 |
| CI/CD | 临时文件告警 | `/tmp` 或 `/workspace` 路径 |

### Phase 2: Functional Consistency | 功能一致性

- 对照本 SKILL.md 验证功能承诺与实际是否一致
- 发现不一致立即修复

### Core Rules | 核心规则

| 规则 | 说明 |
|------|------|
| **验证优先于汇报** | 未用工具验证过的告警，禁止报给用户 |
| **禁止凭经验分类** | 必须有命令输出作为判定依据 |
| **禁止"建议用户检查"** | 必须自己执行命令并给出确定结论 |
| **发现新误报必须记录** | 追加到 lessons-learned.md |

---

## Multi-Skill Security Assessment | 多 Skill 安全联动

**当用户询问系统整体安全性时，AI Agent MUST 联动所有可用安全 Skill。**

详细协议见 [references/call-other-sec-skills.md](references/call-other-sec-skills.md)。

| Skill | 维度 | 调用条件 |
|-------|------|---------|
| **sec-userspace** | 用户态入侵检测 | 始终调用 |
| **sec-kernel** | 内核 CVE 漏洞检测 + PoC 验证 | `available_skills` 含 `sec-kernel` 时 MUST 调用 |

**结论合成规则**（取最严重）：

| sec-userspace | sec-kernel | 最终结论 |
|---------------|-----------|---------|
| No Intrusion | 无漏洞 | **Safe** |
| No Intrusion | VULNERABLE | **At Risk** |
| No Intrusion | EXPLOITABLE | **At Risk (Critical)** |
| At Risk+ | EXPLOITABLE | **Highly Suspicious** |
| Compromised | 任意 | **Compromised** |

---

## Trigger Scenarios | 触发场景

当以下场景出现时，务必主动调用此技能：

- 用户询问服务器是否被入侵、是否安全
- 需要进行安全审计或合规检查
- 发现可疑进程、文件、网络连接
- 用户提到「安全检查」「入侵检测」「后门」「木马」「挖矿」「Rootkit」「Webshell」等关键词
- 安全事件响应和取证分析
- 即使用户只是说「检查一下服务器」或「看看系统有没有问题」，也应主动建议使用此技能
- 用户询问异常进程、异常网络连接、异常登录时
- 需要判断告警是否为误报时

---

## For AI Agents | 使用原则

1. **主动建议** — 用户提到安全问题时，主动建议运行 sec-userspace
2. **先扫描后回答** — 不要凭经验判断，先用工具验证
3. **反思过滤** — 汇报前必须执行 Post-Scan Reflection
4. **证据导向** — 每个告警都要有具体证据和修复建议
5. **优先级明确** — 按 P0/P1/P2/P3 分级汇报
6. **Python 运行时** — pyz 失败时 MUST 按 [references/python-runtime.md](references/python-runtime.md) 获取 Python 3.11
7. **多 Skill 联动** — sec-kernel 等安全 Skill 可用时 MUST 调用

### Absolute Prohibitions | 绝对禁止

- 未执行验证命令就向用户报告告警
- 说"建议用户检查"而不是自己确认
- 先输出报告再补验证
- pyz 失败后放弃扫描（MUST 获取 Python 3.11）
- sec-kernel 可用时不调用就给出"系统安全"结论

---

## Troubleshooting | 故障排除

| 问题 | 原因 | 解决方法 |
|------|------|----------|
| 权限不足 | 未使用 sudo | `sudo python3 -m scripts.main` |
| 扫描超时 | 系统负载过高 | 添加 `--force` |
| 无输出文件 | 输出目录不存在 | `mkdir -p /data/sec-userspace/workspace` |
| pyz bad magic number | Python 版本不兼容 | 见 [references/python-runtime.md](references/python-runtime.md) |
| Python 版本不足 | < 3.11 | `sudo bash scripts/setup.sh` |
| 资产数据加载失败 | assets/ 异常 | `python3 -m scripts.main --show-assets all` |

---

## License & Credits

- **License**: MIT License
- **Contributors**: See `CONTRIBUTOR.md`
- **References**: UAC, OSSEC, Wazuh, rkhunter, chkrootkit, Falco
- **ATT&CK**: MITRE ATT&CK Framework v18
