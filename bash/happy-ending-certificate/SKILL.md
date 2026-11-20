---
name: happy-ending-certificate
description: 独立核验25点signotope染色、九洞共享标签证书（N(8,6,6)<=61）、原生边界迹稀疏整数对偶与松弛上限见证（N(9,8,8)<=688, D_9<=458）、公开遗漏树有限算术，或检查55层历史证据与结构证明接口；返回精确局部证据，不将矩阵见证、分数松弛或抽象见证扩写为几何实现或已审全证。
---

# Happy Ending证据与实际对象核验

本技能接base verify或领域prove的一条准确义务，返回原caller，不另启动全证审计。输入为原规格、完整颜色/坐标或CNF与证书绑定、待核命题、允许进口、输出目录和返回点。先读[领域定义](../mathrsi-happy-ending/SKILL.md)及[证据边界](../mathrsi-happy-ending/references/failures-and-evidence.md)。恢复只查上次未完成的输入/检查，不重跑历史SAT或将模型UNKNOWN作不存在。

## 1. 验证一个显式25点抽象下界

当前仓库有实际2300行TSV，0蓝1红，顶点1…25。薄checker只读TSV，以标准库独立重建全部路径长度及状态，不导入旧SAT辅助变量。仓库根可直接运行：

```bash
python3 plugins/happy-ending/tools/check_lower25.py \
  plugins/happy-ending/archive/source/working/package/proofs/sat-756/color.tsv \
  --output /absolute/task/output/lower25.json
```

输出父目录由caller先建好；不要覆写archive历史收据。路径含空格时正常shell引用。只要求本固定见证的任务可以这样调用；此脚本固定n25及对应谓词，不是任意n/r/s通用checker，换题须读取并适配真实逻辑后按新规格核验。

读取退出码和结果JSON：三元组必须完整无重复、所有12650四点packet合法；DP状态(start,penultimate,last)用位集保存**全部精确可达长度**，两点为基，追加末三元组递推。于是不用依赖待审的路径缩短引理，也能对300外端点检查长度和9的全部颜色组合。另以12格的4096子集枚举下集，得35=25普通+10异常，重建25实际状态互异及e=m9。

通过只证明这个抽象见证的下界N_sig756≥25。它不提供平面坐标，不证明几何实现、全域上界25、55UNSAT或ES≤78。失败时返回首个TSV格式/packet/路径/状态差异与实际输入；若见证本身非法，就修数据来源或撤此候选，不归罪于原全称定理。与历史checker结果一致是本次独立实现的有限核验，不能称另一人/另一机器重现。

本轮真实执行结果在[IMPLEMENTATION](../../evidence/IMPLEMENTATION.md)，脚本默认不联网、不发solver。

## 2. 消费或接续55单元上界证据

上界调用先给数学反例类，核`1≤t≤e≤10`与N=26+e−t，前层归纳确迫m=t−1。注册表只支持三角域记录无缺失；`VERIFIED_UNSAT`是原历史状态，不是本轮重放。实际资料在[sat-756](../../archive/source/working/package/proofs/sat-756/README.md)：JSON/CSV、源码片段、E10–E20收据、EXTERNAL-MATERIALS以及原人类接受链。

原55 CNF与证明主体均未随包，登记证明总3,878,666,467,578字节，约3.879TB；检查器/部分生成闭包也外部。当前无法从此克隆重放这些UNSAT。需要新复核时，明确索取对应原CNF、原证明、历史checker与封存runtime/生成闭包，确认当前任务授权与实际资源；不要直接运行旧Linux绝对命令，也不要拿新默认编码配旧DRAT。原A88中断checker不能算通过，后续完整GRAT/gratchk收据与C8接受分别按原范围消费。

每个单元的关键数学边是“任意真实反例可扩展成这份CNF的满足赋值”。核三元颜色极性、terminal精确定义、状态注入、e/m等式、totalizer与额外bridge/F3的必要性。外路径单向闭包不能直接拿来精确计状态；compact另保精确terminal，原E23有7点反例说明。源码的旧颜色组名可能反写，按实际true=red语义判断。

固定CNF的RUP/GRAT通过只证明该公式不可满足；schema规则有效也不等于所有真实对象都进入这份公式。Closure曾只达dictionary-to-symbolic-schema，actual CNF equality与UNSAT未查，不能据Joint17固定RUP通过宣称外部C49迁到全signotope。返回实际已闭边与缺少的lifting/绑定，不把收据与覆盖拼成全域PASS。

## 3. 结构候选的具体核验

收到40/50/75/76候选（或旧76/77历史稿）时，先按完整稿确认所用版本、a/b进口和原保证状态；不要将55SAT当这些结构的直接证书。按当前scope核实际诱导集合、源/末角色重算、全部新增路径和共同匹配。若只给人口算式，取回它来自哪个真实核及哪份见证路径；若左右分别取了不同中间匹配，补同一匹配上的交会，不能将两个存在性结论相加。

chart核验同时检查packet、所有所需weak子集与目标短帽条件；显式映射及逆操作接回原X。反例必须在候选的原对象域，失败的启发式模板不是ES反例。参数改动重核M0供给和全域分流，不沿用旧缺额目录。实际论文/全证审阅由base verify组织；本技能只回局部结论及证据，不伪造proof-checker audit。

