---
name: soft-delete
description: Read when someone wants back something they deleted, asks what they deleted, or before an app deletes something a person made.
metadata:
  title: "Recently Deleted"
  subtitle: "Restore what you deleted"
  about: "Keeps what's deleted for 30 days, then deletes it for good. Restore anything before then, even an app you uninstalled, with what it kept."
  category: Utilities
---

Soft delete keeps what's deleted for 30 days, as it was, and then purges it for good. People see it as Recently
Deleted. Anything an app made for someone is named by where it is, like `users/alice/made/git-repos/notes`, and its
owner deletes and restores it.

Its words: an item is **deleted** for 30 days, **purging** while it's being deleted for good, then **purged**. A
restored one is **active** again.

- `list` lists what you own that's deleted, the latest first: each item's artifacts, who deleted it, and when it's
  purged. For a group's things, ask for the group (`ONE_SUBJECT=groups/<name>`).
- `restore --item <id>` restores one as it was. Where something new was made at its name since, it's restored beside
  it as `notes-2` (then `notes-3`), and the answer says where. One whose app isn't installed is restored anyway and
  opens once the app is installed again.
- `delete --artifact <name>` deletes one. An app's own way of deleting, such as `git-repos remove`, does the same and
  keeps its own list true, so use the app's when it has one. Delete only when asked.
- An app someone deployed is deleted the same way, by its artifact (`users/alice/apps/notes`), once nobody has
  it installed: `uninstall` it for everyone first. It's gone from the App Store's Marketplace until it's restored.
- Uninstalling an app deletes what it kept and made for whoever it was installed for, as one item. Restoring that
  item installs the app again with all of it, and is the only way an uninstalled app comes back. Purging it removes
  the app for good with all of it. What was deleted before the uninstall stays its own item.
- `purge --item <id>` deletes one for good now, and `purge_all` everything you own. Only when asked: neither can be
  undone.
- `expire` is the clock's, each day: don't call it yourself.

An app deletes what someone asked it to delete with `OneCore.Call.tool(call, "soft-delete", "delete",
%{"artifact" => name})`, never blob by blob, so it can be restored. One that keeps a list of what it made hooks into
`soft-delete.moved`, the hook this app offers, which says each time one moved to another state, and keeps its
list true from it. On `purging` the item is at its name again, nothing erased yet, for the app that made it to read
once more, as one does to revoke a token. An app that fails that hook holds the purge back a day, once.
