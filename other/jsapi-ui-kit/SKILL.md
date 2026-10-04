---
name: jsapi-ui-kit
description: 百度地图官方 UI 交互组件，提供地点自动补全（PlaceAutocomplete）、地点检索（PlaceSearch）、地点详情（PlaceDetail）和路径规划（RoutePlan）组件的使用参考，快速实现地图界面，大幅提升开发效率。
version: 1.0.1
metadata:
  openclaw:
    requires:
      env: BMAP_JSAPI_KEY
    primaryEnv: BMAP_JSAPI_KEY
---

# 百度地图 jsapi-ui-kit

轻量级百度地图 UI 组件库，提供地点自动补全、地点检索、详情展示和路径规划能力。

## 什么时候使用

- 希望快速集成标准化的地图 UI 组件，无需从零开发
- 需要在地图应用中添加搜索输入框自动补全功能
- 需要在地图应用中添加地点搜索功能
- 需要展示 POI 详情信息（名称、地址、电话等）
- 需要实现驾车路径规划功能（支持多方案、途经点）

## 文档导航

- **[快速开始](references/getting-started.md)** - 安装、引入方式、基础示例
- **[PlaceAutocomplete 地点自动补全](references/place-autocomplete.md)** - 搜索输入框实时建议
- **[PlaceSearch 地点检索](references/place-search.md)** - 关键字/周边/范围检索
- **[PlaceDetail 地点详情](references/place-detail.md)** - POI 详情展示
- **[RoutePlan 路径规划](references/route-plan.md)** - 驾车路径规划（多方案、途经点、导航调起）

## 如何使用

根据用户问题查询文档导航，参考详细文档内容和API设计： 
```
references/getting-started.md
```
每个参考文件包含：

- 功能简要说明
- 完整代码示例及解释
- API 参数说明和注意事项

## 注意事项

- 必须先加载百度地图 JS API（BMap 或 BMapGL）
