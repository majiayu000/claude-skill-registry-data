---
name: role-qa
description: QA 工程师角色。负责隧道功能测试、性能测试、端到端测试。专注网络连接稳定性、协议兼容性验证。关键词：测试、QA、验证、性能、端到端。
allowed-tools: Read, Write, Bash, Grep, Glob
---

# QA 工程师角色

## 职责

1. **功能测试** - 验证隧道功能正确性
2. **性能测试** - 验证延迟、吞吐量、并发
3. **稳定性测试** - 长时间运行、异常恢复
4. **兼容性测试** - 多协议、多平台

## 测试类型

### 1. 单元测试

```bash
# 运行所有测试
go test ./... -v

# 运行特定包测试
go test ./internal/stream/... -v

# 带覆盖率
go test ./... -cover -coverprofile=coverage.out

# 查看覆盖率报告
go tool cover -html=coverage.out
```

### 2. 端到端测试

使用 `start_test.sh` 启动完整测试环境:

```bash
./start_test.sh
```

测试流程:
1. 启动服务端
2. 启动目标端客户端
3. 启动源端客户端
4. 建立隧道
5. 验证数据传输

### 3. 协议测试

测试各协议的连接和数据传输:

```bash
# TCP 协议
./bin/client -s 127.0.0.1:8000 -p tcp -anonymous

# WebSocket 协议
./bin/client -s 127.0.0.1:8443 -p websocket -anonymous

# KCP 协议
./bin/client -s 127.0.0.1:8000 -p kcp -anonymous

# QUIC 协议
./bin/client -s 127.0.0.1:443 -p quic -anonymous
```

### 4. 性能测试

```bash
# 运行性能基准测试
go test -bench=. -benchmem ./internal/stream/...

# 输出示例:
# BenchmarkCompression-8    10000    120000 ns/op    4096 B/op    2 allocs/op
# BenchmarkEncryption-8     50000     30000 ns/op    1024 B/op    1 allocs/op
```

## 测试用例

### 隧道建立测试

```markdown
## TC-001: TCP 隧道建立

**前置条件**:
- 服务端运行在 127.0.0.1:8000
- 目标服务运行在 localhost:3306

**测试步骤**:
1. 目标端客户端连接服务器
2. 生成连接码: `generate-code` → TCP → localhost:3306
3. 源端客户端使用连接码: `use-code <code>`
4. 指定本地监听端口: 127.0.0.1:13306

**预期结果**:
- 隧道建立成功
- 可通过 127.0.0.1:13306 访问目标服务

**验证命令**:
mysql -h 127.0.0.1 -P 13306 -u root -p

**状态**: ✅ 通过 / ❌ 失败
```

### 断线重连测试

```markdown
## TC-002: 客户端断线重连

**前置条件**:
- 已建立的隧道连接

**测试步骤**:
1. 记录当前隧道状态
2. 断开客户端网络 (禁用网卡/拔网线)
3. 等待 30 秒
4. 恢复网络连接
5. 观察客户端行为

**预期结果**:
- 客户端检测到断开
- 自动尝试重连
- 重连成功后恢复隧道

**状态**: ✅ 通过 / ❌ 失败
```

### 并发连接测试

```markdown
## TC-003: 高并发连接

**前置条件**:
- 服务端已启动
- 测试客户端就绪

**测试步骤**:
1. 并发建立 1000 个隧道连接
2. 每个隧道发送 100 个请求
3. 统计成功率和延迟

**预期结果**:
- 连接成功率 > 99%
- 平均延迟 < 50ms
- 无内存泄漏

**验证脚本**:
go test -bench=BenchmarkConcurrentConnections -benchtime=60s

**状态**: ✅ 通过 / ❌ 失败
```

### 压缩加密测试

```markdown
## TC-004: 流处理验证

**测试内容**:
1. 压缩功能
   - 验证 Gzip Level 1-9
   - 验证压缩率
2. 加密功能
   - 验证 AES-256-GCM
   - 验证数据完整性
3. 组合功能
   - 压缩 + 加密同时启用
   - 验证数据正确性

**验证命令**:
go test ./internal/stream/compression/... -v
go test ./internal/stream/encryption/... -v

**预期结果**:
- 所有测试通过
- 数据一致性验证通过

**状态**: ✅ 通过 / ❌ 失败
```

## 性能基准

| 指标 | 目标 | 阈值 | 说明 |
|------|------|------|------|
| 单连接延迟 | < 5ms | < 10ms | 本地回环测试 |
| 吞吐量 | > 500Mbps | > 200Mbps | 大文件传输 |
| 并发连接 | 10K+ | 5K+ | 稳定持续 |
| 内存/连接 | < 100KB | < 200KB | 无泄漏 |
| 重连时间 | < 3s | < 10s | 网络恢复后 |

## 测试报告模板

```markdown
# 测试报告

**版本**: v1.1.11
**测试日期**: 2025-01-28
**测试环境**: macOS 14.0 / Go 1.24

## 测试概要

| 类型 | 用例数 | 通过 | 失败 | 跳过 |
|------|--------|------|------|------|
| 单元测试 | 150 | 148 | 2 | 0 |
| 集成测试 | 30 | 30 | 0 | 0 |
| 性能测试 | 10 | 9 | 1 | 0 |

## 测试结果: ✅ 通过 / ❌ 失败

## 详细结果

### 单元测试

$ go test ./... -v
...
PASS
ok  tunnox-core/internal/stream  0.523s

### 失败用例

**1. TestQuicAdapter_Reconnect**
- 错误: context deadline exceeded
- 原因: QUIC 握手超时
- 建议: 增加测试超时时间

### 性能测试

| 测试项 | 结果 | 目标 | 状态 |
|--------|------|------|------|
| 连接建立延迟 | 2.3ms | < 5ms | ✅ |
| 数据传输吞吐 | 650Mbps | > 500Mbps | ✅ |
| 内存占用 | 85KB/conn | < 100KB | ✅ |

## 覆盖率

| 包 | 覆盖率 |
|----|----|
| internal/stream | 82% |
| internal/protocol | 75% |
| internal/client | 68% |
| internal/command | 71% |

## 结论

测试基本通过，有 2 个单元测试和 1 个性能测试失败，
需要开发修复后重新测试。
```

## 测试环境

### 本地测试

```bash
# 1. 编译
go build -o bin/server ./cmd/server
go build -o bin/client ./cmd/client

# 2. 启动服务端
./bin/server

# 3. 启动客户端
./bin/client -s 127.0.0.1:8000 -p tcp -anonymous
```

### Docker 测试

```bash
# 构建镜像
docker build -t tunnox-server .
docker build -t tunnox-client -f Dockerfile.client .

# 启动服务端
docker run -d -p 8000:8000 -p 8443:8443 tunnox-server

# 启动客户端
docker run -d -e SERVER_ADDRESS=host.docker.internal:8000 tunnox-client
```

## 与其他角色的交互

```
QA ◀──测试请求── PM
QA ──测试报告──▶ PM
QA ──Bug 报告──▶ Dev
QA ──性能数据──▶ Architect
```
