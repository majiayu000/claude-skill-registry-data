---
name: multi-service-debug
description: |
  多服务调试技能：针对 Vercel + GCP Cloud Run 混合架构的调试工作流。
  Use when: 跨服务问题排查、日志聚合分析、服务间通信调试、生产环境故障定位。
  Triggers: "调试", "debug", "日志", "logs", "错误", "error", "服务", "service", "通信", "超时", "timeout"
category: debugging
---

# Multi-Service Debug (多服务调试)

> 🔍 **核心理念**: 分布式系统调试需要全局视角。单点日志不够，必须关联多服务日志才能定位根因。

## 🔴 第一原则：先画调用链，再看日志

**调试分布式问题必须先理清服务调用关系！**

```
❌ 错误思路: "报错了，看看这个服务的日志"
✅ 正确思路: "报错了，先画出请求经过哪些服务，再逐个检查"

❌ 错误思路: "这个服务没问题，肯定是那个服务的问题"  
✅ 正确思路: "先确认请求是否正确到达，再判断是哪个环节出问题"
```

**调试优先级**: 网络连通性 > 请求格式 > 服务逻辑 > 资源限制

## When to Use This Skill

使用此技能当你需要：
- 排查跨服务调用失败的问题
- 聚合分析多个服务的日志
- 调试服务间通信（HTTP/WebSocket）
- 定位生产环境的性能瓶颈
- 排查超时、连接失败等网络问题
- 验证服务健康状态

## Not For / Boundaries

此技能不适用于：
- 单服务内部的业务逻辑调试
- 前端 UI 渲染问题
- 数据库查询优化（参考 performance-optimization skill）

---

## Quick Reference

### 🏗️ 项目服务架构

```
┌─────────────────────────────────────────────────────────────────┐
│                         用户浏览器                               │
└─────────────────────────────────────────────────────────────────┘
                                │
                                ▼
┌─────────────────────────────────────────────────────────────────┐
│                    Vercel (前端 + API)                          │
│  ┌─────────────────┐    ┌─────────────────────────────────────┐ │
│  │   React SPA     │    │   Serverless Functions (/api/*)     │ │
│  │   (client/)     │    │   - /api/health                     │ │
│  │                 │    │   - /api/chat                       │ │
│  │                 │    │   - /api/documents                  │ │
│  │                 │    │   - /api/unified-intelligence/*     │ │
│  └─────────────────┘    └─────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────────┘
                                │
                ┌───────────────┼───────────────┐
                ▼               ▼               ▼
┌───────────────────┐ ┌───────────────────┐ ┌───────────────────┐
│   LightRAG        │ │   Voice Service   │ │   Quant Service   │
│   (Cloud Run)     │ │   (Cloud Run)     │ │   (Cloud Run)     │
│                   │ │                   │ │                   │
│   Port: 9621      │ │   Port: 8080      │ │   Port: 6900      │
│   Python/FastAPI  │ │   Python/LiveKit  │ │   Python/FastAPI  │
└───────────────────┘ └───────────────────┘ └───────────────────┘
```

### 📋 服务端点速查

| 服务 | 本地端口 | 生产 URL | 健康检查 |
|------|----------|----------|----------|
| Vercel API | 3000 | `https://your-app.vercel.app` | `/api/health` |
| LightRAG | 9621 | `lightrag-service-xxx-uc.a.run.app` | `/health` |
| Voice | 8080 | `voice-service-xxx-uc.a.run.app` | `/health` |
| Quant | 6900 | `quant-service-xxx-uc.a.run.app` | `/health` |

### 🔍 快速诊断命令

```bash
# 1. 检查所有服务健康状态
curl -s https://your-app.vercel.app/api/health | jq
curl -s https://lightrag-service-xxx-uc.a.run.app/health | jq
curl -s https://voice-service-xxx-uc.a.run.app/health | jq
curl -s https://quant-service-xxx-uc.a.run.app/health | jq

# 2. 查看 GCP 服务日志
gcloud logging read "resource.type=cloud_run_revision" --limit=50 --format=json | jq

# 3. 查看特定服务日志
gcloud logging read "resource.labels.service_name=lightrag-service" --limit=20
```

---

## 多服务调试工作流

### Phase 1: 问题定位

```
1. 确认问题现象（错误信息、HTTP 状态码）
2. 画出请求调用链
3. 确定问题发生在哪个服务之间
4. 收集相关时间点的日志
```

### Phase 2: 日志聚合

```bash
# 设置时间范围（问题发生前后 5 分钟）
START_TIME="2025-01-01T10:00:00Z"
END_TIME="2025-01-01T10:10:00Z"

# 聚合所有 Cloud Run 服务日志
gcloud logging read \
  "resource.type=cloud_run_revision AND timestamp>=\"$START_TIME\" AND timestamp<=\"$END_TIME\"" \
  --format="table(timestamp,resource.labels.service_name,textPayload)" \
  --order=asc
```

