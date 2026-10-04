---
name: audit-knowledge-base
description: 季度审视 Claude 知识体系（CLAUDE.md / skills / memory 三层）的体积、索引同步与失效引用。当用户说审视知识体系 / audit knowledge / 季度知识盘点 / CLAUDE.md 或 memory 体积检查 / 知识库腐化治理时使用。
disable-model-invocation: true
---

# 审视 Claude 知识体系（季度）

知识体系**只进不出会腐化**：CLAUDE.md 越写越长（触碰目录即全量进上下文）、memory 条目膨胀成实现叙述、索引与新文件脱节、路径引用随重构失效。本 skill 把盘点动作固化成清单，每季度（或大批量重构后）跑一轮。

> 第一原则：**知识分层归位**——绑定代码目录的进该目录 CLAUDE.md；跨目录流程进 skill；memory 只留跨会话教训的一句话索引。审视的本质是把漂移出去的内容搬回该在的层，而不是再加新文档。

## 一、失效引用与规模盘点（命令固化）

```bash
# 1. 路径引用校验（memory / vendor / CLAUDE.md 全扫）
pnpm knowledge:check

# 2. CLAUDE.md 体积统计（>400 行是拆分候选）
find . -name CLAUDE.md -not -path "*/node_modules/*" | xargs wc -l | sort -rn | head -15

# 3. memory 体积统计（>20 行/条违反约定，不含 frontmatter）
for f in .claude/memory/*.md; do echo "$(wc -l < "$f") $f"; done | sort -rn | head -10

# 4. skills 索引同步检查（README 表 vs 实际目录）
ls .claude/skills/ | grep -v README.md
```

## 二、memory 审视（`.claude/memory/`）

对照 `.claude/memory/README.md` 的体积约定（单条 ≤20 行、只留「一句话现状 + 非显然教训 hook + 指针」）：

1. **>20 行的条目**：实现叙述能从 git 历史 / CLAUDE.md 读到的全删，只留非显然教训与指向。删完确认 MEMORY.md 索引行仍准确（索引行本身就是 hook，不用动）。
2. **同簇 ≥3 条**：多个 memory 讲的是同一子系统的连续进展 → 收敛为一个案例并入对应目录 CLAUDE.md 或独立 skill，memory 只留一条指针。
3. **已覆盖删除**：条目内容已完整沉淀进 CLAUDE.md/skill 的，直接删 memory 与索引行——memory 不是档案柜。
4. **失效验证**：条目里点名文件/函数/flag 的，grep 确认仍存在再保留（详见 [[memory 失效引用]] 教训——曾出现 3 处真实失效路径）。

## 三、skills 审视（`.claude/skills/`）

1. **季度未触发**：git log 看 skill 目录最近提交距今 >6 个月且对应子系统已稳定 → 归档到 `.claude/skills-archive/`（git 留史），README 同步删行。
2. **description 有效性**：只写触发条件（≤400B），核心心智在正文——发现 description 写成摘要的顺手修。
3. **codex 策略同步**：新增/归档 skill 后跑 `pnpm skills:policy`（同步 `agents/openai.yaml`）。
4. **案例不独立成 skill**：发现有人把功能案例写成 skill → 并入对应子系统 CLAUDE.md（规范见 `.claude/skills/README.md`）。

## 四、CLAUDE.md 审视

1. **>400 行拆分**：按「章 = 候选子域文档」切，子域文档放代码所在目录、头部回指父文档、互指改显式相对路径。参考 2026-07 的 acp/ai/perforce 三分（commit 91ecbc08 一带）。
2. **嵌套地图覆盖**：`apps/editor/CLAUDE.md` 的「嵌套知识地图」表与根 CLAUDE.md 导航表是否覆盖全部现存 CLAUDE.md——`find . -name CLAUDE.md -not -path "*/node_modules/*"` 对照，缺行补行。
3. **与代码漂移**：抽查各文件「文件归位」表点名的文件是否还在原位；章节叙述与代码现状矛盾的，按代码现状改写（禁止照抄 memory 旧叙述——extension-host 双 host 残留即前车之鉴）。
4. **套路去重**：同一套路出现在多处目录 CLAUDE.md 的，保留最贴近代码的一份，其余改指针。

## 五、收尾

```bash
pnpm check   # 全绿才算完（含 knowledge:check / skills:check / lint / typecheck / test）
```

发现的问题**当批修完再提交**，不要留「下次再说」的清单——知识体系债务的教训是：清单即坟墓。提交粒度按「失效修复 / 瘦身 / 拆分 / 索引补全」分批，便于回溯。
