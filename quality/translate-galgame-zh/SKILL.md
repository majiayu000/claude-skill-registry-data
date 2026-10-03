---
name: translate-galgame-zh
description: "将日语 Galgame、视觉小说和 Ren'Py/KiriKiri 等文字冒险游戏翻译为简体中文，支持可恢复的研究与解封包、场景级协作翻译、独立审校、回填、实机验证和补丁交付；也用于恢复、局部修订或审计已有汉化项目。"
---

# Galgame 本地化流水线

主智能体维护权威资料、批准任务边界、裁决术语、合并与交付；研究、翻译和独立审校可由原生子智能体执行。不要调用外部翻译 API。原始游戏目录只读，所有生成物写入独立工作区。项目事实、快照、任务与验证记录以文件为准。

## 按请求选择入口

- **完整新汉化**：建立准确游戏版本和文件清单，依次完成研究、无翻译往返、提取、校准资料库、场景任务、翻译与审校、回填封包、实机验证、补丁交付。
- **恢复或局部修订**：先审计状态和依赖，复用仍有效的证据与批准稿；只重做受影响部分。不要因全局版本数字变化就重译所有任务。
- **只读审计或文本建议**：按请求检查材料、报告范围。未完成实际封包和实机验证时，不宣称补丁可交付。

文中的“批准”通常指主协调者作出的项目判断，不额外要求用户逐阶段确认。用户已明确的范围与选择优先。

## 必须保持的约束

1. 完整补丁在正式全量翻译前，证明目标版本的解包→提取→无修改回填→封包→启动链路。
2. 所有原文单元有稳定 ID、原文/结构摘要、说话人、路线、场景和受保护标记；只按 ID 回填。
3. 按完整场景建立 job，分批只改变执行粒度。每个 ID 恰好属于一个 primary chunk，重叠原文只读。
4. 冻结事实、口吻、称谓、知识门、译例和生效决策。模型资料保留所需语义，来源与检索记录留在权威库；待批准提案不进入生效前缀。
5. 每个任务绑定自己的不可变前缀、依赖闭包和上下文。新旧批次可并存；依赖真正变化才定向重审。
6. 根据完整序列化请求和输出预留分批。脚本的 token 计数默认是保守规划估算，不能代替宿主实际窗口、工具返回上限和 usage。
7. 翻译与审校分别执行；独立审校覆盖完整场景，只输出需修订行和明确的覆盖声明。物化脚本不能替审校者制造“审校通过”。
8. 子智能体只写自己的任务产物。共享资料、任务表和最终脚本由主智能体单独写入；预留审校容量，避免大量草稿积压。

## 按角色和阶段读取

- 主协调者启动或恢复：读 [workflow-and-state.md](references/workflow-and-state.md)。已有项目升级、预算和性能诊断另读 [performance-and-migration.md](references/performance-and-migration.md)。
- 研究：读 [community-research.md](references/community-research.md)。技术与作品事实不限语言，中文惯例研究聚焦目标中文语域；复用已核验的准确版本证据。
- 解包、提取、回填、封包：读 [extraction-and-repacking.md](references/extraction-and-repacking.md)。使用 GARbro 时运行 `scripts/locate_garbro.ps1` 定位用户已安装的版本，可传 `-Path` 或设置 `GARBRO_PATH`；需要交互时加 `-Launch`。
- 字体替换、缺字或发布验证：读 [font-runtime.md](references/font-runtime.md)，分别验证字形覆盖和运行时实际字体选择。
- 翻译执行者：读或继承 [translation-contract.md](references/translation-contract.md)，无需重复加载协调、研究与发布手册。
- 派发与种子管理：主协调者读 [subagent-orchestration.md](references/subagent-orchestration.md) 和 [shared-prefix-and-batching.md](references/shared-prefix-and-batching.md)。不要把长期主对话完整继承给正式工作者。
- 独立审校、批准、全局 QA 与发布：读 [qa-and-release.md](references/qa-and-release.md)。

## 工具入口

- `init_project.py`、`build_manifest.py`：初始化与源文件清单；保留已有项目。
- `audit_project.py`、`set_stage.py`：检查阶段证据并逐级推进；不能靠修改 passed 或阶段字符串绕过错误。
- `plan_jobs.py`：生成新的任务建议文件，主智能体校核上下文依赖后批准。已有非空计划不会被覆盖。
- `build_shared_prefix.py`：编译稳定的生效资料快照；完整资料是默认，`--profile` 可使用经过主协调者批准的依赖闭包。
- `build_context_bundle.py`：单任务或 `--jobs …` / `--all-pending` 批量建包，共享一次输入快照。输出 `contexts/<job>/current.json` 指向不可变任务包。
- `emit_chunk.py`：校验后仅输出一个分批的模型 packet，避免把全部原文或 coverage ID 清单反复读入模型。
- `audit_dependencies.py`：只读列出可复用与需处理任务，不自动修改状态。
- `record_cache_probe.py`：记录逐请求缓存读写和 token。只有完整渲染边界与请求身份明确时才评估边界覆盖；未知值不伪装成零。
- `validate_translation.py`：检查草稿或批准稿的 ID、控制符、换行、术语和异常文本。
- `create_review_report.py`：记录独立审校者完成阅读后的明确声明；脚本本身不执行语义审校。
- `apply_review_delta.py`：核验已有独立声明后生成批准稿和单独的物化收据，保留原审校声明。
- `set_job_status.py`：执行合法状态迁移；`--also-job` 可批量提交相同迁移，失效返工须记录原因。
- `merge_jobs.py --jobs-jsonl …`：只合并任务表列出的批准稿，并核验物化收据，忽略历史备份。
- `audit_font_coverage.py`：检查最终显示文本和发布字体；不能替代实机字体报告。

## 完成交付

完整汉化补丁只有在目标 ID 覆盖、独立审校、自动 QA、封包、字体静态/实机证据、约定路线与安装测试均通过后才可交付。报告未覆盖路线、残留警告、构建标识和复现方法。演示数据、工具自测和合成场景不能充当真实游戏的发布证据。
