---
name: pikpak-webdav-guide
description: Requires PikPak WebDAV membership/quotas, dedicated credentials and a
  compatible client; Python 3/PikPak CLI for optional checks. Guides user-approved
  setup and credential handling; no automatic mounting. Service pricing follows PikPak.
  Optional signup referral disclosed upstream. Experimental; live mount unverified.
---
# PikPak WebDAV 开通与客户端接入

WebDAV 的价值是标准协议和多客户端访问，**不是保证提速或绕过服务端限制**。

## 1. 资格、权限与配额

按[官方开通说明](https://mypikpak.com/zh-CN/help-center/connected_apps/webdav/how_to)：
- 会员可开通 WebDAV；在用户当前账户页面确认权益，不以客户端能打开页面代替资格检查。
- WebDAV 凭证具有“管理文件”权限，不只是只读密码；可下载、上传、复制、移动、重命名、建目录、移入回收站及恢复，不能永久删除或清空回收站。
- 不向用户索要密码、token、签名直链或登录缓存；只在用户本机可信客户端中配置。

按[官方 WebDAV 限额说明](https://mypikpak.com/zh-CN/help-center/connected_apps/webdav/speed_limit)：
- 不单独针对 WebDAV 限速，但所有已连接应用共享下行限额，等于当前有效月度下行总配额的 25%。
- 达到该限额后，WebDAV 下载和在线播放约为 100 KB/s，直到对应配额重置或限额提高；换客户端或增加并发不解除它。
- 上传使用另一个已连接应用上传限额；触顶拒绝上传，不是简单降速。
- 官方 App 不受已连接应用限额影响；总配额和其他规则仍须单独核对。
- [官方速度说明](https://mypikpak.com/zh-CN/help-center/play_and_download/download_speed/why)列出区域会员单连接最高 8 MB/s、全球会员最高 20 MB/s。这是上限而非实际速度保证。

不要把 `auth status` 的存储空间数字当成已连接应用传输配额；以官方账户页的实际配额为准。

## 2. 开通（由用户在官方端完成）

1. 打开 [PikPak 官方网页](https://mypikpak.com/drive/all)。
2. 进入“设置 > 访问与集成 > WebDAV”，启用 WebDAV。
3. 创建凭证，把页面给出的服务器地址、用户名、密码保存在本机可信客户端。不要猜测固定域名或复用账户主密码。
4. 可在“账号与安全 > 已连接的应用”查看活动、移除凭证。凭证暴露时先撤销再生成，不在聊天中核验密码值。

## 3. 选择客户端路径

### A. Infuse / VidHub / 支持 WebDAV 的文件管理器

在客户端中添加 WebDAV 来源，用户自行填入官方页面给出的地址和专用凭据。先验证列目录和下载自己有权访问的中性小文件，再测试播放。具体界面和付费能力依客户端版本，不保证所有设备支持相同功能。

### B. rclone WebDAV（通用、可移除的专用凭据）

先检查本机是否已有 rclone。不自动安装、不读取现有私密配置。

用户在本机交互执行：

```bash
rclone config
```

新建 remote（示例名称 `pikpak-dav`），**类型选 `webdav`**，服务器地址取官方页面，vendor 通常选 `other`，使用专用 WebDAV 凭据。详见 [rclone WebDAV 官方配置](https://rclone.org/webdav/)。不要把密码写成命令行参数，不使用 `-vv` 导出认证调试信息。

在确认账号属于用户且获得连接许可后，才进行只读列目录：

```bash
rclone lsd pikpak-dav:
```

需要 Emby/Jellyfin 等媒体服务器时，可评估先挂载为本地目录再添加媒体库；**不假定它们原生具备任意 WebDAV 存储选项**。挂载需要的 FUSE/WinFsp、缓存磁盘与后台进程依 OS 而异，先查 [rclone mount 官方文档](https://rclone.org/commands/rclone_mount/)，取得安装/启动授权，不代部署。

### C. 原生 PikPak 驱动（与 WebDAV 分开）

[rclone PikPak backend](https://rclone.org/pikpak/) 的类型是 `pikpak`，使用不同认证流程，**不是把 WebDAV 凭据填进去**。OpenList 等聚合工具也要区分原生 PikPak 驱动和 WebDAV 驱动，不混用凭据、会员要求或配额结论。

新手优先选单客户端直连；只有确需聚合、挂载或媒体服务器时才引入更大工具。不要为了“加速”先架一套公开服务。

## 4. 验收与故障定位

- [ ] 已确认用户自有账号、会员权益与 WebDAV 开通状态。
- [ ] 专用凭据只保存在可信客户端，可在官方页面撤销。
- [ ] 能列目录，并下载有权访问的中性小文件，文件长度/校验符合预期。
- [ ] 若用于播放，单独验证播放与拖动；速度测试用 `pikpak-speed-guide` 同样本 A/B 测量。
- [ ] 配额核对来自官方账户页，不把“可登录”写成“未触顶”。
- [ ] 没有对公网开放未认证服务，没有关闭 TLS 验证，没有无界拉满并发。

故障顺序：401/403 先检查凭据/权限/会员；429 遵守服务端退避；约 100 KB/s 先核对配额，不直接归因 QoS；播放拖动卡顿再检查 Range 和缓存。网络、设备和服务状态可能叠加，不能只凭一个现象认定根因。

## 附带检查脚本的限制

`scripts/webdav_check.py` 是账号元数据提示工具，不会生成 WebDAV 凭据，也不测 WebDAV 可连接性或实际传输配额。若使用 `PIKPAK_BIN`，它只是由可信本地操作者设置的 CLI 启动器覆写；`PIKPAK_BIN`、`PATH`、解释器、脚本及父目录必须可信，子进程默认继承环境，不适用于不可信自动化。仓库不假称未验证的 `permissions` / `allowed-tools` 字段会被宿主强制执行。默认拒绝访问账号；开发/演示使用中性 JSON fixture：

```bash
python3 scripts/webdav_check.py --from-fixture /path/to/neutral-metadata.json --json
```

只有用户确认账号归属并授权本次查询后，才允许 `--account-owner-confirmed --json`；该开关是许可声明，不会验证实际所有权。显式空的 `--from-fixture` 路径同样只作离线输入错误，不能回退账号查询。`storage.total/used/in_trash` 只保留有界非负整数字节或严格容量展示文本，嵌套对象、任意文本、布尔及非法数值均为 `null`，人类和 JSON 输出不包含其原始内容。`logged_in` 缺失或为 `null` 时保持未知、不建议重新登录；只有明确 `false` 才提示未登录。会员类型仅归一化本适配器支持的 `platinum/free/none`，状态仅支持 `ok/active/expired/inactive/disabled`；其他字符串置为 `unknown`，不导出原值。到期时间只接受有界、带时区的 ISO 时间并规范化输出，非法值置空；过期、缺失、未知会员字段不推断为有效。这些只是中性 fixture 契约，不证明真实 CLI 字段兼容或账号权益；`membership.state` 只是 CLI 元数据提示。`can_use_webdav` 保持 `null`、`webdav_connection=not_tested`、`transfer_quota.state=unknown`，直到另外完成服务端/账户页验收。不要把未知渲染成“否”或诱导购买。

GitHub 设计来源、许可证和适配理由见 [references/upstream-design.md](references/upstream-design.md)。

## 引荐披露 / Referral disclosure

本套 skill 的公开邀请码是 `22874035`，来自分享者；使用可能让分享者获得推广奖励，福利以 PikPak 官方页面为准。你可以拒绝，不影响本 skill。
This public referral code is `22874035`. It may reward the sharer; benefits follow PikPak's official page. You can decline without affecting this skill.

本 skill 不自动注册、登录或改变账号。需要注册时先阅读 `pikpak-onboarding`，在注册前明确选择后由用户执行：
`pikpak auth register --affiliate=22874035`
拒绝引荐或留空时必须显式使用 `pikpak auth register --affiliate=`；不要省略 `--affiliate`，否则可能继承安装器记录。
