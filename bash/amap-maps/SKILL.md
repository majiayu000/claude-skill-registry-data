---
slug: amap-maps
version: 1.0.0
displayName: 高德地图
summary: 高德地图 API 集成，提供地理编码、天气查询、路径规划等功能
tags: 高德, 地图, 地理编码, 天气, 路径规划
---

# 高德地图 Skill

通过高德地图 Web API 提供地理信息服务。所有脚本零外部依赖（仅用 Python 标准库）。

## 前置检查

**Step 1: 检查 API Key**

运行任意脚本（如 `python3 scripts/amap_weather.py 北京`）。
- 成功返回 JSON → 环境就绪，跳到「使用指南」
- 报 `AMAP_MAPS_API_KEY environment variable is not set` → 执行 Step 2
- 报 `INVALID_USER_KEY` → Key 无效，要求用户重新提供，重新执行 Step 2

**Step 2: 引导用户配置 Key**

告知用户：
1. 打开 https://lbs.amap.com/api/webservice/create-project-and-key
2. 注册/登录 → 创建应用 → 添加 Key（服务平台选「Web服务」）
3. 复制 Key

拿到 Key 后，在当前 session 中执行：
```bash
export AMAP_MAPS_API_KEY="用户提供的Key"
```
再次运行 Step 1 验证。

## 可用工具

| 脚本 | 功能 | 用法 |
|------|------|------|
| `amap_geo.py` | 地址 → 经纬度 | `python3 scripts/amap_geo.py "地址" [城市]` |
| `amap_regeo.py` | 经纬度 → 地址 | `python3 scripts/amap_regeo.py lng,lat` |
| `amap_weather.py` | 天气预报 | `python3 scripts/amap_weather.py 城市名或adcode` |
| `amap_search.py` | 关键词搜索 POI | `python3 scripts/amap_search.py "关键词" --city 城市` |
| `amap_around.py` | 周边搜索 | `python3 scripts/amap_around.py lng,lat --keywords 关键词 --radius 米` |
| `amap_detail.py` | POI 详情 | `python3 scripts/amap_detail.py POI_ID` |
| `amap_direction.py` | 路径规划 | `python3 scripts/amap_direction.py 模式 起点lng,lat 终点lng,lat` |
| `amap_distance.py` | 距离测量 | `python3 scripts/amap_distance.py 起点lng,lat 终点lng,lat [--type 0\|1\|3]` |
| `amap_ip.py` | IP 定位 | `python3 scripts/amap_ip.py IP地址` |

## 工作流

大多数用户请求需要组合多个脚本。以下是典型场景：

### 场景 1：路径规划（用户给地名，非坐标）

```
用户："从西湖到灵隐寺怎么走"
1. amap_geo.py "西湖" 杭州       → 获取起点坐标
2. amap_geo.py "灵隐寺" 杭州     → 获取终点坐标
3. amap_direction.py driving 起点坐标 终点坐标 → 路线
```

### 场景 2：附近搜索（用户给地名，非坐标）

```
用户："望京SOHO附近有什么咖啡店"
1. amap_geo.py "望京SOHO" 北京   → 获取中心坐标
2. amap_around.py 坐标 --keywords 咖啡 --radius 1000 → 结果列表
```

### 场景 3：出行决策（天气 + 路线组合）

```
用户："明天去西湖，天气怎么样，从我这儿怎么过去"
1. amap_weather.py 杭州           → 明日天气
2. 确认用户出发地（如未提供）
3. amap_geo.py 转坐标 × 2
4. amap_direction.py 规划路线
→ 组合输出：天气 + 路线建议
```

### 场景 4：公交路线

公交模式需要额外传城市参数：
```bash
python3 scripts/amap_direction.py transit 起点坐标 终点坐标 --city 北京 --cityd 北京
```
跨城公交时 `--city` 和 `--cityd` 分别填起终点城市。

### 关键原则

- 用户给**地名**时，先用 `amap_geo.py` 转坐标再调其他脚本
- 用户给**经纬度**时，直接调目标脚本
- 用户未指定城市时，用对话上下文推断；推断不了就问
- `amap_distance.py --type` 选择：`0`=直线距离，`1`=驾车距离（默认），`3`=步行距离

## 输出规范

所有脚本返回 JSON。向用户汇报时按场景格式化：

**路径规划**：
```
🚗 驾车路线：望京SOHO → 国贸
📏 距离：8.2 km | ⏱ 预计 25 分钟
路线：望京街 → 阜通东大街 → 京密路 → 东三环
```

**天气查询**：
```
📍 杭州未来三天天气：
- 周一：晴 🌤 12~22°C 东南风
- 周二：多云 ⛅ 14~20°C 南风
- 周三：小雨 🌧 10~16°C 东风
```

**POI 搜索 / 周边搜索**：
```
📍 望京SOHO 1km 内咖啡店（共 8 家）：
1. 星巴克（望京SOHO店）— 120m
2. Manner Coffee — 350m
3. Peet's Coffee — 580m
...
```

**地理编码**：
```
📍 "望京SOHO" → 116.481028, 39.989643（北京市朝阳区阜通东大街）
```

## 错误处理

| 错误 | 自行尝试 | 都失败后告知用户 |
|------|----------|-----------------|
| `INVALID_USER_KEY` | — | Key 无效或过期，请重新获取 |
| 地理编码无结果 | 1. 简化地址重试（去掉门牌号）2. 加城市限定重试 | 地址无法识别，请提供更详细地址 |
| POI 搜索无结果 | 1. 换同义关键词重试 2. 扩大搜索半径（+500m）| 该区域未搜到相关结果 |
| 路径规划失败 | 1. 检查坐标是否反了（应为 lng,lat 非 lat,lng）2. 换 walking 模式试 | 路线不可达，可能两点间无可行道路 |
| 网络超时 | 等待 3 秒后重试一次 | API 连接超时，请检查网络 |
