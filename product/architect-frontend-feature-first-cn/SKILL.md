---
name: architect-frontend-feature-first-cn
description: 解释功能优先前端架构。按业务能力确定归属，按需分层，明确源码依赖和跨功能协作。
metadata:
  language: zh-CN
  translation_of: architect-frontend-feature-first
  version: "0.1.0"
---

# 功能优先前端架构

参考 Rémy Baudet 的 Feature-First Clean Architecture。

一个功能拥有一项业务能力及随它变化的界面、模型和数据访问。商品列表与详情可以同属 `products`。这样的划分让功能变更集中在一个模块内。

## 形状与职责

```text
<源码根>/
  app/
  features/<feature>/
    presentation/
    domain/
    data/
    application/
  shared/
```

- `presentation` 负责界面、交互和界面状态。
- `domain` 定义业务模型和规则。业务需要外部数据时，由这里定义仓库契约。
- `data` 实现仓库契约，负责外部数据访问和转换。
- `application` 编排需要协调多个操作或业务能力的用例。
- `app` 装配依赖并管理路由。`shared` 提供与具体功能无关的通用代码。

按实际职责创建目录。纯展示功能可只有 `presentation`。无界面功能可省去展示层。入口和路由沿用框架约定。

## 依赖规则

箭头表示源码依赖，相关层存在时才应用对应规则。

```text
presentation → domain
presentation → application → domain
data         → domain
```

领域规则独立于界面框架和 I/O 实现。应用入口注入实现。跨功能业务协作使用所有者公开的契约或用例，保持依赖无环。功能表达导航意图，应用路由选择目标。

## 与其他风格的区别

Feature-first 选择业务能力作为一级边界。Layer-first 优先按技术职责归档，页面优先围绕路由或屏幕归档。Clean Architecture 约束源码依赖，MVVM 组织展示层。二者都可与 Feature-first 组合。
