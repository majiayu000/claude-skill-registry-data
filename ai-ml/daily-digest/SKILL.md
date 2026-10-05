---
name: daily-digest
description: Add today's ML/AI paper and news picks to the PaperTrace daily feed. Use when the user wants to update the daily page with new content.
allowed-tools: Read Edit Bash Glob WebFetch WebSearch
---

# PaperTrace · 每日日报

为 PaperTrace 生成当天的日报内容，更新到 `src/lib/daily.ts` 和 `src/app/daily/page.tsx`。

---

## ⛔ 反幻觉原则（所有内容均适用）

**论文条目（`dailyPapers`）的数字必须来自：**
- arXiv abstract 页面（作者、标题、arXiv ID）
- 论文 abstract 本身（主要结果数字）

**新闻条目（`newsItems`）的内容必须来自：**
- 官方公告（官方博客、官方 HuggingFace 页面、官方 X/Twitter 账号）
- 官方技术报告或 README

**绝对禁止：**
- 用第三方媒体报道的数字填写 why/description（例如 "据报~81%"）
- 把推测性技术细节当作事实（例如训练硬件）
- 用 "reportedly" / "据报" 等模糊措辞掩盖无法验证的来源

如果官方数字暂时无法获取，**宁可省略该数字，不写模糊断言**。

---

## 1. 找内容

**Paper 来源（按优先级）：**
```
https://huggingface.co/papers        ← 社区人气榜，首选
https://arxiv.org/list/cs.LG/recent
https://arxiv.org/list/cs.CL/recent
https://paperswithcode.com/latest
```

**新闻来源（仅限官方）：**
```
官方 HuggingFace 模型页 README
官方博客（openai.com, anthropic.com, deepmind.google, ai.meta.com 等）
官方 X/Twitter 账号（@openai, @anthropic, @deepseek_ai 等）
官方技术报告 PDF
```

**筛选标准（论文）：**
- 解决清晰问题，不是 survey
- 有明确数字结果（从 abstract 中可直接提取）
- 与受众相关：LLM / Diffusion / RL / Efficient Training / Reasoning

目标：**每日 2–5 篇 paper + 0–2 条 news**，宁缺毋滥。

---

## 2. 生成论文字段

拿到 abstract 后，只使用 abstract 中明确出现的数字：

```
论文标题：[title]
arXiv ID：[XXXX.XXXXX]
Abstract：[粘贴]

请输出 JSON：
{
  "titleZh": "中文标题",
  "tags": ["从以下选 ≤3 个: Diffusion LM, Pre-training, Fine-tuning, LoRA, Efficient Inference, Reasoning, Alignment, RLHF, Multimodal, Theory, Benchmark, Code, Agent, RAG, Quantization, MoE, Vision"],
  "why": "英文，≤25词，格式：[做了什么] — [为什么重要]，数字必须来自 abstract",
  "whyZh": "中文，≤30字，同格式"
}
```

---

## 3. 新闻条目格式

新闻加到 `src/app/daily/page.tsx` 的 `newsItems` 数组**顶部**：

```ts
{
  date: "YYYY-MM-DD",           // 官方公告日期
  title: "英文标题",             // 准确描述事件
  titleZh: "中文标题",
  description: "...",           // 仅含官方来源确认的事实
  descriptionZh: "...",
  source: "Official Blog / HuggingFace / ...",  // 明确标注来源
  sourceUrl: "https://...",     // 直接链接到官方来源
  tag: "Release" | "Research" | "Industry",
}
```

**Description 写法原则：**
- 用官方公告原文改写，不添加推测
- 数字直接引用官方数据（例如从 HuggingFace README）
- 如确实不确定某个数字，直接省略，不写 "~" 或 "reportedly"

---

## 4. 论文条目格式

加到 `src/lib/daily.ts` 的 `dailyPapers` 数组**顶部**：

```ts
{
  date: "YYYY-MM-DD",
  title: "英文原标题",
  titleZh: "中文标题",
  authors: "第一作者 et al.",
  arxivId: "XXXX.XXXXX",        // 只填 ID；非 arXiv 论文用 paperUrl 字段
  paperUrl: "...",               // 非 arXiv 时填（如 HuggingFace PDF 链接）
  tags: ["Tag1", "Tag2"],
  why: "...",                    // 数字必须来自 abstract 或官方 README
  whyZh: "...",
  pick: true,                    // 最多 1 篇
  slug: "paper-slug",            // 如果已有精读页则填
}
```

---

## 5. 验证

```bash
npm run build
```

- 确认新条目在 `/daily` 顶部
- 中英文切换正常
- 检查 why/description 中无 "reportedly" / "~数字" / "据报" 等模糊措辞

---

## 快速清单

```
[ ] 确认内容来源为官方（论文/公告/README）
[ ] 从 abstract 提取数字，不从第三方报道引用
[ ] 加 paper 条目到 daily.ts 顶部
[ ] 加 news 条目到 page.tsx newsItems 顶部（如有）
[ ] npm run build 验证
[ ] git commit: "feat(daily): YYYY-MM-DD digest"
```
