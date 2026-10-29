---
name: connect-tools
description: Connect Claude to the services an app already uses (RevenueCat, PostHog, Sentry, Expo, Supabase, Stripe and others) through each vendor's official MCP server, so it can read real crashes, analytics, subscriptions and builds instead of guessing. Reads the project to see which services it uses, checks what is already connected, adds the missing ones with the right scope, and records them in the rules file. Use when the user says "connect RevenueCat", "add the PostHog MCP", "what MCP servers should I add", "can Claude see my crashes", during setup, or when a task needs data from a service that is not connected.
---

# Connect tools

Most of the services an app runs on now publish their own MCP server. Once one is
connected, Claude can look at the real thing (this week's crashes, a customer's
subscription, a funnel, a failed build) instead of asking the user to paste it.
This skill finds which ones the project needs and connects them.

The list of servers lives in `references/servers.md` (in this skill's folder,
`${CLAUDE_PLUGIN_ROOT}/skills/connect-tools/references/servers.md` when installed
as a plugin). Every entry there has the vendor's own docs link and a last checked
date. Use only what is in it, or what you find on the vendor's own docs today.

## 1. See what the project uses

Read, do not ask, where you can:

- `package.json` dependencies. The **Detect** column in `servers.md` lists the
  package names that point to each service (for example `react-native-purchases`
  means RevenueCat, `@sentry/react-native` means Sentry).
- `app.json` / `app.config.*` plugins, `eas.json`, a `server/` folder's
  `package.json`, and config files such as `supabase/`, `vercel.json`,
  `railway.json`, `firebase.json`.
- The rules file's stack section, if it has one.

Then list what you found in one short block, and ask once: "Anything else you use
that I missed?" A service with no code footprint (a design tool, a project tracker)
only shows up if the user says so.

## 2. See what is already connected

Run `claude mcp list`. It shows servers from every scope and from claude.ai
connectors (those appear as `claude.ai <Name>`). A service connected either way is
done; do not add it a second time, because duplicate servers give Claude two sets
of the same tools.

In an agent other than Claude Code, check that agent's own MCP settings instead.

## 3. Propose, then add

Show one table: service, already connected or not, what Claude could do with it
(one line from `servers.md`), and whether it can change things or only read.
Recommend; let the user drop any. Where the vendor publishes its own Claude Code
plugin (listed under "Vendor plugins" in `servers.md`), offer that as the
alternative: it adds the vendor's skills too. Never both. Then, for each one they keep:

1. **Open the vendor's setup page** from `servers.md` and confirm the address and
   sign in method are still what the entry says. If they differ, use the page and
   tell the user the entry needs updating (the fact-check skill can fix it).
2. **Pick the scope:**
   - **user** (`-s user`): the user's own accounts, used across all their apps.
     The default for sign in servers like Sentry, PostHog, Stripe, Expo.
   - **project** (`-s project`): writes `.mcp.json` in the repo so everyone who
     clones it gets the server. Only for servers that sign in through the browser,
     because `.mcp.json` is committed. Never put a key in it; if a server needs a
     key, reference an environment variable (`${REVENUECAT_API_KEY}`) and tell the
     user where to set it.
   - **local** (the default when no scope is given): this project, this machine,
     not committed. Use for servers that need a pasted key and are only for this app.
3. **Add it** with the command in `servers.md`. Sign in servers: run the command,
   then the user types `/mcp`, picks the server and signs in in the browser. Key
   servers: ask the user to create the key in the vendor's dashboard (give the exact
   screen from the vendor's docs, fetched today), and have them run the command
   themselves or set the environment variable, so the key never passes through the
   chat. Prefer a read only key whenever the vendor offers one.
4. **Prove it works.** Call one harmless read tool (list projects, list apps, the
   current user) and show the result in one line. A server that is listed but
   fails here is not connected; say so. Then check this app's own project is in
   what came back. A server signs in to one account, and people often have two
   (a second login, another organization). If the app's project is missing, it is
   connected to the wrong account: say so, and ask which account to sign in with
   before using it for this app.

New servers load at the start of a session. If the tools do not appear, the user
restarts Claude Code (or runs `/mcp` to reconnect) and you check again.

## 4. Record it

Add or update a **Connected tools** section in the rules file:

```
## Connected tools (MCP)
- Sentry: user scope, signed in 2026-10-17. Use it before guessing at a crash.
- RevenueCat: local scope, read only key, 2026-10-17. Customer lookups by app user id, not email.
```

One line each: the service, scope, read only or not, date, and one rule of thumb
for using it. Other skills check this section (reference-hunt looks for Mobbin
here). If a server was skipped on purpose, say so in one line so nobody re-proposes
it.

## Safety

- **Writes are real.** Servers that can deploy, refund, run SQL, delete or message
  people act on production. Before any call that changes something, say what it
  will change and wait for a yes, even if the session runs in auto mode. Prefer the
  read only mode or key where `servers.md` lists one, and scope database servers to
  one project.
- **Keys stay out of the repo and out of the chat.** Not in `.mcp.json`, not in
  the rules file, not in a commit. If a key was pasted into the chat, tell the user
  to rotate it.
- **Official servers only.** A community server runs code on the user's machine
  with their keys. Offer one only when the vendor has none, label it community, link
  its repo, and let the user decide.
- **Vendor names are not proof.** A server is official when the vendor's own docs
  link to it, not because its name matches.

## Finish

Show the final table (service, scope, read only or not, proved working or not) and
anything the user still has to do by hand (sign in through `/mcp`, set a variable,
restart).
