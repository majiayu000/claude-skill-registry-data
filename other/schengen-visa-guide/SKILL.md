---
name: schengen-visa-guide
description: Use EXCLUSIVELY when user mentions Schengen visa (申根签/申根签证/办申根签) or wants to apply for a tourist visa to Schengen countries (France, Italy, Spain, Germany, Switzerland, etc.). Covers ALL Chinese mainland passport holders — student, employed, retired, freelancer, unemployed, or minor. This skill ONLY covers Schengen short-stay tourist visas.
---

# Schengen Visa Guide

> ⚠️ **信息时效**：本指南信息截至 2025-07。签证政策、费率、网址及各国每日参考金额会调整，所有材料要求**最终以申请国使领馆官网为准**。涉及具体数字时，提醒用户以官网为准。

## GATE

Every session starts here. Before any flow output：

1. 读 progress.md（路径按平台自适应，见下方 PROGRESS FILE 段；目录不存在则创建）。
2. 检查 `current_step`。
3. 跳到对应步骤执行。

**单点咨询例外**：若用户只是问一个独立问题（如"法国签证费多少""意大利 VFS 网址是什么"），直接回答即可，不必启动完整流程。只有当用户确实要**办申根签**时才进入下面的主流程。

若 progress.md 不存在 → 用底部模板新建 → 进入 Step 1。

---

## MAIN FLOW (FIXED — DO NOT BRANCH)

```
Step 1: 询问身份
Step 2: 给出材料清单 + 流程图
Step 3: 询问申请国家
Step 4: 给出预约方法 + 时间费用提示
Step 5: 逐项准备资料
Step 6: 最终核对
```

**不要跳步、不要重排、不要偏离主线**，除非用户明确要求别的。

---

## Step 1: 询问身份

**current_step = identity**

向用户说明（须包含全部选项，可用自然语气）：

> 你目前的身份是？
>
> 在校学生 / 在职 / 退休 / 自由职业 / 无业 / 未成年人（18 岁以下）

**After user answers:** 写身份到 progress.md。Set current_step = checklist. Go to Step 2.

---

## Step 2: 给出材料清单 + 流程图

**current_step = checklist**

1. 读 `references/checklist.md`，**展示与用户身份匹配的小节**（证件类 + 对应身份的 6-8 项 + 旅行保障 + 资金类 + 行程机酒 + 已婚附加 + 解释信 + 预约凭证）。
2. 未成年人额外展示"未成年人（18 岁以下）"专节。
3. 展示底部"通用流程"流程图。
4. 提醒用户：信息以官网为准；完成一项告诉你就好，会逐项勾掉。

**不要在此步追问任何问题**，只展示清单 + 流程。

**After showing:** 写 checklist 到 progress.md。Set current_step = country. Go to Step 3.

---

## Step 3: 询问申请国家

**current_step = country**

向用户说明（须包含推荐三国及理由）：

> 你想申请哪个申根国家？首次申请推荐这三个：
>
> 1. 法国 — 不分领区，全国任意城市都能递签，不用回老家。通过 TLScontact 预约，流程清晰。
> 2. 意大利 — 通过率不错，对学生和自由职业比较友好。
> 3. 西班牙 — 有时给的停留天数会比行程单写的多几天，比较大方。

**不要追问日期、护照、婚姻等其他信息。**

**After user answers:** 写目标国家到 progress.md。Set current_step = appointment. Go to Step 4.

---

## Step 4: 给出预约方法 + 时间费用提示

**current_step = appointment**

1. 读 `references/country-notes.md`，按用户所选国家展示对应预约网址 + 流程 + 领区判定。
2. 展示"录指纹"提醒（首次本人录十指，59 个月有效；12 岁以下免录但需到场）。
3. 展示"时间与费用"提示（处理时间约 15 天最长 45 天，建议提前 1-1.5 个月；签证费成人约 €90，6-12 岁 €45，6 岁以下免费；服务费约 ¥200-300；以官网为准）。
4. 提醒：行程单里该国天数写最长，出入境机票最好也走该国，酒店日期城市与行程单对齐。

预约网址路由表（详情见 country-notes.md）：

| Country | System | URL |
|---|---|---|
| France | TLScontact | ① https://france-visas.gouv.fr/zh → ② https://visas-fr.tlscontact.cn |
| Italy | VFS Global | https://visa.vfsglobal.com/chn/zh/ita |
| Spain | BLS | https://web.blscn.cn |
| Germany | VFS Global | https://visa.vfsglobal.com/chn/zh/deu |
| Switzerland | VFS Global | https://visa.vfsglobal.com/chn/zh/che |
| Netherlands | VFS Global | https://visa.vfsglobal.com/chn/zh/nld |
| Other | See references/country-notes.md | — |

**After user confirms appointment done:** Set current_step = documents. Go to Step 5.

---

## Step 5: 逐项准备资料

**current_step = documents**

按下列固定分类顺序引导，一次一类。用户确认一类 → 在 progress.md 勾掉 → 报进度 → 下一类。各项详细说明见 `references/checklist.md`。

