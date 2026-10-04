---
name: observability-standard
version: 1.3.2
description: 生产级可观测性规范,**所有后端服务**通用(普通微服务与 agent / 多 agent / RAG 项目;Python / Go / Java / Rust)。核心:trace_id 串 trace/log + 业务 id 反查 db、结构化日志、OpenTelemetry 埋点与跨进程传播、日志级别与边界类型纪律;agent / RAG 在此基线上加 LLM / 工具 / 检索埋点(GenAI 语义约定)。Use whenever writing or reviewing backend code involving logging, tracing, structured logs, context propagation, log levels, log/trace/db correlation, boundary types — or agent orchestration / sub-agents, LLM / tool / retrieval calls. 用户只说"加点日志" "接一下 trace / instrument this" "set up observability" "这个错误怎么查不到" "这个请求怎么追踪"也适用,不限于显式提到规范时。
---

# 可观测性与工程规范

## 何时应用
写或评审**任何后端服务**的代码时应用 —— 普通微服务(auth / 网关 / 业务服务)与 agent / 多 agent / RAG 知识库项目一视同仁,尤其涉及:日志接入、OpenTelemetry 埋点、跨进程 context 传播、日志级别选择、跨 trace/log/db 排障、边界数据建模;**agent 场景额外**涉及编排与子 agent、LLM/工具/检索调用。Python / Go / Java / Rust 通用。即使用户只说"加点日志""接一下 trace""这个错查不到""这请求怎么追",也按本规范做。

## 总纲
**用一条关联主线贯穿定位**:`trace_id` 串起 trace + log;业务库这一环靠**业务 id 同时挂成 span 属性(`order.id` / `run.id`)**双向关联,**不在业务行存 `trace_id`**(trace 受采样 / 短保留,持久行存它多半是死指针 —— 见 references §2.1)。定位永远是
`trace 或业务 id → 查 trace 看哪步 → 查 log 看为什么 → 按业务 id 查 db 看数据对不对`,不靠时间戳猜。

## 五条铁律(所有服务,全部遵守)
1. **一次对外请求 = 一棵 trace**。入站请求 handler 是 root span,所有下游(DB / 缓存 / 跨进程调用 —— agent 场景下还有子 agent / LLM / 工具 / 检索)都是子 span。
2. **宽事件优先**:每步一条富字段结构化事件;事件名是稳定可聚合标识符,变量进字段;不写散文。
3. **三信号可关联**:每条 log 带 `trace_id`+`span_id`(随 trace 同采样 / 保留);**业务 id 挂成 span 属性**以按业务 id 反查 trace,**不往业务行加 `trace_id` 列**;需持久溯源处(AI 决策 / 金额 / 对客输出 / 合规)落自己拥有的 `correlation_id`,优先进专用审计 / outbox 表(见 references §2.1)。
4. **跨进程必传播 W3C `traceparent`**(HTTP / gRPC / 消息队列 / 任何 agent 协议都算)。不传 = trace 断成多棵互不相连的树 = 跨服务定位失效。**优先级高于功能**。
5. **标准在边界 + 后端无关**:跨进程 / 对外响应遵守 OTel 语义约定 + 类型校验(LLM 边界额外遵守 GenAI 约定);内部自由。**只依赖 OTel API/SDK + OTLP,应用代码不 import 厂商 SDK(Langfuse / Datadog 等);标准组件优先用官方 auto-instrumentation 自动埋点,手写 span 只补领域环节;厂商差异只在 Collector / exporter 配置层 → 换后端不重埋(见 references §1 铁律5 / §5.0 / 附录 C)。**

## 日志铁律
- 结构化优先:`event_name + fields`,**绝不字符串拼接**。日志即数据,不即叙事。**宽事件 ≠ JSON**:稳定可解析的行式字段格式即可,不强制 JSON 序列化(有实打实的计算开销;日志管道需要机器解析时再升,升级只动导出层配置)。
- 日志在活跃 span 内打出,`trace_id`/`span_id` 自动注入;**没有 `trace_id` 的 ERROR 视为 bug**。
- 上下文绑一次贯穿全程(语言原生 ambient context 机制,见 references 附录 B),不手传。
- 不要 log-and-throw;密钥/PII/客户机密在边界脱敏;**明文 prompt/completion = 数据披露闸**(显式 flag + 非 prod + 脱敏;audit 仅哈希),非日志级别。
- 统一 named logger 树(语言原生 per-module logger 机制,见 references 附录 B),级别由配置控,**不用环境变量单独门控某条日志**。
- 必记(≥ INFO):决策点 + 依据、状态转移、每次跨进程 / LLM / 工具 / 检索调用的边界与结果状态、重试/回退/降级/补偿、每步 token + 成本(agent 场景)。

