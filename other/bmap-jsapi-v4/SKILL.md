---
name: bmap-jsapi-v4
description: 用于开发、审查或排查使用百度地图 JavaScript API 4.0、v=4.0 加载器或全局 BMap 命名空间的浏览器应用。
---

# 百度地图 JavaScript API 4.0

## 核心原则

聚焦通过 `v=4.0` 加载器和全局 `BMap` 命名空间开发浏览器地图应用，不系统介绍其他版本。

## 固定约束

- 加载地址使用 `https://api.map.baidu.com/api?v=4.0&ak=YOUR_BAIDU_MAP_AK`。
- 新代码使用全局 `BMap`，不要混用其他版本的命名空间和加载参数。
- 示例中的 `YOUR_BAIDU_MAP_AK` 需要替换为开发者自己的 AK；共享代码和日志中不要暴露真实密钥。
- 依赖 AK、在线服务、CORS、WebGL 或真实数据的结果需要在浏览器中验证。
- 创建监听器、覆盖物、控件、图层、服务渲染结果、动画、全景或 Map 时，同时给出对应的解绑、移除、取消或销毁路径。

## 工作流

1. 确认任务确实使用 `v=4.0` 和 `BMap`。
2. 只读取与需求直接相关的 reference；跨模块任务按“接入 → Map/几何 → 业务模块 → 生命周期 → 排障”加载。
3. 从 reference 选择满足需求的最小 API 组合。
4. TypeScript 安装、配置、类型报错或 `.d.ts` 补充任务同时读取 TypeScript 专页。
5. 检查版本参数、容器尺寸、异步状态、事件引用和资源清理。
6. 对网络和渲染相关结果进行真实浏览器验证。

## Reference 路由

### 接入与基础

| 任务 | 读取 |
|---|---|
| 页面加载、AK、同步/异步入口、空白地图 | [project-setup.md](references/project-setup.md) |
| Map 初始化、视野、交互、样式、旋转与倾斜 | [map-core.md](references/map-core.md) |
| 控件主题、深色模式、主题变量 | [ui-version-and-theme.md](references/ui-version-and-theme.md) |
| Point、Pixel、Size、Bounds、坐标换算 | [coordinates-and-geometry.md](references/coordinates-and-geometry.md) |
| 事件监听、解绑、组件销毁 | [events-and-lifecycle.md](references/events-and-lifecycle.md) |
| 内置/自定义控件与右键菜单 | [controls-and-context-menu.md](references/controls-and-context-menu.md) |

### 覆盖物

| 任务 | 读取 |
|---|---|
| Marker、Icon、Symbol、拖拽与事件 | [marker.md](references/marker.md) |
| Label、InfoWindow、内容更新与关闭 | [label-and-info-window.md](references/label-and-info-window.md) |
| Polyline、Polygon、Rectangle、Circle 与编辑 | [vector-overlays.md](references/vector-overlays.md) |
| CustomOverlay、GroundOverlay、Prism、BezierCurve、PlaceDetail | [advanced-overlays.md](references/advanced-overlays.md) |

### 图层与可视化

| 任务 | 读取 |
|---|---|
| GeoJSON、GeoJSONParse、DOMLayer、地图文字 | [data-layers.md](references/data-layers.md) |
| MVT 矢量瓦片、样式与要素状态 | [mvt-layer.md](references/mvt-layer.md) |
| PointIcon、PointShape、Line、Fill 批量图层 | [visualization-layers.md](references/visualization-layers.md) |
| Heatmap、PointLayer、ClusterLayer、TrackLine、Icons 等扩展 API | [runtime-extended-apis.md](references/runtime-extended-apis.md) |
| Tile、XYZ、Raster、WMS、WMTS、Traffic、全景覆盖层 | [tile-and-service-layers.md](references/tile-and-service-layers.md) |
| 行政区边界与 DistrictLayer | [administrative-district.md](references/administrative-district.md) |

### 服务与视图

| 任务 | 读取 |
|---|---|
| LocalSearch、Autocomplete、Geocoder | [search-and-geocoding.md](references/search-and-geocoding.md) |
| 驾车、步行、骑行、公交与公交线检索 | [route-search.md](references/route-search.md) |
| Geolocation、LocalCity、Convertor | [geolocation-and-convertor.md](references/geolocation-and-convertor.md) |
| Panorama、PanoramaService、PanoramaLabel | [panorama.md](references/panorama.md) |
| ViewAnimation、关键帧与取消 | [view-animation.md](references/view-animation.md) |

### 工程集成

| 任务 | 读取 |
|---|---|
| `@baidumap/jsapi-v4-types`、全局类型、tsconfig、声明补充 | [typescript-integration.md](references/typescript-integration.md) |
| 性能、容器、坐标、瓦片、CORS、事件和内存排障 | [performance-and-troubleshooting.md](references/performance-and-troubleshooting.md) |

## 输出契约

- 先给结论，再给最小完整代码和必要说明。
- 在线服务先判断状态码与空结果；异步回调考虑组件已经卸载或请求已经过期。
- 清理顺序遵循“停止业务异步 → 解绑事件 → 移除子资源 → 销毁 Map”。
- 只在避免核心 API 误用确有必要时，用一句话说明旧写法差异；版本迁移不能成为答案主线。
- 语法或类型检查通过不等于 AK、网络、CORS、WebGL 和在线数据已经运行成功。

## 常见错误

- 混用其他版本的加载参数、命名空间或示例。
- 根据类名猜测构造参数、事件或清理方法。
- 把类型检查通过当成浏览器运行成功。
- 用匿名函数分别注册和移除同一个事件。
- 只添加覆盖物或图层，不保存引用并移除。
- 忽略异步服务的失败状态、空结果或迟到回调。
