---
name: dd-obstruction-certificate
description: "Prove or check a precisely scoped degree–diameter obstruction, exact finite certificate or fixed-graph claim. Distinguish necessary route capacity, shared assignment, solver UNKNOWN, complete enumeration, exact dual and actual graph coverage; connect each result to its mathematical caller without expanding the excluded domain."
---

# DD 排除、证书与原图核验

输入为当前精确命题、固定构造域／实际图、必要性推导、程序或证书及下游用途。任务可以只是核一个local gate，也可以装配完整固定图结果；先明确返回父prove／verify的哪一项义务。不要默认对归档所有图重新验距或编译。

读[排除与证书数学](../../references/obstructions-and-certificates.md)、[失败地图](../../references/failure-and-transfer.md)和本次具体原件。先写允许什么：是否保留旧边、允许旧旧补边、new-new、任意helper数、全fiber、线性／仿射／半线性、固定controller／群／phase、源标签和inverse。结论只关闭这些假设覆盖的域。

## 1. 先证明这个门为何必要

把原图路径投影或按最后新增边分类。新根无法到达一个目标可直接否定该候选；新根全部通过，删过旧边时仍可能损坏old-old。容量界中忽略额外冲突是放松，放松已矛盾才可排原域；放松可行不是构造。

controller距离3且唯一word时，所有三步fiber路径必须使用该word，内部修复边没有时间预算；rank或quotient matching条件因此必要。多个word时不能继续假定每个都须满秩。conic齐次规则下所有badword可能共同漏nucleus，才给更强必要性；一般矩阵或offset不能继承这个共同零点论证。

保边增广的饱和目标可给任意helper障碍；允许删边／增加旧旧边后按新规则重推。Exoo72跨侧matching旧证明对一般边界matching失效，应使用完整boundary route disjunction。发现反例先确定否定的是候选引理还是原始图目标。

## 2. 有限域、规范化和枚举的完整性

先给原参数到代表的合法transport：同构／gauge／单位scale／反向word／group law。非零元素不一定是unit；不能把非unit强制归一1。固定边方向后逆参数要按真正RIGHT／LEFT约定算，不凭符号名猜。规范化后joint约束仍须在同一参数上检查。

读实际loop范围、pruning、对称代表、停止条件和结果。记录完整参数数、实际访问、旧结果复用／skip、未试范围和反例。首成功停止适合存在性；首失败停止只排该参数。样本10000未命中仍是样本；原始 UNSAT无checkedproof按实际证据强度报告。

shared参数失败要保留实际相容性：global256固定域每个phase独立可覆盖32，但phase0和2没有共同参数，proper-subset witnesses具体存在。这与route数量不足不同，下一修法应释放共享关系而不是继续计数。见数学参考中的完整域与反例。

## 3. 数值发现与严格证书分别处理

UNKNOWN读真实incumbent／bound／退出信息，不补造字段。可以在新数学／资源授权下继续，但不以一次时限决定全族无解，也不自动重启相同调用。MIP数值infeasible与可重放整数证书分开记；已有证书足以排除必要域时停止更强无用计算。

exact dual检查应核原模型行的数学必要性、非负multipliers、所有列系数、RHS与整数取整。`tools/replay_mizuno_dual.py`直接读随仓MODEL和dual，重建365行检查364列；它不调用solver、不写archive。归档原verifier缺LP_INPUT且会写回，薄适配只补这一输入运输，不改变模型／scope。读[dual案例](../../examples/mizuno-exact-dual.md)。

DP给0边界时不要机械加表。Brown91使用逐组excess不等式，把全局界的等号进一步迫helper度数和为75，从而解析矛盾；DP是发现与辅核，最终结论由完整分类证明。若只是某个DP witness失败，不可排所有同资源pattern。

## 4. 核实际图：属性、范围和证据继承

字面边表核标签、header有无、simple、无向、degree／m。不要把只有edgebody的F9文件当第一行header，也不要按n合并两个不同case。用原case索引和实际格式。

旧边全保且源D已验，则old-old上界继承；新点全部BFS可补涉及新端点的pairs。只有少量新根BFS时，需由完整formula／fullN／对称transport证明其余，不能凭最大图删点推出所有prefix。全部all-rootBFS是一种完整证据，但不是每个新实例都必须重复旧roots。

独立checker应读实际图／参数并重建所需属性，不把producer的cachedpass当自己执行。相同程序第二次执行是复现，不是独立算法。公式图与字面文件之间的绑定、有限前提与数学route证明是不同连接。

## 5. Lean与返回

用户要求固定形式目标时可直接接真实Lean接口，见[Lean参考](../../references/lean-and-representation.md)。先看实际载体、Adj、label、最终类型及caller是否供给所有开发premises，再看指定module实际receipt和传递axioms。没有额外axiom不保证目标没被削弱；`Certificate→Target`仍须证任意实际输入有Certificate。