## 日志级别判据
判据:**这条日志在正常生产运行里读它有意义吗?** 有 → `INFO`;只有出问题深挖才看 → `DEBUG`。
- `INFO` 重建"发生了什么"的骨架(每步 / 每次调用 / 每次状态转移一条,**不刷高频内循环**)。
- `DEBUG` 重建"为什么"的细节(完整 prompt、推理、原始响应、命中 chunk、跨进程报文全文),**生产默认关、可按 trace 动态开**。
- `ERROR` = 失败且影响本次结果,必带 trace + 操作 + 输入标识符 + 栈;`WARNING` = 降级但请求继续。
- 排障时"光看 INFO 不知走到哪步" → **补 INFO,别常开 DEBUG**。
- **span 导出日志不是应用日志**:trace 信号走 OTLP;console/logging 型 span exporter(各语言 OTel SDK 均有)仅 dev 验证用,部署环境把其 logger 类别阈值默认压到 `WARN`(此类行每请求复述一条且无请求上下文,是双写噪音)。
- **环境三档矩阵(默认形状)**:**dev = DEBUG(代码内默认,开发就近调试)· staging = DEBUG(部署层配置开)· prod = INFO 骨架(默认安静侧)**;span 导出行随档位:dev/staging 可见、prod 隐藏。
- **配置分工**:语义级别(哪条算 INFO/DEBUG)归**代码**且默认取安静侧;级别阈值按环境开归**部署层运行时配置**(rationale 与各语言机制见 references §4);prod 静音 span 导出前确认已有真 OTLP sink,否则 trace 信号整体丢失。

## 要开的 span
### 核心(所有服务)
- 入站 **server span**(root,带 `trace_id`,并把**业务 id**挂成 span 属性(`order.id` / `run.id`)→ 供按业务 id 反查 trace),出站 **client span**(每次跨进程调用,**先开 span 再传 `traceparent`**),DB / 缓存 / 外部 API 子 span。`tenant.id` 是非标准 custom span/log 属性,仅在确有并已验证真实业务 tenant 时写;共享后端、产品名、环境或 K8s namespace 均不构成 tenant。
- 服务 OTel Resource 必须有 `service.name` + `service.version`;`service.version` = 当前部署的 release / image tag(例 `20260709-1020-c28e8f2`),用 `OTEL_RESOURCE_ATTRIBUTES=service.version=20260709-1020-c28e8f2` 注入。值必须非空、非 placeholder、与部署 tag 一致。tag 只标识 deployed artifact,不代替动态 effective-config snapshot。
- Resource identity 分层:`service.namespace` = 稳定逻辑系统分组,`deployment.environment.name` = 部署环境,`k8s.cluster.*` / `k8s.namespace.name` = 运行位置;三者不得互相代替或冒充 tenant。应用/部署合同拥有稳定 service identity,Collector 只补运行时属性且不得覆盖已声明身份(完整 ownership 见 references §5.0)。共享 OTLP/SigNoZ 只共享存储与查询面,不提供安全租户隔离。
- 这三类基线 span **优先用官方 auto-instrumentation(自动 / 零代码)产出**(HTTP / gRPC / DB 驱动 / 框架中间件;包见 references 附录 C),手写 span 只补领域环节(下方 agent / LLM / 工具 / 检索)。

