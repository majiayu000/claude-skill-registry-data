---
name: "godot-rust"
description: "Godot-Rust (gdext 0.5.x) API 使用指南、常见陷阱与最佳实践。在编写 Rust GDExtension 代码、使用 gdext 绑定、或遇到 gdext 编译/运行时问题时调用。"
---

# Godot-Rust (gdext 0.5.x) 开发指南

基于 gdext 0.5.3 的实战经验整理，涵盖 API 用法、易错点和最佳实践。

## 文档索引

| 文件 | 主题 | 关键内容 |
|------|------|----------|
| [01-class-definition.md](file:///Users/dengronghui/project/gamekit/gamecore/.trae/skills/godot-rust/01-class-definition.md) | 类定义与注册 | `#[derive(GodotClass)]`、`#[var]`/`#[var(pub)]`、`#[func]`、虚方法重写、信号定义 |
| [02-objects-and-types.md](file:///Users/dengronghui/project/gamekit/gamecore/.trae/skills/godot-rust/02-objects-and-types.md) | 对象创建与类型转换 | `new_gd()`、`from_init_fn()`、upcast/downcast、`call()`/`call_deferred()`、ByValue/ByOption 类型不匹配 |
| [03-borrow-checker.md](file:///Users/dengronghui/project/gamekit/gamecore/.trae/skills/godot-rust/03-borrow-checker.md) | 借用检查器 | `bind()`/`bind_mut()` 冲突、克隆避免借用冲突、let-else 模式 |
| [04-collections.md](file:///Users/dengronghui/project/gamekit/gamecore/.trae/skills/godot-rust/04-collections.md) | 集合类型 | VarDictionary、Array、Variant 类型转换 |
| [05-signals.md](file:///Users/dengronghui/project/gamekit/gamecore/.trae/skills/godot-rust/05-signals.md) | 信号连接 | `connect_flags()`、`emit_signal()`、ConnectFlags |
| [06-resources.md](file:///Users/dengronghui/project/gamekit/gamecore/.trae/skills/godot-rust/06-resources.md) | 资源创建 | 内联 ShaderMaterial、`from_init_fn()` 创建对象 |
| [07-engine-api.md](file:///Users/dengronghui/project/gamekit/gamecore/.trae/skills/godot-rust/07-engine-api.md) | 引擎 API | 版本检测、编辑器检测、输入处理 |
| [08-tilemap-layer.md](file:///Users/dengronghui/project/gamekit/gamecore/.trae/skills/godot-rust/08-tilemap-layer.md) | TileMapLayer API | `set_cell_ex` 构建器、虚方法列表、属性复制、API 名称差异 |
| [09-architecture.md](file:///Users/dengronghui/project/gamekit/gamecore/.trae/skills/godot-rust/09-architecture.md) | 架构模式 | 循环依赖处理（基类类型 + call()） |
| [10-imports-and-best-practices.md](file:///Users/dengronghui/project/gamekit/gamecore/.trae/skills/godot-rust/10-imports-and-best-practices.md) | 导入与最佳实践 | 常用导入清单、8 条最佳实践 |

## 快速查找

- **如何定义类？** → [01-class-definition.md](file:///Users/dengronghui/project/gamekit/gamecore/.trae/skills/godot-rust/01-class-definition.md)
- **`#[var]` vs `#[var(pub)]`？** → [01-class-definition.md](file:///Users/dengronghui/project/gamekit/gamecore/.trae/skills/godot-rust/01-class-definition.md)
- **`#[var(get, set)]` 自定义 getter/setter（Option<Gd<T>>）？** → [01-class-definition.md](file:///Users/dengronghui/project/gamekit/gamecore/.trae/skills/godot-rust/01-class-definition.md)
- **`#[func]` 方法跨模块调用报错？** → [01-class-definition.md](file:///Users/dengronghui/project/gamekit/gamecore/.trae/skills/godot-rust/01-class-definition.md)
- **虚方法 `_update_cells` 不被调用？** → [08-tilemap-layer.md](file:///Users/dengronghui/project/gamekit/gamecore/.trae/skills/godot-rust/08-tilemap-layer.md)
- **`set_tile_set` 类型不匹配？** → [02-objects-and-types.md](file:///Users/dengronghui/project/gamekit/gamecore/.trae/skills/godot-rust/02-objects-and-types.md)
- **`call_deferred` 参数类型错误？** → [02-objects-and-types.md](file:///Users/dengronghui/project/gamekit/gamecore/.trae/skills/godot-rust/02-objects-and-types.md)
- **如何扫描子节点并按名称分类？** → [02-objects-and-types.md](file:///Users/dengronghui/project/gamekit/gamecore/.trae/skills/godot-rust/02-objects-and-types.md)
- **如何动态创建子节点并添加到场景树？** → [02-objects-and-types.md](file:///Users/dengronghui/project/gamekit/gamecore/.trae/skills/godot-rust/02-objects-and-types.md)
- **批量同步属性到子节点（Variant clone）？** → [02-objects-and-types.md](file:///Users/dengronghui/project/gamekit/gamecore/.trae/skills/godot-rust/02-objects-and-types.md)
- **`self.base_mut()` 借用冲突？** → [03-borrow-checker.md](file:///Users/dengronghui/project/gamekit/gamecore/.trae/skills/godot-rust/03-borrow-checker.md)
- **循环中遍历 Vec<Gd<T>> 同时访问 self 其他字段？** → [03-borrow-checker.md](file:///Users/dengronghui/project/gamekit/gamecore/.trae/skills/godot-rust/03-borrow-checker.md)
- **VarDictionary::get() 返回类型？** → [04-collections.md](file:///Users/dengronghui/project/gamekit/gamecore/.trae/skills/godot-rust/04-collections.md)
- **循环依赖怎么处理？** → [09-architecture.md](file:///Users/dengronghui/project/gamekit/gamecore/.trae/skills/godot-rust/09-architecture.md)