### Phase 3: 关联分析

```
1. 按时间排序所有日志
2. 找到请求入口日志
3. 追踪请求 ID（如果有）
4. 找到错误发生点
5. 分析上下文日志
```

### Phase 4: 验证修复

```
1. 本地复现问题
2. 应用修复
3. 本地验证
4. 部署到生产
5. 生产验证
```

---

## 日志聚合分析

### 📊 GCP Cloud Run 日志查询

```bash
# 查看所有服务的错误日志
gcloud logging read \
  "resource.type=cloud_run_revision AND severity>=ERROR" \
  --limit=50 \
  --format="table(timestamp,resource.labels.service_name,textPayload)"

# 查看特定服务的详细日志
gcloud logging read \
  "resource.labels.service_name=lightrag-service" \
  --limit=100 \
  --format=json | jq '.[] | {time: .timestamp, msg: .textPayload}'

# 按关键词搜索日志
gcloud logging read \
  "resource.type=cloud_run_revision AND textPayload:\"error\"" \
  --limit=50
```

### 📊 Vercel 日志查询

```bash
# 查看最近部署的日志
vercel logs <deployment-url> --follow

# 查看函数执行日志
vercel logs <deployment-url> --output=raw | grep -i error
```

### 📊 日志关联技巧

```typescript
// 在请求中添加 trace ID
const traceId = crypto.randomUUID();

// 传递给下游服务
fetch(LIGHTRAG_URL, {
  headers: {
    'X-Trace-ID': traceId,
    'X-Request-Time': new Date().toISOString(),
  }
});

// 在日志中包含 trace ID
console.log(`[${traceId}] Processing request...`);
```

---

## 服务间通信调试

### 🔗 HTTP 调用调试

```bash
# 测试 Vercel -> LightRAG 通信
curl -v -X POST https://lightrag-service-xxx-uc.a.run.app/query \
  -H "Content-Type: application/json" \
  -d '{"query": "test"}'

# 检查响应时间
curl -w "@curl-format.txt" -s -o /dev/null \
  https://lightrag-service-xxx-uc.a.run.app/health

# curl-format.txt 内容:
#   time_namelookup:  %{time_namelookup}s\n
#   time_connect:     %{time_connect}s\n
#   time_appconnect:  %{time_appconnect}s\n
#   time_pretransfer: %{time_pretransfer}s\n
#   time_redirect:    %{time_redirect}s\n
#   time_starttransfer: %{time_starttransfer}s\n
#   time_total:       %{time_total}s\n
```

### 🔗 WebSocket 调试 (Voice Service)

```bash
# 使用 websocat 测试 WebSocket 连接
websocat wss://voice-service-xxx-uc.a.run.app/ws

# 或使用 wscat
npx wscat -c wss://voice-service-xxx-uc.a.run.app/ws
```

### 🔗 常见通信问题

| 问题 | 症状 | 排查方向 |
|------|------|----------|
| 连接超时 | `ETIMEDOUT` | 检查网络、防火墙、服务是否运行 |
| 连接拒绝 | `ECONNREFUSED` | 检查端口、服务状态 |
| SSL 错误 | `CERT_*` | 检查证书配置 |
| 502 Bad Gateway | 上游服务错误 | 检查目标服务日志 |
| 503 Service Unavailable | 服务过载 | 检查资源限制、扩容 |
| CORS 错误 | 跨域被拒绝 | 检查 CORS 配置 |

---

## 常见问题排查

### 🔴 问题 1: Vercel API 调用 Cloud Run 超时

**症状**: API 返回 504 Gateway Timeout

**排查步骤**:
```bash
# 1. 检查 Cloud Run 服务状态
gcloud run services describe lightrag-service --region=us-central1

# 2. 检查服务日志
gcloud logging read "resource.labels.service_name=lightrag-service" --limit=20

# 3. 检查冷启动时间
# 如果服务长时间未访问，可能需要预热

# 4. 检查 Vercel 函数超时配置
# vercel.json 中的 maxDuration 设置
```

**解决方案**:
- 增加 Vercel 函数超时时间
- 设置 Cloud Run 最小实例数避免冷启动
- 优化服务启动时间

### 🔴 问题 2: 服务间认证失败

**症状**: 返回 401 Unauthorized 或 403 Forbidden

**排查步骤**:
```bash
# 1. 检查服务是否需要认证
gcloud run services describe <service> --format="yaml(spec.template.metadata.annotations)"

# 2. 检查 IAM 权限
gcloud run services get-iam-policy <service>

# 3. 检查请求头中的认证信息
curl -v -H "Authorization: Bearer $TOKEN" https://service-url/endpoint
```

