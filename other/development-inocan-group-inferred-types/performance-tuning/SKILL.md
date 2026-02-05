---
name: performance-tuning
description: 性能调优技能。分析和优化隧道系统的延迟、吞吐量、并发能力。关键词：性能、优化、延迟、吞吐量、并发、内存。
allowed-tools: Read, Grep, Glob, Bash, Edit
---

# 性能调优技能

## 性能指标

### 核心指标

| 指标 | 目标 | 优秀 | 可接受 | 需优化 |
|------|------|------|--------|--------|
| 单连接延迟 | < 5ms | < 3ms | < 10ms | > 10ms |
| 吞吐量 | > 500Mbps | > 800Mbps | > 200Mbps | < 200Mbps |
| 并发连接 | 10K+ | 50K+ | 5K+ | < 5K |
| 内存/连接 | < 100KB | < 50KB | < 200KB | > 200KB |
| CPU (空闲) | < 5% | < 2% | < 10% | > 10% |
| 重连时间 | < 3s | < 1s | < 10s | > 10s |

### 测量命令

```bash
# 延迟测试
time curl http://localhost:8080/api/health

# 吞吐量测试
iperf3 -c localhost -p 8000 -t 30

# 并发测试
go test -bench=BenchmarkConcurrent -benchtime=60s

# 内存分析
go tool pprof http://localhost:6060/debug/pprof/heap

# CPU 分析
go tool pprof http://localhost:6060/debug/pprof/profile?seconds=30
```

## 优化策略

### 1. 内存优化

#### 缓冲区复用

```go
// 问题: 频繁分配缓冲区
func handleData(data []byte) {
    buf := make([]byte, 64*1024)  // 每次分配
    // ...
}

// 优化: 使用 sync.Pool
var bufPool = sync.Pool{
    New: func() interface{} {
        return make([]byte, 64*1024)
    },
}

func handleData(data []byte) {
    buf := bufPool.Get().([]byte)
    defer bufPool.Put(buf)
    // ...
}
```

#### 对象复用

```go
// 问题: 频繁创建 Packet 对象
func processPacket() *Packet {
    return &Packet{
        Header: make([]byte, 16),
        Data:   make([]byte, 1024),
    }
}

// 优化: 对象池
var packetPool = sync.Pool{
    New: func() interface{} {
        return &Packet{
            Header: make([]byte, 16),
            Data:   make([]byte, 0, 4096),
        }
    },
}

func getPacket() *Packet {
    p := packetPool.Get().(*Packet)
    p.Header = p.Header[:16]
    p.Data = p.Data[:0]
    return p
}

func putPacket(p *Packet) {
    packetPool.Put(p)
}
```

### 2. CPU 优化

#### 减少锁竞争

```go
// 问题: 全局锁
type Manager struct {
    mu      sync.Mutex
    clients map[string]*Client
}

func (m *Manager) Get(id string) *Client {
    m.mu.Lock()
    defer m.mu.Unlock()
    return m.clients[id]
}

// 优化: 分片锁
type Manager struct {
    shards [256]shard
}

type shard struct {
    mu      sync.RWMutex
    clients map[string]*Client
}

func (m *Manager) Get(id string) *Client {
    s := &m.shards[hash(id)%256]
    s.mu.RLock()
    defer s.mu.RUnlock()
    return s.clients[id]
}
```

#### 避免不必要的拷贝

```go
// 问题: 多次拷贝
func process(data []byte) []byte {
    temp := make([]byte, len(data))
    copy(temp, data)
    // 处理 temp
    return temp
}

// 优化: 原地处理或零拷贝
func process(data []byte) []byte {
    // 直接处理 data
    return data
}
```

### 3. I/O 优化

#### 批量写入

```go
// 问题: 逐个写入
for _, msg := range messages {
    conn.Write(msg)
}

// 优化: 批量写入
var buf bytes.Buffer
for _, msg := range messages {
    buf.Write(msg)
}
conn.Write(buf.Bytes())
```

#### 使用 io.Copy

```go
// 问题: 手动拷贝
buf := make([]byte, 32*1024)
for {
    n, err := src.Read(buf)
    if err != nil {
        break
    }
    dst.Write(buf[:n])
}

// 优化: 使用 io.Copy (可能使用 sendfile)
io.Copy(dst, src)

// 更优: 使用 io.CopyBuffer 复用缓冲区
buf := make([]byte, 32*1024)
io.CopyBuffer(dst, src, buf)
```

### 4. 并发优化

#### Goroutine 池

