---
name: nsis-installer-autoupdate
description: Windows 安装器（electron-builder NSIS）与自动更新（electron-updater）的领域知识与套路。当任务涉及 installer.nsh / NSIS 钩子宏、安装卸载流程、quitAndInstall / --updated / 静默或非静默安装、更新安装慢、Defender 排除、PATH 写入与 WM_SETTINGCHANGE 广播、右键菜单注册表、或安装耗时测量时使用。
disable-model-invocation: true
---

# NSIS 安装器 & 自动更新

## 关键文件

| 文件 | 职责 |
|---|---|
| `apps/editor/build/installer.nsh` | 我们的 NSIS 钩子宏：customInstall / customUnInstall / customInstallMode / customFinishPage（PATH、右键菜单、Defender 询问、更新零点击） |
| `apps/editor/electron-builder.yml` | `nsis:` 配置（oneClick:false + allowToChangeInstallationDirectory:false + allowElevation:false + include——锁死 per-user 安装）、electronLanguages 裁剪、afterPack、extraFiles 带 defender 脚本 |
| `apps/editor/build/afterPack.cjs` | 删框架释放的大文件（LICENSES.chromium.html 等，`files:'!'` 管不到） |
| `apps/editor/resources/defender/add\|remove-defender-exclusion.ps1` | Defender 排除脚本，installer.nsh 经 `ExecShellWait "runas"` 提权调用 |
| `apps/editor/src/main/services/update/updateMainService.ts` | `quitAndInstall`（running-session veto → `autoUpdater.quitAndInstall(false, true)`） |
| `apps/editor/src/main/services/update/updateShutdownTrace.ts` | 跨进程停机 trace（墙钟 epoch + 同步落盘），量"点击更新→新版启动"黑洞的唯一手段 |
| `node_modules/.pnpm/app-builder-lib@*/node_modules/app-builder-lib/templates/nsis/` | electron-builder NSIS 模板源码（改行为前先读这里，别猜） |

## electron-builder NSIS 模板机制速查

- **钩子宏**：在 `nsis.include` 指向的 installer.nsh 里 `!macro customXxx` 定义，模板用 `!ifmacrodef` 探测后插入。可用钩子：`preInit` / `customHeader` / `customWelcomePage` / `customInstallMode` / `customPageAfterChangeDir` / `customFinishPage` / `customInstall` / `customUnInstall` / `customRemoveFiles`。宏名大小写不敏感（模板里 `customInstallmode` 与 `customInstallMode` 混用是正常的）。
- **生成谓词**：构建期 `nsisScriptGenerator.flags([...])` 为 `--updated` / `--force-run` / `/allusers` / `/currentuser` 等生成全局 LogicLib 谓词 `${isUpdated}` / `${isForceRun}` / `${isForAllUsers}` / `${isForCurrentUser}`，任何钩子宏里可直接用。
- **electron-updater 参数拼装**（`NsisUpdater.doInstall`）：恒传 `--updated`；`isSilent=true` 才加 `/S`；`isForceRunAfter=true` 加 `--force-run`。
- **assisted installer 页面流**（oneClick:false）：welcome(未定义则无) → license → install-mode 选择 → directory → INSTFILES(进度) → FINISH。`--updated` 时模板自带 `skipPageIfUpdated`（pre 回调 `${isUpdated}` → Abort）只跳 **license 和 directory** 两页；install-mode 页和 FINISH 页模板不跳，须自己用钩子处理（见下）。
- **initMultiUser**（.onInit）：读 HKLM/HKCU 的 InstallLocation 得 `$hasPerMachineInstallation` / `$hasPerUserInstallation`，早于任何页面 pre 回调，可在 `customInstallMode` 里安全引用。
- **CHECK_APP_RUNNING**：`${isUpdated}` 时不弹"应用正在运行"框，Sleep 后直接 taskkill（静默与否一致）。
- **更新链路中的旧卸载器**恒以 `/S /KEEP_APP_DATA --updated` 运行（installUtil.nsh），customUnInstall 里的 `IfSilent` 守卫在更新时始终生效。
- **安装节自启应用**（installSection.nsh，assisted）：仅 `${isForceRun} && ${Silent}` 才自启——**非静默安装装完不会自动重启**，必须在 FINISH 页链路补。

## 当前设计：更新 = 非静默进度弹窗，全程零点击

`quitAndInstall` **故意传 `isSilent=false`**：assisted installer 可见运行，用户在数秒安装期看到进度页而非"黑洞"（降低焦虑）。零点击靠以下守卫链，改任一处都可能回归"弹向导页 / 装完不重启"：

