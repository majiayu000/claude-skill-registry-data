---
name: suite-network
description: "能力组：网络协议 / API / 认证"
---

# 能力组：网络协议 / API / 认证

协议、API、身份认证、云服务和网络流量的建模、验证与防护。

## 合并后的执行要点

- 请求模型、状态机和字段来源
- OAuth、OIDC、JWT、GraphQL 与 WebSocket
- 抓包、复现、边界条件和修复建议

## 来源范围
共 10 个 Markdown 来源，去重后保留 10 份正文。脚本、JSON、测试夹具和其他资源仅在离线包中保留。

## 合并来源正文

### 来源：`sources/pro/custom-protocol-replay.md`
SHA-256：`1ec4dafb7d9dab3f1f64dfcd79e67aae8ee4fce9b595fffe70655ba3de715550`

# Custom Protocol Replay

## Scope

Use this module only for services and protocols owned by your organization. Focus on understanding message sequences and validating state handling.

## Workflow

1. Capture baseline protocol traffic from the owned service under normal operation.
2. Parse and document message sequence: handshake, authentication, data exchange, teardown.
3. Identify message fields: headers, lengths, sequence numbers, checksums, payloads.
4. Construct replay scripts that reproduce documented message sequences.
5. Test state validation by replaying messages out of order against owned test instance.
6. Document server responses to invalid state transitions.
7. Produce protocol state diagram and validation coverage report.

## Safety Rules

- Do not replay traffic against services you do not own or have authorization for.
- Do not use replay techniques to bypass authentication on production systems.
- Do not capture or replay traffic containing other users' credentials.
- Do not perform replay testing against shared or multi-tenant environments without isolation.

## Output

Return evidence table with columns: Message | Sequence | Fields | Replay Result | State Validation | Finding.

### 来源：`sources/pro/protocol-reverse.md`
SHA-256：`2a99021a6c4076f1fe279178bcb5b7ce1313da74a96a0e87955d06849f68221f`

# 协议逆向工程

## 适用场景

- HTTP/HTTPS API 逆向（抓包分析）
- WebSocket 实时通信协议
- Protobuf/gRPC 二进制协议
- TCP/UDP 自定义协议
- MQTT/CoAP 物联网协议
- 游戏协议（私有二进制格式）

## 标准协议逆向流程（5步法）

### Step 1: 流量捕获

#### mitmproxy（HTTP/HTTPS 推荐）
```bash
# 启动交互式代理
mitmproxy -p 8080

# 保存流量到文件
mitmdump -p 8080 -w capture.mitm

# 脚本模式（自动修改请求/响应）
mitmdump -s script.py
```

**mitmproxy 脚本示例**（自动解密/记录）
```python
# script.py
from mitmproxy import http

def request(flow: http.HTTPFlow) -> None:
    print(f"[→] {flow.request.method} {flow.request.url}")
    print(f"    Headers: {dict(flow.request.headers)}")
    if flow.request.content:
        print(f"    Body: {flow.request.content[:200]}")

def response(flow: http.HTTPFlow) -> None:
    print(f"[←] {flow.response.status_code}")
    print(f"    Body: {flow.response.content[:200]}")
    
    # 自动保存 JSON 响应
    if "application/json" in flow.response.headers.get("content-type", ""):
        with open(f"responses/{flow.request.path.replace('/', '_')}.json", "wb") as f:
            f.write(flow.response.content)
```

#### Wireshark（TCP/UDP/原始流量）
```bash
# 捕获特定端口
tshark -i eth0 -f "tcp port 8080" -w capture.pcap

# 实时查看 HTTP
tshark -i eth0 -Y "http" -T fields -e http.request.method -e http.request.uri

# 导出 HTTP 对象
tshark -r capture.pcap --export-objects http,output/

# 跟踪 TCP 流
tshark -r capture.pcap -z follow,tcp,ascii,0
```

**Wireshark 显示过滤器速查**
```
http                      # 所有 HTTP 流量
http.request              # HTTP 请求
http.response.code == 200 # 成功响应
tcp.port == 443           # 特定端口
ip.addr == 192.168.1.100  # 特定 IP
websocket                 # WebSocket 流量
protobuf                  # Protobuf（需插件）
```

#### Charles Proxy（移动端常用）
```
1. 设置手机代理到 Charles（192.168.x.x:8888）
2. 安装 Charles 证书（Settings → SSL Proxying）
3. Enable SSL Proxying（Proxy → SSL Proxying Settings）
4. 捕获流量（Sequence/Structure 视图）
5. 导出会话（File → Export Session → .chls）
```