### Agent / RAG 扩展(在核心基线上加)
- agent:workflow/agent/tool 用 `gen_ai.operation.name=invoke_workflow|invoke_agent|execute_tool`;模型 inference span 用真实 API operation(`chat` / `generate_content` / `text_completion`),**不是** `inference`。核心字段用 `gen_ai.provider.name`、`gen_ai.request.model`、`gen_ai.usage.*_tokens`、`gen_ai.response.finish_reasons`;prompt 版本用 `gen_ai.prompt.name` / `gen_ai.prompt.version`;tool id 用 `gen_ai.tool.call.id`。`gen_ai.conversation.id` 仅写真正 conversation/thread id,不得拿 trace/request/hash 顶替。GenAI 当前为 Development,按 pinned oracle 校验,不要把 custom 字段称作 OTel 标准(见 references §5.1)。
- 组织级 custom 字段必须由 profile extension 声明:低基数字段钉 allowlist + 长度,跨 span 关联 id 钉同 trace 一致性且不得进 metric label;公共 profile 不内置任何公司/项目 namespace。
- **工具调用 envelope**:稳定 `tool_call_id`(**不复用框架 run_id**)、start+finalize 完整生命周期(别永停 `running`)、`tool_status` 枚举 + `error_type`/`duration_ms`。完整字段见 references §5.1。
- **RAG 额外**开 `embedding` + `retrieval` span,记 query / top-k / 命中 chunk 的 **id+score** / 最终进上下文的 chunk id;**答案要可溯源到 chunk**。
- 仅当所用 instrumentation 仍需旧版迁移开关时设 `OTEL_SEMCONV_STABILITY_OPT_IN=gen_ai_latest_experimental`;升级时按 pinned oracle 复核,不得把 `latest` 当稳定契约。
- LiteLLM Proxy 新接入只选 OTel V2;V1/V2、generic OTLP/vendor preset 与 custom callback 不得重复产同一 inference span。generation span 必须挂当前 domain/invocation span;async worker/callback/poller/streaming 捕获并恢复 context。streaming 只有完整消费才 success,early close/cancel/provider error 分别终结且必须有 conformance 证据(见 references §5.1)。
- 明文 model I/O 放开只走**显式 profile 版本**,永不由运行时开关绕过:oracle 按 `schema_version` 闭集分派(v2 带 content 段 = profile invalid,v3 缺任一子键 = profile invalid,未知版本红),V2 对任何 content key 无条件 fail-closed。`references/conformance-profile-v3.json` 是受控通道:三条件同时成立才放行——运行时 `content_capture_allowed=true` + `deployment.environment.name` 命中环境**白名单**(prod 别名如 `live`/`prd`/带空白值一律红)+ redaction probe 自证(canary 必须像它代表的密钥/邮箱、产出与 canary 1:1 等长非空、canary 不出现在产出**也不出现在被 capture 的内容里**);`audit_records` 子树的字符串叶值必须是哈希或声明的短元数据键(别名字段装明文即红)。gate 判的是 snapshot 级证据自洽,不代替产品仓自己证明 redactor 真接线(形态契约见 references §3 铁律 7)。
- 持久化执行(Temporal/DBOS/Restate/自建)恢复时会丢 trace context,须持久化 `traceparent` 并重建。

## 类型纪律
边界锁结构、运行期校验;ID 用专名类型不混用;状态/角色用枚举式类型;**跨进程失败建模成结果类型**(序列化后异常栈必丢),别靠异常穿透;边界模型尽量不可变。**持久化纪律:只存自己拥有的业务 id / `correlation_id`,不把 ephemeral `trace_id` 当业务行外键**(trace 受采样 / 短保留;需 trace_id↔request_id 映射时用带 TTL 的轻量关联索引或 log,不污染业务热表)。各语言地道写法见 references §2 附录,id 持久化完整 rationale 见 §2.1。

## 三查工作流
对外响应回带 `trace_id`(调试用,受保留期约束)+ 业务 id(如 `order_id`)。① 查 trace:哪个 span 红/慢 →"哪一步"。② 查 log(同 `trace_id`):决策/状态/错误 →"为什么",不够细按此 trace 开 DEBUG 重放。③ 查 db(**按业务 id**,它本就是 span 属性):落库数据对不对。

## 强制生效(让规范咬人,而非形式化)

