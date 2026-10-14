---
name: role-federation
version: 2.0.0
description: |
  角色联邦制 - 多Agent协同治理系统：
  1. 全局考虑：覆盖人/事/物/环境/外部集成/边界情况
  2. 系统考虑：输入→处理→输出→反馈闭环，故障处理机制
  3. 迭代机制：PDCA循环，版本历史，反馈收集
  4. Skill化：标准SKILL.md格式，可安装可调用
  5. 自动化：cron监控+脚本执行+自动报告
author: Satisficing Institute
tags:
  - governance
  - multi-agent
  - federation
  - automation
requires:
  - model: "kimi-coding/k2p5"
  - local_tools: ["python3"]
---

# 角色联邦制 Skill V2.0.0

## S1: 全局考虑 (Global Coverage)

### 1.1 人 - 角色体系

| 角色 | 职责 | 权限 | 外部集成 |
|------|------|------|----------|
| **Captain(协调官)** | 任务分配、资源调度、冲突仲裁 | 最高决策权 | 对接人类Director |
| **Specialist(专家官)** | 研究/写作/分析专项任务 | 子任务自主 | 调用外部API/工具 |
| **Auditor(审计官)** | 质量检查、合规审查、否决权 | 质量否决权 | 质量门禁系统联动 |
| **Messenger(通信官)** | 对外接口、信息聚合 | 通信权限 | 飞书/企业微信/邮件 |

### 1.2 事 - 工作流程

```
外部输入 → 任务接收 → 角色分配 → 并行处理 → 结果聚合 → 质量审计 → 输出交付
                ↑                                              ↓
                └──────────────── 反馈闭环 ← 异常处理 ← 审计反馈
```

### 1.3 物 - 资源管理

| 资源类型 | 管理规则 | 边界情况 |
|----------|----------|----------|
| Token预算 | 三级分配(战略/运营/创新) | 超支自动熔断 |
| 计算资源 | 按优先级分配 | 资源不足时队列化 |
| 存储空间 | 定期归档清理 | 满时自动告警 |
| API配额 | 实时监控 | 耗尽时切换备用源 |

### 1.4 环境 - 运行上下文

| 环境维度 | 监控指标 | 自适应策略 |
|----------|----------|------------|
| 系统负载 | CPU/内存/网络 | 高负载时降级处理 |
| 外部依赖 | API可用性 | 故障时启用缓存/备用 |
| 时间约束 | 截止期限 | 临近时优先级提升 |
| 质量水位 | 信任分/准确率 | 低分时增加审核 |

### 1.5 外部集成

```yaml
integrations:
  feishu:
    type: 消息通知
    trigger: 任务完成/异常告警
    fallback: 邮件备用
  
  wecom:
    type: 联系人同步
    trigger: 角色变更
    fallback: 本地缓存
  
  quality_gate:
    type: 质量审计
    trigger: 输出提交
    fallback: 人工复核
  
  token_enforcer:
    type: 预算控制
    trigger: 任务启动
    fallback: 任务暂停
```

### 1.6 边界情况处理

| 边界场景 | 检测机制 | 处理策略 |
|----------|----------|----------|
| 角色冲突 | 同一任务多角色竞争 | RFP投标机制 |
| 死锁循环 | 任务A依赖B，B依赖A | 超时检测+强制仲裁 |
| 资源耗尽 | Token/计算资源耗尽 | 任务队列化+告警 |
| 外部故障 | API/服务不可用 | 降级模式+备用方案 |
| 质量异常 | 信任分骤降 | 强制审计+人工介入 |

---

## S2: 系统考虑 (Systematic)

### 2.1 输入处理

| 输入类型 | 验证规则 | 转换处理 |
|----------|----------|----------|
| 自然语言指令 | 意图识别+实体提取 | 转换为结构化任务 |
| 结构化数据 | Schema验证 | 标准化为内部格式 |
| 文件上传 | 格式+大小+安全检测 | 提取内容+元数据 |
| 外部事件 | 签名验证+去重 | 触发对应工作流 |

