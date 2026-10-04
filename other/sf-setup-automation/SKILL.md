---
name: sf-setup-automation
description: Configure Salesforce Setup from a session when the Metadata API has no route for it - decide deploy vs scratch-org definition vs browser, gate the decision on the org's own describeMetadata, hand a headless browser one single-use authenticated session without leaking a frontdoor URL, drive Setup from the accessibility tree, and prove the change with SetupAuditTrail. Use for org preferences and feature switches with no metadata type, never for configuration a deploy can carry.
---

# Salesforce Setup automation

## When to use

- A setting has to change in an org and you are not sure whether the Metadata API covers it.
- An org preference or feature switch has no metadata type at all, so no deploy can carry it.
- A deploy failed because a feature it depends on is not enabled in the target org.
- You need evidence that a Setup change happened, not a screenshot that looks convincing.
- Not for anything with a metadata type - that is `sf-deployment-strategies` plus `/vf-deploy`.
- Not for scratch org shape, which belongs in a definition file: `sf-scratch-orgs-sandboxes`.

## Where a configuration change belongs

Work down the table. Only the last two rows involve a browser.

| The change | Route | Why |
| --- | --- | --- |
| Object, field, layout, flow, permission set, profile, settings area with a `Settings` type | `sf project retrieve start` → edit → `/vf-deploy` | Versioned, reviewable, repeatable in every org |
| A feature a scratch org needs | `features` in `config/*-scratch-def.json` | The org is created with it; no click survives a recreate |
| An org preference exposed as a `Settings` member (`Case.settings-meta.xml`) | Deploy the `Settings` component | The guide: "Settings can be accessed using the specific component member or via wildcard" |
| A preference with no metadata type, org-specific and one-off | `/vf-setup` browser hand-off, then `SetupAuditTrail` | Nothing else can do it; make it auditable |
| A feature only Salesforce Support can enable | A case with Salesforce | Not in the API and not in Setup |

