---
name: clash-google-rules-extractor
description: 从 Clash 备份配置中提取并整合 Google 相关规则，插入独立的「🌐 Google专用」代理组。当用户提到「Clash 规则」「Google 专用」「提取 google 规则」「clash backup yaml」「clash-google-rules-extractor」时使用。
metadata:
  short-description: 从 Clash 备份配置中提取 Google 规则并生成 Google专用 代理组
---

# Clash Google Rules Extractor

Extract and consolidate Google-related rules into a dedicated "Google专用" proxy group from a Clash backup configuration.

## Usage

```
/clash-google-rules-extractor <backup_file> [output_file]
```

### Arguments

- `backup_file`: Path to the Clash backup YAML file (e.g., `D:\Data\clash-backup-20261008.yaml`)
- `output_file`: (Optional) Output path. If not specified, generates `clash-google-YYYYMMDD.yaml` in the same directory

### Examples

```
/clash-google-rules-extractor D:\Data\clash-backup-20261008.yaml
/clash-google-rules-extractor D:\Data\clash-backup-20261008.yaml D:\Data\custom-output.yaml
```

## What this does

1. Reads the input Clash backup file
2. Extracts the "🧲 海外AI" proxy group's node list
3. Creates a new "🌐 Google专用" proxy group with the same nodes
4. Applies all predefined Google-related rules (from `google-rules.yaml`)
5. Outputs a complete configuration file ready to use

## Key Features

- **Fixed Rules**: All Google-related domain rules are predefined and consistent
- **Auto Node Sync**: Automatically uses the latest node list from "海外AI" group
- **Minimal Changes**: Original configuration structure preserved, only Google rules extracted
- **Idempotent**: Safe to run multiple times on the same backup

## Configuration

Rules are defined in two separate files:

- **`google-rules.yaml`**: Google-related domain rules (AI products, APIs, etc.)
- **`custom-rules.yaml`**: Custom rules (local direct connections, ad blocking, domestic services, etc.)

To add or modify rules, edit the corresponding YAML file.

## Notes

- The "🌐 Google专用" group is inserted right after "🧲 海外AI"
- Original backup file is never modified
- Output file includes:
  - All original configuration from backup
  - New "🌐 Google专用" proxy group and rules
  - All custom rules from `custom-rules.yaml`
- Rule placement:
  1. Custom rules (`custom-rules.yaml`) go at the very top
  2. AI-specific Google rules (`google-rules.yaml` → `rules`) are inserted right after the last original rule targeting "🧲 海外AI"
  3. Generic Google rules (`google-rules.yaml` → `override_rules`: `DOMAIN-KEYWORD,google`, `googleapis.com`, `googleapis.cn`) replace the matching original rule **in place**, only changing the target group. If no match exists, insert before `GEOIP,CN`
  4. Never move the generic rules to the top: they would shadow more specific original rules such as `dl.google.com` (DIRECT), `mtalk.google.com` (谷歌FCM), `google-analytics.com` (广告过滤) and `youtubei.googleapis.com` (国外媒体)
- Skip a custom rule if an identical rule already exists, or if an earlier `DOMAIN-SUFFIX` rule with the same target already covers it
