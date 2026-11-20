---
name: mathrsi-degree-diameter
description: "Research finite simple undirected degree–diameter graphs using actual graph constructions, shared route coverage, frozen-neighborhood transfer and scoped obstruction certificates. Use for a new or resumed degree–diameter task, selecting a domain method or connecting an existing result to the original graph; historical archive state never resumes a Goal."
---

# Degree–diameter 领域入口

给定最大度数 d、直径 D 和目标阶数，先明确本次是构造一张图、改进公开下界、证明特定构造族失败，还是核验固定公式图。`N(d,D)` 是满足最大度≤d、直径≤D的有限简单无向图的最大阶；找到 n 点合法图给 `N(d,D)≥n`。正则性比最大度约束强，除非目标要求或有证明，不预设正则、Cayley、顶点传递或有限几何来源。

与[MathRSI主入口](../../../../base/skills/mathrsi-research/SKILL.md)配合；这是领域入口，不复制主调度。由 prepare／route-loop／prove／verify 嵌入时，接收原规格、当前义务、实际输入、已证与待证假设、写域、预算和返回点；完成后返回该调用处，不自行启动另一个同级 workflow。独立使用时同样形成实际数学结果及准确剩余。

## 接手和恢复

读任务自己的 FORMAL_SPEC、NEXT_SESSION、已有 wiki 实体和最近一个承重结果。新题写清 d、D、n、简单／无向／连通、是否要求正则、允许的进口与计算证据、以及“改善已知值”是否属于目标。固定构造题不能因找到更大公开图而擅自换题；竞争型选题则让新基线改变下一任务。

原研究有153 named graphs、43参数、47具体 Lean 的历史目录。这些不是153种方法或世界纪录。相同阶数可能对应不同度数／中心集合；定位实例用 `(d,D,n)` 加实际来源路径，不能只用 n。没有新任务授权就只读归档，不执行历史恢复命令。

先读[调用地图](../../references/reading-and-calling.md)，沿本次问题选一条原链，不要求每次全文阅读 archive。原 wiki负责定位；需要某条引理就读其完整假设、证明和实际 caller。新的文献疑问与 base survey 共享同一次任务，分工查异名、已知族、引用链或具体进口，返回原义务。

## 把任务变成原图上的义务

构造的最小完整对象是明确顶点集与邻接关系。字面边表应说明标签、header有无、每条无序边是否只列一次；公式图应说明有限域编码、逆 dart、每个实际参数和标签。小公式可定义巨大图，不要求先存邻接矩阵。

验收要接上：无自环／无重边／无向性、顶点数、每点最大度、全部点对的距离界。可使用完整 all-root BFS，或覆盖所有实际对象的数学路线证明加有限前提绑定；少量 roots只是补充测试。精确直径D还需非≤D−1：Moore计数或一个真实距离见证可以承担，说明采用哪一项。

Moore上界对 d≥2 为 `1+d Σ_{i=0}^{D−1}(d−1)^i`。它给不可能超过的阶数，不表示空隙可实现或成功概率。保边增点中旧点对距离上界继承；删旧边后这一继承通常失效，必须处理实际旧点对。

把当前缺口交给有实质职责的技能：

| 当前输入 | 调用 | 返回后做什么 |
| --- | --- | --- |
| 已选源图、余度和新邻域／代数路线 | [dd-construction](../dd-construction/SKILL.md) | 消费完整生成规则、覆盖与度数证明，或准确未满足条件 |
| 固定必要模型、失败点对、有限域或证书 | [dd-obstruction-certificate](../dd-obstruction-certificate/SKILL.md) | 把实际检查的有限命题接原图；未闭条件仍交prove |
| 换源／换域／放宽连接／基线更新 | [dd-transfer-diagnosis](../dd-transfer-diagnosis/SKILL.md) | 选择真正改变障碍的下一动作，保留旧正负结论的范围 |

## 文献与旧知识怎样用于当前图

公开比较包括维护表、作者实际图、一般构造族的合法代入，分别记所读版本与条件。某家族实例不是全球最好；更大图可以在更低度数上给当前cap的保证。相反，一条公开复制定理可能要求独立中心，而实际需要的是允许matching诱导子图的更一般版本，不能误用较窄特例。

已有wiki和失败地图可直接提供反例与条件工具。重用证明时写出当前对象怎样满足每个假设，不把所有历史参数变成默认值。满秩、必要容量、公开margin、solver可行、实际图和kernel导出分别报告。

## 研究与验证的实际衔接

D5 的新来源先区分保边扩张和改核心重建，按[联合补全参考](../../references/d5-joint-completion.md)接实际原图与覆盖义务。固定前部严格不可补时回到前部，既有前缀成功则立即独验并消费；单批限额、UNKNOWN 和充分证书域查尽分开。原父调度更新当前事实后再派下一任务，[批次/收件工具](../../references/d5-blocking-batches.md)仅服务其明确格式和输入域。共享源 Lean 缺口只保留一个准确义务，不为每个新增前缀重编相同条件 wrapper。

短证明可以直接闭合；需要计算时先固定真实谓词、输入域及结果用途，选最便宜足够的检查。已有完整反例否定候选引理时，不再扩算相同受限模型。UNKNOWN仍是未决，可因新数学或已授权资源继续，但不自动新开相同种子／timer。

完整候选交 base verify时，附当前正文、实际图定义／数据、所有进口、有限覆盖域、运行结果和剩余。Lean按用户需求或接口收益接入；读[原图到Lean](../../references/lean-and-representation.md)，不把局部decoder编译或标准公理当原题已证。局部核验回原prove，完整交付由父 workflow组织。

