---
name: 1688-selection-upload
description: 通过 BrowserWorker 插件浏览器，在 1688 搜索结果页筛选商品，并勾选符合条件的采购助手商品。适用于 1688 选品、扫描、月代销/48H 揽收筛选、待采商品勾选。
title: 1688选品和上架
example: |-
  > **选品扫描**：分析指定关键词的 1688 搜索结果并筛选符合要求的商品，例如："扫描 3 页女鞋，看看哪些符合要求"

  > **勾选待采**：自动勾选符合过滤条件且未处理过的商品，例如："勾选女鞋，最多 5 个，先 dry run 看看"
version: 2.0.0
---

# 1688-selection-upload

> [!IMPORTANT]
> **前置插件约束**：运行本技能前必须确认 1688 采购助手插件 (`1688-extension`) 已安装。平台会在触发 `1688-selection-upload` 任务时自动校验插件状态。若未检测到 1688 插件，平台将拦截任务并引导由**运营主管**（ops_director）使用 `chrome-plugin` 技能安装 1688 插件。

统一入口：

```bash
python3 {baseDir}/run.py <command> [options]
```

该技能使用项目内置 `BrowserWorker` daemon 的 extension-first transport，不再直接依赖 CDP 控制页面，也不要求用户机器安装 ChromeDriver、Playwright、Selenium 或固定 Chrome 路径。页面读取通过 BrowserWorker 插件浏览器执行 `browser.evaluate(...)`，因此能读取 1688 原页面和采购助手插件渲染到当前 DOM 中的内容。

## 意图判断

触发本技能：

- 用户要求在 1688 搜索、选品、筛选商品。
- 用户提到采购助手、待采商品勾选、选品勾选。
- 用户要求按月代销、48H 揽收率、实力商家/源头旗舰筛选。

命令选择：

```text
只查看符合条件的商品 -> scan
勾选符合条件的采购助手商品，不最终提交 -> collect
```

## 命令

| 命令 | 用途 | 语法 |
| --- | --- | --- |
| `scan` | 扫描并返回符合条件的商品，不点击页面 | `python3 run.py scan [关键词] [--pages 页数]` |
| `collect` | 扫描并勾选符合条件商品，不点击最终提交按钮 | `python3 run.py collect [关键词] [--pages 页数] [--max 最大采集数] [--dry]` |

默认值：

- 关键词：`女鞋`
- `--pages`：`1`
- `--max`：`0` 表示不限制
- `--dry`：只列待勾选商品，不点击

## 新架构流程

1. `run.py` 获取浏览器锁，然后调用 daemon `/execute`。
2. `run.py` 必须传入本 skill 的 `action_search_path={baseDir}/scripts/actions`。
3. daemon 必须优先加载 `action_search_path` 下的 `scan_1688.py` 或 `collect_1688.py`；BrowserWorker 内置 actions 只是 fallback，不能覆盖本 skill 同名 action。
4. `/execute` 返回里的 `action_path` 可用于确认实际加载的 action 文件。
5. action 通过 `browser.goto/evaluate/wait_ms/request_help` 操作 BrowserWorker 插件浏览器页面。
6. action 先进入 1688 搜索页，输入关键词，进入搜索结果页。
7. action 拼接排序和商家过滤参数：
   - 销量降序：`sortType=va_sales360&descendOrder=true`
   - 商家标签：`filtMemberTags=5179713,5125953,5343297`
8. 分段滚动页面，等待懒加载和采购助手插件数据面板渲染。
9. 在页面 DOM 中提取商品卡片、月代销、48H 揽收、价格、勾选状态。
10. `scan` 返回符合条件商品；`collect` 只勾选商品卡片内的采购助手复选框，并更新 `data/ledger.json`。不要继续点击最终提交、确认、批量采集或一键上架按钮。

## 筛选口径

当前硬规则：

- `月代销 != "100以内"`，视为月代销 > 100。
- `48h揽收 > 90%`。
- 搜索 URL 会附带实力商家/源头旗舰相关标签过滤。

返回字段包括：

- `offerId`
- `title`
- `dx`：月代销桶值
- `ls`：48H 揽收率数字
- `price`
- `href`
- `qualify`
- `collected`

## 快速定位和排查

如果页面结构变化导致勾选失败，按这个顺序处理：

1. 先读取当前页面匹配的 `page_semantics`，优先按 `semantic_key` 理解关键元素和重复商品卡片，例如 `search.primary_input`、`search.submit`、`result_card`、`result_card.primary_link`、`selection.checkbox`。
2. `page_semantics` 缺失、低置信或执行失败时，再用 BrowserWorker `snapshot` 验证当前页面事实并补充证据。
   - 页面简单：可用 `full snapshot`。
   - 搜索结果/卡片列表：优先 `data snapshot`。
   - snapshot 返回的 `ref` / `handle` 只用于当前页面的一次性验证，不写入脚本或台账。
3. snapshot 找不到时，用小 JS probe 检查真实 DOM：

```javascript
(() => [...document.querySelectorAll("a.search-offer-wrapper,[class*='search-offer-wrapper']")]
  .slice(0, 20)
  .map(el => ({
    text: (el.innerText || "").replace(/\s+/g, " ").trim().slice(0, 240),
    href: el.href || el.querySelector("a[href]")?.href || ""
  })))()
```

4. 页面很复杂、hover 才出现按钮、插件 UI 难判断时，让用户用 BrowserWorker 扩展录制并上传。
5. 读取上传后的三层数据：
   - `*.trace.json`
   - `*.interests.json`
   - `*.script_hints.json`
6. 根据录制里的 `page_key/page_role`、`semantic_key` 和候选节点证据更新 `page_semantics`、action 的结构化目标或 DOM parser；不要把 `@eN`、临时 handle、长路径 selector 当作长期定位键。

## 人工处理

遇到登录、滑块、验证码时，action 会通过 `browser.request_help(...)` 提示用户在 BrowserWorker 插件浏览器中处理，然后继续执行。不要绕过安全验证。

## 输出和台账

`collect` 默认读取并更新本 skill 下的 `data/ledger.json`，避免重复勾选已成功的 `offerId`。也可以用环境变量 `MANAI_1688_SELECTION_LEDGER` 指向外部台账；如果旧版根目录 `ledger.json` 已存在且 `data/ledger.json` 不存在，会兼容读取旧文件。

`run.py` 默认将符合条件的商品链接保存到 `data/outputs/1688_selection_<关键词>.json`。如果 ManAI 全局配置里有 `data_directory`，或设置了 `MANAI_1688_SELECTION_OUTPUT_DIR`，允许写到外部目录。脚本和 action 实现必须留在 `{baseDir}/` 内；运行产物可配置。

## 验证

修改 action 后至少运行：

```bash
python3 - <<'PY'
from pathlib import Path
for p in [
  "scripts/actions/scan_1688.py",
  "scripts/actions/collect_1688.py",
  "run.py",
]:
    src = Path(p).read_text(encoding="utf-8")
    compile(src, p, "exec")
print("syntax ok")
PY
```

真实验证：

```bash
python3 run.py scan 保温杯 --pages 1
python3 run.py collect 保温杯 --pages 1 --max 3 --dry
```
