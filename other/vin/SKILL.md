---
name: jisu-vin
description: 使用极速数据 VIN 车辆识别代码查询 API，通过 17 位 VIN 车架号查询车辆品牌、车型、年款、排量、机油、变速箱等信息，并支持按车型 ID 查询机油和变速箱详细数据。
metadata: { "openclaw": { "emoji": "🚗", "requires": { "bins": ["python3"], "env": ["JISU_API_KEY"] }, "primaryEnv": "JISU_API_KEY" } }
---

# 极速数据 VIN 车辆识别代码查询（Jisu VIN）

基于 [VIN 车辆识别代码查询 API](https://www.jisuapi.com/api/vin/) 的 OpenClaw 技能，支持：

- **VIN 查询**：通过 17 位 VIN 车架号查询车辆品牌、车型、年款、排量、油耗、驱动方式、轮胎规格等；
- **机油信息**：按车型 `carid` 查询机油参考用量、粘稠度、机油分类、质量等级等（`/vin/oil`）；
- **变速箱信息**：按车型 `carid` 查询变速箱型号、品牌、接口型号、加油量及相关图片等（`/vin/gearbox`）。

使用技能前需要申请数据，申请地址：https://www.jisuapi.com/api/vin/

## 环境变量配置

```bash
# Linux / macOS
export JISU_API_KEY="your_appkey_here"

# Windows PowerShell
$env:JISU_API_KEY="your_appkey_here"
```

## 脚本路径

脚本文件：`skills/vin/vin.py`

## 使用方式

### 1. 按 VIN 车架号查询车辆信息

```bash
python3 skills/vin/vin.py '{"vin":"LSVAL41Z882104202"}'
```

可选开启严格校验：

```bash
python3 skills/vin/vin.py '{"vin":"LSVAL41Z882104202","strict":1}'
```

### 2. 按车型 ID 查询机油信息（/vin/oil）

`carid` 一般来自 VIN 查询结果中的 `carlist`：

```bash
python3 skills/vin/vin.py oil 2641
```

### 3. 按车型 ID 查询变速箱信息（/vin/gearbox）

```bash
python3 skills/vin/vin.py gearbox 21617
```

## VIN 查询请求 JSON 参数

| 字段名  | 类型   | 必填 | 说明                                           |
|--------|--------|------|------------------------------------------------|
| vin    | string | 是   | 17 位 VIN 车架号                               |
| strict | int    | 否   | 是否严格校验 VIN，0 否、1 是，默认 0           |

示例：

```json
{
  "vin": "LSVAL41Z882104202",
  "strict": 0
}
```

## VIN 查询返回结果示例

脚本直接输出接口 `result` 字段，结构与官网示例一致（示例简化）：

```json
{
  "name": "大众 途锐 2017款 3.0 TSI 拓野版",
  "brand": "大众",
  "typename": "途锐",
  "logo": "http://pic1.jisuapi.cn/car/static/images/logo/300/34889.jpg",
  "manufacturer": "进口大众",
  "yeartype": "2017",
  "environmentalstandards": "国五",
  "comfuelconsumption": "10.2",
  "fueltype": "汽油",
  "gearbox": "8挡 手自一体",
  "drivemode": "全时四驱",
  "fronttiresize": "255/55 R18",
  "reartiresize": "255/55 R18",
  "displacement": "3.0T",
  "fuelgrade": "95号",
  "price": "71.88万",
  "vin": "WVGAP97P2HD030000",
  "iscorrect": 1,
  "machineoil": {
    "volume": "4.5L",
    "viscosity": "5W-30",
    "grade": "全合成",
    "level": "SN PLUS"
  },
  "carlist": [
    {
      "carid": 40411,
      "name": "大众 途锐 2017款 3.0 TSI 拓界版",
      "typeid": 767,
      "typename": "途锐"
    }
  ]
}
```

当出现错误（如 VIN 不正确或无数据），脚本会输出：

```json
{
  "error": "api_error",
  "code": 202,
  "message": "VIN不正确"
}
```

## /vin/oil 机油信息

按车型 ID 查询机油信息，调用方式：

```bash
python3 skills/vin/vin.py oil 2641
```

典型返回结构（简化自官网示例）：

```json
{
  "carid": 2641,
  "brandname": "奥迪",
  "parentname": "A4L",
  "name": "2012款 2.0 TFSI(155kW) 运动型",
  "price": "42.38万",
  "yeartype": "2012",
  "listdate": "2011-08-30",
  "productionstate": "停产",
  "salestate": "停销",
  "sizetype": "中型车",
  "machineoil": {
    "volume": "5.0L",
    "viscosity": "5W-40",
    "grade": "全合成",
    "level": "SN"
  }
}
```

## /vin/gearbox 变速箱信息

按车型 ID 查询变速箱信息，调用方式：

```bash
python3 skills/vin/vin.py gearbox 21617
```

典型返回结构（简化自官网示例）：

```json
{
  "carid": 21617,
  "brandname": "凯迪拉克",
  "parentname": "凯迪拉克CT6",
  "name": "2016款 28T 领先版",
  "price": "54.99万",
  "yeartype": "2016",
  "sizetype": "中大型车",
  "gearboxinfo": {
    "gearboxmodel": "8L90",
    "gearboxbrand": "通用",
    "joint": "HS18/HS30",
    "gravityoil": "4L",
    "mechanicaloil": "9-11L",
    "jointpiclist": [
      "http://pic1.jisuapi.cn/car/upload/gearbox/I-HS18.png"
    ],
    "positionpiclist": [
      "http://pic1.jisuapi.cn/car/upload/gearbox/TR-8L451.png"
    ]
  }
}
```

## 常见错误码

来源于 [极速数据 VIN 文档](https://www.jisuapi.com/api/vin/)：

| 代号 | 说明       |
|------|------------|
| 201  | VIN 为空   |
| 202  | VIN 不正确 |
| 210  | 没有信息   |

系统错误码：

| 代号 | 说明                 |
|------|----------------------|
| 101  | APPKEY 为空或不存在  |
| 102  | APPKEY 已过期        |
| 103  | APPKEY 无请求权限    |
| 104  | 请求超过次数限制     |
| 105  | IP 被禁止            |

## 在 OpenClaw 中的推荐用法

1. 用户给出车架号：「帮我查一下 VIN `LSVAL41Z882104202` 是什么车」。  
2. 代理构造 JSON：`{"vin":"LSVAL41Z882104202"}` 并调用：  
   `python3 skills/vin/vin.py '{"vin":"LSVAL41Z882104202"}'`  
3. 从返回中选取 `name/brand/yeartype/displacement/fueltype/drivemode` 等字段，给出自然语言总结；  
4. 如需机油或变速箱详情，可从 `carlist` 里选一个 `carid` 再调用：  
   - 机油：`python3 skills/vin/vin.py oil <carid>`  
   - 变速箱：`python3 skills/vin/vin.py gearbox <carid>`。