#### Android 抓包（绕过证书校验）
```bash
# 方法1：安装系统证书（需 Root）
openssl x509 -inform PEM -subject_hash_old -in mitmproxy-ca-cert.cer | head -1
# 输出如 c8750f0d，重命名证书
mv mitmproxy-ca-cert.cer c8750f0d.0
adb push c8750f0d.0 /sdcard/
adb shell
su
mount -o rw,remount /system
cp /sdcard/c8750f0d.0 /system/etc/security/cacerts/
chmod 644 /system/etc/security/cacerts/c8750f0d.0
reboot

# 方法2：使用 VirtualXposed + JustTrustMe（免 Root）
# 方法3：Frida SSL Pinning bypass（见 echo quickref-frida）
```

### Step 2: 协议识别

#### 文本协议特征
- **HTTP**: `GET / HTTP/1.1\r\n`
- **JSON**: `{"key": "value"}`
- **XML**: `<?xml version="1.0"?>`
- **SMTP**: `HELO`, `MAIL FROM:`
- **FTP**: `USER`, `PASS`, `LIST`

#### 二进制协议特征
- **Protobuf**: 字段编号（varint）+ wire type + 值
- **MessagePack**: 0x80-0x8F（固定字典），0x90-0x9F（固定数组）
- **BSON**: 以 `\x00` 结尾的字符串
- **Thrift**: 类型标签 + 字段 ID + 数据
- **自定义**: 观察固定头部（魔术字节、长度字段）

#### 快速判断工具
```bash
# 查看原始字节（前 100 字节）
xxd -l 100 packet.bin

# 熵值分析（高熵 > 7.5 可能是加密或压缩）
ent packet.bin

# 字符串提取
strings packet.bin
```

### Step 3: 消息结构解析

#### 定长协议
```python
# 示例：每条消息固定 64 字节
import struct

with open("capture.bin", "rb") as f:
    while True:
        packet = f.read(64)
        if len(packet) < 64:
            break
        
        # 解析字段（小端序）
        msg_type, user_id, timestamp, data = struct.unpack("<I I Q 44s", packet)
        print(f"Type: {msg_type}, UserID: {user_id}, Time: {timestamp}")
        print(f"Data: {data.hex()}")
```

#### 长度字段协议
```python
# 示例：前4字节是长度（大端序），后面是数据
import struct

with open("capture.bin", "rb") as f:
    while True:
        length_bytes = f.read(4)
        if len(length_bytes) < 4:
            break
        
        length = struct.unpack(">I", length_bytes)[0]
        payload = f.read(length)
        print(f"Length: {length}, Payload: {payload[:50].hex()}...")
```

#### 分隔符协议
```python
# 示例：消息以 \r\n 分隔
with open("capture.txt", "r") as f:
    for line in f:
        line = line.strip()
        if not line:
            continue
        
        parts = line.split(" ")
        print(f"Command: {parts[0]}, Args: {parts[1:]}")
```

### Step 4: Protobuf 逆向（盲解）

#### 识别 Protobuf
- 字节流特征：`0x08` `0x12` `0x1A` `0x22` 等（字段编号 + wire type）
- 常见 Content-Type: `application/x-protobuf`, `application/grpc+proto`

#### 盲解码（无 .proto 文件）
```bash
# protobuf_inspector（自动推断结构）
pip3 install protobuf-inspector
protobuf_inspector < message.bin

# 输出示例：
# 1: 12345 (varint)
# 2: "example_string" (string)
# 3: {...} (message)
```

**手动解析 Protobuf**
```python
import io

def parse_varint(stream):
    """解析 varint 编码"""
    result = 0
    shift = 0
    while True:
        byte = stream.read(1)[0]
        result |= (byte & 0x7F) << shift
        if not (byte & 0x80):
            break
        shift += 7
    return result

def parse_protobuf(data):
    """简单 Protobuf 解析器"""
    stream = io.BytesIO(data)
    fields = {}
    
    while stream.tell() < len(data):
        tag = parse_varint(stream)
        field_number = tag >> 3
        wire_type = tag & 0x07
        
        if wire_type == 0:  # varint
            value = parse_varint(stream)
            fields[field_number] = ("varint", value)
        
        elif wire_type == 2:  # length-delimited
            length = parse_varint(stream)
            value = stream.read(length)
            try:
                fields[field_number] = ("string", value.decode('utf-8'))
            except:
                fields[field_number] = ("bytes", value.hex())
        
        # ... 其他 wire type 处理省略
    
    return fields

# 使用
with open("message.bin", "rb") as f:
    result = parse_protobuf(f.read())
    for field_num, (field_type, value) in result.items():
        print(f"Field {field_num} ({field_type}): {value}")
```

