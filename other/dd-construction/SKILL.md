---
name: dd-construction
description: "Construct degree–diameter graphs from a real source and a proved coverage interface: current-radius extensions, frozen full-neighborhood clones, affine route-image unions and opposite-GQ spread fill. Use during route or proof development; return an actual graph definition and all-pair/degree proof or exact missing assumptions, not a parameter formula alone."
---

# DD 构造推进

输入是原目标、具体源图／控制器／几何输入、允许修改的边、当前度数cap、已有距离进口和本次写域。没有源图时可以推导条件定理；不要凭公式 `30q³` 或 `δR²` 声称已构造。新文献进口有疑问先把实际应用交survey，返回后继续同一义务。

读取[构造数学](../../references/construction-mathematics.md)的相应条目。每个条目有准确假设、结论、证明和实际caller；下面按实际行动使用它们。

## 1. 保边逐点增加：当前图覆盖是义务

在当前简单图G中选择旧邻域S：`|S|≤d`，每个s尚有一度余量，`⋃ B^G_{D−1}(s)=V(G)`。新点只接S，旧边全部保留。度数与覆盖共同给直径≤D；一次成功不自动验证后续添加。

先从实际余度点找覆盖来源：几何blocking set折叠、旧邻域、anchor／guard补残余，或直接覆盖模型。保存选中点的真实标签、当前度数和未覆盖目标。只数总余度不够。第一份真实S通过后，再决定是否联合多个S保留后续资源；记录顺序而不是只保存最终点集合。

已有103步D5配方可通过本克隆的 `"$DD_PLUGIN/archive/source/constructors/early_d5/verify_covers.py"` 重放当前B4并，无需重跑源D5 all-root检查；[运行说明](../../references/programs-and-replay.md)给准确命令及继承范围。新题另有源D证据，不能把这三个源的进口搬给它。

D2时是从余度点选闭支配集；合作helpers必须支付内部边的度数并检查各自旧目标覆盖。D3完整N克隆定理不能直接降D2，先读构造数学的D2接口。

对有已绑定几何核心覆盖证书的 D5 源，先读[联合补全与实际坏点对反馈](../../references/d5-joint-completion.md)：在证书域内取包含极小核心命中集，再从**全部当前余度点**联合补齐剩余覆盖，按折叠后的真实端口成本计费。不要把旧模板、固定核心/尾部配额或首个命中平面当成必要条件。精确限定的 D12 754 平面驱动与已验前缀收件接口见[有界批次](../../references/d5-blocking-batches.md)；其它源先重新绑定，不只改常数。

## 2. 冻结完整N：先证明图对象，再优化负载

适用时定义固定源G、中心函数c:I→V。一次性取每个 `N_G(c(i))`，新点只连该集合，不加new-new，旧边保留。c可重复，中心可相邻。按原源距离0／1／≥2分类证明clone–clone距离；不预设中心独立。

旧点负载为所选完整邻域的重数。先证明每个新N确等于源N，再计算load和新点degree；源非正则时不能统一按正则度数计边。有限域plane横截每个portline，可将整fiber分割变为controller负载。先核所有dart共用同一个plane与坐标transport，不为每个目标换plane。

冻结的是实际source，包括其bonus/filler。若修改后source是G1，后续clone必须使用G1的真实roles；diagonal规则的hub不能直接套旧H collapse。先接正确定理，再生成实例，细节见[完整案例](../../examples/frozen-clones-and-diagonal.md)。

容量上界可以筛掉无意义端点，但可行负载不等于完整图：导出每个实际center／N／标签，核与原规则一致。用原构造器重建时先读所选case参数，输出写任务工作目录，不改archive。

## 3. 仿射lift：同时解决无向性与全部层对

从实际finite field、controllerports、方向和dart矩阵开始。正反dart是实际线性／半线性函数的真逆，方向transport使noise可消去。项目归一逆可能差非零scalar，不能直接当3×3真逆；F11反例保留在失败地图。

写每条短路线的目标像 `M_w x+c_w+H_w`。按相邻、非邻、同fiber等完整分类，决定某类靠单满秩路线、共同pencil还是多个coset并。必须对同一源x／同一参数套件同时成立。若每路线rank失败，先看原目标是否只需并覆盖；若某必要controller路线不存在，fiber chart通常救不了投影障碍。