**解决方案**:
- 配置服务允许未认证访问（公开服务）
- 或配置正确的服务账号和 IAM 权限

### 🔴 问题 3: 环境变量不一致

**症状**: 本地正常，生产报错

**排查步骤**:
```bash
# 1. 检查 Vercel 环境变量
vercel env ls

# 2. 检查 Cloud Run 环境变量
gcloud run services describe <service> \
  --format="yaml(spec.template.spec.containers[0].env)"

# 3. 对比本地 .env 文件
cat .env | grep -E "^[A-Z]"
```

**解决方案**:
- 同步所有环境变量
- 使用 Secret Manager 管理敏感配置

### 🔴 问题 4: 内存/CPU 不足

**症状**: 服务频繁重启、OOM 错误

**排查步骤**:
```bash
# 1. 查看资源使用情况
gcloud run services describe <service> \
  --format="yaml(spec.template.spec.containers[0].resources)"

# 2. 查看 OOM 日志
gcloud logging read \
  "resource.labels.service_name=<service> AND textPayload:\"OOM\""

# 3. 查看 GCP Console Metrics
# Cloud Run > 服务 > Metrics > Memory utilization
```

**解决方案**:
- 增加内存配置
- 优化代码减少内存使用
- 添加内存监控告警

---

## 调试工具推荐

### 🛠️ 命令行工具

| 工具 | 用途 | 安装 |
|------|------|------|
| `gcloud` | GCP 服务管理 | `brew install google-cloud-sdk` |
| `vercel` | Vercel 部署管理 | `npm i -g vercel` |
| `jq` | JSON 处理 | `brew install jq` |
| `websocat` | WebSocket 调试 | `brew install websocat` |
| `httpie` | HTTP 调试 | `brew install httpie` |

### 🛠️ 浏览器工具

- **Network 面板**: 查看请求/响应详情
- **Console 面板**: 查看前端日志
- **Application 面板**: 查看存储、Cookie

### 🛠️ 监控工具

- **GCP Cloud Monitoring**: 服务指标、告警
- **Vercel Analytics**: 前端性能、函数执行
- **Sentry**: 错误追踪（如已集成）

---

## Examples

### Example 1: 排查 LightRAG 查询失败

**场景**: 用户报告文档搜索功能返回错误

**Steps**:
```bash
# 1. 确认问题 - 检查 Vercel API 日志
vercel logs <deployment-url> | grep -i lightrag

# 2. 检查 LightRAG 服务状态
curl -s https://lightrag-service-xxx-uc.a.run.app/health | jq

# 3. 查看 LightRAG 服务日志
gcloud logging read "resource.labels.service_name=lightrag-service" --limit=20

# 4. 本地复现
curl -X POST http://localhost:9621/query \
  -H "Content-Type: application/json" \
  -d '{"query": "test query"}'

# 5. 修复并验证
# ... 修复代码 ...
# 重新部署后验证
```

### Example 2: 排查 Voice 服务 WebSocket 断连

**场景**: 语音对话频繁断开

**Steps**:
```bash
# 1. 检查 WebSocket 连接
websocat wss://voice-service-xxx-uc.a.run.app/ws

# 2. 查看服务日志
gcloud logging read \
  "resource.labels.service_name=voice-service AND textPayload:\"disconnect\"" \
  --limit=50

# 3. 检查资源限制
gcloud run services describe voice-service \
  --format="yaml(spec.template.spec.containers[0].resources)"

# 4. 检查并发连接数
# GCP Console > Cloud Run > voice-service > Metrics
```

### Example 3: 全链路性能分析

**场景**: 用户反馈页面加载慢

**Steps**:
```bash
# 1. 测量各服务响应时间
for service in "vercel-app" "lightrag-service" "quant-service"; do
  echo "Testing $service..."
  curl -w "Total: %{time_total}s\n" -s -o /dev/null \
    "https://$service-xxx.run.app/health"
done

# 2. 分析慢请求
gcloud logging read \
  "resource.type=cloud_run_revision AND httpRequest.latency>\"1s\"" \
  --limit=20

# 3. 检查数据库查询时间
# 查看 Supabase Dashboard > Database > Query Performance
```

---

## References

- `references/service-map.md`: 服务依赖关系图、端口和端点清单
- `references/log-queries.md`: 常用日志查询命令集合
- `references/troubleshooting-checklist.md`: 故障排查检查清单

---

## Maintenance

- **Sources**: GCP Cloud Run 文档, Vercel 文档, 项目实践经验
- **Last Updated**: 2025-01-01
- **Known Limits**: 
  - 日志查询依赖 `gcloud` CLI 认证
  - 某些调试需要相应的 GCP/Vercel 访问权限
