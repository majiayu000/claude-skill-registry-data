---
name: recruiting-source-hunting
description: Find official campus-recruiting application links and JD details by checking existing structured data first, then searching authoritative sources (university career sites, company-built job portals, Moka/Beisen/Feishu systems), and cross-verifying before writing anything down. Use when filling in company job links, verifying whether a company has an open 2027 campus batch, or checking a JD is current.
version: 1.0.0
---

# Recruiting Source Hunting

Get the *real* application link and *current* JD. The failure mode isn't "can't find it" —
it's **finding something wrong and writing it down with confidence**.

## Rule 0: Take it from where the data already is

🔴 **别绕远路去全网搜，先看手上的结构化数据里有没有现成字段。**

真实教训：用户要「每家公司都能点开直达投递页」。我二话不说跑去全网搜，被骂「蠢猪 / 搜啥啊 / 这表里不是有吗」——
原始表里 **536/539 条自带 `applyUrl` 字段**，一行都没用上。

```python
# 先解析原始表，看有哪些字段
s = open('原始表.html', encoding='utf-8').read()
i = s.find('const COMPANIES'); j = s.find('[', i)
data, _ = json.JSONDecoder().raw_decode(s[j:])
print(len(data), list(data[0].keys()))
```

🔴 **grep 零命中 ≠ 里面没有。** 我曾 grep `name:` 一无所获就下结论「原始表里没有公司名称」——
实际字段名是 `company`。先打印一条记录看结构，再下判断。

## Source tiers

按可靠性排序，**从高往低查**：

| 层级 | 来源 | 特点 |
|---|---|---|
| 1 | 公司**自建招聘站**（`hr.g-bits.com`、`campus.geely.com`、`u.4399.com/hr`） | 最准，且常能直接抓到 JD 正文 |
| 2 | **高校就业网**（`career.*.edu.cn`、`*bysjy.com.cn`、`*91job.org.cn`、`*91job.org.cn`） | 官方公告原文，专业/学历/流程最准，**常带内推码** |
| 3 | 第三方职位库（`watchjobs.net`、`nowcoder.com`、`niuqizp.com`） | JD 全文、内推码、截止日期 |
| 4 | 搜索引擎兜底 | **只在前三层都查不到时用** |

### 高校就业网的额外价值

一条招聘公告通常覆盖：面向对象 / 毕业时间要求 / 岗位类别 / 工作地点 / 招聘流程 / **投递方式（含 PC 端直达链接）** / 联系邮箱。
一份公告顶十次搜索。而且**同一条链接在三所不同高校就业网上一致**，可信度就够高了。

### 企业招聘系统的 URL 参数

搜到官方链接时先看 URL 参数，**里面常藏着内推码**：

| 系统 | 参数 | 例 |
|---|---|---|
| Moka | `recommendCode=` | `?recommendCode=DS76qFFH` |
| 飞书招聘 | `spread=` | `&spread=MYEW6ZE` |
| 北森 zhiye | `?KeyWords=` | 该页面常被搜索引擎收录完整 JD |

## Cross-verification before writing

🔴 **单一来源不落笔。** 找到链接后至少确认两件事：

1. **可达性**：`curl -sI -A "Mozilla/5.0" -L <url>` 看状态码
   - 200 = 正常；302 = 重定向（正常）；403/404 = 不能用，换一个
2. **交叉验证**：同一链接/信息在**两处以上独立来源**一致（如两所不同高校就业网）

抽查样本要覆盖新填的链接，别只抽查顺手的几个。

## Don't fake it with fallback

🚫 **搜索兜底不是答案。** 用户要「全部都能打开」，给 467 家塞百度搜索链接 = 没干活。

- 先穷尽 tier 1-3
- 只有**确认查不到**的才走兜底
- **兜底数量要作为指标报出来**（551 直达 / 4 邮箱 / 1 兜底），让用户一眼看出还有多少没补全

## Uncertain company names

用户手打的公司名可能是缩写/错字（`fmg` = FMG时尚动势集团，`51word` = 51WORLD，`虾皮` = Shopee）。

处理：
1. 先按名字搜，**用上下文缩小范围**（前后相邻的公司、行业、城市）
2. 交叉验证（官网 / BOSS直聘公司介绍 / 高校就业网公告）
3. 🔴 **确认不了就直接问用户，别猜**。猜错公司 = 后面所有筛选和链接全错

## Red flags

- 🚫 跳过手上的结构化数据直接全网搜
- 🚫 拿搜索兜底当答案交差
- 🚫 单一来源就落笔
- 🚫 拿「需求人数」当「岗位数」（高校就业网常混用，差好几倍）
- 🚫 用过期 JD（看 URL 里的日期戳、页面发布日期）
- 🚫 猜公司名
