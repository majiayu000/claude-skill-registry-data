---
skill_name: dify-security-deployment
version: 1.0.0
parent_skill: dify-master
description: Dify 安全实践和部署运维完整指南，涵盖SSRF防护、代码沙箱、Docker/Kubernetes部署、监控告警和故障恢复
category: security-operations
tags:
  - security
  - deployment
  - docker
  - kubernetes
  - monitoring
  - ssrf
  - sandbox
dependencies: []
last_updated: 2026-03-04
---

# Dify 安全和部署 SKILL

## 概述

本 SKILL 提供 Dify 平台的安全实践和部署运维完整指南，帮助开发者和运维人员构建安全、稳定、高性能的生产环境。

### 触发场景

使用本 SKILL 当你需要:

- 🚀 **部署 Dify 到生产环境** (Docker/Kubernetes)
- 🔒 **配置安全防护机制** (SSRF、沙箱、加密)
- 🔧 **解决部署问题** (容器启动失败、网络配置、性能瓶颈)
- 📊 **优化生产环境** (监控告警、高可用、故障恢复)
- ✅ **进行安全审计** 和配置验证

### 核心能力

- **安全防护**: SSRF 防护、代码沙箱、数据加密、权限管理
- **Docker 部署**: 快速部署、生产配置、网络架构、资源优化
- **Kubernetes 部署**: 高可用架构、自动扩展、Helm 部署
- **监控告警**: OpenTelemetry、Sentry、日志聚合、性能监控
- **故障恢复**: 问题诊断、恢复流程、备份策略

---

## 快速开始

### 最小部署配置

```bash
# 1. 克隆仓库
git clone https://github.com/langgenius/dify.git
cd dify/docker

# 2. 复制环境变量
cp .env.example .env

# 3. 修改关键安全配置
# 编辑 .env 文件:
SECRET_KEY=$(openssl rand -base64 42)
DB_PASSWORD=your-strong-password
REDIS_PASSWORD=your-redis-password
SANDBOX_API_KEY=$(openssl rand -base64 32)

# 4. 启动服务
docker compose up -d

# 5. 验证部署
docker compose ps
curl http://localhost/health
```

### 安全检查清单

#### 部署前检查

- [ ] **SECRET_KEY** 已更改为强密钥 (使用 `openssl rand -base64 42`)
- [ ] **数据库密码** 已修改默认值
- [ ] **Redis 密码** 已设置
- [ ] **SSRF Proxy** 已配置并阻止内网访问
- [ ] **Sandbox 沙箱** 已启用网络代理
- [ ] **HTTPS/TLS** 证书已配置 (生产环境)
- [ ] **API Key 管理** 机制已启用
- [ ] **文件上传限制** 已设置 (UPLOAD_FILE_SIZE_LIMIT)
- [ ] **敏感环境变量** 已加密存储

#### 运行时检查

- [ ] **容器权限** 以非 root 用户运行
- [ ] **网络隔离** ssrf_proxy_network 正常工作
- [ ] **健康检查** 所有服务健康状态正常
- [ ] **日志记录** 已启用并正常输出
- [ ] **监控告警** 已配置 (OpenTelemetry/Sentry)
- [ ] **备份策略** 已实施 (数据库、文件存储)
- [ ] **资源限制** CPU/内存限制已配置
- [ ] **SSL 证书** 有效期检查和自动续期

---

## 目录结构

```
04-security/
├── SKILL.md                    # 本文件 - 安全和部署总览
├── security/                   # 安全实践
│   ├── ssrf-protection.md     # SSRF 防护配置
│   ├── sandbox.md             # 代码沙箱隔离
│   ├── encryption.md          # 数据加密和 TLS
│   └── auth.md                # 认证和权限管理
├── deployment/                 # 部署指南
│   ├── docker-compose.md      # Docker Compose 部署
│   ├── kubernetes.md          # Kubernetes 部署
│   ├── serverless.md          # Serverless 部署
│   └── high-availability.md   # 高可用架构
├── operations/                 # 运维实践
│   ├── monitoring.md          # 监控和告警
│   ├── logging.md             # 日志管理
│   ├── backup.md              # 备份和恢复
│   └── troubleshooting.md     # 故障排查
└── best-practices.md           # 最佳实践总结
```

