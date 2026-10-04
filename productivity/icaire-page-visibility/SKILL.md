---
name: icaire-page-visibility
description: Change or inspect ICAIRE remote-brain page visibility for public sharing. Use when the user asks to make an ICAIRE page public, unpublish it, make it internal/private again, check whether it is public, get a public link, or manage explicit page publication state in ICAIRE Cortex.
---

# ICAIRE Page Visibility

Use this skill to inspect or change one ICAIRE remote-brain page's public
visibility. Treat publication as an explicit ICAIRE Cortex action, not a normal
page edit.

## Contract

- Use ICAIRE Cortex MCP or the ICAIRE dashboard, not BigBrain personal-brain
  tooling.
- Resolve exactly one ICAIRE page before changing visibility.
- Read current visibility before writing whenever the capability exists.
- Prefer dedicated visibility tools or endpoints over generic page update.
- Keep internal material private unless the user clearly asks to publish the
  specific page.
- Keep raw files private unless the user explicitly asks to publish a specific
  artifact and the connector supports `public_raw_files`.
- Stop cleanly if ICAIRE does not currently expose a dedicated visibility
  capability in the active connector.
- Report the final visibility and public URL when one exists.

## Workflow

1. Confirm the intended action:
   - `public` for publish, share publicly, make public, or get a public link
   - `internal` for unpublish, make private, revoke access, or make internal
   - inspect only when the user asks whether a page is public
2. Resolve the target page:
   - use an explicit slug/path when provided
   - otherwise search/list/read ICAIRE pages through `mcp__icaire`
   - ask the user to choose if more than one page could match
3. Discover ICAIRE visibility capabilities before concluding they are missing:
   - search for `mcp__icaire.get_page_visibility`
   - search for `mcp__icaire.set_page_visibility`
   - search for `mcp__icaire.page_visibility`
   - search for ICAIRE dashboard or API tools that mention page visibility,
     public pages, publication, or `/public/<slug>`
4. If a dedicated visibility read tool exists, call it and record the current
   state.
5. If the user only asked to inspect, report the current visibility and public
   URL when available, then stop.
6. If the user asks to expose a PDF or other raw artifact:
   - verify the raw path exists with `list_raw_files` or `read_raw_file`
   - pass only the requested raw paths in `public_raw_files`
   - do not infer additional attachments from nearby files
7. If changing visibility, use the dedicated ICAIRE visibility write tool or
   dashboard mutation endpoint.
8. Verify the result by read-back, tool result, or public URL check when
   available.
9. Report the page slug/title, previous visibility when known, final visibility,
   and public URL when public.

## If Visibility Tools Are Missing

If the active ICAIRE connector only exposes generic `read`, `create_page`, or
`update_page`, do not emulate publication by editing page frontmatter. Say that
the ICAIRE connector does not currently expose a dedicated page-visibility
capability in this session, and list the exact capability needed:

```text
mcp__icaire.get_page_visibility
mcp__icaire.set_page_visibility
```

Offer to create or update the ICAIRE platform task/implementation plan only if
the user wants that follow-up.

## Guardrails

- Do not use personal BigBrain tools for ICAIRE pages.
- Do not route personal, commercial, or advisory material into ICAIRE unless the
  user explicitly says it belongs there.
- Do not publish from an ambiguous request such as "share this" until the exact
  ICAIRE page and desired public visibility are clear.
- Do not infer page identity from memory when live ICAIRE search/read can verify
  it.
- Do not manually edit markdown frontmatter for visibility unless the user
  explicitly approves a recovery path and understands it bypasses the dedicated
  publication control.
- Do not publish linked pages, raw files, attachments, task timelines, or
  dashboard/search surfaces automatically. Raw files require an explicit
  user request and a verified `public_raw_files` result.
- Do not claim the page is public without a verified final state or public URL.

## Forward Test Prompts

- Should trigger: "Make the ICAIRE onboarding page public and give me the link."
- Should trigger: "Is `ops/icaire-brain-onboarding` public?"
- Should trigger: "Unpublish that ICAIRE page."
- Should not trigger by itself: "Export the ICAIRE onboarding page as a PDF."
- Should not trigger by itself: "Update the ICAIRE initiative summary."

## Output

For a successful publish:

```text
Published `ops/example` publicly: https://.../public/ops/example
Only the approved page content and explicitly listed raw files are public;
private linked pages and unlisted raw files remain private.
```

For a successful unpublish:

```text
Set `ops/example` back to internal. The previous public URL is no longer public.
```

For a missing capability:

```text
I found the ICAIRE page, but this connector does not currently expose a
dedicated page-visibility tool. I did not edit the page manually.
```
