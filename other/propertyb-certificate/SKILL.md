---
name: propertyb-certificate
description: Build, repair, replay, or audit finite Property B probability certificates, connecting actual hypergraph inputs and complete local domains to exact arithmetic and the original coloring conclusion. Use for local coverage, common bad-pair deductions, independent arithmetic, or certificate assembly; use the bound research skill for a new mathematical route.
---

# Property B 证书与实际原图装配

把已经选定的Property B数学路线变成可检查、可复放、能作用于原H的证明。输入可以是一条局部分支、一个正在失败的概率型、已有整表或待接Lean caller。交付按当前缺口确定：精确数值证书、完整覆盖证明、独立复算、真实caller或整个原题装配；不要以“程序通过”混称这五种结果。

本技能不自动恢复旧研究、提高目标边数、启动整图枚举或强制Lean。主插件的[实务索引](../mathrsi-propertyb/references/practice/README.md)保存真实失败、计算方法、Lean性能与五个完整案例。需要新选点/新概率思想时将明确残缺义务交回领域研究；已有路线正确时直接实现与接入，不为调用技能另起框架。

## 接手：把任务读成一条实际义务

读原规格、最新证明/暂停报告、局部分支声明、已有checker及其输入；确定k、M、对象为有限简单k元、原结论为每原边有两色。不要把内部paircover/v范围/正则性/证书前提移到原题。边数预算M与下界m(k)≥M+1分开记。旧资料的活跃状态是历史证据，最新已授权任务才决定执行范围。

把当前产物放在“原H→实际锁/迹/配额→完整必要域→合法概率界→原染色”链上。只列真正未接的一两段，不创建评分或固定状态机。若已有完整证明链仅报告漏链接，读取后直接接回；若证明仅`Certificate H→PropertyB H`，查任意H的Certificate构造；若只有代表值，查有标号域的完整覆盖与代表运输。

第一次实现或更改通用接口时，用一个非平凡真实caller先试，尤其包括empty/singleton、非平凡大迹与真实坏对配额。不要等上万数值文件生成后才发现输入根本无法从H构造。Lean工程沿用既有对象/通用计数，不复制整引擎；普通精确Python检查可以足够，不强制形式化。

## 从原域得到真正该算的表

以下度数域公式取k≥2。最小顶点nonB归约通过合并从不共边的点、去重像边、染色拉回获得paircover，再用

    v ceil((v−1)/(k−1))≤kM

和精确均衡染色界筛全部必要v。若补边到M，证明C(v,k)≥M并统一使用同一补边H的度数。换M先重算整数端点与低度点数量，不直接沿用旧成功范围：M66六元新增44点，M542九元新增195点，M4663十二元起点91而非93。

取实际不同锁f:[s]↪V。定义每个T⊆[s]的count ℓ_T，包含空迹和singleton；核Σℓ=M、度数与共度边际。若大迹在单位锁条件下布尔/互交受限，先证明再剪枝，不能把一般可重复迹误作0/1。新增锁把同一旧迹纤维拆成含/不含新点，promotion受旧重数、新点度与共度容量约束；empty promotion由真实degree恒等式恢复，不是Nat截断减法的任意虚拟数。

对称压缩先有完整带标签域，再显式置换送代表。排序度数时，实际迹、位置与坏对数据随同一置换运输。三单位锁两种迹须全含；四单位锁K4六种带标签团划分保留triangle相对不等度数的标签。611可行大迹族/243代表、1796完整标签/844规范子域、3618容量分配/1993实际剩余域都不是同一个数量。

覆盖的检查是“每个实际H输入进入目录”。目录各行合法、代表不等价、行数正确只是辅助，不推出覆盖。用容量递归时复用`BoundedAllocations.mem_enumerate`与真实PromotionCatalog接口；不声称它们还证明了无重复/双射/每行可实现。

## 实现精确概率与共同删除

