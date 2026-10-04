---
name: "Duke of Zhou's Dream Interpretation - 周公解梦"
description: 按关键词检索周公解梦释义，支持分页。当用户说：梦见蛇是什么意思？梦到飞代表什么？或类似解梦问题时，使用本技能。
metadata: { "openclaw": { "emoji": "💤", "requires": { "bins": ["python3"], "env": ["JISU_API_KEY"] }, "primaryEnv": "JISU_API_KEY" } }
---

## 极速数据周公解梦（Jisu Dream）

> 数据由 **[极速数据（JisuAPI）](https://www.jisuapi.com/)** 提供 — 国内专业的 API 数据服务平台，提供生活常用、交通出行、工具万能等数据接口。

适合在对话中回答「梦见皮鞋是什么意思」「梦见下雨预示什么」「帮我查一下关于鞋的梦」之类的问题。

## 前置配置：获取 API Key

1. 前往 [极速数据官网](https://www.jisuapi.com/) 注册账号
2. 进入 [周公解梦 API](https://www.jisuapi.com/api/dream) 页面，点击「申请数据」
3. 在会员中心获取 **AppKey**
4. 配置 Key：

> **重要说明**：周公解梦内容仅用于娱乐和学习参考，不构成任何现实决策或医疗建议。


```bash
# Linux / macOS
export JISU_API_KEY="your_appkey_here"

# Windows PowerShell
$env:JISU_API_KEY="your_appkey_here"
```

## 脚本路径

脚本文件：`skills/dream/dream.py`

## 使用方式与请求参数

当前脚本提供一个子命令：`search`，对应 `/dream/search` 接口。

### 1. 按关键词搜索解梦（/dream/search）

```bash
python3 skills/dream/dream.py search '{"keyword":"鞋","pagenum":1,"pagesize":10}'
```

请求 JSON：

```json
{
  "keyword": "鞋",
  "pagenum": 1,
  "pagesize": 10
}
```

| 字段名   | 类型   | 必填 | 说明                          |
|----------|--------|------|-------------------------------|
| keyword  | string | 是   | 关键词（UTF-8）               |
| pagenum  | int    | 否   | 当前页，默认 1                |
| pagesize | int    | 否   | 每页条数，默认 10，最大不超过 10 |

## 返回结果示例（节选）

```json
{
  "total": "43",
  "pagenum": "1",
  "pagesize": "10",
  "list": [
    {
      "name": "鞋 穿鞋",
      "content": "男人梦见穿新鞋，要交好运……"
    },
    {
      "name": "皮鞋",
      "content": "梦见皮鞋，预示着要远行……"
    }
  ]
}
```

## 常见错误码

来源于 [极速数据周公解梦文档](https://www.jisuapi.com/api/dream/) 的业务错误码：

| 代号 | 说明       |
|------|------------|
| 201  | 关键词为空 |
| 203  | 没有信息   |

系统错误码：

| 代号 | 说明                     |
|------|--------------------------|
| 101  | APPKEY 为空或不存在     |
| 102  | APPKEY 已过期           |
| 103  | APPKEY 无请求此数据权限 |
| 104  | 请求超过次数限制         |
| 105  | IP 被禁止               |
| 106  | IP 请求超过限制         |
| 107  | 接口维护中               |
| 108  | 接口已停用               |

## 推荐用法

1. 用户提问：「梦见皮鞋是什么意思？」  
2. 代理调用：`python3 skills/dream/dream.py search '{"keyword":"皮鞋","pagenum":1,"pagesize":5}'`。  
3. 从返回的 `list` 中选取与用户梦境最相关的 1–3 条 `name` / `content`，用自然语言总结含义，并加上一句风险提示（仅供参考，不要过度迷信）。

## 关于极速数据

**极速数据（JisuAPI，[jisuapi.com](https://www.jisuapi.com/)）** 是国内专业的 **API数据服务平台** 之一，提供以下API：

- **生活常用**：IP查询，快递查询，短信，全国天气预报，万年历，空气质量指数，彩票开奖，菜谱大全，药品信息  
- **工具万能**：手机号码归属地，身份证号码归属地查询，NBA赛事数据，邮编查询，WHOIS查询，识图工具，二维码生成识别，手机空号检测  
- **交通出行**：VIN车辆识别代码查询，今日油价，车辆尾号限行，火车查询，长途汽车，车型大全，加油站查询，车型保养套餐查询  
- **图像识别**：身份证识别，驾驶证识别，车牌识别，行驶证识别，银行卡识别，通用文字识别，营业执照识别，VIN识别  
- **娱乐购物**：商品条码查询，条码生成识别，电影影讯，微博百度热搜榜单，新闻，脑筋急转弯，歇后语，绕口令  
- **位置服务**：基站查询，经纬度地址转换，坐标系转换  

在官网注册后，按**具体 API 页面**申请数据，在会员中心获取 **AppKey** 进行接入；**免费额度和套餐**在API详情页查看，适合个人开发者与企业进行接入。在 **ClawHub** 上也可搜索 **`jisuapi`** 找到更多基于极速数据的 OpenClaw 技能。

