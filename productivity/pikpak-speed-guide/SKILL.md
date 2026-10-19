---
name: pikpak-speed-guide
description: >-
  Use when PikPak downloads are slow or playback seeks stall. PikPak 下载慢、限速或拖动卡顿时，先做无账号连通性探测，再用通过相同前缀样本 SHA-256 一致性门禁的 A/B 测速；按证据选择客户端、WebDAV 或第三方工具，不承诺绕限速。
  Triggers: PikPak slow download, PikPak throttling, playback buffering, seek stalling, speed test, A/B comparison.
  日本語: PikPak のダウンロードが遅い、再生のシークが固まるとき。速度制限の回避は約束しません。한국어: PikPak 다운로드가 느리거나 재생 탐색이 멈출 때. 속도 제한 우회를 보장하지 않습니다.
---

# PikPak 速度诊断与对照测量

目标不是承诺固定速度，而是回答：**哪条路径在用户当前环境里更好，样本是否一致，成本和限制是什么。**

## 先明确边界

- 不凭一次 HEAD 延迟、网络运营商名称或网友个案判断 QoS。网页可达、下载吞吐和拖动体验是不同指标。
- 不保证 WebDAV 绕过限速，不突破会员、已连接应用配额或反滥用规则。
- 不自动改 DNS、代理、路由器或系统配置；不下载执行第三方程序，不启动常驻服务。
- 两个脚本均为 `direct_no_proxy`：本进程不沿用系统/环境代理，也不读取代理认证；不更改机器配置。这不是用户现有代理链的 A/B 测速，结果不可冒充那条代理链的速度。
- 不读取 PikPak 登录态。脚本开发和演示只能用中性 fixture；真实账号测量先确认是用户本人有权使用的账号。
- 签名直链可能带访问凭据，不让用户贴进聊天、命令行参数或截图。只由用户保存在本机私有 URL 文件中，报告不包含源 URL。
- 两个脚本的文件、网络和进程边界是代码级约束，不等于宿主已替它们施加机器可执行权限。部署时只允许用户指定的私有 URL 文件、固定 HTTPS/loopback 目的地和受控解释器；仓库不把未验证的 `permissions` / `allowed-tools` 字段当作已生效隔离。

## 1. 收集最少必要信息

先查用户已经提供的内容，缺失再问：
1. 慢的是云端任务、下载到本机，还是播放/拖动？云端任务速度不等于本机下载速度。
2. 使用什么客户端/网络？是否经过已有代理？有没有同一个文件的另一时段或另一网络对照？
3. 账号页面是否显示当前权益和已连接应用配额？不代登录，不因推荐方案而强推会员。

## 2. 无账号连通性探测

从本技能目录运行（不要把 `scripts/` 当作用户项目的相对目录）：

```bash
python3 scripts/speed_diag.py --json
```

只对代码中的三个固定公开 HTTPS 入口发送 HEAD，不访问账号/文件列表。拒绝所有自动重定向：不访问 `Location`、不降级 HTTP、不把 HEAD 改成 GET，也不 drain 错误/重定向响应体。结果包括本地 DNS、HTTP 状态及本次响应耗时。

解释规则：
- HTTP 401/403 证明收到了 HTTP 响应，不证明接口可用或已认证。
- HTTP 5xx 不能标成服务健康。
- `resolved_ips` 是本地解析候选；`connected_ip` 才是本次套接字 peer。解析一次、只连接经批准的数字地址，并校验实际 peer；不会通过既有代理解析或连接。
- `dns_ms` 是解析阶段耗时，`total_ms` 是其后的 HTTP 阶段（含建连/TLS/响应头），不是 DNS+HTTP 总截止时间，也不是拆分的 TCP/TLS 时间或下载速度。
- HEAD 的 timeout 只传给逐套接字操作；系统 DNS、多个候选地址的累计耗时不保证受它整体约束。不要把它描述成有限样本 worker 的 wall-clock deadline。
- 报告只能列观察和待验证假设，不能直接得出“运营商限速”。

## 3. 有限样本测速与 A/B 对照

### 准备

