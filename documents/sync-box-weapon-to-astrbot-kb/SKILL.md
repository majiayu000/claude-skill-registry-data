---
name: sync-box-weapon-to-astrbot-kb
description: 将腾讯文档导出的「群员信息总览」xlsx 同步到 AstrBot 知识库「盒武器」。手动触发，不做定时。
---

# 同步盒武器到 AstrBot 知识库

将「群员信息总览.xlsx」转换并上传到 AstrBot 的「盒武器」知识库。

## 触发条件

用户说"更新盒武器""同步盒武器""更新群员信息知识库"等。

## 工作流

### 1. 读取 xlsx 文件

文件通常由腾讯文档导出，路径由用户提供（如 `/mnt/e/Download/群员信息总览.xlsx`）。

**坑**：Arch 上 openpyxl 有 `Fill() takes no arguments` 兼容性问题（Python 3.12+/3.14）。不装 openpyxl，直接用 zipfile + XML 解析：

```python
import zipfile, xml.etree.ElementTree as ET
NS = 'http://schemas.openxmlformats.org/spreadsheetml/2006/main'

with zipfile.ZipFile(xlsx_path) as z:
    # Read shared strings
    ss = ET.parse(z.open('xl/sharedStrings.xml'))
    strings = [''.join(t.text or '' for t in si.iter(f'{{{NS}}}t')) for si in ss.getroot()]

    # Read sheet 1
    sheet = ET.parse(z.open('xl/worksheets/sheet1.xml'))
    rows = []
    for row in sheet.findall(f'.//{{{NS}}}row'):
        rv = {}
        for c in row.findall(f'{{{NS}}}c'):
            col = ''.join(ch for ch in c.get('r') if ch.isalpha())
            v = c.find(f'{{{NS}}}v')
            if v is not None and v.text:
                rv[col] = strings[int(v.text)] if c.get('t') == 's' else v.text
        if rv:
            rows.append(rv)
```

### 2. 转换数据

列映射：A=姓名, B=是否在群, C=生理性别, D=昵称, E=QQ, F=电话, G=生日(Excel序列号), H=去向, I=位置/学校, J=专业, K=Steam好友代码, L=XP, M=收货地址

Excel 序列号转日期：
```python
from datetime import datetime, timedelta
def excel_to_date(serial):
    try:
        s = int(float(serial))
        if s < 60: return ''
        return (datetime(1899,12,30) + timedelta(days=s)).strftime('%Y-%m-%d')
    except: return ''
```

生成 Markdown：**以 QQ 号为 `## QQ: xxxxx` 主键**，不是姓名。开头必须有检索规则序言：

```markdown
# 群员信息总览（盒武器）— QQ号索引版

> **检索规则（最高优先级）：** 匹配群成员时，必须优先匹配 QQ 号。
> 每条聊天消息都附带发送者的 QQ 号（格式如 `昵称/QQ号`）。
> 当用户查询某人信息时，先用 QQ 号在本文档中搜索对应条目；
> 如果 QQ 号不在本文档中，再尝试用姓名或昵称模糊匹配。
> 严禁仅凭群名片或昵称判断身份，严禁将其他人的信息张冠李戴。
```

### 3. 上传到 AstrBot 知识库（先删后传，upload 用 urllib 而非 curl）

**关键**：必须先删除旧文档再上传。上传用 Python `urllib` 构造 multipart/form-data 比 curl 更可靠（curl 在 Hermes 沙箱中 token 容易被截断）。

**知识库信息**：
- kb_id: `c0ca81b9-f1f0-4479-9ce8-f6c3017958cf`
- kb_name: `盒武器`
- WebUI: `http://localhost:6185`
- 用户名: `Publieople`
- 密码: `Fzj103415422`

完整 Python 上传脚本示例：

