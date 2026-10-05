---
name: rulebase-setup
description: Use to get access to Rulebase and connect an AI client to it — signing up, finding your data region, installing the Rulebase MCP server in Claude Code, Claude Desktop or Cursor, and creating an API key for the REST API. Trigger for "connect Claude to Rulebase", "install the Rulebase MCP", "set up the Rulebase connector", "create a Rulebase API key", "how do I sign up for Rulebase", "Rulebase returns 401", "no token provided", or when Rulebase tools are missing from a session.
metadata:
  author: rulebase
  version: "1.0.0"
  archetype: product
---

# Set up Rulebase access

Gets a user from nothing to a working Rulebase connection: an account, the right
data region, an MCP connection for reading workspace data from an AI client, and
an API key for pushing data in over REST.

## The mistake this skill exists to prevent

**Rulebase has two credentials and they are not interchangeable.**

| | MCP server | REST API |
| --- | --- | --- |
| What it's for | An AI client reading workspace data | Pushing conversations and work items in |
| Credential | OAuth browser sign-in, per person | API key, org-wide |
| Identity | You, with your role and scope | The organization, unattributed |
| Where configured | Your MCP client config | Your integration's environment |

Putting the API key in an MCP client config does not work and never will — the MCP
server does not accept API keys. Going the other way, an OAuth session cannot sign
a REST call. Most "Rulebase auth is broken" reports are this crossed over.

The 401 body tells you which surface you actually reached:

- `{"error":"No token provided"}` — you hit the **MCP** server (`mcp.rulebase.co`)
- `{"error":"Unauthorized"}` — you hit the **REST API** (`api.rulebase.co` / `api2.rulebase.co`)

That single distinction resolves most setup confusion, because the hostnames are
similar enough to typo and neither error names the other.

## Step 0: get a workspace

Rulebase is not self-serve. There is no public sign-up form, and no way to create
an organization yourself.

