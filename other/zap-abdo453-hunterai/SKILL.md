---
name: "zap"
description: ">"
---

# Zap

*Sourced from killvxk-malskills-zh*

# OWASP ZAP

开源 Web 应用扫描器与拦截代理。

## 快速开始

```bash
zap.sh
zap.sh -daemon -port 8090 -host 127.0.0.1
docker run -t owasp/zap2docker-stable zap-baseline.py -t http://target.com
docker run -t owasp/zap2docker-stable zap-full-scan.py -t http://target.com
```

## 扫描类型

| 扫描类型 | 命令 | 说明 |
|------|---------|-------|
| 基线扫描 | `zap-baseline.py` | 仅被动扫描，适合生产环境 |
| 全量扫描 | `zap-full-scan.py` | 主动扫描，可能具有破坏性 |
| API 扫描 | `zap-api-scan.py` | 针对 OpenAPI / SOAP / GraphQL 目标 |

## REST API（守护进程模式）

```bash
curl "http://localhost:8090/JSON/spider/action/scan/?url=http://target.com"
curl "http://localhost:8090/JSON/ascan/action/scan/?url=http://target.com"
curl "http://localhost:8090/JSON/core/view/alerts/"
```

## 参考资源

| 文件 | 何时加载 |
|------|--------------|
| `references/` | 认证配置、CI 集成、脚本 API |

