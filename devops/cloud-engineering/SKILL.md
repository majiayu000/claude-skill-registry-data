---
name: cloud-engineering
description: "Cloud and infrastructure knowledge for design, review, non-mutating validation and troubleshooting across Azure, AWS and Google Cloud, with Terraform, Bicep, Docker and Kubernetes. Reads cloud.providers and cloud.iac from the project profile and opens only the matching references. Never runs a live-changing command; writes it out for the user to run. Use when: user says /cloud-engineering, asks to design, review, validate or debug cloud infrastructure or infrastructure-as-code, or when a task touches the paths in cloud.roots."
user_invocable: true
---

# /cloud-engineering — Cloud and Infrastructure Knowledge

## Scope rule (read first)

This skill does design, review, validation and troubleshooting. Validation uses non-mutating commands only.

It never runs a deploy, apply, create, update or destroy command against a live environment. It writes the command out for the user to run, inside a block labelled "for the user to run".

The user's normal Claude Code permission prompts and the existing destructive-operation guards apply to those commands unchanged. This skill writes no settings file and runs no permission check.

## Step 1 — Read the profile

Read two slots with the profile reader, as the other skills do:

- `cloud.providers` — one or more of `azure`, `aws`, `gcp`.
- `cloud.iac` — zero or more of `terraform`, `bicep`, `docker`, `kubernetes`.

The slots `cloud.roots` and `cloud.mcp-server` are optional. `cloud.roots` names where infrastructure source lives. `cloud.mcp-server` is a deferred slot and nothing here calls it.

A placeholder value or `none` reads as unset.

**If `cloud.providers` is unset, stop and print exactly one line:** `Cloud engineering is off: set cloud.providers in the project profile (azure, aws or gcp) to turn it on.`

Provider choice comes only from the profile. It never comes from where an MCP server runs, from a connected account, or from the names of files you happen to see.

## Step 2 — Open only the matching references

Always open `references/cross-cutting.md` first. It holds the provider-neutral rules.

Then open one file for each provider and tool the profile names, and no others:

| Profile value | Reference |
|---|---|
| `azure` | `references/azure.md` |
| `aws` | `references/aws.md` |
| `gcp` | `references/gcp.md` |
| `terraform` | `references/terraform.md` |
| `bicep` | `references/bicep.md` |
| `docker` | `references/docker.md` |
| `kubernetes` | `references/kubernetes.md` |

If a task needs a provider the profile does not name, say so and ask the user to add it to the profile. Do not open that reference.

## Step 3 — Work in one of four modes

1. **Design.** Apply the rule in each cross-cutting topic, then map it to the services in the provider file.
2. **Review.** Check existing infrastructure code against the same rules. Report each gap with the file and line.
3. **Validate.** Pick non-mutating commands from the provider and tool files. They are written as ready `contractLanding.verification.steps` entries for `.claude/work-item-conventions.json`. The project adds the ones it wants; this skill only documents them.
4. **Troubleshoot.** Follow the troubleshooting order in `cross-cutting.md`. Use read-only commands to gather facts before proposing a cause.

## Step 4 — Hand off live changes

When the work needs a live change, write the command in a block with this label directly above it:

**For the user to run**

Then add one line saying what the command changes and how to undo it. Stop there. Do not run the command, and do not ask for a way around the permission prompts.

## What this skill does not do

- It does not store credentials, tokens or keys in any file it writes.
- It does not read secret values; it checks that secrets are referenced from a secret store.
- It does not call a cloud-management MCP server. That adapter is deferred.
