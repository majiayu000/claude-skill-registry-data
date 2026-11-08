---
name: watch-capability-discovery
description: Discover what the paired watch actually supports, what is installed, what OS permissions exist, and which authenticated device tools are ready.
---

# watch-capability-discovery

1. For questions such as "What can this watch do?" use the authenticated `watch.capabilities.list` tool *if it is actually registered*. This skill never creates such a tool.
2. Distinguish five different facts: hardware or OS `supported`, integration installed, OS `permission`, presently `available`, and data actually `observed`. A supported sensor does not establish permission or a fresh reading.
3. Attribute each item to `watch`, `phone` or `relay`. Do not credit the watch with a phone-sourced GPS fix. A phone connection is not an internet connection.
4. Refresh discovery after pairing changes, application updates, permission revocation or reconnect. Do not assume a previous "ready" result is still current.
5. If permission is needed, allow a real Android permission flow. Chat confirmation is not OS permission.
6. Mark unavailable or unknown capabilities honestly. Do not advertise calls, messages, health monitoring, reminders, location or device controls without a verified integration.
7. Action tools require a separate allowlist, structured parameters and enforced authorization beyond capability discovery.
8. Give a compact human summary instead of dumping the capability JSON.
