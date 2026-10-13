---
name: weather-zh
description: 获取当前天气和天气预报（无需 API 密钥）。
homepage: https://wttr.in/:help
metadata: { "openclaw": { "emoji": "🌤️", "requires": { "bins": ["curl"] } } }
---

# 天气查询

两个免费服务，无需 API 密钥。

## wttr.in（主要服务）

快速单行命令：

```bash
curl -s "wttr.in/London?format=3"
# 输出: London: ⛅️ +8°C
```

紧凑格式：

```bash
curl -s "wttr.in/London?format=%l:+%c+%t+%h+%w"
# 输出: London: ⛅️ +8°C 71% ↙5km/h
```

完整天气预报：

```bash
curl -s "wttr.in/London?T"
```

格式代码说明：
- `%c` 天气状况图标
- `%t` 温度
- `%h` 湿度
- `%w` 风速风向
- `%l` 地点名称
- `%m` 月相

使用技巧：

- URL 编码空格：`wttr.in/New+York`
- 使用机场代码：`wttr.in/JFK`
- 单位选择：`?m`（公制）`?u`（美制）
- 仅今天：`?1` · 仅当前：`?0`
- 生成 PNG 图片：`curl -s "wttr.in/Berlin.png" -o /tmp/weather.png`

## Open-Meteo（备用服务，JSON 格式）

免费、无需密钥，适合程序化调用：

```bash
curl -s "https://api.open-meteo.com/v1/forecast?latitude=51.5&longitude=-0.12&current_weather=true"
```

先查询城市的经纬度坐标，再调用 API。返回包含温度、风速、天气代码的 JSON 数据。

文档：https://open-meteo.com/en/docs

## 常用查询示例

### 查询中国城市天气

```bash
# 北京天气
curl -s "wttr.in/Beijing?format=3&lang=zh"

# 上海天气
curl -s "wttr.in/Shanghai?lang=zh"

# 广州完整预报
curl -s "wttr.in/Guangzhou?T&lang=zh"
```

### 使用说明

1. **快速查询**：使用 `format=3` 获取最简洁的天气信息
2. **详细预报**：直接访问 `wttr.in/城市名` 获取 3 天预报
3. **中文显示**：添加 `lang=zh` 参数可获取中文天气描述
4. **温度单位**：默认使用摄氏度，添加 `?u` 切换到华氏度

### 注意事项

- wttr.in 支持中文字符，但建议使用英文城市名或拼音
- 服务免费但可能有访问频率限制
- 如需更稳定的服务，可使用 Open-Meteo API
