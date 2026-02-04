---
name: tunnel-debug
description: 隧道调试技能。诊断和排查隧道连接问题，包括连接失败、数据传输异常、性能问题等。关键词：调试、排查、诊断、问题、连接失败、超时。
allowed-tools: Read, Grep, Glob, Bash
---

# 隧道调试技能

## 常见问题诊断流程

### 问题1: 客户端无法连接服务器

**症状**: 客户端启动后报 `connection refused` 或 `timeout`

**诊断步骤**:

```bash
# 1. 检查服务端是否运行
ps aux | grep tunnox-server

# 2. 检查服务端监听端口
lsof -i :8000
netstat -an | grep 8000

# 3. 检查防火墙
# macOS
sudo pfctl -s rules

# Linux
sudo iptables -L

# 4. 测试网络连通性
telnet 127.0.0.1 8000
nc -zv 127.0.0.1 8000

# 5. 查看服务端日志
tail -100 ~/logs/server.log
```

**常见原因**:
- 服务端未启动
- 端口被占用
- 防火墙阻断
- 地址配置错误

### 问题2: 握手失败

**症状**: 连接建立但握手超时或认证失败

**诊断步骤**:

```bash
# 1. 查看客户端日志
tail -100 /tmp/tunnox-client.log

# 2. 查看服务端日志
grep -i "handshake\|auth" ~/logs/server.log

# 3. 检查 JWT Token
# 确认 token 未过期

# 4. 检查时钟同步
date
# 服务器和客户端时间差不应超过 5 分钟
```

**常见原因**:
- JWT Token 过期
- 客户端 ID 不匹配
- 时钟不同步
- 协议版本不兼容

### 问题3: 隧道建立失败

**症状**: 使用连接码后无法建立隧道

**诊断步骤**:

```bash
# 1. 检查连接码状态
# 在客户端 CLI 中
tunnox> list-codes

# 2. 查看服务端连接码记录
grep -i "connection_code\|code" ~/logs/server.log

# 3. 检查目标端客户端状态
tunnox> status

# 4. 验证目标服务可达
# 在目标端机器上
telnet localhost 3306
```

**常见原因**:
- 连接码已过期
- 连接码已被使用
- 目标端客户端离线
- 目标服务不可达

### 问题4: 数据传输异常

**症状**: 隧道建立成功但数据传输失败或丢失

**诊断步骤**:

```bash
# 1. 检查数据包日志
grep -i "packet\|forward" ~/logs/server.log | tail -50

# 2. 检查压缩/加密配置
# 确认两端配置一致

# 3. 抓包分析
# 服务端
tcpdump -i any port 8000 -w capture.pcap

# 4. 检查内存使用
ps aux | grep tunnox

# 5. 检查 goroutine 数量
# 需要开启 pprof
curl http://localhost:6060/debug/pprof/goroutine?debug=1
```

**常见原因**:
- 压缩/加密配置不匹配
- 缓冲区溢出
- 内存泄漏
- 连接被意外关闭

### 问题5: 性能问题

**症状**: 延迟高、吞吐量低

**诊断步骤**:

```bash
# 1. 测量网络延迟
ping -c 10 server-ip

# 2. 测量吞吐量
# 使用 iperf3
iperf3 -c server-ip -p 8000

# 3. 检查 CPU 使用
top -pid $(pgrep tunnox)

# 4. 检查内存使用
ps aux | grep tunnox

# 5. 分析热点
# 需要开启 pprof
go tool pprof http://localhost:6060/debug/pprof/profile?seconds=30
```

**常见原因**:
- 网络延迟高
- CPU 瓶颈（压缩/加密）
- 内存不足
- 缓冲区配置不当

## 日志分析

### 日志位置

```
服务端: ~/logs/server.log
目标端客户端: /tmp/tunnox-target-client.log
源端客户端: /tmp/tunnox-listen-client.log
```

### 关键日志模式

```bash
# 连接相关
grep -E "connect|disconnect|accept" server.log

# 握手相关
grep -E "handshake|auth|jwt" server.log

# 隧道相关
grep -E "tunnel|mapping|forward" server.log

# 错误相关
grep -E "error|fail|timeout" server.log

# 性能相关
grep -E "latency|throughput|buffer" server.log
```

### 日志级别调整

```yaml
# config.yaml
log:
  level: debug  # 临时调试时使用 debug
```

## 常用诊断命令

### 网络诊断

```bash
# 检查端口监听
lsof -i :8000

# 检查连接状态
netstat -an | grep 8000

# 追踪路由
traceroute server-ip

# DNS 解析
nslookup server-domain
dig server-domain
```

### 进程诊断

```bash
# 查看进程
ps aux | grep tunnox

# 查看线程
ps -M $(pgrep tunnox-server)

# 查看文件描述符
lsof -p $(pgrep tunnox-server)

# 查看内存映射
pmap $(pgrep tunnox-server)
```

### 性能诊断

```bash
# CPU 采样
perf record -p $(pgrep tunnox-server) -g -- sleep 30
perf report

# 内存分析
go tool pprof http://localhost:6060/debug/pprof/heap

# goroutine 分析
go tool pprof http://localhost:6060/debug/pprof/goroutine
```

## 问题报告模板

```markdown
## 问题报告

**环境信息**:
- OS: macOS 14.0 / Linux 5.x
- Go 版本: 1.24
- Tunnox 版本: v1.1.11
- 协议: TCP / WebSocket / KCP / QUIC

**问题描述**:
[描述问题现象]

**复现步骤**:
1. 步骤1
2. 步骤2
3. 步骤3

**预期行为**:
[描述预期结果]

**实际行为**:
[描述实际结果]

**日志片段**:
```
[粘贴相关日志]
```

**诊断结果**:
[诊断过程和发现]

**可能原因**:
[分析可能的原因]

**建议修复**:
[提供修复建议]
```

## 快速检查清单

```markdown
## 快速检查

### 服务端
- [ ] 进程运行中
- [ ] 端口监听正常
- [ ] 日志无错误
- [ ] 内存/CPU 正常

### 客户端
- [ ] 进程运行中
- [ ] 网络可达
- [ ] Token 有效
- [ ] 配置正确

### 网络
- [ ] 端口开放
- [ ] 防火墙允许
- [ ] DNS 解析正常
- [ ] 延迟可接受

### 隧道
- [ ] 连接码有效
- [ ] 目标端在线
- [ ] 目标服务可达
- [ ] 配置匹配
```
