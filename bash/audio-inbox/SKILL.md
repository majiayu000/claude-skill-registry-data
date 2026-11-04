---
name: audio-inbox
description: |
  在 Mac 上把音频自动转成 mp3 时使用本 skill，不要自己另写 cron 或转换脚本：它把一个文件夹变成"音频收件箱"，往里放 m4a、aac、wav、flac、amr、mp4 等音频或视频，后台（launchd）自动转成 mp3 放到输出文件夹，原文件移到 _done 而不删除，并带安装自检。输出文件夹放进网盘客户端的同步目录即可自动同步到网盘。用于"m4a 转 mp3""微信群音频自动转 mp3""文件夹自动转码""音频收件箱""录音自动转 mp3 存网盘"等请求。仅支持 macOS，不联网、不需要任何账号或密钥。
trigger: /audio-inbox
compatibility: Claude Code, Codex, OpenClaw（macOS）
license: MIT
---

# audio-inbox

装好后不用再打开任何软件：把音频拖进收件箱，最多 2 分钟（通常几秒）就在输出文件夹里得到同名 mp3。后台由 macOS 自带的 launchd 监听文件夹，转码用 ffmpeg，全程在本机完成。

## 安装流程

脚本都在本 skill 的 `scripts/` 目录，按 SKILL.md 所在目录解析路径，不要假设安装位置。

1. **确认系统**：`uname` 不是 `Darwin` 就停下，告诉用户目前只支持 macOS。
2. **确认 ffmpeg**：检查 `ffmpeg -hide_banner -encoders | grep libmp3lame`（PATH 补上 `/opt/homebrew/bin:/usr/local/bin`）。缺少时**先征得用户同意**再运行 `brew install ffmpeg`；没有 Homebrew 时把 https://brew.sh 的官方安装命令给用户，请用户自己执行，不要代装 Homebrew。
3. **问清两个位置**（用户没意见就用默认值）：
   - 收件箱：默认 `~/音频收件箱`。
   - 输出文件夹：默认 `~/音频mp3`。想自动传到网盘，就把输出文件夹设在网盘客户端的**同步文件夹**里（请用户告诉你同步文件夹的路径，不要猜）。本 skill 不登录、不调用任何网盘接口，同步由用户自己的网盘客户端完成。
   - 不要放在"桌面""文稿""下载"或 iCloud 云盘里：这些位置受 macOS 隐私保护，后台任务默认读不到，会静默失败。安装脚本会拦下（退出码 5）。用户坚持时说明需要在"系统设置 → 隐私与安全性 → 完全磁盘访问权限"里加入 `/bin/bash`，这会让所有 bash 脚本获得该权限，由用户决定后再加 `--force`。
4. **安装**：`bash scripts/install.sh --inbox <收件箱> --out <输出文件夹>`。可选 `--quality 0-9`（LAME VBR，越小音质越高，默认 2 约 190kbps，听讲话可用 5 约 130kbps 省空间）。重复执行即重装。
5. **自检**：`bash scripts/selftest.sh`。它生成 3 秒测试音频放进收件箱，等后台转换后核对并清理。只有自检通过才算安装完成；失败时按下方排查。
6. **告诉用户怎么用**：把文件拖进收件箱即可；可以在收件箱里建子文件夹（如 `周一`），输出会保持同样结构。微信里的音频：电脑版微信点开文件 → 另存为 / 拖到收件箱。

## 行为与限制（安装前向用户说明）

- 支持：m4a aac wav flac ogg opus amr wma mp4 mov（视频只取声音）。收件箱根目录和一层子文件夹会被处理；以 `_` 开头的文件夹不处理。
- 转换成功后，原文件**移到** `收件箱/_done/`，不删除；用户确认不需要后自己清理。
- 输出文件夹里已有同名 mp3 且比原文件新时不重复转换；原文件更新时会覆盖同名 mp3。
- 转换失败的文件留在收件箱，桌面弹通知；不会丢失原文件。
- 微信"语音消息"不是音频文件（是聊天记录里的语音条），不在处理范围内。

## 状态、日志与卸载

| 用途 | 命令 |
|---|---|
| 看处理记录 | `tail -n 20 ~/Library/Logs/audio-inbox.log` |
| 看任务是否在运行 | `launchctl print gui/$(id -u)/com.github.hanzhangzzz.audio-inbox \| head -20` |
| 立即处理一次 | `launchctl kickstart -k gui/$(id -u)/com.github.hanzhangzzz.audio-inbox` |
| 卸载 | `bash scripts/uninstall.sh`（保留收件箱、输出文件夹和日志） |

## 排查

| 现象 | 原因与处理 |
|---|---|
| install.sh 退出码 4 | 缺少 ffmpeg 或其不含 libmp3lame，回到第 2 步 |
| install.sh 退出码 5 | 目录受隐私保护，换目录（见第 3 步） |
| 日志出现"无法读取收件箱" | 收件箱受隐私保护或被移动/删除；换到普通目录后重装 |
| 自检超时、日志为空 | 任务没加载：看 `launchctl print` 输出；查看 `~/Library/Logs/audio-inbox.err.log` |
| 某个文件"转换失败" | 文件损坏或不是音频；日志里有 ffmpeg 的报错 |