The Metadata API Developer Guide does not publish the unsupported-type list; it names the
[Metadata Coverage Report](https://developer.salesforce.com/docs/metadata-coverage) as "the ultimate
source of truth for metadata coverage". Do not keep a private list either - ask the org.

## 1. Ask the org what it can deploy

`sf org list metadata-types` returns `DescribeMetadataResult` for that org and API version:
"Display details about the metadata types that are enabled for your org." `metadataObjects[].xmlName`
plus `childXmlNames` is the authoritative set.

```bash
node "$CLAUDE_PLUGIN_ROOT/scripts/vf-setup.js" check flows --target-org acme-dev
# verdict: deploy -> exit 1, with the retrieve/deploy commands in the output
node "$CLAUDE_PLUGIN_ROOT/scripts/vf-setup.js" check --path lightning/setup/CompanyProfileInfo/home -o acme-dev
# verdict: unknown -> say what you are changing, then check the Coverage Report
```

The verdict lands in `.vibeforce/state/setup-gate.json`, which the MCP guard reads: a browser
navigation to a `lightning/setup/` URL with no gate record is annotated on every call.

Requires `Modify All Data` or `Modify Metadata Through Metadata API Functions` on the connected user.

## 2. Hand the browser a session, not a credential

`sf org open --url-only` mints a **single-use** frontdoor URI through the UI Bridge endpoint
`/services/oauth2/singleaccess` and prints, verbatim: "This command will expose sensitive information
that allows for subsequent activity using your current authenticated session. Sharing this
information is equivalent to logging someone in under the current credential."

A tool argument is transcript, so that URL must never be one. `vf-setup serve` keeps it in process
memory and hands out a loopback ticket instead:

```bash
node "$CLAUDE_PLUGIN_ROOT/scripts/vf-setup.js" serve setup-home --target-org acme-dev --ttl 180 --json
# {"handoff":"http://127.0.0.1:53137/vf-setup/54f6...","destination":"lightning/setup/SetupOneHome/home",...}
```

| Property | Enforced by |
| --- | --- |
| Binds 127.0.0.1 only, non-loopback `Host` gets 421 | `handoffRefusal` in `scripts/lib/setup-session.js` |
| 48 hex token, length-independent compare | `tokenMatches` |
| Serves exactly one redirect, then the server closes | `consumed` flag, 410 afterwards |
| Expires on `--ttl` (10-900 s, default 120) | 410, and the tool exits 1 so nobody thinks it worked |
| Frontdoor URL only ever printed redacted | `redactUrl` |

Two things that look like alternatives and are not, both checked against `@playwright/mcp` 0.0.80:
a local launcher file (`Access to "file:" protocol is blocked` unless
`--allow-unrestricted-file-access`, which also lifts the workspace-root restriction on file reads),
and `--secrets` (resolved only by `browser_fill_form` for `textbox` and `slider` values).

## 3. Drive Setup from the accessibility tree

```text
browser_navigate  <handoff>        # redirects once, lands on the Setup page already logged in
browser_snapshot                   # refs come from here; screenshots are evidence, not input
browser_fill_form / browser_click  # one change at a time
browser_snapshot                   # re-read: Lightning re-renders and invalidates refs
browser_take_screenshot            # the saved state
browser_close
```

Rules that matter more in Lightning than anywhere else: wait on a condition, never on a timer;
re-snapshot after every action that navigates or saves; treat a stale ref as a re-render, not a bug.
Classic Setup pages sit in an iframe and appear in the snapshot as a frame - refs resolve inside it.
Tables and long forms: `references/browser-loop.md`.

## 4. Prove it, or it did not happen

`SetupAuditTrail` "[r]epresents changes you or other admins made in your org's Setup area for at
least the last 180 days", API 15.0+, `query()` and `retrieve()` only, no aggregate on `count(Id)`.

```bash
node "$CLAUDE_PLUGIN_ROOT/scripts/vf-setup.js" audit --target-org acme-dev --since 30m
```

`Action` is the category (`PermSetCreate`), `Display` the sentence ("Created permission set ..."),
`Section` the Setup area ("Manage Users"). Exit 1 means the org recorded nothing: the click did not
take. More queries, including how to diff a setting before and after:
`references/verification-recipes.md`.

## 5. Make the next time a deploy

After the change, try to retrieve it. If anything comes back, commit it and the next org gets it from
a deploy. If nothing does, write the destination into `.vibeforce/config.json` so the path is a fact
next time rather than a search:

```json
{ "setup": { "destinations": {
  "einstein-activation": { "path": "lightning/setup/EinsteinSetup/home", "metadata": [], "summary": "Einstein activation toggle" }
} } }
```

Paths come out of the address bar of a real org, not out of a guess. `vf-setup list` ships only paths
verified in an official artefact, and says where each one came from.

## Anti-patterns

| Anti-pattern | Why it hurts | Instead |
| --- | --- | --- |
| `browser_navigate` with the frontdoor URL from `sf org open --url-only` | Writes a live admin session into the transcript; the `browser-credential-url` guard denies it | `vf-setup serve`, then navigate the loopback ticket |
| Clicking a field, layout or flow change in Setup | Produces drift no branch contains and no deploy reproduces | `vf-setup check` first; it exits 1 and prints the retrieve/deploy path |
| `browser_evaluate` to flip the setting faster | Arbitrary script inside a logged-in admin session, and no auditable action | `browser_click` / `browser_fill_form`; the `browser-page-script` guard asks first |
| Driving production Setup because "it is only a preference" | Unversioned production change; the tool refuses and the guard denies | Sandbox, then deploy the metadata if a type exists |
| Reporting success from the screenshot | Lightning renders a saved-looking page on validation failure | `vf-setup audit --since 30m` |
| Keeping a hardcoded list of "unsupported" types | Goes stale every release | `vf-setup check`, which asks the org |
| Reusing a hand-off URL for a second page | Frontdoor URLs are single-use; the second request gets 410 | One `serve` per navigation |

## Verification

```bash
node "$CLAUDE_PLUGIN_ROOT/scripts/vf-setup.js" list
node "$CLAUDE_PLUGIN_ROOT/scripts/vf-setup.js" check <dest> --target-org <alias>   # 0 browser/unknown, 1 deploy
node "$CLAUDE_PLUGIN_ROOT/scripts/vf-setup.js" serve <dest> --target-org <alias>   # 0 consumed, 1 unused
node "$CLAUDE_PLUGIN_ROOT/scripts/vf-setup.js" audit --target-org <alias> --since 30m
node --test tests/setup.test.mjs                                                   # gate, hand-off and guard rules
```

Guard behaviour without a session:

```bash
echo '{"hook_event_name":"PreToolUse","tool_name":"mcp__playwright__browser_navigate",
       "tool_input":{"url":"https://acme.my.salesforce.com/secur/frontdoor.jsp?sid=x"}}' \
  | node "$CLAUDE_PLUGIN_ROOT/scripts/hooks/pre-mcp-guard.js" | jq -r '.hookSpecificOutput.permissionDecision'
# -> deny
```

## References

- [references/browser-loop.md](references/browser-loop.md) - the Playwright MCP tool set, waiting
  rules for Lightning, iframes, forms, and what each guard rule does.
- [references/verification-recipes.md](references/verification-recipes.md) - `SetupAuditTrail`
  queries, retrieve-after-click patterns, state file shapes.
- Sibling skills: `sf-deployment-strategies` (the deploy route), `sf-scratch-orgs-sandboxes`
  (`features` and `settings` in a definition file), `sf-security-model` (permission sets and
  profiles, which are always a deploy), `sf-ui-test-automation` (browser tests, not configuration).
- Metadata Coverage Report: <https://developer.salesforce.com/docs/metadata-coverage>
- `sf org list metadata-types`: <https://github.com/salesforcecli/plugin-org/blob/main/messages/metadata-types.md>
- `sf org open` and its security warning: <https://github.com/salesforcecli/plugin-org/blob/main/messages/messages.md>
- Single-use frontdoor: <https://help.salesforce.com/s/articleView?id=xcloud.frontdoor_singleaccess.htm>
- `SetupAuditTrail`: <https://developer.salesforce.com/docs/atlas.en-us.object_reference.meta/object_reference/sforce_api_objects_setupaudittrail.htm>
