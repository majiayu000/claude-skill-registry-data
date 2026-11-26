---
name: vault
description: Read whenever someone mentions or pastes a key, token or password, before asking for one or using one, and before an app signs in to an outside service or uses an account there.
metadata:
  title: "Vault"
  subtitle: "Passwords and keys, kept safe"
  about: "Keeps your passwords, keys and sign-ins, and lets your apps and your AI use them without ever seeing them. You choose who may use each one."
  category: "Privacy & Security"
---

The Vault is the one place for everything a person has given access to: keys, passwords, sign-ins, accounts and
Chrome profiles, each an item, used without being seen. An item has fields (a secret one is never read back, by
anyone), the sites its secrets are sent to, the apps switched on for it, and whether agents may use it, and
can have contents too large for a field, kept sealed.

Never ask for a password, key or token in the chat, and never paste one. `request` gives the person a link to
their own device, where they pick or type it; `save_from_browser` saves one a website shows a browser of yours;
`fetch` makes a web request with an item they let agents use, and you never see the secret. If someone pastes one anyway, don't repeat it: in code mode, or over the web, ask for it
with `request`; only as a plain tool on a device (`one mcp`, `one vault set`) keep it with `set`.

- `security` says how ready the Vault is, first of all: `not_set_up` (no key yet), `no_server` (no server opens it,
  so it keeps nothing), `device_lacks_key` (it works, but this device doesn't hold the key, so can't show the
  recovery key; a browser or an assistant never can, so it's `ready` without) or `ready`; and the devices holding its person's key, those asking to, and the servers that open it.
- `list` shows what's there: each item's `kind` (`password`, `account` or `app_item`, an app's type), its fields, a
  secret one without its value, its websites (`hosts`), its `access` (`agents` and the apps switched on for it), its
  `status` and its `artifact`; every request kept, with its `state`; what was handed to commands in the last month
  (`handles`); the apps that use the Vault, by name and title; and the kinds of item they keep.
- `request` asks for an item by its `title` and the `fields` it needs, for an `app` or, with none, for you. A field
  that isn't secret (`secret: false`) may carry a `value` you know, as an account name or an endpoint: the person's
  sheet shows it filled in and they can change it, so they type only what you don't know. A `value` on a secret field
  is refused: an agent never handles a secret. For an app
  installed for the network or a group, the item is in that Vault, as the app finds it, one for everyone it serves,
  but for one of a type the app registers (Item types, below, by its name's prefix), which is the person's own, in
  their Vault, made as that type, as ClickUp's key is.
  Give the person the link it answers with: it opens Vault on their device, where it asks as an alert, "<you> wants
  to use a key", with Don't Allow and Allow, and waits under Requests too. A request moves once, from `waiting` to
  `allowed`, `declined` or, after a week, `expired`, which `list` says by its `id`. Allowing it gives whoever asked
  access to the item, and lets its secrets go to the request's `hosts` too; new values typed for it make a new item.
- `save_from_browser` is how a secret you set up on a website gets in, as a password manager's Save does: an
  OAuth client's secret, an API key, a key file. It takes it from a Chrome or Chrome Profiles `session` of yours,
  straight from the browser, so it never reaches you: from elements on the page (`fields`, each with its `target`,
  as `snapshot` gives it, or a selector), or from a file the browser downloaded (`download`, by its name, the whole
  file or a `json` value in it, such as `web.client_secret`), which is deleted once it's saved. Save it the moment
  it shows, before you snapshot or screenshot anything. Give the item's `hosts`, and `secret: false` for what may
  be shown, as a client_id. It makes a new item, or adds to one a save from a browser made, never another; its
  person is notified and sees "Added by an agent from <site>", and deletes it if they didn't want it. It answers each field's length and the
  first 8 hex of its SHA-256, to check against what the site says. Using it is still the person's to allow: an app
  that needs it, or `fetch`, still asks with `request`, which they answer with the item. It goes into the Vault of
  whoever the call is for, from your own browser: a group's or the network's with `ONE_SUBJECT=groups/<name>` or
  `network`. For another network's Vault, pipe a handle (below) into that network's `set`.
- `handle` gives a command one secret without you seeing it: a field of an item whose person switched on Commands
  for it, or what a browser of yours shows, taken as `save_from_browser` takes it. It's used once, within 5 minutes,
  by `one vault run --handle <it> [--env NAME] -- <command>` on a device of yours (on the command's input, or in
  NAME), or Remote Shell's `run` and Containers' `exec` (`secrets: {"NAME": "<handle>"}`), and what the command prints of
  it is `<concealed>`. Into another network's Vault: `one vault run --handle <it> -- ptc vault set --item <name>
  --field <field> --value-from /dev/stdin`. Run as the same owner it was made for (`ONE_SUBJECT`). Switching on
  Commands is its person's, as access is; `list` keeps each use, by item and handle, never the value.
- `fetch` fills `{{<field>}}` into a request's url, headers or body (escaped as JSON string text in a body whose
  `content-type` is JSON), for an item agents may use, and answers
  the status, headers and body. It goes only to one of the item's sites, and a secret the site says back is
  blotted out.
- `set` keeps one field of an item, making a password if there's none by that name. Say `secret: false` for what
  may be shown, as a username, and `hosts` for the sites a new item's secrets go to; adding sites to an item that's
  there is its person's, so ask with `request`, whose `hosts` they see as they allow it. The value is encrypted on the device you
  run on before it's sent, so `set` is for `one` or MCP on a device, as a plain tool. A script or `call` in code
  mode runs on a server, where nothing encrypts it, so a secret given there is refused: in code mode, and over the
  web, ask with `request` instead.
- `access` gives an app (`who`, by its name) access to an item, or with `on: false` takes it away. An app with
  access uses it through the Vault's tools without seeing it, or, one with a service, is handed the secret itself,
  which trusts its code with it. `who: "agents"` lets agents use it with `fetch`, and `who: "commands"` hand it to a command (`handle`). Giving access, to an app or to
  agents, is the person's alone, in the Vault on their device: an agent asks with `request` (with `app` for an
  app), and `access` refuses it. Taking access away is anyone's.
- The servers that open the Vault are those that act for whose it is, and they're handed its key only by its
  person's passkey, on the network's sign-in page (the skill `encryption` says how). No tool does it: a Vault no
  server opens keeps no secret, so tell the person to open Sign In & Security, where a server waiting for it says so.
- Someone's Vault is theirs alone: nobody asks for another user's, and the network's owner reads none. A group's
  or the network's is its members' to use (`ONE_SUBJECT=groups/family`), and its owners' to hand to its servers.
- Deleting an item is soft delete's, as for anything an app made: `soft-delete delete --artifact` with its
  `artifact`, as `list` gives it, and it can be restored for 30 days. `remove_field` takes one field out of an item.
- Deleting an item is a person's decision. Do it when asked to, and say what you did.
  Giving access, adding an item's sites and answering a request are theirs to do on their device, never yours.

An app uses an account through this app's tools, which act for the app that calls them (its `caller`),
and never sees a secret, so an untrusted app can use one too. It requires this app:

    def requires, do: %{"vault" => "to sign you in to GitHub"}

    @github %{
      "name" => "GitHub",
      "authorize" => "https://github.com/login/oauth/authorize",
      "token" => "https://github.com/login/oauth/access_token",
      "scopes" => ["repo"],
      "hosts" => ["api.github.com"],
      "client" => "GitHub client"
    }

    def call("sign_in", _inputs, call), do: OneCore.Call.tool(call, "vault", "sign_in", %{"service" => @github})

    def call("me", _inputs, call) do
      request = %{"item" => "GitHub", "url" => "https://api.github.com/user", "headers" => %{"authorization" => "Bearer {{access_token}}"}}
      OneCore.Call.tool(call, "vault", "fetch", request)["body"]
    end

- `sign_in_state` says how a sign-in is going, by the `state` of its link (`started`, `ok` with its `account`, `cancelled`, `failed` with its `problem`): the UI library's `ServiceSignIn` reads it, so a tool that starts one has a page that shows the link and follows it (`ui: "client/sign-in.html"`, its page `<ServiceSignIn url={…} />`).
- `sign_in` starts an OAuth sign-in and gives the link its person opens in their browser. The service sends
  them back to the network's address, and their tokens become the item named as the service is, or as `item`
  says, for a second account, switched on for the app. All the app says is the service's own: where it
  signs in (`authorize`), where it gives tokens (`token`), its `scopes`, the sites its tokens are sent to
  (`hosts`: the token address's site, names under it, such as gmail.googleapis.com under oauth2.googleapis.com's
  googleapis.com, or the client's sites), anything more its sign-in page is asked with (`params`), and `client`, the
  item that holds the `client_id` the service gave whoever registered the app with it, and its `client_secret` if it
  has one, which its person switched on for the app: an app signs in only with a client switched on for it. A person
  without one signs in with the network's, kept once in its Vault for everyone, switched on by an owner, whose secret
  only goes to the service. The
  client item keeps its sign-in page (`authorize`, not secret): the one its person gave it, or else the first an app
  it's switched on for names, so no other app sends its person anywhere else with it. The code goes only to that
  item's sites, its secret too: its person keeps the service's token address among them. An item that's there already is written only by signing in to the same service again, for an app
  that uses it. A network
  without an address has nowhere to be sent back to. An item's name that says `{{<claim>}}` is filled in from
  who signed in, as the service's OpenID Connect ID token says: `"Google {{email}}"`, with `openid` and `email`
  among the scopes, is an item for each account.
- `fetch`, called by an app, makes a web request with an item switched on for it, to one of the item's sites,
  with `{{<field>}}` filled in, and answers the whole of what the site said. It waits 15 seconds for an answer,
  or `timeout`. A signed-in item's `access_token` is renewed when it has ended, or when the service says it has.
- `items` lists the items switched on for the app, each with the service whose sign-in made it:
  `[{"name": "Google a@example.com", "sign_in": "Google", "artifact": "...", "state": null}]`. `state` says which
  of three states one is in (Item types, below), and `access` with `on: false` takes the app's own access to one
  away, as signing out does, leaving it to whatever else uses it. An app never gives itself access.
- The other tools are its person's, and refuse an app.
- An app that does something for other apps, as `google-account` does for the Google apps, calls these on
  behalf of whichever called it: `OneCore.Call.tool(call, "vault", "fetch", request, on_behalf_of: call.caller)`.

An app trusted with a secret itself, whose service hands it to a program, requires this app (`def requires, do:
%{"vault" => "to sign you in to GitHub"}`) and calls its functions, which run inside it on a server of its owner's:

- `value(call, item, field)` gives one field itself, to hand to a program a service brings. Hand it over on the
  program's input, and never answer with it, raise it or log it.
- `keep(call, item, fields)` keeps secrets the app made itself or an outside service handed it, such as the
  key a session it holds is encrypted with, in an item it makes, switched on for it. `remove(call, item)` removes
  one, as when that account is signed out. `items(call)` lists what's switched on for it.
- `value` raises unless the item is switched on for the app, which its person does in the Vault's app or
  with `access`, or which `keep` did. `values(call, item)` gives all its fields at once, and `rename(call, item, to)`
  renames it, its fields and contents with it.
- An item's contents are what's too large for a field, like a Chrome profile, kept as 1Password keeps a file: a
  blob of the Vault's, sealed under a key made for it alone, which only the item holds. `write_contents(call, item,
  name, send)` gives `send` a link that writes one blob and that key, for whatever holds the bytes to seal and send
  them a chunk at a time (Containers' `upload` does), and keeps them once it gives their size; what they replace goes
  then. `read_contents(call, item, name, receive)` gives `receive` a link that reads them and the key, for
  Containers' `download`, or gives `nil` where there are none yet. Neither ever passes the bytes through a tool's
  result, whatever their size. They're the item's, so deleting it deletes them, and restoring it brings them back.
- `state(call, item, state, message, action)` says which of the three states an item is in; `remove(call, item)`
  deletes one through soft delete.

## Item types

An app that keeps items in its people's Vaults says what kind they are, as Android's AccountManager has apps
define account types and keeps the accounts itself. An account (a Gmail address, a WhatsApp number) is one such item,
of a type its app registers, as a password or a Chrome profile is. It hooks into `vault.types`, answering with its
list of types:

    @impl true
    def hooks, do: ["vault.types"]

    @impl true
    def hook("vault.types", _about, _call),
      do: [%{name: "Chrome profile", section: "Chrome Profiles", prefix: "Chrome profile: ", component: "profile", create: %{tool: "create", name: true}}]

- `name` is one item of it, as a person reads it, and `prefix` what its items' names start with. An item the app
  makes (`keep`, or a sign-in) whose name starts with it is of that type, kept as its kind as it's made, and what
  follows is the item as a person reads it. One the app makes that's of no type of its is an account.
- `section` is the heading its items are listed under: its own (Chrome Profiles), or one several apps' types share
  (Accounts).
- `create` is how one is added: a `tool` of the app's, called as its person, or a `page` of its client's (the form
  that adds one); `name: true` asks its person for a name first, which the tool is given as `name`.
- `component` is what draws one item beside the list: a Solid component the app's client exports
  (`client/package.json`: `{"exports": {"./profile": "./profile.tsx"}}`), the module's default export, given `item`
  (the item as a person reads it), `subject` (whose Vault it is), and `open(item)` and `close()`, for once it's
  renamed or gone. Its `Summary` export, given the same, is the item's line in the list when it's ready. A trusted
  app's component is drawn in the Vault's page and acts with what the Vault may do. An untrusted app's item is
  drawn beside the list by its page `client/<component>.html` instead, with the item after a `#`, in a frame of the
  Vault's page (the UI library's `Frame`), its own JS in a sandbox of its own, where it keeps what its own app may
  do. Without a component, an item opens with its fields, as a password does.

An item is in one of three states, which the Vault shows and the app that keeps it says, with `state` (or `state/5`):
only that app, never another with access to it, and never for a password. The app keeps its own detailed states
(WhatsApp's linking, Chrome Profiles' update) and says only which of these it's in:

- `ready`: usable, which shows nothing: fine is silent. Every item starts there, and a password is always there.
- `busy`, with a `message` ("Saving…"): something's under way, shown as a spinner and it.
- `needs_action`, with a `message`, why ("Signed out on your phone"), and one `action`: its person has to act,
  shown as a dot, why and a button. The `action` is that button: a `label`, and a `tool` of the app with its `inputs`
  (`%{label: "Sign In", tool: "account", inputs: %{account: "+614..."}}`), which is all that's kept. A tool that is a
  screen (it says `ui`) opens that screen, at the link the Vault makes from the tool and its inputs each time it lists
  the item; any other is called as its person, and its `url`, if it gives one, opens in their browser.

Two things are each app's to choose, and none chooses for another: whether its person is notified when its item
needs them (`notifications`), and what it does when its item is deleted, restored or purged, which soft delete's hook
tells it (signing out and revoking at once, or keeping its token so a restore just works).

What the app keeps of an item, and the bytes in its contents, are the Vault's to keep and encrypt, and deleting,
restoring and purging an item are soft delete's; what an item means and does (a running browser, signed-in tools) are
the app's.
