---
name: architectrue
description: Production-focused GKE and GCP architecture partner for designing, optimizing, and implementing deployable cloud platforms. Use when tasks involve GKE platform design, API Gateway/Kong/Nginx traffic chains, Cloud Load Balancing, mTLS, Cloud Armor, multi-tenant architecture, CI/CD and Helm release workflows, observability, cost optimization, high availability, or architecture troubleshooting and handoff documentation.
---

# Architectrue

## Overview

Deliver practical, production-grade GKE and GCP architecture guidance.
Prioritize deployable steps, explicit trade-offs, and verifiable outcomes over theory.

## Execution Workflow

### 1. Discovery

- **Load this skill first** (`skill_view(name='architectrue')`) and scan the **Sub-Topic Skills** section below before exploring the user's knowledge tree for context. Each sub-topic has a `references/<topic>.md` + ready-made `templates/<topic>/*` — using them is faster and more consistent than re-deriving from scratch. If the task matches an existing sub-topic, open the reference and (for concrete tasks) reproduce the templates with placeholders filled in.
- **Cite a single source of truth.** When the user points at one canonical artifact (a script, a doc, a URL, a config) as the basis for the task, treat that one as the SOLE authority for naming defaults and assumptions. Do **not** mine adjacent files in the same knowledge tree as supplementary authorities — they often describe adjacent systems or out-of-date patterns and will produce silent conflicts. If you need additional context, ask the user which other doc is in-scope rather than guessing.
- **Reverse-engineering config for an existing system is a discoverable-template task, not a write-from-scratch task.** When asked "given FQDN X, what YAMLs do I need to add?", the workflow is: (a) load this skill, (b) find the matching sub-topic, (c) open the sub-topic reference, (d) fill in placeholders (`<TEAM>`/`<API>`/`<FQDN>`/`<LISTENER_SECTION>`/`<IMAGE>`) for the concrete instance, (e) apply + verify. Do not reconstruct the architecture from the user's other docs in the tree.
- Clarify ambiguous requirements before proposing solutions.
- Classify the request as architecture, networking, security, deployment, performance, or cost.
- Separate recommendations into immediate fix, structural improvement, and long-term redesign.
- Flag risky or over-engineered ideas and provide a simpler alternative.

### 2. Architecture Planning

- Propose a realistic Version 1 architecture first.
- Explain trade-offs across cost, performance, complexity, and operability.
- Prefer GCP native services before introducing third-party tooling.
- Provide a structured flow description for traffic and control-plane components.
- Label implementation complexity as `Simple`, `Moderate`, or `Advanced`.

### 3. Implementation

- Provide step-by-step deployment actions.
- Include concrete commands, YAML snippets, and config templates when needed.
- Explain the purpose of each critical step.
- Include validation checks, rollback paths, and release safety practices.
- Account for HA, rolling updates, PDB, autoscaling, quotas, and platform limits.

### 4. Optimization and Reliability

- Optimize for high availability and zero-downtime operations.
- Improve traffic behavior with retries, timeouts, and fault isolation.
- Tune resource utilization and cost efficiency.
- Strengthen boundaries with IAM, mTLS, Cloud Armor, and WAF controls.
- Define observability coverage for logs, metrics, alerts, and tracing.

### 5. Documentation and Handoff

- Produce a concise architecture summary.
- Provide reusable templates and troubleshooting checklists.
- Capture version upgrade considerations.
- Document future extension paths and technical debt follow-ups.

## Sub-Topic Skills (Architecture Cluster)

These narrow skills are absorbed into the `architectrue` umbrella. Load the main `architectrue` skill and scroll to the relevant subsection for the topic you need.

#### `no-sidecar-pattern` — Istio No-Sidecar Same Namespace Pattern
- **What**: Gateway + HTTPRoute + DestinationRule in same NS; Runtime NS only has Service
- **Key insight**: GKE Gateway (GCLB-based) and Istio Gateway API (Envoy-based) are different — all Gateway CRDs share the same Ingress Gateway Envoy pool; >200 Gateways risks OOM
- **Content**: Minimal working set (3 resources), ReferenceGrant cross-NS rules, one-to-one vs shared Gateway tenant models