```python
import urllib.request, json

# 1. 登录获取 token
login = json.dumps({"username": "Publieople", "password": "Fzj103415422"}).encode()
req = urllib.request.Request("http://localhost:6185/api/auth/login", data=login,
    headers={"Content-Type": "application/json"})
with urllib.request.urlopen(req) as resp:
    token = json.loads(resp.read())["data"]["token"]

KB_ID = "c0ca81b9-f1f0-4479-9ce8-f6c3017958cf"

# 2. 列出已有文档，记录 doc_id
req2 = urllib.request.Request(
    f"http://localhost:6185/api/kb/document/list?kb_id={KB_ID}",
    headers={"Authorization": "Bearer " + token})
with urllib.request.urlopen(req2) as resp:
    docs = json.loads(resp.read())
for item in docs['data']['items']:
    # 3. 删除所有旧文档
    del_data = json.dumps({"doc_id": item['doc_id'], "kb_id": KB_ID}).encode()
    req3 = urllib.request.Request("http://localhost:6185/api/kb/document/delete",
        data=del_data, headers={"Authorization": "Bearer " + token, "Content-Type": "application/json"},
        method="POST")
    with urllib.request.urlopen(req3) as resp3:
        print(f"Deleted: {item['doc_name']}")

# 4. 上传新文档（multipart/form-data）
with open("/tmp/box_weapon_qq.md", "rb") as f:
    content = f.read()

boundary = "----FormBoundary"
body = (
    f"--{boundary}\r\nContent-Disposition: form-data; name=\"kb_id\"\r\n\r\n{KB_ID}\r\n"
    f"--{boundary}\r\nContent-Disposition: form-data; name=\"file\"; filename=\"box_weapon_qq.md\"\r\n"
    f"Content-Type: text/markdown\r\n\r\n"
).encode() + content + f"\r\n--{boundary}--\r\n".encode()

req4 = urllib.request.Request("http://localhost:6185/api/kb/document/upload",
    data=body, headers={
        "Authorization": "Bearer " + token,
        "Content-Type": f"multipart/form-data; boundary={boundary}"
    }, method="POST")
with urllib.request.urlopen(req4, timeout=30) as resp:
    result = json.loads(resp.read())
task_id = result['data']['task_id']
print(f"Upload task: {task_id}")

# 5. 轮询等待完成
import time
for i in range(10):
    time.sleep(2)
    req5 = urllib.request.Request(
        f"http://localhost:6185/api/kb/document/upload/progress?task_id={task_id}",
        headers={"Authorization": "Bearer " + token})
    with urllib.request.urlopen(req5) as resp:
        prog = json.loads(resp.read())
    if prog['data']['status'] == 'completed':
        doc = prog['data']['result']['uploaded'][0]
        print(f"✅ {doc['doc_name']} ({doc['chunk_count']} chunks)")
        break
```

### 4. 验证检索（QQ 号精确匹配）

验证时用 QQ 号而非姓名，确认精确匹配：
```bash
curl -s -X POST http://localhost:6185/api/kb/retrieve \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"kb_names":["盒武器"],"query":"2631792752","top_k":1}'
```

确保返回结果中 QQ 号对应正确的人。

### 5. 告知用户

上传完成后报告：文档名、chunk 数、文件大小、检索验证结果。

## 已知问题与规避

### Hermes token 红action 导致 shell 命令断裂

Hermes 会自动替换 token 为 `***`，导致 bash 中的 `$TOKEN` 变量内容被截断。上传等操作应使用 `execute_code` + Python `urllib.request` 代替 shell `curl` 命令。

### SiliconFlow bge-m3 embedding_dimensions 警告

配置中 `embedding_dimensions: 1024` 会导致刷屏警告：
```
dimensions not supported for model 'BAAI/bge-m3' as SiliconFlow does not support this parameter for non-Qwen models: '1024'
```
虽然不影响实际检索（模型本身输出 1024 维），但建议设为 0 消除噪音。修改 `cmd_config.json` 中 `"embedding_dimensions": 0`。

### RAG 混淆：群名片 ≠ 真名