---

## 一、安全防护机制

### 1.1 SSRF 防护

Dify 使用 Squid 代理实现 SSRF (Server-Side Request Forgery) 防护，阻止访问内网地址。

**核心配置**:

```conf
# squid.conf - 内网地址黑名单
acl localnet src 10.0.0.0/8
acl localnet src 172.16.0.0/12
acl localnet src 192.168.0.0/16
acl localnet src 127.0.0.0/8

# 拒绝访问内网
http_access deny localnet

# 允许的端口
acl Safe_ports port 80 443 1025-65535
http_access deny !Safe_ports
```

**验证方法**:

```bash
# 测试内网访问被阻止
docker compose exec api curl -x http://ssrf_proxy:3128 http://127.0.0.1
# 应返回 403 Forbidden

# 测试外部访问正常
docker compose exec api curl -x http://ssrf_proxy:3128 https://api.openai.com
# 应正常返回
```

📖 **详细文档**: [security/ssrf-protection.md](security/ssrf-protection.md)

### 1.2 代码沙箱

Sandbox 服务提供安全的代码执行环境，隔离用户代码。

**核心配置**:

```yaml
# config.yaml
app:
  key: dify-sandbox  # 修改为强密钥
max_workers: 4
worker_timeout: 15
enable_network: true  # 通过 SSRF Proxy 访问外部
proxy:
  http: 'http://ssrf_proxy:3128'
  https: 'http://ssrf_proxy:3128'
```

**安全特性**:

- ✅ 系统调用白名单限制
- ✅ 资源配额管理 (CPU、内存、超时)
- ✅ 网络访问通过 SSRF Proxy
- ✅ 文件系统隔离

📖 **详细文档**: [security/sandbox.md](security/sandbox.md)

### 1.3 数据加密

**传输加密 (TLS/HTTPS)**:

```bash
# .env 配置
NGINX_HTTPS_ENABLED=true
NGINX_SSL_CERT_FILENAME=fullchain.pem
NGINX_SSL_CERT_KEY_FILENAME=privkey.pem
NGINX_SSL_PROTOCOLS=TLSv1.2 TLSv1.3
```

**数据库连接加密**:

```bash
# PostgreSQL SSL
DB_HOST=db_postgres
POSTGRES_SSL_MODE=require

# Redis SSL
REDIS_USE_SSL=true
REDIS_SSL_CERT_REQS=CERT_REQUIRED
```

📖 **详细文档**: [security/encryption.md](security/encryption.md)

### 1.4 权限管理

**API Key 管理**:

```bash
# 生成强密钥
SECRET_KEY=$(openssl rand -base64 42)
PLUGIN_DAEMON_KEY=$(openssl rand -base64 42)
PLUGIN_DIFY_INNER_API_KEY=$(openssl rand -base64 42)
```

**OAuth 2.0 集成**:

- 支持第三方服务授权
- 访问令牌自动刷新
- 权限范围控制

📖 **详细文档**: [security/auth.md](security/auth.md)

---

## 二、Docker 部署

### 2.1 快速部署

**一键启动**:

```bash
cd dify/docker
cp .env.example .env
# 编辑 .env 修改密码和密钥
docker compose up -d
```

**服务架构**:

```
nginx (80/443)
  ├── web (3000) - 前端 UI
  ├── api (5001) - 业务逻辑
  ├── worker - 后台任务
  ├── beat - 定时任务
  ├── plugin_daemon (5002) - 插件管理
  └── sandbox (8194) - 代码执行

基础服务:
  ├── db_postgres (5432) - 主数据库
  ├── redis (6379) - 缓存和队列
  ├── weaviate (8080) - 向量数据库
  └── ssrf_proxy (3128) - SSRF 防护
```

📖 **详细文档**: [deployment/docker-compose.md](deployment/docker-compose.md)

### 2.2 生产级配置

**资源限制**:

```yaml
# docker-compose.yaml
services:
  api:
    deploy:
      resources:
        limits:
          cpus: '2'
          memory: 4G
        reservations:
          cpus: '1'
          memory: 2G
```