**没有 gate 的规范 = 形式化,必然漂移**——靠人工对照清单的规范,会在"没测试看的地方"悄悄烂掉,埋点的洞恰好出现在没人 gate 的模块(见 §9)。**强制手段是采纳可观测性的一等交付物,不是事后补丁。** 立规范必须同时立 gate(机制按栈替换):
- **conformance 测试断 span 覆盖 + parent 正确,且会变红**:进程内捕获 span(语言的进程内 span 捕获器,见 references 附录 C),断言每条新 LLM/工具/检索/领域决策路径**发出领域 span 且 parent 正确**;**必带负例探针**(删 span / 断 parent → 测试变红),只测 happy-path 不强制任何东西。
- **统一接口**:仓库声明 `observability_conformance_command` + `observability_conformance_paths`;命令复用 `references/conformance-profile-v2.json` 与 `scripts/observability_conformance.py`,覆盖 resource/tenant、GenAI 字段、parent+async/streaming、默认无内容、vendor/legacy static guard,并拒绝 `run.id` 等高基数 metric label;profile 声明的 forbidden prefix 扫完整 snapshot(含 events)。IaC 只执行 command、按 paths 触发、消费 exit code/result,不得复制字段 oracle(见 references §9.5)。
- **gate 真在 CI 跑、能 fail build**:workflow 放工具识别的位置(GitHub Actions 只跑**仓库根** `.github/workflows/`)、paths 覆盖、**无 `|| true`/soft-fail**;**在真 PR 上验证 gate 确实触发**,别假设。
- **每条铁律 → 机制**:铁律5(禁厂商 SDK)→ 静态 import 契约(各语言 import 守卫,见 references 附录 C);铁律4(传 traceparent)→ 跨边界断言下游 span 同 trace_id;类型纪律 → 类型检查进 CI(见 references 附录 A)。
- **孤儿 span 陷阱**(最常见隐形失败):`create_task`/goroutine/线程池/队列交接丢 ambient context → 子 span 变孤儿 root,"埋了却不可见";跨脱离点捕获并重 attach context,conformance 断言异步两侧同 trace_id。
- **宪法条款**:仓库 `AGENTS.md`/`CONTRIBUTING` 写明"新 LLM/工具/检索/领域路径必须有 parent 正确的领域 span",指向本 skill。

达标线:**每条会被违反且能自动检测的铁律,都要有一个会让 CI 变红的 gate;检测不了的才进人工清单。立规范只产文档不产 gate = 没立。** 完整机制 + 实证见 §9。

## 接入初始化 checklist(一次性仪式,自包含——不依赖任何编排工具)

新项目/新仓库采纳本规范时,**当天**走完(排期到以后 = 稀释的开始;完整版见 references §10):
1. **宪法条款**进仓库 AGENTS.md / CONTRIBUTING(新领域路径必须有 parent 正确的 span,指向本 skill)。
2. **按语言立最小 conformance gate**(进程内 span 捕获断言:server span 存在 + 日志带 trace_id + 部署配置无 span 复述输出;语言起手式见 references §10)。
3. **负例探针**:删 span / 断 parent → gate 必须变红,贴双跑证据。
4. **CI wiring 验真**:在真 PR 上让 gate 真 fail 一次,别假设配置生效。
5. **环境三档矩阵**配置就位(dev/staging=DEBUG 可见、prod=INFO 骨架,见日志级别判据)。
6. **import 守卫**(禁厂商 SDK 直依赖,机制见 references 附录 C)。

## 何时读 references/standard.md

> **本 SKILL 是 `references/standard.md` §1–§10 的压缩镜像**(总纲 / 铁律 → §1、类型纪律 → §2 + §2.1、日志铁律 → §3、级别 → §4、span → §5、三查 → §7、强制生效 → §9;standard 另含 §6 日志接入、§8 检查清单、附录 A/B/C 各语言写法与工具链)。**改任一条规则必须同步两处。**

出现以下任一情况,读 `references/standard.md`:
- 需要**具体语言**(Python / Go / Java / Rust)的日志接入与类型纪律地道写法
- 做 **agent / 多 agent**,需要完整 span 拓扑与属性表
- 做 **RAG / 知识库**,需要完整检索链路埋点字段表
- 需要完整 span 属性表、落地检查清单,或某条规则背后的 rationale

落地前对照 `references/standard.md` 文末检查清单自查。