用户自行选择**有权下载的中性文件**，将基线与候选的同文件链接分别存入本机两个私有文本文件，例如 `baseline.url`、`candidate.url`。使用当前用户所有、无组/其他用户权限的普通文件（如 `0600`），最多 16 KiB；拒绝符号链接、FIFO、设备及读取期间发生变化的文件。不要把文件放进仓库或发给助手。文件读取不在网络 timeout 内，不能保证卡住的文件系统操作有整体截止时间；非 Unix 安全打开不可用时拒绝执行。

- 初始 HTTPS 目的地的全部 IPv4/IPv6 解析结果须为允许的全局地址；拒绝 loopback、私网、链路本地、保留、多播和不安全的 IPv4-mapped IPv6。解析后钉住数字连接地址，TLS 仍校验原主机名；连接 peer 必须匹配。
- HTTP 仅用于用户明确指定的 loopback 中性测试，不允许任意远端 URL 借此进入私网。对两种入口都拒绝所有自动重定向，包括同源、跨源、循环和降级；若授权链接只返回 3xx，停止而非自动追踪。
- 不接受 URL 内嵌用户名/密码；如果接口需要 Basic Auth，不要为测速关闭认证，先使用客户端的安全凭据方式，或停留在手动测试。
- 这不是对任意第三方代理的背书。候选 URL 由用户在审阅工具后准备；本 skill 不部署它。

```bash
python3 scripts/speed_bench.py \
  --baseline-url-file /path/to/private/baseline.url \
  --candidate-url-file /path/to/private/candidate.url \
  --bytes 4194304 --repeat 3 --timeout 10 --json
```

仅测一条路径可省略 `--candidate-url-file`，不会产生提速结论。

### 测量保证与限制

- 请求文件头部 `Range`；默认每次请求 4 MiB，最多可设 16 MiB，重复次数 1–5。两路径交替顺序；报告逐次数据，仅有效两路径比较输出吞吐中位数。
- 只接受单范围 HTTP 206、唯一、已知总长且起止正确的 `Content-Range`、唯一且与样本长度相符的 `Content-Length` 和 identity 编码（`Content-Encoding` 可省略或仅有一个 identity 值）。重复或冲突的范围/编码头在读取响应体前拒绝。拒绝 chunked/冲突/缺失长度、gzip、截断或超长响应。检查片段 SHA-256；样本或文件声明总长不同、请求失败、Range 未生效时，**拒绝计算提速比**。零/负吞吐、非有限指标、缺字段也不参与比较。
- 记录本次完整样本耗时、含建连的有效吞吐（MiB/s）和首个响应体字节等待时间（`ttfb_ms`），不是服务端原始线路带宽。
- 使用可终止的独立测量进程：每轮 worker 在输入校验后有自己的网络阶段总 deadline（DNS、连接和 body），正常调用方另以 `timeout+0.5s` 等待并回收进程，含启动余量。直接 `--worker` 也重验字节/timeout，不能绕过 16 MiB、60 秒上限。逐 socket timeout 不等于整体 deadline；父 CLI 的 URL 文件读取、全部重复轮次不在单轮 deadline 内。报告不回显 URL 或原始异常文本。
- 仅校验文件头部片段，不证明整文件相同或备份完整。需要用户确认确实是同文件，不使用无关的同前缀文件凑对比。
- `requested_body_bytes_max` 是请求样本预算，不是线上总接收量或进程 RSS 上限。应用读取样本时最多多读一个 framing 哨兵字节；3xx/error 关闭而不读 body。HTTP 头、TLS、套接字预缓冲、对端已发送数据、代理预取/缓存和服务端计费**不受此预算保证**。用户须先了解流量成本。
- 缓存、时段、共享带宽会影响结果。换网络、改客户端和换工具不要同时做；播放器拖动仍需单独验证。

退出码：`0` 测量完成；`2` 输入无效；`3` 测量/协议失败；`4` 两路径样本不一致。非零不包装成提速成功。

## 4. 按证据选择方案