**健康检查**:

```yaml
healthcheck:
  test: ["CMD", "curl", "-f", "http://localhost:5001/health"]
  interval: 30s
  timeout: 10s
  retries: 3
  start_period: 40s
```

**日志管理**:

```yaml
logging:
  driver: "json-file"
  options:
    max-size: "10m"
    max-file: "3"
```

📖 **详细文档**: [deployment/docker-compose.md](deployment/docker-compose.md)

### 2.3 网络架构

**网络隔离**:

```yaml
networks:
  # 内部网络 - 无法访问外部
  ssrf_proxy_network:
    driver: bridge
    internal: true

  # 默认网络 - 可访问外部
  default:
    driver: bridge
```

**服务通信**:

- API/Worker/Sandbox → ssrf_proxy → 外部 API
- Nginx → API/Web (反向代理)
- API → Database/Redis (内部通信)

📖 **详细文档**: [deployment/docker-compose.md](deployment/docker-compose.md)

---

## 三、Kubernetes 部署

### 3.1 Helm 快速部署

```bash
# 添加 Helm 仓库
helm repo add dify https://borispolonsky.github.io/dify-helm
helm repo update

# 安装 Dify
helm install my-dify dify/dify \
  --set postgresql.enabled=true \
  --set redis.enabled=true \
  --set weaviate.enabled=true

# 查看状态
kubectl get pods -l app.kubernetes.io/name=dify
```

### 3.2 高可用架构

**多副本部署**:

```yaml
# values.yaml
api:
  replicaCount: 3
  resources:
    limits:
      cpu: 2000m
      memory: 4Gi
    requests:
      cpu: 1000m
      memory: 2Gi

worker:
  replicaCount: 2
  autoscaling:
    enabled: true
    minReplicas: 2
    maxReplicas: 10
    targetCPUUtilizationPercentage: 80
```

**Pod 反亲和性**:

```yaml
affinity:
  podAntiAffinity:
    preferredDuringSchedulingIgnoredDuringExecution:
    - weight: 100
      podAffinityTerm:
        labelSelector:
          matchExpressions:
          - key: app
            operator: In
            values:
            - dify-api
        topologyKey: kubernetes.io/hostname
```

📖 **详细文档**: [deployment/kubernetes.md](deployment/kubernetes.md)

### 3.3 托管服务集成

**使用云厂商托管服务**:

```yaml
# 使用 RDS PostgreSQL
postgresql:
  enabled: false
externalDatabase:
  host: your-rds-endpoint.rds.amazonaws.com
  port: 5432
  database: dify
  username: dify
  password: your-password

# 使用 ElastiCache Redis
redis:
  enabled: false
externalRedis:
  host: your-redis.cache.amazonaws.com
  port: 6379
  password: your-password
```

**优势**:

- ✅ 自动备份和恢复
- ✅ 高可用和故障转移
- ✅ 性能监控和优化
- ✅ 减少运维负担

📖 **详细文档**: [deployment/high-availability.md](deployment/high-availability.md)

---

## 四、监控和告警

### 4.1 OpenTelemetry 配置

```bash
# .env
ENABLE_OTEL=true
OTLP_BASE_ENDPOINT=http://otel-collector:4318
OTEL_SAMPLING_RATE=0.1
OTEL_BATCH_EXPORT_SCHEDULE_DELAY=5000
OTEL_MAX_QUEUE_SIZE=2048
OTEL_METRIC_EXPORT_INTERVAL=60000
```

**监控指标**:

- 请求延迟和吞吐量
- 错误率和成功率
- 资源使用 (CPU、内存、磁盘)
- 数据库连接池状态
- 队列深度和处理速度

### 4.2 Sentry 错误追踪

```bash
# .env
API_SENTRY_DSN=https://your-key@sentry.io/project-id
API_SENTRY_TRACES_SAMPLE_RATE=1.0
WEB_SENTRY_DSN=https://your-key@sentry.io/project-id
PLUGIN_SENTRY_ENABLED=true
```

### 4.3 日志聚合

