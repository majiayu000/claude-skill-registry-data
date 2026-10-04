---
name: handoff-codex
description: 向 Codex (GPT-5.6) 咨询复杂问题 / 要第二意见 / 派发需要强推理的任务。后台运行，完成后自动通知。支持并行多任务，支持续接（resume）上次会话继续派发后续任务。
---

# handoff-codex Skill

<interaction_contract>
This skill is executed by Claude Code (an AI agent). The rules below are BINDING — follow them exactly; do not simplify or reinterpret.

派发一个任务 = 两条命令 + 等通知。照抄模板，不要改结构。

## 第 1 步：建任务文件（前台，秒回）

```bash
handoff new --backend codex --slug <≤3个英文单词的任务助记词> --write <<'__HF_EOF__'
[prompt 内容]
__HF_EOF__
```

它只打印一行绝对路径，例如：

```
/Users/x/.handoff/tasks/0720-cx-06-fix-auth.prompt.md
```

去掉目录和 `.prompt.md` 后缀，剩下的 `0720-cx-06-fix-auth` 就是本次任务的 **RUN_ID**。
记住它。三个文件路径由它直接推出，**不需要再从任何输出里捕获**：

| 路径 | 用途 |
| --- | --- |
| `~/.handoff/tasks/<RUN_ID>.prompt.md` | 你刚写的 prompt |
| `~/.handoff/tasks/<RUN_ID>.result.md` | **结果**，任务完成后读这个 |
| `~/.handoff/tasks/<RUN_ID>.out.txt` | 进度日志，仅诊断时才读 |

## 第 2 步：按参数表执行（必须 `run_in_background: true`）

根据用户本轮要求，只能选择下表对应的一行，不得自行增删 `--pro` / `--fast`：

| 用户本轮要求 | 新会话：`run` | 续接：`resume` | 后续行为 |
| --- | --- | --- | --- |
| 未提 Pro，也未提 Fast | `handoff run --backend codex ~/.handoff/tasks/<RUN_ID>.prompt.md` | `handoff resume <首次RUN_ID> --backend codex ~/.handoff/tasks/<新RUN_ID>.prompt.md` | resume 自动继承会话上一轮的 Pro 状态；Fast 关闭 |
| Pro（或要求更强/专业模型） | `handoff run --backend codex --pro ~/.handoff/tasks/<RUN_ID>.prompt.md` | `handoff resume <首次RUN_ID> --backend codex --pro ~/.handoff/tasks/<新RUN_ID>.prompt.md` | Pro 状态持久化，后续 resume 自动继承 |
| Fast / Fast Mode / 明确要求加速 | `handoff run --backend codex --fast ~/.handoff/tasks/<RUN_ID>.prompt.md` | `handoff resume <首次RUN_ID> --backend codex --fast ~/.handoff/tasks/<新RUN_ID>.prompt.md` | Fast 只对本轮有效，下次 resume 默认关闭 |
| 同时要求 Pro + Fast | `handoff run --backend codex --pro --fast ~/.handoff/tasks/<RUN_ID>.prompt.md` | `handoff resume <首次RUN_ID> --backend codex --pro --fast ~/.handoff/tasks/<新RUN_ID>.prompt.md` | Pro 持久化；Fast 只对本轮有效 |

必须后台启动——handoff 耗时 2~20 分钟，前台会阻塞整个会话。Fast Mode 会以更高倍率消耗 credits。

## 第 3 步：等通知，然后读结果

等 Claude Code 的后台任务完成通知。收到后用 `Read` 读 `~/.handoff/tasks/<RUN_ID>.result.md` 汇报。

**通知一定会到。在它到达之前，禁止用任何手段去"看看好了没"**——禁止 `BashOutput`、`TaskGet`、`TaskOutput`、`Monitor`、`sleep`、`tail`、`cat`，禁止提前 `Read` 结果文件，也不要去搜索这类等待/轮询工具。
命令输出里的 `RUN_ID=` 和 `RESULT=` 都不需要读——第 1 步已经知道全部路径了。

只有 `.result.md` 为空或内容异常时，才读同名 `.out.txt` 诊断。

## 其它硬规则

- `--slug` 只写≤3个英文单词、`-` 分隔的语义助记词（如 `fix-auth`）；禁止日期/时间戳/随机数/UUID/计数器，唯一性由 `handoff new` 自动分配的 seq 保证。
- heredoc 界定符固定用 `__HF_EOF__`，prompt 原样粘贴、不转义。
- 不要自己拼任务文件名，不要用 `> RESULT 2> OUT` 重定向——handoff 自己管命名和落盘。
- 回显任何 home 下的任务路径时，缩写成 `~/.handoff/...`，不要暴露 `/Users/<name>/...`。
</interaction_contract>

## 多任务

- **并行**：先在同一条消息里发出多个第 1 步（前台 `handoff new`，各自不同 slug），拿到各自 RUN_ID；再在同一条消息里发出多个第 2 步（`run_in_background: true` 的 `handoff run`）。之后分别等通知、分别读各自的 `.result.md` 汇报。
- **串行**：等上一个的完成通知到达、读并汇报后，再开始下一个的第 1 步。

## 续接上次会话（resume 续派）

要保留某次任务的上下文继续，而非开新会话：第 1 步照旧建新的 prompt 文件，第 2 步把 `run` 换成 `resume <首次RUN_ID>`：

```bash
handoff new --backend codex --slug <任务助记词> --write <<'__HF_EOF__'
[后续任务内容]
__HF_EOF__
```

然后从上方参数表的“续接：`resume`”列复制与用户本轮要求匹配的完整命令，并以 `run_in_background: true` 执行。

- `<首次RUN_ID>` 是该会话**首次**任务的 RUN_ID；它是稳定句柄，每轮续接都用它，不要追每轮新生成的 RUN_ID。
- 本轮结果落在**新** RUN_ID 的 `.result.md`，读这个。
- **必须带 prompt 文件**：不带输入文件的 `resume <RUN_ID>` 是交互式重开，后台会卡死。
- `--pro` / `--fast` 的选择只以上方参数表为准，不要从其它段落推断。
- 不确定用户指哪次任务时，报候选 RUN_ID + 摘要让其确认，别猜。
