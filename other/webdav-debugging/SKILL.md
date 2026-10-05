---
name: webdav-debugging
description: WebDAV proxy/upstream 问题系统调试方法论 — 502/405/协议兼容性诊断
category: devops
---

# WebDAV 服务调试方法论

## 触发条件
WebDAV 同步失败、502/405 等非预期错误、客户端报错但服务端日志不明。

## 参考文件
- `references/nginx-webdav-proxy.md` — OpenList WebDAV 完整 Nginx 代理配置模板（含 Lua Destination 重写）

## 环境提示
- 用户 fish shell 不支持 bash heredoc（`<< 'EOF'`），编辑容器内文件用 `docker cp` + `python3 -c` 或 `sed`
- Docker 容器重启会丢 `/etc/hosts`，`host.docker.internal` 不可靠，直接用 `172.17.0.1`

## 调试流程

### 1. 分层隔离——最核心原则
不要在猜疑链里打转。每层独立验证：
- **客户端层**：curl 直接模拟客户端行为（相同 URL、相同 header）
- **代理层（容器内）**：`docker exec <container> curl http://localhost:<port>/...` — 绕过外部网络
- **上游服务层**：直接 curl 上游地址（如 `http://172.17.0.1:5244`），完全绕过代理

**案例**：本次 debug 花了数小时怀疑 WAF，但容器内 MOVE 是 200 外部却是 502——说明问题在 WAF 和上游之间那层。最终发现是 OpenList 拒绝了 Destination 绝对 URL。

### 2. 不要假定上游支持标准协议
- WebDAV RFC 规定 Destination 可以是绝对 URL，但 OpenList 只接受相对路径
- **操作**：遇到协议级错误（如 502），先测试变体（相对路径 vs 绝对路径、不同 header 值）

### 3. 502 ≠ 代理连不上上游
502 的常见原因不止"上游宕机"：
- 上游接受了连接但返回了无效响应（nginx 判定为 bad gateway）
- 上游对特定 HTTP 方法或 header 组合静默断开
- WAF/Lua 模块在代理层静默拦截

**关键教训**：error.log 没日志 ≠ 没问题。本次 error.log 对 MOVE 完全没有错误记录，但 502 确实在发生。

### 4. 权限/文件类型问题
- `GET /dav/head.json` → 405，因为磁盘上 `head.json` 是**目录**而非文件
- 删除时注意：DELETE 请求可能被 WAF/登录页拦截，用 `rm -rf` 直接从磁盘删除更可靠
- PROPFIND 返回 `<D:collection/>` 就是目录——客户端 GET 目录会 405

### 5. Docker 容器注意事项
- `host.docker.internal` 依赖 `/etc/hosts`，容器重启/重建后会丢失
- **直接用 Docker 网桥 IP**（`172.17.0.1`），这个不会变
- 在宿主机上改容器内文件：`docker cp` 拉出 → 修改 → `docker cp` 塞回

### 6. WAF 烟雾弹识别
- 1Panel WAF 的 `siteConfig.json` 有 methodWhite/header/xss 等规则
- 全部关掉问题依旧 → WAF 不是根因，不要再浪费时间
- `nginx -s reload` 不刷新 Lua 共享内存，需要 `docker restart` 完全重启
- 修改容器内文件注意持久化：容器重启后 `/etc/hosts` 等会丢失
