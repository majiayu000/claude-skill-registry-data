---
name: agent-backend-standard
version: 1.4.2
description: "生产级 agent 时代后端工程手册(hub)——建 / 评审 agent·LLM 后端、**任何碰 DB 的持久层后端**、或为任何后端建立 / 评审 repo 工程门禁时加载。覆盖架构、prompt、工具(ACI)、记忆、检索/RAG、韧性幂等、人在环、安全护栏与有界执行、评估、成本、依赖生命周期,及**数据访问 / 缓存 / 秘密接触面三纪律**与 Python/Go/Java/Rust 统一 `fix/check/test` 门禁。本文件是目录,深度按需读 references/;可观测性/Git/A2A 是独立 skill,本 hub 只交叉引用。Use when building or reviewing agent/LLM backends, ANY backend touching a database, or establishing/reviewing backend repo engineering gates."
---

# Agent Backend — 后端工程手册（hub）

agent 时代后端工程规范的集中入口。**本文件是目录(ToC):每章一句话 + reference 指针。深度全在 `references/`,按需读单章,别全量加载。**

> 双层落地:软层 = 本手册(write-time 预防);硬层(CI 门禁 / ruleset / 清扫 bot)归 你的 IaC 仓 / IaC CTO。
> 粒度:同属"写·评审 agent 后端代码"这一触发的 concern 都在本 hub 作章;**独立 skill 仅限触发动词不同者**——埋点 → `observability-standard`、git → `git-workflow-standard`、A2A 对外契约 → A2A 对外契约规范(本 hub 交叉引用,不重复)。
> *TBD* 章 = 已占位、待真实素材再写实(不空写通用建议)。

## Book I — Foundations
- **I-1 何时该建 agent** → `references/agent-foundations.md` —— simplicity-first 升级路径(单调用→augmented→工作流→agent 循环,实测不够才升);已知步骤用真控制流;停止条件量化不了就别建。
- **I-2 架构与控制流** → `references/agent-foundations.md` —— 五工作流基元(chaining/routing/parallel/orchestrator-workers/evaluator)、循环四分类(turn/goal/time/proactive)、单 vs 多 agent(artifact handoff 不对话)、上下文工程四处方(just-in-time/compaction/note-taking/sub-agent)。

## Book II — Engineering Concerns
- **II-3 上下文与 prompt 工程** → `references/prompt-context.md` —— 含 **prompt 内容生命周期**(写死值绑 eval、模型耦合打 `REVISIT-WHEN`)。
- **II-4 工具 / 函数设计(ACI)** → `references/tool-design.md` —— 质量定义="只拿工具能答多跳真问题";描述/示例杠杆大于实现(Tool Search 49→74%、Examples 72→90%);命名空间/token 效率(response_format、~25k 上限、中间结果不过模型可省 98%)/错误为 LLM 而写;有状态 handle 四约束(MCP 2026-07-28)。(交叉引 A2A 对外契约规范)
- **II-5 记忆 / 状态 / 持久** → `references/state-durability.md` —— workflow 首次 runnable / 首个副作用前原子固化 immutable effective-config snapshot(`snapshot_id` + digest);step / resume / recovery 只读该 snapshot,缺失 / 损坏 / digest mismatch fail-closed。
- **II-6 检索 / RAG / grounding** —— chunking、faithfulness、向量弱点。*TBD*
- **II-7 韧性 / 错误 / 幂等** → `references/resilience.md` —— 每个外部/LLM/工具调用:超时 + 有界重试 + 幂等 + 熔断 + 池/并发;**事件循环不阻塞**(async 运行时承重条,五层门禁:lint→测试期检测→staging 阈值→生产 lag 遥测→部署断言)。
- **II-8 人在环(HITL)+ resume 安全** → `references/hitl-resume-safety.md` —— 可恢复 flow 的 resume 安全:**六道闸**防御(持久 checkpoint 校验请求 ctx、fail-closed、runtime 层)。clarify/approve 协议交叉引 A2A 对外契约规范。
- **II-9 安全 · 护栏 · 生成操作的有界执行** → `references/safety-bounded-execution.md` —— 执行不可信生成操作(尤 SQL)的硬边界、安全分层、workflow 迭代上限。