#### gRPC 逆向（基于 Protobuf）

**捕获 gRPC 流量**
```bash
# mitmproxy 插件
mitmdump -s grpc_dump.py
```

```python
# grpc_dump.py
def response(flow):
    if "application/grpc" in flow.response.headers.get("content-type", ""):
        # gRPC 消息格式：1字节压缩标志 + 4字节长度 + Protobuf数据
        data = flow.response.content
        compressed = data[0]
        length = int.from_bytes(data[1:5], 'big')
        protobuf_data = data[5:]
        
        print(f"[gRPC Response] Compressed: {compressed}, Length: {length}")
        # 使用 protobuf_inspector 解析
        import subprocess
        result = subprocess.run(['protobuf_inspector'], 
                              input=protobuf_data, 
                              capture_output=True)
        print(result.stdout.decode())
```

**gRPC Reflection（如果服务端开启）**
```bash
# grpcurl（列出服务和方法）
grpcurl -plaintext localhost:50051 list
grpcurl -plaintext localhost:50051 list com.example.Service

# 描述方法签名
grpcurl -plaintext localhost:50051 describe com.example.Service.GetUser

# 调用方法
grpcurl -plaintext -d '{"user_id": 123}' localhost:50051 com.example.Service.GetUser
```

### Step 5: 协议重放与构造

#### HTTP 请求重放（curl）
```bash
# 基础重放
curl -X POST "https://api.example.com/login" \
  -H "Content-Type: application/json" \
  -d '{"username":"test","password":"pass123"}'

# 带 Cookie 和自定义 Header
curl "https://api.example.com/profile" \
  -H "Authorization: Bearer eyJhbGc..." \
  -H "User-Agent: CustomApp/1.0" \
  -b "session=abc123"

# 代理到 Burp Suite
curl -x http://127.0.0.1:8080 --insecure "https://api.example.com/data"
```

#### Python 请求构造
```python
import requests

# POST JSON
response = requests.post(
    "https://api.example.com/login",
    json={"username": "test", "password": "pass"},
    headers={"User-Agent": "CustomApp/1.0"}
)
print(response.json())

# 上传文件
files = {'file': open('test.jpg', 'rb')}
response = requests.post("https://api.example.com/upload", files=files)

# Session（自动管理 Cookie）
session = requests.Session()
session.post("https://api.example.com/login", json={"user": "test", "pass": "123"})
response = session.get("https://api.example.com/profile")
```

#### WebSocket 测试
```python
import websocket

def on_message(ws, message):
    print(f"Received: {message}")

def on_open(ws):
    ws.send("Hello Server")

ws = websocket.WebSocketApp(
    "ws://echo.websocket.org",
    on_message=on_message,
    on_open=on_open
)
ws.run_forever()
```

#### 自定义 TCP/UDP（Scapy）
```python
from scapy.all import *

# 构造 TCP 包
ip = IP(dst="192.168.1.100")
tcp = TCP(dport=8080, flags="S")  # SYN 包
packet = ip/tcp/Raw(load=b"custom payload")

# 发送并接收响应
response = sr1(packet, timeout=2)
if response:
    response.show()

# UDP 示例
udp_packet = IP(dst="192.168.1.100")/UDP(dport=5353)/Raw(load=b"\x00\x01\x02\x03")
send(udp_packet)
```

## 常见协议速查

### Protobuf Wire Types
| Wire Type | 含义 | 数据类型 |
|-----------|------|---------|
| 0 | Varint | int32, int64, bool |
| 1 | 64-bit | fixed64, double |
| 2 | Length-delimited | string, bytes, message |
| 5 | 32-bit | fixed32, float |

### HTTP 状态码速查
```
2xx 成功
  200 OK
  201 Created
  204 No Content

3xx 重定向
  301 Moved Permanently
  302 Found
  304 Not Modified

4xx 客户端错误
  400 Bad Request
  401 Unauthorized（需认证）
  403 Forbidden（无权限）
  404 Not Found
  429 Too Many Requests

5xx 服务端错误
  500 Internal Server Error
  502 Bad Gateway
  503 Service Unavailable
```

