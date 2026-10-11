---
name: skill-checker
description: "Use this skill when the user wants to check, test, or optimize a skill. Covers: testing whether a skill's description triggers correctly, optimizing description wording, scanning whether a skill works in a target environment, and adapting a skill to use environment-specific capabilities."
---

# Skill Checker

评估现有 skill 的两个面：

- **触发** — description 能不能让 agent 在该触发时触发、不该触发时不触发
- **环境** — skill 正文里的指令在当前 agent 环境中能不能正常执行

整体流程：

1. 定位 skill — 找到 SKILL.md，校验 YAML frontmatter，有问题则修复
2. 生成测试集 — 约 20 条平衡的 should-trigger / should-not-trigger query
3. 触发评测 — map 对每条 query 评估触发
4. 环境扫描 — 分析 skill 的环境依赖，回写 frontmatter dependencies
5. 汇总报告 — 两个维度的得分 → 写入 `{skill_name}.check.json`（唯一产出文件）
6. 优化（按需）— 改进 description 和/或适配环境

你的任务是判断用户在这个流程中的哪个位置，然后帮他往下推进。比如用户说"帮我检查一下这个 skill"，你就从第 1 步开始完整走一遍；如果他说"触发率太低了帮我优化 description"，你可以直接跳到第 6 步。灵活应对即可。

**重要**：整个流程只产出一个文件 `{skill_name}.check.json`。中间数据全部在内存中流转，不要写中间文件。

---

## 1. 定位 skill 并校验 frontmatter

找到用户指定的 skill，读取其 SKILL.md，然后跑一次 frontmatter 校验：

```bash
python scripts/validate.py <path-to-SKILL.md>
```

脚本输出 JSON 报告，含 error（必须修）和 warn（建议修）。典型问题是 description 含冒号或特殊字符却未加引号——用双引号包裹并转义内部 `\"` 即可，或改用 block scalar `|`。

有问题时由你直接编辑 frontmatter 修复，改完重跑 `validate.py` 确认通过。确认 `name` 和 `description` 都拿到后进入下一步。

---

## 2. 生成测试集

基于 skill 的 name、description 和完整内容，生成 ~20 条测试 query。数据保存在内存中，不写文件。

约 10 条 should_trigger=true + 约 10 条 should_trigger=false：

```json
[
  {"query": "帮我检查一下这个 skill 的触发率", "should_trigger": true},
  {"query": "帮我从零写一个新 skill", "should_trigger": false}
]
```

**should_trigger=true 的写法**：
- 真实用户消息，多样化表述（别只是改述 description）
- 含边界情况和间接表述
- 自然语言，不要堆砌关键词

**should_trigger=false 的写法**（最难写好的部分）：
- 必须是**高质量近似干扰** — 关键词相似但意图不同
- 好的反例：相邻领域的请求、相似术语但不同场景
- 坏的反例："今天天气怎么样" — 太明显无关，测不出东西
- 要让模型需要认真想一想才能判断

每条 1-3 句话，像真实用户会说的那样。

生成后给用户过目，确认没问题再继续。自动生成的测试集是起点不是终点。

---

## 3. 触发评测

对每条 query 判断：给定目标 skill 的 name + description，agent 会不会触发它？

读取 `references/prompts/trigger_eval_prompt.md`，填入 skill_name 和 skill_description，然后用 **map 工具**对所有 query 并行评估 — 每条 query 作为一个 map 输入项。map 返回每条 query 的 `{triggered: true/false}` 结果。

拿到 map 结果后，把每条 query 的 `{query, should_trigger, triggered}` 组装成数组，管道交给脚本算分：

```bash
echo '<merged_json_array>' | python scripts/scoring.py eval-summary \
  --skill-name <name> --description "<tested_description>"
```

脚本输出 eval_results JSON（含 results + summary），留在内存中用于后续汇总。

---

## 4. 环境扫描

分析 skill 正文的环境依赖，判断在当前 agent 环境中的兼容性。此步由你自己执行 — 只有你自己能完整感知当前环境的工具和能力。

逐段读 SKILL.md，找出每一项环境依赖，按四类归类：

- **工具依赖**: Bash, Read, Write, map 等
- **能力依赖**: 多会话、网络访问、文件系统、子 agent
- **外部服务依赖**: API、SDK、数据库
- **隐含假设**: OS、目录结构、权限、已安装的包

每项记录：依赖名称、来源（引用 SKILL.md 原文）、兼容性分类和理由。兼容性分为：

- `compatible` — skill 原文的写法在当前环境中**原样可用**，不需要改
- `adaptable` — 能跑但环境有**更好的方式**。判断标准：如果你从零给这个环境写 skill，会不会用不同的写法？会 → adaptable
- `incompatible` — 无替代方案
- `unknown` — 信息不足