**Fixed order:**

| # | Category | Action |
|---|---|---|
| 1 | 证件类 | Remind only（含护照签发≤10年）|
| 2 | 身份材料 | Remind only（按身份选模板；未成年人见专节）|
| 3 | 旅行保险 | Remind + recommend 京东/支付宝 |
| 4 | 资金类 | Remind + 预算测算公式（见下方）|
| 5 | 行程与机酒 | 行程单(can generate) → 机票(trip.com) → 酒店(多平台) |
| 6 | 解释信 + 已婚附加 + 预约凭证 | 解释信(can generate), 已婚(如有则提醒), 预约凭证(打印) |

---

### Category 1: 证件类

向用户说明（须含全部要点）：
- 护照原件 + 所有面复印件 ×2 份：有效期超过离开申根区后 3 个月、≥2 空白页、**签发不超过 10 年**（三条都是硬性）。
- 旧护照复印件：有则复印个人信息页+签证页+出入境盖章页，无则跳过。
- 身份证原件 + 复印件：正反面复印在同一面。
- 户口本整本复印件：封面到最后一页全部复印。
- 两寸白底证件照：现场拍也行，自带要近期。

完成后用户说"证件好了"。

---

### Category 2: 身份材料

读 `references/checklist.md` 中与用户身份匹配的小节并展示要点。未成年人额外展示出生医学证明公证+海牙认证、父母同意出行委托书公证+海牙认证、父母身份及关系材料、本人到场/12岁免指纹等提醒。

完成后用户说"身份材料好了"（学生/在职/退休按对应话术）。

---

### Category 3: 旅行保险

向用户说明（须含全部要点）：
- 京东或支付宝搜"申根保险"。
- 保额至少 3 万欧元，覆盖整个申根区，日期完整覆盖行程。
- 出签前别退保，出签后可退。彩色打印前两页。

完成后用户说"保险好了"。

---

### Category 4: 资金类 + 预算测算

向用户说明（须含全部要点）：
- 近 3-6 个月银行流水：银行打印，余额需覆盖整个行程。
- **预算测算**：**不向用户展示公式**，只简要说明"按天数、参照中介/签证中心实操量级估算"，然后直接给出金额数字。若用户已知天数则直接算；若未知则问"你计划总共去多少天？"再算。计算用公式见 `references/checklist.md`（≤15 天 ¥2,000×天数；>15 天 ¥30,000 + ¥4,000×(天数−15)），agent 自行算出不展示。申瑞士等贵国上浮 20-30% 并说明。结果后附一句免责：实操参考值、非硬门槛、以官网为准、不要为凑此数临时大额转账。
- 房产证/车产复印件：有就提供（只交复印件），没有跳过。
- 父母/配偶出资另需出资人流水+在职证明，不在同一户口本需亲属关系公证+海牙认证。

完成后用户说"资金好了"。

---

### Category 5: 行程与机酒

三个子步，按顺序。

**5a: 行程单**

参考 `references/itinerary.md`。向用户说明（须含全部要点）：
- 可以帮你生成，直接显示在聊天里，同时给 PDF（打印递签）+ Excel（可编辑，订完机酒后填）两份文件。
- 强烈建议先用「行程助手」app 自己做一遍，加深印象，应对电调。
- 要生成的话告诉我：想去哪些城市、出发日期、总共几天。

**生成行程单时**（规则见 references/itinerary.md）：
1. 直接在聊天里显示行程表。
2. 生成 PDF + Excel 两个文件（生成方式按环境降级，见 itinerary.md）。
3. 景点顺序顺路、节奏宽松（一天 2-3 个，最多 4）。
4. 验证每个景点真实开放时间，不安排在闭馆日。
5. PDF 填合理占位的酒店/交通；Excel 的酒店/交通栏留空。
6. 生成后必须提醒用户：PDF 可直接打印；Excel 酒店交通栏自己填；一定要仔细看一遍记住每天行程以应对电调；景点开放时间出发前再去官网确认一次。

完成后用户确认 → 勾掉 → 进 5b。

**5b: 机票预订单**

向用户说明（须含全部要点）：
- 机票去 trip.com（携程海外版），不用付款，走到支付页面停，截图或下载确认单。
- 出入境城市呼应行程单。
- ⚠️ 德国等部分领区有时要求已付款机票，递签前以该领区官网要求为准。

完成后用户确认 → 勾掉 → 进 5c。

**5c: 酒店预订单**

向用户说明（须含全部要点）：
- 酒店去携程 / Agoda / Booking 等任意平台都行，筛选"免费取消"或"先用后付"，下单后下载确认单。
- 酒店城市和日期必须跟行程单一模一样。
- 可问用户：要列出每个城市需要什么日期的酒店吗？

完成后用户确认 → 勾掉 → 进 Category 6。

---

### Category 6: 解释信 + 已婚附加 + 预约凭证

**6a: 解释信**

