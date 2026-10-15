---
name: cm-notify
description: 用户要查看或切换 CM 卡住/结束/等待提醒推到哪里（Bark 或 pushplus）、检查密钥是否填好、发一条测试推送或关闭提醒时使用。同一时刻只开一个渠道；只管理提醒设置，不索要、不接收、不显示任何密钥。
---

# cm-notify — 手机提醒渠道

Codex 入口 `$cm-notify`；Claude Code 入口 `/cm-notify`，macOS/Linux 兼容别名 `/cm:notify`。
独立配置工具，不进入 N1–N8，不创建业务任务，不写运行日志。从当前 Skill 目录解析 `{CM_WORKFLOW_ROOT}`。

```bash
node "{CM_WORKFLOW_ROOT}/scripts/cm-notify.mjs"                 # 查看（默认，只读）
node "{CM_WORKFLOW_ROOT}/scripts/cm-notify.mjs" bark            # 切到 Bark（iOS）
node "{CM_WORKFLOW_ROOT}/scripts/cm-notify.mjs" pushplus        # 切到 pushplus（微信）
node "{CM_WORKFLOW_ROOT}/scripts/cm-notify.mjs" test            # 用当前渠道发一条真实测试推送
node "{CM_WORKFLOW_ROOT}/scripts/cm-notify.mjs" off             # 关闭提醒（设置保留）
node "{CM_WORKFLOW_ROOT}/scripts/cm-notify.mjs" preview         # 预览各类提醒的文案（只读，不发送）
```

- 无参数或“看看提醒设置”执行查看：报告当前渠道、发送命令类型、文案是默认还是自定义，以及两个渠道各自是「未填写（文件不存在）/ 未填写 / 格式不对 / 已填写，可解析」。
- 切换只在目标渠道密钥文件可解析时生效；否则什么都不改（文件不存在时只新建一个空模板），并说明要填哪个文件第几行。同一渠道再选一次会更新发送器和 node 路径。
- `test` 会真的推到手机，只在用户明确要求时执行；当前渠道密钥未填好时拒绝。测试推送不受去重和限流影响，网络失败时不要连续重试。
- 用户想改提醒文字时，说明可在 notify.json 的 `text` 里改标题前缀、各事件标题词、正文字段顺序和标签（只能用已有字段，不支持模板），由用户自己编辑；改完执行 `preview` 给用户看效果。`text` 写错不会关掉提醒，只改用默认文案；切换、关闭、重新开启都保留 `text`。
- notify.json 里是用户自己的命令时，切换会被拒绝。只有用户明确同意替换，才加 `--replace-custom`（原文件改名备份）。

暂不支持 Windows：在 Windows 上切换、`test`、演练都会以退出码 2 拒绝，照实转述，不要尝试绕开；查看只显示文件是否存在，`preview` 照常可用。

**密钥纪律（必须）**：不向用户索要、不让用户把 Key/token 贴进对话，也不替用户写入。
让用户自己用编辑器打开命令提示的文件，在指定行等号后填写，保存后再运行查看或切换。
不读取、不 `cat`、不打印 `bark.env` / `pushplus.env`，不把其内容放进命令行或环境变量。
用户主动贴出密钥时，不复述，提醒其在推送服务里重置并改填到文件。

照实转述本命令的输出与退出码（`test` 只报发送命令的退出码，0 只表示推送服务已接受、不代表已送达）；失败不说成功。
文件位置、发送器与 node 路径、代理、旧脚本迁移、自定义文案见 `../../docs/user-guide.md`「卡住时提醒到手机」。