#### `ple-environment-design` — PLE (Production-Like Environment) 隔离架构设计
- **What**: PRD/non-PRD isolation architecture, network segmentation, multi-tenant access risk control
- **Key insight**: "Use PRD network infrastructure" + "fully isolated from PRD" are contradictory; correct interpretation: reuse network **design** (topology/naming), not network **traffic** (independent VPC/subnet/IP)
- **Content**: 5-layer isolation pyramid (L7→L2), attack path matrix, GCP native controls (Org Policy/Firewall/IAM Conditional), recommended architecture diagram, verification checklist

#### `gke-policy-controller-vs-gatekeeper` — GKE Policy Controller vs OPA Gatekeeper 选型
- **What**: Decision guide for GKE Policy Controller (Google-managed Gatekeeper) vs upstream OPA Gatekeeper
- **Content**: Single-cluster vs multi-cluster considerations, constraint migration path, operational differences

#### `pod-certificate-design` — Pod 间证书设计（Local vs Team 域名证书）
- **What**: GKE Pod 间 mTLS 证书选型评估 — `*.aliyun.cloud.region.local` (Local CA) vs `*.team.appdev.aibang` (Team 域名证书)
- **Key insight**: Team 证书下沉到 Pod 层引入三重连锁问题：① DNS 语义冲突（K8s 原生 DNS 不解析外部 Team 域名，需 Split-horizon DNS）；② Egress 双向不匹配（内部 SNI vs 外部证书 SAN）；③ Header 控制能力衰减（证书越靠近 Pod，Gateway 层统一策略越难执行）
- **Content**: 两套证书体系对比（签发 CA/生命周期/自动化程度）、DNS 建模方案（Split-horizon/ServiceEntry）、Egress 映射关系、证书下沉 Header 控制衰减模型（Gateway 100% → 最终 Pod 30%）、评估总结矩阵
- **Reference**: `safe/ssl/docs/claude/pod-cert-replacement-evaluation.md`（13 维度评估报告）、`linux/dns/docs/external-internal-dns-separation.md`（DNS 架构设计指南，含集群内域名转换详解）

#### `gke-crd-upgrade-behavior` — GKE 升级后 CRD 保留行为
- **What**: GKE 集群升级后 CRD 和 CR 实例是否保留的判断框架
- **Key insight**: CRD 定义和 CR 实例存储在 etcd 中；GKE 升级是控制平面组件原地替换，不清空 etcd，不重置 CRD 定义；用户的自定义 CRD 升级后完整保留
- **Content**: 按 CRD 来源分类（K8s Gateway API / GKE Platform / Istio）的行为矩阵、ListenerSet 专项分析、Gateway 专项分析、升级前后验证命令清单
- **Reference**: `references/gke-crd-upgrade-behavior.md`（会话探索数据）

#### `gke-experimental-install-yaml-analysis` — Gateway API experimental-install.yaml 误 apply 风险
- **What**: 分析 `experimental-install.yaml` 文件内容（12 CRD + 2 ValidatingAdmissionPolicy），评估同事误 apply 到已有集群的风险
- **Key insight**: 文件中所有 CRD 均标记为 `experimental` channel，存在 `safe-upgrades` ValidatingAdmissionPolicy 阻止在 standard channel 集群上 apply；用户集群已有全部 CRD，重复 apply 无意义
- **Content**: 文件元信息、CRD 清单（standard vs experimental channel）、safe-upgrades Policy 阻止逻辑、channel 机制、GKE 升级影响判断、最佳实践
- **Reference**: `references/gke-experimental-install-yaml-analysis.md`（会话探索数据）

#### `k8s-gateway-timeout` — K8s Gateway API 超时配置
- **What**: ListenerSet 多租户架构下超时配置：HTTPRoute timeouts + DestinationRule trafficPolicy
- **Key insight**: HTTPRoute `timeouts` 是 Extended Support（非 GA）特性，实际以 DestinationRule `trafficPolicy.timeout` 为准；Envoy 默认超时 5s，多租户场景必须显式覆盖
- **Content**: HTTPRoute `timeouts.request` / `timeouts.backendTimeout` 字段定义、DestinationRule `{timeout, connectTimeout, connectionPool}` 完整示例、同 NS/跨 NS 场景配置、调试验证命令、9 项检查清单
- **Reference**: `references/k8s-gateway-timeout.md`（会话探索数据，含架构对齐用户实际目录结构）

