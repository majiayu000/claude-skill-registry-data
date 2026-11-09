---
name: feature-doc
description: Write or refresh a visual feature document from a codebase. Use when the user says "document this feature", "draw the component tree", "how does this page work", "update the feature doc", or when handing over a feature. Produces Mermaid diagrams for the page map, component tree and data flow, a files table, flags, tests, and open follow-ups. Read-only on the codebase, writes only the feature doc.
argument-hint: "<feature name or route>"
allowed-tools: Read, Grep, Glob, Write, Edit, Bash(git:*), Bash(gh:*), Bash(glab:*), Bash(jq:*), Bash(ls:*), Bash(find:*), Bash(rg:*)
---

# Feature doc

Feature: the one the user named. Template: [feature-doc.md](../../../templates/feature-doc.md). Output: the path the user names, for example a `features/` or `docs/features/` folder in their notes checkout. Ask for the path once if you do not know it. The codebase being documented stays read-only. Diagrams are Mermaid fenced blocks so they render on GitHub, GitLab and in most editors.

## Steps

Load [git-workflow](../git-workflow/SKILL.md) for read-only revision and history inspection. Documentation work does not authorize checkout, commits or history changes in the source repository.

1. **Entry point.** Find the route, the controller or page that mounts the UI, and the file that initialises it. Say how a request travels from URL to first render.
2. **Component tree.** From the root component, follow imports two or three levels. Record data flowing down and events flowing up. Note shared UI components used.
3. **Data.** List every query, mutation, subscription or API call the feature makes. For each, name the handler or endpoint on the other side and the model behind it. Note cache policies and optimistic updates.
4. **Flags and permissions.** Feature flags, permission checks, entitlement or licence gates. Say what changes when each is off.
5. **Tests.** Unit, integration and end-to-end specs. Say what each layer covers and what nothing covers.
6. **History and open items.** `git log --oneline -- <dir> | head -30` for the change trail. Search the forge for open issues naming the feature. Link the tracking item.
7. **Draw.** Page map (`flowchart LR`), component tree (`flowchart TD`), data flow (`sequenceDiagram` from user action to data store and back). Keep each diagram under 25 nodes; split otherwise.

## Rules

- Every file path must exist; run `ls` on it. Mark anything unverified with "(verify)".
- Plain English, no em dashes (see the `plain-voice` skill). One idea per sentence.
- Do not paste large code. Quote at most five lines when a detail matters.
- Public sources only: file paths in the repository, public issues and pull requests, official docs. Nothing from private discussions.
- Add a "Last verified against `<branch>` `<sha>` on `<date>`" line at the top.
- Update the index of the folder the doc lives in.
- Distinguish implemented behavior from a proposal. For a released-product document, verify against the named release, not an unrelated development branch. Record which walkthroughs were run, which paths were only inspected and what remains unverified; never imply the quickstart was tested when it was only read.
