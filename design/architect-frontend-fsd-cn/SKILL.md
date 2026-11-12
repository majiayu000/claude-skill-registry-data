---
name: architect-frontend-fsd-cn
description: 解释前端 Feature-Sliced Design（FSD）的层、切片、段、公开 API 与依赖边界。
metadata:
  language: zh-CN
  translation_of: architect-frontend-fsd
  version: "0.1.0"
---

# 前端 Feature-Sliced Design

依据 Feature-Sliced Design 官方规范。

FSD 按职责划层，在层内按产品语义划分切片，再按代码用途划分段。切片把一起变化的代码放在同一处，公开 API 让调用方依赖稳定入口。

## 架构形状

```text
<源码根>/
  app/routes/
  pages/product-details/{ui,api}/
  widgets/product-gallery/ui/
  features/add-to-cart/{ui,model}/
  entities/product/{model,ui}/
  shared/{ui,api}/
```

| 层 | 职责 |
|---|---|
| `app` | 应用入口、路由、全局样式与依赖装配。 |
| `pages` | 完整页面或主要路由内容，包含页面专用界面、状态和请求。 |
| `widgets` | 独立的大块界面，可供多个页面复用，也可承担页面内的独立区域。 |
| `features` | 可复用、具有业务价值的用户操作，例如加入购物车。 |
| `entities` | 业务实体及其模型、数据访问或界面表示，例如商品。 |
| `shared` | 通用界面组件、API 客户端、配置和基础库。 |

`app` 和 `shared` 直接分段。其余各层先分切片，再分段。常用段包括 `ui`（界面）、`model`（状态与规则）、`api`（外部交互）、`lib`（辅助库）和 `config`（配置）。层与段按实际职责使用。`processes` 已弃用。

## 依赖边界

- 层级从高到低为 `app → pages → widgets → features → entities → shared`。跨切片导入只指向严格更低的层，可跳过中间层。同一切片内部可以互相引用，`app` 和 `shared` 各自的段也可在本层内协作。
- 从切片外部访问时，只使用该切片的公开 API。`app` 和 `shared` 的段同样提供公开入口。显式导出调用方需要的内容，切片内部引用直接指向内部模块。
- 同层切片的组合由更高层负责。实体间确有直接模型关系时，可用 `@x` 为指定实体提供专用公开入口。例如 `entities/product/@x/order` 供 `entities/order` 使用。

## 页面优先

页面专用的界面、状态和请求留在页面切片。商品详情的专用请求放在 `pages/product-details/api`。当多个页面复用加入购物车操作时，由 `features/add-to-cart` 承担该行为。各页面通过公开入口组合它。

## 与 Feature-first 的区别

Feature-first 通常先按业务能力划分模块，再在模块内部按职责分层。FSD 先定义全局层级，再在各层内按产品语义划分切片，并用层级规则约束跨切片导入。