### 2.2 处理引擎

```
┌─────────────────────────────────────────────────────────────┐
│                      角色联邦处理引擎                         │
├──────────────┬──────────────┬──────────────┬────────────────┤
│   任务解析器   │   角色路由器   │   并行执行器   │   结果聚合器   │
├──────────────┼──────────────┼──────────────┼────────────────┤
│ • 意图识别    │ • 能力匹配    │ • 子任务分发  │ • 结果合并    │
│ • 优先级排序  │ • 负载均衡    │ • 进度监控    │ • 冲突解决    │
│ • 依赖分析    │ • 故障转移    │ • 超时处理    │ • 质量评分    │
└──────────────┴──────────────┴──────────────┴────────────────┘
```

### 2.3 输出规范

| 输出类型 | 格式要求 | 元数据 |
|----------|----------|--------|
| 文本回复 | Markdown格式 | 置信度/来源/时间戳 |
| 结构化数据 | JSON Schema | 版本/校验和 |
| 文件生成 | 标准命名规范 | 大小/格式/创建时间 |
| 通知消息 | 模板化 | 优先级/过期时间 |

### 2.4 反馈闭环

```
输出交付 → 用户反馈 → 效果评估 → 模型更新
                ↓
         满意度评分 → 信任分调整 → 策略优化
```

| 反馈类型 | 收集方式 | 处理动作 |
|----------|----------|----------|
| 显式反馈 | 评分/评论 | 直接计入信任分 |
| 隐式反馈 | 行为数据 | 模式分析后调整 |
| 质量审计 | 自动检查 | 问题归类+规则更新 |
| 异常报告 | 自动捕获 | 触发复盘流程 |

### 2.5 故障处理机制

| 故障级别 | 检测指标 | 自动响应 | 人工介入 |
|----------|----------|----------|----------|
| P0-致命 | 系统崩溃/数据丢失 | 立即告警+回滚 | 必须 |
| P1-严重 | 核心功能不可用 | 降级模式+重试 | 建议 |
| P2-一般 | 性能下降/偶发错误 | 自动重试+日志 | 可选 |
| P3-轻微 | 非核心功能异常 | 记录待修复 | 不紧急 |

---

## S3: 迭代机制 (Iterative)

### 3.1 PDCA循环

```yaml
Plan(计划):
  - 每周日生成下周任务规划
  - 基于历史数据预测资源需求
  - 设定可量化的目标指标

Do(执行):
  - 按计划分配任务给各角色
  - 实时监控执行进度
  - 记录执行过程中的异常

Check(检查):
  - 每日生成执行报告
  - 对比计划vs实际完成
  - 分析偏差原因

Act(改进):
  - 根据检查结果调整策略
  - 更新规则文档
  - 优化资源分配算法
```

### 3.2 版本历史

| 版本 | 日期 | 变更说明 | 作者 |
|------|------|----------|------|
| v2.0.0 | 2026-03-21 | 全面重构，5标准全覆盖 | 满意解研究所 |
| v1.1.0 | 2026-03-18 | 增加RFP投标机制 | 满意解研究所 |
| v1.0.0 | 2026-03-15 | 初始版本，基础角色定义 | 满意解研究所 |

### 3.3 反馈收集机制

| 反馈来源 | 收集频率 | 处理方式 |
|----------|----------|----------|
| 任务完成反馈 | 每次任务 | 实时计入信任分 |
| 每日执行复盘 | 每日23:00 | 生成日报+趋势分析 |
| 每周系统评估 | 每周日 | 生成周报+优化建议 |
| 月度战略回顾 | 每月1日 | 调整角色配置+规则 |

### 3.4 优化触发条件

