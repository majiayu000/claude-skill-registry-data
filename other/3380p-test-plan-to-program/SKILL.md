---
name: 3380p-test-plan-to-program
description: "根据详细测试计划生成、整理或修订 Chroma 3380P ATE 测试程序草稿。用于把测试计划翻译成可评审的 `.pln`、必要 `.dec` 或 `.pat`，尤其适用于 PLN 测试项、supply sweep threshold、register setup helper、WRITE_PAT_MEM 动态改 pattern、capture readback、DC measure、pattern 执行和 multi-site result/judge 逻辑。"
---

# 3380P 测试计划生成程序

## 核心流程

1. 先读取项目规则：`rules/3380P_project_style.md`。
2. 读取 `notes/test_plan_to_pln_generation_quick_reference.md`，确认输入契约、生成流程和评审检查清单。
3. 判断测试类型，只读取相关专题 notes 和索引：
   - PLN 骨架：`notes/pln_basic_structure_quick_reference.md`
   - DEC/PAT 关系：`notes/dec_file_quick_reference.md`、`notes/pat_file_quick_reference.md`
   - Supply UV/OV/hysteresis sweep：`notes/dc_supply_sweep_threshold_quick_reference.md`
   - 上电、unlock、register setup helper：`notes/register_setup_helper_quick_reference.md`
   - 精确 statement 语法：`doc_index/3380_language_manual_statement_index.md`
   - WRITE_PAT_MEM：`doc_index/write_pat_mem_statement_index.md`
   - Capture/TMU/AWI/tool 主题：按 `AGENTS.md` 中命名的对应 `doc_index/*_index.md` 查找。
4. 只有在用户给出路径，或任务需要项目专属名称时，才检查目标 `.dec`、`.pln`、`.pat`、helper header 或 legacy 工程。
5. 写代码前先建立一个小的输入契约。复杂转换任务应读取 `references/test_plan_workflow.md`。
6. 输出可评审的参考草稿，不承诺量产可用。必须说明假设、TODO、来源链路，以及是否未编译或未在 tester 验证。

## 必要输入契约

需要确认，或在草稿中标成 TODO：

- 目标函数名和测试意图。
- 目标工程或 DEC 路径，包括 `SET_DEC_FILE`。
- pin/resource 名称和 pin group。
- power、unlock、register write/read、protocol access、pattern load、cleanup 的 helper contract。
- register setup list、数值宽度、顺序和 readback 需求。
- sweep、measure 或 pattern 参数，包括方向、settle time、monitor threshold 和 limit。
- per-site result 变量、fail/default 行为、datalog 名称和 `TEST_NO`。
- relay、PPMU、DPS、capture、TFTM、C-bit、临时 pin mode 和 helper 状态的 cleanup 责任。

## 不要编造

不要编造芯片寄存器地址、bit field、unlock key、协议时序、PAT label contract、force range、current clamp、pass/fail limit 或 tester 验证状态。缺少来源资料时，如果会阻塞实现就问用户；不阻塞时在草稿里写清楚 `TODO`。

## 输出规则

- 除非用户明确要求 `.dec` 或 `.pat`，优先输出 `.pln` test item 草稿。
- 保持 DEC/PAT/PLN 职责分离。
- multi-site 行为必须保留 `[SOCKET]`、`[NUM_SITES]`、`SOCKET_INC(FRZ_OFF)`；只有必要时才使用并说明 `FRZ_ON`。
- 量产结果使用 `DATALOG_MSG` 加 `JUDGE_*`、`JUDGE_VARIABLE` 或 `JUDGE_RESULT_MS`，不要依赖 `printf`。
- 每个打开的资源都要在同一个 test item 中 cleanup，或明确交给命名 cleanup helper。
- 输出时保留来源链路，指向实际使用过的 notes、indexes、examples 或 legacy 文件。