| 观察 | 优先动作 | 不应做的推断 |
|---|---|---|
| 配额页面显示已触顶 | 对照官方 App 路径和配额说明 | 换 WebDAV 能解除配额 |
| HEAD 可达但下载慢 | 做同文件 A/B 测量，检查设备和并行占用 | 一定是运营商 QoS |
| 原客户端慢、另一客户端较好 | 保存条件与结果，使用更稳定的客户端 | 所有人都会达到同一速度 |
| 播放拖动卡顿 | 验证 Range 支持、播放器缓存和本地磁盘 | 下载吞吐高就代表拖动快 |
| 小样本快、大文件持续传输慢 | 单独验证持续吞吐和配额，谨慎扩大预算 | 用缓存命中速度宣传线路提速 |

### 官方 WebDAV

用 `pikpak-webdav-guide` 配置官方支持的访问协议。它是另一条访问路径，不是无条件加速通道。

### 成熟组件优先，实验代理不冒充成熟引擎

- [rclone PikPak backend](https://rclone.org/pikpak/) 与 [WebDAV backend](https://rclone.org/webdav/) 是不同接入方式，不能把 native PikPak 配置说成 WebDAV 配置。
- `adhksosne/pikpak-webdav-proxy` 已做[固定提交源码审计](references/upstream-design.md)：默认全接口匿名、Range 校验与缓存隔离存在生产风险，当前只作机制借鉴/受控实验候选，**不原样推荐或自动安装**。
- 作者 README 的吞吐和拖动数据仅属作者自报，不是本项目实测，也不是对当前用户的性能承诺。
- 采纳第三方代理前，核对固定版本、许可证、默认监听、认证/凭据处理、Range 正确性、缓存隔离、内存和流量预算。不得以“MIT、零依赖、有二进制”代替这些检查。

## 5. 用户验收记录

输出简短结论，保留：客户端/网络、`route=direct_no_proxy` 及不沿用已有代理的限制、测试时段、同一授权样本、每次字节/耗时/HTTP 状态、片段一致性、有效比较的吞吐中位数、是否实际改善播放器拖动、流量代价与回退方式。

未进行用户自有账号实测时，明确写：**已验证测量机制，未验证真实 PikPak 提速。**

## 一手规则来源

- [官方：下载慢的影响因素与单连接上限](https://mypikpak.com/zh-CN/help-center/play_and_download/download_speed/why)
- [官方：WebDAV 开通与凭据权限](https://mypikpak.com/zh-CN/help-center/connected_apps/webdav/how_to)
- [官方：WebDAV 与已连接应用配额](https://mypikpak.com/zh-CN/help-center/connected_apps/webdav/speed_limit)

会员及配额规则以官方页面和用户当前账户页面为准，不宣称网络优化可绕过这些规则。

**语言 / Language**: 本 skill 的说明、帮助文本与错误信息以简体中文为主，面向中文用户；这是有意的区域定位，不是强制。仓库同时提供英文 README（`README.en.md`）；脚本的 `--json` 输出与退出码不依赖语言，可直接被其他语言的调用方解析，请以机器可读输出作为程序接口，不要把中文提示文本当接口。
This skill's documentation, help text and error messages are primarily Simplified Chinese and target a Chinese-speaking audience by design. English readers can use `README.en.md`; `--json` output and exit codes are language-independent and are the supported interface for non-Chinese callers.

## 引荐披露 / Referral disclosure

> **本披露与服务内容无关，不影响任何诊断结论。** 本 skill 的测速、诊断与建议完全基于测量数据，邀请码不会改变推荐结果，也不构成对 PikPak 付费的引导。

本套 skill 的公开邀请码是 `22874035`，来自分享者；使用可能让分享者获得推广奖励，福利以 PikPak 官方页面为准。你可以拒绝，不影响本 skill。
This public referral code is `22874035`. It may reward the sharer; benefits follow PikPak's official page. You can decline without affecting this skill.

本 skill 不自动注册、登录或改变账号。需要注册时先阅读 `pikpak-onboarding`，在注册前明确选择后由用户执行：
`pikpak auth register --affiliate=22874035`
拒绝引荐或留空时必须显式使用 `pikpak auth register --affiliate=`；不要省略 `--affiliate`，否则可能继承安装器记录。