- **No workspace yet** — start at [rulebase.co](https://rulebase.co) to request
  access. A Rulebase-provisioned organization is the prerequisite for everything
  below; do not send the user hunting for a sign-up page that does not exist.
- **Your company already uses Rulebase** — you need an invitation, not an account.
  An admin invites you from **Settings → People → Members**, choosing your role.
  You get an email with a join link and appear as **Pending** until you accept.
- **You are the admin doing the inviting** — you need an admin role or the manage-
  invitations permission. Roles are configured under **Settings → People → Roles**.

If SSO is configured for the organization, sign-in goes through the identity
provider and role assignment may be driven by IdP groups rather than by the invite
dialog. Ask before hand-assigning roles in that case.

## Step 1: find the data region

Everything else depends on this, and it is decided by which host you sign in at —
there is no region setting to read, and a user cannot move themselves between
regions.

| Surface | United States | European Union |
| --- | --- | --- |
| App | `https://app.rulebase.co` | `https://eu.app.rulebase.co` |
| MCP | `https://mcp.rulebase.co/mcp` | `https://eu.mcp.rulebase.co/mcp` |
| REST v1 | `https://api.rulebase.co` | `https://eu.api.rulebase.co` |
| REST v2 | `https://api2.rulebase.co` | `https://eu.api2.rulebase.co` |

Ask the user which URL they log in at and derive the rest from it. **The regions
are separate deployments with separate credential stores**: an API key issued in
the US does not authenticate against EU hosts, and a valid key sent to the wrong
region returns exactly the same `401 Unauthorized` as a mistyped one. Nothing in
the response hints that the host is the problem, which is why this is step 1 and
not a troubleshooting footnote.

## Step 2: connect the MCP server

The endpoint **must include the `/mcp` path**. The bare hostname is not an MCP
endpoint, and clients fail against it with an unhelpful transport error.

**Claude Code** — one command:

```bash
claude mcp add --transport http rulebase https://mcp.rulebase.co/mcp
```

Or in the MCP config file directly:

```json
{
  "mcpServers": {
    "rulebase": {
      "type": "http",
      "url": "https://mcp.rulebase.co/mcp"
    }
  }
}
```

Then authenticate. Claude Code prompts on first connection; if it does not, run
`/mcp` in an interactive session and authorize from there. Note that `/mcp` is an
interactive terminal command — if the current session cannot open that panel, tell
the user to run it from an interactive `claude` terminal rather than trying to
authorize programmatically.

**Claude Desktop** — remote servers are added as **custom connectors**:

1. **Settings → Connectors**, or [claude.ai/customize/connectors](https://claude.ai/customize/connectors)
2. **Add custom connector → Web**
3. Enter the MCP endpoint for the region from step 1
4. **Add**, then **Connect**, and sign in to Rulebase
5. In a chat, **+ → Connectors** and enable Rulebase

**Cursor** — same shape as Claude Code, in Cursor's MCP settings:

```json
{
  "mcpServers": {
    "rulebase": {
      "type": "http",
      "url": "https://mcp.rulebase.co/mcp"
    }
  }
}
```

Any client implementing remote MCP with OAuth works. The server publishes standard
discovery documents, so a compliant client needs no manual OAuth configuration:
`/.well-known/oauth-protected-resource` on the MCP host points at the authorization
server, which advertises PKCE (`S256`), authorization-code, refresh-token and
device-code grants, and dynamic client registration. If a client asks for a client
ID or secret, it is not using discovery — check for a remote/HTTP transport option
before entering anything by hand.

## Step 3: verify the MCP connection

Do this before any real work, and do it in this order:

1. **`get_current_organization`** — always first. It confirms both that auth
   succeeded and *which tenant you are in*. State the organization name back to the
   user. Every subsequent query is scoped to it, and operating against the wrong
   workspace is the expensive mistake here.
2. **`get_workspace_schema`** — the authoritative list of queryable entities and
   fields for this workspace. Build queries from what it returns, never from field
   names remembered from another workspace or from a document.

If tools are absent from the session entirely, the client is not connected — go
back to step 2 rather than assuming a permissions problem.

**One symptom worth recognising:** if organization-scoped tools work but
member-identity tools (for example those reading your coaching sessions or saved
chat history) fail with a message that the authenticated organization is not
available in the workspace, that is a membership-resolution problem on the account,
not a client misconfiguration. Reinstalling the connector will not fix it. Report
which tools work and which do not, and route the user to Rulebase support.

## Step 4: create an API key

Only needed if something is pushing data **into** Rulebase — conversations from a
helpdesk with no native connection, or back-office work items from an internal
tool. Reading via MCP needs no key.

1. Go to **Settings → Connections** (`/settings/connections` on your region's app
   host).
2. Open the **API keys** tab.
3. Click **Create API key**. There are no options to fill in; the key is generated
   on click, works immediately, and never expires on its own.
4. Copy it from the **API key created** dialog.
5. Paste it into a secrets manager or your deployment platform's environment
   variables, then click **Done**.

**The dialog is the only place the full key is ever shown.** There is no reveal
action on the list afterwards. The list shows the first 16 characters, which is
enough to identify a key for revocation and not enough to authenticate. Production
keys are prefixed `rk_live_`.

If **Create API key** is greyed out, the account lacks permission to manage
integrations.

### What a key carries

Understand this before deciding how many to create:

- **Organization-wide.** It authenticates as the organization, not as the person
  who created it. Requests are not attributed to that person and are not limited by
  their role.
- **No scopes.** No read-only keys, no per-endpoint permissions, no IP allowlists.
  Every key reaches every endpoint that accepts key auth.
- **Region-bound.** Each region has its own key store.
- **No expiry.** Valid until someone deletes it.

Treat it as a shared production credential. One key per integration costs nothing
and lets you retire one system later without breaking the others.

Revoking is a delete — **there is no disable-and-re-enable, and it takes effect
immediately**. To rotate rather than retire, create and deploy the replacement
first, then delete the old key.

## Step 5: verify the key

Authenticate with `Authorization: Bearer <key>`. Listing conversation uploads is
the right first call because it only reads:

```bash
curl "https://api2.rulebase.co/conversation_uploads?limit=1" \
  -H "Authorization: Bearer $RULEBASE_API_KEY"
```

A working key returns `200` with an envelope even on an organization that has
uploaded nothing:

```json
{ "data": [], "meta": { "page": { "next": null, "limit": 1 } } }
```

Or run the checker, which tests the region, both API versions, and MCP
reachability in one pass and prints a JSON summary:

```bash
export RULEBASE_API_KEY=...        # never pass the key as an argument
node scripts/verify-access.mjs --region us
```

It reads the key from the environment only. Passing a credential as a CLI argument
puts it in shell history, `ps` output, and this transcript.

## Troubleshooting

| Symptom | Cause | Fix |
| --- | --- | --- |
| `{"error":"Unauthorized"}` from REST | Wrong region host, malformed header, or revoked key | Check the `eu.` prefix first — it is invisible in the response. Then the header (`Bearer`, one space, key, **no trailing newline** from a shell variable). Then match the key's first 16 chars against the list in Settings → Connections. |
| `{"error":"No token provided"}` | You reached the MCP server, not the REST API | You are using the wrong hostname for what you are doing, or an MCP client has not completed OAuth. |
| MCP client reports a transport error | Endpoint missing the `/mcp` path | Append `/mcp`. |
| MCP tools absent from the session | Client not connected or not authorized | Re-add the server; authorize via `/mcp` in an interactive session. |
| MCP connects, all data is empty | Connected to the wrong tenant | `get_current_organization` and confirm the name with the user. |
| Org tools work, member tools fail | Membership not resolvable for the account | Not a client problem. Route to Rulebase support with the tool names. |
| Key works for one API version, not the other | Almost never the key | The same key authenticates v1 and v2. Re-check the host: v1 is `api.`, v2 is `api2.`. |
| `Create API key` greyed out | Missing manage-integrations permission | Ask an admin. |

## Guardrails

- **Never print an API key into chat, a log, a commit, or a transcript.** If a key
  has already been pasted into a conversation, say plainly that it must be treated
  as leaked, and walk the user through creating a replacement and deleting the old
  one.
- **Never accept a key as a command-line argument** in anything you write.
- **Confirm the tenant before acting.** `get_current_organization` first, name it
  back to the user.
- **Do not create or delete API keys on the user's behalf** through the UI or API.
  Walk them through it; the key must land in their secret store, not in your
  context.
- **Reading is safe; writing is not.** MCP exposes write tools in some workspaces.
  Do not create, update or delete workspace records while setting up access.

## Present results to the user

1. **Region**, and the app host it was derived from.
2. **Organization name**, from `get_current_organization`.
3. **What is connected** — MCP yes/no, API key verified yes/no. Say which surfaces
   you actually tested rather than implying both.
4. **What is not set up yet**, and whether they need it. Most read-only users never
   need an API key; say so instead of walking them through one.
5. **Anything blocked on a permission or an invite**, naming who can unblock it.
