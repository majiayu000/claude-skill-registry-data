---
name: team-orchestrator
description: AI 团队协调器。启动并管理通信架构师、产品经理、开发、QA 的协作流程。用于大型功能开发的全流程管理。关键词：团队、协作、全流程、启动项目。
allowed-tools: Task, TaskOutput, TodoWrite, Read, Write, Edit
---

# AI 团队协调器

## 团队角色

| 角色 | Skill | 职责 |
|------|-------|------|
| 通信架构师 | `role-network-architect` | 协议设计、性能优化、Code Review |
| 产品经理 | `role-product-pm` | 需求规划、场景分析、商业策略 |
| 开发 | `role-dev` | 按规范编码、实现功能 |
| QA | `role-qa` | 测试验证、性能测试 |

## 工作流程

```
┌─────────────────────────────────────────────────────────────────────────┐
│                           ORCHESTRATOR                                   │
│                     (协调所有角色，管理状态)                              │
└─────────────────────────────────────────────────────────────────────────┘
                                    │
                                    ▼
┌─────────────────────────────────────────────────────────────────────────┐
│ Phase 1: 需求分析                                                        │
│   PM 分析场景 → 定义需求 → 输出《需求规格》                              │
└─────────────────────────────────────────────────────────────────────────┘
                                    │
                                    ▼
┌─────────────────────────────────────────────────────────────────────────┐
│ Phase 2: 架构设计                                                        │
│   Architect 评估可行性 → 技术方案 → 输出《技术设计》                     │
└─────────────────────────────────────────────────────────────────────────┘
                                    │
                                    ▼
┌─────────────────────────────────────────────────────────────────────────┐
│ Phase 3: 任务拆分                                                        │
│   PM 拆分任务 → 识别依赖 → 输出《任务清单》                              │
└─────────────────────────────────────────────────────────────────────────┘
                                    │
                                    ▼
┌─────────────────────────────────────────────────────────────────────────┐
│ Phase 4: 并行开发 (循环)                                                 │
│   ┌──────────┐     ┌──────────┐     ┌──────────┐                        │
│   │  Dev 1   │     │  Dev 2   │     │  Dev N   │  (无依赖任务并行)      │
│   └────┬─────┘     └────┬─────┘     └────┬─────┘                        │
│        │                │                │                               │
│        └────────────────┼────────────────┘                               │
│                         ▼                                                │
│                 ┌──────────────┐                                         │
│                 │  Architect   │  Review 代码                            │
│                 └──────┬───────┘                                         │
│                        │                                                 │
│              ┌─────────┴─────────┐                                       │
│              ▼                   ▼                                       │
│        [通过] → QA          [不通过] → Dev 重构                          │
└─────────────────────────────────────────────────────────────────────────┘
                                    │
                                    ▼
┌─────────────────────────────────────────────────────────────────────────┐
│ Phase 5: 测试验收                                                        │
│   QA 测试 → 性能测试 → 输出《测试报告》                                  │
└─────────────────────────────────────────────────────────────────────────┘
```

## 状态文件

所有状态保存在 `.claude/team-state.json`:

```json
{
  "project": "feature-name",
  "phase": "development",
  "created_at": "2025-01-28T10:00:00Z",
  "updated_at": "2025-01-28T15:30:00Z",

  "requirements": {
    "status": "approved",
    "document": ".claude/team-workspace/requirements.md"
  },

  "architecture": {
    "status": "approved",
    "document": ".claude/team-workspace/architecture.md"
  },

  "tasks": [
    {
      "id": "T001",
      "title": "实现 QUIC 协议适配器",
      "status": "in_progress",
      "assignee": "dev-1",
      "dependencies": [],
      "review_result": null,
      "test_result": null
    }
  ],

  "review_queue": [],
  "test_queue": [],
  "completed": []
}
```

## 启动流程

### 1. 初始化项目

```
用户输入: "启动团队开发：添加 QUIC 协议支持"

Orchestrator 执行:
1. 创建 .claude/team-workspace/ 目录
2. 初始化 team-state.json
3. 启动 PM 分析需求
```

### 2. 调用 PM 分析需求

