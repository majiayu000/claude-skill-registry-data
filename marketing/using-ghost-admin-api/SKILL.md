---
name: Using Ghost Admin API
description: Comprehensive draft and post access, creating, editing and analysis. When Claude needs to work with the Ghost Admin API to access content published on alt-counsel.com as Houfu's partner.
---

# Using Ghost Admin API

## Overview 

The user may ask you to create, edit or analyses posts on Houfu's alt-counsel.com blog using Ghost Admin API. 
You have different tools and workflows available for different tasks. 

## Workflow decision tree

* If there is already a separate SKILL that is used to perform the workflow, STOP and use that skill instead.
   * Example, searching_the_blog or backlink_curating
* For posting a draft on Ghost platform, use [creating_a_draft.md](creating_a_draft.md)
* For checking published posts and syncing to repo (CHECK phase), fetch the post from Ghost API and update the local markdown file with any edits made in Ghost's editor

For all other workflows, read the [Ghost Admin API writeup](ghost-admin-api.md) to create an appropriate `curl` command to perform the task.

## Reference Documentation

* **[ghost-lexical-complete-guide.md](ghost-lexical-complete-guide.md)** - Comprehensive guide to Ghost's lexical format with real-world examples from actual blog posts. Use this when you need to understand or construct complex lexical structures.

## Reminders

* Always announce that you are using this skill.
* You need authentication to access Ghost Admin API. It can be found in the environment values or in a .env file. 
* Documentation is sparse from Ghost. Always report problems so that we can figure out together how to fix them and improve our instructions. 