#### `k8s-gateway-listener-tenant-api` — ListenerSet 租户 API 上线（4-YAML 最小集）
- **What**: 在已存在的 K8s Gateway API + ListenerSet 多租户架构下，给定 FQDN（如 `newapi.team1.appdev.aibang`）反推租户团队需要 apply 的最小资源集（Service + Deployment + HTTPRoute + DestinationRule），并提供 5 层验证流程
- **Key insight**: 脚本 `k8s-gateway-fqdn-minimax.sh` 探查的 5 段链路（HTTPRoute → ListenerSet → BackendRef → Service → Deployment）反向就是要 apply 的资源；FQDN 第 2 段 = tenant namespace；HTTPRoute parentRef 必须是 ListenerSet（不是 Gateway），否则绕过多租户隔离
- **Content**: 反向工程映射表（脚本链路 → YAML 资源）、7 个关键反推假设（ListenerSet 名/sectionName/hostname pattern/Gateway 命名空间/GatewayClass/TLS Secret）+ **#1 silent failure**: 缺 tenant NS 必备 label（ListenerSet.allowedRoutes.selector 强校验，HTTPRoute Accepted=False reason=`NotAllowedByListeners`）、4-YAML 模板（含 `appProtocol: http/https` 字段含义）、**5 种 cross-NS 引用 ReferenceGrant 决策矩阵**、**backend 协议 → DR tls.mode 决策矩阵**（HTTP→DISABLE / HTTPS 自签→SIMPLE+insecureSkipVerify / mesh mTLS→ISTIO_MUTUAL）、3-NS 布局在 tenant 阶段的视角（Service+Deployment+HTTPRoute 在 tenant NS、ListenerSet 在 abjx-listenerset-int、Gateway 在 abjx-gw-int）、5 层验证流程（资源就绪 → 集群内 curl → minimax 脚本探查 → 外部 HTTPS 流量 → 失败模式速查表）、7 个反模式（apply 后不查 status.parents 会漏掉 5/7 错配）、**"与既有 working example 对比"元模式**（部署新变体时显式列出 11 个维度的差异，避免复制时漏改）
- **Reference**: `references/k8s-gateway-listener-tenant-api.md`（反推模式 + 4-YAML 完整示例 + ReferenceGrant 决策表 + DR mode 决策矩阵 + 失败模式速查表）
- **Templates**: `templates/k8s-gateway-listener-tenant-api/{service,deployment,httproute,destinationrule}.yaml`（4 个 starter YAML，带 `<TEAM> <API> <FQDN> <LISTENER_SECTION> <IMAGE> <APP_PROTOCOL>` 占位符，DR 含 `tls.mode` 注释指导）
- **Concrete instance** (用户的 `gcp/` 仓库): `gateway-2.0/k8s-gateway/06-runtime/newapi-*.yaml` + `07-verify/tenant-namespace-newapi-team1-appdev-aibang.md`（HTTP backend 变体，可与同目录 `app-*` HTTPS backend 变体作对比）