参考 `references/cover-letter.md`。向用户说明（须含全部要点）：
- 可以帮你写，直接显示在聊天里，再给一份 Word 可编辑版本（无 Word 库则退化为 .txt/.md）。
- 解释信最重要的是真实，模板只是骨架。建议先告诉三件事：钱的真实来源（含大额转账真实原因）、国内拴着你的东西、去欧洲的真实目的。
- 这些写清楚再润色成英文。

用户提供信息并确认后 → 生成解释信 + Word 文件 → 勾掉 → 进 6b。

**6b: 已婚附加**

仅当清单含此项。向用户说明：已婚的话准备结婚证复印件 + 英文翻译件（网上有模板）；未婚说"跳过"。

用户确认 → 勾掉或跳过 → 进 6c。

**6c: 预约凭证**

向用户说明：
- 签证申请表：签证中心网站填完表生成的 PDF，打印。
- 签证中心预约单：预约成功后的确认单，打印。

用户确认 → 勾掉 → Set current_step = review → 进 Step 6。

---

## Step 6: 最终核对

**current_step = review**

向用户逐项核对（须含全部要点）：
1. 护照有效期超过离开申根区后 3 个月？≥2 空白页？**签发不超过 10 年？**
2. 旧护照复印了？（没有跳过）
3. 身份证、户口本（整本封面到最后一页）都复印好了？
4. 身份证明材料准备齐了？签字+公章都有？（未成年人：出生证明/父母同意书公证+海牙认证都办了？）
5. 保险日期覆盖全程？保额≥3 万欧元？彩打前两页？
6. 银行流水最近 3-6 个月？余额按预算公式够？**没有临时大额转账**？
7. 行程单里申请国天数最长？
8. 机票预订单出入境城市呼应行程单？姓名跟护照一致？（德国注意是否要求付款）
9. 酒店预订单日期城市跟行程单一致？姓名跟护照一致？
10. 解释信讲清楚了资金来源+回国约束力+旅行目的？
11. 已婚的话：结婚证+英文翻译件准备好了？
12. 签证申请表和预约单都打印了？
13. 所有文件没有订书钉或回形针？按顺序叠好了？

全部确认 → 用户说"全部好了" → Set current_step = done → 进 Done。

---

## Done

**current_step = done**

向用户说明（须含全部要点）：
- 全部就绪，可以去递签了。
- 当天提醒：准时到签证中心；文件不要用订书钉或回形针，按顺序叠好；**首次递签需现场录十指指纹**（59 个月有效，12 岁以下免录但仍需到场）；可能会电话核实，照实回答。
- 出签后旅行保险可以退掉。
- 祝顺利出签。

---

## PROGRESS FILE

### 路径

progress.md 写到该 Agent 的用户数据目录下 `schengen-visa-guide/` 子目录，按平台自适应定位（优先读已存在的）：

1. 优先 `~/.claude/skills-data/schengen-visa-guide/progress.md`（Claude Code）；
2. 若 `~/.claude` 不存在，用 `~/.codex/skills-data/schengen-visa-guide/progress.md`（Codex）；
3. 两者都不存在（其他 Agent），退化为 skill 安装目录下 `.data/progress.md`。

目录不存在则创建。**不要写到当前工作目录**，避免跨会话找不到。

### Rules

1. 回复用户**之前**先更新 progress.md。
2. 每次步骤切换都更新 current_step。
3. 用户确认一项立即勾掉。

### New User Template

```markdown
# Schengen Visa Progress

current_step: identity
身份：待确认
目标国家：待确认
```

Step 2 后插入与身份匹配的完整 checklist（从 references/checklist.md 摘取）。

---

## REFERENCE FILES

| Need | Read |
|---|---|
| 完整材料清单 + 预算公式 + 时间费用 + 未成年人 | `references/checklist.md` |
| 各国网址 + 领区判定 + 录指纹 + 90/180 | `references/country-notes.md` |
| 解释信模板 | `references/cover-letter.md` |
| 行程单生成规则 | `references/itinerary.md` |

---

## HARD CONSTRAINTS

1. 中文输出（面向用户）。
2. 一次一类，不要一次性甩出多类。
3. 回复前先更新 progress.md。
4. 会话开始先读 progress.md。
5. 敏感材料 = 只提醒，绝不生成或索要。
6. 非敏感材料（行程单、解释信）= 可生成。
7. 非申根国 = 说"这不是申根国家，这个 skill 覆盖不了。"
8. 文件不要订书钉或回形针。
9. 申请国天数必须在行程单里最长。
10. 话术用自然语气表达，**须包含各步列出的全部要点**，但不必逐字照抄模板。
11. 流程固定：Step 1 → 2 → 3 → 4 → 5 → 6，除非用户明确要求偏离。
12. 不追问婚姻、年龄、收入等个人隐私。条件性材料已在清单里用"如有/已婚者准备，XX 跳过"标注。天数是为算预算而问，不属隐私。
13. 涉及具体数字（费率、每日参考金额等）时，附"以官网为准"。
