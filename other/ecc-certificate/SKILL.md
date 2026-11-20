---
name: ecc-certificate
description: 核验二元线性码的实际矩阵、分类覆盖、陪集保存集与pair拒绝证书，并审计Lean归约的显式前提及实际数据连接。接收verify或prove的具体义务，返回精确范围和真实运行产物。
---

# ECC Certificate

接收一项可独立说明的ECC验证工作：实际生成矩阵是否满足原参数，分类目录是否覆盖，保存的合法陪集是否完整，pair拒绝是否逐项有效，或Lean出口究竟证明了什么。上游通常是 `mathrsi-verify`，也可以是 `mathrsi-prove` 中的局部核验。先读当前规格、正文相关引理、实际输入和调用者要取回的结论，再选本技能的对应段执行；不要为了一个矩阵启动全部历史证书复验。

本技能提供普通确定性核验，不依赖发现阶段模型服务。需要Python≥3.10，pair重放需C++17编译器；图规范化另需pynauty，Lean另需固定工具链和mathlib。可用能力与本次实际安装分别报告。归档副本及其历史结果是证据来源，不是新运行结果。

数学对象和研究方法读 [mathrsi-ecc](../mathrsi-ecc/SKILL.md)，完整数学链读 [结构归约](../mathrsi-ecc/references/reductions.md)，原件范围读 [archive说明](../../archive/README.md)。独立运行可完成本scope并回交；嵌入verify时不递归启动另一轮最终verify/proof-checker，也不抢先启动handoff。

## 1. 先把要验证的命题写成实际输入

从上游拿到当前n/k/d、F₂、是否允许零列、构造或否定路径、原矩阵/母码/集合/证书路径、基和坐标约定、覆盖所需完整域以及已有证明。缺少某项连接就定位它：程序能读输入，并不意味着这个输入来自任意假想目标。

例如“已核F”可能分别指所有保存成员距离正确、两保存集相同，或所有2³²代表均判定过。把当前工作明确为其中哪一项，检查所选程序的真实读域，不将它们合并为一个PASS。否定证明通常需要以下相接但不同的事实：

|义务|实际检查|还不能推出什么|
|---|---|---|
|显式正构造|原n列、k行、满秩及所有非零消息重量|其它码不存在|
|代表合法性|母码秩/距离/偶性/满支撑|目录无遗漏或互不等价|
|目录覆盖|原域归约＋N个互不等价实际代表＋同域至多N类|每个代表无目标扩张|
|保存F成员|每个保存向量距母码达阈值|没有漏掉合法向量|
|F完整性|完整商域遍历/覆盖证明，或足够强的形式证据|pair拒绝有效|
|pair拒绝|每个i<j有实际低权见证，严格EOF|F无遗漏或母码覆盖原题|
|Lean归约|最终定义/类型/证明/公理及实际caller|显式参数已经核内证明|

向父流程说明选择了哪条义务、为何足够改变当前行动。例如已证明目标必含某固定母码的相容pair，且F完整、pair全拒绝，则该母码关闭；无需再查三重和。但只有一个母码关闭时不报告全域不存在。

## 2. 实际矩阵：检查原参数并返回失败见证

整数行用bit j表示第j坐标，消息bit i选第i行，异或是F₂加法。先确定行文件与预期n/k/d分别来自哪里。期望值必须从规格传入，不让候选JSON自己决定验收阈值。

本插件的普通入口读取JSON整数行列表或带 `rows` 的对象。对新候选，保存原矩阵而非搜索器缓存的码字。下列命令从**MathRSI仓库根**运行；用当前任务的实际scratch路径替换示例输出。程序全枚举2^k−1，先估当前k是否可承接，不把大维数抽样称精确验距。

```sh
python3 -B plugins/ecc/tools/check_matrix.py \
  --matrix TASK/scratch/candidate.json --n 43 --k 10 --distance 17 \
  --output TASK/scratch/matrix-result.json
```

检查行数、每行0≤r<2^n、GF₂秩，Gray遍历全部非零消息。结果给实际秩、精确最小重量、谱以及最小权消息/码字。退出0且报告PASS才表示这个矩阵满足传入参数；退出1的FAIL仍留下真实反例，可回prove修改候选。输入解析错误不是数学反例。若秩不足，非零消息可能映到0，报告的0重量正是原满秩条件失败，不能据此讨论距离达标。