#### `k8s-gateway-platform-install` — K8s Gateway + ListenerSet 多租户平台安装（7 阶段管线）
- **What**: 在 GKE 集群上从零搭建 K8s Gateway API + Istio minimal + ListenerSet 多租户基础设施的完整管线（区别于 `k8s-gateway-listener-tenant-api` 的"tenant 上线" 阶段；本子主题是 platform 阶段，给 tenant 提供可用的 Gateway + ListenerSet + Secret）
- **Key insight**: 安装顺序是强约束的——`gcloud container hub mesh disable` 必须先于 `kubectl delete crd`（managed CSM 的 Google fleet controller 30s 内重建 CRD）；卸载 ASM 时 `image: auto` 的 gateway deployment 会进入 `ErrImagePull` 中间态，**这是正常的**（sidecar injector 退出）不应阻塞；GAR 镜像推送需要 `gcloud auth configure-docker` credential helper 而非 `--dest-creds user:pass`（后者会被拒绝 403）；节点 SA 需显式 `roles/artifactregistry.reader` 即使开了 Workload Identity；e2-medium (940m allocatable CPU) 装不下 500m req × 2 istiod，**必须**降为 100m req/500m limit；ListenerSet apiVersion 在 K8s Gateway API v1.5.1 是 `gateway.networking.k8s.io/v1`（GA），**不是** v1beta1（一些过期文档会写错）
- **Content**: 7 阶段管线（00-prereqs → 01-platform → 02-namespaces → 03-gateway → 04-secrets → 05-listenerset → 06-runtime → 07-verify），bastion→cluster 网络路径（`gcloud get-credentials --internal-ip` 走私网 endpoint 解决 masterAuthorizedNetworks 白名单问题），GAR 镜像搬运（skopeo + auth-helper），跨 NS Secret 复制模式，3 NS 布局（`abjx-gw-int` Platform Gateway / `abjx-listenerset-int` ListenerSet / `110139-int` Tenant Runtime）vs 旧 2 NS 布局的差异
- **Reference**: `references/k8s-gateway-platform-install.md`（完整命令 + 9 项 pitfall 速查表 + 验证流程）

