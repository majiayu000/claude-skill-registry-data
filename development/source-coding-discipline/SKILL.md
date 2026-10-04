---
name: source-coding-discipline
version: 0.1.2
description: Use when a task involves reading, editing, reviewing, testing, debugging, refactoring, or otherwise working with source code files. Source paths include **/*.{py,ts,tsx,js,jsx,mjs,go,rs,java,kt,swift,rb,c,cc,cpp,h,hpp,sh,bash,zsh,sql,vue,svelte}. Do not use for docs-only, planning-only, or non-code file tasks unless the task also touches source code.
---

# 写码纪律（碰源码文件时加载）

> 镜像注：四段纪律正文与本仓库 `templates/rules/coding.md` 同源（路径相对 evolab 仓库根；本 skill
> 单独 cp 安装后该文件不随行，同步义务只落在仓库维护侧）——
> rules 形态给支持 `paths:` 条件加载的 agent（Claude Code / omp），skill 形态给不支持的（codex 等）。
> **改任一边必须同步另一边**（硬门：`test/mirror-sync.test.sh` 四段逐字 diff，漂移即红）；
> 同一 agent 勿两种形态同装（双重注入）。

**先思考再编码**：显式说出假设，不确定就问；多种解读全部列出、不静默选边；有更简单的路径就说出来；困惑就停下来问。

**简单优先——交付物代码零投机（仅限交付物；风险枚举 / 预判 / 评审轴不受此限、该大胆发散）**：不做超出要求的功能；单次使用的代码不抽象；没要求的"灵活性/可配置性"不引入；不可能发生的场景不写错误处理。写了 200 行能压到 50 行的，重写。自问："资深工程师会觉得这过度复杂吗？"

**外科手术式改动**：每一行改动都能直接追溯到用户请求。不"改进"邻近代码/注释/格式，顺应已有风格。自己的改动产生的孤儿（未用 import/变量/函数）要清；既有死代码指出来、不删。

**目标驱动执行**：把任务转成可验证目标——"加校验"→"为非法输入写测试并让它过"；"修 bug"→"先写能复现的测试再修到过"；"重构"→"改前改后测试都过"。多步任务先列简短计划：`步骤 → 验证`。强验证标准让你独立循环，弱标准（"能跑"）需要不停澄清。

**验证诚实性**：禁止声称测试通过、命令成功、文件存在，除非实际跑过 / 读过。未跑就说"未运行验证"。完成时简短说明：改了什么 / 跑了什么验证 / 什么没验证 / 剩余假设或风险。