盒武器检索是语义匹配，不精确匹配 QQ 号。当群友用昵称/群名片互动时（如「边牧」「反模联战士」），bot 可能把 A 的信息串到 B 身上。

**缓解方案**（已放弃，改用 QQ 号主键 + agentic mode。以下方案仅供参考）：在生成 Markdown 时，给每个人前面加一行 `<!-- keywords: QQ=xxx, 别名=xxx, 群名片=xxx -->`，嵌入模型会把这段也向量化，提高检索精度。例如：

```markdown
<!-- keywords: QQ=3201115710, 别名=小门墙/马老师, 群名片=你群边牧 -->
## 马涵君
```

这样无论问「马涵君」「马老师」「边牧」都能命中同一 chunk。

### 检索可能把对话上下文信息当成事实

若群聊中 A 说「B 物理 619 分」，bot 可能把这话记成 A 的属性。这不是知识库的问题，是 LLM 上下文混淆。知识库层面无法解决——属于 prompt engineering 范畴。

### AstrBot KB 检索先天性缺陷：用消息文本而非发送者 QQ 号做 query

`kb_agentic_mode: false` 时，AstrBot 自动用**消息文本内容**做 embedding 检索，而非发送者的 QQ 号。这意味着 bot 收到的每个消息都会去 KB 搜"话题相关"的 chunk，而不是"这个人是谁"的 chunk。当消息话题与人员信息无关时，KB 根本不被触发。

**改进方案（已生效）**：
1. 设置 `kb_agentic_mode: true`（cmd_config.json），让 LLM 通过 tool call 主动查 KB
2. 在人格设定中加入身份识别规则：

```
【身份识别规则 - 最高优先级】
- 每条消息的发送者格式为"群名片/QQ号"，你必须用QQ号在"盒武器"知识库中查找此人真实身份
- 识别流程：提取QQ号 → 用QQ号搜知识库 → 确认真实姓名和群名片 → 再回复
- 严禁仅凭群名片或昵称判断身份。严禁将别人的信息串到说话人身上
- 如果盒武器中没有该QQ号，回复时说"我不认识你"，不要猜测
```

### LLM API 连接挂死（CLOSE-WAIT）导致不回复

症状：AstrBot 进程在但不对任何消息作出回应，日志停止更新。根因通常是 DeepSeek API 调用时 TCP 连接进入 CLOSE-WAIT 状态卡住整个异步管线。

诊断：`ss -tnp | grep astrbot` 看到 CLOSE-WAIT 连接即确认。
修复：`sudo systemctl restart astrbot`（systemd 服务，不要用 kill/background 方式重启）。

### AstrBot 操作注意事项

- **AstrBot 支持热重载**：新插件放到 `data/plugins/` 后自动检测，**不要 kill 进程**。
- **AstrBot 是 systemd 服务**：`sudo systemctl restart astrbot` 重启，`sudo journalctl -u astrbot -f` 看实时日志。日志可能在 journal 而非数据目录的 log 文件中。
- **插件重载 API**：`POST /api/plugin/reload-failed` + `{"dir_name": "插件目录名"}`，可单独重载加载失败的插件。
- **token 红action**：Hermes 在 shell 命令中自动将 token 替换为 `***`，导致 bash 语法错误。操作 API 时优先用 `execute_code` + Python `urllib.request` 代替 shell `curl`。

## References

- `references/xlsx-xml-fallback.md` — openpyxl on Python 3.14 的 XML 回退方案（详见 xlsx 技能的 reference）
- `references/excel-date-conversion.py` — Excel 序列号转日期函数
- `references/group-chat-style.md` — 707942526 群聊风格观察（阮出顶号风格参考、黑话速查、LLM 易踩坑）
- `references/astrbot-plugin-install.md` — AstrBot 插件安装流程、排障、重启方式、API 交互注意事项
- `references/astrbot-skill-format.md` — AstrBot Skill 文件格式、LLM 上下文 sender 信息格式、KB vs Skill 选型速查
