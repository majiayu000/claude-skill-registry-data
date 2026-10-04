---
name: bmap-jsapi-three
description: 使用 MapV-Three 构建专业的 3D 地图和 GIS 应用 - 基于 Z-up 坐标系的 3D 地图库，支持地图编辑、测量工具、要素绘制、数据管理等地理可视化功能。适用于创建地图编辑器、测量工具、空间数据可视化等 Web-GIS 应用。
license: MIT
version: 1.0.1
metadata:
  openclaw:
    requires:
      env: BMAP_JSAPI_KEY
    primaryEnv: BMAP_JSAPI_KEY
---

# MapV-Three 开发指南

使用 MapV-Three 构建高性能的 3D 地图和 GIS 应用 - 一个采用 Z-up 坐标系的跨浏览器 WebGL 库。

## 何时适用

在以下场景中参考这些指南：

- 3D 地图编辑和要素绘制
- 地图测量工具开发
- 建筑物、区域等 3D 可视化
- 实时交通数据展示
- 路径追踪动画开发

## 快速参考

### 0. 核心引擎

- `references/engine.md` - Engine 引擎核心：初始化、场景管理、渲染控制
- `references/initialization.md` - 引擎初始化、资源配置、百度地图适配器

### 1. 数据管理

- `references/datasource.md` - DataSource 数据源基类
- `references/datasource/geojson-datasource.md` - GeoJSON 数据源
- `references/datasource/json-datasource.md` - JSON 数据源
- `references/datasource/csv-datasource.md` - CSV 数据源
- `references/datasource/dataitem.md` - DataItem 数据项

### 2. 点对象与标签

- `references/simple-point.md` - SimplePoint 简单点
- `references/effect-point.md` - EffectPoint 特效点（Fan、Bubble、Wave、Breath、Radar 等）
- `references/marker-types.md` - 标记类型（Icon、BallonPoint、DOMPoint、EffectModelPoint）
- `references/circle.md` - Circle 圆形（屏幕空间渲染）
- `references/label.md` - Label 文本/图标标签
- `references/text.md` - Text 文本组件
- `references/cluster.md` - ClusterPoint 点聚合

### 3. 线与面

- `references/polyline.md` - Polyline 折线（flat 参数控制渲染模式）
- `references/simple-line.md` - SimpleLine 简单线
- `references/wall.md` - Wall 墙体/围栏
- `references/polygon.md` - Polygon 多边形
- `references/pillar.md` - Pillar 柱体

### 4. 覆盖物

- `references/marker.md` - Marker 标记
- `references/popup.md` - Popup 弹出窗口
- `references/dom-overlay.md` - DOMOverlay DOM 覆盖物

### 5. 追踪器

- `references/tracker.md` - 追踪器总览与生命周期
- `references/path-tracker.md` - PathTracker 路径追踪
- `references/object-tracker.md` - ObjectTracker 对象追踪
- `references/orbit-tracker.md` - OrbitTracker 轨道追踪

### 6. 编辑与测量

- `references/editor.md` - Editor 编辑器
- `references/measure.md` - Measure 测量工具

### 7. 3D 模型

- `references/model.md` - 3D 模型加载（SimpleModel/AnimationModel/LODModel）
- `references/twin.md` - Twin 孪生车流（实时车流可视化、DataProvider 数据处理）
- `references/mock-twin.md` - MockTwin 模拟车流（基于路线数据的车流模拟生成）

### 8. 材质与特效

- `references/materials.md` - 材质系统（WaterMaterial、ExtendMeshStandardMaterial 等）
- `references/easing-function.md` - 缓动函数（LINEAR、QUINTIC_IN_OUT、CUBIC_OUT）

### 9. 天空与天气

- `references/sky-weather.md` - 天空系统（EmptySky/DynamicSky/StaticSky）和天气

### 10. 热力图

- `references/heatmap.md` - Heatmap 热力图

### 11. 地图图层加载

- `references/imagery-tile-provider.md` - 影像瓦片加载（Baidu、Tianditu、Bing、OSM、Stadia）
- `references/vector-tile-provider.md` - 矢量瓦片加载（Baidu、Mapbox）
- `references/third-party-imagery.md` - 第三方图层接入（WMS、WMTS、XYZ 标准协议）
- `references/terrain-tile-provider.md` - 地形瓦片加载（Cesium、平面地形）
- `references/tile-mask.md` - TileMask 瓦片掩膜（按区域裁剪瓦片图层显示）

### 12. LBS 位置服务

- `references/services.md` - 位置基础服务（地理编码、搜索、路线规划、行政区划等）

### 13. 3DTiles 加载

- `references/3dtiles-loading.md` - 3D Tiles 加载（Default3DTiles、HDMap3DTiles）

### 14. 基础概念

- `references/common/coordinate-system.md` - 坐标系：Z-up、投影方式
- `references/common/event-binding.md` - 事件绑定模式

## 关键注意事项

- **引擎初始化**：`new mapvthree.Engine(container, { map: { center: [lng, lat], range: meters } })`
- **坐标系**：Z-up（X-东、Y-北、Z-上），与 Three.js 默认 Y-up 不同
- **视野控制**：使用 `range`（相机距离，米）而非 zoom
- **属性赋值**：使用属性代理 `obj.color = value`，而非 `obj.setColor(value)`
- **MeasureType**：使用 `mapvthree.Measure.MeasureType`
- **图层设置**：通过 `MapView` 设置影像/矢量/地形提供者，而非 `engine.map`
