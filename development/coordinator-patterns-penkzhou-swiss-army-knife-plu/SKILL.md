---
name: coordinator-patterns
description: master-coordinator 和 review-coordinator 共享的通用模式，包括 Phase 验证、错误处理、TodoWrite 管理和状态说明。所有 coordinator agents 应引用此 skill 以保持一致性。
---

# Coordinator 通用模式

本 skill 定义了所有 coordinator agents 共享的通用模式，包括：

1. Phase 验证逻辑
2. 错误处理模式
3. TodoWrite 管理
4. 状态说明

## Phase 验证逻辑

所有 master-coordinator 必须在初始化时验证 `phase` 参数：

```python
def validate_phase(phase_arg, valid_phases):
    """
    验证 phase 参数

    Args:
        phase_arg: 用户传入的 phase 参数（如 "0,1,2" 或 "all"）
        valid_phases: 有效 phase 列表（如 ["0", "1", "2", "3", "4", "5", "all"]）

    Returns:
        (is_valid, result): 如果有效，result 是 phase 列表；如果无效，result 是错误响应
    """
    if phase_arg == "all":
        # 返回所有数字 phases（排除 "all"）
        return True, sorted([p for p in valid_phases if p != "all"], key=int)

    phases = phase_arg.split(",")
    invalid_phases = [p for p in phases if p not in valid_phases]

    if invalid_phases:
        return False, {
            "status": "failed",
            "error": {
                "code": "INVALID_PHASE",
                "message": f"无效的 phase 参数: {invalid_phases}",
                "valid_values": valid_phases,
                "received": phase_arg,
                "suggestion": f"有效值: 0-{len(valid_phases)-2} 的数字或 'all'，多个用逗号分隔"
            }
        }

    return True, sorted(set(phases), key=int)
```

### 各工作流的有效 Phases

| 工作流 | 有效 Phases | 说明 |
|--------|------------|------|
| Bugfix | 0-5 | 6 阶段 |
| PR Review | 0-7 | 8 阶段 |
| CI Job | 0-6 | 7 阶段 |
| Execute Plan | 0-5 | 6 阶段 |

## 错误处理模式

所有 coordinator 必须处理以下错误类型：

### JSON 解析错误

当 agent 返回的内容无法解析为有效 JSON 时：

```python
try:
    result = json.loads(agent_output)
except json.JSONDecodeError as e:
    return {
        "status": "failed",
        "error": {
            "code": "JSON_PARSE_ERROR",
            "message": "Agent 输出无法解析为 JSON",
            "phase": current_phase,
            "agent": agent_name,
            "parse_error": str(e),
            "raw_output_preview": agent_output[:500],  # 前 500 字符供调试
            "suggestion": "检查 agent 是否正确返回 JSON 格式，或重试命令"
        }
    }
```

### Agent 执行超时

```python
if agent_result.error.code == "TIMEOUT":
    return {
        "status": "failed",
        "error": {
            "code": "AGENT_TIMEOUT",
            "message": f"Agent {agent_name} 执行超时",
            "phase": current_phase,
            "timeout_ms": agent_result.error.timeout_ms,
            "suggestion": "任务可能过于复杂，建议拆分或简化输入"
        }
    }
```

### 响应截断

当 agent 输出超过长度限制被截断时：

```python
if agent_result.truncated:
    # 记录警告但尝试继续
    warnings.append({
        "code": "OUTPUT_TRUNCATED",
        "message": f"Agent {agent_name} 输出被截断",
        "original_length": agent_result.original_length,
        "truncated_length": agent_result.truncated_length,
        "impact": "可能丢失部分诊断信息"
    })
    # 如果关键字段缺失，则停止
    if not validate_required_fields(agent_result):
        return {
            "status": "failed",
            "error": {
                "code": "TRUNCATION_DATA_LOSS",
                "message": "输出截断导致关键数据丢失",
                "missing_fields": get_missing_fields(agent_result),
                "suggestion": "请简化输入或分批处理"
            }
        }
```

### 用户取消

```python
if user_choice in ["取消", "停止"]:
    return {
        "status": "user_cancelled",
        "phase": current_phase,
        "reason": "用户选择停止执行",
        "completed_work": {...}  # 已完成的工作
    }
```

### Agent 调用失败（通用）

```python
if agent_result.status == "failed":
    return {
        "status": "failed",
        "error": {
            "phase": current_phase,
            "agent": agent_name,
            "code": agent_result.error.code,
            "message": agent_result.error.message
        }
    }
```

### 错误恢复机制（可选）

对于支持错误恢复的 coordinator：

