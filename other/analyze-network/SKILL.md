---
name: analyze-network
description: 分析 agent-ebpf-filter 捕获的网络流量，查询网络连接、识别异常行为、追踪特定进程的网络活动。
---

# Analyze Network - 网络流量分析

本 skill 用于分析 agent-ebpf-filter 捕获的网络活动，包括 TCP/UDP 连接、DNS 查询、TLS SNI 等信息。

## 使用场景

- 查看当前活跃的网络连接
- 追踪特定进程的网络行为
- 识别异常或未授权的网络访问
- 分析 Agent 的出站连接模式
- 调查可疑的网络活动

## 可用数据源

### 1. 网络流量快照（MCP 工具）

使用 `get_network_flows` MCP 工具获取当前网络流量摘要：

```
返回字段：
- flowID: 流的唯一标识
- srcIP, dstIP: 源/目标 IP
- srcPort, dstPort: 源/目标端口
- protocol: TCP/UDP
- comm: 发起连接的命令名
- pid: 进程 ID
- direction: inbound/outbound
- state: 连接状态（ESTABLISHED, CLOSED, FAILED 等）
- firstSeen, lastSeen: 首次/最后观测时间
- sni: TLS SNI（如果可用）
- dnsName: DNS 名称（如果已关联）
- httpHost: HTTP Host 头（如果可用）
- alpn: ALPN 协议（如果可用）
```

### 2. 原始事件查询（MCP 工具）

使用 `query_events` MCP 工具过滤网络相关事件：

```json
{
  "eventType": "connect",
  "limit": 100
}
```

支持的网络事件类型：
- `connect`: TCP 连接尝试
- `bind`: 端口绑定
- `sendto`: UDP 发送
- `recvfrom`: UDP 接收

还可以按 `comm` 或 `pid` 过滤。

### 3. 完整事件历史

使用 `tail_events` MCP 工具获取最近的所有事件（包括网络事件）。

## 分析模式

### 模式 1：按进程分析网络活动

```
步骤：
1. 使用 query_events 过滤特定 comm 或 pid 的 connect 事件
2. 分析目标 IP/端口分布
3. 识别：
   - 高频连接目标
   - 异常端口（非 80/443/22）
   - 外网访问 vs 内网访问
   - 失败的连接尝试
```

### 模式 2：识别异常出站连接

```
分析要点：
1. 非预期的目标 IP（非 API 服务器、非公司网络）
2. 非标准端口（非 80/443/22/3306/5432 等）
3. 短时间内大量连接尝试
4. 到已知恶意 IP 的连接
5. DNS 查询与后续连接不匹配
```

### 模式 3：网络指纹分析

```
提取特征：
1. TLS SNI 模式（API 域名、CDN 域名）
2. 端口使用模式
3. 连接时序（短连接 vs 长连接）
4. 协议分布（HTTP/HTTPS/gRPC/WebSocket）
5. 流量方向（主要出站 vs 入站监听）
```

### 模式 4：关联分析

关联维度：

| # | 关联维度 | 说明 |
| --- | --- | --- |
| 1 | 网络事件 + 文件访问 | 读取配置后连接服务器 |
| 2 | 网络事件 + 进程创建 | fork 后立即连接 |
| 3 | DNS 查询 + TCP 连接 | 域名解析后连接 IP |
| 4 | TLS 捕获 + 网络流 | 明文 payload 关联 |

## 典型查询示例

### 示例 1：查看所有活跃连接

```
调用 get_network_flows MCP 工具
过滤 state = "ESTABLISHED"
按 comm 分组统计
```

### 示例 2：追踪 Claude 的网络活动

```
调用 query_events，参数：
{
  "comm": "claude",
  "eventType": "connect",
  "limit": 200
}

分析返回的所有 connect 事件：
- 提取目标 IP 和端口
- 识别 API 端点模式
- 检查是否有非预期连接
```

### 示例 3：检测端口扫描行为

步骤：

1. 调用 `tail_events` 获取最近 500 个事件。
2. 过滤 `eventType = "connect"`。
3. 按 `pid` 分组，统计每个 pid 连接的不同端口数。
4. 如果某个 pid 在短时间内连接了 `>10` 个不同端口，标记为可疑。

### 示例 4：分析失败的连接

```
调用 get_network_flows
过滤 state = "FAILED"
分析失败原因：
- 目标不可达（网络策略阻止？）
- 连接超时（服务器无响应？）
- 被 cgroup sandbox 阻止？
```

## 与安全策略集成

### 自动化响应流程

```
1. 检测阶段：
   - 持续监控网络流量
   - 应用异常检测规则
   
2. 判断阶段：
   - 提取可疑连接特征（IP/端口/频率）
   - 查询 IP 信誉数据库（外部）
   
3. 响应阶段：
   - 低风险：记录告警
   - 中风险：使用 block_network_destination 阻止该 IP/端口
   - 高风险：使用 block_process_cgroup 隔离整个进程
```

### 白名单管理

```
常见合法目标需要白名单：
- API 服务器（api.anthropic.com, api.openai.com 等）
- CDN（*.cloudflare.com, *.amazonaws.com 等）
- 包管理器（pypi.org, registry.npmjs.org 等）
- 版本控制（github.com, gitlab.com 等）

在应用阻止规则前，先检查目标是否在白名单中。
```

## 数据保留和隐私

- 网络流量快照保留在内存中，默认 10 分钟后过期
- 原始事件可选持久化到 JSONL（如果启用 `logPersistenceEnabled`）
- TLS 明文捕获需要显式启用（默认关闭）
- 敏感数据（Authorization headers, API keys）会被自动脱敏

## 性能考虑

- 网络流量聚合在内存中进行，轻量级
- 原始 syscall 事件量较大，建议按需查询而非全量拉取
- 使用 `limit` 参数控制返回结果数量
- 长期分析可导出到外部 SIEM 系统（通过 OTLP 或 JSONL）

## 限制

- 无法捕获加密后的 payload（除非启用 TLS 捕获）
- 无法解析应用层协议（除 HTTP/DNS/TLS SNI）
- 不记录数据包内容，仅记录元数据
- cgroup 级别的网络拦截只能按 IP/端口，不能按域名

## 验证方法

1. 启动一个已追踪的进程（如 `python3` agent）
2. 让它发起网络连接（如访问 API）
3. 调用 `get_network_flows` 查看该连接是否出现
4. 调用 `query_events` 过滤该进程的 `connect` 事件
5. 验证 srcIP、dstIP、port、state 等字段是否正确
