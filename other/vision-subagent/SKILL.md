---
name: vision-subagent
description: 视觉子代理。当主模型不支持图像输入时，用 workflow 派生一个指定当前环境可用视觉模型的子代理，通过 read_image 查看或核验图片内容并结构化返回结论。适用于"需要看图、但主模型读不了图"的任何会话。
---

# 视觉子代理（Vision Sub-agent）

当**主模型不支持图像输入**（`read_image` 会拒读，如纯文本模型）时，用 **`workflow` 派生一个指定视觉模型的子代理**来"看"图——它可以用 `read_image` 读取图片，再根据你的要求描述内容或审查质量并返回结论。

本 skill 是**全局可用**的看图方案，任何预设/会话/项目都可加载，不限定业务场景。

## 触发条件（先判断，再决定用不用本 skill）

**先试一下**：直接调 `read_image`，或查 `llm.resolveModelInfo(provider, model)` 的 `inputModalities`。

- ✅ **主模型支持图像**（`inputModalities` 含 `image`）→ **直接 `read_image` 读图即可，不必派子代理**（更快、少一层）。注意能力靠配置声明——若报 `does not declare image input`，先按本文末"图像能力靠配置声明"排查，可能只是配置漏声明。
- ❌ **主模型不支持图像**（`read_image` 拒读）→ 用本 skill 派生视觉子代理来看图。
- 🔀 **仍值得用子代理的两种情形**：① 想要**独立/隔离的看图结论**（不让主模型既产出又自查）；② 想用**更便宜的视觉模型**替代主模型读图。

## 原理

DeepSeek Harness 的 `workflow` 工具允许在 `agent()` 上独立指定 `provider` 与 `model`。只要选一个**当前部署里真正支持图像输入的模型**（其 `inputModalities` 含 `image`），派生的子代理就能用 `read_image` 读取并处理图片。

不同部署注册的视觉模型名可能不同，**不要硬编码模型名**，应先探测。

## 如何找可用的视觉模型

用 `llm` 服务遍历各 provider 的模型，过滤出 `inputModalities` 含 `image` 的：

```js
// 思路：遍历 provider -> resolveModelInfo -> 过滤 inputModalities 含 'image'，得到 { provider, model }
const vision = /* inputModalities 含 'image' 的 {provider, model} */
await agent(prompt, { provider: vision.provider, model: vision.model })
```

**成本优先（重要）**：识图/看图是高频、轻量任务，**优先选择便宜的经济型视觉模型，不要使用贵的大模型**。具体原则：
- **首选**：`deepseek-official/deepseek-flash`（DeepSeek V4.1 Flash，官方"快·高效·经济"定位，text+image）、`kimi-coding/kimi-for-coding`（K2.7 Code）、`kimi-coding/kimi-for-coding-highspeed` 等经济型视觉模型。
- **避免**：`kimi-coding/k3`、`k3-256k` 这类旗舰/大上下文模型——识图不需要它们的强推理与长上下文，成本不划算。除非便宜模型全部不可用且任务确需更强能力，才考虑它们。
- 换部署后先探测：按"便宜视觉模型优先 → 经济型 → 旗舰兜底"的顺序选。
- 同一批图片审查应尽量**一次性派发**（一次 workflow 调用审多张），减少调用次数与成本。

已验证候选（示例）：`deepseek-official/deepseek-flash`、`kimi-coding/kimi-for-coding`、`kimi-coding/kimi-for-coding-highspeed`（均 text+image，经济型）。

> ⚠️ **图像能力靠配置声明**：模型的 `inputModalities` 在配置里默认是 `["text"]`。若某模型实际支持读图却被拒（`read_image` 报 "does not declare image input"），检查其配置是否声明了 `image`（DSH 的 `dsh-llm-deepseek` 等适配器本身支持图像，声明后即可读图）。

## 用法模板

用 workflow 派发看图子代理（`provider`/`model` 替换为探测到的可用视觉模型）：

```js
await agent(
  '用 read_image 工具读取 <图片绝对路径>，然后完成任务：<你的具体诉求，如描述内容 / 审查质量 / 判断是否达标>，并结构化返回结论。',
  { provider: '<探测到的provider>', model: '<探测到的视觉 model>' }  // 指定视觉模型
)
```

> 把"任务诉求"填进 prompt，子代理会先看图，再按你的要求输出。例如：描述图里有什么、检查是否有空白/遮挡/文字重叠、核验图与某条结论是否一致等。

## 输出约定（建议）

按需要求子代理给出结构化结果，例如：
- **内容描述**：图中关键元素、布局、文字/标题等
- **质量核验**：是否空白、模糊、遮挡/重叠、要素缺失
- **目标核对**：图是否支撑它要支撑的结论或任务
- **判定**：`PASS` / `FAIL`，FAIL 时给原因与改进建议

## 复验闭环（FAIL → 修改 → 重审，强制）

**图片核验不通过后，必须进入"修改-重审"循环，直到 PASS，才算完成。** 不得"审一次出个 FAIL 就当作已核验"。

规则：
1. **FAIL 即回退修改**：子代理返回 `FAIL` 时，按它给出的缺陷与改进建议，把图片退回给制作/修改图片的一方进行修改。
2. **修改后必须重审**：每次修改后，重新派发识图子代理对**修改后的图完整复审一遍**，不能只让修改方自称"改好了"。
3. **循环直至 PASS**：复审 `FAIL` 则继续"修改 → 重审"，直到 `PASS` 为止；每次重审都记录结论（哪一版图、审了什么、结果）。
4. **有界兜底（可选）**：可约定最大重审轮次（如 ≤3 轮）；超限仍不 PASS 时，如实标记"多次修改未通过核验，存在持续缺陷"，不得降级成"视为通过"。
5. **记录留痕**：把每次"FAIL 原因 → 修改动作 → 重审结果"写进审查/核验记录，供追踪与验收。

> 示例：某项目的一张图初检通过（非空、有内容），但在与文字结论的一致性核查中发现坐标/内容被裁剪造成误导（图上表现与结论相反）→ 判定 FAIL → 修改后重审 → PASS。这类问题纯文本主模型发现不了，必须靠复验闭环兜住。

## 兜底

- 若探测不到任何 `inputModalities` 含 `image` 的模型，如实标记"此环境无视觉模型，看图受限"，不要假装通过。
- 主模型若是纯文本模型，直接 `read_image` 报错属预期行为；此时用本方案派生视觉子代理即可。
- 本 skill 只负责"让图能被看/被审"。若还需要**用与主模型不同厂商的模型做内容/推理审查**，那是另一个维度（独立模型审查），可与本方案组合使用。