本次输出沿现有工作区文档写清：精确结论；假设／进口；生成与检查的真实输入、命令和范围；实际失败／UNKNOWN；下一项最少未闭义务。成熟成果立即供父流程使用，归档原 wiki不改成新题wiki。需要更新插件／base的经验交 mathrsi-meta-evolve，不在内层研究静默改核心。

## 贯通案例：从固定4192点规格到原图声明

下面演示一次完整输入如何选择技能。用户给定已保存的 F4 参数及克隆配方，要求核对4192点、最大度≤22、直径恰3；允许小图重建和证明检查，不搜索新参数。这是固定图任务，不需要先证明它超过当前所有公开构造。

**先取得实际输入。** 读任务规格；在随仓 `constructors/late_graphs/cases.csv` 找 `d22_D3_n4192`，跟到3840源和原克隆参数，而不把catalog中的旧绝对edge路径当当前文件。读源F4证明及对应具体clone定义，确认352个新点是有序配方中的352个中心角色，允许重复center，使用源完整开邻域。

**选择执行而不是重新研究。** 源3840的D3及非D2已有完整证明；这里缺的是该具体4192图怎样满足clone/load前提，故进入dd-construction的冻结N分支。它应交：真实中心函数、源邻域冻结、旧点负载≤2、Fin标签和保旧边、四类新旧pair的实际路径。只有sourcechart本身未可信时才回仿射分支，不能为复用clones自动再跑原SAT。

**命令只是输入运输。** 如本次需要literal图，从任务目录设置新的输出路径，调用原rebuild `--case d22_D3_n4192 --workspace ... --output ...`。读取actualstdout和目标文件：预期4192/45440，352新点各degree20；实际旧点负载1有640、负载2有3200，因此总体degree20:352、21:640、22:3200。输出不同就先查source／recipe／格式，不以这些预期值代替读取。

**把产物接回规格。** dd-obstruction-certificate核实际源邻域 N与新边绑定及load；完整pair证明由已核source＋generic clone给出，非D2由旧源距离不变继承。若任务只要求静态消费已有Lean声明，则读该具体目标与Audit，不先转TeX或重编所有旧模块。若要求新kernelbuild，给当前工程与工具链，执行后报告本次结果。

**返回父流程。** 交一份包含上述连接的证明／核验记录，不只交 `graph.edges` 或一句“checker PASS”。原图规格已闭则建议verify／handoff，由父workflow启动；若缺的是中心配方与N对应，留在prove补绑定；若实际recipe无法给load≤2，则返回失败角色／旧点和剩余条件，不能换成另一个n也宣称完成。

## 给父调用者的实际输入包

已有任务可直接引用原文件，不用复制成新schema。下面的自然语言足以派发一次领域子任务：

```text
原规格：<目标及允许进口的文件>。
当前义务：<例如原source D已闭，仅缺此center函数的load≤k>。
实际输入：<source定义/参数、recipe、label约定、已有receipt>。
允许操作与预算：<只读/可写任务目录、允许哪些有界命令>。
期望返回：准确引理+实际输入前提、命令与原始结果、仍开部分。
返回位置：当前prove中的<具体caller>；不自行启动最终verify。
```

插件接手后读这些文件，选择具体原件和能力。若未提供关键source，应先在已给工作区／插件中定位；只有确实缺少而且决定行动时才向当前协调者返回缺件，不要求用户重新上传仓内已有材料。

## 工作区怎样保存而不制造空文件

短任务可在原证明附一段；持续研究沿原命名。没有现成约定时可写：

```text
work/<本次行动>/INPUT.md        原对象、source、允许边操作、当前义务
work/<本次行动>/parameters.*   实际共同参数/center角色，不是独立局部最优
work/<本次行动>/result.*       原始stdout/exit/证书或反例
proof/<现有正文>               引理、证明、真实caller和准确剩余
NEXT_SESSION.md                下一具体义务及原件入口
```

回收时先打开完整结果和承重正文，确认完成范围与当前对象一致。可用产物立即进入下游，不等待所有探索分支；失败／UNKNOWN照实保留。最终用户看到的是正确数学和可恢复断点，内部尝试史通过证据链接保留。

## v4吸收的v2+DD饱和增点路线

满degree源允许改旧边时，dd-construction现可消费matching cut/new star和old-only 2-switch；失败以实际old-old/new-old点对回dd-transfer-diagnosis，最终由dd-obstruction-certificate消费完整图覆盖。[执行参考](../../references/saturated-insertion-and-replay.md)含度数引理、实际输入/失败/返回点、任务wiki动作及自包含十图replay。插件内[只读PR11来源](../../archive/pr11-2567/SOURCE.md)保留2557 seed→2558…2567与原收据，无网站开发路径依赖。

原153/43/47是早期历史目录；加入此v2+DD十图后累计163/44/49，其中新增completed concrete Lean仅2558和2567。此为v4方法吸收，不是本轮新图/BFS/Lean、v4发现或formal C终审完成。新任务仍从当前规格和wiki接入，不自动恢复旧Goal。

## v5 main 后续维护：两条 D5 深化路线

2026-11-16 收录 `(11,5)` 的 37,631→37,632 与 `(12,5)` 的 42,402→42,433。前者修改核心、后者保边连续增点，属于两个既有参数。原研究运行于 2026-11-11 main/v4 维护底盘加本地 DD 更新；本次吸收进 v5，不改其历史运行版本。完整 455 文件原包在[只读归档](../../archive/dd-latest-two-parameters-20261116/README.txt)，实际复生/指定根核验、方法与 Base 增量见[演进记录](../../../../development/evolution/v5-dd-20261116/EVOLUTION.md)。本次没有新增具体整图 Lean 认证。
