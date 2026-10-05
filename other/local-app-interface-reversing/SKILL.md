---
name: local-app-interface-reversing
description: 本地应用接口挖掘，发现开放但未配置的端口/WebSocket API，jar 常量池提取方法名。
---

# Local App Interface Reversing（本地应用接口挖掘）

## 触发信号
- 用户问"应用有没有开放但没配置的接口"、"能不能绕过 GUI 直接调 API"
- 桌面应用自带本地服务（预览端口、外部集成端口）需要自动化控制
- Java/Kotlin 桌面应用（jpackage 打包）的隐藏协议需要逆向
- MCP 桥接层（uvx 安装）源码定位与协议还原

## 工作流

### 1. 端口发现（先找监听面）
```bash
lsof -nP -iTCP -sTCP:LISTEN | grep -iE '<app名>'
lsof -nP -iTCP:<端口>          # 确认端口归属
ps -p <pid> -o command         # 确认进程
```
注意区分：应用自带的端口 vs 周边 Python http.server（预览页）——先确认归属再动手。

### 2. 协议识别（HTTP? WebSocket? 裸 TCP?）
```bash
nc -z -v 127.0.0.1 <port>      # 连通性
curl -s -m 3 -i http://127.0.0.1:<port>/   # 纯 HTTP 探测
curl -s -m 3 -i -H "Connection: Upgrade" -H "Upgrade: websocket" \
  -H "Sec-WebSocket-Version: 13" -H "Sec-WebSocket-Key: dGhlIHNhbXBsZSBub25jZQ==" \
  http://127.0.0.1:<port>/                  # WebSocket 握手探测
```
判定：`101 Web Socket Protocol Handshake` = WebSocket；`Server: TooTallNate Java-WebSocket` 等头部暴露库版本。

### 3. 找桥接层源码（MCP / 集成配置）
很多应用通过 MCP server 暴露 API，MCP 源码就是协议文档：
```bash
grep -riE '<app>' ~/.codex/config.toml ~/.hermes/config.yaml  # 找 mcp_servers 条目
find ~/.cache/uv -iname "*<app>*" -maxdepth 4                 # uvx 安装的 MCP 源码
find ~ -maxdepth 4 -name "*.mcp.json" -not -path "*/node_modules/*"
cat ~/.<app>-mcp/token.txt 2>/dev/null                        # 应用可能持久化 token
```
读 MCP 源码（cubism_mcp.py 之类）能拿到：消息格式、方法名全集、认证流程、token 持久化位置。

### 4. 原生协议探测（写 Python 裸 WebSocket 客户端）
消息格式通常带版本 + 请求 ID + 类型：
```json
{"Version":"1.1.0","RequestId":"<uuid4 hex>","Type":"Request","Method":"<方法名>","Data":{...}}
```
- 注册：`RegisterPlugin`（带 Token + Name），响应会回显/刷新 Token
- 探测方法存在性：`ErrorType: MethodNotFound` = 方法不存在；`InvalidData/InvalidEditOperation/InvalidModel` = 方法存在但参数/上下文不对
- **事务方法要配对**：`EditBegin`/`EditEnd` 必须成对，未配对的编辑事务可能让应用进程退出

### 5. jar 反编译 + 方法名提取（Java/Kotlin 应用）
jpackage 打包的应用主二进制往往只有几百 KB（JVM 启动器），真正逻辑在 jar 里：
```bash
cat <App>.app/Contents/app/<App>.cfg   # app.classpath 列出核心 jar
unzip -o -q <App>_Cubism.jar -d /tmp/x
find /tmp/x -name "*.class" | grep -iE 'webSocket|api|external'   # 定位 API 包
```
**方法名提取（不依赖 JVM）**：class 文件常量池是标准二进制格式，用 Python 解析 UTF8 条目即可拿到方法名字符串。混淆类（a.class, b.class...）常量池里仍保留 dispatch 方法名（GetObject、EditBegin 等）。见 `scripts/parse_class_cp.py`。

### 6. 验证清单
- 每个新发现的方法用真实参数实测（返回 OK / 有意义的 Data 才算数）
- 对比 MCP 已暴露的工具集，列出"协议支持但桥接层未暴露"的接口
- 关键业务问题（如"API 能不能写 X"）用 Get* 先读、Edit* 后写、实测结果说话

## 陷阱
- **macOS `strings` 对 .class 文件报错**（"fat file: truncated or malformed"）——必须用 Python 常量池解析，见 scripts/parse_class_cp.py
- jlinked 运行时（Contents/runtime 或外置 jre）通常只有 lib/ 没有 javap/bin，系统可能无独立 Java——常量池解析是零依赖方案
- **应用重启会重置集成开关**：外部集成/端口开关重启后默认关闭，需 GUI 重新启用（端口消失先查这个，别怀疑协议）
- Token 通常持久化在 ~/.<app>-mcp/token.txt，复用可跳过授权弹窗；但应用重启后授权状态也可能重置
- 枚举方法时用 `{"Version":"1.1.0"}` 固定版本；部分方法要求特定版本前缀（v000900/v000901...），报版本错时试 SetGlobalVersion
- 大量探测请求可能让应用退出（编辑事务未配对 / 连接风暴）——探测完检查进程是否还活着

## 支持文件
- `references/cubism-editor.md` — Cubism Editor 5.4 alpha 外部 API 完整逆向记录：22033 端口、协议格式、完整方法清单（含 MCP 未暴露的 GetAPIVersion/GetCurrentDocumentUID/SetGlobalVersion/SendCubismLog/GetPhysicsInfo/SetPhysicsInfo/6 个 Notify* 事件）、关键帧写入根因结论
- `scripts/parse_class_cp.py` — class 文件常量池解析器，提取混淆类中的方法名字符串
- `scripts/ws_client.py` — 裸 WebSocket 客户端模板（握手 + 掩码帧 + 请求/响应），改 host/port/token 即可用