#### `same-project-psc-test-setup` — 同 project PSC NEG 测试链路（典型 POC 场景）
- **What**: 仅有一个 GCP Project 时测试 PSC NEG 模式（Tenant/Producer 都在同一 project + VPC）的实施指南；包含 4 种 workarounds 和 9 个 operacional gotcha
- **Key insight**: **Regional `EXTERNAL_MANAGED` Backend Service 不能 attach 跟它同 project + 同 VPC 的 PSC NEG**（GCP 错误: "EXTERNAL MANAGED Backend Service in scope REGION can not use Private Service Connect network endpoint group that is in producer network and targets Service Attachment"）— 这是 PSC 的设计目的（cross-project 边界）决定的，但常被忽视。**4 种 workaround**: 2-VPC variant(consumer VPC + producer VPC)、跳过 PSC 直接挂 MIG backend、GKE Standalone NEG、"假装不同 network"。
- **Content**: 限制详细说明 + 4 种 workaround 对比表;9 个 operacional gotcha(no-address MIG 需要 Cloud NAT 才能 apt-get / regional MIG 必须 `--instance-group-region` 而非 `--zone` / PSC NEG backend service **不能**有 health check / Cloud Armor rate-limit rule 需要 `--conform-action`+`--exceed-action` / `--ip-version=IPV4` 不被 regional address 接受 / `--enable-proxy-protocol=false` 报 "ignored" / "default network not found" 错误往往是 backend service 损坏的连锁信号);Cert+key 配对必须用 **modulus** 比较而非 byte-equal(PKCS#1 vs PKCS#8 PEM 头差异);Python stdlib HTTPS server 配方(socketserver.ThreadingMixIn 而非 http.server.ThreadingMixIn)绕过 apt 限制;IAP SSH 到 MIG VM 需要新 firewall rule 覆盖 MIG tag
- **Reference**: `references/same-project-psc-test-setup.md`(9 个 gotcha 详解 + Python HTTPS server 完整代码 + IAP bastion 调试 pattern + 7 步验证命令序列)
- **Reference**: `references/same-project-psc-2vpc-worked-example.md`(补充: 7 个 2-VPC 实操 gotcha — backend service `protocol=HTTP`、Cloud Armor 必须是 regional scope、producer VPC 需要 `10.0.0.0/8` internal firewall、`--network=` 显式 flag for forwarding rule、PSC NEG `balancing-mode=RATE` 不支持、PSC NEG data-plane status None 是正常的;含 2-VPC 完整 4 phase 命令序列 + e2e 验证 + reverse-order cleanup)
- **Templates**: `templates/same-project-psc-test-setup/python-https-server.py`(canonical Python stdlib HTTPS server, HTTP 80 + HTTPS 443, daemon-threaded, modulus-verified cert+key at startup) + `tenant-server.service`(systemd unit file, Type=simple + Restart=always) + `firewall-iap-ssh-mig.yaml`(IAP-SSH-to-MIG firewall rule 模板) + `setup-2vpc-public-ingress.sh`(4 phase idempotent end-to-end setup, 2-VPC variant) + `verify-2vpc-public-ingress.sh`(3-layer verify: resource existence + associations + real HTTPS traffic) + `cleanup-2vpc-public-ingress.sh`(reverse-order teardown)

#### `cross-project-psc-architecture` — 跨项目 PSC NEG 架构（Tenant/Producer 拆分）
- **What**: 跨 GCP Project 部署 GLB 入口（A Project = Tenant，作为 PSC Consumer）+ B Project = Producer（暴露 Service Attachment）。适用于多团队服务共享、租户隔离、producer 控 consumer 访问权限等场景
- **Key insight**: **PSC NEG 是 regional → 整条 LB 链必须 regional**。一旦 backend service 引用了 PSC NEG，整条链路（backend service / URL map / target proxy / forwarding rule）必须用 `--region=...` 而不是 `--global`，`--load-balancing-scheme=EXTERNAL_MANAGED`。**Regional External HTTPS LB 强依赖 proxy-only subnet**（`purpose=REGIONAL_MANAGED_PROXY, role=ACTIVE`），缺这个 subnet 创建 forwarding rule 报 `requires a proxy-only subnet`。**关联资源必须显式传 -region**：`--url-map-region` / `--target-https-proxy-region` / `--address-region` 不传则 gcloud 默认找 global 资源。**Shared VPC IAM 粒度陷阱**：PSC NEG 指定 `--network` 触发 network 级 IAM 校验，subnet 级授权环境下只指定 `--subnetwork` 才能通过。**Consumer subnet 不需要 `PRIVATE_SERVICE_CONNECT` purpose**（与 Producer 的 PSC NAT subnet 相反）
- **Content**: Tenant/Producer 拆分架构图，13 类资源 checklist（9 regional + 1 global 证书 + 1 global Cloud Armor + 2 Host Project subnet），4 个高频 gotcha（proxy-only subnet / explicit --region / Shared VPC IAM / Service Attachment approve），与 `refer-lb-create.sh` 的反推工作流（先在有 MIG 的 reference project 跑出 POC，抄 port-name / hc 协议 / named port 再回到 Tenant 脚本）**+ 4-Way LB 决策矩阵**（Public/Internal × Global/Regional，公开 Org Policy + PSC NEG 双约束下 C/D 不可行的明确解释）+ **Global Access 两个 flag 区别表**（`--allow-global-access` 在 Producer 侧 ILB vs `--allow-psc-global-access` 在 Consumer 侧 PSC Endpoint，PSC NEG 场景只用前者） + **双模式 (Public/Internal) 脚本模板 6 个**（create/verify/cleanup × A/B scheme 通过 `LB_SCHEME` 切换，10/13 资源共享，只 3 个有差异）
- **Reference**: `references/cross-project-psc-architecture.md`（4 大 gotcha 详解 + 验证诊断命令 + 资源依赖图 + 与 `cross-project/psc-firewall.md` 的协同关系）
- **Env application**: `references/cross-project-psc-environment-aibang.md` — 用户 `aibang-12345678-ajbx-dev` 项目（europe-west2 / dev-lon-cluster-xxxxxx GKE / IAP-tunneled bastion dev-lon-bastion-public）的具体实施：12 类资源、3 个幂等脚本（setup/verify/cleanup）、CIDR 规划（避开 GKE 节点 192.168.64.0/20、Core 192.168.0.0/18）、bastion 工作流（私有 GKE 节点 + master-global-access → 必须从 bastion 跑所有 gcloud，本地 TLS handshake timeout）
- **Templates**: `templates/cross-project-psc-architecture/{create,verify,cleanup}-tenant-lb.sh`（3 个可执行 starter，幂等检查 + 逆序删除 + 资源 + 流量双层验证）
- **Templates**: `templates/cross-project-psc-architecture/{create,verify,cleanup}-public-internal-lb.sh`（3 个可执行 starter，**双模式** 通过 `LB_SCHEME` 环境变量切换 Public/Internal 模式，处理 Cloud Armor 绑定 + proxy-only subnet purpose 迁移逻辑）
- **Reference**: `references/cross-project-psc-architecture.md`（5 大 gotcha 详解 + 验证诊断命令 + 资源依赖图 + Two-Mode 对称模式 + 与 `cross-project/psc-firewall.md` 和 `gcp/ingress/public-ingress/public-ingress-tenant-project-psc.md` 的协同关系）

#### `cross-vpc-psc-ilb-https-tls` — Cross-VPC PSC NEG + Producer ILB 二次终结 TLS (L7 HTTPS)
- **What**: Variant of `cross-project-psc-architecture` where the **Producer ILB itself terminates TLS** (L7 HTTPS, port 443) instead of plain HTTP pass-through. Result: every cross-VPC / cross-network hop is TLS-encrypted; only the final ILB→MIG intra-VPC hop is HTTP. Same TrustAsia cert is reused for both the consumer GLB and the producer ILB (same SAN).
- **Key insight #1 — BS `get-health` output mixes 2 independent things**: `port: 80` in get-health = **traffic port** (from `portName=http` → 80 on MIG), NOT the health check port. The HC is a separate config (`ajbx-tenant-vpc-internal-https-hc`, HTTPS :443) whose RESULT shows as `healthState: HEALTHY/UNHEALTHY`. The user's one-sentence summary: "get-health 里的 port: 80 告诉您：如果现在有用户流量来，ILB 会往实例的 80 端口 转发；同时，该实例的可用性是由在 443 端口 跑的 HTTPS 健康检查保障的。" Without this distinction, people read "port 80" as "HC is broken" or "HTTPS requirement violated" — both wrong.
- **Key insight #2 — The 3 TLS hops are NOT "Client→GLB, GLB→BS, BS→ILB"**: the correct 3 terminations are at (1) GLB for Client→GLB, (2) GLB again for re-encryption to BS, (3) ILB for SA→ILB. BS→ILB is NOT one TLS hop — it's BS→NEG (HTTPS, since BS protocol=HTTPS) → NEG→SA (PSC tunnel, GCP-managed) → SA→ILB (TLS 3 terminated at ILB). The "BS→ILB" framing hides the PSC tunnel mechanism and confuses the architecture.
- **Key insight #3 — LB family + PSC NEG compatibility** (answers "do I need `GLOBAL_EXTERNAL_MANAGED_HTTP_HTTPS`?"): the classic `EXTERNAL` LB (deprecated) does NOT support PSC NEG, but **all `*_MANAGED` variants do** — including Regional external ALB (`EXTERNAL_MANAGED` regional), which is the most common choice. `GLOBAL_EXTERNAL_MANAGED_HTTP_HTTPS` is only needed if you want Global scope; Regional external ALB is unaffected by that Org Policy. The user's original assumption that "I must enable GLOBAL_EXTERNAL_MANAGED_HTTP_HTTPS" was wrong — they were already running Regional external ALB successfully.
- **Key insight #4 — Proxy-only subnet purpose types are NOT interchangeable**: `INTERNAL_HTTPS_LOAD_BALANCER` is for the deprecated classic `EXTERNAL` LB. `REGIONAL_MANAGED_PROXY` is for all `*_MANAGED` LBs (Regional external, Global external, Regional internal). The Console "needs to be migrated from `INTERNAL_HTTPS_LOAD_BALANCER`" warning only applies to old subnets; fresh subnets for `*_MANAGED` LBs use `REGIONAL_MANAGED_PROXY` and need no migration.
- **Key insight #5 — v2-over-v1 doc self-containment pattern**: when documenting v2 changes (e.g., upgrading from HTTP backend to ILB-terminated TLS) on top of a v1 doc, the v2 doc's §0 resource tables should list **ALL** resources (v1 unchanged + v2 new/recreated/updated) with a "状态" column showing v1已建 / v2新建 / v2重建 / v2update — colleague should be able to recreate the entire system from this one doc without cross-referencing v1.
- **Content**: Backend Service get-health output semantics (port 80 ≠ HC port), the 3 actual TLS hops (and why "BS→ILB" is wrong), LB family + PSC NEG compatibility matrix, proxy-only subnet purpose types, the 5 most common confusions refuted, v2-over-v1 doc resource table template, 4 gotchas to watch for in this variant
- **Reference**: `references/cross-vpc-psc-ilb-https-tls.md`（BS get-health 输出语义 + 3 TLS 跳真实路径 + LB 家族与 PSC NEG 兼容性矩阵 + proxy-only subnet purpose 类型 + 5 个常见误解反驳 + 资源表 self-containment 模板 + 4 大 gotcha）
- **Concrete instance** (用户的 `gcp/ingress/public-ingress/` 目录): `tenant-tls-setup-https.md` (v2 文档, 893 行) — Producer ILB 用 L7 HTTPS 终结 TLS, BS protocol 改 HTTPS, 复用 TrustAsia cert, e2e `curl https://tenant.taobao.abjx.uk/` → HTTP/2 200。配套 v1 文档 `tenant-tls-setup.md` 保留为 HTTP backend 变体的对照。
- **Concrete instance** (用户的 `gcp/ingress/public-ingress/` 目录):
  - `public-ingress-tenant-project-psc.md` (1468 行) — 通用 4 方案对比矩阵 (Public/Internal × Global/Regional) + 13 类资源全清单 + 4 大 Org Policy 限制的 sidestep 论证 + Cloud Armor 绑定矩阵 + 3 个幂等脚本
  - `public-ingress-external-https-lb.md` (1160 行) — 本环境特化 Plan A: `aibang-12345678-ajbx-dev` project / `europe-west2` region / GKE `dev-lon-cluster-xxxxxx` / 堡垒机 `dev-lon-bastion-public` (IAP tunnel); 复用 `cinternal-vpc1-europe-west2-abjx-core` (192.168.0.0/18) 作 Consumer Subnet,新建 `cinternal-vpc1-europe-west2-abjx-proxy` (192.168.96.0/24) 作 Proxy-only Subnet(刻意避开 GKE 节点 192.168.64.0/20 和 Master 192.168.224.0/28);包含 12 个真实 gcloud 命令 + 模拟输出
- **Templates**: `templates/cross-project-psc-architecture/{create,verify,cleanup}-tenant-lb.sh`（3 个单模式 External 入口 starter）+ `{create,verify,cleanup}-public-internal-lb.sh`（3 个双模式 Public/Internal starter，通过 `LB_SCHEME` env var 切换，含 Gotcha #5 迁移逻辑和 Cloud Armor 绑定，幂等检查 + 逆序删除 + 资源 + 流量双层验证）

## Response Contract
- Use direct language when identifying unnecessary risk.
- Avoid abstract explanations without actionable deployment value.
- Assume production environment unless explicitly told otherwise.
- Prefer maintainable and scalable designs over one-off hacks.
- Ensure each recommendation is deployable or verifiable.

## User workflow preferences (Lex's profile)

When the user says **`继续`** / **`你直接开干`** / **`不要再停`** / **`不要做任何操作`** / **`如果这个没有问题那么就走后面的步骤`**, treat these as conditional green lights:
- **`继续` or `你直接开干`**: just execute the next step, don't re-ask for permission or re-confirm
- **`不要做任何操作`**: stop completely and wait (different from `继续`!)
- **`如果 X 那么就 Y`**: pre-validate X, then execute Y, then report (no need to ask for confirmation between)
- Avoid asking "should I proceed?" mid-flow when the user already said continue; report after action

When the user expresses a preference for concise output, prefer a short "**Status: ✓ / ✗**" header over long explanations. When they ask why a step is needed, give a 1-2 sentence answer, then continue executing.

## Output Template

Use this outline when giving a full solution:

1. Goal and Constraints
2. Recommended Architecture (V1)
3. Trade-offs and Alternatives
4. Implementation Steps
5. Validation and Rollback
6. Reliability and Cost Optimizations
7. Handoff Checklist
