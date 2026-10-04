---
name: steamer
description: "蒸笼：蒸馏任何人的叙事入口——对齐数字永生引擎，强调生活化「蒸」与公开方法论顾问场景；委托上级 kit/personas 执行。"
license: MIT
metadata: {"openclaw": {"requires": {"bins": ["python3"]}, "emoji": "🫖", "parent_skill": "immortal-skill", "kit_path": "../kit"}}
---

## 复制给 AI

- **本 Skill 唯一入口**：当前文件 `steamer-skill/SKILL.md`。
- **仓库根**：假定工作区为克隆后的 **`immortal-skill/`**（若文件夹改名，以存在 `kit/immortal_cli.py` 与根 `SKILL.md` 的目录为准）。
- **执行蒸馏时**：严格跟随本文件 Phase，技术细节与根目录 [`SKILL.md`](../SKILL.md) 对齐；采集/封包命令形如：`python3 kit/immortal_cli.py ...`（均在**仓库根**下执行）。
- **聚合入口**：也可让用户先读仓库根 [`FOR_AI.md`](../FOR_AI.md) 再选段落。

# 蒸笼 · Steamer

## 语言

根据用户**第一条消息**的语言，全程使用同一语言。

## 何时激活

- 用户要「蒸馏任何人」「蒸一个数字分身」「用蒸笼那套」。
- 用户从 **蒸笼 README** 或本文件进入，希望按 Phase 完成蒸馏。

## 核心理念

**蒸笼 = 同一个数字永生引擎，换一副好讲的家常叙事。**  
技术动作与根目录 [`SKILL.md`](../SKILL.md) 一致：**选角色 → 采集 → 分维度提取 → 证据分级 → 封包。**

## 路径约定

- 本 Skill 根目录记为 **`{baseDir}`**（即 `steamer-skill/`）。
- **引擎根目录**记为 **`{repoRoot}`** = `{baseDir}/..`（仓库根）。
- CLI、personas、recipes 均在 **`{repoRoot}`** 下。

## 操作顺序

### Phase 0：对齐预期（蒸笼专属）

1. 确认对象：**任何人**；若涉及 **公众人物 / 大佬 / 顶流**，必须说明 **仅使用公开、可追溯材料**（讲演、论文、访谈、官方社交帖等）。
2. 用一句话说清价值：**借公开方法论当参谋**，不冒充本人、不伪造发言。

### Phase 1：选择角色模板

读取 `{repoRoot}/personas/` 下对应模板；公众人物必读 `{repoRoot}/personas/public-figure.md`。

### Phase 2：采集材料

按 `{repoRoot}/recipes/intake-protocol.md` 执行；CLI：`python3 {repoRoot}/kit/immortal_cli.py ...`。

### Phase 3–6

与根 [`SKILL.md`](../SKILL.md) 的 Phase 3–6 **完全一致**（分维度提取、合并、manifest、告知用户）。

## 不做的事

- 不编造非公开隐私；不鼓励未授权冒充真人。
- 不把蒸笼实现成第二套分叉引擎——**始终委托** `{repoRoot}` 已有工具链。

## 自检

- [ ] 是否已向用户说明「蒸笼」与根 `SKILL.md` 是同一引擎？
- [ ] 公众人物场景是否限定公开出处？
