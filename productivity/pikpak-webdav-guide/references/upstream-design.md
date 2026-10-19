# GitHub 方案核验与采用边界

## 1. 标准 WebDAV 客户端：rclone/rclone

- 固定源码：[d369079a1448c487d09d85bfe11382e16ea4e345 / backend/webdav/webdav.go](https://github.com/rclone/rclone/blob/d369079a1448c487d09d85bfe11382e16ea4e345/backend/webdav/webdav.go)。注册名为 `webdav`，参数包含 URL、vendor、专用用户名/密码；密码字段使用 `IsPassword`。它与原生 `pikpak` backend 不同。
- 配置依据：[同提交 WebDAV 文档](https://github.com/rclone/rclone/blob/d369079a1448c487d09d85bfe11382e16ea4e345/docs/content/webdav.md) 明确交互配置、目录列举，以及普通 WebDAV 不保证提供内容哈希。不能把同长度视为哈希校验成功。
- 许可证：[MIT / COPYING](https://github.com/rclone/rclone/blob/d369079a1448c487d09d85bfe11382e16ea4e345/COPYING)。本技能仅引用流程与接口，没有复制或分发 Go 源码；将来复制代码必须保留声明。
- 适配分类：**可选外部客户端**，不是本项目捆绑引擎。已有 rclone 且用户授权连接时，按官方交互流程创建专用 WebDAV remote；不默默读取现有配置、不自动安装或挂载。
- 采纳：标准协议、凭据种类分离、交互输入密码、保守只读验收。不要为兼容问题默认开启跨主机认证重定向、跳过 TLS 验证或公开 HTTP 服务。
- 不采纳：自研一层中转服务、不必要的 NAS/聚合器部署、把原生 PikPak 登录误称 WebDAV 登录。

## 发行证据与快照边界

- rclone 公开发行记录为 [v1.75.2](https://github.com/rclone/rclone/releases/tag/v1.75.2)，已读取 GitHub REST 元数据：`published_at=2026-10-09T11:03:19Z`、`draft=false`、`prerelease=false`（2026-10-16 核验，不承诺未来 latest）。
- 研读快照为 `d369079a1448c487d09d85bfe11382e16ea4e345`；`snapshot_ancestry=not_verified`，快照与发行 tag 的祖先关系未验证，不能把它冒充该 release 的源码或稳定制品。
- 仅作拒绝对照的实验代理：`proxy_release=not_verified`，正式发行、制品和 tag 祖先关系均未核验；固定审阅快照不等于已发布版本。
- 这些证据不代表运行、WebDAV 连接、官方账号 JSON 兼容或吞吐验收；没有下载/运行上游制品。

## 2. 官方 CLI 与官方服务：能力不同就分开验收

`pikpak auth status --help` 只承诺登录/Profile、VIP、storage 提示，不证明 WebDAV 已开通、凭据可连接或已连接应用传输额度。JSON fixture 是本项目的测试假设，不是假装官方 schema。

本轮对 `webdav_check.py` 的实际改进：

1. 默认不查询账号。中性 `--from-fixture` 全离线；自有账号查询须显式 `--account-owner-confirmed`，该标志不能替代真实归属核验。
2. 校验对象与字段类型，拒绝错误 schema；不把字符串 `false` 当作已登录。`storage.total/used/in_trash` 仅输出有界非负整数字节或严格容量展示文本，容器、任意字符串、布尔及非法数值置 `null`，禁止原样透传嵌套元数据；人类和 JSON 报告使用同一过滤。
3. 对已过期、未知和缺失会员字段保留区分。即使元数据显示会员仍有效，也不把它升级为 WebDAV 可连接。
4. `can_use_webdav=null`、连接 `not_tested`、传输配额 `unknown`；存储数字不冒充传输用量。
5. CLI 失败不回显原始 stdout/stderr，避免私密 URL/字段流入报告；人类报告将未知显示为未验证，而不是否。

## 3. 不引入实验代理

`adhksosne/pikpak-webdav-proxy` 在 [779319f7592bb2109270820760384a7cf58fb89f](https://github.com/adhksosne/pikpak-webdav-proxy/tree/779319f7592bb2109270820760384a7cf58fb89f) 的默认监听/匿名认证、Range 校验、持久缓存命名和凭据 argv 入口不足以作为默认生产方案。只做固定源码审计，没有运行它，也没有验证作者测速。详细采纳边界见速度技能的对应参考。

## 4. 验证边界

- 本地回归：`python3 -m unittest dev.test_maturity_access -v`；主 runner 保留会员正反例与只读 AST 检查，并固定测试时钟。
- 覆盖过期/未知会员、错误 JSON 形状、默认不访问账号、fixture 不调用子进程、未知显示、原始错误输出不泄漏。
- 没有连接真实 PikPak 账号、WebDAV 端点、rclone 或播放器。真实 PROPFIND、Range、权限和配额须在明确授权的自有账号单独验收。
- 服务政策以 [官方开通](https://mypikpak.com/zh-CN/help-center/connected_apps/webdav/how_to) 和 [官方限额](https://mypikpak.com/zh-CN/help-center/connected_apps/webdav/speed_limit) 为准，不用开源项目 README 推断。
