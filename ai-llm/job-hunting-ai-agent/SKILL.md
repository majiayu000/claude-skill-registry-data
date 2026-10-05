---
name: job-hunting-ai-agent
description: Search and filter AI Agent / LLM internship positions in Shanghai for a 2024-cohort AI undergraduate. Covers company lists (955.WLB, 996.ICU), known job links, search strategy, and pitfalls.
category: career
---

# AI Agent 实习岗位搜索方法论

## 适用场景
用户要找上海 AI Agent / 大模型方向的日常实习，中大型公司优先。

## 背景知识

### 关键项目与名单
- **955.WLB**：`github.com/formulahendry/955.WLB` — 955 外企白名单，上海外企密集（Google/Apple/Amazon/MS/AMD/NVIDIA/SAP/PayPal等50+家）
- **996.ICU**：`github.com/996icu/996.ICU` — 996 黑名单，数据较老（2019），小红书/拼多多/依图等在列
- 上海大厂梯队：拼多多（最卷）> 字节/阿里/蚂蚁 > 腾讯/百度 > 携程（较温和）

### 上海大厂分布
| 公司 | 区 | 方向 |
|------|------|------|
| 拼多多 | 长宁 | 电商 |
| 携程 | 长宁 | 旅行 |
| 字节 | 闵行 | 抖音/国际化 |
| 阿里 | 闵行 | 盒马/本地生活 |
| 蚂蚁 | 浦东 | 支付/AI |
| 腾讯 | 徐汇 | 游戏/AI/云 |
| B站 | 杨浦 | 视频/AI |
| 米哈游 | 徐汇 | 游戏/AI |
| 小红书 | 黄浦 | 内容电商 |

### 2026 招聘大年数据
- 字节：7000+ 实习，转正率 55%，研发日薪 500 元
- 腾讯：10000+ 实习，AI 大幅扩招
- 阿里：16 个 BU 同步，AI 岗位占比 80%+
- 蚂蚁：技术岗 85%，新增智能体方向
- 美团：3000+ 转正实习

## 搜索策略

### 1. 先用 MCP jobs 工具搜
```
mcp_jobs_mcp_search_job(keyword="AI Agent 实习", city="上海")
mcp_jobs_mcp_search_job(keyword="大模型 实习", city="上海")
```
> 注意：MCP jobs 工具覆盖有限，常有空结果。不依赖此工具。

### 2. 再用 web_search 搜大方向
```
"上海 AI Agent 实习生 招聘 2025 2026 大厂 字节 蚂蚁 腾讯"
"字节跳动 上海 AI Agent 实习生 投递 岗位"
"腾讯 阿里 蚂蚁 上海 AI Agent 大模型 实习生"
```

### 3. 直接查公司官网
- 字节：`jobs.bytedance.com/campus`
- 腾讯：`careers.tencent.com`
- 阿里/阿里云：`careers.aliyun.com/campus`
- 蚂蚁：`antgroup.com`
- B站：`jobs.bilibili.com/campus`
- 米哈游：牛客/内推渠道更有效

### 4. 上海本地特色渠道
- B站日常实习页面：`jobs.bilibili.com/campus/positions?type=0`
- 牛客网搜"上海+AI+实习"
- 脉脉/应届生求职网

## 已知的具体岗位（截至2026年6月）

| 公司 | 岗位 | 链接 |
|------|------|------|
| 字节 | AI Agent 开发实习生-计算 | jobs.bytedance.com 搜 ID 7600764543892031749 |
| 字节 | AI Agent 开发实习生-抖音平台 | jobs.bytedance.com 搜 ID 7591478820613671221 |
| 字节 | AI 研发实习生-数据与安全 | jobs.bytedance.com 搜 ID 7637457056367298869 |
| 字节 Seed | 通用 Agent 算法工程师 | seed.bytedance.com/zh/career |
| 蚂蚁 | 算法工程师-智能体 | antgroup.com |
| B站 | 视频大模型算法实习生 | jobs.bilibili.com/campus |
| 米哈游 | AI 研发工程师（暑期） | 牛客内推贴 732564788236029952 |

## ⚠️ 关键卡点

### 毕业年份限制
- 用户是 **2024 级（2028 届）**，大厂暑期/转正实习多要求 **2027 届**
- **日常实习**（非暑期/转正项目）通常不严格限毕业年份
- B站、蚂蚁日常实习对年级限制更宽松
- 字节 ByteIntern 明确要 2027 届，但部分日常实习岗位可放宽

### 上海住宿问题
上海 tech 行业明确提供住宿的公司极少——华为（青浦员工公寓）是唯一大厂+AI方向+包住宿的组合。详见 `references/shanghai-housing-companies.md`。

### 第一份实习的策略
大二结束找第一份实习的 KPI **不是转正**，而是让第二份实习能投进更好的公司：
1. 冲华为（有宿舍+AI对口+品牌）
2. B站/小红书/携程日常实习（学历要求相对宽松）
3. 中厂/创业公司 AI Agent 方向（积累经验→跳大厂暑期实习）
大三暑期（2027年夏天）才是真正的转正窗口，届时正好对口2028届。

### 网络问题
- 需要时设置代理：`HTTP_PROXY=http://127.0.0.1:7890`
- `curl`/`web_extract` 遇到超时先用代理重试

## 后续可做的
1. 打开具体岗位 JD 看投递条件
2. 对比简历做匹配分析
3. 用BOSS直聘/脉脉/实习僧搜更多渠道
4. 准备 AI Agent 相关项目经历（Hermes/OpenClaw/MCP/Agent 框架）
