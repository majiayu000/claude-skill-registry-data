---
name: framework
description: GameKitCore 游戏框架（godot-rust GDExtension）GDScript 侧用法手册。当需要用该框架创建游戏项目代码、组装场景节点、编写战斗/对话/地图/UI/数据/协程等功能的 GDScript 示例时使用。按功能模块分类，每个模块文档含真实可用的 GDScript 示例代码与 API 签名。
---

# GameKitCore 框架用法手册

本 skill 是 gamecore 框架的 **GDScript 侧用法参考**。框架结构（Rust 模块划分）见
`rust/src/FRAMEWORK.md`；本 skill 只回答"怎么用"。可运行的完整示例在 `example/` 各目录。

## 使用规则

1. 写游戏代码前，先按功能查对应模块文档（`references/`），示例代码可直接套用。
2. 框架类均为 GDExtension 类（`Gd` 前缀），直接 `GdXxx.new()` 或在场景中挂载即可，无需 preload。
3. 单例通过 `Engine.get_singleton("名字")` 获取，共 5 个：`GDCORE`、`GdConsole`、`GDEVENTBUS`、`GDSPAWNPOOL`、`GDDEBUGDRAW`。
4. 节点组装后属性赋值必须在 `add_child` 之前/之后遵循各文档说明；export 属性可直接 `节点.属性 = 值`。

## 模块索引

| 模块文档 | 覆盖内容 | 对应 Rust 源码 |
|---|---|---|
| [references/scene-manager.md](references/scene-manager.md) | 场景切换/页面栈、全局暂停、设置持久化、相机、音频、输入 | `rust/src/manager/` |
| [references/role.md](references/role.md) | 角色移动/动画驱动/NPC AI 行为 | `rust/src/role/` |
| [references/combat.md](references/combat.md) | 血量/攻击受击判定/射击/子弹、对象池、事件总线、调试绘制 | `rust/src/components/` `pool/` `event/` `debug/` |
| [references/dialogue.md](references/dialogue.md) | 对话控制、触发器、角色绑定、对话 UI 回调 | `rust/src/dialog/` |
| [references/map.md](references/map.md) | 双网格地形地图、噪声生成、寻路、网格移动联动 | `rust/src/map/` |
| [references/environment.md](references/environment.md) | 天气系统（白天/夜晚/雨/雪/风）、画布绘图 | `rust/src/environment/` `drawer/` |
| [references/state-data.md](references/state-data.md) | GDCore 单例、GdCoreData 存档数据、GdBean 数据绑定 | `rust/src/state/` |
| [references/coroutine.md](references/coroutine.md) | 协程等待原语、可暂停协程任务 | `rust/src/runtime/` |
| [references/ui-gml.md](references/ui-gml.md) | GML 标记语言 UI、列表控件、弹窗、主题、Bean 数据驱动 | `rust/src/ui/` |
| [references/console.md](references/console.md) | Lua 调试控制台、注册命令 | `rust/src/console/` |
| [references/rogue.md](references/rogue.md) | 肉鸽卡牌引擎、实体生成、卡堆 | `rust/src/rogue/` |

## 全局约定（必读）

### 场景结构

```
Main (GdSceneRoot)                  # 场景管理器根节点
└── Game (业务脚本, PROCESS_MODE_PAUSABLE)
    ├── World (游戏世界节点)
    └── HUD (CanvasLayer, PROCESS_MODE_ALWAYS)
```

- 场景切换统一走 `GdSceneRoot.change_scene()`，**不要**用 `get_tree().change_scene_to_file()`（绕过页面栈与转场）。
- 全局暂停用 `GdSceneRoot.set_game_paused()`，不要直接改 `get_tree().paused`；HUD 等需要在暂停时响应的节点设 `process_mode = Node.PROCESS_MODE_ALWAYS`。

### 碰撞层约定（战斗）

| 层 | 值 | 用途 |
|---|---|---|
| layer 2 | 2 | 玩家受击盒（GdHurtbox） |
| layer 3 | 4 | 敌方受击盒（GdHurtbox） |

- 子弹（GdBullet）`collision_mask = 4`；敌方 Hitbox `collision_mask = 2`。
- Hitbox 的 `collision_mask` 永远指向**目标** Hurtbox 所在 layer。

### 角色组装公式

```
Player (GdRoleMover)
├── AnimatedSprite2D / GdRoleAnimator
├── GdHealth          (max_health / invincible_time)
├── GdHurtbox + CollisionShape2D   (collision_layer=2, mask=0)
├── GdShooter         (玩家) 或 GdNpcBrain (NPC)
└── GdRoleSpeaker + GdDialogTrigger   (需要对话的 NPC)
```

### 缓动与 juice

`rust/src/anim/`（easing/juice/EaseMover）为 Rust 内部实现，**无 GDScript 导出**；
GDScript 侧动画直接用原生 `create_tween()`。

### 无头测试红线（demo 实测沉淀）

- **无头帧率不节流**：`await process_frame` 帧数 ≠ 墙钟时间（900 帧可 <1s），
  等真实时间流逝的轮询必须用 `Time.get_ticks_msec()` 墙钟时限
- **lambda 按值捕获标量**：GDScript lambda 内 `counter += 1` 改的是副本，
  计数断言用 Array.append 收集
- **rust 扩展类 `get_class()` 返回注册类名**（如 GdDigLayer 而非基类
  GdQuickMap），类型断言勿写死基类
- **改 tscn 数值必 grep 测试硬断言**（旧数值硬编码连带失败的教训）
- **装配期重入**：do_swap_scene rust 栈内场景 `_ready` 禁调组件表方法——
  引导/事件宿主用节流轮询（0.5s）或 `_process` 快照，不用 Bean watch
