---
name: jianzhuxuezhang-image
description: 通过建筑学长已登录网页生成或编辑效果图，切换 GPT-image-2.5、豆包 Seedream 5.0 Pro、千问 qwen-image-3.0 等模型，按各模型当前可见选项设置比例和分辨率并下载核验。用于用户明确选择建筑学长通道或与其他生图通道比较。
---

# 建筑学长生图

默认站内 GPT-image-2.5、2K、1张；比例沿用用户要求或参考图比例，无指定时自动。豆包对应 Seedream 5.0 Pro，千问对应 qwen-image-3.0。网页名称是平台展示名称，不代表已核验其服务端供应商身份。

## 当前入口

复用 Chrome 已登录页面，进入 `https://www.jianzhuxuezhang.com/ai/banana_modifier/operate` 后再配置。首页点击提交会跳转并重置参数，不能把首页读回当作最终参数。用户偏好宽窗口/全屏，避免窄窗布局切换。采用浏览器运行时的 DOM 接口，无需桌面坐标操作，也不另开 Edge 配置文件。验证码由用户完成，不把口令、会话令牌写进脚本或日志。

在 browser/cua 运行时读完接口文档并取得当前 tab 后，导入本 Skill 的 `scripts/browser-workflow.mjs`。该脚本接收受管 tab，是网页脚本适配器，不是站点官方 HTTP API，也不需要用户另申请 API key。

Chrome没有出现在当前工具清单，不等于扩展损坏。先刷新浏览器清单；若与用户已连接的状态矛盾，可在未提交任务时重置一次 cua_repl 并重新取得清单。本次2026-10-10实测重置后Chrome重新出现；此仅是恢复案例，不能保证所有缺失都可自动修复。不要直接切到内置浏览器登录，避免多设备登录踢出原Chrome会话。

常规图生图优先一次调用 `flow.runImageEdit(tab, {referencePath, referenceName, model:'GPT', resolution:'2k', ratio:'自动', count:1, prompt}, {checkpoint, onProgress})`。`checkpoint(record)`负责把请求记录保存至本次项目；`onProgress`负责必要状态提示。此入口串起弹窗处理、上传、编辑弹窗“立即使用”、参数核对、单次提交、按结果控件等待和原图下载。等待最多5分钟，每段控件等待最多30秒；超时保留请求，改用 `finishImageEdit(tab, record, options)`接续，禁止重新提交。它不自动处理短信验证、不保存账号、不替代下载后的本地像素和视觉验收。

```js
// 先把 <CODEX_HOME> 解析为本机实际安装根；默认通常是 %USERPROFILE%\.codex。
var flow = await import('file:///<CODEX_HOME>/skills/jianzhuxuezhang-image/scripts/browser-workflow.mjs');
await flow.clearInterruptions(tab);          // 处理重新登录、广告及升级提醒；每步检查实际结果
await flow.models(tab);                       // 当前站内模型
await flow.selectModel(tab, '豆包');          // 也支持 GPT、千问或准确名称
await flow.capabilities(tab);                 // 当前模型实际可见的比例/尺寸/张数
await flow.uploadReference(tab, 'C:/绝对路径/原图.png', '原图.png'); // 上传后自动点图片编辑弹窗的“立即使用”
var run = await flow.prepare(tab, {
  model: 'GPT', resolution: '2k', ratio: '自动', count: 1,
  prompt: '用户本次确定的提示词'
});
await flow.submitOnce(tab, run);              // 仅在用户已授权生成时调用
await flow.resultStatus(tab, run);            // running / succeeded / failed / unknown
await flow.downloadResults(tab, run);         // 新结果完成后再下载
```

模型先切换，再读其规格，最后回读模型、尺寸、比例、张数与提示词。旧快速/精细参数在新版页面没有对应控件，明确拒绝，不随意映射。`new` 仅是徽标，不能作为模型版本的一部分。不要使用历史卡片或社区模板里的模型文字定位输入区。

弹窗与动画未结束时先处理阻挡，再继续。参数没有生效就停止提交；不能通过点击隐藏4K控件或默默降为1K获得表面成功。站内模型与三方付费模型是不同通道；未明确要求时不切入三方付费通道。

页面出现“本设备已退出登录”时，脚本选择“重新登录”并确认弹窗已消失；后续若需要短信验证码，由用户在页面完成。遇全屏推广弹窗先关闭；遇“升级提醒”先勾选并核验“不再提示”，再点“知道了”。按钮点击后页面未变化就停止并报告，不会把点击动作当成成功。此流程只在 Chrome 已连接的网页实测有效后才能宣称自动处理可用。

## 参考图、结果与恢复

- 图生图先读浏览器 file-uploads 文档，然后调用 `uploadReference`：打开本地上传、选择用户授权的原图、在图片编辑弹窗点“立即使用”、核对带原文件名的缩略图，再 `prepare`。2026-09-30 已在 Chrome 对实际工程图片完整实测；上传失败只依据当前弹窗做一次有界重试，不盲目重复提交。
- 提交前保存 run 与旧图片清单。提交仅一次，页面出现排队/生成中才标为 accepted；遇超时先核对历史当前任务，不重投、不重复扣次。
- 只下载与本次提示词/时间对应的新结果，优先网页原图下载按钮或受支持 downloadMedia。不要拿社区样例、旧历史、缩略图当输出。
- 实际文件像素用本地图片头/图片库读取，记录请求尺寸与实际宽高。2K/4K标签不是像素检验；不同画幅不得强拉成16:9。原文件保留。
- PNG可执行 `node scripts/verify-png.mjs "输出路径"` 获取真实宽高和SHA256；其他格式用合适的解码库，不改扩展名假装PNG。
- 一张测试成功只证明该模型该参数路径，模型切换成功不证明每个模型的生成都成功。
- 三张工程图用 GPT-image-2.5、2K、单张提交并下载已实测；01 选 16:9，02/03 选自动。返回图有 2048×1152 和 2048×1153 两种高度，需逐文件验像素。生成后自动读取结果并下载，避免逐步打开历史卡片。编辑弹窗上传是耗时步骤，优先用脚本串起选择文件和“立即使用”；出现 transient 控件未就绪时只做有界状态重试。
- 页面结果与必要截图、本次请求、实际参数、下载路径与宽高写入具体项目运行目录；不写入Skill固定样例，也不把账号资料放入打包。

已核对的网页能力见 `references/site-capabilities.json`；它是有日期的快照，运行时仍以可见控件为准。

## Chrome固定流程适配（2026-10-10）

使用已连接Chrome的受管tab，不固定易变化的浏览器/标签ID。当前工作区已实测：域名升级遮挡先关闭、输入区展开、上传编辑弹窗点立即使用、GPT-image-2.5/2K/自动/单张配置回读、单次提交、结果匹配下载。常规一次调用runImageEdit，不让模型逐按钮确认；仅状态变化或异常回报，超时接续finishImageEdit。点击后核对实际状态，不用鼠标移动模拟充当进展。当前是依赖浏览器运行时的DOM脚本，不是独立CLI/CDP或后台API，后台无前台占用尚未验收。