```python
# 可恢复错误类型
RECOVERABLE_ERRORS = {
    "TIMEOUT": True,           # 超时可重试
    "RATE_LIMIT": True,        # 限流可重试
    "OUTPUT_TRUNCATED": True,  # 截断可简化输入重试
}

MAX_RETRIES = 2  # 最多重试 2 次

def is_recoverable(error):
    """判断错误是否可恢复"""
    return RECOVERABLE_ERRORS.get(error.code, False)
```

## TodoWrite 管理

所有 coordinator 必须使用 TodoWrite 跟踪执行进度：

### 初始化 Todo 列表

```python
def create_phase_todos(phases, phase_descriptions):
    """
    创建 Phase 任务列表

    Args:
        phases: Phase 列表（如 ["0", "1", "2"]）
        phase_descriptions: Phase 描述映射（如 {"0": ("问题收集", "收集中"), ...}）

    Returns:
        todos 列表
    """
    todos = []
    for i, phase in enumerate(phases):
        desc, active_form = phase_descriptions.get(phase, (f"Phase {phase}", f"执行 Phase {phase}"))
        todos.append({
            "content": f"Phase {phase}: {desc}",
            "status": "in_progress" if i == 0 else "pending",
            "activeForm": active_form
        })
    return todos
```

### 更新 Todo 状态

```python
def on_phase_complete(todos, phase_index):
    """完成 Phase 后更新状态"""
    todos[phase_index]["status"] = "completed"
    if phase_index + 1 < len(todos):
        todos[phase_index + 1]["status"] = "in_progress"
    return todos
```

### 各工作流的 Phase 描述

**Bugfix 工作流：**
```python
BUGFIX_PHASES = {
    "0": ("问题收集与分类", "收集中"),
    "1": ("诊断分析", "分析中"),
    "2": ("方案设计", "设计中"),
    "3": ("方案文档化", "文档化中"),
    "4": ("实施执行", "执行中"),
    "5": ("验证与审查", "审查中")
}
```

**PR Review 工作流：**
```python
PR_REVIEW_PHASES = {
    "0": ("初始化", "初始化中"),
    "1": ("评论获取", "获取评论中"),
    "2": ("评论过滤", "过滤评论中"),
    "3": ("评论分类", "分类评论中"),
    "4": ("修复协调", "协调修复中"),
    "5": ("回复生成", "生成回复中"),
    "6": ("回复提交", "提交回复中"),
    "7": ("审查与汇总", "审查汇总中")
}
```

**CI Job 工作流：**
```python
CI_JOB_PHASES = {
    "0": ("初始化", "初始化中"),
    "1": ("日志获取", "获取日志中"),
    "2": ("失败分类", "分类失败中"),
    "3": ("根因分析", "分析根因中"),
    "4": ("修复执行", "执行修复中"),
    "5": ("验证与审查", "验证审查中"),
    "6": ("汇总报告", "生成报告中")
}
```

**Execute Plan 工作流：**
```python
EXECUTE_PLAN_PHASES = {
    "0": ("初始化与计划解析", "初始化中"),
    "1": ("计划验证", "验证中"),
    "2": ("方案细化", "细化方案中"),
    "3": ("批次执行", "执行中"),
    "4": ("Review 审查", "审查中"),
    "5": ("汇总报告", "生成报告中")
}
```

## 状态说明

所有 coordinator 输出的 `status` 字段使用统一的语义：

| status | 含义 | 适用场景 |
|--------|------|----------|
| `success` | 所有 Phase 成功完成 | 正常完成 |
| `failed` | 某个 Phase 失败且无法继续 | 不可恢复错误 |
| `partial` | 部分任务失败，但流程完成 | 有剩余问题 |
| `user_cancelled` | 用户选择停止 | 用户主动取消 |
| `dry_run_complete` | Dry run 模式完成分析 | --dry-run 模式 |

## 必填输出字段

每个 coordinator 的 JSON 输出**必须**包含：

```json
{
  "status": "success|failed|partial|user_cancelled|dry_run_complete",
  "agent": "xxx-master-coordinator",
  "phases_completed": ["phase_0", "phase_1", ...],
  "errors": [],
  "warnings": []
}
```

## 关键原则

1. **闭环执行**：所有逻辑在 agent 内部完成，不依赖命令层
2. **状态透明**：每个 Phase 的输出都保存并传递到下一 Phase
3. **用户控制**：关键决策点使用 AskUserQuestion 询问用户
4. **进度可见**：使用 TodoWrite 让用户了解执行进度
5. **错误隔离**：单个任务失败不应影响其他独立任务
