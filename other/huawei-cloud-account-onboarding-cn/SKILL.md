---
name: huawei-cloud-account-onboarding-cn
description: "Checks Huawei Cloud real-name verification (实名认证) status and guides face-scan verification, read-only via hcloud: reads the account's verification state, and when unverified fetches the face-auth QR address, renders it in the terminal to scan by phone, then polls until verified. Use when the user mentions 华为云 / Huawei Cloud plus 实名认证/实名/认证状态/real-name verification, or a Huawei Cloud flow reports verification is required. Face-scan channel only; refuses ID, document, bank-card and SMS-code intake, refuses write operations (enterprise and certificate channels are console-only), and refuses non-Huawei-Cloud identity flows."
metadata:
  language: zh-CN
  translation_of: huawei-cloud-account-onboarding
  version: "1.0.3"
  openclaw:
    requires:
      bins: [hcloud]
    primaryEnv: HUAWEICLOUD_SDK_AK
    homepage: https://github.com/concept-git/cloud-concept-skills/tree/main/skills/zh-CN/huawei-cloud-account-onboarding-cn
    envVars:
      - {name: HUAWEICLOUD_SDK_AK, required: false}
      - {name: HUAWEICLOUD_SDK_SK, required: false}
---

# 华为云账号开通 · 实名认证引导

> **华为社区版** · 社区维护，非华为云官方；结论以当次 hcloud 响应为准。

使用 **hcloud ≥7.2**，只读查询当前账号的实名状态和类型。已实名只说明实名前提已满足，不证明库存、配额、支付或创建权限；未实名时引导账号本人扫码完成认证。

用户仅检查 hcloud 安装或连接时，转可用性检查流程；不以实名状态查询充当连接探测。

## 三步

1. **查状态** —— 先跑 `ShowRealNameAuthStatus`，按四态分流。取码命令不校验实名状态，已实名账号照样返回可用二维码，门禁只能由技能承担。
2. **递二维码** —— 仅当未实名、且用户此刻能拿手机时才取码，交 `scripts/render-qr.ts` 渲染。地址是一次性凭据：不落盘、不转发、不复用。
3. **盯落地** —— 用 waiter 轮询至已实名；超时先问用户再重取，不自动重发。

命令、响应字段与取值一律抄 `references/commands.md`，不用 `--help` 现场发现、不自拼参数。无 hcloud profile 时停下，请用户自行配置，不接收聊天凭证，不代写凭证。

## 红线

- **只读** —— 不提交、不变更、不撤销认证，写命令一律拒绝。
- **不收材料** —— 身份证号、证件照、银行卡号、短信验证码一律拒收并提示删除；三步流程不需要其中任何一项。
- **不代认证** —— 不代扫码、不代做活体、不把二维码给他人；代做会被华为云判定非本人并可能冻结账号。
- **只做人脸通道** —— 企业认证、证件认证、银行卡认证、认证变更、审核意见查询均指路控制台「账号中心 → 实名认证」；非华为云或通用 KYC 说明超出范围。

## References

实体与四态状态机 `references/concepts.md` · 命令与字段 `references/commands.md` · 二维码渲染 `scripts/render-qr.ts`（`npx tsx render-qr.ts <地址>`；首次先 `cd scripts && npm install`）
