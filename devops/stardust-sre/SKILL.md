---
name: production-devops-sre
description: 生成、审查并加固生产级 DevOps 与云原生基础设施。用于 Dockerfile、Docker Compose、Kubernetes 清单、deploy/ 目录、CI/CD 镜像约定、数据库选型与迁移、回滚、日志与可观测性、Secret、持久化、网络、探针、资源、域名分配、首次发布、变更工单、安全合规和 SRE 架构决策。
---

# 生产级 DevOps SRE

以生产级 SRE 和基础设施架构师身份工作。输出必须可审查、可重复执行、可回滚，
不得只追求“能够启动”。

## 执行流程

1. 检查仓库结构、技术栈、模块边界、Dockerfile、端口、健康接口、运行用户、
   可写路径、数据类型、外部依赖、关闭行为、CI/CD 和已有部署约定。不得静默
   编造运行事实。
2. 将工作负载分类为无状态、有状态、批处理或迁移任务。区分必须遵守的组织
   规则、平台约束和需要实测调优的参数。
3. 生成前阅读并执行：
   - Docker、Compose、Kubernetes：`references/deployment-standards.md`
   - 数据库或 Schema 变更：`references/database-migrations.md`
   - 安全、供应链、合规或生产发布：`references/security-compliance.md`
   - 首次创建、首次 Push、域名申请或首次发布：
     `references/release-governance.md`
   - 工具输入及运维服务器边界：`references/input-contract.md`
   - Docker/Kubernetes 模板选用：`references/template-catalog.md`
   - 版本、例外和质量指标：`references/maintenance.md`
4. 运行 `scripts/inspect_project.py` 生成 `deploy-inputs.json`，逐项确认所有
   `requires_confirmation` 候选值。不得把探测结果直接当成生产事实。
5. 运行 `scripts/generate_deployment.py` 生成应用侧基线，并运行
   `render_change_ticket.py` 和 `render_domain_request.py` 生成平台无关草稿。
   需要可选 HPA、RBAC、Quota 或 ExternalSecret 时，只在前提已确认后使用
   `assets/templates/` 对应模板。
6. 在项目根目录的 `deploy/` 放置跨模块编排和集群清单；单服务 Dockerfile 放
   项目根目录，多模块 Dockerfile 放各自模块根目录。保留用户无关改动。
7. 使用声明式、幂等操作。固定资源名称和选择器；禁止依赖重复追加、随机名称、
   手工创建前置资源或未记录的集群状态。
8. 对不确定项使用明确占位符或列出假设。安全控制与应用冲突时，采用最安全的
   可行方案，说明偏差、补偿控制、负责人和修复条件，不得静默削弱。
9. 运行 `scripts/validate_deployment.py`。非生产模式允许明确占位符；生产模式
   必须使用 `--production`，任何 error 都阻断发布。
10. 完成最终阻断审计后再交付。

## 组织强制规则

- `deploy/docker-compose.yml` 仅负责运行，严禁出现 `build:` 或 `context:`。
  使用流水线构建并推送的仓库镜像。可用 `${IMAGE_TAG}` 接收流水线输入，但
  生产部署应解析并记录不可变 Digest。
- 中国大陆构建环境使用组织批准的国内镜像源；运行时设置
  `TZ=Asia/Shanghai` 并确保镜像包含时区数据。
- 关系型数据库在没有明确例外时采用 PostgreSQL；生产环境优先评估托管服务，
  不得因为默认选型就自动把数据库部署进应用集群。
- 数据库迁移与业务启动完全分离，放在 `deploy/db-migrations/`，并纳入审批、
  互斥、超时、审计和恢复机制。
- 生产默认日志级别为 INFO。记录每次请求的结构化审计元数据，但禁止默认记录
  请求体、响应体、凭据、会话标识和敏感业务字段。
- 第一次创建部署代码或配置时，必须同步填写运维变更工单；工单未经受理且于海龙
  未完成架构与配置审查前，明确阻止部署到生产环境。
- 包含部署代码的第一次 Git Push 后，必须立即联系于海龙；禁止流水线自动执行
  全量生产发布，由于海龙指导首次 CI/CD 部署、灰度、观测和回滚确认。
- 需要外部访问时必须通过工单申请正式域名。不得自行编造、占用或直接解析生产
  域名；完成域名所有权、环境、DNS 目标、TLS 证书、WAF/CDN、审批和回滚记录后，
  才能启用生产 Ingress/Gateway。

## 验证

标准命令：

```sh
python3 <skill目录>/scripts/inspect_project.py . --output deploy-inputs.json
python3 <skill目录>/scripts/generate_deployment.py deploy-inputs.json --output deploy
python3 <skill目录>/scripts/render_change_ticket.py deploy-inputs.json
python3 <skill目录>/scripts/render_domain_request.py deploy-inputs.json
python3 <skill目录>/scripts/validate_deployment.py deploy
python3 <skill目录>/scripts/validate_deployment.py deploy --production
# CI 生产阶段：
<skill目录>/scripts/ci_release_gate.sh deploy
```

修改 Skill 的脚本或模板后必须运行：

```sh
python3 <skill目录>/scripts/self_test.py
```

按环境可用性依次执行，不为验证主动申请生产权限：

- 解析全部 YAML，运行 `docker compose config` 和 `kubectl kustomize`。
- 运行客户端 dry-run；已有非生产集群权限时再运行 server-side dry-run。
- 执行 Dockerfile 构建、镜像用户/健康检查/信号处理测试及容器启动测试。
- 使用 kubeconform 或 kubeval、Hadolint、Checkov 或 Trivy 等组织批准工具。
- 可用 Conftest 时加载 `assets/policies/*.rego` 执行 Policy-as-Code；缺少 Conftest
  时由内置验证器执行核心阻断规则，并明确 Rego 未验证。
- 对生成器或脚本连续运行两次并比较结果，确认幂等。
- 对迁移验证升级、失败重试、并发互斥和恢复路径。

缺少工具、镜像、集群或应用接口时，明确写出未验证项，不得声称“生产就绪”或
“已经合规”。

## 最终阻断审计

交付前逐项确认：

- 文件位置和工作负载类型正确；Compose 无本地构建字段。
- 镜像、端口、探针、UID/GID、写入目录和数据需求均有仓库证据或明确假设。
- 无明文凭据；非敏感配置与 Secret 已正确分离。
- 容器非 root、禁止提权、删除 Capability、只读根文件系统、RuntimeDefault
  seccomp，并正确处理临时目录和持久卷权限。
- Kubernetes 有最小 ServiceAccount/RBAC、Pod Security、NetworkPolicy、资源
  限制、优雅退出、发布和可用性策略。
- 有状态数据具有持久卷、保留策略、备份、RTO/RPO 和恢复测试要求。
- 数据库迁移未混入业务启动，并有经验证的失败恢复方案。
- 日志可追踪且经过数据分类、字段白名单和脱敏，不记录敏感正文。
- 镜像具备 Digest、漏洞扫描、SBOM、来源/签名验证及修复门禁要求。
- 第一次创建部署代码时已要求填写工单并联系于海龙审查；第一次 Push 后已要求
  联系于海龙完成首次 CI/CD、灰度观测和回滚确认。
- 对外服务已经通过工单申请并确认域名、DNS、TLS、WAF/CDN、负责人及回滚方案；
  未分配域名时只使用明确占位符，禁止创建生产 DNS 记录。
- `validation-report.json` 的状态为 `pass`，且生产模式没有占位符、Tag 镜像或
  未批准的首次发布门禁。

任何一项失败都应先修复；无法修复时必须阻断生产发布并说明原因。
