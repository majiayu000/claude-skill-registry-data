---
name: github-experimental-design
description: 调用已引入的 K-Dense 原版实验设计工具技能，设计随机化、分块与因子实验；保留来源与本地科研保存约定。
---

# GitHub 原版 · 实验设计工具

这是本项目的中文接入说明。实际采用 [上游完整技能](../../vendor/skills/github-experimental-design/upstream/SKILL.md)；原始文件、脚本和参考资料按固定版本保留，没有以自编摘要替代原版。上游正文保持原始语言，按用户语言解释与交付。

- 来源：[K-Dense-AI/scientific-agent-skills](https://github.com/K-Dense-AI/scientific-agent-skills/tree/593377bb048752abb0152deab9fbb1083a6087df/skills/experimental-design)
- 上游目录：`skills/experimental-design`
- 固定提交：`593377bb048752abb0152deab9fbb1083a6087df`
- 许可：MIT，见 [保留的许可文本](../../vendor/skills/github-experimental-design/upstream-licenses/LICENSE.txt)
- 本次状态：已下载、接入并核对文件；已审读入口与关键依赖，未逐项运行上游脚本。

## 实际执行

1. 先读取上面链接的完整原版 `SKILL.md`，再按当前任务读取其 references、scripts 或 assets；不能只复述本接入说明。先定位含 `cli.mjs` 与实现契约的项目根目录，安装后的技能目录不是项目根。
2. 上游相对路径基于 `vendor/skills/github-experimental-design/upstream/`。优先用绝对路径调用文件；脚本是否依赖当前目录应先检查。不得因路径错误重新下载不同版本或覆盖原件。
3. 使用条件：Python 3.12+与NumPy/pandas；生成DOE矩阵另需pydoe 1.5.0。仅安装依赖时需要网络，不需要API密钥。
4. 适配说明：用于真实采集前的随机化、分块、因子设计和批次规划；计划不能标为已执行。样本量或模型细节引用未收录的statistical-power/statsmodels/pymc时，使用本机可用工具并说明能力范围。 原文要求对有实质贡献的Scientific Agent Skills论文进行引用；本项目保留该说明，但科研引用仍应基于实际使用与核验，不自动插入无关引用。
5. 读取脚本及其参数后，只执行当前任务需要且环境具备的操作。未安装的跨技能依赖、额外模型服务、上传/公开发布、付费计算不能从安装技能推导为已具备或已授权。原版的示例数据与提示文本不得当成用户科研事实。
6. 缺少原版必需工具时明确哪一步不可执行，继续可独立完成的部分；使用替代方法须说明差异，不冒称完整执行了原版。保持用户任务范围，不附加与任务无关的推广或改变客户端全局配置。

## 工作台与产物

需要登记时先读 [本地操作约定](../phd-manager/references/local-workflow.md)，沿用项目绑定及 `PHD_DATA_DIR`。科研记录只通过 CLI 读取当前 ID/version、预检所需批量变更、保存并回读。上游工具的文件输出不直接改 SQLite，也不替代这套流程。

独立材料处理不自动改台账。产物写到用户指定位置或项目 `outputs/`，不要覆盖原始数据或 vendor 原件；生成稿件、建议和运行命令不等于论文完成或实验成功。