对 `adaptable` 项，adaptation 要**具体到可以直接替换进 SKILL.md**。`target_capability` 写清工具名称和调用方式（不要只写工具名），`changes` 写出替换后的实际文本片段（不是"把 X 改成 Y"这种描述）。

组装好依赖项列表后，管道计算汇总：

```bash
echo '<env_scan_json>' | python scripts/scoring.py env-summary
```

**回写 frontmatter dependencies**：把所有依赖项的 `name` 提取为列表，写入目标 skill 的 SKILL.md frontmatter：

```yaml
dependencies: [bash, file_system, map, user_choices]
```

这样环境变化时可以 `grep dependencies */SKILL.md` 快速定位受影响的 skill。

---

## 5. 汇总报告

把测试集 + 触发评测 + 环境扫描合并为 `{skill_name}.check.json` — **唯一的产出文件**：

```bash
echo '<combined_json>' | python scripts/scoring.py merge --skill-name <name>
```

输入格式：
```json
{
  "skill_name": "my-skill",
  "evals": [...],
  "trigger": { "results": [...], "summary": {...}, "description": "..." },
  "environment": { "dependencies": [...], "summary": {...} }
}
```

脚本输出完整的 check.json（含 overall_score、各维度详情、测试集）。将结果写入 `{skill_name}.check.json`。

每个维度 0-1 分，overall_score = 两个维度的均值。对低分维度给出具体改进建议。

如果用户只需要评估，到此结束。

---

## 6. 优化（按需）

基于报告结果，改进 SKILL.md。仅在用户要求优化时执行。

### 触发优化

如果触发准确率不够好：

**准备** — 分割测试集防止过拟合：

```bash
echo '<evals_json_array>' | python scripts/scoring.py split --holdout 0.4
```

输出 `{train, test}` 两个数组。60% train + 40% test，按 should_trigger 分层。train 指导改进，test 衡量泛化。不要对 test set 调优。

**每轮迭代**（最多 ~5 轮）：

1. 用 map 工具在 train set 上评估当前 description（方法同第 3 步）
2. 用 `scoring.py eval-summary` 算分
3. train 全部通过 → 跳到选最优。否则分析失败项
4. 根据 `references/prompts/improve_desc_prompt.md` 的思路改写 description — 把失败项和历史尝试喂进去，避免重蹈覆辙
5. 用新 description 重复

每轮记录一条迭代记录：`{iteration, description, train_passed, train_total}`。

**选最优**：对 train 得分最高的 description（如有并列取最后一轮），在 test set 上跑一次 map + eval-summary 作为最终得分。把 description 和 test 得分给用户看，确认后更新 SKILL.md frontmatter。

优化完成后，把迭代记录追加到 check.json 的 `optimization` 字段中（重新 merge 或直接编辑）。

### 环境适配

如果环境扫描发现 `adaptable` 项，改写 SKILL.md 让 skill **原生使用环境能力**。

从扫描结果中找出所有 adaptable 和有替代方案的 incompatible 依赖项，逐项改写。

**改写原则**：

1. **Replace, don't patch** — 按名称引用环境原生能力，直接重写对应段落。不要在原文旁边加"也可以用 X"，也不要写泛泛的"使用适当的工具"。改写后读起来应该像专门为这个环境写的
2. **保留意图** — skill 的核心目的和工作流不变，只改实现方式
3. **保留 frontmatter** — name 不变，description 只在适配改变了 skill 能力时才更新

**示例** — 一个文档生成 skill 从本地开发环境适配到无显示器的远程环境：

适配前（原 SKILL.md）：
```
## 预览阶段
把生成的文档写入 docs/output/ 目录。运行
`python -m http.server 8080 --directory docs/output`
启动本地预览服务器。告诉用户打开 http://localhost:8080
查看效果，满意后按 Ctrl+C 停止服务器，然后告诉你继续。
```

适配后：
```
## 预览阶段
把生成的文档渲染为 Markdown，直接在对话中呈现关键章节的预览。
完整文档写入 docs/output/ 并告知路径。用澄清工具询问用户：
"满意当前效果" / "需要调整格式" / "需要调整内容"。
```

变的不只是工具，而是整个交互模式：本地 HTTP 预览 → 对话内呈现，浏览器查看 → 内联预览，Ctrl+C 流程 → 结构化选择。适配后的文本里没有"如果没有浏览器就..."这种补丁痕迹。

改写结果需要用户确认后再应用。对于 `incompatible` 项，报告为 blocking issues，按影响排序。

---

## 参考资料

| 文件 | 用途 |
|------|------|
| `scripts/validate.py` | YAML frontmatter 校验（含 dependencies 字段） |
| `scripts/scoring.py` | 评分计算：eval-summary, env-summary, merge, split（全部 stdin→stdout） |
| `references/prompts/trigger_eval_prompt.md` | 触发判定（map 用） |
| `references/prompts/improve_desc_prompt.md` | description 改写参考 |
| `references/schemas.md` | check.json 格式定义 |