### WebSocket Frame 结构
```
 0                   1                   2                   3
 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1
+-+-+-+-+-------+-+-------------+-------------------------------+
|F|R|R|R| opcode|M| Payload len |    Extended payload length    |
|I|S|S|S|  (4)  |A|     (7)     |             (16/64)           |
|N|V|V|V|       |S|             |   (if payload len==126/127)   |
+-+-+-+-+-------+-+-------------+-------------------------------+
```

**Opcode 类型**
- 0x0: 继续帧
- 0x1: 文本帧
- 0x2: 二进制帧
- 0x8: 关闭连接
- 0x9: Ping
- 0xA: Pong

## 加密协议处理

### TLS/SSL 解密（mitmproxy）
```bash
# 1. 导出客户端的 SSLKEYLOGFILE
export SSLKEYLOGFILE=~/sslkeys.log

# 2. 启动目标程序（会写入密钥）
./target_app

# 3. Wireshark 加载密钥文件
# Edit → Preferences → Protocols → TLS → (Pre)-Master-Secret log filename

# 现在可以看到解密后的 HTTP/2 流量
```

### 自定义加密识别
```python
# 检测是否使用常见加密算法（搜索特征常量）
import re

def detect_crypto(data):
    # AES S-box
    if b'\x63\x7c\x77\x7b\xf2\x6b' in data:
        return "Likely AES"
    
    # Base64 编码特征
    if re.match(b'^[A-Za-z0-9+/]+={0,2}$', data):
        return "Likely Base64"
    
    # 高熵值（可能加密或压缩）
    import math
    byte_counts = [data.count(bytes([i])) for i in range(256)]
    entropy = -sum((count/len(data)) * math.log2(count/len(data)) 
                   for count in byte_counts if count > 0)
    if entropy > 7.5:
        return f"High entropy ({entropy:.2f}): encrypted or compressed"
    
    return "Unknown"
```

详细加密算法特征见：`echo quickref-crypto`

## 输出要求

协议逆向完成后提供：

1. **协议文档**
   - 消息格式（字段名、类型、偏移、长度）
   - 状态机（握手/认证/会话/心跳/关闭）
   - 示例消息（十六进制 + 解析后结构）

2. **抓包证据**
   - 原始 PCAP/MITM 文件
   - 关键请求/响应截图
   - 时序图（如有多步交互）

3. **重放脚本**
   - Python/curl 完整代码
   - 必需参数说明（Token/签名计算）
   - 测试结果（成功/失败响应）

4. **Protobuf 定义**（如适用）
   - 推断的 .proto 文件
   - 字段编号和类型映射
   - 嵌套消息结构

5. **安全发现**（如有）
   - 未加密的敏感数据
   - 可重放的 Token
   - 缺失的签名验证

## 下一步

- 加密算法识别与破解 → `echo quickref-crypto`
- 移动端抓包（SSL Pinning 绕过）→ `echo mobile-reverse`
- Frida Hook 网络函数 → `echo quickref-frida`

### 来源：`sources/pro/port-scan.md`
SHA-256：`31b4767957b7b662a4d558af911f2edffec75672c2394e690b28cc705da2fb86`

# Service Discovery

Run only against `127.0.0.1`, an owned test host, or an explicitly authorized
range. Confirm the target and port ceiling before sending probes. Prefer a
small, slow inventory over broad scanning.

## Phase 1

Record the target, port range, probe type, timestamp, response evidence, and
request count. Identify listening services and versions without authentication
attempts.

## Phase 2

Verify only findings that matter to the stated local test. Do not brute force,
exploit, evade controls, or modify service state. Output a service inventory,
confidence, exposure impact, and remediation. If scope is unclear, perform no
active probe and state `未执行`.

### 来源：`sources/pro/pcap-protocol.md`
SHA-256：`3cdfc1b23ed98ae74d6a7f345ff69f72cc823c8e1a2500948fe75fa4c38d655e`

# PCAP Protocol Analysis

## Scope

Use this module only for packet captures from networks you own or are authorized to analyze. Focus on session reconstruction, payload inspection, and anomaly identification.

## Workflow

1. Load PCAP file and generate capture statistics: packet count, duration, protocols observed.
2. Extract and list unique conversations by source/destination and protocol.
3. Reconstruct TCP sessions for protocols of interest.
4. Extract and examine payloads: HTTP objects, DNS queries, file transfers.
5. Identify anomalous traffic: unusual ports, malformed packets, beaconing patterns.
6. Correlate findings with known IOCs or behavioral signatures.
7. Document findings with packet references and extracted artifacts.

## Safety Rules

- Do not analyze packet captures from networks without proper authorization.
- Do not extract or store credentials found in cleartext traffic beyond documentation.
- Do not share PCAP files containing sensitive organizational data externally.
- Do not use extracted information to access systems without authorization.