归档五个下界/172母码的整体检查使用原件：

```sh
python3 -B plugins/ecc/archive/source/computation/check_data.py \
  --output TASK/scratch/finite-data.json
```

它实际枚举五矩阵71,675非零消息及172母码21,844非零消息，检查母码参数、全部字/重量一致性与四次多项式恒等式；同时读历史覆盖数。它不做图规范化，不读取pair大流，不重跑商域。`d₂(45,11)≥16`矩阵是44位距离16矩阵补零，不能读成距离17构造。

## 3. 分类目录：合法、互异和覆盖分别装配

原归约须先把任意目标送入正确母码域；本案例是满支撑偶[40,7,18]，不是projective。数据检查确认172份实际矩阵合法。互异性使用40坐标＋128全部码字的两色关联图：坐标置换对应码等价，所有码字顶点避免生成基选择影响。规范化得到172不同对象，结合E2同域至多172类才能封口。

原catalogue入口不调用manifest，不依赖缺失pair流。安装pynauty==2.8.8.1后，从仓库根运行：

```sh
python3 -B plugins/ecc/archive/source/computation/reproduce.py catalogue \
  --output-dir TASK/scratch/ecc-catalogue
```

入口及参数见 [REPRODUCE](../../archive/source/REPRODUCE.md) 与源码。没有pynauty或本轮scope不要求重新互异核验时，可复用 `verification/certificates/catalogue/catalogue_check.json` 的历史结果，并明确本次未重跑；不将源码存在写成执行成功。本轮未新增另一个图规范化框架。

若目录仅是已知库，没有文献类数上界或其它穷尽覆盖证明，回交“已知代表库”。同谱不等于等价，hull分布33/62/77只是交叉一致性，不能替代全部坐标等价类覆盖。

## 4. 保存集读回：运输到共同表示后比较

本例每母码偶商为2³²域。A使用零主元33自由位压缩整数、保留偶代表；B独立选反向主元32维偶商基，以Gray次序遍历实际40位向量。比较前把B接受字用A线性正规化映射回共同压缩坐标。仅比数量不够。

精简分发仍保留全部172例两套保存集、输入及完成结果。冻结 `common.py` 会连pair路径也检查，因此提供薄适配 `tools/check_saved_sets.py`：原检查数学逻辑不变，仅用 `relocated_manifest.py` 解析它实际读的original_scan/independent_full_F路径，不解析从不读取的pair流。

```sh
python3 -B plugins/ecc/tools/check_saved_sets.py \
  --manifest plugins/ecc/archive/source/evidence/manifest.json \
  --output TASK/scratch/saved-sets.json
```

返回172例429,024条保存记录的一一Gray展开、完整基秩、正规化、重复检查、两接受集精确相等，并核历史全域完成标记。这是**保存证据读回**，没有当前执行2³²域。若出错，保留首个不一致的实际行/母码/基，先判断输入绑定或运输错误，不能通过取交集删记录修成PASS。完整性仍由已接受的历史双全域扫描及域覆盖论证承担。

新任务若没有完整性证据，回prove补全域生成或其它覆盖证明。不能因保存成员全合法就把complete前提标为真。原完整扫描计划与执行命令在REPRODUCE，必须显式授权当前大域计算后才加 `--run`；本技能的轻量复核不会隐式执行它。

## 5. 一个完整母码pair证书：真实可复制例子

随仓母码index169 `catalog_after163_169` 有546个F代表，全部148,785个无序pair的7位拒绝消息，148,785字节二进制流。它是完整固定母码例子；其余171流仅登记原包路径，不能拿此例替代全172母码。

冻结原C++checker固定172批次。`tools/replay_selected.cpp` 只将批次数检查放宽为1..172、保留原编号，并将结果键从all172改为all_selected；矩阵运输、系统主元、128母码字、F距离、逐pair低权、索引/消息与EOF检查全部保留。`replay_one.py` 读manifest及实际矩阵快照，生成单例计划、编译、执行并读取native结果。

```sh
python3 -B plugins/ecc/tools/replay_one.py \
  --index 169 --output-dir TASK/scratch/ecc-one-mother
```