| 触发条件 | 阈值 | 优化动作 |
|----------|------|----------|
| 任务成功率下降 | <90% | 增加审计频率 |
| 平均响应时间上升 | >30s | 优化路由算法 |
| 资源利用率不均 | 方差>20% | 调整负载均衡 |
| 用户满意度下降 | <4.0/5 | 专项复盘+改进 |

---

## S4: Skill化 (Skill-ified)

### 4.1 目录结构

```
role-federation/
├── SKILL.md                    # 本文件
├── _meta.json                  # 元数据
├── scripts/
│   ├── federation_runner.py    # 主运行脚本
│   ├── role_manager.py         # 角色管理
│   ├── task_router.py          # 任务路由
│   ├── conflict_arbitrator.py  # 冲突仲裁
│   └── feedback_collector.py   # 反馈收集
├── config/
│   ├── roles.yaml              # 角色定义
│   ├── rules.yaml              # 运行规则
│   └── thresholds.yaml         # 阈值配置
└── logs/
    ├── federation.log          # 运行日志
    └── feedback.json           # 反馈数据
```

### 4.2 标准化接口

```python
# 角色联邦接口定义
class RoleFederation:
    
    def assign_task(self, task: Task) -> Assignment:
        """分配任务给合适角色"""
        pass
    
    def bid_task(self, task: Task, role: Role) -> Bid:
        """角色投标任务"""
        pass
    
    def arbitrate_conflict(self, conflict: Conflict) -> Resolution:
        """仲裁角色冲突"""
        pass
    
    def collect_feedback(self, feedback: Feedback) -> None:
        """收集执行反馈"""
        pass
    
    def generate_report(self, period: str) -> Report:
        """生成周期报告"""
        pass
```

### 4.3 调用方式

```bash
# 安装Skill
openclaw skill install role-federation

# 分配任务
openclaw skill run role-federation assign --task "analyze market"

# 仲裁冲突
openclaw skill run role-federation arbitrate --roles "A,B" --issue "resource"

# 查看状态
openclaw skill run role-federation status

# 生成报告
openclaw skill run role-federation report --period daily
```

---

## S5: 自动化 (Automation)

### 5.1 Cron定时任务

```json
{
  "jobs": [
    {
      "name": "role-federation-morning-brief",
      "schedule": "13 9 * * *",
      "command": "cd /root/.openclaw/workspace/skills/role-federation && python3 scripts/federation_runner.py morning-brief",
      "description": "每日09:13生成角色联邦晨间简报"
    },
    {
      "name": "role-federation-health-check",
      "schedule": "*/30 * * * *",
      "command": "cd /root/.openclaw/workspace/skills/role-federation && python3 scripts/federation_runner.py health-check",
      "description": "每30分钟健康检查"
    },
    {
      "name": "role-federation-daily-report",
      "schedule": "47 23 * * *",
      "command": "cd /root/.openclaw/workspace/skills/role-federation && python3 scripts/federation_runner.py daily-report",
      "description": "每日23:47生成角色联邦日报"
    },
    {
      "name": "role-federation-weekly-review",
      "schedule": "17 22 * * 0",
      "command": "cd /root/.openclaw/workspace/skills/role-federation && python3 scripts/federation_runner.py weekly-review",
      "description": "每周日22:17生成周回顾报告"
    }
  ]
}
```

### 5.2 自动化脚本

| 脚本 | 功能 | 触发方式 |
|------|------|----------|
| `federation_runner.py` | 主控脚本 | cron/手动 |
| `role_manager.py` | 角色生命周期管理 | 自动 |
| `task_router.py` | 智能任务路由 | 任务创建时 |
| `conflict_arbitrator.py` | 自动冲突仲裁 | 检测到冲突时 |
| `feedback_collector.py` | 反馈数据收集 | 任务完成时 |

### 5.3 自动监控与告警

