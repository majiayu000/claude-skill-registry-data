---
name: Strix•新手入口
description: "给中文用户和新手用的 Strix Lite 统一入口：先判断该用哪一个 strix-* 工具或漏洞测试 skill，再给最小化起手步骤；适合在 Web 安全测试、工具链使用、漏洞验证时不知道先用哪个 Strix skill 的场景;触发名:strix-beginner-hub"
---

# Strix 新手入口

这是给 **不会选 Strix skill 的人** 用的轻量入口。

它不是为了替代 `ctf-super-hub`，而是作为你现有 CTF 主包的 **增强层**：
- CTF 主入口仍然是 `ctf-super-hub`
- 当题目明显进入 Web 测试、漏洞验证、工具链使用阶段时，再调用这一层

## 什么时候用

出现下面情况时优先考虑这个入口：

- 你已经判断是 Web 题，但不知道该先用 `httpx / ffuf / katana / nuclei / sqlmap` 哪个
- 你知道大概是 SQLi / XSS / SSRF / 文件上传 / JWT / IDOR 一类，但不会选专项 skill
- 你想先用更工具化、命令手册化的方式推进，而不是纯思路型讲解

## 使用原则

- **不改变主结构**：它只是增强能力，不替代现有 CTF 主入口
- **先小步验证**：默认只给最小化下一步，不一上来就堆很多命令
- **先判断工具还是漏洞**：
  - 如果你还在发现目标 / 枚举入口 / 抓取路由，优先走工具 skill
  - 如果你已经知道疑似漏洞类型，优先走漏洞专项 skill

## 新手默认路由

### 工具链类
- `strix-httpx`：先探测站点、标题、状态码、技术指纹
- `strix-katana`：爬路径、JS、路由
- `strix-ffuf`：目录、文件、参数模糊测试
- `strix-nuclei`：快速模板扫描
- `strix-sqlmap`：SQL 注入自动验证与枚举

### 漏洞专项类
- `strix-sql-injection`
- `strix-xss`
- `strix-ssrf`
- `strix-rce`
- `strix-authentication-jwt`
- `strix-idor`
- `strix-information-disclosure`
- `strix-insecure-file-uploads`
- `strix-open-redirect`
- `strix-csrf`
- `strix-business-logic`
- `strix-broken-function-level-authorization`
- `strix-path-traversal-lfi-rfi`

### 模式类
- `strix-quick`：先打高价值、快确认
- `strix-standard`：更平衡地覆盖测试面

## 推荐默认策略

如果用户没有指定：
- **还在摸目标结构** -> `strix-httpx` / `strix-katana` / `strix-ffuf`
- **已经怀疑具体漏洞** -> 对应专项 skill
- **想快一点扫高影响点** -> `strix-quick`
- **想更系统但不过深** -> `strix-standard`

## 新手友好输出格式

1. 现在更像哪一类问题
2. 为什么先用这个 Strix skill
3. 先做哪 1~3 步
4. 每一步是在干什么
5. 如果没结果，下一步切到哪个 skill

## 参考文件

- `references/router-cheatsheet.md`
- `references/examples.md`
