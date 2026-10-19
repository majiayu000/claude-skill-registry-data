# GitHub 方案核验与速度产品设计

## 决策

优先官方链路与已安装的成熟客户端；先证明 Range 字节正确、测量有界且同样本，再谈速度。本项目实现小流量 A/B 测量，不从零制造生产下载/媒体代理，不承诺绕过服务端配额。

## 候选与真实适配

| 候选 | 一手证据与许可证 | 适配/决定 |
|---|---|---|
| rclone/rclone | [固定提交 d369079 / WebDAV backend](https://github.com/rclone/rclone/blob/d369079a1448c487d09d85bfe11382e16ea4e345/backend/webdav/webdav.go)、[原生 PikPak backend](https://github.com/rclone/rclone/blob/d369079a1448c487d09d85bfe11382e16ea4e345/backend/pikpak/pikpak.go)、[MIT](https://github.com/rclone/rclone/blob/d369079a1448c487d09d85bfe11382e16ea4e345/COPYING) | 可选外部客户端；保留两类认证和协议差异。不是捆绑依赖，未在本机接账号验证，不因多连接就推断提速。 |
| adhksosne/pikpak-webdav-proxy | [固定提交 779319f / MIT](https://github.com/adhksosne/pikpak-webdav-proxy/blob/779319f7592bb2109270820760384a7cf58fb89f/LICENSE)；下列源码证据 | 仅机制借鉴/受控实验候选，**不原样安装或推荐为生产引擎**。源码审计不等于运行复现；作者测速不是本产品测量。 |
| 官方 CLI / 官方 WebDAV | [CLI](https://mypikpak.com/cli)、[WebDAV 限额](https://mypikpak.com/zh-CN/help-center/connected_apps/webdav/speed_limit) | 对照基线与政策来源，不以第三方方案宣称解除会员、配额或反滥用限制。 |

## 发行证据与快照边界

- rclone 的公开发行记录为 [v1.75.2](https://github.com/rclone/rclone/releases/tag/v1.75.2)，已读取的 GitHub REST 元数据给出 `published_at=2026-10-09T11:03:19Z`、`draft=false`、`prerelease=false`（核验时点 2026-10-16）。此处固定记录，不承诺未来仍是 latest。
- 本文研究的是 `d369079a1448c487d09d85bfe11382e16ea4e345` 源码快照；`snapshot_ancestry=not_verified`，未核验快照与发行 tag 的祖先关系，不能将该快照等同 v1.75.2 的源码或制品。
- 实验代理的正式发行未核验：`proxy_release=not_verified`。审阅的是 `779319f7592bb2109270820760384a7cf58fb89f`；未核验任何 tag、制品或对应祖先关系，不把作者 README 的版本字样当发行证据。
- 发行元数据和固定源码审阅均不代表运行、兼容、安全或性能验收；未下载/执行发行制品，不以版本号升级实验候选的成熟度。

## 为什么不直接采用小型加速代理

审阅的上游固定为 `779319f7592bb2109270820760384a7cf58fb89f`：

1. [main.go:35–53](https://github.com/adhksosne/pikpak-webdav-proxy/blob/779319f7592bb2109270820760384a7cf58fb89f/main.go#L35-L53)：默认 `:7777` 全接口、代理认证为空；上游密码和可选代理密码只从 argv 进入。把环境变量展开到密码参数仍是 argv，不能当安全凭据接口。
2. [stream.go:698–753](https://github.com/adhksosne/pikpak-webdav-proxy/blob/779319f7592bb2109270820760384a7cf58fb89f/internal/server/stream.go#L698-L753)：分片读取同时接受 200 与 206，不核验 Content-Range。如果上游忽略 Range，非零偏移可读取文件头并错位拼接。这是条件性静态缺陷，不宣称真实 PikPak 已触发。
3. [diskcache.go:38–94](https://github.com/adhksosne/pikpak-webdav-proxy/blob/779319f7592bb2109270820760384a7cf58fb89f/internal/server/diskcache.go#L38-L94)、[stream.go:129–140](https://github.com/adhksosne/pikpak-webdav-proxy/blob/779319f7592bb2109270820760384a7cf58fb89f/internal/server/stream.go#L129-L140)：持久缓存名源自 basename，没有账号/target/完整对象版本隔离；目录/文件权限为 0755/0644。不能宣传跨账号缓存安全。
4. 源码存在连接复用、滑动窗口和缓存等可借鉴机制，但全局资源上限、取消传播、HEAD 与签名失效等仍须单独修复、动态验证。MIT、二进制和 stars 不是验收替代品。

没有下载、运行或构建该代理；没有接入真实账号、扫描 CDN 节点、改 DNS 或代理配置。没有复制上游代码到本项目。

## 本轮已实现

- `speed_diag.py` 将 DNS/HTTP 观察与吞吐、QoS 归因分开；401/403 只是有响应，5xx 不是健康。
- 新增 `speed_bench.py`：私有普通 URL 文件输入、每次有限文件头部样本、worker 自截止与调用方回收、首个 body 字节等待时间；有效两路径比较输出吞吐中位数，单路径保留逐次数据。
- 成功比较要求 206、精确且总长已知的 Content-Range、唯一且正确的 Content-Length、identity 编码、长度与片段 SHA-256 一致；拒绝 chunked、截断/超长、缺字段或非有限指标，失败或不同样本不给速度比。
- 两脚本均为 `direct_no_proxy`，不沿用系统/环境代理，不读取代理认证，不改机器配置；不将本次结果当成既有代理链 A/B。解析一次、钉住数字连接地址并核验 peer；HTTPS 只接受经验证的全局地址，显式 loopback HTTP 只用于中性测试。
- 拒绝所有自动重定向，关闭而不 drain 3xx/error body；固定目标 HEAD 不会改成 GET 或降级。源 URL 与原始异常不进入结果。
- 不读取账号元数据，不启动服务，不自动安装候选工具。

## 验证与未验收

- 从仓库根使用 `PYTHONDONTWRITEBYTECODE=1 python3 -B dev/run_tests.py`，并将同次 `TMPDIR` 设为自选的中性 scratch 目录。根 runner 发现全部 `dev/test_*.py`；中性 loopback HTTP 验证真实读取，域名/peer/认证风险仅用内存替身和合成审计，不做实际公网 DNS/HTTP。
- 持久负例覆盖 301/302/303/307/308 大 body、零 read/零后继请求、hostname-to-private、重绑定后的 pinned 连接、peer 不符、短/长/压缩/未知总长、冲突 framing、非法 worker 参数与持续滴流 deadline、私有 URL 文件类型/权限、不可比指标。保留忽略 Range、403、错误范围、首字节慢、不同片段与敏感 URL 不回显断言。最终完整通过数以根 runner 实际结果为准，不由这份静态名单保证。
- runner 的拒绝默认子进程门禁只批准精确解释器/脚本/argv/环境；子解释器经 `-I -B -S` 禁用用户路径与 site/.pth 启动钩子，显式 bootstrap 安装同一审计后才运行入口，私有假 CLI 也不通过真实 shell。UDP、非数字 loopback DNS、shell/env/exec/spawn、任意解释器和环境覆盖被拒绝。这是可信仓库测试的误用兜底，不是 OS sandbox：不防恶意改写 guard、native/ctypes、既存句柄或 loopback 服务转发，不提供文件系统隔离。
- 本机 Python 3.9 的 unittest 只在存在 tearDownModule 时清理 addModuleCleanup；runner 为缺失 teardown 的已发现模块补无操作边界，让原 ExitStack 正常关闭。不要用全局 stopall 或重置 guard 代替模块清理，也不要只缩窄 discovery 来隐藏失败。
- 只验证前缀样本，不证明整文件相同、不证明持续大文件吞吐、不证明播放器拖动或真实用户线路提速。
- HEAD 的解析时间与逐 socket timeout 不是整体 deadline；仅样本 worker 有可回收总 deadline，URL 文件系统 I/O 和多轮累计不在单轮时间内。`resolved_ips` 与实际 `connected_ip` 分开。
- 请求样本预算不等于进程 RSS 或线上总接收量；样本读取多至一个 framing 哨兵，HTTP 头、TLS、缓冲及对端/第三方预取和后台缓存另计。扩大测量前先确认成本。
- 真实 PikPak A/B、冷/热缓存分离、播放器拖动和任何新客户端部署均须对自有账号单独授权验收。
