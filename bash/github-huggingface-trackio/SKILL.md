---
name: github-huggingface-trackio
description: 调用已引入的 Hugging Face 原版本地实验日志技能，整理用户指定的本地实验指标与日志；保留来源与本地科研保存约定。
---

# GitHub 原版 · 本地实验日志

这是本项目的中文接入说明。实际采用 [上游完整技能](../../vendor/skills/github-huggingface-trackio/upstream/SKILL.md)；原始文件、脚本和参考资料按固定版本保留，没有以自编摘要替代原版。上游正文保持原始语言，按用户语言解释与交付。

- 来源：[huggingface/skills](https://github.com/huggingface/skills/tree/fabc634a893f62ad5c2039830397efa35fa62715/skills/huggingface-trackio)
- 上游目录：`skills/huggingface-trackio`
- 固定提交：`fabc634a893f62ad5c2039830397efa35fa62715`
- 许可：Apache-2.0，见 [保留的许可文本](../../vendor/skills/github-huggingface-trackio/upstream-licenses/LICENSE.txt)
- 本次状态：已下载、接入并核对文件；已审读入口与关键依赖，未逐项运行上游脚本。

## 实际执行

1. 先读取上面链接的完整原版 `SKILL.md`，再按当前任务读取其 references、scripts 或 assets；不能只复述本接入说明。先定位含 `cli.mjs` 与实现契约的项目根目录，安装后的技能目录不是项目根。
2. 上游相对路径基于 `vendor/skills/github-huggingface-trackio/upstream/`。优先用绝对路径调用文件；脚本是否依赖当前目录应先检查。不得因路径错误重新下载不同版本或覆盖原件。
3. 使用条件：运行指标读写需另有 Python 和 trackio 包；本地模式无需模型 API 密钥。HF Space 同步需联网与账号授权，云资源费用取决于用户选用服务。
4. 适配说明：仅处理用户指定的本地实验日志；默认不云同步、不设置 webhook、不自动改参重跑或持续监控。HF 自动创建 Space 可能默认公开。其 references/retrieving_metrics.md 尾部 docs/source/cli_commands.md 和 docs/source/api_mcp_server.md 不在技能包或本仓库中，是外部 Trackio 项目文档引用；如需要应查官方 Trackio 文档而非假定本地存在。
5. 读取脚本及其参数后，只执行当前任务需要且环境具备的操作。未安装的跨技能依赖、额外模型服务、上传/公开发布、付费计算不能从安装技能推导为已具备或已授权。原版的示例数据与提示文本不得当成用户科研事实。
6. 缺少原版必需工具时明确哪一步不可执行，继续可独立完成的部分；使用替代方法须说明差异，不冒称完整执行了原版。保持用户任务范围，不附加与任务无关的推广或改变客户端全局配置。

## 工作台与产物

需要登记时先读 [本地操作约定](../phd-manager/references/local-workflow.md)，沿用项目绑定及 `PHD_DATA_DIR`。科研记录只通过 CLI 读取当前 ID/version、预检所需批量变更、保存并回读。上游工具的文件输出不直接改 SQLite，也不替代这套流程。

独立材料处理不自动改台账。产物写到用户指定位置或项目 `outputs/`，不要覆盖原始数据或 vendor 原件；生成稿件、建议和运行命令不等于论文完成或实验成功。
