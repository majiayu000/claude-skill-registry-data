---
name: Deep Analysis
description: Perform complex fault analysis requiring multi-step diagnostics and subtask decomposition. Use when user asks to "troubleshoot", "analyze root cause", "why is network slow", "cannot access server", or needs systematic network fault diagnosis.
version: 1.0.0

# OLAV Extended Fields
intent: diagnose
complexity: complex

# Output Configuration
output:
  format: markdown
  language: auto
  sections:
    - summary
    - details
    - recommendations
---

# Deep Analysis

## Applicable Scenarios
- Network fault troubleshooting
- Performance problem analysis
- Path tracing
- Root cause identification

## Identification Signals
User questions contain: "why", "troubleshoot", "analyze", "fault", "not working", "cannot access", "slow"

## Execution Strategy
1. **Use write_todos to decompose problems**
2. Identify problem type and choose analysis direction
3. Delegate to appropriate Subagent
4. Synthesize analysis and provide conclusions and recommendations

## Subagent Delegation Strategy (Phase 3)

### How to Use Subagents

OLAV now supports specialized Subagents for complex analysis tasks. Use the `task` tool to delegate:

```
task(subagent_type="macro-analyzer", task_description="...")
task(subagent_type="micro-analyzer", task_description="...")
```

### macro-analyzer (Macro Analysis Agent)

**When to Use**:
- "Which node is the problem"
- "Where is packet loss on the path"
- "How large is the fault scope"
- Need to view topology relationships
- End-to-end connectivity issues
- Multi-device failures
- Routing path analysis
- BGP/OSPF neighbor problems

**Delegation Method**:
```
task(subagent_type="macro-analyzer",
     task_description="Analyze the path from R1 to R3, locate which node causes packet loss. Please:
     1. Execute traceroute to trace the path
     2. Check BGP/OSPF neighbor status
     3. Determine fault domain and impact scope
     Return: Fault node location, impact scope description")
```

**Subagent Capabilities**:
- Network topology analysis (LLDP/CDP/BGP)
- Data path tracing (traceroute, routing table)
- End-to-end connectivity checks
- Fault domain identification

### micro-analyzer (Micro Analysis Agent)

**When to Use**:
- "Why is this port not working"
- "Interface has errors"
- Need to troubleshoot specific device layer-by-layer
- Single port failure
- High interface error counts
- VLAN issues
- ARP/MAC problems

**Delegation Method**:
```
task(subagent_type="micro-analyzer",
     task_description="Perform TCP/IP layer-by-layer troubleshooting for R1's Gi0/1:
     1. Physical layer: Check interface status, CRC errors, optical power
     2. Data link layer: Check VLAN, MAC table, STP
     3. Network layer: Check IP configuration, routing, ARP
     Analyze layer by layer and return results for each layer")
```

**Subagent Capabilities**:
- TCP/IP layer-by-layer troubleshooting (physical to application layer)
- Deep device diagnostics
- Interface-level problem identification
- Configuration checks and validation

### Combined Usage Strategy (Recommended)

**Two-Stage Analysis Method**:
1. **Stage 1: Delegate macro-analyzer**
   - Goal: Determine fault domain
   - Output: Problem device/interface list

2. **Stage 2: Delegate micro-analyzer**
   - Goal: Locate specific root cause
   - Output: Layer-by-layer check results

**Example**:
```
# User: "R1 to R3 network is slow"

# Agent Response:
# 1. Use macro analysis to locate problem
task("macro-analyzer", "Check R1-R3 path, find which node is slow")

# 2. Based on macro analysis, use micro analysis to dig deeper
task("micro-analyzer", "Perform TCP/IP layer-by-layer troubleshooting on [R2], find why network is slow")

# 3. Synthesize subagent results and generate report
```

## TCP/IP Layer-by-Layer Troubleshooting Framework (Micro)

### 1. Physical Layer
**Symptoms**: Complete communication failure, link down
**Check**:
```bash
show interfaces status          # Port status
show interfaces transceiver     # Optical module info
show interfaces counters errors # Error counts
```
**Common Issues**: Optical module failure, high optical power loss, cable damage, CRC errors

### 2. Data Link Layer
**Symptoms**: Link up but cannot ping
**Check**:
```bash
show vlan brief                 # VLAN status
show mac address-table          # MAC table
show spanning-tree              # STP status
show lldp neighbors             # Neighbor discovery
```
**Common Issues**: VLAN mismatch, STP blocked, MAC not learned

### 3. Network Layer
**Symptoms**: Cannot communicate across subnets
**Check**:
```bash
show ip interface brief         # IP status
show ip route                   # Routing table
show arp                        # ARP table
show ip ospf neighbor           # OSPF neighbors
show ip bgp summary             # BGP neighbors
```
**Common Issues**: Missing route, ARP unresolved, routing protocol not established

### 4. Transport Layer
**Symptoms**: Some applications not working
**Check**:
```bash
show access-lists               # ACL rules
show ip nat translations        # NAT table
show control-plane              # CoPP configuration
```
**Common Issues**: ACL blocking, NAT misconfiguration, port filtering

### 5. Application Layer
**Symptoms**: Specific application failure
**Check**:
```bash
show ip dns server              # DNS configuration
show running-config | include service # Application services
```
**Common Issues**: DNS resolution failure, service not enabled

## Typical Fault Scenarios

### Scenario 1: Slow Network
1. macro-analyzer: traceroute to locate slow node
2. micro-analyzer: Check node interface errors, CPU, queues

### Scenario 2: Cannot Access Server
1. macro-analyzer: Check end-to-end path
2. micro-analyzer: Start from server and troubleshoot toward source

### Scenario 3: Route Flapping
1. macro-analyzer: Check all BGP/OSPF neighbors
2. micro-analyzer: Check problem neighbor's interface and route configuration

### Scenario 4: Broadcast Storm
1. macro-analyzer: Determine storm scope
2. micro-analyzer: Find loop port, check STP

## Output Format
Use structured report:
```
## 故障分析报告

### 问题概述
用户反映: 从上海到北京专线不稳定

### 宏观分析 (macro-analyzer)
1. 路径: 上海路由器 → 出口 → 运营商 → 北京入口
2. 故障点: 上海路由器 Gi0/1 接口错误率高
3. 影响范围: 所有经该接口的流量

### 微观分析 (micro-analyzer)
1. 物理层: 接口up，CRC错误增长中
2. 数据链路层: 正常
3. 网络层: 正常
4. **根因**: 光模块老化，接收功率偏低

### 建议
1. 更换上海路由器 Gi0/1 光模块
2. 临时方案: 降低接口速率至1G
```

## 学习行为
成功解决后，将案例保存到 knowledge/solutions/:
```markdown
# 案例: [问题标题]

## 问题描述
[用户描述]

## 排查过程
1. [第一步]
2. [第二步]
...

## 根因
[根本原因]

## 解决方案
[解决方法]

## 关键命令
- command1
- command2

## 标签
#标签1 #标签2
```