锁位置固定，其余命名顶点均匀注入N自由槽。可沿用二项式实现；独核宜另写下降阶乘计数。每位置h的终点/起点/临界对上界A/B/C必须指同一实际失败事件，最终

    U=Σ_h min(A_h,B_h,C_h−D_h)。

有序不同边对用ℓ_T(ℓ_U−1[T=U])；固定单交边对的共同点已确定，自由公共点因子仅1/N，不乘r_T r_U。左右自由点无放回联合安排，分母不是两次独立选择。先用N=5左右各2槽、120排列8成功即1/15的小例核归一化，再扩完整表。

对k≥3、中心x及避锁R子族，link大小k−1，实际不同link的交至多k−2，给

    q_R=max(0,ceil(((k−1)f_R−(v−1−|R|))/(k−2)))。

每实际无序坏对落唯一type胞，capacity为C(ℓ_T,2)或ℓ_Tℓ_U，删除成本是两个有序方向权重之和。零权胞保留；不可用q乘忽略零槽的正最小权。23点(6,7,7)末中心有capacity1双零槽，q≥2仅保证一个正槽。

多个避锁quota约束同一实际整数向量。可按当前必要成本选择：

- 完整共同整数最小化一次目标，遍历所有坐标（包括核心）；作者的强制核心优化需有证明或独核完整矩形胞验证。
- 各R分别给合法成本下界后取最大，常足够且更便宜；不能把它们直接相加。
- LP只找候选非负有理乘子，以容量罚项的精确dual验收，不信任浮点容差/最优标签。

不能换到更弱算法却沿用旧严格分数。需要公式与真实成功/失败数据时读[计算指南](../mathrsi-propertyb/references/practice/computation-and-efficiency.md)。

## 先定位活跃项，再补证书

失败型保存v、实际选择条件、count、布局、每h的A/B/C/D和赢家。令L=min(A,B)，扣除d的实际收益

    max(0,d−max(0,C−L))。

名义D改善但C−D仍非最小项，当前总界可能完全不变。T33二十点(7,9)的10/221名义删除实际下降零。别花整轮优化非活跃项。

若少数残型临界，复用已strict证书，定向加真实quota/新布局。23点group212在相同位置由12156/12155变2385/2431，就是有用新增；无需重做其余242代表。若大多数失败，或新quota完全不改变赢家，退回选点/共同对象诊断，不盲扩全表。已证明旧松弛解析恒等（21点component majorant等于旧U）则停止其余同类计算。

把失败含义写准：确有满足全部前提的反例才否定引理；K4,7压缩反模型/必要松弛可行只揭示信息不足；固定菜单界≥1不是所有布局最优；超时/栈溢出不是数学反例。[失败地图](../mathrsi-propertyb/references/practice/failure-map.md)有具体重试条件。

## 整数定向上界与精确比较

小表优先Python整数/Fraction，判strict比较正分母与分子，不用显示小数1.000000判等。大表若复用S=2^52定向算术，概率正项ceil(S p)、删除项floor(S w)，在舍入后的槽权上重新排序取q最低成本，含零槽。证明实际删除≥所扣值，每位置重新取min，最终总和U_num<S。

若用NumPy int64，核本次实际M² max(pair coefficient)和M max(endpoint)不溢出，非负收缩部分和被完整和界住；删除和最终position sum用Python整数，检查C−D非负。不要把int64自带“精确整数”误解为不会溢出。完整证明方向与历史实现见[十二元例](../mathrsi-propertyb/examples/k12-adaptive-coverage.md)。

## 独立复放：独立的是哪一层

读checker源码的import/read_text与write_text：它是否导入作者概率函数，是否自己重建域/trace，是否只遍历成功结果。重建domain键并比对，再用不同计数表示复算算术。布局可读原证书；概率不能只是照读原数。联合胞独核不要漏核心；组件配额可以换“至多预算”递归检验作者前缀截断。

所有会改写相邻JSON的旧程序在工作副本执行。下面是可直接本地试用的m6独核，不启动新研究：