## Output

Return evidence table with columns: Session | Protocol | Packets | Finding | Artifact | Severity | Notes.

### 来源：`sources/pro/radio-sdr.md`
SHA-256：`5a3714161bedec324ee0ee612efd48beb07744a7ec8a3b83af8f8c3646738ac9`

# SDR Security Assessment

## Scope

Use this module only for radio frequency analysis on bands and equipment you own or are authorized to assess. Comply with all local radio regulations.

## Workflow

1. Define target frequency range and authorized transmission parameters.
2. Configure SDR hardware and software for passive reception.
3. Perform spectrum scan to identify active signals in authorized band.
4. Capture signal samples for offline analysis and characterization.
5. Identify modulation scheme, data rate, and framing structure.
6. Document protocol layers if digital encoding is present.
7. Assess signal for known vulnerabilities in modulation or encoding.

## Safety Rules

- Do not transmit on frequencies without proper licensing and authorization.
- Do not intercept communications not intended for your equipment.
- Do not jam, interfere with, or disrupt any radio communications.
- Do not violate local telecommunications regulations.

## Output

Return evidence table with columns: Frequency | Modulation | Bandwidth | Protocol | Security Finding | Regulatory Status.

### 来源：`sources/pro/ghidra-rpc.md`
SHA-256：`6bba7f1eb38a924fa26a7bd88510fa06ea580b450a4350215ceacd26f0e0f7d5`

# Ghidra Scripted Analysis

## Scope

Use this module only for authorized/owned binaries to perform automated analysis using Ghidra headless mode, P-Code intermediate representation, and cross-reference tracing.

## Workflow

1. Launch Ghidra in headless (analyzeHeadless) mode with target binary.
2. Run auto-analysis with appropriate analyzer configuration for the architecture.
3. Execute P-Code analysis scripts to identify cryptographic constants and algorithms.
4. Trace cross-references from exported functions to internal call trees.
5. Recover function signatures using type propagation and calling convention analysis.
6. Export analysis results (function list, types, strings) in structured format.
7. Document recovered program structure and key function purposes.

## Safety Rules

- Do not analyze binaries without ownership or written authorization.
- Do not execute target binaries during analysis.
- Do not distribute Ghidra project files containing proprietary analysis.
- Do not automate analysis against binaries obtained without permission.

## Output

Return evidence table with columns: Function Address | Recovered Signature | Xref Count | Purpose | Confidence.

### 来源：`sources/pro/dns-enum.md`
SHA-256：`72d3ca573b5dc6cce02b2cc8bb27dbb578e51733cb82ca88813b55a20e5afe90`

# DNS Inventory

Use only for a domain in the authorized scope. Prefer an owned local zone or a
passive data source. Do not perform broad third-party enumeration.

## Phase 1: bounded inventory

Record the target domain, scope, resolver, timestamp, and source. Query only the
necessary records and subdomains needed to document the owned surface. Keep
request volume bounded and write results under the local case directory.

## Phase 2: verification

For each discovered record, verify ownership and expected routing with a normal
DNS query. Do not attempt takeover, credential collection, or service access.

Output an inventory with evidence, confidence, stale-record candidates, and
remediation. A missing authorization or non-local target stops the active phase.

### 来源：`sources/pro/rev-protocol.md`
SHA-256：`bf4c20f4c1ce7d95b41160d650f721b94b2dd86d049c093cbabca5b8d7780d6c`

# 协议与接口逆向参考手册

## Scope

目标与操作范围以用户当前请求为准；核对方法前置条件、工具和附件，按实际执行层级记录结果。

## 一、Wireshark 过滤器速查

### 显示过滤器

```
# 基础过滤
ip.addr == 192.168.1.1          # IP 地址
tcp.port == 8080                # TCP 端口
udp.port == 5353                # UDP 端口
http.request.method == "POST"   # HTTP POST
dns.qry.name contains "example" # DNS 查询

# 协议过滤
websocket                       # WebSocket 流量
tls.handshake                   # TLS 握手
mqtt                            # MQTT 协议
modbus                          # Modbus 工业协议
protobuf                        # Protobuf

# 组合过滤
http && ip.dst == 10.0.0.1 && tcp.port == 443
tcp.flags.syn == 1 && tcp.flags.ack == 0  # SYN 包
frame.len > 1000                # 大于 1000 字节的包
```

### 捕获过滤器（BPF）