| 监控项 | 阈值 | 告警方式 |
|--------|------|----------|
| 任务积压数 | >10 | 飞书通知 |
| 角色响应时间 | >60s | 邮件告警 |
| 冲突发生频率 | >5/小时 | 紧急通知 |
| 系统资源使用率 | >85% | 资源告警 |
| 信任分下降 | >10分/天 | 质量告警 |

### 5.4 自动报告生成

| 报告类型 | 频率 | 内容 | 接收者 |
|----------|------|------|--------|
| 晨间简报 | 每日09:13 | 今日任务+昨日完成 | 所有角色 |
| 健康报告 | 每30分钟 | 系统状态+异常 | 监控系统 |
| 日报 | 每日23:47 | 完成统计+问题汇总 | Director |
| 周报 | 每周日22:17 | 趋势分析+优化建议 | Director |

---

## 附录：命令参考

| 命令 | 功能 | 示例 |
|------|------|------|
| `assign [task]` | 分配任务 | `assign "分析竞品"` |
| `bid [task]` | 投标任务 | `bid "调研报告"` |
| `arbitrate [conflict]` | 仲裁冲突 | `arbitrate "资源竞争"` |
| `status` | 查看状态 | `status` |
| `report [period]` | 生成报告 | `report daily` |

---

## S7: 对抗验证 (Devil's Advocate Views)

### 反方观点：角色联邦机制可能失效的场景

#### 观点1：角色协调开销超过协作收益
**提出者**: 蓝军
**论据**:
- 多角色讨论可能增加沟通成本
- 简单任务可能因"联邦流程"而变得复杂
- 投标/仲裁机制可能消耗额外Token

**失效场景**:
```yaml
scenario: 联邦开销过大
触发条件:
  - 任务协调时间 > 任务执行时间 50%
  - 简单任务（<10分钟）仍需完整联邦流程
  - 角色间重复沟通
后果: 协作效率低于单一执行者
```

#### 观点2：Devil's Advocate沦为反对一切
**提出者**: 蓝军
**论据**:
- 强制异议可能导致"为反对而反对"
- 可能延误紧急任务的执行
- 反方观点质量可能参差不齐

**失效场景**:
```yaml
scenario: 异议疲劳
触发条件:
  - 90%的异议被证明无价值
  - 任务因反复异议延期 > 50%
  - 团队开始忽视所有异议
后果: Devil's Advocate失去预警价值
```

#### 观点3：角色固化扼杀灵活性
**提出者**: 蓝军
**论据**:
- 预定义角色可能不适应新型任务
- 可能出现"角色真空"（无人适合）
- 多面手角色可能被强行拆分

**失效场景**:
```yaml
scenario: 角色不匹配
触发条件:
  - 新类型任务无对应角色
  - 任务需要多角色能力融合
  - 角色切换开销 > 任务本身
后果: 角色体系成为负担而非助力
```

### 缓解措施（已实施）

| 反方观点 | 缓解措施 |
|---------|----------|
| 联邦开销 | 简单任务（<10分钟）可跳过联邦流程 |
| 异议疲劳 | 异议必须提供具体论据，禁止无依据反对 |
| 角色固化 | 允许动态角色创建，标准角色非强制 |

### 失效预警指标

```yaml
warning_indicators:
  - metric: 协调/执行时间比
    threshold: >50%
    meaning: 联邦开销过大
    action: 简化流程或跳过联邦
    
  - metric: 异议采纳率
    threshold: <10%持续1周
    meaning: 异议质量下降
    action: 审查异议机制
    
  - metric: 角色匹配成功率
    threshold: <80%
    meaning: 角色体系不匹配
    action: 更新角色定义
```

### 认知谦逊声明

- [KNOWN] 角色设计基于当前任务类型，对未来任务类型的覆盖有限
- [INFERRED] 投标评分机制基于经验权重，未经严格优化
- [UNKNOWN] 长期使用角色联邦对人类决策习惯的影响尚不明确

---

*版本: v2.0.0*  
*更新日期: 2026-03-21*  
*作者: 满意解研究所*
