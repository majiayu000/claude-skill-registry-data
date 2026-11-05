---
name: github-brainstorming-research-ideas
description: 调用已引入的 Orchestra Research 原版研究选题构思技能，比较研究问题、假设与验证路径；保留来源与本地科研保存约定。
---

# GitHub 原版 · 研究选题构思

这是本项目的中文接入说明。实际采用 [上游完整技能](../../vendor/skills/github-brainstorming-research-ideas/upstream/SKILL.md)；原始文件、脚本和参考资料按固定版本保留，没有以自编摘要替代原版。上游正文保持原始语言，按用户语言解释与交付。

- 来源：[Orchestra-Research/AI-Research-SKILLs](https://github.com/Orchestra-Research/AI-Research-SKILLs/tree/773a52944ba4747a18bd4ae9ade53fff041adcbc/21-research-ideation/brainstorming-research-ideas)
- 上游目录：`21-research-ideation/brainstorming-research-ideas`
- 固定提交：`773a52944ba4747a18bd4ae9ade53fff041adcbc`
- 许可：MIT，见 [保留的许可文本](../../vendor/skills/github-brainstorming-research-ideas/upstream-licenses/LICENSE.txt)
- 本次状态：已下载、接入并核对文件；已审读入口与关键依赖，未逐项运行上游脚本。

## 实际执行

1. 先读取上面链接的完整原版 `SKILL.md`，再按当前任务读取其 references、scripts 或 assets；不能只复述本接入说明。先定位含 `cli.mjs` 与实现契约的项目根目录，安装后的技能目录不是项目根。
2. 上游相对路径基于 `vendor/skills/github-brainstorming-research-ideas/upstream/`。优先用绝对路径调用文件；脚本是否依赖当前目录应先检查。不得因路径错误重新下载不同版本或覆盖原件。
3. 使用条件：纯文本选题工作流，无额外运行包、账号或模型 API 密钥要求；核查新颖性和现有工作需要可用检索工具。
4. 适配说明：原创上游完整单文件，未改原文；选题方案是 AI 建议，不能作为已完成实验或已核实创新。提及的 scientific-skills:literature-review 是其他技能推荐，不是已安装依赖；本项目可路由到已有文献综述技能。无脚本或跨目录文件依赖。
5. 读取脚本及其参数后，只执行当前任务需要且环境具备的操作。未安装的跨技能依赖、额外模型服务、上传/公开发布、付费计算不能从安装技能推导为已具备或已授权。原版的示例数据与提示文本不得当成用户科研事实。
6. 缺少原版必需工具时明确哪一步不可执行，继续可独立完成的部分；使用替代方法须说明差异，不冒称完整执行了原版。保持用户任务范围，不附加与任务无关的推广或改变客户端全局配置。

## 工作台与产物

需要登记时先读 [本地操作约定](../phd-manager/references/local-workflow.md)，沿用项目绑定及 `PHD_DATA_DIR`。科研记录只通过 CLI 读取当前 ID/version、预检所需批量变更、保存并回读。上游工具的文件输出不直接改 SQLite，也不替代这套流程。

独立材料处理不自动改台账。产物写到用户指定位置或项目 `outputs/`，不要覆盖原始数据或 vendor 原件；生成稿件、建议和运行命令不等于论文完成或实验成功。