```
host 192.168.1.1                # 指定主机
port 80                         # 指定端口
src net 10.0.0.0/8              # 源网段
tcp port 443 and host 10.0.0.1  # 组合
not arp and not icmp            # 排除协议
```

### 实用操作

```
# 跟踪 TCP/HTTP 流：右键 → Follow → TCP Stream
# 导出 HTTP 对象：File → Export Objects → HTTP
# 会话统计：Statistics → Conversations
# 协议分层：Statistics → Protocol Hierarchy
```

## 二、mitmproxy 脚本编程

```python
# addon_example.py
from mitmproxy import http, ctx

class LogAddon:
    def request(self, flow: http.HTTPFlow):
        ctx.log.info(f"[REQ] {flow.request.method} {flow.request.url}")
        # 修改请求头
        flow.request.headers["X-Custom"] = "injected"

    def response(self, flow: http.HTTPFlow):
        ctx.log.info(f"[RSP] {flow.response.status_code} {flow.request.url}")
        # 修改响应体
        if "application/json" in flow.response.headers.get("content-type", ""):
            ctx.log.info(f"    Body: {flow.response.text[:200]}")

    def websocket_message(self, flow: http.HTTPFlow):
        msg = flow.websocket.messages[-1]
        direction = "->" if msg.from_client else "<-"
        ctx.log.info(f"[WS] {direction} {msg.content[:100]}")

addons = [LogAddon()]
# 运行: mitmproxy -s addon_example.py -p 8080
```

## 三、TCP/UDP 协议分析

### tcpdump 常用命令

```bash
tcpdump -i eth0 -nn port 8080                    # 抓指定端口
tcpdump -i eth0 -nn -w capture.pcap tcp port 443  # 保存到文件
tcpdump -r capture.pcap -nn                        # 读取文件
tcpdump -i eth0 -nn 'tcp[((tcp[12:1] & 0xf0) >> 2):4] = 0x47455420'  # 匹配 GET 请求
```

### 协议结构识别模式

```
常见协议层次:
┌──────────┬──────────┬──────────────────────┐
│  Header  │  Length  │     Payload          │
│ (固定)    │ (变长)    │  (Length 指定)        │
└──────────┴──────────┴──────────────────────┘

长度字段模式:
1. 固定长度: 每个包都是 N 字节
2. TLV (Type-Length-Value): [1B type][2B length][NB value]
3. 分隔符: 以 \r\n 或 \0 分隔
4. 长度前缀: [4B 长度][数据]
```

### Python struct 解析

```python
import struct

# 大端序解析
header = data[:4]
msg_type, msg_len = struct.unpack('>HH', header)
payload = data[4:4+msg_len]

# 小端序
val = struct.unpack('<I', data[:4])[0]

# 常见格式: >I (大端32位), <H (小端16位), >Q (大端64位)
# 网络字节序通常为大端（Big Endian）
```

### 字节序检测技巧

```python
# 方法：发送已知值，观察字节排列
# 值 0x12345678
# 大端: 12 34 56 78
# 小端: 78 56 34 12
# 通常：网络协议用大端，x86 本地程序用小端
```

## 四、Scapy 协议重放

```python
from scapy.all import *

# 基础包构造
pkt = IP(dst="10.0.0.1") / TCP(dport=8080, flags="S")  # SYN
resp = sr1(pkt)  # 发送并等待一个响应

# 自定义协议层
class MyProto(Packet):
    name = "MyProto"
    fields_desc = [
        ShortField("msg_type", 0),
        ShortField("msg_len", 0),
        StrLenField("payload", "", length_from=lambda p: p.msg_len),
    ]

pkt = IP(dst="10.0.0.1") / TCP(dport=9000) / MyProto(msg_type=1, payload=b"hello")
send(pkt)

# 从 pcap 读取并重放
pkts = rdpackets("capture.pcap")
for pkt in pkts:
    if pkt.haslayer(TCP) and pkt[TCP].dport == 8080:
        send(pkt[IP])  # 重放

# Fuzzing
pkt = IP(dst="10.0.0.1") / TCP(dport=8080) / MyProto(payload=Fuzz())
send(pkt, count=100)
```

## 五、Protobuf 逆向

### 识别

```
特征: 字节流以 0x0a (field 1, wire type 2) 开头
varint 编码: 最高位为 1 表示后续字节属于同一值
field tag = (field_number << 3) | wire_type
wire_type: 0=varint, 1=64bit, 2=length-delimited, 5=32bit
```

### 解码