## Book III — Operations & Governance
- **III-10 评估与测试** → `references/evals.md` —— 从 20-50 真实失败起步/两专家同判=好任务/grade outputs not paths;**pass^k 非 pass@k**、<3pp 差距不当能力差;judge 用 Kappa 校准+多 judge 一致门+Unknown 逃生口;威胁模型=被测物会作弊(reward hacking);MCP server eval 形态(10 多跳问题+字符串比对)。
- **III-11 可观测与成本 / 时延** → `references/observability-cost.md` —— 薄:成本/token/时延预算;埋点本体交叉引 `observability-standard`,不重复。
- **III-12 规范治理** → `references/governance.md` —— 例外/偏离、owner、手册如何演化。

## 附(本仓并入,非 agent 专属但同一触发)
- **A 代码 / 依赖生命周期 + 反死代码** → `references/code-dependency-lifecycle.md` —— 引入即退役(ADR-with-sunset)、stale-but-live(`EXPIRES`/`REVISIT-WHEN`)、**功能旗标生命周期(分类 + 毕业/退休 + 登记册)**、死代码检测 + 盲区、反 bloat、清扫。
- **B 数据访问纪律(连接·读·写)** → `references/data-write-discipline.md` —— **读也占连接**(弱事务/autocommit 用完即释放;MANAGED+closeConnection=false 无事务读 = 泄漏);记账写移出主链路 / 不跨 LLM 持锁 / 服务端增量;**关键写保留原子性但同样不持锁跨 LLM/执行**(短原子写 + 锁外执行)。
- **C Agent-friendly engineering interface** → `references/engineering-interface.md` §1–§6 —— Python / Go / Java / Rust 统一 repo-owned `fix/check/test` 接口；legacy ratchet 分 finding-aware hold gate + 单一 canonical close job，改善 durable 锁定后才放下一次集成、`check` 不改 baseline；另含初始化 forcing function 与失败自解释契约。边界类型规则只交叉引 observability §2,不复制。
- **D 缓存纪律(准入·永不缓存·失效治理)** → `references/caching-discipline.md` —— 四轴准入(读写比>10:1 / 陈旧红线 / 所有权 / DB 实测不够快,任一不过即不缓存)+ 金钱/占位/鉴权永不缓存、per-user 键强制 userId 命名空间 + **agent 时代失效治理三件套**(缓存决策表 SoT / 失效键注册 enum / 写路径配对失效机检门,任何缓存必有 TTL 兜底)+ 由外向内引入路线(升级触发即 ADR;负缓存/jitter/singleflight 随第一个缓存点同车)。
- **E 秘密接触面纪律(分离·注入)** → references/secrets-discipline.md —— 值/元数据物理分离(说明文档只留名字+gotcha,值进 gitignored `chmod 600` 的 env 文件)+ 注入形态唯一(`set -a; source; set +a`,值不落 stdout/argv/transcript);**不用 permissions deny 拦值文件**(2026-09 减法:误拦远大于召回);遮蔽/扫描面只用假数据验,真值永不作测试载荷。
- **F 自检清单与评审蒸馏门禁(电在回路 shock-in-the-loop)** → `references/selfcheck-gates.md` —— soft prompts steer, hard gates hold the line;真实评审 findings → PR 自检清单 → 可机检条目下沉 diff-scoped pre-push(纯 git+grep 毫秒级) → 负探针台账;铁律:每关必须指到真 finding,禁理论关卡;hook 是提醒、CI 复跑同脚本才是门。门禁接口归附录 C,本章管门禁的供给与演化。

## 关联(独立 skill,不在本 hub 重复)
- 埋点 / telemetry → `observability-standard`;Git SOP → `git-workflow-standard`;A2A 对外契约 → A2A 对外契约规范。
- 硬层 CI 门禁 / ruleset / 清扫 bot → 你的 IaC 仓。
