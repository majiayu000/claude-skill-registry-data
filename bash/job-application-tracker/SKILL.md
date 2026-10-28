---
name: job-application-tracker
description: Track campus-recruiting job applications in a single-file HTML ledger — status model, 100% clickable company links with three visual tiers, visited receipts, and safe incremental merging of user-exported backups without creating duplicate companies. Use when the user maintains or extends a job application tracking table.
version: 1.0.0
---

# Job Application Tracker

Track *what you already applied to*. This is downstream of `job-application-screener`
(which decides *whether* to apply). Don't merge them.

## Data model

One record per company:

| 字段 | 含义 |
|---|---|
| `n` | 公司名（唯一键） |
| `c` | 行业 |
| `s` | 状态 |
| `j` | 投递岗位数 |
| `d` | 截止日期 |
| `l` | 地点 |
| `k` | 内推码 |
| `o` | 备注 |
| `url` | **专属投递链接字段**（别塞备注里） |
| `a` | 是否归档 |
| `h` | 是否有历史变更 |

## Status enum — 语义不同的状态不许合并

```
已投 → 笔试 → 面试 → Offer
     ↘ 挂了
无岗        ← 官方还没开岗，**不是**"没投"
待查验      ← 信息待核实，**不是**"没投"
```

🔴 **`无岗` 和 `待查验` 绝不能合并进 `未投`。**
曾经为了图省事把 366 家「无岗」统一标成「未投」，结果用户筛「未投」时看到的全是压根没开岗的公司，台账直接失去意义。

## The 100% clickable rule

**每一行的公司名都必须能点开。** 有 4 家公司点了没反应，用户就会认为整张表是坏的。

三档视觉区分（让人在点之前就知道会发生什么）：

| 档 | 判定 | 样式 | 角标 |
|---|---|---|---|
| 网页直达 | `url` 字段 / 备注里有 http | 主题色 + 实线下划 | `↗` |
| 邮箱投递 | 有 `mailto:` | 灰色 + 点线 | `✉` |
| 搜索兜底 | 以上都没有 | 灰色 + 虚线 | `⌕` |

搜索兜底**必须是最后手段**，不能拿它交差：

```js
function searchUrl(name){
  var q = encodeURIComponent(name + ' 2027届校园招聘 官方投递');
  return 'https://www.baidu.com/s?wd=' + q;
}
```

## Incremental backup merging

用户在外面改完数据导出备份发回来 → **备份 = 最新真相**，用它重建底表：

```bash
python scripts/merge_backup.py <备份.json> [底表.json]
```

### 匹配顺序（顺序错了就会并出重复公司）

```
1. 精确名                  "携程" == "携程"
2. 括号内简称              "四三九九(4399)" → "四三九九"
3. 规范化名                norm() 之后相等
4. 双向包含（最后手段）     "携程旅行" ⊃ "携程"
```

🔴 **「携程旅行」「四三九九(4399)」「合众新能源汽车（哪吒汽车）」如果不按顺序匹配，会被当成新公司，台账里出现两条。**

更隐蔽的坑：这些公司在旧版本里**不是没有，是被标成 0 岗位 / 无岗**。正确处理是**补岗位数**，不是新增记录。

### 保守归一化

```python
def norm(s):
    s = re.sub(r"[（(].*?[)）]", "", s)          # 去括号内容
    s = s.replace(" ", "").replace("\u3000", "")
    s = re.sub(r"(股份有限公司|有限公司|股份公司)$", "", s)
    return s
```

🔴 **只去这三个后缀。绝不去「集团 / 科技 / 技术 / 网络」** —— TCL科技 ≠ TCL，锐捷网络 ≠ 锐捷。
底表内部归一化撞名必须报错，不能静默通过。

## Visited receipt

点过的公司名变灰，靠 localStorage 单独存：

```js
var VKEY = KEY + '_visited';
function markVisited(id){
  var v = JSON.parse(localStorage.getItem(VKEY) || '{}');
  v[id] = 1; localStorage.setItem(VKEY, JSON.stringify(v));
}
```

和主数据分开存 —— 清数据时不会连带清掉「投过没投过」的记录。

## Workflow

1. **先备份当前底表**（`cp _merged_seed.json _merged_seed.bak_YYYYMMDD.json`）
2. 跑 `merge_backup.py` 合并用户备份
3. 跑 diff 看新增了什么、变更了什么
4. **补全新公司的投递链接**（新公司通常不在原始表里，要单独搜）
5. 重跑构建
6. **跑假 DOM 冒烟测试**，重点验「无 href 数 = 0」

## Red flags

- 🚫 用黑名单正则提取 URL（会把中文一起吞了，链接失效）
- 🚫 把链接塞进备注字段（备注有别的用途，会互相污染）
- 🚫 改了底表不 bump SEED_VERSION（老用户看到旧数据）
- 🚫 用搜索兜底覆盖「本来能查到直达链接」的公司
- 🚫 归一化时删「集团/科技/技术」（会撞名）