```bash
# protoc 原始解码（无需 .proto 文件）
echo "0a0368656c6c6f" | xxd -r -p | protoc --decode_raw

# blackboxprotobuf（Python，无需 .proto）
pip install blackboxprotobuf
python3 -c "
import blackboxprotobuf
data = bytes.fromhex('0a0368656c6c6f')
message, typedef = blackboxprotobuf.decode_message(data)
print(message)
print(typedef)
"

# protobuf-inspector
pip install protobuf-inspector
cat data.bin | protobuf_inspector
```

### Proto 文件还原

```python
# 用 blackboxprotobuf 生成 typedef 后手动还原为 .proto
import blackboxprotobuf
data = open('sample.bin', 'rb').read()
message, typedef = blackboxprotobuf.decode_message(data)
# typedef 是字段定义字典，转换为 .proto 格式
```

### gRPC 反射

```bash
# 使用 grpcurl 调用反射 API
grpcurl -plaintext localhost:50051 list          # 列出服务
grpcurl -plaintext localhost:50051 describe pkg.ServiceName  # 描述服务
grpcurl -plaintext -d '{"key":"value"}' localhost:50051 pkg.ServiceName/Method
```

## 六、序列化格式识别

| 格式 | 魔数/特征 | 识别方法 |
|------|----------|---------|
| Protobuf | `0x0a` 开头，varint 编码 | protoc --decode_raw |
| MessagePack | `0xc0-0xdf` 前缀 | `msgpack -b data.bin` |
| Thrift | `0x80` 或 `0x00` 开头 | TBinaryProtocol: 4B version + method |
| Avro | `Obj\x01` 魔数 | avro-tools |
| CBOR | major type 前 3 bit | cbor2 Python 库 |
| JSON | `{` 或 `[` 开头 | 直接可读 |

### MessagePack 解码

```python
import msgpack
with open('data.bin', 'rb') as f:
    obj = msgpack.unpack(f)
    print(obj)
```

### 自定义二进制格式

```python
import struct

def parse_custom(data):
    offset = 0
    results = []
    while offset < len(data):
        # 假设: [2B type][2B length][NB payload]
        if len(data) - offset < 4:
            break
        msg_type, msg_len = struct.unpack('>HH', data[offset:offset+4])
        offset += 4
        payload = data[offset:offset+msg_len]
        offset += msg_len
        results.append({'type': msg_type, 'payload': payload})
    return results
```

## 七、RPC 协议逆向

### gRPC

```bash
# gRPC over HTTP/2
# 识别: HTTP/2 帧，Content-Type: application/grpc
# 帧格式: [1B compressed][4B length][NB message]

# 反射
grpcurl -plaintext localhost:50051 list
grpcurl -plaintext localhost:50051 describe package.Service

# 无需反射时：抓包分析 protobuf 编码的请求/响应
```

### JSON-RPC 2.0

```json
// 请求
{"jsonrpc":"2.0","method":"getUser","params":{"id":1},"id":1}
// 响应
{"jsonrpc":"2.0","result":{"name":"test"},"id":1}
// 特征: 固定 jsonrpc 字段，method/params/id 结构
```

### IPC 机制

```bash
# Named Pipes (Windows)
# 特征: \\.\pipe\pipename
# 工具: Pipe Monitor, Process Monitor

# Unix Domain Sockets (Linux)
# 特征: /tmp/.X11-unix/X0 等 socket 文件
strace -e trace=connect -f target_program

# D-Bus (Linux)
dbus-monitor --session   # 监控会话总线
dbus-monitor --system    # 监控系统总线
busctl list              # 列出总线连接
```

## 八、蓝牙与 IoT

### BLE 分析

```bash
# nRF Connect (手机 App) - 扫描 BLE 设备
# Wireshark - 导入 BLE 抓包
# 关键: GATT Service UUID → Characteristic UUID → Read/Write/Notify

# BLE 特征码
# Service: 0x1800 (Generic Access), 0x1801 (Generic Attribute)
# 常见: 0x180A (Device Information), 0x180F (Battery)
```

### MQTT

```bash
# 订阅所有主题
mosquitto_sub -h broker.example.com -t '#' -v

# 发布消息
mosquitto_h -h broker.example.com -t 'test/topic' -m 'hello'

# 抓包分析: Wireshark MQTT dissector
# 关键: CONNECT/SUBSCRIBE/PUBLISH 包, topic, payload
```

### Modbus

