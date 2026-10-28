---
name: single-file-html-tool
description: Build and verify a zero-dependency single-file HTML tool (tracker, ledger, dashboard, calculator) with localStorage persistence, JSON/CSV import-export, seed versioning, and a fake-DOM smoke test that catches first-screen crashes node --check misses. Also covers patching existing HTML pages with a byte-level minimal insert that is proven to touch nothing else. Use when delivering "一个能双击打开的表/台账/看板", maintaining an existing one, or adding tags to pages already online.
version: 1.1.0
---

# Single-File HTML Tool

Deliver one `.html` that the user double-clicks. No build step, no npm, no CDN, no backend. It must survive being opened six months later on a machine with no toolchain.

## Architecture

```
_ledger_tpl.html     ← 模板，数据位置写死为 __DATA__ 占位符
_build_ledger.py     ← 读底表 JSON，压缩成短键，替换占位符，输出成品
_merged_seed.json    ← 底表（唯一真相源）
秋招投递台账.html      ← 生成物，不手工编辑
```

**永远编辑模板和底表，重跑构建。** 直接改成品 HTML，下次构建就覆盖了。

短键压缩（底表 556 条 → 197 KB）：内部存 `n/c/s/j/d/l/k/o/u/a/h`，运行时 `sanitize()` 展开成 `name/category/status/jobs/...`。体积差 3-4 倍，值得。

## Six gates before delivery

### 1. Seed versioning — 老用户也要看到新底表

内置种子 + localStorage 的页面，**改了种子必须 bump 版本号**，否则老用户永远看到旧数据：

```js
var SEED_VERSION = 6;                      // 每次改底表 +1
var saved = JSON.parse(localStorage.getItem(KEY) || 'null');
if (saved && saved.seedVersion === SEED_VERSION) { DB = saved; }
else { DB = seedRecords(); save(); }       // 版本不一致 → 重建
```

忘了 bump = 用户反馈「我更新了但没变化」，而且极难排查。

### 2. 数据链路字段一致性（最容易静默丢数据）

模板 `sanitize()` 写 `url`，构建脚本输出 `u`，种子读取 `c.u` —— **字段名对不上，数据被静默丢弃，脚本还一路跑通**。

规则：
- 全链路只用一个字段名。要缩写就全链路缩写。
- 构建脚本改完，**必须验证生成物里真的有这个字段**：
  ```bash
  grep -c "ruijie.com.cn" 秋招投递台账.html   # 应 > 0
  ```
- 别只跑通脚本就宣布完成，要看产物。

### 3. 可点击元素必须有静态视觉信号

**功能已实现 ≠ 用户能看到。** 这是被反复踩的坑。

```css
/* 错：点了有反应，但看不出来能点 */
.cname .lnk { color: inherit; opacity: .38; }

/* 对：静态就能看出是链接 */
.cname .lnk {
  color: var(--navy2);
  border-bottom: 1.5px solid rgba(79,70,229,.5);
}
.cname .lnk:hover { background: rgba(79,70,229,.08); }
.cname .lnk:focus-visible { outline: 2px solid var(--navy2); }
```

三档区分（让人一眼知道点下去会发生什么）：

| 档 | 样式 | 角标 |
|---|---|---|
| 网页直达 | 主题色 + 实线下划 | `↗` |
| 邮箱投递 | 灰色 + 点线 | `✉` |
| 搜索兜底 | 灰色 + 虚线 | `⌕` |

**覆盖率必须 100%**：每一行的公司名都要有 `href`。宁可给搜索兜底，也不能有「点了没反应」的行。

### 4. 从脏文本里提取 URL — 用白名单，别用黑名单

```js
// 错：\S+ 会把中文全角括号一起吞进去
//    "https://a.com/x（官网人才招聘板块）" → 整条吞入 → 链接失效
var bad = /https?:\/\/\S+/;

// 对：RFC 3986 字符白名单，遇中文立即截断
var URL_CH = "A-Za-z0-9\\-._~:/?#\\[\\]@!$&()*+,;=%";
var URL_RE = new RegExp("https?://[" + URL_CH + "]");
```

