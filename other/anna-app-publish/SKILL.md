---
name: anna-app-publish
description: 把纯前端静态 SPA 打包并上架到 Anna AI OS 应用平台（anna.partners）。覆盖 manifest schema 选择、三条会被 Pydantic extra="forbid" 直接拒的硬规则、CSP 内联事件处理器改造、bundle 上传与"发布≠上架"的状态机。适用于用户要求"上架 Anna""把我的网页应用做成 Anna App"等场景。
version: 1.0.0
---

# Anna AI OS 应用上架

## 何时用
- 用户要把一个纯前端（HTML/CSS/JS，无后端）应用上架到 Anna 应用市场
- 用户已经在 Anna Developer Console 建好了应用，卡在 manifest 校验 / bundle 上传 / Publish 被拦

## 先分清三件事（搞混必卡）

| 概念 | 位置 | 说明 |
|---|---|---|
| **Listing 元数据** | Console 的「基本信息 / Listing」标签 | 名称、slug、分类、简介、logo、截图。**不在 manifest 里** |
| **Manifest** | 版本编辑器里的 JSON | 声明 Executas、prompt、ui 段 |
| **Bundle** | CLI 上传的静态文件 | 真正被 iframe 加载的 HTML/CSS/JS |

## 三条硬规则（踩一次就退回重来）

### 规则 1：manifest JSON 里绝对不能写 `name` 和 `version`
`AppManifest` 是 Pydantic **`extra="forbid"`** 模型，多一个字段整体拒绝：

```
✗ schema (root): must NOT have additional properties {"additionalProperty":"name"}
✗ schema (root): must NOT have additional properties {"additionalProperty":"version"}
```

这两个值由 Console 上面的**表单字段**（应用名称 / 版本号）自动合并进去。
⚠️ Console 在编辑框下面写着「必填：schema、**name**、**version**、required_executas[]」——**这句是误导**，别照抄。

### 规则 2：`required_executas` 在 schema ≥ 2 时可以留空
官方校验清单原文：非空检查**只对 schema 1 生效**；schema ≥ 2 的**纯 Bundle UI 应用**（靠 `ui.host_api` 的 `llm.*` / `storage.*` / `image.*`）两个数组都可以留空。

Console 的 Executas 标签写着「发布前至少需要一个必需 Executa」——**那是 schema 1 时代的过期提示**。
⚠️ 但 Console 的「验证」按钮打的是服务端 Python 校验器，比本地 JSON Schema 更严，最终以它为准。

### 规则 3：`apps publish` ≠ 上架
```
DRAFT ──submit-review──▶ PENDING_REVIEW ──管理员通过──▶ APPROVED ──release 版本──▶ PUBLISHED
```
在 APPROVED 之前点 Publish 会得到 `App must be APPROVED before publishing versions`。
**没有邮件通知，也没有承诺的审核 SLA**——只看 Console「My Apps」的状态，别干等。

## schema 怎么选

| schema | 用途 |
|---|---|
| `1` | 纯聊天增强，必须有 ≥1 个 Executa |
| `2` | 有 UI（`ui` 段），Executas 可留空。**大多数网页应用用这个** |
| `3` | 额外支持顶层 `storage` 声明（真持久化 APS），但**会拒绝 `permissions` 字段** |

⚠️ schema 2 下 `ui.host_api.storage` 是 **per-window runtime_state（≤256KB）**，不一定跨设备持久。
要跨设备持久得升 schema 3 并声明 `storage: {kv: true, ...}`。

## 标准流程

### 1. 改代码：把所有内联事件处理器改成事件委托
bundle 的基线 CSP 是 `script-src 'self' <sdk-origin>`，**不含 `'unsafe-inline'`**。
而 `csp_overrides.script-src` 只接受 `'self' | 'wasm-unsafe-eval' | 'sha256-…' | 'nonce-…'`——**加不了 unsafe-inline，无解，只能改代码**。