```bash
# 功能码: 01=读线圈, 02=读离散输入, 03=读保持寄存器, 04=读输入寄存器
# 05=写单个线圈, 06=写单个寄存器

# Wireshark 过滤
modbus && ip.addr == 192.168.1.100

# Python Modbus 客户端
from pymodbus.client import ModbusTcpClient
client = ModbusTcpClient('192.168.1.100', port=502)
result = client.read_holding_registers(0, 10, slave=1)
print(result.registers)
```

## 九、协议文档化

### 字段表模板

```markdown
## 消息格式: LoginRequest (type=0x01)

| 偏移 | 长度 | 类型 | 字段名 | 说明 |
|------|------|------|--------|------|
| 0x00 | 2 | uint16 BE | msg_type | 消息类型 = 0x01 |
| 0x02 | 2 | uint16 BE | msg_len | 后续数据长度 |
| 0x04 | 4 | uint32 BE | user_id | 用户 ID |
| 0x08 | N | string | username | 用户名（UTF-8） |
| 0x08+N | 16 | bytes | token | 认证令牌 |
```

### Wireshark Lua Dissector 模板

```lua
-- myproto.lua
local myproto = Proto("myproto", "My Custom Protocol")

myproto.fields.msg_type = ProtoField.uint16("myproto.type", "Message Type", base.HEX)
myproto.fields.msg_len  = ProtoField.uint16("myproto.len", "Length", base.DEC)
myproto.fields.payload  = ProtoField.bytes("myproto.payload", "Payload")

function myproto.dissector(buf, pinfo, tree)
    pinfo.cols.protocol = "MYPROTO"
    local subtree = tree:add(myproto, buf())
    subtree:add(myproto.fields.msg_type, buf(0,2))
    subtree:add(myproto.fields.msg_len, buf(2,2))
    local len = buf(2,2):uint()
    subtree:add(myproto.fields.payload, buf(4, len))
end

-- 注册到 TCP 端口
local tcp_table = DissectorTable.get("tcp.port")
tcp_table:add(9000, myproto)
-- 加载: wireshark -X lua_script:myproto.lua
```

### 来源：`sources/pro/wifi-wireless.md`
SHA-256：`e1e662bd7db9598dde23ae9778460ee76fb4a8a10733a563fe7298c9073bf9b1`

# Wireless Security Assessment

## Scope

Use this module only for wireless networks you own or have written authorization to assess. Focus on configuration hardening and rogue device detection.

## Workflow

1. Document authorized wireless infrastructure: SSIDs, BSSIDs, channels, encryption.
2. Perform passive scan to enumerate all visible access points in range.
3. Identify rogue or unauthorized access points by comparing against inventory.
4. Assess encryption configuration: WPA3/WPA2 settings, PMF, key rotation.
5. For owned networks, capture WPA handshake to verify password strength offline.
6. Review client isolation, VLAN segmentation, and management interface security.
7. Document findings with remediation recommendations.

## Safety Rules

- Do not assess wireless networks without ownership or written authorization.
- Do not perform deauthentication attacks against networks with active users.
- Do not intercept or store traffic from networks you do not own.
- Do not attempt to crack credentials for networks without explicit authorization.

## Output

Return evidence table with columns: SSID | BSSID | Encryption | Channel | Finding | Risk | Recommendation.

### 来源：`sources/pro/protocol-reverse-advanced.md`
SHA-256：`e575afc9787ee0f4c1692a03d37928db4d3e5915163af3cd21cef424cd1c4f1f`

# Advanced Protocol Reverse Engineering

## Scope

Use this module only for authorized/owned network protocols to document binary framing, reconstruct stateful sessions, and map protocol state machines.

## Workflow

1. Set up controlled TLS interception proxy on owned infrastructure.
2. Capture protocol traffic between authorized client and server endpoints.
3. Identify binary framing structure: header fields, length encoding, type identifiers.
4. Map message types and their associated payload schemas.
5. Reconstruct session state machine from observed message sequences.
6. Document authentication and key exchange handshake flows.
7. Produce protocol specification with field-level annotations.

## Safety Rules

- Do not intercept traffic on networks or services you do not own.
- Do not capture credentials or session tokens beyond documentation needs.
- Do not replay captured sessions against production systems.
- Do not distribute interception tooling configured for third-party services.

## Output

Return evidence table with columns: Message Type | Direction | Fields | State Transition | Notes.

## 云端资料获取

`module:ID` 表示本技能库的云模块。客户端会在需要时用当前登录会话获取目标模块；不要把模块内容写回源文件。

Windows PowerShell：

Bash：

## 使用前核对

目标与操作范围以用户当前请求为准；核对方法前置条件、工具和附件，按实际执行层级记录结果。正文不表示示例代码已经在本机执行或验证。