取值优先级链（多字段兜底，别只查一个）：

```js
function linkUrl(c){
  return directUrl(c)      // 专属 url 字段
      || noteUrl(c)        // 备注里带的
      || codeUrl(c)        // 内推码栏里塞的
      || mailUrl(c)        // mailto:
      || searchUrl(c.name);// 百度兜底（最后手段）
}
```

### 5. 假 DOM 冒烟测试 — 必须真跑一遍

`node --check` 只查语法，**抓不到首屏崩溃**。

```bash
node scripts/fake_dom_smoke.js <target.html> --export DB,stats,render
```

脚手架 stub 掉 `document` / `localStorage` / `window` / `FileReader` / `Blob`，
用 `new Function(code + ';return {...}')` 真正执行页面脚本，再把内部符号导出供断言。

必测项：
- 页面脚本能执行完不抛错
- 底表条数 / 统计数字与底表一致
- **全库每一行的目标元素都带 `href`（无 href 数 = 0）**
- 导出→导入往返后数据不丢
- 带筛选条件 render 不抛错

> 坑：Node 的 `console.log` 不支持 `%-46s` 这类宽度占位，用字符串拼接 + `padEnd`。

### 6. 改已上线的页面 — 字节级插入，且证明没碰别的

给已经在线的页面加东西（meta 标签、一段脚本、一个埋点），**不要重新生成整个文件**。
重新生成会带上模板的版本漂移、编码变化、行尾变化，产出一大片无法解释的 diff。

以字节为单位操作：读 `rb`，找到锚点，插入一段 UTF-8 编码的内容，其余**一个字节都不动**。

```python
raw = open(path, 'rb').read()
i   = raw.find(b'</title>')          # 锚点用 </title> 或 <head>
out = raw[:i+8] + block.encode('utf-8') + raw[i+8:]
```

**验证必须做**：把插入块从新文件里删掉，看是否等于原文件。

```python
assert out.replace(block, b'', 1) == raw     # 逐字节一致 = 只插了这一块
for tag in (b'<head>', b'</head>', b'</html>', b'<body>'):
    assert out.count(tag) == raw.count(tag)  # 骨架标签数量未变
```

> **Real case (2026-10-21):** 9 个已上线的作品页要补 og/twitter 社交预览标签。
> 全部用字节级插入，9 个文件每一个都过了「删掉插入块 == 原文件」。
> 上线后 curl 复查确认生效。Reviewer 看到的 diff 只有新增的 meta 行，没有杂音。

**宁可缺一张图，也不要挂一张错的图。** 目标仓库里没有与页面内容对得上的封面时，
不写 `og:image`，`twitter:card` 用 `summary` 而不是 `summary_large_image`，并在 CHANGELOG 里
写明为什么故意不写。

## Persistence contract

- 键名带年份/用途前缀：`qiuzhao2027_ledger_v1`
- 点击回执单独存：`KEY + '_visited'`
- 每次写盘存**全量**（别只存首屏 60 条），否则筛选后刷新会缺数据
- 导出 JSON 里带 `snapshot` 统计 + `exportedAt`，方便日后对账

## Delivery checklist

- [ ] 双击能开，无外部依赖（图标内联 SVG / data URI）
- [ ] 无残留占位符（`grep -c __DATA__` = 0）
- [ ] SEED_VERSION 已 bump
- [ ] 生成物里能 grep 到关键数据（字段没被丢）
- [ ] 假 DOM 冒烟测试全绿
- [ ] 若改的是既有页面：字节级插入 + 「删掉插入块 == 原文件」已验证
- [ ] 文件落在**工作区**，没进投递区

## Example

用户说「做个能记录我投了哪些公司的表」→ 走本 skill：
底表 JSON 建 556 条 → 模板写 `nameHTML()` 三档链接 → 构建脚本注入 →
跑 `fake_dom_smoke.js` 验「无 href 数 = 0」→ 交付 HTML。