```html
<!-- Before -->
<button onclick="save()">保存</button>
<!-- After -->
<button data-act="save">保存</button>
```
配套在 `document.body` 上挂一个委托监听器统一分派。

### 2. 接宿主 runtime
```js
import { AnnaAppRuntime } from "/static/anna-apps/_sdk/latest/index.js";
const anna = await AnnaAppRuntime.connect();   // 本地/开源版要能优雅返回 null
```
LLM 走 `anna.llm.complete`，存储走 `anna.storage.{get,set,delete,list}`——**不需要任何 Executa 插件，也不需要自带 API Key**。

### 3. 写 manifest（schema 2 模板）
```json
{
  "schema": 2,
  "required_executas": [],
  "optional_executas": [],
  "ui": {
    "bundle": { "format": "static-spa", "entry": "index.html", "external_origins": [] },
    "form_factors": ["desktop"],
    "views": [{ "name": "main", "title": "应用名", "default": true,
                "min_size": {"w":360,"h":480}, "default_size": {"w":420,"h":760},
                "max_size": {"w":1200,"h":1400} }],
    "host_api": { "llm": ["complete"], "storage": ["get","set","delete"], "window": ["set_title"] }
  }
}
```
约束：`views` 1–16 项且**最多一个 `default: true`**；尺寸 `120 ≤ w,h ≤ 4096` 且 `default_size` 落在 `[min,max]` 内。

### 4. 本地先过校验（零成本，别跳过）
```bash
anna-app validate --strict
```
用的是和服务端同一份 `@anna-ai/app-schema`。
⚠️ 本地是 JSON Schema，**比服务端宽松**（schema 1 + 空 executas 本地都放行，服务端才拦）。本地过了不代表一定过。

### 5. 上传 bundle
Console **只能声明** bundle（入口 / 格式 / Origin），**传不了文件**。
上传只有两条路：官方 CLI（`anna-app apps push`）或 REST（`bundle/init` → 逐个 PUT → `bundle/finalize`）。
配额：总量 50MB / 文件数 2000 / 单文件 10MB。`bundle_ready` 之后不可改。

### 6. 提交审核前的四项预检
- [ ] Listing 字段填完（logo 只收 PNG/JPG/WebP/GIF，**SVG 不行**）
- [ ] Console 里 Validate 返回 `valid: true`
- [ ] bundle 状态 `bundle_ready`
- [ ] ⭐ **自己完整装一遍、用一遍**（官方明确列在预检里）

## Example

> 用户：「把我这个日计划网页应用上架到 Anna。」

1. 查代码有没有 `onclick=`——有就先改成 `data-act` 委托，这一步不做后面必被 CSP 拦。
2. 按上面模板写 manifest，**不写 name/version**，executas 留空。
3. `anna-app validate --strict` 通过。
4. Console 建应用 → 粘贴 manifest → **先点「验证」** → 再创建版本 `0.1.0`。
5. CLI 上传 bundle，确认 `bundle_ready`。
6. `submit-review` → 看 My Apps 状态（别等邮件）。
7. 被 REJECTED 无惩罚，改完重提即可。

## 坑位清单
- **logo 只收 PNG/JPG/WebP/GIF**（≤2MB，自动裁 256×256），SVG 不在允许格式里
- 开发者 handle 规则 2–39 字符、小写/数字/单个连字符，应用发布为 `@handle/slug`；改 handle 后**旧名冻结 90 天**
- 官方限额：App 创建 10/天、**提交审核 5/天**、活跃非归档 App 20
- `ui.host_api` 那列表里灰色的 `* (allow all)` 是**占位符不是默认值**——留空 = 拒绝该命名空间
- 平台仍是 beta，约每周一版，接口可能变

## 隐私与边界
只处理用户自己拥有的仓库代码与 manifest。不代填任何凭据；PAT 走本机凭据管理器，用完不落盘。
简历口径注意：**审核通过前不能写「已上架」**，只能写「已提交审核 + 开源同步 GitHub」——审核状态外人看不到，GitHub 谁都能点开验证。