输出目录必须不存在且不能位于冻结source下；编译器默认c++，可传 `--cxx clang++`。脚本实际编译一次C++17并执行，保存编译与运行命令/退出码/日志、literal计划、逐例JSONL和native结果。程序重新核实际矩阵经坐标置换与扫描矩阵码字集合相同、主元系统形、所有546×128=69,888条F距离，以及每对 `wt(F_i xor F_j xor uG)<16`，并要求流严格结束。它不重新计算最小距离，只需要一个低权拒绝字。

完整结果应为一例PASS、546成员、148785 pairs、全部EOF、零无效/非拒绝见证、F_domains_rerun=0。编译失败、超时或native FAIL保留原输出，不当成数学排除。缺流会明确返回未分发路径；不能造空流、跳过pair或删除记录补PASS。

若持有完整发布包并按原路径补齐171流，可直接用原 `verify.py certificates` 在新输出目录重放全172；其中还需pynauty。精简插件不自动下载、合成或重建这些流，不宣称全包自包含重放。

## 6. Lean：核最终类型及实际矩阵，而非只查axioms

先读 [混合Lean边界](references/lean-boundary.md)。两个工程固定Lean4.34.1与各自manifest，不运行 `lake update`。原 `verify.py lean` 不依赖缺失pair流；执行它会把工程复制到新输出目录，从没有本项目olean的源码状态构建，允许复用固定mathlib依赖缓存。

```sh
cd plugins/ecc/archive/source
python3 -B verify.py lean --get-cache --output-dir /ABS/TASK/scratch/ecc-lean
```

`--get-cache`需网络和工具链，已有固定packages可用 `--dependency-cache /ABS/path/to/packages`；用绝对输出，避免复制目录后相对路径误解。这个有网络/构建成本的动作按当前scope决定，本轮插件实现仅复用已保存的构建/类型/公理日志，没有再次执行Lean。

阅读最终 `#check` 类型及定义，列出显式theorem参数各由哪份数学或计算证据提供，再读传递公理。无sorryAx只排除相应未证公理，不会自动填入hE1/hE2/hComputed。实际目录数据在CatalogueData、实际下界矩阵在LowerBoundData/TableLowerBoundData，通过MatrixBridge/Packed接到Submodule与MinWeight；只编译一个 `Certificate → MainClaim` 无法证明任意原输入已有Certificate。

新输入改变后，不能以旧矩阵Lean定理证明新矩阵合法。先对齐行/坐标/实际声明，再决定替换数据后核内验距还是保留外部普通检查。42/16下界当前只由Python全枚举，ECC42 Lean归约没有核它。

## 节点范围与父结论连接

调用方采用节点推进时，先读其 node_id/task_id、准确谓词、实际输入和[归属记录](../mathrsi-ecc/references/node-research.md)。检查本次结果究竟关闭哪个局部域，是否覆盖调用方声称的范围；共用任务分别说明对每个消费节点的含义。缺少归属时先退回范围核对，不因任务完成就批准数学节点。

若申请关闭父节点，另外核子域覆盖父域的论证、所有必要子证据及其假设、未覆盖补集和失效依赖；单个母码闭合、任务全部完成或重叠子域计数之和均不足。候选见证则直接核原存在性规格。证据修正时标出受影响依赖并回原义务，不改写历史为已通过。详细状态和恢复规则仍由当前工作区维护，不另建核验账本。

## 7. 消费产物、修复和恢复

向父调用者返回：检查的精确命题、实际数据/参数、命令和输出、完整读域、未重跑/未闭义务、结论怎样接原caller。构造PASS可以直接供存在路径；局部pair PASS只供该固定母码排除；历史覆盖与现次读回分别写出；Lean参数和常规公理分别说明。

失败先回对应义务：矩阵低权回候选修订；运输/编码不一致回同一表示证明；F完整性缺失回全域覆盖；分类域不匹配回结构归约；Lean暴露数学缺口回prove，单纯API或工具链问题留在形式化内部。不要把所有失败都返回路线从零开始。

恢复先读上次结果和首个错误，不覆盖已生成目录、不重跑未改变的范围。已核产物及时交回，上游决定同轮下一步。验收记录见 [IMPLEMENTATION](../../evidence/IMPLEMENTATION.md)，本轮真实范围不升级旧题数学状态，也没有恢复45/11研究。
