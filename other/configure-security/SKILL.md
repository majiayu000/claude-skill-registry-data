---
name: configure-security
description: 配置 agent-ebpf-filter 的安全策略，包括 cgroup 网络拦截、BPF LSM 文件/执行拦截、tracked commands/paths 和 wrapper 规则。
---

# Configure Security - 安全策略配置

本 skill 用于配置 agent-ebpf-filter 的多层安全策略。

## 使用场景

- 添加或删除被追踪的命令/路径
- 配置 wrapper 规则控制命令执行
- 启用 cgroup 网络拦截策略（阻止特定 IP/端口/进程网络访问）
- 启用 BPF LSM 文件/执行拦截策略
- 查看当前安全配置状态

## 前置要求

**重要**：修改安全策略需要在 Runtime Config 中启用 `policyManagementEnabled` 标志。

## 可用操作

### 1. 查看当前配置

使用 MCP 工具 `config_snapshot` 获取完整配置快照：

```
调用 MCP 工具 config_snapshot 可获取：
- 所有 tags
- 所有 tracked commands 及其 tag
- 所有 tracked paths 及其 tag  
- 所有 wrapper rules
- Runtime settings
```

### 2. 添加追踪命令

使用 MCP 工具 `add_tracked_command`：

```json
{
  "command": "python3",
  "tag": "ai-agent"
}
```

追踪命令使用**精确 16 字节匹配**，不支持通配符。

### 3. 添加追踪路径

使用 MCP 工具 `add_tracked_path`：

```json
{
  "path": "/home/user/project/src",
  "tag": "sensitive-code"
}
```

追踪路径使用**精确 256 字节匹配**，不是递归匹配。

### 4. 网络拦截（cgroup sandbox）

#### 阻止 IP 地址访问

```json
{
  "ip": "192.168.1.100"
}
// 或 IPv6
{
  "ip": "2001:db8::1"
}
```

#### 阻止端口访问

```json
{
  "port": 443
}
```

#### 阻止特定进程的所有网络访问

```json
{
  "pid": 12345
}
```

这会阻止该 PID 所在 cgroup 的所有网络流量。

### 5. 文件/执行拦截（BPF LSM）

#### 阻止特定可执行文件路径

```json
{
  "path": "/usr/bin/suspicious-binary",
  "isExec": true
}
```

#### 阻止可执行文件名（basename）

```json
{
  "basename": "malware.exe",
  "isExec": true
}
```

#### 阻止文件/目录名访问

```json
{
  "basename": "secrets.txt",
  "isExec": false
}
```

这会阻止对该 basename 的 open/read/write/mmap 等操作。

## 安全边界说明

### Cgroup Network Sandbox

- **作用范围**：cgroup v2 级别，影响整个 cgroup 内的所有进程
- **拦截点**：kernel `cgroup/connect4`、`cgroup/connect6`、`cgroup/sendmsg4`、`cgroup/sendmsg6`
- **匹配规则**：
  - IP 地址：精确匹配（IPv4 或 IPv6）
  - 端口：精确匹配 TCP/UDP 目标端口
  - Cgroup：按 cgroup v2 inode ID 匹配
- **限制**：不支持 CIDR 或端口范围

### BPF LSM Enforcer

- **作用范围**：全局文件系统 LSM hooks
- **拦截 hooks**：
  - `bprm_check_security`：execve 拦截
  - `file_open`、`file_permission`：文件访问拦截
  - `mmap_file`、`file_mprotect`：内存映射拦截
  - `inode_*`：文件创建/删除/重命名拦截
- **匹配规则**：
  - Exec path：精确路径匹配
  - Exec name：可执行文件 basename 匹配
  - File name：文件/目录 basename 匹配（不是全路径）
- **限制**：不支持通配符或正则表达式

## 验证方法

1. **查看配置**：调用 `config_snapshot` MCP 工具
2. **查看系统健康**：调用 `get_system_health` MCP 工具查看 enforcement 状态
3. **测试拦截**：
   - 网络拦截：尝试访问被阻止的 IP/端口，应失败
   - 文件拦截：尝试访问被阻止的文件，应返回 `EPERM`
   - 执行拦截：尝试执行被阻止的程序，应失败

## 常见场景示例

### 场景 1：阻止 AI Agent 访问外网

```
1. 获取 AI agent 进程的 PID
2. 使用 block_process_cgroup 阻止该 PID 的 cgroup
3. Agent 将无法发起任何网络连接
```

### 场景 2：保护敏感文件

```
1. 使用 block_file_access 阻止 "api_keys.json" basename
2. 所有进程尝试打开该文件名都会被拦截
```

### 场景 3：追踪特定命令的文件访问

```
1. 使用 add_tracked_command 添加 "claude" 命令
2. Dashboard 中会显示所有 claude 进程的 syscall 事件
```

## 注意事项

- **权限要求**：所有策略修改都需要 `policyManagementEnabled=true`
- **持久化**：eBPF maps 会被 pin 到 `/sys/fs/bpf/agent-ebpf/`，重启后保留
- **性能影响**：LSM hooks 在每次文件操作时执行，大量规则可能影响性能
- **恢复方法**：
  - 手动清理：删除 `/sys/fs/bpf/agent-ebpf/` 下的 pinned maps
  - 或通过 UI 的 Security Policies 页面逐条删除规则
