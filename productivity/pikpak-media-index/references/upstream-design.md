# 媒体索引：上游字段与可信度

## 正式发行与研读快照边界

截至 2026-10-16，经公开 GitHub `releases/latest` 元数据核验，下列正式发行均非 draft/prerelease；这里只核验 tag、公开 release URL 与发布时间（UTC），不证明该发行源码或实际运行兼容。

- **rclone/rclone**：[v1.75.2](https://github.com/rclone/rclone/releases/tag/v1.75.2)，发布于 `2026-10-09T11:03:19Z`。
- **FFmpeg 发行未核验**：GitHub REST 端点 `GET /repos/FFmpeg/FFmpeg/releases/latest` 返回 404（以纯文本记录，文档不含可点击的外部 API 链接，运行时也不发起该请求），仅说明该 endpoint 未返回 latest，不能证明 FFmpeg 没有官方发行；[官方发行页](https://ffmpeg.org/releases/) 本次未核验。

下文固定 commit 仅是研读快照；与上述 release tag 的祖先关系未核验，不能称为稳定发行源码。许可证依据仍以列出的具体快照文件为准，不把 release 元数据等同源码、许可或线上行为认证。

## 一手来源（固定修订）

1. **FFmpeg/FFmpeg**，65,267 stars，2026-10-16 活跃：
   - [ffprobe 官方文档](https://github.com/FFmpeg/FFmpeg/blob/3e6cd5e7603cb81b028b9c17530697b8986bf69a/doc/ffprobe.texi#L141-L172)：`-show_format`、`-show_streams`、`-show_entries` 按节输出；不能把容器 duration 和任意流字段混为同一单位。
   - [ffprobe.c show_stream](https://github.com/FFmpeg/FFmpeg/blob/3e6cd5e7603cb81b028b9c17530697b8986bf69a/fftools/ffprobe.c#L1995-L2050)：`codec_name`、`width`、`height` 来自解码参数，不从扩展名猜编码。
   - [LICENSE.md](https://github.com/FFmpeg/FFmpeg/blob/3e6cd5e7603cb81b028b9c17530697b8986bf69a/LICENSE.md)：大部分 LGPL-2.1-or-later，启用 GPL 组件会改变整体许可证；不是 MIT；不能仅以 MIT 分发未经合规评估的派生代码，这不等于完全不能复制或与 MIT 项目结合。当前仅机制借鉴，不复制、不引入二进制或依赖；未来复用须先评估具体组件、构建配置与对应许可义务。
2. **rclone/rclone**，MIT：[PikPak FileParams/Media](https://github.com/rclone/rclone/blob/d369079a1448c487d09d85bfe11382e16ea4e345/backend/pikpak/api/types.go#L188-L280)、[许可证](https://github.com/rclone/rclone/blob/d369079a1448c487d09d85bfe11382e16ea4e345/COPYING)。`FileParams.duration` 明确注释“秒”，width/height 为字符串整数；`medias` 可能包含原始和转码版本，`is_origin` 表示原始流。上游的 schema 只作字段依据，不是本 CLI 实测。

## 采用与拒绝

- 保留 `params.duration` 的秒契约，严格解析完整非负整数，不从 `12garbage` 或 `-3840` 抽数字；缺失/损坏时长标“未知”，不推断服务端正在转码。
- 编码仅从 `is_origin=true` 的 media 读取；只有转码 h264 时不冒充原文件 h264。尺寸必须同时存在才判断 4K；文件名带 2160p/hevc 不构成证据。
- 识别以 MIME video、VIDEO category、媒体元数据或正时长优先，扩展名兜底；补无扩展名视频。显式 audio MIME/AUDIO category 排除；缺类型但有 duration 的音频仍可能误入，因此这是候选清单而非逐文件探测认证。
- 来源已真正落到 Markdown/CSV；HTTP URL 移除 userinfo/query/fragment，magnet 仅保留 xt，不导出 tracker/显示名。脱敏不是匿名化：路径和 infohash 本身仍可能敏感。
- CSV 每个字符串单元格中和公式前缀，标准 CSV 引号不足以防 Excel 公式；Markdown 将全部不可信单元格编码为纯文本，ASCII 标点转字符实体、换行转空格；两种现有 Markdown 解析器实际渲染确认无图片/链接/代码/强调节点。导出字段只接受标量白名单，嵌套 video_codec/metadata 统一留空，禁止用 `str()` 泄漏 passcode/link。先脱敏 params.url，无效才退回 original_url。
- 不自动对云端直链运行 ffprobe：会产生网络请求、暴露签名链接，且未获准安装/真实访问。未来可增加显式本地 `ffprobe -v error -show_entries format=duration:stream=codec_type,codec_name,width,height,duration -of json FILE` 导入，但**本次未实现**。

## 验收与剩余

新测试覆盖损坏值/不猜编码、不把转码当原码、CSV 公式、无扩展名视频、来源列、URL 脱敏、嵌套 codec 不泄漏（Markdown/CSV 真实渲染）和分页环路；fixture 显式空/坏输入不回退 live；只验证本地逻辑。超大整数在浮点转换溢出时以安全原始字节数展示。未实现本地 ffprobe 导入、来源搜索/pending 筛选、精确多流关联或真实 CLI 字段认证；MD/CSV 是候选元数据快照，不是媒体有效性证明。
## 证据与法律边界

本次仅通过未认证的公开 GitHub HTTPS 读取源码和许可证；未安装、执行上游代码，未访问 PikPak 账号。GitHub 源码可证明其自身实现，不能证明本项目所调用的官方 `pikpak` CLI 与这些第三方项目的 JSON/下载行为兼容。fixture 是离线回归，不是线上兼容认证。只借鉴机制，未复制上游实现；将来复制代码须保留对应版权与许可证。
