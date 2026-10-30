---
name: local-web-search
description: Use before web search or follow-up page access from the user's machine or local workspace through a browser, CLI, script, or local client, including a fallback from cloud search. Also classify an uncertain execution location before that access. Confirmed cloud-hosted search and unrelated web app actions stay outside.
---

# Local Web Search

Keep local research requests relevant, avoid adding machine information, and
stop automated access when a site challenges or limits it. These constraints
cannot guarantee that Cloudflare or another service will not classify a
request as automated.

Defaults you may adapt, saying so: query wording and report layout. Every other rule here and in the references this skill loads binds.

## Select The Execution Boundary

Before the first request, use available tool documentation and host context to
identify where the request will originate. A tool invoked from a local chat is
not necessarily a local network client. Do not probe a website, enumerate
machine identifiers, or inspect secrets to make this decision.

- Confirmed local browser, CLI, script, or HTTP client: read
  `references/local-browsing.md` before sending the request.
- Confirmed cloud-hosted search or retrieval: return to the host's normal
  workflow. Reassess if a later step uses a local client.
- Execution location still unknown: read `references/local-browsing.md` and
  apply its constraints to the proposed access without claiming it is local.

## Scope

Apply the reference throughout this research task's local searches, selected
result pages, and relevant follow-up links. A switch of tools does not erase a
site's blocked state.

This skill does not authorize new disclosures, account actions, installation,
or changes to browser or network settings. Keep any other applicable owner and
host restrictions. Do not load it merely because a task mentions browsers,
Cloudflare, or bot detection, or asks to edit this skill.

## Report

Report the useful research result and any access limitation. Describe only
observed outcomes; neither these instructions nor a successful page load prove
that future requests will avoid bot detection.