保留已编模块。纯API／表示性能问题在形式化内部修；新数学缺口回prove。构造全域覆盖、独立算术、kernel、模型review分别报告。归档中的完成记录可以静态消费，不称本次新build或他人独立复现。

交付准确命题、假设、原件／代码／输入、实际执行范围和结论用途。失败给具体target／参数／column／caller；只缺源文件就说明缺件，不升级为数学反例。原目标已由足够弱的必要门解决时，停止后继图生成；局部核验完成直接返回父调用处。

## 实际输入例：消费364列exact dual

父verify给固定Mizuno13源、full27 affine横截块规则，要求核“213块不可能”，不搜索新图。首先读[原exact证明](../../archive/source/research/ddp/two_successful_methods_20261101/mizuno13_clone_interface/source_dependent_geometry/controller213_capacity_gate/lp_exact_bound/PROOF.md)的第一段：**每个被选原fiber至多一个完整27块**，可各选斜率与phase。这个binary选择域是实际假设，不能省成任意数量块或一般14度图。

沿原几何证明核controller row和cost为何必要；打开MODEL看364行确按普通incoming＋Mmate计，Mmate重叠产生系数2，cost为203个5、161个6。输入必要性读明后，在当前任务工作区运行。`DD_PLUGIN` 按本次克隆确定为绝对路径；脚本从自身位置找到归档，不依赖任务的 cwd，也不向归档写结果：

```sh
DD_PLUGIN="/path/to/MathRSI/plugins/degree-diameter"
python3 -B "$DD_PLUGIN/tools/replay_mizuno_dual.py"
```

读取完整stdout，不只status。期望364列、min10001、Q10000、RHS2061908、bound515477/2500、整数T≤206；同时source_writes/solver_calls/graph_generation/Lean_runs均0。脚本检查原包缺LP_INPUT时从presentMODEL重建的同365行，不改证书或求解新dual。

返回当前verify：几何必要性由哪些原proof承担；本次所有列／符号／RHS的实际检查；因此本binary满块域T≤206，所需213不可能；nonlinear／partial／不同source不在域内。若父目标就是排此域，可以停止后继graph生成；若父目标为一般14度构造，只关闭这条路线并回prove，不宣布原题不存在。

若脚本字段缺失／coefficient不同，就把实际error、输入path和对应row／column返回，不以同一旧result替代。缺几何前提回prove；只有数据运输问题在本局部修；新的优化问题需当前任务授权和明确模型，不因已有replay入口自动启动。

## 实际输入例：删除边之后的新根PASS怎样消费

父prove给小源G，删matching旧边、添newstar，程序显示新根覆盖。先取得实际deletededges、pins、最终Adj与源D证据。由于旧边删除，旧D不是当前old-old全部的证明。

选被删边所承担的旧shortpath，按实际最终邻接检查相关旧点对。若失败，保存原source路径、新最短距离或无≤D路径的target；不能用“新根全部PASS”覆盖这项结果。反过来，若数学已证明除明确criticalpairs外旧路线均保留，就只需验证这些必要pairs，不强制所有root重复BFS。

对于106 internal-S模型，selected-selected由z修复，outside-outside保留所有旧两步边，即使middle在S；只有selected/outside需要exact新route。读code是否对每orderednonedge两方向均加条件，closedDom是否允许selecteddegree10点没有selected邻点。唯一solverUNKNOWN保持原样；某个对称pinshape被排只关闭该shape。

## 工作区记录与返回的最小完整内容

没有现成报告时，在当前run写一段即可：

```text
待核命题/原调用：<精确结论与父caller>。
输入与域：<source、允许操作、变量/标签、完整性依据>。
数学方向：<必要门/充分构造/等价模型/有限算术>。
实际执行：<cwd、argv、exit、结果路径、完整覆盖和未试范围>。
代入：<哪些原前提已供给；支持何结论；剩余条件>。
失败/恢复：<具体witness、下一项要改什么；返回哪个prove/verify>。
```

若只做静态审计，执行栏写实际读取范围和未运行；若读旧Leanreceipt，写历史build而非本次。已有证据未变就引用，不重生成同一报告。父流程收到后能直接代入命题、修准确缺口或关闭该有限域。

## cut-star候选的完整距离消费

[饱和源参考](../../references/saturated-insertion-and-replay.md)给matching cut/new star与old-only switch的精确对象。先核literal source和最终delta；degree引理不承担D。检查必须覆盖old-old和new-old，部分roots/超时返回实际覆盖域；失败返回具体pair、原路径所用cut及最终邻接下缺失路径，供当前prove联合修复。新root全部过而旧pair坏只否定当前候选，不排整个matching域。

静态复用PR11时按参考§4分别消费十图历史全根BFS、2558/2567 kernel/import和未完成formal C。当前最小replay只生成边表，不是本轮BFS/Lean或再次accepted-original比对；完整Lean工程不在插件中。实际运行结果及下一未闭义务写任务wiki，返回原verify/prove调用处。
