---
name: radio-sdr
description: "SDR Security Assessment"
---

# SDR Security Assessment

## Scope

Use this module only for radio frequency analysis on bands and equipment you own or are authorized to assess. Comply with all local radio regulations.

## Workflow

1. Define target frequency range and authorized transmission parameters.
2. Configure SDR hardware and software for passive reception.
3. Perform spectrum scan to identify active signals in authorized band.
4. Capture signal samples for offline analysis and characterization.
5. Identify modulation scheme, data rate, and framing structure.
6. Document protocol layers if digital encoding is present.
7. Assess signal for known vulnerabilities in modulation or encoding.

## Safety Rules

- Do not transmit on frequencies without proper licensing and authorization.
- Do not intercept communications not intended for your equipment.
- Do not jam, interfere with, or disrupt any radio communications.
- Do not violate local telecommunications regulations.

## Output

Return evidence table with columns: Frequency | Modulation | Bandwidth | Protocol | Security Finding | Regulatory Status.

## 使用前核对

目标与操作范围以用户当前请求为准；核对方法前置条件、工具和附件，按实际执行层级记录结果。正文不表示示例代码已经在本机执行或验证。
