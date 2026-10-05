---
name: weekly-digest
description: Compile and publish the weekly ML/AI digest for PaperTrace. Selects top papers from the week, defines a theme, and updates the daily feed. Use on Fridays or Sundays.
allowed-tools: Read Edit Bash Glob WebSearch WebFetch
---

# PaperTrace · 每周周报

每周（周五/周日）整理一周 ML/AI 精华，发到 PaperTrace 日报页面。

---

## 1. 收集本周候选

**抓取来源：**
```
https://huggingface.co/papers        ← 本周人气榜（默认显示近7天）
https://arxiv.org/list/cs.LG/recent
https://arxiv.org/list/cs.CL/recent
```

**筛选：5–10 篇进入周报**，优先级：
1. 和本周主题直接相关
2. HuggingFace Papers 本周人气最高
3. 顶会/顶实验室
4. 对求职者有实际价值（新技术栈、面试考点）

---

## 2. 定本周主题

从候选里找一个"本周 narrative"：

```
这周的主线是什么？
  - 技术方向：某个方法突然多篇论文？（reasoning、diffusion LM...）
  - 行业事件：某个模型发布引发讨论？
  - 社区共识：某个争议正在收敛？
```

主题一句话：
```
例："本周 reasoning 三连：CoT → RL → 推理时计算，一条技术脉络"
例："Diffusion LM 爆发周：三篇论文从效率、理论、scale 三角推进"
```

---

## 3. 批量生成字段（Claude Prompt）

```
本周主题：[主题一句话]

以下是本周周报候选论文：
1. [title] — arXiv [ID] — [abstract 一句话]
2. ...

请为每篇生成：
{
  "titleZh": "中文标题",
  "tags": ["≤3个，从: Diffusion LM, Pre-training, Fine-tuning, LoRA, Efficient Inference, Reasoning, Alignment, RLHF, Multimodal, Theory, Benchmark, Code, Agent, RAG, Quantization, MoE, Vision"],
  "why": "英文，≤40词，说清楚为什么这周特别值得关注",
  "whyZh": "中文，≤50字"
}

输出 JSON 数组。
```

---

## 4. 更新文件

```
Read src/lib/daily.ts
Edit src/lib/daily.ts   ← 本周所有条目加到数组顶部，按时间倒序
```

所有周报条目都可以加 `pick: true`。

---

## 5. 验证 + 发布

```bash
npm run build
git add src/lib/daily.ts
git commit -m "feat(daily): weekly digest $(date +%Y-W%V)"
git push
```

---

## 6. 可选：外部分发文案

从已生成字段提取，用于微信/小红书/邮件：

```
本周 PaperTrace 精选 · YYYY 第 W 周

🎯 本周主题：[主题]

📄 精选：
[每篇：标题 + whyZh]

🔗 完整版：papertrace.app/daily
```
