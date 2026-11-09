---
name: lumail
description: Manage Lumail email marketing from Claude with the Lumail CLI or MCP. Use for setup and login, sending domains and DNS, subscribers, tags, double opt-in, transactional emails (OTP codes), campaigns, workflows (automations), segments, API keys and analytics.
---

Connect first:

```bash
npx lumail@latest setup --authenticate   # installs the Lumail MCP + skills for your agent, opens the browser to authorize
npx lumail@latest auth test              # checks the saved login, fails: run the setup-lumail skill
```

The "copy the prompt" button in the Lumail onboarding does the same. Once connected, prefer the Lumail MCP tools and fall back to the CLI (`lumail --help`, then `lumail <resource> --help`). Never invent flags. Pass `--json` when parsing, and never print API keys.

Where each job lives:

- Count or find subscribers: MCP `count_subscribers`, `get_subscriber`; CLI `lumail subscribers list`, `lumail subscribers get <email>`.
- Add or update a subscriber with tags: MCP `add_subscriber`; CLI `lumail subscribers create --help`.
- Tags: MCP `list_tags`, `get_or_create_tags`; CLI `lumail tags list`, `lumail tags create`.
- API key for an app (OTP emails, signups): `lumail tokens --help`. Create it yourself and store it only in the app env.
- Transactional email (login code): MCP `send_email`; CLI `lumail emails --help`.
- Sending domain and web domain: `lumail domain --help`, then add the DNS records it returns in Cloudflare yourself.
- Anything else: `lumail tools list`, `lumail tools get <tool>`, `lumail tools run <tool> --params '<json>'`.

For signups from an app, upsert the person on signup or purchase with a tag per product (`student`, `customer`, `<product-slug>`), through one server helper so the API key never reaches the browser. Double opt-in is on by default and keeps a new subscriber "pending confirmation" until they click the email: keep it for cold forms, and create buyers and account signups as subscribed (skip double opt-in) so tag workflows fire right away.

Create campaigns and workflows as drafts; send, schedule or publish only when the user asks. Before writing a campaign body or a workflow graph, load the format guide with MCP `get_skill` and `{"type":"campaign"}` or `{"type":"workflow"}`. For a workflow, create it, read it back with `get_workflow`, then configure the full graph in one call (a trigger such as "tag added", then the email steps) with the exact `updatedAt` value. After any change, read back the saved object and render it to check content and links.

Reply in the user's language with what changed, a link, and anything left to do.