```bash
# 日志配置
LOG_LEVEL=INFO
LOG_OUTPUT_FORMAT=json
LOG_FILE=/app/logs/server.log
LOG_FILE_MAX_SIZE=20
LOG_FILE_BACKUP_COUNT=5
```

**日志查看**:

```bash
# Docker
docker compose logs -f api
docker compose logs --tail=100 worker

# Kubernetes
kubectl logs -f deployment/dify-api
kubectl logs -l app=dify-worker --tail=100
```

📖 **详细文档**: [operations/monitoring.md](operations/monitoring.md)

### 4.4 队列监控

```bash
# .env
QUEUE_MONITOR_THRESHOLD=200
QUEUE_MONITOR_ALERT_EMAILS=admin@example.com,ops@example.com
QUEUE_MONITOR_INTERVAL=30
ENABLE_DATASETS_QUEUE_MONITOR=true
```

---

## 五、故障排查

### 5.1 常见问题

#### 容器启动失败

**症状**: 容器反复重启或无法启动

**诊断**:

```bash
# 查看容器状态
docker compose ps

# 查看日志
docker compose logs api

# 检查健康状态
docker compose exec api curl http://localhost:5001/health
```

**常见原因**:

1. **数据库连接失败**
   ```bash
   # 检查数据库
   docker compose exec db_postgres pg_isready
   # 验证连接
   docker compose exec api env | grep DB_
   ```

2. **依赖服务未就绪**
   ```yaml
   # 检查 depends_on 配置
   depends_on:
     db_postgres:
       condition: service_healthy
   ```

3. **环境变量配置错误**
   ```bash
   # 验证必需变量
   docker compose config | grep -E "SECRET_KEY|DB_PASSWORD"
   ```

#### 网络连接问题

**症状**: 无法访问外部 API 或内部服务

**诊断**:

```bash
# 测试 SSRF Proxy
docker compose exec api curl -x http://ssrf_proxy:3128 https://api.openai.com

# 测试内部服务
docker compose exec api curl http://redis:6379
docker compose exec api curl http://db_postgres:5432
```

#### 性能问题

**症状**: 响应慢、超时、资源耗尽

**诊断**:

```bash
# 查看资源使用
docker stats

# 查看数据库连接
docker compose exec db_postgres psql -U postgres -d dify -c "SELECT count(*) FROM pg_stat_activity;"

# 查看 Redis 内存
docker compose exec redis redis-cli INFO memory
```

📖 **详细文档**: [operations/troubleshooting.md](operations/troubleshooting.md)

### 5.2 故障恢复流程

#### 数据库故障

```bash
# 1. 检查状态
docker compose ps db_postgres

# 2. 查看日志
docker compose logs db_postgres

# 3. 重启服务
docker compose restart db_postgres

# 4. 验证连接
docker compose exec db_postgres pg_isready

# 5. 检查数据完整性
docker compose exec db_postgres psql -U postgres -d dify -c "SELECT count(*) FROM accounts;"
```

#### 服务重启顺序

```bash
# 1. 基础服务
docker compose restart db_postgres redis

# 2. 核心服务
docker compose restart api worker beat

# 3. 前端服务
docker compose restart web nginx

# 4. 验证
docker compose ps
curl http://localhost/health
```

📖 **详细文档**: [operations/backup.md](operations/backup.md)

---

## 六、最佳实践

### 6.1 安全最佳实践

1. **定期更新密钥**
   - 每 90 天轮换 SECRET_KEY
   - 使用密钥管理服务 (AWS KMS, HashiCorp Vault)

2. **最小权限原则**
   - 容器以非 root 用户运行
   - 数据库用户仅授予必需权限

3. **网络隔离**
   - 使用内部网络隔离敏感服务
   - 通过 SSRF Proxy 控制外部访问

4. **审计日志**
   - 启用详细日志记录
   - 定期审查访问日志和错误日志

### 6.2 部署最佳实践

1. **环境分离**
   - 开发、测试、生产环境独立
   - 使用不同的配置和密钥

2. **自动化部署**
   - 使用 CI/CD 流水线
   - 自动化测试和验证

3. **版本控制**
   - 配置文件版本化 (排除敏感信息)
   - 使用 Git 管理基础设施代码

