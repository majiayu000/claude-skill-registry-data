---
name: jyr-draft
description: 用代码生成剪映专业版 / CapCut 国际版(macOS) 草稿并放到首页。多轨、切碎、变速、转场、关键帧、画中画、文字与识别字幕、贴纸、特效滤镜、BGM 淡入淡出、踩点；读 / 改 CapCut 草稿副本。草稿在剪映 / CapCut 里打开、微调、导出。当用户说"用代码做剪映草稿 / 生成剪映工程 / 把素材拼进剪映 / 做 CapCut 草稿 / 剪映升级了"时使用。
---

# jyr · 剪映 / CapCut 草稿（核心）

所有命令：`jyr <命令>`（未安装时在仓库根目录用 `python3 -m jyr <命令>`）。CapCut 加 `--app capcut`（只装了一个就自动用它）。

## 0. 第一次用 / App 升级后
```bash
jyr doctor            # 找到剪映，读版本号；status 应为 ok
jyr adapt             # 报 "not in jyr's version table" 时跑，然后在剪映里打开一份生成的草稿确认
jyr --app capcut catalog scan   # CapCut：从你自己的 CapCut 草稿学资源（区分免费 / Pro）
```

## 1. 写计划 → 生成草稿 → 上首页
计划是 JSON，时间单位**秒**。最小示例：
```json
{"name": "我的草稿", "canvas": "9:16",
 "tracks": [
  {"type": "video", "clips": [
    {"src": "/abs/a.mp4", "in": 2, "duration": 3, "transition": "叠化"},
    {"src": "/abs/b.mp4", "duration": 4, "speed": 1.5, "fade": {"out": 1}}]},
  {"type": "text", "clips": [{"text": "标题", "start": 0.5, "duration": 3,
     "style": {"font": "auto:title", "size": 12, "color": "#FFD400", "stroke": {"color": "#000000"}},
     "transform": {"y": 0.6}, "keyframes": {"opacity": [[0, 0], [0.5, 1]]}}]},
  {"type": "audio", "clips": [{"src": "/abs/bgm.mp3", "volume": 0.6, "fade": {"in": 1, "out": 2}}]}]}
```
```bash
jyr build plan.json --out /abs/work/build1 [--publish] [--name 名字]
jyr publish /abs/work/build1 --name 名字      # App 必须完全退出
```
字段全集见 `docs/plan-format.md`。要点：
- 片段不写 `start` 就接在同轨上一段后面；不写 `duration` 就用到素材结尾。
- 资源用界面里的中文名。**默认只能用免费资源**（剪映 175 个：转场 推近/叠化/闪黑/滑动/翻页、特效、贴纸、字体等）。用户说自己是剪映会员 / CapCut Pro 时，计划顶层加 `"member": true`（或 `jyr --member build ...`），会员转场、蒙版、文字动画也能用；没声明就点名会员资源会报错并提示。`jyr catalog list transition` 能看到每个资源是 free / paid / ?。
- `"auto"` = 免费资源里你最常用的那个；字体 `"auto:title|subtitle|body|handwriting|cute"`。
- 第一条 video 轨是主轨，应从 0 开始、连续；画中画放后面的 video 轨。
- 转场挂在前一段上，后面必须紧接下一段；末段不能有转场。

## 2. 读 / 改草稿（永远改副本）
能读的：CapCut 草稿、jyr 自己生成且剪映还没存过的草稿。剪映存过的草稿不读——要改就改计划重新生成。
```bash
jyr --app capcut list                        # 首页草稿
jyr --app capcut inspect "草稿名"            # 轨道、文字、丢失素材、用到的资源
jyr --app capcut srt "草稿名" --out a.srt    # 字幕存成 SRT
jyr --app capcut edit "草稿名" --replace "旧=>新" --relink-dir ~/素材 --add-srt a.srt --name 新名字
```
`--ops ops.json` 支持：replace_text / relink / track_volume / remove_tracks / add_subtitles / shift。

## 3. 成片
jyr 不操作 App 界面。告诉用户：在剪映 / CapCut 里打开草稿，微调后自己导出。

## 安全
- `build` 不碰 App；`publish/edit` 只**追加**首页条目，写前自动备份到 `~/.jyr/backups/`；App 开着会拒绝。
- `edit` 永远在副本上改，原草稿不动。
- publish 前抽帧看一眼素材本身（黑屏/占位图查不出来）。