| 环节 | 守卫 | 位置 |
|---|---|---|
| license 页 | 模板 `skipPageIfUpdated`（directory 页已因 `allowToChangeInstallationDirectory:false` 不再存在） | 模板自带 |
| per-user/per-machine 选择页 | `customInstallMode` 无条件 `StrCpy $isForceCurrentInstall "1"` 跳页——安装器锁死 per-user，首装与更新都不再提供 per-machine / 目录选择 | installer.nsh |
| FINISH 页 | `customFinishPage`：isUpdated 时 pre 回调 `Call StartApp` + `Abort`（自动重启并关闭安装器）；全新安装保持默认"运行+完成"页 | installer.nsh |
| Defender 询问 MessageBox | `IfSilent` **加** `${isUpdated}` 双守卫（更新不再静默，单靠 IfSilent 挡不住） | installer.nsh |
| 运行中应用 / 旧卸载器 | 模板自动处理（见上） | 模板自带 |

首装的 Defender 排除按路径注册、更新后仍有效，所以更新期间不重复弹 UAC。`--force-run` 仅覆盖静默回退路径（如 elevate 失败转静默）。

## Defender 排除脚本

- 脚本自定位：位于 `$INSTDIR\resources\defender\`，安装根 = `$PSScriptRoot` 上两级；排除两条路径：安装根 + electron-updater 下载缓存 `%LOCALAPPDATA%\<updaterCacheDirName>`。
- **缓存目录名不硬编码**：从随包 `resources/app-update.yml` 读 `updaterCacheDirName`（值可能带单引号，要 Trim）。当前值 `@universe-editoreditor-updater`。
- 已知取舍：UAC 输入了**另一个**管理员账号凭据时 `$env:LOCALAPPDATA` 指向该管理员 profile——极少数场景，排错路径只是少一条排除，无副作用。
- Defender 的**正解是代码签名**（VSCode 零排除、靠 EV 签名信誉）；排除是治标，本机排除生效时解压 ~22ms/MB。

## 性能根因（2026-07 定案，别再走弯路）

"点击更新→新版启动"黑洞两部分：

1. **`WM_SETTINGCHANGE` 广播被挂死窗口阻塞（波动大头，0~35s+）**：NSIS `SendMessage ${HWND_BROADCAST} ... /TIMEOUT=5000` 底层是 `SMTO_NORMAL`，对桌面**每个**消息泵挂死的顶层窗口串行等满 5s（实测一个卡死的 VSCode 更新器 7 窗 = +35s）。修复（installer.nsh 两处已落地）：
   ```nsis
   System::Call 'user32::SendMessageTimeout(p 0xFFFF, i 0x1A, p 0, t "Environment", i 0x2, i 1000, *p .r0)'
   ```
   （0x1A=WM_SETTINGCHANGE，0x2=SMTO_ABORTIFHUNG，1s 超时）。**边界**：ABORTIFHUNG 依赖系统 hung 标记，对长期挂死进程有效（微基准 36.5s→1.3s），对刚被 `NtSuspendProcess` 挂起的进程无效（标记滞后，两种 flag 都 ~71s）——必须叠加 1s 短超时兜底；正常窗口毫秒级响应无损失。另：PowerShell `[Environment]::SetEnvironmentVariable(...,'User')` 内部**自带一次 SMTO_NORMAL 广播**，卸载侧 PATH 移除因此改 `Set-ItemProperty` 直写注册表。
2. **解压双写本体（固定 ~6s @305MB）**：模板 `extractUsing7za` 先解到 `$PLUGINSDIR` 再 CopyFiles 到 `$INSTDIR`（PR #6547 原子性保护）。耗时 ∝ 净荷字节 ~22ms/MB（本机 Defender 排除生效），瘦身 48MB 仅省 ~1s；patch 掉双写收益 ~2-3s 且丢保护，**已评估搁置**。压缩等级/差量/盘速均已排除。

## 测量与验证方法学

- **离线安装计时**：`<installer>.exe /S /D=%TEMP%\x` + PowerShell 计时。坑：计时前必须删 HKCU uninstall 注册表项（`HKCU\Software\Microsoft\Windows\CurrentVersion\Uninstall\<GUID>`，否则先跑旧卸载器污染数据）；每轮安装会向用户 PATH prepend `$INSTDIR\bin` 并写右键菜单注册表，测完清理。
- **真实更新端到端**：靠 `updateShutdownTrace.ts`（quitAndInstall 打 click/confirmed/afterQuitAndInstall，index.ts 打 will-quit 三点，下次启动用 `process.getCreationTime()` 算黑洞）。离线 `/S /D=` 只测安装器一段，测不到"旧卸载器+安装+relaunch"全链。
- **非静默更新流程验证**（打包后必做，验证零点击守卫链）：
  ```powershell
  $p = Start-Process -FilePath '<installer>.exe' -ArgumentList '--updated' -PassThru
  $p.WaitForExit(180000)   # 卡在任何交互页 → 超时 = 失败信号
  Get-Process -Name 'Universe Editor'   # 装完应自动重启
  ```
- **人造复现广播阻塞**：WinForms `Show()+Sleep` 的窗口**不会**阻塞广播；要用真实挂死进程或 `NtSuspendProcess`。
- 打包命令：`pnpm --filter @universe-editor/editor package:win:installer`（产物在 `apps/editor/release/`）。
