---
name: setup-fsm
description: "为角色配置动画状态机。Use when users need to (1) 给角色添加动画状态机, (2) 让角色能走路/跑/跳, (3) 配置角色动画切换, (4) setup fsm, (5) 角色动画状态, (6) 状态机配置。"
---

# 动画状态机配置指南

## 前置条件

角色节点上必须已有 **AnimatedModel** 组件。

## 参考文档

完整格式说明和 API：`engine-docs/recipes/state-machine.md`

## 模板文件位置

```
engine-docs/recipes/templates/fsm/
├── StandardLocomotion_Template.fsm                 # FSM 模板
├── MovementBlendSpace1D_Template.blendspace        # 1D 混合空间模板
└── MovementBlendSpace2D_Polar_Template.blendspace  # 2D Polar 混合空间模板
```

## 工作流

### 步骤 1: 选择模板类型

| 类型 | 适用场景 | 需要的参数 |
|------|---------|-----------|
| **1D 简单移动** | 角色只前后移动（平台跳跃、跑酷） | moveSpeed |
| **2D 八方向移动** | 角色可 8 方向移动（TPS、RPG） | moveSpeed + direction |

### 步骤 2: 复制模板并替换占位符

模板文件中的 `$PLACEHOLDER$` 需要替换为实际的动画 `uuid://`。通过 MCP 接口检索关键词（如"行走"、"奔跑"、"跳跃"）找到匹配的动画 uuid。

### 步骤 3: 复制模板到项目

```bash
# 在项目 scripts/ 下创建 FSM 目录
mkdir -p /workspace/scripts/FSM

# 复制 FSM 和 BlendSpace 模板文件
cp /workspace/engine-docs/recipes/templates/fsm/StandardLocomotion_Template.fsm /workspace/scripts/FSM/Character.fsm
# 1D 移动（二选一）
cp /workspace/engine-docs/recipes/templates/fsm/MovementBlendSpace1D_Template.blendspace /workspace/scripts/FSM/MovementBlendSpace.blendspace
# 或 2D 八方向移动（二选一）
cp /workspace/engine-docs/recipes/templates/fsm/MovementBlendSpace2D_Polar_Template.blendspace /workspace/scripts/FSM/MovementBlendSpace.blendspace
```

复制后，替换所有 `$PLACEHOLDER$` 为实际动画 uuid：

| 占位符 | 含义 |
|--------|------|
| `$MOVEMENT_BLENDSPACE$` | BlendSpace 文件路径（如 `FSM/MovementBlendSpace.blendspace`） |
| `$IDLE$` | 待机动画 |
| `$WALK$` / `$WALK_FORWARD$` | 行走动画 |
| `$RUN$` / `$RUN_FORWARD$` | 奔跑动画 |
| `$WALK_BACKWARD$` / `$RUN_BACKWARD$` | 后退行走/奔跑 |
| `$WALK_LEFT$` / `$RUN_LEFT$` | 左移行走/奔跑 |
| `$WALK_RIGHT$` / `$RUN_RIGHT$` | 右移行走/奔跑 |
| `$WALK_LEFT_BACK$` / `$RUN_LEFT_BACK$` | 左后行走/奔跑（2D Polar 模板 ±91° 方向） |
| `$WALK_RIGHT_BACK$` / `$RUN_RIGHT_BACK$` | 右后行走/奔跑（2D Polar 模板 ±91° 方向） |
| `$JUMP_START$` | 起跳动画 |
| `$JUMP_AIR$` | 空中滞空动画 |
| `$JUMP_LANDING$` | 落地动画 |

### 步骤 4: 添加组件和驱动代码

在 Lua 脚本中加载 FSM 并每帧更新参数：

```lua
-- 初始化（在 Start 或 DelayedStart 中）
local characterNode = -- 角色节点（已有 AnimatedModel）
characterNode:GetOrCreateComponent("AnimationController")
local fsm = characterNode:GetOrCreateComponent("AnimationStateMachine")

local jsonFile = cache:GetResource("JSONFile", "FSM/Character.fsm")
fsm:LoadFromJSONFile(jsonFile)
fsm:Start()

-- 每帧更新（在 Update 中）
fsm:SetFloat("moveSpeed", currentSpeed)        -- 当前移动速度
fsm:SetBool("isGrounded", isOnGround)           -- 是否在地面
-- 如果使用 2D Polar：
-- fsm:SetFloat("direction", moveDirection)      -- 移动方向角度 (-180~180)

-- 跳跃时触发
if jumpPressed then
    fsm:SetTrigger("jump")
end
```

### 步骤 5: 验证

运行场景，检查：
- 角色静止时播放 Idle 动画
- 移动时平滑过渡到 Walk → Run
- 按跳跃后播放 JumpStart → JumpAir → JumpLanding
- 各状态之间过渡平滑

## 典型使用场景

| 场景 | 做法 |
|------|------|
| 快速让角色动起来 | 复制模板 FSM + BlendSpace，替换占位符为动画 uuid，加 Lua 驱动代码 |
| 8 方向移动（TPS） | 用 2D Polar 版 BlendSpace，FSM 中增加 direction 参数 |
| 需要更复杂的状态 | 阅读 `recipes/state-machine.md` 的多层 FSM 章节 |
| 参考完整示例 | 查看 `examples/22-third-person-shooter` 的 Unified.fsm |

## 注意事项

- FSM 和 BlendSpace 文件路径相对于资源根目录（`scripts/` 或 `assets/`）
- 节点上必须同时有 `AnimationController` 和 `AnimationStateMachine` 两个组件
- `SetTrigger` 触发后会自动重置，只在需要触发时调用一次
- 官方动画会自动重定向到用户导入模型的骨架，无需额外配置