交回材料写明：精确谓词、输入、命令/实际范围与退出码；核了什么/缺什么；若有反例给可重建颜色/路径；证据怎样供给原caller的哪一箭头。下界复验通过就仅关闭见证合法性；历史上界作为具名进口；结构稿未经独审仍保原状态。75/76完整原件已在新archive，仍保持same-session/unreviewed/unaccepted；本技能的局部检查不替代完整独立数学验收。

## 4. 临界取等与端点相容的具体返回

prove/verify传来新替锁义务时，读取[取等执行说明](../mathrsi-happy-ending/references/equality-exchange.md)。输入同一X的临界n/w/t、M0/根分类进口、角色容器、全部外端口与其路径、C_D和换入换出集合；纯符号证明无需虚构颜色实例。逐条核：实际删点与角色覆盖的夹等式来自同一域；每个被归零项确非负；单射排重复owner；全锁序来自实际匹配；旧根排除先于最终替锁；F不交且无B5；容量被迫路径的末点、前驱和私有R5的端点确按原身份定位。检查同一k对应的外首对和最终长度4+5=9。只核人口式、只核一份匹配或两条端点不同的路径，保持相应箭头开放。

有小反例用于校准候选引理时，可在仓库根运行：

```bash
python3 plugins/happy-ending/tools/check_strategy_examples.py \
  --output /absolute/task/output/strategy-examples.json
```

caller先建输出父目录。脚本只检查新原稿中的两个固定抽象例：11点双红块的逐点R5供应不强迫跨侧R5，10点canonical A分别可加7/10但联合出现B4。枚举全部递增子集为路径，检查packet、帽长、同端长度和、实际角色和失败见证，不导入SAT辅助变量。通过仅确认这两个反例的陈述，不证明b容量、全称75/76、几何实现或regular共根定理。失败返回实际packet/路径/角色差异，先核数据定义。

若收到regular共根加权候选，另核增强根族非空、共同极值在I\Γ、I内锁序及w=0；再核各e/h/d松弛和精确人口式。n=3b只余e_L/e_R/d_D单单位支是该条件接口的结论，不能宣布原全域已归到这三支。返回记录实际使用的原件段落、逐式核对、运行命令/退出码与未核进口，由base verify决定整体接受；不把固定反例PASS写为原证明PASS。

## 5. 九洞共享标签证书、稀疏原生迹整数对偶与公开遗漏树重放

仓库根跨平台（macOS / Linux）标准库核验入口如下，均只向 `--output` 写入回执而不改动 `archive/`：

```bash
# 1. 九参数稀疏原生迹整数对偶（N(9,8,8)<=688 与 D_9<=458）及深度<=3 全部 47,635 行松弛上限见证
python3 plugins/happy-ending/tools/check_native_trace_cert.py \
  --check plugins/happy-ending/archive/nmrs-20261117/source/reports/n79-overlap-20261116/direct-cycle-lp/run-988-d2/compact-certificate.json \
  --output /absolute/task/output/native-988.json

python3 plugins/happy-ending/tools/check_native_trace_cert.py \
  --check plugins/happy-ending/archive/nmrs-20261117/source/reports/n79-overlap-20261116/direct-cycle-lp/run-d9-d3/compact-certificate.json \
  --fractional-witness plugins/happy-ending/archive/nmrs-20261117/source/reports/n79-overlap-20261116/direct-cycle-lp/run-d9-d3/fractional-grid.json \
  --output /absolute/task/output/native-d9.json

# 2. 八参数 N(8,6,6)<=61 九洞封包（语义重建 + 9 洞紧性 + 传入 --checker 时执行完整 DRAT 复核）
python3 plugins/happy-ending/tools/check_n866_milestone9.py \
  --directory plugins/happy-ending/archive/nmrs-20261117/source/reports/n866-joint-label-order-20261117/milestone9 \
  --checker /path/to/drat-trim \
  --output /absolute/task/output/n866-milestone9.json

# 3. 八参数公开 15 文件遗漏树有限算术重放（C_8<=193, D_8<=124）
python3 plugins/happy-ending/tools/check_octagon_omission.py \
  --output /absolute/task/output/octagon-omission.json
```

返回时严格写清每份证书的精确边界：`check_native_trace_cert.py` 从参数 `(q, p, inc, exc, weight)` 独立重建每条正权迹行与过载惩罚 $P$，零浮点认证 $C_9 \le 688, D_9 \le 458$（单行必要性与 R7/R20 几何装配仍属工作证明，`fractional-grid.json` 仅证深度 $\le 3$ LP 松弛上限为 124 而非整数点集）；`check_n866_milestone9.py` 认证 115 行共享标签编码与 budget-8 UNSAT（9 洞向量仅证该矩阵最小值为 9，不是 61 点 signotope）；`check_octagon_omission.py` 重放 Schroeder 公开有限遗漏树算术（不构建 Lean，也不自动认证 `EIGHT-CYCLE-TRANSFER.md` 的抽象循环符号 packet 桥）。
