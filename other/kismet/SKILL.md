---
name: "kismet"
description: ">"
---

# Kismet

*Sourced from killvxk-malskills-zh*

# Kismet

无线探测器和嗅探器 — 被动 Wi-Fi、Bluetooth、Zigbee、SDR。

## 快速开始

```bash
apt install kismet

# 启动并开启 Web UI（端口 2501）
kismet -c wlan0

# 打开 Web UI
open http://localhost:2501
# 默认凭证：kismet/kismet

# 捕获到 pcap
kismet -c wlan0 --log-types pcapppi
```

## 主要功能

| 功能 | 用途 |
|------|------|
| AP 发现 | SSID、BSSID、信道、加密、信号强度 |
| 客户端追踪 | 关联到 AP 的设备 |
| Bluetooth | BT 经典 + BLE 扫描（需要适配器） |
| Zigbee | IoT/传感器网络检测 |
| GPS 集成 | 使用 gpsd 为设备标注地图位置 |
| 日志记录 | Kismet DB、pcap、JSON、netxml |

## 核心参数

| 参数 | 用途 |
|------|------|
| `-c IFACE` | 捕获接口 |
| `--no-logging` | 禁用日志记录 |
| `--log-prefix DIR` | 日志输出目录 |
| `--log-types TYPE` | 日志格式 |
| `--daemonize` | 在后台运行 |
| `--override wardriving` | 战争驾驶模式 |

## 常用工作流

**被动战争驾驶 (Wardriving)：**
```bash
kismet -c wlan0 --override wardriving --log-prefix /tmp/wardriving
```

**捕获所有流量以供离线分析：**
```bash
kismet -c wlan0 --log-types pcapppi --log-prefix /tmp/capture
# 使用 wireshark 分析
```

## 参考资源

| 文件 | 加载时机 |
|------|----------|
| `references/` | GPS 配置、Bluetooth 适配器配置 |