四port F5实例在q>5相邻pencil已不足，不能照换域。六port F9、七port F11的PGL半集分类和反向port类型不同；读实际局部库，不复制“sortedneighbors任意可用”到F11。新q／维数／controller先做代数及短词门，再决定生成大图。

有限门返回可行chart时，构建真实邻接，核每点邻居互异、无loop、反向、度数及路线全域。SATassignment只能在完整literalCNF校验和实际参数恢复后用；若失败返回明确route／inverse／target，不以总坏对分数代替缺口。

## 4. Opposite-GQ：从真实incidence到完整图

已有实际GQ incidence、共线投影、spread owner时，源顶点为(point,line)。邻接由交叉incidence定义，自flag处去loop造成一度余量。每条spread的所有incidentflags作为新helper pins，partition掉余度，旧点对由projection短Walk，新helper对由实际两侧incidence连接。

要给的是所有projection前提与实际标签绑定，不只是一个几何名称。已有q4/q7/q8原件可复用，不能据它们证明任意q相同对象存在。partialovoid×spread中心允许相邻，通过两种唯一性证明openN disjoint；不错误要求partialovoid一定达到理论上界。

若uniform fullcopy同cap后续被privateclasses容量挡住，允许研究真正改边规则。diagonal省边＋hub是新对象，需新pair分类；成熟G1后才可用冻结N复制新roles。不要继续在不变对象上增加随机顺序。

## 5. 交实际产物，供原caller消费

生成前保留定义、参数、预测和本次预算；成本包括输入处理、生成、保存与必要独核，不把小rankkernel时间当整条成本。优先复用已核构造器；只有明确缺口才新增薄适配。

结果含实际vertex／edge定义、n/m/degree、完整pair证明、有限输入绑定、生成与检查范围。保边继承哪些旧点对、新roots测了多少、哪些由定理覆盖，分开写。存在性命中可停止搜索并验这张图，不要求证明搜索穷尽。完整候选回父prove／verify；条件引理有价值但缺source前提时，保留它并交准确caller缺口。

## 展开执行A：先接通一个冻结源，再扩大克隆数

假设父prove已有简单无孤立源G及D≥3，给中心列表，但负载／标签还没接上。先在本次任务中写 `source = <实际定义或文件>` 与 `centers = <有重数的列表>`，明确旧点标签范围、新点第i项对应哪个center；相同center的两个索引不能去重。

读source的实际邻接与既有D证明。对每个center从这个source导出一次N，保存为该角色的pins；生成器之后只读取此冻结数据。若源用公式，直接列出其N；不必先解析一份巨大边表。选择一种方便的表示后，用一个相邻centerpair和一个重复centerpair核路线：相邻为 `i–c(j)–c(i)–j`，同center为共同oldneighbor的2步。这样实际caller在大批生成之前已经明确。

随后计算每个oldv的load及每个newi的degree。若采用plane压缩，先证所有实际 dart都把该plane横截到noise line，再把controller负载向量代入；其中一个dart不满足就返回它的实际矩阵／交向量，不能继续只检查其它dart。

如本次目标固定某个 case，可从当前任务工作区复用原构造器。将 `DD_PLUGIN` 替换为当前克隆的真实插件绝对路径，`TASK_DIR` 是本次任务目录；程序与输出分别由这两个位置决定：

```sh
DD_PLUGIN="/path/to/MathRSI/plugins/degree-diameter"
TASK_DIR=$(pwd -P)
run_dir=$(mktemp -d "$TASK_DIR/dd-replay.XXXXXX")
python3 -B "$DD_PLUGIN/archive/source/constructors/late_graphs/rebuild.py" \
  --case d22_D3_n4192 --workspace "$run_dir/source" --output "$run_dir/g4192.edges"
```

读stdout确认真正执行的是该case；读header和实际new-old边，将每newlabel的N与相应冻结源邻域 N比较，检查没有new-new且所有旧边保留。不要将rebuild退出0当作这几个比较已经独立完成；需要的literal核查由当前verify任务明确承担。

交回如下连接，形式可以是现有正文一节：