4. **监控和告警**
   - 配置全面的监控指标
   - 设置合理的告警阈值

### 6.3 运维最佳实践

1. **备份策略**
   - 每日自动备份数据库
   - 定期测试恢复流程

2. **容量规划**
   - 监控资源使用趋势
   - 提前扩容避免性能问题

3. **文档维护**
   - 记录配置变更
   - 维护运维手册

4. **应急响应**
   - 建立故障响应流程
   - 定期演练恢复场景

📖 **详细文档**: [best-practices.md](best-practices.md)

---

## 七、配置模板

### 7.1 开发环境模板

```bash
# .env.development
DEBUG=true
LOG_LEVEL=DEBUG
MIGRATION_ENABLED=true

# 使用默认密码 (仅开发环境)
DB_PASSWORD=difyai123456
REDIS_PASSWORD=difyai123456

# 禁用 HTTPS
NGINX_HTTPS_ENABLED=false
```

### 7.2 生产环境模板

```bash
# .env.production
DEBUG=false
LOG_LEVEL=INFO
DEPLOY_ENV=PRODUCTION

# 强密钥 (必须修改)
SECRET_KEY=$(openssl rand -base64 42)
DB_PASSWORD=<strong-password>
REDIS_PASSWORD=<strong-password>

# 启用 HTTPS
NGINX_HTTPS_ENABLED=true
NGINX_SSL_CERT_FILENAME=fullchain.pem
NGINX_SSL_CERT_KEY_FILENAME=privkey.pem

# 启用监控
ENABLE_OTEL=true
API_SENTRY_DSN=<your-sentry-dsn>
```

### 7.3 高可用模板

```yaml
# docker-compose.ha.yaml
services:
  api:
    deploy:
      replicas: 3
      resources:
        limits:
          cpus: '2'
          memory: 4G
      restart_policy:
        condition: on-failure
        max_attempts: 3

  worker:
    deploy:
      replicas: 2
      resources:
        limits:
          cpus: '4'
          memory: 8G
```

---

## 八、参考资料

### 官方文档

- [Dify 官方文档](https://docs.dify.ai/)
- [Docker 部署指南](https://docs.dify.ai/getting-started/install-self-hosted/docker-compose)
- [环境变量参考](https://docs.dify.ai/getting-started/install-self-hosted/environments)

### 社区资源

- [Dify GitHub](https://github.com/langgenius/dify)
- [Dify Helm Chart](https://github.com/BorisPolonsky/dify-helm)
- [阿里云 ACK 部署实践](https://alibabacloud.com/blog/high-availability-and-performance-best-practices-for-deploying-dify-based-on-ack_601874)

### 相关 SKILL

- [01-workflow](../01-workflow/SKILL.md) - 工作流设计
- [02-plugin](../02-plugin/SKILL.md) - 插件开发
- [03-performance](../03-performance/SKILL.md) - 性能优化

---

## 快速命令参考

```bash
# Docker 部署
docker compose up -d                    # 启动所有服务
docker compose ps                       # 查看服务状态
docker compose logs -f api              # 查看 API 日志
docker compose restart api              # 重启 API 服务
docker compose down                     # 停止所有服务

# 健康检查
curl http://localhost/health            # 检查服务健康
docker compose exec db_postgres pg_isready  # 检查数据库
docker compose exec redis redis-cli ping    # 检查 Redis

# 日志查看
docker compose logs --tail=100 api      # 查看最近 100 行日志
docker compose logs -f worker           # 实时查看 worker 日志

# 数据库操作
docker compose exec db_postgres psql -U postgres -d dify  # 连接数据库
docker compose exec db_postgres pg_dump -U postgres dify > backup.sql  # 备份

# Kubernetes
kubectl get pods -l app=dify            # 查看 Pod 状态
kubectl logs -f deployment/dify-api     # 查看日志
kubectl describe pod <pod-name>         # 查看 Pod 详情
kubectl exec -it <pod-name> -- /bin/bash  # 进入容器
```

---

**版本**: 1.0.0
**最后更新**: 2026-03-04
**维护者**: Dify SKILL Team
