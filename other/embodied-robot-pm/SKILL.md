---
name: embodied-robot-pm
description: "具身智能/具身机器人产品管理工作流。Use for embodied AI, humanoid, legged robot, mobile robot, AMR/AGV product strategy, scenario discovery, PRD, capability map, technical roadmap, ODD, safety, BOM/TCO and validation."
---

# 具身机器人产品经理

## Purpose

把业务问题转成可交付的机器人产品定义。保持产品经理视角：理解技术实现路径和约束，但不替代算法、硬件、安全或认证负责人做专业签署。

## Input

用户可以只给一个想法，也可以提供场景流程、客户需求、机器人形态、已有方案、预算或研发阶段。使用用户已提供的信息，不重复询问；缺失信息不影响启动时，采用最佳判断并明确标为“待验证假设”。

示例：`使用 embodied-robot-pm，规划一款在仓库搬运周转箱的轮式机器人，从场景到技术路径和MVP。`

## Key Concepts

- **场景先于形态**：先证明任务值得自动化，再选择轮式、足式、人形或混合形态。
- **任务闭环**：观察 -> 理解 -> 规划 -> 移动/操作 -> 确认 -> 异常恢复。
- **ODD**：明确机器人允许运行的环境、人员、地面、光照、网络和天气边界。
- **能力可验证**：每项能力同时定义指标、测试条件、证据和降级策略。
- **技术路线有层级**：区分产品目标、系统能力、算法/硬件方案和具体实现，不把技术名词当需求。
- **安全是主路径**：安全、人工接管和故障恢复从第一版进入设计，不作为末期补丁。
- **经济性按成功任务计算**：关注每个成功任务或有效工时的总成本，而不只看整机售价。

## Application

### 1. 判断用户需要的深度

选择最小工作范围：

- **技术认知**：解释实现路径、模块关系、关键取舍和研发顺序。
- **产品定义**：形成场景、能力、指标、边界和验收条件。
- **项目决策**：补充优先级、里程碑、资源、成本和风险。
- **专项评审**：仅处理架构、底盘、足式/人形、安全或成本问题。

若用户未指定，默认输出“产品定义 + 技术认知”。

### 2. 建立场景证据

调用 `robotics-scenario-discovery`，描述当前人工流程、任务频率、失败代价、环境变化、接口对象和人工接管条件。没有场景证据时，不承诺机器人形态和算法路线。

### 3. 形成能力与技术地图

调用 `robotics-capability-technical-map`，把任务拆成能力树，覆盖感知、状态估计、定位、规划、移动、操作、控制、交互、安全、数据闭环和运维。为每个能力连接产品指标和验收证据。

### 4. 选择形态并写规格

- 以连续平整地面运输为主：调用 `mobile-base-product-spec`。
- 需要跨越台阶、复杂地形或全身操作：调用 `legged-humanoid-product-spec`。
- 同时评估多种形态时：先比较任务覆盖、风险、成本、部署周期和维护复杂度，再分别形成规格。

### 5. 评审系统方案

调用 `robotics-architecture-review`，检查端到端链路、接口、时序、算力、功耗、通信、数据、可观测性、故障隔离和升级回滚。把争议写成“决策、备选、证据、截止时间、负责人”。

### 6. 建立安全与经济性门槛

- 始终调用 `robotics-safety-reliability`，定义危害、保护状态、可靠性指标和验证层级。
- 涉及产品立项、采购或量产时，调用 `robotics-cost-production`，建立BOM、NRE、运维、良率、供应风险和单位任务成本。

### 7. 转成产品执行材料

根据用户需要，衔接已安装的 PM 技能：

- `prd-development`：形成PRD。
- `prioritization-advisor`：选择MVP能力。
- `roadmap-planning`：形成研发和试点路线图。
- `user-story-mapping`：按用户与机器人协作流程拆解版本。
- `epic-breakdown-advisor`：把系统能力拆成可交付工作包。

### 8. 输出决策包

使用 [交付模板](references/delivery-template.md)。至少包含：场景与ODD、成功指标、形态选择、能力技术地图、系统边界、安全与恢复、成本假设、验证计划、里程碑、风险和待验证假设。

## Examples

### 轮式场景

“评估仓库周转箱转运机器人”应先量化任务频次、路线变化、交接点和人工异常处理，再决定差速/舵轮、定位方式、调度接口和自动充电，不直接从导航算法选型开始。

### 足式/人形场景

“规划工厂巡检与阀门操作人形机器人”应拆开巡检、到达、识别、接触、施力、确认和恢复。若轮式移动底盘加机械臂可覆盖大多数任务，应把人形形态作为需额外证明的方案。

## Common Pitfalls

- **形态崇拜**：先决定做人形，再寻找场景。修正：用任务覆盖与经济性证明形态。
- **算法名词代替需求**：把SLAM、VLA或强化学习写成功能。修正：先写可观察行为、条件和指标。
- **只看演示成功**：忽略长尾环境、人工介入和恢复。修正：用连续任务、干预率和故障恢复验收。
- **指标无条件**：只写速度、精度或成功率。修正：同时写载荷、地面、光照、拥挤度、持续时间和样本量。
- **安全后置**：直到试点才讨论急停和保护。修正：从ODD、危害和安全状态开始。

## References

- [交付模板](references/delivery-template.md)
- 相关技能：`robotics-scenario-discovery`、`robotics-capability-technical-map`、`robotics-architecture-review`、`mobile-base-product-spec`、`legged-humanoid-product-spec`、`robotics-safety-reliability`、`robotics-cost-production`
