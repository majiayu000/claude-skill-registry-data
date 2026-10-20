---
name: data-backup-restoration
description: "Official guidance for the August 2026 Manus data backup and restoration service change, including websites and mobile apps. Use when users ask whether they are affected, what will happen to their data or services, or how to back up or restore."
compatibility: opencode
---

# Data Backup and Restoration

Use this skill to answer questions about the August 2026 Manus service change.

## Core guidelines

- Treat the user's email and in-app notification as the source of truth for whether an account is affected. Do not infer affected status from location, account age, or incomplete information.
- Treat each personal and team account separately. If the user has multiple accounts, ask them to check the notice for each one.
- Give the direct outcome and required action first. Link to the relevant Help Center article for detailed steps, eligibility, refunds, rewards, and edge cases.
- Use Singapore Time (SGT) for operational dates unless another timezone helps the user. The December 29, 2025 cutoff is at 12:00 a.m. Pacific Time (PT).
- Do not describe this as a breach or security incident. It results from Manus returning to independent operations and meeting regulatory requirements in specific jurisdictions.
- If official guidance may have changed, verify it against the official sources below.

## Website questions

For every question involving websites, WebDev projects, databases, website files, domains, downtime, maintenance pages, SEO, DNS, or migration, read and follow [references/websites.md](references/websites.md). It contains the complete website policy and should not be replaced by a shortened summary from this file.

## Mobile App questions

For every question involving Manus-built mobile apps, AppDev projects, local APKs, App Store or Google Play releases, APK/AAB/IPA builds, Expo/EAS, App backends, or mobile App restoration, read and follow [references/mobile-apps.md](references/mobile-apps.md). It contains the complete mobile App policy and should not be replaced by a shortened summary from this file.

## Timeline

| Event | Time |
|---|---|
| Backup deadline | August 23, 2026 at 7:59 a.m. SGT |
| Deletion and service-unavailable period | August 23 at 8:00 a.m. through August 25 at 7:59 a.m. SGT |
| Restoration opens | August 25, 2026 at 8:00 a.m. SGT |

Official Help Center guidance states that affected users can continue using Manus normally during the backup period, until access closes at 7:59 a.m. SGT on August 23.

## Determine the impact

- **Unaffected account:** Nothing changes. The account, subscription, tasks, connectors, and services continue operating normally. No action is required.
- **Affected or unsure:** Tell the user to check their in-app notice and email. Apple ID or Facebook-only users should check in-app notifications because Manus may not have their email address.
- **Type A/B:** The account remains, but tasks generated or updated on or after the cutoff, their generated artifacts, and enabled connectors are deleted. The user must restore a Task Data Backup.
- **Type C:** The account and associated data are fully deleted. The user must restore the Account Info Backup before restoring Task Data.

The user's official notification controls the exact deletion scope. Refer detailed account, subscription, team, and refund questions to [What’s Happening and Am I Affected?](https://help.manus.im/en/articles/16147831-service-change-overview-what-s-happening-and-am-i-affected).

## Backup

Affected users must complete the required backup before August 23 at 7:59 a.m. SGT using the [Data Backup Tool](https://manus.im/backup).

- All affected users need a Task Data Backup for the selected tasks and Manus-generated artifacts they want to preserve.
- Emphasize that **every export is a fixed point-in-time snapshot**. It does not update or sync after it is created.
- For a website or mobile App with live users, recommend regular Task Data exports during the backup window and a final fresh export before the deadline. New registrations, orders, uploads, content, and other database activity after an export are not contained in that snapshot.
- For the broadest updated snapshot, use **Export task data → Export more → All tasks → All time → Start export**. For a website-only snapshot, use **Custom export → Website tasks → All time → Start export**; Base data is included automatically.
- Type C users must create the Account Info Backup first, followed by the Task Data Backup. Type A/B users do not need an Account Info Backup because their account remains.
- Task Data is not backed up automatically.
- Team data can only be backed up by the team owner. Personal and team workspaces require separate backups.
- Confirm that every backup package exists in the chosen destination. Do not modify or rename the packages. Multiple complete export sets may be restored together, but do not substitute split parts from one export for parts from another.

For export options, package handling, Facebook-login requirements, team cases, and troubleshooting, use [How to Back Up Your Data](https://help.manus.im/en/articles/16147892-service-change-overview-how-to-back-up-your-data).

## Restoration

Restoration opens August 25 at 8:00 a.m. SGT.

- Type A/B users log in and restore their Task Data Backup.
- Type C users restore their account first, log in, and then restore Task Data.
- Team data can only be restored by the team owner.
- Restoration can only be completed once. Users should confirm that they have all correct and current backup packages before proceeding.
- Multiple packages can be uploaded together; Manus deduplicates and consolidates them.
- Restored third-party connectors must be manually re-enabled.

For the complete sequence and account-matching requirements, use [How to Restore Your Data](https://help.manus.im/en/articles/16147895-service-change-overview-how-to-restore-your-data).

## Official sources

- [A Note to Our Users](https://manus.im/blog/a-note-to-our-users)
- [Data Back Up and Restoration collection](https://help.manus.im/en/collections/19704025-data-back-up-and-restoration)
- [What’s Happening and Am I Affected?](https://help.manus.im/en/articles/16147831-service-change-overview-what-s-happening-and-am-i-affected)
- [How to Back Up Your Data](https://help.manus.im/en/articles/16147892-service-change-overview-how-to-back-up-your-data)
- [How to Restore Your Data](https://help.manus.im/en/articles/16147895-service-change-overview-how-to-restore-your-data)
- [Welcome Back Bonus for Affected Users](https://help.manus.im/en/articles/16147914-service-change-overview-welcome-back-bonus-for-affected-users)
- [Data Backup Tool](https://manus.im/backup)
- Support: support@manus.im