```go
// 问题: 无限制创建 goroutine
for conn := range connections {
    go handleConn(conn)
}

// 优化: 使用工作池
type WorkerPool struct {
    workers int
    tasks   chan func()
}

func (p *WorkerPool) Start() {
    for i := 0; i < p.workers; i++ {
        go func() {
            for task := range p.tasks {
                task()
            }
        }()
    }
}

func (p *WorkerPool) Submit(task func()) {
    p.tasks <- task
}
```

#### 无锁队列

```go
// 高并发场景使用无锁队列
type LockFreeQueue struct {
    head unsafe.Pointer
    tail unsafe.Pointer
}
```

### 5. 网络优化

#### TCP 参数调优

```go
// 优化 TCP 参数
conn.(*net.TCPConn).SetNoDelay(true)      // 禁用 Nagle
conn.(*net.TCPConn).SetKeepAlive(true)    // 启用 KeepAlive
conn.(*net.TCPConn).SetKeepAlivePeriod(30 * time.Second)

// 调整缓冲区
conn.(*net.TCPConn).SetReadBuffer(256 * 1024)
conn.(*net.TCPConn).SetWriteBuffer(256 * 1024)
```

#### 连接复用

```go
// HTTP 连接复用
transport := &http.Transport{
    MaxIdleConns:        100,
    MaxIdleConnsPerHost: 10,
    IdleConnTimeout:     90 * time.Second,
}
```

## 性能分析工具

### pprof 集成

```go
import _ "net/http/pprof"

func main() {
    go func() {
        http.ListenAndServe(":6060", nil)
    }()
    // ...
}
```

### 分析命令

```bash
# CPU 分析
go tool pprof http://localhost:6060/debug/pprof/profile?seconds=30

# 内存分析
go tool pprof http://localhost:6060/debug/pprof/heap

# goroutine 分析
go tool pprof http://localhost:6060/debug/pprof/goroutine

# 阻塞分析
go tool pprof http://localhost:6060/debug/pprof/block

# 互斥锁分析
go tool pprof http://localhost:6060/debug/pprof/mutex

# 生成火焰图
go tool pprof -http=:8080 profile.pb.gz
```

### 基准测试

```go
func BenchmarkForward(b *testing.B) {
    // 设置
    src := bytes.NewReader(data)
    dst := &bytes.Buffer{}

    b.ResetTimer()
    for i := 0; i < b.N; i++ {
        src.Reset(data)
        dst.Reset()
        io.Copy(dst, src)
    }
}

func BenchmarkConcurrentConnections(b *testing.B) {
    b.RunParallel(func(pb *testing.PB) {
        for pb.Next() {
            conn := dial()
            conn.Close()
        }
    })
}
```

## 优化检查清单

```markdown
## 性能优化检查

### 内存
- [ ] 缓冲区使用 sync.Pool
- [ ] 大对象使用对象池
- [ ] 避免不必要的字符串转换
- [ ] slice 预分配容量

### CPU
- [ ] 热点函数优化
- [ ] 减少锁竞争
- [ ] 避免不必要的拷贝
- [ ] 使用原子操作替代锁

### I/O
- [ ] 使用 io.Copy
- [ ] 批量读写
- [ ] 异步 I/O
- [ ] 缓冲区大小合适

### 并发
- [ ] goroutine 数量可控
- [ ] 使用工作池
- [ ] 减少 channel 竞争
- [ ] 避免 goroutine 泄漏

### 网络
- [ ] TCP 参数调优
- [ ] 连接复用
- [ ] 合适的超时设置
- [ ] 启用 KeepAlive
```

## 优化报告模板

```markdown
## 性能优化报告

**优化目标**: 降低延迟 / 提升吞吐量 / 减少内存

### 优化前

| 指标 | 数值 |
|------|------|
| 延迟 | 15ms |
| 吞吐量 | 300Mbps |
| 内存/连接 | 150KB |

### 优化措施

1. **措施1**: 使用 sync.Pool 复用缓冲区
   - 文件: internal/stream/processor.go
   - 影响: 减少 GC 压力

2. **措施2**: 调整 TCP 缓冲区大小
   - 文件: internal/protocol/adapter/tcp_adapter.go
   - 影响: 提升吞吐量

### 优化后

| 指标 | 数值 | 提升 |
|------|------|------|
| 延迟 | 8ms | 47% |
| 吞吐量 | 650Mbps | 117% |
| 内存/连接 | 85KB | 43% |

### 基准测试对比

```
Before:
BenchmarkForward-8    10000    150000 ns/op    8192 B/op    4 allocs/op

After:
BenchmarkForward-8    20000     75000 ns/op    1024 B/op    1 allocs/op
```
```