```sh
PB_ARCHIVE="$PWD/plugins/propertyb/knowledge/archive"
PB_REPLAY=$(mktemp -d "${TMPDIR:-/tmp}/mathrsi-certificate-XXXXXX")
cp -R "$PB_ARCHIVE/context/propertyb-m6-66-20261029" "$PB_REPLAY/m6"
python3 -B "$PB_REPLAY/m6/independent/check.py"
```

从MathRSI仓根执行，Python标准库。预期379型、621579共同整数向量、全strict，最紧682298/682341；历史约1.49CPU秒。具体输入、公式、原题连接见[完整六元例](../mathrsi-propertyb/examples/m6-complete-proof.md)，不要将这次旧证明复放说成新m6≥67验收。

十二元`independent/check.py`必须读COMPLETE/CONDITIONAL/TAIL三JSON；它全域664355/tracePASS，但只20例概率Fraction，输出`complete_second_probability_replay:false`。不能为了统一宣传写成“全表双实现通过”。[能力地图](../mathrsi-propertyb/references/practice/checker-capabilities.md)列m7/m8/m9、反例与Lean的输入、输出和限度。

出现缺文件先补原依赖到副本；域键不等先定位漏/多输入；分数不等比较每h权、对角、方向、mask与分母；只有实际必要输入在合法公式下不strict，才回领域研究。保留失败见证和旧产物，不静默删除行、放宽原题或把assert关闭。

## 审阅和修正接在真实义务上

关键新选点/覆盖/概率公式/actual caller稳定后，使用仓内[proof-checker](../../../../base/skills/skills-codex/proof-checker/SKILL.md)或[research-review](../../../../base/skills/skills-codex/research-review/SKILL.md)，先读实际宿主入口。Claude入口同名在`base/skills/`；具体helper绑定本副本见[ARIS复用](../../../../docs/ARIS_REUSE.md)。不新造review客户端、不自动调用付费模型。

给审阅者原规格、正在承重的证明、实际输入/覆盖、checker源码与结果，问具体可攻击义务，不只问“是否同意”。第一次独立判断不灌执行者结论/另一模型答案。记录静态读取/实际执行、精确范围和未完成项；同家族标same-family/provisional，跨家族有效意见也不是形式证明或替代程序。

异议按见证/推导处理：若模型把无放回写成独立，回原样本空间核对；若反例不满足全部前提，保留它揭示的压缩边界，不改原题迎合模型。真实错误修复受影响公式/覆盖/caller并重新检查其依赖；未变材料不机械重审积累票数。外模调用失败不能记认可，也不阻塞不依赖它的本地证明。

## 最后接回原染色，并交给下游

每原H经内部归约和选择进入一个已覆盖实际型；合法非空条件排列空间中U<1给成功贪心排列；贪心终态没有全红/全蓝边；限制回原边、拉回商，返回原Bool染色。局部证书未消掉的假设写入条件引理，别冒称完整原题。

需要Lean时调用仓内[lean-formalize](../../../../base/skills/skills-codex/lean-formalize/SKILL.md)，使用[Lean实务](../mathrsi-propertyb/references/practice/lean-practice.md)。先试实际caller，数据/昂贵核验/dispatcher分开；构建指定新Main，再原题复述、实际定义类型与传递公理审计。默认旧Main成功不算新主定理；只有标准公理也不能排除`P→P`。本技能不改Lean信任边界。

交付用自然散文讲清新关闭了哪条义务，附实际源码/输入/输出、命令/退出码、完整覆盖范围、最大严格分数及进口。若只新增覆盖或独核，就明确它让哪条下游装配可以继续；若仍开，交出最小准确未闭输入和变化才值得重试的条件。复用已验证证书，已strict父型停止扩锁，剩余未知数学不按表行/文件数折算完成率或承诺“最后半小时”。

本技能本地使用证据见[实务阅读与重放报告](../../../../development/propertyb-rebuild/PRACTICE_READING_REPORT.md)。已完成旧结果、暂停35 Lean/36以及独立ECC项目保持原状态；技能执行不自动开启下一整数参数。
