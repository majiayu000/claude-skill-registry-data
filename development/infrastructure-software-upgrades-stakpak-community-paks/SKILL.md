---
name: infrastructure-software-upgrades
description: Generic guidelines on how to perform infrastructure component upgrades in a reliable way
license: MIT
tags:
  - upgrades
  - maintenance
  - devops
  - operations
metadata:
  author: Stakpak <team@stakpak.dev>
  version: "1.0.2"
---

When upgrading infrastructure components like Kubernetes Cluster, Jenkins, Kubernetes Operators, Databases, always consider the following:

1) Find the current version of the component you want to upgrade

2) Research online the new available versions of this component, preferring stable versions in production unless you want to test newer unstable versions of the software or need to for other reasons the nightly/unstable version installed -> this depends on why the user wants to do the upgrade in the first place\
3) Once you know the target version, perform comprehensive research on all the change logs of all the versions between the current version and the target version, you must check each version in the upgrade sequence for breaking changes, this is crucial to make sure you did not miss any important stps\
4) Identify any potential breaking changes, dependencies, and specific steps or tools required while performing the upgrade

5) Always try to perform upgrades in a non-destructive and reversible manner, so take backups or perform rolling deployments when necessary to avoid downtime, unless the user wants to do a YOLO upgrade, in this case keep aside a plan for rollback

6) Write down the upgrade plan in a markdown file for future reference or for approval when needed

7) Once you get confirmation or approval on the plan, proceed with the execution, keeping in mind that you might need to revisit it and update as you hit unexpected issues during the upgrade

8) After you're done, you MUST test that the component and it's dependencies are functioning properly, check health checks and functionality if possible (you're are not truly done until you do this)
