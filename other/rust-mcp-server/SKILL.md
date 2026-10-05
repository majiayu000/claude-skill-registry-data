---
name: rust-mcp-server
description: 用 Rust 写 MCP server（rmcp crate）并暴露 CLI/工具为 MCP tools。
category: mcp
tags: [mcp, rust, rmcp, stdio, ai-agent, protocol]
---

# Rust MCP Server（rmcp 3.x）

用 `rmcp` crate 把现有 Rust 工具/CLI 暴露为 MCP tools，让协议系 agent 能调用。MCP 是 CLI 的薄适配层——core 只暴露 CLI/函数，server 只做包装。

## 何时使用

- 已有 Rust 后端/CLI，想让 Claude Desktop、Cursor、Codex 等 agent 能调用
- 用户说"做 MCP server"、"让 AI agent 能调用我们的工具"
- 已有 Python MCP server（见 mcp-python-patterns），需要 Rust 侧对应物

## Cargo.toml 依赖

```toml
[dependencies]
rmcp = { version = "3.1", features = ["server", "transport-io", "macros"] }
schemars = { version = "1.0", features = ["derive"] }   # ← 必须 1.0，见坑表
tokio = { version = "1", features = ["macros", "rt-multi-thread"] }
serde = { version = "1", features = ["derive"] }
serde_json = "1"
anyhow = "1"
```

features 名：`server` + `transport-io`（stdio）。**没有** `server-stdio` feature（不存在，写了会 resolve 冲突）。查真实 feature 列表：`crates.io/api/v1/crates/rmcp/<version>` 的 JSON。

## 最小 server（宏模式）

```rust
use rmcp::{
    ServerHandler, ServiceExt,
    handler::server::{router::tool::ToolRouter, wrapper::Parameters},
    tool, tool_handler, tool_router,
};
use rmcp::schemars::JsonSchema;
use serde::{Deserialize, Serialize};

#[derive(Debug, Clone)]
pub struct MyServer { tool_router: ToolRouter<Self> }

impl MyServer {
    pub fn new() -> Self { Self { tool_router: Self::tool_router() } }
}

#[tool_handler(router = self.tool_router)]
impl ServerHandler for MyServer {}

#[derive(Serialize, Deserialize, JsonSchema)]
struct ListParam { #[serde(default)] category: Option<String> }

#[tool_router(router = tool_router)]
impl MyServer {
    /// 工具描述（agent 看到的就是这个）。
    #[tool(name = "list_items", description = "List items. Returns JSON array.")]
    pub async fn list_items(&self, p: Parameters<ListParam>) -> String {
        // 返回 String（JSON 文本），MCP 会包成 text content
        serde_json::to_string(&vec![1, 2, 3]).unwrap()
    }
}

#[tokio::main]
async fn main() -> anyhow::Result<()> {
    let running = MyServer::new().serve(rmcp::transport::io::stdio()).await?;
    running.waiting().await?;   // ← 必须！否则进程 init 后立即退出
    Ok(())
}
```

## 验证（python 裸客户端，不用 MCP SDK）

```python
import subprocess, json, select
p = subprocess.Popen(['./target/debug/my-mcp'], stdin=subprocess.PIPE,
                     stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, bufsize=1)
def send(o): p.stdin.write(json.dumps(o) + '\n'); p.stdin.flush()
def recv(t=3):
    r,_,_ = select.select([p.stdout], [], [], t)
    return p.stdout.readline().strip() if r else None
send({"jsonrpc":"2.0","id":1,"method":"initialize","params":{"protocolVersion":"2024-11-05","capabilities":{},"clientInfo":{"name":"t","version":"1"}}})
print("init:", recv())
send({"jsonrpc":"2.0","method":"notifications/initialized"})
send({"jsonrpc":"2.0","id":2,"method":"tools/list"})
print("tools:", recv(5))
```

stdio 传输是 **JSON-Lines**（每行一个 JSON + `\n`），不是 Content-Length 帧。

## 详细坑位

见 `references/rmcp-3.1-pitfalls.md`。高频要点：

1. **schemars 版本必须和 rmcp 匹配**：rmcp 3.1 依赖 schemars **1.0**。用 0.8 derive 的 `JsonSchema` 和 rmcp 的 `Parameters<T>` 类型不兼容 → `trait bound unsatisfied`。要么 `rmcp::schemars::JsonSchema`（derive 宏要独立 schemars 开 derive feature），要么独立 schemars 1.0 + derive。
2. **`RunningService::waiting().await` 必须调用**：`serve()` 返回后 main 一结束 `RunningService` 被 drop → 连接关闭 → 进程退出。症状：init 响应正常，但 tools/list 时 BrokenPipe。这是本会话最隐蔽的坑。
3. **没有 `#[tool(aggr)]` 属性**：参数就是 `Parameters<T>` 类型，直接作为 fn 参数，不要加任何 attribute。
4. **写工具（提权/确认）也走同一 server**：把写操作委托给共享 launcher（helper 弹窗），AI 无法绕过确认——MCP tool 只是调用入口，硬确认在运行时。

## 参考文件

- `references/rmcp-3.1-pitfalls.md` — rmcp 3.1 完整坑位（版本、宏、stdio、进程生命周期）
