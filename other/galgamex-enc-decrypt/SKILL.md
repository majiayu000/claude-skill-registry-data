---
name: galgamex-enc-decrypt
description: 解密并从 galgamex.com 下载的 .enc 文件中提取游戏。.enc 是 Paranoia File & Text Encryption (P.T.E. / S.S.E. File Encryptor) 加密的归档，解密后得到一个 RAR/ZIP（通常与 .enc 同密码）。适用于用户在 Gamex-xxxxx 等目录下拿到 PC.enc / *.enc 文件，需要还原成可运行的 galgame 的场景。
agent_created: true
---

# 解密 galgamex .enc 文件并提取游戏

## 背景
galgamex.com 的资源是 **P.T.E.（Paranoia File & Text Encryption，命令行版叫 S.S.E. File Encryptor）** 加密的 `.enc` 归档。文件头魔数为 `53 53 45 46 45`（`SSEFE`）。
解密后会得到一个 **RAR 或 ZIP** 归档，**该归档本身通常也用同一密码加密**（如 `galgamex.com`）。

依赖一般已随资源一起放在工作区（不要自己重装）：
- `./.ssecli/ssefenc.jar` — S.S.E. 命令行加解密工具
- `./.jre_extract/PFiles64/Eclipse Adoptium/jre-21.0.12.101-hotspot/bin/java.exe` — 随附的 JRE（Java 11+ 即可）
- 系统中需有 7-Zip（`7z` 命令）用于解 RAR/ZIP

## 步骤

### 1. 解密 .enc → 原始归档（RAR/ZIP）
用 ssefenc 的 `dec` 子命令，密码用 `--password`/`-p`（也可走 `--password-env` 避免进历史）：

```bash
JRE="C:/SoftWare/FUN/Game/.jre_extract/PFiles64/Eclipse Adoptium/jre-21.0.12.101-hotspot/bin/java.exe"
SSECLI="C:/SoftWare/FUN/Game/.ssecli"
ENC="C:/SoftWare/FUN/Game/Gamex-005650/PC.enc"

"$JRE" -Xmx4g -jar "$SSECLI/ssefenc.jar" dec -p galgamex.com -o "$(dirname "$ENC")" "$ENC"
```

- 输出文件默认与输入同目录，名称由 .enc 去掉后缀得到（可能带原始扩展名如 `.rar`/`.zip`）。
- 退出码 3 = 密码错误或文件损坏。
- 文件较大（1~4GB）时放到后台跑（`run_in_background: true`），用 TaskOutput 等完成。

### 2. 解压还原出的 RAR/ZIP 到目标目录
先验证密码（`Everything is Ok` 即正确），再解压：

```bash
7z="C:/SoftWare/Sys Soft/7-Zip/7z"   # 按实际路径调整
ARCHIVE="C:/SoftWare/FUN/Game/Gamex-005650/PC.rar"

# 验证（测试密码）
"$7z" t -pgalgamex.com "$ARCHIVE"

# 解压到目标目录（x = 保留完整路径）
"$7z" x -pgalgamex.com -y -o"C:/SoftWare/FUN/Game" "$ARCHIVE"
```

- `Encrypted = +` 表示归档内文件也加密，必须带 `-p<密码>`。
- 顶层通常是一个游戏名文件夹，直接解压到 `C:\SoftWare\FUN\Game` 即可保持整洁。
- 解压后会出现游戏 exe（如 `ElectronicsThriftStore.exe`）。

## 注意事项
- 不要删除 `.enc` 和解密出的归档，除非用户确认要回收空间。
- 多卷分卷（如 `PC.z01.enc`/`PC.z02.enc`/...）需要先各自解密成 `PC.z01`/`PC.z02`/... 再用 7z 从 `.zip`/`.rar` 主卷解压（7z 会自动拼接）。
- 解压后的 `steam_appid.txt` 等是正常现象，直接运行 exe 即可。

## 验证
- 解密：ssefenc 输出 `Completed: OK`。
- 解压：7z 输出 `Everything is Ok`，目标目录出现 exe 与 `_Data` 文件夹。
