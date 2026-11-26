---
name: sign-in
description: Read before inviting someone to a network or taking someone out, when a device or an assistant says it isn't in yet or shows a code, or to list or remove someone's devices, assistants and passkeys.
metadata:
  title: "Sign-In"
  subtitle: "People, devices and passkeys"
  about: "Invite people to your network, who sign in with a passkey or Google and no password. See and remove your devices and the AI assistants you let in."
  category: "Privacy & Security"
---

Sign-in is how people get into a network, and what acts as each of them: their devices, and the assistants they
let in. A person signs in with a passkey at the network's address, or with Google where its edge has a Google client. An assistant becomes theirs when they answer
that one question for it, and a new device when they also say the code it shows matches.

- `invite` makes a link someone joins by: they open it and make a passkey, or continue with Google, and are that
  user from then on. The
  network's owners invite, and whoever they made an editor of `network/own/sign-in`. The link works once, for a
  week, and a new one for them ends it, so pass on the newest. Whoever joins by it is that user, so only the network's
  owner invites someone who's already in, as a way back when they've lost every passkey, and never an owner: an owner
  adds a passkey on a device they're signed in on.
- `domains` says which Google Workspace domains' people join by signing in with Google, with no invitation, and
  sets them for whoever invites. They're `users/<their email's name before the @>`, and go by their Google name.
- `network` says the network's name, icon and logo, and sets them for whoever invites: null is the One App's. Its icon,
  on a tile of its own, is its web app's tab, Home Screen icon and manifest, and its own apps' icon; its logo, its mark
  alone, is what its sign-in page draws, one for a light page and one for a dark, either alone shown on both (`--name
  "the PTC App" --icon-from icon.b64 --logo-from logo/`, square PNGs as base64, `logo/` holding `light` and `dark`). A
  network's own app is finished with the same. Its `apple_app` and `android_package`, which `tooling/installers` sets as it publishes
  the network's installers, are trusted with its passkeys and links (`/.well-known/apple-app-site-association`,
  `/.well-known/assetlinks.json`).
- `devices` lists your devices, the assistants you let in and the browsers you're signed in on, and your
  passkeys. An app says whether it's `connected`, and if not when it was `last_seen`, as a browser does when it was last used: one not used for 30 days is signed out, and one that signs in again replaces its old session. An app run from a terminal says its `command` (`ptc`: the CLI). `remove_device` takes one out: it's nobody's from the next thing it asks. `remove_passkey` removes a
  passkey, but never your last. `add_passkey` lets your person make another passkey: whoever opens its link makes
  one of theirs, so the link goes only to their own screen, and you're given none. They're notified, and Sign-In &
  Security makes it there.
- A passkey with WebAuthn's PRF unlocks its person's key, and only it hands the key to their devices and servers
  (the encryption app's skill says how). `devices` says which do (`unlocks`). Whoever uses one has the key, so a
  device that holds it encrypts it to a passkey only once its person allows that passkey there, by name and when it
  was added, and the code the sign-in page showed them, in Sign In & Security: `encrypt_for_passkeys` with that
  `passkey` and `code`. Ask them first; never for a passkey they don't know they added. `unlock_with_passkey` makes
  the link where a passkey hands the key over: to a device that's asking for it (`device`), and to the servers
  waiting for it, the person's or a group's or the network's they own (`scope`). Sign In & Security shows each key
  servers wait for with Use Passkey, which opens it; the network's owners are notified once when one starts
  waiting (`check`). Open it on their screen, don't pass it on: nobody but the person hands a key over.
- `username` changes your person's username, which their addresses are under (`users/<username>`,
  `/git-repos/<username>/notes`), when they ask, or with `--who` someone else's, which only the network's owners do:
  lowercase letters, digits, dots and hyphens. Everything of theirs moves with it, and their old addresses, sharing
  links, webhooks and git remotes lead to the new one, as GitHub's do; nobody else is given an old one.
- `people` says who people are: the name each goes by, chosen as they joined, their email where signing in
  has one, and whose picture they're shown by (`picture`: the one they set, `own`, or Google's, `google`, or none). `name` changes the name your person goes by, when they ask. `picture` sets the picture they go by, which wins over Google's (`--upload-from photo.jpg`: any picture up to 10 MB, made square and small from its middle), and with none takes it away. Signing in with Google gives
  their Google picture, taken again each time. `pictures` gives those of people (`users/<name>`) and the network (`network`, its icon, or the One App's) as `data:` addresses, which
  the UI library's `Avatar` draws, with a person's initials where they have none. A group (`groups/<name>`) has none: it gives up to four of its members, those with a picture first, and their pictures, which `Avatar` draws together. `everyone` lists everyone in the network
  and everyone invited who hasn't joined yet. `remove_person` takes someone out, or ends an invitation: their
  devices, assistants and passkeys stop working, they're in no group and shared nothing, and what they made stays. Whoever invites does it.
- A device that isn't in yet shows a code and a link at the network's address. Its person opens the link where
  they sign in, with a passkey or Google, on the device or any device of theirs, and says whether the code there
  matches. Pass both on as they are: the code is what keeps a stranger's device out. A device signed in reaches
  what's unencrypted at once, and what's encrypted once their passkey lets it hold the key.
- `approve` lets that device in yourself, as the person you act for, with no tap from them: when a device shows a
  code and they've asked for that device to be let in, call it with the code, and say which device it let in by
  the name it answers. Never let in a device nobody asked for, or one whose code came from anyone but your person
  or the device they asked about: a code someone sends you could be a stranger's. After five codes no device
  shows, it refuses for a quarter of an hour.
- Letting something in, and taking it out, are a person's decisions. Do them when asked to, and say what you
  did.
