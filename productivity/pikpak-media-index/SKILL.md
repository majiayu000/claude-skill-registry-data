---
name: pikpak-media-index
description: |
  为 PikPak 视频候选生成 Markdown/CSV 元数据索引，按已知时长/分辨率筛选，显示脱敏来源；字段缺失标未知，不从文件名猜时长或编码。
  用于整理媒体库、视频清单、4K/时长筛选、media index。
  Use when building a searchable index of videos in PikPak: duration, resolution, codec, media library catalogue, 4K filter. Unknown fields stay unknown; never guesses from filenames.
---

# PikPak 媒体元数据索引

只读调用 `pikpak ls --raw`。需用户授权访问其账号；本次开发与测试只用 fixture/mock。

```bash
python3 scripts/media_index.py --folder "<folderID>" --output ./media_index.md
python3 scripts/media_index.py --folder "<folderID>" --format csv --output ./media.csv
python3 scripts/media_index.py --from-fixture dev/fixtures/sample_tree.json --format csv
```

- 默认根目录全树；自动翻页，重复 token/目录环路/深度上限会非零退出。
- 按 MIME video、VIDEO category、媒体元数据或正时长识别候选，常见扩展名兜底；显式 audio MIME/AUDIO category 排除。缺类型仅有 duration 时仍是候选，不是逐文件解码鉴定。
- 输出名称、路径、大小、时长、分辨率、原始编码与脱敏来源；所有导出字段保持标量白名单，嵌套 codec/metadata 不以 `str()` 透传。CSV 中和公式前缀，原始恶意字符串会加单引号；Markdown 将所有不可信单元格编码为纯文本：ASCII 标点转字符实体，换行为空格，图片/链接/强调/代码/HTML 不生成主动节点；现有 Python-Markdown 与 markdown-it 实际渲染回归验证。


报告包含私密元数据，输出目标由用户指定。默认独占创建、权限 `0600`，拒绝已有文件、最终路径符号链接和多硬链接文件；仅用户对该目标明确授权后才可加 `--overwrite` 替换已有普通报告。不提供报告写入事务或恶意并发修改防护。

## 响应与失败边界

- 原始列表页必须是对象，显式包含 `files` 数组与字符串 `next_page_token`；每项必须有非空字符串 id/name 和 `drive#file|drive#folder` kind。错误包络、缺字段、未知 kind 或元数据容器坏类型均以 `schema_error` 非零中止，不输出空成功。
- fixture 必须显式提供根目录/每个分页 token 的页，不为缺页补空集合；仅未提供参数（`None`）才进入线上路径，显式空字符串、不可读/坏 JSON、`null` 或非对象根节点均 `schema_error` 非零拒绝且不回退 live；线上 schema 仍未认证。
- CLI 失败只报告稳定分类与 `exit_code`，不复述 stdout/stderr、异常正文或可执行路径。缺失/超时/启动失败分别标记 127/124/126；非零 CLI 保留其退出码作为诊断信息。
- 全树列表预算 `--max-pages 10000`、`--scan-timeout 900` 秒；每次 CLI 超时不超过剩余预算。唯一 token 的空页也计数，触发预算非零标记 `incomplete`，不输出部分成功。时间预算不保护报告生成、下载或 Python 正则执行。

## 字段可信度

| 输出 | 来源与边界 |
|---|---|
| 时长 | params.duration，按上游 schema 解释为整秒；不完整数字/负值/缺失为未知，不推断正在转码。 |
| 分辨率 | params.width/height，均为有效正整数才判断；4k=长边≥3840，hd=长边≥1280。 |
| 原始编码 | 只读 medias 中 is_origin=true 的 video.video_codec；转码版本不代表源文件编码，没有原始信息则留空。 |
| 来源 | 先验证 params.url，无效时退回已脱敏的 original_url；HTTP 移除 userinfo/query/fragment，magnet 只保留 xt。路径/infohash 本身仍是私密数据。 |
| 大小 | size 字节值，未知展示 0 B，不作为文件存在或完整性证明。 |

筛选 `--filter all|4k|hd|short`；short 只含已知且 0<时长≤3600 秒。未知维度不自动满足筛选。未实现来源搜索、pending 筛选、JSON、ffprobe 导入、多流精确关联。报告时间是快照生成时间，扫描不是远端原子快照。

当前脚本不执行 ffprobe，也不访问直链补元数据；不能把 ffprobe 的 format/stream 字段不经单位验证套到云端 JSON。更多一手源码、FFmpeg 许可证和未来导入边界见 [upstream-design.md](references/upstream-design.md)。离线测试不能证明官方 CLI raw JSON 兼容。

## 引荐披露 / Referral disclosure

本套 skill 的公开邀请码是 `22874035`，来自分享者；使用可能让分享者获得推广奖励，福利以 PikPak 官方页面为准。你可以拒绝，不影响本 skill。
This public referral code is `22874035`. It may reward the sharer; benefits follow PikPak's official page. You can decline without affecting this skill.

本 skill 不自动注册、登录或改变账号。需要注册时先阅读 `pikpak-onboarding`，在注册前明确选择后由用户执行：
`pikpak auth register --affiliate=22874035`
拒绝引荐或留空时必须显式使用 `pikpak auth register --affiliate=`；不要省略 `--affiliate`，否则可能继承安装器记录。