```text
Lemma：本次source与center函数满足完整N克隆定理。
前提供给：sourceD/noisolates→<证据>；load/newdegree→<证明或结果>。
对象绑定：old/new labels、每角色sourceN、保留oldedges→<实际输入>。
结论：全pair≤D、最大度≤cap；原source非D2时新图非D2。
未做：是否新BFS/新Lean/公开比较；不隐含其它检查。
```

若load超cap，返回具体oldv及所有贡献角色；若N不匹配，返回角色和缺／多的pin；若只是源D没有被接受，返回缺的源进口。它们分别回负载选择、输入运输和源证明，不笼统重开整个研究。

## 展开执行B：共同路线并如何变成真实caller

当父任务报告“单rank路线失败”时，先读取controller word、实际矩阵／noise、被漏的目标层对。写原义务：对任意source x，所有允许≤D路线像的并覆盖该目标 fiber；不要先改成每条route满rank。

对一个实际pair计算每条route的 `M_w x+c_w+H_w`。选reference只为把中心统一，必须证明每条 `im(M_w−M_r)⊆H_w`；用矩阵列空间包含或符号证明都可以。再将相对coset `(c_w−c_r)+H_w` 在实际field中求并。输出应含word真实端点、matrix／noise生成、reference、包含证据和未覆盖residual，而不只有每个rank数。

一般代数的reference可只是比较用的仿射映射，不要求它是一条word。源15552的[实际共同coset应用](../../archive/source/research/ddp/two_successful_methods_20261101/retained_edge_transfer/published_d15_15552_D4_source_gate/GLOBAL_COSET4_NOTE.md)则只选从a到同一b、长度≤2的实际reference word。97组尝试中保留6次首reference失败；91组成功证书覆盖原缺失的3648个控制器对，其余33216对沿用rank-4 word。读原件可复用这些证据，不默认重跑91组。包含条件失败时换有依据的reference或保持多中心表示，并说明新义务；并仍漏点时给具体residual，不据此排所有maps。

有完整覆盖后，将目标y减去reference中心，选能命中该residual的实际word／noise，得到端点正确的状态序列。在15552源中，序列长度≤4；仅删除连续相同完整global label的virtual stay。同控制器不同fiber、同fiber不同控制器都保留，其余步骤是真实源图边，才形成长度≤4的walk。这一选择、端点等式和原邻接桥是下游caller所需；只有空间计数不能交完整图证明，阶、度与非D3另有义务。

## 展开执行C：小构造成功后怎样收卷

已保存参数产生实际graph后，先核当前对象而非继续优化。若原目标为存在性且simple／degree／全部pair／精确D都闭，交候选证明与适用验证，不为达到更好margin自动加k或换q。若只得到条件机制，明确缺的是GQ存在、controllerGOOD、plane横截还是负载可行；条件工具仍交回wiki供复用。

碰到公共基线更强，只对竞争型下一动作重判；已经构造的合法图与Lean不删除。需要换连接时把实际变化交transfer-diagnosis，旧事实逐项继承，不机械重编原source或重跑全roots。

## 部分折叠源：坏点对反馈到前部选择

若反例证明固定前部已不可能靠剩余端口修补，立即带实际坏点对返回前部选择。D11 的[部分折叠改色案例](../../references/d5-joint-completion.md)通过共同颜色与平面端口选择、分量方向调整及共同锚点交集修复全图。改了核心边就重开相关旧点对义务：实际核心定理与标签绑定覆盖核心内部，最终图全部旧外围根及新根覆盖其余点对，不能只验新根。

## 饱和源的局部增点：cut matching、new star与可选旧点switch

源已满cap而当前任务允许删旧边时，读[饱和增点与有限编辑](../../references/saturated-insertion-and-replay.md)。接实际G、matching M、d/D、允许修改和源距离证据；删除M并让新点连全部端点，先用逐点损益证明degree与simple，再在**同一最终图**接old-old/new-old全部距离。需要时合法old-only 2-switch保持度数但重新开启受影响距离义务。返回具体cut/switch、完整图、全pair证明或失败点对；不能只返回新根PASS。

(10,4)2558…2567现有冻结配方可直接从插件archive重放，输出写当前任务，不重跑发现搜索。详细输入、合法性证明、错误返回、CLI和历史receipt范围均在该参考。失败交transfer-diagnosis；完整图交当前prove/verify，当前任务wiki记录实际delta及新旧证据，插件archive保持只读。
