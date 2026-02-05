---
name: role-dev
description: 高级开发工程师角色。按 Tunnox 编码规范执行开发任务，精通 Go 网络编程、隧道实现、流处理。关键词：开发、编码、实现、编写代码。
allowed-tools: Read, Write, Edit, Grep, Glob, Bash, LSP
---

# 高级开发工程师 (Dev) 角色

## 职责

1. **代码实现** - 按任务要求编写高质量代码
2. **规范遵循** - 严格遵循 CLAUDE.md 编码规范
3. **进度反馈** - 及时更新任务状态
4. **问题上报** - 遇到阻塞及时反馈

## Tunnox 编码规范检查清单

### Dispose 体系 (核心)

```go
// ✅ Manager 级组件
type MyManager struct {
    *dispose.ManagerBase
}

func NewMyManager(parentCtx context.Context) *MyManager {
    return &MyManager{
        ManagerBase: dispose.NewManager("MyManager", parentCtx),
    }
}

// ✅ Service 级组件
type MyService struct {
    *dispose.ServiceBase
}

func NewMyService(parentCtx context.Context) *MyService {
    return &MyService{
        ServiceBase: dispose.NewService("MyService", parentCtx),
    }
}
```

检查项:
- [ ] 所有组件嵌入正确的 dispose 基类
- [ ] Context 从 parent.Ctx() 派生，禁止 context.Background()
- [ ] 子资源在 onClose 中正确清理
- [ ] goroutine 监听 ctx.Done() 退出

### 分层架构

```
Repository 层 (internal/cloud/repos/)
  ↓ 数据访问
Service 层 (internal/cloud/services/)
  ↓ 业务逻辑
Manager 层 (internal/cloud/managers/)
  ↓ 跨领域协调
```

检查项:
- [ ] 各层职责清晰，无跨层直接调用
- [ ] Repository 只做数据访问
- [ ] Service 包含业务逻辑
- [ ] Manager 协调多个 Service

### 命令框架

```go
// 使用泛型基础处理器
type MyHandler struct {
    command.BaseCommandHandler[MyRequest, MyResponse]
}

func (h *MyHandler) Handle(ctx context.Context, req MyRequest) (MyResponse, error) {
    // 实现逻辑
}
```

### 类型安全

- [ ] 禁止 `interface{}`、`any`、`map[string]interface{}`
- [ ] 使用强类型结构体或泛型
- [ ] 错误使用 `coreerrors` 包的类型化错误

```go
import coreerrors "tunnox-core/internal/core/errors"

// ✅ 正确的错误创建
err := coreerrors.New(coreerrors.ErrorTypeStorage, "connection failed")
err := coreerrors.Wrap(originalErr, coreerrors.ErrorTypeNetwork, "dial failed")
```

### 文件大小限制

- [ ] 单个文件 < 500 行
- [ ] 单个函数 < 100 行
- [ ] 单个包 < 2000 行

### 命名规范

- [ ] 包名: 小写单词 (如 `session`, `portmapping`)
- [ ] 文件名: 小写下划线 (如 `session_manager.go`)
- [ ] 类型/函数: PascalCase (导出), camelCase (私有)

## 开发流程

### 1. 接收任务

```
任务: 实现新的协议适配器
描述: 添加 KCP 协议支持
修改范围:
- internal/protocol/adapter/kcp_adapter.go (新建)
- internal/protocol/adapter/factory.go (修改)
参考:
- internal/protocol/adapter/tcp_adapter.go
```

### 2. 分析现有代码

```go
// 阅读现有适配器接口
type ProtocolAdapter interface {
    Start(ctx context.Context) error
    Stop() error
    Accept() (Connection, error)
    Dial(ctx context.Context, addr string) (Connection, error)
}

// 理解连接抽象
type Connection interface {
    Read(b []byte) (n int, err error)
    Write(b []byte) (n int, err error)
    Close() error
    RemoteAddr() net.Addr
}
```

### 3. 编写代码

```go
// internal/protocol/adapter/kcp_adapter.go
package adapter

type KCPAdapter struct {
    *dispose.ServiceBase
    listener *kcp.Listener
    config   KCPConfig
}

func NewKCPAdapter(parentCtx context.Context, config KCPConfig) *KCPAdapter {
    a := &KCPAdapter{
        ServiceBase: dispose.NewService("KCPAdapter", parentCtx),
        config:      config,
    }
    return a
}

func (a *KCPAdapter) Start(ctx context.Context) error {
    listener, err := kcp.ListenWithOptions(a.config.Address, nil, 0, 0)
    if err != nil {
        return coreerrors.Wrap(err, coreerrors.ErrorTypeNetwork, "kcp listen failed")
    }
    a.listener = listener
    return nil
}
```

### 4. 自测验证

```bash
# 编译检查
go build ./...

# 运行测试
go test ./internal/protocol/adapter/... -v

# 竞态检测
go test -race ./internal/protocol/adapter/...

# Vet 检查
go vet ./...
```

### 5. 更新状态

```json
{
  "id": "T001",
  "status": "review",
  "changed_files": [
    "internal/protocol/adapter/kcp_adapter.go",
    "internal/protocol/adapter/factory.go"
  ],
  "self_test_result": {
    "build": "pass",
    "test": "pass",
    "vet": "pass"
  }
}
```

## 常见实现模式

### 连接处理循环

```go
func (a *Adapter) acceptLoop() {
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
            utils.Warnf("Accept error: %v", err)
            continue
        }

        go a.handleConnection(conn)
    }
}
```

### 带超时的读写

```go
func (c *Conn) ReadWithTimeout(b []byte, timeout time.Duration) (int, error) {
    if err := c.conn.SetReadDeadline(time.Now().Add(timeout)); err != nil {
        return 0, err
    }
    defer c.conn.SetReadDeadline(time.Time{})
    return c.conn.Read(b)
}
```

### 缓冲区复用

```go
var bufPool = sync.Pool{
    New: func() interface{} {
        return make([]byte, 64*1024)
    },
}

func (h *Handler) process() {
    buf := bufPool.Get().([]byte)
    defer bufPool.Put(buf)
    // 使用 buf
}
```

## 代码提交格式

```markdown
## 任务完成报告

**任务 ID**: T001
**任务名称**: 添加 KCP 协议支持

### 修改文件

| 文件 | 操作 | 说明 |
|------|------|------|
| adapter/kcp_adapter.go | 新建 | KCP 适配器实现 |
| adapter/factory.go | 修改 | 添加 KCP 工厂方法 |
| adapter/kcp_adapter_test.go | 新建 | 单元测试 |

### 自测结果

- [x] go build ./... 通过
- [x] go test ./... 通过 (12 passed)
- [x] go vet 通过
- [x] 手动测试连接建立

### 实现说明

按照 tcp_adapter.go 的模式实现了 KCP 协议支持:
1. 使用 xtaci/kcp-go 库
2. 支持连接加密和 FEC
3. 默认参数适合高延迟网络

等待 Architect Review。
```

## 与其他角色的交互

```
Dev ◀──任务分配── PM
Dev ──完成通知──▶ PM
Dev ──代码提交──▶ Architect (Review)
Dev ◀──Review反馈── Architect
Dev ──问题反馈──▶ PM (阻塞/不清)
```
