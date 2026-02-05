---
name: protocol-design
description: 协议设计技能。设计和实现新的传输协议适配器，遵循统一的 ProtocolAdapter 接口。关键词：协议、适配器、TCP、UDP、WebSocket、QUIC、KCP。
allowed-tools: Read, Write, Edit, Grep, Glob, Bash
---

# 协议设计技能

## 目标

设计和实现符合 Tunnox 架构的传输协议适配器。

## 协议适配器接口

```go
// internal/protocol/adapter/adapter.go
type ProtocolAdapter interface {
    // 启动监听
    Start(ctx context.Context) error

    // 停止监听
    Stop() error

    // 接受连接 (服务端)
    Accept() (Connection, error)

    // 建立连接 (客户端)
    Dial(ctx context.Context, addr string) (Connection, error)

    // 获取监听地址
    Addr() net.Addr

    // 获取协议类型
    Protocol() string
}

// 连接抽象
type Connection interface {
    Read(b []byte) (n int, err error)
    Write(b []byte) (n int, err error)
    Close() error
    LocalAddr() net.Addr
    RemoteAddr() net.Addr
    SetDeadline(t time.Time) error
    SetReadDeadline(t time.Time) error
    SetWriteDeadline(t time.Time) error
}
```

## 实现模板

### 1. 适配器结构

```go
// internal/protocol/adapter/xxx_adapter.go
package adapter

import (
    "context"
    "tunnox-core/internal/core/dispose"
    coreerrors "tunnox-core/internal/core/errors"
)

type XXXAdapter struct {
    *dispose.ServiceBase
    config   XXXConfig
    listener XXXListener  // 具体协议的监听器
}

type XXXConfig struct {
    Address    string
    // 协议特定配置
}

func NewXXXAdapter(parentCtx context.Context, config XXXConfig) *XXXAdapter {
    a := &XXXAdapter{
        ServiceBase: dispose.NewService("XXXAdapter", parentCtx),
        config:      config,
    }
    return a
}
```

### 2. 启动和停止

```go
func (a *XXXAdapter) Start(ctx context.Context) error {
    // 1. 创建监听器
    listener, err := xxx.Listen(a.config.Address)
    if err != nil {
        return coreerrors.Wrap(err, coreerrors.ErrorTypeNetwork, "xxx listen failed")
    }
    a.listener = listener

    // 2. 启动接受循环 (如果需要)
    go a.acceptLoop()

    return nil
}

func (a *XXXAdapter) Stop() error {
    // 1. 关闭监听器
    if a.listener != nil {
        return a.listener.Close()
    }
    return nil
}

func (a *XXXAdapter) acceptLoop() {
    for {
        select {
        case <-a.Ctx().Done():
            return
        default:
        }

        conn, err := a.listener.Accept()
        if err != nil {
            if a.IsClosed() {
                return
            }
            continue
        }

        // 处理连接
        a.handleConnection(conn)
    }
}
```

### 3. 连接管理

```go
func (a *XXXAdapter) Accept() (Connection, error) {
    if a.IsClosed() {
        return nil, coreerrors.New(coreerrors.ErrorTypeNetwork, "adapter closed")
    }

    conn, err := a.listener.Accept()
    if err != nil {
        return nil, coreerrors.Wrap(err, coreerrors.ErrorTypeNetwork, "accept failed")
    }

    return &xxxConnection{conn: conn}, nil
}

func (a *XXXAdapter) Dial(ctx context.Context, addr string) (Connection, error) {
    conn, err := xxx.DialContext(ctx, addr)
    if err != nil {
        return nil, coreerrors.Wrap(err, coreerrors.ErrorTypeNetwork, "dial failed")
    }

    return &xxxConnection{conn: conn}, nil
}
```

### 4. 连接包装

```go
// 包装底层连接，实现 Connection 接口
type xxxConnection struct {
    conn xxx.Conn
}

func (c *xxxConnection) Read(b []byte) (int, error) {
    return c.conn.Read(b)
}

func (c *xxxConnection) Write(b []byte) (int, error) {
    return c.conn.Write(b)
}

func (c *xxxConnection) Close() error {
    return c.conn.Close()
}

func (c *xxxConnection) LocalAddr() net.Addr {
    return c.conn.LocalAddr()
}

func (c *xxxConnection) RemoteAddr() net.Addr {
    return c.conn.RemoteAddr()
}

// ... 其他方法
```

## 已实现协议参考

### TCP 适配器

```
文件: internal/protocol/adapter/tcp_adapter.go
特点:
- 最基础的实现
- 标准 net.Listener
- 无额外依赖
```

### WebSocket 适配器

```
文件: internal/protocol/adapter/websocket_adapter.go
特点:
- HTTP 升级握手
- 帧协议封装
- 支持 TLS
依赖: gorilla/websocket
```

### KCP 适配器

```
文件: internal/protocol/adapter/kcp_adapter.go
特点:
- 基于 UDP
- ARQ 重传机制
- 低延迟优化
依赖: xtaci/kcp-go
```

### QUIC 适配器

```
文件: internal/protocol/adapter/quic_adapter.go
特点:
- 多路复用
- 0-RTT 连接
- 内置加密
依赖: quic-go/quic-go
```

## 新协议检查清单

### 设计阶段

- [ ] 确定协议库选择
- [ ] 分析连接模型（单连接/多路复用）
- [ ] 确定配置参数
- [ ] 评估性能特性

### 实现阶段

- [ ] 嵌入 dispose.ServiceBase
- [ ] 实现 ProtocolAdapter 接口
- [ ] 实现 Connection 包装
- [ ] 添加错误处理
- [ ] 添加日志记录

### 测试阶段

- [ ] 单元测试
- [ ] 连接建立测试
- [ ] 数据传输测试
- [ ] 并发测试
- [ ] 性能基准测试

### 集成阶段

- [ ] 更新 adapter factory
- [ ] 更新配置解析
- [ ] 更新文档
- [ ] 更新 CLI 选项

## 性能考量

### 缓冲区管理

```go
// 使用 sync.Pool 复用缓冲区
var bufPool = sync.Pool{
    New: func() interface{} {
        return make([]byte, 64*1024)
    },
}
```

### 连接复用

```go
// 对于多路复用协议 (如 QUIC)
type MultiplexAdapter struct {
    session QuicSession  // 单个会话
    streams sync.Map     // 多个流
}
```

### 超时控制

```go
// 合理的超时设置
const (
    DialTimeout      = 10 * time.Second
    ReadTimeout      = 30 * time.Second
    WriteTimeout     = 30 * time.Second
    KeepAliveTimeout = 60 * time.Second
)
```

## 输出

完成新协议实现后，输出:

```markdown
## 协议实现报告

**协议名称**: XXX
**库依赖**: github.com/xxx/xxx

### 文件变更

| 文件 | 操作 | 说明 |
|------|------|------|
| adapter/xxx_adapter.go | 新建 | 适配器实现 |
| adapter/xxx_adapter_test.go | 新建 | 单元测试 |
| adapter/factory.go | 修改 | 添加工厂方法 |

### 配置示例

```yaml
server:
  protocols:
    xxx:
      enabled: true
      port: 8000
      # 协议特定配置
```

### 使用示例

```bash
./bin/client -s 127.0.0.1:8000 -p xxx -anonymous
```

### 性能数据

| 指标 | 结果 |
|------|------|
| 连接延迟 | X ms |
| 吞吐量 | X Mbps |
| 并发连接 | X |
```
