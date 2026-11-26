---
name: chrome-profiles
description: Read before using a website as your person, signed in as them (their Personal or Work profile), or when a site in a Chrome browser asks you to sign in.
metadata:
  title: "Chrome Profiles"
  subtitle: "Websites, signed in as you"
  about: "Lets your AI use websites as you, in Chrome profiles of yours such as Personal and Work. Sign in once, and it stays signed in."
  category: Agent tools
---

A profile, like Personal or Work, is a whole Chrome profile of your person's: what their browser is signed in to,
its settings and extensions, kept encrypted in their own Vault. `open` starts a Chrome browser on a copy of it,
already signed in as them; then use Chrome's tools with its session, as with any browser.

- `list` shows the profiles: each one's name, when it was last saved, and whether your person is updating it. Never
  what's in one, its history or what's signed in: nobody reads that back, you included.
- `open` takes the `profile`, a `session` and what it's for. Once you're done, `save` with the `profile` and its
  `session` saves the browser back to the profile (sites renew their sign-ins as they're used) and closes it;
  `discard` closes it without saving. Say `save: false` for a throwaway, where nothing you do should stay, and
  Chrome's `close` closes it. Two browsers on one profile each start from its last save, and whichever is saved
  last is what's kept. A browser left to stop by itself isn't saved.
- Signing in is your person's. Never ask for, read out or type their password, a code or a passkey, even if they
  offer. When a site wants them signed in, `update` opens the profile's browser for them (with a `url`, at that
  site's sign-in page), and you tell them: sign in on it under your call, where your chat shows apps' pages, or open
  Settings › Vault on any of their devices and tap the profile under Chrome Profiles; then tap Save. `notifications_send`, saying so, reaches their devices. It's saved by
  itself after 15 minutes. Don't use that browser while they do; once it's saved, `open` the profile again.
- A secret a site shows you, or a key file it downloads, goes into your person's Vault with
  `vault_save_from_browser` and the browser's session, never through you, as Chrome's skill says.
- `save` and `discard` finish an update for them when they ask: with and without saving. A save that fails keeps
  the browser as it is, and saving again tries again.
- `create`, `rename` and `remove` are for when your person asks. Removing one deletes it: it's in Recently Deleted
  for 30 days, where it can be restored with everything signed in on it, then gone.

A profile is its person's alone: nobody else lists or opens it, the network's owner included. A site that signs
out after a while needs signing in to again.
