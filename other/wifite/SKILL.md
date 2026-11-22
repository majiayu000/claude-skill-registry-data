---
name: "wifite"
description: ">"
---

# Wifite

*Sourced from killvxk-malskills-zh*

# Wifite

自动化 Wi-Fi 破解工具 —— 一条命令即可攻击 WEP/WPA/WPA2/PMKID。

## 快速开始

```bash
pip install wifite   # 或使用：apt install wifite

# 全自动模式（扫描并攻击所有可见网络）
sudo wifite

# 针对指定 BSSID
sudo wifite --bssid AA:BB:CC:DD:EE:FF

# 仅 WPA 握手包抓取 + 字典破解
sudo wifite --wpa --dict /usr/share/wordlists/rockyou.txt

# PMKID 攻击
sudo wifite --pmkid
```

## 核心参数

| 参数 | 用途 |
|------|---------|
| `--bssid MAC` | 针对指定接入点 (AP) |
| `--essid NAME` | 按 SSID 名称指定目标 |
| `--channel N` | 指定目标信道 |
| `--wpa` | 仅攻击 WPA 目标 |
| `--wep` | 仅攻击 WEP 目标 |
| `--pmkid` | PMKID 攻击（无需客户端） |
| `--dict FILE` | 用于破解的字典文件 |
| `--no-deauth` | 跳过去认证（更隐蔽） |
| `--timeout N` | 攻击超时时间（秒） |
| `--crack` | 捕获后自动破解 |

## 常用工作流

**自动化 PMKID + 破解：**
```bash
sudo wifite --pmkid --dict rockyou.txt
```

**仅抓取 WPA 握手包（不破解）：**
```bash
sudo wifite --wpa --no-crack
# 握手包保存到 ~/hs/
# 稍后手动破解：aircrack-ng ~/hs/*.cap -w rockyou.txt
```

## 参考资源

| 文件 | 何时加载 |
|------|--------------|
| `references/` | 依赖项检查清单及故障排查 |

