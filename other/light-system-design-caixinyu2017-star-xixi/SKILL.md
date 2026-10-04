---
name: light-system-design
description: 后端系统设计与数据库能力。当任务涉及系统架构、数据库设计、接口设计、权限/日志/异常/性能/部署时使用。设计 ER 图、数据表结构、接口文档、用户权限、数据流转、模块划分、API 规范、数据库索引、安全策略、部署方案，尤其适合科研系统、管理系统、数据分析平台、可视化平台、竞赛作品与软著项目。
user-invocable: false
---

# 后端系统与数据库设计

## 适用场景
科研系统、管理系统、数据分析/可视化平台、竞赛作品、软著申请项目。设计要既能落地(交 a03 实现)又能写进软著/论文(交 m15/m07)。

## 系统架构
- 模块划分(分层：接口层/业务层/数据层)、职责边界、数据流转图。
- 技术选型按需(见 a09，各框架起手式/分层/配置见 references.md)：**FastAPI**(路由+Pydantic 校验+`Depends` 注入+`/docs` Swagger)、**Django REST**(serializer+ModelViewSet+Router，`REST_FRAMEWORK` 集中配)、**Spring Boot**(`@RestController→@Service→@Repository` 分层+构造器注入+多 profile)。
- 非功能性：性能(缓存/索引/分页)、可扩展、可观测。
- **向量检索选型**（科研 RAG/语义检索常用）：百万级以内优先 **pgvector + HNSW**（一套 Postgres 管关系+向量，运维简单），算子类与查询距离要一致（cosine→`vector_cosine_ops`）；千万~亿级、高 QPS 或需分布式才上专用向量库（Milvus/Qdrant/Weaviate）。选型对照见 references「pgvector + HNSW」节。
- **可观测**：科研 AI 服务用 **OpenTelemetry** 统一采 trace/metric/log（`opentelemetry-instrument` 零改代码自动埋点，OTLP 导出到 Jaeger/Prometheus），定位"一次推理耗时花在哪、哪步报错"，别用 print 调试；注意采样率与别把密钥/PII 写进 span。详见 references「OpenTelemetry」节。

## 数据库设计
- **ER 图**：实体、关系、基数。可用 `scripts/er_diagram.py` 把表结构定义（YAML/JSON：entities + columns(PK/FK/UK) + relationships(基数)）一键转成 Mermaid `erDiagram` 文本，粘进 Markdown/软著文档或 mermaid.live 预览（`python scripts/er_diagram.py --in schema.yaml`，纯离线）。**需要更强表达力/可编辑矢量源/纳入 Git 版本控制**（复杂 ER、系统架构图、分层图、数据流转图，尤其软著功能说明/论文系统描述用的正式图）时，用 **Draw.io MCP**（diagram-as-code，官方 jgraph/drawio-mcp，`.drawio` 即 XML 可程序化生成与版本管理，导出 PNG/SVG/PDF）——比 Mermaid 排版更可控、可反复改稿（配置见 README 推荐 MCP 表，规划走 m09 figure-planning）。
- **表结构**：字段、类型、约束、主外键、范式 vs 反范式权衡。刻意选型，别无脑 text/超大 numeric。
- **索引**：按查询模式选型——B-Tree(等值/范围/排序/前缀 `LIKE 'x%'`)、GIN(数组/JSONB/全文/trigram)、BRIN(超大表+物理有序时间列)、GiST(几何/最近邻)、Hash(纯等值)。**外键必须建索引**(最常见漏建)；生产建索引用 `CREATE INDEX CONCURRENTLY` 避免锁表；上线前 `EXPLAIN ANALYZE` 验证计划。
- **迁移**：Alembic `revision --autogenerate` 生成后**必须人工审**（检不出重命名/匿名约束，报成 drop+add），`upgrade head` 应用，CI `alembic check`；Prisma 开发 `migrate dev`、**生产只能 `migrate deploy`**（不 reset/shadow DB），手改 SQL 用 `--create-only`。
- **ORM 防 N+1**：SQLAlchemy 用 `selectinload`(二次 IN 查询)/`joinedload`(JOIN) 预加载；DRF 用 `select_related`/`prefetch_related`。连接必须用连接池。
- 最佳实践参考 supabase-postgres-best-practices(下方安全段含 RLS 具体写法、命名规范)。

## 接口设计
- RESTful/OpenAPI 3.x 规范：顶层 `openapi`/`info`/`servers`(完整 base URL，版本化放 `/v1`)/`paths`/`components`。
- 资源命名、方法、状态码(201 Created/204/4xx)、版本化。
- 请求/响应 schema 放 `components.schemas` 用 `$ref` 复用；`securitySchemes` 定义 bearer/oauth2。
- 错误码体系、分页(游标优先于大 OFFSET)/过滤/排序约定。
- 接口文档可导出：FastAPI `/openapi.json`、DRF/Spring 均可自动产出 OpenAPI；手写时别漏 error 响应码与示例。

## 安全与运维
- **权限**：认证(JWT/session)+授权(RBAC)；最小权限原则。
- **行级安全(RLS)**：多租户表 `enable row level security` + 显式 policy，别只靠应用层 WHERE；性能上函数包进 `select` 触发 initPlan 缓存、policy 引用列建索引、永远写 `to` 子句、复杂跨表用 `security definer` 函数；授权数据用 `raw_app_meta_data`（用户改不了）。骨架与写法见 references「supabase RLS」段。
- **缓存(Redis)**：Cache-aside(查缓存→未命中读 DB→写回带 TTL)；`maxmemory-policy` 默认 `allkeys-lru`；TTL 加随机抖动防雪崩、空值缓存防穿透；监控命中率与 `evicted_keys`。
- **日志**：分级日志、请求追踪、审计日志。
- **异常处理**：统一异常响应、不泄露内部细节。
- **安全策略**：输入校验、防注入、限流、密钥管理(不入库/不硬编码)。
- **部署**（完整配置/骨架见 references.md 与 `templates/ci.yml`）：Docker 多阶段构建、依赖清单先于源码护缓存、非 root + slim/distroless + 钉 digest；K8s Deployment+三探针(readiness/liveness/startup)+requests/limits+HPA、Secret 配 RBAC；Nginx 反代透传 XFF/TLS 终止/`limit_req`、改配 `nginx -t` 后 reload；CI(Actions) checkout→install→lint→test→`alembic check`/`migrate deploy`，最小权限 `contents: read`、回滚 `kubectl rollout undo`。
⚠ 网络暴露服务若无鉴权必须主动提示(security_awareness)。

## 产出
架构图 + ER 图 + 表结构 DDL + 接口文档(OpenAPI) + 权限/安全/部署说明。设计文档可直接喂 m15 软著功能说明。起手骨架见 `templates/`(schema.sql / openapi.yaml / rls_policy.sql / ci.yml)，按项目改字段即可。

## 衔接
设计→a03 实现→a06 规整目录；与论文系统描述、软著材料保持一致(a07)；版本入 db09。

> 各工具真实端点/语法/配置/已知坑见 references.md（逐工具核查笔记）。