```python
Task(
    description="PM 分析需求",
    prompt="""
    你是通信产品经理。

    需求: 添加 QUIC 协议支持

    请分析:
    1. 用户场景 - 谁会使用 QUIC？解决什么问题？
    2. 核心需求 - 必须实现的功能
    3. 验收标准 - 如何验证功能完成
    4. 优先级 - 与其他功能的关系

    输出到: .claude/team-workspace/requirements.md
    """,
    subagent_type="general-purpose"
)
```

### 3. 调用 Architect 技术评审

```python
Task(
    description="Architect 技术评审",
    prompt="""
    你是通信架构师。

    基于 PM 的需求规格，进行技术评审:
    1. 可行性分析 - 技术难点、风险
    2. 架构设计 - 与现有协议适配器的关系
    3. 实现方案 - 关键类/接口设计
    4. 性能考量 - 延迟、吞吐量目标

    参考:
    - internal/protocol/adapter/tcp_adapter.go
    - internal/protocol/adapter/websocket_adapter.go

    输出到: .claude/team-workspace/architecture.md
    """,
    subagent_type="general-purpose"
)
```

### 4. 任务拆分

```python
Task(
    description="PM 拆分任务",
    prompt="""
    基于需求和技术方案，拆分开发任务:

    要求:
    1. 每个任务独立可执行
    2. 标注依赖关系
    3. 估算复杂度 (S/M/L)
    4. 无代码冲突

    输出到: .claude/team-workspace/tasks.md
    更新: .claude/team-state.json
    """,
    subagent_type="general-purpose"
)
```

### 5. 并行开发

```python
# 获取可并行任务
parallel_tasks = [t for t in tasks if t.dependencies_met]

# 并行启动开发
for task in parallel_tasks:
    Task(
        description=f"Dev: {task.title}",
        prompt=f"""
        你是高级开发工程师。

        任务: {task.title}
        描述: {task.description}

        要求:
        1. 遵循 CLAUDE.md 编码规范
        2. 遵循 Dispose 体系
        3. 完成后更新 team-state.json
        """,
        subagent_type="general-purpose",
        run_in_background=True
    )
```

### 6. 架构师 Review

```python
Task(
    description="Architect Review",
    prompt="""
    你是通信架构师，审查代码:

    审查任务: {task.title}
    修改文件: {task.changed_files}

    审查标准:
    1. Dispose 体系是否正确
    2. Context 传递是否正确
    3. 并发安全性
    4. 资源释放
    5. 性能考量

    输出:
    - 通过: 更新状态为 "testing"
    - 不通过: 更新状态为 "rework"，附带修改意见
    """,
    subagent_type="general-purpose"
)
```

### 7. QA 测试

```python
Task(
    description="QA 测试",
    prompt="""
    你是 QA 工程师，测试功能:

    测试任务: {task.title}

    执行:
    1. 单元测试: go test ./...
    2. 连接测试: 验证协议连接
    3. 性能测试: 延迟和吞吐量

    输出测试报告到: .claude/team-workspace/test-reports/{task.id}.md

    结果:
    - 通过: 更新状态为 "completed"
    - 不通过: 更新状态为 "fix"
    """,
    subagent_type="general-purpose"
)
```

## 快速启动命令

```
/team-orchestrator 启动团队开发：添加 QUIC 协议支持
```

或:

```
请启动 AI 团队，完成以下工作：
1. 添加 QUIC 协议适配器
2. 实现连接迁移支持
3. 优化移动网络性能
4. 完善测试覆盖
```

## 协调器主循环

```python
while not all_tasks_completed:
    state = read_state()

    if state.phase == "requirements":
        wait_for_pm()
        if pm_done: start_architect()

    elif state.phase == "architecture":
        wait_for_architect()
        if architect_done: start_task_split()

    elif state.phase == "development":
        for task in state.tasks:
            if task.status == "review":
                start_architect_review(task)
            elif task.status == "testing":
                start_qa_test(task)
            elif task.status == "rework":
                restart_dev(task)

        if all_reviewed_and_tested:
            state.phase = "acceptance"

    elif state.phase == "acceptance":
        run_final_acceptance()

    save_state(state)
```
